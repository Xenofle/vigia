from datetime import date
from django.db import models

# UD3.3a - Modelo Cliente: persona o entidad a la que se emiten facturas
class Cliente(models.Model):
    nombre = models.CharField(verbose_name='Nombre', max_length=256)
    apellidos = models.CharField(verbose_name='Apellidos', max_length=512)
    nif = models.CharField(verbose_name='NIF', max_length=20)
    email = models.EmailField(verbose_name='Correo electrónico')

    class Meta:
        # UD3.4e - Nombre singular y plural del modelo en el administrador
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        # UD3.4f - Ordenación por defecto de los registros
        ordering = ['apellidos', 'nombre']
        # UD3.3c - Restricciones de unicidad del modelo
        unique_together = [['nif'], ['email']]

    # UD3.3b - Representación textual del cliente
    def __str__(self):
        return self.nombre + ' ' + self.apellidos + ' (' + self.nif + ')'
   
# UD3.3a - Modelo Factura: documento de cobro emitido a un cliente
class Factura(models.Model):

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, verbose_name='Cliente')
    num_factura = models.CharField(verbose_name='N.º factura', max_length=20)
    concepto = models.TextField(verbose_name='Concepto')
    fecha = models.DateField(verbose_name='Fecha', default=date.today)
    total = models.DecimalField(verbose_name='Total', max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        # UD3.4e - Nombre singular y plural del modelo en el administrador
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        # UD3.4f - Ordenación por defecto de los registros
        ordering = ['num_factura']
        # UD3.3c - Restricción de unicidad del número de factura
        unique_together = [['num_factura']]

    # UD3.3b - Representación textual: cliente y número de factura
    def __str__(self):
        return str(self.cliente) + ' - ' + self.num_factura
    
# UD3.3a - Modelo Cobro: pago, total o parcial, asociado a una factura
class Cobro(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.PROTECT, verbose_name='Factura')
    fecha = models.DateField(verbose_name='Fecha', default=date.today)
    importe = models.DecimalField(verbose_name='Importe', max_digits=10, decimal_places=2, default=0)

    class Meta:
        # UD3.4e - Nombre singular y plural del modelo en el administrador
        verbose_name = 'Cobro'
        verbose_name_plural = 'Cobros'
        # UD3.4f - Ordenación por defecto de los registros, del más reciente al más antiguo
        ordering = ['-fecha']

    # UD3.3b - Representación textual: número de factura e importe
    def __str__(self):
        return self.factura.num_factura + ' - ' + str(self.importe)