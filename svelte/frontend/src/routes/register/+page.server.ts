// src/routes/register/+page.server.ts
import { fail, redirect } from '@sveltejs/kit';
import type { Actions } from './$types';
import { register } from '$lib/api/login';

export const actions: Actions = {
  register: async ({ request }) => {
    const form = await request.formData();
    const username = form.get('username') as string;
    const email = form.get('email') as string;
    const password = form.get('password') as string;
    const companyId = form.get('companyId') as string;

    const data = await register(username, password, email, companyId);

    if (data.error) {
      return fail(400, { error: JSON.stringify(data) });
    }

    throw redirect(302, '/login');
  }
};
