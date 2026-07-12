<template>
  <div class="doc-container">

    <!-- ── Header ── -->
    <header class="doc-header">
      <p class="header-overline">Guía para administradores</p>
      <h2>Documentación</h2>
      <p class="doc-subtitle">
        Proceso completo para capturar, procesar y publicar un nuevo nodo dentro del recorrido 360°.
      </p>
    </header>

    <!-- ── Pasos (carrusel horizontal con snap) ── -->
    <div class="doc-carousel">
      <div
        ref="trackRef"
        class="doc-steps"
        @scroll="onScroll"
        @wheel="onWheel"
      >
        <section
          v-for="(step, idx) in extendedSteps"
          :key="step.isClone ? step.cloneId : step.number"
          class="doc-step"
          :class="{ 
            'is-active': getActiveIndexForCard(step, idx),
            'is-clone': step.isClone
          }"
          :ref="el => setCardRef(el, idx)"
        >
        <!-- Columna izquierda: texto de la interfaz -->
        <div class="doc-step-text">
          <div class="doc-step-heading">
            <span class="doc-step-number">{{ step.number }}</span>
            <h3 class="doc-step-title">{{ step.title }}</h3>
          </div>

          <p class="doc-step-intro" v-html="step.intro"></p>

          <!-- Enlace externo (GCam o Figma) -->
          <a
            v-if="step.downloadLink"
            :href="step.downloadLink.url"
            target="_blank"
            rel="noopener noreferrer"
            class="doc-download-tag"
          >
            <svg class="download-icon" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
              <polyline points="15 3 21 3 21 9"></polyline>
              <line x1="10" y1="14" x2="21" y2="3"></line>
            </svg>
            <span>{{ step.downloadLink.text }}</span>
          </a>

          <ul class="doc-step-list">
            <li v-for="(item, i) in step.items" :key="i" v-html="item"></li>
          </ul>

          <!-- Caja destacada para la estructura del nombre de archivo -->
          <div v-if="step.extraBox" class="doc-extra-box">
            <h4 class="extra-box-heading">{{ step.extraBox.title }}</h4>
            <div class="extra-box-format">
              <code>{{ step.extraBox.format }}</code>
            </div>
            
            <div class="extra-box-example">
              <div class="example-file">
                <svg class="file-icon" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                  <polyline points="14 2 14 8 20 8"></polyline>
                </svg>
                <span class="file-name">
                  <span class="highlight-blue">001</span>.PHOTOSPHERE.jpg
                </span>
              </div>
              <div class="example-arrow-container">
                <span class="arrow-up-indicator">↑</span>
                <span class="arrow-text">{{ step.extraBox.hint }}</span>
              </div>
            </div>
          </div>

          <!-- Sección de notas -->
          <div v-if="step.note" class="doc-step-note">
            <span class="note-label">Nota</span>
            <p class="note-content">{{ step.note }}</p>
          </div>
        </div>

        <!-- Columna derecha: video/imagen (solo si existe el recurso) -->
        <div v-if="step.video || step.youtubeId || step.image" class="doc-step-media">
          <!-- Renderizar imagen limpia si está definida (sin marco) -->
          <div v-if="step.image" class="doc-image-wrapper">
            <img :src="step.image" class="doc-step-image" alt="Visualización del paso" />
          </div>

          <!-- Si no, renderizar smartphone mockup para los videos -->
          <div v-else class="phone-mockup">
            <div class="phone-island"></div>
            <div class="phone-screen">
              <div class="doc-video-frame">
                <!-- Paso 1: video sugerido de YouTube -->
                <iframe
                  v-if="step.youtubeId"
                  class="doc-video"
                  :src="`https://www.youtube.com/embed/${step.youtubeId}`"
                  title="Video de YouTube"
                  frameborder="0"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowfullscreen
                ></iframe>

                <!-- Resto de pasos: videos alojados en el frontend -->
                <video
                  v-else-if="step.video"
                  class="doc-video"
                  :src="step.video"
                  autoplay
                  muted
                  loop
                  playsinline
                  disablepictureinpicture
                  preload="auto"
                ></video>

                <!-- Placeholder mientras no exista el recurso -->
                <div v-else class="doc-video-placeholder">
                  <UIcon name="icons/image" size="28" color="rgba(255,255,255,0.35)" />
                  <span>Video pendiente</span>
                  <small>{{ step.mediaHint }}</small>
                </div>
              </div>
            </div>
            <div class="phone-home-indicator"></div>
          </div>
        </div>
        </section>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import UIcon from '@/components/UIcon.vue';
import step1Video from '@/assets/videos/step_1.mp4';
import step2Video from '@/assets/videos/step_2.mp4';
import step4Video from '@/assets/videos/step_4.mp4';
import step5Video from '@/assets/videos/step_5.mp4';
import step3Image from '@/assets/images/doc_step_3.png';

// ── Contenido de la guía ────────────────────────────────────────────────────
// Paso 1: video sugerido de YouTube (coloca aquí el ID del video).
// Pasos 2-6: videos alojados en el frontend (ruta en `video`, aún pendientes).
const steps = [
  {
    number: 1,
    title: 'Captura de la fotografía',
    intro: 'Para iniciar, captura el entorno utilizando la aplicación GCam (disponible para correos institucionales <strong class="highlight-blue">@unet.edu.ve</strong>).',
    items: [
      'El archivo debe estar en formato 360.',
      'Renombra el archivo siguiendo la estructura <code class="highlight-blue">xxx.PHOTOSPHERE.jpg</code>.',
      'Sustituye <code class="highlight-blue">xxx</code> por el número único del nodo que identificará su posición en el mapa.',
    ],
    downloadLink: {
      text: 'Descargar GCam APK',
      url: 'https://drive.google.com/file/d/12yUBHB5SlbLu8Wt5ck20CJ1pZSv1lTk_/view?usp=drivesdk',
    },
    extraBox: {
      title: 'Estructura de nombre de archivo:',
      format: 'xxx.PHOTOSPHERE.jpg',
      hint: 'Número de nodo único',
    },
    note: 'GCam es una recomendación para sistemas operativos Android. Cualquier aplicación que genere el formato PHOTOSPHERE es aceptada.',
    youtubeId: '',
    video: step1Video,
    mediaHint: 'Clip de GCam en modo "Foto Esférica" y renombrado a 001.PHOTOSPHERE.jpg.',
  },
  {
    number: 2,
    title: 'Ubicación en el mapa',
    intro: 'Antes de subir la imagen, debes registrar su posición espacial en nuestro archivo de Figma.',
    items: [
      'Abre el enlace de Figma del proyecto y dirígete a la página <strong>Map</strong>.',
      'Encontrarás dos versiones de cada mapa: una limpia y otra con marcas.',
      'Diseña la nueva ubicación en la versión correspondiente y añade un nodo visual en el punto exacto donde tomaste la foto.',
      'Identifica este nuevo nodo con su número único (<code>xxx</code>).',
      'Indica también el peso entre dos nodos (distancia aproximada) con el número posicionado entre ambos.',
    ],
    downloadLink: {
      text: 'Ver Figma del proyecto',
      url: 'https://www.figma.com/design/lWEpqefrXPZsmWFmA9jBaJ/UNET360-Styleguide?node-id=20-24',
    },
    youtubeId: '',
    video: step2Video,
    mediaHint: 'Grabación en Figma duplicando y renombrando un nodo en la pestaña "Map".',
  },
  {
    number: 3,
    title: 'Pre-procesamiento de la foto',
    intro: 'Prepara la imagen fragmentándola en cuadrículas para optimizar su carga. Necesitarás una terminal compatible con Bash, la herramienta <code>zip</code> y tener instalado ImageMagick (versión 7+ que reconozca el comando <code>magick</code>).',
    items: [
      'Coloca la imagen original y el script <code>generate_tiles.sh</code> en el mismo directorio.',
      'Abre la terminal en esa ubicación y otorga permisos de ejecución con el comando: <code>chmod +x generate_tiles.sh</code>',
      'Ejecuta el script pasando el identificador del nodo como argumento. Por ejemplo: <code>./generate_tiles.sh 001</code>',
      'El sistema automatizará el recorte y generará un archivo <code>.zip</code> finalizado.',
    ],
    youtubeId: '',
    video: null,
    image: step3Image,
    note: 'Antes de proceder con la carga de la fotografía, se recomienda registrar la ubicación (en caso de ser nueva) desde el módulo "Administrar nodos". Asimismo, es indispensable que el desarrollador del equipo haya incorporado al repositorio la imagen correspondiente al nuevo minimapa.',
    mediaHint: 'Captura de terminal ejecutando el script y generando el .zip resultante.',
  },
  {
    number: 4,
    title: 'Carga de la foto y conexiones',
    intro: 'Sube el archivo <code>.zip</code> al formulario e ingresa el identificador único del nodo. A continuación, establece sus rutas:',
    items: [
      '<strong>Conexiones:</strong> Configura los nodos adyacentes (Frente, Derecha, Atrás, Izquierda) guiándote por el Figma. El "Frente" siempre corresponde al nodo ubicado al <strong>Este</strong>.',
      '<strong>Peso de conexión:</strong> Ingresa la distancia hacia cada nodo. Una unidad equivale a un metro (crucial para el cálculo de rutas óptimas).',
      '<strong>Ubicación general:</strong> Selecciona el área a la que pertenece (o crea una nueva desde el apartado correspondiente).',
      '<strong>Coordenadas del minimapa:</strong> Ve a Figma y dibuja un rectángulo que vaya desde la esquina superior izquierda de la imagen hasta el centro exacto de la marca de tu nodo. El ancho del rectángulo es tu valor X, y el alto es tu valor Y.',
    ],
    youtubeId: '',
    video: step4Video,
    note: 'La demostración de este procedimiento se realizó utilizando como referencia el nodo preexistente 168, motivo por el cual se empleó el identificador 0168.',
    mediaHint: 'Pantalla dividida: formulario de pesos y el trazado del rectángulo en Figma.',
  },
  {
    number: 5,
    title: 'Post-procesamiento',
    intro: 'Verifica y ajusta el entorno inmersivo en vivo.',
    items: [
      'Ingresa a la aplicación utilizando la ruta del nodo: <code>360-map?node=xxx</code> (reemplaza las \'x\' por tu identificador).',
      'Accede al modo de edición de nodo.',
      'Ajusta la cámara inicial para que el frente mire hacia el <strong>Este</strong>.',
      'Fija las posiciones de las flechas de navegación direccional.',
      'Agrega los "tags" (etiquetas) señalando los lugares de interés visibles desde este punto.',
    ],
    youtubeId: '',
    video: step5Video,
    note: 'Existe la opción de definir una rotación de cámara específica dependiendo del nodo del cual provenga el usuario. Esta configuración es de utilidad para corregir la perspectiva visual en trayectos curvos o no lineales (como al subir escaleras o doblar una esquina), garantizando una transición de visualización fluida y coherente con el sentido de la marcha.',
    mediaHint: 'Visor 360 web: edición de vista, guardado de posición y añadido de etiquetas.',
  },
  {
    number: 6,
    title: 'Revisión',
    intro: 'Dirígete a la página de administración de nodos para comprobar el estado final:',
    items: [
      'El nodo cargado no debe presentar ninguna alerta roja.',
      'Las alertas amarillas indican que faltan nodos adyacentes por cargar (no es un error crítico).',
      'Si el recorrido no carga al hacer pruebas de navegación, presiona el botón <strong>Corregir pesos</strong>. Esto solucionará las inconsistencias de distancia si dos nodos conectados tienen valores discordantes en la base de datos.',
    ],
    youtubeId: '',
    video: null,
    mediaHint: 'Recorrido por el panel de administración y clic en el botón "Corregir pesos".',
  },
];

// ── Carrusel horizontal con snap ────────────────────────────────────────────
const trackRef = ref(null);
const cardEls = [];
const activeIndex = ref(0);

const extendedSteps = computed(() => {
  if (steps.length === 0) return [];
  const first = steps[0];
  const last = steps[steps.length - 1];
  return [
    { ...last, isClone: true, cloneId: 'prev-clone' },
    ...steps.map(s => ({ ...s, isClone: false })),
    { ...first, isClone: true, cloneId: 'next-clone' }
  ];
});

const setCardRef = (el, idx) => {
  if (el) cardEls[idx] = el;
};

const getActiveIndexForCard = (step, idx) => {
  let originalIdx = idx - 1;
  if (originalIdx < 0) originalIdx = steps.length - 1;
  if (originalIdx >= steps.length) originalIdx = 0;
  return originalIdx === activeIndex.value;
};

const goTo = (idx) => {
  const clamped = Math.max(0, Math.min(idx, steps.length - 1));
  const domIdx = clamped + 1;
  const el = cardEls[domIdx];
  if (el) el.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
};

const jumpToDOMIndex = (domIdx) => {
  const track = trackRef.value;
  if (!track) return;
  const el = cardEls[domIdx];
  if (el) {
    const origScrollBehavior = track.style.scrollBehavior;
    const origSnapType = track.style.scrollSnapType;
    track.style.scrollBehavior = 'auto';
    track.style.scrollSnapType = 'none';
    
    track.scrollLeft = el.offsetLeft - (track.clientWidth - el.offsetWidth) / 2;
    
    requestAnimationFrame(() => {
      track.style.scrollBehavior = origScrollBehavior;
      track.style.scrollSnapType = origSnapType;
    });
  }
};

const onScroll = () => {
  const track = trackRef.value;
  if (!track) return;

  const center = track.scrollLeft + track.clientWidth / 2;
  let best = 1;
  let bestDist = Infinity;
  cardEls.forEach((el, i) => {
    if (!el) return;
    const elCenter = el.offsetLeft + el.offsetWidth / 2;
    const dist = Math.abs(elCenter - center);
    if (dist < bestDist) {
      bestDist = dist;
      best = i;
    }
  });

  if (best > 0 && best < extendedSteps.value.length - 1) {
    activeIndex.value = best - 1;
  } else if (best === 0) {
    activeIndex.value = steps.length - 1;
  } else if (best === extendedSteps.value.length - 1) {
    activeIndex.value = 0;
  }

  // Si nos estamos acercando a los clones por arrastre manual, saltamos de inmediato
  // sin esperar al scrollend, para evitar la sensación de "tope" o retraso.
  // Evitamos hacerlo si hay un bloqueo de rueda activo (ya que el onWheel maneja su propia transición).
  if (!wheelLocked) {
    if (best === 0 && bestDist < 30) {
      jumpToDOMIndex(steps.length);
    } else if (best === extendedSteps.value.length - 1 && bestDist < 30) {
      jumpToDOMIndex(1);
    }
  }
};

const WHEEL_COOLDOWN_MS = 650;
let wheelLocked = false;

const onWheel = (e) => {
  const track = trackRef.value;
  if (!track) return;
  if (Math.abs(e.deltaY) <= Math.abs(e.deltaX)) return;
  if (track.scrollWidth <= track.clientWidth) return;

  e.preventDefault();
  if (wheelLocked) return;

  wheelLocked = true;
  const currentDomIdx = activeIndex.value + 1;
  const direction = e.deltaY > 0 ? 1 : -1;
  let targetDomIdx = currentDomIdx + direction;

  // Pre-jump para evitar límites y peleas de animación
  if (currentDomIdx === 1 && direction === -1) {
    // Si estamos en Paso 1 e ir a Paso 6, saltamos al clon 1 (índice 7) y deslizamos al 6
    jumpToDOMIndexSync(extendedSteps.value.length - 1); // clon 1 (7)
    targetDomIdx = steps.length; // real 6 (6)
  } else if (currentDomIdx === steps.length && direction === 1) {
    // Si estamos en Paso 6 e ir a Paso 1, saltamos al clon 6 (índice 0) y deslizamos al 1
    jumpToDOMIndexSync(0); // clon 6 (0)
    targetDomIdx = 1; // real 1 (1)
  }

  const el = cardEls[targetDomIdx];
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
  }

  // Restablecemos el comportamiento de snap en el track
  requestAnimationFrame(() => {
    track.style.scrollBehavior = '';
    track.style.scrollSnapType = '';
  });

  setTimeout(() => { wheelLocked = false; }, WHEEL_COOLDOWN_MS);
};

const jumpToDOMIndexSync = (domIdx) => {
  const track = trackRef.value;
  if (!track) return;
  const el = cardEls[domIdx];
  if (el) {
    track.style.scrollBehavior = 'auto';
    track.style.scrollSnapType = 'none';
    track.scrollLeft = el.offsetLeft - (track.clientWidth - el.offsetWidth) / 2;
  }
};

onMounted(() => {
  // Posicionar inicialmente en el primer elemento real
  setTimeout(() => {
    jumpToDOMIndex(1);
  }, 100);
});
</script>

<script>
import UIcon from '@/components/UIcon.vue';
export default { components: { UIcon } };
</script>

<style lang="scss" scoped>
@import '@/assets/styles/pages/_documentation.scss';
</style>
