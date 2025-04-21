# MiniCore 

Este proyecto es una aplicación Python lista para ser desplegada en [Render.com](https://render.com).

## Despliegue en Render

### 1. Clonar el repositorio en GitHub
Sube este proyecto a un repositorio público o privado.

### 2. Crear nuevo Web Service en Render

- Ingresa a [Render Dashboard](https://dashboard.render.com/)
- Haz clic en **"New Web Service"**
- Conecta tu cuenta de GitHub y selecciona el repositorio del proyecto.

### 3. Configura el Servicio

- **Build Command**: *(dejar vacío o usar `pip install -r requirements.txt` si te lo pide Render)*
- **Start Command**:  
  ```bash
  gunicorn main:app --bind 0.0.0.0:10000
