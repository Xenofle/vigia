<script setup>
defineProps({
  message: { type: String, default: '' },
  error: { type: String, default: '' },
  loading: { type: Boolean, default: false },
})
</script>

<template>
  <div class="result">
    <!-- Las regiones vivas existen siempre en el DOM; solo cambia su contenido,
         así el lector de pantalla anuncia cada cambio -->
    <div aria-live="polite">
      <p v-if="loading" class="result__loading">
        <span class="spinner" aria-hidden="true"></span>
        Cargando…
      </p>
      <p v-else-if="message && !error" class="result__card">{{ message }}</p>
    </div>

    <div role="alert">
      <div v-if="error && !loading" class="result__error">
        <svg class="result__icon" viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false">
          <path
            fill="currentColor"
            d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Zm1 15h-2v-2h2v2Zm0-4h-2V7h2v6Z"
          />
        </svg>
        <p>{{ error }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.result {
  margin-top: var(--space-l);
}

p {
  margin: 0;
}

/* Tarjeta rellena (filled card) */
.result__card {
  padding: var(--space-m);
  border-radius: var(--radius-m);
  background: var(--color-primary-container);
  color: var(--color-on-primary-container);
  font-size: var(--font-size-title-section);
  line-height: var(--line-height-title-section);
}

/* Aviso de error con icono a la izquierda */
.result__error {
  display: flex;
  align-items: flex-start;
  gap: var(--space-m);
  padding: var(--space-m);
  border-radius: var(--radius-m);
  background: var(--color-error-container);
  color: var(--color-on-error-container);
}

.result__icon {
  flex-shrink: 0;
}

/* Cargando: indicador circular en primary + texto */
.result__loading {
  display: flex;
  align-items: center;
  gap: var(--space-s);
  color: var(--color-on-surface-variant);
}

.spinner {
  width: 24px;
  height: 24px;
  border: 4px solid var(--color-primary-container);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: girar 1s linear infinite;
}

@keyframes girar {
  to {
    transform: rotate(360deg);
  }
}

@media (prefers-reduced-motion: reduce) {
  .spinner {
    animation-duration: 3s;
  }
}
</style>
