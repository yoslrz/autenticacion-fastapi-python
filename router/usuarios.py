import datetime
import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from funciones.dbconexion import sql_instance
from funciones.funciones import ALGORITH, crear_acces_token, generar_hash_sha256,  verifica_correo
from funciones.models_object import Acceso
from jose import jwt

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl='/')

#region Inicio de sesion
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    usuario = sql_instance.busca("accesos","*",f"correo = '{form.username}'")
   
    if type(usuario) == Exception:
        raise HTTPException(status_code=500,detail="Error al obtener info de la base de datos")
    if len(usuario) == 0:
        return {"message":"Usuario inexistente"}
    usuario = usuario[0]
    passhash = generar_hash_sha256(form.password)
    if passhash != usuario[0]['password']:
        raise HTTPException(status_code=406,detail="Contraseña incorrecta")
    token = crear_acces_token(({"user": usuario["correo"], "id": usuario["id"]}))
    return {"token": token}

#region nuevo usuario 
@router.post("/usuarios")
async def nuevo_usuario(info:Acceso):
    validacion_correo = verifica_correo(info.correo)
    if not validacion_correo:
        raise HTTPException(status_code=406,detail="Formato de correo incorrecto")
    existencia = sql_instance.busca("accesos","*",f"correo = '{info.correo}'")
    if type(existencia) == Exception:
        raise HTTPException(status_code=500,detail="Error al obtener info de la base de datos")
    if len(existencia) > 0:
        raise HTTPException(status_code=406,detail="El correo ya se encuentra registrado")
    password = generar_hash_sha256(info.password)
    info.password = password
    ingreso = sql_instance.ingreso_registro("accesos",info)
    if type(ingreso) == Exception:
        raise HTTPException(status_code=500,detail="Error al obtener info de la base de datos")
    return {"message":"Usuario registrado con exito"}


#region verificar token 
@router.get("/validador")
async def validador_tok(token:str=Depends(oauth2)): 
    exception = HTTPException(
        status_code=404,
        detail= {"texto":"Credenciales de autenticación inválidas"} ,
        headers={"WWW-Authenticate": "Bearer"})
    try:
        info = jwt.decode(token, os.getenv("SECRETKEY"), algorithms=[ALGORITH])
        fecha_ven = datetime.fromtimestamp(info.get("exp"))
        id_user = info.get('id')
        vigencia = fecha_ven - datetime.now()
        if vigencia.total_seconds() <= 0:
            raise exception
    except Exception as e:
        raise exception
    info_us = sql_instance.busca(tabla="accesos",condicion=f"id ='{id_user}'",campos="*")
    if type(info_us) == Exception:
        raise HTTPException(status_code=500,detail="Error al obtener info de la base de datos")
    if len(info_us) == 0:
        raise HTTPException(status_code=406,detail="Usuario no encontrado")
    info_us = info_us[0]
    return {"correo": info_us["correo"], "id": info_us["id"]} 

#region refrescar token
@router.get("/refresh_token")
async def refrescar_token(token:str=Depends(validador_tok)):
    token = crear_acces_token(({"user": token["correo"], "id": token["id"]}))
    return {"token": token}

#region logout
@router.post("/logout")
async def logout():
    return {"message": "Sesion cerrada exitosamente"}


