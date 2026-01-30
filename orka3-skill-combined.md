---
name: orka3-cli
description: Expert guidance for using the Orka3 CLI to manage macOS virtualization infrastructure. Use when users need to work with Orka VMs, images, nodes, or cluster resources through natural language requests like "Create 3 VMs with macOS Sonoma", "Show me all running VMs", "How do I configure VM networking?", "Set up a CI/CD pipeline", or any VM management, troubleshooting, or infrastructure configuration tasks. Covers VM lifecycle, image management, OCI registries, node operations, namespaces, RBAC, and authentication.
---

# Orka3 CLI

## Overview

This skill provides expert guidance for using the Orka3 CLI, MacStadium's command-line tool for managing macOS virtualization infrastructure. Use this skill to translate natural language requests into proper Orka3 CLI commands and workflows.

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

---


# admin-commands

# Admin Commands Reference

This reference provides detailed syntax and examples for administrative Orka3 CLI commands including namespace management, RBAC, and service accounts.

## Namespace Commands

### orka3 namespace create

Create a new namespace.

**Syntax:**
```bash
orka3 namespace create <NAME> [--enable-custom-pods] [flags]
```

**Options:**
- `--enable-custom-pods` - Configure for custom K8s resources (cannot run Orka VMs)

**Name Requirements:**
- Begins with `orka-` prefix
- Max 63 characters (including prefix)
- Lowercase alphanumeric or dashes
- Ends with alphanumeric
- Unique to cluster

**Post-Creation Steps:**
1. Move nodes: `orka3 node namespace <NODE> <NAMESPACE>`
2. Grant access: `orka3 rb add-subject --namespace <NS> --user <EMAIL>`

**Examples:**
```bash
orka3 namespace create orka-test
orka3 namespace create orka-cp --enable-custom-pods
```

### orka3 namespace list

List all namespaces.

**Syntax:**
```bash
orka3 namespace list [<NAME>] [--output <FORMAT>] [flags]
```

**Options:**
- `-o, --output string` - Output format: table|wide|json

### orka3 namespace delete

Delete specified namespaces.

**Syntax:**
```bash
orka3 namespace delete <NAME> [<NAME2> ...] [--timeout <DURATION>] [flags]
```

**Options:**
- `-t, --timeout duration` - Time to wait before giving up (default: 1h0m0s)

**Prerequisites:**
- All VMs/pods must be removed
- All nodes must be moved out

**CAUTION:** Destructive operation - cannot be undone.

## Service Account Commands

### orka3 serviceaccount create (alias: sa)

Create a service account in the specified namespace.

**Syntax:**
```bash
orka3 serviceaccount create <NAME> [--namespace <NS>] [flags]
```

**Options:**
- `-n, --namespace string` - Target namespace (default: "orka-default")
- `-h, --help` - Display help

**Name Requirements:**
- Max 253 characters
- Lowercase alphanumeric, dashes, or periods
- Begins and ends with lowercase alphanumeric
- Unique to namespace

### orka3 serviceaccount token (alias: sa)

Obtain an authentication token for a service account.

**Syntax:**
```bash
orka3 serviceaccount token <NAME> [--duration <DURATION>] [--namespace <NS>] [flags]
```

**Options:**
- `--duration duration` - Token lifetime (default: 8760h = 1 year)
- `--no-expiration` - Create token with no expiration
- `-n, --namespace string` - Target namespace (default: "orka-default")

**Examples:**
```bash
orka3 sa token sa-jenkins
orka3 sa token sa-jenkins --duration 1h
orka3 sa token sa-jenkins --no-expiration
```

### orka3 serviceaccount list (alias: sa)

List service accounts in the specified namespace.

**Syntax:**
```bash
orka3 serviceaccount list [<NAME>] [--namespace <NS>] [--output <FORMAT>] [flags]
```

**Options:**
- `-o, --output string` - Output format: table|wide|json
- `-n, --namespace string` - Target namespace

### orka3 serviceaccount delete (alias: sa)

Delete one or more service accounts.

**Syntax:**
```bash
orka3 serviceaccount delete <NAME> [<NAME2> ...] [--namespace <NS>] [flags]
```

**CAUTION:** Deleting a service account invalidates all associated tokens.

## RBAC Commands (Rolebinding)

### orka3 rolebinding add-subject (alias: rb)

Add a subject to a namespace rolebinding (grant access).

**Syntax:**
```bash
orka3 rolebinding add-subject --namespace <NS> --user <EMAIL>[,<EMAIL2>,...] AND/OR --serviceaccount <SA_NS>:<SA_NAME>[,<SA_NS2>:<SA_NAME2>,...] [flags]
```

**Options:**
- `-u, --user strings` - Users (email addresses, comma-separated)
- `-s, --serviceaccount strings` - Service accounts (NAMESPACE:NAME format, comma-separated)
- `-n, --namespace string` - Target namespace (default: "orka-default")

**Examples:**
```bash
orka3 rb add-subject --namespace orka-test --user user@company.com
orka3 rb add-subject --namespace orka-test --user user1@company.com,user2@company.com
orka3 rb add-subject --namespace orka-test --serviceaccount orka-default:sa-jenkins
orka3 rb add-subject --namespace orka-test --serviceaccount orka-default:sa-jenkins,orka-production:sa-release
orka3 rb add-subject --namespace orka-test --user user@company.com --serviceaccount orka-default:sa-jenkins
```

### orka3 rolebinding list-subjects (alias: rb)

List all rolebinding subjects in a namespace.

**Syntax:**
```bash
orka3 rolebinding list-subjects [--namespace <NS>] [--output <FORMAT>] [flags]
```

**Options:**
- `-o, --output string` - Output format: table|wide|json
- `-n, --namespace string` - Target namespace (default: "orka-default")

**Examples:**
```bash
orka3 rb list-subjects
orka3 rb list-subjects --namespace orka-test
orka3 rb list-subjects | grep 'ServiceAccount'
```

### orka3 rolebinding remove-subject (alias: rb)

Remove a subject from a namespace rolebinding (revoke access).

**Syntax:**
```bash
orka3 rolebinding remove-subject --user <EMAIL>[,<EMAIL2>,...] AND/OR --serviceaccount <SA_NS>:<SA_NAME>[,<SA_NS2>:<SA_NAME2>,...] [--namespace <NS>] [flags]
```

**Options:**
- `-u, --user strings` - Users to remove (email addresses, comma-separated)
- `-s, --serviceaccount strings` - Service accounts to remove (NAMESPACE:NAME format, comma-separated)
- `-n, --namespace string` - Target namespace (default: "orka-default")

**Examples:**
```bash
orka3 rb remove-subject --namespace orka-test --user user@company.com
orka3 rb remove-subject --namespace orka-test --user user1@company.com,user2@company.com
orka3 rb remove-subject --namespace orka-test --serviceaccount orka-default:sa-jenkins
orka3 rb remove-subject --namespace orka-test --user user@company.com --serviceaccount orka-default:sa-jenkins
```

# config-commands

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

# image-commands

# Image Commands Reference

This reference provides detailed syntax and examples for image-related Orka3 CLI commands, including image cache operations.

## Local Image Commands

### orka3 image list

List locally stored images in your Orka cluster.

**Syntax:**
```bash
orka3 image list [<NAME>] [--output <FORMAT>] [flags]
```

**Options:**
- `-o, --output string` - Output format: table|wide|json

**Examples:**
```bash
orka3 image list
orka3 image list sonoma-90gb-orka3-arm
orka3 image list --output json
orka3 image list | grep 'amd64'
```

### orka3 image copy

Copy an image and set a new name for the copy.

**Syntax:**
```bash
orka3 image copy <SOURCE> <DESTINATION> [--description '<DESC>'] [flags]
```

**Options:**
- `-d, --description string` - Custom description for the copy

**Notes:**
- Async operation - check status with `orka3 image list <NAME>`
- Copies description from source by default

### orka3 image generate (Intel only)

Generate a new empty image with the specified size.

**Syntax:**
```bash
orka3 image generate <NAME> <SIZE> [--description '<DESC>'] [flags]
```

**Options:**
- `-d, --description string` - Custom description

**Examples:**
```bash
orka3 image generate 120gbemptyimage 120G
```

**Notes:**
- Intel-only (amd64 architecture)
- Async operation
- Used for fresh macOS installs from ISO

### orka3 image set-description

Set a custom description for an image.

**Syntax:**
```bash
orka3 image set-description <NAME> <DESCRIPTION> [flags]
```

**CAUTION:** Overrides existing description (cannot be undone).

### orka3 image delete

Delete the specified locally stored images.

**Syntax:**
```bash
orka3 image delete <NAME> [<NAME2> ...] [flags]
```

**CAUTION:** Cannot be undone. Affects VMs/configs using this image.

## Image Cache Commands (Apple Silicon only)

### orka3 imagecache add (alias: ic)

Cache an image on specified node(s).

**Syntax:**
```bash
orka3 imagecache add <IMAGE> {--nodes|--tags|--all} [--namespace <NS>] [flags]
```

**Options:**
- `--nodes string` - Specific nodes (comma-separated)
- `--tags string` - Node tags to filter by (comma-separated)
- `--all` - Cache on all nodes in namespace
- `-n, --namespace string` - Target namespace

**Examples:**
```bash
orka3 ic add ghcr.io/macstadium/orka-images/sequoia:latest --nodes mini-arm-10
orka3 ic add sonoma-90gb-orka3-arm --nodes mini-arm-10,mini-arm-11
orka3 ic add sequoia:latest --all
orka3 ic add sonoma:latest --tags jenkins-builds
```

**Notes:**
- Async operation
- Image must be pulled first (or be an OCI image)
- `--nodes`, `--tags`, and `--all` are mutually exclusive

### orka3 imagecache info (alias: ic)

Display the caching status of an image across nodes.

**Syntax:**
```bash
orka3 imagecache info <IMAGE> [--namespace <NS>] [--output <FORMAT>] [flags]
```

**Options:**
- `-o, --output string` - Output format: table|wide|json
- `-n, --namespace string` - Target namespace

**Status Values:**
- `ready` - Available for deployment
- `caching` - Operation still active

### orka3 imagecache list (alias: ic)

List cached images across nodes.

**Syntax:**
```bash
orka3 imagecache list [<IMAGE>] [--namespace <NS>] [--output <FORMAT>] [flags]
```

**Options:**
- `-o, --output string` - Output format: table|wide|json
- `-n, --namespace string` - Target namespace

**Examples:**
```bash
orka3 ic list
orka3 ic list sonoma-90gb-orka3-arm
orka3 ic list ghcr.io/macstadium/orka-images/sequoia
orka3 ic list ghcr.io/macstadium/orka-images/sonoma:14.0
```

# node-commands

# Node Commands Reference

This reference provides detailed syntax and examples for node-related Orka3 CLI commands.

## orka3 node list

Show information about Orka nodes.

**Syntax:**
```bash
orka3 node list [<NAME>] [--namespace <NS>] [--output <FORMAT>] [flags]
```

**Options:**
- `-o, --output string` - Output format: table|wide|json
- `-n, --namespace string` - Target namespace

**Examples:**
```bash
orka3 node list
orka3 node list --output wide
orka3 node list mini-1
orka3 node list --namespace orka-test
orka3 node list --output wide | grep 'mini-arm'
```

## orka3 node tag (Admin)

Tag a node for targeted VM deployment (set node affinity).

**Syntax:**
```bash
orka3 node tag <NODE_NAME> <TAG> [--namespace <NS>] [flags]
```

**Tag Requirements:**
- Max 63 characters
- Alphanumeric, dashes, underscores, or periods
- Begins and ends with alphanumeric
- One tag at a time

**Examples:**
```bash
orka3 node tag mini-1 jenkins
orka3 node tag mini-1 jenkins --namespace orka-test
orka3 node list mini-1 --output wide  # Verify tag
```

## orka3 node untag (Admin)

Remove a tag from a node.

**Syntax:**
```bash
orka3 node untag <NODE_NAME> <TAG> [--namespace <NS>] [flags]
```

**Examples:**
```bash
orka3 node untag mini-1 my-tag
orka3 node untag mini-1 my-tag --namespace orka-test
```

## orka3 node namespace (Admin)

Move Orka nodes across namespaces.

**Syntax:**
```bash
orka3 node namespace <NODE> [--namespace <CURRENT_NS>] <TARGET_NS> [flags]
```

**Options:**
- `-n, --namespace string` - Current namespace (default: "orka-default")

**Examples:**
```bash
orka3 node namespace mini-1 orka-test
orka3 node namespace mini-1 --namespace orka-test orka-production
orka3 node namespace mini-1 --namespace orka-production orka-default
```

# registry-commands

# OCI Registry Commands Reference

This reference provides detailed syntax and examples for OCI registry credential management in Orka3. These are admin-only operations.

## orka3 registrycredential add (alias: regcred)

Add credentials for an OCI registry server.

**Syntax:**
```bash
orka3 registrycredential add <SERVER> --username <USER> {--password <PASS>|--password-stdin} [--replace] [--allow-insecure] [--namespace <NS>] [flags]
```

**Options:**
- `-u, --username string` - (Required) Username
- `-p, --password string` - Password
- `--password-stdin` - Read password from stdin
- `--replace` - Replace existing credentials
- `--allow-insecure` - Fall back to HTTP if HTTPS unavailable
- `-n, --namespace string` - Target namespace

**Server Address Requirements:**
- Must include scheme and hostname (and optionally port)
- Examples: `https://ghcr.io`, `https://10.221.188.5:30080`

**Examples:**
```bash
orka3 regcred add https://ghcr.io --username whoami --password ghp_***
echo -n "$PASSWORD" | orka3 regcred add https://ghcr.io --username whoami --password-stdin
orka3 regcred add --allow-insecure http://10.221.188.5:30080 --username admin --password p@ssw0rd
orka3 regcred add --replace https://ghcr.io --username whoami --password ghp_***
```

## orka3 registrycredential list (alias: regcred)

List OCI registry servers with stored credentials.

**Syntax:**
```bash
orka3 registrycredential list [--namespace <NS>] [--output <FORMAT>] [flags]
```

**Options:**
- `-o, --output string` - Output format: table|wide|json
- `-n, --namespace string` - Target namespace

## orka3 registrycredential remove (alias: regcred)

Remove authentication credentials for a registry server.

**Syntax:**
```bash
orka3 registrycredential remove <SERVER> [--namespace <NS>] [flags]
```

**Options:**
- `-n, --namespace string` - Target namespace

# vm-commands

# VM Commands Reference

This reference provides detailed syntax and examples for VM-related Orka3 CLI commands.

## orka3 vm deploy

Deploy a VM with specified configuration.

**Syntax:**
```bash
orka3 vm deploy [<NAME>] --image <IMAGE> [flags]
orka3 vm deploy [<NAME>] --config <TEMPLATE> [flags]
```

**Options:**
- `-i, --image string` - (Required if no --config) Base image (local or OCI)
- `--config string` - VM configuration template
- `-c, --cpu int` - Number of CPU cores (default: 3)
- `-m, --memory float` - RAM in gigabytes
- `--node string` - Specific node for deployment
- `--tag string` - Node affinity tag
- `--tag-required` - Require tagged nodes
- `--generate-name` - Generate unique name with suffix
- `--scheduler string` - Scheduler: 'default' or 'most-allocated'
- `--metadata stringToString` - Custom metadata (key1=value1,key2=value2)
- `-p, --ports strings` - Port mapping (NODE_PORT:VM_PORT)
- `--timeout int` - Deployment timeout in minutes (default: 10)
- `-n, --namespace string` - Target namespace
- `-o, --output string` - Output format: json|wide

**Intel-only Options:**
- `--iso string` - ISO name to attach
- `--gpu` - Enable GPU passthrough (requires --disable-vnc)
- `--system-serial string` - Custom serial number
- `--disable-net-boost` - Disable network performance boost
- `--disable-vnc` - Disable VNC

**VM Name Requirements:**
- Max 63 characters (including generated suffix)
- Lowercase alphanumeric or dashes
- Starts with alphabetic, ends with alphanumeric
- Unique to namespace

**Examples:**
```bash
# Basic deployments
orka3 vm deploy --image ghcr.io/macstadium/orka-images/sonoma:latest
orka3 vm deploy my-vm --image sonoma-90gb-orka3-arm --cpu 4
orka3 vm deploy --image sonoma:latest --memory 10
orka3 vm deploy --image sonoma:latest --generate-name

# Targeted deployments
orka3 vm deploy --image sonoma:latest --node mini-arm-14
orka3 vm deploy --image sonoma:latest --tag jenkins-builds --tag-required
orka3 vm deploy --image sonoma:latest --namespace orka-test

# Advanced deployments
orka3 vm deploy --image sonoma:latest --metadata 'foo=1,baz=https://example.com'
orka3 vm deploy --image sonoma:latest --ports 9000:4000,9001:4001

# Intel-only deployments
orka3 vm deploy --image emptydisk.img --iso ventura.iso
orka3 vm deploy --image ventura.img --gpu=true --disable-vnc
orka3 vm deploy --image ventura.img --system-serial A00BC123D4

# Template deployments
orka3 vm deploy --config small-ventura-config
orka3 vm deploy my-vm --config small-ventura-config
orka3 vm deploy --config small-ventura-config --cpu 6 --memory 16
```

## orka3 vm list

Show information about VMs.

**Syntax:**
```bash
orka3 vm list [<NAME>] [--namespace <NS>] [--output <FORMAT>] [flags]
```

**Options:**
- `-o, --output string` - Output format: table|wide|json
- `-n, --namespace string` - Target namespace

**Examples:**
```bash
orka3 vm list
orka3 vm list --output wide
orka3 vm list my-vm
orka3 vm list --namespace orka-test
orka3 vm list --output wide | grep 'mini-arm-14'
```

**Note:** Stopped/suspended VMs appear as 'Running' when listed.

## orka3 vm delete

Delete specified VMs.

**Syntax:**
```bash
orka3 vm delete <NAME> [<NAME2> ...] [--namespace <NS>] [flags]
```

**CAUTION:** Cannot be undone. Unsaved/uncommitted data will be lost.

## orka3 vm save

Save a new image from a running VM.

**Syntax:**
```bash
orka3 vm save <VM_NAME> <NEW_IMAGE_NAME> [--description '<DESC>'] [--namespace <NS>] [flags]
```

**Options:**
- `-d, --description string` - Custom description for new image
- `-n, --namespace string` - Target namespace

**Notes:**
- Preserves original image
- Async operation (check with `orka3 image list <NAME>`)
- Restarts the VM

## orka3 vm commit

Update an existing image from a running VM.

**Syntax:**
```bash
orka3 vm commit <VM_NAME> [--description '<DESC>'] [--namespace <NS>] [flags]
```

**Options:**
- `-d, --description string` - New description for original image
- `-n, --namespace string` - Target namespace

**Notes:**
- Modifies original image
- Intel: image must not be in use by other VMs
- Async operation
- Restarts the VM

## orka3 vm push (Apple Silicon only)

Push VM state to an OCI-compatible registry.

**Syntax:**
```bash
orka3 vm push <VM_NAME> <IMAGE[:TAG]> [--namespace <NS>] [flags]
```

**Notes:**
- Image format: `server.com/repository/image:tag`
- Tag defaults to `latest` if not provided
- Registry credentials required in same namespace
- Async operation (check with `orka3 vm get-push-status`)

**Examples:**
```bash
orka3 vm push vm-5rjn4 ghcr.io/myorg/orka-images/base:latest
orka3 vm push vm-fxwj5 ghcr.io/myorg/orka-images/base:1.0 --namespace orka-test
```

## orka3 vm get-push-status (Apple Silicon only)

View status of image push to OCI registry.

**Syntax:**
```bash
orka3 vm get-push-status [<JOB_NAME>] [--namespace <NS>] [--output <FORMAT>] [flags]
```

**Notes:**
- Job name from push operation
- Status viewable for 1 hour after completion
- Lists all pushes if no job name provided

## orka3 vm resize

Resize the disk of a running VM (increase only).

**Syntax:**
```bash
orka3 vm resize <VM_NAME> <NEW_SIZE_GB> [--user <SSH_USER>] [--password <SSH_PASS>] [--namespace <NS>] [flags]
```

**Options:**
- `-u, --user string` - (Intel-only) SSH user for automatic repartition
- `-p, --password string` - (Intel-only) SSH password for automatic repartition
- `-n, --namespace string` - Target namespace

**Architecture Behavior:**
- **Apple Silicon**: Automatic - no additional steps needed
- **Intel**: Provide SSH credentials for automatic repartition, or manually complete

**Notes:**
- Size always in GB
- Restarts the VM
- Can only increase size

**Examples:**
```bash
orka3 vm resize my-vm 100
orka3 vm resize intel-vm 100 --user admin --password admin
```

## orka3 vm start (Intel only)

Power ON a stopped VM.

**Syntax:**
```bash
orka3 vm start <VM_NAME> [--namespace <NS>] [flags]
```

## orka3 vm stop (Intel only)

Power OFF a running VM.

**Syntax:**
```bash
orka3 vm stop <VM_NAME> [--namespace <NS>] [flags]
```

## orka3 vm suspend (Intel only)

Suspend a running VM (freezes processes).

**Syntax:**
```bash
orka3 vm suspend <VM_NAME> [--namespace <NS>] [flags]
```

## orka3 vm resume (Intel only)

Resume a suspended VM.

**Syntax:**
```bash
orka3 vm resume <VM_NAME> [--namespace <NS>] [flags]
```

## orka3 vm revert (Intel only)

Revert a VM to the latest state of its image.

**Syntax:**
```bash
orka3 vm revert <VM_NAME> [--namespace <NS>] [flags]
```

**CAUTION:** Cannot be undone. All unsaved/uncommitted data will be lost.

# vm-config-commands

# VM Configuration Commands Reference

This reference provides detailed syntax and examples for VM configuration template commands in Orka3 CLI.

## orka3 vm-config create (alias: vmc)

Create a VM configuration template.

**Syntax:**
```bash
orka3 vm-config create <NAME> [flags]
```

**Options:**
- `-i, --image string` - (Required) Base image (local or OCI)
- `-c, --cpu int` - Number of CPU cores (default: 3)
- `-m, --memory float` - RAM in gigabytes
- `--scheduler string` - Scheduler: 'default' or 'most-allocated'
- `--tag string` - Node affinity tag
- `--tag-required` - Require tagged nodes
- `--disable-vnc` - Disable VNC

**Intel-only Options:**
- `--iso string` - ISO name to attach
- `--gpu` - Enable GPU passthrough
- `--system-serial string` - Custom serial number
- `--disable-net-boost` - Disable network boost

**Config Name Requirements:**
- Max 50 characters
- Lowercase alphanumeric or dashes
- Starts with alphabetic, ends with alphanumeric
- Unique to cluster

**Examples:**
```bash
orka3 vmc create medium-ventura-vm --image 90gbventurassh.img --cpu 6
orka3 vmc create small-arm-vm -i ghcr.io/org/orka-images/orka-arm:latest --cpu 4
orka3 vmc create medium-vm --image sonoma.orkasi --memory 5
orka3 vmc create build-vm --image sonoma.orkasi --tag jenkins-builds --tag-required
```

## orka3 vm-config list (alias: vmc)

Show information about VM configurations.

**Syntax:**
```bash
orka3 vm-config list [<NAME>] [--output <FORMAT>] [flags]
```

**Options:**
- `-o, --output string` - Output format: table|wide|json

**Examples:**
```bash
orka3 vmc list
orka3 vmc list --output wide
orka3 vmc list small-ventura-vm
orka3 vmc list --output wide | grep 'user@company.com'
```

## orka3 vm-config delete (alias: vmc)

Delete VM configuration templates.

**Syntax:**
```bash
orka3 vm-config delete <NAME> [<NAME2> ...] [flags]
```

# admin-workflows

# Administrative Workflows

This guide covers namespace management, RBAC configuration, and node organization.

## Multi-Namespace Team Setup

**Set up isolated namespaces for different teams:**

```bash
# As admin:

# 1. Create namespaces for teams
orka3 namespace create orka-dev-team
orka3 namespace create orka-qa-team
orka3 namespace create orka-prod

# 2. Dedicate nodes to each namespace
# Dev team gets 2 nodes
orka3 node namespace mini-arm-1 orka-dev-team
orka3 node namespace mini-arm-2 orka-dev-team

# QA team gets 2 nodes
orka3 node namespace mini-arm-3 orka-qa-team
orka3 node namespace mini-arm-4 orka-qa-team

# Production gets 4 nodes
orka3 node namespace mini-arm-5 orka-prod
orka3 node namespace mini-arm-6 orka-prod
orka3 node namespace mini-arm-7 orka-prod
orka3 node namespace mini-arm-8 orka-prod

# 3. Grant team members access
# Dev team
orka3 rb add-subject --namespace orka-dev-team \
  --user dev1@company.com,dev2@company.com,dev3@company.com

# QA team
orka3 rb add-subject --namespace orka-qa-team \
  --user qa1@company.com,qa2@company.com

# Production (admin only, plus service accounts)
orka3 sa create sa-prod-deploy --namespace orka-prod
orka3 rb add-subject --namespace orka-prod \
  --serviceaccount orka-prod:sa-prod-deploy

# 4. Verify setup
orka3 namespace list
orka3 rb list-subjects --namespace orka-dev-team
orka3 rb list-subjects --namespace orka-qa-team
orka3 rb list-subjects --namespace orka-prod

# 5. Verify resources
orka3 node list --namespace orka-dev-team
orka3 node list --namespace orka-qa-team
orka3 node list --namespace orka-prod
```

## Node Affinity and Tagging Strategy

**Organize nodes for workload isolation:**

```bash
# 1. Tag nodes by hardware capability
orka3 node tag mac-studio-1 high-performance
orka3 node tag mac-studio-2 high-performance
orka3 node tag mini-m1-1 standard
orka3 node tag mini-m1-2 standard

# 2. Tag nodes by workload type
orka3 node tag mini-m1-3 ci-builds
orka3 node tag mini-m1-4 ci-builds
orka3 node tag mac-studio-1 rendering
orka3 node tag mac-studio-2 rendering

# 3. Create VM configs with node affinity
# Flexible affinity (will use tagged nodes if available, otherwise any node)
orka3 vmc create ci-vm \
  --image sonoma-ci \
  --cpu 4 \
  --tag ci-builds \
  --tag-required=false

# Strict affinity (ONLY uses tagged nodes)
orka3 vmc create render-vm \
  --image sonoma-render \
  --cpu 8 \
  --memory 16 \
  --tag rendering \
  --tag-required=true

# 4. Deploy and verify placement
orka3 vm deploy --config ci-vm
orka3 vm deploy --config render-vm

# 5. Check which nodes VMs landed on
orka3 vm list --output wide

# 6. View all node tags
orka3 node list --output wide | grep -E 'NAME|Tags'

# 7. Remove tags when reconfiguring
orka3 node untag mini-m1-3 ci-builds
orka3 node untag mini-m1-4 ci-builds
```

## Access Control Patterns

### Grant User Access

```bash
# Single user
orka3 rb add-subject --namespace orka-team --user user@company.com

# Multiple users
orka3 rb add-subject --namespace orka-team --user user1@company.com,user2@company.com
```

### Grant Service Account Access

```bash
# Service account from same namespace
orka3 rb add-subject --namespace orka-team --serviceaccount orka-team:sa-builds

# Service account from different namespace
orka3 rb add-subject --namespace orka-prod --serviceaccount orka-ci:sa-deploy
```

### Revoke Access

```bash
# Revoke user access
orka3 rb remove-subject --namespace orka-team --user user@company.com

# Revoke service account access
orka3 rb remove-subject --namespace orka-team --serviceaccount orka-ci:sa-deploy
```

### Audit Access

```bash
# List all subjects in namespace
orka3 rb list-subjects --namespace orka-team

# Filter by type
orka3 rb list-subjects --namespace orka-team | grep 'User'
orka3 rb list-subjects --namespace orka-team | grep 'ServiceAccount'
```

## Namespace Lifecycle

### Creating Namespaces

```bash
# Standard namespace for VMs
orka3 namespace create orka-newteam

# Namespace for custom Kubernetes pods (no VMs)
orka3 namespace create orka-custom --enable-custom-pods
```

### Deleting Namespaces

Prerequisites before deletion:
1. Delete all VMs in namespace
2. Move all nodes to another namespace

```bash
# Check what's in namespace
orka3 vm list --namespace orka-oldteam
orka3 node list --namespace orka-oldteam

# Clean up VMs
orka3 vm delete <VM1> <VM2> --namespace orka-oldteam

# Move nodes back to default
orka3 node namespace mini-arm-1 orka-default --namespace orka-oldteam

# Delete namespace
orka3 namespace delete orka-oldteam
```

# cicd-workflows

# CI/CD Pipeline Workflows

This guide covers setting up service accounts and CI/CD pipelines with Orka3.

## CI/CD Pipeline Setup

**Set up service account for Jenkins/GitHub Actions/GitLab:**

```bash
# 1. Create service account (admin)
orka3 sa create sa-ci-pipeline

# 2. Get long-lived token (1 year)
orka3 sa token sa-ci-pipeline

# 3. (Optional) Create namespace for CI workloads
orka3 namespace create orka-ci

# 4. Move dedicated nodes to CI namespace
orka3 node namespace mini-arm-10 orka-ci
orka3 node namespace mini-arm-11 orka-ci

# 5. Grant service account access to CI namespace
orka3 rb add-subject --namespace orka-ci --serviceaccount orka-default:sa-ci-pipeline

# 6. Create VM config for consistent builds
orka3 vmc create ci-build \
  --image ghcr.io/macstadium/orka-images/sonoma:latest \
  --cpu 4 \
  --memory 8 \
  --namespace orka-ci

# 7. Tag nodes for specific workload types (optional)
orka3 node tag mini-arm-10 fast-builds --namespace orka-ci
orka3 node tag mini-arm-11 integration-tests --namespace orka-ci

# 8. Create tagged VM configs
orka3 vmc create fast-build \
  --image sonoma:latest \
  --cpu 6 \
  --tag fast-builds \
  --tag-required \
  --namespace orka-ci
```

## CI/CD Pipeline Commands

**In your CI script:**

```bash
# Authenticate with service account token
orka3 user set-token $SA_TOKEN

# Deploy VM for build
VM_NAME=$(orka3 vm deploy --config ci-build --namespace orka-ci --generate-name -o json | jq -r '.name')

# Get VM connection info
VM_INFO=$(orka3 vm list $VM_NAME --namespace orka-ci -o json)
VM_IP=$(echo $VM_INFO | jq -r '.items[0].ip')
VM_SSH_PORT=$(echo $VM_INFO | jq -r '.items[0].ssh')

# Run your build (via SSH)
ssh -p $VM_SSH_PORT admin@$VM_IP 'cd /path/to/project && make test'

# Clean up
orka3 vm delete $VM_NAME --namespace orka-ci
```

## Service Account Token Options

```bash
# Default: 1 year expiration
orka3 sa token sa-jenkins

# Custom duration
orka3 sa token sa-jenkins --duration 1h
orka3 sa token sa-jenkins --duration 24h
orka3 sa token sa-jenkins --duration 8760h  # 1 year

# No expiration (for long-lived automation)
orka3 sa token sa-jenkins --no-expiration
```

## Best Practices for CI/CD

1. **Use service accounts, not user credentials** - User tokens expire in 1 hour
2. **Create dedicated namespaces** - Isolate CI workloads from other environments
3. **Use VM configs** - Ensure consistent build environments
4. **Tag nodes** - Route different workloads to appropriate hardware
5. **Generate unique names** - Use `--generate-name` to avoid conflicts
6. **Clean up after builds** - Always delete VMs when done
7. **Cache images** - Pre-cache images on CI nodes for faster deployments

## Multiple Pipeline Setup

For organizations with multiple CI/CD pipelines:

```bash
# Create service accounts per pipeline
orka3 sa create sa-jenkins --namespace orka-ci
orka3 sa create sa-github-actions --namespace orka-ci
orka3 sa create sa-gitlab-runner --namespace orka-ci

# Grant access to each
orka3 rb add-subject --namespace orka-ci --serviceaccount orka-ci:sa-jenkins
orka3 rb add-subject --namespace orka-ci --serviceaccount orka-ci:sa-github-actions
orka3 rb add-subject --namespace orka-ci --serviceaccount orka-ci:sa-gitlab-runner

# Create different VM configs per workload type
orka3 vmc create unit-tests --image sonoma:latest --cpu 4 --memory 8
orka3 vmc create integration-tests --image sonoma:latest --cpu 6 --memory 12
orka3 vmc create ui-tests --image sonoma:latest --cpu 4 --memory 16
```

# getting-started

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

# image-workflows

# Image Management Workflows

This guide covers custom image preparation, caching, and OCI registry integration.

## Custom Image Preparation Workflow

**Create a custom configured image from a base image:**

```bash
# 1. Deploy base VM
orka3 vm deploy base-config --image ghcr.io/macstadium/orka-images/sonoma:latest

# 2. Get connection info
orka3 vm list base-config --output wide

# 3. Connect via Screen Sharing
# vnc://<VM_IP>:<Screenshare_port>
# Credentials: admin/admin

# 4. On the VM:
#    - Change password (System Settings > Users & Groups)
#    - Install software (brew install xcode-select git node)
#    - Apply OS updates
#    - Configure settings
#    - Install/upgrade Orka VM Tools:
#      brew install orka-vm-tools  # or brew upgrade orka-vm-tools

# 5. Save as new image (preserves original)
orka3 vm save base-config my-configured-sonoma

# OR commit to original image (modifies original)
orka3 vm commit base-config --description 'Configured with build tools'

# 6. Wait for async operation to complete
orka3 image list my-configured-sonoma --output wide

# 7. Clean up base VM
orka3 vm delete base-config

# 8. Test the new image
orka3 vm deploy test-vm --image my-configured-sonoma

# 9. Verify configuration persists
# Connect via Screen Sharing and verify changes

# 10. Clean up test VM
orka3 vm delete test-vm

# 11. Deploy production VMs with configured image
orka3 vm deploy prod-vm-1 --image my-configured-sonoma --cpu 6 --memory 12
```

## Image Caching for Fast Deployments (Apple Silicon)

**Pre-cache images on nodes for consistent deployment times:**

```bash
# 1. Check current node image cache
orka3 ic list

# 2. Cache base images on all nodes
orka3 ic add ghcr.io/macstadium/orka-images/sonoma:latest --all

# 3. Check caching progress
orka3 ic info ghcr.io/macstadium/orka-images/sonoma:latest

# Wait until status shows 'ready' on all nodes

# 4. Cache additional images on specific nodes
orka3 ic add my-configured-image --nodes mini-arm-1,mini-arm-2,mini-arm-3

# 5. Cache by node tags
# First, tag nodes
orka3 node tag mini-arm-4 xcode-15
orka3 node tag mini-arm-5 xcode-15

# Then cache image on tagged nodes
orka3 ic add xcode-15-image --tags xcode-15

# 6. Verify all images are cached
orka3 ic list --output wide

# 7. Deploy VMs (will use cached images - fast!)
orka3 vm deploy --image ghcr.io/macstadium/orka-images/sonoma:latest
```

## OCI Registry Integration Workflow

**Set up and use private OCI registry for images:**

```bash
# As admin:

# 1. Add registry credentials
orka3 regcred add https://ghcr.io \
  --username your-username \
  --password ghp_your_github_token

# OR read password securely from file
orka3 regcred add https://ghcr.io \
  --username your-username \
  --password-stdin < token.txt

# 2. Verify credentials
orka3 regcred list

# 3. Deploy VM from OCI image
orka3 vm deploy --image ghcr.io/your-org/orka-images/custom-sonoma:v1.2

# 4. Customize VM (connect via Screen Sharing)
# Install software, configure settings, etc.

# 5. Push customized VM back to registry (Apple Silicon only)
orka3 vm push <VM_NAME> ghcr.io/your-org/orka-images/custom-sonoma:v1.3

# 6. Check push status
orka3 vm get-push-status

# 7. Deploy new VMs from updated image
orka3 vm deploy --image ghcr.io/your-org/orka-images/custom-sonoma:v1.3

# 8. (Optional) Cache OCI images on nodes
orka3 ic add ghcr.io/your-org/orka-images/custom-sonoma:v1.3 --all
```

## VM save vs. VM commit

| Operation | Behavior | Use Case |
|-----------|----------|----------|
| `vm save` | Creates new image, preserves original | Creating variants of a base image |
| `vm commit` | Updates original image | Iterative development on single image |

## Image Management Best Practices

1. **Test images before deployment** - Always verify new images work correctly
2. **Use descriptive names** - Include version or date in image names
3. **Cache images for CI/CD** - Pre-cache on dedicated CI nodes
4. **Use OCI registries** - Modern approach for image distribution
5. **Document image configurations** - Track what's installed in each image
6. **Clean up unused images** - Regularly remove old/unused images

# migration-workflows

# Migration and Backup Workflows

This guide covers Intel to Apple Silicon migration and disaster recovery strategies.

## Migration from Intel to Apple Silicon

**Plan and execute architecture migration:**

```bash
# 1. Audit current Intel VMs
orka3 vm list --output wide | grep 'amd64'

# 2. Identify Intel-specific features in use
# - GPU passthrough
# - Custom serial numbers
# - ISO installations
# - Power operations (start/stop/suspend/resume)

# 3. For each Intel VM:
#    a. Document configuration
orka3 vm list <INTEL_VM> --output wide

#    b. Create ARM equivalent image
#       Deploy Intel VM, configure, save as new image
orka3 vm save <INTEL_VM> intel-configured-image

#    c. Manually recreate on ARM (no direct conversion)
#       Deploy ARM VM, manually configure with same settings
orka3 vm deploy arm-vm --image ghcr.io/macstadium/orka-images/sonoma:latest

#    d. Test ARM VM thoroughly
#    e. Create VM config for ARM version
orka3 vmc create arm-version \
  --image arm-configured-image \
  --cpu 4 \
  --memory 8

# 4. Update CI/CD pipelines to use ARM configs
# 5. Monitor performance and adjust resources as needed
# 6. Decommission Intel VMs after validation
```

## Intel vs. Apple Silicon Feature Comparison

| Feature | Intel (amd64) | Apple Silicon (arm64) |
|---------|---------------|----------------------|
| Power operations | start, stop, suspend, resume, revert | Not available |
| GPU passthrough | Supported | Not supported |
| ISO installation | Supported | Not supported |
| Custom serial | Supported | Not supported |
| OCI registry push | Not supported | Supported |
| Image caching | Not supported | Supported |
| Disk resize | Requires SSH credentials | Automatic |

## Disaster Recovery and Backup Strategy

**Back up images and configurations:**

```bash
# 1. List all images and VM configs
orka3 image list -o json > images-backup-$(date +%Y%m%d).json
orka3 vmc list -o json > vm-configs-backup-$(date +%Y%m%d).json

# 2. For Apple Silicon: Push important images to OCI registry
orka3 regcred add https://ghcr.io --username backup-user --password $TOKEN

# Deploy VM from image, then push to registry
orka3 vm deploy backup-vm --image important-image
orka3 vm push backup-vm ghcr.io/company/backups/important-image:$(date +%Y%m%d)
orka3 vm delete backup-vm

# 3. For Intel: Copy images to another Orka cluster
# (Use remote-image commands or manual file transfer)

# 4. Document namespace configurations
orka3 namespace list -o json > namespaces-backup-$(date +%Y%m%d).json
orka3 rb list-subjects --namespace orka-default -o json > rbac-default-$(date +%Y%m%d).json
orka3 rb list-subjects --namespace orka-prod -o json > rbac-prod-$(date +%Y%m%d).json

# 5. Document node assignments
orka3 node list --output wide > nodes-layout-$(date +%Y%m%d).txt
```

## Image Backup to OCI Registry (Apple Silicon)

```bash
# 1. Ensure registry credentials are configured
orka3 regcred list

# 2. For each important image:
#    a. Deploy a VM from the image
orka3 vm deploy backup-vm --image <IMAGE_NAME>

#    b. Push to registry with date tag
orka3 vm push backup-vm ghcr.io/company/backups/<IMAGE_NAME>:$(date +%Y%m%d)

#    c. Wait for push to complete
orka3 vm get-push-status

#    d. Clean up backup VM
orka3 vm delete backup-vm

# 3. Verify backup in registry
# Use external registry tools or GitHub UI to confirm
```

## Recovery Procedures

### Restore from OCI Registry

```bash
# 1. Add registry credentials (if not already configured)
orka3 regcred add https://ghcr.io --username <USER> --password <TOKEN>

# 2. Deploy VM from backed-up image
orka3 vm deploy restored-vm --image ghcr.io/company/backups/<IMAGE_NAME>:<DATE>

# 3. Save as local image (optional)
orka3 vm save restored-vm <LOCAL_IMAGE_NAME>

# 4. Clean up
orka3 vm delete restored-vm
```

### Recreate Namespace Configuration

```bash
# Using saved backup files:

# 1. Create namespace
orka3 namespace create <NAMESPACE_NAME>

# 2. Move nodes (from saved node layout)
orka3 node namespace <NODE> <NAMESPACE_NAME>

# 3. Restore access (from saved RBAC backup)
# Review rbac-*.json files and recreate rolebindings
orka3 rb add-subject --namespace <NS> --user <EMAIL>
orka3 rb add-subject --namespace <NS> --serviceaccount <SA_NS>:<SA_NAME>
```

## Migration Checklist

- [ ] Document all current Intel VM configurations
- [ ] Identify Intel-only features in use
- [ ] Plan workarounds for unavailable features
- [ ] Create ARM-compatible images
- [ ] Test ARM VMs thoroughly
- [ ] Update CI/CD pipelines
- [ ] Train team on ARM-specific workflows
- [ ] Set migration date and cutover plan
- [ ] Back up all Intel images before decommissioning
- [ ] Monitor ARM VMs post-migration

# scaling-workflows

# Scaling and Resource Optimization Workflows

This guide covers VM scaling, disk management, and resource optimization.

## Scaling VMs for Load Testing

**Deploy multiple VMs for parallel workloads:**

```bash
# 1. Create VM config for load testing
orka3 vmc create load-test-vm \
  --image sonoma-configured \
  --cpu 4 \
  --memory 8 \
  --tag load-testing \
  --tag-required=false

# 2. Tag nodes that can handle load testing
orka3 node tag mini-arm-1 load-testing
orka3 node tag mini-arm-2 load-testing
orka3 node tag mini-arm-3 load-testing

# 3. Deploy multiple VMs with generated names
for i in {1..10}; do
  orka3 vm deploy load-test --config load-test-vm --generate-name
done

# 4. List all VMs
orka3 vm list --output wide

# 5. Get VM IPs for load testing script
orka3 vm list -o json | jq -r '.items[] | select(.name | startswith("load-test")) | .ip'

# 6. After load testing, clean up all VMs
orka3 vm list -o json | jq -r '.items[] | select(.name | startswith("load-test")) | .name' | \
  while read vm; do orka3 vm delete $vm; done
```

## VM Disk Management Workflow

**Resize VM disks and manage storage:**

### Apple Silicon - Simple resize

```bash
# 1. Deploy VM
orka3 vm deploy my-vm --image sonoma-90gb --cpu 4

# 2. Resize to 150GB (automatic)
orka3 vm resize my-vm 150

# 3. Verify resize (VM will restart)
orka3 vm list my-vm --output wide
```

### Intel - Resize with repartition

```bash
# 1. Deploy VM
orka3 vm deploy intel-vm --image ventura-90gb.img --cpu 6

# 2. Resize with automatic repartition (requires SSH access)
orka3 vm resize intel-vm 150 --user admin --password YourPassword

# OR resize without automatic repartition
orka3 vm resize intel-vm 150
# Then manually repartition via Disk Utility on the VM

# 3. Save resized image for future use
orka3 vm save intel-vm ventura-150gb.img

# 4. Clean up
orka3 vm delete intel-vm

# 5. Deploy new VMs with larger disk
orka3 vm deploy --image ventura-150gb.img
```

## Resource Optimization

**Monitor and optimize cluster resource usage:**

```bash
# 1. Check overall cluster resources
orka3 node list --output wide

# 2. Identify underutilized nodes
# Look for nodes with high available CPU/memory

# 3. Check VM distribution
orka3 vm list --output wide | awk '{print $NF}' | sort | uniq -c

# 4. Identify over-provisioned VMs
orka3 vm list --output wide | sort -k3 -nr  # Sort by CPU
orka3 vm list --output wide | sort -k4 -nr  # Sort by memory

# 5. Right-size VM configs
# Create smaller configs for less demanding workloads
orka3 vmc create small-vm --image sonoma --cpu 2 --memory 4
orka3 vmc create medium-vm --image sonoma --cpu 4 --memory 8
orka3 vmc create large-vm --image sonoma --cpu 6 --memory 12

# 6. Use scheduler for better packing
orka3 vmc create packed-vm \
  --image sonoma \
  --cpu 4 \
  --scheduler most-allocated

# 7. Clean up unused images
orka3 image list --output wide
# Identify old/unused images
orka3 image delete <OLD_IMAGE>

# 8. Clean up unused VM configs
orka3 vmc list --output wide
# Identify obsolete configs
orka3 vmc delete <OLD_CONFIG>
```

## Scheduler Options

| Scheduler | Behavior | Use Case |
|-----------|----------|----------|
| `default` | Spreads VMs across nodes | General workloads, high availability |
| `most-allocated` | Packs VMs on fewest nodes | Cost optimization, power savings |

```bash
# Spread VMs (default)
orka3 vmc create spread-vm --image sonoma --cpu 4 --scheduler default

# Pack VMs
orka3 vmc create packed-vm --image sonoma --cpu 4 --scheduler most-allocated
```

## Parallel VM Deployment Patterns

### Deploy Multiple VMs Sequentially

```bash
for i in {1..5}; do
  orka3 vm deploy build-$i --image sonoma:latest --cpu 4
done
```

### Deploy Multiple VMs with Generated Names

```bash
for i in {1..5}; do
  orka3 vm deploy build --image sonoma:latest --cpu 4 --generate-name
done
```

### Get All VM IPs for Scripting

```bash
# All VMs
orka3 vm list -o json | jq -r '.items[].ip'

# Filtered by name prefix
orka3 vm list -o json | jq -r '.items[] | select(.name | startswith("build")) | .ip'

# With name and IP
orka3 vm list -o json | jq -r '.items[] | "\(.name) \(.ip)"'
```

# auth-issues

# Authentication Troubleshooting

This guide covers common authentication and access control issues with the Orka3 CLI.

## Problem: "Authentication token expired"

**Symptoms:**
- Commands fail with authentication error
- "Token expired" message

**Solutions:**
```bash
# 1. Re-authenticate
orka3 login

# 2. For service accounts, generate new token
orka3 sa token <SERVICE_ACCOUNT_NAME>

# 3. Set new token
orka3 user set-token <NEW_TOKEN>

# 4. Verify authentication
orka3 node list
```

**Prevention:**
- User tokens expire after 1 hour
- Service account tokens expire after their configured duration (default: 1 year)
- For long-running automation, use service accounts with long-lived tokens

## Problem: "Unable to connect to Orka cluster"

**Symptoms:**
- Connection timeout
- "Connection refused" errors
- "No route to host"

**Diagnosis:**
```bash
# 1. Check CLI configuration
orka3 config view

# 2. Verify VPN connection
# Ensure you're connected to cluster VPN

# 3. Test connectivity
ping <ORKA_SERVICE_URL_WITHOUT_HTTP>

# 4. Check firewall rules
```

**Solutions:**
```bash
# 1. Verify API URL is correct
orka3 config set --api-url http://10.221.188.20  # Orka 2.1+
# OR
orka3 config set --api-url http://10.221.188.100  # Pre-2.1
# OR
orka3 config set --api-url https://company.orka.app  # Domain

# 2. Ensure VPN is connected
# Check your VPN client

# 3. Contact MacStadium support if issues persist
```

## Problem: "Forbidden" or "Insufficient permissions"

**Symptoms:**
- 403 Forbidden errors
- "User does not have permission" messages

**Diagnosis:**
```bash
# Check which namespaces you have access to
orka3 namespace list

# Try operations in orka-default (all users have access)
orka3 vm list --namespace orka-default
```

**Solutions:**
```bash
# Ask admin to grant access to required namespace
# Admin runs:
orka3 rb add-subject --namespace <TARGET_NAMESPACE> --user <YOUR_EMAIL>

# For service accounts:
orka3 rb add-subject --namespace <TARGET_NAMESPACE> \
  --serviceaccount <SA_NAMESPACE>:<SA_NAME>
```

## Problem: Cannot create namespace / admin commands fail

**Symptoms:**
- "Requires administrative privileges"
- "Forbidden" on admin operations

**Cause:**
Only admin users can perform certain operations:
- Create/delete namespaces
- Create/delete service accounts
- Manage rolebindings
- Tag/untag nodes
- Move nodes between namespaces
- Manage OCI registry credentials

**Solutions:**
```bash
# Contact your Orka cluster admin
# Or contact MacStadium to request admin privileges

# Verify your role:
orka3 login  # Check if you have admin access
orka3 namespace list  # Admins can see all namespaces
```

## Problem: Service account token not working

**Symptoms:**
- "Invalid token"
- "Token not found"

**Diagnosis:**
```bash
# Check if service account exists
orka3 sa list --namespace <SA_NAMESPACE>

# Verify token hasn't expired
# (Check when token was generated)
```

**Solutions:**
```bash
# Generate new token
orka3 sa token <SERVICE_ACCOUNT_NAME> --namespace <SA_NAMESPACE>

# For automation, use no-expiration tokens
orka3 sa token <SA_NAME> --no-expiration

# If service account was deleted, create new one
orka3 sa create <SA_NAME> --namespace <NAMESPACE>
orka3 sa token <SA_NAME> --namespace <NAMESPACE>
```

## Token Expiration Reference

| Token Type | Default Expiration | Configurable |
|------------|-------------------|--------------|
| User login | 1 hour | No |
| Service account | 1 year (8760h) | Yes |
| Service account (no expiration) | Never | Yes |

## Best Practices for Authentication

1. **Use service accounts for automation** - Never use user credentials in CI/CD
2. **Set appropriate token durations** - Balance security vs. convenience
3. **Regularly rotate tokens** - Even long-lived tokens should be rotated periodically
4. **Use no-expiration tokens carefully** - Only for trusted, long-running automation
5. **Document service account purposes** - Track which SA is used where

# deployment-issues

# VM Deployment Troubleshooting

This guide covers common VM deployment issues with the Orka3 CLI.

## Problem: VM deployment fails with "Insufficient resources"

**Symptoms:**
- "Not enough CPU available"
- "Not enough memory available"
- Deployment times out

**Diagnosis:**
```bash
# 1. Check node resources
orka3 node list --output wide

# Look for available CPU and memory

# 2. Check current VM usage
orka3 vm list --output wide

# 3. Check if namespace has any nodes
orka3 node list --namespace <YOUR_NAMESPACE>
```

**Solutions:**
```bash
# Option 1: Reduce VM resource requirements
orka3 vm deploy --image <IMAGE> --cpu 3 --memory 6  # Smaller resources

# Option 2: Deploy to specific node with resources
orka3 node list --output wide  # Find node with resources
orka3 vm deploy --image <IMAGE> --node <NODE_WITH_RESOURCES>

# Option 3: Remove tag-required if using tagged deployment
orka3 vm deploy --image <IMAGE> --tag <TAG> --tag-required=false

# Option 4: Wait for resources to free up
orka3 vm delete <UNUSED_VM>  # Clean up unused VMs

# Option 5: Ask admin to add more nodes to namespace
# Admin runs:
orka3 node namespace <ADDITIONAL_NODE> <YOUR_NAMESPACE>
```

## Problem: VM deployment succeeds but VM is unresponsive

**Symptoms:**
- VM appears as "Running"
- Cannot connect via Screen Sharing or SSH
- Timeout connecting

**Diagnosis:**
```bash
# 1. Check VM status
orka3 vm list <VM_NAME> --output wide

# 2. Verify IP and ports are assigned
# Look for IP address, SSH port, Screen Sharing port

# 3. Check if this is an Intel VM that needs power on
# Intel VMs may need explicit start command
```

**Solutions:**
```bash
# For Intel VMs - try power operations
orka3 vm start <VM_NAME>

# For Apple Silicon VMs - wait a few minutes for boot
# macOS takes time to boot, especially on first launch

# Check if Screen Sharing is enabled on the VM
# Some images require manual enablement

# Verify image has connectivity tools installed
# MacStadium base images (ghcr.io/macstadium/orka-images/*)
# come pre-configured with SSH and Screen Sharing

# If VM is still unresponsive:
orka3 vm delete <VM_NAME>
orka3 vm deploy --image <VERIFIED_IMAGE>  # Use known-good image
```

## Problem: VM deployment fails with "Image not found"

**Symptoms:**
- "Image <n> not found"
- "No such image"

**Diagnosis:**
```bash
# 1. List available local images
orka3 image list

# 2. Check if it's an OCI image
orka3 ic list  # Check cached OCI images

# 3. Verify image name spelling
```

**Solutions:**
```bash
# For local images - verify exact name
orka3 image list | grep <IMAGE_PATTERN>

# For OCI images - ensure full path with registry
orka3 vm deploy --image ghcr.io/macstadium/orka-images/sonoma:latest

# Check if image needs to be cached (Apple Silicon)
orka3 ic add <OCI_IMAGE> --all
orka3 ic info <OCI_IMAGE>  # Wait for 'ready' status

# For Intel - check if deprecated remote-image command was used
# Use OCI registries instead
```

## Problem: VM name already exists

**Symptoms:**
- "VM with name <n> already exists"
- Name conflict error

**Solutions:**
```bash
# Option 1: Use different name
orka3 vm deploy my-vm-2 --image <IMAGE>

# Option 2: Use auto-generated name
orka3 vm deploy --image <IMAGE>  # Random name

# Option 3: Use generate-name for unique suffix
orka3 vm deploy my-vm --image <IMAGE> --generate-name

# Option 4: Delete existing VM if no longer needed
orka3 vm list <VM_NAME>  # Verify it exists
orka3 vm delete <VM_NAME>
orka3 vm deploy <VM_NAME> --image <IMAGE>
```

## Problem: "Namespace has no nodes"

**Symptoms:**
- Cannot deploy VMs in namespace
- "No nodes available in namespace"

**Diagnosis:**
```bash
# Check nodes in namespace
orka3 node list --namespace <NAMESPACE>
```

**Solutions:**
```bash
# Ask admin to move nodes to namespace
# Admin runs:
orka3 node namespace <NODE_NAME> <TARGET_NAMESPACE>

# Verify nodes appear
orka3 node list --namespace <TARGET_NAMESPACE>
```

## Problem: "Tag required but no tagged nodes available"

**Symptoms:**
- Deployment fails with tag requirement error

**Solutions:**
```bash
# Check if tagged nodes exist
orka3 node list --output wide | grep <TAG>

# Option 1: Ask admin to tag nodes
orka3 node tag <NODE> <TAG>

# Option 2: Deploy without strict tag requirement
orka3 vm deploy --image <IMAGE> --tag <TAG> --tag-required=false

# Option 3: Deploy without tag
orka3 vm deploy --image <IMAGE>
```

## Troubleshooting Deployment Issues - Debug Workflow

```bash
# 1. Check node resources
orka3 node list --output wide

# Look for:
# - Available CPU/memory
# - Node status
# - Existing VM count

# 2. Check if image exists and is ready
orka3 image list <IMAGE_NAME> --output wide

# For OCI images, verify caching status
orka3 ic info <OCI_IMAGE>

# 3. Verify namespace has resources
orka3 node list --namespace <YOUR_NAMESPACE>

# 4. Check for VM name conflicts
orka3 vm list | grep <VM_NAME>

# 5. Try deployment with longer timeout
orka3 vm deploy --image <IMAGE> --timeout 20

# 6. Try deployment on specific node
orka3 vm deploy --image <IMAGE> --node <NODE_NAME>

# 7. Check if VM config exists
orka3 vmc list <CONFIG_NAME> --output wide

# 8. If tag-required is set, verify tagged nodes exist
orka3 node list --output wide | grep <TAG>

# 9. Try with JSON output for detailed error messages
orka3 vm deploy --image <IMAGE> -o json
```

# image-issues

# Image Management Troubleshooting

This guide covers common image-related issues with the Orka3 CLI.

## Problem: Async image operations stuck in progress

**Symptoms:**
- `orka3 image list` shows image but with errors
- Image save/commit/copy not completing
- "Operation in progress" for extended time

**Diagnosis:**
```bash
# Check image status with extended output
orka3 image list <IMAGE_NAME> --output wide

# Look for error messages or status indicators
```

**Solutions:**
```bash
# 1. Wait longer - large images take time
# 90GB+ images can take 10-30+ minutes

# 2. If stuck for hours, contact MacStadium support

# 3. For save/commit operations - ensure source VM is stable
orka3 vm list <SOURCE_VM> --output wide

# 4. Avoid concurrent operations on same image
# Wait for one operation to complete before starting another
```

## Problem: Cannot delete image (in use)

**Symptoms:**
- "Image is in use by VM"
- "Cannot delete image"

**Diagnosis:**
```bash
# Find VMs using the image
orka3 vm list --output wide | grep <IMAGE_NAME>

# Find VM configs using the image
orka3 vmc list --output wide | grep <IMAGE_NAME>
```

**Solutions:**
```bash
# Option 1: Delete VMs using the image
orka3 vm delete <VM_NAME>

# Option 2: Delete or update VM configs
orka3 vmc delete <CONFIG_NAME>
# OR update config to use different image

# Then try deletion again
orka3 image delete <IMAGE_NAME>

# For Intel: Ensure image is not in use by ANY VM
# For Apple Silicon: Image can be deleted if only used by one VM
```

## Problem: Image cache not working (Apple Silicon)

**Symptoms:**
- `imagecache add` succeeds but deployments still slow
- `imagecache info` shows "not ready" indefinitely

**Diagnosis:**
```bash
# Check caching status
orka3 ic info <IMAGE>

# Verify nodes have the image cached
orka3 ic list --output wide
```

**Solutions:**
```bash
# 1. Wait for caching to complete (can take time for large images)
watch -n 30 'orka3 ic info <IMAGE>'

# 2. Verify registry credentials exist for OCI images
orka3 regcred list

# For private registries:
orka3 regcred add <REGISTRY_URL> --username <USER> --password <TOKEN>

# 3. Try caching on specific nodes
orka3 ic add <IMAGE> --nodes <NODE_NAME>

# 4. Check node storage capacity
orka3 node list --output wide

# 5. If cache fails persistently, contact MacStadium support
```

## Problem: "Invalid image format"

**Cause:** Incorrect OCI image path

**Solution:**
```bash
# Use full OCI path with registry
orka3 vm deploy --image ghcr.io/org/repo/image:tag

# Verify registry credentials exist
orka3 regcred list
```

## Problem: Image push fails (Apple Silicon)

**Symptoms:**
- `orka3 vm push` command fails
- Push job stuck or errored

**Diagnosis:**
```bash
# Check push status
orka3 vm get-push-status

# List all push jobs
orka3 vm get-push-status --output wide
```

**Solutions:**
```bash
# 1. Verify registry credentials
orka3 regcred list

# 2. Ensure credentials are in the same namespace as the VM
orka3 regcred add <REGISTRY_URL> --username <USER> --password <TOKEN> --namespace <VM_NAMESPACE>

# 3. Verify image format is correct
# Format: server.com/repository/image:tag
orka3 vm push <VM_NAME> ghcr.io/org/repo/image:tag

# 4. Check VM is running and stable
orka3 vm list <VM_NAME> --output wide

# 5. Try with different tag
orka3 vm push <VM_NAME> ghcr.io/org/repo/image:new-tag
```

## Problem: Image copy operation slow or failing

**Symptoms:**
- `orka3 image copy` taking very long
- Copy operation stuck

**Solutions:**
```bash
# 1. Check image size (large images take longer)
orka3 image list <SOURCE_IMAGE> --output wide

# 2. Monitor copy progress
orka3 image list <DESTINATION_IMAGE> --output wide

# 3. Avoid starting multiple copy operations simultaneously

# 4. For very large images, expect 30+ minutes
```

## Image Operation Timing Reference

| Operation | Typical Duration | Factors |
|-----------|-----------------|---------|
| image list | Instant | - |
| image copy | 5-30+ minutes | Image size |
| image delete | Instant | - |
| vm save | 5-30+ minutes | Image size, VM disk usage |
| vm commit | 5-30+ minutes | Image size, VM disk usage |
| vm push | 10-60+ minutes | Image size, network speed |
| imagecache add | 5-30+ minutes | Image size, number of nodes |

## Best Practices for Image Operations

1. **Check status of async operations** - Don't assume completion
2. **Avoid concurrent operations** - One operation per image at a time
3. **Use descriptive names** - Include version or date in names
4. **Test images before deployment** - Verify with single VM first
5. **Clean up unused images** - Regularly remove old images
6. **Cache images before mass deployment** - Improves consistency

# network-issues

# Network and Connectivity Troubleshooting

This guide covers common network and connectivity issues with Orka3 VMs.

## Problem: Cannot connect to VM via Screen Sharing

**Symptoms:**
- Connection timeout
- "Connection refused"
- Authentication fails

**Diagnosis:**
```bash
# 1. Get VM connection info
orka3 vm list <VM_NAME> --output wide

# Note the IP and Screenshare port

# 2. Verify VM is running
# Intel VMs may need explicit start

# 3. Check if it's a fresh OS install
# Screen Sharing may not be enabled by default
```

**Solutions:**
```bash
# 1. Ensure you're using the correct format
# vnc://<VM_IP>:<Screenshare_port>

# 2. For Intel VMs - ensure VM is powered on
orka3 vm start <VM_NAME>

# 3. Try SSH first if available
ssh -p <SSH_PORT> admin@<VM_IP>

# Then enable Screen Sharing from command line:
sudo /System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart \
  -activate -configure -access -on \
  -restart -agent -privs -all

# 4. Use MacStadium base images which have Screen Sharing pre-enabled
orka3 vm deploy --image ghcr.io/macstadium/orka-images/sonoma:latest

# 5. Wait longer - VM may still be booting
# First boot can take 5-10 minutes
```

## Problem: Cannot connect via SSH

**Symptoms:**
- SSH connection timeout
- "Connection refused" on SSH port
- Authentication failures

**Diagnosis:**
```bash
# 1. Get VM connection info
orka3 vm list <VM_NAME> --output wide

# Note the IP and SSH port

# 2. Verify SSH is listening
# Connect via Screen Sharing and check System Settings > Sharing > Remote Login
```

**Solutions:**
```bash
# 1. Use correct port (not 22)
ssh -p <SSH_PORT> admin@<VM_IP>

# 2. If SSH is disabled, enable via Screen Sharing:
# System Settings > Sharing > Remote Login > Enable

# 3. Or enable via command line (if you have another way in):
sudo systemsetup -setremotelogin on

# 4. Use MacStadium base images (SSH pre-enabled)
orka3 vm deploy --image ghcr.io/macstadium/orka-images/sonoma:latest

# 5. Check firewall on VM
# System Settings > Network > Firewall
```

## Problem: Port conflicts

**Symptoms:**
- "Port already in use"
- Custom port mapping fails

**Diagnosis:**
```bash
# Check which ports are in use
orka3 vm list --output wide | grep <NODE_NAME>
```

**Solutions:**
```bash
# Let Orka assign ports automatically (recommended)
orka3 vm deploy --image <IMAGE>  # No --ports flag

# Or specify different available ports
orka3 vm deploy --image <IMAGE> --ports 9100:4000,9101:5000
```

## Problem: VM is slow/unresponsive during use

**Symptoms:**
- Laggy Screen Sharing
- Slow application performance
- Builds taking too long

**Diagnosis:**
```bash
# 1. Check VM resource allocation
orka3 vm list <VM_NAME> --output wide

# Look at CPU and memory allocated

# 2. Check node load
orka3 node list --output wide

# Look at available resources on host node

# 3. Check if too many VMs on one node
orka3 vm list --output wide | awk '{print $NF}' | sort | uniq -c
```

**Solutions:**
```bash
# Option 1: Increase VM resources
# Create new config with more resources
orka3 vmc create larger-vm --image <IMAGE> --cpu 6 --memory 16

# Delete old VM and redeploy
orka3 vm delete <VM_NAME>
orka3 vm deploy <VM_NAME> --config larger-vm

# Option 2: Reduce load on node
# Delete unnecessary VMs
orka3 vm delete <UNUSED_VM>

# Option 3: Use node affinity to spread VMs
# Tag less loaded nodes
orka3 node tag <UNDERUTILIZED_NODE> low-load

# Deploy new VMs to those nodes
orka3 vm deploy --image <IMAGE> --tag low-load

# Option 4: Use most-allocated scheduler for better packing
orka3 vmc create packed-vm --image <IMAGE> --scheduler most-allocated
```

## Problem: VM deployments are very slow

**Symptoms:**
- Deployments take 15+ minutes
- Inconsistent deployment times
- Timeout errors

**Diagnosis:**
```bash
# 1. Check if images are cached (Apple Silicon)
orka3 ic list

# 2. Check node load
orka3 node list --output wide

# 3. Verify image size
orka3 image list <IMAGE> --output wide
```

**Solutions:**
```bash
# For Apple Silicon: Pre-cache images
orka3 ic add <IMAGE> --all

# Wait for caching to complete
orka3 ic info <IMAGE>

# Then deploy (should be much faster)
orka3 vm deploy --image <IMAGE>

# Use smaller images if possible
# Consider creating optimized base images

# Deploy to less loaded nodes
orka3 node list --output wide  # Find node with fewer VMs
orka3 vm deploy --image <IMAGE> --node <LESS_LOADED_NODE>

# Increase deployment timeout
orka3 vm deploy --image <IMAGE> --timeout 20
```

## Default Credentials

For MacStadium base images (ghcr.io/macstadium/orka-images/*):
- **Username:** admin
- **Password:** admin

**Important:** Change the password after first login for security.

## Common Ports

| Service | Default Port | Notes |
|---------|-------------|-------|
| SSH | Varies (not 22) | Check `orka3 vm list --output wide` |
| Screen Sharing (VNC) | Varies | Check `orka3 vm list --output wide` |
| Custom ports | User-defined | Use `--ports` flag |

## Getting Help

If you cannot resolve an issue:

1. **Get Verbose Output:**
   ```bash
   orka3 <command> --output json
   ```

2. **Collect Diagnostic Information:**
   ```bash
   orka3 version
   orka3 config view
   orka3 node list --output wide
   orka3 vm list --output wide
   ```

3. **Contact MacStadium Support:**
   - Provide CLI version, cluster version, and error messages
   - Include diagnostic output
   - Describe what you were trying to accomplish
