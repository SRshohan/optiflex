<script lang="ts">
	import DOMPurify from 'dompurify';

	import { onDestroy } from 'svelte';

	import tippy from 'tippy.js';


	let { placement = 'top',content = `I'm a tooltip!`,touch = true,className = 'flex',theme = '',offset = [0, 4],allowHTML = true,tippyOptions = {}} = $props()

	let tooltipElement = $state();
	let tooltipInstance = $state();

	$effect(()=>{
		if (tooltipElement && content) {
			if (tooltipInstance) {
				tooltipInstance.setContent(DOMPurify.sanitize(content));
			} else {
				tooltipInstance = tippy(tooltipElement, {
					content: DOMPurify.sanitize(content),
					placement: placement,
					allowHTML: allowHTML,
					touch: touch,
					...(theme !== '' ? { theme } : { theme: 'dark' }),
					arrow: false,
					offset: offset,
					...tippyOptions
				});
			}
		} else if (tooltipInstance && content === '') {
			if (tooltipInstance) {
				tooltipInstance.destroy();
			}
		}
	})

	onDestroy(() => {
		if (tooltipInstance) {
			tooltipInstance.destroy();
		}
	});
</script>

<div bind:this={tooltipElement} class={className}>
	<slot />
</div>
