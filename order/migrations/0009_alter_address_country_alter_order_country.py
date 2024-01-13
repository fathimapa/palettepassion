# Generated by Django 4.2.5 on 2023-11-27 13:08

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_alter_order_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='country',
            field=django_countries.fields.CountryField(max_length=255),
        ),
        migrations.AlterField(
            model_name='order',
            name='country',
            field=django_countries.fields.CountryField(max_length=255),
        ),
    ]
