<script>
    import Card2 from "card.svelte";

    export let strategy_name;
    export let pair_name;
    export let wallet;
    export let fees_maker;
    export let fees_taker;
    export let dateString;
    export let time_interval;
    export let handleSubmit;
    export let strategy;
    export let interval;
    export let pair;
    export let is_loading;
</script>

<slot>
<Card2>
    <div class="container">
        <div class="row">
            <div class="elt">
                <form on:submit|preventDefault={handleSubmit}>
                    <div class="form_elt">
                        <h2>Strategy</h2>
                        <select bind:value={strategy_name}>
                            {#each strategy as question}
                                <option value={question}>
                                    {question.text}
                                </option>
                            {/each}
                        </select>
                    </div>
                </form>
            </div>
            <div class="elt">
                <form on:submit|preventDefault={handleSubmit}>
                    <div class="form_elt">
                        <h2>Crypto</h2>
                        <select bind:value={pair_name}>
                            {#each pair as question}
                                <option value={question}>
                                    {question.text}
                                </option>
                            {/each}
                        </select>
                    </div>
                </form>
            </div>
        </div>

        <div class="elt">
                <h2>Starting wallet</h2>
                <input type=number bind:value={wallet}>
        </div>

        <div class="row">
            <div class="elt">
                <h2>Maker fee</h2>
                <input type=number bind:value={fees_maker}>
            </div>

            <div class="elt">
                <h2>Taker fee</h2>
                <input type=number bind:value={fees_taker}>
            </div>
        </div>

        <div class="row">
            <div class="elt">
                <h2>Start date</h2>
                <input type=date bind:value={dateString}>
            </div>

            <div class="elt">
                <h2>Time interval</h2>
                <select bind:value={time_interval}>
                    {#each interval as question}
                        <option value={question}>
                            {question.text}
                        </option>
                    {/each}
                </select>
            </div>
        </div>

        <div class="row">
        {#if is_loading == 0}
            <button disabled={!pair_name || !strategy_name || !dateString || !fees_maker || !time_interval || !fees_taker || !wallet} type=submit on:click={handleSubmit}>
                
                Simulate
            </button>
        {/if}
            
        </div>
    </div>
</Card2>
</slot>

<style>
    .elt
    {
        text-align: center;
    }

    button
	{
		margin-top: 20px;
		width: 150px;
	}

    .row
	{
		display: flex;
		flex-direction: row;
		justify-content: center;
		gap: 20px;
	}

    input
    {
		width: 150px;
	}
</style>