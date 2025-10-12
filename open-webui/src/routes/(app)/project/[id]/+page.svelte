<script lang="ts">
	import { page } from '$app/stores';

	import Chat from '$lib/components/chat/Chat.svelte';
	import { temporaryChatEnabled } from '$lib/stores';
	import { onMount } from 'svelte';

onMount(async()=>{
	await temporaryChatEnabled.set(false);
})
</script>

<Chat projectId={$page.params.id} />
