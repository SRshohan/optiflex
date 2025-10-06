<script>
	import { createNewProject, editProject } from "$lib/apis/chats";
	import { addedProjects, editProjectId } from "$lib/stores";
	import { toast } from "svelte-sonner";
	import Modal from "../common/Modal.svelte";

    let {show = $bindable(false), onClose=()=>{}} = $props();
    let projectName = $state("");
    let projectDescription = $state("");
    let error = $state("");

    $effect(()=>{
        if($editProjectId.length > 0){
            projectName = $addedProjects.filter(project=>project.id === $editProjectId)[0]?.name;
            projectDescription = $addedProjects.filter(project=>project.id === $editProjectId)[0]?.description;
        }
    })

    async function handleProject(){
        if(projectName === "" || projectDescription === ""){
            error = "Field/s cannot be Empty"
            return;
        }
        let oldState = $addedProjects;
        let res;
        if($editProjectId.length > 0){
            res = await editProject(localStorage.token,{name:projectName,description:projectDescription,color:"blue"},$editProjectId);
            oldState = oldState.map(prev=>{
                if(prev.id === $editProjectId){
                    prev.name=projectName;
                    prev.description=projectDescription;
                    prev.color="blue";
                }
                return prev
            })
            toast.success("Project Edit Successful");
        }else{
            if(projectName.length > 0){
                res = await createNewProject(localStorage.token,{name:projectName,description:projectDescription,color:"blue"});
                oldState.push(res);
                toast.success("Project Creation Successful");
            }
        }
        
        $addedProjects = oldState;
        projectName = "";
        projectDescription = "";
        $editProjectId  = ""
        onClose()
    }
</script>

<Modal size="md" bind:show>
    <div class="text-white p-6 flex flex-col justify-center items-center gap-5">
        <div class="w-full flex justify-between items-center">
            <h1 class="text-lg font-bold">Project Name</h1>
            <button onclick={onClose}>X</button>
        </div>
        <input bind:value={projectName} oninput={(e)=> { error = ""; projectName = e.target.value}} placeholder="eg: programming" class="w-full bg-gray-700/40 h-12 rounded-lg px-4 py-1" />
        <textarea rows="4" bind:value={projectDescription} oninput={(e)=> { error = "";projectDescription = e.target.value}} placeholder="Description" class="w-full bg-gray-700/40 rounded-lg px-4 py-2" />
        
        {#if error.length > 0}
            <p class="text-sm p-2 text-red-600">{error}</p>
        {/if}
        <p class="rounded-lg text-sm p-2 bg-gray-600/40">Projects keep chats, files, and custom instructions in one place. Use them for ongoing work, or just to keep things tidy.</p>
        <div class="w-full flex justify-end items-center p-2 rounded-full">
            <button onclick={handleProject} class="bg-gray-700/40 px-4 py-2 rounded-full font-semibold">{$editProjectId.length > 0 ? "Edit":"Create"} Project</button>
        </div>
    </div>
</Modal>