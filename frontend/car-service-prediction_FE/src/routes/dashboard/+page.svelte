<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { api } from '$lib/api';

	let stats: any = null;
	let recentPredictions: any[] = [];
	let vehicles: any[] = [];
	let loading = true;

	onMount(async () => {
		await new Promise((resolve) => setTimeout(resolve, 100));

		if (!$auth.isAuthenticated) {
			goto('/login');
			return;
		}

		await loadDashboardData();
	});

	async function loadDashboardData() {
		try {
			// Load statistics
			const statsResponse = await api.get('/predictions/stats');
			if (statsResponse.ok) {
				stats = await statsResponse.json();
			}

			// Load recent predictions
			const predictionsResponse = await api.get('/predictions/history?limit=5');
			if (predictionsResponse.ok) {
				recentPredictions = await predictionsResponse.json();
			}

			// Load vehicles
			const vehiclesResponse = await api.get('/vehicles/');
			if (vehiclesResponse.ok) {
				vehicles = await vehiclesResponse.json();
			}
		} catch (e) {
			console.error('Error loading dashboard data:', e);
		} finally {
			loading = false;
		}
	}

	function formatDate(dateString: string) {
		return new Date(dateString).toLocaleDateString();
	}
</script>

<div class="container mx-auto p-6">
	<h1 class="text-3xl font-bold mb-6">Dashboard</h1>

	{#if loading}
		<div class="flex justify-center items-center h-64">
			<span class="loading loading-spinner loading-lg"></span>
		</div>
	{:else}
		<!-- Statistics Cards -->
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
			<div class="stats shadow">
				<div class="stat">
					<div class="stat-figure text-primary">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
							class="inline-block w-8 h-8 stroke-current"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
							></path>
						</svg>
					</div>
					<div class="stat-title">Total Predictions</div>
					<div class="stat-value text-primary">{stats?.total_predictions || 0}</div>
					<div class="stat-desc">{stats?.predictions_this_month || 0} this month</div>
				</div>
			</div>

			<div class="stats shadow">
				<div class="stat">
					<div class="stat-figure text-secondary">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
							class="inline-block w-8 h-8 stroke-current"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
							></path>
						</svg>
					</div>
					<div class="stat-title">Vehicles</div>
					<div class="stat-value text-secondary">{stats?.total_vehicles || 0}</div>
					<div class="stat-desc"><a href="/vehicles" class="link">Manage vehicles</a></div>
				</div>
			</div>

			<div class="stats shadow">
				<div class="stat">
					<div class="stat-figure text-accent">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
							class="inline-block w-8 h-8 stroke-current"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
							></path>
						</svg>
					</div>
					<div class="stat-title">Services Tracked</div>
					<div class="stat-value text-accent">{stats?.total_services || 0}</div>
					<div class="stat-desc">Service records</div>
				</div>
			</div>

			<div class="stats shadow">
				<div class="stat">
					<div class="stat-figure text-warning">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
							class="inline-block w-8 h-8 stroke-current"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
							></path>
						</svg>
					</div>
					<div class="stat-title">Upcoming Services</div>
					<div class="stat-value text-warning">{stats?.upcoming_services || 0}</div>
					<div class="stat-desc">Next 30 days</div>
				</div>
			</div>
		</div>

		<!-- Quick Actions -->
		<div class="mb-8">
			<h2 class="text-2xl font-bold mb-4">Quick Actions</h2>
			<div class="flex flex-wrap gap-4">
				<a href="/" class="btn btn-primary">
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
							d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
						/>
					</svg>
					New Prediction
				</a>
				<a href="/vehicles" class="btn btn-secondary">
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
							d="M12 6v6m0 0v6m0-6h6m-6 0H6"
						/>
					</svg>
					Add Vehicle
				</a>
			</div>
		</div>

		<!-- Recent Predictions -->
		<div class="mb-8">
			<h2 class="text-2xl font-bold mb-4">Recent Predictions</h2>
			{#if recentPredictions.length > 0}
				<div class="overflow-x-auto">
					<table class="table w-full">
						<thead>
							<tr>
								<th>Date</th>
								<th>Vehicle</th>
								<th>Mileage</th>
								<th>Service Needed</th>
								<th>Risk Level</th>
								<th>Days Until Service</th>
							</tr>
						</thead>
						<tbody>
							{#each recentPredictions as prediction}
								<tr>
									<td>{formatDate(prediction.created_at)}</td>
									<td>{prediction.make} {prediction.model} ({prediction.year})</td>
									<td>{prediction.mileage.toLocaleString()} km</td>
									<td>
										{#if prediction.service_needed}
											<span class="badge badge-warning">Yes</span>
										{:else}
											<span class="badge badge-success">No</span>
										{/if}
									</td>
									<td>
										<span
											class="badge"
											class:badge-error={prediction.risk_level === 'high'}
											class:badge-warning={prediction.risk_level === 'medium'}
											class:badge-success={prediction.risk_level === 'low'}
										>
											{prediction.risk_level}
										</span>
									</td>
									<td>{prediction.estimated_days_until_service} days</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
				<div class="mt-4">
					<a href="/predictions" class="link">View all predictions →</a>
				</div>
			{:else}
				<div class="alert alert-info">
					<span>No predictions yet. <a href="/" class="link">Make your first prediction!</a></span>
				</div>
			{/if}
		</div>

		<!-- My Vehicles -->
		<div>
			<h2 class="text-2xl font-bold mb-4">My Vehicles</h2>
			{#if vehicles.length > 0}
				<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
					{#each vehicles as vehicle}
						<div class="card bg-base-100 shadow-xl">
							<div class="card-body">
								<h3 class="card-title">
									{vehicle.nickname || `${vehicle.make} ${vehicle.model}`}
									{#if vehicle.is_default}
										<span class="badge badge-primary">Default</span>
									{/if}
								</h3>
								<p class="text-sm text-gray-600">
									{vehicle.year} • {vehicle.mileage.toLocaleString()} km
								</p>
								<p class="text-sm">
									{vehicle.transmission} • {vehicle.fuel_type}
								</p>
								<div class="card-actions justify-end mt-4">
									<a href="/vehicles/{vehicle.id}" class="btn btn-sm btn-primary">View Details</a>
								</div>
							</div>
						</div>
					{/each}
				</div>
			{:else}
				<div class="alert alert-info">
					<span
						>No vehicles added yet. <a href="/vehicles" class="link">Add your first vehicle!</a
						></span
					>
				</div>
			{/if}
		</div>
	{/if}
</div>
