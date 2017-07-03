from __future__ import unicode_literals

from django.apps import AppConfig


class ActivityConfig(AppConfig):
    name = 'activity'
    label = "activity"

    verbose_name = "Activities"
    icon = '<i class="material-icons">grain</i>'
