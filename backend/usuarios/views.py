from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import FormView

from usuarios.forms import LoginForm


# UD5.2 - Pantalla de acceso a la aplicación
class LoginView(FormView):
    template_name = 'usuarios/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('panel')

    def form_valid(self, form):
        usuario = authenticate(
            self.request,
            username=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
        )

        if usuario is None:
            messages.error(self.request, 'Correo electrónico o contraseña incorrectos.')
            return super().form_invalid(form)

        login(self.request, usuario)
        return super().form_valid(form)


# UD5.2 - Cierre de sesión
class LogoutView(View):

    def post(self, request):
        logout(request)
        messages.success(request, 'Sesión cerrada correctamente.')
        return redirect('login')
