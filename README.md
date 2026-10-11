# Vigía — Plataforma de monitorización y página de estado

Proyecto Intermodular — 2º de Desarrollo de Aplicaciones Web (DAW)
IES Severo Ochoa, Elche · Curso 2026/2027
Autor: José Javier Contreras Morillo

---

## Descripción

Cualquier organización que ofrece servicios en línea necesita saber si esos servicios funcionan, y enterarse antes de que se lo diga un cliente. **Vigía** es una aplicación web que supervisa de forma automática y continua la disponibilidad de servicios web y servidores.

El usuario da de alta monitores sobre una URL o un puerto, y el sistema los comprueba periódicamente en segundo plano, registrando el resultado y la latencia de cada comprobación. Cuando un monitor falla varias veces seguidas, se marca como caído, se abre una incidencia y se envía un aviso por correo electrónico.

Hay dos interfaces, para dos perfiles distintos: un **panel de gestión privado**, actualizado en tiempo real mediante WebSocket, para el personal técnico; y una **página de estado pública** con el estado de cada servicio, el historial de disponibilidad de los últimos 90 días y las incidencias publicadas.

---

## Stack tecnológico

| Capa | Tecnología |
|---|---|
| Cliente | React 19 + Vite + Tailwind CSS |
| Servidor | Node.js 22 + Express 5 |
| Base de datos | PostgreSQL 16 (a partir del Hito 2) |
| Contenedores | Docker + Docker Compose |
| Control de versiones | Git · `main` + ramas de trabajo · Conventional Commits |

> La **justificación completa de cada tecnología**, con las alternativas descartadas y el motivo, está en [`docs/hito0-tecnologias.md`](docs/hito0-tecnologias.md) (entregable del Hito 0).

---

## Estructura del repositorio

```
vigia/
├── backend/            # API REST (Node + Express)
│   ├── src/
│   │   ├── config/     # carga y validación de variables de entorno
│   │   ├── middlewares/
│   │   ├── routes/
│   │   ├── app.js      # construcción de la aplicación Express
│   │   └── server.js   # arranque del servidor
│   ├── .env.example
│   └── Dockerfile
├── frontend/           # Cliente web (React + Vite)
│   ├── src/
│   │   ├── api/        # cliente de la API
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── .env.example
│   └── Dockerfile
├── docs/               # documentación técnica
├── .env.example        # variables usadas por Docker Compose
├── docker-compose.yml
└── README.md
```

---

## Requisitos previos

| Herramienta | Versión mínima | Comprobación |
|---|---|---|
| Node.js | 20 (probado con 22) | `node -v` |
| npm | 10 | `npm -v` |
| Git | 2.x | `git --version` |
| Docker *(opcional)* | 24 | `docker --version` |

---

## Puesta en marcha en local

Los comandos están pensados para copiarse y pegarse en orden. Se necesitan **dos terminales**: una para el backend y otra para el frontend.

### 1. Clonar el repositorio

```bash
git clone https://github.com/Xenofle/vigia.git
cd vigia
```

### 2. Configurar las variables de entorno

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

Valores por defecto, válidos para desarrollo sin tocar nada:

| Fichero | Variable | Valor por defecto | Para qué sirve |
|---|---|---|---|
| `backend/.env` | `NODE_ENV` | `development` | Entorno de ejecución |
| `backend/.env` | `PORT` | `4000` | Puerto en el que escucha la API |
| `backend/.env` | `CORS_ORIGIN` | `http://localhost:5173` | Origen autorizado a llamar a la API |
| `backend/.env` | `DATABASE_URL` | `postgresql://vigia:vigia@localhost:5432/vigia` | Conexión a PostgreSQL. **Aún no se usa**, se incorpora en el Hito 2 |
| `frontend/.env` | `VITE_API_URL` | `http://localhost:4000/api` | URL base de la API que consume el cliente |

### 3. Instalar las dependencias

```bash
npm install --prefix backend
npm install --prefix frontend
```

### 4. Preparar la base de datos

**No es necesario en este hito.** El proyecto todavía no tiene modelo de datos ni migraciones: el servicio de PostgreSQL está declarado en `docker-compose.yml` y la variable `DATABASE_URL` queda preparada para el Hito 2, pero la API arranca y funciona sin base de datos.

### 5. Arrancar el backend

En la primera terminal:

```bash
npm run dev --prefix backend
```

Queda disponible en **http://localhost:4000**, con el endpoint de comprobación en **http://localhost:4000/api/health**.

### 6. Arrancar el frontend

En la segunda terminal:

```bash
npm run dev --prefix frontend
```

Queda disponible en **http://localhost:5173**.

### 7. Comprobar que funciona

**a) La API responde por sí sola:**

```bash
curl http://localhost:4000/api/health
```

Respuesta esperada:

```json
{
  "estado": "ok",
  "servicio": "vigia-api",
  "version": "0.1.0",
  "entorno": "development",
  "marcaDeTiempo": "2026-10-07T14:30:31.039Z",
  "tiempoActivoSegundos": 2
}
```

**b) El frontend se comunica con la API:**

Abre **http://localhost:5173** en el navegador. Si la comunicación funciona, la tarjeta muestra el indicador verde **«API operativa»** junto con el servicio, la versión, el entorno y el tiempo activo que ha devuelto el backend.

Si en su lugar aparece el aviso rojo «No se ha podido contactar con la API», revisa que el backend esté arrancado en el puerto 4000 y que `VITE_API_URL` apunte a él. Tras cambiar un `.env`, reinicia el servidor de desarrollo correspondiente.

---

## Alternativa: arranque con Docker

Levanta la base de datos, la API y el cliente web con un solo comando:

```bash
cp .env.example .env
docker compose up --build
```

| Servicio | Contenedor | URL / puerto |
|---|---|---|
| `web` | `vigia-web` | http://localhost:5173 |
| `api` | `vigia-api` | http://localhost:4000/api/health |
| `db` | `vigia-db` | `localhost:5432` |

`docker compose up --build` reconstruye las imágenes; en arranques posteriores basta con `docker compose up`. Para detenerlo todo:

```bash
docker compose down          # detiene y elimina los contenedores
docker compose down -v       # además, borra el volumen de la base de datos
```

El servicio `api` espera a que PostgreSQL esté listo mediante un *healthcheck*, de modo que el orden de arranque es siempre correcto.

---

## Comandos disponibles

| Comando | Carpeta | Descripción |
|---|---|---|
| `npm run dev` | `backend` | Arranca la API con recarga automática (`node --watch`) |
| `npm start` | `backend` | Arranca la API sin recarga (uso en contenedor) |
| `npm run dev` | `frontend` | Servidor de desarrollo de Vite |
| `npm run build` | `frontend` | Compila el cliente para producción en `dist/` |
| `npm run preview` | `frontend` | Sirve localmente la compilación de producción |

---

## Flujo de trabajo con Git

- **`main`**: rama estable. No se trabaja directamente sobre ella; solo recibe código mediante *pull request*.
- **Ramas de trabajo**: una por bloque funcional, con el prefijo correspondiente — `feat/<descripcion>`, `fix/<descripcion>`, `docs/<descripcion>`, `chore/<descripcion>` — que se integran en `main` cuando el bloque está terminado.
- **Mensajes de commit**: [Conventional Commits](https://www.conventionalcommits.org/) en español.
  Ejemplos: `feat(api): endpoint de comprobación de estado`, `docs(readme): instrucciones de arranque en local`.
- **Etiquetas**: una por hito entregado (`hito-0`, `hito-1`, …).

---

## Estado del proyecto

| Hito | Contenido | Estado |
|---|---|---|
| Hito 0 | Repositorio y definición tecnológica | Completado |
| Hito 1 | Boilerplate, arranque en local y documentación | Completado |
| Hito 2 | Modelo de datos, autenticación y CRUD de monitores | Pendiente |

Documentación relacionada:

- [`docs/hito0-tecnologias.md`](docs/hito0-tecnologias.md) — justificación completa del stack.
- [`docs/instalacion.md`](docs/instalacion.md) — instalación del entorno, pruebas realizadas y problemas encontrados.
