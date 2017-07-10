from __future__ import unicode_literals

from django.db import models
from django.db.models.fields.related import ForeignKey
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from file.models import File



class Gallery(File):
    def __init__(self, *args, **kwargs):
        self._meta.get_field('location').default = "gallery/thumbnails"
        super(Gallery, self).__init__(*args, **kwargs)

    REQUIRED = ['name', 'file']

    class Meta(File.Meta):
        verbose_name = "Gallery"
        verbose_name_plural = "Galleries"

    def __unicode__(self):
        return self.name


class GalleryPhoto(File):
    def __init__(self, *args, **kwargs):
        self._meta.get_field('location').default = "gallery/placeholder"
        super(GalleryPhoto, self).__init__(*args, **kwargs)

    gallery = ForeignKey(Gallery, null=False, blank=False, on_delete=models.CASCADE)

    REQUIRED = ['gallery', 'name', 'file']

    def __unicode__(self):
        return self.name

    class Meta(File.Meta):
        abstract = False
        verbose_name = "Gallery Photo"
        verbose_name_plural = "Gallery Photos"


@receiver(pre_delete, sender=Gallery)
@receiver(pre_delete, sender=GalleryPhoto)
def file_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)
