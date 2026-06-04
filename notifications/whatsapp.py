import os
from dotenv import load_dotenv
from twilio.rest import Client
from notifications.base import Notificacion

load_dotenv()

class WhatsApp(Notificacion):
    def send(self , mensaje , numero_destino):
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        from_number = os.getenv("TWILIO_WHATSAPP_FROM")

        cliente = Client(account_sid , auth_token)
        cliente.messages.create(
            from_=from_number,
            to=f"whatsapp:{numero_destino}",
            body=mensaje
        )