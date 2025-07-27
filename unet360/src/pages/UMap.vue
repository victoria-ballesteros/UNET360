<template>
  <div ref="viewerContainer" class="w-full h-screen"></div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { Viewer } from '@photo-sphere-viewer/core';
import '@photo-sphere-viewer/core/index.css';

const viewerContainer = ref(null);

// Reemplaza esta URL por la de tu imagen 360
const imageUrl = 'https://photo-sphere-viewer-data.netlify.app/assets/sphere.jpg';

onMounted(() => {
  new Viewer({
    container: viewerContainer.value,
    panorama: imageUrl,
    loadingImg: null, // o una imagen de carga si quieres
    defaultLong: Math.PI, // posición inicial opcional
  });
});
</script>