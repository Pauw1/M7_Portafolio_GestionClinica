from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .models import Paciente, Cita, Dentista

@login_required
def dashboard_dentista(request):
    try:
        # Intentamos ver si el usuario logueado es un dentista
        dentista_actual = request.user.dentista
        # Si es dentista, filtramos SUS pacientes y SUS citas
        pacientes = Paciente.objects.filter(dentista_asignado=dentista_actual)
        citas_proximas = Cita.objects.filter(dentista=dentista_actual, asistio=False).order_by('fecha')
    except:
        # Si no es dentista (ej: es un superusuario administrador), mostramos todo
        pacientes = Paciente.objects.all()
        citas_proximas = Cita.objects.filter(asistio=False).order_by('fecha')

    return render(request, 'core/dashboard.html', {
        'pacientes': pacientes,
        'citas': citas_proximas
    })

@login_required
def ficha_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    ficha = getattr(paciente, 'ficha', None)
    
    context = {'paciente': paciente, 'ficha': ficha}
    
    if ficha:
        # Usamos los métodos del modelo (Refactorización limpia)
        total_presupuesto = ficha.calcular_presupuesto()
        total_pagado = ficha.calcular_pagado()
        deuda_actual = ficha.calcular_deuda()

        tratamientos = ficha.tratamientos.all()
        dentistas_historicos = ficha.evoluciones.values_list('dentista__usuario__last_name', flat=True).distinct()

        context.update({
            'tratamientos': tratamientos,
            'dentistas_historicos': dentistas_historicos,
            'evoluciones': ficha.evoluciones.all().order_by('-fecha'),
            'finanzas': {
                'presupuesto': total_presupuesto,
                'pagado': total_pagado,
                'deuda': deuda_actual
            }
        })
        
    return render(request, 'core/ficha.html', context)