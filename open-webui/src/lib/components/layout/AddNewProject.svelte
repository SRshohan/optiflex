<script>
	import { addedProjects } from "$lib/stores";
	import Modal from "../common/Modal.svelte";

    let {show = $bindable(false), onClose=()=>{}} = $props();
    let projectName = $state("")

    function handleCreateProject(){
        if(projectName.length > 0){
            let oldState = $addedProjects
            oldState.push({id:$addedProjects.length + 1,name:projectName})
            $addedProjects = oldState;
            projectName = ""
            onClose()
        }
    }
</script>

<Modal size="md" bind:show>
    <div class="text-white p-6 flex flex-col justify-center items-center gap-5">
        <div class="w-full flex justify-between items-center">
            <h1 class="text-lg font-bold">Project Name</h1>
            <button onclick={onClose}>X</button>
        </div>
        <input bind:value={projectName} onchange={(e)=> projectName = e.target.value} placeholder="eg: programming" class="w-full bg-gray-700/40 h-12 rounded-full px-4 py-1" />
        <p class="rounded-lg text-sm p-2 bg-gray-600/40">Projects keep chats, files, and custom instructions in one place. Use them for ongoing work, or just to keep things tidy.</p>
        <div class="w-full flex justify-end items-center p-2 rounded-full">
            <button onclick={handleCreateProject} class="bg-gray-700/40 px-4 py-2 rounded-full font-semibold">Create Project</button>
        </div>
    </div>
</Modal>