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