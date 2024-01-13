# Generated by Django 4.2.7 on 2023-12-11 06:52

from django.db import migrations, models
import storages.backends.s3


class Migration(migrations.Migration):

    dependencies = [
        ('banner_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='image',
            field=models.ImageField(blank=True, null=True, storage=storages.backends.s3.S3Storage(), upload_to='banner/images/'),
        ),
    ]
