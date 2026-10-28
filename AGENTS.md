# AGENTS.md

Instrucciones para agentes de IA (Claude Code, GitHub Copilot, Cursor…) que trabajen en este repositorio.

---

## Qué es Vigía

Plataforma de monitorización de servicios web con módulo de facturación. El usuario da de alta monitores sobre una URL o un puerto; el sistema los comprueba periódicamente en segundo plano, registra latencia y resultado, marca el servicio como caído si falla varias veces seguidas, abre una incidencia y envía un aviso por correo. La facturación gestiona los clientes a los que se presta el servicio, sus facturas y sus cobros.

Dos interfaces: **zona de gestión privada**, accesible solo con el rol correspondiente, y **página de estado pública** con el estado de los servicios y las incidencias publicadas.

Es el Proyecto Intermodular de 2º de Desarrollo de Aplicaciones Web (DAW). El stack viene fijado por el profesorado: Django, Docker y, en la parte pública, React.

---

## Stack

| Capa | Tecnología |
|---|---|
| Servidor | Python 3.13 + Django 5.2 |
| Plantillas | Django Template Language + Bootstrap 5.2 |
| Base de datos | SQLite en desarrollo; PostgreSQL prevista para el despliegue |
| ORM | El de Django |
| Contenedores | Docker + Docker Compose |
| Cliente público | React 19 + Vite + Tailwind CSS (carpeta `frontend/`, en pausa) |

Se usa Django **5.2** y no la última versión porque es la que tiene soporte a largo plazo.

> La carpeta `frontend/` procede de una etapa anterior del proyecto y **no está en uso**. Queda a la espera de definir cómo encaja React con las plantillas de Django. No tocarla.

---

## Estructura

```
vigia/
├── piapp-env/              entorno virtual (fuera de backend, no versionado)
├── backend/
│   ├── vigiaDjango/        configuración del proyecto: settings.py, urls.py
│   ├── common/             código compartido; vistas Home y Panel; actividadorm.py
│   ├── core/               monitorización: servicios, monitores, comprobaciones, incidencias
│   ├── billing/            facturación: clientes, facturas, cobros
│   ├── templates/
│   │   ├── common/         base.html, base_intranet.html, panel, menú, paginación
│   │   ├── core/           listados y detalles de los cinco modelos
│   │   └── billing/        listados y detalles de los tres modelos
│   ├── fixtures/           datos de prueba exportados con dumpdata
│   ├── manage.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── docker-compose.yml
├── docs/                   documentación del proyecto
└── frontend/               cliente React (en pausa)
```

Las aplicaciones son hermanas de `manage.py`, no van dentro del paquete de configuración.

---

## Cómo arrancar

### Local

```powershell
# Entorno virtual (está fuera de backend)
..\piapp-env\Scripts\Activate.ps1

cd backend
pip install -r requirements.txt
Copy-Item .env.example .env       # si existe
python manage.py migrate
python manage.py runserver
```

Disponible en `http://localhost:8000/`. El administrador, en `/admin/`.

**Arrancar sin indicar dirección.** Con `runserver 0.0.0.0:8000`, en Windows `localhost` se resuelve como IPv6 y la conexión se rechaza. El `0.0.0.0` solo se usa dentro del contenedor.

### Docker

```powershell
docker compose up --build        # primera vez
docker compose up                # arranques posteriores
docker compose down
```

El contenedor publica el 8000 interno en el puerto configurado en `docker-compose.yml`.

### Otros comandos

| Comando | Para qué |
|---|---|
| `python manage.py check` | validar configuración, modelos y administrador sin arrancar |
| `python manage.py makemigrations` | generar migraciones tras tocar los modelos |
| `python manage.py createsuperuser` | crear usuario para el administrador |
| `python manage.py collectstatic` | recolectar estáticos en `backend/static/` |
| `python manage.py shell` | consola con la configuración del proyecto cargada |
| `python manage.py dumpdata billing core --indent 2 --output fixtures/datos_prueba.json` | exportar datos de prueba |
| `python manage.py loaddata fixtures/datos_prueba.json` | restaurar datos de prueba |

> **Nunca uses la redirección `>` de PowerShell con `dumpdata`:** escribe el fichero en UTF-16 y `loaddata` falla. Usa siempre la opción `--output`.

---

## Arquitectura

### Aplicaciones

- **`core`** — la monitorización. Modelos `Servicio`, `Monitor`, `Comprobacion`, `Incidencia` y `ActualizacionIncidencia`.
- **`billing`** — la facturación. Modelos `Cliente`, `Factura` y `Cobro`. Es la parte guiada del módulo; sus campos vienen fijados por el enunciado y **no deben modificarse**.
- **`common`** — código compartido. Vistas `HomeView` y `PanelView`, plantillas base y `actividadorm.py`.

### Decisiones de modelo que no deben deshacerse

- El **estado actual** del monitor (`estado`, `estado_desde`, `fallos_consecutivos`) se almacena en la propia tabla. Es desnormalización deliberada: calcularlo desde el histórico obligaría a recorrer millones de comprobaciones en cada carga del panel.
- El comportamiento ante el borrado se decide por entidad: `CASCADE` cuando el hijo carece de sentido sin el padre, `PROTECT` para impedir borrar algo referenciado (un cliente con facturas, un usuario con monitores) y `SET_NULL` cuando el histórico debe sobrevivir a la referencia.
- Las restricciones de unicidad se declaran con **`unique_together`**, no con `UniqueConstraint`, porque así lo exige el enunciado.

### Vistas y URLs

Vistas genéricas basadas en clases: `ListView` y `DetailView`, con `model` y `template_name`. **Todas las rutas se declaran en `vigiaDjango/urls.py`**, no hay un `urls.py` por aplicación: es el criterio del ejemplo del profesor.

Nomenclatura de rutas: `<modelo>_list/` y `<modelo>_detail/<int:pk>/`, con nombres `<modelo>_list` y `<modelo>_detail`.

### Plantillas

Herencia en tres niveles: `base.html` → `base_intranet.html` → plantilla concreta, que rellena el bloque `main_content`. Los controles de paginación están en `common/paginacion.html` y se insertan con `include` en los ocho listados.

Los enlaces siempre con `{% url %}`, nunca con la ruta escrita a mano.

### Administrador

Cada modelo tiene su clase `ModelAdmin`. Las **comprobaciones son de solo lectura** y tienen el alta bloqueada con `has_add_permission`, porque las genera el sistema. Los campos de estado del monitor están en `readonly_fields` por el mismo motivo.

---

## Convenciones

- **Idioma del código**: identificadores, comentarios y textos en **español**. No traducir al inglés.
- **Comentarios con código de tarea**: cada fragmento lleva encima un comentario con el código de la actividad del boletín, por ejemplo `# UD3.3a - Modelo Servicio`. En las plantillas se usa `{% comment %}`. Los atributos de `ModelAdmin` se comentan en la misma línea y solo la primera vez que aparece cada uno.
- **Commits**: [Conventional Commits](https://www.conventionalcommits.org/) en español, citando el código de tarea cuando corresponda.
  Ejemplos: `feat(core): vistas y URLs de los cinco modelos (UD3.7)`, `fix(fixtures): regenera los datos con codificación UTF-8`.
- **Ramas**: una por bloque de trabajo, con prefijo `feat/`, `fix/`, `docs/` o `chore/`. Nunca trabajar directamente sobre `main`.
- **Integración**: solo mediante pull request a `main`.
- **Etiquetas**: una por hito entregado — `hito-0`, `hito-1`, `hito-2`…

---

## Qué no hacer

- **No modificar los modelos de `billing`.** Sus campos, nombres y restricciones vienen fijados por el enunciado.
- **No traducir identificadores al inglés.** Todo el código está en español.
- **No omitir los comentarios con código de tarea.** Son un criterio de evaluación: el código sin identificar no se evalúa.
- **No sustituir `unique_together` por `UniqueConstraint`**, aunque sea lo que Django recomienda hoy.
- **No crear un `urls.py` por aplicación.** Todas las rutas van en el del proyecto.
- **No editar a mano los ficheros de migraciones.**
- **No tocar `frontend/`** mientras esté en pausa.
- **No actualizar Django por encima de la 5.2**, que es la versión fijada.
- **No subir al repositorio** el entorno virtual, `db.sqlite3`, `static/`, `media/` ni ningún `__pycache__`.
- **No hacer push directo a `main`** ni usar `--force` en ramas compartidas.
