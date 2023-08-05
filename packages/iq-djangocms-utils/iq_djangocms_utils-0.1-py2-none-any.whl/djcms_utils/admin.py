from django.contrib import admin

from .models import CommonData

@admin.register(CommonData)
class CommonDataAdmin(admin.ModelAdmin):
    pass
