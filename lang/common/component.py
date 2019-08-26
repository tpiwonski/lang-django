import json

from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import View


class ComponentView(View):
    fragment_id = None
    page_template = None
    fragment_template = None

    def render(self, context, **kwargs):
        if self.request.GET.get('ic-request') or self.request.POST.get('ic-request'):
            content = {
                self.fragment_id: render_to_string(self.fragment_template, context, self.request)
            }
            return HttpResponse(json.dumps(content), content_type="application/json")
        else:
            return render(self.request, self.page_template, context)
