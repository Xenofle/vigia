from django.views.generic import DetailView, ListView

from .models import (
    ActualizacionIncidencia,
    Comprobacion,
    Incidencia,
    Monitor,
    Servicio,
)


# UD3.7a - Vista de listado de servicios
class ServicioListView(ListView):
    model = Servicio
    template_name = 'core/servicio_list.html'


# UD3.7a - Vista de detalle de un servicio
class ServicioDetailView(DetailView):
    model = Servicio
    template_name = 'core/servicio_detail.html'


# UD3.7a - Vista de listado de monitores
class MonitorListView(ListView):
    model = Monitor
    template_name = 'core/monitor_list.html'


# UD3.7a - Vista de detalle de un monitor
class MonitorDetailView(DetailView):
    model = Monitor
    template_name = 'core/monitor_detail.html'


# UD3.7a - Vista de listado de comprobaciones
class ComprobacionListView(ListView):
    model = Comprobacion
    template_name = 'core/comprobacion_list.html'


# UD3.7a - Vista de detalle de una comprobación
class ComprobacionDetailView(DetailView):
    model = Comprobacion
    template_name = 'core/comprobacion_detail.html'


# UD3.7a - Vista de listado de incidencias
class IncidenciaListView(ListView):
    model = Incidencia
    template_name = 'core/incidencia_list.html'


# UD3.7a - Vista de detalle de una incidencia
class IncidenciaDetailView(DetailView):
    model = Incidencia
    template_name = 'core/incidencia_detail.html'


# UD3.7a - Vista de listado de actualizaciones de incidencia
class ActualizacionIncidenciaListView(ListView):
    model = ActualizacionIncidencia
    template_name = 'core/actualizacionincidencia_list.html'


# UD3.7a - Vista de detalle de una actualización de incidencia
class ActualizacionIncidenciaDetailView(DetailView):
    model = ActualizacionIncidencia
    template_name = 'core/actualizacionincidencia_detail.html'