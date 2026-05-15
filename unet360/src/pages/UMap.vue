<template>
  <div class="viewer-wrapper">
    <div class="viewer-container" ref="viewerContainer" style="width: 100vw; height: 100vh; background: grey"></div>

    <div class="top-controls">
      <UInputCard v-model:searchBar="searchInput" v-model:searchSource="searchSource"
        v-model:searchTarget="searchTarget" v-model:searchedNode="searchedNode" v-model:actualRoute="actualRoute"
        :searchResults="searchResults" :actualNode="{ name: currentNodeData.name }" :searchedNode="searchedNode"
        :key="varAux" />
    </div>

    <div v-if="isEditMode" class="tools-carousel">

      <div class="tool-btn" :class="{ active: selectedTool === 'arrow' }" @click="selectTool('arrow')">
        <!-- Arrow / Flecha -->
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <path d="M8 2L8 11M8 2L5 5M8 2L11 5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
          <circle cx="8" cy="13.5" r="1.5" fill="currentColor"/>
        </svg>
        Flecha
      </div>

      <div class="tool-btn" :class="{ active: selectedTool === 'tag' }" @click="selectTool('tag')">
        <!-- Tag / Etiqueta -->
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <path d="M2 2.5C2 2.22 2.22 2 2.5 2H7.38C7.64 2 7.89 2.1 8.08 2.29L13.71 7.92C14.1 8.31 14.1 8.94 13.71 9.33L9.33 13.71C8.94 14.1 8.31 14.1 7.92 13.71L2.29 8.08C2.1 7.89 2 7.64 2 7.38V2.5Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
          <circle cx="5" cy="5" r="1" fill="currentColor"/>
        </svg>
        Etiqueta
      </div>

      <div class="tool-btn" :class="{ active: selectedTool === 'forward' }" @click="selectTool('forward')">
        <!-- Eye / Fijar Frente -->
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <path d="M1.5 8C1.5 8 3.5 3.5 8 3.5C12.5 3.5 14.5 8 14.5 8C14.5 8 12.5 12.5 8 12.5C3.5 12.5 1.5 8 1.5 8Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
          <circle cx="8" cy="8" r="2" stroke="currentColor" stroke-width="1.5"/>
          <path d="M8 6V4.5M8 11.5V10M10.6 9.6L11.7 10.7M4.3 5.3L5.4 6.4M11.5 8H13M3 8H4.5" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
        </svg>
        Fijar Frente
      </div>

    </div>

    <div class="map-2d-box">
      <UCustomMap v-if="currentNodeData && visualMapCoords" :key="customMapUrl" :mapUrl="customMapUrl"
        :iconUrl="customIconUrl" :node="visualMapCoords" />
    </div>
  </div>
  
  <UToast ref="toastRefMap" />

  <UDialog v-model="showActionModal" headerTitle="Opciones del Marcador">
    <div class="action-modal-content">
      <p>¿Qué deseas hacer con este elemento?</p>
      <div class="action-buttons">
        <button class="btn-delete-element" @click="deleteSelectedElement">
          🗑️ Eliminar
        </button>
        <button class="btn-edit-element" @click="openEditForSelectedElement">
          ✏️ Editar
        </button>
      </div>
    </div>
  </UDialog>

  <UDialog v-model="showEditModal" :headerTitle="modalTitle">
    <div class="edit-form-content">
      <template v-if="editForm.type === 'arrow'">
        <div class="form-group">
          <label>Dirección Relativa:</label>
          <select v-model="editForm.direction" class="edit-input">
            <option value="0">Frente</option>
            <option value="1">Derecha</option>
            <option value="2">Atrás</option>
            <option value="3">Izquierda</option>
          </select>
        </div>
        <div class="form-group">
          <label>Nodo Destino (Nombre/ID):</label>
          <input type="text" v-model="editForm.targetNode" class="edit-input" placeholder="Ej: 002" />
        </div>
      </template>

      <template v-if="editForm.type === 'tag'">
        <div class="form-group">
          <label>Categoría del Tag:</label>
          <input type="text" v-model="editForm.tagName" class="edit-input" placeholder="Ej: Laboratorios" />
        </div>
        <div class="form-group">
          <label>Nombre del Marcador:</label>
          <input type="text" v-model="editForm.tagValue" class="edit-input" placeholder="Ej: Lab de Física" />
        </div>
      </template>

      <template v-if="editForm.type === 'forward'">
        <p class="edit-warning">¿Deseas establecer la vista actual (Yaw: {{ editForm.yaw.toFixed(2) }}) como la perspectiva frontal predeterminada de este nodo?</p>
      </template>

      <div class="edit-actions">
        <button class="btn-cancel" @click="showEditModal = false">Cancelar</button>
        <button class="btn-save" @click="saveEditedElement">Aplicar</button>
      </div>
    </div>
  </UDialog>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref, watch, computed } from "vue";
import { useRoute } from "vue-router";
import UCustomMap from "@/components/UCustomMap.vue";
import UInputCard from "@/components/UInputCard.vue";
import UToast from "@/components/UToast.vue";
import UDialog from "@/components/UDialog.vue"; 
import arrowImg from "../assets/images/arrow-up.png";
import arrowHighlighted from "../assets/images/arrow-up-highlighted.png";
import campusMap from "@/assets/images/campus-map.jpg";
import locationIconRaw from "@/assets/icons/location.svg?url";
import { Viewer } from "@photo-sphere-viewer/core";
import { MarkersPlugin } from "@photo-sphere-viewer/markers-plugin";
import { EquirectangularTilesAdapter } from "@photo-sphere-viewer/equirectangular-tiles-adapter";
import { useNodeStore } from "@/service/stores/nodes";
import { useTagStore } from "@/service/stores/tags";
import { useAuthStore } from "@/service/stores/auth"; 
import {
  adjustAngle,
  getImagePath,
  searchNodeByKeyword,
} from "@/service/shared/utils";
import "@photo-sphere-viewer/core/index.css";
import "@photo-sphere-viewer/markers-plugin/index.css";

// Stores
const route = useRoute();
const nodeStore = useNodeStore();
const tagStore = useTagStore();
const authStore = useAuthStore();

// --- SISTEMA DE EDICIÓN AVANZADA ---
const isAdmin = computed(() => true); // TODO: Lógica real de authStore
const isEditMode = ref(false);
const selectedTool = ref(null);
const originalNodeDataBackup = ref(null); // Respaldo para "Cancelar"

// Modales
const showActionModal = ref(false);
const showEditModal = ref(false);

const selectedMarkerData = ref(null); // Datos del marcador cliqueado

const editForm = ref({
  isEditing: false, 
  originalData: null,
  type: '',
  yaw: 0,
  pitch: 0,
  direction: '0',
  targetNode: '',
  tagName: '',
  tagValue: ''
});

const modalTitle = computed(() => {
  if (editForm.value.isEditing) return 'Editando Elemento';
  if (editForm.value.type === 'arrow') return 'Configurar Adyacencia';
  if (editForm.value.type === 'tag') return 'Agregar Nuevo Tag';
  if (editForm.value.type === 'forward') return 'Definir Perspectiva Frontal';
  return 'Edición de Nodo';
});

// Activar o desactivar modo edición desde un evento externo (Ej: Sidebar)
const toggleEditMode = () => {
  if (!isEditMode.value) {
    // Entrar a edición: Hacemos backup
    originalNodeDataBackup.value = JSON.parse(JSON.stringify(currentNodeData.value));
    isEditMode.value = true;
    toastRefMap.value.showToast("Modo edición activado. Selecciona herramientas o haz clic en marcadores existentes.");
  } else {
    // Guardar cambios en BD
    console.log("Guardando cambios definitivos en BD:", currentNodeData.value);
    // TODO: Llamada al backend para guardar currentNodeData.value
    
    isEditMode.value = false;
    selectedTool.value = null;
    originalNodeDataBackup.value = null;
    toastRefMap.value.showToast("¡Cambios guardados en la base de datos!");
  }
  
  // Avisamos al Sidebar el estado actual de la edición
  window.dispatchEvent(new CustomEvent('map-edit-mode-changed', { detail: isEditMode.value }));
};

// Evento global para cancelar todo sin guardar
const handleCancelEdit = () => {
  if (isEditMode.value && originalNodeDataBackup.value) {
    currentNodeData.value = JSON.parse(JSON.stringify(originalNodeDataBackup.value));
    isEditMode.value = false;
    selectedTool.value = null;
    originalNodeDataBackup.value = null;
    addMarkersFromCurrentNode();
    toastRefMap.value.showToast("Cambios cancelados y restaurados.");
    
    // Avisamos al Sidebar que se canceló la edición
    window.dispatchEvent(new CustomEvent('map-edit-mode-changed', { detail: false }));
  }
};

const selectTool = (tool) => {
  selectedTool.value = tool;
  if (tool === 'forward') {
    editForm.value.isEditing = false;
    editForm.value.type = 'forward';
    editForm.value.yaw = viewer.getPosition().yaw;
    editForm.value.pitch = viewer.getPosition().pitch;
    showEditModal.value = true;
  } else {
    toastRefMap.value.showToast(`Herramienta seleccionada. Haz clic en el visor para posicionar.`);
  }
};

// Abre formulario para editar un elemento ya existente
const openEditForSelectedElement = () => {
  showActionModal.value = false;
  const data = selectedMarkerData.value;
  
  editForm.value.isEditing = true;
  editForm.value.originalData = data;
  editForm.value.type = data.type;
  editForm.value.yaw = data.yaw || 0;
  
  if (data.type === 'arrow') {
    editForm.value.direction = data.index.toString();
    editForm.value.targetNode = data.target;
  } else if (data.type === 'tag') {
    editForm.value.tagName = data.category;
    editForm.value.tagValue = data.label;
  }
  
  showEditModal.value = true;
};

// Ejecuta eliminación en el JSON local del nodo
const deleteSelectedElement = async () => {
  const data = selectedMarkerData.value;
  
  if (data.type === 'arrow') {
    currentNodeData.value.adjacent_nodes[data.index] = {};
    currentNodeData.value.arrow_angles[data.index] = null;
  } else if (data.type === 'tag') {
    delete currentNodeData.value.tags[data.category][data.label];
    if (Object.keys(currentNodeData.value.tags[data.category]).length === 0) {
      delete currentNodeData.value.tags[data.category];
    }
  }

  showActionModal.value = false;
  selectedMarkerData.value = null;
  toastRefMap.value.showToast("Elemento eliminado localmente.");
  await addMarkersFromCurrentNode();
};

// Aplica guardado/creación en el JSON local del nodo
const saveEditedElement = async () => {
  if (editForm.value.isEditing && editForm.value.originalData) {
    const origData = editForm.value.originalData;
    if (origData.type === 'arrow') {
      currentNodeData.value.adjacent_nodes[origData.index] = {};
      currentNodeData.value.arrow_angles[origData.index] = null;
    } else if (origData.type === 'tag') {
      delete currentNodeData.value.tags[origData.category][origData.label];
    }
  }

  if (editForm.value.type === 'arrow') {
    const dirIdx = parseInt(editForm.value.direction);
    currentNodeData.value.adjacent_nodes[dirIdx] = { [editForm.value.targetNode]: editForm.value.targetNode };
    currentNodeData.value.arrow_angles[dirIdx] = editForm.value.yaw;
  } 
  else if (editForm.value.type === 'tag') {
    if (!currentNodeData.value.tags) currentNodeData.value.tags = {};
    if (!currentNodeData.value.tags[editForm.value.tagName]) currentNodeData.value.tags[editForm.value.tagName] = {};
    currentNodeData.value.tags[editForm.value.tagName][editForm.value.tagValue] = editForm.value.yaw;
  }
  else if (editForm.value.type === 'forward') {
    currentNodeData.value.forward_heading = editForm.value.yaw;
  }

  showEditModal.value = false;
  selectedTool.value = null;
  await addMarkersFromCurrentNode(); 
  toastRefMap.value.showToast("Elemento aplicado al nodo (Guarda para confirmar).");
};
// --- FIN SISTEMA DE EDICIÓN ---


// Inputs para búsqueda
const searchInput = ref("");
const searchSource = ref("");
const searchTarget = ref("");
const varAux = ref(0);
const searchResults = ref(null);

// Viewer y contenedor
let viewer;
const viewerContainer = ref(null);

// Datos actuales
const currentImage = ref("");
const currentNodeData = ref({});
const markersPlugin = ref(null);
const visualMapCoords = ref({ x: 0, y: 0 });
const pendingMapUpdate = ref(null);

const POSITION_LABELS = ["Frente", "Derecha", "Atrás", "Izquierda"];
const customMapUrl = ref(campusMap);
const customIconUrl = locationIconRaw;
const lastDirection = ref("");
const searchedNode = ref("");
const actualRoute = ref({});
const checkedRouteNodes = ref({});
const isTravelling = ref(false);
const toastRefMap = ref(null);

const setVh = () => {
  const vh = window.innerHeight * 0.01;
  document.documentElement.style.setProperty("--vh", `${vh}px`);
};

const setNode = (nodeName) => {
  const nodes = nodeStore.nodes;
  const node = nodes.find((n) => n.name === nodeName);
  if (!node) return;
  currentNodeData.value = node;
};

const defineData = async () => {
  let newMapUrl = campusMap;
  let newCoords = { x: 0, y: 0 };
  if (currentNodeData.value.minimap) {
    newMapUrl = new URL(`../assets/images/${currentNodeData.value.minimap.image}`, import.meta.url).href;
    newCoords = { x: currentNodeData.value.minimap.x, y: currentNodeData.value.minimap.y };
  }

  if (viewer && currentNodeData.value.name) {
    const tilesConfig = getTilesConfig(currentNodeData.value.name);
    const markers = viewer.getPlugin(MarkersPlugin);
    markers.clearMarkers();

    let initialYaw = adjustAngle(currentNodeData.value.forward_heading ?? 0, lastDirection.value);

    if (isTravelling.value && actualRoute.value?.route) {
      const nextIndex = currentNodeData.value.adjacent_nodes.findIndex((adyNode) => {
        if (!adyNode || Object.keys(adyNode).length === 0) return false;
        const neighborName = Object.keys(adyNode)[0];
        return actualRoute.value.route.includes(neighborName) && !checkedRouteNodes.value[neighborName];
      });

      if (nextIndex !== -1) initialYaw = currentNodeData.value.arrow_angles[nextIndex];
    }

    await viewer.setPanorama(tilesConfig, { position: { yaw: initialYaw, pitch: 0 }, transition: { rotation: false, effect: "fade" } });
    await addMarkersFromCurrentNode();
  }

  currentImage.value = currentNodeData.value.url_image;
  pendingMapUpdate.value = { url: newMapUrl, coords: newCoords };
  if (pendingMapUpdate.value) {
    if (customMapUrl.value !== pendingMapUpdate.value.url) customMapUrl.value = pendingMapUpdate.value.url;
    visualMapCoords.value = pendingMapUpdate.value.coords;
    pendingMapUpdate.value = null;
  }
};

const addMarkersFromCurrentNode = async () => {
  const node = currentNodeData.value;
  const nodes = nodeStore.nodes;
  const markers = viewer.getPlugin(MarkersPlugin);

  markers.clearMarkers();
  await new Promise((resolve) => setTimeout(resolve, 50));

  let flag = false;

  const addMarker = (markerConfig) => {
    return new Promise((resolve) => {
      viewer.addEventListener("render", () => {
        markers.addMarker(markerConfig);
        resolve();
      }, { once: true });
      viewer.needsUpdate();
    });
  };

  checkedRouteNodes.value[node.name] = true;

  // Adyacentes (Flechas)
  for (const [i, adyNode] of (node.adjacent_nodes || []).entries()) {
    if (adyNode && Object.keys(adyNode).length > 0) {
      const neighborName = Object.keys(adyNode)[0];
      const neighbor = nodes.find((n) => n.name === neighborName);
      if (!neighbor) continue;

      let arrow = arrowImg;
      if (isTravelling.value && actualRoute.value?.route != null) {
        for (let routeNode of actualRoute.value.route) {
          if (routeNode == neighborName && checkedRouteNodes.value?.[neighborName] !== true) {
            arrow = arrowHighlighted;
            flag = true;
          }
        }
      }

      await addMarker({
        id: `nav-${i}-${neighbor.name}`,
        position: { yaw: node.arrow_angles[i], pitch: -0.20 },
        html: `<img src="${arrow}" class="arrow-marker-img" />`,
        width: 32, height: 32,
        tooltip: { content: POSITION_LABELS[i], position: "right center" },
        anchor: "bottom center",
        data: JSON.stringify({ type: 'arrow', index: i, target: neighbor.name, url: neighbor.url_image, yaw: node.arrow_angles[i] }),
      });
    }
  }

  if (!flag && isTravelling.value === true) {
    isTravelling.value = false;
    notifyTravelEnd();
  }

  // Tags
  for (const tagName in node.tags) {
    const tagData = node.tags[tagName];
    for (const key in tagData) {
      const iconName = getIconNameForTag(tagName);
      await addMarker({
        id: `tag-${tagName.replace(/\s+/g, '')}-${key.replace(/\s+/g, '')}`,
        position: { yaw: tagData[key], pitch: 0 },
        html: `<img src="${getImagePath(iconName)}" class="arrow-marker-img" />`,
        width: 32, height: 32,
        tooltip: { content: key, position: "right center" },
        anchor: "bottom center",
        data: JSON.stringify({ type: 'tag', category: tagName, label: key, yaw: tagData[key] }),
      });
    }
  }

  viewer.needsUpdate();
};

watch(searchInput, (newValue) => {
  if (newValue.trim() === "") return searchResults.value = new Map();
  searchResults.value = searchNodeByKeyword(newValue);
});

watch(searchedNode, (newVal) => {
  if (newVal.trim() !== "") {
    setNode(newVal);
    defineData(newVal);
    searchResults.value = null;
    searchInput.value = "";
    varAux.value++;
  }
});

watch(actualRoute, async (newVal) => {
  isTravelling.value = true;
  checkedRouteNodes.value = {};
  setNode(newVal.route[0]);
  await defineData();
  varAux.value++;
  notifyTravel(newVal.weight);
}, { deep: true });

function notifyTravel(distancia) {
  const timeSeconds = distancia / 1.39;
  toastRefMap.value.showToast(`Distancia promedio: ${distancia.toFixed(2)}m. Tiempo aprox: ${Math.round(timeSeconds / 60)} min.`);
}

function notifyTravelEnd() {
  toastRefMap.value.showToast("¡Tu viaje ha terminado!");
}

const getTilesConfig = (nodeName) => {
  const basePath = `${import.meta.env.VITE_API_BASE_URL}/tiles/${nodeName}`;
  return {
    width: 8192, cols: 8, rows: 4,
    baseUrl: `${basePath}/pano.jpg`,
    tileUrl: (col, row) => `${basePath}/L2_${col}_${row}.jpg`,
  };
};

onBeforeUnmount(() => {
  window.removeEventListener("resize", setVh);
  window.removeEventListener('trigger-cancel-edit', handleCancelEdit);
  window.removeEventListener('trigger-toggle-edit', toggleEditMode);
});

onMounted(async () => {
  setVh();
  window.addEventListener("resize", setVh);
  
  // Escuchar eventos globales del Sidebar (Guardar/Editar y Cancelar)
  window.addEventListener('trigger-cancel-edit', handleCancelEdit);
  window.addEventListener('trigger-toggle-edit', toggleEditMode);

  setNode(route.query.node || "001");

  viewer = new Viewer({
    container: viewerContainer.value,
    adapter: [EquirectangularTilesAdapter, {}],
    panorama: getTilesConfig(currentNodeData.value.name),
    plugins: [[MarkersPlugin, {}]],
    defaultZoomLvl: 0, moveSpeed: 1.75,
    defaultYaw: currentNodeData.value.forward_heading,
  });

  const markers = viewer.getPlugin(MarkersPlugin);
  markersPlugin.value = markers;

  // Lógica de click en marcadores existentes
  markers.addEventListener("select-marker", ({ marker }) => {
    if (isEditMode.value) {
      if (marker.config.data) {
        selectedMarkerData.value = JSON.parse(marker.config.data);
        showActionModal.value = true;
      }
      return;
    }
    
    // Navegación normal
    lastDirection.value = marker.config.tooltip?.content || "";
    try {
      const markerData = JSON.parse(marker.config.data || marker.data);
      if (markerData.target) {
        setNode(markerData.target);
        defineData();
      }
    } catch (error) { console.error("Error marcador:", error); }
  });

  viewer.addEventListener("panorama-loaded", async () => {
    let newMapUrl = campusMap;
    let newCoords = { x: 0, y: 0 };
    if (currentNodeData.value.minimap) {
      newMapUrl = new URL(`../assets/images/${currentNodeData.value.minimap.image}`, import.meta.url).href;
      newCoords = { x: currentNodeData.value.minimap.x, y: currentNodeData.value.minimap.y };
    }
    customMapUrl.value = newMapUrl;
    visualMapCoords.value = newCoords;
    await addMarkersFromCurrentNode();
  }, { once: true });

  // Inserción de nuevos elementos al hacer clic en el mapa vacío
  viewer.addEventListener("click", ({ data }) => {
    if (isEditMode.value && selectedTool.value && selectedTool.value !== 'forward') {
      editForm.value.isEditing = false;
      editForm.value.originalData = null;
      editForm.value.type = selectedTool.value;
      editForm.value.yaw = data.yaw;
      editForm.value.pitch = data.pitch;
      editForm.value.targetNode = '';
      editForm.value.tagName = '';
      editForm.value.tagValue = '';
      showEditModal.value = true;
    }
  });
});

const getIconNameForTag = (tagName) => {
  const tag = tagStore.tags.find((item) => item.name === tagName);
  return tag?.icon_name || "default-icon";
};
</script>

<style lang="scss">
@import "@/assets/styles/pages/_map.scss";
</style>