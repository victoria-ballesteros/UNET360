export function getSidebarOptions(authState, isAdmin = false) {
  if (!authState) {
    return [
      { label: "Inicia sesión", to: { name: "Auth" } },
      { label: "Regístrate", to: { name: "Auth" } },
      { label: "Acerca de", to: { name: "About" } },
    ];
  }

  if (isAdmin) {
    return [
      { label: "Administrar nodos", to: { name: "NodeCreate" } },
      { label: "Acerca de", to: { name: "About" } },
      { label: "Cerrar sesión", to: { name: "Logout" } },
    ];
  }

  return [
    { label: "Acerca de", to: { name: "About" } },
    { label: "Cerrar sesión", to: { name: "Logout" } },
  ];
}
