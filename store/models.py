from datetime import datetime
from django.db import models
from django.urls import reverse
from category.models import category
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist




# Create your models here.


class Product(models.Model):
    product_name         = models.CharField(max_length = 200 , unique= True)
    slug                 = models.SlugField(max_length = 200, unique= False)
    product_description  = models.TextField(max_length = 500 , blank= True)
    price                = models.IntegerField()
    sale_price           = models.IntegerField(blank=True, null=True, help_text="Discounted price for the product")
    image                = models.ImageField(upload_to= 'photos/products')
    is_available         = models.BooleanField(default= True)
    category             = models.ForeignKey(category,related_name='products', on_delete= models.CASCADE)
    created_date         = models.DateTimeField(auto_now_add= True)
    modified_date        = models.DateTimeField(auto_now= True)
    is_active            = models.BooleanField(default= True)
    is_on_sale           = models.BooleanField(default=False, help_text="Is the product currently on sale?")



    def __str__(self):
        return self.product_name
    
    def get_url(self):
        return reverse('product_detail',args=[self.category.slug, self.slug])
    def save(self , *args , **kwargs):
        self.slug = slugify(self.product_name)
        super(Product ,self).save(*args , **kwargs)
    
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height ="50"/>'.format(self.image.url))
        else:
            return ""
        
    def get_product_price_by_size(self,size):
        
        try:
            size_variant = Variation.objects.filter(product=self,size=size)
            if size_variant.exists():
                # Assuming you want the price from the first matching variation
                size_variant = size_variant.first()
                return self.price + size_variant.price
            else:
                # Handle the case where no matching SizeVariant is found
                return self.price       
        except ObjectDoesNotExist:
            # Handle the case where the SizeVariant is not found
            # You might want to return a default price or handle it in another way
            return self.price
        
    def get_product_price_by_size_id(self,size):
        
        try:
            size_variant = Variation.objects.filter(product=self,pk=size)
            if size_variant.exists():
                # Assuming you want the price from the first matching variation
                size_variant = size_variant.first()
                return self.price + size_variant.price
            else:
                # Handle the case where no matching SizeVariant is found
                return self.price  
        except ObjectDoesNotExist:
            # Handle the case where the SizeVariant is not found
            # You might want to return a default price or handle it in another way
            return self.price
        
    


class VariationManager(models.Manager):
    def sizes(self):
        return self.filter(is_active=True).values_list('size',flat=True).distinct()
    
    def variations_by_size(self,size):
        return self.filter(size=size,is_active=True)
    

SIZE_CHOICES = [
    ('small','Small'),
    ('medium','Medium'),
    ('large','Large'),
    ('extralarge','Extra Large'),

]


    
class Variation(models.Model):
    product    = models.ForeignKey(Product ,on_delete=models.CASCADE) 
    size       = models.CharField(max_length=100,choices=SIZE_CHOICES)
    price      = models.DecimalField(max_digits=10,decimal_places=2)
    stock      = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now= True)
    updated_at = models.DateTimeField(auto_now_add= True)   
    is_active  = models.BooleanField(default=True)

    objects = VariationManager
    
    
    def __str__(self) -> str:
        return f" {self.size}"
    

        
    
    

class ProductGallery(models.Model):
    product = models.ForeignKey(Product , default= None , on_delete= models.CASCADE)
    image = models.ImageField(upload_to= 'photos/products' , max_length= 255)

    def __str__(self):
        return self.product.product_name
    
    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'

