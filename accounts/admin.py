from django.contrib import admin
from . import models 

# Register your models here.
@admin.register(models.Profile)
class UserAdmin(admin.ModelAdmin):
    list_display = ["account_id", "email", "first_name", "last_name", "username", "phone_number", "tax_id", "is_active"]
    list_editable = ["is_active"]