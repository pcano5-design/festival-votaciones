# Sistema Web de Votaciones – Festival de la Leyenda Vallenata 2027

Proyecto académico de **Desarrollo Web** (Fundación Universitaria del Área Andina) – **Entrega 2: desarrollo inicial**.

Aplicación web construida con **Python 3.12, Django 5.2 (patrón MVT) y MySQL 8.0**.

**Integrantes:** Paula Andrea Cano Calvo · Paula Catalina Hincapié Huertas · Jesús Daniel Vega Jiménez · Eliezer Omar Vielma Castro

**Tutor:** Deivys Morales Uribe

---

## Funcionalidades de esta entrega

| Funcionalidad | Dirección |
|---|---|
| Lista pública de ediciones del festival | `/` |
| Detalle de una edición: categorías y votaciones publicadas | `/edicion/<año>/` |
| Detalle de una votación con sus opciones | `/votacion/<id>/` |
| Registro de usuarios | `/cuentas/registro/` |
| Inicio y cierre de sesión | `/cuentas/login/` y botón *Cerrar sesión* |
| Página protegida (solo con sesión iniciada) | `/cuentas/perfil/` |
| Administración de ediciones, categorías, votaciones y opciones | `/admin/` |

Las votaciones en estado **borrador** no se muestran al público, ni siquiera escribiendo la dirección a mano.

## Modelo de datos

```
Edicion ──1:N──► Categoria ──1:N──► Votacion ──1:N──► Opcion
```

- Una **categoría** pertenece a una edición y una **votación** pertenece a una categoría (`PROTECT`: no se pueden borrar si tienen datos asociados).
- Las **opciones** pertenecen a una votación (`CASCADE`: se borran con ella).
- No se repiten categorías en una misma edición ni opciones en una misma votación.

## Estructura del proyecto

```
festival-votaciones/
├── festival/        # Configuración del proyecto (settings.py, urls.py)
├── votaciones/      # App: modelos, vistas, rutas y plantillas del festival
├── cuentas/         # App: registro, inicio/cierre de sesión y perfil
├── templates/       # Plantilla base compartida (base.html)
├── requirements.txt # Dependencias
├── .env.example     # Plantilla de variables de entorno
└── manage.py
```

## Requisitos

- Python 3.12
- MySQL Server 8.0 y MySQL Workbench
- Git

## Instalación (Windows – Símbolo del sistema)

1. **Clonar el repositorio**
   ```
   git clone <URL-DEL-REPOSITORIO>
   cd festival-votaciones
   ```

2. **Crear y activar el entorno virtual**
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Instalar las dependencias**
   ```
   python -m pip install -r requirements.txt
   ```

4. **Crear la base de datos y el usuario en MySQL Workbench** (conectado como `root`), cambiando `CLAVE_SEGURA` por una contraseña propia:
   ```sql
   CREATE DATABASE festival_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'festival_user'@'localhost' IDENTIFIED BY 'CLAVE_SEGURA';
   GRANT ALL PRIVILEGES ON festival_db.* TO 'festival_user'@'localhost';
   GRANT ALL PRIVILEGES ON test_festival_db.* TO 'festival_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

5. **Configurar las variables de entorno:** copiar `.env.example` con el nombre `.env` y escribir la contraseña del paso 4 y una `SECRET_KEY` propia. Para generar una clave:
   ```
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

6. **Crear las tablas**
   ```
   python manage.py migrate
   ```

7. **Crear el usuario administrador**
   ```
   python manage.py createsuperuser
   ```

8. **Ejecutar el servidor**
   ```
   python manage.py runserver
   ```
   - Sitio público: http://127.0.0.1:8000/
   - Administración: http://127.0.0.1:8000/admin/

## Pruebas automáticas

```
python manage.py test
```

Se ejecutan 8 pruebas: ediciones visibles, ocultamiento de borradores (en la lista y por URL), validación de fechas, registro válido e inválido, página protegida, inicio y cierre de sesión.

## Seguridad

- La contraseña de MySQL y la `SECRET_KEY` se leen del archivo `.env`, que **no** se sube al repositorio (`.gitignore`).
- Django guarda las contraseñas de los usuarios cifradas (hash).
- Todos los formularios usan protección **CSRF** y el cierre de sesión se hace por **POST**.
- Los datos cargados son **ficticios** y solo sirven como prueba.

## Pendiente para la Entrega 3

Registro de votos, control de un voto por usuario, reglas de elegibilidad, publicación de resultados y auditoría.