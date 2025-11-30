from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Sum  # <--- IMPORTANTE: Necesario para los cálculos

# --- Entidades Base ---
class TarifaInsumo(models.Model):
    nombre = models.CharField(max_length=100)
    costo_base = models.DecimalField(max_digits=10, decimal_places=0)
    stock = models.IntegerField(default=0)
    def __str__(self): return self.nombre

class Dentista(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    especialidad = models.CharField(max_length=100)
    def __str__(self): return f"Dr. {self.usuario.last_name}"

class Paciente(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    def __str__(self): return f"{self.nombre} ({self.rut})"

# --- FICHA CLÍNICA (Ahora con superpoderes) ---
class FichaClinica(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE, related_name='ficha')
    antecedentes = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # --- REFACTORIZACIÓN: Métodos de Negocio ---
    def calcular_presupuesto(self):
        """Calcula el total de tratamientos activos (no previos)."""
        return self.tratamientos.exclude(estado='PREVIO').aggregate(Sum('costo'))['costo__sum'] or 0

    def calcular_pagado(self):
        """Calcula cuánto ha abonado el paciente efectivamente."""
        return self.tratamientos.filter(pagado=True).exclude(estado='PREVIO').aggregate(Sum('costo'))['costo__sum'] or 0

    def calcular_deuda(self):
        """Calcula la deuda final."""
        return self.calcular_presupuesto() - self.calcular_pagado()

    def __str__(self):
        return f"Ficha: {self.paciente.nombre}"

# --- TRATAMIENTOS ---
class Tratamiento(models.Model):
    ESTADOS = [('PREVIO', 'Previo'), ('PENDIENTE', 'Pendiente'), ('REALIZADO', 'Realizado')]
    ficha = models.ForeignKey(FichaClinica, on_delete=models.CASCADE, related_name='tratamientos')
    nombre = models.CharField(max_length=200)
    costo = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    pagado = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # MEJORA: Validación de seguridad de datos
        if self.costo < 0:
            raise ValidationError("El costo no puede ser negativo")
        
        # Regla de negocio: Previos siempre están pagados (históricos)
        if self.estado == 'PREVIO':
            self.pagado = True 
        super().save(*args, **kwargs)

    def __str__(self): return self.nombre

# --- EVOLUCIÓN ---
class Evolucion(models.Model):
    ficha = models.ForeignKey(FichaClinica, on_delete=models.CASCADE, related_name='evoluciones')
    dentista = models.ForeignKey(Dentista, on_delete=models.PROTECT)
    fecha = models.DateTimeField(auto_now_add=True)
    nota_clinica = models.TextField()
    bloqueado = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk and self.bloqueado:
            raise ValidationError("Registro cerrado por seguridad legal.")
        super().save(*args, **kwargs)

    def __str__(self): return f"Evolución {self.fecha}"

class Cita(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    dentista = models.ForeignKey(Dentista, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    motivo = models.CharField(max_length=200)