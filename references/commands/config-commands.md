# Configuration and Utility Commands Reference

This reference provides detailed syntax and examples for configuration, authentication, and utility Orka3 CLI commands.

## Configuration Commands

### orka3 config set

Set the Orka service URL for your environment.

**Syntax:**
```bash
orka3 config set --api-url <URL> [flags]
```

**Options:**
- `-a, --api-url string` - (Required) The Orka service URL
- `-h, --help` - Display help

**Examples:**
```bash
orka3 config set --api-url http://10.221.188.20
orka3 config set --api-url https://company.orka.app
```

### orka3 config view

View the current local Orka CLI configuration.

**Syntax:**
```bash
orka3 config view [flags]
```

## Authentication Commands

### orka3 login

Log in to your Orka cluster with MacStadium Customer Portal credentials.

**Syntax:**
```bash
orka3 login [flags]
```

**Notes:**
- Opens browser for authentication
- Token stored in `~/.kube/config`
- Token valid for 1 hour

### orka3 user get-token

Print your authentication token from ~/.kube/config.

**Syntax:**
```bash
orka3 user get-token [flags]
```

### orka3 user set-token

Log in with a valid authentication token.

**Syntax:**
```bash
orka3 user set-token <TOKEN> [flags]
```

## Utility Commands

### orka3 completion

Generate shell autocompletion scripts.

**Syntax:**
```bash
orka3 completion {bash|fish|powershell|zsh} [flags]
```

**Examples:**
```bash
# Bash (load current session)
source <(orka3 completion bash)

# Bash (persist - Linux)
orka3 completion bash > /etc/bash_completion.d/orka3

# Bash (persist - macOS)
orka3 completion bash > $(brew --prefix)/etc/bash_completion.d/orka3

# Zsh (load current session)
source <(orka3 completion zsh)

# Zsh (persist - Linux)
orka3 completion zsh > "${fpath[1]}/_orka3"

# Zsh (persist - macOS)
orka3 completion zsh > $(brew --prefix)/share/zsh/site-functions/_orka3
```

### orka3 version

Print the current version of the Orka CLI.

**Syntax:**
```bash
orka3 version [flags]
```

**Output Includes:**
- CLI build information
- Compatibility with Orka cluster
