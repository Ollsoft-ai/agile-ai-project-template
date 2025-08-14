<script lang="ts">
	import { signIn } from '$lib/supertokens';
	import { goto } from '$app/navigation';

	let email = '';
	let password = '';
	let loading = false;
	let errors: string[] = [];

	async function handleSignIn() {
		errors = [];
		loading = true;

		try {
			const response = await signIn({
				formFields: [
					{
						id: 'email',
						value: email
					},
					{
						id: 'password',
						value: password
					}
				]
			});

			if (response.status === 'FIELD_ERROR') {
				response.formFields.forEach((formField) => {
					if (formField.id === 'email') {
						errors.push(formField.error);
					}
				});
			} else if (response.status === 'WRONG_CREDENTIALS_ERROR') {
				errors.push('Email or password is incorrect.');
			} else if (response.status === 'SIGN_IN_NOT_ALLOWED') {
				errors.push(response.reason);
			} else {
				// Sign in successful
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
</script>

<div class="w-full max-w-md mx-auto bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
	<h2 class="text-2xl font-bold text-center text-gray-900 dark:text-white mb-6">Sign In</h2>
	
	{#if errors.length > 0}
		<div class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-md p-3 mb-4">
			{#each errors as error}
				<p class="text-sm text-red-600 dark:text-red-400">{error}</p>
			{/each}
		</div>
	{/if}

	<form on:submit|preventDefault={handleSignIn} class="space-y-4">
		<div>
			<label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
				Email
			</label>
			<input
				type="email"
				id="email"
				bind:value={email}
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

		<button
			type="submit"
			disabled={loading}
			class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
		>
			{loading ? 'Signing In...' : 'Sign In'}
		</button>
	</form>

	<div class="mt-4 text-center">
		<p class="text-sm text-gray-600 dark:text-gray-400">
			Forgot your password? 
			<a href="/auth/reset-password" class="text-blue-600 hover:text-blue-500 dark:text-blue-400 dark:hover:text-blue-300">
				Reset it here
			</a>
		</p>
	</div>
</div>
