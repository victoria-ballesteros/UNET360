<template>
  <div class="node-admin-container">

    <!-- Header -->
    <div class="node-admin-header">
      <div class="text-section">
        <p class="header-overline">Panel de control</p>
        <h2>Administrar Nodos</h2>
      </div>

      <div class="button-section">
        <UButton text="Crear Nuevo Nodo" type="contrast-2" @click="router.push({ name: 'NodeCreate' })" />
        <div class="admin-entities-buttons">
          <UButton text="Tags" type="secondary" @click="router.push({ name: 'AdminEntities', params: { entity: 'tags' } })" />
          <UButton text="Locations" type="secondary" @click="router.push({ name: 'AdminEntities', params: { entity: 'locations' } })" />
        </div>
      </div>
    </div>

    <!-- Toolbar: search + sort -->
    <div class="nodes-list-section">
      <div class="nodes-list-toolbar">
        <div class="search-wrap">
          <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <circle cx="11" cy="11" r="7"/><path d="m21 21-4.35-4.35"/>
          </svg>
          <input
            v-model="searchQuery"
            type="text"
            class="nodes-search-input"
            placeholder="Buscar por nombre o ubicación..."
          />
        </div>

        <div class="sort-toggle">
          <button
            class="sort-btn"
            :class="{ active: sortOrder === 'asc' }"
            @click="sortOrder = 'asc'"
            title="A → Z"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 6h18M3 12h12M3 18h6"/><path d="m17 14 3 3 3-3"/><path d="M20 17V8"/>
            </svg>
            A–Z
          </button>
          <button
            class="sort-btn"
            :class="{ active: sortOrder === 'desc' }"
            @click="sortOrder = 'desc'"
            title="Z → A"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 6h18M3 12h12M3 18h6"/><path d="m17 10-3-3-3 3"/><path d="M14 7v9"/>
            </svg>
            Z–A
          </button>
        </div>
      </div>

      <div v-if="filteredNodes.length === 0" class="empty-message">
        No hay nodos registrados.
      </div>

      <div v-else class="node-list-wrap">
        <div v-for="(node, index) in paginatedNodes" :key="node.name" class="node-item">
          <div class="node-main" @click="toggleNode(node.name)">
            <div class="node-info">
              <span class="node-status" :style="{ background: getStatusColor(node.status) }" />
              <span class="node-name">{{ node.name }}</span>
            </div>
            <div class="node-actions">
              <button class="icon-btn" @click.stop="goToMap(node)" title="Ver en mapa 360°">
                <UIcon name="icons/image" class="node-action-icon" size="100%" />
              </button>
              <button class="icon-btn" @click.stop="editNode(node)">
                <UIcon name="icons/edit" class="node-action-icon" size="100%" />
              </button>
            </div>
          </div>

          <div v-if="expandedNode === node.name" class="node-details">
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
              <div class="location-info">
                <span class="location-label">{{ locationLabel }}</span>
                <span class="location-value">{{ node.location }}</span>
              </div>
            </div>

            <div class="tags-info">
              <span class="tags-label">{{ tagsLabel }}</span>
              <div class="tags-list">
                <span
                  v-if="node.tags && Object.keys(node.tags).length"
                  v-for="(values, tag) in node.tags"
                  :key="tag"
                  class="tag-item"
                >
                  {{ tag }}:
                  <template v-if="Array.isArray(values)">{{ values.join(', ') }}</template>
                  <template v-else>{{ Object.entries(values)[0][0] }}</template>
                </span>
                <span v-else class="tag-item">{{ tagsEmpty }}</span>
              </div>
            </div>

            <div class="reasons" v-if="node.reasons && node.reasons.length">
              <div class="reasons-title">Advertencias:</div>
              <ul class="reasons-list">
                <li v-for="(r, i) in node.reasons" :key="i">{{ r }}</li>
              </ul>
            </div>

            <div class="delete-section">
              <button class="delete-node-btn" @click.stop="openDeleteConfirm(node.name)">
                <UIcon name="icons/trash" class="delete-icon" />
                {{ deleteLabel }}
              </button>
            </div>
          </div>

          <div v-if="index !== paginatedNodes.length - 1" class="node-separator" />
        </div>

        <div class="pagination" v-if="totalPages > 1">
          <button class="page-btn" :disabled="currentPage === 1" @click="goToPage(currentPage - 1)">Anterior</button>
          <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
          <button class="page-btn" :disabled="currentPage === totalPages" @click="goToPage(currentPage + 1)">Siguiente</button>
        </div>
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

const pageSize = 10;
const currentPage = ref(1);
const searchQuery = ref('');
const sortOrder = ref('asc'); // 'asc' | 'desc'

const statusPriority = { 'ERROR': 0, 'WARNING': 1, 'OK': 2 };

const sortedNodes = computed(() => {
  const arr = [...nodes.value];
  arr.sort((a, b) => {
    const pa = statusPriority[a.status] ?? 3;
    const pb = statusPriority[b.status] ?? 3;
    if (pa !== pb) return pa - pb;
    // nombre A→Z o Z→A según sortOrder
    const nameA = a.name?.toLowerCase() ?? '';
    const nameB = b.name?.toLowerCase() ?? '';
    return sortOrder.value === 'asc'
      ? nameA.localeCompare(nameB)
      : nameB.localeCompare(nameA);
  });
  return arr;
});

const filteredNodes = computed(() => {
  if (!searchQuery.value.trim()) return sortedNodes.value;
  const q = searchQuery.value.trim().toLowerCase();
  return sortedNodes.value.filter(n =>
    n.name?.toLowerCase().includes(q) || n.location?.toLowerCase().includes(q)
  );
});

const totalPages = computed(() => Math.max(1, Math.ceil(filteredNodes.value.length / pageSize)));
const paginatedNodes = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  return filteredNodes.value.slice(start, start + pageSize);
});

watch(sortedNodes, () => {
  if (currentPage.value > totalPages.value) currentPage.value = totalPages.value;
});
watch(searchQuery, () => { currentPage.value = 1; });
watch(sortOrder,  () => { currentPage.value = 1; });

function goToPage(p) {
  if (p >= 1 && p <= totalPages.value) currentPage.value = p;
}

const expandedNode = ref(null);

const adyacentTitle = 'Adyacentes';
const adyacentGroups = [
  { name: 'group1', class: 'adyacent-node-group-1', items: [{ label: 'Fre', key: 'frente' }, { label: 'Atr', key: 'atras' }] },
  { name: 'group2', class: 'adyacent-node-group-2', items: [{ label: 'Izq', key: 'izquierda' }, { label: 'Der', key: 'derecha' }] },
];

const locationLabel = 'Ubicación';
const tagsLabel = 'Tags';
const tagsEmpty = 'Sin tags';
const deleteLabel = 'Eliminar nodo';

const showDeleteDialog = ref(false);
const nodeToDelete = ref('');

const getStatusColor = status => ({
  'OK': 'var(--status-green, #4caf50)',
  'WARNING': 'var(--status-yellow, #ffb300)',
  'ERROR': 'var(--status-red, #e53935)',
}[status] ?? 'rgba(255,255,255,0.25)');

const toggleNode = name => {
  expandedNode.value = expandedNode.value === name ? null : name;
};

const goToMap = node => {
  router.push({ name: 'Map', query: { node: node.name } });
};

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
    if (index !== -1) nodes.value.splice(index, 1);
    if (currentNode?.url_image) await deleteImageFromServer(currentNode.url_image);
  }
  showDeleteDialog.value = false;
};

const getAdyacentValue = (node, key) => {
  const keyMap = { frente: 0, atras: 2, izquierda: 3, derecha: 1 };
  if (Array.isArray(node.adjacent_nodes)) {
    const adj = node.adjacent_nodes[keyMap[key]];
    if (adj && typeof adj === 'object') return Object.keys(adj)[0] || 'N/A';
    return 'N/A';
  }
  return node.adjacent_nodes?.[key] || 'N/A';
};

onMounted(async () => { await nodeStore.fetchNodes(); });
</script>

<script>
export default { components: { UIcon, UButton, UDialog } };
</script>

<style lang="scss" scoped>
@import '@/assets/styles/pages/_node_admin.scss';
</style>
