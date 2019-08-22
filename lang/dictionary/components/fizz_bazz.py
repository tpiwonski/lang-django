from django import template

register = template.Library()


@register.inclusion_tag('dictionary/components/fizz_bazz.html', takes_context=True)
def fizz_bazz(context):
    return {
        'answer': '42'
    }
