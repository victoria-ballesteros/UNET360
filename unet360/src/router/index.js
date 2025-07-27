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
import Map from "@/pages/UMap.vue";

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
    {
    path: "/360-map",
    name: "Map",
    component: Map,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Guard global para proteger rutas que requieren autenticación
router.beforeEach(async (to, from, next) => {
  try {
    const auth = useAuthStore();
    auth.checkAuthCookie();

    const authOnlyRoutes = ["Login", "Signup", "Recovery", "SuccessRegister", "SuccessNewPassword", "SuccessPrepassword", "SuccessConfirmation"];
    const isAuthRoute = authOnlyRoutes.includes(to.name);
    const isAuthenticated = await auth.validateToken();

    if (isAuthRoute && isAuthenticated) {
      next({ name: "Home" });
      return;
    }

    if (to.meta.requiresAuth && !isAuthenticated) {
      next({ name: "Login", query: { redirect: to.fullPath } });
      return;
    }

    next();
  } catch (error) {
    console.error("Error en router.beforeEach:", error);
    next({ name: "Login" });
  }
});

export default router;
