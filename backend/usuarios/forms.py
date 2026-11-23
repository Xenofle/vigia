from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field


# UD5.2 - Formulario de acceso: no gestiona ningún modelo, por eso hereda de Form
class LoginForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

    # UD5.2 - Helper y layout del formulario
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False  # El elemento <form> ya está en la plantilla

        self.helper.layout = Layout(
            Div(Div(Field('email'), css_class='col-12'), css_class='row'),
            Div(Div(Field('password'), css_class='col-12'), css_class='row'),
        )