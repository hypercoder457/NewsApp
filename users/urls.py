from django.contrib.auth.views import LoginView
from django.urls import include, path

from users.forms import EmailAuthenticationForm

from . import views

app_name = 'users'
urlpatterns = [
    path('login/', LoginView.as_view(form_class=EmailAuthenticationForm), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('activate/<slug:uidb64>/<slug:token>', views.activate, name='activate'),
    path('profile/<email>/', views.profile, name='profile'),
    path('delete-account/<email>/', views.delete_account, name='delete-account'),
    path('edit-profile/<email>/', views.edit_profile, name='edit-profile'),
    path('change-password/', views.change_password, name='change-password')
]
