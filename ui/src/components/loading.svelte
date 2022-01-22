<script>
    import { Moon } from 'svelte-loading-spinners'
</script>

<div class="row">
	<div class="BarLoader">
		<h3>Processing</h3>
		<Moon size="60" color="#ae5bf8" unit="px" duration="2s" ></Moon>
	</div>
</div>

<style>
    .BarLoader
	{
		display: flex;
		flex-direction: column;
		align-items: center;
		margin-top: 20px;
		text-align: center;
	}

    h3
	{
		font-size: 20px;
		color: #616161;
		font-family: 'Quicksand', sans-serif;
	}
</style>