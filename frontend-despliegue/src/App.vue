<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header class="app-header">
    <nav aria-label="Principal">
      <RouterLink to="/">Inicio</RouterLink>
      <RouterLink to="/hello">Hello</RouterLink>
    </nav>
  </header>

  <main class="app-main">
    <RouterView />
  </main>
</template>

<style scoped>
.app-header {
  padding: 0 var(--space-l);
  background: var(--color-primary);
}

nav {
  display: flex;
  gap: var(--space-s);
}

/* Enlaces de navegación: Label Large, peso medium y área táctil de 48px */
nav a {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: var(--touch-target);
  min-width: var(--touch-target);
  padding: 0 var(--space-s);
  color: var(--color-on-primary);
  font-size: var(--font-size-label);
  line-height: var(--line-height-label);
  font-weight: var(--font-weight-medium);
  text-decoration: none;
}

nav a:hover {
  text-decoration: underline;
}

nav a.router-link-exact-active {
  text-decoration: underline;
  text-underline-offset: 4px;
}

/* El secondary apenas contrasta con el primary (≈1,1:1): sobre la cabecera, foco en on-primary */
nav a:focus-visible {
  outline-color: var(--color-on-primary);
  outline-offset: calc(var(--focus-offset) * -1 - var(--focus-width));
}

.app-main {
  padding: var(--space-l);
}
</style>
