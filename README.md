# 📋 Gestor de Tareas Avanzado

![Django](https://img.shields.io/badge/Django-5.x-092E20?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?logo=postgresql&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.x-06B6D4?logo=tailwindcss&logoColor=white)
![Render](https://img.shields.io/badge/Deploy-Render-46E3B7?logo=render&logoColor=black)
![Resend](https://img.shields.io/badge/Email-Resend-000000)
![License](https://img.shields.io/badge/License-MIT-green)

Aplicación tipo **Trello minimalista y moderna**, desarrollada con Django y PostgreSQL.  
Diseñada para escalar a usuarios reales en producción.

---

# ✨ Features

- 🔐 Autenticación de usuarios
- 👥 Boards colaborativos con miembros
- 🗂 Columnas reordenables (Drag & Drop)
- 🎯 Tareas movibles entre columnas
- 🔄 Persistencia de orden en base de datos
- 📊 Dashboard con progreso por board
- 📤 Exportación de tareas a CSV
- 📬 Envío de emails con Resend
- 🎨 Interfaz moderna con TailwindCSS
- 🛡 Control de permisos por usuario

---

# 🛠 Stack Tecnológico

- **Backend:** Django
- **Base de datos:** PostgreSQL
- **Frontend:** TailwindCSS
- **Servidor:** Gunicorn
- **Deploy:** Render
- **Email:** Resend API

---

# 🧑‍💻 Instalación Completa en Local

---

## 1️⃣ Clonar repositorio

```bash
git clone https://github.com/tuusuario/gestor-tareas.git
cd gestor-tareas
```

---

## 2️⃣ Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux

# En Windows
venv\Scripts\activate
```

---

## 3️⃣ Instalar dependencias Python

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Instalar PostgreSQL

### Opción A — Instalación local

Instala PostgreSQL desde:
https://www.postgresql.org/download/

Crear base de datos:

```bash
psql -U postgres
```

```sql
CREATE DATABASE gestor;
CREATE USER gestor_user WITH PASSWORD 'password';
ALTER ROLE gestor_user SET client_encoding TO 'utf8';
ALTER ROLE gestor_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE gestor_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE gestor TO gestor_user;
```

---

### Opción B — Con Docker (Recomendado)

```bash
docker run --name postgres-gestor \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=gestor \
  -p 5432:5432 \
  -d postgres:15
```

---

## 5️⃣ Configurar Variables de Entorno

Crea un archivo `.env` o exporta variables:

```bash
export SECRET_KEY="tu_secret_key"
export DEBUG=True
export DATABASE_URL="postgres://postgres:postgres@localhost:5432/gestor"
export RESEND_API_KEY="re_xxxxxxxxxxxxx"
```

---

## 6️⃣ Configuración DATABASE en settings.py

```python
import dj_database_url
import os

DATABASES = {
    "default": dj_database_url.config(default=os.environ.get("DATABASE_URL"))
}
```

---

## 7️⃣ Migraciones

```bash
python manage.py migrate
```

---

## 8️⃣ Crear superusuario

```bash
python manage.py createsuperuser
```

---

# 🎨 Configuración de Tailwind

---

## 9️⃣ Instalar Node (si no lo tienes)

Descargar desde:
https://nodejs.org

Verificar instalación:

```bash
node -v
npm -v
```

---

## 🔟 Instalar dependencias Tailwind

```bash
cd theme
npm install
cd ..
```

---

## 1️⃣1️⃣ Build Tailwind

```bash
python manage.py tailwind build
```

---

# 🚀 Ejecutar el Proyecto

```bash
python manage.py runserver
```

Acceder a:

```
http://127.0.0.1:8000
```

# ☁️ Deploy en Render

---

## Crear Web Service en Render

- Runtime: Python
- Conectar repositorio GitHub
- Añadir base de datos PostgreSQL en Render

---

## Variables de entorno en Render

- `SECRET_KEY`
- `DEBUG=False`
- `DATABASE_URL`
- `RESEND_API_KEY`

---

## Build Command

```bash
pip install -r requirements.txt
cd theme
npm install
cd ..
python manage.py tailwind build
python manage.py collectstatic --noinput
```

---

## Start Command

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

---

# 📊 Arquitectura del Proyecto

```
User
 ├── Boards
 │     ├── TaskLists
 │     │       ├── Tasks
 │     │
 │     └── Members
```

---

# 🔐 Seguridad Implementada

- LoginRequiredMixin
- Validación de miembros en cada vista sensible
- Método `board.user_has_access(user)`
- Protección CSRF
- Transacciones atómicas en movimientos
- Control de acceso en Drag & Drop

---

# 📈 Roadmap

- 🔔 Notificaciones en tiempo real
- 📅 Fechas límite y recordatorios
- 📱 Versión mobile optimizada
- 📊 Métricas avanzadas
- 🧠 Sistema de prioridades

---

# 📄 Licencia

MIT License