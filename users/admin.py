from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'type', 'first_name', 'is_active', 'is_superuser', 'is_staff')
    list_editable = ('is_active', 'type')
    paginate_by = 20
