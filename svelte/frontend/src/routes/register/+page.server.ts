import type { Actions } from './$types';

export const actions: Actions = {
	register: async ({ request }) => {
		const data = await request.formData();
		const username = data.get('username');
		const email = data.get('email');
		const password = data.get('password');
		const companyId = data.get('companyId');

		// TODO: Add your registration logic here, e.g., call your backend API

		console.log('Registering user:', { username, email, password, companyId });

		return { success: true };
	}
};