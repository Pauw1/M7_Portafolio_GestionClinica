from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# --- 1. ENTIDAD INDEPENDIENTE (El error estaba aquí, faltaba esto) ---
class TarifaInsumo(models.Model):
    nombre = models.CharField(max_length=100)
    costo_base = models.DecimalField(max_digits=10, decimal_places=0)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

# --- 2. PERSONAS ---
class Dentista(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    especialidad = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Dr. {self.usuario.last_name}"

class Paciente(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    
    def __str__(self):
        return f"{self.nombre} ({self.rut})"

# --- 3. FICHA CLÍNICA ---
class FichaClinica(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE, related_name='ficha')
    antecedentes = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ficha: {self.paciente.nombre}"

# --- 4. TRATAMIENTOS ---
class Tratamiento(models.Model):
    ESTADOS = [
        ('PREVIO', 'Tratamiento Previo (Existente)'),
        ('PENDIENTE', 'Pendiente (Por hacer)'),
        ('REALIZADO', 'Realizado'),
    ]
    ficha = models.ForeignKey(FichaClinica, on_delete=models.CASCADE, related_name='tratamientos')
    nombre = models.CharField(max_length=200)
    costo = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    pagado = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.estado == 'PREVIO':
            self.pagado = True 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} ({self.get_estado_display()})"

# --- 5. EVOLUCIÓN ---
class Evolucion(models.Model):
    ficha = models.ForeignKey(FichaClinica, on_delete=models.CASCADE, related_name='evoluciones')
    dentista = models.ForeignKey(Dentista, on_delete=models.PROTECT)
    fecha = models.DateTimeField(auto_now_add=True)
    nota_clinica = models.TextField()
    bloqueado = models.BooleanField(default=False, help_text="Si es True, no se puede editar")

    def save(self, *args, **kwargs):
        if self.pk and self.bloqueado:
            raise ValidationError("Esta evolución clínica está cerrada y no se puede editar.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Evolución {self.fecha.date()} - {self.dentista}"

class Cita(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    dentista = models.ForeignKey(Dentista, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    motivo = models.CharField(max_length=200)
    asistio = models.BooleanField(default=False)