import os
import yaml
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from utils.console import console

if not os.path.exists("data/profile.yaml"):
    console.print(Panel("👤 Configuración inicial — Perfil profesional", style="bold blue"))
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
