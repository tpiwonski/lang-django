from django import forms
from django.views.generic.base import View
from django.views.generic.base import TemplateResponseMixin
from django.shortcuts import redirect

from lang.common.component import ContextMixin
from lang.dictionary.controllers import AddTranslation
from lang.dictionary.views.current_date import CurrentDateContext


class AddTranslationForm(forms.Form):
    entry = forms.CharField(max_length=255)
    translations = forms.CharField()


class AddTranslationView(ContextMixin, TemplateResponseMixin, View):
    template_name = 'dictionary/pages/add_translation.html'
    add_translation_controller = AddTranslation()
    context_classes = [CurrentDateContext]

    def get(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context['form'] = AddTranslationForm()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = AddTranslationForm(request.POST)
        if not form.is_valid():
            return self.render_to_response({
                'form': form
            })

        entry = {
            'text': form.cleaned_data['entry'],
            'language': 'en'   
        }
        translations = []
        for translation in [t.strip() for t in form.cleaned_data['translations'].split(';')]:
            translations.append({
                'text': translation,
                'language': 'pl'
            })
        
        self.add_translation_controller.execute(entry, translations)
        return redirect('entry-list')
