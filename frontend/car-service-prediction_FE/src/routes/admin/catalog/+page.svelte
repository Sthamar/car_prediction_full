<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { api } from '$lib/api';

	let makes: any[] = [];
	let loading = true;
	let showAddMakeForm = false;
	let showAddModelForm = false;
	let selectedMake: any = null;

	let newMakeName = '';
	let newModelName = '';
	let newModelMakeId = 0;

	let loaded = false;

	$: if (!$auth.loading && !loaded) {
		loaded = true;
		if (!$auth.isAuthenticated || !$auth.user?.is_superuser) {
			goto('/login');
		} else {
			loadMakes();
		}
	}

	async function loadMakes() {
		try {
			const response = await api.get('/catalog/makes');
			if (response.ok) {
				makes = await response.json();
			}
		} catch (e) {
			console.error('Error loading makes:', e);
		} finally {
			loading = false;
		}
	}

	async function handleAddMake() {
		if (!newMakeName.trim()) return;

		try {
			const response = await api.post('/catalog/makes', { name: newMakeName });
			if (response.ok) {
				await loadMakes();
				newMakeName = '';
				showAddMakeForm = false;
			} else {
				const error = await response.json();
				alert(error.detail || 'Failed to add make');
			}
		} catch (e) {
			alert('An error occurred');
		}
	}

	async function handleAddModel() {
		if (!newModelName.trim() || !newModelMakeId) return;

		try {
			const response = await api.post('/catalog/models', {
				name: newModelName,
				make_id: newModelMakeId
			});
			if (response.ok) {
				await loadMakes();
				newModelName = '';
				newModelMakeId = 0;
				showAddModelForm = false;
				selectedMake = null;
			} else {
				const error = await response.json();
				alert(error.detail || 'Failed to add model');
			}
		} catch (e) {
			alert('An error occurred');
		}
	}

	async function deleteMake(id: number) {
		if (!confirm('Are you sure? This will delete all models for this make.')) return;

		try {
			const response = await api.delete(`/catalog/makes/${id}`);
			if (response.ok) {
				await loadMakes();
			}
		} catch (e) {
			alert('Failed to delete make');
		}
	}

	async function deleteModel(id: number) {
		if (!confirm('Are you sure you want to delete this model?')) return;

		try {
			const response = await api.delete(`/catalog/models/${id}`);
			if (response.ok) {
				await loadMakes();
			}
		} catch (e) {
			alert('Failed to delete model');
		}
	}

	function openAddModelForm(make: any) {
		selectedMake = make;
		newModelMakeId = make.id;
		showAddModelForm = true;
		showAddMakeForm = false;
	}
</script>

<div class="container mx-auto p-6">
	<h1 class="text-3xl font-bold mb-6">Vehicle Catalog Management</h1>

	{#if loading}
		<div class="flex justify-center items-center h-64">
			<span class="loading loading-spinner loading-lg"></span>
		</div>
	{:else}
		<div class="mb-6 flex gap-4">
			<button
				class="btn btn-primary"
				on:click={() => {
					showAddMakeForm = !showAddMakeForm;
					showAddModelForm = false;
				}}
			>
				{showAddMakeForm ? 'Cancel' : 'Add Make'}
			</button>
		</div>

		{#if showAddMakeForm}
			<div class="card bg-base-100 shadow-xl mb-6">
				<div class="card-body">
					<h2 class="card-title">Add Vehicle Make</h2>
					<form on:submit|preventDefault={handleAddMake}>
						<div class="form-control">
							<label class="label" for="make-name">
								<span class="label-text">Make Name</span>
							</label>
							<input
								type="text"
								id="make-name"
								bind:value={newMakeName}
								placeholder="e.g., Toyota, Honda, Ford"
								class="input input-bordered"
								required
							/>
						</div>
						<div class="card-actions justify-end mt-4">
							<button type="button" class="btn" on:click={() => (showAddMakeForm = false)}
								>Cancel</button
							>
							<button type="submit" class="btn btn-primary">Add Make</button>
						</div>
					</form>
				</div>
			</div>
		{/if}

		{#if showAddModelForm}
			<div class="card bg-base-100 shadow-xl mb-6">
				<div class="card-body">
					<h2 class="card-title">Add Model for {selectedMake?.name}</h2>
					<form on:submit|preventDefault={handleAddModel}>
						<div class="form-control">
							<label class="label" for="model-name">
								<span class="label-text">Model Name</span>
							</label>
							<input
								type="text"
								id="model-name"
								bind:value={newModelName}
								placeholder="e.g., Camry, Accord, F-150"
								class="input input-bordered"
								required
							/>
						</div>
						<div class="card-actions justify-end mt-4">
							<button
								type="button"
								class="btn"
								on:click={() => {
									showAddModelForm = false;
									selectedMake = null;
								}}>Cancel</button
							>
							<button type="submit" class="btn btn-primary">Add Model</button>
						</div>
					</form>
				</div>
			</div>
		{/if}

		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
			{#each makes as make}
				<div class="card bg-base-100 shadow-xl">
					<div class="card-body">
						<h2 class="card-title flex justify-between">
							{make.name}
							<button class="btn btn-sm btn-error" on:click={() => deleteMake(make.id)}
								>Delete</button
							>
						</h2>

						<div class="divider">Models ({make.models?.length || 0})</div>

						{#if make.models && make.models.length > 0}
							<ul class="menu bg-base-200 rounded-box">
								{#each make.models as model}
									<li class="flex flex-row justify-between items-center">
										<span>{model.name}</span>
										<button class="btn btn-xs btn-ghost" on:click={() => deleteModel(model.id)}>
											<svg
												xmlns="http://www.w3.org/2000/svg"
												class="h-4 w-4"
												fill="none"
												viewBox="0 0 24 24"
												stroke="currentColor"
											>
												<path
													stroke-linecap="round"
													stroke-linejoin="round"
													stroke-width="2"
													d="M6 18L18 6M6 6l12 12"
												/>
											</svg>
										</button>
									</li>
								{/each}
							</ul>
						{:else}
							<p class="text-sm text-gray-500">No models added yet</p>
						{/if}

						<div class="card-actions justify-end mt-4">
							<button class="btn btn-sm btn-primary" on:click={() => openAddModelForm(make)}>
								Add Model
							</button>
						</div>
					</div>
				</div>
			{/each}
		</div>

		{#if makes.length === 0}
			<div class="alert alert-info">
				<span>No vehicle makes added yet. Click "Add Make" to get started!</span>
			</div>
		{/if}
	{/if}
</div>
