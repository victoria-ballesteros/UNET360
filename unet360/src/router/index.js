import { createRouter, createWebHistory } from "vue-router";
import { useUserStore } from "@/service/stores/user";

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

router.beforeEach(async (to, from, next) => {
  const store = useUserStore();

  if (store.authState === null) {
    await store.fetchUserState();
  }

  const isAuth = store.authState;

  if (to.meta.requiresAuth && !isAuth) {
    next({ name: "Auth" });
  } else {
    next();
  }
});

export default router;
