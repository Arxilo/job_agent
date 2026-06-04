from utils.console import console
from database.db import inicializar_db , guardar_oferta , obtener_por_estado 

inicializar_db()
guardar_oferta("Data Analyst Jr", "Google", "Bogotá", "Se busca analista", "https://linkedin.com/job/1", "linkedin")
guardar_oferta("Data Analyst Jr", "Google", "Bogotá", "Se busca analista", "https://linkedin.com/job/1", "linkedin")
ofertas = obtener_por_estado("sin_filtrar")

console.print(ofertas)


