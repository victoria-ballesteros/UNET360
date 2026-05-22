<template>
    <div ref="wrapperEl" :class="[
        'uselect-wrapper',
        `uselect-wrapper--${styleType}`,
        { 'uselect-wrapper--has-value': modelValue && modelValue.length > 0 },
        { 'uselect-wrapper--open': isOpen },
        { 'uselect-wrapper--disabled': disabled },
    ]" @click="toggle">
        <!-- Valor mostrado / placeholder -->
        <span class="uselect-display">
            {{ modelValue || placeholder }}
        </span>

        <!-- Chevron -->
        <UIcon name="icons/chevron-down" :size="16"
            :color="styleType === 'dark' ? 'rgba(255,255,255,0.4)' : 'var(--border-gray)'" class="uselect-chevron"
            :class="{ 'uselect-chevron--open': isOpen }" />

        <!-- Dropdown -->
        <Transition name="uselect-fade">
            <ul v-if="isOpen" class="uselect-dropdown" @click.stop>
                <li v-for="option in options" :key="option" class="uselect-option"
                    :class="{ 'uselect-option--selected': option === modelValue }" @click="select(option)">
                    {{ option }}
                    <UIcon v-if="option === modelValue" name="icons/check" :size="14" color="var(--main-yellow)"
                        class="uselect-check" />
                </li>
            </ul>
        </Transition>
    </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import UIcon from './UIcon.vue';

const props = defineProps({
    modelValue: {
        type: String,
        default: '',
    },
    styleType: {
        type: String,
        default: 'default',
    },
    placeholder: {
        type: String,
        default: 'Selecciona una opción',
    },
    options: {
        type: Array,
        default: () => [],
    },
    disabled: {
        type: Boolean,
        default: false,
    },
});

const emit = defineEmits(['update:modelValue']);

const isOpen = ref(false);
const wrapperEl = ref(null);

function toggle() {
    if (props.disabled) return;
    isOpen.value = !isOpen.value;
}

function select(option) {
    emit('update:modelValue', option);
    isOpen.value = false;
}

function onClickOutside(e) {
    if (wrapperEl.value && !wrapperEl.value.contains(e.target)) {
        isOpen.value = false;
    }
}

onMounted(() => document.addEventListener('mousedown', onClickOutside));
onBeforeUnmount(() => document.removeEventListener('mousedown', onClickOutside));
</script>

<style scoped lang="scss">
// ── Base wrapper ──────────────────────────────────────────
.uselect-wrapper {
    background: var(--fill-gray);
    border-radius: 12px;
    padding: 0.938rem 1rem;
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 0.5rem;
    width: 100%;
    box-sizing: border-box;
    cursor: pointer;
    position: relative;
    user-select: none;
}

.uselect-display {
    flex: 1;
    min-width: 0;
    @include paragraph-small;
    color: var(--border-gray);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.uselect-wrapper--has-value .uselect-display {
    color: var(--strong-gray);
}

.uselect-wrapper--disabled {
    pointer-events: none;
    opacity: 0.5;
}

.uselect-chevron {
    flex-shrink: 0;
    transition: transform 0.2s ease;

    &--open {
        transform: rotate(180deg);
    }
}

// ── Dropdown ──────────────────────────────────────────────
.uselect-dropdown {
    position: absolute;
    top: calc(100% + 6px);
    left: 0;
    right: 0;
    z-index: 999;
    list-style: none;
    margin: 0;
    padding: 0.375rem;
    border-radius: 12px;
    background: var(--fill-gray);
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    max-height: 220px;
    overflow-y: auto;

    &::-webkit-scrollbar {
        width: 4px;
    }

    &::-webkit-scrollbar-track {
        background: transparent;
    }

    &::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 2px;
    }
}

.uselect-option {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.625rem 0.75rem;
    border-radius: 8px;
    @include paragraph-small;
    color: rgba(255, 255, 255, 0.65);
    cursor: pointer;
    transition: background 0.15s ease, color 0.15s ease;

    &:hover {
        background: rgba(255, 255, 255, 0.06);
        color: var(--full-white);
    }

    &--selected {
        color: var(--main-yellow);
        background: rgba(255, 239, 61, 0.07);
    }
}

.uselect-check {
    flex-shrink: 0;
}

// ── Transition ────────────────────────────────────────────
.uselect-fade-enter-active,
.uselect-fade-leave-active {
    transition: opacity 0.15s ease, transform 0.15s ease;
}

.uselect-fade-enter-from,
.uselect-fade-leave-to {
    opacity: 0;
    transform: translateY(-4px);
}

// ── Dark variant ──────────────────────────────────────────
.uselect-wrapper--dark {
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.12);
    transition: border-color 0.2s ease, box-shadow 0.2s ease;

    &:hover {
        border-color: rgba(255, 239, 61, 0.3);
    }

    &.uselect-wrapper--open {
        border-color: var(--main-yellow);
        box-shadow: 0 0 0 2px rgba(255, 239, 61, 0.1);
    }

    .uselect-display {
        color: rgba(255, 255, 255, 0.35);
    }

    &.uselect-wrapper--has-value .uselect-display {
        color: var(--full-white);
    }

    .uselect-dropdown {
        background: #1a1a1a;
        border-color: rgba(255, 255, 255, 0.1);
    }

    &.uselect-wrapper--disabled {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(255, 255, 255, 0.08);
    }
}
</style>