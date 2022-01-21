<div class="card">
    <slot></slot>
</div>

<style>
    .card
    {
        display: flex;
		flex-direction: row;
		justify-content: center;
        margin-left: 30%;
        margin-right: 30%;
        background: #fff;
        padding: 20px;
        border-radius: 6px;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
    }
</style>