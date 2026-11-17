from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect


# UD4.2d - Mixin que pasa por contexto las variables de base_create_update.html
class CreateUpdateMixin(SuccessMessageMixin):
    template_name = 'common/base_create_update.html'
    titulo_creacion = None
    titulo_actualizacion = None
    url_borrado = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_creacion'] = self.titulo_creacion
        context['titulo_actualizacion'] = self.titulo_actualizacion
        context['url_borrado'] = self.url_borrado
        return context


# UD4.2f - Mixin de borrado: pasa el contexto y avisa si el objeto tiene dependencias
class BorradoMixin:
    template_name = 'common/base_confirm_delete.html'
    titulo = None
    mensaje_confirmación = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = self.titulo
        context['mensaje_confirmación'] = self.mensaje_confirmación
        return context

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            # UD4.2f - Mensaje construido con la representación textual del objeto
            messages.error(
                self.request,
                'Existen dependencias para el objeto {}. Elimine antes dichas dependencias'.format(str(self.object))
            )
            return HttpResponseRedirect(self.request.path)
        
        
# UD4.2i - Permite reordenar un listado por id con el parámetro ordering de la URL
class OrdenacionMixin:

    def get_queryset(self):
        queryset = super().get_queryset()
        ordering = self.request.GET.get('ordering')

        if ordering == 'asc':
            queryset = queryset.order_by('id')
        elif ordering == 'desc':
            queryset = queryset.order_by('-id')

        return queryset