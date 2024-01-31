from django.db import models
from store.models import *
from accounts.models import *

# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length= 250 , blank= True) 
    date_added = models.DateField(auto_now_add= True)

    def __str__(self):
        return self.cart_id
    


class CartItem(models.Model,):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True)
    product = models.ForeignKey(Product , on_delete=models.CASCADE , default=0)
    cart = models.ForeignKey(Cart , on_delete=models.CASCADE)
    size_variant = models.ForeignKey(Variation , on_delete=models.SET_NULL, null= True , blank= True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default= True)

    # def __str__(self):
    #     return self.product 
    
    def sub_total(self):
        return self.product.price * self.quantity
    

class Wishlist(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add= True)
    
    def __str__(self):
        return str(self.product)