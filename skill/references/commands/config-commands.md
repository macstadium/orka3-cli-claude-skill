# Configuration and Authentication Commands Reference

## orka3 config set

```bash
orka3 config set --api-url <URL>
```

```bash
orka3 config set --api-url http://10.221.188.20
orka3 config set --api-url https://company.orka.app
```

## orka3 config view

```bash
orka3 config view
```

## Default Namespace Detection (v3.5.2+)

Namespace resolution hierarchy (highest to lowest priority):
1. `--namespace` / `-n` flag
2. `ORKA_DEFAULT_NAMESPACE` environment variable
3. Namespace from orka kubeconfig context
4. Falls back to `orka-default`

```bash
# Set via environment variable
export ORKA_DEFAULT_NAMESPACE=my-team-namespace

# Set via kubectl context
kubectl config set-context orka --namespace=orka-default
```

## orka3 login

Opens browser for MacStadium Customer Portal authentication. Token stored in `~/.kube/config`, valid for 1 hour.

```bash
orka3 login
```

## orka3 user get-token

Prints authentication token from `~/.kube/config`.

```bash
orka3 user get-token
```

## orka3 user set-token

Authenticates with a token directly (used for service account auth in CI/CD).

```bash
orka3 user set-token <TOKEN>
```

## orka3 completion

```bash
orka3 completion {bash|fish|powershell|zsh}
```

**Persistent setup:**
```bash
# Bash (macOS)
orka3 completion bash > $(brew --prefix)/etc/bash_completion.d/orka3
# Bash (Linux)
orka3 completion bash > /etc/bash_completion.d/orka3
# Zsh (macOS)
orka3 completion zsh > $(brew --prefix)/share/zsh/site-functions/_orka3
# Zsh (Linux)
orka3 completion zsh > "${fpath[1]}/_orka3"
```

## orka3 version

```bash
orka3 version
```

Shows CLI build info and cluster compatibility.
