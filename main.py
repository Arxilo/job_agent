import os
import yaml
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from utils.console import console
from database.db import inicializar_db, guardar_oferta, obtener_por_estado
from scraper.job_scraper import buscar_ofertas
from ai.filter import filtrar_ofertas
from notifications.whatsapp import WhatsApp
import schedule
from utils.logger import logger
import time


if not os.path.exists("data/profile.yaml"):
    console.print(
        Panel("👤 Configuración inicial — Perfil profesional", style="bold blue"))
    cargo = Prompt.ask("¿Cuál es tu cargo o el cargo que buscas?")
    skills = Prompt.ask("¿Cuáles son tus skills principales?")
    experiencia = Prompt.ask("¿Cuántos años de experiencia tienes?")

    console.print(Panel("📱 Datos de contacto", style="bold blue"))
    nombre = Prompt.ask("¿Cuál es tu nombre?")
    whatsapp = Prompt.ask("¿Cuál es tu número de WhatsApp?", default="+57")
    zona_horaria = Prompt.ask(
        "¿Cuál es tu zona horaria?", default="America/Bogota")

    perfil = {
        "perfil_profesional": {"cargo": cargo, "skills": skills, "experiencia": experiencia},
        "datos_usuario": {"nombre": nombre, "whatsapp": whatsapp, "zona_horaria": zona_horaria}
    }
    with open("data/profile.yaml", "w") as f:
        yaml.dump(perfil, f, allow_unicode=True)
    console.print(
        "✅ [bold green]¡Perfil guardado exitosamente![/bold green]")


else:
    if Confirm.ask("Ya tienes un perfil guardado. ¿Deseas editarlo?"):
        os.remove("data/profile.yaml")
        console.print(
            "🗑️ [yellow]Perfil eliminado. Reinicia el programa para ingresar uno nuevo.[/yellow]")
    else:
        console.print(
            "▶️ [green]Continuando con el perfil existente...[/green]")

if os.path.exists("data/profile.yaml"):
    with open("data/profile.yaml", "r") as f:
        perfil = yaml.safe_load(f)


def ciclo_scraping():
    logger.info("Iniciando ciclo de scraping")
    inicializar_db()
    trabajos = buscar_ofertas(
        perfil["perfil_profesional"]["cargo"],
        "Colombia"
    )

    for _, trabajo in trabajos.iterrows():
        guardar_oferta(
            str(trabajo.get("title", "")),
            str(trabajo.get("company", "")),
            str(trabajo.get("location", "")),
            str(trabajo.get("description", "")),
            str(trabajo.get("job_url", "")),
            str(trabajo.get("site", ""))
        )
    filtrar_ofertas(perfil["perfil_profesional"])


def enviar_notificaciones():
    notificador = WhatsApp()
    numero = perfil["datos_usuario"]["whatsapp"]
    pendientes = obtener_por_estado("pendiente")

    if len(pendientes) == 0:
        notificador.send(f"Hola {perfil['datos_usuario']['nombre']} 😊 hoy no hay ofertas nuevas para ti.", numero)
    elif len(pendientes) == 1:
        oferta = pendientes[0]
        mensaje = f"Hola {perfil['datos_usuario']['nombre']} 📌 te tenemos una nueva oferta:\n{oferta[1]} en {oferta[2]}\n📍 {oferta[3]}\n🔗{oferta[5]}"
        notificador.send(mensaje, numero)
    else:
        oferta = pendientes[0]
        mensaje = f"Hola {perfil['datos_usuario']['nombre']} 📌 te tenemos una nueva oferta:\n{oferta[1]} en {oferta[2]}\n📍 {oferta[3]}\n🔗{oferta[5]}"
        notificador.send(mensaje, numero)


if os.path.exists("data/profile.yaml"):
    schedule.every().day.at("06:00").do(ciclo_scraping)
    schedule.every().day.at("09:00").do(enviar_notificaciones)
    schedule.every().day.at("18:00").do(enviar_notificaciones)

    console.print(Panel("🤖 Job Agent corriendo — Ctrl+C para detener", style="bold green")) 

    while True:
        schedule.run_pending()
        time.sleep(60)
