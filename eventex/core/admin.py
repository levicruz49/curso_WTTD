from django.contrib import admin
from django.utils.html import format_html

from eventex.core.models import Speaker

class SpeakerModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ['name', 'website_link', 'photo_img']

    def website_link(self, obj):
        return format_html('<a target="_blank" href="{0}">{0}</a>'.format(obj.website))

    def photo_img(self, obj):
        return format_html('<img target="_blank" width="32px" src="{}" />'.format(obj.photo))

    website_link.short_description = 'WebSite'
    photo_img.short_description = 'Foto'

admin.site.register(Speaker, SpeakerModelAdmin)