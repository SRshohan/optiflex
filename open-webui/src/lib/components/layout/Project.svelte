<script>
	import { getContext } from "svelte";
	import ChevronDown from "../icons/ChevronDown.svelte";
	import ChevronRight from "../icons/ChevronRight.svelte";

    const i18n = getContext('i18n');
    let open = false
</script>

<div>
    <div class="flex justify-start items-center gap-2 text-gray-800 dark:text-gray-200">
 
        <div>
            <svg
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
            </svg>
        </div>
        <div onclick={()=> open = !open} class="w-full flex justify-start items-center gap-2">
            <p class="m-0 p-0 text-[16px]">{$i18n.t('Project')}</p>
            {#if open}
                <ChevronDown className="cursor-pointer size-3" strokeWidth="2.5" />
            {:else}
                <ChevronRight className="cursor-pointer size-3" strokeWidth="2.5" />
            {/if}
        </div>

        
    </div>
    {#if open}
        <div class="ml-4 mt-5 flex flex-col justify-start gap-3">
            <p>Project 1</p>
            <p>Project 2</p>
            <p>Project 3</p>
        </div>
    {/if}
</div>