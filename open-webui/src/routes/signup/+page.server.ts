import { fail, redirect } from '@sveltejs/kit';

export const actions = {
	default: async ({ request }) => {
		const data = await request.formData();

		return fail(401, { error: 'Server is busy!' });
		throw redirect(303, '/auth');
	}
};
