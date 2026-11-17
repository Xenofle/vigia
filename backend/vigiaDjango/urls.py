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
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
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
    path('factura_list/', billing_views.FacturaListView.as_view(), name='factura_list'),
    path('cobro_list/', billing_views.CobroListView.as_view(), name='cobro_list'),

    # UD3.7b - URLs de la aplicación core
    path('servicio_list/', core_views.ServicioListView.as_view(), name='servicio_list'),
    path('monitor_list/', core_views.MonitorListView.as_view(), name='monitor_list'),
    path('comprobacion_list/', core_views.ComprobacionListView.as_view(), name='comprobacion_list'),
    path('incidencia_list/', core_views.IncidenciaListView.as_view(), name='incidencia_list'),
    path('actualizacion_list/', core_views.ActualizacionIncidenciaListView.as_view(), name='actualizacion_list'),

    # UD4.2b - URLs de alta, modificación y baja de clientes
    path('cliente_create/', billing_views.ClienteCreateView.as_view(), name='cliente_create'),
    path('cliente_update/<int:pk>/', billing_views.ClienteUpdateView.as_view(), name='cliente_update'),
    path('cliente_delete/<int:pk>/', billing_views.ClienteDeleteView.as_view(), name='cliente_delete'),

    # UD4.2b - URLs de alta, modificación y baja de facturas
    path('factura_create/', billing_views.FacturaCreateView.as_view(), name='factura_create'),
    path('factura_update/<int:pk>/', billing_views.FacturaUpdateView.as_view(), name='factura_update'),
    path('factura_delete/<int:pk>/', billing_views.FacturaDeleteView.as_view(), name='factura_delete'),

    # UD4.2b - URLs de alta, modificación y baja de cobros
    path('cobro_create/', billing_views.CobroCreateView.as_view(), name='cobro_create'),
    path('cobro_update/<int:pk>/', billing_views.CobroUpdateView.as_view(), name='cobro_update'),
    path('cobro_delete/<int:pk>/', billing_views.CobroDeleteView.as_view(), name='cobro_delete'),

    # UD4.2b - URLs de alta, modificación y baja de servicios
    path('servicio_create/', core_views.ServicioCreateView.as_view(), name='servicio_create'),
    path('servicio_update/<int:pk>/', core_views.ServicioUpdateView.as_view(), name='servicio_update'),
    path('servicio_delete/<int:pk>/', core_views.ServicioDeleteView.as_view(), name='servicio_delete'),

    # UD4.2b - URLs de alta, modificación y baja de monitores
    path('monitor_create/', core_views.MonitorCreateView.as_view(), name='monitor_create'),
    path('monitor_update/<int:pk>/', core_views.MonitorUpdateView.as_view(), name='monitor_update'),
    path('monitor_delete/<int:pk>/', core_views.MonitorDeleteView.as_view(), name='monitor_delete'),

    # UD4.2b - URLs de alta, modificación y baja de comprobaciones
    path('comprobacion_create/', core_views.ComprobacionCreateView.as_view(), name='comprobacion_create'),
    path('comprobacion_update/<int:pk>/', core_views.ComprobacionUpdateView.as_view(), name='comprobacion_update'),
    path('comprobacion_delete/<int:pk>/', core_views.ComprobacionDeleteView.as_view(), name='comprobacion_delete'),

    # UD4.2b - URLs de alta, modificación y baja de incidencias
    path('incidencia_create/', core_views.IncidenciaCreateView.as_view(), name='incidencia_create'),
    path('incidencia_update/<int:pk>/', core_views.IncidenciaUpdateView.as_view(), name='incidencia_update'),
    path('incidencia_delete/<int:pk>/', core_views.IncidenciaDeleteView.as_view(), name='incidencia_delete'),

    # UD4.2b - URLs de alta, modificación y baja de actualizaciones de incidencia
    path('actualizacion_create/', core_views.ActualizacionIncidenciaCreateView.as_view(), name='actualizacion_create'),
    path('actualizacion_update/<int:pk>/', core_views.ActualizacionIncidenciaUpdateView.as_view(), name='actualizacion_update'),
    path('actualizacion_delete/<int:pk>/', core_views.ActualizacionIncidenciaDeleteView.as_view(), name='actualizacion_delete'),
    
]

# UD3.2e - Servicio de los ficheros de medios mientras DEBUG está activo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)