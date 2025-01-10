from django.contrib import admin
from .models import InventoryItem
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


# Registering the InventoryItem model with custom admin settings
@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'price', 'category', 'managed_by', 'date_added', 'last_updated')
    list_editable = ('quantity', 'price', 'category')
    search_fields = ('name', 'category')
    list_filter = ('category', 'date_added')
    ordering = ('-date_added',)


# Extending the default UserAdmin to customise the user management view
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')


# Unregistering the default User admin to replace it with the custom one
admin.site.unregister(User)


# Registering the User model with the custom admin settings
admin.site.register(User, CustomUserAdmin)
