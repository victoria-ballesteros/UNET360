<template>
  <div class="viewer-wrapper" :class="{ 'moving-mode-active': movingMarkerData }">
    <!-- NO TOCAR ESTA LÍNEA POR NINGUNA RAZÓN PORQUE EL VISOR DEPENDE DE ESTO -->
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

      <div class="tool-btn" :class="{ active: selectedTool === 'rotation' }" @click="selectTool('rotation')">
        <!-- Rotate / Rotación -->
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <path d="M12 8C12 10.2091 10.2091 12 8 12C5.79086 12 4 10.2091 4 8C4 5.79086 5.79086 4 8 4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
          <path d="M6.5 2L8.5 4L6.5 6" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Rotación
      </div>

    </div>

    <!-- Backdrop oscuro para enfocar el mapa cuando está expandido -->
    <div 
      v-if="isMapExpanded" 
      class="map-backdrop" 
      @click="isMapExpanded = false"
    ></div>

    <div class="map-2d-wrapper" :class="{ 'is-expanded': isMapExpanded }">
      <div 
        class="map-2d-box" 
        @click="expandMap"
      >
        <!-- Marcas de la brújula (rotadas 90°: E en el frente, S en la derecha, O en el sur, N en la izquierda) -->
        <span class="compass-mark compass-n" aria-hidden="true">E</span>
        <span class="compass-mark compass-s" aria-hidden="true">O</span>
        <span class="compass-mark compass-e" aria-hidden="true">S</span>
        <span class="compass-mark compass-w" aria-hidden="true">N</span>

        <!-- Botón de minimizar (solo visible cuando está expandido) -->
        <button 
          v-if="isMapExpanded" 
          class="minimize-map-btn" 
          @click.stop="isMapExpanded = false"
          aria-label="Minimizar mapa"
        >
          <span class="minimize-line"></span>
        </button>

        <UCustomMap v-if="currentNodeData && visualMapCoords" :key="customMapUrl" :mapUrl="customMapUrl"
          :iconUrl="customIconUrl" :node="visualMapCoords" />
      </div>
    </div>

    <!-- Chip de Nodo actual para Administradores -->
    <div v-if="isAdmin && currentNodeData && currentNodeData.name" class="admin-node-chip">
      <span class="node-name-text">{{ currentNodeData.name }}</span>
    </div>
  </div>
  
  <UToast ref="toastRefMap" />

  <UBaseModal v-model="showActionModal" title="Opciones del Marcador" size="sm">
    <div class="action-modal-content">
      <p class="modal-confirm-text">¿Qué deseas hacer con este elemento?</p>
    </div>
    <template #footer>
      <UButton text="Eliminar" type="danger"   icon="icons/trash"  @click="deleteSelectedElement" />
      <UButton text="Mover"    type="secondary" icon="icons/route-arrow" @click="startMovingElement" title="Reubicar este elemento en otra posición del visor" />
      <UButton text="Editar"   type="contrast-2" icon="icons/edit" @click="openEditForSelectedElement" />
    </template>
  </UBaseModal>

  <UBaseModal v-model="showEditModal" :title="modalTitle" size="md">
    <div class="edit-form-content">
      <template v-if="editForm.type === 'arrow'">
        <div class="form-group">
          <label>Dirección Relativa:</label>
          <USelect
            styleType="dark"
            v-model="directionLabel"
            :options="['Frente', 'Derecha', 'Atrás', 'Izquierda']"
            placeholder="Seleccionar..."
          />
        </div>
        <div class="form-group">
          <label>Nodo Destino (Nombre/ID):</label>
          <UInput styleType="dark" v-model="editForm.targetNode" placeholder="Ej: 002" />
        </div>
        <div class="form-group">
          <label>Peso de Conexión:</label>
          <UInput
            styleType="dark"
            v-model="editForm.weight"
            placeholder="Ej: 1.0"
            pattern="[0-9.]*"
          />
        </div>
      </template>

      <template v-if="editForm.type === 'tag'">
        <div class="form-group">
          <label>Categoría del Tag:</label>
          <div class="custom-select-wrapper" @click.stop="toggleTagDropdown" v-click-outside="closeTagDropdown">
            <div class="custom-select-trigger edit-input" :class="{ open: tagDropdownOpen }">
              <span class="selected-tag-display">
                <UIcon 
                  v-if="selectedTagIcon" 
                  :name="selectedTagIcon" 
                  class="select-tag-icon" 
                  size="1.1rem" 
                />
                <span>{{ editForm.tagName || 'Seleccionar categoría...' }}</span>
              </span>
              <svg class="select-chevron" :class="{ rotated: tagDropdownOpen }" width="14" height="14" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                <path d="M2.5 5L7 9.5L11.5 5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <transition name="dropdown-fade">
              <ul v-show="tagDropdownOpen" class="custom-select-options max-height-options">
                <li
                  v-for="tag in tagStore.tags"
                  :key="tag.name"
                  class="custom-select-option tag-option-item"
                  :class="{ selected: editForm.tagName === tag.name }"
                  @click.stop="selectTagName(tag.name)"
                >
                  <UIcon :name="tag.icon_name || 'icons/location'" class="tag-option-icon" size="1.1rem" />
                  <span>{{ tag.name }}</span>
                </li>
              </ul>
            </transition>
          </div>
        </div>
        <div class="form-group">
          <label>Nombre del Marcador:</label>
          <UInput
            styleType="dark"
            v-model="editForm.tagValue"
            placeholder="Ej: Lab de Física"
          />
        </div>
      </template>

      <template v-if="editForm.type === 'forward'">
        <p class="edit-warning">¿Deseas establecer la vista actual (Yaw: {{ editForm.yaw.toFixed(2) }}) como la perspectiva frontal predeterminada de este nodo?</p>
      </template>
      <template v-if="editForm.type === 'rotation'">
        <p class="edit-warning">Establece la rotación a aplicar al llegar a este nodo ({{ currentNodeData.name }}) desde sus vecinos:</p>
        
        <div v-for="neighborName in adjacentNeighborNames" :key="neighborName" class="form-group neighbor-rotation-group">
          <label>Al venir desde el Nodo <strong>{{ neighborName }}</strong>:</label>
          <div class="custom-select-wrapper" @click.stop="toggleNeighborRotationDropdown(neighborName)" v-click-outside="() => closeNeighborRotationDropdown(neighborName)">
            <div class="custom-select-trigger edit-input" :class="{ open: neighborRotationDropdownOpen[neighborName] }">
              <span>{{ rotationOptions.find(o => o.value === editForm.rotation_corrections[neighborName])?.label || '0°' }}</span>
              <svg class="select-chevron" :class="{ rotated: neighborRotationDropdownOpen[neighborName] }" width="14" height="14" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                <path d="M2.5 5L7 9.5L11.5 5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <transition name="dropdown-fade">
              <ul v-show="neighborRotationDropdownOpen[neighborName]" class="custom-select-options">
                <li
                  v-for="opt in rotationOptions"
                  :key="opt.value"
                  class="custom-select-option"
                  :class="{ selected: editForm.rotation_corrections[neighborName] === opt.value }"
                  @click.stop="selectNeighborRotation(neighborName, opt.value)"
                >
                  {{ opt.label }}
                </li>
              </ul>
            </transition>
          </div>
        </div>

        <div v-if="adjacentNeighborNames.length === 0" class="edit-warning">
          Este nodo no tiene conexiones adyacentes configuradas para asociar rotación.
        </div>
      </template>

      <div class="edit-actions">
        <UButton text="Cancelar" type="tertiary"    @click="showEditModal = false" />
        <UButton text="Aplicar"  type="contrast-2" @click="saveEditedElement" />
      </div>
    </div>
  </UBaseModal>
</template>

<script setup>
import api from '@/axios';
import { onBeforeUnmount, onMounted, ref, watch, computed, reactive } from "vue";
import { useRoute } from "vue-router";
import UCustomMap from "@/components/UCustomMap.vue";
import UInputCard from "@/components/UInputCard.vue";
import UToast from "@/components/UToast.vue";
import UBaseModal from "@/components/UBaseModal.vue";
import UButton from '@/components/UButton.vue';
import UIcon from '@/components/UIcon.vue';
import UInput from '@/components/UInput.vue';
import USelect from '@/components/USelect.vue';

// Directiva personalizada para cerrar el dropdown al hacer click fuera
const vClickOutside = {
  mounted(el, binding) {
    el._clickOutsideHandler = (event) => {
      if (!el.contains(event.target)) binding.value();
    };
    document.addEventListener('click', el._clickOutsideHandler);
  },
  unmounted(el) {
    document.removeEventListener('click', el._clickOutsideHandler);
  },
};

// Custom select: Dirección Relativa
const directionOptions = [
  { value: '0', label: 'Frente' },
  { value: '1', label: 'Derecha' },
  { value: '2', label: 'Atrás' },
  { value: '3', label: 'Izquierda' },
];
const selectDirection = (val) => {
  editForm.value.direction = val;

  // Autocomplete info if there's already a connection in that direction
  const dirIdx = parseInt(val, 10);
  const existingAdj = currentNodeData.value.adjacent_nodes?.[dirIdx];
  if (existingAdj && typeof existingAdj === 'object' && Object.keys(existingAdj).length > 0) {
    const target = Object.keys(existingAdj)[0];
    const weight = existingAdj[target];
    editForm.value.targetNode = target;
    editForm.value.weight = weight !== undefined && weight !== null ? weight.toString() : '1.0';
  } else {
    editForm.value.targetNode = '';
    editForm.value.weight = '1.0';
  }
};

const directionLabel = computed({
  get() {
    const opt = directionOptions.find(o => o.value === editForm.value.direction);
    return opt ? opt.label : '';
  },
  set(newValue) {
    const opt = directionOptions.find(o => o.label === newValue);
    if (opt) {
      selectDirection(opt.value);
    }
  }
});


// Custom select: Categoría del Tag
const tagDropdownOpen = ref(false);
const toggleTagDropdown = () => { tagDropdownOpen.value = !tagDropdownOpen.value; };
const closeTagDropdown = () => { tagDropdownOpen.value = false; };
const selectTagName = (name) => {
  editForm.value.tagName = name;
  tagDropdownOpen.value = false;
};
const selectedTagIcon = computed(() => {
  if (!editForm.value.tagName) return null;
  const tag = tagStore.tags?.find(t => t.name === editForm.value.tagName);
  return tag?.icon_name || 'icons/location';
});

// Custom select: Corrección de Rotación por vecino
const rotationOptions = [
  { value: '0', label: '0°' },
  { value: '90', label: '90°' },
  { value: '180', label: '180°' },
  { value: '270', label: '270°' },
];
const neighborRotationDropdownOpen = reactive({});
const toggleNeighborRotationDropdown = (name) => {
  neighborRotationDropdownOpen[name] = !neighborRotationDropdownOpen[name];
};
const closeNeighborRotationDropdown = (name) => {
  neighborRotationDropdownOpen[name] = false;
};
const selectNeighborRotation = (name, val) => {
  editForm.value.rotation_corrections[name] = val;
  neighborRotationDropdownOpen[name] = false;
};

const adjacentNeighborNames = computed(() => {
  const names = [];
  if (currentNodeData.value?.adjacent_nodes) {
    currentNodeData.value.adjacent_nodes.forEach((adj) => {
      if (adj && Object.keys(adj).length > 0) {
        const neighborName = Object.keys(adj)[0];
        names.push(neighborName);
      }
    });
  }
  return names;
});
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
  generateRandomStartNode,
} from "@/service/shared/utils";
import "@photo-sphere-viewer/core/index.css";
import "@photo-sphere-viewer/markers-plugin/index.css";

// Stores
const route = useRoute();
const nodeStore = useNodeStore();
const tagStore = useTagStore();
const authStore = useAuthStore();

// --- SISTEMA DE EDICIÓN AVANZADA ---
const isAdmin = computed(() => {
  return authStore.user?.role === 'admin' || authStore.user?.role === 'ADMIN'; 
}); // TODO: Lógica real de authStore
const isEditMode = ref(false);
const isMapExpanded = ref(false);
const isAutoRotating = ref(true); // Control de reproducción/pausa de rotación lenta
let rotationFrameId = null;
let idleTimeout = null;
let isUserInteracting = false;

const expandMap = () => {
  if (!isMapExpanded.value) {
    isMapExpanded.value = true;
  }
};
const selectedTool = ref(null);
const originalNodeDataBackup = ref(null); // Respaldo para "Cancelar"
const previousNodeData = ref(null); // Respaldo de nodo anterior para corrección de rotación

// Modales
const showActionModal = ref(false);
const showEditModal = ref(false);

const selectedMarkerData = ref(null); // Datos del marcador cliqueado
const movingMarkerData = ref(null);   // Marcador en proceso de reubicación

const editForm = ref({
  isEditing: false, 
  originalData: null,
  type: '',
  yaw: 0,
  pitch: 0,
  direction: '0',
  targetNode: '',
  weight: '1.0',
  tagName: '',
  tagValue: '',
  rotation_corrections: {}
});

const modalTitle = computed(() => {
  if (editForm.value.isEditing) return 'Editando Elemento';
  if (editForm.value.type === 'arrow') return 'Configurar Adyacencia';
  if (editForm.value.type === 'tag') return 'Agregar Nuevo Tag';
  if (editForm.value.type === 'forward') return 'Definir Perspectiva Frontal';
  if (editForm.value.type === 'rotation') return 'Corregir Rotación del Nodo';
  return 'Edición de Nodo';
});


// Activar o desactivar modo edición desde un evento externo (Ej: Sidebar)
const toggleEditMode = async () => {
  if (!isEditMode.value) {
    // Entrar a edición: Hacemos backup
    originalNodeDataBackup.value = JSON.parse(JSON.stringify(currentNodeData.value));
    isEditMode.value = true;
    toastRefMap.value.showToast("Modo edición activado.");
  } else {
    // Guardar cambios en BD
    try {
      toastRefMap.value.showToast("Guardando cambios en la base de datos...");
      
      // Construimos el payload siguiendo el modelo de UNodeEdit.vue
      const payload = {
        location: currentNodeData.value.location || null,
        url_image: currentNodeData.value.url_image,
        adjacent_nodes: currentNodeData.value.adjacent_nodes,
        arrow_angles: currentNodeData.value.arrow_angles,
        forward_heading: parseFloat(currentNodeData.value.forward_heading) || 0,
        rotation_correction: currentNodeData.value.rotation_correction || null,
        tags: currentNodeData.value.tags,
      };

      // Adjuntamos el minimapa solo si tiene datos válidos
      if (currentNodeData.value.minimap && Object.keys(currentNodeData.value.minimap).length > 0) {
        payload.minimap = currentNodeData.value.minimap;
      }

      // Hacemos la petición PATCH a la API
      const { data } = await api.patch(`nodes/${encodeURIComponent(currentNodeData.value.name)}`, payload);

      if (data?.status) {
        isEditMode.value = false;
        selectedTool.value = null;
        originalNodeDataBackup.value = null;
        toastRefMap.value.showToast("¡Cambios guardados exitosamente!");
        nodeStore.fetchNodes();
      } else {
        toastRefMap.value.showToast("Ocurrió un error al guardar en la base de datos.");
        return; // Detenemos la ejecución si falla
      }
    } catch (error) {
      console.error("Error al guardar nodo:", error);
      toastRefMap.value.showToast("Error de conexión al intentar guardar.");
      return; // Detenemos la ejecución
    }
  }
  
  // Avisamos al Sidebar el estado actual de la edición (para cambiar los botones)
  window.dispatchEvent(new CustomEvent('map-edit-mode-changed', { detail: isEditMode.value }));
};

// Evento global para cancelar todo sin guardar
const handleCancelEdit = () => {
  if (isEditMode.value && originalNodeDataBackup.value) {
    currentNodeData.value = JSON.parse(JSON.stringify(originalNodeDataBackup.value));
    isEditMode.value = false;
    selectedTool.value = null;
    movingMarkerData.value = null;
    originalNodeDataBackup.value = null;
    addMarkersFromCurrentNode();
    toastRefMap.value.showToast("Cambios cancelados y restaurados.");
    
    // Avisamos al Sidebar que se canceló la edición
    window.dispatchEvent(new CustomEvent('map-edit-mode-changed', { detail: false }));
  }
};

const selectTool = (tool) => {
  movingMarkerData.value = null; // Cancelar movimiento activo al cambiar de herramienta
  selectedTool.value = tool;
  if (tool === 'forward') {
    editForm.value.isEditing = false;
    editForm.value.type = 'forward';
    editForm.value.yaw = viewer.getPosition().yaw;
    editForm.value.pitch = viewer.getPosition().pitch;
    showEditModal.value = true;
  } else if (tool === 'rotation') {
    editForm.value.isEditing = false;
    editForm.value.type = 'rotation';
    editForm.value.rotation_corrections = {};
    adjacentNeighborNames.value.forEach((neighborName) => {
      const rot = (currentNodeData.value.rotation_correction && currentNodeData.value.rotation_correction[neighborName]) || 0;
      editForm.value.rotation_corrections[neighborName] = rot.toString();
    });
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
    const adj = currentNodeData.value.adjacent_nodes[data.index];
    let w = 1.0;
    if (adj && typeof adj === 'object') {
      w = adj[data.target] ?? 1.0;
    }
    editForm.value.weight = w.toString();
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

const startMovingElement = () => {
  movingMarkerData.value = selectedMarkerData.value;
  showActionModal.value = false;
  toastRefMap.value.showToast("Haz clic en la nueva posición del visor 360° para reubicar este elemento.");
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
    const weightVal = parseFloat(editForm.value.weight) || 1.0;
    currentNodeData.value.adjacent_nodes[dirIdx] = { [editForm.value.targetNode]: weightVal };
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
  else if (editForm.value.type === 'rotation') {
    const newCorrections = {};
    for (const [neighborName, rotStr] of Object.entries(editForm.value.rotation_corrections)) {
      const rot = parseInt(rotStr, 10) || 0;
      if (rot !== 0) {
        newCorrections[neighborName] = rot;
      }
    }
    currentNodeData.value.rotation_correction = Object.keys(newCorrections).length > 0 ? newCorrections : null;
    defineData();
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
const activeSearchTargetTag = ref("");

// Helper para buscar el yaw de un tag en un nodo según el query de búsqueda del usuario
const findMatchingTagYaw = (node, targetQuery) => {
  if (!node || !node.tags || !targetQuery) return null;
  const cleanQuery = targetQuery.trim().toLowerCase();

  // 1. Coincidencia exacta por valor/nombre de la etiqueta
  for (const tagName in node.tags) {
    const tagData = node.tags[tagName];
    for (const key in tagData) {
      if (key.toLowerCase() === cleanQuery) {
        return tagData[key];
      }
    }
  }

  // 2. Coincidencia parcial por valor/nombre de la etiqueta
  for (const tagName in node.tags) {
    const tagData = node.tags[tagName];
    for (const key in tagData) {
      if (key.toLowerCase().includes(cleanQuery)) {
        return tagData[key];
      }
    }
  }

  // 3. Coincidencia por categoría de etiqueta (tagName)
  for (const tagName in node.tags) {
    if (tagName.toLowerCase() === cleanQuery) {
      const tagData = node.tags[tagName];
      const firstKey = Object.keys(tagData)[0];
      if (firstKey) {
        return tagData[firstKey];
      }
    }
  }

  return null;
};
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

    const prevNodeName = previousNodeData.value?.name;
    const currRot = (currentNodeData.value.rotation_correction && prevNodeName && currentNodeData.value.rotation_correction[prevNodeName]) || 0;
    const rotCorrection = -currRot * (Math.PI / 180);
    let initialYaw = adjustAngle((currentNodeData.value.forward_heading ?? 0) + rotCorrection, lastDirection.value);

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

    // Rotación del buscador directo
    if (activeSearchTargetTag.value) {
      const tagYaw = findMatchingTagYaw(currentNodeData.value, activeSearchTargetTag.value);
      if (tagYaw !== null) {
        setTimeout(() => {
          viewer.animate({ yaw: tagYaw, pitch: 0, speed: '8rpm' });
        }, 300);
      }
      activeSearchTargetTag.value = ""; // Reset
    }
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

    if (actualRoute.value?.targetTag) {
      const tagYaw = findMatchingTagYaw(currentNodeData.value, actualRoute.value.targetTag);
      if (tagYaw !== null) {
        setTimeout(() => {
          viewer.animate({ yaw: tagYaw, pitch: 0, speed: '8rpm' });
        }, 300);
      }
    }
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
    let nodeName = newVal;
    let targetTag = "";
    if (newVal.includes('|')) {
      const parts = newVal.split('|');
      nodeName = parts[0];
      targetTag = parts[1];
    }

    activeSearchTargetTag.value = targetTag;
    previousNodeData.value = null;
    setNode(nodeName);
    defineData();
    searchResults.value = null;
    searchInput.value = "";
    varAux.value++;
  }
});

watch(actualRoute, async (newVal) => {
  isTravelling.value = true;
  checkedRouteNodes.value = {};
  previousNodeData.value = null;
  setNode(newVal.route[0]);
  await defineData();
  varAux.value++;
  notifyTravel(newVal.weight);
}, { deep: true });

const playSvg = `<svg class="psv-button-svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>`;
const pauseSvg = `<svg class="psv-button-svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>`;

watch(isAutoRotating, (newVal) => {
  const btn = document.querySelector('.custom-rotate-btn');
  if (btn) {
    btn.innerHTML = newVal ? pauseSvg : playSvg;
  }
});

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
  if (idleTimeout) clearTimeout(idleTimeout);
  if (rotationFrameId) cancelAnimationFrame(rotationFrameId);
});

onMounted(async () => {
  await tagStore.fetchTags();
  setVh();
  window.addEventListener("resize", setVh);
  
  // Escuchar eventos globales del Sidebar (Guardar/Editar y Cancelar)
  window.addEventListener('trigger-cancel-edit', handleCancelEdit);
  window.addEventListener('trigger-toggle-edit', toggleEditMode);

  // Escuchar interacciones para pausar rotación y reactivar tras inactividad
  const startIdleTimer = () => {
    if (idleTimeout) clearTimeout(idleTimeout);
    idleTimeout = setTimeout(() => {
      isUserInteracting = false;
    }, 2500);
  };

  const container = viewerContainer.value;
  if (container) {
    container.addEventListener('mousedown', () => {
      isUserInteracting = true;
      if (idleTimeout) clearTimeout(idleTimeout);
    });
    window.addEventListener('mouseup', () => {
      startIdleTimer();
    });
    container.addEventListener('touchstart', () => {
      isUserInteracting = true;
      if (idleTimeout) clearTimeout(idleTimeout);
    });
    window.addEventListener('touchend', () => {
      startIdleTimer();
    });
  }

  setNode(route.query.node || generateRandomStartNode());

  viewer = new Viewer({
    container: viewerContainer.value,
    adapter: [EquirectangularTilesAdapter, {}],
    panorama: getTilesConfig(currentNodeData.value.name),
    plugins: [[MarkersPlugin, {}]],
    defaultZoomLvl: 0, moveSpeed: 1.75,
    defaultYaw: currentNodeData.value.forward_heading,
    navbar: [
      'zoom',
      'move',
      {
        id: 'autorotate-custom',
        title: 'Rotación automática',
        className: 'custom-rotate-btn',
        content: pauseSvg, // Inicia pausando (porque gira por defecto)
        onClick: () => {
          isAutoRotating.value = !isAutoRotating.value;
          if (isAutoRotating.value) {
            isUserInteracting = false;
            if (idleTimeout) clearTimeout(idleTimeout);
          }
        }
      },
      'fullscreen'
    ]
  });

  // Bucle de animación de rotación lenta
  const animateRotation = () => {
    if (viewer && isAutoRotating.value && !isUserInteracting && !isEditMode.value) {
      try {
        const pos = viewer.getPosition();
        viewer.rotate({
          yaw: pos.yaw + 0.0006, // Rotación suave (~0.034° por frame)
          pitch: pos.pitch
        });
      } catch (e) {
        // Ignorar si el visor no está listo
      }
    }
    if (viewer) {
      rotationFrameId = requestAnimationFrame(animateRotation);
    }
  };
  animateRotation();

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
        previousNodeData.value = currentNodeData.value;
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

    if (route.query.edit === 'true' && !isEditMode.value && isAdmin.value) {
      toggleEditMode();
    } else if (route.query.edit === 'true' && !isAdmin.value) {
      toastRefMap.value.showToast("Acceso denegado: No tienes permisos para editar nodos.");
    }
  }, { once: true });
  
  viewer.addEventListener("click", ({ data }) => {
    if (isAdmin.value && isEditMode.value) {
      if (movingMarkerData.value) {
        const origData = movingMarkerData.value;
        const newYaw = data.yaw;
        
        if (origData.type === 'arrow') {
          currentNodeData.value.arrow_angles[origData.index] = newYaw;
          toastRefMap.value.showToast(`Flecha de ${POSITION_LABELS[origData.index] || 'adyacencia'} reubicada (Guarda para confirmar).`);
        } else if (origData.type === 'tag') {
          if (currentNodeData.value.tags && currentNodeData.value.tags[origData.category]) {
            currentNodeData.value.tags[origData.category][origData.label] = newYaw;
            toastRefMap.value.showToast(`Marcador '${origData.label}' reubicado (Guarda para confirmar).`);
          }
        }
        
        movingMarkerData.value = null;
        selectedMarkerData.value = null;
        addMarkersFromCurrentNode();
        return;
      }

      if (selectedTool.value && selectedTool.value !== 'forward') {
        editForm.value.isEditing = false;
        editForm.value.originalData = null;
        editForm.value.type = selectedTool.value;
        editForm.value.yaw = data.yaw;
        editForm.value.pitch = data.pitch;
        editForm.value.targetNode = '';
        editForm.value.weight = '1.0';
        editForm.value.tagName = '';
        editForm.value.tagValue = '';
        
        if (selectedTool.value === 'arrow') {
          editForm.value.direction = '0'; // default Frente
          const existingAdj = currentNodeData.value.adjacent_nodes?.[0];
          if (existingAdj && typeof existingAdj === 'object' && Object.keys(existingAdj).length > 0) {
            const target = Object.keys(existingAdj)[0];
            const weight = existingAdj[target];
            editForm.value.targetNode = target;
            editForm.value.weight = weight !== undefined && weight !== null ? weight.toString() : '1.0';
          }
        }
        
        showEditModal.value = true;
      }
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

.max-height-options {
  max-height: 200px !important;
  overflow-y: auto !important;
}
.tag-option-item {
  display: flex !important;
  align-items: center !important;
  gap: 0.5rem !important;
}
.tag-option-icon {
  width: 1.1rem;
  height: 1.1rem;
  opacity: 0.7;
}
.selected-tag-display {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.select-tag-icon {
  width: 1.1rem;
  height: 1.1rem;
  color: var(--main-blue);
}

.admin-node-chip {
  position: absolute;
  bottom: 2rem;
  right: 1.5rem;
  display: flex;
  align-items: center;
  background: rgba(48, 55, 69, 0.7);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 40px;
  padding: 6px 8px 6px 8px;
  z-index: 20;
  box-shadow: 
    0 10px 25px -5px rgba(0, 0, 0, 0.3),
    0 8px 10px -6px rgba(0, 0, 0, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  animation: fadeIn 0.4s ease-out forwards;
  pointer-events: auto;
}

.node-name-text {
  color: var(--fill-white);
  font-size: 0.8rem;
  font-weight: 600;
  font-family: 'SF Mono', Monaco, Consolas, monospace;
  letter-spacing: 0.05em;
}

.viewer-wrapper.moving-mode-active {
  .viewer-container, .psv-container, .psv-canvas {
    cursor: crosshair !important;
  }
}
</style>