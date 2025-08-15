<template>
  <div class="node-admin-container">
    <div class="text-section">
      <h2>ADMINISTRAR NODOS</h2>
    </div>
    <div class="button-section">
      <UButton text="Crear Nuevo Nodo" type="contrast-2" @click="router.push({ name: 'NodeCreate' })" />
      <div class="admin-entities-buttons">
      <UButton text="Administrar Tags" type="secondary" @click="router.push({ name: 'AdminEntities', params: { entity: 'tags' } })" />
      <UButton text="Administrar Locations" type="secondary" @click="router.push({ name: 'AdminEntities', params: { entity: 'locations' } })" />
      </div>
    </div>
    <div class="nodes-list-section">
      <div class="nodes-list-toolbar">
        <input
          v-model="searchQuery"
          type="text"
          class="nodes-search-input"
          placeholder="Buscar por nombre o ubicación..."
        />
      </div>
      <div v-if="filteredNodes.length === 0" class="empty-message">
        No hay nodos registrados.
      </div>
      <div v-else>
        <div v-for="(node, index) in paginatedNodes" :key="node.name" class="node-item">
          <div class="node-main" @click="toggleNode(node.name)">
            <div class="node-info">
              <span class="node-status" :style="{ background: getStatusColor(node.status) }"></span>
              <span class="node-name">{{ node.name }}</span>
            </div>
            <div class="node-actions">
              <button class="icon-btn" @click.stop="openImageModal(node)">
                <UIcon name="icons/image" class="node-action-icon" size="100%" />
              </button>
              <button class="icon-btn" @click.stop="editNode(node)">
                <UIcon name="icons/edit" class="node-action-icon" size="100%" />
              </button>
            </div>
          </div>
          <div v-if="expandedNode === node.name" class="node-details">
            <!-- Primary Info -->
            <div class="primary-info">
              <div class="adyacent-info">
                <div class="adyacent-title">{{ adyacentTitle }}</div>
                <div class="adyacent-nodes">
                  <div v-for="group in adyacentGroups" :key="group.name" :class="group.class">
                    <span v-for="adj in group.items" :key="adj.key" class="adyacent-label">
                      {{ adj.label }}:
                      <span class="adyacent-value-blue">{{ getAdyacentValue(node, adj.key) }}</span>
                    </span>
                  </div>
                </div>
              </div>
              <!-- Location Info -->
              <div class="location-info">
                <span class="location-label">{{ locationLabel }}</span>
                <span class="location-value">{{ node.location }}</span>
              </div>
            </div>
            <!-- Tags -->
            <div class="tags-info">
              <span class="tags-label">{{ tagsLabel }}</span>
              <div class="tags-list">
                <span v-if="node.tags && Object.keys(node.tags).length" v-for="(values, tag) in node.tags" :key="tag"
                  class="tag-item">
                  {{ tag }}:
                  <template v-if="Array.isArray(values)">
                    {{ values.join(', ') }}
                  </template>
                  <template v-else>
                    {{ Object.entries(values)[0][0] }}
                  </template>
                </span>
                <span v-else class="tag-item">{{ tagsEmpty }}</span>
              </div>
            </div>
            <!-- Status reasons -->
            <div class="reasons" v-if="node.reasons && node.reasons.length">
              <div class="reasons-title">Advertencias:</div>
              <ul class="reasons-list">
                <li v-for="(r, i) in node.reasons" :key="i">{{ r }}</li>
              </ul>
            </div>
            <!-- Delete Button -->
            <div class="delete-section">
              <button class="delete-node-btn" @click.stop="openDeleteConfirm(node.name)">
                <UIcon name="icons/trash" size="10" class="delete-icon" />
                {{ deleteLabel }}
              </button>
            </div>
          </div>
          <div v-if="index !== paginatedNodes.length - 1" class="node-separator"></div>
        </div>
        <!-- Controles de paginación -->
        <div class="pagination" v-if="totalPages > 1">
          <button class="page-btn" :disabled="currentPage === 1" @click="goToPage(currentPage - 1)">Anterior</button>
          <span class="page-info">Página {{ currentPage }} / {{ totalPages }}</span>
          <button class="page-btn" :disabled="currentPage === totalPages" @click="goToPage(currentPage + 1)">Siguiente</button>
        </div>
      </div>
    </div>
    <!-- Modal de imagen -->
    <div v-if="showImageModal" class="image-modal-overlay" @click.self="closeImageModal">
      <div class="image-modal-content">
        <div class="image-modal-header">
          <span class="image-modal-title">Nodo: {{ modalNodeName }}</span>
          <button class="image-modal-close" @click="closeImageModal">✕</button>
        </div>
        <div v-if="isImageLoading" class="loading-bar-container">
          <div class="loading-bar"></div>
        </div>
        <img v-show="!isImageLoading" :src="modalImageUrl" alt="Imagen del nodo" class="image-modal-img"
          @load="isImageLoading = false" @error="isImageLoading = false" />
      </div>
    </div>
  </div>
  <UDialog v-model="showDeleteDialog" :headerTitle="''">
    <div class="delete-dialog-content">
      <div class="delete-dialog-header">¿Desea eliminar el nodo {{ nodeToDelete }}?</div>
      <div class="delete-dialog-actions">
        <UButton text="Cancelar" type="tertiary" @click="showDeleteDialog = false" />
        <UButton text="Continuar" type="danger" @click="confirmDelete" />
      </div>
    </div>
  </UDialog>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useNodeStore } from '@/service/stores/nodes.js';
import { useRouter } from 'vue-router';
import { storeToRefs } from 'pinia';

import UIcon from '@/components/UIcon.vue';
import UButton from '@/components/UButton.vue';
import UDialog from '@/components/UDialog.vue';

import { deleteNode as deleteNodeRequest, deleteImageFromServer } from '@/service/requests/requests.js';

const router = useRouter();
const nodeStore = useNodeStore();
const { nodes } = storeToRefs(nodeStore);
// Paginación, ordenamiento y búsqueda
const pageSize = 10;
const currentPage = ref(1);
const searchQuery = ref('');

// Orden: Primero status ERROR, luego WARNING, luego OK (u otros), y dentro de cada grupo por "reciente".
// No hay timestamp, así que usamos el orden original asumido que llega como insertion order, invertido para "más reciente primero".
// Si se añade un campo de fecha en el futuro (ej: created_at), reemplazar la parte de fallback con esa fecha.
const statusPriority = { 'ERROR': 0, 'WARNING': 1, 'OK': 2 };

const sortedNodes = computed(() => {
  // Copia para no mutar
  const arr = [...nodes.value];
  // Asumimos que el array ya viene en orden de creación (antiguo -> nuevo); para reciente primero invertimos.
  arr.reverse();
  return arr.sort((a, b) => {
    const pa = statusPriority[a.status] ?? 3;
    const pb = statusPriority[b.status] ?? 3;
    if (pa !== pb) return pa - pb;
    // Como segundo criterio dejamos el orden (ya invertido) sin más cambios.
    return 0;
  });
});

const filteredNodes = computed(() => {
  if (!searchQuery.value.trim()) return sortedNodes.value;
  const q = searchQuery.value.trim().toLowerCase();
  return sortedNodes.value.filter(n => {
    const nameMatch = n.name?.toLowerCase().includes(q);
    const locMatch = n.location?.toLowerCase().includes(q);
    return nameMatch || locMatch;
  });
});

const totalPages = computed(() => Math.max(1, Math.ceil(filteredNodes.value.length / pageSize)));
const paginatedNodes = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  return filteredNodes.value.slice(start, start + pageSize);
});

watch(sortedNodes, () => {
  // Si al cambiar los datos la página actual queda fuera de rango, reajustar
  if (currentPage.value > totalPages.value) currentPage.value = totalPages.value;
});

watch(searchQuery, () => {
  currentPage.value = 1; // Reiniciar al buscar
});

function goToPage(p) {
  if (p >= 1 && p <= totalPages.value) currentPage.value = p;
}
const isImageLoading = ref(true);

const expandedNode = ref(null);
const showImageModal = ref(false);
const modalImageUrl = ref('');
const modalNodeName = ref('');

const adyacentTitle = 'Adyacentes';
const adyacentNA = 'N/A';
const adyacentGroups = [
  {
    name: 'group1',
    class: 'adyacent-node-group-1',
    items: [
      { label: 'Fre', key: 'frente' },
      { label: 'Atr', key: 'atras' },
    ],
  },
  {
    name: 'group2',
    class: 'adyacent-node-group-2',
    items: [
      { label: 'Izq', key: 'izquierda' },
      { label: 'Der', key: 'derecha' },
    ],
  },
];

const locationLabel = 'Ubicación:';
const tagsLabel = 'Tags:';
const tagsEmpty = 'Sin tags';
const deleteLabel = 'Eliminar nodo';

const showDeleteDialog = ref(false);
const nodeToDelete = ref('');

const getStatusColor = status => {
  switch (status) {
    case 'OK': return 'var(--status-green, #4caf50)';
    case 'WARNING': return 'var(--status-yellow, #ffb300)';
    case 'ERROR': return 'var(--status-red, #e53935)';
    default: return 'var(--status-gray, #bdbdbd)';
  }
};

const toggleNode = name => {
  expandedNode.value = expandedNode.value === name ? null : name;
};

const openImageModal = node => {
  modalImageUrl.value = node.url_image;
  modalNodeName.value = node.name;
  isImageLoading.value = true;
  showImageModal.value = true;
};

const closeImageModal = () => {
  showImageModal.value = false;
  modalImageUrl.value = '';
  modalNodeName.value = '';
};

const viewImages = node => openImageModal(node);

const editNode = node => {
  router.push({ name: 'NodeEdit', params: { name: node.name } });
};

const openDeleteConfirm = name => {
  nodeToDelete.value = name;
  showDeleteDialog.value = true;
};

const confirmDelete = async () => {
  if (!nodeToDelete.value) return;
  const currentNode = nodes.value.find(obj => obj.name === nodeToDelete.value);

  const resp = await deleteNodeRequest(nodeToDelete.value);
  if (resp?.status) {
    const index = nodes.value.findIndex(obj => obj.name === nodeToDelete.value);
    if (index !== -1) {
      nodes.value.splice(index, 1);
    }

    if (currentNode?.url_image) {
      await deleteImageFromServer(currentNode.url_image);
    }
  }
  showDeleteDialog.value = false;
};

const getAdyacentValue = (node, key) => {
  const keyMap = { frente: 0, atras: 2, izquierda: 3, derecha: 1 };
  if (Array.isArray(node.adjacent_nodes)) {
    const idx = keyMap[key];
    const adj = node.adjacent_nodes[idx];
    if (adj && typeof adj === 'object') {
      return Object.keys(adj)[0] || adyacentNA;
    }
    return adyacentNA;
  }
  return node.adjacent_nodes?.[key] || adyacentNA;
};

onMounted(async () => {
  await nodeStore.fetchNodes();
});

</script>

<script>
export default {
  components: { UIcon, UButton, UDialog },
};
</script>


<style lang="scss" scoped>
@import '@/assets/styles/pages/_node_admin.scss';
</style>
