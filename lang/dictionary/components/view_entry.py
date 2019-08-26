from django import template

register = template.Library()


@register.inclusion_tag('dictionary/components/view_entry.html')
def view_entry(entry):
    return {
        'entry': entry
    }
