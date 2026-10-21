// @ts-check
import { defineConfig } from 'astro/config';

import tailwindcss from '@tailwindcss/vite';
import react from '@astrojs/react';

// https://astro.build/config
export default defineConfig({
  // La home es la página de la escuela: las viejas rutas de esa sección
  // redirigen a su ancla para no romper links compartidos.
  redirects: {
    '/institucion': '/#institucion',
    '/carrera': '/#carrera',
    '/inscripcion': '/#inscripcion',
    // Astrónomos por un día: todo el proyecto vive en una sola página.
    '/proceso': '/proyecto#proceso',
    '/cronologia': '/proyecto#cronologia',
    '/impacto': '/proyecto#impacto',
    '/testimonios': '/proyecto#testimonios',
    '/competencias': '/proyecto#competencias',
  },

  vite: {
    plugins: [tailwindcss()]
  },

  integrations: [react()]
});
