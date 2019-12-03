from django.shortcuts import render
from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas
from django.views.generic import View
from .models import *
from reportlab import *
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, TA_CENTER
from reportlab.lib.units import inch, mm, cm
from reportlab.lib import colors
from reportlab.platypus import (
        Paragraph,
        Table,
        SimpleDocTemplate,
        Spacer,
        TableStyle,
        Paragraph)
from .models import Producto
from django.http import HttpResponse

def detailPdf(request, id, *args, **kwargs):
    queryset = Vehiculo.objects.filter(id=id)
    print(queryset)
    return renderizar_pdf('pdf.html', queryset)

class ReportePersonasPDF(View):
    def renombrar(self,x):
        estado_p = ""
        if x == "1":
            estado_p = 'Ingresado'
        elif x == "2":
            estado_p = 'Diagnosticando'
        elif x == "3":
            estado_p = 'Esperando aprobacion'
        elif x == "4":
            estado_p = 'Aprobado'
        elif x == "5":
            estado_p = 'No aprobado'
        elif x == "6":
            estado_p = 'Esperando repuestos'
        elif x == "7":
            estado_p = 'Reparando'
        elif x == "8":
            estado_p = 'Lista'
        elif x == "9":
            estado_p = 'Entregada'
        elif x == "10":
            estado_p = 'Entregada sin reparar'
        return estado_p

    def cabecera(self,pdf):
        #Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
        pdf.setFont("Helvetica", 16)
        #Dibujamos una cadena en la ubicación X,Y especificada
        pdf.setFont("Helvetica", 14)
        pdf.drawString(200, 770, u"REPORTE DE PRODUCTOS")



    def tabla(self,pdf,y):
        data = [["Dueño","Nombre","Modelo","Estado"]] \
        +[[x.sucursal_o_particular, x.nombre, x.modelo, self.renombrar(x.estado)]
        for x in Producto.objects.all()]

        detalle_orden = Table(data, colWidths=[5 * cm, 5 * cm, 5 * cm, 5 * cm])
        #Aplicamos estilos a las celdas de la tabla
        detalle_orden.setStyle(TableStyle(
        [
                #La primera fila(encabezados) va a estar centrada
                ('ALIGN',(0,0),(3,0),'CENTER'),
                #Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                #El tamaño de las letras de cada una de las celdas será de 10
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ]
        ))
        #Establecemos el tamaño de la hoja que ocupará la tabla
        detalle_orden.wrapOn(pdf, 600, 600)
        #Definimos la coordenada donde se dibujará la tabla
        detalle_orden.drawOn(pdf, 13, y)

    def get(self, request):
            #Indicamos el tipo de contenido a devolver, en este caso un pdf
            response = HttpResponse(content_type='application/pdf')
            #La clase io.BytesIO permite tratar un array de bytes como un fichero bi./nario, se utiliza como almacenamiento temporal
            buffer = BytesIO()
            #Canvas nos permite hacer el reporte con coordenadas X y Y
            pdf = canvas.Canvas(buffer)
            #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
            self.cabecera(pdf)
            y = 600
            self.tabla(pdf, y)
            #Con show page hacemos un corte de página para pasar a la siguiente
            pdf.showPage()
            pdf.save()
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            return response