<template>
  <div class="entity-admin-container">
    <div class="text-section">
        <h2>{{ title }}</h2>
    </div>
    <div class="admin-entities-buttons">
        <UButton :text="createButtonText" type="contrast-2" @click="goCreate" />
        <UButton text="Volver a nodos" type="tertiary" @click="router.push({ name: 'NodeAdmin' })" />
    </div>

    <div class="list-section">
      <div v-if="isLoading" class="empty-message">Cargando...</div>
      <div v-else>
        <div v-if="items.length === 0" class="empty-message">No hay {{ entityLabelPlural }}.</div>
        <div v-else>
          <div class="item-list-section">
            <div v-for="(it,index) in items" :key="it.name" class="item">
              <div class="item-info">
                <div class="item-primary">
                    <UIcon
                    v-if="entity === 'tags' && it.icon_name"
                    :name="`icons/${it.icon_name}`"
                    class="item-left-icon"
                    :color="'var(--status-green, #4caf50)'"
                    />
                    <span class="item-name">{{ it.name }}</span>
                </div>
                <div class="item-actions">
                    <button v-if="entity === 'tags'" class="icon-btn" @click="editItem(it)">
                    <UIcon name="icons/edit" class="entity-action-icon" />
                    </button>
                    <button class="icon-btn" @click="confirmDelete(it)">
                    <UIcon name="icons/trash" class="entity-action-icon" />
                    </button>
                </div>
              </div>
              
              <div v-if="index !== items.length - 1" class="separator"></div>
            </div>
            
          </div>
        </div>
      </div>
    </div>



    <UDialog v-model="showDeleteDialog" :headerTitle="''">
      <div class="delete-dialog-content">
        <div class="delete-dialog-header">¿Eliminar {{ entityLabel }} {{ itemToDelete?.name }}?</div>
        <div class="delete-dialog-actions">
          <UButton text="Cancelar" type="tertiary" @click="showDeleteDialog = false" />
          <UButton text="Eliminar" type="danger" @click="doDelete" />
        </div>
      </div>
    </UDialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import UButton from '@/components/UButton.vue';
import UDialog from '@/components/UDialog.vue';
import UIcon from '@/components/UIcon.vue';
import api from '@/axios';

const route = useRoute();
const router = useRouter();
const entity = computed(() => route.params.entity); // 'tags' or 'locations'

const items = ref([]);
const isLoading = ref(false);
const showDeleteDialog = ref(false);
const itemToDelete = ref(null);

const entityLabel = computed(() => entity.value === 'tags' ? 'tag' : 'location');
const entityLabelPlural = computed(() => entity.value === 'tags' ? 'tags' : 'locations');
const title = computed(() => entity.value === 'tags' ? 'ADMINISTRAR TAGS' : 'ADMINISTRAR LOCATIONS');
const createButtonText = computed(() => entity.value === 'tags' ? 'Crear Tag' : 'Crear Location');

async function fetchItems() {
  isLoading.value = true;
  try {
    const { data } = await api.get(`${entity.value}/`);
    if (data?.status && Array.isArray(data.response_obj)) {
      items.value = data.response_obj;
    } else {
      items.value = [];
    }
  } catch (_) {
    items.value = [];
  } finally {
    isLoading.value = false;
  }
}

function goCreate() {
  router.push({ name: 'EntityEdit', params: { entity: entity.value } });
}

function editItem(it) {
  router.push({ name: 'EntityEdit', params: { entity: entity.value, name: it.name } });
}

function confirmDelete(it) {
  itemToDelete.value = it;
  showDeleteDialog.value = true;
}

async function doDelete() {
  if (!itemToDelete.value) return;
  try {
    const { data } = await api.delete(`${entity.value}/${encodeURIComponent(itemToDelete.value.name)}`);
    if (data?.status) {
      items.value = items.value.filter(i => i.name !== itemToDelete.value.name);
    }
  } catch (_) { /* ignore */ }
  showDeleteDialog.value = false;
  itemToDelete.value = null;
}

onMounted(fetchItems);
watch(entity, fetchItems);
</script>

<style lang="scss" scoped>
@import '@/assets/styles/pages/_entity_admin.scss';
</style>
