import { createRouter, createWebHistory } from "vue-router";
// Importa el store de autenticación global
import { useAuthStore } from "@/service/stores/auth";

// Node related pages
import NodeCreate from "@/pages/UNodeCreate.vue";
import NodeAdmin from "@/pages/UNodeAdmin.vue";
import NodeEdit from "@/pages/UNodeEdit.vue";

// Other pages
import Home from "@/pages/UHome.vue";
import Showcase from "@/pages/UShowcase.vue";
import Auth from "@/pages/UAuth.vue";
import AuthSuccess from "@/pages/UAuthSuccess.vue";
import Map from "@/pages/UMap.vue";
import About from "@/pages/UAbout.vue";
import UEntityEdit from "@/pages/UEntityEdit.vue";
import UAdminEntities from "@/pages/UAdminEntities.vue";

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
        path: "edit/:name",
        name: "NodeEdit",
        component: NodeEdit,
        meta: { requiresAuth: true, requiresAdmin: true },
        props: true,
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
    auth.checkAuthCookie();

    const authOnlyRoutes = ["Login", "Signup", "Recovery", "NewPassword", "SuccessNewPassword", "SuccessPrePassword"];
    const isAuthRoute = authOnlyRoutes.includes(to.name);

    const hash = window.location.hash;
    let isSupabaseSignup = hash.includes('access_token') && hash.includes('type=signup');
    if (!isSupabaseSignup && sessionStorage.getItem('supabase_signup') === 'true') {
      isSupabaseSignup = true;
    }

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


// Detecta el hash de Supabase y redirige a success-confirmation si corresponde
function handleSupabaseRedirect(router) {
  const hash = window.location.hash;
  // Confirmación de registro
  if (hash.includes('access_token') && hash.includes('type=signup')) {
    sessionStorage.setItem('supabase_signup', 'true');
    import('@/service/stores/auth').then(mod => {
      mod.useAuthStore().successState = true;
      router.replace({ name: 'SuccessConfirmation' });
    });
  }
  // Recuperación de contraseña
  if (hash.includes('access_token') && hash.includes('type=recovery')) {
    router.replace({ name: 'NewPassword', hash });
  }
}

setTimeout(() => handleSupabaseRedirect(router), 0);

export default router;
