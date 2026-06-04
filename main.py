from utils.console import console
from ai.filter import filtar_ofertas
from database.db import inicializar_db , guardar_oferta , obtener_por_estado 

inicializar_db()
guardar_oferta("Data Analyst Jr", "Google", "Bogotá", "Se busca analista", "https://linkedin.com/job/1", "linkedin")
filtar_ofertas()
pendientes = obtener_por_estado("pendiente")
no_enviar = obtener_por_estado("no_enviar")

console.print("Si enviar: ", pendientes  , style= " bold green")
console.print("No enviar: ", no_enviar , style= "bold red")


