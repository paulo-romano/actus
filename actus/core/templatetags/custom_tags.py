from django import template
from django.template.loader import get_template

register = template.Library()


@register.simple_tag(takes_context=True)
def fields_for(context, form, template="includes/form_fields.html"):
    context["form_for_fields"] = form
    return get_template(template).render(context)