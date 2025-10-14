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
			<main class="flex flex-col gap-4 space-y-10 rounded-xl p-6 overflow-y-scroll h-full">
				<h1 class="text-3xl font-bold mb-6">Refund Policy — Optiflex AI</h1>
				<p class="text-gray-400 mb-8">Effective Date: September 30, 2025</p>
				<p class="text-gray-400 mb-10">
					Optiflex AI strives to provide a fair and transparent refund policy that balances user satisfaction 
					with the operational costs of delivering AI services. This policy explains the situations where 
					refunds are granted and where they are not.
				</p>

				<!-- Eligible Refund Cases -->
				<section class="mb-12">
					<h2 class="text-2xl font-semibold mb-4">Eligible Refund Cases</h2>
					<ul class="list-disc list-inside space-y-4 text-gray-400">
					<li>
						<span class="font-medium">Technical Failures (System Issues):</span>
						If our platform experiences downtime, outages, or bugs that prevent you from using purchased credits, 
						we will issue a refund or service credit.
					</li>
					<li>
						<span class="font-medium">Double Charges / Billing Errors:</span>
						If you were charged more than once or an incorrect amount, we will promptly refund the duplicate or erroneous charge.
					</li>
					<li>
						<span class="font-medium">Unused Balance (Case-by-Case):</span>
						If you purchased credits but never used them, we may offer a full or partial refund as a courtesy. 
						Once credits are consumed, refunds are generally not available.
					</li>
					<li>
						<span class="font-medium">Failure to Deliver Promised Service:</span>
						If you purchased access to a specific feature or add-on that was unavailable or non-functional, we will honor a refund.
					</li>
					</ul>
				</section>

				<!-- Non-Eligible Refund Cases -->
				<section class="mb-12">
					<h2 class="text-2xl font-semibold mb-4">Non-Eligible Refund Cases</h2>
					<ul class="list-disc list-inside space-y-4 text-gray-400">
					<li>
						<span class="font-medium">Change of Mind:</span>
						Refunds are not available if you decide you no longer want the service or purchased credits.
					</li>
					<li>
						<span class="font-medium">Already Used Credits:</span>
						Once credits have been consumed, they cannot be refunded as costs are already incurred.
					</li>
					<li>
						<span class="font-medium">External Issues / Subjective Dissatisfaction:</span>
						Refunds are not provided for dissatisfaction with AI responses. 
						We welcome feedback but cannot refund based on subjective expectations.
					</li>
					</ul>
				</section>

				<!-- Refund Process -->
				<section class="mb-12">
					<h2 class="text-2xl font-semibold mb-4">Refund Process</h2>
					<ol class="list-decimal list-inside space-y-4 text-gray-400">
					<li>Email <a href="mailto:support@optiflex.ai" class="text-blue-600 underline">support@optiflex.ai</a> with:
						<ul class="list-disc list-inside ml-6 mt-2 space-y-1">
						<li>Your account email</li>
						<li>Transaction details (date and amount)</li>
						<li>A brief description of the issue</li>
						</ul>
					</li>
					<li>Our team will review your request and respond with next steps.</li>
					<li>Approved refunds will be processed to your original payment method or as service credits.</li>
					</ol>
				</section>

				<!-- Commitment -->
				<section>
					<h2 class="text-2xl font-semibold mb-4">Commitment</h2>
					<p class="text-gray-400">
					We stand behind our service and are committed to treating all users fairly. 
					This policy ensures clarity while protecting both our users and the sustainability of our AI services.
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
