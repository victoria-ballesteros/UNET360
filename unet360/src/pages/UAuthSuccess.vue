<template>
  <div class="form-container">
    <div class="text-section">
      <p class="upper-paragrah">{{ currentTexts?.upper }}</p>
      <p class="lower-paragraph">
        {{ lowerText }}
      </p>
      <!-- Lista de detalles para SuccessPrePassword -->
      <ul v-if="currentMode === 'SuccessPrePassword'" class="success-details-list">
        <li v-for="item in currentTexts.lowerList" :key="item">{{ item }}</li>
      </ul>
    </div>
    <div class="form-section success-visual-section">
      <!-- Illustrative icon -->
      <div class="success-illustration">
        <!-- Mail Sent SVG -->
        <svg v-if="currentMode === 'SuccessRegister' || currentMode === 'SuccessPrePassword'" viewBox="0 0 120 120" class="illustration-svg mail-sent-svg" aria-hidden="true">
          <circle cx="60" cy="60" r="50" fill="rgba(255, 239, 61, 0.03)" stroke="rgba(255, 239, 61, 0.1)" stroke-width="1" />
          <path d="M30 42h60c4 0 8 3.5 8 8v28c0 4.5-4 8-8 8H30c-4 0-8-3.5-8-8V50c0-4.5 4-8 8-8z" fill="rgba(255,255,255,0.02)" stroke="rgba(255,255,255,0.12)" stroke-width="1.8"/>
          <path d="M22 50l38 23 38-23" fill="none" stroke="var(--main-yellow)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M35 78l18-13M85 78L67 65" stroke="rgba(255,255,255,0.12)" stroke-width="1.8" stroke-linecap="round"/>
          <!-- Animated particles -->
          <circle cx="35" cy="30" r="2.5" fill="var(--main-blue)" class="particle p-1"/>
          <circle cx="85" cy="34" r="3.5" fill="var(--main-yellow)" class="particle p-2"/>
          <circle cx="75" cy="85" r="2" fill="var(--main-yellow)" class="particle p-3"/>
        </svg>

        <!-- Check Success SVG -->
        <svg v-else viewBox="0 0 120 120" class="illustration-svg check-success-svg" aria-hidden="true">
          <circle cx="60" cy="60" r="50" fill="rgba(255, 239, 61, 0.03)" stroke="rgba(255, 239, 61, 0.1)" stroke-width="1" />
          <path d="M38 60l15 15 30-30" fill="none" stroke="var(--main-yellow)" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" class="checkmark-path"/>
        </svg>
      </div>

      <div class="button-container">
        <UButton
          :text="buttonText"
          type="contrast-2"
          @click="handleSubmit"
          :full="true"
        />
      </div>
    </div>
    
  </div>
</template>

<script setup>
import { useRoute, useRouter } from "vue-router";
import { computed, onMounted } from "vue";

import { useAuthStore } from '@/service/stores/auth';
import UButton from "@/components/UButton.vue";

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const email = computed(() => authStore.successEmail);

onMounted(() => {
  if (!authStore.successState) {
    router.replace({ name: 'Login' });
    return;
  }
  authStore.successState = false;
});

const successTexts = {
  SuccessRegister: {
    upper: "¡CUENTA CREADA CON EXITO!",
    lower: "Hemos enviado un correo de confirmación a %EMAIL%. Por favor, verifica tu bandeja de entrada."
  },
  SuccessConfirmation: {
    upper: "SU CUENTA HA SIDO CONFIRMADA",
    lower: "Inicia sesión para disfrutar de UNET360."
  },
  SuccessPrePassword: {
    upper: "¡ENLACE ENVIADO!",
    lowerMain: "Hemos enviado un correo a %EMAIL% con instrucciones para restablecer tu contraseña.",
    lowerList: [
      "¿No lo ves? Revisa tu carpeta de spam.",
      "El enlace expirará en 24 horas por seguridad."
    ]
  },
  SuccessNewPassword: {
    upper: "¡CONTRASEÑA ACTUALIZADA!",
    lower: "Ya puedes iniciar sesión con tu nueva contraseña."
  }
};

const currentMode = computed(() => route.name);
const currentTexts = computed(() => successTexts[currentMode.value]);

const buttonText = computed(() => {
  if (currentMode.value === 'SuccessRegister' || currentMode.value === 'SuccessPrePassword') {
    return "Volver a Iniciar Sesión";
  }
  return "Iniciar Sesión";
});

const lowerText = computed(() => {
  if (currentMode.value === 'SuccessRegister') {
    return currentTexts.value.lower.replace('%EMAIL%', email.value);
  }
  if (currentMode.value === 'SuccessPrePassword') {
    return currentTexts.value.lowerMain.replace('%EMAIL%', email.value);
  }
  return currentTexts.value?.lower || "";
});

function handleSubmit() {
  router.push({ name: 'Login' });
}
</script>

<style scoped lang="scss">
@import "@/assets/styles/pages/_user_auth.scss";

// ── Success page specific styles ───────────────────
.success-visual-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2rem;

  .button-container {
    width: 100%;
  }
}

.success-details-list {
  color: rgba(255, 255, 255, 0.45);
  margin-top: 1rem;
  padding-left: 1.25rem;
  
  li {
    @include paragraph-small;
    line-height: 1.6;
    margin-bottom: 0.5rem;
    color: rgba(255, 255, 255, 0.6);
  }
}

.success-illustration {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 120px;
  height: 120px;
  position: relative;
  margin-bottom: 0.5rem;
}

.illustration-svg {
  width: 100%;
  height: 100%;
}

.mail-sent-svg {
  animation: floatEnvelope 3s ease-in-out infinite;
}

.checkmark-path {
  stroke-dasharray: 100;
  stroke-dashoffset: 100;
  animation: drawCheck 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  animation-delay: 0.15s;
}

.particle {
  animation: blinkParticle 2.5s ease-in-out infinite;
  opacity: 0.7;
  transform-origin: center;

  &.p-1 { animation-delay: 0.2s; }
  &.p-2 { animation-delay: 0.8s; }
  &.p-3 { animation-delay: 1.4s; }
}

@keyframes floatEnvelope {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-8px);
  }
}

@keyframes drawCheck {
  to {
    stroke-dashoffset: 0;
  }
}

@keyframes blinkParticle {
  0%, 100% {
    transform: scale(1);
    opacity: 0.3;
  }
  50% {
    transform: scale(1.3);
    opacity: 1;
  }
}
</style>




