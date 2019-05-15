from django.utils import timezone

from lang.common.component import ComponentView, ComponentContext


class CurrentDateContext(ComponentContext):

    def get_context(self, request, *args, **kwargs):
        return {
            'current_date': timezone.now()
        }


class CurrentDateView(ComponentView):
    fragment_id = 'current-date'
    fragment_template = 'dictionary/fragments/current_date.html'
    context_classes = [CurrentDateContext]

    def get(self, request, *args, **kwargs):
        return self.render_fragment({}, **kwargs)
