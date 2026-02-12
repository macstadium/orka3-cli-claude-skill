---
name: orka3-cli
description: >-
  Expert guidance for using the Orka3 CLI to manage macOS virtualization
  infrastructure. Use when users need to work with Orka VMs, images, nodes,
  or cluster resources through requests like "Create 3 VMs with macOS Sonoma",
  "Show me all running VMs", "How do I deploy a VM?", "Set up CI/CD", or any
  VM management, troubleshooting, or infrastructure configuration tasks.
---

# Orka3 CLI — Quick Reference

**Current Version:** 3.5.2 | **Support:** support@macstadium.com

## Essential Context

Orka virtualizes macOS on physical Mac hardware. The CLI (`orka3`) manages VMs, images, nodes, namespaces, and access control.

**Architecture split** — Intel (`amd64`: Mac Pro, Intel Mac mini) and Apple Silicon (`arm64`: M1–M4 Mac mini, Mac Studio) have different command sets. Intel has power operations (`start`/`stop`/`suspend`/`resume`/`revert`), GPU passthrough, and ISO installs. ARM has OCI registry push (`vm push`), image caching (`imagecache`), and automatic disk resize.

**Auth lifecycle** — `orka3 login` opens a browser and stores a token in `~/.kube/config`. User tokens expire in **1 hour**. For anything automated (CI/CD, scripts, pipelines), use service accounts: `orka3 sa create <name>` then `orka3 sa token <name>` (default: 1 year, or `--no-expiration`).

**Execution contexts** — (1) Local machine: full CLI, interactive login. (2) CI/CD pipeline: ephemeral, service account tokens only, credentials via CI settings not `export`. (3) Claude Code: can probe the cluster directly. (4) Chat/conversation: suggest commands, can't execute.

**Async operations** — `vm save`, `vm commit`, `vm push`, `image copy`, `imagecache add` are all async. Check status with `orka3 image list <IMAGE>`, `orka3 ic info <IMAGE>`, or `orka3 vm get-push-status`.

**Shared disk (v3.5.2+)** — When enabled, VMs use an attached shared disk on the host. Apple Silicon: **only 1 VM per node** when enabled. Requires Ansible config (`vm_shared_disk_enabled: true`) plus per-host sizing. First-time per-host: the guest disk arrives unformatted — must `diskutil eraseDisk` once (see `shared-disk-workflows.md`). Persists across reboots.

**Namespace resolution (v3.5.2+)** — Priority: `--namespace` flag > `ORKA_DEFAULT_NAMESPACE` env var > kubeconfig context > `orka-default`.

## Quick CLI Guide

### Setup
```bash
orka3 config set --api-url <ORKA_API_URL>
orka3 login                                    # Browser-based auth
orka3 node list                                # Verify connectivity
```

API URLs: `http://10.221.188.20` (Orka 2.1+), `https://company.orka.app` (domain), or custom.

### Deploy VMs
```bash
orka3 vm deploy --image ghcr.io/macstadium/orka-images/sonoma:latest
orka3 vm deploy my-vm --image <IMAGE> --cpu 4 --memory 8
orka3 vm deploy --image <IMAGE> --generate-name           # Unique suffix
orka3 vm deploy --image <IMAGE> --node <NODE>              # Target node
orka3 vm deploy --image <IMAGE> --tag <TAG> --tag-required # Node affinity
orka3 vm deploy --config <TEMPLATE>                        # From VM config
orka3 vm deploy --config <TEMPLATE> --cpu 6 --memory 16    # Override template
```

### List & Inspect
```bash
orka3 vm list                       # All VMs
orka3 vm list my-vm                 # Filter by name
orka3 vm list -o wide               # Extended details (IP, ports, node)
orka3 vm list -o json               # Machine-readable
```

### Connect to VMs
```
vnc://<VM-IP>:<Screenshare-port>    # From vm list -o wide
Default credentials: admin / admin  # MacStadium base images
```

### Delete VMs
```bash
orka3 vm delete <VM>
orka3 vm delete <VM1> <VM2>         # Multiple
```

### Save Work
```bash
orka3 vm save <VM> <NEW_IMAGE>      # New image, preserves original
orka3 vm commit <VM>                # Overwrites source image
orka3 vm push <VM> registry/img:tag # Push to OCI registry (ARM only)
# All three are async. Check: orka3 image list <IMAGE>
```

### Images
```bash
orka3 image list                    # Local images
orka3 image list <NAME>             # Filter by name
orka3 image copy <SRC> <DST>        # Async
orka3 image delete <IMAGE>
```

### Image Caching (ARM only)
```bash
orka3 ic add <IMAGE> --all                     # All nodes in namespace
orka3 ic add <IMAGE> --nodes <N1>,<N2>         # Specific nodes
orka3 ic add <IMAGE> --tags <TAG>              # Tagged nodes
orka3 ic info <IMAGE>                          # Check status
orka3 ic list                                  # All cached images
```

### VM Configs (Templates)
```bash
orka3 vmc create <NAME> --image <IMAGE> --cpu 4 --memory 8
orka3 vmc create <NAME> --image <IMAGE> --tag <TAG> --tag-required
orka3 vmc list                      # All configs
orka3 vmc list <NAME>               # Filter by name
orka3 vmc delete <NAME>
```

### Disk Resize
```bash
orka3 vm resize <VM> <SIZE_GB>                              # ARM: automatic
orka3 vm resize <VM> <SIZE_GB> --user admin --password admin # Intel: needs SSH
```

### Power Operations (Intel only)
```bash
orka3 vm start|stop|suspend|resume|revert <VM>
```

### Nodes
```bash
orka3 node list                     # All nodes
orka3 node list <NAME>              # Filter by name
orka3 node list -o wide             # CPU, memory, tags, VMs
orka3 node tag <NODE> <TAG>         # Admin: set affinity tag
orka3 node untag <NODE> <TAG>       # Admin: remove tag
orka3 node namespace <NODE> <NS>    # Admin: move node to namespace
```

### Namespaces & Access Control (Admin)
```bash
orka3 namespace create orka-<name>
orka3 namespace create orka-<name> --enable-custom-pods  # K8s pods, no VMs
orka3 namespace list
orka3 namespace delete orka-<name>                       # Must be empty first

# Grant access
orka3 rb add-subject --namespace <NS> --user <EMAIL>
orka3 rb add-subject --namespace <NS> --serviceaccount <SA_NS>:<SA_NAME>
orka3 rb list-subjects --namespace <NS>
orka3 rb remove-subject --namespace <NS> --user <EMAIL>
```

### Service Accounts
```bash
orka3 sa create <NAME>                          # In current namespace
orka3 sa create <NAME> -n <NS>                  # In specific namespace
orka3 sa token <NAME>                           # 1-year token (default)
orka3 sa token <NAME> --duration 24h            # Custom duration
orka3 sa token <NAME> --no-expiration           # Never expires
orka3 sa list
orka3 sa delete <NAME>
```

### OCI Registry Credentials (Admin)
```bash
orka3 regcred add https://ghcr.io --username "$USER" --password "$TOKEN"
orka3 regcred list
orka3 regcred remove <SERVER>
```

### Output & Flags
```bash
-o wide|json|table    # Output format (table is default)
-n <namespace>        # Override namespace
--generate-name       # Auto-suffix for unique VM names
--timeout <minutes>   # Deployment timeout (default: 10)
```

**Aliases:** `vm-config` = `vmc`, `serviceaccount` = `sa`, `rolebinding` = `rb`, `registrycredential` = `regcred`, `imagecache` = `ic`

### Intel-Only Deploy Flags
```bash
--iso <NAME>          # Attach ISO for OS install
--gpu                 # GPU passthrough (requires --disable-vnc)
--system-serial <SN>  # Custom serial number
--disable-net-boost   # Disable network boost
```

### JSON Scripting
```bash
orka3 vm list -o json | jq -r '.items[].name'
orka3 vm list -o json | jq '.items[] | select(.cpu > 4)'
orka3 vm list -o json | jq '.items | length'
```

## Reference Files

Most questions are answerable from this file. Load references for full flag details, complex workflows, or troubleshooting.

### Commands
| File | When to load |
|------|-------------|
| `references/commands/vm-commands.md` | Full deploy flags, save/commit/push details, resize, power ops |
| `references/commands/image-commands.md` | Image list/copy/delete flags, imagecache syntax |
| `references/commands/node-commands.md` | Node tag/untag/namespace full syntax |
| `references/commands/admin-commands.md` | Namespace, service account, RBAC full syntax |
| `references/commands/config-commands.md` | CLI config, login, completion setup |
| `references/commands/vm-config-commands.md` | VM config create/list/delete flags |
| `references/commands/registry-commands.md` | Registry credential management |

### Workflows
| File | When to load |
|------|-------------|
| `references/workflows/cicd-workflows.md` | CI/CD pipeline setup, multi-pipeline patterns |
| `references/workflows/image-workflows.md` | Golden image creation, caching strategy, OCI registry |
| `references/workflows/admin-workflows.md` | Multi-namespace setup, node tagging strategy, RBAC patterns |
| `references/workflows/scaling-workflows.md` | Batch deployments, disk management, resource optimization |
| `references/workflows/migration-workflows.md` | Intel → ARM migration, backup/recovery |
| `references/workflows/shared-disk-workflows.md` | Shared disk config (v3.5.2+), first-time disk init |

### Troubleshooting
| File | When to load |
|------|-------------|
| `references/troubleshooting/auth-issues.md` | Token expired, permissions, service account tokens |
| `references/troubleshooting/deployment-issues.md` | Insufficient resources, image not found, name conflicts |
| `references/troubleshooting/image-issues.md` | Async ops stuck, deletion blocked, cache issues |
| `references/troubleshooting/network-issues.md` | Screen Sharing, SSH, port conflicts, slow VMs |
