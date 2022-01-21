<script>
	import Card from "./components/card.svelte";
	import Array from "./shared/Data_array.svelte";
	import Array_head from "./shared/Data_head.svelte";
	import { onMount } from 'svelte';
	import axios from 'axios';
	import Tabs from "./shared/Tabs.svelte"
	import { BarLoader } from 'svelte-loading-spinners'
	import SvelteTable from "svelte-table";
	import { listen } from "svelte/internal";

  	const columns = [
		{
			key: "strategy",
			title: "Strategy",
			value: v => v.strategy,
			sortable: true,
			class: "text-center",
			headerClass: "text-head",
		},
		{
			key: "bot_wallet",
			title: "Bot wallet",
			value: v => v.bot_wallet,
			sortable: true,
			class: "text-center",
			headerClass: "text-head",
		},
		{
			key: "hold_wallet",
			title: "Hold Wallet",
			value: v => v.hold_wallet,
			sortable: true,
			class: "text-center",
			headerClass: "text-head",
		},
		{
			key: "bot_vs_hold %",
			title: "Bot vs hold",
			value: v => v.bot_vs_hold,
			sortable: true,
			class: "text-center2",
			headerClass: "text-head",
		},
	];

	const strategy = [
		{ id: 1, text: `Big Will`, val: 'big_will' },
		{ id: 2, text: `Trix`, val: 'trix' },
		{ id: 3, text: `Aligator`, val: 'aligator' },
		{ id: 4, text: `EMA`, val: 'ema' },
		{ id: 5, text: `True`, val: 'true' }
	];

	const pair = [
		{ id: 1, text: `BTC`, val: 'BTCUSDT' },
		{ id: 2, text: `ETH`, val: 'ETHUSDT' },
		{ id: 3, text: `EGLD`, val: 'EGLDUSDT' },
		{ id: 4, text: `MANA`, val: 'MANAUSDT' },
		{ id: 5, text: `SAND`, val: 'SANDUSDT' },
		{ id: 6, text: `BNB`, val: 'BNBUSDT' },
		{ id: 7, text: `SOL`, val: 'SOLUSDT' },
		{ id: 8, text: `ADA`, val: 'ADAUSDT' },
		{ id: 9, text: `XRP`, val: 'XRPUSDT' },
		{ id: 10, text: `DOT`, val: 'DOTUSDT' }
	];

	const interval = [
		{ id: 1, text: `1 minutes`, val: '1m' },
		{ id: 2, text: `15 minutes`, val: '15m' },
		{ id: 3, text: `30 minutes`, val: '30m' },
		{ id: 4, text: `1 hour`, val: '1h' },
		{ id: 5, text: `2 hours`, val: '2h' },
		{ id: 6, text: `4 hours`, val: '4h' },
		{ id: 7, text: `12 hours`, val: '12h' },
		{ id: 8, text: `1 day`, val: '1d' },
		{ id: 9, text: `3 days`, val: '3d' },
	];

	let pair_name;
	let strategy_name;
	let wallet;
	let fees_maker;
	let fees_taker;
	let time_interval;
	let is_loading = 0;
	let test_all = false;
	let optimize = false;

	let res;

	// tab
	const items = ['Home', 'Result'];
	let activeItem = 'Home';

	let now = new Date(), month, day, year;
	let dateString;
	
	onMount(async ()=> {

		const response = await axios.get('http://127.0.0.1:5000/result');
		res = response.data.data;

        month = '' + (now.getMonth() + 1);
        day = '' + now.getDate();
        year = now.getFullYear();

		if (month.length < 2) 
			month = '0' + month;
		if (day.length < 2) 
			day = '0' + day;

		dateString = [year, month, day].join('-');
	})

	async function handleSubmit() {
		is_loading = 1;
		const response = await axios.post("http://127.0.0.1:5000/parameter?pair="
		+ pair_name.val + "&strategy=" + strategy_name.val
		+ "&wallet=" + wallet + "&interval=" + time_interval.val
		+ "&start=" + dateString + "&maker_fee=" + fees_maker
		+ "&taker_fee=" + fees_taker + "&test_all=" + test_all
		+ "&optimize=" + optimize);

		const response_data = await axios.get('http://127.0.0.1:5000/result');
		res = response_data.data.data;
		generateData();
		console.log(res.test_all[0])
		is_loading = 0;
		activeItem = 'Result';
	}

	let rows = []

	function generateData(){
		for (var i = 0; i < 1 + test_all * 3; i++){
			rows = [...rows, { strategy: res.res[0][i][0], bot_wallet: res.res[0][i][1], hold_wallet: res.res[0][i][2], bot_vs_hold: res.res[0][i][3] }];
		}
		
	};
	

	const Switch = (e) => {
		activeItem = e.detail;
	}

</script>

<svelte:head>
	<title>crypto strat</title>
</svelte:head>

<main>
	
	<h1>TRADING STRAT</h1>
</main>

<Tabs {activeItem} {items} on:switch={Switch}/>

<footer>
{#if activeItem == 'Home'}
	<Card>
		<div class="container">
			<div class="row">
				<div class="elt">
					<form on:submit|preventDefault={handleSubmit}>
						<h2>Strategy</h2>
						<select disabled={test_all} bind:value={strategy_name}>
							{#each strategy as question}
								<option value={question}>
									{question.text}
								</option>
							{/each}
						</select>
					</form>
				</div>
				<div class="elt">
					<form on:submit|preventDefault={handleSubmit}>
						<h2>Crypto</h2>
						<select bind:value={pair_name}>
							{#each pair as question}
								<option value={question}>
									{question.text}
								</option>
							{/each}
						</select>
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
			<div class="row" style="justify-content: left; padding-left: 10px;">
				<label style="padding-top: 10px; "><input type="checkbox" bind:checked={test_all} style="width: 30px;"/> Compare all strategies</label>
			</div>
			<div class="row" style="justify-content: left; padding-left: 10px;">
				<label style="padding-top: 10px;"><input type="checkbox" bind:checked={optimize} style="width: 30px;"/> Optimize (could take time)</label>
			</div>
			
			<div class="row">
			{#if is_loading == 0}
				<button disabled={!pair_name || !strategy_name || !dateString || !fees_maker || !time_interval || !fees_taker || !wallet} type=submit on:click={handleSubmit}>
					Simulate
				</button>
			{/if}
			</div>
		</div>
	</Card>
{:else}
	<Card>
		<div style="text-align: center;width: 600px;">
			<SvelteTable columns="{columns}" rows="{rows}"></SvelteTable>
		</div>
	</Card>
{/if}

{#if is_loading}
<div class="row">
	<div class="BarLoader">
		<h3>Processing</h3>
		<BarLoader size="100" color="#ae5bf8" unit="px" duration="1s"></BarLoader>
	</div>
</div>
{/if}

</footer>


<style>
	main {
		font-size: 10px;
		text-align: center;
	}

	.container
	{
		display: flex;
		flex-direction: column;
		justify-content: center;

	}
	
	.row
	{
		display: flex;
		flex-direction: row;
		justify-content: center;
		align-items: flex-start;
		gap: 25px;
	}

	.elt
	{
		text-align: center;
	}

	button
	{
		margin-top: 20px;
		width: 150px;
	}

	.BarLoader
	{
		display: flex;
		flex-direction: column;
		justify-content: center;
		margin-top: 20px;
		text-align: center;
	}

	input {
		width: 150px;
	}

	h1 {
		color: #ae5bf8;
		text-transform: uppercase;
		font-size: 4em;
	}

	h2
	{
		font-size: 16px;
		color: #616161;
		font-family: 'Quicksand', sans-serif;
	}

	h3
	{
		font-size: 22px;
		color: #616161;
	}

	:global(.text-center) {
		font-size: 17px;
		color: #3d3d3d;
	}

	:global(.text-center2) {
		font-size: 17px;
		color: #3d3d3d;
	}

	:global(.text-head) {
		font-size: 17px;
		color: #616161;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>