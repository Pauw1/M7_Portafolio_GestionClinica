from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from .models import Paciente

def ficha_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    # Intenta obtener la ficha relacionada; si no existe, devuelve None
    ficha = getattr(paciente, 'ficha', None)

    context = {'paciente': paciente, 'ficha': ficha}

    if ficha:
        tratamientos = ficha.tratamientos.all()
        
        # Cálculos Financieros
        # Suma costos excluyendo los 'PREVIO'
        total_presupuesto = tratamientos.exclude(estado='PREVIO').aggregate(Sum('costo'))['costo__sum'] or 0
        
        # Suma costos pagados excluyendo 'PREVIO'
        total_pagado = tratamientos.filter(pagado=True).exclude(estado='PREVIO').aggregate(Sum('costo'))['costo__sum'] or 0
        
        deuda_actual = total_presupuesto - total_pagado

        # Obtener lista de dentistas únicos del historial
        dentistas_historicos = ficha.evoluciones.values_list('dentista__usuario__last_name', flat=True).distinct()

        context.update({
            'tratamientos': tratamientos,
            'tratamientos_pendientes': tratamientos.filter(estado='PENDIENTE'),
            'tratamientos_previos': tratamientos.filter(estado='PREVIO'),
            'dentistas_historicos': dentistas_historicos,
            'evoluciones': ficha.evoluciones.all().order_by('-fecha'),
            'finanzas': {
                'presupuesto': total_presupuesto,
                'pagado': total_pagado,
                'deuda': deuda_actual
            }
        })
        
    return render(request, 'core/ficha.html', context)