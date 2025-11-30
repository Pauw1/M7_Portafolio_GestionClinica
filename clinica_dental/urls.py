from django.contrib import admin
from django.urls import path
from core.views import ficha_paciente

urlpatterns = [
    path('admin/', admin.site.urls),
    path('paciente/<int:id>/', ficha_paciente, name='detalle_paciente'),
]