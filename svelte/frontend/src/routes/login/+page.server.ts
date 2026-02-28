// src/routes/login/+page.server.ts
import { fail, redirect } from '@sveltejs/kit';
import type { Actions } from './$types';
import { login } from '$lib/api/login';

export const actions: Actions = {
  default: async ({ request, cookies }) => {
    const form = await request.formData();
    const username = form.get('username') as string;
    const password = form.get('password') as string;

    const data = await login(username, password);

    if (data.error) {
      return fail(401, { error: data.error });
    }

    throw redirect(302, '/tasks');
  }
};
