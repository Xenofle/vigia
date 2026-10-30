"""
URL configuration for vigiaDjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from common import views as common_views
from billing import views as billing_views
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', common_views.HomeView.as_view(), name='home'),
    path('panel/', common_views.PanelView.as_view(), name='panel'),
    path('cliente_list/', billing_views.ClienteListView.as_view(), name='cliente_list'),
    path('cliente_detail/<int:pk>/', billing_views.ClienteDetailView.as_view(), name='cliente_detail'),
    path('factura_list/', billing_views.FacturaListView.as_view(), name='factura_list'),
    path('factura_detail/<int:pk>/', billing_views.FacturaDetailView.as_view(), name='factura_detail'),
    path('cobro_list/', billing_views.CobroListView.as_view(), name='cobro_list'),
    path('cobro_detail/<int:pk>/', billing_views.CobroDetailView.as_view(), name='cobro_detail'),
    # UD3.7b - URLs de la aplicación core
    path('servicio_list/', core_views.ServicioListView.as_view(), name='servicio_list'),
    path('servicio_detail/<int:pk>/', core_views.ServicioDetailView.as_view(), name='servicio_detail'),
    path('monitor_list/', core_views.MonitorListView.as_view(), name='monitor_list'),
    path('monitor_detail/<int:pk>/', core_views.MonitorDetailView.as_view(), name='monitor_detail'),
    path('comprobacion_list/', core_views.ComprobacionListView.as_view(), name='comprobacion_list'),
    path('comprobacion_detail/<int:pk>/', core_views.ComprobacionDetailView.as_view(), name='comprobacion_detail'),
    path('incidencia_list/', core_views.IncidenciaListView.as_view(), name='incidencia_list'),
    path('incidencia_detail/<int:pk>/', core_views.IncidenciaDetailView.as_view(), name='incidencia_detail'),
    path('actualizacion_list/', core_views.ActualizacionIncidenciaListView.as_view(), name='actualizacion_list'),
    path('actualizacion_detail/<int:pk>/', core_views.ActualizacionIncidenciaDetailView.as_view(), name='actualizacion_detail'),
]

# UD3.2e - Servicio de los ficheros de medios mientras DEBUG está activo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)