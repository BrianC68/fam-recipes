from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView, make_user_staff, ProfileDetailView, ProfileUpdateView

app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('enable/', make_user_staff),
    path('profile/<slug>/', ProfileDetailView.as_view(), name='profile'),
    path('profile/<slug>/edit/', ProfileUpdateView.as_view(), name='profile-edit'),

]
