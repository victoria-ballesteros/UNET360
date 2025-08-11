<template>
  <div class="viewer-wrapper">
    <div class="viewer-container" ref="viewerContainer"></div>

    <div class="top-controls">
      <UInputCard v-model="searchInput" styleType="map" placeholder="Ej. Edificio A" icon="icons/arrow-up"
        :searchSource="searchSource" :searchTarget="searchTarget" />
    </div>

    <div class="map-2d-box">
      <UCustomMap v-if="currentNodeData && visualMapCoords" :key="customMapUrl" :mapUrl="customMapUrl"
        :iconUrl="customIconUrl" :node="visualMapCoords" />
    </div>
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref, watch } from 'vue';
import UCustomMap from '@/components/UCustomMap.vue';
import UInputCard from '@/components/UInputCard.vue';
import arrowImg from '../assets/images/arrow-up.png';
import campusMap from '@/assets/images/campus-map.jpg';
import locationIconRaw from '@/assets/icons/location.svg?url';
import { Viewer } from '@photo-sphere-viewer/core';
import { MarkersPlugin } from '@photo-sphere-viewer/markers-plugin';
import { useNodeStore } from '@/service/stores/nodes';
import { useTagStore } from '@/service/stores/tags';
import { fetchShortestPath } from '@/service/requests/graph';
import { adjustAngle, getImagePath } from '@/service/shared/utils';

// Stores
const nodeStore = useNodeStore();
const tagStore = useTagStore();

// Inputs para búsqueda
const searchInput = ref('');
const searchSource = ref('');
const searchTarget = ref('');

// Viewer y contenedor
let viewer;
const viewerContainer = ref(null);

// Datos y estado actuales
const currentImage = ref('');
const currentNodeData = ref({});
const markersPlugin = ref(null);
const visualMapCoords = ref({ x: 200, y: 250 });
const pendingMapUpdate = ref(null);

// Constantes de posicionamiento y direcciones
const POSITION_LABELS = ['Frente', 'Derecha', 'Atrás', 'Izquierda'];

// Recursos visuales
const customMapUrl = ref(campusMap);
const customIconUrl = locationIconRaw;

// Estado adicional
const lastDirection = ref('');

// Funciones auxiliares (que no pertenecen a UTILS)
const setVh = () => {
  const vh = window.innerHeight * 0.01;
  document.documentElement.style.setProperty('--vh', `${vh}px`);
}

// Funciones de inicialización del nodo
const setNode = (nodeName) => {
  const nodes = nodeStore.nodes;
  const node = nodes.find(n => n.name === nodeName);
  if (!node) {
    console.warn('Nodo no encontrado:', nodeName);
    return;
  }

  currentNodeData.value = node;
};

const defineData = async () => {
  let newMapUrl = campusMap;
  let newCoords = { x: 200, y: 250 };
  if (currentNodeData.value.minimap) {
    newMapUrl = new URL(`../assets/images/${currentNodeData.value.minimap.image}`, import.meta.url).href;
    newCoords = { x: currentNodeData.value.minimap.x, y: currentNodeData.value.minimap.y };
  }

  currentImage.value = currentNodeData.value.url_image;
  pendingMapUpdate.value = { url: newMapUrl, coords: newCoords };
};

// CREACIÓN DE MARCADORES DE LA IMAGEN
const addMarkersFromCurrentNode = async () => {
  const node = currentNodeData.value;
  const nodes = nodeStore.nodes;
  const markers = viewer.getPlugin(MarkersPlugin);

  markers.clearMarkers();

  await new Promise(resolve => setTimeout(resolve, 50));

  // MARCADORES PARA LOS NODOS ADYACENTES
  node.adjacent_nodes.forEach((adyNode, i) => {
    if (adyNode && Object.keys(adyNode).length > 0) {
      const neighborName = Object.keys(adyNode)[0];
      const neighbor = nodes.find(n => n.name === neighborName);

      if (!neighbor) {
        console.warn(`Vecino ${neighborName} no encontrado`);
        return;
      }

      const markerId = `arrow-${POSITION_LABELS[i].toLowerCase()}-${neighbor.name}`;

      setTimeout(() => {
        markers.addMarker({
          id: markerId,
          position: { yaw: node.arrow_angles[i], pitch: 0 },
          html: `<img src="${arrowImg}" class="arrow-marker-img" />`,
          width: 32,
          height: 32,
          tooltip: {
            content: POSITION_LABELS[i],
            position: 'right center'
          },
          anchor: 'bottom center',
          data: JSON.stringify({
            target: neighbor.name,
            url: neighbor.url_image
          })
        });
      }, 100);
    }
  });

  // MARCADORES PARA PUNTOS DE ENCUENTRO
  const ptsEncuentro = node.tags?.["Punto de encuentro"]
  for (const key in ptsEncuentro) {
    const keyNormalizada = key.toLowerCase().replace(/\s+/g, '');
    const markerId = `arrow-${keyNormalizada.toLowerCase()}-${ptsEncuentro[key]}`;
    const iconName = tagStore.tags.find(item => item.name === "Punto de encuentro")?.icon_name;

    setTimeout(() => {
      markers.addMarker({
        id: markerId,
        position: { yaw: ptsEncuentro[key], pitch: 0 },
        html: `<img src="${getImagePath(iconName)}" class="arrow-marker-img" />`,
        width: 32,
        height: 32,
        tooltip: {
          content: key,
          position: 'right center'
        },
        anchor: 'bottom center',
      });
    }, 100);
  }
};

// DISPARADOR DE CAMBIO DE NODO
watch(currentImage, async (newImage) => {
  if (viewer && newImage) {
    markersPlugin.value?.clearMarkers();

    await viewer.setPanorama(newImage, {
      position: { yaw: adjustAngle(currentNodeData.value.forward_heading, lastDirection.value), pitch: 0 },
      transition: {
        rotation: false,
        effect: 'fade',
      },
    });
  }
});

// VUE LIFETIME FUNCTIONS

onBeforeUnmount(() => {
  window.removeEventListener('resize', setVh);
});

onMounted(async () => {
  setVh();
  window.addEventListener('resize', setVh);

  setNode('021');

  viewer = new Viewer({
    container: viewerContainer.value,
    panorama: '',
    plugins: [
      [MarkersPlugin, {}]
    ],
    defaultYaw: currentNodeData.value.forward_heading,
  });

  const markers = viewer.getPlugin(MarkersPlugin);

  markers.addEventListener('select-marker', ({ marker }) => {
    lastDirection.value = marker.config.tooltip.content;
    try {
      const markerData = JSON.parse(marker.data);
      setNode(markerData.target);
      defineData(markerData.target);
    } catch (error) {
      console.error('Error al procesar marcador:', error);
    }
  });

  await defineData();

  viewer.addEventListener('panorama-loaded', async () => {
    await addMarkersFromCurrentNode();

    if (pendingMapUpdate.value) {
      if (customMapUrl.value !== pendingMapUpdate.value.url) {
        customMapUrl.value = pendingMapUpdate.value.url;
      }
      visualMapCoords.value = pendingMapUpdate.value.coords;
      pendingMapUpdate.value = null;
    }
  });

  // viewer.addEventListener('click', ({ data }) => {
  //   console.log(`${data.rightclick ? 'right ' : ''}clicked at yaw: ${data.yaw} pitch: ${data.pitch}`);
  // });

  // const response = await fetchShortestPath('002', '004');
  // console.log("Response: ", response)
});

</script>

<style>
@import "@/assets/styles/pages/_map.scss";
</style>
