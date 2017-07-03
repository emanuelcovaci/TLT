from django.contrib.admin.filters import (ChoicesFieldListFilter,
                                          DateFieldListFilter)

from models import Post
from .forms import (PostChangeFormAdmin, PostCreationFormAdmin)
from django.contrib import admin


class PostAdmin(admin.ModelAdmin):
    change_form = PostChangeFormAdmin
    add_form = PostCreationFormAdmin

    add_form_template = "admin/add_files_form.html"

    icon = '<i class="material-icons">description</i>'

    list_display = ('author', 'fileLink', 'location', 'date', 'slug',)
    readonly_fields = ['fileLink', 'author', 'location']

    fieldsets = ()
    change_fieldsets = (
        ('File', {'fields': ('name', 'author', ('file', 'location'))}),
    )

    add_fieldsets = (
        ('File', {'fields': ('name', 'file')}),
    )

    search_fields = ('name', 'date', 'slug',)

    ordering = ['date']
    filter_horizontal = ()

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            self.fieldsets = self.add_fieldsets
            form = self.add_form
            form.current_user = request.user
            return form
        else:
            self.fieldsets = self.change_fieldsets
            return self.change_form

admin.site.register(Post,PostAdmin)