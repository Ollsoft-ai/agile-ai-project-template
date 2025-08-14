<script lang="ts">
	import { setLocale } from '$lib/paraglide/runtime';
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import { m } from '$lib/paraglide/messages.js';
	import { isLoggedIn, user } from '$lib/stores/auth';
</script>

<main class="min-h-[100svh] flex items-center justify-center bg-gray-50 text-gray-900 dark:bg-gray-900 dark:text-gray-100">
	<section class="w-full max-w-xl rounded-2xl border border-gray-200 dark:border-gray-800 bg-white/70 dark:bg-gray-950/60 backdrop-blur p-8 shadow-sm">
		<h1 class="text-3xl font-semibold tracking-tight">{m.hello_world({ name: 'SvelteKit User' })}d</h1>

		<div class="mt-6 flex items-center gap-3">
			<button
				class="inline-flex items-center rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500/70 focus-visible:ring-offset-2 focus-visible:ring-offset-white dark:focus-visible:ring-offset-gray-950"
				on:click={() => setLocale('en')}
			>
				English
			</button>
			<button
				class="inline-flex items-center rounded-lg bg-slate-200 px-4 py-2 text-sm font-medium text-slate-900 hover:bg-slate-300 dark:bg-slate-800 dark:text-slate-100 dark:hover:bg-slate-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-400/70 focus-visible:ring-offset-2 focus-visible:ring-offset-white dark:focus-visible:ring-offset-gray-950"
				on:click={() => setLocale('de')}
			>
				Deutsch
			</button>
		</div>

		<!-- Authentication Section -->
		<div class="mt-8 border-t border-gray-200 dark:border-gray-700 pt-6">
			{#if $isLoggedIn}
				<div class="text-center">
					<p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
						Welcome back, {$user?.name || $user?.email || 'User'}!
					</p>
					<div class="flex gap-3 justify-center">
						<button
							class="inline-flex items-center rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500/70 focus-visible:ring-offset-2 focus-visible:ring-offset-white dark:focus-visible:ring-offset-gray-950"
							on:click={() => goto('/dashboard')}
						>
							Go to Dashboard
						</button>
					</div>
				</div>
			{:else}
				<div class="text-center">
					<p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
						Get started by signing in to your account
					</p>
					<div class="flex gap-3 justify-center">
						<button
							class="inline-flex items-center rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500/70 focus-visible:ring-offset-2 focus-visible:ring-offset-white dark:focus-visible:ring-offset-gray-950"
							on:click={() => goto('/auth')}
						>
							Sign In / Sign Up
						</button>
					</div>
				</div>
			{/if}
		</div>

		<p class="mt-6 text-sm text-gray-600 dark:text-gray-400">
			If you use VSCode, install the
			<a
				class="font-medium text-blue-700 underline underline-offset-4 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300"
				href="https://marketplace.visualstudio.com/items?itemName=inlang.vs-code-extension"
				target="_blank"
			>
				Sherlock i18n extension
			</a>
			for a better i18n experience.
		</p>
	</section>
</main>
