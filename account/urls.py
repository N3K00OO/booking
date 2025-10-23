from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('profile/', views.profile_dashboard, name='profile_dashboard'),
]
