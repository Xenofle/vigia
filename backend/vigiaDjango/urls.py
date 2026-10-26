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
]

# UD3.2e - Servicio de los ficheros de medios mientras DEBUG está activo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)