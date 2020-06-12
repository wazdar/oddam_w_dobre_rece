from django.contrib import admin

from .models import Institution, Category, Donation
# Register your models here.
admin.site.register(Institution)
admin.site.register(Category)
admin.site.register(Donation)