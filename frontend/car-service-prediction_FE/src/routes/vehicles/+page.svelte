<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { api } from '$lib/api';

	let vehicles: any[] = [];
	let loading = true;
	let showAddForm = false;
	let editingVehicle: any = null;

	// Form fields
	let formData = {
		make: '',
		model: '',
		year: new Date().getFullYear(),
		vin: '',
		nickname: '',
		mileage: 0,
		engine_size: 0,
		transmission: 'Automatic',
		fuel_type: 'Petrol',
		is_default: false
	};

	// Catalog data
	let makes: any[] = [];
	let modelsByMake: Record<number, any[]> = {};

	onMount(async () => {
		await new Promise((resolve) => setTimeout(resolve, 100));

		if (!$auth.isAuthenticated) {
			goto('/login');
			return;
		}

		await loadCatalog();
		await loadVehicles();
	});

	async function loadCatalog() {
		try {
			const response = await api.get('/catalog/makes');
			if (response.ok) {
				makes = await response.json();
				// For each make, fetch its models
				for (const make of makes) {
					const res = await api.get(`/catalog/makes/${make.id}/models`);
					if (res.ok) {
						modelsByMake[make.id] = await res.json();
					} else {
						modelsByMake[make.id] = [];
					}
				}
			}
		} catch (e) {
			console.error('Error loading catalog', e);
		}
	}

	async function loadVehicles() {
		try {
			const response = await api.get('/vehicles/');
			if (response.ok) {
				vehicles = await response.json();
			}
		} catch (e) {
			console.error('Error loading vehicles:', e);
		} finally {
			loading = false;
		}
	}

	function resetForm() {
		formData = {
			make: '',
			model: '',
			year: new Date().getFullYear(),
			vin: '',
			nickname: '',
			mileage: 0,
			engine_size: 0,
			transmission: 'Automatic',
			fuel_type: 'Petrol',
			is_default: false
		};
		editingVehicle = null;
		showAddForm = false;
	}

	function editVehicle(vehicle: any) {
		formData = { ...vehicle };
		editingVehicle = vehicle;
		showAddForm = true;
	}

	async function handleSubmit() {
		try {
			let response;
			if (editingVehicle) {
				response = await api.put(`/vehicles/${editingVehicle.id}`, formData);
			} else {
				response = await api.post('/vehicles/', formData);
			}

			if (response.ok) {
				await loadVehicles();
				resetForm();
			} else {
				const error = await response.json();
				alert(error.detail || 'Failed to save vehicle');
			}
		} catch (e) {
			alert('An error occurred');
		}
	}

	async function deleteVehicle(id: number) {
		if (!confirm('Are you sure you want to delete this vehicle?')) return;

		try {
			const response = await api.delete(`/vehicles/${id}`);
			if (response.ok) {
				await loadVehicles();
			}
		} catch (e) {
			alert('Failed to delete vehicle');
		}
	}
</script>

<div class="container mx-auto p-6">
	<div class="flex justify-between items-center mb-6">
		<h1 class="text-3xl font-bold">My Vehicles</h1>
		<button class="btn btn-primary" on:click={() => (showAddForm = !showAddForm)}>
			{#if showAddForm}
				Cancel
			{:else}
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
			{/if}
		</button>
	</div>

	{#if showAddForm}
		<div class="card bg-base-100 shadow-xl mb-6">
			<div class="card-body">
				<h2 class="card-title">{editingVehicle ? 'Edit' : 'Add'} Vehicle</h2>
				<form on:submit|preventDefault={handleSubmit}>
					<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
						<div class="form-control">
							<label class="label" for="make">
								<span class="label-text">Make *</span>
							</label>
							<select
								id="make"
								bind:value={formData.make}
								class="select select-bordered"
								required
								on:change={() => {
									formData.model = '';
								}}
							>
								<option value="" disabled selected>Select Make</option>
								{#each makes as make}
									<option value={make.name}>{make.name}</option>
								{/each}
							</select>
						</div>

						<div class="form-control">
							<label class="label" for="model">
								<span class="label-text">Model *</span>
							</label>
							<select
								id="model"
								bind:value={formData.model}
								class="select select-bordered"
								required
								disabled={!formData.make}
							>
								<option value="" disabled selected>Select Model</option>
								{#if formData.make}
									{#each modelsByMake[makes.find((m) => m.name === formData.make)?.id] || [] as model}
										<option value={model.name}>{model.name}</option>
									{/each}
								{/if}
							</select>
						</div>

						<div class="form-control">
							<label class="label" for="year">
								<span class="label-text">Year *</span>
							</label>
							<input
								type="number"
								id="year"
								bind:value={formData.year}
								min="1900"
								max={new Date().getFullYear() + 1}
								class="input input-bordered"
								required
							/>
						</div>

						<div class="form-control">
							<label class="label" for="nickname">
								<span class="label-text">Nickname</span>
							</label>
							<input
								type="text"
								id="nickname"
								bind:value={formData.nickname}
								placeholder="e.g., My Daily Driver"
								class="input input-bordered"
							/>
						</div>

						<div class="form-control">
							<label class="label" for="vin">
								<span class="label-text">VIN</span>
							</label>
							<input
								type="text"
								id="vin"
								bind:value={formData.vin}
								placeholder="Vehicle Identification Number"
								class="input input-bordered"
							/>
						</div>

						<div class="form-control">
							<label class="label" for="mileage">
								<span class="label-text">Mileage (km) *</span>
							</label>
							<input
								type="number"
								id="mileage"
								bind:value={formData.mileage}
								min="0"
								class="input input-bordered"
								required
							/>
						</div>

						<div class="form-control">
							<label class="label" for="engine_size">
								<span class="label-text">Engine Size (L)</span>
							</label>
							<input
								type="number"
								id="engine_size"
								bind:value={formData.engine_size}
								step="0.1"
								min="0"
								class="input input-bordered"
							/>
						</div>

						<div class="form-control">
							<label class="label" for="transmission">
								<span class="label-text">Transmission *</span>
							</label>
							<select
								id="transmission"
								bind:value={formData.transmission}
								class="select select-bordered"
							>
								<option>Automatic</option>
								<option>Manual</option>
								<option>CVT</option>
							</select>
						</div>

						<div class="form-control">
							<label class="label" for="fuel_type">
								<span class="label-text">Fuel Type *</span>
							</label>
							<select id="fuel_type" bind:value={formData.fuel_type} class="select select-bordered">
								<option>Petrol</option>
								<option>Diesel</option>
								<option>Electric</option>
								<option>Hybrid</option>
							</select>
						</div>

						<div class="form-control">
							<label class="label cursor-pointer">
								<span class="label-text">Set as default vehicle</span>
								<input
									type="checkbox"
									bind:checked={formData.is_default}
									class="checkbox checkbox-primary"
								/>
							</label>
						</div>
					</div>

					<div class="card-actions justify-end mt-6">
						<button type="button" class="btn" on:click={resetForm}>Cancel</button>
						<button type="submit" class="btn btn-primary"
							>{editingVehicle ? 'Update' : 'Add'} Vehicle</button
						>
					</div>
				</form>
			</div>
		</div>
	{/if}

	{#if loading}
		<div class="flex justify-center items-center h-64">
			<span class="loading loading-spinner loading-lg"></span>
		</div>
	{:else if vehicles.length > 0}
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
			{#each vehicles as vehicle}
				<div class="card bg-base-100 shadow-xl">
					<div class="card-body">
						<h2 class="card-title">
							{vehicle.nickname || `${vehicle.make} ${vehicle.model}`}
							{#if vehicle.is_default}
								<span class="badge badge-primary">Default</span>
							{/if}
						</h2>
						<div class="space-y-2">
							<p class="text-sm"><strong>Make:</strong> {vehicle.make}</p>
							<p class="text-sm"><strong>Model:</strong> {vehicle.model}</p>
							<p class="text-sm"><strong>Year:</strong> {vehicle.year}</p>
							<p class="text-sm"><strong>Mileage:</strong> {vehicle.mileage.toLocaleString()} km</p>
							{#if vehicle.vin}
								<p class="text-sm"><strong>VIN:</strong> {vehicle.vin}</p>
							{/if}
							<p class="text-sm"><strong>Transmission:</strong> {vehicle.transmission}</p>
							<p class="text-sm"><strong>Fuel:</strong> {vehicle.fuel_type}</p>
						</div>
						<div class="card-actions justify-end mt-4">
							<button class="btn btn-sm btn-primary" on:click={() => editVehicle(vehicle)}
								>Edit</button
							>
							<button class="btn btn-sm btn-error" on:click={() => deleteVehicle(vehicle.id)}
								>Delete</button
							>
						</div>
					</div>
				</div>
			{/each}
		</div>
	{:else}
		<div class="alert alert-info">
			<span>No vehicles added yet. Click "Add Vehicle" to get started!</span>
		</div>
	{/if}
</div>
