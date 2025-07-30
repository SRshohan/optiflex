<script lang="ts">
	import { onMount } from 'svelte';
	import { WEBUI_API_BASE_URL } from '$lib/constants';
	let status: 'idle' | 'loading' | 'success' | 'error' = 'idle';
	let message = '';


	async function updateUserSettings() {
		const token = localStorage.getItem('token');
		if (!token) {
			status = 'error';
			message = 'You must be logged in.';
			return;
		}
		status = 'loading';
		try {
			const res = await fetch(`${WEBUI_API_BASE_URL}/payment/user/plan/update`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': `Bearer ${token}`
				},
				// body: JSON.stringify(newSettings)
			});
			const data = await res.json();
			if (res.ok) {
				status = 'success';
				message = 'Your account has been upgraded!';
			} else {
				status = 'error';
				message = 'Failed to update settings: ' + (data.detail || 'Unknown error');
			}
		} catch (err) {
			status = 'error';
			message = 'Network error: ' + err;
		}
	}

	onMount(() => {
		updateUserSettings();
	});
</script>

<div style="max-width: 500px; margin: 4rem auto; background: #23272f; color: #fff; border-radius: 1.5rem; padding: 2.5rem; text-align: center;">
	<h1>Payment Successful!</h1>
	{#if status === 'loading'}
		<p>Upgrading your account...</p>
	{:else if status === 'success'}
		<p style="color: #10a37f;">{message}</p>
	{:else if status === 'error'}
		<p style="color: #ff5a5f;">{message}</p>
	{:else}
		<p>Preparing your upgrade...</p>
	{/if}
</div>