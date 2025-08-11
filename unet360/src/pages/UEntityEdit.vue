<template>
  <div class="form-container">
    <div class="text-section">
      <p class="upper-paragrah">{{ isEdit ? ('Editar ' + entityLabelCap + ': ' + originalName) : ('Crear ' + entityLabelCap) }}</p>
      <p class="lower-paragraph" v-if="entity === 'tags'">{{ isEdit ? 'Actualiza los datos del tag.' : 'Registra un nuevo tag.' }}</p>
      <p class="lower-paragraph" v-else>{{ isEdit ? 'Actualiza la location.' : 'Registra una nueva location.' }}</p>
    </div>

    <div class="form-section">
      <div class="input-container">
        <p class="input-label">Nombre</p>
        <UInput v-model="form.name" styleType="default" :placeholder="'Nombre de ' + entityLabel" :disabled="isEdit" />
      </div>

      <div v-if="entity === 'tags'" class="input-container">
        <p class="input-label">Icon name (opcional)</p>
        <UInput v-model="form.icon_name" styleType="default" placeholder="icon-name" />
      </div>

      <div class="button-container">
        <UButton text="Cancelar" type="tertiary" @click="goBack" />
        <UButton :text="isEdit ? 'Guardar cambios' : 'Crear'" type="contrast-2" @click="submit" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import UInput from '@/components/UInput.vue';
import UButton from '@/components/UButton.vue';
import api from '@/axios';

const route = useRoute();
const router = useRouter();

const entity = computed(() => route.params.entity); // 'tags' or 'locations'
const nameParam = computed(() => route.params.name || null);
const isEdit = computed(() => !!nameParam.value);

const form = reactive({
  name: '',
  icon_name: ''
});
const originalName = computed(() => nameParam.value || form.name);

const entityLabel = computed(() => entity.value === 'tags' ? 'tag' : 'location');
const entityLabelCap = computed(() => entityLabel.value.charAt(0).toUpperCase() + entityLabel.value.slice(1));

async function loadItem() {
  if (!isEdit.value) return;
  try {
    const { data } = await api.get(`${entity.value}/${encodeURIComponent(nameParam.value)}`);
    if (data?.status && data.response_obj) {
      form.name = data.response_obj.name || '';
      if (entity.value === 'tags') {
        form.icon_name = data.response_obj.icon_name || '';
      }
    }
  } catch (_) { /* ignore */ }
}

function goBack() {
  router.push({ name: 'AdminEntities', params: { entity: entity.value } });
}

async function submit() {
  try {
    if (isEdit.value) {
      const payload = entity.value === 'tags' ? { icon_name: form.icon_name } : { name: form.name };
      const { data } = await api.patch(`${entity.value}/${encodeURIComponent(originalName.value)}`, payload);
      if (data?.status) goBack();
    } else {
      const payload = entity.value === 'tags' ? { name: form.name, icon_name: form.icon_name || null } : { name: form.name };
      const { data } = await api.post(`${entity.value}/`, payload);
      if (data?.status) goBack();
    }
  } catch (_) { /* ignore */ }
}

onMounted(loadItem);
</script>

<style lang="scss">
@import '@/assets/styles/pages/_entity_edit.scss';
</style>
