# Generated by Django 5.1.6 on 2025-03-04 19:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0005_alter_purchaserequest_customer'),
        ('users', '0005_purchase_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='trader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.trader'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.customer'),
        ),
    ]
