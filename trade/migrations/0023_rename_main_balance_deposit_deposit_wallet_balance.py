# Generated by Django 5.0.7 on 2024-07-13 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0022_pin'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deposit',
            old_name='main_balance',
            new_name='deposit_wallet_balance',
        ),
    ]