# codigo para seleccionar al amigo secreto
from multiprocessing import synchronize
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

"""creando todo los modelos"""
# con esto apenas se ejecute el código, si no existen las tablas (modelos)
# en postgres, el código los va a crear de forma automatica
models.Base.metadata.create_all(bind=engine) 

# creando una instancia de FastAPI
app = FastAPI()

# definiendo el modelo
# definiendo como debe ser un post
class Amigo(BaseModel):
    nombre_persona : str
    direccion : str
    regalo_deseado : str
    seleccionado : bool = False
    selecciono : bool = False


@app.get("/")
def get_inicial():
    return {"data":"app funcionando :)"}

    
@app.get("/amigos")
def get_amigos(db: Session = Depends(get_db)):
    # accediendo a la base de datos.vamos a hacer una query.vamos a buscar el modelo.traemos todos los datos que concuerden con el modelo
    amigo = db.query(models.Amigo).all()
    return {"data":amigo}



# creando un nuevo participante
@app.post("/amigos", status_code=status.HTTP_201_CREATED)
def crear_amigo(amigo: Amigo, db: Session = Depends(get_db)):
    
    # con esto desempacamos los datos del deiccionario y python los acomoda a la columna que corresponde
    new_amigo = models.Amigo(**amigo.dict())
    # lo agregamos a la base de datos
    db.add(new_amigo)
    # hacemos el commit
    db.commit()
    # traemos el objeto que fue creado
    db.refresh(new_amigo)
    return { "data": new_amigo }



@app.put("/amigos/{id}")
def update_amigo(id: int, updated_amigo:Amigo, db: Session = Depends(get_db)):

    yo_query = db.query(models.Amigo).filter(models.Amigo.id_persona == id and models.Amigo.selecciono == True)
    yo = yo_query.first()
    if yo == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"usted ya selecciono su amigo secreto"
        )

    yo_query = db.query(models.Amigo).filter(models.Amigo.id_persona == id)
    yo = yo_query.first()
    if yo == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"especifique bien su id"
        )

    yo_query.update({"selecciono":True}, synchronize_session=False)
    db.commit()

    amigo_query = db.query(models.Amigo).filter(models.Amigo.id_persona != id and models.Amigo.seleccionado == False)
    amigo = amigo_query.first()
    if amigo == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"No hay más amigos, digale a Sergio que revise"
        )
    
    amigo_query = db.query(models.Amigo).filter(models.Amigo.id_persona == amigo.id_persona)
    amigo_query.update({"seleccionado":True}, synchronize_session=False)
    db.commit()
    
    return {"data" : yo_query.first(), "id_amigo_secreto": amigo_query.first()}