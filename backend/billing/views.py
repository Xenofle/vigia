from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from billing.models import Cliente, Factura, Cobro
from billing.forms import ClienteForm, FacturaForm, CobroForm
from common.mixins import CreateUpdateMixin, BorradoMixin, OrdenacionMixin

# Cliente

# UD3.7a - Listado de clientes
class ClienteListView(OrdenacionMixin, ListView):
    model = Cliente
    template_name = 'billing/cliente_list.html'
    paginate_by = 10  # UD3.8b - Número de registros por página


# UD3.7a - Detalle de un cliente
class ClienteDetailView(DetailView):
    model = Cliente
    template_name = 'billing/cliente_detail.html'


# UD4.2a - Atributos y comportamiento comunes al alta y la modificación de clientes
class ClienteMixin(CreateUpdateMixin):
    model = Cliente
    form_class = ClienteForm
    titulo_creacion = 'Nuevo cliente'
    titulo_actualizacion = 'Actualizar cliente'
    url_borrado = 'cliente_delete'

    # UD4.2a - Tras crear o actualizar se vuelve a la pantalla de actualización
    def get_success_url(self):
        return reverse_lazy('cliente_update', kwargs={'pk': self.object.id})


# UD4.2a - Alta de clientes
class ClienteCreateView(ClienteMixin, CreateView):

    # UD4.4a - Mensaje de éxito con la representación textual del objeto
    def get_success_message(self, cleaned_data):
        return "Cliente '{}' creado correctamente".format(str(self.object))


# UD4.2a - Modificación de clientes
class ClienteUpdateView(ClienteMixin, UpdateView):

    def get_success_message(self, cleaned_data):
        return "Cliente '{}' actualizado correctamente".format(str(self.object))


# UD4.2a - Baja de clientes, con comprobación de dependencias
class ClienteDeleteView(BorradoMixin, DeleteView):
    model = Cliente
    success_url = reverse_lazy('cliente_list')
    titulo = 'Eliminar cliente'
    mensaje_confirmación = '¿Está seguro de que quiere eliminar este cliente?'

# Factura

# UD3.7a - Listado de facturas
class FacturaListView(OrdenacionMixin, ListView):
    model = Factura
    template_name = 'billing/factura_list.html'
    paginate_by = 10  # UD3.8b


# UD3.7a - Detalle de una factura
class FacturaDetailView(DetailView):
    model = Factura
    template_name = 'billing/factura_detail.html'


# UD4.2a - Atributos y comportamiento comunes al alta y la modificación de facturas
class FacturaMixin(CreateUpdateMixin):
    model = Factura
    form_class = FacturaForm
    titulo_creacion = 'Nueva factura'
    titulo_actualizacion = 'Actualizar factura'
    url_borrado = 'factura_delete'

    def get_success_url(self):
        return reverse_lazy('factura_update', kwargs={'pk': self.object.id})


# UD4.2a - Alta de facturas
class FacturaCreateView(FacturaMixin, CreateView):

    def get_success_message(self, cleaned_data):
        return "Factura '{}' creada correctamente".format(str(self.object))


# UD4.2a - Modificación de facturas
class FacturaUpdateView(FacturaMixin, UpdateView):

    def get_success_message(self, cleaned_data):
        return "Factura '{}' actualizada correctamente".format(str(self.object))


# UD4.2a - Baja de facturas, con comprobación de dependencias
class FacturaDeleteView(BorradoMixin, DeleteView):
    model = Factura
    success_url = reverse_lazy('factura_list')
    titulo = 'Eliminar factura'
    mensaje_confirmación = '¿Está seguro de que quiere eliminar esta factura?'

# Cobro

# UD3.7a - Listado de cobros
class CobroListView(OrdenacionMixin, ListView):
    model = Cobro
    template_name = 'billing/cobro_list.html'
    paginate_by = 10  # UD3.8b


# UD3.7a - Detalle de un cobro
class CobroDetailView(DetailView):
    model = Cobro
    template_name = 'billing/cobro_detail.html'


# UD4.2a - Atributos y comportamiento comunes al alta y la modificación de cobros
class CobroMixin(CreateUpdateMixin):
    model = Cobro
    form_class = CobroForm
    titulo_creacion = 'Nuevo cobro'
    titulo_actualizacion = 'Actualizar cobro'
    url_borrado = 'cobro_delete'

    def get_success_url(self):
        return reverse_lazy('cobro_update', kwargs={'pk': self.object.id})

    # UD4.2g - La suma de los cobros de una factura no puede superar su total
    def form_valid(self, form):
        factura = form.instance.factura

        # Los demás cobros de la factura: al actualizar se excluye el que se edita
        cobros = factura.cobro_set.all()
        if form.instance.pk:
            cobros = cobros.exclude(pk=form.instance.pk)

        total_cobrado = 0
        for cobro in cobros:
            total_cobrado = total_cobrado + cobro.importe

        if total_cobrado + form.instance.importe > factura.total:
            messages.error(
                self.request,
                'La suma de los cobros ({}) superaría el total de la factura ({}).'.format(
                    total_cobrado + form.instance.importe, factura.total
                )
            )
            return super().form_invalid(form)

        return super().form_valid(form)


# UD4.2a - Alta de cobros
class CobroCreateView(CobroMixin, CreateView):

    def get_success_message(self, cleaned_data):
        return "Cobro '{}' creado correctamente".format(str(self.object))


# UD4.2a - Modificación de cobros
class CobroUpdateView(CobroMixin, UpdateView):

    def get_success_message(self, cleaned_data):
        return "Cobro '{}' actualizado correctamente".format(str(self.object))


# UD4.2a - Baja de cobros
class CobroDeleteView(BorradoMixin, DeleteView):
    model = Cobro
    success_url = reverse_lazy('cobro_list')
    titulo = 'Eliminar cobro'
    mensaje_confirmación = '¿Está seguro de que quiere eliminar este cobro?'