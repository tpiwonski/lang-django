import json

from django.views.generic import TemplateView, View
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.http import HttpResponse


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
    fragment_id = None
    page_template = None
    fragment_template = None
    context_classes = []
    component_classes = []

    def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        context = {}
        context.update(self.build_context(self.request, **kwargs))
        context.update(self.get_context(self.request, **kwargs))
        return context

    def render(self, context, **kwargs):
        if not context:
            context = self.get_context_data(**kwargs)
        else:
            context.update(self.get_context_data(**kwargs))

        if self.request.GET.get('ic-request') or self.request.POST.get('ic-request'): 
            content = {
                self.fragment_id: render_to_string(self.fragment_template, context, self.request)
            }
            for component in self.component_classes:
                content[component.fragment_id] = render_to_string(component.fragment_template, context, self.request)
            
            return HttpResponse(json.dumps(content), content_type="application/json")
        else:
            return render(self.request, self.page_template, context)    

    #     return render(self.request, template, context)

    def render_page(self, context, **kwargs):
        if not context:
            context = self.get_context_data(**kwargs)
        else:
            context.update(self.get_context_data(**kwargs))

        return render(self.request, self.page_template, context)

    # def render_fragment(self, context, **kwargs):
    #     if not context:
    #         context = self.get_context_data(**kwargs)
    #     else:
    #         context.update(self.get_context_data(**kwargs))

    #     return render(self.request, self.fragment_template, context)

    def render_fragment(self, context, **kwargs):
        if not context:
            context = self.get_context_data(**kwargs)
        else:
            context.update(self.get_context_data(**kwargs))

        content = {
            self.fragment_id: render_to_string(self.fragment_template, context, self.request)
        }
        for component in self.context_classes:
            content[component.fragment_id] = render_to_string(component.fragment_template, context, self.request)
        
        return HttpResponse(json.dumps(content), content_type="application/json")

    # def render_response(self, context, templates, **kwargs):
    #     context.update(self.get_context_data(**kwargs))
    #     content = {}
    #     for name, template in templates.items():
    #         content[name] = render_to_string(template, context, self.request)
        
    #     return HttpResponse(json.dumps(content), content_type="application/json")
