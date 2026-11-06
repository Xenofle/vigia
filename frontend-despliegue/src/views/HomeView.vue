<template>
<section class="home">
<h1>Bienvenido</h1>
<p>Esta aplicación consume el endpoint <code>/api/hello</code> de nuestro backend
Laravel.</p>
<RouterLink to="/hello" class="home__link">Ir al saludo</RouterLink>
</section>
</template>
<style scoped>
.home__link {
display: inline-block;
margin-top: var(--space-m);
padding: var(--space-s) var(--space-l);
border-radius: var(--radius-m);
background: var(--color-primary);
color: var(--color-on-primary);
text-decoration: none;
}
</style>