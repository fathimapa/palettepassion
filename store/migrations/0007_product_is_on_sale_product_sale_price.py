# Generated by Django 4.2.7 on 2023-12-13 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_productgallery_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_on_sale',
            field=models.BooleanField(default=False, help_text='Is the product currently on sale?'),
        ),
        migrations.AddField(
            model_name='product',
            name='sale_price',
            field=models.IntegerField(blank=True, help_text='Discounted price for the product', null=True),
        ),
    ]
