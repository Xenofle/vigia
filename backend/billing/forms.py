from django import forms
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field

from billing.models import Cliente, Factura, Cobro


# UD4.3a - Formulario del modelo Cliente
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellidos', 'nif', 'email']

    # UD4.4c - Helper y layout del formulario
    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False  # El elemento <form> ya está en la plantilla

        # UD4.4d - Fila 1: nombre 3, apellidos 6, NIF 3. Fila 2: email 12
        self.helper.layout = Layout(
            Div(
                Div(Field('nombre'), css_class='col-3'),
                Div(Field('apellidos'), css_class='col-6'),
                Div(Field('nif'), css_class='col-3'),
                css_class='row'
            ),
            Div(
                Div(Field('email'), css_class='col-12'),
                css_class='row'
            ),
        )


# UD4.3a - Formulario del modelo Factura
class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['cliente', 'num_factura', 'concepto', 'fecha', 'total']

    # UD4.3b - El total de la factura ha de ser mayor que 0
    def clean_total(self):
        total = self.cleaned_data['total']
        if total <= 0:
            raise ValidationError('El total de la factura ha de ser mayor que 0.')
        return total

    # UD4.4c - Helper y layout del formulario
    def __init__(self, *args, **kwargs):
        super(FacturaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        # UD4.4d - Fila 1: cliente. Fila 2: n.º factura, fecha y total a 4. Fila 3: concepto
        self.helper.layout = Layout(
            Div(
                Div(Field('cliente'), css_class='col-12'),
                css_class='row'
            ),
            Div(
                Div(Field('num_factura'), css_class='col-4'),
                Div(Field('fecha'), css_class='col-4'),
                Div(Field('total'), css_class='col-4'),
                css_class='row'
            ),
            Div(
                Div(Field('concepto'), css_class='col-12'),
                css_class='row'
            ),
        )


# UD4.3a - Formulario del modelo Cobro
class CobroForm(forms.ModelForm):
    class Meta:
        model = Cobro
        fields = ['factura', 'fecha', 'importe']

    # UD4.3b - El importe del cobro ha de ser mayor que 0
    def clean_importe(self):
        importe = self.cleaned_data['importe']
        if importe <= 0:
            raise ValidationError('El importe del cobro ha de ser mayor que 0.')
        return importe

    # UD4.4c - Helper y layout del formulario
    def __init__(self, *args, **kwargs):
        super(CobroForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        # UD4.4d - Fila 1: factura. Fila 2: fecha e importe a 6
        self.helper.layout = Layout(
            Div(
                Div(Field('factura'), css_class='col-12'),
                css_class='row'
            ),
            Div(
                Div(Field('fecha'), css_class='col-6'),
                Div(Field('importe'), css_class='col-6'),
                css_class='row'
            ),
        )