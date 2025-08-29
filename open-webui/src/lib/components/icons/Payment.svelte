<script lang="ts">
    // No changes needed here
    export let className: string = 'w-5 h-5';
    export let strokeWidth: string = '1.5';
</script>

<svg
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
    stroke-width={strokeWidth}
    stroke="currentColor"
    class={className}
>

    <g transform="translate(8 8) scale(0.7)">
        <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M2.25 8.25h19.5M2.25 9h19.5m-16.5 5.25h6m-6 2.25h3.375"
        />
        <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M2.25 18.75h19.5a2.25 2.25 0 002.25-2.25V9.75A2.25 2.25 0 0021.75 7.5H2.25A2.25 2.25 0 000 9.75v6.75A2.25 2.25 0 002.25 18.75z"
        />
    </g>
</svg>