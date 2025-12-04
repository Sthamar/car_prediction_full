<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { api } from '$lib/api';

	let stats: any = {
		total_users: 0,
		total_vehicles: 0,
		total_predictions: 0,
		total_makes: 0
	};
	let loading = true;
	let loaded = false;

	$: if (!$auth.loading && !loaded) {
		loaded = true;
		if (!$auth.isAuthenticated || !$auth.user?.is_superuser) {
			goto('/login');
		} else {
			loadStats();
		}
	}

	async function loadStats() {
		try {
			const usersRes = await api.get('/users/');
			const makesRes = await api.get('/catalog/makes');

			if (usersRes.ok) {
				const users = await usersRes.json();
				stats.total_users = users.length;
			}

			if (makesRes.ok) {
				const makes = await makesRes.json();
				stats.total_makes = makes.length;
			}
		} catch (e) {
			console.error('Error loading admin stats', e);
		} finally {
			loading = false;
		}
	}
</script>

<div class="container mx-auto p-6">
	<h1 class="text-3xl font-bold mb-6">Super Admin Dashboard</h1>

	{#if loading}
		<div class="flex justify-center items-center h-64">
			<span class="loading loading-spinner loading-lg"></span>
		</div>
	{:else}
		<!-- Stats Overview -->
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
			<div class="stats shadow">
				<div class="stat">
					<div class="stat-title">Total Users</div>
					<div class="stat-value">{stats.total_users}</div>
					<div class="stat-desc">Registered users</div>
				</div>
			</div>

			<div class="stats shadow">
				<div class="stat">
					<div class="stat-title">Vehicle Makes</div>
					<div class="stat-value">{stats.total_makes}</div>
					<div class="stat-desc">In catalog</div>
				</div>
			</div>
		</div>

		<!-- Quick Actions -->
		<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
			<div class="card bg-base-100 shadow-xl">
				<div class="card-body">
					<h2 class="card-title">Vehicle Catalog</h2>
					<p>Manage vehicle makes and models available to users.</p>
					<div class="card-actions justify-end">
						<a href="/admin/catalog" class="btn btn-primary">Manage Catalog</a>
					</div>
				</div>
			</div>

			<div class="card bg-base-100 shadow-xl">
				<div class="card-body">
					<h2 class="card-title">User Management</h2>
					<p>View and manage registered users.</p>
					<div class="card-actions justify-end">
						<a href="/admin" class="btn btn-secondary">Manage Users</a>
					</div>
				</div>
			</div>
		</div>
	{/if}
</div>
