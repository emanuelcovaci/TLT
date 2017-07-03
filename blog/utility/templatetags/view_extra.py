
from django import template

from file.models import Post

register = template.Library()


@register.assignment_tag
def get_files():
    return Post.objects.filter(location="articolFiles")
