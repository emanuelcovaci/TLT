from django.contrib import admin
from .models import Activity
from .forms import ActivityCreationFormAdmin, ActivityChangeFormAdmin



class ActivityAdmin(admin.ModelAdmin):
    add_form = ActivityCreationFormAdmin
    change_form = ActivityChangeFormAdmin
    icon = '<i class="material-icons">rss_feed</i>'

    list_display = ('author', 'name', 'slug',)

    fieldsets = ()
    change_fieldsets = (
        ('Activity', {'fields': ('name', 'author','date',)}),
        ('Activity content', {'fields': ('text', 'file')})
    )

    add_fieldsets = (
        ('Activity', {'fields': ('name','date',)}),
        ('Activity content', {'fields': ('text', 'file')})
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
            return form

    pass


admin.site.register(Activity,ActivityAdmin)
