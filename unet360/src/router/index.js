import { createRouter, createWebHistory } from "vue-router";
import { useUserStore } from "@/service/stores/user";

// Node related pages
import NodeCreate from "@/pages/UNodeCreate.vue";

// Other pages
import Home from "@/pages/UHome.vue";
import Showcase from "@/pages/UShowcase.vue";
import Auth from "@/pages/UAuth.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/showcase",
    name: "Showcase",
    component: Showcase,
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
        path: "auth",
        name: "Auth",
        component: Auth,
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
