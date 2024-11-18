from django.contrib import admin

from beauty.models.region import Address
from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'username', 'email', 'phone', 'address', 'is_active', 'is_staff', 'is_master')
    search_fields = ('full_name', 'username', 'email', 'phone')
    ordering = ('-id',)


admin.site.register(User, UserAdmin)

admin.site.register(Address)
