from pydantic import BaseModel
from typing import List

class Acceso(BaseModel):
    id:str | bool = False
    correo: str
    password: str|bool = False
    nombre:str
    apellido_paterno:str


