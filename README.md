# A template to start a fullstack AI project asap

I will make a better README for this soon to describe this.

## Setup

### Frontend
```
cd frontend
npm install
```

Install the "Sherlock - inspector for i18n" extension to be able to preview language mutations.

### Backend
```
openssl rand -hex 32      # 64 hex chars
openssl rand -hex 32      # 64 hex chars
```
Put to .env:
OIDC_CLIENT_SECRET="something1"
SESSION_SECRET="something2"



### Authentik

```
openssl rand -base64 32
```
put the result to .env as:
AUTHENTIK_SECRET_KEY="result"

http://localhost:9000/if/flow/initial-setup/
make initial adming account



TODO:
# SMTP Host Emails are sent to
AUTHENTIK_EMAIL__HOST=localhost
AUTHENTIK_EMAIL__PORT=25
# Optionally authenticate (don't add quotation marks to your password)
AUTHENTIK_EMAIL__USERNAME=
AUTHENTIK_EMAIL__PASSWORD=
# Use StartTLS
AUTHENTIK_EMAIL__USE_TLS=false
# Use SSL
AUTHENTIK_EMAIL__USE_SSL=false
AUTHENTIK_EMAIL__TIMEOUT=10
# Email address authentik will send from, should have a correct @domain
AUTHENTIK_EMAIL__FROM=authentik@localhost


## Instructions

### Frontend

When installing new dependencies, always use the "-D" tag!
```
npm install -D @neco
```