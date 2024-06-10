from django.contrib import admin

from brons.models import Bron


@admin.register(Bron)
class BronAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'stadion', 'is_active', 'is_confirmed',)
    autocomplete_fields = ['user']

