from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# from ..db import (HOST, DATABASE_NAME, USER, PASSWORD, PORT)

HOST = 'host'
DATABASE_NAME = 'database_name'
USER = 'user'
PASSWORD = 'password'
PORT = 5432

# connecion string
SQLALCHEMY_DATABASE_URL = f'postgresql://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}'

# engine --> es la responsable de establecer la conexión    
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# debemos hacer uso de una sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# todos los modelos que se creen van a estar usando esta base class
Base = declarative_base()

# funcion que se va a ejecutar cada vez que hagamos una request
# lo que va a hacer es establecer un conexión con la base de datos
# y cerrar la ejecución después de ejecutar la query
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()