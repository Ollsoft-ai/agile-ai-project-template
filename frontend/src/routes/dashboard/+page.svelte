<script lang="ts">
	import ProtectedRoute from '$lib/components/ProtectedRoute.svelte';
	import { user, signOut } from '$lib/stores/auth';
</script>

<svelte:head>
	<title>Dashboard - Ollsoft</title>
</svelte:head>

<ProtectedRoute>
	<main class="min-h-screen bg-gray-50 dark:bg-gray-900">
		<!-- Header -->
		<header class="bg-white dark:bg-gray-800 shadow">
			<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
				<div class="flex justify-between items-center py-6">
					<div class="flex items-center">
						<h1 class="text-3xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
					</div>
					<div class="flex items-center space-x-4">
						{#if $user}
							<span class="text-sm text-gray-700 dark:text-gray-300">
								Welcome, {$user.name || $user.email}!
							</span>
						{/if}
						<button
							on:click={signOut}
							class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
						>
							Sign Out
						</button>
					</div>
				</div>
			</div>
		</header>

		<!-- Main Content -->
		<div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
			<div class="px-4 py-6 sm:px-0">
				<div class="border-4 border-dashed border-gray-200 dark:border-gray-700 rounded-lg p-8">
					<div class="text-center">
						<h2 class="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
							🎉 Welcome to your Dashboard!
						</h2>
						<p class="text-gray-600 dark:text-gray-400 mb-6">
							You have successfully authenticated with SuperTokens. This is a protected route that requires authentication to access.
						</p>
						
						{#if $user}
							<div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 max-w-md mx-auto">
								<h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">User Information</h3>
								<div class="space-y-2 text-left">
									<div>
										<span class="font-medium text-gray-700 dark:text-gray-300">User ID:</span>
										<span class="text-gray-900 dark:text-white ml-2">{$user.id}</span>
									</div>
									<div>
										<span class="font-medium text-gray-700 dark:text-gray-300">Email:</span>
										<span class="text-gray-900 dark:text-white ml-2">{$user.email}</span>
									</div>
									{#if $user.name}
										<div>
											<span class="font-medium text-gray-700 dark:text-gray-300">Name:</span>
											<span class="text-gray-900 dark:text-white ml-2">{$user.name}</span>
										</div>
									{/if}
								</div>
							</div>
						{/if}
					</div>
				</div>
			</div>
		</div>
	</main>
</ProtectedRoute>
