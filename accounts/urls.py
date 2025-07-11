from django.urls import path

from .views import HomeView, healthz, oidc_config_view

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('healthz', healthz, name='healthz'),
    path('oidc-config/', oidc_config_view, name='oidc_config'),
]
