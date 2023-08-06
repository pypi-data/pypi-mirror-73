import os
from django.template.loader import render_to_string
from django import template
from distutils.sysconfig import get_python_lib

PYTHON_PATH = os.path.abspath(
    os.path.join(os.path.abspath(__file__),
        "../.."
    )
)
BASE_DIR = os.path.join(PYTHON_PATH, 'templates')

register = template.Library()

@register.filter(name='paginator')
def paginator(object_list, style=None):
    path = os.path.join(BASE_DIR, 'paginator.html')
    html = render_to_string(
        path,
        {
            'obj_list': object_list,
            'style': style
        }
    )

    return html
