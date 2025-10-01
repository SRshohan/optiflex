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
						{$i18n.t('Privacy Policy of {{WEBUI_NAME}}', { WEBUI_NAME: $WEBUI_NAME })}
					</div>
				</div>
			</div>    
        <div class="flex flex-col gap-2 text-white justify-center items-center h-[90vh]">
			<!-- Main content -->
			<main class="flex flex-col gap-4 space-y-10 rounded-xl p-6 overflow-y-scroll h-full">
				
				<!-- Intro -->
				<section>
				<h2 class="text-lg font-semibold mb-2">Summary</h2>
				<p class="text-gray-600">Your privacy is important to us. This Policy describes the types of information we collect, how we use and share it, how long we retain it, and your rights regarding your personal data.</p>
				</section>

				<!-- Data We Collect -->
				<section id="data-collected">
				<h2 class="text-lg font-semibold mb-3">Data We Collect</h2>
				<dl class="space-y-4">
					<div>
					<dt class="font-medium">Account Information</dt>
					<dd class="text-gray-600">Name, email, hashed password. Payments are handled by Stripe; we store only billing references.</dd>
					</div>
					<div>
					<dt class="font-medium">Usage Data</dt>
					<dd class="text-gray-600">Logs of interactions (API calls, chats, timestamps, frequency), plus error and system logs.</dd>
					</div>
					<div>
					<dt class="font-medium">Uploaded Content</dt>
					<dd class="text-gray-600">Files, images, and documents uploaded for AI processing, treated as confidential.</dd>
					</div>
					<div>
					<dt class="font-medium">Device & Technical Data</dt>
					<dd class="text-gray-600">IP address, approximate location, browser, OS, device identifiers, cookies, diagnostic logs.</dd>
					</div>
				</dl>
				</section>

				<!-- How We Use -->
				<section id="how-we-use">
				<h2 class="text-lg font-semibold mb-3">How We Use the Data</h2>
				<ul class="list-disc list-inside space-y-1 text-gray-600">
					<li><span class="font-medium">Provide the Service:</span> Use prompts and uploads to generate responses; authenticate accounts.</li>
					<li><span class="font-medium">Improve & Personalize:</span> Analyze usage data (anonymized/aggregated) to enhance features.</li>
					<li><span class="font-medium">Security & Fraud Prevention:</span> Detect suspicious logins, unusual activity, or abuse.</li>
					<li><span class="font-medium">Customer Support:</span> Troubleshoot using account and usage data; communicate service updates.</li>
					<li><span class="font-medium">Analytics & Development:</span> Conduct aggregated analytics and A/B testing.</li>
					<li><span class="font-medium">Billing & Account Management:</span> Calculate usage, manage subscriptions, ensure compliance.</li>
				</ul>
				</section>

				<!-- Third Parties -->
				<section id="third-parties">
				<h2 class="text-lg font-semibold mb-3">Third-Party Services</h2>
				<p class="text-gray-600 mb-4">We work with trusted partners to provide core services. These providers process data under strict agreements:</p>
				<details class="mb-2">
					<summary class="cursor-pointer font-medium">Stripe (Payments)</summary>
					<p class="ml-4 text-gray-600">Processes payments securely. We do not store your full payment information.</p>
				</details>
				<details class="mb-2">
					<summary class="cursor-pointer font-medium">Supabase (Database & Auth)</summary>
					<p class="ml-4 text-gray-600">Hosts account data and authentication. Operates under our instructions.</p>
				</details>
				<details class="mb-2">
					<summary class="cursor-pointer font-medium">AI Model APIs (OpenAI, Google Gemini, etc.)</summary>
					<p class="ml-4 text-gray-600">Used to generate AI responses. Only necessary data is shared with these services.</p>
				</details>
				<details>
					<summary class="cursor-pointer font-medium">Analytics Tools</summary>
					<p class="ml-4 text-gray-600">Tools like Google Analytics (if enabled) help us understand usage; you may opt out.</p>
				</details>
				</section>

				<!-- Retention -->
				<section id="retention">
				<h2 class="text-lg font-semibold mb-3">Data Retention</h2>
				<ul class="list-disc list-inside space-y-1 text-gray-600">
					<li><span class="font-medium">Account Info:</span> Retained while account is active; deleted/anonymized after deletion, except required legal records.</li>
					<li><span class="font-medium">Usage Data:</span> Stored for functionality and improvement; may be anonymized for analytics.</li>
					<li><span class="font-medium">Uploaded Content:</span> Kept only as needed for AI processing; deletable by user.</li>
					<li><span class="font-medium">Legal Retention:</span> Certain records (e.g., transactions) kept as required by law.</li>
				</ul>
				</section>

				<!-- User Rights -->
				<section id="user-rights">
				<h2 class="text-lg font-semibold mb-3">User Rights</h2>
				<ul class="list-disc list-inside space-y-1 text-gray-600">
					<li><span class="font-medium">Access:</span> Request a copy of your personal data.</li>
					<li><span class="font-medium">Deletion:</span> Request account and data deletion (subject to legal obligations).</li>
					<li><span class="font-medium">Opt-Out:</span> Disable analytics cookies, opt out of communications.</li>
					<li><span class="font-medium">Correction & Portability:</span> Correct errors, request common-format exports.</li>
				</ul>
				<p class="text-sm text-gray-500 mt-2">To exercise rights, email <a href="mailto:contact@optiflex.ai" class="text-blue-600 hover:underline">contact@optiflex.ai</a>. We may verify your identity before fulfilling requests.</p>
				</section>

				<!-- Security -->
				<section id="security">
				<h2 class="text-lg font-semibold mb-3">Security Measures</h2>
				<ul class="list-disc list-inside space-y-1 text-gray-600">
					<li><span class="font-medium">Encryption:</span> TLS for data in transit, encryption at rest, hashed passwords.</li>
					<li><span class="font-medium">Access Controls:</span> Role-based access, audits, minimum necessary access.</li>
					<li><span class="font-medium">Organizational Practices:</span> Staff training, security incident procedures.</li>
					<li><span class="font-medium">Third-Party Security:</span> Vendors with high security standards only.</li>
					<li><span class="font-medium">Monitoring:</span> Regular audits, patching, and penetration testing.</li>
				</ul>
				</section>

				<!-- Children -->
				<section id="childrens-privacy">
				<h2 class="text-lg font-semibold mb-3">Children’s Privacy</h2>
				<p class="text-gray-600">Optiflex AI is not intended for children under 13 (or under 16 where applicable by law). We do not knowingly collect data from minors, and any discovered data will be deleted promptly.</p>
				</section>

				<!-- Updates -->
				<section id="policy-updates">
				<h2 class="text-lg font-semibold mb-3">Policy Updates</h2>
				<p class="text-gray-600">We may update this policy from time to time. Material updates will be communicated via email or prominent notices. Continued use after updates means acceptance of the new policy.</p>
				</section>

				<!-- Contact -->
				<section id="contact">
				<h2 class="text-lg font-semibold mb-3">Contact</h2>
				<p class="text-gray-600">If you have questions or wish to exercise your rights, contact us at:</p>
				<address class="not-italic text-gray-400">
					Email: <a href="mailto:contact@optiflex.ai" class="text-blue-600 hover:underline">contact@optiflex.ai</a><br>
					(Add postal address if applicable)
				</address>
				</section>
				<div class=" flex justify-center items-center gap-10 mb-0">
					<a class="text-primary" href="/auth">Go to Login</a>
            		<a class="text-primary" href="/aignup">Go to Register</a>
				</div>
				<!-- Footer -->
				<footer class="border-t pt-4 text-sm text-gray-500">
				<p>This Privacy Policy is for informational purposes only and does not constitute legal advice. For compliance questions, consult a qualified attorney.</p>
				</footer>
			</main>
        </div>
    </div>

</div>
