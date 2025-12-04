<script lang="ts">
	import { api } from '$lib/api';
	import { goto } from '$app/navigation';

	let email = '';
	let password = '';
	let confirmPassword = '';
	let error = '';

	async function handleRegister() {
		if (password !== confirmPassword) {
			error = 'Passwords do not match';
			return;
		}

		if (password.length > 72) {
			error = 'Password too long, max 72 characters';
			return;
		}

		try {
			const response = await api.post('/auth/register', {
				email,
				password
			});

			if (response.ok) {
				goto('/login');
			} else {
				const data = await response.json();
				error = data.detail || 'Registration failed';
			}
		} catch (e) {
			error = 'An error occurred';
		}
	}
</script>

<div class="flex justify-center items-center min-h-screen bg-base-200">
	<div class="card w-96 bg-base-100 shadow-xl">
		<div class="card-body">
			<h2 class="card-title justify-center mb-4">Register</h2>
			{#if error}
				<div class="alert alert-error mb-4">
					<span>{error}</span>
				</div>
			{/if}
			<form on:submit|preventDefault={handleRegister}>
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
						maxlength="72"
						required
					/>
				</div>
				<div class="form-control w-full max-w-xs mt-4">
					<label class="label" for="confirmPassword">
						<span class="label-text">Confirm Password</span>
					</label>
					<input
						type="password"
						id="confirmPassword"
						bind:value={confirmPassword}
						placeholder="********"
						class="input input-bordered w-full max-w-xs"
						maxlength="72"
						required
					/>
				</div>
				<div class="card-actions justify-center mt-6">
					<button type="submit" class="btn btn-primary w-full">Register</button>
				</div>
			</form>
			<div class="text-center mt-4">
				<a href="/login" class="link link-primary">Already have an account? Login</a>
			</div>
		</div>
	</div>
</div>
