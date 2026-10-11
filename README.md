# Hito 0 — Definición tecnológica

Vigía · Plataforma de monitorización y página de estado
Proyecto Intermodular — 2º de Desarrollo de Aplicaciones Web (DAW)
IES Severo Ochoa, Elche · Curso 2026/2027
Autor: José Javier Contreras Morillo

---

## Descripción

Cualquier organización que ofrece servicios en línea necesita saber si esos servicios funcionan, y enterarse antes de que se lo diga un cliente enfadado. Comprobarlo a mano no es viable y los productos comerciales del sector (UptimeRobot, Better Stack, Statuspage) resuelven exactamente ese problema.

**Vigía** es una aplicación web que supervisa de forma automática y continua la disponibilidad de servicios web y servidores. El usuario da de alta monitores sobre una URL o un puerto, y el sistema los comprueba periódicamente en segundo plano, registrando el resultado y la latencia de cada comprobación.

Cuando un monitor falla varias veces seguidas, el sistema lo marca como caído, abre una incidencia y envía un aviso por correo electrónico. El estado se refleja en tiempo real, sin recargar la página, en un panel de gestión privado.

Hay dos perfiles de usuario y, por tanto, dos interfaces: el **personal técnico**, que configura monitores y gestiona incidencias desde el panel privado; y el **usuario final**, que consulta una **página de estado pública** con el estado actual de cada servicio, el historial de disponibilidad de los últimos 90 días y las incidencias publicadas.

---

## Tecnologías

Cada elección se justifica frente a la alternativa que se ha descartado.

### Guía de estilo / diseño

**Tailwind CSS** con un conjunto propio de tokens de color, espaciado y tipografía definidos en `tailwind.config.js`.

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
| `prisma` | ORM y migraciones | Tipado del modelo y control de versiones del esquema con migraciones reproducibles |
| `jsonwebtoken` | Autenticación | Sesión sin estado, adecuada para una API consumida por una SPA |
| `argon2` | Cifrado de contraseñas | Algoritmo recomendado actualmente frente a bcrypt |
| `zod` | Validación de entrada | Valida el cuerpo de las peticiones en un único punto y genera los tipos |
| `socket.io` | Tiempo real | Reconexión automática y salas, frente a WebSocket nativo |
| `nodemailer` | Envío de alertas | Estándar de facto para SMTP en Node |
| `undici` / `net` | Comprobaciones HTTP y TCP | Cliente HTTP moderno con control de tiempo de espera; módulo nativo para los sockets |
| `pino` | Registro de eventos | Registro estructurado en JSON, útil para depurar el motor |

**Cliente**

| Librería | Función | Motivo |
|---|---|---|
| `react-router` | Enrutado | Estándar para navegación en React |
| `@tanstack/react-query` | Estado del servidor | Caché, revalidación y estados de carga sin escribirlos a mano |
| `socket.io-client` | Tiempo real | Contraparte del servidor |
| `recharts` | Gráficas de latencia y disponibilidad | Construida sobre componentes de React, suficiente para gráficas de serie temporal |
| `tailwindcss` | Estilos | Ver apartado de guía de diseño |

**Calidad**

| Librería | Función |
|---|---|
| `vitest` | Pruebas unitarias (máquina de estados, cálculo de disponibilidad) |
| `supertest` | Pruebas de integración de la API |
| `eslint` + `prettier` | Análisis estático y formato uniforme |

La planificación de las comprobaciones se implementa con un **planificador propio** basado en temporizadores, sin `BullMQ` ni Redis. Para el volumen previsto (unos 100 monitores con intervalo de 60 segundos) una cola distribuida añadiría un servicio más al despliegue y un concepto más que mantener, sin aportar nada. Queda documentado como línea de evolución si el volumen creciera.

### Control de versiones y flujo de trabajo

- **Sistema:** Git, alojado en GitHub.
- **Rama principal:** `main`, protegida. Nunca se trabaja directamente sobre ella.
- **Ramas de trabajo:** `feat/<descripcion>`, `fix/<descripcion>`, `docs/<descripcion>`, `chore/<descripcion>`.
- **Integración:** mediante *pull request*, incluso siendo un proyecto individual, para dejar registro escrito de cada bloque funcional y poder revisar los cambios antes de integrarlos.
- **Convención de commits:** [Conventional Commits](https://www.conventionalcommits.org/), en español.
  Ejemplos: `feat(monitors): alta y edición de monitores HTTP`, `fix(worker): reinicio del contador de fallos tras recuperación`, `docs(readme): justificación de tecnologías`.
- **Etiquetas:** una etiqueta por hito del proyecto (`hito-0`, `hito-1`, …).

### Otros

**Contenedores:** **Docker** y **Docker Compose**, incorporados desde el inicio del desarrollo y no al final. El sistema se compone de varios servicios (base de datos, API, motor de comprobaciones, cliente y proxy inverso), y Compose permite levantar el conjunto con un único comando y garantizar que el entorno de desarrollo y el de despliegue son equivalentes.

| Servicio | Contenido |
|---|---|
| `db` | PostgreSQL con volumen persistente |
| `api` | API REST y servidor WebSocket |
| `worker` | Motor de comprobaciones (misma imagen que `api`, distinto comando) |
| `web` | Cliente React compilado y servido de forma estática |
| `proxy` | Nginx como proxy inverso y terminación TLS |

**Integración continua:** **GitHub Actions**. En cada *push* se ejecutan el análisis estático, las pruebas y la construcción de las imágenes; en `main`, además, se publican las imágenes.

**Entorno de despliegue previsto:** servidor virtual privado con Docker y Nginx, certificado TLS mediante Let's Encrypt, variables de entorno en fichero `.env` fuera del repositorio y copia de seguridad diaria de la base de datos con `pg_dump`.

---

## Estructura prevista del repositorio

```
vigia/
├── api/                  # API REST, WebSocket y motor de comprobaciones
│   ├── src/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── worker/       # planificador y ejecución de comprobaciones
│   │   └── lib/
│   └── prisma/           # esquema y migraciones
├── web/                  # cliente React (panel privado y página pública)
│   └── src/
├── docs/                 # documentación, diagramas, OpenAPI
├── docker/               # Dockerfiles y configuración de Nginx
├── docker-compose.yml
└── README.md
```

---

## Estado del proyecto

En desarrollo. Hito 0 completado: repositorio creado y definición tecnológica documentada.
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

Estructura de carpetas del proyecto:

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
cd backend && npm run dev
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
cd frontend && npm run dev
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
cd frontend && npm run build
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
