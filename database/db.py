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


def existe_oferta(url):

    conexion = sqlite3.connect("data/jobs.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT id FROM jobs WHERE url = ?", (url,))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado is not None


def guardar_oferta(titulo, empresa, ubicacion, descripcion, url, plataforma):
    
    conexion = sqlite3.connect("data/jobs.db")
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO jobs (titulo, empresa, ubicacion, descripcion, url, plataforma) VALUES (?,?,?,?,?,?)",
        (titulo, empresa, ubicacion, descripcion, url, plataforma)
    )
    conexion.commit()
    conexion.close()


def obtener_por_estado():
    pass
