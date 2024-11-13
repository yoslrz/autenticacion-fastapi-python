models = [
    '''CREATE TABLE IF NOT EXISTS accesos(
        id VARCHAR(100) PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        apellido_paterno VARCHAR(100) NOT NULL,
        correo VARCHAR(60) NOT NULL,
        password VARCHAR(200) NOT NULL,
        estatus INT(1) NOT NULL DEFAULT '0',
        creacion_fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    ) ENGINE = InnoDB;''',
]