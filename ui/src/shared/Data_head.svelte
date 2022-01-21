<script>
    export let res;
    
    genTable(res);

    function genTable(data){
		var table = document.getElementById('TableBot')

		for (var i = 0; i < data.length; i++){
			var row = `<tr>
							<td>${data[i][0][0]}</td>
							<td>${data[i]}</td>
							<td>${data[i]}</td>
					  </tr>`
			table.innerHTML += row
		}
	}
</script>

<table class="data">
    <tr class="row">
        <th><h2>Strategy</h2></th>

        <th><h2>Final wallet</h2></th>

        <th><h2>Hold wallet</h2></th>

        <th><h2>Total fees</h2></th>

        <th><h2>Bot vs hold %</h2></th>
    </tr>

    <tbody id="TableBot">
        
    </tbody>
</table>

<style>
	.row
	{
		display: flex;
		flex-direction: row;
		justify-content: center;
		align-items: flex-start;
		gap: 25px;
	}

    h2
	{
		font-size: 20px;
		color: #616161;
		font-family: 'Quicksand', sans-serif;
	}
</style>