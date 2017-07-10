from __future__ import unicode_literals

import os
import uuid

from django.contrib.auth.models import User

from django.db import models

# Create your models here.
from tinymce.models import HTMLField
from django.utils.datetime_safe import datetime
from gallery.models import Gallery


def user_directory_path(self, filename):
    filename, file_extension = os.path.splitext(filename)
    return './activity{0}/{1}{2}'.format('past',
                                         self.slug, file_extension)


class Activity(models.Model):
    author = models.ForeignKey(to=User, related_name='activity',
                               null=True, blank=True)
    name = models.CharField(max_length=100, blank=False, null=True)
    text = HTMLField()
    file = models.FileField(upload_to=user_directory_path, null=True)
    slug = models.SlugField(default=uuid.uuid1, unique=True, editable=False)
    date = models.DateTimeField(default=datetime.now, blank=False, null=True, editable=True)
    album = models.ForeignKey(Gallery, related_name='Gallery',
                              null=True)

    @property
    def filename(self):
        return os.path.basename(self.file.url)
