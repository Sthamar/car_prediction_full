<script lang="ts">
	import { api } from '$lib/api';
	import { auth } from '$lib/stores/auth';
	import { goto } from '$app/navigation';

	let email = '';
	let password = '';
	let error = '';

	async function handleLogin() {
		try {
			const formData = new FormData();
			formData.append('username', email);
			formData.append('password', password);

			const response = await fetch('http://localhost:8000/auth/token', {
				method: 'POST',
				body: formData
			});

			if (response.ok) {
				const data = await response.json();
				auth.login(data.access_token);
				goto('/');
			} else {
				const data = await response.json();
				error = data.detail || 'Login failed';
			}
		} catch (e) {
			error = 'An error occurred';
		}
	}
</script>

<div class="flex justify-center items-center min-h-screen bg-base-200">
	<div class="card w-96 bg-base-100 shadow-xl">
		<div class="card-body">
			<h2 class="card-title justify-center mb-4">Login</h2>
			{#if error}
				<div class="alert alert-error mb-4">
					<span>{error}</span>
				</div>
			{/if}
			<form on:submit|preventDefault={handleLogin}>
				<div class="form-control w-full max-w-xs">
					<label class="label" for="email">
						<span class="label-text">Email</span>
					</label>
					<input
						type="email"
						id="email"
						bind:value={email}
						placeholder="email@example.com"
						class="input input-bordered w-full max-w-xs"
						required
					/>
				</div>
				<div class="form-control w-full max-w-xs mt-4">
					<label class="label" for="password">
						<span class="label-text">Password</span>
					</label>
					<input
						type="password"
						id="password"
						bind:value={password}
						placeholder="********"
						class="input input-bordered w-full max-w-xs"
						required
					/>
				</div>
				<div class="card-actions justify-center mt-6">
					<button type="submit" class="btn btn-primary w-full">Login</button>
				</div>
			</form>
			<div class="text-center mt-4">
				<a href="/register" class="link link-primary">Don't have an account? Register</a>
			</div>
		</div>
	</div>
</div>
