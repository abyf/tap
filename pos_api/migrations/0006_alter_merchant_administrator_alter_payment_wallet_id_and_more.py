# Generated by Django 4.1.5 on 2023-04-19 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pos_api', '0005_alter_cardholder_administrator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchant',
            name='administrator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pos_api.administrator', verbose_name='Created_by'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='wallet_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos_api.merchant', to_field='wallet_id', verbose_name='To_Merchant'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='administrator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pos_api.administrator', verbose_name='Performed_by'),
        ),
    ]
