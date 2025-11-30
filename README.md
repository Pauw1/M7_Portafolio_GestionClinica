# Sistema de Gestión Clínica Dental - Portafolio Django

## 1. Descripción del Proyecto
Sistema para la gestión integral de pacientes, historiales clínicos inmutables, control financiero y agenda de citas.

## 2. Integración de Django con Bases de Datos
Django utiliza un ORM (Object-Relational Mapping) que actúa como capa de abstracción.
* **Configuración:** En `settings.py`, la variable `DATABASES` define el motor (PostgreSQL en este caso), nombre, usuario y host. Django gestiona el pool de conexiones automáticamente.
* **Operaciones:** A través del ORM, interactuamos con clases Python (Modelos) en lugar de escribir SQL crudo, lo que aporta seguridad y portabilidad.

## 3. Implementación de Modelos
* **Entidades Simples:** Modelo `TarifaInsumo` para tablas independientes.
* **Relaciones:**
    * **1 a 1:** `Paciente` <-> `FichaClinica` (Un paciente tiene una única ficha).
    * **1 a Muchos:** `FichaClinica` <-> `Tratamiento` (Una ficha tiene múltiples tratamientos).
    * **Muchos a Muchos:** Implícita en la gestión de citas y asignaciones.

## 4. Consultas y Filtrado (ORM)
Se implementaron consultas avanzadas en `views.py`:
* **Filter:** Para separar tratamientos pendientes de realizados.
* **Exclude:** Para ignorar tratamientos previos en el cálculo de deuda.
* **Aggregate (Sum):** Para calcular totales monetarios teóricos y reales.

## 5. Aplicaciones Preinstaladas
* **django.contrib.admin:** Utilizado para gestionar el back-office de la clínica. Se personalizaron permisos de solo lectura para el historial clínico.
* **django.contrib.auth:** Gestión de acceso para los dentistas.

## 6. Instrucciones de Instalación
1. Clonar repositorio.
2. Crear entorno virtual.
3. Configurar `.env` con credenciales de BD.
4. `python manage.py migrate`
5. `python manage.py runserver`