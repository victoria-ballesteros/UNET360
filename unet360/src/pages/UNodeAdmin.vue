<template>
  <div class="node-admin-container">
    <div class="text-section">
      <h2>ADMINISTRAR NODOS</h2>
    </div>
    <div class="button-section">
      <UButton
        text="Crear Nuevo Nodo"
        type="contrast-2"
        @click="router.push({ name: 'NodeCreate' })"
      />
    </div>
    <div class="nodes-list-section">
      <div v-if="nodes.length === 0" class="empty-message">
        No hay nodos registrados.
      </div>
      <div v-else>
        <div v-for="node in nodes" :key="node.name" class="node-item">
          <div class="node-main" @click="toggleNode(node.name)">
            <div class="node-info">
              <span class="node-status" :style="{ background: getStatusColor(node.status) }"></span>
              <span class="node-name">{{ node.name }}</span>
            </div>
            <div class="node-actions">
              <button class="icon-btn" @click.stop="openImageModal(node)">
                <UIcon name="icons/image" class="node-action-icon" size="100%"/>
              </button>
              <button class="icon-btn" @click.stop="editNode(node)">
                <UIcon name="icons/edit" class="node-action-icon" size="100%"/>
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
                <span v-if="node.tags && Object.keys(node.tags).length" v-for="(values, tag) in node.tags" :key="tag" class="tag-item">{{ tag }}: {{ Array.isArray(values) ? values.join(', ') : values }}</span>
                <span v-else class="tag-item">{{ tagsEmpty }}</span>
              </div>
            </div>
            <!-- Status reasons -->
            <div class="reasons" v-if="node.reasons && node.reasons.length">
              <div class="reasons-title">Motivos:</div>
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
          <div class="node-separator"></div>
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
        <img :src="modalImageUrl" alt="Imagen del nodo" class="image-modal-img" />
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

<script>
import { onMounted, ref } from 'vue';
import { useNodeStore } from '@/service/stores/nodes.js';
import UIcon from '@/components/UIcon.vue';
import UButton from '@/components/UButton.vue';
import UDialog from '@/components/UDialog.vue';
import { useRouter } from 'vue-router';
import { deleteNode as deleteNodeRequest } from '@/service/requests/requests.js';
export default {
  name: 'UNodeAdmin',
  components: { UIcon, UButton, UDialog },
  setup() {
    const router = useRouter();
    const { nodes, isLoading, error, fetchNodes } = useNodeStore();
    const expandedNode = ref(null);
    const showImageModal = ref(false);
    const modalImageUrl = ref('');
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

    onMounted(fetchNodes);

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
    const modalNodeName = ref('');
    const openImageModal = node => {
      modalImageUrl.value = node.url_image;
      modalNodeName.value = node.name;
      showImageModal.value = true;
    };
    const closeImageModal = () => {
      showImageModal.value = false;
      modalImageUrl.value = '';
    };
    const viewImages = node => openImageModal(node);
    const editNode = node => router.push({ name: 'NodeEdit', params: { name: node.name } });
    const openDeleteConfirm = (name) => {
      nodeToDelete.value = name;
      showDeleteDialog.value = true;
    };
    const confirmDelete = async () => {
      if (!nodeToDelete.value) return;
      const resp = await deleteNodeRequest(nodeToDelete.value);
      if (resp?.status) {
        showDeleteDialog.value = false;
        nodeToDelete.value = '';
        await fetchNodes();
      }
    };
    const getAdyacentValue = (node, key) => {
      const keyMap = { frente: 0, atras: 1, izquierda: 2, derecha: 3 };
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

    return {
      router,
      nodes,
      isLoading,
      error,
      expandedNode,
      adyacentTitle,
      adyacentNA,
      adyacentGroups,
      locationLabel,
      tagsLabel,
      tagsEmpty,
      deleteLabel,
      showDeleteDialog,
      nodeToDelete,
      getStatusColor,
      toggleNode,
      viewImages,
      editNode,
      openDeleteConfirm,
      confirmDelete,
      getAdyacentValue,
      showImageModal,
      modalImageUrl,
      openImageModal,
      closeImageModal,
      modalNodeName,
    };
  },
};
</script>

<style lang="scss" scoped>
@import '@/assets/styles/pages/_node_admin.scss';
</style>
