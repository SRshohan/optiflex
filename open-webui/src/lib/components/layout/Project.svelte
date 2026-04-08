<script>
	import { getContext } from "svelte";
    import {addedProjects, deleteProjectId, showAddProjectModal, showDeleteProjectModal , editProjectId , showEditProjectModal} from '$lib/stores';
	import Chats from "./Chats.svelte";
	import ChevronDown from "../icons/ChevronDown.svelte";
	import ChevronRight from "../icons/ChevronRight.svelte";
    const i18n = getContext('i18n');

    let showChats = $state(false);
    let projectId = $state("")

    async function handleDelete(id){
        deleteProjectId.set(id);
        showDeleteProjectModal.set(true);
    }

    async function handleEdit(id){
        editProjectId.set(id);
        
        // showEditProjectModal.set(true);
        $showAddProjectModal = true
    }
</script>

<div>
    <div class="flex justify-start items-center gap-2 text-gray-800 dark:text-gray-200">
 
        <div>
            <img src="/Icons/Project.svg" alt="newProject" />
            <!-- <svg
                    class="size-4"
                    aria-hidden="true"
                    xmlns="http://www.w3.org/2000/svg"
                    width="32"
                    height="32"
                    fill="none"
                    viewBox="0 0 24 24"
                >
                    <path
                        stroke="currentColor"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M10 3v4a1 1 0 0 1-1 1H5m4 8h6m-6-4h6m4-8v16a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V7.914a1 1 0 0 1 .293-.707l3.914-3.914A1 1 0 0 1 9.914 3H18a1 1 0 0 1 1 1Z"
                    />
            </svg> -->
        </div>
        <div onclick={()=> $showAddProjectModal = true} class="w-full flex justify-start items-center gap-2">
            <p class="cursor-pointer m-0 p-0 text-[16px]">{$i18n.t('New Project')}</p>
        </div>

        
    </div>
    <div class="ml-4 mt-5 flex flex-col justify-start gap-3">
        {#each $addedProjects as project}
            <div class="flex justify-between items-center">
                <a href={`/project/${project.id}`} class="cursor-pointer">{project.name}</a>
                <div class="flex items-center gap-2 cursor-pointer">
                    <span onclick={()=> {showChats = !showChats; projectId = project.id }}>
                        {#if showChats && projectId === project.id}
                            <ChevronDown className="coursor-pointer size-3" strokeWidth="2.5" />
                        {:else}
                            <ChevronRight className="coursor-pointer size-3" strokeWidth="2.5" />
                        {/if}
                    </span>
                    <span onclick={()=>handleEdit(project.id)}>
                        <img  class="h-4" src="/Icons/Edit.svg" alt="edit" />
                    </span>
                    <p onclick={()=>handleDelete(project.id)} class="text-lg text-red-600 font-bold">X</p>
                </div>
            </div>
            {#if showChats && projectId === project.id}
                <Chats projectId={project.id} />
            {/if}
        {/each}
    </div>
</div>