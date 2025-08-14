<script lang="ts">
	import { signUp, doesEmailExist } from '$lib/supertokens';
	import { goto } from '$app/navigation';

	let email = '';
	let password = '';
	let confirmPassword = '';
	let name = '';
	let loading = false;
	let errors: string[] = [];

	async function handleSignUp() {
		errors = [];
		
		if (password !== confirmPassword) {
			errors.push('Passwords do not match');
			return;
		}

		if (password.length < 8) {
			errors.push('Password must be at least 8 characters');
			return;
		}

		loading = true;

		try {
			const response = await signUp({
				formFields: [
					{
						id: 'email',
						value: email
					},
					{
						id: 'password',
						value: password
					},
					{
						id: 'name',
						value: name
					}
				]
			});

			if (response.status === 'FIELD_ERROR') {
				response.formFields.forEach((formField) => {
					if (formField.id === 'email') {
						errors.push(formField.error);
					} else if (formField.id === 'password') {
						errors.push(formField.error);
					}
				});
			} else if (response.status === 'SIGN_UP_NOT_ALLOWED') {
				errors.push(response.reason);
			} else {
				// Sign up successful
				goto('/dashboard');
			}
		} catch (err: any) {
			if (err.isSuperTokensGeneralError === true) {
				errors.push(err.message);
			} else {
				errors.push('Something went wrong. Please try again.');
			}
		} finally {
			loading = false;
		}
	}

	async function checkEmailUnique() {
		if (!email) return;
		
		try {
			const response = await doesEmailExist({ email });
			if (response.doesExist) {
				errors = errors.filter(e => !e.includes('email'));
				errors.push('Email already exists. Please sign in instead.');
			}
		} catch (err: any) {
			// Handle silently for now
		}
	}
</script>

<div class="w-full max-w-md mx-auto bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
	<h2 class="text-2xl font-bold text-center text-gray-900 dark:text-white mb-6">Create Account</h2>
	
	{#if errors.length > 0}
		<div class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-md p-3 mb-4">
			{#each errors as error}
				<p class="text-sm text-red-600 dark:text-red-400">{error}</p>
			{/each}
		</div>
	{/if}

	<form on:submit|preventDefault={handleSignUp} class="space-y-4">
		<div>
			<label for="name" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
				Name
			</label>
			<input
				type="text"
				id="name"
				bind:value={name}
				required
				class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
				placeholder="Enter your name"
			/>
		</div>

		<div>
			<label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
				Email
			</label>
			<input
				type="email"
				id="email"
				bind:value={email}
				on:blur={checkEmailUnique}
				required
				class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
				placeholder="Enter your email"
			/>
		</div>

		<div>
			<label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
				Password
			</label>
			<input
				type="password"
				id="password"
				bind:value={password}
				required
				class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
				placeholder="Enter your password"
			/>
		</div>

		<div>
			<label for="confirm-password" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
				Confirm Password
			</label>
			<input
				type="password"
				id="confirm-password"
				bind:value={confirmPassword}
				required
				class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
				placeholder="Confirm your password"
			/>
		</div>

		<button
			type="submit"
			disabled={loading}
			class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
		>
			{loading ? 'Creating Account...' : 'Create Account'}
		</button>
	</form>
</div>
