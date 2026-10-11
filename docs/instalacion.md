# Hito 1 — Instalación y configuración del entorno

Vigía · Proyecto Intermodular 2º de Desarrollo de Aplicaciones Web (DAW)
Autor: José Javier Contreras Morillo

Este documento recoge cómo se ha montado el entorno de desarrollo, las pruebas realizadas para comprobar que funciona y los problemas encontrados durante el proceso. Las instrucciones para que una persona ajena al proyecto lo levante están en el [`README.md`](../README.md); aquí se documenta el proceso seguido.

---

## 1. Entorno de trabajo

| Elemento | Versión utilizada |
|---|---|
| Sistema operativo | *(completar: Windows 11 …)* |
| Terminal | Windows PowerShell 5.1 |
| Node.js | 22.12 o superior (lo exige Vite 8) |
| npm | 10.x |
| Git | 2.x |
| Docker | *(completar si se ha usado)* |
| Editor | *(completar: Visual Studio Code …)* |

---

## 2. Creación del repositorio

1. Repositorio creado en GitHub con el nombre `vigia`, rama principal `main`.
2. Clonado por HTTPS con token personal de acceso. **No se usa SSH**, porque el acceso por SSH está bloqueado en la red del centro (WIFI_EDU).

```bash
git clone https://github.com/Xenofle/vigia.git
cd vigia
```

3. Estrategia de ramas: `main` como rama estable y una rama de trabajo por bloque funcional, integrada mediante *pull request*. Al ser un proyecto individual no se emplea rama `develop` intermedia.

```bash
git checkout -b feat/boilerplate-backend
```

4. Se añade un fichero `.gitattributes` con `* text=auto eol=lf` para normalizar los finales de línea, ya que el desarrollo se hace en Windows y los contenedores son Linux.

---

## 3. Estructura de carpetas

```
vigia/
├── backend/
├── frontend/
├── docs/
├── .gitignore
├── .gitattributes
├── .env.example
└── README.md
```

El `.gitignore` de la raíz excluye `node_modules/`, los ficheros `.env` y las carpetas de compilación (`dist/`, `build/`), de modo que en el repositorio no hay ni dependencias ni secretos. Solo se versionan los ficheros `.env.example`, que documentan qué variables hacen falta sin incluir ningún valor sensible.

---

## 4. Instalación del backend (Node + Express)

```powershell
cd backend
npm init -y
npm install express cors dotenv
```

Ajustes realizados sobre el `package.json` generado:

- `"type": "module"` para usar sintaxis de módulos ECMAScript (`import`/`export`) en lugar de CommonJS.
- Scripts `dev` (con `node --watch`, recarga automática nativa de Node, sin necesidad de `nodemon`) y `start` (arranque simple, el que se usa dentro del contenedor).

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

```powershell
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

En la primera terminal:

```powershell
cd backend
npm run dev
```

En una segunda terminal:

```powershell
curl.exe http://localhost:4000/api/health
```

Respuesta obtenida:

```json
{
  "estado": "ok",
  "servicio": "vigia-api",
  "version": "0.1.0",
  "entorno": "development",
  "marcaDeTiempo": "2026-10-11T11:22:29.899Z",
  "tiempoActivoSegundos": 19
}
```

La respuesta incluye además la cabecera `Access-Control-Allow-Origin: http://localhost:5173`, lo que confirma que el CORS está configurado para el cliente.

Se comprueba también que una ruta inexistente devuelve JSON y no una página de error HTML:

```powershell
curl.exe http://localhost:4000/api/nada
# {"error":"Recurso no encontrado","ruta":"/api/nada"}
```

> **Captura 1 — Backend arrancado y respuesta de `/api/health`**
> *(insertar aquí la captura: terminal con el servidor arrancado y la respuesta)*

### 6.2 El frontend arranca

En otra terminal:

```powershell
cd frontend
npm run dev
```

Vite indica la URL local en la que queda disponible el cliente (http://localhost:5173).

> **Captura 2 — Servidor de desarrollo de Vite arrancado**
> *(insertar aquí la captura de la terminal mostrando la URL local)*

### 6.3 Comunicación entre frontend y backend

Con ambos servidores en marcha, al abrir http://localhost:5173 la aplicación realiza una petición a `/api/health` y muestra en pantalla los datos devueltos por el backend, lo que demuestra que las dos piezas se comunican.

> **Captura 3 — Interfaz mostrando la respuesta de la API**
> *(insertar aquí la captura del navegador con el indicador «API operativa» y los datos)*

> **Captura 4 — Pestaña de red del navegador**
> *(la petición a `/api/health` con código 200, que prueba la comunicación de forma inequívoca)*

### 6.4 Compilación de producción

```powershell
cd frontend
npm run build
```

La compilación finaliza sin errores y genera la carpeta `dist/`.

### 6.5 Comprobación de reproducibilidad

Para verificar que las instrucciones del `README.md` son reproducibles, se clonó el repositorio en una carpeta distinta y se siguieron los pasos desde cero, sin usar nada del entorno ya montado. Los problemas detectados en esa prueba están recogidos en el apartado siguiente y corregidos en el `README.md`.

---

## 7. Problemas encontrados y soluciones

| # | Problema | Causa | Solución |
|---|---|---|---|
| 1 | El nombre del repositorio aparecía como `Vig-a` | GitHub no admite caracteres no ASCII en el nombre del repositorio y sustituye la tilde | Nombrar el repositorio `vigia` sin tilde y reservar «Vigía» para el título del proyecto y la interfaz |
| 2 | `npm install --prefix backend` fallaba con `ENOENT: package.json` | En Windows, npm sigue buscando el `package.json` en el directorio actual aunque se indique `--prefix` | Sustituir esas instrucciones por `cd` a cada carpeta antes de ejecutar npm, que funciona igual en los tres sistemas operativos |
| 3 | `curl` mostraba un aviso de riesgo de ejecución de script | En PowerShell, `curl` es un alias de `Invoke-WebRequest`, que analiza el contenido de la página | Usar `curl.exe`, que es el programa real, o `Invoke-RestMethod`, que además devuelve el JSON ya convertido |
| 4 | Vite no arrancaba: `Cannot find native binding` | El `package-lock.json` se había generado en otro sistema operativo y no incluía el binario nativo de Rolldown para Windows | Eliminar `node_modules` y el lockfile y reinstalar las dependencias en la máquina de desarrollo. Además, en el `Dockerfile` del frontend se usa `npm install` en vez de `npm ci`, para que el contenedor Linux resuelva su propio binario |
| 5 | Avisos `EBADENGINE` al instalar el frontend | Vite 8 requiere Node 20.19 o 22.12 en adelante, y la versión instalada era la 22.11 | Actualizar Node a la última versión LTS y corregir el requisito mínimo documentado en el `README.md` |
| 6 | El `git pull` abortaba con «local changes would be overwritten» | Había cambios sin confirmar en el `README.md` al intentar actualizar la rama | Confirmar o guardar los cambios antes de actualizar. Se adopta la costumbre de ejecutar `git status` antes de cualquier `pull` o cambio de rama |
| 7 | Los comandos encadenados con `&&` no funcionaban | Windows PowerShell 5.1 no admite ese operador, que sí está disponible en PowerShell 7 y en Bash | Escribir cada comando en su propia línea en toda la documentación |

---

## 8. Verificación final

- [ ] El repositorio no contiene `node_modules/` ni ficheros `.env`.
- [ ] `.env.example` documenta todas las variables necesarias.
- [ ] El backend arranca siguiendo únicamente el `README.md`.
- [ ] El frontend arranca siguiendo únicamente el `README.md`.
- [ ] La interfaz muestra la respuesta de `/api/health`.
- [ ] Las capturas de este documento están insertadas.
- [ ] El historial de Git tiene commits descriptivos y las ramas de trabajo integradas en `main`.
