<template>
  <div class="doc-container">

    <!-- ── Header ── -->
    <header class="doc-header">
      <p class="header-overline">Guía para administradores</p>
      <h2>Documentación</h2>
      <p class="doc-subtitle">
        Guía paso a paso para tomar la foto de un nuevo punto y agregarlo al recorrido 360°, sin necesidad de conocimientos técnicos.
      </p>
    </header>

    <!-- ── Requerimientos mínimos ── -->
    <section class="doc-requirements">
      <h3 class="doc-section-title">Requerimientos mínimos</h3>
      <p class="doc-section-subtitle">Lo que necesitas antes de empezar a tomar fotos para el recorrido.</p>

      <div class="requirements-grid">
        <div v-for="(req, i) in requirements" :key="i" class="requirement-item">
          <h4 class="requirement-title">{{ req.title }}</h4>
          <p class="requirement-desc">{{ req.desc }}</p>
          <a
            v-if="req.link"
            :href="req.link.url"
            target="_blank"
            rel="noopener noreferrer"
            class="doc-download-tag"
          >
            <svg class="download-icon" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
              <polyline points="15 3 21 3 21 9"></polyline>
              <line x1="10" y1="14" x2="21" y2="3"></line>
            </svg>
            <span>{{ req.link.text }}</span>
          </a>
        </div>
      </div>
    </section>

    <!-- ── Glosario ── -->
    <section class="doc-glossary">
      <h3 class="doc-section-title">Glosario</h3>
      <p class="doc-section-subtitle">Palabras que vas a encontrar en esta guía, explicadas de forma sencilla.</p>

      <div class="glossary-grid">
        <div v-for="(entry, i) in glossary" :key="i" class="glossary-item">
          <h4 class="glossary-term">{{ entry.term }}</h4>
          <p class="glossary-def">{{ entry.def }}</p>
        </div>
      </div>
    </section>

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
    intro: 'Para empezar, toma una foto de 360° del lugar usando la aplicación GCam (puedes descargarla con tu correo institucional <strong class="highlight-blue">@unet.edu.ve</strong>).',
    items: [
      'Asegúrate de que la foto haya quedado en formato "360" (una foto esférica, que se ve completa en todas direcciones).',
      'Cambia el nombre del archivo para que quede así: <code class="highlight-blue">xxx.PHOTOSPHERE.jpg</code>.',
      'Donde dice <code class="highlight-blue">xxx</code>, escribe el número que identificará a este punto (nodo) dentro del mapa.',
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
    note: 'GCam es solo una recomendación para celulares Android. Puedes usar cualquier otra aplicación, siempre que genere fotos en formato "foto esférica" (PHOTOSPHERE).',
    youtubeId: '',
    video: step1Video,
    mediaHint: 'Clip de GCam en modo "Foto Esférica" y renombrado a 001.PHOTOSPHERE.jpg.',
  },
  {
    number: 2,
    title: 'Ubicación en el mapa',
    intro: 'Antes de subir la foto, hay que marcar en un mapa el lugar exacto donde la tomaste. Esto se hace en Figma, una herramienta de diseño donde tenemos guardados los mapas del recorrido.',
    items: [
      'Abre el enlace de Figma del proyecto y entra a la página llamada <strong>Map</strong>.',
      'Vas a ver dos versiones del mismo mapa: una limpia y otra con los puntos ya marcados.',
      'En la versión marcada, agrega un punto nuevo justo donde tomaste la foto.',
      'Escríbele a ese punto el mismo número único (<code>xxx</code>) que usaste para nombrar la foto.',
      'Si ese punto se conecta con otro cercano, escribe entre ambos la distancia aproximada en metros (esto se llama "peso" de la conexión).',
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
    title: 'Preparar la foto',
    intro: 'Antes de subirla, la foto se corta en varios pedazos pequeños (como un rompecabezas) para que cargue más rápido en la aplicación. Esto se hace con un script (un pequeño programa) que ya está preparado, así que no necesitas saber programar, solo seguir estos pasos en la terminal de tu computadora.',
    items: [
      'Guarda la foto original y el archivo <code>generate_tiles.sh</code> juntos, en la misma carpeta.',
      'Necesitarás tener instaladas dos herramientas gratuitas de antemano: <code>zip</code> e ImageMagick (versión 7 o más reciente, que traiga el comando <code>magick</code>).',
      'Abre la terminal (línea de comandos) en esa carpeta y escribe: <code>chmod +x generate_tiles.sh</code> (esto solo se hace una vez, y le da permiso al script para ejecutarse).',
      'Ahora ejecútalo escribiendo el número del nodo al final. Por ejemplo: <code>./generate_tiles.sh 001</code>',
      'El script hace el trabajo solo y te entrega un archivo <code>.zip</code> ya listo para subir.',
    ],
    youtubeId: '',
    video: null,
    image: step3Image,
    note: 'Si el punto todavía no existe en el sistema, créalo primero desde "Administrar nodos". Además, antes de subir la foto, confirma con el equipo de desarrollo que ya se agregó la imagen del minimapa correspondiente al repositorio.',
    mediaHint: 'Captura de terminal ejecutando el script y generando el .zip resultante.',
  },
  {
    number: 4,
    title: 'Subir la foto y conectarla con el resto',
    intro: 'Ahora sube el archivo <code>.zip</code> en el formulario del sistema y escribe el número del nodo. Luego completa estos datos, para que quede bien conectado con los demás puntos del mapa:',
    items: [
      '<strong>Conexiones:</strong> indica con qué nodos se conecta este (Frente, Derecha, Atrás, Izquierda), guiándote por el mapa de Figma. Importante: "Frente" siempre significa el nodo que está hacia el <strong>Este</strong>, sin importar hacia dónde mirabas al tomar la foto.',
      '<strong>Peso de la conexión:</strong> escribe la distancia hacia cada nodo vecino, en metros. Esto ayuda al sistema a calcular el camino más corto entre dos puntos.',
      '<strong>Ubicación general:</strong> elige a qué zona o edificio pertenece el nodo (o crea una zona nueva si no existe todavía).',
      '<strong>Coordenadas del minimapa:</strong> en Figma, dibuja un rectángulo que empiece en la esquina superior izquierda de la imagen del mapa y termine justo en el centro de tu nodo. El ancho de ese rectángulo es el valor X, y el alto es el valor Y.',
    ],
    youtubeId: '',
    video: step4Video,
    note: 'En el video de ejemplo se usó el nodo 168 (ya existente) para mostrar el procedimiento, por eso ahí aparece como "0168".',
    mediaHint: 'Pantalla dividida: formulario de pesos y el trazado del rectángulo en Figma.',
  },
  {
    number: 5,
    title: 'Revisar y ajustar dentro de la aplicación',
    intro: 'Con la foto ya cargada, entra a la aplicación para revisar cómo se ve y hacerle los últimos ajustes en vivo.',
    items: [
      'Abre la aplicación en esta dirección: <code>360-map?node=xxx</code> (cambia las \'x\' por el número de tu nodo).',
      'Entra al modo de edición de nodo.',
      'Gira la vista inicial hasta que el frente quede mirando hacia el <strong>Este</strong>.',
      'Acomoda las flechas que sirven para caminar hacia los nodos vecinos, dejándolas en el lugar correcto.',
      'Agrega "tags" (etiquetas) señalando los lugares de interés que se ven desde este punto (por ejemplo, un salón, una oficina o un baño).',
    ],
    youtubeId: '',
    video: step5Video,
    note: 'También puedes indicar una rotación de cámara distinta según de qué nodo venga la persona. Esto es útil en pasillos con curvas o esquinas (como al subir unas escaleras o doblar), para que la vista siempre gire de forma natural y en el sentido en que la persona va caminando.',
    mediaHint: 'Visor 360 web: edición de vista, guardado de posición y añadido de etiquetas.',
  },
  {
    number: 6,
    title: 'Revisión final',
    intro: 'Por último, entra a la página "Administrar nodos" para confirmar que todo haya quedado bien:',
    items: [
      'El nodo que acabas de cargar no debería mostrar ninguna alerta roja.',
      'Las alertas amarillas no son graves: solo avisan que todavía faltan nodos vecinos por cargar.',
      'Si al probar el recorrido notas que no conecta bien entre dos puntos, presiona el botón <strong>Corregir pesos</strong>. Esto arregla automáticamente las distancias cuando dos nodos conectados no coinciden entre sí en la base de datos.',
    ],
    youtubeId: '',
    video: null,
    mediaHint: 'Recorrido por el panel de administración y clic en el botón "Corregir pesos".',
  },
];

// ── Glosario ─────────────────────────────────────────────────────────────────
const glossary = [
  { term: 'Nodo', def: 'Un punto del recorrido. Cada foto 360° que subes se convierte en un nodo, como si fuera una "parada" dentro del mapa.' },
  { term: 'Foto esférica (360°)', def: 'Una sola foto que muestra todo lo que hay alrededor tuyo, no solo lo que tienes al frente. Al verla, puedes girar la vista en cualquier dirección.' },
  { term: 'Conexión / nodo adyacente', def: 'Un nodo vecino al que se puede caminar directamente desde el nodo actual (por ejemplo, el que está justo delante o a un lado).' },
  { term: 'Peso', def: 'La distancia (en metros) entre dos nodos conectados. Se usa para que el sistema sepa calcular el camino más corto entre dos lugares.' },
  { term: 'Minimapa', def: 'El mapa 2D (visto desde arriba) que se muestra como referencia mientras alguien recorre el espacio en 360°.' },
  { term: 'Tag (etiqueta)', def: 'Una marca que le pones a un nodo para señalar qué hay cerca, por ejemplo "Biblioteca" o "Cafetería".' },
  { term: 'Recorrido virtual', def: 'La experiencia completa que ve el usuario final: caminar de nodo en nodo dentro de la aplicación como si estuviera ahí en persona.' },
  { term: 'Panel de administración', def: 'La sección de la aplicación donde se crean, editan o eliminan los nodos y su información.' },
];

// ── Requerimientos mínimos ───────────────────────────────────────────────────
const requirements = [
  {
    title: 'Teléfono',
    desc: 'Calidad mínima equivalente a un Samsung Galaxy S21+: cámara principal de 12 MP (f/1.8) con ultra gran angular de 12 MP (f/2.2).',
  },
  {
    title: 'Sistema operativo',
    desc: 'Se recomienda Android 11 o superior, ya que es compatible con GCam. Otros sistemas también sirven, siempre que la app usada genere fotos en formato "foto esférica" (PHOTOSPHERE).',
  },
  {
    title: 'iOS (iPhone)',
    desc: 'Si tu teléfono es un iPhone, sigues el mismo proceso que con Android, solo que la app se descarga directamente desde la App Store en lugar de instalar un APK.',
    link: {
      text: 'Descargar Teleport 360 Camera',
      url: 'https://apps.apple.com/us/app/teleport-360-camera/id6476905405',
    },
  },
  {
    title: 'Giroscopio',
    desc: 'El teléfono debe contar con sensor de giroscopio. Es lo que permite que la aplicación de captura reconozca el movimiento y arme correctamente la foto esférica.',
  },
  {
    title: 'Orientación al tomar la foto',
    desc: 'La foto debe tomarse siempre con el teléfono en posición vertical (modo retrato), nunca en horizontal.',
  },
  {
    title: 'Inclinación al tomar la foto',
    desc: 'Además de estar en vertical, el teléfono debe mantenerse derecho (sin inclinarlo hacia adelante, atrás o los lados). Esto evita que el recorrido se vea torcido.',
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
