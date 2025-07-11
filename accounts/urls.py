from django.urls import path

from .views import HomeView, healthz

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('healthz', healthz, name='healthz'),
]
