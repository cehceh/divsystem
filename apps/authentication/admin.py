from django.contrib import admin
from .models import CustomUser



# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = [f.name for f in CustomUser._meta.fields]


admin.site.register(CustomUser, CustomUserAdmin)
