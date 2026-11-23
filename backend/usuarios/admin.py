from django.contrib import admin

from usuarios.models import MyUser


# UD5.1 - Gestión del modelo de usuario en el administrador
@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_active', 'is_staff')
    list_display_links = ('email',)
    list_filter = ('is_active', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('create_date', 'update_date', 'last_login', 'password')