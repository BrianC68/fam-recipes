from django.shortcuts import render, redirect
from django.views.generic import TemplateView


def handler404(request, exception, template_name='404.html'):
    response = render(request, template_name)
    response.status_code = 404
    return response

def handler500(request, template_name='500.html'):
    response = render(request, template_name)
    response.status_code = 500
    return response


class HomePageTemplateView(TemplateView):
    '''View displays the home page.'''

    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('recipes:recipes-index')
        else:
            return super().get(request, *args, **kwargs)
