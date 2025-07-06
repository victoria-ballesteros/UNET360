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
        <transition name="expand-height" @enter="setAutoHeight" @after-enter="clearHeight" @leave="setAutoHeight"
            @after-leave="clearHeight">
            <div class="lower-container" :class="['lower-container', { 'transparent-bg': isImageLoaded }]"
                ref="lowerContainer" v-show="showLower">
                <p class="form-title"> {{ formTitle }} </p>
                <div class="form-container" ref="scrollContainer">
                    <div class="input-container" :class="{ 'has-error': inputErrors[input] }"
                        v-for="(input, index) in inputLabels" :key="index">
                        <p class="input-label" :class="{ 'label-disabled': inputDisabled[input] }">{{ input }}</p>
                        <UInput v-model="inputModels[input]" type="default" :placeholder="inputPlaceholders[input]"
                            :icon="inputIcon[input]" :iconRotation="index * 90" :disabled="inputDisabled[input]" />
                        <p v-if="inputErrors[input]" class="input-error-label"> {{ inputErrors[input] }}</p>
                    </div>
                    <div class="input-container" v-show="expandForm">
                        <p class="input-label">Datos opcionales</p>
                        <div class="tag-container">
                            <UIcon v-for="(tag, index) in tags" :key="index" :name="tag.icon_name" size="34"
                            :color="tagSelection[tag.name] ? 'var(--main-blue)' : 'var(--border-gray)'"
                            @click="() => tagSelection[tag.name] = !tagSelection[tag.name]" />
                        </div>
                    </div>
                </div>
                <div class="button-container">
                    <UButton text='Cancelar' @click="handleCancelEvent" type="tertiary" />
                    <UButton :text='actionButton' @click.stop="handleFormExpansion" :type="buttonType" />
                </div>
            </div>
        </transition>
    </div>
</template>

<script setup>
import UButton from '@/components/UButton.vue'
import UInput from '@/components/UInput.vue'
import UIcon from '@/components/UIcon.vue';

import { ref, computed, reactive, watch, nextTick, onMounted, onBeforeUnmount } from 'vue';
import { Viewer } from '@photo-sphere-viewer/core'
import '@photo-sphere-viewer/core/index.css'

// COMPONENTS VARIABLES
const formTitle = ref('Ingrese los datos de la nueva ubicación')
const lowerContainer = ref(null);
const showLower = ref(true)
const actionButton = ref('Continuar')
const expandForm = ref(false)

function setAutoHeight(el) {
  el.style.height = el.scrollHeight + 'px';
}

function clearHeight(el) {
  el.style.height = '';
}

// 360 SHOWCASE POC
const viewerContainer = ref(null)
const isImageLoaded = ref(false)
const imageFile = ref(null)
let viewer = null

// SAVED INFORMATION
import { useNodeStore } from '../service/stores/nodes'
import { useTagStore } from '@/service/stores/tags';
const nodeStore = useNodeStore()
const nodes = computed(() => nodeStore.nodes)
const tagStore = useTagStore()
const tags = computed(() => tagStore.tags)

// NODES CONNECTIONS INPUTS FUNCTIONS
const buttonType = ref('deactivated')

const inputLabels = reactive(['Nodo siguiente', 'Nodo derecho', 'Nodo anterior', 'Nodo izquierdo']);
const inputPlaceholders = {};
const inputModels = reactive({});
const inputErrors = reactive({});
const inputDisabled = reactive({});
const inputIcon = reactive({});

inputLabels.forEach(label => {
    inputPlaceholders[label] = `Identificación del ${label.toLowerCase()}`;
    inputModels[label] = '';
    inputErrors[label] = '';
    inputDisabled[label] = false;
    inputIcon[label] = 'arrow-up';
});

function checkIfReadyToSubmit() {
    const allFilled = Object.values(inputModels).every(value => value?.trim() !== '')
    const noErrors = Object.values(inputErrors).every(error => error === '')
    buttonType.value = (allFilled && noErrors && imageFile) ? 'primary' : 'deactivated'
}

inputLabels.forEach(label => {
    watch(
        () => inputModels[label],
        (newVal) => {
            const exists = nodes?.value.some(node => node.name === newVal?.trim())
            inputErrors[label] = exists ? '' : 'El nodo no existe'
            checkIfReadyToSubmit()
        }
    );
}, { immediate: true, deep: true });

// FILE UPLOAD FUNCTIONS

const fileInput = ref(null)

function openUploadFileDialog() {
    fileInput.value?.click()
}

function handleFileChange(event) {
    const file = event.target.files[0]
    if (file && file.type.startsWith('image/')) {
        imageFile.value = file
        const url = URL.createObjectURL(file)
        showLower.value = false
            nextTick(() => {
                showLower.value = true
            })
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

// FORM BUTTONS FUNCTIONS

function handleCancelEvent() {

}

const scrollContainer = ref(null)

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

// TAG-CONTAINER FUNCTIONS

const tagSelection = reactive({})
watch(
  tags,
  (newTags) => {
    if (Array.isArray(newTags)) {
      newTags.forEach(tag => {
        tagSelection[tag.name] = false;
      });
    }
  },
  { immediate: true }
)

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
.background-viewer {
    position: fixed;
    width: 100vw;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 0;
    pointer-events: none;
    overflow: hidden;
}

.fade-panorama-enter-active,
.fade-panorama-leave-active {
    transition: opacity 1.2s ease;
}

.fade-panorama-enter-from,
.fade-panorama-leave-to {
    opacity: 0;
}

.fade-panorama-enter-to,
.fade-panorama-leave-from {
    opacity: 1;
}

.expand-height-enter-active,
.expand-height-leave-active {
  transition: max-height 0.4s ease, opacity 0.4s ease;
  overflow: hidden;
}
.expand-height-enter-from,
.expand-height-leave-to {
  max-height: 0;
  opacity: 0;
}
.expand-height-enter-to,
.expand-height-leave-from {
  max-height: 999px;
  opacity: 1;
}

.outer-container {
    height: 100%;
    max-height: 100%;

    display: flex;
    flex-direction: column;

    gap: 12px;

    overflow-y: hidden;

    position: relative;
    z-index: 1;

    .upper-container {
        padding: 24px 12px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;

        flex: 1;

        .icons-container {
            width: 100%;
            display: flex;
            justify-content: space-between;

            .pair-container {
                display: flex;
                gap: 0.25rem;
            }
        }
    }

    .lower-container {
        background: var(--fill-white);
        padding: 9px 36px 18px 36px;
        border-radius: 56px 56px 0px 0px;
        min-height: 0;

        display: flex;
        flex-direction: column;
        align-items: center;

        transition: opacity 0.4s ease, max-height 0.4s ease, background 0.4s ease;

        &.transparent-bg {
            background: rgba(255, 255, 255, 0.82);
        }

        .form-title {
            @include section-title;
            color: var(--strong-gray);
            width: 100%;
        }

        .form-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.25rem;
            width: 100%;
            margin: 0rem 0rem 0.625rem 0rem;

            overflow-y: scroll;
            flex-grow: 1;
            min-height: 0;

            .input-container {
                width: 100%;

                display: flex;
                flex-direction: column;
                padding: 0rem 0rem 2.063rem 0rem;

                .input-label {
                    @include paragraph-medium;
                    color: var(--strong-gray);
                    width: 100%;
                }

                .label-disabled {
                    color: var(--border-gray);
                }

                .input-error-label {
                    @include paragraph-extra-small;
                    color: var(--main-red);
                    width: 100%;
                }

                .tag-container {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }

                &.has-error {
                    padding-bottom: 0rem;
                }
            }
        }

        .button-container {
            display: flex;
            gap: 0.75rem;
        }
    }
}
</style>