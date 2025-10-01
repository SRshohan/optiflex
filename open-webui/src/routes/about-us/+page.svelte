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
						{$i18n.t('About Us')}
					</div>
				</div>
			</div>    
        <div class="flex flex-col gap-2 text-white justify-center items-center">
			<p class="max-w-[60%] mx-auto text-justify">Optiflex AI was founded with a simple yet ambitious vision: to make advanced AI technology accessible, flexible, and beneficial for everyone. We are a passionate startup that believes in the transformative power of AI to augment human creativity and productivity. Our journey began with the idea of providing a unified platform where users can tap into multiple state-of-the-art AI models (like OpenAI’s GPT series, Google’s Gemini, Perplexity, and more) without the usual complexity. By abstracting away the hard parts and integrating these tools seamlessly, we empower developers, businesses, and curious individuals to leverage cutting-edge AI capabilities in their own projects and workflows.
			At Optiflex AI, we foster a culture of innovation and customer-centric development. We move fast and iterate often, driven by the excitement of solving real problems with intelligent solutions. Every member of our team – from engineers and researchers to support staff – is motivated by the impact our technology can have on users’ lives. We’ve seen our platform help people automate tedious tasks, generate creative content, gain insights from data, and much more. These success stories inspire us every day. We also embrace a “learning” mindset: each interaction is a chance to improve, and each piece of feedback fuels our next breakthrough. As a startup, we take pride in being agile and attentive – unencumbered by bureaucracy, we can quickly adapt to user needs and the rapidly evolving AI landscape. Our mission is not only to provide powerful AI tools, but to do so in a way that is optimally flexible (true to our name) – giving users control, choices, and confidence in how AI works for them.
			Looking ahead, we are excited about the future we are building. We see a world where AI is an everyday collaborator for people in all fields, and we want to lead in making that future friendly and accessible. Optiflex AI stands for optimizing the future and flexing the possibilities of artificial intelligence. We’re incredibly grateful to our growing community of users and supporters. Together, we’re exploring new frontiers of technology. We promise to remain transparent, responsible, and bold in our pursuit of innovation. Thank you for believing in our vision – we’re here to innovate with you and for you.
			(Feel free to reach out to us at contact@optiflex.ai – we love hearing from our users and partners!)
			</p>
            <a class="text-primary" href="/auth">Go to Login</a>
            <a class="text-primary" href="/aignup">Go to Register</a>
        </div>
    </div>

</div>
