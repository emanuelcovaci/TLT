from django.contrib.admin.filters import DateFieldListFilter
from django.contrib import admin
from event.forms import EventChangeFormAdmin, EventCreationFormAdmin
from models import Event



class EventAdmin(admin.ModelAdmin):
    add_form = EventCreationFormAdmin
    change_form = EventChangeFormAdmin
    change_own_field = "author__id"
    change_own_owner_field = "id"

    icon = '<i class="material-icons">room</i>'

    list_display = ('name', 'author', 'address', 'date', 'slug',)
    list_filter = (
        ('date', DateFieldListFilter),
    )
    readonly_fields = ['author']
    
    search_fields = ('name', 'author__first_name', 'author__last_name', 'address', 'date',)

    ordering = ['date']
    filter_horizontal = ()
    
    change_fieldsets = (
        ('Event Info', {'fields': ('name', 'author')}),
        ('Event Description', {'fields': ('text', 'file')}),
        ('Location and Time', {'fields': ('date', 'address', 'geolocation')}),
    )
    
    add_fieldsets = (
        ('Event Info', {'fields': ('name', )}),
        ('Event Description', {'fields': ('text', 'file')}),
        ('Location and Time', {'fields': ('date', 'address', 'geolocation')}),
    )

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            self.fieldsets = self.add_fieldsets
            form = self.add_form
            form.current_user = request.user
            return form
        else:
            self.fieldsets = self.change_fieldsets
            form = self.change_form
            form.text_initial = obj.text
            form.date_initial = obj.date
            form.address_initial = obj.address
            form.geolocation_initial = obj.geolocation
            return form
    
    pass

admin.site.register(Event,EventAdmin)