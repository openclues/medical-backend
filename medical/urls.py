
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.routers import BaseRouter

from user.views import MedicalCenterListApiView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/medical', MedicalCenterListApiView.as_view()),
    path('api/user/', include('djoser.urls')),
    path('api/user/', include('djoser.urls.authtoken')),
    # Optional UI:
    path('api/docs', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]
