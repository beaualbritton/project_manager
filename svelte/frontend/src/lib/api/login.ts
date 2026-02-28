//login, logout, register
import { API_URL } from "$lib/config";

let csrf : string;

export async function getCsrf()
{
  const csrfResponse= await fetch(`${API_URL}/csrf/`, {
    credentials: "include"
  });

  let data = await csrfResponse.json();
  csrf = data.csrfToken;

  return csrf; 
}

export async function login(username: string, password: string)
{
  let csrfToken = await getCsrf();

  const apiResponse = await fetch(`${API_URL}/login/`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken},
    //cookies for session 
    credentials: "include",
    body: JSON.stringify({ username,password }),
  });
  return await apiResponse.json();
}

export async function logout()
{
  let csrfToken = await getCsrf();

  const apiResponse = await fetch(`${API_URL}/logout/`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken},
    //cookies for session 
    credentials: "include",
  });

  return await apiResponse.json();
}


export async function register(username: string, password: string)
{
  let csrfToken = await getCsrf();

  const apiResponse = await fetch(`${API_URL}/register/`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken},
    //cookies for session 
    credentials: "include",
    body: JSON.stringify({ username,password }),
  });
  return await apiResponse.json();
}
