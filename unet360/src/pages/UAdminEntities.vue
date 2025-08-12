<template>
  <div class="entity-admin-container">
    <div class="text-section">
        <h2>{{ title }}</h2>
    </div>
  <div v-if="entity !== 'tenants'" class="admin-entities-buttons">
        <UButton :text="createButtonText" type="contrast-2" @click="goCreate" />
        <UButton text="Volver a nodos" type="tertiary" @click="router.push({ name: 'NodeAdmin' })" />
    </div>

    <div class="list-section">
      <div v-if="isLoading" class="empty-message">Cargando...</div>
      <div v-else>
        <div v-if="items.length === 0" class="empty-message">No hay {{ entityLabelPlural }}.</div>
        <div v-else>
          <div class="item-list-section">
      <div v-for="(it,index) in items" :key="itemKey(it)" class="item">
              <div class="item-info">
                <div class="item-primary">
        <span v-if="entity === 'tenants'" class="status-dot" :class="statusClass(it)"></span>
        <UIcon
        v-else-if="entity === 'tags' && it.icon_name"
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
        <button v-if="entity === 'tenants'" class="icon-btn" @click="openRoleDialog(it)">
        <UIcon name="icons/journal-text" class="entity-action-icon" :color="'var(--full-white)'" />
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
    <UDialog v-model="showRoleDialog" :headerTitle="' '">
      <div class="delete-dialog-content">
        <div class="delete-dialog-header">Usuario: {{ userForRole?.name }}</div>
        <div style="display:flex; gap:.5rem; align-items:center;">
          <label>
            <input type="radio" value="viewer" v-model="selectedRole"> Viewer
          </label>
          <label>
            <input type="radio" value="admin" v-model="selectedRole"> Admin
          </label>
        </div>
        <div class="delete-dialog-actions">
          <UButton text="Cancelar" type="tertiary" @click="showRoleDialog = false" />
          <UButton text="Guardar" type="contrast-2" @click="saveRole" />
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
const entity = computed(() => {
  if (route.name === 'AdminTenants') return 'tenants';
  return route.params.entity || route.meta.entity;
}); // 'tags' | 'locations' | 'tenants'
const items = ref([]);
const isLoading = ref(false);
const showDeleteDialog = ref(false);
const itemToDelete = ref(null);

const entityLabel = computed(() => entity.value === 'tags' ? 'tag' : (entity.value === 'tenants' ? 'usuario' : 'location'));
const entityLabelPlural = computed(() => entity.value === 'tags' ? 'tags' : (entity.value === 'tenants' ? 'usuarios' : 'locations'));
const title = computed(() => entity.value === 'tags' ? 'ADMINISTRAR TAGS' : (entity.value === 'tenants' ? 'ADMINISTRAR USUARIOS' : 'ADMINISTRAR LOCATIONS'));
const createButtonText = computed(() => entity.value === 'tags' ? 'Crear Tag' : (entity.value === 'tenants' ? null : 'Crear Location'));

async function fetchItems() {
  isLoading.value = true;
  try {
    const { data } = await api.get(`${entity.value}/`);
    if (data?.status && Array.isArray(data.response_obj)) {
      items.value = data.response_obj;
      // If tenants, also fetch their statuses from backend
      if (entity.value === 'tenants') {
        await fetchTenantStatuses();
      }
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

// Helpers para tenants
function itemKey(it) { return entity.value === 'tenants' ? (it.supabase_user_id || it.name) : it.name; }
function statusClass(user) {
  const status = user.status; // 'OK' | 'WARNING' | 'ERROR' | undefined
  return { 'status-ok': status === 'OK', 'status-warn': status === 'WARNING', 'status-err': status === 'ERROR' };
}

async function fetchTenantStatuses() {
  try {
    const { data } = await api.get('tenants/statuses');
    if (data?.status && Array.isArray(data.response_obj)) {
      const map = new Map(data.response_obj.map((u) => [u.name, u.status]));
      items.value = items.value.map((u) => ({ ...u, status: map.get(u.name) }));
    }
  } catch (_) { /* ignore */}
}

const showRoleDialog = ref(false);
const userForRole = ref(null);
const selectedRole = ref('viewer');

function openRoleDialog(user) {
  userForRole.value = user;
  selectedRole.value = user.role || 'viewer';
  showRoleDialog.value = true;
}

async function saveRole() {
  if (!userForRole.value) return;
  try {
    const id = userForRole.value.supabase_user_id;
    if (!id) return;
    const { data } = await api.patch(`tenants/${encodeURIComponent(id)}`, { role: selectedRole.value });
    if (data?.status) {
      items.value = items.value.map(u => (itemKey(u) === id ? { ...u, role: selectedRole.value } : u));
      showRoleDialog.value = false;
      userForRole.value = null;
    }
  } catch (e) { console.error(e?.response?.data || e); }
}

async function doDelete() {
  if (!itemToDelete.value) return;
  try {
    const key = entity.value === 'tenants' ? itemToDelete.value.supabase_user_id : itemToDelete.value.name;
    if (entity.value === 'tenants' && !key) return;
    const { data } = await api.delete(`${entity.value}/${encodeURIComponent(key)}`);
    if (data?.status) {
      items.value = items.value.filter(i => itemKey(i) !== key);
    }
  } catch (e) { console.error(e?.response?.data || e); }
  showDeleteDialog.value = false;
  itemToDelete.value = null;
}

onMounted(fetchItems);
watch(entity, fetchItems);
</script>

<style lang="scss" scoped>
@import '@/assets/styles/pages/_entity_admin.scss';
</style>
