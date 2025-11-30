from django.contrib import admin
from django.urls import path
from core.views import ficha_paciente, dashboard_dentista

urlpatterns = [
    path('admin/', admin.site.urls),
    # Ruta raíz lleva al dashboard
    path('', dashboard_dentista, name='dashboard'),
    path('paciente/<int:id>/', ficha_paciente, name='detalle_paciente'),
]