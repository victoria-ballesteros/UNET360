

<template>
  <div class="form-container">
    <!-- ═══════════════  Títulos y subtítulos  ═══════════════ -->
    <div class="text-section">
      <p class="upper-paragrah">{{ currentTexts.upper }}</p>
      <p class="lower-paragraph">{{ currentTexts.lower }}</p>
    </div>

    <!-- ═══════════════  Formulario dinámico  ═══════════════ -->
    <div class="form-section">
      <div
        v-for="field in currentFields"
        :key="field"
        class="input-container"
        :class="{ 'has-error': inputErrors[field] }"
      >
        <!-- Etiqueta del campo -->
        <p class="input-label">{{ fieldLabels[field] }}</p>

        <!-- Input reutilizable con icono de ojo para contraseñas -->
        <UInput
          v-model="inputModels[field]"
          :type="isPasswordField(field) && !showPassword[field] ? 'password' : 'text'"
          :placeholder="fieldLabels[field]"
          :error="inputErrors[field]"
          :icon="isPasswordField(field) ? (showPassword[field] ? 'icons/eye' : 'icons/eye-slash') : null"
          @icon-click="() => { if(isPasswordField(field)) showPassword[field] = !showPassword[field] }"
          :iconColor="'var(--border-gray)'"
          @update:modelValue="() => { inputErrors.email = ''; inputErrors.password = ''; }"
        />

        <!-- Mensaje de error -->
        <p v-if="inputErrors[field]" class="input-error-label">
          {{ inputErrors[field] }}
        </p>

        <!-- Link de recuperación solo en login y campo password -->
        <RouterLink v-if="currentMode === 'Login' && field === 'password'" :to="{ name: 'Recovery' }">
          <p class="forgot-password-link">¿Olvidaste tu contraseña?</p>
        </RouterLink>
      </div>

      <!-- Botón principal -->
      <div class="button-container">
        <UButton
          :text="buttonTexts[currentMode]"
          :type="isFormValid ? 'contrast-2' : 'deactivated'"
          @click="handleSubmit"
        />
      </div>

      <!-- Link para cambiar entre login y registro -->
      <div class="text-container">
        <p class="register-link" style="margin:0;">
          <template v-if="currentMode === 'Login'">
            ¿No tienes cuenta?
            <RouterLink :to="{ name: 'Signup' }">
              <b>Regístrate aquí</b>
            </RouterLink>
          </template>
          <template v-else-if="currentMode === 'Signup'">
            ¿Ya tienes cuenta?
            <RouterLink :to="{ name: 'Login' }">
              <b>Inicia sesión</b>
            </RouterLink>
          </template>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRoute, useRouter, RouterLink } from "vue-router";
import { reactive, computed, ref, watch } from "vue";

import { useAuthSuccessStore } from '@/service/stores/authSuccess';
import { useAuthStore } from '@/service/stores/auth';

import UInput from "@/components/UInput.vue";
import UButton from "@/components/UButton.vue";


// ═══════════════  Variables reactivas y helpers  ═══════════════
// Estado para mostrar/ocultar contraseñas
const showPassword = reactive({
  password: false,
  confirmPassword: false
});

const authSuccessStore = useAuthSuccessStore();
const authStore = useAuthStore();
const route = useRoute();
const router = useRouter();

const authTexts = {
  Login: {
    upper: "INICIAR SESIÓN",
    lower: "Ingresa tus credenciales para acceder"
  },
  Signup: {
    upper: "CREAR UNA CUENTA",
    lower: "Completa los campos para registrarte"
  },
  Recovery: {
    upper: "¿OLVIDASTE TU CONTRASEÑA?",
    lower: "Ingresa el correo electrónico asociado a tu cuenta y te enviaremos un enlace para restablecerla."
  },
  NewPassword: {
    upper: "CREA UNA NUEVA CONTRASEÑA",
    lower: ""
  }
}

const formFields = {
  Login: ["email", "password"],
  Signup: ["email", "password", "confirmPassword"],
  Recovery: ["email"],
  NewPassword: ["password", "confirmPassword"],
}

const buttonTexts = {
  Login: "Iniciar Sesión",
  Signup: "Registrarse",
  Recovery: "Enviar enlace",
  NewPassword: "Guardar contraseña"
};

const fieldLabels = {
  email: "Email ID",
  password: "Contraseña",
  confirmPassword: "Confirmar contraseña",
};

const inputModels = reactive({
  email: "",
  password: "",
  confirmPassword: ""
});

const inputErrors = reactive({
  email: "",
  password: "",
  confirmPassword: ""
});



// Helpers para modo, campos y textos actuales
const currentMode = computed(() => route.name || "Login");
const currentFields = computed(() => formFields[currentMode.value] || []);
const currentTexts = computed(() => authTexts[currentMode.value] || authTexts.Login);

// Helper para saber si un campo es de tipo contraseña
function isPasswordField(field) {
  return field === 'password' || field === 'confirmPassword';
}


// ═══════════════  Validación de formulario  ═══════════════
// El formulario es válido si todos los campos requeridos están llenos y sin errores
const isFormValid = computed(() =>
  currentFields.value.every(field => inputModels[field] && !inputErrors[field])
);


// ═══════════════  Validación y envío del formulario  ═══════════════
/**
 * Valida los campos del formulario según el modo actual y muestra errores si corresponde.
 * Si no hay errores, ejecuta la lógica de submit (API, etc).
 */
async function handleSubmit() {
  // Limpiar errores previos
  currentFields.value.forEach(field => inputErrors[field] = "");

  // Validación de email
  if (currentFields.value.includes("email")) {
    const email = inputModels.email;
    if (!email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
      inputErrors.email = "Correo electrónico inválido";
    }
  }

  // Validación de contraseña
  if (currentFields.value.includes("password")) {
    if (!inputModels.password || inputModels.password.length < 6) {
      inputErrors.password = "La contraseña debe tener al menos 6 caracteres";
    }
  }

  // Validación de confirmación de contraseña
  if (currentFields.value.includes("confirmPassword")) {
    if (inputModels.confirmPassword !== inputModels.password) {
      inputErrors.confirmPassword = "Las contraseñas no coinciden";
    }
  }

  // Si hay errores, no continuar
  if (!isFormValid.value) return;

  // ═══════════════ LOGIN FLOW ═══════════════
  if (currentMode.value === 'Login') {
    // Llama al store de autenticación
    await authStore.login(inputModels.email, inputModels.password);

    // Si login exitoso, redirige a Home
    if (authStore.isAuthenticated) {
      router.push({ name: 'Home' });
    } else {
      // Si falla, muestra el error debajo de Contraseña y pone el input de email en rojo
      inputErrors.email = ' '; 
      inputErrors.password = authStore.error || 'Error de autenticación';
    }
    return;
  }

  if (backendResult) {
    // Solo guardar el email y permitir acceso a éxito si se usará en la pantalla de éxito
    if (currentMode.value === 'Signup') {
      authSuccessStore.setEmail(inputModels.email);
      authSuccessStore.allowSuccess();
      router.push({ name: 'SuccessRegister' });
    } else if (currentMode.value === 'Recovery') {
      authSuccessStore.setEmail(inputModels.email);
      authSuccessStore.allowSuccess();
      router.push({ name: 'SuccessPrePassword' });
    } else if (currentMode.value === 'NewPassword') {
      authSuccessStore.allowSuccess();
      router.push({ name: 'SuccessNewPassword' });
    }
  }
  // Aquí iría la lógica de submit real (API, etc.)
  alert(`Formulario enviado para modo: ${currentMode.value}`);

}


// ═══════════════  Limpiar formulario al cambiar de modo  ═══════════════
/**
 * Limpia los modelos, errores y visibilidad de contraseñas.
 */
function resetForm() {
  Object.keys(inputModels).forEach(key => inputModels[key] = "");
  Object.keys(inputErrors).forEach(key => inputErrors[key] = "");
  Object.keys(showPassword).forEach(key => showPassword[key] = false);
}

// Limpiar formulario cada vez que cambia el modo (ruta)
watch(currentMode, resetForm);

</script>

<style scoped lang="scss">
@import "@/assets/styles/pages/_user_auth.scss";
</style>




