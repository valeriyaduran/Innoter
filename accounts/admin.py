from django.contrib import admin

from accounts.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'username', 'is_blocked')
    list_display_links = ('email', 'username')
    list_editable = ('role', 'is_blocked')


admin.site.register(User, UserAdmin)
