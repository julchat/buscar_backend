from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app_mvc.models import Account


class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_active')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined', 'last_password_change', 'is_admin', 'is_staff', 'is_superuser')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
