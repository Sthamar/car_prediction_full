<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { api } from '$lib/api';

	let userDetails: any = null;
	let loading = true;

	onMount(async () => {
		// Wait a bit for auth store to initialize from localStorage
		await new Promise((resolve) => setTimeout(resolve, 100));

		if (!$auth.isAuthenticated) {
			goto('/login');
			return;
		}

		try {
			const response = await api.get('/auth/me');
			if (response.ok) {
				userDetails = await response.json();
				// Update auth store with full user details including is_superuser
				auth.setUser(userDetails);
			} else {
				// Token might be invalid
				auth.logout();
				goto('/login');
			}
		} catch (e) {
			console.error(e);
		} finally {
			loading = false;
		}
	});
</script>

<div class="card bg-base-100 shadow-xl max-w-2xl mx-auto mt-10">
	<div class="card-body">
		<h2 class="card-title">User Profile</h2>
		{#if loading}
			<span class="loading loading-spinner loading-lg"></span>
		{:else if userDetails}
			<div class="overflow-x-auto">
				<table class="table">
					<tbody>
						<tr>
							<th>ID</th>
							<td>{userDetails.id}</td>
						</tr>
						<tr>
							<th>Email</th>
							<td>{userDetails.email}</td>
						</tr>
						<tr>
							<th>Active</th>
							<td>
								{#if userDetails.is_active}
									<span class="badge badge-success">Yes</span>
								{:else}
									<span class="badge badge-error">No</span>
								{/if}
							</td>
						</tr>
						<tr>
							<th>Superuser</th>
							<td>
								{#if userDetails.is_superuser}
									<span class="badge badge-primary">Yes</span>
								{:else}
									<span class="badge badge-ghost">No</span>
								{/if}
							</td>
						</tr>
					</tbody>
				</table>
			</div>
		{:else}
			<p>Could not load profile.</p>
		{/if}
	</div>
</div>
