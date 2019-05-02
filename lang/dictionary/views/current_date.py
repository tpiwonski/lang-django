from django.utils import timezone

from lang.common.component import ComponentView, ComponentContext


class CurrentDateContext(ComponentContext):

    def get_context(self, request, *args, **kwargs):
        return {
            'current_date': timezone.now()
        }


class CurrentDateView(ComponentView):
    template_name = 'dictionary/fragments/current_date.html'
    context_classes = [CurrentDateContext]
