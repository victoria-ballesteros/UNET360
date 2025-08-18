<template>
  <div class="form-container">
    <div class="text-section">
      <p class="upper-paragrah">Editar nodo</p>
      <p class="lower-paragraph">Actualiza los datos del nodo seleccionado.</p>
    </div>

    <div class="form-section">
      <div class="input-container">
        <p class="input-label">Identificación</p>
        <UInput v-model="form.name" styleType="default" :disabled="true" />
      </div>

      <div class="input-container">
        <p class="input-label">Ubicación</p>
        <div class="autosuggest">
          <UInput v-model="form.location" styleType="default" placeholder="Nombre de ubicación" />
          <div v-if="showLocationSuggest && locationSuggestions.length" class="suggestions">
            <button
              v-for="opt in locationSuggestions"
              :key="opt"
              class="sugg-item"
              type="button"
              @mousedown.prevent="selectLocation(opt)"
            >{{ opt }}</button>
          </div>
        </div>
      </div>

      <div class="input-container">
        <p class="input-label">URL de imagen</p>
        <UInput v-model="form.url_image" styleType="default" placeholder="https://..." />
      </div>

      <div class="input-container">
        <p class="input-label">Nodos adyacentes</p>
        <div class="adjacent-grid">
          <div v-for="(label, idx) in adjacentLabels" :key="idx" class="adjacent-row">
            <UInput v-model="adjacentInputs[idx].name" styleType="default" :placeholder="label" />
            <UInput v-model="adjacentInputs[idx].weight" styleType="default" type="text" :inputMode="'numeric'" pattern="[0-9.]*" placeholder="Peso" />
          </div>
        </div>
      </div>

      <div class="input-container">
        <div class="label-row">
          <p class="input-label">Dirección de las flechas</p>
          <UButton text="Asignar" type="contrast-2" @click="openArrowDirectionAssignment" />
        </div>
        <div class="angles-grid">
          <div v-for="(label, idx) in adjacentLabels" :key="'ang-'+idx" class="angle-row">
            <UInput v-model="arrowAngles[idx]" styleType="default" type="text" :inputMode="'numeric'" pattern="-?[0-9]*(\.[0-9]+)?" :placeholder="label + ' - dirección'" />
          </div>
        </div>
      </div>

      <div class="input-container">
        <div class="label-row">
          <p class="input-label">Frente de la imagen</p>
          <UButton text="Asignar" type="contrast-2" @click="openFrontImageAssignment" />
        </div>
        <UInput v-model="form.forward_heading" styleType="default" type="text" :inputMode="'numeric'" pattern="-?[0-9]*(\.[0-9]+)?" />
      </div>

      <!-- Minimap 2D -->
      <div class="input-container">
        <p class="input-label">Mapa 2D</p>
        <div class="minimap-grid">
          <UInput v-model="form.minimap.image" styleType="default" placeholder="Nombre del mapa" />
          <UInput v-model="form.minimap.x" styleType="default" type="text" :inputMode="'numeric'" pattern="-?[0-9]*(\.[0-9]+)?" placeholder="X" />
          <UInput v-model="form.minimap.y" styleType="default" type="text" :inputMode="'numeric'" pattern="-?[0-9]*(\.[0-9]+)?" placeholder="Y" />
        </div>
      </div>

      <div class="input-container">
        <p class="input-label">Tags</p>
        <div class="tag-list">
          <div v-for="(tag, tagIdx) in tags" :key="tagIdx" class="tag-item">
            <div class="tag-header">
              <div class="autosuggest">
                <UInput v-model="tag.name" styleType="default" :placeholder="'Nombre del tag'" />
                <div v-if="showTagSuggest[tagIdx] && getTagSuggestions(tagIdx).length" class="suggestions">
                  <button
                    v-for="opt in getTagSuggestions(tagIdx)"
                    :key="opt"
                    class="sugg-item"
                    type="button"
                    @mousedown.prevent="selectTagName(tagIdx, opt)"
                  >{{ opt }}</button>
                </div>
              </div>
              <UButton text="Eliminar" type="danger" @click="removeTag(tagIdx)" />
            </div>
            <div class="tag-values">
              <div v-for="(val, valIdx) in tag.values" :key="valIdx" class="tag-value-row">
                <div class="tag-value-grid">
                  <UInput v-model="tag.values[valIdx].text" styleType="default" placeholder="Valor" />
                  <div class="angle-assign-wrapper">
                    <UInput v-model="tag.values[valIdx].angle" styleType="default" type="text" :inputMode="'numeric'" pattern="-?[0-9]*(\.[0-9]+)?" placeholder="Yaw (rad)" />
                    <UButton text="Asignar" type="contrast-2" @click="openTagValueAssignment(tagIdx, valIdx)" />
                  </div>
                </div>
                <UButton text="-" type="danger" @click="removeTagValue(tagIdx, valIdx)" />
              </div>
              <UButton text="Añadir valor" type="secondary" @click="addTagValue(tagIdx)" />
            </div>
          </div>
        </div>
        <div class="tag-actions">
          <UButton text="Añadir tag" type="blue" @click="addTag()" />
        </div>
      </div>

      <div class="button-container">
        <UButton text="Cancelar" type="tertiary" @click="router.push({ name: 'NodeAdmin' })" />
        <UButton text="Guardar cambios" type="contrast-2" @click="submit" />
      </div>
    </div>
  </div>

  <!-- Dialogo para asignar direcciones / frente -->
  <UDialog v-model="showDirectionDialog" :headerTitle="directionDialogTitle">
    <div class="direction-dialog">
      <p class="direction-instructions" v-if="directionMode === 'arrow'">
        Clic para capturar orientación: <strong>{{ arrowOrder[currentArrowIndex] }}</strong> (orden: Frente, Derecha, Atras, Izquierda).
      </p>
      <p class="direction-instructions" v-else>
        Clic para capturar yaw del Frente de la imagen.
      </p>
      <div ref="directionViewerContainer" class="direction-viewer"></div>
      <div class="direction-footer">
        <UButton text="Reiniciar" type="tertiary" @click="resetCurrentDirectionSequence" />
        <UButton text="Cerrar" type="secondary" @click="closeDirectionDialog" />
      </div>
    </div>
  </UDialog>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted, onBeforeUnmount, nextTick, defineProps } from 'vue';
// Accept optional name prop (avoids extraneous attribute warning if parent passes it)
defineProps({ name: { type: String, required: false } });
import { useRoute, useRouter } from 'vue-router';
import UInput from '@/components/UInput.vue';
import UButton from '@/components/UButton.vue';
import UDialog from '@/components/UDialog.vue';
import api from '@/axios';
import { Viewer } from '@photo-sphere-viewer/core';
import '@photo-sphere-viewer/core/index.css';

const route = useRoute();
const router = useRouter();

const form = reactive({
  name: '',
  location: '',
  url_image: '',
  forward_heading: '',
  minimap: { image: '', x: '', y: '' },
});

const adjacentLabels = ['Frente', 'Derecha', 'Atras', 'Izquierda'];
const adjacentInputs = reactive([
  { name: '', weight: '' },
  { name: '', weight: '' },
  { name: '', weight: '' },
  { name: '', weight: '' },
]);
const arrowAngles = reactive(['', '', '', '']);

// 360 direction assignment state
const showDirectionDialog = ref(false);
const directionMode = ref('arrow'); // 'arrow' | 'front' | 'tagValue'
const arrowOrder = ['Frente', 'Derecha', 'Atras', 'Izquierda'];
const currentArrowIndex = ref(0);
const directionViewerContainer = ref(null);
let directionViewer = null;
const directionDialogTitle = computed(() => {
  if (directionMode.value === 'arrow') return 'Asignar direcciones de flecha';
  if (directionMode.value === 'front') return 'Asignar frente de la imagen';
  return 'Asignar ángulo de tag';
});

// Para tag value assignment
const currentTagIndex = ref(null);
const currentTagValueIndex = ref(null);

async function openArrowDirectionAssignment() {
  if (!form.url_image) return; // necesita imagen
  directionMode.value = 'arrow';
  currentArrowIndex.value = 0;
  showDirectionDialog.value = true;
  await nextTick();
  initDirectionViewer();
}
async function openFrontImageAssignment() {
  if (!form.url_image) return;
  directionMode.value = 'front';
  showDirectionDialog.value = true;
  await nextTick();
  initDirectionViewer();
}
async function openTagValueAssignment(tagIdx, valIdx) {
  if (!form.url_image) return;
  currentTagIndex.value = tagIdx;
  currentTagValueIndex.value = valIdx;
  directionMode.value = 'tagValue';
  showDirectionDialog.value = true;
  await nextTick();
  initDirectionViewer();
}
function resetCurrentDirectionSequence() {
  if (directionMode.value === 'arrow') {
    for (let i = 0; i < 4; i++) arrowAngles[i] = '';
    currentArrowIndex.value = 0;
  } else {
    form.forward_heading = '';
  }
}
function closeDirectionDialog() { showDirectionDialog.value = false; }

function initDirectionViewer() {
  if (!directionViewerContainer.value) return; // aún no montado
  if (directionViewer) { directionViewer.destroy(); directionViewer = null; }
  try {
    directionViewer = new Viewer({
      container: directionViewerContainer.value,
      panorama: form.url_image,
      navbar: false,
      mousewheel: false,
      keyboard: false,
    });
    directionViewer.addEventListener('click', ({ data }) => {
      if (!data) return;
      const yaw = data.yaw; // radianes
      if (directionMode.value === 'arrow') {
        arrowAngles[currentArrowIndex.value] = yaw.toString();
        if (currentArrowIndex.value < arrowOrder.length - 1) {
          currentArrowIndex.value++;
        } else {
          closeDirectionDialog();
        }
      } else if (directionMode.value === 'front') {
        form.forward_heading = yaw.toString();
        closeDirectionDialog();
      } else if (directionMode.value === 'tagValue') {
        if (currentTagIndex.value != null && currentTagValueIndex.value != null && tags[currentTagIndex.value] && tags[currentTagIndex.value].values[currentTagValueIndex.value]) {
          tags[currentTagIndex.value].values[currentTagValueIndex.value].angle = yaw.toString();
        }
        closeDirectionDialog();
      }
    });
  } catch (e) {
    // fallback: cerrar dialog si falla crear viewer
    console.warn('No se pudo inicializar el visor 360:', e);
    closeDirectionDialog();
  }
}

// Tags como arreglo; cada tag tiene valores [{ text, angle }]
const tags = reactive([]);

// Autosuggest data
const allLocations = ref([]);
const allTags = ref([]);
const showLocationSuggest = ref(false);
const suppressLocationOnce = ref(false);
const showTagSuggest = reactive([]);
const suppressTagOnce = reactive([]);

const locationSuggestions = computed(() => {
  const q = (form.location || '').trim().toLowerCase();
  if (!q) return [];
  return allLocations.value.filter(n => n.toLowerCase().includes(q)).slice(0, 6);
});
function getTagSuggestions(idx) {
  const q = ((tags[idx]?.name) || '').trim().toLowerCase();
  if (!q) return [];
  return allTags.value.filter(n => n.toLowerCase().includes(q)).slice(0, 6);
}
function selectLocation(name) {
  suppressLocationOnce.value = true;
  showLocationSuggest.value = false;
  form.location = name;
}
function selectTagName(idx, name) {
  if (tags[idx]) {
    suppressTagOnce[idx] = true;
    showTagSuggest[idx] = false;
    tags[idx].name = name;
  }
}

async function loadNode() {
  const name = route.params.name;
  try {
    const { data } = await api.get(`nodes/${encodeURIComponent(name)}`);
    if (data?.status && data.response_obj) {
      const n = data.response_obj;
      form.name = n.name ?? '';
      form.location = n.location ?? '';
      form.url_image = n.url_image ?? '';
      form.forward_heading = (n.forward_heading ?? 0).toString();

      // Adjacent nodes
      const list = Array.isArray(n.adjacent_nodes) ? n.adjacent_nodes : [null, null, null, null];
      for (let i = 0; i < 4; i++) {
        const adj = list[i] || null;
        if (adj && typeof adj === 'object') {
          const adjName = Object.keys(adj)[0];
          const w = adj[adjName];
          adjacentInputs[i].name = adjName || '';
          adjacentInputs[i].weight = (w ?? '').toString();
        } else {
          adjacentInputs[i].name = '';
          adjacentInputs[i].weight = '';
        }
      }

      // Angles
      const a = Array.isArray(n.arrow_angles) ? n.arrow_angles : [null, null, null, null];
      for (let i = 0; i < 4; i++) {
        arrowAngles[i] = (a[i] ?? '').toString();
      }

      // Minimap
      if (n.minimap && typeof n.minimap === 'object') {
        form.minimap.image = (n.minimap.image ?? '').toString();
        form.minimap.x = (n.minimap.x ?? '').toString();
        form.minimap.y = (n.minimap.y ?? '').toString();
      } else {
        form.minimap.image = '';
        form.minimap.x = '';
        form.minimap.y = '';
      }

      // Tags
      tags.length = 0;
      showTagSuggest.length = 0;
      suppressTagOnce.length = 0;
      if (n.tags && typeof n.tags === 'object') {
        Object.entries(n.tags).forEach(([k, v]) => {
          let pairs = [];
          if (Array.isArray(v)) {
            pairs = v.map(item => ({ text: (item ?? '').toString(), angle: '0' }));
          } else if (typeof v === 'object' && v !== null) {
            pairs = Object.entries(v).map(([txt, ang]) => ({ text: (txt ?? '').toString(), angle: (ang ?? 0).toString() }));
          }
          tags.push({ name: k, values: pairs });
          showTagSuggest.push(false);
          suppressTagOnce.push(false);
        });
      }
    }
  } catch (e) {
    // noop
  }
}

async function loadSuggestSources() {
  try {
    const [locRes, tagRes] = await Promise.all([
      api.get('locations/'),
      api.get('tags/'),
    ]);
    if (locRes?.data?.status && Array.isArray(locRes.data.response_obj)) {
      allLocations.value = locRes.data.response_obj
        .map(x => x?.name)
        .filter(Boolean);
    }
    if (tagRes?.data?.status && Array.isArray(tagRes.data.response_obj)) {
      allTags.value = tagRes.data.response_obj
        .map(x => x?.name)
        .filter(Boolean);
    }
  } catch(_) { /* ignore */ }
}

function addTag() {
  tags.push({ name: '', values: [{ text: '', angle: '' }] });
  showTagSuggest.push(false);
  suppressTagOnce.push(false);
}

function removeTag(tagIdx) {
  tags.splice(tagIdx, 1);
  showTagSuggest.splice(tagIdx, 1);
  suppressTagOnce.splice(tagIdx, 1);
}

function addTagValue(tagIdx) {
  tags[tagIdx].values.push({ text: '', angle: '' });
}

function removeTagValue(tagIdx, valIdx) {
  tags[tagIdx].values.splice(valIdx, 1);
}

function buildPayload() {
  const adjacent_nodes = adjacentInputs.map(a => {
    const nm = (a.name || '').trim();
    if (!nm) return null;
    const w = parseFloat(a.weight);
    if (isNaN(w)) return null;
    return { [nm]: w };
  });

  const angles = arrowAngles.map(a => {
    const v = parseFloat(a);
    return isNaN(v) ? null : v;
  });

  const tagsObj = {};
  tags.forEach(t => {
    const key = (t.name || '').trim();
    if (!key) return;
    const valueMap = {};
    (t.values || []).forEach(pair => {
      const txt = (pair.text || '').trim();
      if (!txt) return;
      const ang = parseFloat(pair.angle);
      valueMap[txt] = isNaN(ang) ? 0.0 : ang;
    });
  tagsObj[key] = valueMap;
  });

  return {
    location: form.location || null,
  url_image: form.url_image,
    adjacent_nodes,
    arrow_angles: angles,
    forward_heading: parseFloat(form.forward_heading) || 0,
    tags: tagsObj,
    ...(function () {
      const image = (form.minimap.image || '').trim();
      const xNum = parseFloat(form.minimap.x);
      const yNum = parseFloat(form.minimap.y);
      const minimap = {};
      if (image) minimap.image = image;
      if (!isNaN(xNum)) minimap.x = xNum;
      if (!isNaN(yNum)) minimap.y = yNum;
      return Object.keys(minimap).length ? { minimap } : {};
    })(),
  };
}

async function submit() {
  try {
    const payload = buildPayload();
    const { data } = await api.patch(`nodes/${encodeURIComponent(form.name)}`, payload);
    if (data?.status) {
      router.push({ name: 'NodeAdmin' });
    }
  } catch (e) {
    console.log(e);
  }
}

onMounted(async () => {
  await Promise.all([loadNode(), loadSuggestSources()]);
});

// Destruir viewer al cerrar el dialog
watch(showDirectionDialog, (open) => {
  if (!open && directionViewer) {
    directionViewer.destroy();
    directionViewer = null;
  } else if (open) {
    // en caso de que se abra por un cambio externo y la ref ya exista
    nextTick().then(() => initDirectionViewer());
  }
});

onBeforeUnmount(() => {
  if (directionViewer) { directionViewer.destroy(); directionViewer = null; }
});

// Show/hide logic while typing
watch(() => form.location, (v) => {
  if (suppressLocationOnce.value) {
    showLocationSuggest.value = false;
    suppressLocationOnce.value = false;
    return;
  }
  const has = !!(v && v.trim().length > 0);
  showLocationSuggest.value = has && locationSuggestions.value.length > 0;
});

watch(() => tags.map(t => t.name), (names) => {
  names.forEach((v, i) => {
    if (suppressTagOnce[i]) {
      showTagSuggest[i] = false;
      suppressTagOnce[i] = false;
      return;
    }
    const has = !!(v && v.trim().length > 0);
    const list = getTagSuggestions(i);
    showTagSuggest[i] = has && list.length > 0;
  });
});
</script>

<style lang="scss">
@import "@/assets/styles/pages/node_edit.scss";

.label-row { display:flex; justify-content:space-between; align-items:center; gap:12px; }
.direction-dialog { display:flex; flex-direction:column; gap:12px; max-width:760px; }
.direction-viewer { width:100%; height:360px; border:1px solid var(--border-gray); border-radius:8px; overflow:hidden; }
.direction-footer { display:flex; justify-content:flex-end; gap:12px; }
.direction-instructions { font-size:14px; }
.angle-assign-wrapper { display:flex; gap:8px; align-items:center; }
</style>
