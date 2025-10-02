<script>
	import { goto } from "$app/navigation";
	import { getChatsOfProject } from "$lib/apis/chats";
	import { onMount } from "svelte";

    let { projectId } = $props()
    let allChats = $state([]);
    onMount(async()=>{
		allChats = await getChatsOfProject(localStorage.token,projectId)
	})
</script>

 {#if allChats.length > 0 }
    {#each allChats as chat}
        <p onclick={()=> goto(`/c/${chat.id}`)} class="cursor-pointer text-xs">{chat.title}</p>
    {/each}
{/if}