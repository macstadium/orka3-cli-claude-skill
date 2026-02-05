---
name: orka3-cli
description: Expert guidance for using the Orka3 CLI to manage macOS virtualization infrastructure. Use when users need to work with Orka VMs, images, nodes, or cluster resources through natural language requests like "Create 3 VMs with macOS Sonoma", "Show me all running VMs", "How do I configure VM networking?", "Set up a CI/CD pipeline", or any VM management, troubleshooting, or infrastructure configuration tasks. Covers VM lifecycle, image management, OCI registries, node operations, namespaces, RBAC, and authentication.
---

# Orka3 CLI

## Overview

This skill provides expert guidance for using the Orka3 CLI, MacStadium's command-line tool for managing macOS virtualization infrastructure. Use this skill to translate natural language requests into proper Orka3 CLI commands and workflows.

**Current Version:** Orka 3.5.2 (requires cluster upgrade from Orka 3.4+ / k8s v1.33+)

## Core Concepts

**Architecture Types:**
- `amd64` (Intel): Mac Pro, Mac mini (Intel), iMac Pro
- `arm64` (Apple Silicon): Mac mini (M1/M2/M3/M4), Mac Studio

**Key Components:**
- **VMs**: Virtual machines running macOS
- **Images**: Disk images containing macOS OS and configurations (local or OCI-based)
- **Nodes**: Physical Mac hardware providing compute resources
- **Namespaces**: Resource isolation and access control (default: `orka-default`)
- **Service Accounts**: Authentication for CI/CD integrations

**Authentication:**
- User login: `orka3 login` (MacStadium Customer Portal credentials)
- Service accounts: For automation and CI/CD
- Tokens: Valid for 1 hour, stored in `~/.kube/config`

**Namespace Resolution (v3.5.2+):**
The CLI uses hierarchical namespace resolution:
1. `--namespace` flag (highest priority)
2. `ORKA_DEFAULT_NAMESPACE` environment variable
3. Namespace from orka kubeconfig context (automatic detection)
4. Falls back to `orka-default`

## Getting Started Workflow

For first-time setup, follow this sequence:

```bash
# 1. Configure the CLI
orka3 config set --api-url <ORKA_API_URL>

# 2. Set up shell completion (optional)
orka3 completion bash  # or zsh, fish, powershell

# 3. Authenticate
orka3 login

# 4. Verify connectivity
orka3 node list
```

**Finding API URL:**
- Orka 2.1+: `http://10.221.188.20` (Private-1 .20 address)
- Pre-2.1: `http://10.221.188.100`
- Orka domain: `https://company.orka.app`
- Custom domain: `https://company.com`

## Quick VM Operations

**Deploy a VM (simplest form):**
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

**List VMs:**
```bash
orka3 vm list                    # Basic info
orka3 vm list --output wide      # Detailed info
orka3 vm list <VM_NAME>          # Specific VM
```

**Delete VMs:**
```bash
orka3 vm delete <VM_NAME>
orka3 vm delete <VM1> <VM2>      # Multiple VMs
```

**Connect to VMs:**
- Screen Sharing: `vnc://<VM-IP>:<Screenshare-port>` (from `orka3 vm list`)
- Default credentials: `admin/admin` (for MacStadium base images)

## Image Management

**Working with Local Images:**
```bash
orka3 image list                 # List local images
orka3 image copy <SRC> <DST>     # Copy image
orka3 image delete <IMAGE>       # Delete image
```

**Image Caching (Apple Silicon only):**
```bash
# Cache image on specific nodes
orka3 imagecache add <IMAGE> --nodes <NODE1>,<NODE2>

# Cache on all nodes in namespace
orka3 imagecache add <IMAGE> --all

# Cache on tagged nodes
orka3 imagecache add <IMAGE> --tags <TAG>

# Check caching status
orka3 imagecache info <IMAGE>

# List cached images
orka3 imagecache list
```

**OCI Registry Integration:**
```bash
# Add registry credentials (admin only)
orka3 regcred add https://ghcr.io --username <USER> --password <TOKEN>

# Deploy from OCI image
orka3 vm deploy --image ghcr.io/org/repo/image:tag

# Push VM to OCI registry (ARM only)
orka3 vm push <VM_NAME> ghcr.io/org/repo/image:tag
orka3 vm get-push-status <JOB_NAME>
```

## VM Lifecycle Operations

**Saving Changes:**
```bash
# Save as new image (preserves original)
orka3 vm save <VM_NAME> <NEW_IMAGE_NAME>

# Commit to original image (modifies original)
orka3 vm commit <VM_NAME>

# Push to OCI registry (ARM only)
orka3 vm push <VM_NAME> <IMAGE:TAG>
```

**Resizing Disks:**
```bash
# Apple Silicon (automatic)
orka3 vm resize <VM_NAME> <NEW_SIZE_GB>

# Intel (with automatic repartition)
orka3 vm resize <VM_NAME> <SIZE> --user admin --password admin
```

**Power Operations (Intel only):**
```bash
orka3 vm start <VM_NAME>         # Power on
orka3 vm stop <VM_NAME>          # Power off
orka3 vm suspend <VM_NAME>       # Suspend
orka3 vm resume <VM_NAME>        # Resume
orka3 vm revert <VM_NAME>        # Revert to image
```

## VM Configuration Templates

Create reusable templates for consistent VM deployments:

```bash
# Create template
orka3 vm-config create <NAME> \
  --image <IMAGE> \
  --cpu 6 \
  --memory 12

# Create with node affinity
orka3 vm-config create <NAME> \
  --image <IMAGE> \
  --tag jenkins-builds \
  --tag-required

# Deploy from template
orka3 vm deploy --config <TEMPLATE_NAME>

# Deploy and override settings
orka3 vm deploy --config <TEMPLATE> --cpu 8 --memory 16

# List and delete templates
orka3 vm-config list
orka3 vm-config delete <NAME>
```

## Node Management

**Basic Operations:**
```bash
orka3 node list                  # List nodes
orka3 node list --output wide    # Detailed info
orka3 node list <NODE_NAME>      # Specific node
```

**Node Tagging (admin only):**
```bash
# Tag node for affinity
orka3 node tag <NODE> <TAG>

# Remove tag
orka3 node untag <NODE> <TAG>

# Check tags
orka3 node list <NODE> --output wide
```

**Moving Nodes Between Namespaces (admin only):**
```bash
orka3 node namespace <NODE> <TARGET_NAMESPACE>
```

## Namespace Management (Admin)

**Creating and Managing Namespaces:**
```bash
# Create namespace
orka3 namespace create orka-test

# Create for custom pods
orka3 namespace create orka-cp --enable-custom-pods

# List namespaces
orka3 namespace list

# Delete namespace (must be empty)
orka3 namespace delete orka-test
```

**After Creating a Namespace:**
1. Move nodes to provide resources: `orka3 node namespace <NODE> <NAMESPACE>`
2. Grant user access: `orka3 rb add-subject --namespace <NS> --user <EMAIL>`
3. Grant service account access: `orka3 rb add-subject --namespace <NS> --serviceaccount <SA_NS>:<SA_NAME>`

## Access Control (Admin)

**Service Accounts:**
```bash
# Create service account
orka3 sa create <SA_NAME>

# Create in specific namespace
orka3 sa create <SA_NAME> --namespace <NS>

# Get token (valid 1 year by default)
orka3 sa token <SA_NAME>

# Get token with custom duration
orka3 sa token <SA_NAME> --duration 1h

# Get token with no expiration
orka3 sa token <SA_NAME> --no-expiration

# List service accounts
orka3 sa list
orka3 sa list --namespace <NS>

# Delete service account
orka3 sa delete <SA_NAME>
```

**Rolebindings (RBAC):**
```bash
# Grant user access to namespace
orka3 rb add-subject --namespace <NS> --user <EMAIL>

# Grant multiple users access
orka3 rb add-subject --namespace <NS> --user <EMAIL1>,<EMAIL2>

# Grant service account access
orka3 rb add-subject --namespace <NS> --serviceaccount <SA_NS>:<SA_NAME>

# List subjects in namespace
orka3 rb list-subjects --namespace <NS>

# Revoke access
orka3 rb remove-subject --namespace <NS> --user <EMAIL>
orka3 rb remove-subject --namespace <NS> --serviceaccount <SA_NS>:<SA_NAME>
```

## Common Workflows

**Setting Up a CI/CD Pipeline:**
1. Create service account: `orka3 sa create sa-jenkins`
2. Get token: `orka3 sa token sa-jenkins`
3. Configure token in CI/CD tool
4. Create VM config for builds: `orka3 vmc create ci-build --image <IMAGE> --cpu 4`
5. Deploy in CI: `orka3 vm deploy --config ci-build`

**Multi-Namespace Setup:**
1. Create namespace: `orka3 namespace create orka-team`
2. Move nodes: `orka3 node namespace mini-1 orka-team`
3. Grant access: `orka3 rb add-subject --namespace orka-team --user team@company.com`
4. Create service account: `orka3 sa create sa-team-ci --namespace orka-team`

**Image Preparation Workflow:**
1. Deploy base VM: `orka3 vm deploy --image ghcr.io/macstadium/orka-images/sonoma:latest`
2. Connect via Screen Sharing
3. Install software and configure
4. Save image: `orka3 vm save <VM> my-configured-image`
5. Delete VM: `orka3 vm delete <VM>`
6. Deploy new VMs: `orka3 vm deploy --image my-configured-image`

## Command Patterns & Flags

**Common Global Flags:**
- `-n, --namespace`: Specify namespace (default: `orka-default`)
- `-o, --output`: Output format (`table` (default), `wide`, `json`)
- `-h, --help`: Display help

**Output Formats:**
- `table`: Essential information (default)
- `wide`: Extended details and additional columns
- `json`: Machine-readable for scripting

**Command Aliases:**
- `vm-config` → `vmc`
- `serviceaccount` → `sa`
- `rolebinding` → `rb`
- `registrycredential` → `regcred`
- `imagecache` → `ic`

## Architecture-Specific Features

**Intel Only (amd64):**
- `orka3 image generate`: Create empty images for OS installs
- `orka3 iso` commands: Manage installation ISOs
- Power operations: `start`, `stop`, `suspend`, `resume`, `revert`
- `--iso`: Attach ISO during deployment
- `--gpu`: Enable GPU passthrough (requires `--disable-vnc`)
- `--system-serial`: Custom serial number
- `--disable-net-boost`: Disable network performance boost

**Apple Silicon Only (arm64):**
- `orka3 vm push`: Push to OCI registries
- `orka3 imagecache`: Cache images on nodes
- OCI image support: Deploy directly from registries
- Automatic disk resize (no SSH credentials needed)

## VM Shared Attached Disk Configuration (v3.5.2+)

The Orka AMI supports automatic setup of VM shared attached disks during instance initialization. This is an infrastructure-level configuration, not a CLI command.

**Key Capabilities:**
- **Flexible deployment control**: Enable/disable shared disk usage globally via `vm_shared_disk_enabled: true` in Ansible
- **Instance-level disk sizing**: Specify shared disk size per Mac instance via user data script (AWS) or Ansible (on-prem)
- **Consistent VM storage**: When enabled, all VMs deployed from the instance automatically use the shared attached disk

**Critical Limitation for Apple Silicon:** When shared attached disk is enabled, **only one VM may run per Apple silicon node**.

### AWS Deployment (Two-Step Process)

**Step 1: Enable globally via CodeBuild/Ansible**
```yaml
vm_shared_disk_enabled: true
```

**Step 2: Configure each EC2 Mac Instance via user data script**
```bash
#!/bin/bash
export VM_SHARED_DISK_SIZE=500
/usr/local/bin/bootstrap-orka <eks-cluster-name> <aws-region> <orka-engine-license-key>
```

Both steps are required. The bootstrap script configures the instance to use shared disk, and all subsequent VM deployments from that instance will utilize it.

**To disable:** Set `vm_shared_disk_enabled: false` in Ansible, re-run CodeBuild, then terminate and re-create EC2 Mac instances.

### On-Prem / MSDC Deployment

Set in Ansible:
```yaml
vm_shared_disk_enabled: true
osx_node_orka_vm_shared_disk_size: <SIZE_IN_GB>  # Optional disk size
```

### Requirements
- Orka cluster upgraded to v3.5.2 (from Orka 3.4+ / k8s v1.33+)
- Global config: `vm_shared_disk_enabled: true` in Ansible (disabled by default)
- AWS: `VM_SHARED_DISK_SIZE` environment variable in user data script
- Apple Silicon: Shared disk feature is disabled by default

## Getting Help

**Built-in Help:**
```bash
orka3 --help                     # Main help
orka3 <command> --help           # Command help
orka3 <command> <sub> --help     # Sub-command help
```

**Checking Async Operations:**
- Images: `orka3 image list <IMAGE>`
- Image caching: `orka3 imagecache info <IMAGE>`
- Image push: `orka3 vm get-push-status <JOB_NAME>`

**JSON Output with jq:**
```bash
# Get all VM names
orka3 vm list -o json | jq -r '.items[].name'

# Get VMs with >4 CPUs
orka3 vm list -o json | jq '.items[] | select(.cpu > 4)'

# Count VMs
orka3 vm list -o json | jq '.items | length'
```

## Reference Documentation

For detailed command syntax, options, and advanced usage patterns, load the specific reference file based on the user's query:

### Command References (by domain)
| File | Contents |
|------|----------|
| `references/commands/vm-commands.md` | VM deploy, list, delete, save, commit, push, resize, power operations |
| `references/commands/image-commands.md` | Image list, copy, delete, generate; Image cache operations |
| `references/commands/registry-commands.md` | OCI registry credential management |
| `references/commands/admin-commands.md` | Namespace, service account, and RBAC commands |
| `references/commands/node-commands.md` | Node list, tag, untag, namespace operations |
| `references/commands/config-commands.md` | CLI config, authentication, shell completion |
| `references/commands/vm-config-commands.md` | VM configuration template commands |

### Workflow Guides
| File | Contents |
|------|----------|
| `references/workflows/getting-started.md` | Initial setup, first VM, shell completion |
| `references/workflows/cicd-workflows.md` | CI/CD pipeline setup, service accounts |
| `references/workflows/image-workflows.md` | Custom image creation, caching, OCI registry |
| `references/workflows/admin-workflows.md` | Multi-namespace setup, node tagging, RBAC |
| `references/workflows/scaling-workflows.md` | Load testing, disk management, optimization |
| `references/workflows/migration-workflows.md` | Intel to ARM migration, backup/recovery |
| `references/workflows/shared-disk-workflows.md` | VM shared attached disk configuration (v3.5.2+) |

### Troubleshooting Guides
| File | Contents |
|------|----------|
| `references/troubleshooting/auth-issues.md` | Token expiration, permissions, service accounts |
| `references/troubleshooting/deployment-issues.md` | Resource errors, VM unresponsive, name conflicts |
| `references/troubleshooting/image-issues.md` | Async operations, deletion, caching problems |
| `references/troubleshooting/network-issues.md` | Screen Sharing, SSH, port conflicts, performance |

### Loading Strategy

Load references based on user query type:
- **"How do I deploy a VM?"** → `references/commands/vm-commands.md`
- **"Set up CI/CD"** → `references/workflows/cicd-workflows.md`
- **"Authentication error"** → `references/troubleshooting/auth-issues.md`
- **"VM won't start"** → `references/troubleshooting/deployment-issues.md`
- **"Create namespace"** → `references/commands/admin-commands.md`
- **"Shared disk" / "attached disk"** → `references/workflows/shared-disk-workflows.md`

## Log Sources (v3.4+)

For troubleshooting and monitoring, Orka provides several log sources:

| Log Type | Location | Access Method | Purpose |
|----------|----------|---------------|---------|
| Virtual Kubelet Logs | Mac Node | Via promtail: `/var/log/virtual-kubelet/vk.log` | Interactions between k8s and worker node for managing virtualization |
| Orka VM Logs | Mac Node | Via promtail: `/opt/orka/logs/vm/` | Logs pertaining to the lifecycle of a specific VM |
| Orka Engine Logs | Engine Node | `/opt/orka/logs/com.macstadium.orka-engine.server.managed.log` | Logs pertaining to Orka Engine |
| Pod Logs | Kubernetes | Kubernetes Client, Dashboard, or Helm Chart exposing to secondary service | All Kubernetes-level behavior |

## macOS Compatibility (v3.5.2+)

**Supported macOS Versions:**
- macOS Tahoe (26.0): Full support with v3.5.2 fixes for image deletion, copying, and tagging
- macOS Sequoia: Display resolution fixes require Orka VM tools v3.5.2
  - New images created with Orka 3.5.2 include updated VM tools automatically
  - Existing images must have Orka VM tools updated manually to receive display resolution fixes

## Best Practices

1. **Always verify namespace context** - Use `-n` flag or check current context
2. **Use output formats appropriately** - `--output wide` for troubleshooting, `json` for scripting
3. **Cache images before mass deployments** - Improves deployment consistency
4. **Use VM configs for repeatability** - Create templates for common VM types
5. **Tag nodes for workload isolation** - Use `--tag` for targeted deployments
6. **Test with single VM first** - Verify image/config before mass deployment
7. **Save images regularly** - Preserve work with `vm save` or `vm commit`
8. **Use service accounts for automation** - Never use user credentials in CI/CD
9. **Check async operation status** - Don't assume operations completed
10. **Use OCI registries for images** - Modern approach recommended over deprecated remote-image commands

## Documentation & Troubleshooting Guidelines

When writing documentation, troubleshooting guides, or CI/CD integration docs, follow these rules:

### CLI Patterns

**Use CLI's built-in filtering - NEVER pipe to grep:**
```bash
# CORRECT: Use CLI arguments
orka3 vm-config list <config-name>
orka3 vm list <vm-name>
orka3 image list <image-name>

# WRONG: Don't pipe to grep
orka3 vm-config list | grep "config-name"
orka3 vm list | grep "vm-name"
```

### CI/CD Authentication

**NEVER suggest `orka3 login` or `orka3 user get-token` for CI/CD pipelines.** User tokens expire after 1 hour.

**ALWAYS use service accounts for automation:**
```bash
# Create service account
orka3 sa create <name>

# Get token (valid 1 year by default)
orka3 sa token <name>
```

### Environment Variables in Containers

**Don't suggest `export VAR=value` for CI/CD troubleshooting.** Environment variables must be:
- Configured in CI/CD settings (GitLab CI/CD Variables, GitHub Secrets, Jenkins credentials)
- Passed during container start
- NOT exported in a troubleshooting shell session (they won't persist)

### Network Connectivity Checks

**Use ONE consistent approach. Prefer curl over ping (ping can be disabled):**
```bash
# CORRECT: Use curl to cluster-info endpoint
curl -s -o /dev/null -w "%{http_code}" "$ORKA_ENDPOINT/api/v1/cluster-info"

# AVOID: ping can be disabled on networks
ping -c 3 <ip-address>
```

### Troubleshooting Docs Structure

1. **Trust CLI error messages** - If CLI says "config does not exist", it doesn't exist. Don't add "verify it exists" steps.

2. **Don't duplicate integration error handling** - If a Docker image validates dependencies at build time, don't add "verify CLI is installed" steps.

3. **Understand execution context:**
   - Tokens passed via CI/CD job context are only available during job execution
   - You cannot manually verify `$ORKA_TOKEN` inside a container - it's injected at runtime
   - CI/CD runners often auto-delete failed VMs - suggest deploying manually to troubleshoot

4. **One approach per problem** - Don't show 3 different ways to check connectivity. Pick the best one.

### Example: SSH Troubleshooting in CI/CD

**WRONG approach:**
```markdown
1. Check SSH on the failed VM
2. Verify the key fingerprint
```

**CORRECT approach:**
```markdown
Since the runner automatically deletes failed VMs, deploy a VM manually to troubleshoot:
1. orka3 vm deploy test-debug --config <config>
2. Connect via VNC and verify SSH settings
3. Test SSH manually
4. orka3 vm delete test-debug
```
