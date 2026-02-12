# Authentication Troubleshooting

## Token expired

```bash
# Re-authenticate (interactive)
orka3 login

# For service accounts, generate new token
orka3 sa token <SA_NAME>
orka3 user set-token <NEW_TOKEN>
```

User tokens expire after 1 hour. Service account tokens expire after their configured duration (default: 1 year). Use service accounts with `--no-expiration` for long-running automation.

## Unable to connect to Orka cluster

Symptoms: connection timeout, "Connection refused", "No route to host".

```bash
# Verify API URL
orka3 config view

# Fix if incorrect
orka3 config set --api-url http://10.221.188.20    # Orka 2.1+
orka3 config set --api-url http://10.221.188.100   # Pre-2.1
orka3 config set --api-url https://company.orka.app  # Domain

# Test connectivity
curl -s -o /dev/null -w "%{http_code}" "$ORKA_API_URL/api/v1/cluster-info"
```

Also verify VPN connection. Contact MacStadium support if issues persist.

## Forbidden / Insufficient permissions

```bash
# Check your namespace access
orka3 namespace list

# Ask admin to grant access
orka3 rb add-subject --namespace <NS> --user <YOUR_EMAIL>

# For service accounts
orka3 rb add-subject --namespace <NS> --serviceaccount <SA_NS>:<SA_NAME>
```

## Admin commands fail

Only admin users can create/delete namespaces, manage service accounts, manage rolebindings, tag/untag nodes, move nodes between namespaces, and manage registry credentials. Contact your Orka cluster admin or MacStadium to request admin privileges.

## Service account token not working

```bash
# Verify SA exists
orka3 sa list

# Generate new token
orka3 sa token <SA_NAME>

# For automation, use no-expiration
orka3 sa token <SA_NAME> --no-expiration

# If SA was deleted, recreate
orka3 sa create <SA_NAME>
orka3 sa token <SA_NAME>
```

## Token Expiration Reference

| Token Type | Default Expiration | Configurable |
|------------|-------------------|--------------|
| User login | 1 hour | No |
| Service account | 1 year (8760h) | Yes |
| Service account (no expiration) | Never | Yes |
