<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { isLoggedIn, isLoading, checkSession } from '$lib/stores/auth';

	let { children } = $props();

	onMount(async () => {
		await checkSession();
		
		if (!$isLoggedIn) {
			goto('/auth');
		}
	});
</script>

{#if $isLoading}
	<div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
		<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
	</div>
{:else if $isLoggedIn}
	{@render children?.()}
{:else}
	<div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
		<div class="text-center">
			<p class="text-lg text-gray-600 dark:text-gray-400">Redirecting to authentication...</p>
		</div>
	</div>
{/if}
