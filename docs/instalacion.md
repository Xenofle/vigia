# Hito 1 — Instalación y configuración del entorno

Vigía · Proyecto Intermodular 2º de Desarrollo de Aplicaciones Web (DAW)
Autor: José Javier Contreras Morillo

Este documento recoge cómo se ha montado el entorno de desarrollo, las pruebas realizadas para comprobar que funciona y los problemas encontrados durante el proceso. Las instrucciones para que una persona ajena al proyecto lo levante están en el [`README.md`](../README.md); aquí se documenta el proceso seguido.

---

## 1. Entorno de trabajo

| Elemento | Versión utilizada |
|---|---|
| Sistema operativo | *(completar: Windows 11 / Ubuntu 24.04 …)* |
| Node.js | 22.x |
| npm | 10.x |
| Git | 2.x |
| Docker | *(completar si se ha usado)* |
| Editor | *(completar: VS Code …)* |

---

## 2. Creación del repositorio

1. Repositorio creado en GitHub con el nombre `vigia`, rama principal `main`.
2. Añadido el profesor como colaborador *(solo si el repositorio es privado)*.
3. Clonado por HTTPS con token personal de acceso. **No se usa SSH**, porque el acceso por SSH está bloqueado en la red del centro (WIFI_EDU).

```bash
git clone https://github.com/Xenofle/vigia.git
cd vigia
```

4. Estrategia de ramas: `main` como rama estable y una rama de trabajo por bloque funcional, integrada mediante *pull request*. Al ser un proyecto individual no se emplea rama `develop` intermedia.

```bash
git checkout -b feat/boilerplate-backend
```

---

## 3. Estructura de carpetas

Se ha creado la estructura mínima exigida por el enunciado:

```
vigia/
├── backend/
├── frontend/
├── docs/
├── .gitignore
├── .env.example
└── README.md
```

El `.gitignore` de la raíz excluye `node_modules/`, los ficheros `.env` y las carpetas de compilación (`dist/`, `build/`), de modo que en el repositorio no hay ni dependencias ni secretos. Solo se versionan los ficheros `.env.example`, que documentan qué variables hacen falta sin incluir ningún valor sensible.

---

## 4. Instalación del backend (Node + Express)

```bash
cd backend
npm init -y
npm install express cors dotenv
```

Ajustes realizados sobre el `package.json` generado:

- `"type": "module"` para usar sintaxis de módulos ECMAScript (`import`/`export`) en lugar de CommonJS.
- Scripts `dev` (con `node --watch`, recarga automática nativa de Node 22, sin necesidad de `nodemon`) y `start` (arranque simple, el que se usa dentro del contenedor).

Estructura del código fuente:

| Fichero | Responsabilidad |
|---|---|
| `src/config/env.js` | Carga de variables de entorno con valores por defecto; detiene el arranque si falta alguna obligatoria |
| `src/routes/health.routes.js` | Endpoint `GET /api/health` |
| `src/middlewares/errores.js` | Respuesta 404 en JSON y manejador de errores centralizado |
| `src/app.js` | Construcción de la aplicación Express (sin arrancarla) |
| `src/server.js` | Arranque del servidor |

Se separa `app.js` de `server.js` de forma deliberada: así, en hitos posteriores, las pruebas automáticas podrán montar la aplicación sin ocupar un puerto.

---

## 5. Instalación del frontend (React + Vite)

```bash
cd frontend
npm init -y
npm install react react-dom
npm install -D vite @vitejs/plugin-react tailwindcss @tailwindcss/vite
```

Configuración:

- `vite.config.js` registra el plugin de React y el de Tailwind CSS v4, y fija el puerto 5173 con `host: true` para que el servidor de desarrollo sea accesible desde el contenedor.
- `src/index.css` importa Tailwind con `@import 'tailwindcss'` y declara en un bloque `@theme` los colores semánticos de estado (activo, degradado, caído), que se reutilizarán en el panel y en la página pública.
- `src/api/cliente.js` centraliza la URL base de la API, leída de `VITE_API_URL`, para no repetirla por los componentes.

---

## 6. Pruebas de funcionamiento

### 6.1 El backend arranca y responde

```bash
npm run dev --prefix backend
curl http://localhost:4000/api/health
```

Respuesta obtenida:

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

Se comprueba además que una ruta inexistente devuelve JSON y no una página de error HTML:

```bash
curl http://localhost:4000/api/nada
# {"error":"Recurso no encontrado","ruta":"/api/nada"}
```

> **Captura 1 — Backend arrancado y respuesta de `/api/health`**
> *(insertar aquí la captura: terminal con el servidor arrancado y la respuesta de `curl` o del navegador)*

### 6.2 El frontend arranca

```bash
npm run dev --prefix frontend
```

> **Captura 2 — Servidor de desarrollo de Vite arrancado**
> *(insertar aquí la captura de la terminal mostrando la URL local)*

### 6.3 Comunicación entre frontend y backend

Con ambos servidores en marcha, al abrir http://localhost:5173 la aplicación realiza una petición a `/api/health` y muestra en pantalla los datos devueltos por el backend, lo que demuestra que las dos piezas se comunican.

> **Captura 3 — Interfaz mostrando la respuesta de la API**
> *(insertar aquí la captura del navegador con el indicador «API operativa» y los datos)*

> **Captura 4 — Pestaña de red del navegador**
> *(opcional pero recomendable: la petición a `/api/health` con código 200, que prueba la comunicación de forma inequívoca)*

### 6.4 Compilación de producción

```bash
npm run build --prefix frontend
```

La compilación finaliza sin errores y genera la carpeta `dist/`.

---

## 7. Problemas encontrados y soluciones

| # | Problema | Causa | Solución |
|---|---|---|---|
| 1 | El nombre del repositorio aparecía como `Vig-a` | GitHub no admite caracteres no ASCII en el nombre del repositorio y sustituye la tilde | Nombrar el repositorio `vigia` sin tilde y reservar «Vigía» para el título del proyecto y la interfaz |
| 2 | *(completar)* Error de CORS al llamar a la API desde el navegador | El navegador bloquea las peticiones entre orígenes distintos (5173 → 4000) si el servidor no lo autoriza | Middleware `cors` en el backend, con el origen permitido configurado en `CORS_ORIGIN` |
| 3 | *(completar)* Los cambios en `.env` no se aplicaban | Vite solo lee las variables de entorno al arrancar, y únicamente expone al navegador las que empiezan por `VITE_` | Reiniciar el servidor de desarrollo tras modificar el fichero y respetar el prefijo `VITE_` |
| 4 | *(completar con cualquier otro problema real que surja)* | | |

> Los problemas marcados como *(completar)* están redactados a partir de los fallos habituales en este montaje. Sustituye o amplía la tabla con los que te ocurran realmente: el documento debe reflejar tu proceso.

---

## 8. Verificación final

- [ ] El repositorio no contiene `node_modules/` ni ficheros `.env`.
- [ ] `.env.example` documenta todas las variables necesarias.
- [ ] El backend arranca siguiendo únicamente el `README.md`.
- [ ] El frontend arranca siguiendo únicamente el `README.md`.
- [ ] La interfaz muestra la respuesta de `/api/health`.
- [ ] Las capturas de este documento están insertadas.
- [ ] El historial de Git tiene commits descriptivos y las ramas de trabajo integradas en `main`.
