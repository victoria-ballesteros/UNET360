import { createRouter, createWebHistory } from "vue-router";
// Importa el store de autenticación global
import { useAuthStore } from "@/service/stores/auth";

// Node related pages
import NodeCreate from "@/pages/UNodeCreate.vue";

// Other pages
import Home from "@/pages/UHome.vue";
import Showcase from "@/pages/UShowcase.vue";
import Auth from "@/pages/UAuth.vue";
import AuthSuccess from "@/pages/UAuthSuccess.vue";

const routes = [
  {
    path: "/Home",
    name: "Home",
    component: Home,
    alias: "/",
  },
  {
    path: "/showcase",
    name: "Showcase",
    component: Showcase,
  },
  {
    path: "/about",
    name: "About",
    component: Home,
  },
  {
    path: "/nodes",
    children: [
      {
        path: "create",
        name: "NodeCreate",
        component: NodeCreate,
        meta: { requiresAuth: true },
      },
    ],
  },
  {
    path: "/user",
    children: [
      {
        path: "login",
        name: "Login",
        component: Auth,
      },
      {
        path: "signup",
        name: "Signup",
        component: Auth,
      },
      {
        path: "recovery",
        name: "Recovery",
        component: Auth,
      },
      {
        path: "success-register",
        name: "SuccessRegister",
        component: AuthSuccess,
      },
      {
        path: "success-newpassword",
        name: "SuccessNewPassword",
        component: AuthSuccess,
      },
      {
        path: "success-prepassword",
        name: "SuccessPrePassword",
        component: AuthSuccess,
      },
      {
        path: "success-confirmation",
        name: "SuccessConfirmation",
        component: AuthSuccess,
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Guard global para proteger rutas que requieren autenticación
router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore();
  auth.checkAuthCookie(); // Sincroniza el token desde la cookie en cada navegación
  
  const authOnlyRoutes = ["Login", "Signup", "Recovery", "SuccessRegister", "SuccessNewPassword", "SuccessPrePassword", "SuccessConfirmation"];
  const isAuthRoute = authOnlyRoutes.includes(to.name);
  const isAuthenticated = await auth.validateToken();

  // Si el usuario está autenticado y visita una ruta de autenticación, redirige al Home
  if (isAuthRoute && isAuthenticated) {
    next({ name: "Home" });
    return;
  }

  // Si la ruta requiere autenticación, valida el token con backend
  if (to.meta.requiresAuth) {
    if (!isAuthenticated) {
      next({ name: "Login", query: { redirect: to.fullPath } });
      return;
    }
  }
  next();
});

export default router;
