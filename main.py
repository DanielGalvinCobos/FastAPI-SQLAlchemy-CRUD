from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

class TareaSchema(BaseModel):
    titulo: str
    descripcion: str | None = None
    completada: bool = False

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/tareas/")
def get_tareas(db: Session = Depends(get_db)):
    return db.query(models.Tarea).all()

@app.get("/tareas/{id}")
def get_tarea(id: int, db: Session = Depends(get_db)):
    return db.query(models.Tarea).filter(models.Tarea.id == id).first()

@app.post("/tareas/")
def crear_tarea(tarea: TareaSchema, db: Session = Depends(get_db)):
    nueva_tarea = models.Tarea(**tarea.model_dump())
    db.add(nueva_tarea)
    db.commit()
    db.refresh(nueva_tarea)
    return nueva_tarea

@app.put("/tareas/{id}")
def completar_tarea(id: int, db: Session = Depends(get_db)):
    tarea = db.query(models.Tarea).filter(models.Tarea.id == id).first()
    tarea.completada = True
    db.commit()
    db.refresh(tarea)
    return tarea

@app.delete("/tareas/{id}")
def eliminar_tarea(id: int, db: Session = Depends(get_db)):
    tarea = db.query(models.Tarea).filter(models.Tarea.id == id).first()
    db.delete(tarea)
    db.commit()
    return {"mensaje": "Tarea eliminada"}