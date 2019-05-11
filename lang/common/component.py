from django.views.generic import TemplateView, View
from django.shortcuts import redirect, render


class ComponentContext(object):
    context_classes = []

    def build_context(self, request, *args, **kwargs):
        context = {}
        for context_class in self.context_classes:
            context.update(context_class().build_context(request, **kwargs))

        context.update(self.get_context(request, *args, **kwargs))
        return context

    def get_context(self, request, *args, **kwargs):
        return {}


class ComponentView(ComponentContext, View):
    page_template = None
    fragment_template = None

    def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        context = {}
        context.update(self.build_context(self.request, **kwargs))
        context.update(self.get_context(self.request, **kwargs))
        return context

    def render_page(self, context, **kwargs):
        if not context:
            context = self.get_context_data(**kwargs)
        else:
            context.update(self.get_context_data(**kwargs))

        return render(self.request, self.page_template, context)
    
    def render_fragment(self, context, **kwargs):
        if not context:
            context = self.get_context_data(**kwargs)
        else:
            context.update(self.get_context_data(**kwargs))

        return render(self.request, self.fragment_template, context)
