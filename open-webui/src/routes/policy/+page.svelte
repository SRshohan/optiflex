<script>
	    import { WEBUI_NAME } from "$lib/stores";
	    import { getContext } from "svelte";

    	const i18n = getContext('i18n');
</script>

<div class="w-full h-screen max-h-[100dvh] text-white relative">
	<div class="w-full h-full absolute top-0 left-0 bg-white dark:bg-black"></div>

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
        <div class="flex flex-col gap-2 text-white justify-center items-center">
            <a href="/auth">Go to Login</a>
            <a href="/aignup">Go to Register</a>
        </div>
    </div>

</div>
