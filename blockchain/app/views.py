from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View



class Index(View):
    # initial = {'key': 'value'}
    template_name = 'website/index.html'

    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        return render(request, self.template_name)
