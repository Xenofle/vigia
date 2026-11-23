from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


# UD5.1 - Manager que identifica al usuario por su correo electrónico
class MyUserManager(BaseUserManager):

    def create_user(self, email, password=None):
        """
        Crea y guarda un usuario con el correo y la contraseña indicados.
        """
        if not email:
            raise ValueError('Ha de proporcionar un e-mail válido')
        user = self.model(email=self.normalize_email(email))
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Crea y guarda un superusuario con el correo y la contraseña indicados.
        """
        if not email:
            raise ValueError('Ha de proporcionar un e-mail válido')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# UD5.1 - Modelo de usuario cuyo campo principal es el correo electrónico
class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        verbose_name='Nombre de usuario', max_length=150, null=True, blank=True
    )
    email = models.EmailField(verbose_name='Correo electrónico', unique=True)
    create_date = models.DateTimeField(verbose_name='Fecha de alta', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='Última modificación', auto_now=True)
    is_staff = models.BooleanField(verbose_name='Acceso al administrador', default=False)
    is_active = models.BooleanField(verbose_name='Activo', default=False)

    # UD5.1 - El correo sustituye al nombre de usuario como identificador
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['email']

    # UD5.1 - Representación textual del usuario
    def __str__(self):
        return self.email