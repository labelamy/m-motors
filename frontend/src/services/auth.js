
// Retourne l'utilisateur actuel stocké dans localStorage (depuis le login)
export function getCurrentUser() {
  const user = localStorage.getItem("user");
  return user ? JSON.parse(user) : null;
}

// Stocke l'utilisateur après login
export function setCurrentUser(user) {
  localStorage.setItem("user", JSON.stringify(user));
}

// Supprime l'utilisateur (logout)
export function removeCurrentUser() {
  localStorage.removeItem("user");
}

export const getToken = () => {
  const token = localStorage.getItem("token");
  if (!token) return null;

  // On peut aussi décoder le token pour vérifier sa validité (optionnel)
  // Ici on se contente de vérifier qu'il existe
  return token;
};

export const logout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("currentUser");
};