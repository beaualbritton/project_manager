// src/lib/api/login.ts
import { API_URL } from "$lib/config";

async function getCsrf(): Promise<string> {
  const res = await fetch(`${API_URL}/auth/csrf/`, { credentials: "include" });
  const data = await res.json();
  return data.csrfToken;
}

export async function login(username: string, password: string) {
  const csrf = await getCsrf();
  const res = await fetch(`${API_URL}/auth/login/`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrf },
    credentials: "include",
    body: JSON.stringify({ username, password }),
  });
  return await res.json();
}

export async function logout() {
  const csrf = await getCsrf();
  const res = await fetch(`${API_URL}/auth/logout/`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrf },
    credentials: "include",
  });
  return await res.json();
}

export async function register(username: string, password: string, email: string, companyId: string) {
  const csrf = await getCsrf();
  const res = await fetch(`${API_URL}/auth/register/`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrf },
    credentials: "include",
    body: JSON.stringify({ username, password, email, company_id: companyId }),
  });
  return await res.json();
}
