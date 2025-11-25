from django.contrib import admin
from .models import LinkCategory, Link
from django.utils.html import format_html


@admin.register(LinkCategory)
class LinkCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'description', 'color']
    list_editable = ['order', 'color']
    list_filter = ['order', 'name']
    search_fields = ['name']

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'display_icon', 'authenticated_only', 'url', 'order', 'icon_class']
    list_filter = ['category', 'authenticated_only']
    list_editable = ['order', 'category', 'authenticated_only', 'icon_class']
    search_fields = ['title', 'description', 'url']
    fieldsets = [
        (None, {
            'fields': ['title', 'url', 'description', 'category']
        }),
        ('Access Control', {
            'fields': ['authenticated_only'],
            'classes': ['collapse']
        }),
        ('Display Options', {
            'fields': ['icon_class', 'order'],
            'classes': ['collapse']
        })
    ]
    ordering = ['category__order', 'order', 'title']
    readonly_fields = ['created_at', 'updated_at']
    
    def display_icon(self, obj):
        """Display the icon with preview in admin list"""
        if obj.icon_class:
            return format_html(
                '<div style="display: flex; align-items: center; gap: 8px;">'
                '<i class="{}" style="font-size: 3.2em;"></i>'
                '<code>{}</code>'
                '</div>',
                obj.icon_class, obj.icon_class
            )
        return "-"
    display_icon.short_description = "Icon Preview"
    
    class Media:
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',
            )
        }