"""fam_recipes URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

handler404 = 'fam_recipes.views.handler404'
handler500 = 'fam_recipes.views.handler500'

def trigger_error(request):
    '''User for testing 500 server error.'''
    division_by_zero = 1 / 0


urlpatterns = [
    path('', views.HomePageTemplateView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('recipes/', include('recipes.urls')),
    path('menu/', include('meal_menu.urls')),
    path('500/', views.handler500),
    path('server_error/', trigger_error),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
