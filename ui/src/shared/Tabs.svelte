<script>
    import { createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

    export let items;
    export let activeItem;
</script>

<div class="tabs">
    <ul>
        {#each items as item}
            <li on:click={ () => dispatch('switch', item)}>
                <div class:active={activeItem == item}>{item}</div>
            </li>
        {/each}
    </ul>
</div>

<style>
    ul
    {
        display: flex;
        justify-content: center;
        padding: 0;
        list-style-type: none;
    }

    li
    {
        margin: 0 16px;
        font-size: 18px;
        cursor: pointer;
        color: #616161;
    }

    .tabs
    {
        margin-bottom: 40px;
    }
    .active
    {
        color:#ae5bf8;
        border-bottom: 2px solid #ae5bf8;
        padding-bottom: 8px;
    }
</style>