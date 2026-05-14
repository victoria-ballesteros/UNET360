<template>
  <!-- Loading bar -->
  <div v-if="isUploading" class="loading-bar-container">
    <div class="loading-bar" />
  </div>

  <div class="create-container">

    <!-- dot-grid + vignette (igual que UAbout hero) -->
    <div class="bg-grid" />
    <div class="bg-noise" />

    <!-- ── HEADER ── -->
    <div class="page-header">
      <span class="overline">
        <span class="eyebrow-dot" />
        Administración de nodos
      </span>
      <h1 class="page-title">Crear <em>nuevo nodo</em></h1>
      <p class="page-sub">Sube una imagen 360° y define la metadata del nodo.</p>
    </div>

    <!-- ── MAIN CARD ── -->
    <div class="card">

      <!-- left: visor / upload zone -->
      <div class="card-viewer">
        <transition name="fade-panorama">
          <div v-show="isImageLoaded" ref="viewerContainer" class="panorama-viewer" />
        </transition>

        <div v-if="!isImageLoaded" class="upload-zone" @click="openUploadFileDialog">
          <div class="upload-icon-wrap">
            <UIcon name="icons/cloud-upload" size="28" color="var(--main-yellow)" />
          </div>
          <p class="upload-label">Haz clic para subir las teselas de la imagen 360°</p>
          <p class="upload-hint">FORMATO ZIP EXCLUSIVAMENTE</p>
        </div>

        <button v-if="isImageLoaded" class="change-image-btn" @click="openUploadFileDialog">
          <UIcon name="icons/cloud-upload" size="16" color="var(--main-yellow)" />
          Cambiar imagen
        </button>

        <input type="file" accept="image/*" ref="fileInput" style="display:none" @change="handleFileChange" />
      </div>

      <!-- right: form -->
      <div class="card-form">
        <p class="form-section-label">Identificación</p>

        <!-- ID del nodo -->
        <div class="input-wrapper" :class="{ 'has-error': inputErrors['Identificación'] }">
          <p class="input-label">Id. del nodo</p>
          <UInput v-model="inputModels['Identificación']" styleType="default" placeholder="Ej: 003"
            icon="arrow-up" @update:modelValue="() => {
              inputTouched['Identificación'] = true;
            }" />
          <p v-if="inputErrors['Identificación']" class="error-msg">
            {{ inputErrors['Identificación'] }}
          </p>
        </div>

        <div class="divider" />

        <p class="form-section-label">Conexiones</p>

        <!-- Nodos adyacentes -->
        <div v-for="(label, index) in adjacentLabels" :key="label" class="input-wrapper"
          :class="{ 'has-error': inputErrors[label] }">
          <p class="input-label">{{ label }}</p>
          <div class="adjacent-row">
            <UInput v-model="inputModels[label]" styleType="default" :placeholder="inputPlaceholders[label]"
              icon="arrow-up" :iconRotation="index * 90" @update:modelValue="() => {
                inputTouched[label] = true;
              }" />

            <UInput v-model="inputWeightModels[label]" styleType="default" placeholder="Peso" @update:modelValue="(value) => {
              inputTouched[label] = true;

              inputWeightModels[label] = value
                ?.replace(',', '.')
                ?.replace(/[^0-9.]/g, '');
            }" />
          </div>
          <p v-if="inputErrors[label]" class="error-msg">{{ inputErrors[label] }}</p>
        </div>

        <div class="divider" />

        <!-- Tags opcionales -->
        <div class="input-wrapper">
          <p class="form-section-label">Tags opcionales</p>
          <div class="tag-row">
            <UIcon v-for="(tag, i) in tags" :key="i" :name="'icons/' + tag.icon_name" size="34"
              :color="tagSelection[tag.name] ? 'var(--main-yellow)' : 'var(--border-gray)'"
              @click="handleTagClick(tag.name)" />
          </div>
        </div>

        <!-- Buttons -->
        <div class="form-actions">
          <UButton text="Cancelar" type="tertiary" @click="handleCancelEvent" />
          <UButton text="Crear nodo" :type="buttonType" @click.stop="handleFormSubmit" />
        </div>
      </div>
    </div>
  </div>

  <!-- Dialog: nombre de tag -->
  <UDialog v-model="showDialog" headerTitle="Identificación del tag">
    <div class="tag-dialog-content">
      <UInput v-model="tagCustomName[actualTagSelected]" styleType="default" placeholder="Baño oeste" />
      <UButton style="align-self:flex-end" text="Aceptar" @click="handleTagCustomization" :type="dialogButtonType" />
    </div>
  </UDialog>

  <!-- Dialog: resultado -->
  <UDialog v-model="showResultDialog" :headerTitle="''">
    <div class="result-dialog">
      <div class="result-icon">
        <UIcon :name="resultSuccess ? 'icons/check-square-fill' : 'icons/close-session'" size="48"
          :color="resultSuccess ? 'var(--status-green, #4caf50)' : 'var(--status-red, #e53935)'" />
      </div>
      <div class="result-text">
        <p class="upper-paragraph">{{ resultTitle }}</p>
        <p class="lower-paragraph">{{ resultMessage }}</p>
      </div>
      <div class="result-actions">
        <UButton text="Ver nodos" type="contrast-2" @click="navigateToNodes" />
        <UButton text="Crear Nuevo Nodo" type="contrast-2" @click="startNewNode" />
      </div>
    </div>
  </UDialog>
</template>

<script setup>
import {
  ref, computed, reactive, watch, nextTick, onMounted, onBeforeUnmount,
} from 'vue';
import UButton from '@/components/UButton.vue';
import UInput from '@/components/UInput.vue';
import UIcon from '@/components/UIcon.vue';
import UDialog from '@/components/UDialog.vue';

import { useNodeStore } from '../service/stores/nodes';
import { useTagStore } from '@/service/stores/tags';
import { obtainData } from '../service/shared/utils';
import { uploadImageToServer, createNode } from '@/service/requests/requests';
import { useRouter } from 'vue-router';
import { Viewer } from '@photo-sphere-viewer/core';
import '@photo-sphere-viewer/core/index.css';

const router = useRouter();

// ═══════════════  Stores  ═══════════════
const nodeStore = useNodeStore();
const tagStore = useTagStore();
const nodes = computed(() => nodeStore.nodes);
const tags = computed(() => tagStore.tags);

// ═══════════════  UI state  ═══════════════
const isUploading = ref(false);
const buttonType = ref('deactivated');
const showDialog = ref(false);
const actualTagSelected = ref('');
const dialogButtonType = ref('deactivated');
const showResultDialog = ref(false);
const resultSuccess = ref(false);
const resultTitle = ref('');
const resultMessage = ref('');

// ═══════════════  360 viewer  ═══════════════
const viewerContainer = ref(null);
const isImageLoaded = ref(false);
const imageFile = ref(null);
const previewUrl = ref(null);
let viewer = null;

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
  if (!file?.type.startsWith('image/')) return;

  imageFile.value = file;
  if (previewUrl.value) { URL.revokeObjectURL(previewUrl.value); previewUrl.value = null; }

  let previewBlob = file;
  try {
    previewBlob = await compressImage(file, { maxWidth: 3072, maxHeight: 1536, quality: 1.0, mimeType: 'image/webp' });
  } catch (_) { /* usa original */ }

  const url = URL.createObjectURL(previewBlob);
  previewUrl.value = url;
  viewer.setPanorama(url).then(() => {
    viewer.animate({ yaw: Math.PI / 2, pitch: '20deg', zoom: 50, speed: '2rpm' });
    isImageLoaded.value = true;
    checkIfReadyToSubmit();
  });
}

function handleCloseViewer() {
  isImageLoaded.value = false;
  setTimeout(() => {
    viewer?.destroy(); viewer = null;
    if (previewUrl.value) { URL.revokeObjectURL(previewUrl.value); previewUrl.value = null; }
  }, 800);
}

// ═══════════════  Submit  ═══════════════
async function handleFormSubmit() {
  if (buttonType.value === 'deactivated') return;
  isUploading.value = true;

  let fileToUpload = imageFile.value;
  try {
    const compressed = await compressImage(imageFile.value, { maxWidth: 4096, maxHeight: 2048, quality: 0.9, mimeType: 'image/webp' });
    if (compressed?.size > 0) {
      const newName = (imageFile.value.name || 'image').replace(/\.[^.]+$/, '') + '.webp';
      fileToUpload = new File([compressed], newName, { type: compressed.type });
    }
  } catch (_) { /* usa original */ }

  let uploadImageResponse = null;
  try { uploadImageResponse = await uploadImageToServer(fileToUpload); } catch (_) { }

  if (!uploadImageResponse?.status) {
    isUploading.value = false;
    resultSuccess.value = false;
    resultTitle.value = 'Error al subir imagen';
    resultMessage.value = uploadImageResponse?.response_obj?.message || 'No se pudo subir la imagen.';
    showResultDialog.value = true;
    return;
  }

  const adjacentNodes = adjacentLabels.map((label) => {
    const name = inputModels[label];
    const weight = parseFloat(inputWeightModels[label]);
    return (name && !isNaN(weight)) ? { [name]: weight } : null;
  });

  const tagDict = {};
  for (const tag of tagStore.tags) {
    if (tagSelection[tag.name]) {
      tagDict[tag.name] = { [tagCustomName[tag.name]]: 0.0 };
    }
  }

  const nodeData = {
    name: inputModels['Identificación'],
    location: null,
    url_image: uploadImageResponse?.response_obj?.public_url,
    adjacent_nodes: adjacentNodes,
    tags: tagDict,
  };

  try {
    const createResp = await createNode(nodeData);
    isUploading.value = false;
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
    resultSuccess.value = false;
    resultTitle.value = 'Error inesperado';
    resultMessage.value = String(e);
  }
  showResultDialog.value = true;
}

// ═══════════════  Tags  ═══════════════
const tagSelection = reactive({});
const tagCustomName = reactive({});

watch(tags, (newTags) => {
  if (Array.isArray(newTags)) {
    newTags.forEach((tag) => {
      tagSelection[tag.name] = false;
      tagCustomName[tag.name] = '';
    });
  }
}, { immediate: true });

let stopWatching = null;
function handleTagClick(tagName) {
  if (tagSelection[tagName]) { tagSelection[tagName] = false; return; }
  actualTagSelected.value = tagName;
  tagSelection[tagName] = true;
  showDialog.value = true;
  if (!stopWatching) {
    stopWatching = watch(
      () => tagCustomName[actualTagSelected.value],
      (v) => { dialogButtonType.value = v?.trim() ? 'primary' : 'deactivated'; },
    );
  }
}

const tagSubmited = ref(false);
async function handleTagCustomization() {
  tagSubmited.value = true;
  showDialog.value = false;
  if (!tagCustomName[actualTagSelected.value]) tagSelection[actualTagSelected.value] = false;
  await nextTick();
  tagSubmited.value = false;
}

watch(showDialog, (newVal) => {
  if (!newVal && !tagSubmited.value) {
    tagSelection[actualTagSelected.value] = false;
    tagCustomName[actualTagSelected.value] = '';
    tagSubmited.value = false;
  }
});

// ═══════════════  Lifecycle  ═══════════════
function handleCancelEvent() { router.push({ name: 'NodeAdmin' }); }
function navigateToNodes() { showResultDialog.value = false; router.push({ name: 'NodeAdmin' }); }
function startNewNode() { showResultDialog.value = false; router.replace({ name: 'NodeCreate' }); }

onMounted(async () => {
  router.isReady().then(() => obtainData());
  viewer = new Viewer({
    container: viewerContainer.value,
    panorama: '',
    navbar: false,
    mousewheel: false,
    keyboard: false,
  });
});
onBeforeUnmount(() => { handleCloseViewer(); });

// ═══════════════  Compresión  ═══════════════
async function compressImage(file, opts = {}) {
  const { maxWidth = 1600, maxHeight = 1600, quality = 0.82, mimeType = 'image/webp' } = opts;
  const dataUrl = await new Promise((res, rej) => {
    const fr = new FileReader();
    fr.onload = () => res(fr.result);
    fr.onerror = rej;
    fr.readAsDataURL(file);
  });
  const img = await new Promise((res, rej) => {
    const i = new Image();
    i.onload = () => res(i);
    i.onerror = rej;
    i.src = dataUrl;
  });
  const ratio = Math.min(1, maxWidth / img.width, maxHeight / img.height);
  const canvas = document.createElement('canvas');
  canvas.width = Math.round(img.width * ratio);
  canvas.height = Math.round(img.height * ratio);
  const ctx = canvas.getContext('2d');
  ctx.imageSmoothingEnabled = true;
  ctx.imageSmoothingQuality = 'high';
  ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
  const outBlob = await new Promise((res) => canvas.toBlob(res, mimeType, quality));
  return outBlob?.size < file.size ? outBlob : file;
}
</script>

<style scoped lang="scss">
@import '@/assets/styles/_colors.scss';
@import '@/assets/styles/_typography.scss';

/* ─── LOADING BAR ───────────────────────────────────────── */
.loading-bar-container {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 9999;
  height: 3px;
  background: rgba(255, 239, 61, 0.15);

  .loading-bar {
    height: 100%;
    width: 40%;
    background: var(--main-yellow);
    border-radius: 0 2px 2px 0;
    animation: loading-slide 1.4s ease-in-out infinite;
  }
}

@keyframes loading-slide {
  0% {
    transform: translateX(-100%);
    width: 40%;
  }

  50% {
    width: 60%;
  }

  100% {
    transform: translateX(260%);
    width: 40%;
  }
}

/* ─── PAGE WRAPPER ──────────────────────────────────────── */
.create-container {
  position: relative;

  display: flex;
  flex-direction: column;

  height: calc(100vh - 60px);
  /* Resta el header de 60px */
  max-height: calc(100vh - 60px);
  /* Evita que crezca más */

  color: var(--full-white);

  padding: 1.5rem;
  box-sizing: border-box;

  overflow: hidden;
  /* Oculta cualquier overflow del contenedor principal */
  gap: 1.5rem;
}

/* dot-grid igual que UAbout */
.bg-grid {
  position: absolute;
  inset: 0;
  background-image: radial-gradient(circle, rgba(255, 239, 61, 0.10) 1px, transparent 1px);
  background-size: 32px 32px;
  pointer-events: none;
  z-index: 0;
}

.bg-noise {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse 80% 60% at 50% 20%, transparent 30%, var(--strong-gray-dark, #111) 100%);
  pointer-events: none;
  z-index: 1;
}

/* ─── HEADER ────────────────────────────────────────────── */
.page-header {
  position: relative;
  z-index: 2;
  max-width: 560px;
  flex-shrink: 0;
  /* No se encoja */
}

.overline {
  @include paragraph-small;
  color: var(--main-yellow);
  text-transform: uppercase;
  letter-spacing: 0.12em;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.eyebrow-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--main-yellow);
  display: inline-block;
  flex-shrink: 0;
}

.page-title {
  @include paragraph-h1;
  font-size: 2.5rem;
  line-height: 1.1;
  letter-spacing: -0.03em;
  margin-bottom: 0.75rem;
  color: var(--full-white);

  em {
    font-style: normal;
    color: var(--main-yellow);
  }

  @media (min-width: 768px) {
    font-size: 3rem;
  }
}

.page-sub {
  @include paragraph-medium-extra-light;
  color: rgba(255, 255, 255, 0.45);
  line-height: 1.6;
}

/* ─── MAIN CARD ─────────────────────────────────────────── */
/* ─── MAIN CARD ─────────────────────────────────────────── */
.card {
  position: relative;
  z-index: 2;

  display: flex;
  flex: 1;
  min-height: 0;
  /* Crucial para que flex respete el espacio */

  overflow: hidden;

  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;

  @media (max-width: 859px) {
    flex-direction: column;
  }
}

/* ─── VIEWER PANEL ──────────────────────────────────────── */
.card-viewer {
  position: relative;
  flex: 1;
  min-height: 0;

  background: var(--strong-gray-dark, #111);

  border-right: 1px solid rgba(255, 255, 255, 0.08);

  display: flex;
  align-items: center;
  justify-content: center;

  overflow: hidden;

  @media (max-width: 859px) {
    flex: 0 0 25%;
    /* Ocupa exactamente el 25% del alto, no se expande ni se contrae */
    border-right: none;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  }
}

.panorama-viewer {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

.upload-zone {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.6rem;
  cursor: pointer;
  padding: 2.5rem;
  border: 1.5px dashed rgba(255, 239, 61, 0.25);
  border-radius: 12px;
  margin: 1.5rem;
  transition: border-color 0.2s, background 0.2s;

  &:hover {
    border-color: rgba(255, 239, 61, 0.5);
    background: rgba(255, 239, 61, 0.04);
  }
}

.upload-icon-wrap {
  width: 52px;
  height: 52px;
  border-radius: 12px;
  border: 1px solid rgba(255, 239, 61, 0.25);
  background: rgba(255, 239, 61, 0.07);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.25rem;
}

.upload-label {
  @include paragraph-medium;
  color: var(--full-white);
}

.upload-hint {
  @include paragraph-small;
  color: rgba(255, 255, 255, 0.35);
}

.change-image-btn {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
  z-index: 4;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.4rem 0.85rem;
  border-radius: 8px;
  border: 1px solid rgba(255, 239, 61, 0.3);
  background: rgba(0, 0, 0, 0.55);
  backdrop-filter: blur(6px);
  color: var(--main-yellow);
  cursor: pointer;
  @include paragraph-small;
  transition: background 0.2s;

  &:hover {
    background: rgba(255, 239, 61, 0.12);
  }
}

/* ─── FORM PANEL ────────────────────────────────────────── */
.card-form {
  background: var(--strong-gray-dark, #111);
  flex: 1;
  min-height: 0;
  /* Crucial para que funcione el scroll */

  padding: 2rem 1.75rem;

  display: flex;
  flex-direction: column;
  gap: 1.25rem;

  overflow-y: auto;
  /* Solo aquí hay scroll */
  overflow-x: hidden;

  -webkit-overflow-scrolling: touch;
  /* Mejor scroll en iOS */

  /* Asegura que el padding no se coma al hacer scroll */
  scroll-padding: 2rem 1.75rem;

  @media (max-width: 859px) {
    flex: 1;
    /* Toma el 75% restante */
    min-height: 0;
  }
}

.form-section-label {
  @include paragraph-extra-small;
  color: var(--main-yellow);
  text-transform: uppercase;
  letter-spacing: 0.12em;
  padding: 0.75rem 1rem;
  border-radius: 4px;
  border: 1px solid rgba(255, 239, 61, 0.2);
  background: rgba(255, 239, 61, 0.06);
  display: inline-block;
  width: fit-content;
  margin-bottom: 0.25rem;
}

.input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;

  &.has-error .input-label {
    color: var(--status-red, #e53935);
  }
}

.input-label {
  @include paragraph-small;
  color: rgba(255, 255, 255, 0.55);
  transition: color 0.2s;
}

.adjacent-row {
  display: flex;
  gap: 0.5rem;
  width: 100%;
  min-width: 0;
}

.adjacent-row>* {
  min-width: 0;
}

.adjacent-row> :first-child {
  flex: 1;
}



:deep(input::placeholder) {
  color: rgba(255, 255, 255, 0.35);
}

.error-msg {
  @include paragraph-extra-small;
  color: var(--status-red, #e53935);
  font-size: 0.7rem;
}

.divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.07);
  margin: 0.25rem 0;
}

/* ─── TAGS ──────────────────────────────────────────────── */
.tag-row {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  padding-top: 0.5rem;

  :deep(svg) {
      cursor: pointer;
      transition: all 0.1s ease;
  
      &:hover {
        filter: brightness(1.2) drop-shadow(0 0 4px rgba(255, 239, 61, 0.4));
        transform: scale(1.05);
      }
    }
}

/* ─── FORM ACTIONS ──────────────────────────────────────── */
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: auto;
  padding-top: 1rem;
  flex-shrink: 0;
  /* Los botones no se encogen */
}

/* ─── DIALOGS ───────────────────────────────────────────── */
.tag-dialog-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 0.5rem 0;
}

.result-dialog {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 0.5rem 0;
}

.result-icon {
  display: flex;
  justify-content: center;
}

.result-text {
  text-align: center;

  .upper-paragraph {
    @include paragraph-medium;
    color: var(--full-white);
    margin-bottom: 0.35rem;
  }

  .lower-paragraph {
    @include paragraph-small;
    color: rgba(255, 255, 255, 0.5);
  }
}

.result-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

/* ─── TRANSITIONS ───────────────────────────────────────── */
.fade-panorama-enter-active,
.fade-panorama-leave-active {
  transition: opacity 0.8s ease;
}

.fade-panorama-enter-from,
.fade-panorama-leave-to {
  opacity: 0;
}
</style>