from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage

s3_storage = S3Boto3Storage()
# Create your models here.

class Banner(models.Model):
    banner_name = models.CharField(max_length=100)
    banner = models.FileField(upload_to='photos/banners/',null=True, blank=True)
    url = models.URLField(blank=True,default='#')
    button_text = models.CharField(max_length=10,default='Buy Now')
    order = models.PositiveIntegerField ( default=0 ) 
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.banner_name