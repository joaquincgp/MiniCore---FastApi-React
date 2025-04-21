from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from backend.db.db import Empleado, Proyecto, Tarea
from backend.db import db as db
import backend.db.db_connection as db_connection
from backend.db.db_connection import db_dependency
from datetime import date, timedelta
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    archivo_sql = "db/data.sql"
    try:
        with open(archivo_sql, 'r') as file:
            sql_content = file.read()
        connection = db_connection.engine.raw_connection()
        try:
            cursor = connection.cursor()
            cursor.executescript(sql_content)
            connection.commit()
        finally:
            cursor.close()
            connection.close()
        print("Archivo SQL ejecutado con éxito.")
    except Exception as e:
        print(f"Error al ejecutar el archivo SQL: {e}")
    finally:
        db_connection.engine.dispose()
    yield


app = FastAPI(lifespan=lifespan)


# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Base de datos
db.Base.metadata.create_all(bind=db_connection.engine)


# ✅ Endpoint que consume JSON
class DateFilter(BaseModel):
    start_date: date
    end_date: date

@app.post("/api/filter-inprogress-tasks")
async def filter_inprogress_tasks(data: DateFilter, db: db_dependency):
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

    filtered_tasks = [
        {
            "empleado": tarea.empleado_name,
            "descripcion": tarea.descripcion,
            "fecha_inicio": tarea.fecha_inicio,
            "fecha_fin": tarea.fecha_inicio + timedelta(days=tarea.estimado),
            "dias_pasados": (data.end_date - (tarea.fecha_inicio + timedelta(days=tarea.estimado))).days,
            "proyecto": tarea.proyecto_name,
        }
        for tarea in result
        if tarea.fecha_inicio > data.start_date and tarea.fecha_inicio + timedelta(days=tarea.estimado) < data.end_date
    ]

    return filtered_tasks


# ✅ Ejecutar
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
