<script lang="ts">
	import SignIn from '$lib/components/SignIn.svelte';
	import SignUp from '$lib/components/SignUp.svelte';

	let showSignUp = false;
</script>

<svelte:head>
	<title>Authentication - Ollsoft</title>
</svelte:head>

<main class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
	<div class="max-w-md w-full space-y-8">
		{#if showSignUp}
			<SignUp />
			<div class="text-center">
				<p class="text-sm text-gray-600 dark:text-gray-400">
					Already have an account?
					<button
						on:click={() => showSignUp = false}
						class="font-medium text-blue-600 hover:text-blue-500 dark:text-blue-400 dark:hover:text-blue-300"
					>
						Sign in here
					</button>
				</p>
			</div>
		{:else}
			<SignIn />
			<div class="text-center">
				<p class="text-sm text-gray-600 dark:text-gray-400">
					Don't have an account?
					<button
						on:click={() => showSignUp = true}
						class="font-medium text-blue-600 hover:text-blue-500 dark:text-blue-400 dark:hover:text-blue-300"
					>
						Sign up here
					</button>
				</p>
			</div>
		{/if}
	</div>
</main>
