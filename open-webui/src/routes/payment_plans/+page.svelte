<script lang="ts">
	import { goto } from '$app/navigation';

    async function getUserEmail() {
        const token = localStorage.getItem('token');
        if (!token) {
            return null;
        }
        const res = await fetch('http://127.0.0.1:8080/api/v1/auths', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });
        const data = await res.json();
        console.log(data);
        return data.email;
    }

	async function handleUpgrade(plan: string) {
		if (plan === 'pro') {
			const token = localStorage.getItem('token'); // Get the user's OpenWebUI token
			if (!token) {
				alert('You must be logged in to upgrade.');
				return;
			}
			const userEmail = await getUserEmail();
            console.log(userEmail);
			const res = await fetch(`http://127.0.0.1:8080/api/v1/payment/checkout/stripe-webhook`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': `Bearer ${token}`
				},
                body: JSON.stringify({
                    user_email: userEmail
                })
			});
			if (res.ok) {
				const data = await res.json();
                console.log(data);
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
			goto('/'); // Or whatever you want for free plan
		} else if (plan === 'custom') {
			window.location.href = 'mailto:sales@yourdomain.com'; // Or open a contact form
		}
	}
</script>

<style>
:global(html, body) {
	margin: 0;
	padding: 0;
	background: #181c23;
	min-height: 100vh;
	box-sizing: border-box;
}
.pricing-root {
	min-height: 100vh;
	background: #181c23;
}
.pricing-header {
	text-align: center;
	margin-top: 3rem;
	margin-bottom: 2.5rem;
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
.pricing-container {
	max-width: 1200px;
	margin: 0 auto;
	padding: 2rem 1rem 4rem 1rem;
	display: flex;
	flex-wrap: wrap;
	justify-content: center;
	gap: 2.5rem;
}
.pricing-card {
	background: var(--card-bg, #23272f);
	border-radius: 2rem;
	border: 2px solid var(--card-border, #2a2f38);
	box-shadow: 0 4px 32px rgba(16,163,127,0.13);
	padding: 3rem 2.5rem;
	flex: 1 1 340px;
	max-width: 400px;
	min-width: 320px;
	display: flex;
	flex-direction: column;
	align-items: center;
	transition: border 0.2s, box-shadow 0.2s;
}
.pricing-card.featured {
	border: 3px solid #10a37f;
	box-shadow: 0 8px 40px rgba(16,163,127,0.18);
}
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
	box-shadow: 0 2px 8px rgba(16,163,127,0.10);
	margin-top: auto;
}
.pricing-btn:hover {
	background: #0e8c6b;
}
@media (max-width: 1200px) {
	.pricing-container {
		flex-direction: column;
		align-items: center;
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