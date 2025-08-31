import { fail, redirect } from '@sveltejs/kit';
import { toast } from 'svelte-sonner';
import { config, user, socket } from '$lib/stores';
import { getBackendConfig } from '$lib/apis';
import { goto } from '$app/navigation';

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
			body: JSON.stringify(userData)
		});
		console.log(response);

		if (response.ok) {
			return { success: true, response };
		}
		return fail(401, { error: 'Something went wrong!!' });
	}
};

const querystringValue = (key) => {
	const querystring = window.location.search;
	const urlParams = new URLSearchParams(querystring);
	return urlParams.get(key);
};

const setSessionUser = async (sessionUser) => {
	if (sessionUser) {
		toast.success($i18n.t(`You're now logged in.`));
		if (sessionUser.token) {
			localStorage.token = sessionUser.token;
		}
		$socket.emit('user-join', { auth: { token: sessionUser.token } });
		await user.set(sessionUser);
		await config.set(await getBackendConfig());

		const redirectPath = querystringValue('redirect') || '/';
		goto(redirectPath);
	}
};
