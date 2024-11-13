from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app  

client = TestClient(app)

def test_login_correcto():
    data = {"username": "usuario@dominio.com", "password": "password123"}
    response = client.post("/login", data=data)
    assert response.status_code == 200
    assert "token" in response.json()

def test_login_usuario_inexistente():
    data = {"username": "inexistente@dominio.com", "password": "password123"}
    response = client.post("/login", data=data)
    assert response.status_code == 200
    assert response.json() == {"message": "Usuario inexistente"}

def test_login_contrasena_incorrecta():
    data = {"username": "usuario@dominio.com", "password": "contrasenaIncorrecta"}
    response = client.post("/login", data=data)
    assert response.status_code == 406
    assert response.json()["detail"] == "Contrasenia incorrecta"


def test_nuevo_usuario_correcto():
    data = {"correo": "nuevo@dominio.com", "password": "password123"}
    response = client.post("/usuarios", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "Usuario registrado con exito"}

def test_nuevo_usuario_correo_invalido():
    data = {"correo": "correo_invalido", "password": "password123"}
    response = client.post("/usuarios", json=data)
    assert response.status_code == 500
    assert response.json()["detail"] == "Formato de correo incorrecto"

def test_nuevo_usuario_correo_existente():
    data = {"correo": "usuario@dominio.com", "password": "password123"}
    with patch("sql_instance.busca", return_value=[{"correo": "usuario@dominio.com"}]):
        response = client.post("/usuarios", json=data)
    assert response.status_code == 406
    assert response.json()["detail"] == "El correo ya se encuentra registrado"

def test_nuevo_usuario_error_base_datos():
    data = {"correo": "nuevo@dominio.com", "password": "password123"}
    with patch("sql_instance.busca", side_effect=Exception("Error al obtener la base de datos")):
        response = client.post("/usuarios", json=data)
    assert response.status_code == 500
    assert response.json()["detail"] == "Error al obtener info de la base de datos"
