from django.contrib import admin
from .models import *
import admin_thumbnails
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .form import ProductImageForm

# Register your models here.

@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1
    fk_name = 'product'


@admin_thumbnails.thumbnail('image')
class ProductGalleryAdmin(admin.ModelAdmin):
    list_display = ['product','image','image_thumbnail']

class ProductAdmin(admin.ModelAdmin):
    list_display  = ('product_name', 'price', 'category','modified_date', 'is_available')
    list_filter = ['category']
    readonly_fields = ('image_tag',)
    prepopulated_fields = {'slug':('product_name',) }
    inlines = [ProductGalleryInline]

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','size','stock','price','is_active')
    list_editable = ('is_active',)
    list_filter = list_display = ('product','size','is_active')


admin.site.register(Product,ProductAdmin)    
admin.site.register(ProductGallery,ProductGalleryAdmin) 
admin.site.register(Variation,VariationAdmin)
