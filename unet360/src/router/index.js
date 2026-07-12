import { createRouter, createWebHistory } from "vue-router";
// Importa el store de autenticación global
import { useAuthStore } from "@/service/stores/auth";

// Node related pages
import NodeCreate from "@/pages/UNodeCreate.vue";
import NodeAdmin from "@/pages/UNodeAdmin.vue";

// Other pages
import Home from "@/pages/UHome.vue";
import Showcase from "@/pages/UShowcase.vue";
import Auth from "@/pages/UAuth.vue";
import AuthSuccess from "@/pages/UAuthSuccess.vue";
import Map from "@/pages/UMap.vue";
import About from "@/pages/UAbout.vue";
import UEntityEdit from "@/pages/UEntityEdit.vue";
import UAdminEntities from "@/pages/UAdminEntities.vue";
import Documentation from "@/pages/UDocumentation.vue";

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
    component: About,
  },
  {
    path: "/nodes",
    children: [
      {
        path: "create",
        name: "NodeCreate",
        component: NodeCreate,
        meta: { requiresAuth: true, requiresAdmin: true },
      },
      {
        path: "admin",
        name: "NodeAdmin",
        component: NodeAdmin,
        meta: { requiresAuth: true, requiresAdmin: true },
      },

      {
        path: "manage/:entity(tags|locations)",
        name: "AdminEntities",
        component: UAdminEntities,
        meta: { requiresAuth: true, requiresAdmin: true },
        props: true,
      },
      {
        path: "manage/:entity(tags|locations)/edit/:name?",
        name: "EntityEdit",
        component: UEntityEdit,
        meta: { requiresAuth: true, requiresAdmin: true },
        props: true,
      },
    ],
  },
  {
    path: "/documentation",
    name: "Documentation",
    component: Documentation,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: "/admin/tenants",
    name: "AdminTenants",
    component: UAdminEntities,
    meta: { requiresAuth: true, requiresAdmin: true, entity: "tenants" },
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
      {
        path: "newpassword",
        name: "NewPassword",
        component: Auth,
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

    // 1. Detectar e interceptar hash de Supabase antes de evaluar autenticación
    const hash = window.location.hash;

    if (hash && hash.includes("access_token")) {
      const params = new URLSearchParams(hash.substring(1));

      const accessToken = params.get("access_token");
      const refreshToken = params.get("refresh_token");
      const type = params.get("type");

      if (accessToken) {

        // CONFIRMACIÓN DE CUENTA
        if (type === "signup") {

          document.cookie = `auth=${accessToken}; path=/`;

          auth.token = accessToken;
          auth.isAuthenticated = true;

          sessionStorage.setItem("supabase_signup", "true");

          window.history.replaceState(
            null,
            null,
            window.location.pathname
          );

          return next({ name: "SuccessConfirmation" });
        }

        // RECUPERACIÓN DE CONTRASEÑA
        if (type === "recovery") {

          sessionStorage.setItem(
            "recovery_access_token",
            accessToken
          );

          sessionStorage.setItem(
            "recovery_refresh_token",
            refreshToken || ""
          );

          window.history.replaceState(
            null,
            null,
            "/user/newpassword"
          );

          return next({
            name: "NewPassword"
          });
        }

        // LOGIN GOOGLE
        document.cookie = `auth=${accessToken}; path=/`;

        auth.token = accessToken;
        auth.isAuthenticated = true;

        window.history.replaceState(
          null,
          null,
          window.location.pathname
        );
      }
    }

    auth.checkAuthCookie();

    const authOnlyRoutes = ["Login", "Signup", "Recovery", "SuccessNewPassword", "SuccessPrePassword"];
    const isAuthRoute = authOnlyRoutes.includes(to.name);

    let isSupabaseSignup = sessionStorage.getItem('supabase_signup') === 'true';

    const isAuthenticated = await auth.validateToken();

    if (isAuthRoute && isAuthenticated) {
      return next({ name: "Home" });
    }

    if (to.name === "SuccessConfirmation" && !isSupabaseSignup) {
      return next({ name: "Login" });
    }

    if (to.meta.requiresAuth && !isAuthenticated) {
      return next({ name: "Login", query: { redirect: to.fullPath } });
    }

    // Rutas que requieren rol de administrador
    if (to.meta.requiresAdmin) {
      // Si no está autenticado ya fue manejado arriba; aquí confirmamos y verificamos rol
      if (!isAuthenticated) {
        return next({ name: "Login", query: { redirect: to.fullPath } });
      }
      const isAdmin = auth.user?.role === "admin";
      if (!isAdmin) {
        return next({ name: "Home" });
      }
    }

    next();
  } catch (error) {
    console.error("Error en beforeEach:", error);
    next({ name: "Login" });
  }
});

export default router;