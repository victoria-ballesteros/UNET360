<template>
  <div class="node-admin-container">

    <!-- ── Header ── -->
    <div class="node-admin-header">
      <div class="header-top-row">
        <div class="text-section">
          <p class="header-overline">Panel de control</p>
          <h2>Administrar Nodos</h2>
        </div>
        <div class="admin-entities-buttons">
          <UButton text="Tags"      type="secondary" @click="router.push({ name: 'AdminEntities', params: { entity: 'tags' } })" />
          <UButton text="Locations" type="secondary" @click="router.push({ name: 'AdminEntities', params: { entity: 'locations' } })" />
        </div>
      </div>

      <div class="action-buttons">
        <UButton text="Crear nuevo nodo" type="contrast-2" @click="router.push({ name: 'NodeCreate' })" />
        <UButton text="Corregir pesos" type="contrast-2" :loading="isFixing" @click="fixWeights" />
        <UButton text="Buscar perdidos" type="contrast-2" :loading="isSearchingMissing" @click="searchMissingTiles" />
      </div>

      <div class="node-stats-chips">
        <span class="node-stat-chip" title="Número de nodo más alto registrado">
          <span class="chip-label">Nodo más alto:</span>
          <span class="chip-value">{{ highestNodeNumber }}</span>
        </span>
        <span class="node-stat-chip" title="Último nodo creado">
          <span class="chip-label">Último creado:</span>
          <span class="chip-value">{{ lastCreatedNode }}</span>
        </span>
        <span
          v-if="missingTilesResult !== null"
          class="node-stat-chip"
          :class="{ 'chip-danger': missingTilesResult.length > 0, 'chip-ok': missingTilesResult.length === 0 }"
          :title="missingTilesResult.length ? 'Nodos: ' + missingTilesResult.join(', ') : 'Todas las carpetas de tiles existen'"
        >
          <span class="chip-label">Imágenes perdidas:</span>
          <span class="chip-value">{{ missingTilesResult.length }}<template v-if="missingTilesResult.length"> ({{ missingTilesResult.join(', ') }})</template></span>
        </span>
      </div>
    </div>

    <!-- ── Lista de nodos ── -->
    <div class="nodes-list-section">
      <UAdminList
        :items="paginatedNodes"
        :loading="isListLoading"
        :server-side="true"
        :total-items="totalNodesCount"
        :extra-offset="67"
        @change="handleListChange"
        search-placeholder="Buscar por nombre..."
        empty-message="No hay nodos registrados."
        no-results-message="No se encontraron nodos."
        item-key-field="name"
      >
        <template #item="{ item: node }">
          <div class="node-item">

            <div class="node-main" @click="toggleNode(node.name)">
              <div class="node-info">
                <span class="node-status" :style="{ background: getStatusColor(node.status), color: getStatusColor(node.status) }" />
                <span class="node-name">{{ node.name }}</span>
              </div>
              <div class="node-actions">
                <UButton
                  icon="icons/image"
                  type="tertiary"
                  size="md"
                  @click.stop="goToMap(node)"
                  title="Ver en mapa 360°"
                />
                <UButton
                  icon="icons/edit"
                  type="tertiary"
                  size="md"
                  @click.stop="editNode(node)"
                  title="Editar nodo"
                />
              </div>
            </div>

            <div v-if="expandedNode === node.name" class="node-details">
              
              <!-- Información General -->
              <div class="info-group">
                <div class="info-item" v-if="node.location">
                  <span class="info-label">Ubicación:</span>
                  <span class="info-value location-text">{{ node.location }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">Orientación Inicial:</span>
                  <span class="info-value">
                    <strong class="highlight-yellow">{{ radToDeg(node.forward_heading) }}</strong>
                    <span class="rad-desc">({{ formatAngleRad(node.forward_heading) }})</span>
                  </span>
                </div>
                <div class="info-item" v-if="node.minimap && node.minimap.image">
                  <span class="info-label">Mapa 2D:</span>
                  <span class="info-value code-text">
                    {{ node.minimap.image }}
                    <span class="coords-suffix">(X: {{ node.minimap.x ?? 'N/A' }}, Y: {{ node.minimap.y ?? 'N/A' }})</span>
                  </span>
                </div>
              </div>

              <!-- Conexiones Existentes (Sin ángulos ni N/As) -->
              <div class="details-row-section" v-if="getExistingConnections(node).length">
                <span class="details-section-label">Conexiones:</span>
                <div class="connections-tags">
                  <span v-for="conn in getExistingConnections(node)" :key="conn.dir" class="connection-tag-item">
                    <span class="direction-indicator" :class="conn.dir">
                      {{ conn.dir === 'frente' ? '↑' : conn.dir === 'derecha' ? '→' : conn.dir === 'atras' ? '↓' : '←' }}
                    </span>
                    <span class="conn-dir-label">{{ conn.dir.charAt(0).toUpperCase() + conn.dir.slice(1) }}:</span>
                    <strong class="conn-neighbor-val">{{ conn.neighbor }}</strong>
                  </span>
                </div>
              </div>

              <!-- Correcciones de Rotación Existentes -->
              <div class="details-row-section" v-if="node.rotation_correction && Object.keys(node.rotation_correction).length">
                <span class="details-section-label">Correcciones de Rotación:</span>
                <div class="rotations-tags">
                  <span v-for="(deg, neighbor) in node.rotation_correction" :key="neighbor" class="rotation-tag-item">
                    <span class="rot-label">Desde {{ neighbor }}:</span>
                    <strong class="rot-val">{{ deg }}°</strong>
                  </span>
                </div>
              </div>

              <!-- Tags del Nodo -->
              <div class="tags-info">
                <span class="tags-label">{{ tagsLabel }}:</span>
                <div class="tags-list">
                  <span
                    v-if="node.tags && Object.keys(node.tags).length"
                    v-for="(values, tag) in node.tags"
                    :key="tag"
                    class="tag-item"
                  >
                    <span class="tag-category">{{ tag }}:</span>
                    <span class="tag-val">
                      <template v-if="Array.isArray(values)">{{ values.join(', ') }}</template>
                      <template v-else>{{ Object.entries(values)[0][0] }}</template>
                    </span>
                  </span>
                  <span v-else class="tag-item empty-tags">{{ tagsEmpty }}</span>
                </div>
              </div>

              <!-- Advertencias de Estado -->
              <div class="reasons" v-if="node.reasons && node.reasons.length">
                <div class="reasons-header-container">
                  <UIcon name="icons/exclamation-circle" class="warning-icon" />
                  <span class="reasons-title">Advertencias detectadas:</span>
                </div>
                <ul class="reasons-list">
                  <li v-for="(r, i) in node.reasons" :key="i">{{ r }}</li>
                </ul>
              </div>

              <!-- Sección de Eliminación -->
              <div class="delete-section">
                <UButton
                  class="delete-node-btn"
                  type="danger"
                  icon="icons/trash"
                  :text="deleteLabel"
                  @click.stop="openDeleteConfirm(node.name)"
                />
              </div>
            </div>

          </div>
        </template>
      </UAdminList>
    </div>

  </div>

  <!-- ── Modal de confirmación de borrado ── -->
  <UBaseModal
    v-model="showDeleteDialog"
    title="Eliminar nodo"
    size="sm"
    :danger="true"
  >
    <p class="modal-confirm-text">¿Seguro que deseas eliminar el nodo <strong>{{ nodeToDelete }}</strong>? Esta acción no se puede deshacer.</p>
    <template #footer>
      <UButton text="Cancelar"  type="tertiary" @click="showDeleteDialog = false" />
      <UButton text="Eliminar"  type="danger"   @click="confirmDelete" />
    </template>
  </UBaseModal>
  <UToast ref="toastRef" />
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useNodeStore } from '@/service/stores/nodes.js';
import { useRouter } from 'vue-router';
import { storeToRefs } from 'pinia';
import api from '@/axios';

import UIcon    from '@/components/UIcon.vue';
import UButton  from '@/components/UButton.vue';
import UBaseModal from '@/components/UBaseModal.vue';
import UAdminList from '@/components/UAdminList.vue';
import UToast from '@/components/UToast.vue';

import { deleteNode as deleteNodeRequest, deleteImageFromServer, fixAsymmetricWeights, getMissingTiles } from '@/service/requests/requests.js';

const router    = useRouter();
const nodeStore = useNodeStore();
const { nodes, isLoading } = storeToRefs(nodeStore);

// ── Estado de paginación de servidor ───────────────────────────────────────
const rawPaginatedNodes = ref([]);
const totalNodesCount   = ref(0);
const isListLoading     = ref(false);
const currentListParams = ref({ page: 1, pageSize: 10, search: '', sort: 'asc' });

// Mapeo y ordenación reactiva de nodos usando computeds (evita condiciones de carrera y fallos de status)
const paginatedNodes = computed(() => {
  const mapped = rawPaginatedNodes.value.map(n => {
    const storeNode = nodes.value.find(sn => sn.name === n.name);
    return {
      ...n,
      status: storeNode?.status || null,
      reasons: storeNode?.reasons || null,
    };
  });
  
  // Ordenar localmente la página actual por prioridad de estado
  const statusPriority = { ERROR: 0, WARNING: 1, OK: 2 };
  return [...mapped].sort((a, b) => {
    const pa = statusPriority[a.status] ?? 3;
    const pb = statusPriority[b.status] ?? 3;
    if (pa !== pb) return pa - pb;
    const na = a.name?.toLowerCase() ?? '';
    const nb = b.name?.toLowerCase() ?? '';
    return currentListParams.value.sort === 'asc' 
      ? na.localeCompare(nb, undefined, { numeric: true }) 
      : nb.localeCompare(na, undefined, { numeric: true });
  });
});

const handleListChange = async (params) => {
  currentListParams.value = params;
  isListLoading.value = true;
  
  try {
    const { data } = await api.get('nodes/', {
      params: {
        page: params.page,
        page_size: params.pageSize,
        search: params.search || undefined,
        sort: params.sort || 'asc'
      }
    });
    
    if (data?.status && data.response_obj) {
      const res = data.response_obj;
      rawPaginatedNodes.value = res.items || [];
      totalNodesCount.value = res.total || 0;
    }
  } catch (error) {
    console.error("Error al obtener nodos paginados:", error);
  } finally {
    isListLoading.value = false;
  }
};

const triggerRefetch = async () => {
  await handleListChange(currentListParams.value);
};

// ── Estadísticas de nodos (más alto / último creado) ───────────────────────
// Se asume que node.name es numérico (ej. "001"), pero no todos los nodos
// tienen por qué serlo, de ahí el try/catch para descartar los que no lo son.
const highestNodeNumber = computed(() => {
  let highest = null;
  for (const node of nodes.value) {
    try {
      const num = parseInt(node.name, 10);
      if (isNaN(num)) continue;
      if (highest === null || num > highest) highest = num;
    } catch (_) {
      continue;
    }
  }
  return highest !== null ? highest : 'N/A';
});

const lastCreatedNode = computed(() => {
  if (!nodes.value.length) return 'N/A';
  const last = nodes.value[nodes.value.length - 1];
  try {
    return last?.name ?? 'N/A';
  } catch (_) {
    return 'N/A';
  }
});

// ── Estado expandible ──────────────────────────────────────────────────────
const expandedNode = ref(null);

const toggleNode = (name) => {
  expandedNode.value = expandedNode.value === name ? null : name;
};

// ── Labels y grupos de adyacencia ─────────────────────────────────────────
const tagsLabel     = 'Tags';
const tagsEmpty     = 'Sin tags';
const deleteLabel   = 'Eliminar nodo';

// ── Estado del nodo ────────────────────────────────────────────────────────
const getStatusColor = (status) => ({
  OK:      'var(--status-green,  #4caf50)',
  WARNING: 'var(--status-yellow, #ffb300)',
  ERROR:   'var(--status-red,    #e53935)',
}[status] ?? 'rgba(255,255,255,0.25)');

const radToDeg = (rad) => {
  if (rad === null || rad === undefined || isNaN(rad) || rad === '') return 'N/A';
  let deg = rad * (180 / Math.PI);
  deg = (deg % 360 + 360) % 360;
  return `${deg.toFixed(1)}°`;
};

const formatAngleRad = (rad) => {
  if (rad === null || rad === undefined || isNaN(rad) || rad === '') return 'N/A';
  return `${parseFloat(rad).toFixed(2)} rad`;
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

const getExistingConnections = (node) => {
  const directions = ['frente', 'derecha', 'atras', 'izquierda'];
  const existings = [];
  for (const dir of directions) {
    const val = getAdyacentValue(node, dir);
    if (val && val !== 'N/A') {
      existings.push({ dir, neighbor: val });
    }
  }
  return existings;
};

// ── Navegación ─────────────────────────────────────────────────────────────
const goToMap   = (node) => router.push({ name: 'Map', query: { node: node.name } });
const editNode  = (node) => router.push({ name: 'Map', query: { node: node.name, edit: 'true' } });

// ── Borrado ────────────────────────────────────────────────────────────────
const showDeleteDialog = ref(false);
const nodeToDelete     = ref('');

const openDeleteConfirm = (name) => {
  nodeToDelete.value    = name;
  showDeleteDialog.value = true;
};

const confirmDelete = async () => {
  if (!nodeToDelete.value) return;
  const currentNode = paginatedNodes.value.find(obj => obj.name === nodeToDelete.value) || 
                      nodes.value.find(obj => obj.name === nodeToDelete.value);
  const resp = await deleteNodeRequest(nodeToDelete.value);
  if (resp?.status) {
    const index = nodes.value.findIndex(obj => obj.name === nodeToDelete.value);
    if (index !== -1) nodes.value.splice(index, 1);
    if (currentNode?.url_image) await deleteImageFromServer(currentNode.url_image);
    await triggerRefetch();
  }
  showDeleteDialog.value = false;
};

const isFixing = ref(false);
const toastRef = ref(null);

const fixWeights = async () => {
  isFixing.value = true;
  try {
    const resp = await fixAsymmetricWeights();
    isFixing.value = false; // Detener estado de carga inmediatamente al terminar la petición
    if (resp?.status) {
      const count = resp.response_obj?.updated_count ?? 0;
      if (toastRef.value) {
        toastRef.value.showToast(`Éxito: se corrigieron los pesos de ${count} nodos.`);
      } else {
        console.log(`Éxito: se corrigieron los pesos de ${count} nodos.`);
      }
      await nodeStore.fetchNodes(); // Cargar nodos asincrónicamente en background
      await triggerRefetch(); // Refrescar vista paginada
    } else {
      const msg = resp?.response_obj?.message || "No se pudieron corregir los pesos del grafo.";
      if (toastRef.value) {
        toastRef.value.showToast(`Error: ${msg}`);
      } else {
        console.error(`Error: ${msg}`);
      }
    }
  } catch (error) {
    isFixing.value = false;
    if (toastRef.value) {
      toastRef.value.showToast("Error al intentar corregir los pesos.");
    } else {
      console.error("Error al intentar corregir los pesos:", error);
    }
  }
};

// ── Buscar imágenes perdidas ───────────────────────────────────────────────
const isSearchingMissing = ref(false);
const missingTilesResult = ref(null);

const searchMissingTiles = async () => {
  isSearchingMissing.value = true;
  missingTilesResult.value = null;
  try {
    const resp = await getMissingTiles();
    if (resp?.status && resp.response_obj) {
      missingTilesResult.value = resp.response_obj.missing || [];
      const count = resp.response_obj.count ?? 0;
      if (toastRef.value) {
        if (count > 0) {
          toastRef.value.showToast(`Se encontraron ${count} nodos sin carpeta de tiles.`);
        } else {
          toastRef.value.showToast('Todas las carpetas de tiles están presentes.');
        }
      }
    } else {
      const msg = resp?.response_obj?.message || 'No se pudo verificar las imágenes.';
      if (toastRef.value) {
        toastRef.value.showToast(`Error: ${msg}`);
      }
    }
  } catch (error) {
    if (toastRef.value) {
      toastRef.value.showToast('Error al buscar imágenes perdidas.');
    }
  } finally {
    isSearchingMissing.value = false;
  }
};

// ── Carga inicial ──────────────────────────────────────────────────────────
onMounted(async () => {
  await nodeStore.fetchNodes();
});
</script>

<script>
export default { components: { UIcon, UButton, UBaseModal, UAdminList, UToast } };
</script>

<style lang="scss" scoped>
@import '@/assets/styles/pages/_node_admin.scss';
</style>
