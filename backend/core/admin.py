from django.contrib import admin

from .models import (
    ActualizacionIncidencia,
    Comprobacion,
    Incidencia,
    Monitor,
    Servicio,
)


# UD3.4e - Configuración del administrador para el modelo Servicio
@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'publico', 'orden')
    list_display_links = ('nombre', 'slug')
    list_filter = ('publico',)
    search_fields = ('nombre', 'descripcion')
    preserve_filters = True
    prepopulated_fields = {'slug': ('nombre',)}  # UD3.4a - Rellena el identificador de la URL a partir del nombre


# UD3.4e - Configuración del administrador para el modelo Monitor
@admin.register(Monitor)
class MonitorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'servicio', 'tipo', 'estado', 'activo', 'estado_desde')
    list_display_links = ('nombre',)
    list_filter = ('estado', 'tipo', 'activo', 'servicio')
    search_fields = ('nombre', 'url', 'host')
    preserve_filters = True
    autocomplete_fields = ('servicio',)  # UD3.4a - Sustituye el desplegable por un buscador cuando hay muchos registros
    readonly_fields = ('estado', 'estado_desde', 'fallos_consecutivos')  # UD3.4a - Campos visibles pero no editables
    fieldsets = (  # UD3.4a - Agrupación de los campos del formulario en secciones
        (None, {
            'fields': ('servicio', 'creado_por', 'nombre', 'tipo', 'activo', 'publico')
        }),
        ('Destino de la comprobación', {
            'fields': ('url', 'host', 'puerto')
        }),
        ('Parámetros de ejecución', {
            'fields': ('intervalo_segundos', 'timeout_ms', 'reintentos', 'umbral_latencia_ms')
        }),
        ('Estado actual', {
            'fields': ('estado', 'estado_desde', 'fallos_consecutivos')
        }),
    )


# UD3.4e - Configuración del administrador para el modelo Comprobacion
@admin.register(Comprobacion)
class ComprobacionAdmin(admin.ModelAdmin):
    list_display = ('monitor', 'ejecutada_en', 'correcta', 'latencia_ms', 'codigo_http')
    list_display_links = ('monitor',)
    list_filter = ('correcta', 'monitor__servicio')
    search_fields = ('monitor__nombre',)
    preserve_filters = True
    date_hierarchy = 'ejecutada_en'  # UD3.4a - Navegación por fechas en la cabecera del listado
    readonly_fields = ('monitor', 'ejecutada_en', 'correcta', 'latencia_ms', 'codigo_http', 'error')

    # UD3.4e - Las comprobaciones las genera el motor del sistema, no se dan de alta a mano
    def has_add_permission(self, request):
        return False


# UD3.4e - Cronología de la incidencia, editable desde la propia incidencia
class ActualizacionEnLinea(admin.TabularInline):
    model = ActualizacionIncidencia
    extra = 1
    fields = ('estado', 'mensaje', 'autor')


# UD3.4e - Configuración del administrador para el modelo Incidencia
@admin.register(Incidencia)
class IncidenciaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'servicio', 'estado', 'severidad', 'origen', 'abierta_en')
    list_display_links = ('titulo',)
    list_filter = ('estado', 'severidad', 'origen', 'publica', 'servicio')
    search_fields = ('titulo',)
    preserve_filters = True
    date_hierarchy = 'abierta_en'
    autocomplete_fields = ('servicio',)
    inlines = [ActualizacionEnLinea]  # UD3.4a - Modelos relacionados editables dentro del formulario principal


# UD3.4e - Configuración del administrador para el modelo ActualizacionIncidencia
@admin.register(ActualizacionIncidencia)
class ActualizacionIncidenciaAdmin(admin.ModelAdmin):
    list_display = ('incidencia', 'estado', 'autor', 'creada_en')
    list_display_links = ('incidencia',)
    list_filter = ('estado',)
    search_fields = ('incidencia__titulo', 'mensaje')
    preserve_filters = True