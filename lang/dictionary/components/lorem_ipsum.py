#
# class LoremIpsum(object):
#     template = 'dictionary/components/lorem_ipsum.html'
#
#     @staticmethod
#     def render(context):
#         return {
#             'text': 'lorem ipsum'
#         }


from django import template
from django.template.loader import get_template

# from lang.dictionary.components.lorem_ipsum import LoremIpsum

register = template.Library()
# register.inclusion_tag(get_template(LoremIpsum.template), takes_context=True)(LoremIpsum.render)


@register.inclusion_tag('dictionary/components/lorem_ipsum.html', takes_context=True)
def lorem_ipsum(context):
    return {
        'text': 'lorem ipsum'
    }
