// ═══════════════   Layout related dialogs  ═══════════════

export const getSidebarOptions = (authState, isAdmin = null) => {
  if (isAdmin == "admin") {
    return [
      { label: "Administrar nodos", to: { name: "NodeAdmin" } },
      { label: "Administrar usuarios", to: { name: "AdminTenants" } },
      { label: "Acerca de", to: { name: "About" } },
      { label: "Cerrar sesión", action: "logout" },
    ];
  }

  return [
    { label: "Inicia sesión", to: { name: "Login" } },
    { label: "Regístrate", to: { name: "Signup" } },
    { label: "Acerca de", to: { name: "About" } },
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
  return "Navega el campus con mapas 360°, rutas personalizadas y búsqueda inteligente. Disfruta de una experiencia universitaria fluida donde perderse es cosa del pasado.";
};

export const getButtonData = (authStatus = false) => ({
  label: authStatus ? "Ir al mapa" : "Empieza ahora",
  route: authStatus ? "Map" : "Login",
});
