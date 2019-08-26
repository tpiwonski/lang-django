from django import template

register = template.Library()


@register.inclusion_tag('dictionary/components/entry_list_item.html')
def entry_list_item(entry):
    return {
        'entry': entry
    }
