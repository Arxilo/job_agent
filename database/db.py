import sqlite3


def inicializar_db():

    conexion = sqlite3.connect("data/jobs.db")
    cursor = conexion.cursor()
    cursor.execute(
        """
        
        CREATE TABLE IF NOT EXISTS jobs (
            
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo      TEXT,
            empresa     TEXT,
            ubicacion   TEXT,
            descripcion TEXT,
            url         TEXT UNIQUE,
            plataforma  TEXT,
            estado      TEXT DEFAULT 'sin_filtrar',
            fecha_guardado TEXT
            
        )

        """
    )

    conexion.commit()
    conexion.close()


def existe_oferta():
    pass


def guardar_oferta():
    pass


def obtener_por_estado():
    pass
