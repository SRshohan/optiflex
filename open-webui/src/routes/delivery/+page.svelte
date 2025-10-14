<script>
	    import { WEBUI_NAME } from "$lib/stores";
	    import { getContext } from "svelte";

    	const i18n = getContext('i18n');
</script>

<div class="w-full h-screen max-h-[100dvh] text-white relative">
	<div class="w-full h-full absolute top-0 left-0 bg-white dark:bg-gray-950/40"></div>

	<div class="w-full absolute top-0 left-0 right-0 h-8 drag-region" />
		<div class="fixed m-10 z-50">
			<div class="flex space-x-2">
				<div class=" self-center">
					<img
						id="logo"
						crossorigin="anonymous"
						src="/static/favicon.png"
						class=" w-6 rounded-full"
						alt=""
					/>
				</div>
			</div>
		</div>
    <div
			class="fixed bg-transparent min-h-screen w-full flex flex-col justify-center font-primary z-50 text-black dark:text-white"
		>
			<div class="mx-auto pb-10 w-full">
				<div
					class="flex items-center justify-center gap-3 text-xl sm:text-2xl text-center font-semibold dark:text-gray-200"
				>
					<div>
						{$i18n.t('Refund Policy of {{WEBUI_NAME}}', { WEBUI_NAME: $WEBUI_NAME })}
					</div>
				</div>
			</div>    
        <div class="flex flex-col gap-2 text-white justify-center items-center h-[90vh] max-w-[80%] mx-auto">
			<!-- Main content -->
			<main class="text-white flex flex-col gap-4 space-y-10 rounded-xl p-6 overflow-y-scroll h-full">
				<h1 class="text-3xl font-bold mb-6">Service Delivery Policy — Optiflex AI</h1>
				<p class="text-gray-400 mb-10">
					Optiflex AI is a cloud-based Software-as-a-Service (SaaS) product, meaning all delivery is digital. 
					Upon purchase, you receive instant access to our platform with no physical shipping involved. 
					Below are the details of how our service is provisioned and accessed.
				</p>

				<!-- Service Access -->
				<section class="mb-12">
					<h2 class="text-2xl font-semibold mb-4">Service Access</h2>
					<p class="text-gray-400">
					Upon successful sign-up and payment, your account is provisioned with the purchased subscription 
					or credits instantly, and you can begin using our AI services right away.
					</p>
				</section>

				<!-- Instant Activation -->
				<section class="mb-12">
					<h2 class="text-2xl font-semibold mb-4">Instant Activation</h2>
					<p class="text-gray-400">
					If you are a new user, once your payment is confirmed, an account is created or upgraded immediately. 
					Credits or usage tokens are added to your balance right away. For example, if you purchase a pack of 
					100,000 tokens, your account will reflect that balance as soon as the transaction completes.
					</p>
				</section>

				<!-- Account Login -->
				<section class="mb-12">
					<h2 class="text-2xl font-semibold mb-4">Account Login</h2>
					<p class="text-gray-400">
					Access is provided through your Optiflex AI account on our website or app. All features of your plan 
					or any add-ons are enabled upon login. New users will set a password during sign-up, and support is 
					available if login issues occur.
					</p>
				</section>

				<!-- 24/7 Availability -->
				<section class="mb-12">
					<h2 class="text-2xl font-semibold mb-4">24/7 Availability</h2>
					<p class="text-gray-400">
					Optiflex AI is available 24/7 worldwide. As long as you have an internet connection, you can log in 
					and use our AI services anytime. Planned maintenance is communicated in advance, and we strive for 
					near 100% uptime.
					</p>
				</section>

				<!-- No Physical Delivery -->
				<section class="mb-12">
					<h2 class="text-2xl font-semibold mb-4">No Physical Delivery</h2>
					<p class="text-gray-400">
					All outputs and results are delivered digitally through the online dashboard or API. 
					No shipping or downloads are required unless you choose an optional local client. 
					Interaction with our AI happens in real-time within the platform.
					</p>
				</section>

				<!-- Confirmation of Delivery -->
				<section class="mb-12">
					<h2 class="text-2xl font-semibold mb-4">Confirmation of Service Delivery</h2>
					<p class="text-gray-400">
					After purchase, you will receive an on-screen confirmation and an email receipt. 
					This confirms your account has been updated with the purchased credits or subscription. 
					The email also includes support contact information.
					</p>
				</section>

				<!-- Support and Troubleshooting -->
				<section class="mb-12">
					<h2 class="text-2xl font-semibold mb-4">Support and Troubleshooting</h2>
					<p class="text-gray-400">
					If credits do not appear or a purchased feature is inaccessible, 
					contact us at <a href="mailto:support@optiflex.ai" class="text-blue-600 underline">support@optiflex.ai</a>. 
					Our team will promptly investigate and resolve the issue. Such cases are rare but are treated with priority.
					</p>
				</section>

				<!-- Summary -->
				<section>
					<h2 class="text-2xl font-semibold mb-4">Summary</h2>
					<p class="text-gray-400">
					Optiflex AI’s delivery model is simple: instant online access. 
					From the moment you complete your purchase, you can log in and use our AI services without delay. 
					With continuous availability, you can focus on building and creating with AI—hassle-free.
					</p>
				</section>
				<div class=" flex justify-center items-center gap-10 mb-0">
					<a class="text-primary" href="/auth">Go to Login</a>
            		<a class="text-primary" href="/aignup">Go to Register</a>
				</div>
			</main>
        </div>
    </div>

</div>
