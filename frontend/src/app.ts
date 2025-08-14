import { initSuperTokens } from '$lib/supertokens';
import { browser } from '$app/environment';

// Initialize SuperTokens when the app starts in the browser
if (browser) {
	initSuperTokens();
}
