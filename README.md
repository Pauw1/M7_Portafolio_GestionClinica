Sistema de Gestión Clínica Dental (Versión Mejorada M8_AE2)

Rama de Desarrollo M8: Esta versión incluye refactorización de código, mejoras de seguridad y una nueva interfaz de usuario respecto a la entrega del Módulo 7.

📋 Descripción del Proyecto

Este sistema es una solución web integral desarrollada con Django y PostgreSQL para la administración de una clínica dental. Permite la gestión de pacientes, fichas clínicas con historial inmutable y control financiero automático.

La versión actual (M8) se enfoca en la calidad del software, separando la lógica de negocio de la interfaz y mejorando la experiencia del usuario profesional (Dentistas).

✨ Nuevas Funcionalidades (Mejoras M8)

1. Dashboard de Gestión (Portal del Dentista) 🦷

Se eliminó la dependencia del Panel de Administración para los dentistas. Ahora cuentan con un Dashboard exclusivo (/) que ofrece:

Agenda Inteligente: Visualización inmediata de citas pendientes y futuras.

Pacientes Asignados: Filtro automático para ver solo los pacientes a cargo del profesional logueado.

Accesos Rápidos: Botones directos para agendar o registrar pacientes.

2. Refactorización de Arquitectura (Backend) 🛠️

Se aplicó el principio de "Fat Models, Thin Views":

Antes (M7): La vista calculaba deudas, sumaba pagos y filtraba tratamientos manualmente.

Ahora (M8): El modelo FichaClinica posee métodos propios (calcular_deuda(), calcular_presupuesto()) que encapsulan esta lógica, haciendo el código más limpio, reutilizable y fácil de testear.

3. Seguridad y Control de Acceso 🔒

Protección de Rutas: Se implementó el decorador @login_required en todas las vistas sensibles. Ya no es posible acceder a una ficha clínica copiando la URL si no se ha iniciado sesión.

Integridad de Datos: Se agregaron validaciones para impedir costos negativos y modificaciones en historiales clínicos cerrados (Epicrisis).

🛠️ Tecnologías Utilizadas

Backend: Python, Django 5.x

Base de Datos: PostgreSQL

Frontend: HTML5, CSS3, Bootstrap 5 (Responsive)

Control de Versiones: Git (Manejo de ramas main vs mejora-m8)

🚀 Instalación y Despliegue

Sigue estos pasos para probar la versión mejorada en tu entorno local:

Clonar el repositorio (Rama específica):

git clone -b mejora-m8 [https://github.com/TU_USUARIO/TU_REPO.git](https://github.com/TU_USUARIO/TU_REPO.git)
cd TU_REPO


Configurar entorno virtual:

python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate


Instalar dependencias:

pip install django psycopg2-binary


Configurar Base de Datos:

Asegúrate de tener PostgreSQL corriendo y una base de datos creada.

Verifica las credenciales en clinica_dental/settings.py.

Ejecutar migraciones y servidor:

python manage.py migrate
python manage.py createsuperuser  # Para crear el primer dentista/admin
python manage.py runserver


Acceso:

Ve a http://127.0.0.1:8000/.

Inicia sesión con tus credenciales.

¡Verás el nuevo Dashboard!

Autor: [Tu Nombre]
Módulo: Calidad de Software y Mejora Continua (M8)
