# Generated by Django 4.1.5 on 2023-03-31 08:34

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('pos_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=120, unique=True)),
                ('name', models.CharField(max_length=120)),
                ('phone', models.CharField(max_length=120, unique=True)),
                ('email', models.EmailField(max_length=120)),
                ('cardholder_commission', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('merchant_commission', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='cardholder',
            name='card_id',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, null=True, unique=True),
        ),
    ]