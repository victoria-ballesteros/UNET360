<template>
    <div class="menu-wrapper">
        <div class="search-wrapper">
            <UIcon v-if="!routeSearcherActive" name="icons/list" size="32" color="var(--fill-white)"
                :rotation="listIconRotation" @click="toggleMenu" class="menu-toggle-icon" />
            <input :value="searchBar" type="text" class="search-input" :placeholder="searcherInputPlaceholder"
                @input="handleSearchBar" />
            <UIcon v-if="!menuVisible" name="icons/route-arrow" size="32" color="var(--fill-white)"
                @click="toggleRouteSearcher" />
            <UIcon v-if="routeSearcherActive" name="icons/x-lg" size="26" color="var(--fill-white)"
                @click="toggleMenu" />
        </div>

        <div v-if="menuVisible" class="dropdown-menu-wrapper">
            <div v-if="Object.keys(searchResults ?? {}).length > 0" class="dropdown-menu">
                <div v-for="[key, value] in Object.entries(searchResults)" :key="key" class="menu-item"
                    @click="handleSearchClick(value, key)">
                    <span>{{ key }}</span>
                </div>
            </div>
            <div v-else-if="!routeSearcherActive" class="dropdown-menu">
                <div v-for="[label, icon] in Object.entries(menuOptions)" :key="label" class="menu-item"
                    @click="toggleMenu(label)">
                    <UIcon :name="'icons/' + icon" size="20" color="var(--fill-white)" />
                    <span>{{ label }}</span>
                </div>

                <template v-if="isAdmin">
                    <hr class="menu-separator" />
                    
                    <div class="menu-item text-warning" @click="toggleEditMapa">
                        <UIcon name="icons/edit" size="20" :color="isMapEditMode ? 'var(--main-blue)' : 'var(--main-yellow)'" />
                        <span>{{ isMapEditMode ? 'Guardar Cambios' : 'Editar Nodo Actual' }}</span>
                    </div>

                    <div v-if="isMapEditMode" class="menu-item text-danger" @click="cancelEditMapa">
                        <UIcon name="icons/x-lg" size="20" color="var(--main-red, #e53935)" />
                        <span>Cancelar Edición</span>
                    </div>
                </template>
            </div>
            
            <div v-else>
                <div class="route-searcher">
                    <div class="route-icons-container">
                        <UIcon name="icons/dot-inside-dot" size="20" />
                        <div class="three-dots-container">
                            <span>•</span>
                            <span>•</span>
                            <span>•</span>
                        </div>
                        <UIcon name="icons/point-sign" size="20" />
                    </div>

                    <div class="route-inputs-container">
                        <!-- Origen Input con Dropdown Custom -->
                        <div class="custom-select-container">
                            <input
                                ref="sourceInputRef"
                                :value="searchSource"
                                type="text"
                                class="route-input"
                                placeholder="Ingresa el origen"
                                @input="handleSource"
                                @focus="showSourceSuggestions = true"
                                @blur="showSourceSuggestions = false"
                                @keyup.enter="searchPath"
                            />
                            <button
                                type="button"
                                class="dropdown-arrow-btn"
                                @mousedown.prevent="toggleSourceDropdown"
                                @touchstart.prevent="toggleSourceDropdown"
                            >
                                <UIcon
                                    name="icons/chevron-down"
                                    size="12"
                                    color="var(--strong-gray)"
                                    :rotation="showSourceSuggestions ? 180 : 0"
                                />
                            </button>
                            <ul
                                v-if="showSourceSuggestions && Object.keys(sourceSuggestionsToDisplay).length > 0"
                                class="custom-suggestions-list"
                            >
                                <li
                                    v-for="(nodeName, displayName) in sourceSuggestionsToDisplay"
                                    :key="displayName"
                                    class="suggestion-item"
                                    @mousedown.prevent="selectSource(displayName)"
                                    @touchstart.prevent="selectSource(displayName)"
                                >
                                    {{ displayName }}
                                </li>
                            </ul>
                        </div>

                        <!-- Destino Input con Dropdown Custom -->
                        <div class="custom-select-container">
                            <input
                                ref="targetInputRef"
                                :value="searchTarget"
                                type="text"
                                class="route-input"
                                placeholder="Ingresa el destino"
                                @input="handleTarget"
                                @focus="showTargetSuggestions = true"
                                @blur="showTargetSuggestions = false"
                                @keyup.enter="searchPath"
                            />
                            <button
                                type="button"
                                class="dropdown-arrow-btn"
                                @mousedown.prevent="toggleTargetDropdown"
                                @touchstart.prevent="toggleTargetDropdown"
                            >
                                <UIcon
                                    name="icons/chevron-down"
                                    size="12"
                                    color="var(--strong-gray)"
                                    :rotation="showTargetSuggestions ? 180 : 0"
                                />
                            </button>
                            <ul
                                v-if="showTargetSuggestions && Object.keys(targetSuggestionsToDisplay).length > 0"
                                class="custom-suggestions-list"
                            >
                                <li
                                    v-for="(nodeName, displayName) in targetSuggestionsToDisplay"
                                    :key="displayName"
                                    class="suggestion-item"
                                    @mousedown.prevent="selectTarget(displayName)"
                                    @touchstart.prevent="selectTarget(displayName)"
                                >
                                    {{ displayName }}
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>

                <div class="route-button-container">
                    <button type="button" class="btn-start-route" @click="searchPath">
                        <UIcon name="icons/route" size="18" color="var(--fill-white)" />
                        <span>Comenzar viaje</span>
                    </button>
                </div>
            </div>
        </div>
    </div>
    <UToast ref="toastRef" />
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount, computed } from 'vue'
import UIcon from './UIcon.vue'
import UToast from './UToast.vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from "@/service/stores/auth";
import { searchNodeByKeyword } from '@/service/shared/utils';
import { fetchShortestPath } from '@/service/requests/graph';
import { useNodeStore } from "@/service/stores/nodes";

const router = useRouter();
const authStore = useAuthStore();

// --- Lógica de Edición ---
// Obtenemos el rol del usuario (Asumiendo que 'role' está en el objeto user)
// TODO: Ajusta 'admin' al valor real que devuelva tu API para este rol
const isAdmin = computed(() => {
    return authStore.user?.role === 'admin' || authStore.user?.role === 'ADMIN'; 
});

const isMapEditMode = ref(false);

const toggleEditMapa = () => {
    window.dispatchEvent(new CustomEvent('trigger-toggle-edit'));
    menuVisible.value = false; // Cerramos el menú después de hacer clic
    listIconRotation.value = 0;
};

const cancelEditMapa = () => {
    window.dispatchEvent(new CustomEvent('trigger-cancel-edit'));
    menuVisible.value = false; // Cerramos el menú
    listIconRotation.value = 0;
};

const syncEditMode = (e) => {
    isMapEditMode.value = e.detail;
};

onMounted(() => {
    window.addEventListener('map-edit-mode-changed', syncEditMode);
});

onBeforeUnmount(() => {
    window.removeEventListener('map-edit-mode-changed', syncEditMode);
});
// --- Fin Lógica de Edición ---

const menuVisible = ref(false)
const listIconRotation = ref(0)
const routeSearcherActive = ref(false)
const searcherInputPlaceholder = ref("Ej. Edificio A");

const showSourceSuggestions = ref(false);
const showTargetSuggestions = ref(false);
const sourceInputRef = ref(null);
const targetInputRef = ref(null);

const sourceValue = ref(null);
const targetValue = ref(null);

const route = ref([]);
const toastRef = ref(null);

const props = defineProps({
    searchSource: {
        type: String,
        required: true
    },
    searchTarget: {
        type: String,
        required: true
    },
    searchBar: {
        type: String,
        required: true
    },
    searchResults: {
        type: Object,
        required: false,
        default: () => ({})
    },
    actualRoute: {
        type: Object,
        required: true,
        default: () => ({})
    },
    actualNode: {
        type: Object,
        required: true,
        default: () => ({})
    },
    searchedNode: {
        type: String,
        default: ""
    }
});

const emit = defineEmits(['update:searchSource', 'update:searchTarget', 'update:searchBar', 'update:searchedNode', 'update:actualRoute'])

const nodeStore = useNodeStore();

// Genera un listado ordenado de sugerencias de ubicaciones y tags del sistema
const allSuggestionsList = computed(() => {
    const suggestions = {};
    if (!nodeStore.nodes) return suggestions;

    for (const node of nodeStore.nodes) {
        if (node.location && node.location.trim() !== '') {
            suggestions[node.location.trim()] = node.name;
        }

        if (node.tags && Object.keys(node.tags).length > 0) {
            for (const [_, value] of Object.entries(node.tags)) {
                for (const [tagKey, _] of Object.entries(value)) {
                    if (tagKey && tagKey.trim() !== '') {
                        suggestions[tagKey.trim()] = node.name;
                    }
                }
            }
        }
    }

    const sorted = {};
    Object.keys(suggestions)
        .sort((a, b) => a.localeCompare(b, undefined, { sensitivity: 'base' }))
        .forEach(key => {
            sorted[key] = suggestions[key];
        });

    return sorted;
});

// Filtra las sugerencias del origen
const sourceSuggestionsToDisplay = computed(() => {
    const query = props.searchSource || '';
    const queryClean = query.trim().toLowerCase();

    if (queryClean === '') {
        const list = { ...allSuggestionsList.value };
        if (props.actualNode && props.actualNode.name) {
            const sortedList = { "Posición actual": props.actualNode.name };
            Object.assign(sortedList, list);
            return sortedList;
        }
        return list;
    }

    const filtered = {};
    if (props.actualNode && props.actualNode.name && "posición actual".includes(queryClean)) {
        filtered["Posición actual"] = props.actualNode.name;
    }

    for (const [displayName, nodeName] of Object.entries(allSuggestionsList.value)) {
        if (displayName.toLowerCase().includes(queryClean)) {
            filtered[displayName] = nodeName;
        }
    }
    return filtered;
});

// Filtra las sugerencias del destino
const targetSuggestionsToDisplay = computed(() => {
    const query = props.searchTarget || '';
    const queryClean = query.trim().toLowerCase();

    if (queryClean === '') {
        return allSuggestionsList.value;
    }

    const filtered = {};
    for (const [displayName, nodeName] of Object.entries(allSuggestionsList.value)) {
        if (displayName.toLowerCase().includes(queryClean)) {
            filtered[displayName] = nodeName;
        }
    }
    return filtered;
});

const selectSource = (displayName) => {
    emit('update:searchSource', displayName);
    sourceValue.value = displayName;
    showSourceSuggestions.value = false;
};

const selectTarget = (displayName) => {
    emit('update:searchTarget', displayName);
    targetValue.value = displayName;
    showTargetSuggestions.value = false;
};

const toggleSourceDropdown = () => {
    showSourceSuggestions.value = !showSourceSuggestions.value;
    if (showSourceSuggestions.value) {
        sourceInputRef.value?.focus();
    }
};

const toggleTargetDropdown = () => {
    showTargetSuggestions.value = !showTargetSuggestions.value;
    if (showTargetSuggestions.value) {
        targetInputRef.value?.focus();
    }
};

const handleSource = (event) => {
    emit('update:searchSource', event.target.value);
    sourceValue.value = event.target.value;
    showSourceSuggestions.value = true;
}

const handleTarget = (event) => {
    emit('update:searchTarget', event.target.value);
    targetValue.value = event.target.value;
    showTargetSuggestions.value = true;
}

const handleSearchBar = (event) => {
    emit('update:searchBar', event.target.value)
}

const handleSearchClick = (value, displayName) => {
    emit('update:searchedNode', `${value}|${displayName}`)
}

function notify() {
    toastRef.value.showToast("¡Error!: por favor asegúrate de que los puntos entre los que te vas a trasladar sean válidos.");
}

const menuOptions = {
    "Ruta": "route-arrow",
    "Inicio": "house",
    "Acerca de": "about",
    "Cerrar sesión": "close-session"
}

const menuRouter = {
    "Ruta": "route-arrow",
    "Inicio": "Home",
    "Acerca de": "About",
    "Cerrar sesión": "About"
}

function toggleMenu(label = null) {
    menuVisible.value = !menuVisible.value
    listIconRotation.value = menuVisible.value ? 90 : 0
    routeSearcherActive.value = false
    searcherInputPlaceholder.value = "Ej. Edificio A"

    if (label === null || typeof label !== 'string') {
        return;
    }

    if (label === "Ruta") {
        toggleRouteSearcher();
    } else if (label === "Cerrar sesión") {
        authStore.logout();
        router.push({ name: 'Login' });
    } else {
        const route = menuRouter?.[label];
        if (route != undefined) {
            router.push({ name: route });
        }
    }
}

function toggleRouteSearcher() {
    menuVisible.value = true
    routeSearcherActive.value = !routeSearcherActive.value
    searcherInputPlaceholder.value = "Ruta"
    sourceValue.value = "Posición actual";
    emit('update:searchSource', sourceValue.value);
}

const resolveNodeId = (typedValue) => {
    if (!typedValue) return null;
    const cleanVal = typedValue.trim();
    const lowerVal = cleanVal.toLowerCase();

    // 1. "Posición actual" -> props.actualNode.name
    if (lowerVal === "posición actual" || lowerVal === "posicion actual" || lowerVal === "posicion_actual") {
        return props.actualNode?.name || null;
    }

    // 2. Coincidencia exacta por nombre de nodo (ej: "003")
    const exactNode = nodeStore.nodes.find(n => n.name.toLowerCase() === lowerVal);
    if (exactNode) return exactNode.name;

    // 3. Coincidencia por nombre de nodo corto/sin ceros (ej: "3" -> "003")
    const paddedNode = nodeStore.nodes.find(n => n.name.toLowerCase() === lowerVal.padStart(3, '0'));
    if (paddedNode) return paddedNode.name;

    // 4. Coincidencia exacta por nombre de ubicación (ej: "Edificio A")
    const exactLocationNode = nodeStore.nodes.find(n => n.location && n.location.toLowerCase() === lowerVal);
    if (exactLocationNode) return exactLocationNode.name;

    // 5. Coincidencia exacta por identificador o etiquetas de Tag
    for (const n of nodeStore.nodes) {
        if (n.tags && Object.keys(n.tags).length > 0) {
            for (const [_, tagObj] of Object.entries(n.tags)) {
                for (const [tagKey, customNames] of Object.entries(tagObj)) {
                    if (tagKey.toLowerCase() === lowerVal) {
                        return n.name;
                    }
                    if (Array.isArray(customNames)) {
                        if (customNames.some(name => String(name).toLowerCase() === lowerVal)) {
                            return n.name;
                        }
                    }
                }
            }
        }
    }

    // 6. Coincidencia parcial usando la función de palabras clave del sistema
    const matches = searchNodeByKeyword(cleanVal);
    const firstMatchKey = Object.keys(matches)[0];
    if (firstMatchKey) {
        return matches[firstMatchKey];
    }

    return null;
}

const searchPath = async () => {
    const sourceId = resolveNodeId(props.searchSource);
    const targetId = resolveNodeId(props.searchTarget);

    if (!sourceId || !targetId) {
        notify();
        return;
    }

    route.value = await fetchShortestPath(sourceId, targetId);
    if (route.value.status == true && route.value.response_obj.total_weight != 0) {
        emit('update:actualRoute', { 
            'route': route.value.response_obj.path, 
            'weight': parseFloat(route.value.response_obj.total_weight) * 10, 
            'targetTag': props.searchTarget 
        });
    } else {
        notify();
    }
    sourceValue.value = null;
    targetValue.value = null;
    emit('update:searchSource', '');
    emit('update:searchTarget', '');
}

watch(
    () => props.searchResults,
    (newVal, _) => {
        if (newVal == null || newVal == {}) {
            menuVisible.value = false;
            return;
        } else if (Object.keys(newVal).length > 0) {
            menuVisible.value = true;
            return;
        }

        menuVisible.value = false;
    },
    { deep: true }
);

watch(
    () => props.searchBar,
    (newVal, _) => {
        if (newVal.trim() !== '') {
            return;
        } else {
            menuVisible.value = false;
        }
    }
);

</script>

<style scoped lang="scss">
@import "@/assets/styles/pages/_input_card.scss";

// Pequeños estilos adicionales para las opciones de admin
.menu-separator {
    border: none;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    margin: 4px 10px;
}

.text-warning {
    color: var(--main-yellow, #ffeb3b);
}

.text-danger {
    color: var(--main-red, #e53935);
}
</style>