<template>
  <div class="custom-map-box" style="position: relative;">
    <div class="map-image-wrapper" :style="mapTransformStyle">
      <img
        :src="mapUrl"
        class="map-image"
        ref="mapImgRef"
        @load="onMapImgLoad"
      />
    </div>
    <!-- Icono siempre centrado en el área visible -->
    <div v-if="iconUrl" class="location-icon-overlay" :style="iconOverlayStyle">
      <img :src="iconUrl" alt="Ubicación" style="width: 40px; height: 40px; pointer-events: none;" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

// Props
const props = defineProps({
  mapUrl: { type: String, required: true },
  iconUrl: { type: String, default: '' },
  node: {                                 
    type: Object,
    required: true,
    validator: v => typeof v.x === 'number' && typeof v.y === 'number'
  }
})

const offsetX = ref(0)
const offsetY = ref(0)
const prevCoords = ref({ x: 200, y: 250 })

// Observa cambios en las props.node y mueve el mapa solo si cambian
watch(() => props.node, (newCoords, oldCoords) => {
  if (newCoords && (newCoords.x !== oldCoords?.x || newCoords.y !== oldCoords?.y)) {
    let x = newCoords.x;
    let y = newCoords.y;
    if (x <= 100 && y <= 100) {
      x = x * mapWidth.value / 100;
      y = y * mapHeight.value / 100;
    }
    centerOn(x, y);
    prevCoords.value = { ...newCoords };
  }
});

// Centrar un punto (x, y) en el área visible
function centerOn(x, y) {
  const box = document.querySelector('.custom-map-box');
  if (!box) return;
  const visibleWidth = box.offsetWidth;
  const visibleHeight = box.offsetHeight;
  offsetX.value = Math.max(0, Math.round(x - visibleWidth / 2));
  offsetY.value = Math.max(0, Math.round(y - visibleHeight / 2));
}

// Centrar el nodo actual cuando la imagen se carga
function onMapImgLoad(e) {
  mapWidth.value = e.target.naturalWidth
  mapHeight.value = e.target.naturalHeight

  let x = props.node.x;
  let y = props.node.y;
  if (x <= 100 && y <= 100) {
    x = x * mapWidth.value / 100;
    y = y * mapHeight.value / 100;
  }
  centerOn(x, y);
  prevCoords.value = { ...props.node };
}

// Tamaño real de la imagen
const mapWidth = ref(2000)
const mapHeight = ref(2000)
const mapImgRef = ref(null)

// Animación de movimiento
const transitionMs = 800 

// Estilo para la imagen del mapa
const mapTransformStyle = computed(() => ({
  width: mapWidth.value + 'px',
  height: mapHeight.value + 'px',
  position: 'absolute',
  left: -offsetX.value + 'px',
  top: -offsetY.value + 'px',
  transform: `scale(1)`,
  transition: `left ${transitionMs}ms, top ${transitionMs}ms, transform ${transitionMs}ms`,
}))

// Estilo para el overlay del icono, centrado en el área visible
const iconOverlayStyle = computed(() => ({
  position: 'absolute',
  left: '50%',
  top: '50%',
  width: '40px',
  height: '40px',
  zIndex: 100,
  pointerEvents: 'none',
  transform: 'translate(-50%, -100%)', // La base del icono queda en el centro
  transition: `left ${transitionMs}ms, top ${transitionMs}ms, transform ${transitionMs}ms`,
}));

function move(dir) {
  const step = 100
  if (dir === 'up') offsetY.value = Math.max(offsetY.value - step, 0)
  if (dir === 'down') offsetY.value = Math.min(offsetY.value + step, mapHeight.value)
  if (dir === 'left') offsetX.value = Math.max(offsetX.value - step, 0)
  if (dir === 'right') offsetX.value = Math.min(offsetX.value + step, mapWidth.value)
}
</script>

<style scoped>
.custom-map-box {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
  border-radius: 0.5rem;
  background: rgba(40,40,40,0.8);
}
.map-image-wrapper {
  position: absolute;
  width: 100%;
  height: 100%;
  overflow: hidden;
}
.map-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  pointer-events: none;
  user-select: none;
}
.location-icon {
  position: absolute;
  transition: left 400ms, top 400ms;
  will-change: left, top;
}
.location-icon-overlay {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}
</style>
