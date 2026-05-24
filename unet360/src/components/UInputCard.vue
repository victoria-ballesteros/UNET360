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
                <div v-for="[key, value] in Object.entries(searchResults)" :key="label" class="menu-item"
                    @click="handleSearchClick(value)">
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
            
            <div v-else class="route-searcher">
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
                    <input :value="searchSource" type="text" class="route-input" placeholder="Ingresa el origen"
                        @input="handleSource" list="source-suggestions" />

                    <datalist id="source-suggestions">
                        <option v-for="(value, key) in routeSearcherResult" :key="key" :value="key">
                            {{ value }}
                        </option>
                    </datalist>

                    <input :value="searchTarget" type="text" class="route-input" placeholder="Ingresa el destino"
                        @input="handleTarget" list="source-suggestions-2" />

                    <datalist id="source-suggestions-2">
                        <option v-for="(value, key) in routeSearcherTargetResult" :key="key" :value="key">
                            {{ value }}
                        </option>
                    </datalist>
                </div>
                <UIcon name="icons/check-square-fill" size="23" @click="searchPath" />
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

const routeSearcherResult = ref({});
const routeSearcherTargetResult = ref({});

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

const handleSource = (event) => {
    emit('update:searchSource', event.target.value);
    routeSearcherResult.value = searchNodeByKeyword(event.target.value);
    routeSearcherResult.value["Posición actual"] = props.actualNode.name;
    routeSearcherResult.value = { ...routeSearcherResult.value };
    sourceValue.value = event.target.value;
}

const handleTarget = (event) => {
    emit('update:searchTarget', event.target.value)
    routeSearcherTargetResult.value = searchNodeByKeyword(event.target.value);
    targetValue.value = event.target.value;
}

const handleSearchBar = (event) => {
    emit('update:searchBar', event.target.value)
}

const handleSearchClick = (value) => {
    emit('update:searchedNode', value)
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
    routeSearcherResult.value["Posición actual"] = props.actualNode.name;
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

    const nodeStore = useNodeStore();

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
    routeSearcherResult.value = {};
    routeSearcherTargetResult.value = {};
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