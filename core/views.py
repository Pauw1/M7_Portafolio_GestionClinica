from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Q, F
from .models import Paciente, FichaClinica, Tratamiento, Cita

def ficha_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    # 1. ORM: Obtener Ficha (Relación 1 a 1 inversa)
    # Usamos try/except o getattr por seguridad
    ficha = getattr(paciente, 'ficha', None)

    context = {'paciente': paciente, 'ficha': ficha}

    if ficha:
        # 2. ORM Filtrado: Tratamientos Pendientes vs Previos
        tratamientos_pendientes = ficha.tratamientos.filter(estado='PENDIENTE')
        tratamientos_previos = ficha.tratamientos.filter(estado='PREVIO')
        
        # 3. ORM Annotate/Aggregate: Calcular Deuda Financiera
        # Sumamos el costo de todo lo que NO está pagado y NO es previo
        deuda_total = ficha.tratamientos.filter(
            pagado=False
        ).exclude( # Requisito: uso de exclude()
            estado='PREVIO'
        ).aggregate(total=Sum('costo'))['total'] or 0
        
        # Dinero pagado
        pagado_total = ficha.tratamientos.filter(pagado=True).aggregate(total=Sum('costo'))['total'] or 0

        # 4. ORM Relaciones: Historial de Dentistas (Distinct)
        # Recuperamos los dentistas únicos que han escrito evoluciones en esta ficha
        dentistas_historicos = ficha.evoluciones.values_list('dentista__usuario__last_name', flat=True).distinct()

        context.update({
            'tratamientos_pendientes': tratamientos_pendientes,
            'tratamientos_previos': tratamientos_previos,
            'deuda_total': deuda_total,
            'pagado_total': pagado_total,
            'dentistas_historicos': dentistas_historicos,
            'evoluciones': ficha.evoluciones.all().order_by('-fecha')
        })

    return render(request, 'core/ficha_detalle.html', context)