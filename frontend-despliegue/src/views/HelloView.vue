<script setup>
import { ref } from 'vue'
import { getHello } from '@/services/helloService'
import HelloResult from '@/components/HelloResult.vue'

// Estado de la vista
const name = ref('')
const message = ref('')
const error = ref('')
const loading = ref(false)

// Acción: se ejecuta al enviar el formulario
async function saludar() {
  loading.value = true
  error.value = ''
  message.value = ''

  try {
    message.value = await getHello(name.value)
  } catch (e) {
    error.value = 'No se ha podido contactar con el backend. Inténtalo de nuevo.'
    console.error(e)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="hello">
    <h1>Hello World</h1>

    <form class="hello__form" @submit.prevent="saludar">
      <!-- Campo con borde (outlined) y etiqueta flotante.
           El placeholder " " permite detectar con CSS si el campo tiene texto -->
      <div class="field">
        <div class="field__box">
          <input
            id="name"
            v-model="name"
            type="text"
            placeholder=" "
            autocomplete="given-name"
            aria-describedby="name-ayuda"
          />
          <label for="name">Tu nombre (opcional)</label>
        </div>
        <p id="name-ayuda" class="field__help">Por ejemplo, Ana</p>
      </div>

      <button type="submit" :disabled="loading">Saluda</button>
    </form>

    <HelloResult :message="message" :error="error" :loading="loading" />
  </section>
</template>

<style scoped>
/* Headline Medium */
h1 {
  margin: 0 0 var(--space-l);
  font-size: var(--font-size-title);
  line-height: var(--line-height-title);
  font-weight: var(--font-weight-regular);
}

.hello {
  max-width: 360px;
}

.hello__form {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--space-m);
}

/* ---------- Campo de texto (outlined) ---------- */
.field {
  width: 100%;
}

.field__box {
  position: relative;
}

.field input {
  width: 100%;
  height: var(--field-height);
  padding: 0 var(--space-m);
  border: 1px solid var(--color-outline);
  border-radius: var(--radius-xs);
  background: transparent;
  color: var(--color-on-surface);
  font-family: inherit;
  font-size: var(--font-size-body);
  line-height: var(--line-height-body);
}

.field input:hover {
  border-color: var(--color-on-surface);
}

/* El borde primary de 2px es el indicador de foco del campo (primary/surface = 6,12:1) */
.field input:focus {
  outline: none;
  border: 2px solid var(--color-primary);
  padding: 0 calc(var(--space-m) - 1px); /* compensa el borde para que el texto no salte */
}

.field label {
  position: absolute;
  top: 50%;
  left: calc(var(--space-m) - var(--space-xs));
  transform: translateY(-50%);
  padding: 0 var(--space-xs);
  background: var(--color-surface); /* corta el borde al flotar */
  color: var(--color-on-surface-variant);
  font-size: var(--font-size-body);
  line-height: var(--line-height-body);
  pointer-events: none;
  transition:
    top 150ms ease,
    font-size 150ms ease,
    line-height 150ms ease;
}

/* La etiqueta sube al borde al enfocar o cuando hay texto */
.field input:focus + label,
.field input:not(:placeholder-shown) + label {
  top: 0;
  font-size: var(--font-size-supporting);
  line-height: var(--line-height-supporting);
}

.field input:focus + label {
  color: var(--color-primary);
}

.field__help {
  margin: var(--space-xs) 0 0;
  padding: 0 var(--space-m);
  color: var(--color-on-surface-variant);
  font-size: var(--font-size-supporting);
  line-height: var(--line-height-supporting);
}

/* ---------- Botón relleno (filled) ---------- */
button {
  position: relative;
  height: var(--button-height);
  padding: 0 var(--space-l);
  border: none;
  border-radius: var(--radius-full);
  background: var(--color-primary);
  color: var(--color-on-primary);
  font-family: inherit;
  font-size: var(--font-size-label);
  line-height: var(--line-height-label);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
}

/* Área táctil de 48px sin cambiar el tamaño visual (40px) */
button::after {
  content: '';
  position: absolute;
  inset: calc((var(--button-height) - var(--touch-target)) / 2) 0;
}

/* Capas de estado de on-primary sobre primary */
button:hover {
  background: color-mix(in srgb, var(--color-on-primary) var(--state-hover), var(--color-primary));
}

button:focus-visible {
  background: color-mix(in srgb, var(--color-on-primary) var(--state-focus), var(--color-primary));
}

button:active {
  background: color-mix(in srgb, var(--color-on-primary) var(--state-pressed), var(--color-primary));
}

button:disabled {
  background: color-mix(in srgb, var(--color-on-surface) var(--state-disabled-container), transparent);
  color: color-mix(in srgb, var(--color-on-surface) var(--state-disabled-content), transparent);
  cursor: not-allowed;
}
</style>
