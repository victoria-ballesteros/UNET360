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
      <div class="doc-steps" ref="trackRef" @scroll="onScroll" @wheel="onWheel">
        <section
          v-for="(step, idx) in steps"
          :key="step.number"
          class="doc-step"
          :class="{ 'is-active': idx === activeIndex }"
          :ref="el => setCardRef(el, idx)"
        >
        <!-- Columna izquierda: texto de la interfaz -->
        <div class="doc-step-text">
          <div class="doc-step-heading">
            <span class="doc-step-number">{{ step.number }}</span>
            <h3 class="doc-step-title">{{ step.title }}</h3>
          </div>

          <p class="doc-step-intro" v-html="step.intro"></p>

          <ul class="doc-step-list">
            <li v-for="(item, i) in step.items" :key="i" v-html="item"></li>
          </ul>
        </div>

        <!-- Columna derecha: video -->
        <div class="doc-step-media">
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
              controls
              preload="metadata"
            ></video>

            <!-- Placeholder mientras no exista el recurso -->
            <div v-else class="doc-video-placeholder">
              <UIcon name="icons/image" size="28" color="rgba(255,255,255,0.35)" />
              <span>Video pendiente</span>
              <small>{{ step.mediaHint }}</small>
            </div>
          </div>
        </div>
        </section>
      </div>
    </div>

    <!-- Puntos indicadores -->
    <div class="doc-dots">
      <button
        v-for="(step, idx) in steps"
        :key="step.number"
        class="doc-dot"
        :class="{ active: idx === activeIndex }"
        :aria-label="`Ir al paso ${step.number}`"
        :aria-current="idx === activeIndex"
        @click="goTo(idx)"
      />
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue';
import UIcon from '@/components/UIcon.vue';

// ── Contenido de la guía ────────────────────────────────────────────────────
// Paso 1: video sugerido de YouTube (coloca aquí el ID del video).
// Pasos 2-6: videos alojados en el frontend (ruta en `video`, aún pendientes).
const steps = [
  {
    number: 1,
    title: 'Captura de la fotografía',
    intro: 'Para iniciar, captura el entorno utilizando la aplicación GCam (disponible para correos institucionales <strong>@unet.edu.ve</strong>).',
    items: [
      'El archivo debe estar en formato 360.',
      'Renombra el archivo siguiendo la estructura <code>xxx.PHOTOSPHERE.jpg</code>.',
      'Sustituye <code>xxx</code> por el número único del nodo que identificará su posición en el mapa.',
    ],
    youtubeId: '', // TODO: ID del video de YouTube sugerido
    video: null,
    mediaHint: 'Clip de GCam en modo "Foto Esférica" y renombrado a 001.PHOTOSPHERE.jpg.',
  },
  {
    number: 2,
    title: 'Ubicación en el mapa',
    intro: 'Antes de subir la imagen, debes registrar su posición espacial en nuestro archivo de Figma.',
    items: [
      'Abre el enlace de Figma del proyecto y dirígete a la pestaña <strong>Map</strong>.',
      'Encontrarás dos versiones de cada mapa: una limpia y otra con marcas.',
      'Diseña la nueva ubicación en la versión correspondiente y añade un nodo visual en el punto exacto donde tomaste la foto.',
      'Identifica este nuevo nodo con su número único (<code>xxx</code>).',
    ],
    youtubeId: '',
    video: null, // TODO: video alojado en el frontend
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
    video: null,
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
    video: null,
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

const setCardRef = (el, idx) => {
  if (el) cardEls[idx] = el;
};

// Desplaza (con animación) hasta centrar el paso indicado
const goTo = (idx) => {
  const clamped = Math.max(0, Math.min(idx, steps.length - 1));
  const el = cardEls[clamped];
  if (el) el.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
};

// Detecta qué paso está más centrado tras hacer scroll y actualiza el estado activo
let ticking = false;
const onScroll = () => {
  if (ticking) return;
  ticking = true;
  requestAnimationFrame(() => {
    const track = trackRef.value;
    if (track) {
      const center = track.scrollLeft + track.clientWidth / 2;
      let best = 0;
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
      activeIndex.value = best;
    }
    ticking = false;
  });
};

// Convierte el scroll vertical de la rueda en desplazamiento horizontal,
// dejando pasar el scroll de la página cuando el carrusel llega a un extremo
const onWheel = (e) => {
  const track = trackRef.value;
  if (!track) return;
  if (Math.abs(e.deltaY) <= Math.abs(e.deltaX)) return; // gesto ya horizontal
  if (track.scrollWidth <= track.clientWidth) return;    // nada que desplazar

  const atStart = track.scrollLeft <= 0;
  const atEnd = track.scrollLeft + track.clientWidth >= track.scrollWidth - 1;
  if ((e.deltaY < 0 && atStart) || (e.deltaY > 0 && atEnd)) return;

  e.preventDefault();
  track.scrollLeft += e.deltaY;
};
</script>

<script>
import UIcon from '@/components/UIcon.vue';
export default { components: { UIcon } };
</script>

<style lang="scss" scoped>
@import '@/assets/styles/pages/_documentation.scss';
</style>
