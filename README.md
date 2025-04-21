# MiniCore - Sistema de Filtrado de Tareas Atrasadas

MiniCore es una aplicación web construida con FastAPI (backend) y React + Material UI (frontend), que permite filtrar tareas en estado "In progress" dentro de un rango de fechas determinado. También se despliega de forma profesional en [Render.com](https://render.com) como Web Service (backend) y Static Site (frontend).

## Tecnologías Usadas
- Backend: Python 3.11, FastAPI, Uvicorn, SQLite, SQLAlchemy

- Frontend: React 19, Material UI, Axios

- Despliegue: Render.com (Web Service + Static Site)

```bash
MiniCore/
├── backend/
│   ├── main.py
│   ├── db/
│   │   ├── db.py                # Modelos SQLAlchemy
│   │   ├── db_connection.py     # Configuración de la BD SQLite
│   │   └── data.sql   # Datos masivos a insertar automáticamente
│   │── requirements.txt  # Dependencias de Python para el backend
├── frontend/
│   ├── public/
│   ├── src/
│   │   └── components/
│   │       └── TaskFilter.jsx   # Componente principal de filtrado
│   │   └── App.jsx              # Componente raíz
│   └── package.json             # Scripts, dependencias y configuración
├── README.md          
```

### 1. Clonar el repositorio de GitHub
Importar el proyecto al IDE de preferencia del [repositorio](https://github.com/joaquincgp/MiniCore---FastApi-React/)

### 2. Backend (FastAPI)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # o .venv\Scripts\activate en Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

Esto crea la base de datos MiniCore.db y ejecuta automáticamente el archivo data.sql al levantar el servidor.

### 3. Frontend (React)
```bash
cd frontend
npm install
npm start 

```
## Despliegue en Render

**Backend - Web Service**

- Tipo: Web Service

- Branch: master

- Root Directory: *`backend`*

Build Command:
- Ingresa a [Render Dashboard](https://dashboard.render.com/)
- Haz clic en **"New Web Service"**
- Conectar a la cuenta de GitHub y seleccionar el repositorio del proyecto.

### 3. Configura el Servicio

- **Build Command**: *`pip install -r requirements.txt`*
- **Start Command**:  
  ```bash
  uvicorn main:app --host 0.0.0.0 --port 8000
    ```

Exposición: https://minicore-fastapi-react.onrender.com


**Frontend - Static Site**

- Tipo: Static Site

- Root Directory: *`frontend`*

- **Build Command**:  *`npm install && npm run build`*
- **Publish Directory**: *`build`*

Exposición: https://minicore-fastapi-react-1.onrender.com
 
## Uso de la App

Ingresa un rango de fechas en el formulario del frontend.

Al hacer clic en "Filtrar", se envía una solicitud POST al backend:

`POST /api/filter-inprogress-tasks*npm install && npm run build`

El backend consulta todas las tareas con estado "In progress" que estén dentro del rango y calcula días de retraso.

El frontend renderiza la tabla con los resultados.

## 👨 Autor

Joaquin Chacon — 2025

Proyecto académico para prácticas de desarrollo web moderno y despliegue en la nube con Render.