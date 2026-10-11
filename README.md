# Vigía — Plataforma de monitorización y página de estado

Proyecto Intermodular — 2º de Desarrollo de Aplicaciones Web (DAW)
IES Severo Ochoa, Elche · Curso 2026/2027
Autor: José Javier Contreras Morillo

---

## Índice

1. [Descripción](#descripción)
2. [Justificación](#justificación)
3. [Tecnologías](#tecnologías)
4. [Estructura del repositorio](#estructura-del-repositorio)
5. [Requisitos previos](#requisitos-previos)
6. [Puesta en marcha en local](#puesta-en-marcha-en-local)
7. [Alternativa: arranque con Docker](#alternativa-arranque-con-docker)
8. [Comandos disponibles](#comandos-disponibles)
9. [Flujo de trabajo con Git](#flujo-de-trabajo-con-git)
10. [Estado del proyecto](#estado-del-proyecto)

---

## Descripción

Cualquier organización que ofrece servicios en línea necesita saber si esos servicios funcionan, y enterarse antes de que se lo diga un cliente enfadado. Comprobarlo a mano no es viable y los productos comerciales del sector (UptimeRobot, Better Stack, Statuspage) resuelven exactamente ese problema.

**Vigía** es una aplicación web que supervisa de forma automática y continua la disponibilidad de servicios web y servidores. El usuario da de alta monitores sobre una URL o un puerto, y el sistema los comprueba periódicamente en segundo plano, registrando el resultado y la latencia de cada comprobación.

Cuando un monitor falla varias veces seguidas, el sistema lo marca como caído, abre una incidencia y envía un aviso por correo electrónico. El estado se refleja en tiempo real, sin recargar la página, en un panel de gestión privado.

Hay dos perfiles de usuario y, por tanto, dos interfaces: el **personal técnico**, que configura monitores y gestiona incidencias desde el panel privado; y el **usuario final**, que consulta una **página de estado pública** con el estado actual de cada servicio, el historial de disponibilidad de los últimos 90 días y las incidencias publicadas.

## Justificación

La monitorización es una necesidad real de cualquier organización con servicios en línea, y existen productos comerciales equivalentes que validan el planteamiento. Desde el punto de vista académico, el proyecto obliga a trabajar procesos en segundo plano, gestión de series temporales, comunicación en tiempo real y despliegue con contenedores, que son competencias directamente aplicables en el entorno profesional.

---

## Tecnologías

Resumen de la pila y, a continuación, la justificación de cada elección frente a la alternativa descartada.

| Capa | Tecnología |
|---|---|
| Cliente | React 19 + Vite + Tailwind CSS 4 |
| Servidor | Node.js 22 + Express 5 |
| Base de datos | PostgreSQL 16 (a partir del Hito 2) |
| Contenedores | Docker + Docker Compose |
| Control de versiones | Git · `main` + ramas de trabajo · Conventional Commits |

### Guía de estilo / diseño

**Tailwind CSS** con un conjunto propio de tokens de color, espaciado y tipografía definidos en el bloque `@theme`.

El proyecto tiene dos interfaces con necesidades opuestas: un panel técnico denso, con mucha información por pantalla, y una página pública minimalista. Un framework de componentes cerrado como Bootstrap impondría el mismo aspecto a ambas y obligaría a pelearse con sus estilos. Tailwind aporta un sistema de utilidades coherente sin imponer componentes, de modo que los tokens se comparten entre las dos interfaces pero cada una mantiene su propio lenguaje visual.

Los estados de servicio (activo, degradado, caído) se definen como tokens semánticos y no como colores sueltos, para garantizar el mismo significado en ambas interfaces y poder revisar el contraste en un único sitio (objetivo de accesibilidad AA).

### Backend

**Node.js** con **Express**.

Tres motivos concretos:

1. El núcleo del proyecto es un proceso en segundo plano que lanza decenas de comprobaciones de red simultáneas. El modelo no bloqueante de Node encaja de forma natural con esa carga, que es de entrada y salida y no de cálculo.
2. El sistema necesita comunicación en tiempo real mediante WebSocket; en Node es una integración directa en el mismo proceso que sirve la API.
3. Se usa el mismo lenguaje en cliente y servidor, lo que reduce el coste de cambiar de contexto en un proyecto individual.

Se descartó **PHP con Laravel**, que es sólido para la parte de gestión, pero en el que los procesos de larga duración y el WebSocket requieren piezas adicionales (colas, Reverb o un servidor aparte) que complican el despliegue de un proyecto de este tamaño.

**Express** frente a **NestJS**: NestJS aporta una estructura más rica, pero también una curva de aprendizaje que no se rentabiliza en un proyecto de un solo desarrollador. Se opta por Express con una estructura por capas definida a mano (rutas → servicios → repositorios).

El **motor de comprobaciones se ejecuta como servicio independiente** de la API, aunque comparta el código base y la imagen de contenedor. De esta forma, una comprobación lenta o un fallo del motor nunca afecta al tiempo de respuesta del panel.

### Frontend

**React** con **Vite** como empaquetador.

React por el modelo declarativo: el panel recibe eventos de cambio de estado por WebSocket y la interfaz se actualiza sola a partir del estado, sin manipular el DOM a mano. Es además la tecnología con mayor demanda en el mercado laboral, lo que refuerza el objetivo formativo del proyecto.

Vite frente a Webpack: arranque en desarrollo prácticamente inmediato, recarga en caliente muy rápida y configuración mínima. Webpack ofrece más control del que este proyecto necesita a cambio de bastante más configuración.

Se descartó **Angular** por sobredimensionado para una sola persona, y **Vue** por decisión formativa (React tiene más recorrido profesional).

### Base de datos

**PostgreSQL** (modelo relacional).

Los datos del sistema están fuertemente relacionados: monitores que pertenecen a servicios, comprobaciones que pertenecen a monitores, incidencias con actualizaciones y con servicios afectados. Un modelo relacional con claves foráneas garantiza la integridad de esas relaciones a nivel de motor y no de código.

Además, el proyecto se apoya intensamente en consultas de agregación sobre el histórico (porcentaje de disponibilidad, medias y percentiles de latencia por intervalo). SQL, con funciones de ventana e índices compuestos, es la herramienta adecuada para eso.

Se descartó **MongoDB**: la flexibilidad de esquema no aporta nada aquí, porque el esquema es conocido y estable, y en cambio se perdería la integridad referencial.

Se descartó también una base de datos específica de series temporales (**InfluxDB**, **TimescaleDB**): encajaría bien con la tabla de comprobaciones, pero obligaría a mantener dos motores de base de datos y a introducir una tecnología fuera del temario. El crecimiento del histórico se resuelve con índices compuestos y una tabla de agregados horarios.

### Documentación

| Tipo | Herramienta |
|---|---|
| Documentación general del proyecto | Markdown en el propio repositorio (`/docs`) |
| API REST | **OpenAPI 3** con interfaz **Swagger UI** servida por la propia API |
| Código | **JSDoc** en servicios y en la lógica de estados |
| Base de datos | Diagrama entidad-relación exportado a `/docs` |

La API se documenta con OpenAPI porque es el estándar del sector y permite probar los endpoints desde el navegador durante el desarrollo, sin depender de una herramienta externa.

### Librerías y dependencias relevantes

**Servidor**

| Librería | Función | Motivo |
|---|---|---|
| `express` | Framework HTTP | Minimalista y suficiente para una API REST |
| `cors` | Control de orígenes | El cliente y la API se sirven en puertos distintos |
| `dotenv` | Variables de entorno | Carga la configuración sin incrustarla en el código |
| `prisma` | ORM y migraciones *(Hito 2)* | Tipado del modelo y migraciones reproducibles |
| `jsonwebtoken` | Autenticación *(Hito 2)* | Sesión sin estado, adecuada para una API consumida por una SPA |
| `argon2` | Cifrado de contraseñas *(Hito 2)* | Algoritmo recomendado actualmente frente a bcrypt |
| `zod` | Validación de entrada *(Hito 2)* | Valida el cuerpo de las peticiones en un único punto |
| `socket.io` | Tiempo real *(Hito 3)* | Reconexión automática y salas, frente a WebSocket nativo |
| `nodemailer` | Envío de alertas *(Hito 3)* | Estándar de facto para SMTP en Node |

**Cliente**

| Librería | Función | Motivo |
|---|---|---|
| `react` / `react-dom` | Interfaz | Modelo declarativo, idóneo para datos que cambian solos |
| `vite` | Empaquetador y servidor de desarrollo | Arranque y recarga muy rápidos |
| `tailwindcss` | Estilos | Ver apartado de guía de diseño |
| `@tanstack/react-query` | Estado del servidor *(Hito 2)* | Caché y revalidación sin escribirlas a mano |
| `recharts` | Gráficas *(Hito 3)* | Construida sobre componentes de React |

**Calidad** *(a partir del Hito 2)*: `vitest` para pruebas unitarias, `supertest` para pruebas de integración de la API, y `eslint` con `prettier` para análisis estático y formato uniforme.

La planificación de las comprobaciones se implementará con un **planificador propio** basado en temporizadores, sin `BullMQ` ni Redis. Para el volumen previsto (unos 100 monitores con intervalo de 60 segundos) una cola distribuida añadiría un servicio más al despliegue y un concepto más que mantener, sin aportar nada. Queda documentado como línea de evolución si el volumen creciera.

### Otros: contenedores y despliegue

**Docker** y **Docker Compose**, incorporados desde el inicio del desarrollo y no al final. El sistema se compone de varios servicios y Compose permite levantar el conjunto con un único comando, garantizando que el entorno de desarrollo y el de despliegue son equivalentes.

**Integración continua:** GitHub Actions. En cada *push* se ejecutarán el análisis estático, las pruebas y la construcción de las imágenes.

**Entorno de despliegue previsto:** servidor virtual privado con Docker y Nginx, certificado TLS mediante Let's Encrypt, variables de entorno en fichero `.env` fuera del repositorio y copia de seguridad diaria de la base de datos con `pg_dump`.

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
| Node.js | 20.19 o 22.12 en adelante (lo exige Vite 8) | `node -v` |
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
cd backend
npm install
cd ../frontend
npm install
cd ..
```

### 4. Preparar la base de datos

**No es necesario en este hito.** El proyecto todavía no tiene modelo de datos ni migraciones: el servicio de PostgreSQL está declarado en `docker-compose.yml` y la variable `DATABASE_URL` queda preparada para el Hito 2, pero la API arranca y funciona sin base de datos.

### 5. Arrancar el backend

En la primera terminal, desde la raíz del proyecto:

```bash
cd backend
npm run dev
```

Queda disponible en **http://localhost:4000**, con el endpoint de comprobación en **http://localhost:4000/api/health**.

### 6. Arrancar el frontend

En la segunda terminal, también desde la raíz del proyecto:

```bash
cd frontend
npm run dev
```

Queda disponible en **http://localhost:5173**.

### 7. Comprobar que funciona

**a) La API responde por sí sola:**

```bash
curl http://localhost:4000/api/health
```

En **PowerShell**, `curl` es un alias de `Invoke-WebRequest` y muestra un aviso de seguridad. Usa cualquiera de estas dos formas:

```powershell
curl.exe http://localhost:4000/api/health
Invoke-RestMethod http://localhost:4000/api/health
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

- [`docs/hito0-tecnologias.md`](docs/hito0-tecnologias.md) — entregable del Hito 0, con la definición tecnológica recogida también en este README.
- [`docs/instalacion.md`](docs/instalacion.md) — instalación del entorno, pruebas realizadas y problemas encontrados.
