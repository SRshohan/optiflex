<script>
	import { hasLetter, hasNumber, validateEmail, validateName } from "$lib/utils/helper";
	import { getContext } from "svelte";
    
    const i18n = getContext('i18n');
    let { value = $bindable(""), type,name,id,placeHolder,isAuth = false,className="" } = $props();
    let hasError = $state("");

    $effect(()=>{
        if(type === "email" && validateEmail(value) || isAuth && type === "password" && hasLetter(value) && hasNumber(value) || type === "name" && validateName(value)){
            hasError=""
        }
    })

    function fieldValidation(){
        if(type === "email" && !validateEmail(value)){
            hasError="Invalid Email"
        }

        if(type === "name" && !validateName(value)){
            hasError="Name should be between 2 to 20 Characters."
        }

        if(isAuth && type === "password" && !hasLetter(value) && !hasNumber(value)){
             hasError="Password must be 8 Characters long and must contain at least 1 letter and 1 number"
        }
    }
    
</script>

<div class="flex flex-col space-y-2 my-0.5 items-start">
    <input
        bind:value={value}
        type={type}
        onblur={fieldValidation}
        id={id}
        class={`p-1 w-full text-sm rounded ${hasError.length > 0 ? 'border-2 border-red-500':""} ${className}`}
        autocomplete={name}
        name={name}
        placeholder={$i18n.t(placeHolder)}
        required
    />

    {#if hasError.length > 0}
        <p class="text-red-500 text-sm">{hasError}</p>
    {/if}
</div>