from database.db import obtener_por_estado, actualizar_estado
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()


def filtar_ofertas(perfil):

    ofertas = obtener_por_estado("sin_filtrar")

    for oferta in ofertas:
        
        titulo = oferta[1]
        descripcion = oferta[4]
        prompt = f"""
            
            Eres un filtro de ofertas de trabajo. Analiza si esta oferta es relevante para el perfil del usuario.

            PERFIL DEL USUARIO:
            Cargo buscado: {perfil['cargo']}
            Skills: {perfil['skills']}
            Experiencia: {perfil['experiencia']}

            OFERTA:
            Título: {titulo}
            Descripción: {descripcion}

            Responde ÚNICAMENTE con una de estas dos palabras, sin explicación:
            PENDIENTE (si la oferta es relevante para el perfil)
            NO_ENVIAR (si la oferta no es relevante para el perfil)
        
        """

        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        resultado = response.text.strip()
        if resultado == "PENDIENTE":
            actualizar_estado(oferta[0], "pendiente")
        else:
            actualizar_estado(oferta[0], "no_enviar")
