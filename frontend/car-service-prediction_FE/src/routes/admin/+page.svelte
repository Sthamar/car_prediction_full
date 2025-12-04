<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { api } from '$lib/api';

	let users: any[] = [];
	let loading = true;
	let error = '';

	onMount(async () => {
		await new Promise((resolve) => setTimeout(resolve, 100));

		if (!$auth.isAuthenticated || !$auth.user?.is_superuser) {
			goto('/login');
			return;
		}

		await fetchUsers();
	});

	async function fetchUsers() {
		try {
			const response = await api.get('/users/');
			if (response.ok) {
				users = await response.json();
			} else {
				const data = await response.json();
				error = data.detail || 'Failed to fetch users';
			}
		} catch (e) {
			error = 'An error occurred';
		} finally {
			loading = false;
		}
	}

	async function deleteUser(userId: number) {
		if (!confirm('Are you sure you want to delete this user?')) return;

		try {
			const response = await api.delete(`/users/${userId}`);
			if (response.ok) {
				users = users.filter((u) => u.id !== userId);
			} else {
				alert('Failed to delete user');
			}
		} catch (e) {
			alert('Error deleting user');
		}
	}
</script>

<div class="container mx-auto p-6">
	<h1 class="text-3xl font-bold mb-6">Admin Dashboard</h1>

	<!-- Quick Actions -->
	<div class="mb-8">
		<h2 class="text-2xl font-bold mb-4">Quick Actions</h2>
		<div class="flex flex-wrap gap-4">
			<a href="/admin/catalog" class="btn btn-primary">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-5 w-5 mr-2"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M8 7v8a2 2 0 002 2h6M8 7V5a2 2 0 012-2h4.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V15a2 2 0 01-2 2h-2M8 7H6a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2v-2"
					/>
				</svg>
				Manage Vehicle Catalog
			</a>
		</div>
	</div>

	<!-- User Management -->
	<div>
		<h2 class="text-2xl font-bold mb-4">User Management</h2>

		{#if error}
			<div class="alert alert-error mb-4">
				<span>{error}</span>
			</div>
		{/if}

		{#if loading}
			<div class="flex justify-center items-center h-64">
				<span class="loading loading-spinner loading-lg"></span>
			</div>
		{:else}
			<div class="overflow-x-auto">
				<table class="table w-full">
					<thead>
						<tr>
							<th>ID</th>
							<th>Email</th>
							<th>Active</th>
							<th>Superuser</th>
							<th>Actions</th>
						</tr>
					</thead>
					<tbody>
						{#each users as user}
							<tr>
								<td>{user.id}</td>
								<td>{user.email}</td>
								<td>
									{#if user.is_active}
										<span class="badge badge-success">Yes</span>
									{:else}
										<span class="badge badge-error">No</span>
									{/if}
								</td>
								<td>
									{#if user.is_superuser}
										<span class="badge badge-primary">Yes</span>
									{:else}
										<span class="badge badge-ghost">No</span>
									{/if}
								</td>
								<td>
									<button
										class="btn btn-error btn-xs"
										on:click={() => deleteUser(user.id)}
										disabled={user.is_superuser}
									>
										Delete
									</button>
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		{/if}
	</div>
</div>
