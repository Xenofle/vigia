EJECUTAR_ALTAS = False
EJECUTAR_MODIFICACIONES = False
EJECUTAR_BORRADOS = True
 
 
from billing.models import Cliente, Cobro, Factura
from common import actividadorm
 
 
def titulo(numero, texto):
    print()
    print('=' * 70)
    print(f'Metodo {numero} - {texto}')
    print('-' * 70)
 
 
def mostrar(resultado):
    """Imprime un queryset línea a línea, o un objeto suelto."""
    if hasattr(resultado, 'count'):
        for elemento in resultado:
            print('  ', elemento)
        print('   Total:', resultado.count())
    else:
        print('  ', resultado, '  (objeto:', type(resultado).__name__, ')')
 
 
# ----------------------------------------------------------------------
# FASE 1 - Consultas. No modifican nada, se pueden repetir sin problema.
# ----------------------------------------------------------------------
 
titulo(1, 'Todos los clientes')
mostrar(actividadorm.get_clientes_all())
 
titulo(2, 'Las 3 primeras facturas')
mostrar(actividadorm.get_factura_first_3())
 
titulo(3, 'Facturas de importe 0')
mostrar(actividadorm.get_factura_0())
 
titulo(4, 'Clientes excluyendo los de DNI que empieza por 74')
mostrar(actividadorm.get_cliente_not_0612())
 
titulo(5, 'Cliente con DNI 92436593F y apellidos con Perez')
mostrar(actividadorm.get_cliente_dni_apellido())
 
titulo(6, 'Facturas con id menor que 2, por numero descendente')
mostrar(actividadorm.get_cli_id_lt_2_num_fact_des())
 
titulo(7, 'Clientes con id mayor que 2')
mostrar(actividadorm.get_cli_id_gt_2())
 
titulo(8, 'Facturas con PHP en el concepto, por numero ascendente')
mostrar(actividadorm.get_fact_des_nom_des())
 
titulo(9, 'Facturas excluyendo las que acaban en 1')
mostrar(actividadorm.get_fact_not_1())
 
titulo(10, 'Primer cobro de factura con python y con id acabado en 2')
mostrar(actividadorm.get_cobro_python_id2())
 
titulo(11, 'Cobros de facturas con 06, excluyendo al cliente Manu')
mostrar(actividadorm.get_cobro_fact6_not_manu())
 
titulo(12, 'Facturas con importe mayor o igual a 5')
mostrar(actividadorm.get_fact_gt_5())
 
titulo(13, 'Cobros con importe entre 5 y 10')
mostrar(actividadorm.get_cobro_5_10())
 
 
# Altas.
 
if EJECUTAR_ALTAS:
    titulo(14, 'Crear cliente')
    cliente_nuevo = actividadorm.create_cliente()
    print('  ', cliente_nuevo, '| id:', cliente_nuevo.id)
 
    titulo(15, 'Crear factura con fecha de ayer')
    factura_nueva = actividadorm.create_factura()
    print('  ', factura_nueva, '| fecha:', factura_nueva.fecha, '| total:', factura_nueva.total)
else:
    print()
    print('FASE 2 (altas) desactivada.')
 
 
# Modificaciones
 
if EJECUTAR_MODIFICACIONES:
    titulo(16, 'Anadir (ultima) al concepto de la ultima factura')
    print('   Antes: ', Factura.objects.last().concepto)
    actividadorm.update_last_factura()
    print('   Despues:', Factura.objects.last().concepto)
 
    titulo(17, 'Duplicar importes de cobros de facturas acabadas en 2')
    print('   Antes:')
    for cobro in Cobro.objects.filter(factura__num_factura__endswith='2'):
        print('    ', cobro.factura.num_factura, cobro.importe)
    print('   Cobros modificados:', actividadorm.update_cobro_fact2_x2())
    print('   Despues:')
    for cobro in Cobro.objects.filter(factura__num_factura__endswith='2'):
        print('    ', cobro.factura.num_factura, cobro.importe)
 
    titulo(18, 'Dividir entre 2 los cobros de facturas acabadas en 1 de clientes Gonzalez')
    print('   Antes:')
    for cobro in Cobro.objects.filter(factura__num_factura__endswith='1'):
        print('    ', cobro.factura.num_factura, cobro.factura.cliente.apellidos, cobro.importe)
    print('   Cobros modificados:', actividadorm.update_cobro_fact1_cligonz_div2())
    print('   Despues:')
    for cobro in Cobro.objects.filter(factura__num_factura__endswith='1'):
        print('    ', cobro.factura.num_factura, cobro.factura.cliente.apellidos, cobro.importe)
else:
    print()
    print('FASE 3 (modificaciones) desactivada.')
 
 
# Borrados
 
if EJECUTAR_BORRADOS:
    titulo(19, 'Borrar cobros de facturas con importe menor que 1')
    print('   Cobros antes: ', Cobro.objects.count())
    print('   Resultado:    ', actividadorm.delete_cobro_fact_lt_1())
    print('   Cobros despues:', Cobro.objects.count())
 
    titulo(20, 'Borrar cobros de facturas de clientes Pablo')
    print('   Cobros antes: ', Cobro.objects.count())
    print('   Resultado:    ', actividadorm.delete_cobro_cli_pablo())
    print('   Cobros despues:', Cobro.objects.count())
else:
    print()
    print('FASE 4 (borrados) desactivada.')
 
 
print()
print('=' * 70)
print('Fin del guion de pruebas.')