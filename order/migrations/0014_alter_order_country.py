# Generated by Django 4.2.7 on 2024-01-18 15:35

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0013_alter_address_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, null=True),
        ),
    ]