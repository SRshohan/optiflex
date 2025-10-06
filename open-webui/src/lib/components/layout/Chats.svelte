<script>
	import { goto } from "$app/navigation";
	import { getChatById, getChatsOfProject } from "$lib/apis/chats";
	import { allChatsInProjects, deleteChatProjectId, deleteProjectId, showDeleteChatOfProjectModal } from "$lib/stores";
	import { onMount } from "svelte";

    let { projectId } = $props()
    onMount(async()=>{
		$allChatsInProjects = await getChatsOfProject(localStorage.token,projectId)
	})

    async function handleDelete(id){
        deleteProjectId.set(projectId);
        deleteChatProjectId.set(id);
        showDeleteChatOfProjectModal.set(true);
    }

    
</script>

 {#if $allChatsInProjects.length > 0 }
    {#each $allChatsInProjects as chat}
        <div class="flex justify-between items-center">
            <p onclick={()=> goto(`/c/${chat.id}`)} class="cursor-pointer text-xs">{chat.title}</p>
            <p onclick={()=>handleDelete(chat.id)} class="text-xs text-red-600 font-bold cursor-pointer">X</p>
        </div>
    {/each}
{/if}