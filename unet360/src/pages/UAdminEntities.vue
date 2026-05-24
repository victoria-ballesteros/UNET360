<template>
  <div class="entity-admin-container">
    <div v-if="isLoading" class="full-page-loader">
      <ULoader size="60" />
    </div>

    <template v-else>
      <!-- ── Header ── -->
      <div class="entity-admin-header">
        <div class="text-section">
          <p v-if="entity === 'tenants'" class="header-overline">Panel de control</p>
          <h2>{{ title }}</h2>
        </div>
        <div class="admin-entities-buttons">
          <UButton v-if="entity !== 'tenants'" :text="createButtonText" type="contrast-2" @click="goCreate" />
          <UButton text="Volver a nodos"   type="tertiary"   @click="router.push({ name: 'NodeAdmin' })" />
        </div>
      </div>

      <!-- ── Lista ── -->
      <div class="list-section">
        <UAdminList
          :items="items"
          :search-fields="entity === 'tenants' ? ['name', 'email'] : ['name']"
          :show-search="true"
          :show-sort="true"
          :search-placeholder="entity === 'tenants' ? 'Buscar por nombre o email...' : 'Buscar...'"
          :empty-message="`No hay ${entityLabelPlural}.`"
          :no-results-message="`No se encontraron ${entityLabelPlural}.`"
          item-key-field="name"
        >
          <template #item="{ item: it }">
            <div class="item-info">
              <div class="item-primary">
                <span v-if="entity === 'tenants'" class="status-dot" :class="statusClass(it)" />
                <UIcon
                  v-else-if="entity === 'tags' && it.icon_name"
                  :name="`icons/${it.icon_name}`"
                  class="item-left-icon"
                  size="22"
                  :color="'var(--status-green, #4caf50)'"
                />
                <span class="item-name">{{ it.name }}</span>
              </div>

              <div class="item-actions">
                <UButton
                  v-if="entity === 'tags'"
                  icon="icons/edit"
                  type="tertiary"
                  size="md"
                  @click="editItem(it)"
                />
                <UButton
                  v-if="entity === 'tenants'"
                  icon="icons/journal-text"
                  type="tertiary"
                  size="md"
                  @click="openRoleDialog(it)"
                />
                <UButton
                  icon="icons/trash"
                  type="tertiary"
                  size="md"
                  @click="confirmDelete(it)"
                  class="delete-entity-btn"
                />
              </div>
            </div>
          </template>
        </UAdminList>
      </div>

      <!-- ── Modal: eliminar ── -->
      <UBaseModal
        v-model="showDeleteDialog"
        title="Confirmar eliminación"
        size="sm"
        :danger="true"
      >
        <p class="modal-confirm-text">¿Seguro que quieres eliminar {{ entityLabel }} <strong>{{ itemToDelete?.name }}</strong>?</p>
        <template #footer>
          <UButton text="Cancelar" type="tertiary"   @click="showDeleteDialog = false" />
          <UButton text="Eliminar" type="danger"     @click="doDelete" />
        </template>
      </UBaseModal>

      <!-- ── Modal: cambiar rol ── -->
      <UBaseModal
        v-model="showRoleDialog"
        title="Cambiar rol de usuario"
        size="sm"
      >
        <div class="modal-role-body">
          <p class="modal-confirm-text">Usuario: <strong>{{ userForRole?.name }}</strong></p>
          <div class="modal-radio-group">
            <label class="modal-radio-label"><input type="radio" value="viewer" v-model="selectedRole"> Viewer</label>
            <label class="modal-radio-label"><input type="radio" value="admin"  v-model="selectedRole"> Admin</label>
          </div>
        </div>
        <template #footer>
          <UButton text="Cancelar" type="tertiary"   @click="showRoleDialog = false" />
          <UButton text="Guardar"  type="contrast-2" @click="saveRole" />
        </template>
      </UBaseModal>
    </template>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import UButton    from '@/components/UButton.vue';
import UBaseModal from '@/components/UBaseModal.vue';
import UIcon      from '@/components/UIcon.vue';
import ULoader    from '@/components/ULoader.vue';
import UAdminList from '@/components/UAdminList.vue';
import api from '@/axios';

const route  = useRoute();
const router = useRouter();

const entity = computed(() => {
  if (route.name === 'AdminTenants') return 'tenants';
  return route.params.entity || route.meta.entity;
});

const items          = ref([]);
const isLoading      = ref(false);
const showDeleteDialog = ref(false);
const itemToDelete   = ref(null);

// ── Labels ────────────────────────────────────────────────────────────────
const entityLabel      = computed(() => ({ tags: 'tag', tenants: 'usuario', locations: 'location' }[entity.value] ?? entity.value));
const entityLabelPlural = computed(() => ({ tags: 'tags', tenants: 'usuarios', locations: 'locations' }[entity.value] ?? entity.value));
const title            = computed(() => ({ tags: 'ADMINISTRAR TAGS', tenants: 'ADMINISTRAR USUARIOS', locations: 'ADMINISTRAR LOCATIONS' }[entity.value] ?? entity.value));
const createButtonText = computed(() => ({ tags: 'Crear Tag', locations: 'Crear Location' }[entity.value] ?? null));

// ── Fetch ─────────────────────────────────────────────────────────────────
async function fetchItems() {
  isLoading.value = true;
  try {
    const { data } = await api.get(`${entity.value}/`);
    if (data?.status && Array.isArray(data.response_obj)) {
      items.value = data.response_obj;
      if (entity.value === 'tenants') await fetchTenantStatuses();
    } else {
      items.value = [];
    }
  } catch (_) {
    items.value = [];
  } finally {
    isLoading.value = false;
  }
}

async function fetchTenantStatuses() {
  try {
    const { data } = await api.get('tenants/statuses');
    if (data?.status && Array.isArray(data.response_obj)) {
      const map = new Map(data.response_obj.map((u) => [u.name, u.status]));
      items.value = items.value.map((u) => ({ ...u, status: map.get(u.name) }));
    }
  } catch (_) {}
}

// ── Helpers ───────────────────────────────────────────────────────────────
const itemKey     = (it) => entity.value === 'tenants' ? (it.supabase_user_id || it.name) : it.name;
const statusClass = (user) => ({
  'status-ok':   user.status === 'OK',
  'status-warn': user.status === 'WARNING',
  'status-err':  user.status === 'ERROR',
});

// ── Navegación ────────────────────────────────────────────────────────────
const goCreate  = () => router.push({ name: 'EntityEdit', params: { entity: entity.value } });
const editItem  = (it) => router.push({ name: 'EntityEdit', params: { entity: entity.value, name: it.name } });

// ── Borrado ───────────────────────────────────────────────────────────────
function confirmDelete(it) {
  itemToDelete.value    = it;
  showDeleteDialog.value = true;
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
  itemToDelete.value     = null;
}

// ── Rol (tenants) ─────────────────────────────────────────────────────────
const showRoleDialog = ref(false);
const userForRole    = ref(null);
const selectedRole   = ref('viewer');

function openRoleDialog(user) {
  userForRole.value    = user;
  selectedRole.value   = user.role || 'viewer';
  showRoleDialog.value = true;
}

async function saveRole() {
  if (!userForRole.value) return;
  try {
    const id = userForRole.value.supabase_user_id;
    if (!id) return;
    const { data } = await api.patch(`tenants/${encodeURIComponent(id)}`, { role: selectedRole.value });
    if (data?.status) {
      items.value      = items.value.map(u => (itemKey(u) === id ? { ...u, role: selectedRole.value } : u));
      showRoleDialog.value = false;
      userForRole.value    = null;
    }
  } catch (e) { console.error(e?.response?.data || e); }
}

// ── Ciclo de vida ─────────────────────────────────────────────────────────
onMounted(fetchItems);
watch(entity, fetchItems);
</script>

<style lang="scss" scoped>
@import '@/assets/styles/pages/_entity_admin.scss';
</style>