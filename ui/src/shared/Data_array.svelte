<script>
    export let strategy;
    export let botWallet;
    export let holdWallet;
    export let totalFees;
    export let percentage;
</script>

<div class="data">
    <div class="row">
        <h2>{strategy}</h2>
        <h2>{botWallet} $</h2>
        <h2>{holdWallet} $</h2>
        <h2>{totalFees} $</h2>
        <h2>{percentage}</h2>
    </div>
</div>

<style>
	.row
	{
		display: flex;
		flex-direction: row;
		justify-content: space-around;
		align-items: flex-start;
		gap: 25px;
        background-color: chartreuse;
	}

    h2
	{
		font-size: 16px;
		color: #616161;
		font-family: 'Quicksand', sans-serif;
	}
</style>