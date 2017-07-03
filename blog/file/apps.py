from __future__ import unicode_literals

from django.apps import AppConfig

from material.frontend.apps import ModuleMixin


class FileConfig(ModuleMixin, AppConfig):
    name = 'file'
    label = "file"

    verbose_name = "Files"
    icon = '<i class="material-icons">description</i>'
