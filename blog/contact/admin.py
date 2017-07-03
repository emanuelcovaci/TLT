from django.contrib import admin
from .models import ContactUs

class ContactAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">contact_mail</i>'
admin.site.register(ContactUs,ContactAdmin)