from __future__ import unicode_literals

import os
import uuid

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.template.defaultfilters import truncatechars
from django.utils.datetime_safe import datetime
from django.contrib.auth.models import User



def user_directory_path(self, filename):
    filename, file_extension = os.path.splitext(filename)
    return './documents/{0}/{1}{2}'.format(self.location,
                                           self.slug, file_extension)


class File(models.Model):
    author = models.ForeignKey(to=User, blank=False)
    name = models.CharField(max_length=100, blank=False, null=True)
    file = models.FileField(upload_to=user_directory_path, null=True)
    date = models.DateTimeField(default=datetime.now, blank=False, null=True, editable=True)
    slug = models.SlugField(default=uuid.uuid1, unique=True, editable=False)
    location = models.CharField(max_length=50, default="articolFiles")

    @property
    def filename(self):
        return os.path.basename(self.file.url)

    def fileLink(self):
        if self.file:
            return '<a href="' + "/download/" + str(self.slug) + '">' + "Download file" + '</a>'
        else:
            return '<a href="''"></a>'

    fileLink.allow_tags = True
    fileLink.short_description = "Download"

    def __unicode__(self):
        return "File %s from %s" % (self.filename, self.author.username)

    @property
    def short_name(self):
        return truncatechars(self.name, 40)

    class Meta:
        abstract = True
        get_latest_by = 'date'
        verbose_name = 'File'
        verbose_name_plural = 'Files'


class Post(File):
    def __init__(self, *args, **kwargs):
        self._meta.get_field('location').default = "articolFiles"
        super(Post, self).__init__(*args, **kwargs)

    REQUIRED = ['name', 'file']

    class Meta(File.Meta):
        abstract = False
        get_latest_by = 'date'
        verbose_name = 'File'
        verbose_name_plural = 'Files'


@receiver(pre_delete, sender=Post)
def file_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)
