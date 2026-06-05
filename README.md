# Job Agent 🤖

> Agente autónomo que busca ofertas de trabajo, las filtra con IA y te las manda por WhatsApp.

![Python](https://img.shields.io/badge/Python-3.12.10-3776AB?style=flat&logo=python&logoColor=white)
![Google Gemini](https://img.shields.io/badge/AI-Gemini%202.0%20Flash-4285F4?style=flat&logo=google&logoColor=white)
![Twilio](https://img.shields.io/badge/WhatsApp-Twilio-F22F46?style=flat&logo=twilio&logoColor=white)
![SQLite](https://img.shields.io/badge/DB-SQLite3-003B57?style=flat&logo=sqlite&logoColor=white)
![uv](https://img.shields.io/badge/Package%20Manager-uv-DE5FE9?style=flat)
![Estado](https://img.shields.io/badge/Estado-Terminado-22C55E?style=flat)

---

## ¿Qué hace?

Job Agent corre en segundo plano todos los días y hace lo siguiente de forma automática:

```
06:00 AM  →  Scraping en LinkedIn e Indeed
            →  Deduplicación en base de datos
            →  Filtro con Google Gemini (¿aplica a tu perfil?)

09:00 AM  →  Envía las mejores ofertas a tu WhatsApp
06:00 PM  →  Segunda ronda de notificaciones
```

Solo lo configuras una vez. Después, tú decides — el agente trabaja por ti.

---

## Flujo completo

```
┌─────────────┐    ┌──────────────┐    ┌────────────────┐    ┌──────────────┐
│   Scraping   │ → │  Base datos  │ → │  Filtro con AI  │ → │  WhatsApp    │
│  JobSpy      │    │  SQLite3     │    │  Gemini Flash   │    │  Twilio      │
└─────────────┘    └──────────────┘    └────────────────┘    └──────────────┘
```

**Estados de una oferta:**

| Estado | Significado |
|--------|------------|
| `sin_filtrar` | Recién scrapeada, pendiente de revisión IA |
| `pendiente` | Aprobada por Gemini, lista para notificar |
| `no_enviar` | Rechazada por Gemini, no aplica al perfil |
| `enviada` | Ya notificada por WhatsApp |

---

## Stack tecnológico

| Categoría | Tecnología | Para qué |
|-----------|-----------|----------|
| Scraping | `python-jobspy` | Scraping de LinkedIn, Indeed, GetOnBoard, Computrabajo |
| IA | `google-genai` (Gemini 2.0 Flash) | Filtrar ofertas según perfil profesional |
| Notificaciones | `twilio` | Envío de mensajes por WhatsApp |
| Base de datos | `SQLite3` (nativo) | Persistencia de ofertas y estados |
| Scheduler | `schedule` | Tareas automáticas en horarios definidos |
| CLI | `rich` | Interfaz en terminal con color y formato |
| Logging | `loguru` | Registro de eventos y errores |
| Config | `python-dotenv` + `pyyaml` | Variables de entorno y perfil de usuario |

---

## Estructura del proyecto

```
job-agent/
│
├── main.py                  # Orquestador y único punto de salida al usuario
│
├── ai/
│   └── filter.py            # Filtrado de ofertas con Google Gemini
│
├── scraper/
│   └── job_scraper.py       # Scraping de plataformas de empleo
│
├── database/
│   └── db.py                # Operaciones CRUD en SQLite
│
├── notifications/
│   ├── base.py              # Clase base abstracta (Open/Closed Principle)
│   └── whatsapp.py          # Implementación con Twilio
│
├── utils/
│   ├── console.py           # Instancia global de Rich
│   └── logger.py            # Instancia global de Loguru
│
├── data/                    # Generado en runtime (git-ignored)
│   ├── jobs.db              # Base de datos SQLite
│   ├── profile.yaml         # Perfil del usuario
│   └── logs/agent.log       # Logs de la aplicación
│
├── docs/
│   ├── CLAUDE.md            # Contexto técnico y guía de arquitectura
│   └── requirements.md      # Requerimientos funcionales y casos de uso
│
├── .env                     # Credenciales de API (git-ignored)
├── pyproject.toml           # Metadata y dependencias
└── uv.lock                  # Lock file de dependencias
```

---

## Instalación

### Prerequisitos

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) — gestor de paquetes
- Cuenta en [Google AI Studio](https://aistudio.google.com/) (gratis) para la API de Gemini
- Cuenta en [Twilio](https://www.twilio.com/) con WhatsApp Sandbox configurado

### Pasos

**1. Clonar el repositorio**
```bash
git clone <url-del-repo>
cd job_agent
```

**2. Instalar dependencias**
```bash
uv sync
```

**3. Configurar credenciales**

Crea un archivo `.env` en la raíz del proyecto:

```env
GEMINI_API_KEY=tu_api_key_de_gemini

TWILIO_ACCOUNT_SID=tu_account_sid
TWILIO_AUTH_TOKEN=tu_auth_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
```

> El número `+14155238886` es el sandbox compartido de Twilio. Asegúrate de que tu número esté registrado en el sandbox antes de correr el agente.

---

## Uso

```bash
python main.py
```

### Primera vez

El agente te pide tu perfil profesional y datos de contacto:

```
¿Cuál es tu cargo o el cargo que buscas?
> Java Developer

¿Cuáles son tus skills principales?
> Java, Spring Boot, SQL

¿Cuántos años de experiencia tienes?
> 1

¿Cuál es tu nombre?
> Mateo

¿Cuál es tu número de WhatsApp? (ej: +573146938467)
> +573146938467

¿Cuál es tu zona horaria? (ej: America/Bogota)
> America/Bogota
```

El perfil se guarda en `data/profile.yaml`. En siguientes ejecuciones el sistema pregunta si deseas editarlo.

### Corridas posteriores

```
Ya tienes un perfil guardado. ¿Deseas editarlo? (s/n):
> n

✓ Agente iniciado. Scraping a las 06:00, notificaciones a las 09:00 y 18:00.
```

El agente queda corriendo indefinidamente. Para detenerlo: `Ctrl + C`.

---

## Lógica de notificaciones

| Ofertas pendientes | Qué pasa |
|-------------------|----------|
| 0 | Se envía: *"Hoy no hay nuevas ofertas para ti"* |
| 1 | Se envía 1 mensaje a las 09:00 AM |
| 2+ | Se envía 1 oferta a las 09:00 AM y 1 a las 06:00 PM |

---

## Arquitectura

El proyecto aplica principios de diseño sólidos para mantener el código limpio y extensible:

- **Single Responsibility** — Cada módulo tiene una sola responsabilidad
- **Open/Closed Principle** — Nuevos canales de notificación (Telegram, Email) se agregan extendiendo `Notificacion`, sin tocar código existente
- **Separación de capas** — Solo `main.py` imprime en consola; el resto es lógica pura
- **Fail Gracefully** — Los errores se loguean y el programa continúa; errores críticos notifican al usuario
- **Credenciales seguras** — Todas las API keys viven en `.env`, nunca en el código

---

## Logs

Los eventos y errores se registran automáticamente en `data/logs/agent.log`:

```
2025-06-05 06:00:01 | INFO | Iniciando scraping para: Java Developer
2025-06-05 06:00:08 | INFO | 12 ofertas encontradas, 3 nuevas guardadas
2025-06-05 06:00:15 | INFO | Filtrado completado: 2 pendientes, 1 rechazada
2025-06-05 09:00:00 | INFO | Notificación enviada a +57314...
```

---

## Ramas del proyecto (Gitflow)

```
main
 └── develop
      ├── feature/mateo/fase-1/configuracion    ✅
      ├── feature/mateo/fase-2/webScraping       ✅
      ├── feature/mateo/fase-3/base_de_datos     ✅
      ├── feature/mateo/fase-4/filtro_ai         ✅
      ├── feature/mateo/fase-5/notificaciones    ✅
      ├── feature/mateo/fase-6/perfiles          ✅
      └── feature/mateo/fase-7/orquestacion      ✅
```

---

## Límites de API

| API | Límite gratuito | Estrategia |
|-----|----------------|------------|
| Google Gemini Flash | 1500 req/día | Solo filtra trabajos `sin_filtrar`, no reprocesa |
| Twilio WhatsApp | Según créditos | Máx. 2 mensajes por día por diseño |
| python-jobspy | Sin límite explícito | 5 resultados por búsqueda, 96h de antigüedad |

---

## Requisitos del sistema

```toml
[project]
requires-python = ">=3.12.10"
```

```
python-jobspy >= 1.1.82
google-genai  >= 2.8.0
twilio        >= 9.10.9
schedule      >= 1.2.2
rich          >= 15.0.0
loguru        >= 0.7.3
python-dotenv >= 1.2.2
pyyaml        >= 6.0.3
```
