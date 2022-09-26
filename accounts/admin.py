from django.contrib import admin

from accounts.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'title', 'is_blocked')
    list_display_links = ('email', 'title')
    list_editable = ('role', 'is_blocked')


admin.site.register(User, UserAdmin)
