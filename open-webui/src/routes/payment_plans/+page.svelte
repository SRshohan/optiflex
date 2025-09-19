<script lang="ts">
	import { goto } from '$app/navigation';
	import { WEBUI_API_BASE_URL } from '$lib/constants';

	const token = localStorage.getItem('token');

    async function getUserEmail(token: string) {
        if (!token) {
			alert('No token found');
            return null;
        }
		try {
		// alert(`Fetching user email from ${WEBUI_API_BASE_URL}/auths/`);
        const res = await fetch(`${WEBUI_API_BASE_URL}/auths/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });

		if (!res.ok) {
			console.error('Failed to get user email:', res.status);
			const errorText = await res.text();
			console.error('Failed to get user email errortext: ' + errorText);
			return null;
		}
			const data = await res.json();
			return data.email;
		} catch (error) {
			console.error('Error getting user email:', error);
			return null;
		}
    }

	async function handleUpgrade(plan: string) {
		if (plan === 'pro') {
			// const token = localStorage.getItem('token'); // Get the user's OpenWebUI token
			if (!token) {
				alert('You must be logged in to upgrade.');
				return;
			}
			const userEmail = await getUserEmail(token);
			if (!userEmail) {
				alert('Failed to get user email');
				return;
			}
			const res = await fetch(`${WEBUI_API_BASE_URL}/payment/checkout/stripe-webhook`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': `Bearer ${token}`
				},
                body: JSON.stringify({
                    user_email: userEmail,
					plan: plan
                })
			});
			if (res.ok) {
				const data = await res.json();
				if (data.checkout_url) {
					// Redirect to Stripe Checkout
					window.location.href = data.checkout_url;
				} else {
					alert('Failed to get checkout URL.');
				}
			} else {
				const err = await res.json();
				alert('Upgrade failed: ' + (err.detail || 'Unknown error'));
			}
		} else if (plan === 'starter') {
			// const token = localStorage.getItem('token'); // Get the user's OpenWebUI token
			// if (!token) {
			// 	alert('You must be logged in to upgrade.');
			// 	return;
			// }
			// const userEmail = await getUserEmail(token);
			// if (!userEmail) {
			// 	alert('Failed to get user email');
			// 	return;
			// }
			// const res = await fetch(`${WEBUI_API_BASE_URL}/payment/checkout/stripe-webhook`, {
			// 	method: 'POST',
			// 	headers: {
			// 		'Content-Type': 'application/json',
			// 		'Authorization': `Bearer ${token}`
			// 	},
            //     body: JSON.stringify({
            //         user_email: userEmail,
			// 		plan: plan
            //     })
			// });
			// if (res.ok) {
			// 	const data = await res.json();
			// 	if (data.checkout_url) {
			// 		// Redirect to Stripe Checkout
			// 		window.location.href = data.checkout_url;
			// 	} else {
			// 		alert('Failed to get checkout URL.');
			// 	}
			// } else {
			// 	const err = await res.json();
			// 	alert('Upgrade failed: ' + (err.detail || 'Unknown error'));
			// }
			goto('/');
		} else if (plan === 'custom') {
			window.location.href = 'mailto:sales@optiflex.ai'; // Or open a contact form
		}
	}
</script>

<style>
/* Global resets and box-sizing */
:global(html, body) {
  margin: 0;
  padding: 0;
  height: 100%;
  box-sizing: border-box;
  /* Ensure the viewport can scroll vertically when needed */
  overflow-y: auto;
}

/* Root container: full-height and both axes scrollable */
.pricing-root {
  height: 100vh;
  overflow-y: auto;
  overflow-x: auto;
  background: #181c23;
}

/* Header section */
.pricing-header {
  text-align: center;
  margin: 3rem 0 2.5rem;
}
.pricing-title {
  font-size: 2.8rem;
  font-weight: 900;
  letter-spacing: -0.03em;
  color: #fff;
  margin-bottom: 0.5rem;
}
.pricing-subtitle {
  font-size: 2rem;
  font-weight: 700;
  color: #10a37f;
  margin-bottom: 0.5rem;
}
.pricing-desc {
  font-size: 1.15rem;
  color: #b0b6c3;
  margin-bottom: 2.5rem;
}

/* Responsive grid for the cards */
.pricing-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2.5rem;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem 4rem;
}

/* Card base styling */
.pricing-card {
  border-radius: 2rem;
  box-shadow: 0 4px 32px rgba(16, 163, 127, 0.13);
  padding: 3rem 2.5rem;
  transition: border 0.2s, box-shadow 0.2s;
}

/* Highlighted (“featured”) card */
.pricing-card.featured {
  box-shadow: 0 8px 40px rgba(16, 163, 127, 0.18);
}

/* Plan title & price */
.pricing-plan-title {
  font-size: 1.6rem;
  font-weight: 800;
  margin-bottom: 0.7rem;
  letter-spacing: 0.01em;
  color: #fff;
}
.pricing-price {
  font-size: 2.7rem;
  font-weight: 900;
  margin-bottom: 0.7rem;
  color: #10a37f;
}
.pricing-plan-desc {
  color: #b0b6c3;
  margin-bottom: 2rem;
  text-align: center;
  font-size: 1.1rem;
}

/* Feature list */
.pricing-features {
  list-style: none;
  padding: 0;
  margin: 0 0 2rem 0;
  width: 100%;
}
.pricing-features li {
  margin: 0.7rem 0;
  display: flex;
  align-items: center;
  gap: 0.7rem;
  font-size: 1.1rem;
}
.pricing-features li.negative {
  color: #ff5a5f;
}

/* Buttons */
.pricing-btn {
  background: #10a37f;
  color: white;
  border: none;
  border-radius: 999px;
  padding: 1rem 2.5rem;
  font-size: 1.15rem;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s;
  box-shadow: 0 2px 8px rgba(16, 163, 127, 0.10);
  margin-top: auto;
}
.pricing-btn:hover {
  background: #0e8c6b;
}

/* Small-screen tweaks */
@media (max-width: 400px) {
  .pricing-plan-title {
    font-size: 1.4rem;
  }
  .pricing-price {
    font-size: 2.4rem;
  }
}

</style>

<svelte:head>
	<title>Pricing | Optiflex.Ai</title>
</svelte:head>

<div class="pricing-root">
	<div class="pricing-header">
		<div class="pricing-title">Optiflex.Ai</div>
		<div class="pricing-subtitle">Pricing</div>
		<div class="pricing-desc">See pricing for individual needs</div>
	</div>
	<div class="pricing-container">
		<!-- Starter Plan -->
		<div class="pricing-card flex flex-col items-start gap-8 py-4 bg-black/20 backdrop-blur-sm">
			<div class="text-lg bg-gray-700/30 px-4 py-2 rounded-full mx-auto">Starter</div>
			<div class="text-4xl text-primary mx-auto">Free</div>
			<div class="text-medium text-center text-gray-500">Get started with basic features and limited usage.</div>
			<ul class="flex flex-col items-start justify-center gap-3 my-5">
				<li class="flex justify-start gap-2">
					<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="18" height="18" viewBox="0 0 256 256" xml:space="preserve">
						<g style="stroke: none; stroke-width: 0; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: none; fill-rule: nonzero; opacity: 1;" transform="translate(1.4065934065934016 1.4065934065934016) scale(2.81 2.81)">
							<path d="M 85 90 H 5 c -2.761 0 -5 -2.238 -5 -5 V 5 c 0 -2.761 2.239 -5 5 -5 h 80 c 2.762 0 5 2.239 5 5 v 80 C 90 87.762 87.762 90 85 90 z" style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(39,196,72); fill-rule: nonzero; opacity: 1;" transform=" matrix(1 0 0 1 0 0) " stroke-linecap="round"/>
							<path d="M 38.269 64.615 c -1.28 0 -2.559 -0.488 -3.536 -1.465 L 18.964 47.383 c -1.953 -1.953 -1.953 -5.119 0 -7.071 c 1.953 -1.952 5.118 -1.952 7.071 0 l 12.233 12.232 l 25.696 -25.695 c 1.951 -1.952 5.119 -1.952 7.07 0 c 1.953 1.953 1.953 5.119 0 7.071 L 41.804 63.15 C 40.828 64.127 39.548 64.615 38.269 64.615 z" style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(255,255,255); fill-rule: nonzero; opacity: 1;" transform=" matrix(1 0 0 1 0 0) " stroke-linecap="round"/>
						</g>
					</svg>
					 Basic chat access</li>
				<li class="flex justify-start gap-2">
					<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="18" height="18" viewBox="0 0 256 256" xml:space="preserve">
						<g style="stroke: none; stroke-width: 0; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: none; fill-rule: nonzero; opacity: 1;" transform="translate(1.4065934065934016 1.4065934065934016) scale(2.81 2.81)">
							<path d="M 85 90 H 5 c -2.761 0 -5 -2.238 -5 -5 V 5 c 0 -2.761 2.239 -5 5 -5 h 80 c 2.762 0 5 2.239 5 5 v 80 C 90 87.762 87.762 90 85 90 z" style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(39,196,72); fill-rule: nonzero; opacity: 1;" transform=" matrix(1 0 0 1 0 0) " stroke-linecap="round"/>
							<path d="M 38.269 64.615 c -1.28 0 -2.559 -0.488 -3.536 -1.465 L 18.964 47.383 c -1.953 -1.953 -1.953 -5.119 0 -7.071 c 1.953 -1.952 5.118 -1.952 7.071 0 l 12.233 12.232 l 25.696 -25.695 c 1.951 -1.952 5.119 -1.952 7.07 0 c 1.953 1.953 1.953 5.119 0 7.071 L 41.804 63.15 C 40.828 64.127 39.548 64.615 38.269 64.615 z" style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(255,255,255); fill-rule: nonzero; opacity: 1;" transform=" matrix(1 0 0 1 0 0) " stroke-linecap="round"/>
						</g> 
					</svg>
					Community support</li>
				<li class="flex justify-start gap-2">
					<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="18" height="18" viewBox="0 0 256 256" xml:space="preserve">
						<g style="stroke: none; stroke-width: 0; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: none; fill-rule: nonzero; opacity: 1;" transform="translate(1.4065934065934016 1.4065934065934016) scale(2.81 2.81)">
							<path d="M 11 90 c -2.815 0 -5.63 -1.074 -7.778 -3.222 c -4.295 -4.296 -4.295 -11.261 0 -15.557 l 68 -68 c 4.297 -4.296 11.26 -4.296 15.557 0 c 4.296 4.296 4.296 11.261 0 15.557 l -68 68 C 16.63 88.926 13.815 90 11 90 z" style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(214,0,0); fill-rule: nonzero; opacity: 1;" transform=" matrix(1 0 0 1 0 0) " stroke-linecap="round"/>
							<path d="M 79 90 c -2.815 0 -5.63 -1.074 -7.778 -3.222 l -68 -68 c -4.295 -4.296 -4.295 -11.261 0 -15.557 c 4.296 -4.296 11.261 -4.296 15.557 0 l 68 68 c 4.296 4.296 4.296 11.261 0 15.557 C 84.63 88.926 81.815 90 79 90 z" style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(214,0,0); fill-rule: nonzero; opacity: 1;" transform=" matrix(1 0 0 1 0 0) " stroke-linecap="round"/>
						</g>
					</svg> No API access</li>
				<li class="flex justify-start gap-2">
					<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="18" height="18" viewBox="0 0 256 256" xml:space="preserve">
						<g style="stroke: none; stroke-width: 0; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: none; fill-rule: nonzero; opacity: 1;" transform="translate(1.4065934065934016 1.4065934065934016) scale(2.81 2.81)">
							<path d="M 11 90 c -2.815 0 -5.63 -1.074 -7.778 -3.222 c -4.295 -4.296 -4.295 -11.261 0 -15.557 l 68 -68 c 4.297 -4.296 11.26 -4.296 15.557 0 c 4.296 4.296 4.296 11.261 0 15.557 l -68 68 C 16.63 88.926 13.815 90 11 90 z" style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(214,0,0); fill-rule: nonzero; opacity: 1;" transform=" matrix(1 0 0 1 0 0) " stroke-linecap="round"/>
							<path d="M 79 90 c -2.815 0 -5.63 -1.074 -7.778 -3.222 l -68 -68 c -4.295 -4.296 -4.295 -11.261 0 -15.557 c 4.296 -4.296 11.261 -4.296 15.557 0 l 68 68 c 4.296 4.296 4.296 11.261 0 15.557 C 84.63 88.926 81.815 90 79 90 z" style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(214,0,0); fill-rule: nonzero; opacity: 1;" transform=" matrix(1 0 0 1 0 0) " stroke-linecap="round"/>
						</g>
					</svg>
					No priority support</li>
			</ul>
			<button class="text-xl bg-gradient-to-r from-primary to-secondary w-full rounded-xl px-4 py-2 mt-auto" on:click={() => handleUpgrade('starter')}>Get Started</button>
		</div>

		<!-- Pro Plan (Featured) -->
		<div class="pricing-card flex flex-col items-start gap-8 py-4 bg-black/20 backdrop-blur-sm featured border-2 border-primary relative">
			<div class="absolute bg-gradient-to-r from-primary to-secondary text-500/40 px-4 py-2 rounded-full right-2 top-2">Popular</div>
			<div class="text-lg bg-gray-700/30 px-4 py-2 rounded-full mx-auto">Pro</div>
			<div class="text-4xl text-primary mx-auto">$20<span style="font-size:1.1rem;font-weight:500;">/mo</span></div>
			<div class="text-medium text-center text-gray-500">Unlock advanced features, higher limits, and priority support.</div>
			<ul class="flex flex-col items-start justify-center gap-3  my-5">
				<li class="flex justify-start gap-2">
					<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="18" height="18" viewBox="0 0 256 256" xml:space="preserve">
						<g style="stroke: none; stroke-width: 0; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: none; fill-rule: nonzero; opacity: 1;" transform="translate(1.4065934065934016 1.4065934065934016) scale(2.81 2.81)">
							<path d="M 85 90 H 5 c -2.761 0 -5 -2.238 -5 -5 V 5 c 0 -2.761 2.239 -5 5 -5 h 80 c 2.762 0 5 2.239 5 5 v 80 C 90 87.762 87.762 90 85 90 z" style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(39,196,72); fill-rule: nonzero; opacity: 1;" transform=" matrix(1 0 0 1 0 0) " stroke-linecap="round"/>
							<path d="M 38.269 64.615 c -1.28 0 -2.559 -0.488 -3.536 -1.465 L 18.964 47.383 c -1.953 -1.953 -1.953 -5.119 0 -7.071 c 1.953 -1.952 5.118 -1.952 7.071 0 l 12.233 12.232 l 25.696 -25.695 c 1.951 -1.952 5.119 -1.952 7.07 0 c 1.953 1.953 1.953 5.119 0 7.071 L 41.804 63.15 C 40.828 64.127 39.548 64.615 38.269 64.615 z" style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(255,255,255); fill-rule: nonzero; opacity: 1;" transform=" matrix(1 0 0 1 0 0) " stroke-linecap="round"/>
						</g>
					</svg> Everything in Starter</li>
				<li class="flex justify-start gap-2">
					<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="18" height="18" viewBox="0 0 256 256" xml:space="preserve">
						<g style="stroke: none; stroke-width: 0; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: none; fill-rule: nonzero; opacity: 1;" transform="translate(1.4065934065934016 1.4065934065934016) scale(2.81 2.81)">
							<path d="M 85 90 H 5 c -2.761 0 -5 -2.238 -5 -5 V 5 c 0 -2.761 2.239 -5 5 -5 h 80 c 2.762 0 5 2.239 5 5 v 80 C 90 87.762 87.762 90 85 90 z" style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(39,196,72); fill-rule: nonzero; opacity: 1;" transform=" matrix(1 0 0 1 0 0) " stroke-linecap="round"/>
							<path d="M 38.269 64.615 c -1.28 0 -2.559 -0.488 -3.536 -1.465 L 18.964 47.383 c -1.953 -1.953 -1.953 -5.119 0 -7.071 c 1.953 -1.952 5.118 -1.952 7.071 0 l 12.233 12.232 l 25.696 -25.695 c 1.951 -1.952 5.119 -1.952 7.07 0 c 1.953 1.953 1.953 5.119 0 7.071 L 41.804 63.15 C 40.828 64.127 39.548 64.615 38.269 64.615 z" style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(255,255,255); fill-rule: nonzero; opacity: 1;" transform=" matrix(1 0 0 1 0 0) " stroke-linecap="round"/>
						</g>
					</svg> Priority access to new features</li>
				<li class="flex justify-start gap-2">
					<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="18" height="18" viewBox="0 0 256 256" xml:space="preserve">
						<g style="stroke: none; stroke-width: 0; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: none; fill-rule: nonzero; opacity: 1;" transform="translate(1.4065934065934016 1.4065934065934016) scale(2.81 2.81)">
							<path d="M 85 90 H 5 c -2.761 0 -5 -2.238 -5 -5 V 5 c 0 -2.761 2.239 -5 5 -5 h 80 c 2.762 0 5 2.239 5 5 v 80 C 90 87.762 87.762 90 85 90 z" style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(39,196,72); fill-rule: nonzero; opacity: 1;" transform=" matrix(1 0 0 1 0 0) " stroke-linecap="round"/>
							<path d="M 38.269 64.615 c -1.28 0 -2.559 -0.488 -3.536 -1.465 L 18.964 47.383 c -1.953 -1.953 -1.953 -5.119 0 -7.071 c 1.953 -1.952 5.118 -1.952 7.071 0 l 12.233 12.232 l 25.696 -25.695 c 1.951 -1.952 5.119 -1.952 7.07 0 c 1.953 1.953 1.953 5.119 0 7.071 L 41.804 63.15 C 40.828 64.127 39.548 64.615 38.269 64.615 z" style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(255,255,255); fill-rule: nonzero; opacity: 1;" transform=" matrix(1 0 0 1 0 0) " stroke-linecap="round"/>
						</g>
					</svg> API access</li>
				<li class="flex justify-start gap-2">
					<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="18" height="18" viewBox="0 0 256 256" xml:space="preserve">
						<g style="stroke: none; stroke-width: 0; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: none; fill-rule: nonzero; opacity: 1;" transform="translate(1.4065934065934016 1.4065934065934016) scale(2.81 2.81)">
							<path d="M 85 90 H 5 c -2.761 0 -5 -2.238 -5 -5 V 5 c 0 -2.761 2.239 -5 5 -5 h 80 c 2.762 0 5 2.239 5 5 v 80 C 90 87.762 87.762 90 85 90 z" style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(39,196,72); fill-rule: nonzero; opacity: 1;" transform=" matrix(1 0 0 1 0 0) " stroke-linecap="round"/>
							<path d="M 38.269 64.615 c -1.28 0 -2.559 -0.488 -3.536 -1.465 L 18.964 47.383 c -1.953 -1.953 -1.953 -5.119 0 -7.071 c 1.953 -1.952 5.118 -1.952 7.071 0 l 12.233 12.232 l 25.696 -25.695 c 1.951 -1.952 5.119 -1.952 7.07 0 c 1.953 1.953 1.953 5.119 0 7.071 L 41.804 63.15 C 40.828 64.127 39.548 64.615 38.269 64.615 z" style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(255,255,255); fill-rule: nonzero; opacity: 1;" transform=" matrix(1 0 0 1 0 0) " stroke-linecap="round"/>
						</g>
					</svg> Priority support</li>
			</ul>
			<button class="text-xl bg-gradient-to-r from-primary to-secondary w-full rounded-xl px-4 py-2 mt-auto" on:click={() => handleUpgrade('pro')}>Upgrade to Pro</button>
		</div>

		<!-- Custom/Enterprise Plan -->
		<div class="pricing-card flex flex-col items-start gap-8 py-4 bg-black/20 backdrop-blur-sm">
			<div class="text-lg bg-gray-700/30 px-4 py-2 rounded-full mx-auto">Custom</div>
			<div class="text-4xl text-primary mx-auto">Contact Us</div>
			<div class="text-medium text-center text-gray-500">For teams and enterprises with custom needs and high volume.</div>
			<ul class="flex flex-col items-start justify-center gap-3  my-5">
				<li class="flex justify-start gap-2">
					<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="18" height="18" viewBox="0 0 256 256" xml:space="preserve">
						<g style="stroke: none; stroke-width: 0; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: none; fill-rule: nonzero; opacity: 1;" transform="translate(1.4065934065934016 1.4065934065934016) scale(2.81 2.81)">
							<path d="M 85 90 H 5 c -2.761 0 -5 -2.238 -5 -5 V 5 c 0 -2.761 2.239 -5 5 -5 h 80 c 2.762 0 5 2.239 5 5 v 80 C 90 87.762 87.762 90 85 90 z" style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(39,196,72); fill-rule: nonzero; opacity: 1;" transform=" matrix(1 0 0 1 0 0) " stroke-linecap="round"/>
							<path d="M 38.269 64.615 c -1.28 0 -2.559 -0.488 -3.536 -1.465 L 18.964 47.383 c -1.953 -1.953 -1.953 -5.119 0 -7.071 c 1.953 -1.952 5.118 -1.952 7.071 0 l 12.233 12.232 l 25.696 -25.695 c 1.951 -1.952 5.119 -1.952 7.07 0 c 1.953 1.953 1.953 5.119 0 7.071 L 41.804 63.15 C 40.828 64.127 39.548 64.615 38.269 64.615 z" style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(255,255,255); fill-rule: nonzero; opacity: 1;" transform=" matrix(1 0 0 1 0 0) " stroke-linecap="round"/>
						</g>
					</svg> Everything in Pro</li>
				<li class="flex justify-start gap-2">
					<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="18" height="18" viewBox="0 0 256 256" xml:space="preserve">
						<g style="stroke: none; stroke-width: 0; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: none; fill-rule: nonzero; opacity: 1;" transform="translate(1.4065934065934016 1.4065934065934016) scale(2.81 2.81)">
							<path d="M 85 90 H 5 c -2.761 0 -5 -2.238 -5 -5 V 5 c 0 -2.761 2.239 -5 5 -5 h 80 c 2.762 0 5 2.239 5 5 v 80 C 90 87.762 87.762 90 85 90 z" style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(39,196,72); fill-rule: nonzero; opacity: 1;" transform=" matrix(1 0 0 1 0 0) " stroke-linecap="round"/>
							<path d="M 38.269 64.615 c -1.28 0 -2.559 -0.488 -3.536 -1.465 L 18.964 47.383 c -1.953 -1.953 -1.953 -5.119 0 -7.071 c 1.953 -1.952 5.118 -1.952 7.071 0 l 12.233 12.232 l 25.696 -25.695 c 1.951 -1.952 5.119 -1.952 7.07 0 c 1.953 1.953 1.953 5.119 0 7.071 L 41.804 63.15 C 40.828 64.127 39.548 64.615 38.269 64.615 z" style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(255,255,255); fill-rule: nonzero; opacity: 1;" transform=" matrix(1 0 0 1 0 0) " stroke-linecap="round"/>
						</g>
					</svg> Dedicated support</li>
				<li class="flex justify-start gap-2">
					<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="18" height="18" viewBox="0 0 256 256" xml:space="preserve">
						<g style="stroke: none; stroke-width: 0; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: none; fill-rule: nonzero; opacity: 1;" transform="translate(1.4065934065934016 1.4065934065934016) scale(2.81 2.81)">
							<path d="M 85 90 H 5 c -2.761 0 -5 -2.238 -5 -5 V 5 c 0 -2.761 2.239 -5 5 -5 h 80 c 2.762 0 5 2.239 5 5 v 80 C 90 87.762 87.762 90 85 90 z" style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(39,196,72); fill-rule: nonzero; opacity: 1;" transform=" matrix(1 0 0 1 0 0) " stroke-linecap="round"/>
							<path d="M 38.269 64.615 c -1.28 0 -2.559 -0.488 -3.536 -1.465 L 18.964 47.383 c -1.953 -1.953 -1.953 -5.119 0 -7.071 c 1.953 -1.952 5.118 -1.952 7.071 0 l 12.233 12.232 l 25.696 -25.695 c 1.951 -1.952 5.119 -1.952 7.07 0 c 1.953 1.953 1.953 5.119 0 7.071 L 41.804 63.15 C 40.828 64.127 39.548 64.615 38.269 64.615 z" style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(255,255,255); fill-rule: nonzero; opacity: 1;" transform=" matrix(1 0 0 1 0 0) " stroke-linecap="round"/>
						</g>
					</svg> Custom integrations</li>
				<li class="flex justify-start gap-2">
					<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="18" height="18" viewBox="0 0 256 256" xml:space="preserve">
						<g style="stroke: none; stroke-width: 0; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: none; fill-rule: nonzero; opacity: 1;" transform="translate(1.4065934065934016 1.4065934065934016) scale(2.81 2.81)">
							<path d="M 85 90 H 5 c -2.761 0 -5 -2.238 -5 -5 V 5 c 0 -2.761 2.239 -5 5 -5 h 80 c 2.762 0 5 2.239 5 5 v 80 C 90 87.762 87.762 90 85 90 z" style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(39,196,72); fill-rule: nonzero; opacity: 1;" transform=" matrix(1 0 0 1 0 0) " stroke-linecap="round"/>
							<path d="M 38.269 64.615 c -1.28 0 -2.559 -0.488 -3.536 -1.465 L 18.964 47.383 c -1.953 -1.953 -1.953 -5.119 0 -7.071 c 1.953 -1.952 5.118 -1.952 7.071 0 l 12.233 12.232 l 25.696 -25.695 c 1.951 -1.952 5.119 -1.952 7.07 0 c 1.953 1.953 1.953 5.119 0 7.071 L 41.804 63.15 C 40.828 64.127 39.548 64.615 38.269 64.615 z" style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(255,255,255); fill-rule: nonzero; opacity: 1;" transform=" matrix(1 0 0 1 0 0) " stroke-linecap="round"/>
						</g>
					</svg> SLA & onboarding</li>
			</ul>
			<button class="text-xl bg-gradient-to-r from-primary to-secondary w-full rounded-xl px-4 py-2 mt-auto" on:click={() => handleUpgrade('custom')}>Contact Sales</button>
		</div>
	</div>
</div>