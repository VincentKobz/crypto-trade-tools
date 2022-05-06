<script>
	import Card from "./components/card.svelte";
	import Tabs from "./shared/Tabs.svelte"
	import SvelteTable from "svelte-table";
	import Select from 'svelte-select';
	import Copy from './components/copy.svelte';
	import Loading from './components/loading.svelte';

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
			title: "Bot wallet ($)",
			value: v => v.bot_wallet,
			sortable: true,
			class: "text-center",
			headerClass: "text-head",
		},
		{
			key: "hold_wallet",
			title: "Hold Wallet ($)",
			value: v => v.hold_wallet,
			sortable: true,
			class: "text-center",
			headerClass: "text-head",
		},
		{
			key: "total_fee",
			title: "Total fees ($)",
			value: v => v.total_fee,
			sortable: true,
			class: "text-center",
			headerClass: "text-head",
		},
		{
			key: "nb_trades",
			title: "Number of trade",
			value: v => v.nb_trades,
			sortable: true,
			class: "text-center",
			headerClass: "text-head",
		},
		{
			key: "bot_vs_hold",
			title: "Bot vs hold (%)",
			value: v => v.bot_vs_hold,
			sortable: true,
			class: "text-center2",
			headerClass: "text-head",
		},
	];

	const strategy = [
		{ id: 1, label: `Big Will`, value: 'big_will' },
		{ id: 2, label: `Trix`, value: 'trix' },
		{ id: 3, label: `Aligator`, value: 'aligator' },
		{ id: 4, label: `EMA`, value: 'ema' },
		{ id: 5, label: `True`, value: 'true' },
		{ id: 6, label: `MACD`, value: 'macd' }
	];

	const pair = [
		{ id: 1, label: `BTC`, value: 'BTCUSDT' },
		{ id: 2, label: `ETH`, value: 'ETHUSDT' },
		{ id: 3, label: `EGLD`, value: 'EGLDUSDT' },
		{ id: 4, label: `MANA`, value: 'MANAUSDT' },
		{ id: 5, label: `SAND`, value: 'SANDUSDT' },
		{ id: 6, label: `BNB`, value: 'BNBUSDT' },
		{ id: 7, label: `SOL`, value: 'SOLUSDT' },
		{ id: 8, label: `ADA`, value: 'ADAUSDT' },
		{ id: 9, label: `XRP`, value: 'XRPUSDT' },
		{ id: 10, label: `DOT`, value: 'DOTUSDT' }
	];

	const interval = [
		{ id: 1, label: `1 minutes`, value: '1m' },
		{ id: 2, label: `15 minutes`, value: '15m' },
		{ id: 3, label: `30 minutes`, value: '30m' },
		{ id: 4, label: `1 hour`, value: '1h' },
		{ id: 5, label: `2 hours`, value: '2h' },
		{ id: 6, label: `4 hours`, value: '4h' },
		{ id: 7, label: `12 hours`, value: '12h' },
		{ id: 8, label: `1 day`, value: '1d' },
		{ id: 9, label: `3 days`, value: '3d' },
	];

	let pair_name;
	let strategy_name;
	let wallet;
	let maker_fee;
	let taker_fee;
	let time_interval;
	let is_loading = 0;
	let test_all = false;
	let optimize = false;

	let res;

	// tab
	const items = ['Home', 'Result'];
	let activeItem = 'Home';

	let dateString;

	async function handleSubmit() {
		is_loading = 1;

		const raw = JSON.stringify({
			pair: pair_name,
			strategy: strategy_name,
			wallet: wallet,
			maker_fee: maker_fee,
			taker_fee: taker_fee,
			start: dateString,
			interval: time_interval,
			test_all: test_all,
			optimize: optimize
  		});

		var myHeaders = new Headers();
		myHeaders.append("Content-Type", "application/json");

		var requestOptions = {
			method: 'POST',
			headers: myHeaders,
			body: raw,
			redirect: 'follow'
		};

		fetch("http://127.0.0.1:5000/calculate", requestOptions)
		.then(response => response.json())
		.then(result => {
			res = result.data;
			is_loading = 0;
			activeItem = 'Result';
			console.log(res[0])
			generateData(res);
		})
		.catch(error => console.log('error', error));
	}

	let rows = []

	function generateData(res){
		rows = []
		for (var i = 0; i < 1 + (test_all * strategy.length - test_all * 1); i++){
			rows = [...rows, { strategy: res[i][0], bot_wallet: res[i][1], hold_wallet: res[i][2], bot_vs_hold: res[i][4], total_fee:  res[i][3], nb_trades:  res[i][5]}];
		}
		
	};

	function handleSelectStrat(event) {
		strategy_name = event.detail.value;
 	};

	function handleSelectPair(event) {
		pair_name = event.detail.value;
 	};

	function handleSelectInterval(event) {
		time_interval = event.detail.value;
 	};
	
	const Switch = (e) => {
		activeItem = e.detail;
	}

</script>

<svelte:head>
	<title>crypto strat</title>
</svelte:head>

<header>
	<h1>Trading Strat</h1>
</header>

<Tabs {activeItem} {items} on:switch={Switch}/>


{#if activeItem == 'Home'}
	<Card>
		<div class="container">
			<div class="row">
				<div class="elt">
					<form on:submit|preventDefault={handleSubmit}>
						<h2>Strategy</h2>
						<div class="selectThemed">
							<Select items={strategy} on:select={handleSelectStrat} placeholder="..." isDisabled={test_all}></Select>
						</div>
					</form>
				</div>
				<div class="elt">
					<form on:submit|preventDefault={handleSubmit}>
						<h2>Crypto</h2>
						<div class="selectThemed">
							<Select items={pair} on:select={handleSelectPair} placeholder="..."></Select>
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
					<input type=number bind:value={maker_fee}>
				</div>

				<div class="elt">
					<h2>Taker fee</h2>
					<input type=number bind:value={taker_fee}>
				</div>
			</div>

			<div class="row">
				<div class="elt">
					<h2>Start date</h2>
					<input type=date bind:value={dateString}>
				</div>

				<div class="elt">
					<h2>Time interval</h2>
					<div class="selectThemed">
						<Select items={interval} on:select={handleSelectInterval} placeholder="..."></Select>
					</div>
				</div>
			</div>
			<div class="row" style="justify-content: left; padding-left: 10px;">
				<label style="padding-top: 10px; "><input type="checkbox" bind:checked={test_all} style="width: 30px;"/> Compare all strategies</label>
			</div>
			<div class="row" style="justify-content: left; padding-left: 10px; align-items: center;">
				<label style="padding-top: 10px;"><input type="checkbox" bind:checked={optimize} style="width: 30px;"/> Optimize (could take time)</label>
			</div>
			
			<div class="row">
			{#if is_loading == 0}
				<button disabled={!pair_name || !strategy_name || !dateString || !maker_fee || !time_interval || !taker_fee || !wallet} type=submit on:click={handleSubmit}>
					Simulate
				</button>
			{/if}
			</div>
		</div>
	</Card>
{:else}
	<Card>
		<div style="text-align: left; width: 1000px;">
			<SvelteTable columns="{columns}" rows="{rows}"></SvelteTable>
		</div>
	</Card>
{/if}

{#if is_loading}
	<Loading/>
{/if}

<Copy/>

<style>
	header {
		padding: 20px;
		background: #f7f7f7f7;
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

	input {
		width: 150px;
		
	}

	h1 {
		font-size: 30px;
		color: #616161;
		font-family: 'Quicksand', sans-serif;
	}

	h2
	{
		font-size: 16px;
		color: #616161;
		font-family: 'Quicksand', sans-serif;
	}

	.selectThemed {
		min-width: 130px;
		--border: 3px solid #ae5bf8;
		--borderRadius: 10px;
		--placeholderColor: #ae5bf8;
		--borderFocusColor: #ae5bf8;
		--itemIsActiveBG: #c277ff;
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
</style>