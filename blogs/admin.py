from django.contrib import admin
from .models import Category,Blog
# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)} # autoamatically generate text based on the specific attribute


admin.site.register(Category)
admin.site.register(Blog, BlogAdmin)