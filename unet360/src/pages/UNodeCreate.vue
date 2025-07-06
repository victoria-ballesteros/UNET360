<template>
    <transition name="fade-panorama">
        <div v-show="isImageLoaded" ref="viewerContainer" class="background-viewer" />
    </transition>
    <div class="outer-container">
        <div v-if="!imageFile" class="upper-container">
            <UButton text='Subir imagen' @click="openUploadFileDialog" type="secondary" icon="cloud-upload" />
            <input type="file" ref="fileInput" style="display: none" @change="handleFileChange" />
            <div class="icons-container">
                <div class="pair-container">
                    <UIcon name="star" size="22" color="var(--strong-gray)" :rotation="15" />
                    <UIcon name="star" size="15" color="var(--strong-gray)" :rotation="22" />
                </div>
                <UIcon name="star" size="22" color="var(--strong-gray)" />
            </div>
        </div>
        <div class="lower-container" :class="['lower-container', { 'transparent-bg': isImageLoaded }]"
            ref="lowerContainer">
            <p class="form-title"> {{ formTitle }} </p>
            <div class="form-container" ref="scrollContainer">
                <div class="input-container" :class="{ 'has-error': inputErrors[input] }"
                    v-for="(input, index) in inputLabels" :key="index">
                    <p class="input-label" :class="{ 'label-disabled': inputDisabled[input] }">{{ input }}</p>
                    <div class="node-input-container">
                        <UInput v-model="inputModels[input]" styleType="default" :placeholder="inputPlaceholders[input]"
                            :icon="inputIcon[input]" :iconRotation="index * 90" :disabled="inputDisabled[input]"
                            @input="() => inputTouched[input] = true" />
                        <UInput v-if="inputWeightModels[input] != null" v-model="inputWeightModels[input]" styleType="default" :disabled="inputDisabled[input]"
                            type="text" inputmode="numeric" pattern="[0-9.]*" placeholder="Peso"
                            @input="() => inputTouched[input] = true" />
                    </div>
                    <p v-if="inputErrors[input]" class="input-error-label"> {{ inputErrors[input] }}</p>
                </div>
                <div class="input-container" v-show="expandForm">
                    <p class="input-label">Datos opcionales</p>
                    <div class="tag-container">
                        <UIcon v-for="(tag, index) in tags" :key="index" :name="tag.icon_name" size="34"
                            :color="tagSelection[tag.name] ? 'var(--main-blue)' : 'var(--border-gray)'"
                            @click="handleTagClick(tag.name)" />
                    </div>
                </div>
            </div>
            <div class="button-container">
                <UButton text='Cancelar' @click="handleCancelEvent" type="tertiary" />
                <UButton :text='actionButton' @click.stop="handleFormExpansion" :type="buttonType" />
            </div>
        </div>
    </div>

    <UDialog v-model="showDialog" headerTitle="Identificación del tag">
        <div class="tag-dialog-content">
            <UInput v-model="tagCustomName[actualTagSelected]" styleType="default" placeholder="Baño oeste" />
            <UButton style="align-self: flex-end;" text='Aceptar' @click="handleTagCustomization"
                :type="dialogButtonType" />
        </div>
    </UDialog>
</template>

<script setup>
import { ref, computed, reactive, watch, nextTick, onMounted, onBeforeUnmount } from 'vue';
import UButton from '@/components/UButton.vue'
import UInput from '@/components/UInput.vue'
import UIcon from '@/components/UIcon.vue';
import UDialog from '@/components/UDialog.vue';

import { useNodeStore } from '../service/stores/nodes'
import { useTagStore } from '@/service/stores/tags';

import { Viewer } from '@photo-sphere-viewer/core'
import '@photo-sphere-viewer/core/index.css'

// ═══════════════  Components variables  ═══════════════

const formTitle = ref('Ingrese los datos de la nueva ubicación');
const lowerContainer = ref(null);
const showLower = ref(true);
const actionButton = ref('Continuar');
const buttonType = ref('deactivated');
const expandForm = ref(false);
const showDialog = ref(false);
const scrollContainer = ref(null);
const actualTagSelected = ref('');
const dialogButtonType = ref('deactivated');


// ═══════════════  360 viewer  ═══════════════

const viewerContainer = ref(null)
const isImageLoaded = ref(false)
const imageFile = ref(false)
let viewer = null

// ═══════════════  360 stores  ═══════════════

const nodeStore = useNodeStore()
const tagStore = useTagStore()
const nodes = computed(() => nodeStore.nodes)
const tags = computed(() => tagStore.tags)

// ═══════════════  Nodes validations  ═══════════════


const inputLabels = reactive(['Nodo siguiente', 'Nodo derecho', 'Nodo anterior', 'Nodo izquierdo']);
const inputPlaceholders = {};
const inputModels = reactive({});
const inputWeightModels = reactive({});
const inputErrors = reactive({});
const inputDisabled = reactive({});
const inputIcon = reactive({});

inputLabels.forEach(label => {
    inputPlaceholders[label] = `Id. del ${label.toLowerCase()}`;
    inputModels[label] = '';
    inputWeightModels[label] = '';
    inputErrors[label] = '';
    inputDisabled[label] = false;
    inputIcon[label] = 'arrow-up';
});

function checkIfReadyToSubmit() {
    const allFilled = Object.values(inputModels).every(value => value?.trim() !== '')
    const noErrors = Object.values(inputErrors).every(error => error === '')
    buttonType.value = (allFilled && noErrors && imageFile.value) ? 'primary' : 'deactivated'
}

const inputTouched = reactive({})
inputLabels.forEach(label => {
    inputTouched[label] = false
})

inputLabels.forEach(label => {
    watch(
        [() => inputModels[label], () => inputWeightModels[label]],
        ([newVal, newWeight]) => {
            if (!inputTouched[label]) {
                return
            }
            const trimmed = newVal?.trim()
            const exists = nodes.value?.some(node => node.name === trimmed)
            if (!exists && trimmed) {
                inputErrors[label] = 'El nodo no existe'
            } else if (!newWeight?.toString().trim() && trimmed) {
                inputErrors[label] = 'El peso no puede estar vacío'
            } else {
                inputErrors[label] = ''
            }

            checkIfReadyToSubmit()
        },
        { immediate: true }
    )
})

// ═══════════════  Image upload validation  ═══════════════

const fileInput = ref(null)

function openUploadFileDialog() {
    fileInput.value?.click()
}

async function handleFileChange(event) {
    const file = event.target.files[0]
    if (file && file.type.startsWith('image/')) {
        imageFile.value = file
        const url = URL.createObjectURL(file)
        viewer.setPanorama(url).then(() => {
            viewer.animate({
                yaw: Math.PI / 2,
                pitch: '20deg',
                zoom: 50,
                speed: '2rpm',
            });
            isImageLoaded.value = true
            checkIfReadyToSubmit()
        })
    }
}

function handleCloseViewer() {
    isImageLoaded.value = false

    setTimeout(() => {
        if (viewer) {
            viewer.destroy()
            viewer = null
        }
    }, 800)
}

// ═══════════════  Form buttons  ═══════════════

function handleCancelEvent() {

}

async function handleFormExpansion() {
    handleCloseViewer()

    formTitle.value = 'Nodo verificado'
    inputLabels.forEach(label => {
        inputDisabled[label] = true;
    });

    inputLabels.push('Identificación')
    inputPlaceholders['Identificación'] = 'Identificación del nodo actual';
    inputModels['Identificación'] = '';
    inputErrors['Identificación'] = '';
    inputDisabled['Identificación'] = false;
    buttonType.value = 'deactivated';
    actionButton.value = 'Subir nodo';
    expandForm.value = true;

    await nextTick()

    if (scrollContainer.value) {
        scrollContainer.value.scrollTo({
            top: scrollContainer.value.scrollHeight,
            behavior: 'smooth'
        })
    }

    watch(
        () => inputModels['Identificación'],
        (newVal) => {
            const exists = nodes.value.some(node => node.name === newVal?.trim())
            inputErrors['Identificación'] = exists ? 'El nodo ya existe' : ''
            checkIfReadyToSubmit()
        }
    )
}

// ═══════════════  Tag handling  ═══════════════

const tagSelection = reactive({})
const tagCustomName = reactive({})

watch(
    tags,
    (newTags) => {
        if (Array.isArray(newTags)) {
            newTags.forEach(tag => {
                tagSelection[tag.name] = false;
                tagCustomName[tag.name] = '';
            });
        }
    },
    { immediate: true }
)

let stopWatching = null

function handleTagClick(tagName) {
    actualTagSelected.value = tagName
    showDialog.value = true
    tagSelection[tagName] = true;

    if (!stopWatching) {
        stopWatching = watch(
            () => tagCustomName[actualTagSelected.value],
            (newInput) => {
                dialogButtonType.value = newInput?.trim()
                    ? 'primary'
                    : 'deactivated';
            }
        )
    }
}

const tagSubmited = ref(false)

async function handleTagCustomization() {
    tagSubmited.value = true
    showDialog.value = false;

    if (!tagCustomName[actualTagSelected.value]) {
        tagSelection[actualTagSelected.value] = false
    }
    await nextTick()
    tagSubmited.value = false
}

watch(showDialog, (newVal, oldVal) => {
    if (!newVal && !tagSubmited.value) {
        tagSelection[actualTagSelected.value] = false
        tagCustomName[actualTagSelected.value] = ''
        tagSubmited.value = false
    }
})

// ═══════════════  Page state related functions  ═══════════════

onMounted(() => {
    viewer = new Viewer({
        container: viewerContainer.value,
        panorama: '',
        navbar: false,
        mousewheel: false,
        keyboard: false,
    });
})

onBeforeUnmount(() => {
    handleCloseViewer()
})

</script>

<style scoped lang="scss">
@import '@/assets/styles/pages/_node_create.scss'
</style>