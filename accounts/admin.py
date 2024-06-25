from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, App

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('app', 'field_extra')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(App)
