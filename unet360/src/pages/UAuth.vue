
<template>
<div class="form-container">
  
  <div class="text-section">
    <p class="upper-paragrah">{{ currentTexts.upper }}</p>
    <p class="lower-paragraph">{{ currentTexts.lower }}</p>
  </div>

  <div class="form-section">
    <div
      v-for="field in currentFields"
      :key="field"
      class="input-container"
    >
      <p class="input-label">{{ fieldLabels[field] }}</p>

      <UInput
        v-model="inputModels[field]"
        :type="field.includes('password') && !showPassword[field] ? 'password' : 'text'"
        :placeholder="fieldLabels[field]"
        :error="inputErrors[field]"
        :icon="field.includes('password') ? (showPassword[field] ? 'icons/eye' : 'icons/eye-slash') : null"
        @icon-click="() => { if(field.includes('password')) showPassword[field] = !showPassword[field] }"
        :iconColor="'var(--border-gray)'"
      />

      <p v-if="inputErrors[field]" class="input-error-label">
        {{ inputErrors[field] }}
      </p>

      <RouterLink :to="{ name: 'Recovery' }">
        <p
        v-if="currentMode === 'Login' && field === 'password'"
        class="forgot-password-link"
        >
        ¿Olvidaste tu contraseña?
        </p>
      </RouterLink>
      
    </div>

    <div class="button-container">
      <UButton
        :text="buttonTexts[currentMode]"
        :type="isFormValid ? 'contrast-2' : 'deactivated'"
        @click="handleSubmit"
      />
    </div>
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
import { useRoute, RouterLink } from "vue-router";
import { reactive, computed, ref } from "vue";

import UInput from "@/components/UInput.vue";
import UButton from "@/components/UButton.vue";

// ═══════════════  Components variables  ═══════════════
const showPassword = reactive({
  password: false,
  confirmPassword: false
}
)

const route = useRoute();

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


const currentMode = computed(() => route.name || "Login");
const currentFields = computed(() => formFields[currentMode.value] || []);
const currentTexts = computed(() => authTexts[currentMode.value] || authTexts.Login);

// ═══════════════  Validación de formulario  ═══════════════
const isFormValid = computed(() => {
  // Todos los campos requeridos deben estar llenos y sin errores
  return currentFields.value.every(field => {
    return inputModels[field] && !inputErrors[field];
  });
});

function handleSubmit() {
  // Validaciones básicas por modo
  // Limpia errores
  currentFields.value.forEach(field => {
    inputErrors[field] = "";
  });

  // Email simple
  if (currentFields.value.includes("email")) {
    const email = inputModels.email;
    if (!email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
      inputErrors.email = "Correo electrónico inválido";
    }
  }

  // Passwords
  if (currentFields.value.includes("password")) {
    if (!inputModels.password || inputModels.password.length < 6) {
      inputErrors.password = "La contraseña debe tener al menos 6 caracteres";
    }
  }

  // Confirmar contraseña
  if (currentFields.value.includes("confirmPassword")) {
    if (inputModels.confirmPassword !== inputModels.password) {
      inputErrors.confirmPassword = "Las contraseñas no coinciden";
    }
  }

  // Si hay algún error, no continuar
  const hasError = currentFields.value.some(field => inputErrors[field]);
  if (hasError) return;

  // Aquí iría la lógica de submit real (API, etc.)
  alert(`Formulario enviado para modo: ${currentMode.value}`);
}

</script>

<style scoped lang="scss">
@import "@/assets/styles/pages/_user_auth.scss";
</style>




