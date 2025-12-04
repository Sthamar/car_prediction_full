<script lang="ts">
	import favicon from '$lib/assets/favicon.svg';
	import '../app.css';
	import { auth } from '$lib/stores/auth';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	let { children } = $props();

	onMount(() => {
		auth.initialize();
	});

	function handleLogout() {
		auth.logout();
		goto('/login');
	}
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<div class="min-h-screen bg-base-100">
	<div class="navbar bg-base-100 shadow-sm">
		<div class="flex-1">
			<a href="/" class="btn btn-ghost text-xl">CarServicePrediction</a>
		</div>
		<div class="flex-none">
			<ul class="menu menu-horizontal px-1">
				{#if $auth.isAuthenticated}
					<li><a href="/dashboard">Dashboard</a></li>
					<li><a href="/vehicles">Vehicles</a></li>
					<li><a href="/profile">Profile</a></li>
					{#if $auth.user?.is_superuser}
						<li><a href="/admin">Admin</a></li>
					{/if}
					<li><button on:click={handleLogout}>Logout</button></li>
				{:else}
					<li><a href="/login">Login</a></li>
					<li><a href="/register">Register</a></li>
				{/if}
			</ul>
		</div>
	</div>

	<main class="container mx-auto p-4">
		{@render children()}
	</main>
</div>
