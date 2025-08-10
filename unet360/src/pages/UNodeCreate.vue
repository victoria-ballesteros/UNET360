<template>
  <div v-if="isUploading" class="loading-bar-container">
    <div class="loading-bar"></div>
  </div>
  <transition name="fade-panorama">
    <div v-show="isImageLoaded" ref="viewerContainer" class="background-viewer" />
  </transition>
  <div v-if="!isUploading" class="outer-container">
    <div v-if="!imageFile" class="upper-container">
      <UButton text="Subir imagen" @click="openUploadFileDialog" type="secondary" icon="cloud-upload" />
      <input type="file" ref="fileInput" style="display: none" @change="handleFileChange" />
      <div class="icons-container">
        <div class="pair-container">
          <UIcon name="icons/star" size="22" color="var(--strong-gray)" :rotation="15" />
          <UIcon name="icons/star" size="15" color="var(--strong-gray)" :rotation="22" />
        </div>
        <UIcon name="icons/star" size="22" color="var(--strong-gray)" />
      </div>
    </div>
    <div class="lower-container" :class="['lower-container', { 'transparent-bg': isImageLoaded }]" ref="lowerContainer">
      <p class="form-title">{{ formTitle }}</p>
      <div class="form-container" ref="scrollContainer">
        <div class="input-container" :class="{ 'has-error': inputErrors[input] }" v-for="(input, index) in inputLabels"
          :key="index">
          <p class="input-label" :class="{ 'label-disabled': inputDisabled[input] }">
            {{ input }}
          </p>
          <div class="node-input-container">
            <UInput v-model="inputModels[input]" styleType="default" :placeholder="inputPlaceholders[input]"
              :icon="inputIcon[input]" :iconRotation="index * 90" :disabled="inputDisabled[input]"
              @input="() => (inputTouched[input] = true)" />
            <UInput v-if="inputWeightModels[input] != null" v-model="inputWeightModels[input]" styleType="default"
              :disabled="inputDisabled[input]" type="text" inputmode="numeric" pattern="[0-9.]*" placeholder="Peso"
              @input="() => (inputTouched[input] = true)" />
          </div>
          <p v-if="inputErrors[input]" class="input-error-label">
            {{ inputErrors[input] }}
          </p>
        </div>
        <div class="input-container" v-show="expandForm">
          <p class="input-label">Datos opcionales</p>
          <div class="tag-container">
            <UIcon v-for="(tag, index) in tags" :key="index" :name="'icons/' + tag.icon_name" size="34" :color="tagSelection[tag.name]
              ? 'var(--main-blue)'
              : 'var(--border-gray)'
              " @click="handleTagClick(tag.name)" />
          </div>
        </div>
      </div>
      <div class="button-container">
        <UButton text="Cancelar" @click="handleCancelEvent" type="tertiary" />
        <UButton :text="actionButton" @click.stop="handlePrimaryClick" :type="buttonType" />
      </div>
    </div>
  </div>

  <UDialog v-model="showDialog" headerTitle="Identificación del tag">
    <div class="tag-dialog-content">
      <UInput v-model="tagCustomName[actualTagSelected]" styleType="default" placeholder="Baño oeste" />
      <UButton style="align-self: flex-end" text="Aceptar" @click="handleTagCustomization" :type="dialogButtonType" />
    </div>
  </UDialog>

  <!-- Resultado de creación -->
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
      <div class="button-container" style="margin-top: 12px; display: flex; gap: 12px; justify-content: flex-end;">
        <UButton text="Ver nodos" type="contrast-2" @click="navigateToNodes" />
        <UButton text="Crear Nuevo Nodo" type="contrast-2" @click="startNewNode" />
      </div>
    </div>
  </UDialog>
</template>

<script setup>
import {
  ref,
  computed,
  reactive,
  watch,
  nextTick,
  onMounted,
  onBeforeUnmount,
} from "vue";
import UButton from "@/components/UButton.vue";
import UInput from "@/components/UInput.vue";
import UIcon from "@/components/UIcon.vue";
import UDialog from "@/components/UDialog.vue";

import { useNodeStore } from "../service/stores/nodes";
import { useTagStore } from "@/service/stores/tags";

import { obtainData } from "../service/shared/utils";
import { uploadImageToServer, createNode } from "@/service/requests/requests";

import { useRouter } from "vue-router";

import { Viewer } from "@photo-sphere-viewer/core";
import "@photo-sphere-viewer/core/index.css";

const router = useRouter();

// ═══════════════  Components variables  ═══════════════

const formTitle = ref("Ingrese los datos de la nueva ubicación");
const lowerContainer = ref(null);
const showLower = ref(true);
const actionButton = ref("Continuar");
const buttonType = ref("deactivated");
const expandForm = ref(false);
const showDialog = ref(false);
const scrollContainer = ref(null);
const actualTagSelected = ref("");
const dialogButtonType = ref("deactivated");

// Resultado creación
const showResultDialog = ref(false);
const resultSuccess = ref(false);
const resultTitle = ref("");
const resultMessage = ref("");


// ═══════════════  Reload page state  ═══════════════

const isUploading = ref(false);

function resetForm() {
  isUploading.value = false;
}

// ═══════════════  360 viewer  ═══════════════

const viewerContainer = ref(null);
const isImageLoaded = ref(false);
const imageFile = ref(false);
let viewer = null;

// ═══════════════  360 stores  ═══════════════

const nodeStore = useNodeStore();
const tagStore = useTagStore();
const nodes = computed(() => nodeStore.nodes);
const tags = computed(() => tagStore.tags);

// ═══════════════  Nodes validations  ═══════════════

const inputLabels = reactive([
  "Nodo siguiente",
  "Nodo derecho",
  "Nodo anterior",
  "Nodo izquierdo",
]);
const inputPlaceholders = {};
const inputModels = reactive({});
const inputWeightModels = reactive({});
const inputErrors = reactive({});
const inputDisabled = reactive({});
const inputIcon = reactive({});

inputLabels.forEach((label) => {
  inputPlaceholders[label] = `Id. del ${label.toLowerCase()}`;
  inputModels[label] = "";
  inputWeightModels[label] = "";
  inputErrors[label] = "";
  inputDisabled[label] = false;
  inputIcon[label] = "arrow-up";
});

function checkIfReadyToSubmit() {
  //   const allFilled = Object.values(inputModels).every(
  //     (value) => value?.trim() !== ""
  //   );
  const noErrors = Object.values(inputErrors).every((error) => error === "");
  buttonType.value = (noErrors && imageFile.value) ? "primary" : "deactivated";
}

const inputTouched = reactive({});
inputLabels.forEach((label) => {
  inputTouched[label] = false;
});

inputLabels.forEach((label) => {
  watch(
    [() => inputModels[label], () => inputWeightModels[label]],
    ([newVal, newWeight]) => {
      if (!inputTouched[label] && !newVal && !newWeight) {
        return;
      }
      const trimmed = newVal?.trim();
      const exists = nodes.value?.some((node) => node.name === trimmed);

      inputErrors[label] = "";

      //   if (!exists && trimmed) {
      //     inputErrors[label] = "";
      //     return;
      //   }

      if (!newWeight?.toString().trim() && trimmed) {
        inputErrors[label] = "El peso no puede estar vacío";
      } else if (newWeight?.toString().trim() && inputModels[label] == "") {
        inputErrors[label] = "Peso asignado a una arista incompleta";
      }

      checkIfReadyToSubmit();
    },
    { immediate: true }
  );
});

// ═══════════════  Image upload validation  ═══════════════

const fileInput = ref(null);

function openUploadFileDialog() {
  fileInput.value?.click();
}

async function handleFileChange(event) {
  const file = event.target.files[0];
  if (file && file.type.startsWith("image/")) {
    imageFile.value = file;
    const url = URL.createObjectURL(file);
    viewer.setPanorama(url).then(() => {
      viewer.animate({
        yaw: Math.PI / 2,
        pitch: "20deg",
        zoom: 50,
        speed: "2rpm",
      });
      isImageLoaded.value = true;
      checkIfReadyToSubmit();
    });
  }
}

function handleCloseViewer() {
  isImageLoaded.value = false;

  setTimeout(() => {
    if (viewer) {
      viewer.destroy();
      viewer = null;
    }
  }, 800);
}

// ═══════════════  Form buttons  ═══════════════

function handleCancelEvent() {
  router.push({ name: 'NodeAdmin' });
}

async function handlePrimaryClick() {
  if (actionButton.value == "Continuar") {
    await handleFormExpansion();
  } else {
    await handleFormSubmit();
  }
}

async function handleFormExpansion() {
  handleCloseViewer();

  formTitle.value = "Nodo verificado";
  inputLabels.forEach((label) => {
    inputDisabled[label] = true;
  });

  inputLabels.push("Identificación");
  inputPlaceholders["Identificación"] = "Identificación del nodo actual";
  inputModels["Identificación"] = "";
  inputErrors["Identificación"] = "";
  inputDisabled["Identificación"] = false;
  buttonType.value = "deactivated";
  actionButton.value = "Subir nodo";
  expandForm.value = true;

  await nextTick();

  if (scrollContainer.value) {
    scrollContainer.value.scrollTo({
      top: scrollContainer.value.scrollHeight,
      behavior: "smooth",
    });
  }

  watch(
    () => inputModels["Identificación"],
    (newVal) => {
      const trimmed = newVal?.trim();
      let err = "";
      if (!trimmed) {
        err = "La identificación es obligatoria";
      } else if (trimmed.length < 3) {
        err = "La identificación debe tener al menos 3 caracteres";
      } else if (!/^\d+(-[a-zA-Z0-9]+)*$/.test(trimmed)) {
        err = "Formato inválido. Ej: 003-HallA";
      } else if (nodes.value.some((node) => node.name === trimmed)) {
        err = "El nodo ya existe";
      }
      inputErrors["Identificación"] = err;
      checkIfReadyToSubmit();
    }
  );
}

async function handleFormSubmit() {
  isUploading.value = true;
  if (!imageFile.value) {
    isUploading.value = false;
    return;
  }
  let uploadImageResponse = null;
  try {
    uploadImageResponse = await uploadImageToServer(imageFile.value);
  } catch (e) {
    // ignored
  }
  if (!uploadImageResponse || !uploadImageResponse?.status) {
    isUploading.value = false;
    resultSuccess.value = false;
    resultTitle.value = 'Error al subir imagen';
    resultMessage.value = uploadImageResponse?.response_obj?.message || 'No se pudo subir la imagen.';
    showResultDialog.value = true;
    resetForm();
    return;
  }

  const adjacentNodes = [];
  const tagDict = {};

  for (let i = 0; i < 4; i++) {
    const label = inputLabels[i];
    const nodeName = inputModels[label];
    const rawWeight = inputWeightModels[label];

    const parsedWeight = parseFloat(rawWeight);
    const weight = isNaN(parsedWeight) ? null : parsedWeight;

    if (nodeName) {
      adjacentNodes.push({ [nodeName]: weight });
    } else {
      adjacentNodes.push(null);
    }
  }

  for (const tag of tagStore.tags) {
    if (tagSelection[tag.name]) {
      tagDict[tag.name] = {
        [tagCustomName[tag.name]]: 0.0
      };
    }
  }

  const nodeData = {
    name: inputModels["Identificación"],
    location: null,
    url_image: uploadImageResponse?.response_obj.signed_url,
    adjacent_nodes: adjacentNodes,
    tags: tagDict
  }
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
    showResultDialog.value = true;
  } catch (e) {
    isUploading.value = false;
    resultSuccess.value = false;
    resultTitle.value = 'Error inesperado';
    resultMessage.value = String(e);
    showResultDialog.value = true;
  }
}


// ═══════════════  Tag handling  ═══════════════

const tagSelection = reactive({});
const tagCustomName = reactive({});

watch(
  tags,
  (newTags) => {
    if (Array.isArray(newTags)) {
      newTags.forEach((tag) => {
        tagSelection[tag.name] = false;
        tagCustomName[tag.name] = "";
      });
    }
  },
  { immediate: true }
);

let stopWatching = null;

function handleTagClick(tagName) {
  if (tagSelection[tagName]) {
    tagSelection[tagName] = false;
    return;
  }
  actualTagSelected.value = tagName;
  showDialog.value = true;
  tagSelection[tagName] = true;

  if (!stopWatching) {
    stopWatching = watch(
      () => tagCustomName[actualTagSelected.value],
      (newInput) => {
        dialogButtonType.value = newInput?.trim() ? "primary" : "deactivated";
      }
    );
  }
}

const tagSubmited = ref(false);

async function handleTagCustomization() {
  tagSubmited.value = true;
  showDialog.value = false;

  if (!tagCustomName[actualTagSelected.value]) {
    tagSelection[actualTagSelected.value] = false;
  }
  await nextTick();
  tagSubmited.value = false;
}

watch(showDialog, (newVal, oldVal) => {
  if (!newVal && !tagSubmited.value) {
    tagSelection[actualTagSelected.value] = false;
    tagCustomName[actualTagSelected.value] = "";
    tagSubmited.value = false;
  }
});

// ═══════════════  Page state related functions  ═══════════════

onMounted(async () => {
  router.isReady().then(async () => {
    await obtainData();
  });
  viewer = new Viewer({
    container: viewerContainer.value,
    panorama: "",
    navbar: false,
    mousewheel: false,
    keyboard: false,
  });
});

onBeforeUnmount(() => {
  handleCloseViewer();
});

// Navegación de resultado
function navigateToNodes() {
  showResultDialog.value = false;
  router.push({ name: 'NodeAdmin' });
}

function startNewNode() {
  showResultDialog.value = false;
  // Reinicia la ruta para limpiar estado del formulario
  router.replace({ name: 'NodeCreate' });
}
</script>

<style scoped lang="scss">
@import "@/assets/styles/pages/_node_create.scss";
</style>
