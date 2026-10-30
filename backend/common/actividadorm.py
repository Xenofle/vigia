
from datetime import date, timedelta
 
from django.db.models import F
 
from billing.models import Cliente, Cobro, Factura
 
 
# UD3.6a - Devuelve un queryset con todos los clientes
def get_clientes_all():
    return Cliente.objects.all()
 
 
# UD3.6a - Devuelve un queryset con las 3 primeras facturas
def get_factura_first_3():
    # La rodaja se aplica sobre el orden por defecto del modelo (num_factura)
    return Factura.objects.all()[:3]
 
 
# UD3.6a - Devuelve un queryset con las facturas de importe 0
def get_factura_0():
    return Factura.objects.filter(total=0)
 
 
# UD3.6a - Devuelve todos los clientes, excluyendo aquellos cuyo DNI empiece por "74"
# (el nombre del método procede del enunciado; la condición es la descrita en el anexo)
def get_cliente_not_0612():
    return Cliente.objects.exclude(nif__startswith='74')
 
 
# UD3.6a - Devuelve los clientes cuyo DNI sea 92436593F y cuyos apellidos contengan "Pérez"
def get_cliente_dni_apellido():
    # Dos condiciones en el mismo filter se combinan con un Y lógico
    return Cliente.objects.filter(nif='92436593F', apellidos__icontains='Pérez')
 
 
# UD3.6a - Devuelve las facturas cuyo id sea menor que 2, ordenadas por número de factura descendente
# (el nombre del método procede del enunciado, aunque la consulta devuelve facturas)
def get_cli_id_lt_2_num_fact_des():
    return Factura.objects.filter(id__lt=2).order_by('-num_factura')
 
 
# UD3.6a - Devuelve los clientes cuyo id sea mayor que 2
def get_cli_id_gt_2():
    return Cliente.objects.filter(id__gt=2)
 
 
# UD3.6a - Devuelve las facturas cuyo concepto contenga "PHP", ordenadas por número de factura ascendente
def get_fact_des_nom_des():
    return Factura.objects.filter(concepto__icontains='PHP').order_by('num_factura')
 
 
# UD3.6a - Devuelve todas las facturas, excluyendo aquellas cuyo número acabe en "1"
def get_fact_not_1():
    return Factura.objects.exclude(num_factura__endswith='1')
 
 
# UD3.6a - Devuelve el primer cobro (objeto, no queryset) cuya factura contenga "python"
# en el concepto y cuyo id de cobro acabe en "2"
def get_cobro_python_id2():
    # id es un entero: la base de datos lo convierte a texto para aplicar endswith
    return Cobro.objects.filter(
        factura__concepto__icontains='python',
        id__endswith='2',
    ).first()
 
 
# UD3.6a - Devuelve los cobros cuya factura contenga "06" en el número,
# excluyendo los del cliente cuyo nombre contenga "Manu"
def get_cobro_fact6_not_manu():
    # Dos saltos de relación: del cobro a la factura y de la factura al cliente
    return Cobro.objects.filter(
        factura__num_factura__icontains='06',
    ).exclude(
        factura__cliente__nombre__icontains='Manu',
    )
 
 
# UD3.6a - Devuelve las facturas con un importe mayor o igual a 5
def get_fact_gt_5():
    return Factura.objects.filter(total__gte=5)
 
 
# UD3.6a - Devuelve los cobros con un importe entre 5 y 10, ambos incluidos
def get_cobro_5_10():
    return Cobro.objects.filter(importe__range=(5, 10))
 
 
# UD3.6a - Crea un cliente con nombre "Nuevo", apellidos "apellido1 apellido2" y un DNI válido
def create_cliente():
    # El NIF y el correo son únicos: ejecutar el método dos veces provoca un error de integridad
    return Cliente.objects.create(
        nombre='Nuevo',
        apellidos='apellido1 apellido2',
        nif='12345678Z',
        email='nuevo.cliente@example.com',
    )
 
 
# UD3.6a - Crea una factura para el cliente anterior, con fecha de ayer e importe 100
def create_factura():
    cliente = Cliente.objects.filter(nombre='Nuevo').first()
    # La fecha de ayer se calcula, no se escribe
    ayer = date.today() - timedelta(days=1)
 
    return Factura.objects.create(
        cliente=cliente,
        num_factura='F-2026-100',
        concepto='Factura creada desde el ORM',
        fecha=ayer,
        total=100,
    )
 
 
# UD3.6a - Concatena el texto "(última)" al concepto de la última factura
def update_last_factura():
    # last() aplica el orden por defecto del modelo, que es el número de factura
    factura = Factura.objects.last()
    factura.concepto = factura.concepto + ' (última)'
    factura.save()
 
    return factura
 
 
# UD3.6a - Multiplica por 2 el importe de los cobros cuyas facturas acaben en "2"
def update_cobro_fact2_x2():
    # F permite operar sobre el valor actual del campo en una sola consulta,
    # sin recorrer los objetos en Python
    return Cobro.objects.filter(
        factura__num_factura__endswith='2',
    ).update(importe=F('importe') * 2)
 
 
# UD3.6a - Divide por 2 el importe de los cobros cuyas facturas acaben en "1"
# y cuyo cliente contenga "González" en los apellidos
def update_cobro_fact1_cligonz_div2():
    return Cobro.objects.filter(
        factura__num_factura__endswith='1',
        factura__cliente__apellidos__icontains='González',
    ).update(importe=F('importe') / 2)
 
 
# UD3.6a - Elimina los cobros cuyas facturas tengan un importe menor que 1
def delete_cobro_fact_lt_1():
    # delete() devuelve el número de objetos eliminados
    return Cobro.objects.filter(factura__total__lt=1).delete()
 
 
# UD3.6a - Elimina los cobros de las facturas cuyo cliente contenga "Pablo" en el nombre
def delete_cobro_cli_pablo():
    return Cobro.objects.filter(factura__cliente__nombre__icontains='Pablo').delete()