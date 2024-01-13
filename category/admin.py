from django.contrib import admin
from .models import category

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ('__str__','category_name', 'slug')

admin.site.register(category,CategoryAdmin)
