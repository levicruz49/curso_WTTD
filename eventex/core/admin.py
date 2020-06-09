from django.contrib import admin
from django.utils.html import format_html

from eventex.core.models import Speaker, Contact, Talk


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 1

class SpeakerModelAdmin(admin.ModelAdmin):
    inlines = [ContactInline]
    prepopulated_fields = {'slug':('name',)}
    list_display = ['name', 'website_link', 'photo_img', 'email', 'phone']

    def website_link(self, obj):
        return format_html('<a target="_blank" href="{0}">{0}</a>'.format(obj.website))

    def photo_img(self, obj):
        return format_html('<img target="_blank" width="32px" src="{}" />'.format(obj.photo))

    def email(self, obj):
        return obj.contact_set.emails().first()

    def phone(self, obj):
        return obj.contact_set.phones().first()

    email.short_description = 'E-mail'
    phone.short_description = 'Telefone'
    website_link.short_description = 'WebSite'
    photo_img.short_description = 'Foto'

admin.site.register(Speaker, SpeakerModelAdmin)
admin.site.register(Talk)