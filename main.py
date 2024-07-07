from contextlib import asynccontextmanager
from typing import Annotated

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.sql import func
from db.db import Empleado, Proyecto, Tarea
import db.db as db
import db.db_connection as db_connection
from db.db_connection import db_dependency
from datetime import date, datetime, timedelta
import uvicorn
from fastapi import FastAPI, Form, status


@asynccontextmanager
async def lifespan(app: FastAPI):
    archivo_sql = "./db/data.sql"
    try:
        # Abrir el archivo SQL
        with open(archivo_sql, 'r') as file:
            sql_content = file.read()

        # Obtener la conexión de bajo nivel a SQLite
        connection = db_connection.engine.raw_connection()
        try:
            cursor = connection.cursor()
            cursor.executescript(sql_content)
            connection.commit()
        except Exception as e:
            print(f"Error al ejecutar el archivo SQL: {e}")
        finally:
            # Cerrar manualmente el cursor y la conexión
            cursor.close()
            connection.close()

        print("Archivo SQL ejecutado con éxito.")
    except Exception as e:
        print(f"Error al ejecutar el archivo SQL: {e}")
    finally:
        # Asegurarse de cerrar la conexión de alto nivel
        db_connection.engine.dispose()

    yield


app = FastAPI(lifespan=lifespan)


db.Base.metadata.create_all(bind=db_connection.engine)

templates = Jinja2Templates(directory="templates")


@app.get(
    "/filter-inprogress-tasks",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    description="Retorna el template con todas las tareas pasadas de su estimado que sigan IN Progress en el rango de fechas seleccionado.",
)
def filter_inprogress_tasks():

    return templates.TemplateResponse(
        "filter_inprogress_tasks.html",
        {
            "request": {
                "start_date": "",
                "end_date": "",
            },
            "tasks": [],
        },
    )


@app.post(
    "/filter-inprogress-tasks",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    description="Retorna el template con todas las tareas pasadas de su estimado que sigan IN Progress en el rango de fechas seleccionado.",
)
async def filter_inprogress_tasks(
    start_date: Annotated[date, Form(...)],
    end_date: Annotated[date, Form(...)],
    db: db_dependency
):
    # Une las tablas empleados, proyectos y taras
    result = db.query(
        Tarea.descripcion.label("descripcion"),
        Tarea.fecha_inicio.label("fecha_inicio"),
        Tarea.estado.label("estado"),
        Tarea.estimado.label("estimado"),
        Empleado.nombre.label("empleado_name"),
        Proyecto.nombre.label("proyecto_name"),
    ).join(Empleado).join(Proyecto).filter(
        Tarea.estado == "In progress",
    ).all()

    result = [
        {
            "empleado": tarea.empleado_name,
            "descripcion": tarea.descripcion,
            "fecha_inicio": tarea.fecha_inicio,
            "fecha_fin": tarea.fecha_inicio + timedelta(days=tarea.estimado),
            "dias_pasados": (end_date - (tarea.fecha_inicio + timedelta(days=tarea.estimado))).days,
            "proyecto": tarea.proyecto_name,
        }
        for tarea in result
        # Solo las tareas que la fecha de inicio sea mayor a una fecha dada y la fecha de fin sea menor a una fecha dada
        if tarea.fecha_inicio > start_date and tarea.fecha_inicio + timedelta(days=tarea.estimado) < end_date
    ]

    return templates.TemplateResponse(
        "filter_inprogress_tasks.html",
        {
            "request": {
                "start_date": start_date,
                "end_date": end_date,
            },
            "tasks": result,
        },
    )

# Entry point for the API
if __name__ == "__main__":
    # Run the application using uvicorn and enable auto-reload
    uvicorn.run("main:app", reload=True)
