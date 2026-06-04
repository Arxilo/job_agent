from utils.console import console
from scraper.job_scraper import buscar_ofertas

trabajos = buscar_ofertas()

console.print( trabajos, style="bold green")
