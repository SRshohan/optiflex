<script >
	import Button from "$lib/components/ui/Button.svelte";
	import Input from "$lib/components/ui/Input.svelte";
	import { getContext } from "svelte";
	import {  WEBUI_BASE_URL } from '$lib/constants';
	import { enhance } from "$app/forms";

	let { form } = $props();
    let name = $state('');
	let email = $state('');
	let password = $state('');
	let confirmPassword = $state('');
	let passwordMatched = $state("")
	const i18n = getContext('i18n');

	$effect(()=>{
        if(confirmPassword.length > 0 && passwordMatched.length > 0){
            passwordMatched=""
        }
    })

	function fieldValidation(){
		if(password !== confirmPassword){
			passwordMatched = "Confirm Password and Password should Match"
		}
	}
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
						src="{WEBUI_BASE_URL}/static/favicon.png"
						class=" w-6 rounded-full"
						alt=""
					/>
				</div>
			</div>
		</div>

		<div
			class="fixed bg-transparent min-h-screen w-full flex justify-center font-primary z-50 text-black dark:text-white"
		>
			<div class="w-full sm:max-w-md px-10 min-h-screen flex flex-col text-center"> 
				<div class=" my-auto pb-10 w-full dark:text-gray-100">
					<form
						method="POST"
						use:enhance
						class="flex flex-col justify-center space-y-2 gap-y-1"
					>
						<div class="mb-2">
							<label for="name" class="text-sm font-medium text-left mb-1 block"
								>{$i18n.t('Name')}</label
							>
							<Input className="bg-white text-black" bind:value={name} type="name" name="name" id="name" placeHolder="Enter Your Name" />
						</div>

						<div class="mb-2">
							<label for="email" class="text-sm font-medium text-left mb-1 block"
								>{$i18n.t('Email')}</label
							>
							<Input className="bg-white text-black" bind:value={email} type="email" name="email" id="email" placeHolder="Enter Your Email" />
						</div>

						<div class="mb-2">
							<label for="password" class="text-sm font-medium text-left mb-1 block"
								>{$i18n.t('Password')}</label
							>
							<Input className="bg-white text-black" isAuth={true} bind:value={password} type="password" name="password" id="password" placeHolder="Enter Your Password" />
						</div>

						<div class="mb-2 flex flex-col gap-0.5 items-start">
							<label for="confirmPassword" class="text-sm font-medium text-left mb-1 block"
								>{$i18n.t('Confirm Password')}</label
							>
							<input
								bind:value={confirmPassword}
								type="password"
								id="confirmPassword"
								class={`p-1 w-full text-sm rounded text-black bg-white ${passwordMatched.length > 0 ? 'border-2 border-red-500':""}`}
								placeholder={$i18n.t('Confirm Password')}
								name="confirm-password"
								onblur={fieldValidation}
								required
							/>
							{#if passwordMatched.length > 0}
								<p class="text-red-500 text-sm">{passwordMatched}</p>
							{/if}
						</div>

						{#if form?.error}
							<p class="text-red-500 text-sm">{form?.error}</p>
						{/if}
						<div class="flex flex-col space-y-2">
							<Button disabled={form?.pending} type="submit">
								{$i18n.t('Sign up')}
							</Button>
							<button
								class="flex justify-center items-center bg-gray-700/5 hover:bg-gray-700/10 dark:bg-gray-100/5 dark:hover:bg-gray-100/10 dark:text-gray-300 dark:hover:text-white transition w-full rounded-full font-medium text-sm py-2.5"
								onclick={()=>{}}
							>
								<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" class="size-6 mr-3">
									<path
										fill="#EA4335"
										d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"
									/><path
										fill="#4285F4"
										d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"
									/><path
										fill="#FBBC05"
										d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"
									/><path
										fill="#34A853"
										d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"
									/><path fill="none" d="M0 0h48v48H0z" />
								</svg>
								<span>{$i18n.t('Sign-Up with {{provider}}', { provider: 'Google' })}</span>
							</button>

						</div>
					</form>
				</div>
   			</div>
		</div>
</div>