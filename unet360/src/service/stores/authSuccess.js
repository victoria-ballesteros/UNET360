
// Pinia store para manejar el estado de pantallas de éxito en autenticación
// Simplificado y comentado para claridad y mantenibilidad
import { defineStore } from 'pinia';

export const useAuthSuccessStore = defineStore('authSuccess', {
  state: () => ({
    email: '',              // Email del usuario para mostrar en pantallas de éxito
    canAccessSuccess: false // Flag para controlar acceso a rutas de éxito
  }),
  actions: {
    // Guarda el email para mostrar en la pantalla de éxito
    setEmail(email) {
      this.email = email;
    },

    // Limpia el email almacenado
    clearEmail() {
      this.email = '';
    },

    // Permite acceso a la pantalla de éxito
    allowSuccess() {
      this.canAccessSuccess = true;
    },

    // Bloquea acceso a la pantalla de éxito
    blockSuccess() {
      this.canAccessSuccess = false;
    }
  }
});