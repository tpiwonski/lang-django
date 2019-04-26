from django.utils import timezone

from lang.component import ComponentContext, ComponentView


class CurrentDateContext(ComponentContext):

    def get_context(self, request, **kwargs):
        context = super(CurrentDateContext, self).get_context(request, **kwargs)
        context['current_date'] = timezone.now()
        return context


class CurrentDateView(CurrentDateContext, ComponentView):
    template_name = 'dictionary/fragments/current_date.html'
