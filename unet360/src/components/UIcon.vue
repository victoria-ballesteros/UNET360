<template>
  <component
    :is="IconComponent"
    v-if="IconComponent"
    :height="size"
    :fill="color"
    :style="{
      transform: `rotate(${props.rotation}deg)`,
    }"
  />
  <img
    v-else-if="pngUrl"
    :src="pngUrl"
    :style="{
      height: size,
      width: size,
      transform: `rotate(${props.rotation}deg)`,
      objectFit: 'contain'
    }"
    aria-hidden="true"
  />
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  name: {
    type: String,
    required: true,
  },
  size: {
    type: [Number, String],
  },
  color: {
    type: String,
    default: "currentColor",
  },
  rotation: {
    type: Number,
    default: 0,
  },
});

// Carga recursiva de SVGs en assets utilizando '**'
const icons = import.meta.glob("@/assets/**/*.svg", {
  eager: true,
  import: "default",
});

const IconComponent = computed(() => {
  if (!props.name) return null;

  // 1. Probar ruta exacta solicitada
  let path = `/src/assets/${props.name}.svg`;
  if (icons[path]) return icons[path];
  
  // 2. Probar en carpeta icons/ si se provee un nombre simple
  path = `/src/assets/icons/${props.name}.svg`;
  if (icons[path]) return icons[path];

  // 3. Probar en carpeta images/icons-images/
  path = `/src/assets/images/icons-images/${props.name}.svg`;
  if (icons[path]) return icons[path];
  
  return null;
});

// Soporte de fallback para imágenes PNG en la carpeta de iconos de tags
const pngUrl = computed(() => {
  if (IconComponent.value) return null;
  if (!props.name) return null;
  
  let filename = props.name;
  // Extraer sólo el nombre de archivo si viene con ruta
  if (filename.includes('/')) {
    filename = filename.substring(filename.lastIndexOf('/') + 1);
  }
  
  try {
    return new URL(`../assets/images/icons-images/${filename}.png`, import.meta.url).href;
  } catch (e) {
    return null;
  }
});
</script>
