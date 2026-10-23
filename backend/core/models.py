from django.conf import settings
from django.db import models
 
 
# UD3.3a - Modelo Servicio: sistema supervisado que agrupa monitores
class Servicio(models.Model):
    nombre = models.CharField(verbose_name='Nombre', max_length=150)
    descripcion = models.TextField(verbose_name='Descripción', null=True, blank=True)
    slug = models.SlugField(verbose_name='Identificador para la URL', max_length=60)
    orden = models.PositiveSmallIntegerField(verbose_name='Orden de aparición', default=0)
    publico = models.BooleanField(verbose_name='Visible en la página pública', default=True)
    creado_en = models.DateTimeField(verbose_name='Fecha de creación', auto_now_add=True)
 
    class Meta:
        # UD3.4g - Nombre singular y plural del modelo en el administrador
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        # UD3.4h - Ordenación por defecto de los registros
        ordering = ['orden', 'nombre']
        # UD3.3f - Restricciones de unicidad del modelo
        unique_together = [['nombre'], ['slug']]
 
    # UD3.3e - Representación textual del servicio
    def __str__(self):
        return self.nombre
 
 
# UD3.3a - Modelo Monitor: comprobación configurada sobre una URL o un puerto
class Monitor(models.Model):
 
    # UD3.3a - Valores admitidos para el tipo de comprobación
    class Tipo(models.TextChoices):
        HTTP = 'http', 'HTTP/HTTPS'
        TCP = 'tcp', 'Puerto TCP'
 
    # UD3.3a - Valores admitidos para el estado del monitor
    class Estado(models.TextChoices):
        PENDIENTE = 'pendiente', 'Pendiente'
        ACTIVO = 'activo', 'Activo'
        DEGRADADO = 'degradado', 'Degradado'
        CAIDO = 'caido', 'Caído'
 
    servicio = models.ForeignKey(
        Servicio, on_delete=models.CASCADE, verbose_name='Servicio'
    )
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='Creado por'
    )
    nombre = models.CharField(verbose_name='Nombre', max_length=100)
    tipo = models.CharField(
        verbose_name='Tipo', max_length=10, choices=Tipo.choices, default=Tipo.HTTP
    )
 
    # Destino de la comprobación: según el tipo se usa la URL o la pareja host y puerto
    url = models.URLField(verbose_name='URL', null=True, blank=True)
    host = models.CharField(verbose_name='Host', max_length=255, null=True, blank=True)
    puerto = models.PositiveIntegerField(verbose_name='Puerto', null=True, blank=True)
 
    # Parámetros que gobiernan la ejecución de la comprobación
    intervalo_segundos = models.PositiveIntegerField(
        verbose_name='Intervalo (segundos)', default=60
    )
    timeout_ms = models.PositiveIntegerField(
        verbose_name='Tiempo máximo de espera (ms)', default=5000
    )
    reintentos = models.PositiveSmallIntegerField(
        verbose_name='Reintentos antes de darlo por caído', default=3
    )
    umbral_latencia_ms = models.PositiveIntegerField(
        verbose_name='Umbral de latencia (ms)', default=2000
    )
    activo = models.BooleanField(verbose_name='Activo', default=True)
    publico = models.BooleanField(verbose_name='Visible en la página pública', default=True)
 
    # Estado actual, almacenado en el propio monitor para no recalcularlo
    # recorriendo la tabla de comprobaciones en cada consulta del panel
    estado = models.CharField(
        verbose_name='Estado',
        max_length=15,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
    )
    estado_desde = models.DateTimeField(verbose_name='Estado desde', null=True, blank=True)
    fallos_consecutivos = models.PositiveSmallIntegerField(
        verbose_name='Fallos consecutivos', default=0
    )
 
    class Meta:
        # UD3.4g - Nombre singular y plural del modelo en el administrador
        verbose_name = 'Monitor'
        verbose_name_plural = 'Monitores'
        # UD3.4h - Ordenación por defecto de los registros
        ordering = ['servicio', 'nombre']
        # UD3.3f - Un monitor no puede repetir nombre dentro del mismo servicio
        unique_together = [['servicio', 'nombre']]
 
    # UD3.3e - Representación textual: servicio y nombre del monitor
    def __str__(self):
        return str(self.servicio) + ' - ' + self.nombre
 
 
# UD3.3a - Modelo Comprobacion: resultado de una ejecución concreta de un monitor
class Comprobacion(models.Model):
    monitor = models.ForeignKey(
        Monitor, on_delete=models.CASCADE, verbose_name='Monitor'
    )
    ejecutada_en = models.DateTimeField(verbose_name='Fecha de ejecución', auto_now_add=True)
    correcta = models.BooleanField(verbose_name='Correcta')
    latencia_ms = models.PositiveIntegerField(
        verbose_name='Latencia (ms)', null=True, blank=True
    )
    codigo_http = models.PositiveSmallIntegerField(
        verbose_name='Código HTTP', null=True, blank=True
    )
    error = models.CharField(verbose_name='Error', max_length=255, null=True, blank=True)
 
    class Meta:
        # UD3.4g - Nombre singular y plural del modelo en el administrador
        verbose_name = 'Comprobación'
        verbose_name_plural = 'Comprobaciones'
        # UD3.4h - De la más reciente a la más antigua
        ordering = ['-ejecutada_en']
        # Es la tabla que más crece del proyecto: un índice compuesto por monitor
        # y fecha descendente acelera la consulta habitual del histórico
        indexes = [
            models.Index(fields=['monitor', '-ejecutada_en'], name='idx_comprobacion_monitor')
        ]
 
    # UD3.3e - Representación textual: monitor, resultado y fecha
    def __str__(self):
        resultado = 'correcta' if self.correcta else 'fallida'
        return str(self.monitor) + ' - ' + resultado
 
 
# UD3.3a - Modelo Incidencia: interrupción de un servicio, automática o manual
class Incidencia(models.Model):
 
    # UD3.3a - Valores admitidos para el estado de la incidencia
    class Estado(models.TextChoices):
        INVESTIGANDO = 'investigando', 'Investigando'
        IDENTIFICADO = 'identificado', 'Identificado'
        MONITORIZANDO = 'monitorizando', 'Monitorizando'
        RESUELTA = 'resuelta', 'Resuelta'
 
    # UD3.3a - Valores admitidos para la severidad de la incidencia
    class Severidad(models.TextChoices):
        MENOR = 'menor', 'Menor'
        MAYOR = 'mayor', 'Mayor'
        CRITICA = 'critica', 'Crítica'
 
    # UD3.3a - Valores admitidos para el origen de la incidencia
    class Origen(models.TextChoices):
        AUTOMATICO = 'automatico', 'Automático'
        MANUAL = 'manual', 'Manual'
 
    servicio = models.ForeignKey(
        Servicio, on_delete=models.CASCADE, verbose_name='Servicio'
    )
 
    # Queda a nulo en las incidencias abiertas a mano, que no proceden de un monitor.
    # Se usa SET_NULL para que la incidencia sobreviva a la desaparición del monitor.
    monitor = models.ForeignKey(
        Monitor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Monitor de origen',
    )
 
    titulo = models.CharField(verbose_name='Título', max_length=150)
    estado = models.CharField(
        verbose_name='Estado',
        max_length=15,
        choices=Estado.choices,
        default=Estado.INVESTIGANDO,
    )
    severidad = models.CharField(
        verbose_name='Severidad',
        max_length=10,
        choices=Severidad.choices,
        default=Severidad.MAYOR,
    )
    origen = models.CharField(
        verbose_name='Origen',
        max_length=10,
        choices=Origen.choices,
        default=Origen.AUTOMATICO,
    )
    publica = models.BooleanField(verbose_name='Visible en la página pública', default=True)
    abierta_en = models.DateTimeField(verbose_name='Fecha de apertura', auto_now_add=True)
    cerrada_en = models.DateTimeField(verbose_name='Fecha de cierre', null=True, blank=True)
 
    class Meta:
        # UD3.4g - Nombre singular y plural del modelo en el administrador
        verbose_name = 'Incidencia'
        verbose_name_plural = 'Incidencias'
        # UD3.4h - De la más reciente a la más antigua
        ordering = ['-abierta_en']
 
    # UD3.3e - Representación textual: título y estado de la incidencia
    def __str__(self):
        return self.titulo + ' (' + self.get_estado_display() + ')'
 
 
# UD3.3a - Modelo ActualizacionIncidencia: cada entrada de la cronología de una incidencia
class ActualizacionIncidencia(models.Model):
    incidencia = models.ForeignKey(
        Incidencia, on_delete=models.CASCADE, verbose_name='Incidencia'
    )
 
    # El autor puede quedar a nulo si el usuario que la escribió se da de baja,
    # pero la actualización debe conservarse como parte del histórico
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Autor',
    )
 
    estado = models.CharField(
        verbose_name='Estado', max_length=15, choices=Incidencia.Estado.choices
    )
    mensaje = models.TextField(verbose_name='Mensaje')
    creada_en = models.DateTimeField(verbose_name='Fecha', auto_now_add=True)
 
    class Meta:
        # UD3.4g - Nombre singular y plural del modelo en el administrador
        verbose_name = 'Actualización de incidencia'
        verbose_name_plural = 'Actualizaciones de incidencias'
        # UD3.4h - En orden ascendente: una cronología se lee de principio a fin
        ordering = ['creada_en']
 
    # UD3.3e - Representación textual: incidencia y estado al que pasó
    def __str__(self):
        return str(self.incidencia) + ' - ' + self.get_estado_display()
 