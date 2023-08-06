import os
from django.template.loader import render_to_string
from django import template
from distutils.sysconfig import get_python_lib

BASE_DIR = os.path.join(get_python_lib(), '/leafage/',  'templates')
register = template.Library()

@register.filter(name='pagination')
def pagination(object_list, style=None):
    path = os.path.join(BASE_DIR, 'paginator.tpl')
    html = render_to_string(
        path,
        {
            'obj_list': object_list
        }
    )

    return html
