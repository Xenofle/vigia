from django import forms
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, HTML

from core.models import Servicio, Monitor, Comprobacion, Incidencia, ActualizacionIncidencia


# UD4.3a - Formulario del modelo Servicio
class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre', 'slug', 'descripcion', 'orden', 'publico']

    # UD4.4c - Helper y layout del formulario
    def __init__(self, *args, **kwargs):
        super(ServicioForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False  # El elemento <form> ya está en la plantilla

        # UD4.4e - Fila 1: nombre 8 e identificador 4. Fila 2: descripción. Fila 3: orden y visibilidad
        self.helper.layout = Layout(
            Div(
                Div(Field('nombre'), css_class='col-8'),
                Div(Field('slug'), css_class='col-4'),
                css_class='row'
            ),
            Div(
                Div(Field('descripcion'), css_class='col-12'),
                css_class='row'
            ),
            Div(
                Div(Field('orden'), css_class='col-6'),
                Div(Field('publico'), css_class='col-6'),
                css_class='row'
            ),
        )


# UD4.3a - Formulario del modelo Monitor
class MonitorForm(forms.ModelForm):
    class Meta:
        model = Monitor
        # Se excluyen estado, estado_desde y fallos_consecutivos: los escribe el sistema
        fields = [
            'servicio', 'creado_por', 'nombre', 'tipo', 'activo', 'publico',
            'url', 'host', 'puerto',
            'intervalo_segundos', 'timeout_ms', 'reintentos', 'umbral_latencia_ms',
        ]

    # UD4.3c - El destino ha de ser coherente con el tipo de comprobación
    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        url = cleaned_data.get('url')
        host = cleaned_data.get('host')
        puerto = cleaned_data.get('puerto')

        if tipo == Monitor.Tipo.HTTP and not url:
            raise ValidationError('Un monitor de tipo HTTP necesita una URL.')

        if tipo == Monitor.Tipo.TCP and (not host or not puerto):
            raise ValidationError('Un monitor de tipo TCP necesita un host y un puerto.')

        return cleaned_data

    # UD4.3c - Un intervalo demasiado corto saturaría el servicio comprobado
    def clean_intervalo_segundos(self):
        intervalo = self.cleaned_data['intervalo_segundos']
        if intervalo < 10:
            raise ValidationError('El intervalo no puede ser inferior a 10 segundos.')
        return intervalo

    # UD4.4c - Helper y layout del formulario
    def __init__(self, *args, **kwargs):
        super(MonitorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        # UD4.4e - Identificación, destino y parámetros de ejecución, separados
        self.helper.layout = Layout(
            Div(
                Div(Field('servicio'), css_class='col-6'),
                Div(Field('nombre'), css_class='col-6'),
                css_class='row'
            ),
            Div(
                Div(Field('creado_por'), css_class='col-6'),
                Div(Field('tipo'), css_class='col-6'),
                css_class='row'
            ),
            Div(
                Div(Field('activo'), css_class='col-6'),
                Div(Field('publico'), css_class='col-6'),
                css_class='row'
            ),
            HTML('<hr>'),
            Div(
                Div(Field('url'), css_class='col-12'),
                css_class='row'
            ),
            Div(
                Div(Field('host'), css_class='col-8'),
                Div(Field('puerto'), css_class='col-4'),
                css_class='row'
            ),
            HTML('<hr>'),
            Div(
                Div(Field('intervalo_segundos'), css_class='col-3'),
                Div(Field('timeout_ms'), css_class='col-3'),
                Div(Field('reintentos'), css_class='col-3'),
                Div(Field('umbral_latencia_ms'), css_class='col-3'),
                css_class='row'
            ),
        )


# UD4.3a - Formulario del modelo Comprobacion
class ComprobacionForm(forms.ModelForm):
    class Meta:
        model = Comprobacion
        # ejecutada_en queda fuera: es auto_now_add, y por tanto no editable
        fields = ['monitor', 'correcta', 'latencia_ms', 'codigo_http', 'error']

    # UD4.4c - Helper y layout del formulario
    def __init__(self, *args, **kwargs):
        super(ComprobacionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        # UD4.4e - Fila 1: monitor 8 y resultado 4. Fila 2: métricas. Fila 3: error
        self.helper.layout = Layout(
            Div(
                Div(Field('monitor'), css_class='col-8'),
                Div(Field('correcta'), css_class='col-4'),
                css_class='row'
            ),
            Div(
                Div(Field('latencia_ms'), css_class='col-6'),
                Div(Field('codigo_http'), css_class='col-6'),
                css_class='row'
            ),
            Div(
                Div(Field('error'), css_class='col-12'),
                css_class='row'
            ),
        )


# UD4.3a - Formulario del modelo Incidencia
class IncidenciaForm(forms.ModelForm):
    class Meta:
        model = Incidencia
        # abierta_en queda fuera: es auto_now_add, y por tanto no editable
        fields = ['servicio', 'monitor', 'titulo', 'estado', 'severidad', 'origen', 'publica', 'cerrada_en']

    # UD4.3c - Coherencia entre el estado de la incidencia y su fecha de cierre
    def clean(self):
        cleaned_data = super().clean()
        estado = cleaned_data.get('estado')
        cerrada_en = cleaned_data.get('cerrada_en')

        if estado == Incidencia.Estado.RESUELTA and not cerrada_en:
            raise ValidationError('Una incidencia resuelta ha de tener fecha de cierre.')

        if cerrada_en and self.instance.abierta_en and cerrada_en < self.instance.abierta_en:
            raise ValidationError('La fecha de cierre no puede ser anterior a la de apertura.')

        return cleaned_data

    # UD4.4c - Helper y layout del formulario
    def __init__(self, *args, **kwargs):
        super(IncidenciaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        # UD4.4e - Origen, título, clasificación y cierre
        self.helper.layout = Layout(
            Div(
                Div(Field('servicio'), css_class='col-6'),
                Div(Field('monitor'), css_class='col-6'),
                css_class='row'
            ),
            Div(
                Div(Field('titulo'), css_class='col-12'),
                css_class='row'
            ),
            HTML('<hr>'),
            Div(
                Div(Field('estado'), css_class='col-4'),
                Div(Field('severidad'), css_class='col-4'),
                Div(Field('origen'), css_class='col-4'),
                css_class='row'
            ),
            Div(
                Div(Field('publica'), css_class='col-6'),
                Div(Field('cerrada_en'), css_class='col-6'),
                css_class='row'
            ),
        )


# UD4.3a - Formulario del modelo ActualizacionIncidencia
class ActualizacionIncidenciaForm(forms.ModelForm):
    class Meta:
        model = ActualizacionIncidencia
        # creada_en queda fuera: es auto_now_add, y por tanto no editable
        fields = ['incidencia', 'autor', 'estado', 'mensaje']

    # UD4.4c - Helper y layout del formulario
    def __init__(self, *args, **kwargs):
        super(ActualizacionIncidenciaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        # UD4.4e - Fila 1: incidencia, autor y estado. Fila 2: mensaje a lo ancho
        self.helper.layout = Layout(
            Div(
                Div(Field('incidencia'), css_class='col-6'),
                Div(Field('autor'), css_class='col-3'),
                Div(Field('estado'), css_class='col-3'),
                css_class='row'
            ),
            Div(
                Div(Field('mensaje'), css_class='col-12'),
                css_class='row'
            ),
        )