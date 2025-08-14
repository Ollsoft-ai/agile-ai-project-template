import SuperTokens from 'supertokens-web-js';
import Session from 'supertokens-web-js/recipe/session';
import EmailPassword from 'supertokens-web-js/recipe/emailpassword';

let isInitialized = false;

export function initSuperTokens() {
	if (isInitialized) return;

	SuperTokens.init({
		appInfo: {
			appName: 'Ollsoft Frontend',
			apiDomain: window.location.origin,
			apiBasePath: '/api',
			websiteDomain: window.location.origin,
			websiteBasePath: '/auth'
		},
		recipeList: [
			EmailPassword.init(),
			Session.init()
		]
	});

	isInitialized = true;
}

// Export commonly used functions
export { signUp, signIn, doesEmailExist } from 'supertokens-web-js/recipe/emailpassword';
export { signOut, doesSessionExist } from 'supertokens-web-js/recipe/session';
