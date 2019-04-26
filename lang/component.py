from django.views.generic import TemplateView


class ComponentView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_context(self.request, **kwargs))
        return context


class ComponentContext(object):
    
    def get_context(self, request, **kwargs):
        return {}
