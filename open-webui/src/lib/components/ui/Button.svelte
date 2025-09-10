<script>
    const{ type, disabled = false,onclick=()=>{}, children} = $props()
</script>

<button
    {disabled}
    {onclick}
    class="bg-gray-700/5 hover:bg-gray-700/10 dark:bg-gray-100/5 dark:hover:bg-gray-100/10 dark:text-gray-300 dark:hover:text-white transition w-full rounded-full font-medium text-sm py-2.5"
    {type}
>
    {@render children()}
</button>