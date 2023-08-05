from django.template.context import Context, RequestContext
from django.template.loader import render_to_string
from django.template.base import Template
from orionframework.middleware import get_request


def parse(template_or_name, context=None):
    """
    Parse the given template String or template name using the given context dictionary
    and return its result as a String

    @param template_or_name: the template name (if ending with *.html) or the template
    String itself

    @param context the dictionary holding additional variables

    @return: parsed template content
    """
    context = context or {}

    if template_or_name.endswith(".html") or template_or_name.endswith(".text"):

        return render_to_string(template_or_name, context=context)

    else:

        request = get_request()
        context = RequestContext(request, context) if request else Context(context)

        template_or_name = Template(template_or_name)

        return template_or_name.render(context)
