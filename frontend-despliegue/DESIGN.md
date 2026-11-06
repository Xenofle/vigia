# DESIGN.md — Guía de estilo de mi frontend

## Guía elegida
- Nombre: Material Design 3 (esquema base claro, color semilla #6750A4)
- Enlace oficial: https://m3.material.io
- Por qué la he elegido: es la guía más documentada, publica todos sus tokens (color, tipografía, forma) con nombre propio y tiene herramienta oficial para generar y verificar paletas (Material Theme Builder). Además existe implementación web oficial (Material Web), así que los valores se pueden pasar directamente a variables CSS.

## Colores (design tokens)
| Token | Valor | Uso |
|---|---|---|
| color-primary | #6750A4 | Botones principales, enlaces, cabecera |
| color-on-primary | #FFFFFF | Texto sobre color primario |
| color-primary-container | #EADDFF | Fondo de la tarjeta de resultado |
| color-on-primary-container | #21005D | Texto sobre primary-container |
| color-surface | #FEF7FF | Fondo de la página |
| color-on-surface | #1D1B20 | Texto principal |
| color-on-surface-variant | #49454F | Texto secundario, etiquetas, texto de ayuda |
| color-outline | #79747E | Borde de los campos de texto (solo bordes, no texto) |
| color-error | #B3261E | Mensajes de error, borde de campo con error |
| color-error-container | #F9DEDC | Fondo del aviso de error |
| color-on-error-container | #410E0B | Texto sobre error-container |

Fuente: tokens `md.sys.color.*` del esquema base claro (Material Web). Verificar en Material Theme Builder con la semilla #6750A4.

### Contraste comprobado (WCAG)
| Pareja | Ratio | Resultado |
|---|---|---|
| on-primary / primary | 6,44:1 | AA ✔ |
| on-surface / surface | 16,23:1 | AAA ✔ |
| on-surface-variant / surface | 8,88:1 | AAA ✔ |
| primary / surface (enlaces) | 6,12:1 | AA ✔ |
| error / surface | 6,21:1 | AA ✔ |
| on-primary-container / primary-container | 13,32:1 | AAA ✔ |
| on-error-container / error-container | 12,77:1 | AAA ✔ |
| outline / surface | 4,33:1 | Válido para bordes (≥ 3:1), **no** para texto |

## Tipografía
- Familia: Roboto (alternativa: system-ui, sans-serif)
- Tamaño de título: 28 px / 36 px de interlineado (Headline Medium); títulos de sección 22 px / 28 px (Title Large)
- Tamaño de texto normal: 16 px / 24 px (Body Large)
- Texto de botones y etiquetas: 14 px / 20 px (Label Large)
- Pesos utilizados: 400 (regular) para títulos y cuerpo, 500 (medium) para botones y navegación

## Espaciado y forma
- Unidad base de espaciado: 4 px (todo múltiplo de 4; lo habitual, 8 px)
- Espaciados: s = 8 px, m = 16 px, l = 24 px (xl = 32 px para separar secciones)
- Radio de los bordes:
  - Botones: completo (pill, 20 px para 40 px de alto)
  - Campos de texto: 4 px (extra-small), solo esquinas superiores en el campo relleno
  - Tarjetas y avisos: 12 px (medium)

## Componentes
- Botón principal: botón relleno (filled), 40 px de alto, padding horizontal 24 px, forma pill, fondo primary y texto on-primary, texto **sin mayúsculas** (sentence case). Hover/foco/pulsado: capa de estado del color on-primary al 8 % / 10 % / 10 %. Deshabilitado: fondo on-surface al 12 % y texto on-surface al 38 %.
- Campo de texto: campo con borde (outlined), 56 px de alto, borde outline de 1 px que pasa a primary de 2 px al enfocar, etiqueta flotante (dentro del campo y sube al borde al escribir o enfocar). Texto de ayuda debajo en 12 px, color on-surface-variant.
- Zona de resultado o mensaje: tarjeta rellena (filled card) con fondo primary-container, texto on-primary-container, radio 12 px, padding 16 px.
- Mensaje de error: aviso con fondo error-container, texto on-error-container, icono de error a la izquierda, radio 12 px, situado en la propia zona de resultado (debajo del botón). Se anuncia con `role="alert"`.
- Cargando: indicador de progreso circular en color primary + texto "Cargando…"; el botón queda deshabilitado mientras dura la petición.

## Accesibilidad
- Contraste mínimo del texto: 4.5:1 (WCAG AA) — todas las parejas de texto lo cumplen (ver tabla).
- Foco visible: indicador de foco de 3 px de grosor, separado 2 px del elemento (`outline: 3px solid; outline-offset: 2px`), en color secondary (#625B71). Solo con teclado (`:focus-visible`).
- Todos los campos tienen etiqueta visible (`<label>` asociada, no solo placeholder).
- La zona de resultado usa `aria-live="polite"` para que el lector de pantalla anuncie el saludo.
- Área táctil mínima de 48 × 48 px en botones y enlaces de navegación.

## Tono de los textos
- Cercano, con tuteo ("Escribe tu nombre", "Saluda").
- Mensajes cortos (una frase), en sentence case, sin signos de exclamación salvo el saludo.
- Los errores dicen qué ha pasado y qué hacer: "No se ha podido contactar con el backend. Inténtalo de nuevo."
