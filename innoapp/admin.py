from django.contrib import admin

from innoapp.models import Tag, Page, Post


class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class PageAdmin(admin.ModelAdmin):
    list_display = ('name', 'uuid', 'is_private', 'unblock_date')
    list_display_links = ('name', 'uuid')
    list_editable = ['is_private']


class PostAdmin(admin.ModelAdmin):
    list_display = ('content', 'created_at', 'updated_at')
    list_display_links = ['content']


admin.site.register(Tag, TagAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Post, PostAdmin)
