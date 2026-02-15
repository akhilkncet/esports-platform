from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView
)
from .auth_views import login_view, logout_view, check_auth, get_csrf_token

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Authentication API endpoints
    path('api/login/', login_view, name='api-login'),
    path('api/logout/', logout_view, name='api-logout'),
    path('api/check-auth/', check_auth, name='check-auth'),
    path('api/get-csrf-token/', get_csrf_token, name='get-csrf-token'),
    
    # API endpoints
    path("api/accounts/", include('accounts.urls')),
    path("api/teams/", include('teams.urls')),
    path("api/tournaments/", include('tournaments.urls')),
    
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    path('api-auth/', include('rest_framework.urls')),
    
    # Frontend routes (protected)
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('', login_required(TemplateView.as_view(template_name='index.html'), login_url='/login/'), name='home'),
    path('teams/', login_required(TemplateView.as_view(template_name='teams.html'), login_url='/login/'), name='teams'),
    path('tournaments/', login_required(TemplateView.as_view(template_name='tournaments.html'), login_url='/login/'), name='tournaments'),
]

