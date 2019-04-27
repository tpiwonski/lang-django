from django.views.generic import TemplateView


class ComponentContext(object):
    context_classes = []

    def get_context(self, request, *args, **kwargs):
        context = {}
        for context_class in self.context_classes:
            context.update(context_class().get_context(self.request, **kwargs))

        return context


class ComponentView(ComponentContext, TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_context(self.request, **kwargs))
        return context
