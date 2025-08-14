# Frontend Authentication Guide

This guide explains how to modify the SuperTokens authentication setup in your Svelte application.

## 🔧 Current Setup

The authentication is configured in `/src/lib/supertokens.ts` with:
- **Email/Password** authentication
- **Session management**
- Custom UI components

## 📍 Key Files to Modify

| Component | File Path | Purpose |
|-----------|-----------|---------|
| **Core Config** | `/src/lib/supertokens.ts` | SuperTokens initialization & recipe setup |
| **Auth Store** | `/src/lib/stores/auth.ts` | Session state management |
| **Sign In Form** | `/src/lib/components/SignIn.svelte` | Custom sign-in UI |
| **Sign Up Form** | `/src/lib/components/SignUp.svelte` | Custom sign-up UI |
| **Auth Page** | `/src/routes/auth/+page.svelte` | Main authentication page |

## 🚀 Adding New Authentication Methods

### Microsoft Entra ID (Azure AD)

**1. Update SuperTokens Config** (`/src/lib/supertokens.ts`):

```typescript
import SuperTokens from 'supertokens-web-js';
import Session from 'supertokens-web-js/recipe/session';
import EmailPassword from 'supertokens-web-js/recipe/emailpassword';
import ThirdParty from 'supertokens-web-js/recipe/thirdparty'; // Add this

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
		ThirdParty.init({
			signInAndUpFeature: {
				providers: [
					{
						id: "active-directory",
						name: "Microsoft"
					}
				]
			}
		}), // Add this
		Session.init()
	]
});
```

**2. Update Auth Components** - Add social sign-in buttons to your auth forms.

**📚 Reference:** [SuperTokens Built-in Providers](https://supertokens.com/docs/authentication/social/built-in-providers)

### Other Social Providers

Add any of these providers to the `ThirdParty.init()` configuration:

```typescript
providers: [
	{ id: "google", name: "Google" },
	{ id: "github", name: "GitHub" },
	{ id: "apple", name: "Apple" },
	{ id: "discord", name: "Discord" },
	{ id: "facebook", name: "Facebook" },
	{ id: "active-directory", name: "Microsoft" }
]
```

**📚 Reference:** [All Built-in Providers](https://supertokens.com/docs/authentication/social/built-in-providers)

### Passwordless Authentication (OTP/Magic Links)

**1. Install Recipe:**
```bash
npm install supertokens-web-js
```

**2. Update Config:**
```typescript
import Passwordless from 'supertokens-web-js/recipe/passwordless';

// Add to recipeList:
Passwordless.init({
	contactMethod: "EMAIL" // or "PHONE" or "EMAIL_OR_PHONE"
})
```

**📚 Reference:** [Passwordless Setup](https://supertokens.com/docs/authentication/passwordless/initial-setup)

## 🔒 Session Management

### Customize Session Handling

Modify `/src/lib/stores/auth.ts` to:
- Add custom user data fetching
- Handle custom session claims
- Implement role-based access

**📚 Reference:** [Session Management](https://supertokens.com/docs/additional-verification/session-verification/protect-frontend-routes)

### Multi-Factor Authentication

Add TOTP or Email/SMS OTP:

```typescript
import MultiFactorAuth from 'supertokens-web-js/recipe/multifactorauth';
import TOTP from 'supertokens-web-js/recipe/totp';

// Add to recipeList:
MultiFactorAuth.init(),
TOTP.init()
```

**📚 Reference:** [MFA Setup](https://supertokens.com/docs/additional-verification/mfa/initial-setup)

## 🎨 UI Customization

### Using Pre-built UI Components

Replace custom components with SuperTokens pre-built UI:

```bash
npm install supertokens-auth-react
```

**📚 Reference:** [Pre-built UI](https://supertokens.com/docs/references/frontend-sdks/prebuilt-ui/ui-showcase)

### Custom UI Components

Current implementation uses custom Svelte components. Modify:
- `/src/lib/components/SignIn.svelte` - Sign-in form
- `/src/lib/components/SignUp.svelte` - Sign-up form
- `/src/routes/auth/+page.svelte` - Auth page layout

## 🛠️ Backend Requirements

⚠️ **Important:** Any frontend authentication changes require corresponding backend configuration.

**📚 Reference:** [Backend Setup Guide](https://supertokens.com/docs/quickstart/backend-setup)

## 🚨 Testing

After making changes:
1. Clear browser cookies/localStorage
2. Test sign-up flow
3. Test sign-in flow
4. Verify session persistence
5. Test sign-out functionality

---

**📖 Full Documentation:** [SuperTokens Docs](https://supertokens.com/docs)
