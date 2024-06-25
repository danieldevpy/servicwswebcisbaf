from django.contrib import admin
from .models import Register, Archive, Setting
# Register your models here.


class AdminRegister(admin.ModelAdmin):
    pass


class AdminArchive(admin.ModelAdmin):
    pass


class AdminSettings(admin.ModelAdmin):
    pass


admin.site.register(Register, AdminRegister)
admin.site.register(Archive, AdminArchive)
admin.site.register(Setting, AdminSettings)