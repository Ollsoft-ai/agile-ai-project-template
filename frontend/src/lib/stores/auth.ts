import { writable } from 'svelte/store';
import { browser } from '$app/environment';
import { doesSessionExist, signOut as superTokensSignOut } from '$lib/supertokens';
import { goto } from '$app/navigation';

interface User {
	id: string;
	email: string;
	name?: string;
}

export const isLoggedIn = writable<boolean>(false);
export const user = writable<User | null>(null);
export const isLoading = writable<boolean>(true);

// Check session status
export async function checkSession() {
	if (!browser) return;
	
	isLoading.set(true);
	
	try {
		const sessionExists = await doesSessionExist();
		isLoggedIn.set(sessionExists);
		
		if (sessionExists) {
			// You can fetch user info here from your backend
			// For now, we'll just set a placeholder
			user.set({ id: 'user-id', email: 'user@example.com' });
		} else {
			user.set(null);
		}
	} catch (error) {
		console.error('Error checking session:', error);
		isLoggedIn.set(false);
		user.set(null);
	} finally {
		isLoading.set(false);
	}
}

// Sign out function
export async function signOut() {
	try {
		await superTokensSignOut();
		isLoggedIn.set(false);
		user.set(null);
		goto('/auth');
	} catch (error) {
		console.error('Error signing out:', error);
		// Force redirect even if there's an error
		goto('/auth');
	}
}

// Initialize session check when the store is created
if (browser) {
	checkSession();
}
