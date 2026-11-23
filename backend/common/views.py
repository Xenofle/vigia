from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


# Página pública de bienvenida: no se protege
class HomeView(TemplateView):
    template_name = 'common/home.html'


# UD5.3 - El panel pertenece a la zona privada
@method_decorator(login_required, name='dispatch')
class PanelView(TemplateView):
    template_name = 'common/panel.html'