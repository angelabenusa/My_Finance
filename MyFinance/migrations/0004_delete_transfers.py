# Generated by Django 4.2.6 on 2023-12-20 19:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MyFinance', '0003_rename_amount_transfers_value'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Transfers',
        ),
    ]
