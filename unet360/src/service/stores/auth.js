
// Pinia store para autenticación global
import { defineStore } from 'pinia';
import api from "@/axios";
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null,           // Token Bearer de autenticación
    user: null,            // Datos del usuario autenticado
    isAuthenticated: false,// Flag de sesión activa
    loading: false,        // Estado de carga para feedback visual
    error: null            // Mensaje de error para mostrar en UI
  }),
  actions: {
    // Obtiene el token de la cookie 'auth'. Útil para persistencia entre sesiones.
    checkAuthCookie() {
      const match = document.cookie.match(/(^|;)\s*auth=([^;]*)/);
      this.token = match ? match[2] : null;
      api.defaults.headers.common["Authorization"] = `Bearer ${this.token}`;
      this.isAuthenticated = !!this.token;
    },

    // Valida el token con el backend usando /auth/status
    async validateToken() {
      this.loading = true;
      let valid = false;
      if (this.token) {
        try {
          const res = await fetch(`${API_BASE_URL}/auth/status`, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${this.token}` }
          });

          const data = await res.json();
          valid = res.ok && data.status;

          if (valid) {
            if (data.response_obj.user_id) {
              const userRes = await fetch(`${API_BASE_URL}/tenants/${data.response_obj.user_id}`, {
                  method: 'GET',
                  headers: { 'Authorization': `Bearer ${this.token}` }
              });
              const userData = await userRes.json();
              this.user = userData.response_obj;
            }
          }
        } catch (e) {
          valid = false;
        }
      }
      this.isAuthenticated = valid;
      this.loading = false;
      if (!valid) this.token = null;
      return valid;
    },

    // Inicia sesión con email y password
    async login(email, password) {
      this.loading = true;
      try {
        const res = await fetch(`${API_BASE_URL}/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });
        const data = await res.json();
        if (res.ok && data.response_obj && data.response_obj.access_token) {
          this.token = data.response_obj.access_token;
          document.cookie = `auth=${this.token}; path=/`;
          this.isAuthenticated = true;
          this.error = null;
        } else {
          this.error = data.response_obj.message || 'Login failed.';
          this.isAuthenticated = false;
        }
      } catch (e) {
        this.error = 'Error de red';
        this.isAuthenticated = false;
      }
      this.loading = false;
    },

    // Cierra sesión y elimina token de cookie
    logout() {
      this.token = null;
      this.user = null;
      this.isAuthenticated = false;
      document.cookie = "auth=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
    },

    // Registra un nuevo usuario
    async signup(email, password) {
      this.loading = true;
      let result = { success: false, message: 'Error en el registro' };
      try {
        const res = await fetch(`${API_BASE_URL}/auth/signup`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });
        const data = await res.json();
        result.success = res.ok && data.status;
        result.message = data.response_obj?.message || result.message;
      } catch (e) {
        this.error = 'Error de red';
        result.message = 'Error de red';
      }
      this.loading = false;
      return result;
    },

    // Envía email de recuperación de contraseña
    async sendRecoveryEmail(email) {
      this.loading = true;
      // Aquí iría la lógica real para enviar el email
      this.loading = false;
    },

    // Cambia la contraseña del usuario autenticado
    async changePassword(newPassword) {
      this.loading = true;
      // Aquí iría la lógica real para cambiar la contraseña usando el token
      this.loading = false;
    }
  }
});
