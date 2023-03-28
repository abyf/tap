from django import forms
from .models import Payment, CardHolder, Merchant, Transaction
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from .serializers import PaymentSerializer
from decimal import Decimal
from django.db.models import Q, F
from django.db import transaction

class PaymentForm(forms.ModelForm):
    #card_info = forms.CharField(label='Card ID or QR code', max_length=100, required=True,widget=forms.TextInput(attrs={'size':'30'}))

    class Meta:
        model = Payment
        fields = ('amount','card_id','qr_code','wallet_id')

        widgets = {
                'amount': forms.NumberInput(attrs={'size':'30'}),
                'card_id': forms.TextInput(attrs={'size':'30'}),
                'qr_code': forms.TextInput(attrs={'size':'30'}),
                'wallet_id': forms.HiddenInput(),
           }
        error_messages = {
           'card_info': {'invalid_choice': 'User does not exist!!!'}
           }

    def clean_card_info(self):
        serializer = PaymentSerializer(data=self.cleaned_data)
        card_id = serializer.data['card_id']
        qr_code = serializer.data['qr_code']
        if not card_id and not qr_code:
            raise forms.ValidationError('Either a QR_code or CARD_ID is required!')

        try:
            #cardholder = CardHolder.objects.get(Q(card_id=card_id)|Q(qr_code=qr_code))
            if card_id:
                cardholder = CardHolder.objects.get(card_id=card_id)
            else:
                cardholder = CarHolder.objects.get(qr_code=qr_code)
        except CardHolder.DoesNotExist:
            raise forms.ValidationError('Customer not found !!!')
        return cardholder

    @transaction.atomic    #Wrapping the transaction in an atomic block to ensure that all database operations are rolled back if an error occurs
    def charge_and_credit(self,merchant):
        serializer = PaymentSerializer(self.cleaned_data)
        card_id = serializer.data['card_id']
        qr_code = serializer.data['qr_code']
        amount = Decimal(serializer.data['amount'])

        try:
            #Using the select_for_update method to lock the CarHolder record during the transaction to prevent concurrent access and updates to the same record.
            cardholder = CardHolder.objects.select_for_update().get(Q(card_id=card_id)|Q(qr_code=qr_code))
        except CardHolder.DoesNotExist:
            raise ValueError('Customer not found!!!: Please enter a valied card ID or QR code')
        if amount <= 0 :
            raise ValueError('Invalid amount: Please enter the correct amount')
        if cardholder.balance < amount:
            raise ValueError('Insufficient funds, Please charge your card!!!')

       # Updating CardHolder and Merchant fields using F expressions to avoid race conditions
        cardholder.balance = F('balance') - amount
        cardholder.save()
        merchant.balance = F('balance') + amount
        merchant.save()

        payment = self.save(commit=False)
        payment.merchant_id = merchant
        payment.cardholder_id = cardholder
        payment.save()

        Transaction.objects.create(cardholder_id=cardholder, amount=amount,merchant_id=merchant,message=f'Payment of {amount} to {merchant} is successful')

class MerchantAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self,user):
        if not user.is_active:
            raise forms.ValidationError(self.error_messages['inactive'],code='inactive',)
        try:
            merchant = Merchant.objects.get(user=user)
        except Merchant.DoesNotExist:
            raise forms.ValidationError('Merchant Not Found!!!',code='invalid_login',)
        super().confirm_login_allowed(user)
