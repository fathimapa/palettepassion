from django.db import models
from accounts.models import *
from store.models import *
from django_countries.fields import CountryField
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.

class Address(models.Model):
    user          = models.ForeignKey(Account,on_delete=models.CASCADE)
    first_name    = models.CharField(max_length = 50)
    last_name     = models.CharField(max_length = 50)
    phone         = models.CharField(max_length = 15)
    email         = models.EmailField(max_length = 50)
    address_line1 = models.CharField(max_length=50)
    address_line2 = models.CharField(max_length=50,null=True)
    state         = models.CharField(max_length=50)
    country       = CountryField()
    city          = models.CharField(max_length=50,blank=True)
    zipcode       = models.CharField(max_length=20)
    order_note    = models.CharField(max_length=100, blank=True)
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def address(self):
        return f"{self.address_line1} {self.address_line2}"

    def __str__(self):
        return self.first_name
    
class Payment(models.Model):
    user           = models.ForeignKey(Account,on_delete=models.CASCADE)
    payment_id     = models.CharField(max_length=100)
    order_id       = models.CharField(max_length=100,blank=True,default='empty')
    payment_method = models.CharField(max_length=100)
    amount_paid    = models.FloatField(default=0)
    status         = models.CharField(max_length=100)
    created_at     = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.payment_id
    

class Order(models.Model):
    STATUS = (
        ('Order_Confirmed', 'Order Confirmed'),
        ('Shipped',"Shipped"),
        ('Out_for_delivery',"Out for delivery"),
        ('Delivered', 'Delivered'),
        ('Cancelled','Cancelled'),
        ('Returned','Returned'),
    )
    user           = models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)
    payment        = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    order_number   = models.CharField(max_length=20)
    first_name     = models.CharField(max_length=50)
    last_name      = models.CharField(max_length=50)
    phone          = models.CharField(max_length=15)
    email          = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50,blank=True)
    country        = CountryField()
    state          = models.CharField(max_length=50)
    city           = models.CharField(max_length=50)
    order_note     = models.CharField(max_length=100,blank=True)
    zipcode        = models.CharField(max_length=20,default=1)
    order_total    = models.FloatField()
    order_discount = models.FloatField(default=0)
    tax            = models.FloatField()
    status         = models.CharField(max_length=50,choices=STATUS,default='Order Confirmed')
    ip             = models.CharField(blank=True,max_length=20)
    is_ordered     = models.BooleanField(default=False)
    is_returned    = models.BooleanField(default=False)
    return_reason  = models.CharField(max_length=50, blank=True)
    created_at     = models.DateField(auto_now_add=True)
    updated_at     = models.DateField(auto_now=True)
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'

    def __str__(self):
        return self.first_name 
    
class OrderProduct(models.Model):
    order         = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='user_order_page')
    payment       = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    user          = models.ForeignKey(Account,on_delete=models.CASCADE)
    product       = models.ForeignKey(Product,on_delete=models.CASCADE)
    variations    = models.ForeignKey(Variation,on_delete=models.CASCADE,default=0)
    quantity      = models.IntegerField()
    product_price = models.FloatField()
    ordered       = models.BooleanField(default=False)
    created_at    = models.DateField(auto_now_add=True)
    updated_at    = models.DateField(auto_now=True)

    def __str__(self):
        return self.product.product_name
    def sub_total(self):
        return self.product.get_product_price_by_size_id(self.variations.pk) * self.quantity
    

class Coupon(models.Model):
    code       = models.CharField(max_length= 50, unique= True)
    discount   = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(30)])
    min_value  = models.IntegerField(validators=[MinValueValidator(0)])
    valid_from = models.DateTimeField(auto_now_add= True)
    valid_to   = models.DateField()
    active     = models.BooleanField(default= False)

    def __str__(self):
        return self.code
    
class UserCoupon(models.Model):
    user      = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    coupon    = models.ForeignKey(Coupon,on_delete=models.CASCADE,null=True)
    order     = models.ForeignKey(Order,on_delete=models.CASCADE,null=True,related_name='order_coupon')
    used      = models.BooleanField(default= False)

    def __str__(self):
        return str(self.id)