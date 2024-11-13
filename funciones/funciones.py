import os
import re
import datetime
import hashlib
import json
from jose import jwt



SECRETKEY = 'PRUEBATECNICA'
ALGORITH = 'HS256'




def generar_hash_sha256(contrasena)->str:
    """Genera un hash de una cadena

    Args:
        contrasena (_type_): cadena a la que se le genera el hash

    Returns:
        str: hash
    """    
    contrasena_bytes = contrasena.encode('utf-8')
    sha256_hash = hashlib.sha256()
    sha256_hash.update(contrasena_bytes)
    hash_hexadecimal = sha256_hash.hexdigest()
    return hash_hexadecimal

def crear_acces_token(info_user: dict, days: int = 3)-> str:
    """Esta funcion crea un token de acceso para el usuario.

    Args:
        info_user (dict): informacion del usuario al que se le creara el token 
        days (int, optional): número de días . Defaults to 3.

    Returns:
       str: token
    """    
    to_encode = info_user.copy()
    expire = datetime.datetime.now() + datetime.timedelta(days=days)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRETKEY"), algorithm=ALGORITH)
    return encoded_jwt

def verifica_correo(cadena):
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    coincidencia = re.match(patron,cadena)
    return coincidencia

def generar_sql(tabla:str,modelo:object)->str: 
    valores_str =[]
    valores = list(dict(modelo).values())
    campos = list(dict(modelo))
    for i in valores:
        if isinstance(i, dict) or isinstance(i, list): 
            i = f"{json.dumps(i)}"
        i= f"'{str(i)}'" 
        valores_str.append(i)
    texto_valores = f'({",".join(valores_str)})'
    texto_campos = f'({",".join(campos)})'
    sql = f"INSERT INTO {tabla} {texto_campos} VALUES {texto_valores}"
    return sql 