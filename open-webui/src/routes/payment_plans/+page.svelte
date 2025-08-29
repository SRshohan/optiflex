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
  background: var(--card-bg, #23272f);
  border-radius: 2rem;
  border: 2px solid var(--card-border, #2a2f38);
  box-shadow: 0 4px 32px rgba(16, 163, 127, 0.13);
  padding: 3rem 2.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: border 0.2s, box-shadow 0.2s;
}

/* Highlighted (“featured”) card */
.pricing-card.featured {
  border: 3px solid #10a37f;
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
		<div class="pricing-card">
			<div class="pricing-plan-title">Starter</div>
			<div class="pricing-price">Free</div>
			<div class="pricing-plan-desc">Get started with basic features and limited usage.</div>
			<ul class="pricing-features">
				<li>✔️ Basic chat access</li>
				<li>✔️ Community support</li>
				<li class="negative">❌ No API access</li>
				<li class="negative">❌ No priority support</li>
			</ul>
			<button class="pricing-btn" on:click={() => handleUpgrade('starter')}>Get Started</button>
		</div>

		<!-- Pro Plan (Featured) -->
		<div class="pricing-card featured">
			<div class="pricing-plan-title">Pro</div>
			<div class="pricing-price">$20<span style="font-size:1.1rem;font-weight:500;">/mo</span></div>
			<div class="pricing-plan-desc">Unlock advanced features, higher limits, and priority support.</div>
			<ul class="pricing-features">
				<li>✔️ Everything in Starter</li>
				<li>✔️ Priority access to new features</li>
				<li>✔️ API access</li>
				<li>✔️ Priority support</li>
			</ul>
			<button class="pricing-btn" on:click={() => handleUpgrade('pro')}>Upgrade to Pro</button>
		</div>

		<!-- Custom/Enterprise Plan -->
		<div class="pricing-card">
			<div class="pricing-plan-title">Custom</div>
			<div class="pricing-price">Contact Us</div>
			<div class="pricing-plan-desc">For teams and enterprises with custom needs and high volume.</div>
			<ul class="pricing-features">
				<li>✔️ Everything in Pro</li>
				<li>✔️ Dedicated support</li>
				<li>✔️ Custom integrations</li>
				<li>✔️ SLA & onboarding</li>
			</ul>
			<button class="pricing-btn" on:click={() => handleUpgrade('custom')}>Contact Sales</button>
		</div>
	</div>
</div>