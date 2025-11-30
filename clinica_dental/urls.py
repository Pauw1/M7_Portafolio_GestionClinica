from django.contrib import admin
from django.urls import path, include
from core.views import ficha_paciente, dashboard_dentista # Eliminamos el import de redirect, ya no se usa aquí

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', dashboard_dentista, name='dashboard'), # La nueva raíz
    
    # RUTA CORREGIDA: Agregué la coma al final (,) y eliminé la duplicidad de paths.
    path('paciente/<int:id>/', ficha_paciente, name='detalle_paciente'), 
    
    # Incluye las URLs de autenticación de Django una sola vez
    path('accounts/', include('django.contrib.auth.urls')), 
]