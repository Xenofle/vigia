# Vigía — Plataforma de monitorización y página de estado

Proyecto Intermodular — 2º de Desarrollo de Aplicaciones Web (DAW)
IES Severo Ochoa, Elche · Curso 2026/2027
Autor: José Javier Contreras Morillo

---

## Índice

1. [Descripción](#descripción)
2. [Objetivos](#objetivos)
3. [Tecnologías](#tecnologías)
4. [Esquema entidad-relación](#esquema-entidad-relación)
5. [Estructura del repositorio](#estructura-del-repositorio)
6. [Requisitos previos](#requisitos-previos)
7. [Puesta en marcha en local](#puesta-en-marcha-en-local)
8. [Alternativa: arranque con Docker](#alternativa-arranque-con-docker)
9. [Comandos disponibles](#comandos-disponibles)
10. [Tutorial de uso](#tutorial-de-uso)
11. [Flujo de trabajo con Git](#flujo-de-trabajo-con-git)
12. [Estado del proyecto](#estado-del-proyecto)
13. [Enlaces del proyecto](#enlaces-del-proyecto)
14. [Bitácora](#bitácora)
15. [Bibliografía](#bibliografía)

---

## Descripción

Cualquier organización que ofrece servicios en línea necesita saber si esos servicios funcionan, y enterarse antes de que se lo diga un cliente. Comprobarlo a mano no es viable, y existen productos comerciales dedicados a ello (UptimeRobot, Better Stack, Statuspage) que confirman que el problema es real.

**Vigía** es una aplicación web que supervisa de forma automática y continua la disponibilidad de servicios web y servidores. El usuario da de alta monitores sobre una URL o un puerto, y el sistema los comprueba periódicamente en segundo plano, registrando el resultado y la latencia de cada comprobación.

Cuando un monitor falla varias veces seguidas, el sistema lo marca como caído, abre una incidencia y envía un aviso por correo electrónico.

Al tratarse de un servicio que se presta a terceros, la aplicación incorpora además un **módulo de facturación y cobro**, que gestiona los clientes a los que se factura la supervisión, sus facturas y los cobros asociados.

### Las dos caras de la aplicación

- **Zona de gestión privada**, accesible solo con el rol correspondiente, donde el personal técnico configura servicios y monitores, consulta el histórico, gestiona las incidencias y lleva la facturación.
- **Página de estado pública**, sin autenticación, donde cualquier usuario consulta el estado actual de los servicios, el historial de disponibilidad de los últimos 90 días y las incidencias publicadas.

El control de acceso se apoya en el sistema de autenticación de Django, con dos perfiles: **administrador**, que gestiona usuarios y permisos además del contenido, y **operador**, que gestiona servicios, monitores, incidencias y facturación pero no usuarios.

## Objetivos

**Objetivo general**

Desarrollar y desplegar una aplicación web completa que permita definir monitores sobre servicios, comprobar su estado de forma automática y periódica, notificar los fallos, publicar el estado de los servicios y gestionar la facturación del servicio prestado.

**Objetivos específicos**

1. Diseñar un modelo de datos relacional preparado para el crecimiento de la información histórica.
2. Implementar una zona de administración con control de acceso por roles.
3. Implementar un proceso de comprobación periódica independiente de la atención de peticiones web.
4. Aplicar una lógica de estados tolerante a fallos puntuales, basada en reintentos, que evite falsas alarmas.
5. Ofrecer actualización en tiempo real de la información del panel.
6. Implementar un sistema de notificaciones por correo electrónico ante cambios de estado.
7. Gestionar clientes, facturas y cobros asociados al servicio prestado.
8. Desarrollar dos interfaces diferenciadas, una privada y otra pública, con criterios de accesibilidad.
9. Desplegar la aplicación mediante contenedores, con un flujo de integración continua.

---

## Tecnologías

| Capa | Tecnología |
|---|---|
| Servidor | Python 3.13 + Django 5.2 |
| Plantillas | Django Template Language + Bootstrap 5.2 |
| Base de datos | SQLite en desarrollo; PostgreSQL prevista para el despliegue |
| ORM | El de Django, con migraciones versionadas |
| Contenedores | Docker + Docker Compose |
| Control de versiones | Git · `main` + ramas de trabajo · Conventional Commits |

### Backend

**Django** aporta de serie dos piezas que este proyecto necesita y que de otro modo habría que construir: el sistema de autenticación con usuarios, grupos y permisos, y el panel de administración, que cubre directamente el requisito de disponer de una zona de gestión restringida por rol. Su ORM gestiona el esquema mediante migraciones versionadas, lo que mantiene la base de datos sincronizada con el código a lo largo del curso.

Se emplea la **versión 5.2** y no la más reciente. Aunque existen versiones posteriores, la 5.2 es la última con soporte a largo plazo, lo que garantiza mantenimiento durante más tiempo y mayor compatibilidad con los paquetes de terceros. Elegir la última versión daría acceso a funcionalidades más nuevas a cambio de más errores y menos compatibilidad.

### Organización en aplicaciones

El proyecto se divide en tres aplicaciones independientes, según la forma de modularizar propia de Django:

- **`core`** — la monitorización: servicios, monitores, comprobaciones e incidencias.
- **`billing`** — la facturación: clientes, facturas y cobros.
- **`common`** — código compartido entre las anteriores, plantillas base y navegación.

Esta separación permite que cada bloque sea autónomo y reutilizable, y mantiene la lógica de negocio dividida por responsabilidades.

### Presentación

La zona de gestión se construye con el **motor de plantillas de Django** y **Bootstrap 5**, sobre una jerarquía de herencia de tres niveles: una plantilla base con la estructura común, una plantilla de intranet que añade el menú lateral, y las plantillas concretas de cada listado y detalle. Así, un cambio en la cabecera o en el pie afecta a todas las pantallas a la vez.

Las vistas son **genéricas basadas en clases** (`ListView` y `DetailView`): Django consulta la base de datos y prepara el contexto, y la plantilla se limita a mostrarlo. Es la separación entre lógica de negocio y presentación llevada a la práctica.

### Base de datos

Se trabaja sobre **SQLite** durante el desarrollo, que es la base de datos que Django configura por defecto y resulta adecuada para un volumen reducido de datos. Para el despliegue está prevista la migración a **PostgreSQL**, por tratarse de un motor preparado para mayor volumen y concurrencia. El cambio no afecta al código, porque el acceso a datos se hace íntegramente a través del ORM.

El modelo es **relacional** porque los datos están fuertemente relacionados y las claves foráneas garantizan la integridad a nivel de motor. Además, el proyecto se apoya en consultas de agregación sobre el histórico (disponibilidad, medias y percentiles de latencia), para las que SQL con índices compuestos es la herramienta adecuada. Se descarta un modelo documental porque el esquema es conocido y estable, y se perdería la integridad referencial.

### Contenedores

**Docker** y **Docker Compose**, incorporados desde el inicio del desarrollo y no al final: conviene que el entorno de desarrollo y el de despliegue sean equivalentes.

### Cliente público

La página de estado pública se desarrollará con **React** y **Vite**, por su modelo declarativo: recibe los cambios de estado y actualiza la interfaz a partir del estado, sin manipular el DOM a mano. La carpeta `frontend/` contiene el trabajo realizado hasta ahora y está en pausa mientras se define su encaje con las plantillas de Django.

---

## Esquema entidad-relación

### Entidades de monitorización (`core`)

- **Servicio** — sistema supervisado. Agrupa monitores y dispone de página de estado pública.
- **Monitor** — comprobación configurada sobre una URL o un puerto, con su intervalo y su estado actual.
- **Comprobación** — resultado de cada ejecución de un monitor, con la latencia y el código de respuesta.
- **Incidencia** — interrupción de servicio, abierta automáticamente al detectarse una caída o manualmente.
- **Actualización de incidencia** — cada entrada de la cronología de una incidencia.

### Entidades de facturación (`billing`)

- **Cliente** — persona o entidad a la que se emiten facturas.
- **Factura** — documento emitido a un cliente por el servicio prestado.
- **Cobro** — pago, total o parcial, asociado a una factura.

### Relaciones

```
Usuario (1) ─────< (N) Monitor

Servicio (1) ─────< (N) Monitor (1) ─────< (N) Comprobacion
    │                      │
    └──< (N) Incidencia <──┘ (opcional)
                 │
                 └──< (N) ActualizacionIncidencia


Cliente (1) ─────< (N) Factura (1) ─────< (N) Cobro
```

- Un **servicio** tiene muchos **monitores**; el nombre de un monitor no se repite dentro del mismo servicio.
- Un **monitor** acumula muchas **comprobaciones**.
- Un **servicio** puede tener varias **incidencias**, que referencian opcionalmente al monitor que las originó: la referencia queda a nulo en las abiertas manualmente.
- Una **incidencia** tiene muchas **actualizaciones**, que forman su cronología.
- Un **cliente** tiene muchas **facturas**, y una factura puede recibir varios **cobros** parciales.

### Decisiones de diseño

El **estado actual** del monitor se almacena en la propia tabla de monitores en lugar de calcularse a partir del histórico. Es una desnormalización deliberada: mostrar el panel no puede implicar recorrer millones de filas de comprobaciones.

La tabla de comprobaciones lleva un **índice compuesto** por monitor y fecha descendente, porque todas las consultas son del tipo «las últimas comprobaciones de este monitor».

El comportamiento ante el **borrado** se decide por entidad: en cascada cuando el registro hijo carece de sentido sin el padre, protegido para impedir eliminar un cliente con facturas o un usuario con monitores a su nombre, y a nulo cuando el dato histórico debe sobrevivir aunque desaparezca la referencia.

---

## Estructura del repositorio

```
vigia/
├── piapp-env/              # entorno virtual (no versionado)
├── backend/
│   ├── vigiaDjango/        # configuración: settings.py, urls.py
│   ├── common/             # código compartido, vistas Home y Panel
│   ├── core/               # monitorización
│   ├── billing/            # facturación
│   ├── templates/
│   │   ├── common/         # plantillas base, panel, menú, paginación
│   │   ├── core/           # listados y detalles de core
│   │   └── billing/        # listados y detalles de billing
│   ├── fixtures/           # datos de prueba
│   ├── manage.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── docker-compose.yml
├── docs/                   # documentación técnica y capturas
├── frontend/               # cliente React (en pausa)
└── README.md
```

---

## Requisitos previos

| Herramienta | Versión | Comprobación |
|---|---|---|
| Python | 3.11 o superior (probado con 3.13) | `python --version` |
| pip | incluido con Python | `pip --version` |
| Git | 2.x | `git --version` |
| Docker *(opcional)* | 24 | `docker --version` |

---

## Puesta en marcha en local

### 1. Clonar el repositorio

```powershell
git clone https://github.com/Xenofle/vigia.git
cd vigia
```

### 2. Crear y activar el entorno virtual

```powershell
python -m venv piapp-env
.\piapp-env\Scripts\Activate.ps1
```

El prompt debe empezar por `(piapp-env)`. Si PowerShell se niega a ejecutar el script de activación:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### 3. Instalar las dependencias

```powershell
cd backend
pip install -r requirements.txt
```

### 4. Preparar la base de datos

```powershell
python manage.py migrate
python manage.py createsuperuser
```

Opcionalmente, cargar los datos de prueba incluidos en el repositorio:

```powershell
python manage.py loaddata fixtures/datos_prueba.json
```

### 5. Arrancar la aplicación

```powershell
python manage.py runserver
```

La aplicación queda disponible en **http://localhost:8000/** y el administrador en **http://localhost:8000/admin/**.

> **No arranques con `runserver 0.0.0.0:8000` en local.** En Windows, `localhost` se resuelve primero como IPv6 y la conexión se rechaza. Esa dirección solo se usa dentro del contenedor.

### 6. Comprobar que funciona

Entra en **http://localhost:8000/panel/** con el superusuario. Desde ahí se accede a los listados de las dos aplicaciones, y desde cada listado al detalle de cada registro.

---

## Alternativa: arranque con Docker

```powershell
cd backend
docker compose up --build        # primera vez
docker compose up                # arranques posteriores
docker compose down              # detener
```

El contenedor publica el puerto 8000 de la aplicación en el puerto indicado en `docker-compose.yml`. Requiere Docker Desktop en marcha.

---

## Comandos disponibles

| Comando | Descripción |
|---|---|
| `python manage.py runserver` | Servidor de desarrollo |
| `python manage.py check` | Valida configuración, modelos y administrador sin arrancar |
| `python manage.py makemigrations` | Genera migraciones tras modificar los modelos |
| `python manage.py migrate` | Aplica las migraciones pendientes |
| `python manage.py createsuperuser` | Crea un usuario con acceso al administrador |
| `python manage.py collectstatic` | Recolecta los ficheros estáticos |
| `python manage.py shell` | Consola con la configuración del proyecto cargada |
| `python manage.py dumpdata billing core --indent 2 --output fixtures/datos_prueba.json` | Exporta los datos de prueba |
| `python manage.py loaddata fixtures/datos_prueba.json` | Restaura los datos de prueba |

> Usa siempre la opción `--output` de `dumpdata`. La redirección `>` de PowerShell escribe el fichero en UTF-16 y `loaddata` no puede leerlo.

---

## Tutorial de uso

*(Pendiente: recorrido por la aplicación con capturas de pantalla, en `docs/tutorial.md`.)*

Las capturas del administrador y de los listados están en [`docs/img/`](docs/img/).

---

## Flujo de trabajo con Git

- **`main`**: rama estable. No se trabaja directamente sobre ella; solo recibe código mediante *pull request*.
- **Ramas de trabajo**: una por bloque funcional, con prefijo `feat/`, `fix/`, `docs/` o `chore/`.
- **Mensajes de commit**: [Conventional Commits](https://www.conventionalcommits.org/) en español, citando el código de tarea del boletín cuando corresponda.
  Ejemplos: `feat(core): vistas y URLs de los cinco modelos (UD3.7)`, `fix(fixtures): regenera los datos con codificación UTF-8`.
- **Etiquetas**: una por hito entregado (`hito-0`, `hito-1`, …).

---

## Estado del proyecto

| Hito | Contenido | Estado |
|---|---|---|
| Hito 0 | Repositorio y definición tecnológica | Completado |
| Hito 1 | Proyecto base funcionando en local y documentado | Completado |
| Hito 2 | Modelo de datos, administración, ORM, vistas, URLs y plantillas | En curso |
| Hito 3 | Motor de comprobaciones, histórico, alertas e incidencias | Pendiente |
| Hito 4 | Página de estado pública y actualización en tiempo real | Pendiente |
| Hito 5 | Despliegue, integración continua y documentación final | Pendiente |

---

## Enlaces del proyecto

| Recurso | Enlace |
|---|---|
| Anteproyecto (ClickUp) | *(pendiente de añadir)* |
| Diseño de la aplicación | *(pendiente)* |
| Landing page desplegada | *(pendiente)* |
| Presentación en PDF | *(pendiente)* |
| Vídeo explicativo | *(pendiente, para el checkpoint)* |

---

## Bitácora

Registro de las tareas realizadas. El detalle completo, con estimaciones y estado, está en el espacio de ClickUp enlazado arriba.

| Fecha | Tarea |
|---|---|
| Septiembre 2026 | Hito 0: creación del repositorio y definición tecnológica |
| Octubre 2026 | Hito 1: proyecto base, arranque en local y documentación |
| Octubre 2026 | Cambio de stack a Django, Docker y React por requisito del profesorado |
| Octubre 2026 | Puesta a punto del proyecto Django con las aplicaciones `common`, `core` y `billing` |
| Octubre 2026 | Modelos de datos, administrador y datos de prueba |
| Octubre 2026 | Operaciones con el ORM |
| Octubre 2026 | Vistas, URLs, plantillas y paginación |

---

## Documentación relacionada

- [`docs/hito0-tecnologias.md`](docs/hito0-tecnologias.md) — definición tecnológica inicial del proyecto.
- [`docs/instalacion.md`](docs/instalacion.md) — instalación del entorno, pruebas realizadas y problemas encontrados.

---

## Bibliografía

- [Documentación oficial de Django 5.2](https://docs.djangoproject.com/en/5.2/)
- [Modelos de Django](https://docs.djangoproject.com/en/5.2/topics/db/models/)
- [Consultas con el ORM](https://docs.djangoproject.com/en/5.2/topics/db/queries/)
- [Referencia de búsquedas en consultas](https://docs.djangoproject.com/en/5.2/ref/models/querysets/)
- [El administrador de Django](https://docs.djangoproject.com/en/5.2/ref/contrib/admin/)
- [Vistas genéricas basadas en clases](https://docs.djangoproject.com/en/5.2/topics/class-based-views/)
- [Motor de plantillas de Django](https://docs.djangoproject.com/en/5.2/topics/templates/)
- [Paginación](https://docs.djangoproject.com/en/5.2/topics/pagination/)
- [Configuración de aplicaciones](https://docs.djangoproject.com/en/5.2/ref/applications/)
- [Documentación de Bootstrap 5.2](https://getbootstrap.com/docs/5.2/)
- [Documentación de Docker Compose](https://docs.docker.com/compose/)
- [Conventional Commits](https://www.conventionalcommits.org/)
