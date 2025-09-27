<script>
	import { deleteProject } from "$lib/apis/chats";
	import { toast } from "svelte-sonner";
	import Modal from "../common/Modal.svelte";
	import { addedProjects, deleteProjectId } from "$lib/stores";

    let {show = $bindable(false), onClose=()=>{}} = $props();

    async function handleDeleteFunction(){
        const res = await deleteProject(localStorage.token,$deleteProjectId);
        console.log(res,"res delete");
        
        if(res.message === "Project deleted successfully"){
            toast.success(`${res.message}`);
            let oldState = $addedProjects;
            oldState = oldState.filter(prev=>prev.id !== $deleteProjectId)
            $addedProjects = oldState;
            onClose();
        }
    }
</script>

<Modal size="md" bind:show>
    <div class="text-white p-6 flex flex-col justify-center items-center gap-5">
        <div class="w-full flex justify-between items-center">
            <h1 class="text-lg font-bold">Delete Project</h1>
            <button onclick={onClose}>X</button>
        </div>
        <p class="rounded-lg text-sm p-2 bg-gray-600/40">Do you want to delete this Project?</p>
        <div class="w-full flex justify-end items-center p-2 rounded-full gap-6">
            <button onclick={onClose} class="bg-gray-700/40 text-red-600 px-4 py-2 rounded-full font-semibold">No</button>
            <button onclick={handleDeleteFunction} class="bg-gray-700/40 text-green-600 px-4 py-2 rounded-full font-semibold">Delete Project</button>
        </div>
    </div>
</Modal>