from django.shortcuts import render
from django.views.generic import ListView, DetailView
from billing.models import Cliente, Factura, Cobro


class ClienteListView(ListView):
    model = Cliente
    template_name = 'billing/cliente_list.html'


class ClienteDetailView(DetailView):
    model = Cliente
    template_name = 'billing/cliente_detail.html'


class FacturaListView(ListView):
    model = Factura
    template_name = 'billing/factura_list.html'


class FacturaDetailView(DetailView):
    model = Factura
    template_name = 'billing/factura_detail.html'


class CobroListView(ListView):
    model = Cobro
    template_name = 'billing/cobro_list.html'


class CobroDetailView(DetailView):
    model = Cobro
    template_name = 'billing/cobro_detail.html'
