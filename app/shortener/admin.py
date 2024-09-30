"""
Django admin customization
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from shortener import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users"""
    ordering = ['id']
    list_display = ['email', 'is_active', 'is_staff', 'is_superuser']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),   # This is kind of CSS styling
            'fields': (
                'email',
                'password1',
                'password2',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )


class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'original_url', 'full_short_url', 'times_accessed', 'user', 'created_at')
    search_fields = ('original_url', 'short_url')
    list_filter = ('created_at', 'user')
    exclude = ('short_url', 'times_accessed')

    def full_short_url(self, obj):
        return 'https://helguera.link/{}'.format(obj.short_url)
    
    full_short_url.short_description = 'Short URL'

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Link, LinkAdmin)