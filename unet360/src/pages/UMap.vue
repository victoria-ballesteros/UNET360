<template>
  <div class="viewer-wrapper">
    <div class="viewer-container" ref="viewerContainer"></div>

    <div class="top-controls">
      <UInputCard v-model:searchBar="searchInput" v-model:searchSource="searchSource"
        v-model:searchTarget="searchTarget" v-model:searchedNode="searchedNode" v-model:actualRoute="actualRoute"
        :searchResults="searchResults" :actualNode="{ 'name': currentNodeData.name }" :searchedNode="searchedNode" :key="varAux" />
    </div>

    <div class="map-2d-box">
      <UCustomMap v-if="currentNodeData && visualMapCoords" :key="customMapUrl" :mapUrl="customMapUrl"
        :iconUrl="customIconUrl" :node="visualMapCoords" />
    </div>
  </div>
  <UToast ref="toastRefMap" />
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref, watch } from 'vue';
import UCustomMap from '@/components/UCustomMap.vue';
import UInputCard from '@/components/UInputCard.vue';
import UToast from '@/components/UToast.vue';
import arrowImg from '../assets/images/arrow-up.png';
import arrowHighlighted from '../assets/images/arrow-up-highlighted.png';
import campusMap from '@/assets/images/campus-map.jpg';
import locationIconRaw from '@/assets/icons/location.svg?url';
import { Viewer } from '@photo-sphere-viewer/core';
import { MarkersPlugin } from '@photo-sphere-viewer/markers-plugin';
import { useNodeStore } from '@/service/stores/nodes';
import { useTagStore } from '@/service/stores/tags';
import { adjustAngle, getImagePath, searchNodeByKeyword, generateRandomStartNode } from '@/service/shared/utils';

// Stores
const nodeStore = useNodeStore();
const tagStore = useTagStore();

// Inputs para búsqueda
const searchInput = ref('');
const searchSource = ref('');
const searchTarget = ref('');
const varAux = ref(0);

const searchResults = ref(null);

// Viewer y contenedor
let viewer;
const viewerContainer = ref(null);

// Datos y estado actuales
const currentImage = ref('');
const currentNodeData = ref({});
const markersPlugin = ref(null);
const visualMapCoords = ref({ x: 0, y: 0 });
const pendingMapUpdate = ref(null);

// Constantes de posicionamiento y direcciones
const POSITION_LABELS = ['Frente', 'Derecha', 'Atrás', 'Izquierda'];

// Recursos visuales
const customMapUrl = ref(campusMap);
const customIconUrl = locationIconRaw;

// Estado adicional
const lastDirection = ref('');
const searchedNode = ref('');
const actualRoute = ref({});
const checkedRouteNodes = ref({});
const isTravelling = ref(false);
const toastRefMap = ref(null);

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
  let newCoords = { x: 0, y: 0 };
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

  let flag = false;

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
      let arrow = arrowImg;

      if (isTravelling.value && actualRoute.value != null && actualRoute.value?.route != null) {
        for (let node of actualRoute.value.route) {
          if (node == neighborName) {
            if (checkedRouteNodes.value?.[neighborName] !== true) {
              arrow = arrowHighlighted;
              flag = true;
            }
          }
        }
        // ESTO IMPLEMENTA UN VIAJE AUTOMÁTICO (NO SÉ POR QUÉ) (¿FUTURO FEATURE?) (YA SÉ POR QUÉ PERO TENGO SUEÑO)
        // actualRoute.value.route = actualRoute.value.route.filter(thisNode => {
        //   if (thisNode === node.name) {
        //     return false;
        //   }
        //   return true;
        // });
      }

      checkedRouteNodes.value[node.name] = true;

      setTimeout(() => {
        markers.addMarker({
          id: markerId,
          position: { yaw: node.arrow_angles[i], pitch: 0 },
          html: `<img src="${arrow}" class="arrow-marker-img" />`,
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

  if (!flag && isTravelling.value == true) {
    isTravelling.value = false;
    notifyTravelEnd();
  }

  // MARCADORES PARA TODOS LOS TAGS
  for (const tagName in node.tags) {
    const tagData = node.tags[tagName];
    for (const key in tagData) {
      const keyNormalizada = key.toLowerCase().replace(/\s+/g, '');
      const markerId = `arrow-${keyNormalizada.toLowerCase()}-${tagData[key]}`;
      const iconName = getIconNameForTag(tagName); // Fetch icon dynamically based on tagName

      setTimeout(() => {
        markers.addMarker({
          id: markerId,
          position: { yaw: tagData[key], pitch: 0 },
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

// FUNCIONES DE INPUTS
watch(searchInput, (newValue) => {
  if (newValue.trim() === '') {
    searchResults.value = new Map();
    return;
  }

  const result = searchNodeByKeyword(newValue);
  searchResults.value = result;
});

watch(
  searchedNode,
  (newVal, oldVal) => {
    if (newVal.trim() !== '') {
      setNode(newVal);
      defineData(newVal);
      searchResults.value = null;
      searchInput.value = '';
      varAux.value++;
    }
  }
);

watch(
  actualRoute,
  async (newVal, oldVal) => {
    setNode(newVal.route[0]);
    defineData(newVal.route[0]);
    isTravelling.value = true;
    await addMarkersFromCurrentNode();
    varAux.value++;
    notifyTravel(newVal.weight);
  },
  { deep: true }
);

// TOAST FUNCTIONS
function walkingTimeCampus(distanceMeters, speedMps = 1.39) {
  const timeSeconds = distanceMeters / speedMps;
  const minutes = Math.round(timeSeconds / 60);
  return minutes;
}

function notifyTravel(distancia) {
  const aproxTime = walkingTimeCampus(distancia);
  toastRefMap.value.showToast(`¡Tu viaje está por empezar, explora a tu alrededor y sigue las flechas!: la distancia promedio es de ${distancia.toFixed(2)} metros, y una duración promedio de ${aproxTime} minutos.`);
}

function notifyTravelEnd() {
  toastRefMap.value.showToast("¡Tu viaje ha terminado!");
}

// VUE LIFETIME FUNCTIONS

onBeforeUnmount(() => {
  window.removeEventListener('resize', setVh);
});

onMounted(async () => {
  setVh();
  window.addEventListener('resize', setVh);

  setNode(generateRandomStartNode());

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

const getIconNameForTag = (tagName) => {
  const tag = tagStore.tags.find(item => item.name === tagName);
  return tag?.icon_name || 'default-icon'; // Fallback to 'default-icon' if not found
};

</script>

<style>
@import "@/assets/styles/pages/_map.scss";
</style>
