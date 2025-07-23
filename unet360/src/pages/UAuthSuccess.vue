<template>
  <div class="form-container">
    <div class="text-section">
      <p class="upper-paragrah">{{ currentTexts.upper }}</p>
      <p class="lower-paragraph">
        <!-- Mensaje principal para SuccessPrePassword -->
        <template v-if="currentMode === 'SuccessPrePassword'">
          {{ currentTexts.lowerMain }}
        </template>
        <!-- Mensaje normal para otros modos -->
        <template v-else>
          {{ currentTexts.lower }}
        </template>
      </p>
      <!-- Lista de detalles para SuccessPrePassword -->
      <ul v-if="currentMode === 'SuccessPrePassword'">
        <li v-for="item in currentTexts.lowerList" :key="item">{{ item }}</li>
      </ul>
    </div>
    <div class="form-section">
        <div class="button-container" v-if="currentMode === 'SuccessConfirmation' || currentMode === 'SuccessNewPassword'">
            <UButton
            :text="buttonText"
            :type="'contrast-2'"
            @click="handleSubmit"
            />
        </div>
    </div>
    
  </div>
</template>

<script setup>
import { useRoute, RouterLink } from "vue-router";
import { computed } from "vue";

import UButton from "@/components/UButton.vue";

// ═══════════════  Variables reactivas y helpers  ═══════════════
const route = useRoute();

const successTexts = {
    SuccessRegister: {
    upper: "¡CUENTA CREADA CON EXITO!",
    lower: "Hemos enviado un correo de confirmación a pedro.perez@unet.edu.ve. Por favor, verifica tu bandeja de entrada."
    },
    SuccessConfirmation: {
        upper: "SU CUENTA HA SIDO CONFIRMADA",
        lower: "Inicia sesión para disfrutar de UNET360."
    },
    SuccessPrePassword: {
        upper: "¡ENLACE ENVIADO!",
        lowerMain: "Hemos enviado un correo a gabriel.ulacio@unet.edu.ve con instrucciones para restablecer tu contraseña.",
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

const buttonText = "Iniciar Sesión";

const currentMode = computed(() => route.name);
const currentTexts = computed(() => successTexts[currentMode.value]);

function handleSubmit() {
  // Ejemplo: navega a login
  // router.push({ name: 'Login' });
}

</script>

<style scoped lang="scss">
@import "@/assets/styles/pages/_user_auth.scss";
</style>




