<template>
  <div class="viewer-wrapper">
    <div class="viewer-container" ref="viewerContainer"></div>

    <div class="top-controls">
      <UInputCard
        v-model="searchInput"
        styleType="map"
        placeholder="Ej. Edificio A"
        icon="icons/arrow-up"
      />

      <!-- <RouterLink :to="{ name: 'Home' }" class="floating-icon">
        <UIcon name="icons/logo" size="18" />
      </RouterLink> -->
    </div>

    <div class="map-2d-box">
      <UCustomMap
        v-if="currentNodeData && visualMapCoords"
        :key="customMapUrl"
        :mapUrl="customMapUrl"
        :iconUrl="customIconUrl"
        :node="visualMapCoords"
      />
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue';
import { RouterLink } from 'vue-router';
import UIcon from '@/components/UIcon.vue';
import UCustomMap from '@/components/UCustomMap.vue';
import UInputCard from '@/components/UInputCard.vue';
import { obtainMockNodes } from '@/service/shared/utils';
import arrowImg from '../assets/images/arrow-up.png';
import campusMap from '@/assets/images/campus-map.jpg';
import locationIconRaw from '@/assets/icons/location.svg?url';
import { Viewer } from '@photo-sphere-viewer/core';
import { MarkersPlugin } from '@photo-sphere-viewer/markers-plugin';


const searchInput = ref('')

let viewer;
const viewerContainer = ref(null);

const currentImage = ref('');
const currentNodeData = ref({});
const markersPlugin = ref(null);
const visualMapCoords = ref({ x: 200, y: 250 });
const pendingMapUpdate = ref(null);

const YAW_MAP = [0, Math.PI / 2, Math.PI, -Math.PI / 2];
const POSITION_LABELS = ['Frente', 'Derecha', 'Atrás', 'Izquierda'];

const MAP_BASE_PATH = '/src/assets/images/';
const customMapUrl = ref(campusMap);
const customIconUrl = locationIconRaw;

const defineData = async (nodeName) => {
  const nodes = await obtainMockNodes();
  const node = nodes.find(n => n.name === nodeName);
  if (!node) {
    console.warn('Nodo no encontrado:', nodeName);
    return;
  }

  let newMapUrl = campusMap;
  let newCoords = { x: 200, y: 250 };
  if (node.minimap) {
    newMapUrl = MAP_BASE_PATH + node.minimap.image;
    newCoords = { x: node.minimap.x, y: node.minimap.y };
  }

  currentImage.value = node.url_image;
  currentNodeData.value = node;
  pendingMapUpdate.value = { url: newMapUrl, coords: newCoords };
};

onMounted(async () => {
  viewer = new Viewer({
    container: viewerContainer.value,
    panorama: '',
    plugins: [
      [MarkersPlugin, {}]
    ],
    defaultYaw: 0,
  });

  const markers = viewer.getPlugin(MarkersPlugin);

  markers.addEventListener('select-marker', ({ marker }) => {
    try {
      const markerData = JSON.parse(marker.data);
      defineData(markerData.target);
    } catch (error) {
      console.error('Error al procesar marcador:', error);
    }
  });

  await defineData('001');

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
});

const addMarkersFromCurrentNode = async () => {
  const node = currentNodeData.value;
  const nodes = await obtainMockNodes();
  const markers = viewer.getPlugin(MarkersPlugin);

  markers.clearMarkers();

  await new Promise(resolve => setTimeout(resolve, 50));

  node.adyacent_nodes.forEach((adyNode, i) => {
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
          position: { yaw: YAW_MAP[i], pitch: 0 },
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
};

watch(currentImage, async (newImage) => {
  if (viewer && newImage) {
    console.log('Actualizando imagen:', newImage);

    markersPlugin.value?.clearMarkers();

    await viewer.setPanorama(newImage);

    viewer.addEventListener('panorama-loaded', async () => {
      console.log('Imagen cargada, agregando marcadores...');
      await addMarkersFromCurrentNode();
    });
  }
});
</script>

<style>
@import "@/assets/styles/pages/_map.scss";
</style>
