import os
import logging
from typing import List
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from datetime import datetime, date
from contextlib import asynccontextmanager

from sqlalchemy import Boolean, Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session

from models import TaskCreate, TaskUpdate, TaskResponse

# --- Logging ---
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Carga las variables del archivo .env al entorno de ejecución
load_dotenv()


# --- DB setup ---
def init_db():
    DATABASE_URL = f"postgresql+psycopg2://{os.getenv('DATABASE_USER', 'none')}:{os.getenv('DATABASE_PASSWORD', 'none')}@{os.getenv('DATABASE_SERVER', 'none')}:{os.getenv('DATABASE_PORT', 'none')}/{os.getenv('DATABASE_CATALOG', 'none')}"
    global engine
    global SessionLocal
    engine = create_engine(DATABASE_URL, echo=True)
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    Base_db.metadata.create_all(bind=engine)

Base_db = declarative_base()

class Task_db(Base_db):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)

    titulo = Column(String, index=True, unique=True)
    contenido = Column(String)
    deadline = Column(DateTime)
    completada = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime)
    fecha_modificacion = Column(DateTime, nullable=True)

#FastAPI app with lifespan event to initialize the database
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- CÓDIGO DE ARRANQUE (Startup) ---
    # Aquí lanzas el create_all de manera controlada cuando arranca el servidor
    try:
        init_db()
        print("Base de datos inicializada correctamente en el arranque.")
    except Exception as e:
        print(f"Error al conectar o inicializar la BD en el arranque: {e}")
        # Opcional: puedes decidir si quieres que falle el arranque o no
        
    yield  # Aquí es donde FastAPI arranca y empieza a atender peticiones
    
    # --- CÓDIGO DE APAGADO (Shutdown) - Opcional ---
    print("Apagando la aplicación...")

app = FastAPI(title="API para gestion de tareas", version="1.0.0", lifespan=lifespan)

# TODO: Implementar clase TaskManager con lógica de negocio
class TaskManager:
        

    def set_TaskResponse(self, task_db: Task_db) -> TaskResponse:
        return TaskResponse(
            id=task_db.id,
            titulo=task_db.titulo,
            contenido=task_db.contenido,
            deadline=task_db.deadline,
            completada=task_db.completada,
            fecha_creacion=task_db.fecha_creacion,
            fecha_modificacion=task_db.fecha_modificacion
        )   

    
    def title_exists(self, db, title: str) -> bool: 
        logger.debug(f"Verificando si el título '{title}' ya existe en la base de datos")
        existing = db.query(Task_db).filter(Task_db.titulo.ilike(title)).first()

        if existing:
            logger.warning(f"El título '{title}' ya existe en la base de datos")

        return existing is not None

    def new_task(self, db, task: TaskCreate) -> TaskResponse:

        task_db=Task_db(
            titulo=task.titulo,
            contenido=task.contenido,
            deadline=task.deadline,
            completada=False,
            fecha_creacion=str(datetime.now())
        )
        db.add(task_db)
        db.commit()
        db.refresh(task_db)
        return self.set_TaskResponse(task_db)

    def obtener_tarea(self, db, task_id: int) -> TaskResponse:
        task_db = db.query(Task_db).filter(Task_db.id == task_id).first()

        if not task_db:
            return None
        
        return self.set_TaskResponse(task_db)


    def completar_tarea(self, db, task_id: int) -> TaskResponse:
        task_update = TaskUpdate(id=task_id, completada=True)
        return self.actualizar_tarea(db, task_update)

    def actualizar_tarea(self, db, task: TaskUpdate) -> TaskResponse:

        task_db = db.query(Task_db).filter(Task_db.id == task.id).first()
        if not task_db:
            return None

        task_db.completada = task.completada   
        task_db.fecha_modificacion = str(datetime.now())
        db.commit() 
        db.refresh(task_db)
        return self.set_TaskResponse(task_db)

    def eliminar_tarea(self, db, task_id: int) -> int:

        task_db = db.query(Task_db).filter(Task_db.id == task_id).first()
        logger.debug(f"Eliminando tarea con ID {task_id}. Tarea encontrada: {task_db}")
        if not task_db:
            return -1

        db.delete(task_db)
        db.commit()
        return task_id
    
    def obtener_tareas_caducadas(self,db) -> List[TaskResponse]:
        today = date.today()
        logger.debug(f"Obteniendo tareas caducadas. Fecha de hoy: {today}") 
        caducadas_db = db.query(Task_db).filter(Task_db.deadline < today, Task_db.completada == False).all()

        caducadas = [self.set_TaskResponse(task) for task in caducadas_db]
        return caducadas

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 

def get_task_manager():
    return TaskManager()

# TODO: Implementar endpoints
@app.post("/tasks/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def new_task(task: TaskCreate, db: Session = Depends(get_db),tm: TaskManager = Depends(get_task_manager)):
     
    existing_title = tm.title_exists(db, task.titulo)
    if existing_title: 
         raise HTTPException(status_code=400, detail=f"Ya existe una tarea con el título '{task.titulo}'")

    respuesta = tm.new_task(db, task)
    return respuesta

@app.get("/tasks/caducadas", response_model=List[TaskResponse])
def obtener_tareas_caducadas(db: Session = Depends(get_db),tm: TaskManager = Depends(get_task_manager)):
    expired_tasks = tm.obtener_tareas_caducadas(db)
    logger.debug(f"Expired tasks: {expired_tasks}")
    if expired_tasks is None:
        expired_tasks = []
    return expired_tasks

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def obtener_tarea(task_id: int, db: Session = Depends(get_db), tm: TaskManager = Depends(get_task_manager)):
     task = tm.obtener_tarea(db, task_id)     

     if task is None:
         raise HTTPException(status_code=404, detail=f"Tarea {task_id} no encontrada")
     return task

@app.patch("/tasks/{task_id}/completar", response_model=TaskResponse)
def marcar_completada(task_id: int, db: Session = Depends(get_db), tm: TaskManager = Depends(get_task_manager)):
    task = tm.completar_tarea(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Tarea {task_id} no encontrada")
    return task

@app.delete("/tasks/{task_id}/eliminar", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tarea(task_id: int, db: Session = Depends(get_db), tm: TaskManager = Depends(get_task_manager)):
    task = tm.eliminar_tarea(db, task_id)
    if task == -1:
        raise HTTPException(status_code=404, detail=f"Tarea {task_id} no encontrada")
    return None

@app.get("/")
def root():
    return {"message": "API para gestion de tareas. \n " +
            "Crea una nueva tarea con el endpoint /tasks/ indicandole titulo, contenido y fecha de vencimiento. \n " +
            "Obtén una tarea por id con el endpoint /tasks/{task_id}. \n " +
            "Marca una tarea como completada con el endpoint /tasks/{task_id}/completar. \n " +
            "Obtén todas las tareas caducadas con el endpoint /tasks/caducadas. \n " +
            "Todos los endpoints (salvo el de la raiz) devuelven la tarea afectada (o una lista de tareas si son varias) \n " + 
            "con los campos: id, titulo, contenido, deadline, completada, fecha_creacion y fecha_modificacion (si la hubo). \n " +
            "Si ocurre un error, se devuelve un mensaje de error con el código de estado correspondiente. \n "
    }
