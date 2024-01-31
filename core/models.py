from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from accounts.models import *
from store.models import *

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    subject = models.CharField(max_length = 300)
    message = models.TextField()
    
@receiver(post_save, sender=Contact)
def _post_save_receiver(sender, instance, **kwargs):
    subject = 'Your 6-digit OTP for email verification'
    message = f'{instance.message}'
    from_email = instance.email 
    recipient_email =  'fathimagm0@gmail.com'
    recipient_list = [recipient_email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

class RecentViewedProduct(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE , related_name='recent_viewed_product')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Get the total count of rows in the table
        total_rows = RecentViewedProduct.objects.filter(user=self.user).count()

        # If the user already has 10 rows, delete the oldest row before adding the new one
        if total_rows >= 7:
            oldest_row = RecentViewedProduct.objects.filter(user=self.user).order_by('updated_at').first()
            oldest_row.delete()

        # Call the parent class's save method to save the new row
        super(RecentViewedProduct, self).save(*args, **kwargs)
        
        

    def __str__(self):
        return self.user.first_name+" "+self.product.product_name()