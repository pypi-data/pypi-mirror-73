=====
Django Leafage
=====

Simple and Easiest paginator for Django.

Installation
-----------

    pip install django-leafage


Quick start
-----------

1. Add "leafage" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'leafage',
        ...
    ]

2. In views ""import leafage" like this::

    import leafage

    def home(request):
    """
        Home page handler.
    """
    template = 'home.html'

    per_page_obj = 10 # default = 10(if not provided)

    queryset = Model.objects.all()
    queryset = leafage.pagination(request=request, obj_list=queryset, obj_count=per_page_obj)

    context = {
        'queryset': queryset
    }
    return render(request, template, context)

3.  End of template look like this.

    {% with obj_list=queryset %}
      {% include 'paginator.tpl' %}
    {% endwith %}
