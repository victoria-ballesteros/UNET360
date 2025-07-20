export function getSidebarOptions(authState, isAdmin = false) {
  if (!authState) {
    return [
      { label: "Inicia sesión", to: "/auth" },
      { label: "Regístrate", to: "/auth" },
      { label: "Acerca de", to: "/about" },
    ];
  }

  if (isAdmin) {
    return [
      { label: "Administrar nodos", to: "/nodes/create" },
      { label: "Acerca de", to: "/about" },
      { label: "Cerrar sesión", to: "/logout" },
    ];
  }

  return [
    { label: "Acerca de", to: "/about" },
    { label: "Cerrar sesión", to: "/logout" },
  ];
}
