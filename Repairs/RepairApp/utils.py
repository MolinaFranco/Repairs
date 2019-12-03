from RepairApp.models import Producto
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.forms.models import model_to_dict
from io import BytesIO
from django.http import HttpResponse


def renderizar_pdf(template, queryset):
    estados = {
        '1': 'Ingresado',
        '2': 'Diagnosticando',
        '3': 'Esperando aprobación',
        '4': 'Aprobado',
        '5': 'No aprobado',
        '6': 'Esperando repuestos',
        '7': 'Reparando',
        '8': 'Lista',
        '9': 'Entregada',
        '10': 'Entregada sin reparar'
    }
    template = get_template(template)
    serialized = []
    for obj in queryset:
        dict = model_to_dict(Producto.objects.get(id=obj.id))
        dict['cliente'] = obj.sucursal_o_particular
        dict['modelo'] = obj.modelo
        dict['estado'] = estados[obj.estado]
        dict['nombre'] = obj.nombre
        serialized.append(dict)
    html  = template.render({'objects': serialized})
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

    if not pdf.err:
        return HttpResponse(html)
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None