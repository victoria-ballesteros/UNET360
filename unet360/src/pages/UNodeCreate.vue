<template>
  <div class="create-container">

    <!-- dot-grid + vignette -->
    <div class="bg-grid" />
    <div class="bg-noise" />

    <!-- ── HEADER ── -->
    <div class="page-header">
      <h1 class="page-title">Crear <em>nuevo nodo</em></h1>
      <p class="page-sub">Sube un archivo ZIP con las teselas y define la metadata del nodo.</p>
    </div>

    <!-- ── MAIN CARD ── -->
    <div class="card">

      <!-- left: upload zone / zip status -->
      <div class="card-viewer">
        <div v-if="isUploading" class="zip-uploading-state">
          <ULoader :progress="uploadProgress" title="Subiendo teselas" description="Procesando archivo ZIP..."
            size="medium" />
        </div>

        <div v-else-if="!isImageLoaded" class="upload-zone" @click="openUploadFileDialog">
          <div class="upload-icon-wrap">
            <UIcon name="icons/cloud-upload" size="28" color="var(--main-yellow)" />
          </div>
          <p class="upload-label">Haz clic para subir las teselas de la imagen 360°</p>
          <p class="upload-hint">FORMATO ZIP EXCLUSIVAMENTE</p>
        </div>

        <div v-else class="zip-loaded-state">
          <div class="zip-icon-wrapper">
            <UIcon name="icons/sphere" size="48" color="var(--main-yellow)" />
          </div>
          <div class="zip-info">
            <p class="zip-name">{{ imageFile?.name }}</p>
            <p class="zip-size">{{ formatFileSize(imageFile?.size) }}</p>
          </div>
          <button class="change-zip-btn" @click="openUploadFileDialog">
            <UIcon name="icons/edit" size="16" color="var(--main-yellow)" />
            Cambiar ZIP
          </button>
        </div>

        <input type="file" accept=".zip" ref="fileInput" style="display:none" @change="handleFileChange" />
      </div>

      <div class="card-form-wrapper">
        <div class="card-form">
          <!-- Identificación con tags inline -->
          <div class="identification-section">
            <p class="form-section-label">Identificación</p>

            <div class="id-tags-row">
              <div class="id-input-wrapper" :class="{ 'has-error': inputErrors['Identificación'] }">
                <p class="input-label">Id. del nodo</p>
                <UInput v-model="inputModels['Identificación']" styleType="dark" placeholder="Ej: 003" icon="arrow-up"
                  @update:modelValue="() => {
                    inputTouched['Identificación'] = true;
                  }" />
                <p v-if="inputErrors['Identificación']" class="error-msg">
                  {{ inputErrors['Identificación'] }}
                </p>
              </div>
            </div>
          </div>

          <div class="divider" />

          <p class="form-section-label">Conexiones</p>

          <!-- Nodos adyacentes en grid 2x2 -->
          <div class="connections-grid">
            <div v-for="(label, index) in adjacentLabels" :key="label" class="input-wrapper"
              :class="{ 'has-error': inputErrors[label] }">
              <p class="input-label">{{ label }}</p>
              <div class="adjacent-row">
                <UInput v-model="inputModels[label]" styleType="dark" :placeholder="inputPlaceholders[label]"
                  icon="arrow-up" :iconRotation="index * 90" @update:modelValue="() => {
                    inputTouched[label] = true;
                  }" />

                <UInput v-model="inputWeightModels[label]" styleType="dark" placeholder="Peso" @update:modelValue="(value) => {
                  inputTouched[label] = true;
                  inputWeightModels[label] = value
                    ?.replace(',', '.')
                    ?.replace(/[^0-9.]/g, '');
                }" />
              </div>
              <p v-if="inputErrors[label]" class="error-msg">{{ inputErrors[label] }}</p>
            </div>
          </div>

          <div class="divider" />

          <!-- Ubicación -->
          <p class="form-section-label">Ubicación</p>
          <div class="input-wrapper">
            <p class="input-label">Ubicación del nodo</p>
            <USelect v-model="selectedLocation" :options="locationOptions" styleType="dark"
              placeholder="Selecciona una ubicación" />
          </div>

          <div class="divider" />

          <!-- Minimapa -->
          <p class="form-section-label">Minimapa</p>
          <div class="input-wrapper">
            <p class="input-label">Nombre del minimapa</p>
            <USelect v-model="selectedMinimap" :options="MINIMAP_OPTIONS" styleType="dark"
              placeholder="Selecciona un minimapa" />
          </div>
          <div class="adjacent-row">
            <div class="input-wrapper" style="flex: 1">
              <p class="input-label">Coordenada X</p>
              <UInput v-model="minimapX" styleType="dark" placeholder="Ej: 120"
                @update:modelValue="(v) => { minimapX = v?.replace(/[^0-9-]/g, ''); }" />
            </div>
            <div class="input-wrapper" style="flex: 1">
              <p class="input-label">Coordenada Y</p>
              <UInput v-model="minimapY" styleType="dark" placeholder="Ej: 240"
                @update:modelValue="(v) => { minimapY = v?.replace(/[^0-9-]/g, ''); }" />
            </div>
          </div>
        </div>

        <!-- Footer de la card: botones de acción -->
        <div class="form-actions">
          <UButton text="Cancelar"   type="tertiary"    @click="handleCancelEvent" />
          <UButton text="Crear nodo" :type="buttonType" @click.stop="handleFormSubmit" />
        </div>
      </div>
    </div>
  </div>

  <!-- Modal: identificación del tag -->
  <UBaseModal v-model="showDialog" title="Identificación del tag" size="sm">
    <div class="tag-dialog-content">
      <div v-for="(_, index) in tagCustomNames[actualTagSelected]" :key="index" class="tag-name-row">
        <UInput v-model="tagCustomNames[actualTagSelected][index]" styleType="dark" placeholder="Baño oeste" />
        <button v-if="tagCustomNames[actualTagSelected].length > 1" class="tag-remove-btn"
          @click="removeTagName(index)">
          <UIcon name="icons/close" size="14" color="currentColor" />
        </button>
      </div>

      <button class="tag-add-btn" @click="addTagName">
        <UIcon name="icons/plus" size="14" color="var(--main-yellow)" />
        Agregar otro
      </button>
    </div>
    <template #footer>
      <UButton text="Aceptar" @click="handleTagCustomization" :type="dialogButtonType" />
    </template>
  </UBaseModal>

  <!-- Modal: resultado de creación -->
  <UResultDialog
    v-model="showResultDialog"
    :success="resultSuccess"
    :title="resultTitle"
    :message="resultMessage"
    primary-btn-text="Ver nodos"
    secondary-btn-text="Crear Nuevo Nodo"
    @primary-click="navigateToNodes"
    @secondary-click="startNewNode"
  />
</template>
<script setup>
import {
  ref, computed, reactive, watch, nextTick, onMounted,
} from 'vue';
import UButton from '@/components/UButton.vue';
import UInput from '@/components/UInput.vue';
import USelect from '@/components/USelect.vue';
import UIcon from '@/components/UIcon.vue';
import UBaseModal    from '@/components/UBaseModal.vue';
import UResultDialog from '@/components/UResultDialog.vue';
import ULoader from '@/components/ULoader.vue';

import { useNodeStore } from '../service/stores/nodes';
import { useTagStore } from '@/service/stores/tags';
import { obtainData } from '../service/shared/utils';
import { createNode, uploadTilesToServer, getLocations } from '@/service/requests/requests';
import { useRouter } from 'vue-router';

import { formatFileSize } from '@/service/shared/utils';

const router = useRouter();

// ═══════════════  Stores  ═══════════════
const nodeStore = useNodeStore();
const tagStore = useTagStore();
const nodes = computed(() => nodeStore.nodes);
const tags = computed(() => tagStore.tags);

// ═══════════════  UI state  ═══════════════
const isUploading = ref(false);
const uploadProgress = ref(0);
const buttonType = ref('deactivated');
const showDialog = ref(false);
const actualTagSelected = ref('');
const dialogButtonType = ref('deactivated');
const showResultDialog = ref(false);
const resultSuccess = ref(false);
const resultTitle = ref('');
const resultMessage = ref('');

// ═══════════════  ZIP upload  ═══════════════
const isImageLoaded = ref(false);
const imageFile = ref(null);

// ═══════════════  Form — Identificación  ═══════════════
const inputModels = reactive({});
const inputWeightModels = reactive({});
const inputErrors = reactive({});
const inputTouched = reactive({});

// Labels separados: adyacentes + identificación
const adjacentLabels = reactive([
  'Nodo siguiente',
  'Nodo derecho',
  'Nodo anterior',
  'Nodo izquierdo',
]);
const allLabels = [...adjacentLabels, 'Identificación'];
const inputPlaceholders = {};

allLabels.forEach((label) => {
  inputPlaceholders[label] = label === 'Identificación'
    ? 'Identificación del nodo actual'
    : `Id. del ${label.toLowerCase()}`;
  inputModels[label] = '';
  inputWeightModels[label] = '';
  inputErrors[label] = '';
  inputTouched[label] = false;
});

// ─── Validación de Identificación ───
watch(
  () => inputModels['Identificación'],
  (newVal) => {
    if (!inputTouched['Identificación'] && !newVal) return;
    const trimmed = newVal?.trim();
    let err = '';
    if (!trimmed) {
      err = 'La identificación es obligatoria';
    } else if (trimmed.length < 3) {
      err = 'La identificación debe tener al menos 3 caracteres';
    } else if (!/^\d+(-[a-zA-Z0-9]+)*$/.test(trimmed)) {
      err = 'Formato inválido. Ej: 003-HallA';
    } else if (nodes.value.some((node) => node.name === trimmed)) {
      err = 'El nodo ya existe';
    }
    inputErrors['Identificación'] = err;
    checkIfReadyToSubmit();
  },
);

// ─── Validación de nodos adyacentes ───
adjacentLabels.forEach((label, index) => {
  watch(
    [() => inputModels[label], () => inputWeightModels[label]],
    ([newVal, newWeight]) => {
      if (!inputTouched[label] && !newVal && !newWeight) return;
      inputErrors[label] = '';
      if (!newWeight?.toString().trim() && newVal?.trim()) {
        inputErrors[label] = 'El peso no puede estar vacío';
      } else if (newWeight?.toString().trim() && !newVal?.trim()) {
        inputErrors[label] = 'Peso asignado a una arista incompleta';
      }
      checkIfReadyToSubmit();
    },
    { immediate: true },
  );
});

function checkIfReadyToSubmit() {
  const noErrors = Object.values(inputErrors).every((e) => e === '');
  const hasId = inputModels['Identificación']?.trim().length >= 3;
  buttonType.value = (noErrors && imageFile.value && hasId) ? 'primary' : 'deactivated';
}

// ═══════════════  Image upload  ═══════════════
const fileInput = ref(null);
function openUploadFileDialog() { fileInput.value?.click(); }

async function handleFileChange(event) {
  const file = event.target.files[0];
  if (!file || (!file.name.endsWith('.zip') && file.type !== 'application/zip')) {
    resultSuccess.value = false;
    resultTitle.value = 'Formato incorrecto';
    resultMessage.value = 'Por favor, selecciona un archivo ZIP válido.';
    showResultDialog.value = true;
    return;
  }

  imageFile.value = file;

  isImageLoaded.value = true;
  checkIfReadyToSubmit();
}

// ═══════════════  Submit  ═══════════════
async function handleFormSubmit() {
  if (buttonType.value === 'deactivated') return;

  isUploading.value = true;
  uploadProgress.value = 0;

  let uploadTilesResponse = null;
  try {
    uploadTilesResponse = await uploadTilesToServer(imageFile.value, (progress) => {
      uploadProgress.value = progress;
    });
  } catch (error) {
    console.error('Error uploading tiles:', error);
  }

  if (!uploadTilesResponse?.status) {
    isUploading.value = false;
    uploadProgress.value = 0;
    resultSuccess.value = false;
    resultTitle.value = 'Error al subir teselas';
    resultMessage.value = uploadTilesResponse?.response_obj?.message || 'No se pudo subir el archivo ZIP de teselas.';
    showResultDialog.value = true;
    return;
  }

  // Construir datos del nodo
  const adjacentNodes = adjacentLabels.map((label) => {
    const name = inputModels[label];
    const weight = parseFloat(inputWeightModels[label]);
    return (name && !isNaN(weight)) ? { [name]: weight } : null;
  });

  const tagDict = {};
  for (const tag of tagStore.tags) {
    if (tagSelection[tag.name]) {
      const names = tagCustomNames[tag.name].filter((n) => n.trim());
      if (names.length > 0) {
        tagDict[tag.name] = Object.fromEntries(names.map((n) => [n, 0.0]));
      }
    }
  }

  const nodeData = {
    name: inputModels['Identificación'],
    location: selectedLocation.value || null,
    minimap: (selectedMinimap.value || minimapX.value !== '' || minimapY.value !== '')
      ? {
        image: selectedMinimap.value || null,
        x: minimapX.value !== '' ? parseInt(minimapX.value, 10) : null,
        y: minimapY.value !== '' ? parseInt(minimapY.value, 10) : null,
      }
      : null,
    tiles_path: uploadTilesResponse?.response_obj?.path,
    adjacent_nodes: adjacentNodes,
    tags: tagDict,
  };

  try {
    const createResp = await createNode(nodeData);
    isUploading.value = false;
    uploadProgress.value = 0;

    if (createResp?.status) {
      resultSuccess.value = true;
      resultTitle.value = '¡Nodo creado con éxito!';
      resultMessage.value = `Se creó el nodo "${nodeData.name}" correctamente.`;
    } else {
      resultSuccess.value = false;
      resultTitle.value = 'Error al crear nodo';
      resultMessage.value = createResp?.response_obj?.message || 'No se pudo crear el nodo.';
    }
  } catch (e) {
    isUploading.value = false;
    uploadProgress.value = 0;
    resultSuccess.value = false;
    resultTitle.value = 'Error inesperado';
    resultMessage.value = String(e);
  }
  showResultDialog.value = true;
}

// ═══════════════  Ubicación  ═══════════════
const locationOptions = ref([]);
const selectedLocation = ref('');

async function fetchLocations() {
  try {
    const resp = await getLocations();
    if (resp?.status && Array.isArray(resp.response_obj)) {
      locationOptions.value = resp.response_obj.map((loc) => loc.name);
    }
  } catch (e) {
    console.error('Error al obtener ubicaciones:', e);
  }
}

// ═══════════════  Minimapa  ═══════════════
const MINIMAP_OPTIONS = [
  'map-A1.jpg',
  'map-A2.jpg',
  'map-A3.jpg',
  'map-A4.jpg',
  'map-C1.jpg',
];

const selectedMinimap = ref('');
const minimapX = ref('');
const minimapY = ref('');

// ═══════════════  Tags  ═══════════════
const tagSelection = reactive({});
// Ahora cada tag tiene un array de nombres en lugar de uno solo
const tagCustomNames = reactive({});

watch(tags, (newTags) => {
  if (Array.isArray(newTags)) {
    newTags.forEach((tag) => {
      tagSelection[tag.name] = false;
      tagCustomNames[tag.name] = [''];
    });
  }
}, { immediate: true });

function dialogHasValue() {
  return tagCustomNames[actualTagSelected.value]?.some((n) => n.trim());
}

function addTagName() {
  tagCustomNames[actualTagSelected.value].push('');
}

function removeTagName(index) {
  tagCustomNames[actualTagSelected.value].splice(index, 1);
  dialogButtonType.value = dialogHasValue() ? 'primary' : 'deactivated';
}

const tagSubmited = ref(false);
async function handleTagCustomization() {
  tagSubmited.value = true;
  showDialog.value = false;
  // Limpiar entradas vacías; si no queda ninguna, deseleccionar el tag
  const cleaned = tagCustomNames[actualTagSelected.value].filter((n) => n.trim());
  if (cleaned.length === 0) {
    tagSelection[actualTagSelected.value] = false;
    tagCustomNames[actualTagSelected.value] = [''];
  } else {
    tagCustomNames[actualTagSelected.value] = cleaned;
  }
  await nextTick();
  tagSubmited.value = false;
}

watch(showDialog, (newVal) => {
  if (!newVal && !tagSubmited.value) {
    tagSelection[actualTagSelected.value] = false;
    tagCustomNames[actualTagSelected.value] = [''];
    tagSubmited.value = false;
  }
});

// ═══════════════  Lifecycle  ═══════════════
function handleCancelEvent() { router.push({ name: 'NodeAdmin' }); }
function navigateToNodes() { showResultDialog.value = false; router.push({ name: 'NodeAdmin' }); }
function startNewNode() { showResultDialog.value = false; router.replace({ name: 'NodeCreate' }); }

onMounted(async () => {
  router.isReady().then(() => obtainData());
  fetchLocations();
});
</script>

<style scoped lang="scss">
@import '@/assets/styles/_colors.scss';
@import '@/assets/styles/_typography.scss';
@import '@/assets/styles/pages/_node_create.scss';

.tag-name-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;

  &> :first-child {
    flex: 1;
  }
}

.tag-remove-btn {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: 1px solid rgba(0, 0, 0, 0.12);
  background: transparent;
  color: var(--border-gray);
  cursor: pointer;
  transition: background 0.15s ease, color 0.15s ease, border-color 0.15s ease;

  &:hover {
    background: rgba(229, 57, 53, 0.08);
    color: var(--status-red, #e53935);
    border-color: rgba(229, 57, 53, 0.3);
  }
}

.tag-add-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  align-self: flex-start;
  padding: 0.375rem 0.75rem;
  border-radius: 8px;
  border: 1px dashed rgba(255, 239, 61, 0.4);
  background: transparent;
  color: var(--main-yellow);
  cursor: pointer;
  font-size: 0.8rem;
  transition: background 0.15s ease, border-color 0.15s ease;

  &:hover {
    background: rgba(255, 239, 61, 0.07);
    border-color: rgba(255, 239, 61, 0.7);
  }
}
</style>