from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.models import Servicio, Monitor, Comprobacion, Incidencia, ActualizacionIncidencia
from core.forms import (
    ServicioForm,
    MonitorForm,
    ComprobacionForm,
    IncidenciaForm,
    ActualizacionIncidenciaForm,
)
from common.mixins import CreateUpdateMixin, BorradoMixin, OrdenacionMixin

# Servicio

# UD3.7a - Vista de listado de servicios
class ServicioListView(OrdenacionMixin, ListView):
    model = Servicio
    template_name = 'core/servicio_list.html'
    paginate_by = 10  # UD3.8b - Número de registros por página


# UD4.2a - Atributos y comportamiento comunes al alta y la modificación de servicios
class ServicioMixin(CreateUpdateMixin):
    model = Servicio
    form_class = ServicioForm
    titulo_creacion = 'Nuevo servicio'
    titulo_actualizacion = 'Actualizar servicio'
    url_borrado = 'servicio_delete'

    # UD4.2a - Tras crear o actualizar se vuelve a la pantalla de actualización
    def get_success_url(self):
        return reverse_lazy('servicio_update', kwargs={'pk': self.object.id})


# UD4.2a - Alta de servicios
class ServicioCreateView(ServicioMixin, CreateView):

    # UD4.4a - Mensaje de éxito con la representación textual del objeto
    def get_success_message(self, cleaned_data):
        return "Servicio '{}' creado correctamente".format(str(self.object))


# UD4.2a - Modificación de servicios
class ServicioUpdateView(ServicioMixin, UpdateView):

    def get_success_message(self, cleaned_data):
        return "Servicio '{}' actualizado correctamente".format(str(self.object))


# UD4.2a - Baja de servicios, con comprobación de dependencias
class ServicioDeleteView(BorradoMixin, DeleteView):
    model = Servicio
    success_url = reverse_lazy('servicio_list')
    titulo = 'Eliminar servicio'
    mensaje_confirmación = '¿Está seguro de que quiere eliminar este servicio? Se eliminarán también sus monitores.'

# Monitor

# UD3.7a - Vista de listado de monitores
class MonitorListView(OrdenacionMixin, ListView):
    model = Monitor
    template_name = 'core/monitor_list.html'
    paginate_by = 10  # UD3.8b




# UD4.2a - Atributos y comportamiento comunes al alta y la modificación de monitores
class MonitorMixin(CreateUpdateMixin):
    model = Monitor
    form_class = MonitorForm
    titulo_creacion = 'Nuevo monitor'
    titulo_actualizacion = 'Actualizar monitor'
    url_borrado = 'monitor_delete'

    def get_success_url(self):
        return reverse_lazy('monitor_update', kwargs={'pk': self.object.id})

    # UD4.2h - Un monitor público dentro de un servicio privado no se vería nunca
    def form_valid(self, form):
        if form.instance.publico and not form.instance.servicio.publico:
            messages.error(
                self.request,
                'El servicio {} no es público, así que este monitor no aparecería en la página '
                'de estado. Publique antes el servicio o desmarque la casilla.'.format(
                    str(form.instance.servicio)
                )
            )
            return super().form_invalid(form)

        return super().form_valid(form)


# UD4.2a - Alta de monitores
class MonitorCreateView(MonitorMixin, CreateView):

    def get_success_message(self, cleaned_data):
        return "Monitor '{}' creado correctamente".format(str(self.object))


# UD4.2a - Modificación de monitores
class MonitorUpdateView(MonitorMixin, UpdateView):

    def get_success_message(self, cleaned_data):
        return "Monitor '{}' actualizado correctamente".format(str(self.object))


# UD4.2a - Baja de monitores, con comprobación de dependencias
class MonitorDeleteView(BorradoMixin, DeleteView):
    model = Monitor
    success_url = reverse_lazy('monitor_list')
    titulo = 'Eliminar monitor'
    mensaje_confirmación = '¿Está seguro de que quiere eliminar este monitor? Se eliminará también su histórico de comprobaciones.'


# Comprobacion

# UD3.7a - Vista de listado de comprobaciones
class ComprobacionListView(OrdenacionMixin, ListView):
    model = Comprobacion
    template_name = 'core/comprobacion_list.html'
    paginate_by = 10  # UD3.8b



# UD4.2a - Atributos y comportamiento comunes al alta y la modificación de comprobaciones
class ComprobacionMixin(CreateUpdateMixin):
    model = Comprobacion
    form_class = ComprobacionForm
    titulo_creacion = 'Nueva comprobación'
    titulo_actualizacion = 'Actualizar comprobación'
    url_borrado = 'comprobacion_delete'

    def get_success_url(self):
        return reverse_lazy('comprobacion_update', kwargs={'pk': self.object.id})


# UD4.2a - Alta de comprobaciones
class ComprobacionCreateView(ComprobacionMixin, CreateView):

    def get_success_message(self, cleaned_data):
        return "Comprobación '{}' creada correctamente".format(str(self.object))


# UD4.2a - Modificación de comprobaciones
class ComprobacionUpdateView(ComprobacionMixin, UpdateView):

    def get_success_message(self, cleaned_data):
        return "Comprobación '{}' actualizada correctamente".format(str(self.object))


# UD4.2a - Baja de comprobaciones
class ComprobacionDeleteView(BorradoMixin, DeleteView):
    model = Comprobacion
    success_url = reverse_lazy('comprobacion_list')
    titulo = 'Eliminar comprobación'
    mensaje_confirmación = '¿Está seguro de que quiere eliminar esta comprobación del histórico?'

# Incidencia

# UD3.7a - Vista de listado de incidencias
class IncidenciaListView(OrdenacionMixin, ListView):
    model = Incidencia
    template_name = 'core/incidencia_list.html'
    paginate_by = 10  # UD3.8b



# UD4.2a - Atributos y comportamiento comunes al alta y la modificación de incidencias
class IncidenciaMixin(CreateUpdateMixin):
    model = Incidencia
    form_class = IncidenciaForm
    titulo_creacion = 'Nueva incidencia'
    titulo_actualizacion = 'Actualizar incidencia'
    url_borrado = 'incidencia_delete'

    def get_success_url(self):
        return reverse_lazy('incidencia_update', kwargs={'pk': self.object.id})

    # UD4.2h - Un servicio no puede tener dos incidencias abiertas a la vez
    def form_valid(self, form):
        if form.instance.cerrada_en is None:
            abiertas = Incidencia.objects.filter(
            # Una incidencia abierta es la que no tiene fecha de cierre: se filtra por el nulo
            # https://docs.djangoproject.com/en/5.2/ref/models/querysets/ (sección Field lookups, isnull)
                servicio=form.instance.servicio, cerrada_en__isnull=True
            )
            if form.instance.pk:
                abiertas = abiertas.exclude(pk=form.instance.pk)
        # exists() comprueba si hay alguna fila sin traer los objetos a memoria
        # https://docs.djangoproject.com/en/5.2/ref/models/querysets/#django.db.models.query.QuerySet.exists
            if abiertas.exists():
                messages.error(
                    self.request,
                    'El servicio {} ya tiene una incidencia abierta. Añada una actualización '
                    'a la existente en lugar de abrir otra.'.format(str(form.instance.servicio))
                )
                return super().form_invalid(form)

        return super().form_valid(form)


# UD4.2a - Alta de incidencias
class IncidenciaCreateView(IncidenciaMixin, CreateView):

    def get_success_message(self, cleaned_data):
        return "Incidencia '{}' creada correctamente".format(str(self.object))


# UD4.2a - Modificación de incidencias
class IncidenciaUpdateView(IncidenciaMixin, UpdateView):

    def get_success_message(self, cleaned_data):
        return "Incidencia '{}' actualizada correctamente".format(str(self.object))


# UD4.2a - Baja de incidencias, con comprobación de dependencias
class IncidenciaDeleteView(BorradoMixin, DeleteView):
    model = Incidencia
    success_url = reverse_lazy('incidencia_list')
    titulo = 'Eliminar incidencia'
    mensaje_confirmación = '¿Está seguro de que quiere eliminar esta incidencia? Se eliminarán también sus actualizaciones.'

# ActualizacionIncidencia

# UD3.7a - Vista de listado de actualizaciones de incidencia
class ActualizacionIncidenciaListView(OrdenacionMixin, ListView):
    model = ActualizacionIncidencia
    template_name = 'core/actualizacionincidencia_list.html'
    paginate_by = 10  # UD3.8b



# UD4.2a - Atributos y comportamiento comunes al alta y la modificación de actualizaciones
class ActualizacionIncidenciaMixin(CreateUpdateMixin):
    model = ActualizacionIncidencia
    form_class = ActualizacionIncidenciaForm
    titulo_creacion = 'Nueva actualización'
    titulo_actualizacion = 'Modificar actualización'
    url_borrado = 'actualizacion_delete'

    def get_success_url(self):
        return reverse_lazy('actualizacion_update', kwargs={'pk': self.object.id})


# UD4.2a - Alta de actualizaciones de incidencia
class ActualizacionIncidenciaCreateView(ActualizacionIncidenciaMixin, CreateView):

    def get_success_message(self, cleaned_data):
        return "Actualización '{}' creada correctamente".format(str(self.object))


# UD4.2a - Modificación de actualizaciones de incidencia
class ActualizacionIncidenciaUpdateView(ActualizacionIncidenciaMixin, UpdateView):

    def get_success_message(self, cleaned_data):
        return "Actualización '{}' modificada correctamente".format(str(self.object))


# UD4.2a - Baja de actualizaciones de incidencia
class ActualizacionIncidenciaDeleteView(BorradoMixin, DeleteView):
    model = ActualizacionIncidencia
    success_url = reverse_lazy('actualizacion_list')
    titulo = 'Eliminar actualización'
    mensaje_confirmación = '¿Está seguro de que quiere eliminar esta actualización de la cronología?'