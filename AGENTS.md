# AGENTS.md

Instrucciones para agentes de IA (Claude Code, GitHub Copilot, Cursor…) que trabajen en este repositorio.

---

## Qué es Vigía

Plataforma de monitorización de servicios web. El usuario da de alta monitores sobre una URL o un puerto; el sistema los comprueba periódicamente en segundo plano, registra latencia y resultado, marca el servicio como caído si falla varias veces seguidas, abre una incidencia y envía un aviso por correo.

Dos interfaces: **panel privado** (técnicos — configura monitores, gestiona incidencias) y **página de estado pública** (usuarios finales — estado actual, historial 90 días, incidencias publicadas). Actualización en tiempo real vía WebSocket sin recargar la página.

---

## Stack

| Capa | Tecnología |
|---|---|
| Cliente | React 19 + Vite 8 + Tailwind CSS 4 |
| Servidor | Node.js 22 + Express 5 (ESM) |
| Base de datos | PostgreSQL 16 (Hito 2+) |
| ORM | Prisma (Hito 2+) |
| Tiempo real | socket.io (Hito 3+) |
| Alertas | nodemailer (Hito 3+) |
| Contenedores | Docker + Docker Compose |

Ambos paquetes usan `"type": "module"` (ES modules, no CommonJS).

---

## Cómo arrancar

### Local (dos terminales)

```powershell
# Variables de entorno (solo la primera vez)
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Terminal 1 — API en http://localhost:4000
cd backend && npm install && npm run dev

# Terminal 2 — Frontend en http://localhost:5173
cd frontend && npm install && npm run dev
```

Verificación: `Invoke-RestMethod http://localhost:4000/api/health`

### Docker (todo en uno)

```powershell
cp .env.example .env
docker compose up --build        # primera vez
docker compose up                # arranques posteriores
docker compose down              # parar; añadir -v para borrar el volumen de BD
```

### Otros comandos

| Comando | Carpeta | Para qué |
|---|---|---|
| `npm start` | `backend` | arranque sin recarga (contenedor) |
| `npm run build` | `frontend` | compilación de producción en `dist/` |
| `npm run preview` | `frontend` | sirve localmente la build de producción |

> `eslint`, `prettier`, `vitest` y `supertest` se incorporan en el **Hito 2**; no hay scripts de lint ni test todavía.

---

## Arquitectura

### Backend — `backend/src/`

Arquitectura por capas: **rutas → servicios → repositorios** (servicios y repositorios se añaden en Hito 2).

`app.js` exporta `crearApp()`, una factoría que construye la app Express sin arrancarla. `server.js` llama a `crearApp()` y luego a `.listen()`. Este patrón permite montar la app en pruebas sin ocupar un puerto.

```
config/env.js           lee y valida todas las variables de entorno al arrancar
                        (falla al inicio si falta alguna obligatoria)
middlewares/errores.js  404 genérico + manejador centralizado (4 parámetros, Express 5)
routes/                 un fichero por recurso, montados bajo /api en app.js
```

### Frontend — `frontend/src/`

SPA React. Tailwind CSS 4 se integra como plugin de Vite (sin `tailwind.config.js`). Los tokens semánticos de color (`estado-activo`, etc.) se definen en el bloque `@theme` de `index.css`.

```
api/cliente.js   centraliza todos los fetch; lee VITE_API_URL del entorno
App.jsx          componente raíz del Hito 1; el árbol crecerá desde aquí
```

`VITE_API_URL` se hornea en el bundle en tiempo de compilación; cambiarla requiere reiniciar el servidor de desarrollo.

### Docker Compose

Tres servicios: `db` → `api` → `web`. `api` espera a que `db` supere su healthcheck antes de arrancar. `DATABASE_URL` ya está cableada en Compose pero **no se usa hasta el Hito 2**.

---

## Convenciones

- **Idioma del código**: identificadores, comentarios y mensajes en **español** — `crearApp`, `manejadorErrores`, `estado`, `marcaDeTiempo`, etc. No traducir al inglés.
- **Commits**: [Conventional Commits](https://www.conventionalcommits.org/) en español.
  Ejemplos: `feat(api): endpoint de monitores`, `fix(web): corrige estado de carga`, `docs(readme): añade sección de despliegue`.
- **Ramas**: prefijos `feature/`, `fix/`, `docs/`, `chore/`. Nunca trabajar directamente sobre `main`.
- **Integración**: solo mediante pull request a `main`.
- **Etiquetas**: una por hito entregado — `hito-0`, `hito-1`, `hito-2`…

---

## Qué no hacer

- **No traducir identificadores al inglés.** Todo el código está en español; mantener la coherencia.
- **No saltarse la factoría `crearApp()`.** El patrón existe para permitir pruebas sin puerto; no mover la lógica de arranque a `server.js`.
- **No hardcodear variables de entorno.** Toda configuración pasa por `config/env.js`.
- **No añadir dependencias de hitos futuros antes de tiempo.** Prisma, JWT, argon2, zod, socket.io y nodemailer se incorporan en sus hitos respectivos.
- **No hacer push directo a `main`** ni usar `--force` en ramas compartidas.
- **No omitir el prefijo de rama.** `main` ← PR ← `feature/nombre`, nunca commits sueltos.
- **No usar `npm start` en desarrollo local.** `npm run dev` activa la recarga automática.
- **No borrar el volumen de BD sin querer.** `docker compose down` es seguro; `docker compose down -v` borra todos los datos.
