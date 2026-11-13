# MasterClass

FastAPI + LangChain backend with an OpenRouter-powered LLM gateway, built for production and containerized deployment (Docker/Dokploy).

---

# Guía para principiantes (español)

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
| **GitHub** | La nube donde vive el código versionado | Repositorio remoto de este proyecto |

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

- `--reload` reinicia solo cuando cambias código (solo para desarrollo).
- Verifica: abre http://127.0.0.1:8000/health → debe responder `{"status": "ok"}`.
- Bonus: http://127.0.0.1:8000/docs muestra la documentación automática (Swagger) que FastAPI genera solo.
- Para apagar: `Ctrl + C`.

### Paso 6 — Usar el agente de SEO por terminal

```bash
# Pregunta única (entre comillas)
python app/testing/seo_agent.py "¿Cómo posiciono un departamento en Palermo?"

# Modo conversación (recuerda tus preguntas anteriores)
python app/testing/seo_agent.py
```

El script lee la clave desde `.env` automáticamente; no necesitas exportar nada.
Para salir del modo conversación: escribe `exit` o presiona `Ctrl + D`.

### Paso 7 — La vía Docker (opcional)

```bash
docker compose up --build   # construye y enciende todo en el puerto 8000
docker compose down         # apaga
```

Docker usa el `Dockerfile`: una receta que instala las dependencias y ejecuta la API en un contenedor aislado, igual a como correrá en producción (Dokploy).

### Paso 8 — Guardar y subir tus cambios

```bash
git add -A                            # elegir todos los cambios
git commit -m "feat: lo que hiciste"  # guardar una versión con mensaje
git push                              # subir a GitHub
```

---

## Estructura del proyecto

```
app/
  main.py                # fábrica de la app + endpoint /health
  core/config.py         # configuración tipada (pydantic-settings)
  testing/seo_agent.py   # agente CLI de SEO inmobiliario (OpenRouter)
requirements.txt         # lista de dependencias
Dockerfile               # receta de la imagen de producción
docker-compose.yml       # orquestación local (puerto 8000, recarga en vivo)
.env.example             # plantilla de secretos (copiar a .env)
```

---

## Problemas comunes

| Síntoma | Causa probable | Solución |
|---------|----------------|----------|
| `Error: OPENROUTER_API_KEY is not set` | No existe el archivo `.env` | Créalo: `cp .env.example .env` y completa la clave |
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

## Glosario del mundo de la programación con IA (Kilo Code, agentes y más)

Los términos de la tabla explican cómo trabajan las herramientas de IA que configuran este proyecto (Kilo Code, Gentle AI, OpenRouter). Léalos en orden: cada concepto se apoya en el anterior.

| Término | ¿Qué significa? |
|---------|-----------------|
| **IA (inteligencia artificial)** | Programas que realizan tareas que antes requerían inteligencia humana: entender lenguaje, escribir código, resumir documentos. |
| **LLM (modelo de lenguaje)** | El "cerebro" detrás de la IA de texto: lee y escribe lenguaje natural y código (ej.: GPT, Claude, DeepSeek). Adivina la palabra siguiente más probable, una y otra vez, con muchísimo entrenamiento detrás. |
| **Prompt** | La instrucción que le das a la IA. La calidad del resultado depende de la claridad del pedido. |
| **Prompt de sistema** | Las reglas ocultas que definen cómo debe comportarse la IA (su rol y estilo). En este proyecto, `seo_agent.py` lleva una: "eres un experto en SEO inmobiliario". |
| **Agente de IA** | Una IA que no solo conversa: planifica y ejecuta tareas usando herramientas (leer archivos, editar código, correr comandos). Tú pides el resultado; él decide los pasos. |
| **Kilo Code** | El agente de programación con IA usado en este proyecto: funciona dentro del editor (VS Code), lee tu código, edita archivos, ejecuta comandos y verifica su propio trabajo. |
| **Vibe Coding** | Estilo de programar donde describes qué quieres en lenguaje natural y el agente escribe el código. Tú conduces la intención, la IA ejecuta. Funciona bien si revisas lo que produce; es peligroso si confías a ciegas. |
| **Herramientas (tools)** | Las capacidades concretas del agente: leer archivos, editarlos, ejecutar comandos de terminal, buscar en el código. Sin herramientas, un agente solo puede conversar. |
| **Subagente** | Agente secundario que el principal lanza para una tarea acotada (explorar el código, revisar un cambio) sin contaminar su propia conversación. |
| **SDD (Spec-Driven Development)** | "Desarrollo guiado por especificaciones": antes de escribir código, se define por escrito qué debe hacer el sistema (endpoints, flujos, reglas) y la IA programa contra esa especificación. Menos improvisación, menos rework. |
| **ODD (Organic Driven Development)** | Evolución de SDD usada por Gentle AI: los cambios chicos van directo al código, y solo el trabajo grande merece un documento de especificación recuperable. Proporcional al riesgo, no al tamaño. |
| **Skills (librería de habilidades)** | Instrucciones especializadas que el agente carga automáticamente cuando la tarea coincide: una para FastAPI, otra para Docker, otra para testing. Es la "biblioteca de experiencia" del agente. |
| **Gentle AI** | El framework que configura los agentes de IA de este proyecto: instala skills, memoria persistente y flujos de trabajo (ODD) sobre el agente que ya usas. |
| **MCP (Model Context Protocol)** | Estándar para conectar herramientas externas al agente, como enchufes a una regleta. Ejemplo: Context7 le da al agente documentación actualizada de librerías en vivo. |
| **Memoria persistente** | El agente guarda decisiones y aprendizajes entre sesiones (con Engram): hoy resuelve algo, mañana recuerda cómo lo hizo sin que se lo expliques de nuevo. |
| **Contexto / ventana de contexto** | Todo el texto que el modelo puede "ver" a la vez (tu código, la conversación, los archivos leídos). Es finito: cuando se llena, lo viejo se comprime u olvida. |
| **Token** | La unidad en que se mide y cobra el texto: 1 token ≈ ¾ de palabra. Más contexto y respuestas largas = más tokens = más costo. |
| **Alucinación** | Cuando la IA afirma algo incorrecto con total seguridad (una función que no existe, un comando inventado). Se combate verificando: por eso este proyecto prueba todo antes de darlo por bueno. |

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
