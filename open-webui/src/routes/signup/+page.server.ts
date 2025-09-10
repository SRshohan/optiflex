import { fail, redirect } from '@sveltejs/kit';

export const actions = {
	default: async ({ request }) => {
		const data = await request.formData();
		const userData = {
			name: data.get('name'),
			email: data.get('email'),
			password: data.get('password'),
			profile_image_url: '/user.png'
		};
		console.log(userData);

		const response = await fetch('http://localhost:8080/api/v1/auths/signup', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			credentials: 'include',
			body: JSON.stringify({
				name: data.get('name'),
				email: data.get('email'),
				password: data.get('password'),
				profile_image_url: '/user.png'
			})
		});

		const result = await response.json();

		if (response.ok) {
			return { success: true, data: result };
		}
		return fail(401, { error: 'Something went wrong!!' });
	}
};
