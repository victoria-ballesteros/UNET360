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
          @update:modelValue="() => { inputErrors.email = ''; inputErrors.password = ''; inputErrors.confirmPassword = ''; }"
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
          :type="isFormValid && !authStore.loading ? 'contrast-2' : 'deactivated'"
          :disabled="authStore.loading"
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

import { useAuthStore } from '@/service/stores/auth';

import UInput from "@/components/UInput.vue";
import UButton from "@/components/UButton.vue";


// ═══════════════  Variables reactivas y helpers  ═══════════════
// Estado para mostrar/ocultar contraseñas
const showPassword = reactive({
  password: false,
  confirmPassword: false
});

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
const validModes = ["Login", "Signup", "Recovery", "NewPassword"];
const currentMode = computed(() => validModes.includes(route.name) ? route.name : "Login");
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
  if (authStore.loading) return;
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
      inputErrors.password = " ";
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
      const redirectPath = route.query.redirect || { name: 'Home' };
      router.push(redirectPath);
    } else {
      // Si falla, muestra el error debajo de Contraseña y pone el input de email en rojo
      inputErrors.email = ' '; 
      inputErrors.password = authStore.error || 'Error de autenticación';
    }
    return;
  }

  // ═══════════════ SIGNUP FLOW ═══════════════
  if (currentMode.value === 'Signup') {
    const result = await authStore.signup(inputModels.email, inputModels.password);
    if (result.success) {
      // Puedes guardar el email en el store principal si lo necesitas
      authStore.successEmail = inputModels.email;
      authStore.successState = true;
      router.push({ name: 'SuccessRegister' });
    } else {
      inputErrors.email = ' ';
      inputErrors.password = result.message;
    }
    return;
  }
  // ═══════════════ RECOVERY FLOW ═══════════════
  if (currentMode.value === 'Recovery') {
    const result = await authStore.sendRecoveryEmail(inputModels.email);
    authStore.successEmail = inputModels.email;
    authStore.successState = true;
    router.push({ name: 'SuccessPrePassword' });
    return;
  }
  // ═══════════════ NEW PASSWORD FLOW ═══════════════
  if (currentMode.value === 'NewPassword') {
    // Extrae los tokens del hash
    const hash = window.location.hash;
    const access_token = hash.match(/access_token=([^&]+)/)?.[1] || '';
    const refresh_token = hash.match(/refresh_token=([^&]+)/)?.[1] || '';
    if (!access_token || !refresh_token) {
      inputErrors.password = 'Enlace inválido o expirado.';
      return;
    }
    const result = await authStore.changePassword({
      access_token,
      refresh_token,
      new_password: inputModels.password
    });
    if (result.success) {
      authStore.successState = true;
      router.push({ name: 'SuccessNewPassword' });
    } else {
      inputErrors.password = result.message;
    }
    return;
  }

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




