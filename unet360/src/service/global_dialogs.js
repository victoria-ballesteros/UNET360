// ═══════════════   Layout related dialogs  ═══════════════

export const getSidebarOptions = (authState, isAdmin = null) => {
  if (!authState) {
    return [
      { label: "Inicia sesión", to: { name: "Login" } },
      { label: "Regístrate", to: { name: "Signup" } },
      { label: "Acerca de", to: { name: "About" } },
    ];
  }

  if (isAdmin == "admin") {
    return [
      { label: "Administrar nodos", to: { name: "NodeCreate" } },
      { label: "Acerca de", to: { name: "About" } },
      { label: "Cerrar sesión", action: "logout" },
    ];
  }

  return [
    { label: "Acerca de", to: { name: "About" } },
    { label: "Mapa 360", to: { name: "Map" } },
    { label: "Cerrar sesión", action: "logout" },
  ];
};

// ═══════════════   Home related dialogs  ═══════════════

export const getCardsInfo = () => {
  return [
    {
      text: "Encuentra aulas, baños o servicios en segundos",
      icon: "icons/binoculars",
    },
    {
      text: "Explora el campus como si estuvieras allí",
      icon: "icons/aperture",
    },
    {
      text: "Llega rápido con señalamiento paso a paso",
      icon: "icons/route",
    },
  ];
};

export const getGeneralInfo = () => {
  return "Navega el campus con mapas 360°, rutas personalizadas y búsqueda inteligente. Olvídate de perderte y disfruta de una experiencia universitaria fluida.";
};

export const getButtonData = (authStatus = false) => ({
  label: authStatus ? "Ir al mapa" : "Empieza ahora",
  route: authStatus ? "Map" : "Login",
});
