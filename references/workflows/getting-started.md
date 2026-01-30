# Getting Started Workflow

This guide covers initial setup and basic VM operations for new Orka3 CLI users.

## Initial Setup Workflow

**Complete first-time setup:**

```bash
# 1. Configure CLI
orka3 config set --api-url http://10.221.188.20

# 2. Enable shell completion (optional but recommended)
source <(orka3 completion bash)  # or zsh, fish, powershell

# 3. Authenticate
orka3 login

# 4. Verify connectivity
orka3 node list
orka3 vm list

# 5. Check available images
orka3 image list
```

## Finding Your API URL

- **Orka 2.1+**: `http://10.221.188.20` (Private-1 .20 address)
- **Pre-2.1**: `http://10.221.188.100`
- **Orka domain**: `https://company.orka.app`
- **Custom domain**: `https://company.com`

## Quick VM Operations

### Deploy Your First VM

```bash
# Deploy from OCI image (recommended)
orka3 vm deploy --image ghcr.io/macstadium/orka-images/sonoma:latest

# Deploy from local image
orka3 vm deploy --image sonoma-90gb-orka3-arm

# Deploy with specific resources
orka3 vm deploy --image <IMAGE> --cpu 6 --memory 16

# Deploy with custom name
orka3 vm deploy my-vm --image <IMAGE> --cpu 4
```

### List and Monitor VMs

```bash
orka3 vm list                    # Basic info
orka3 vm list --output wide      # Detailed info
orka3 vm list <VM_NAME>          # Specific VM
```

### Connect to VMs

1. Get connection info: `orka3 vm list <VM_NAME> --output wide`
2. Connect via Screen Sharing: `vnc://<VM-IP>:<Screenshare-port>`
3. Default credentials: `admin/admin` (for MacStadium base images)

### Delete VMs

```bash
orka3 vm delete <VM_NAME>
orka3 vm delete <VM1> <VM2>      # Multiple VMs
```

## Shell Completion Setup

For persistent shell completion:

**Bash (macOS):**
```bash
orka3 completion bash > $(brew --prefix)/etc/bash_completion.d/orka3
```

**Bash (Linux):**
```bash
orka3 completion bash > /etc/bash_completion.d/orka3
```

**Zsh (macOS):**
```bash
orka3 completion zsh > $(brew --prefix)/share/zsh/site-functions/_orka3
```

**Zsh (Linux):**
```bash
orka3 completion zsh > "${fpath[1]}/_orka3"
```

## Next Steps

After completing initial setup:
1. Explore available images: `orka3 image list`
2. Check node resources: `orka3 node list --output wide`
3. Create VM configuration templates for repeatability
4. Set up service accounts for CI/CD automation
