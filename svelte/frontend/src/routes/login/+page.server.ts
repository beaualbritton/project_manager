// src/routes/login/+page.server.ts
import { fail, redirect } from '@sveltejs/kit';
import type { Actions } from './$types';
import { API_URL } from '$lib/config';

export const actions: Actions = {
  default: async ({ request, cookies, fetch }) => {
    const form = await request.formData();
    const username = form.get('username') as string;
    const password = form.get('password') as string;

    // Get CSRF
    const csrfRes = await fetch(`${API_URL}/auth/csrf/`);
    const { csrfToken } = await csrfRes.json();

    // Login
    const res = await fetch(`${API_URL}/auth/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
      body: JSON.stringify({ username, password }),
    });

    if (!res.ok) return fail(401, { error: 'Invalid username or password' });

    // Extract sessionid from Django's response and store it in SvelteKit cookies
    const setCookie = res.headers.get('set-cookie') ?? '';
    const sessionMatch = setCookie.match(/sessionid=([^;]+)/);
    if (sessionMatch) {
      cookies.set('sessionid', sessionMatch[1], {
        path: '/',
        httpOnly: true,
        sameSite: 'lax',
        secure: false,
      });
    }

    throw redirect(302, '/tasks');
  }
};
