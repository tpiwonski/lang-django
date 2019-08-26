from django import template

register = template.Library()


@register.inclusion_tag('dictionary/components/entry_list.html')
def entry_list(entries):
    return {
        'entries': entries
    }
