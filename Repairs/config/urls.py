
from django.contrib import admin
from django.urls import path, include
from RepairApp import views

urlpatterns = [
    path('', admin.site.urls),
    path('/', include('jet.urls', 'jet')),
    #path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('report/', views.ReportePersonasPDF.as_view(), name="producto.pdf" )]
    
