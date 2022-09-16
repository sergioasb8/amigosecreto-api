# este archivo va a almacenar todos los modelos
from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

# definiendo nuestro modelo (tabla de postgres)
class Amigo(Base): #los nombres de las clases siempre van en mayuscula

    # definiendo el nombre de la tabla
    __tablename__ = "amigo_secreto"
    # generando el nombre de las columnas
    id_persona = Column(Integer, primary_key=True, nullable=False)
    nombre_persona = Column(String, nullable=False)
    direccion = Column(String, nullable=False)
    regalo_deseado = Column(String, nullable=False)
    seleccionado = Column(Boolean, server_default='False', nullable=False)
    selecciono = Column(Boolean, server_default='False', nullable=False)
