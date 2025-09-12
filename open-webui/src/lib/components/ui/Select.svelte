<script>
	import { onDestroy, onMount } from "svelte";

    let { selectTitle = "Default Placeholder",className="",options=$bindable([]),optionClass="",onChange=()=>{},selectValue="" } = $props();

    let onOptionClick = $state(false);
    let dropdownElement = $state(); // Reference to the dropdown element

    function handleClickOutside(event) {
        if (dropdownElement && !dropdownElement.contains(event.target)) {
            onOptionClick = false;
        }
    }

    onMount(() => {
        // selectTitle = options[0].title
        // selectValue = options[0].value
        document.addEventListener('click', handleClickOutside);
    });

    onDestroy(() => {
        document.removeEventListener('click', handleClickOutside);
    });
</script>

<div bind:this={dropdownElement} class="flex items-center relative">
    <button onclick={()=> onOptionClick = !onOptionClick} class={`cursor-pointer dark:bg-gray-700/20 max-w-fit rounded-sm py-2 px-2 text-xs bg-transparent text-right ${className}`}>{selectTitle}</button>

    {#if onOptionClick}
        <span class={`z-30 w-full max-h-[300px] overflow-y-scroll absolute top-[110%] dark:bg-black/60 rounded-sm py-2 px-2 backdrop-blur-xl text-xs text-right flex flex-col justify-start items-start gap-3 ${optionClass}`}>
            {#each options as option}
                <button onclick={()=>{
                    selectTitle = option['title']
                    selectValue = option['value']
                    onOptionClick = false
                    onChange(selectValue)
                }} class="border-b w-full border-gray-700/50 py-1 cursor-pointer">{option['title']}</button>
            {/each}
        </span>
    {/if}
</div>