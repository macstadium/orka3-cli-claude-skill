# OCI Registry Commands Reference (Admin only)

## orka3 registrycredential add (alias: regcred)

```bash
orka3 regcred add <SERVER> -u <USER> {-p <PASS> | --password-stdin} [--replace] [--allow-insecure] [-n <NS>]
```

- `--replace` -- Replace existing credentials for this server
- `--allow-insecure` -- Fall back to HTTP if HTTPS unavailable
- Server must include scheme: `https://ghcr.io`, `https://10.221.188.5:30080`

```bash
orka3 regcred add https://ghcr.io -u "$USER" -p "$TOKEN"
echo -n "$PASSWORD" | orka3 regcred add https://ghcr.io -u whoami --password-stdin
orka3 regcred add --allow-insecure http://10.221.188.5:30080 -u admin -p "$PASS"
orka3 regcred add --replace https://ghcr.io -u "$USER" -p "$TOKEN"
```

## orka3 registrycredential list (alias: regcred)

```bash
orka3 regcred list [-n <NAMESPACE>] [-o table|wide|json]
```

## orka3 registrycredential remove (alias: regcred)

```bash
orka3 regcred remove <SERVER> [-n <NAMESPACE>]
```
