# Guía para principiantes: tecnologías del proyecto MasterClass

Esta guía explica, en lenguaje simple, **qué tecnologías usa este proyecto y cómo usarlas paso a paso**. Está pensada para personas sin experiencia: si nunca programaste o nunca usaste la terminal, empieza aquí.

---

## Lo esencial en 5 minutos

```bash
# 1. Entrar a la carpeta del proyecto
cd MasterClass

# 2. Activar el entorno virtual (una vez por terminal abierta)
source .venv/bin/activate

# 3. Encender la API
uvicorn app.main:app --reload

# 4. Abrir en el navegador: http://127.0.0.1:8000/docs
```

Si eso funcionó, ya estás usando el proyecto. Abajo tienes el detalle de cada pieza.

---

## ¿Qué es este proyecto?

Es un **backend**: un programa que corre en una computadora (o servidor) y responde pedidos por internet. Este backend combina dos cosas:

1. Una **API** (FastAPI) que expone direcciones web (`/health`, y en el futuro más) que otros programas pueden consultar.
2. **Inteligencia artificial** (LangChain + OpenRouter) que conecta la app con modelos de lenguaje (LLM) para responder preguntas de marketing inmobiliario y SEO.

También incluye `seo_agent.py`: un pequeño programa de terminal para hacerle preguntas al agente de SEO directamente, sin navegador.

---

## Las tecnologías, una por una

| Tecnología | ¿Qué es? (analogía) | Rol en este proyecto |
|------------|--------------------|----------------------|
| **Python** | El idioma en el que está escrito todo el proyecto | Lenguaje de programación principal (versión 3.13) |
| **venv** (entorno virtual) | Una caja cerrada donde viven las librerías de ESTE proyecto, sin mezclarlas con otros | Aísla las dependencias en la carpeta `.venv` |
| **pip** | El repartidor: instala librerías desde internet | Instala lo que figura en `requirements.txt` |
| **FastAPI** | El mesero del restaurante: recibe pedidos (requests) y responde (responses) | Framework que crea la API (rutas, validaciones, documentación automática) |
| **Pydantic** | El control de calidad: revisa que los datos tengan forma correcta | Valida configuración y datos de entrada/salida |
| **Uvicorn** | El motor: hace que la API realmente funcione y atienda usuarios | Servidor web que ejecuta FastAPI |
| **LangChain** | El kit de herramientas para armar flujos con IA | Compondrá las cadenas (chains) que hablan con el LLM |
| **OpenRouter** | El proveedor de IA: una puerta única a muchos modelos de lenguaje | Entrega acceso al modelo `deepseek/deepseek-v4.1-flash-1017` usando una API key |
| **LLM** (modelo de lenguaje) | El "cerebro" que lee y escribe texto (ej.: ChatGPT, DeepSeek) | Responde las preguntas del agente de SEO |
| **Docker** | Una caja de envío: empaqueta el programa con todo lo que necesita para funcionar igual en cualquier computadora | Empaqueta la API en una imagen ligera y segura |
| **Docker Compose** | El director de orquesta: ordena a los contenedores cómo levantarse | Levanta la API con un solo comando |
| **Git** | La máquina del tiempo del código: guarda versiones de cada cambio | Control de versiones del proyecto |
| **GitHub** | La nube donde vive el código versionado | Repositorio remoto: github.com/JulianCanoDev/MasterClass |

---

## Paso a paso desde cero

### Paso 0 — Requisitos

- Python 3.12 o superior → verifica con `python3 --version`
- Git → verifica con `git --version`
- Docker (opcional, solo para la vía contenedora) → verifica con `docker --version`

### Paso 1 — Obtener el proyecto

```bash
git clone https://github.com/JulianCanoDev/MasterClass.git
cd MasterClass
```

### Paso 2 — Crear y activar el entorno virtual

```bash
python3 -m venv .venv      # crea la caja (una sola vez)
source .venv/bin/activate  # la abre (cada vez que abras una terminal)
```

Sabes que está activo cuando tu terminal muestra `(.venv)` al inicio.
Para salir del entorno: `deactivate`.

### Paso 3 — Instalar las dependencias

```bash
pip install -r requirements.txt
```

`requirements.txt` es la lista de compras: pip lee el archivo e instala cada librería con su versión.

### Paso 4 — Configurar los secretos (`.env`)

El proyecto necesita una **API key** de OpenRouter (una contraseña que te identifica y paga por el uso de la IA).

1. Crea una cuenta en https://openrouter.ai y genera una API key.
2. Copia el archivo ejemplo:

```bash
cp .env.example .env
```

3. Abre `.env` con cualquier editor y pega tu clave en `OPENROUTER_API_KEY=`.

> **Importante:** `.env` nunca se sube a GitHub (está ignorado a propósito). Las contraseñas no se comparten.

### Paso 5 — Encender la API

```bash
uvicorn app.main:app --reload
```

- `--reload` reinicia solo cuando cambiás código (solo para desarrollo).
- Verifica: abre http://127.0.0.1:8000/health → debe responder `{"status": "ok"}`.
- Bonus: http://127.0.0.1:8000/docs muestra la documentación automática (Swagger) que FastAPI genera solo.
- Para apagar: `Ctrl + C`.

### Paso 6 — Usar el agente de SEO por terminal

```bash
# Pregunta única (entre comillas)
python seo_agent.py "¿Cómo posiciono un departamento en Palermo?"

# Modo conversación (recuerda tus preguntas anteriores)
python seo_agent.py
```

El script lee la clave desde `.env` automáticamente; no necesitás exportar nada.
Para salir del modo conversación: escribe `exit` o presiona `Ctrl + D`.

### Paso 7 — La vía Docker (opcional)

```bash
docker compose up --build   # construye y enciende todo en el puerto 8000
docker compose down         # apaga
```

Docker usa el `Dockerfile`: una receta que instala las dependencias y ejecuta la API en un contenedor aislado, igual a como correrá en producción (Dokploy).

### Paso 8 — Guardar y subir tus cambios

```bash
git add -A                          # elegir todos los cambios
git commit -m "feat: lo que hiciste"  # guardar una versión con mensaje
git push                            # subir a GitHub
```

---

## Problemas comunes

| Síntoma | Causa probable | Solución |
|---------|----------------|----------|
| `Error: OPENROUTER_API_KEY is not set` | No existe el archivo `.env` | Crealo: `cp .env.example .env` y completa la clave |
| `Error code: 401 - User not found` | La clave es inválida o exportaste un valor de relleno | `unset OPENROUTER_API_KEY`, revisa la clave real en `.env` |
| `command not found: python` | En muchas distros el comando es `python3` | Usa `python3` (o crea un alias) |
| `command not found: uvicorn` | El entorno virtual no está activo | `source .venv/bin/activate` |
| `Address already in use` (puerto 8000) | Otro proceso usa el puerto | Ciérralo o usa `--port 8001` |
| `pip install` muy lento o falla | Red o caché | Reintenta; verifica conexión |

---

## Mini glosario

- **API**: programa que responde pedidos por internet mediante direcciones (URLs).
- **Endpoint**: una dirección específica de la API (ej.: `/health`).
- **API key**: contraseña para usar un servicio (como OpenRouter).
- **LLM**: modelo de lenguaje; el "cerebro" que genera texto.
- **Variable de entorno**: valor que el programa lee desde afuera (ej.: lo que vive en `.env`).
- **Contenedor**: caja aislada donde corre el programa con todo lo que necesita.
- **Commit**: fotografía de tu código en un momento dado.
- **Push**: subir tus commits a GitHub.

---

## Checklist de arranque exitoso

- [ ] `python3 --version` responde 3.12+
- [ ] Terminal muestra `(.venv)` activado
- [ ] `pip install -r requirements.txt` termina sin errores
- [ ] `.env` existe y tiene tu clave real de OpenRouter
- [ ] `http://127.0.0.1:8000/health` responde `{"status": "ok"}`
- [ ] `python seo_agent.py` responde una pregunta sin errores

## Próximo paso

Con la base andando, el siguiente módulo del backend (nuevos endpoints y cadenas de LangChain) se especifica antes de programarse. Cuando tengas el primero, arrancamos por ahí.
