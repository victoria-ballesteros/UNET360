<template>
  <div class="al-root">

    <!-- ── Toolbar: Search + Sort ── -->
    <div v-if="(showSearch || showSort) && !loading" class="al-toolbar">
      <div v-if="showSearch" class="al-search-wrap">
        <svg class="al-search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
          <circle cx="11" cy="11" r="7"/><path d="m21 21-4.35-4.35"/>
        </svg>
        <input
          v-model="internalSearch"
          type="text"
          class="al-search-input"
          :placeholder="searchPlaceholder"
        />
      </div>

      <div v-if="showSort" class="al-sort-toggle">
        <UButton
          class="al-sort-btn"
          :class="{ active: sortOrder === 'asc' }"
          text="A–Z"
          @click="sortOrder = 'asc'"
          title="A → Z"
        />
        <UButton
          class="al-sort-btn"
          :class="{ active: sortOrder === 'desc' }"
          text="Z–A"
          @click="sortOrder = 'desc'"
          title="Z → A"
        />
      </div>
    </div>

    <!-- ── Loading state (Skeleton Loader) ── -->
    <div v-if="loading" class="al-list-wrap al-skeleton-wrap">
      <div class="al-items-container">
        <div v-for="n in pageSize" :key="n" class="al-skeleton-item">
          <div class="al-skeleton-primary">
            <div class="al-skeleton-icon"></div>
            <div class="al-skeleton-text"></div>
          </div>
          <div class="al-skeleton-actions">
            <div class="al-skeleton-btn"></div>
            <div class="al-skeleton-btn"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- ── Empty state ── -->
    <div v-else-if="processedItems.length === 0" class="al-empty">
      {{ items.length === 0 ? emptyMessage : noResultsMessage }}
    </div>

    <!-- ── List + Pagination ── -->
    <div v-else class="al-list-wrap">
      <div class="al-items-container">
        <template v-for="(item, idx) in paginatedItems" :key="resolveKey(item)">
          <slot name="item" :item="item" :index="idx" />
          <div v-if="idx !== paginatedItems.length - 1" class="al-separator" />
        </template>
      </div>

      <div v-if="totalPages > 1" class="al-pagination">
        <UButton
          class="al-page-btn"
          type="secondary"
          size="sm"
          text="← Anterior"
          :disabled="currentPage === 1"
          @click="goToPage(currentPage - 1)"
        />
        <span class="al-page-info">{{ currentPage }} / {{ totalPages }}</span>
        <UButton
          class="al-page-btn"
          type="secondary"
          size="sm"
          text="Siguiente →"
          :disabled="currentPage === totalPages"
          @click="goToPage(currentPage + 1)"
        />
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';
import UButton from './UButton.vue';

const props = defineProps({
  /** Array de items a mostrar */
  items: { type: Array, default: () => [] },

  /** Indicar si está cargando para mostrar skeleton loader */
  loading: { type: Boolean, default: false },

  /** Campos del objeto a buscar (e.g. ['name', 'email']) */
  searchFields: { type: Array, default: () => ['name'] },

  /** Placeholder del input de búsqueda */
  searchPlaceholder: { type: String, default: 'Buscar...' },

  /** Mensaje cuando el array items está vacío */
  emptyMessage: { type: String, default: 'No hay elementos.' },

  /** Mensaje cuando la búsqueda no encuentra resultados */
  noResultsMessage: { type: String, default: 'No se encontraron resultados.' },

  /** Mostrar el input de búsqueda */
  showSearch: { type: Boolean, default: true },

  /** Mostrar los botones de ordenación A-Z / Z-A */
  showSort: { type: Boolean, default: true },

  /**
   * Función de ordenación personalizada.
   * Firma: (items: Array, direction: 'asc' | 'desc') => Array
   * Si no se pasa, ordena alfabéticamente por `name`.
   */
  sortFn: { type: Function, default: null },

  /** Campo a usar como key única del v-for */
  itemKeyField: { type: String, default: 'name' },
});

// ── Estado interno ─────────────────────────────────────────────────────────
const internalSearch = ref('');
const sortOrder      = ref('asc');
const currentPage    = ref(1);
const pageSize       = ref(10);

// ── Helpers ────────────────────────────────────────────────────────────────
const resolveKey = (item) => item[props.itemKeyField] ?? JSON.stringify(item);

// ── Computeds ──────────────────────────────────────────────────────────────
const sortedItems = computed(() => {
  if (props.sortFn) return props.sortFn(props.items, sortOrder.value);
  return [...props.items].sort((a, b) => {
    const na = String(a.name ?? '').toLowerCase();
    const nb = String(b.name ?? '').toLowerCase();
    return sortOrder.value === 'asc' ? na.localeCompare(nb) : nb.localeCompare(na);
  });
});

const processedItems = computed(() => {
  const q = internalSearch.value.trim().toLowerCase();
  if (!q) return sortedItems.value;
  return sortedItems.value.filter(item =>
    props.searchFields.some(field =>
      String(item[field] ?? '').toLowerCase().includes(q)
    )
  );
});

const totalPages = computed(() =>
  Math.max(1, Math.ceil(processedItems.value.length / pageSize.value))
);

const paginatedItems = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  return processedItems.value.slice(start, start + pageSize.value);
});

// ── Watchers ───────────────────────────────────────────────────────────────
watch([internalSearch, sortOrder], () => { currentPage.value = 1; });
watch(totalPages, (val) => {
  if (currentPage.value > val) currentPage.value = Math.max(1, val);
});

// ── Paginación ─────────────────────────────────────────────────────────────
const goToPage = (p) => {
  if (p >= 1 && p <= totalPages.value) currentPage.value = p;
};

// ── Cálculo responsive de pageSize ─────────────────────────────────────────
const calculatePageSize = () => {
  if (window.innerWidth < 768) { pageSize.value = 10; return; }
  const offsetHeight   = 380; // Header + toolbar + padding + paginación + footer + layout margins
  const itemHeight     = 65;  // Alto de una fila contraída
  const available      = window.innerHeight - offsetHeight;
  pageSize.value       = Math.max(4, Math.floor(available / itemHeight));
};

onMounted(() => {
  calculatePageSize();
  window.addEventListener('resize', calculatePageSize);
});

onUnmounted(() => {
  window.removeEventListener('resize', calculatePageSize);
});
</script>

<style lang="scss" scoped>
// ══════════════════════════════════════════════════
// ═══  UAdminList — estilos del componente        ═══
// ══════════════════════════════════════════════════

.al-root {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  flex: 1;
  min-height: 0;
}

// ── Toolbar ───────────────────────────────────────
.al-toolbar {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  justify-content: space-between;
  flex-shrink: 0;
}

.al-search-wrap {
  flex: 1;
  position: relative;
  display: flex;
  align-items: center;
}

.al-search-icon {
  position: absolute;
  left: 0.75rem;
  width: 1rem;
  height: 1rem;
  color: rgba(255, 255, 255, 0.3);
  pointer-events: none;
  flex-shrink: 0;
}

.al-search-input {
  width: 100%;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  padding: 0.6rem 1rem 0.6rem 2.25rem;
  color: var(--full-white);
  outline: none;
  font-size: 0.875rem;
  font-weight: 400;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;

  &::placeholder { color: rgba(255, 255, 255, 0.25); }

  &:focus {
    border-color: rgba(255, 239, 61, 0.4);
    box-shadow: 0 0 0 3px rgba(255, 239, 61, 0.08);
  }
}

// ── Sort toggle ───────────────────────────────────
.al-sort-toggle {
  display: flex;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  overflow: hidden;
  flex-shrink: 0;
}

.al-sort-btn {
  // Override UButton scoped styles via :deep()
  :deep(.ub) {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.55rem 0.85rem;
    background: rgba(255, 255, 255, 0.04);
    border: none;
    border-radius: 0;
    color: rgba(255, 255, 255, 0.4);
    cursor: pointer;
    font-size: 0.7rem;
    font-weight: 400;
    letter-spacing: 0.04em;
    transition: background 0.15s ease, color 0.15s ease;
    box-shadow: none;

    &:hover:not(:disabled) {
      transform: none;
      background: rgba(255, 255, 255, 0.08);
      color: rgba(255, 255, 255, 0.7);
      border-color: transparent;
      box-shadow: none;
    }

    &:active:not(:disabled) {
      transform: none;
    }
  }

  &:first-child :deep(.ub) {
    border-right: 1px solid rgba(255, 255, 255, 0.08);
  }

  &.active :deep(.ub) {
    background: rgba(255, 239, 61, 0.1);
    color: var(--main-yellow);
  }
}

// ── Empty state ───────────────────────────────────
.al-empty {
  color: rgba(255, 255, 255, 0.35);
  text-align: center;
  padding: 3rem 1rem;
  font-size: 0.9rem;
  font-weight: 400;
}

// ── List container (scroll interno) ───────────────
.al-list-wrap {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 14px;
  overflow-y: auto;
  background: var(--strong-gray-dark, #252932); // Superpuesto sobre el fondo decorativo

  // Scrollbar sutil
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.12) transparent;

  &::-webkit-scrollbar       { width: 4px; }
  &::-webkit-scrollbar-track { background: transparent; }
  &::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.12); border-radius: 4px; }
}

.al-items-container {
  display: flex;
  flex-direction: column;
  flex: 1;
}

// ── Separador entre filas ─────────────────────────
.al-separator {
  width: calc(100% - 2.5rem);
  margin: 0 1.25rem;
  height: 1px;
  background: rgba(255, 255, 255, 0.06);
  flex-shrink: 0;
}

// ── Paginación ────────────────────────────────────
.al-pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  padding: 0.65rem 0;
  flex-shrink: 0;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  background: rgba(255, 255, 255, 0.02);
  position: sticky;
  bottom: 0;
}

.al-page-btn {
  // Override UButton scoped styles via :deep()
  :deep(.ub) {
    background: rgba(255, 255, 255, 0.05);
    color: var(--full-white);
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 0.4rem 1rem;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.75rem;
    font-weight: 400;
    transition: background 0.15s ease;
    box-shadow: none;

    &:hover:not(:disabled) {
      background: rgba(255, 255, 255, 0.1);
      transform: none;
      border-color: rgba(255, 255, 255, 0.1);
      color: var(--full-white);
      box-shadow: none;
    }

    &:active:not(:disabled) {
      transform: none;
    }

    &:disabled {
      opacity: 0.25;
      cursor: not-allowed;
    }
  }
}

.al-page-info {
  color: rgba(255, 255, 255, 0.4);
  font-size: 0.75rem;
  min-width: 3.5rem;
  text-align: center;
}

// ── Skeleton Loader ───────────────────────────────
.al-skeleton-wrap {
  pointer-events: none;
  background: var(--strong-gray-dark, #252932);
}

.al-skeleton-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.875rem 1.25rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);

  &:last-child {
    border-bottom: none;
  }
}

.al-skeleton-primary {
  display: flex;
  align-items: center;
  gap: 0.875rem;
}

.al-skeleton-icon {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.06);
  animation: alSkeletonPulse 1.5s ease-in-out infinite;
}

.al-skeleton-text {
  width: 130px;
  height: 16px;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.06);
  animation: alSkeletonPulse 1.5s ease-in-out infinite;
}

.al-skeleton-actions {
  display: flex;
  gap: 0.5rem;
}

.al-skeleton-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  animation: alSkeletonPulse 1.5s ease-in-out infinite;
}

@keyframes alSkeletonPulse {
  0%, 100% {
    opacity: 0.35;
  }
  50% {
    opacity: 0.75;
  }
}
</style>
