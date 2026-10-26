from django.contrib import admin

from .models import Cliente, Cobro, Factura


# UD3.4b - Configuración del administrador para el modelo Cliente
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellidos', 'nif', 'email')        # UD3.4a - Columnas mostradas en el listado
    list_display_links = ('nombre', 'apellidos', 'nif', 'email')  # UD3.4a - Columnas que enlazan a la ficha del registro
    list_filter = ('nif',)                                        # UD3.4a - Campos de filtrado en la barra lateral
    search_fields = ('nombre', 'apellidos', 'nif', 'email')       # UD3.4a - Campos sobre los que actúa el buscador
    preserve_filters = True                                       # UD3.4a - Mantiene los filtros al volver del detalle al listado


# UD3.4c - Configuración del administrador para el modelo Factura
@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('num_factura', 'fecha', 'total')
    list_display_links = ('num_factura', 'fecha', 'total')
    list_filter = ('cliente',)
    search_fields = ('num_factura', 'cliente__nombre', 'cliente__apellidos')
    preserve_filters = True


# UD3.4d - Configuración del administrador para el modelo Cobro
@admin.register(Cobro)
class CobroAdmin(admin.ModelAdmin):
    list_display = ('num_factura', 'fecha', 'importe')
    list_display_links = ('num_factura', 'fecha', 'importe')
    list_filter = ('factura__cliente',)
    search_fields = ( 'factura__num_factura', 'factura__cliente__nombre', 'factura__cliente__apellidos', )
    preserve_filters = True

    # UD3.4d - Columna calculada con el número de la factura asociada
    @admin.display(description='N.º factura', ordering='factura__num_factura')
    def num_factura(self, obj):
        return obj.factura.num_factura