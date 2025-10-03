import type { Usuario } from "../types/usuario";

const API_URL = "http://localhost:8001/usuarios";

export async function loginUsuario(email: string, password: string): Promise<{ user: Usuario; token: string }> {
  const response = await fetch(`${API_URL}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) throw new Error("Credenciales inválidas");
  return response.json(); // { user, token }
}

export async function createUsuarioWithRol(usuario: Omit<Usuario, "id">, rol_id: number): Promise<Usuario> {
  const response = await fetch(`${API_URL}/with-rol/?rol_id=${rol_id}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(usuario),
  });

  if (!response.ok) throw new Error("Error al crear el usuario");
  return response.json();
}

export async function logoutUsuario(): Promise<void> {
  localStorage.removeItem("token");
  return Promise.resolve();
}
