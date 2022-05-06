<script>
    import GoFlame from 'svelte-icons/go/GoFlame.svelte';
</script>

<footer>
	<div class="copy">
        <div style="display: inline-flex; align-items: center; justify-content: center;">
            <div class="icon">
                <GoFlame/>
            </div>
            Made by Vincent Libeskind
        </div>
    </div>
</footer>

<style>
    footer
	{
		padding: 40px;
		text-align: center;
	}

	.copy
	{
		color: #aaa;
		display: inline-block;
		padding: 20px;
		border-top: 1px solid #bbb;
	}

    .icon
    {
        color: #e9ceff;
        width: 32px;
        height: 32px;
        padding: 10px;
        padding-bottom: 15px;
    }
</style>