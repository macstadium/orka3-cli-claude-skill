---
name: orka3-cli
description: >-
  Provides command syntax, workflows, and troubleshooting for the Orka 3 CLI
  (orka3), MacStadium's tool for managing macOS virtualization on Apple Silicon
  and Intel Mac infrastructure. Use when users mention Orka, orka3, MacStadium
  VMs, macOS virtual machines, or need help with VM deployment, image management,
  node operations, namespaces, CI/CD pipelines, or Orka cluster administration.
---

# Orka 3 CLI

## Essential Context

Orka runs macOS VMs on physical Mac hardware in two architectures. **Intel (amd64)** has power operations (start/stop/suspend/resume/revert), ISO attach, GPU passthrough, and custom serial numbers. **Apple Silicon (arm64)** has OCI registry push (`vm push`), image caching (`imagecache`), and automatic disk resize. Always determine which architecture applies before suggesting commands.

**Auth:** User tokens (`orka3 login`) expire in **1 hour** -- fine for interactive use, never for automation. Service accounts (`sa create` / `sa token`) support configurable or non-expiring tokens. All CI/CD and automation must use service accounts with `user set-token`.

**Execution contexts:** In Claude Code, run `orka3 node list -o wide` to detect architecture and cluster state. In CI/CD, credentials are injected by the platform at runtime -- don't suggest `export` or `orka3 login`. Without CLI access, ask the user for environment details.

**Async operations:** Save, commit, push, copy, and image caching are all async. Always pair with a status-check: `image list <IMAGE>` for save/commit/copy, `imagecache info <IMAGE>` for caching, `vm get-push-status <JOB>` for push.

**Namespaces** resolve via: `--namespace` flag > `ORKA_DEFAULT_NAMESPACE` env var > kubeconfig context > `orka-default`. Some features (shared disk, namespace auto-detection, macOS Tahoe support) require **v3.5.2+**.

## Quick CLI Guide

### Setup
```
orka3 config set --api-url <ORKA_API_URL>
orka3 login                                  # Interactive auth
orka3 node list                              # Verify connectivity
```

### Deploy VMs
```
orka3 vm deploy --image ghcr.io/macstadium/orka-images/sonoma:latest
orka3 vm deploy --image <IMAGE> --cpu 6 --memory 16
orka3 vm deploy my-vm --image <IMAGE>        # Custom name
orka3 vm deploy --config <TEMPLATE>          # From VM config
orka3 vm deploy build --image <IMG> --generate-name  # Unique suffix
```

### Manage VMs
```
orka3 vm list                                # Basic info
orka3 vm list -o wide                        # IP, ports, node, resources
orka3 vm list <VM>                           # Specific VM
orka3 vm delete <VM>                         # Also accepts multiple names
```
Connect via Screen Sharing: `vnc://<IP>:<Screenshare_port>` (default creds: `admin`/`admin`).

### Save Work
```
orka3 vm save <VM> <NEW_IMAGE>               # New image, preserves original
orka3 vm commit <VM>                         # Overwrites source image
orka3 vm push <VM> registry/repo:tag         # OCI push (ARM only)
```
All async -- check with `image list <IMAGE>` or `vm get-push-status <JOB>`.

### Images
```
orka3 image list                             # All local images
orka3 image list <IMAGE>                     # Status of specific image
orka3 image copy <SRC> <DST>
orka3 image delete <IMAGE>
```

### Image Caching (ARM only)
```
orka3 imagecache add <IMAGE> --all           # All namespace nodes
orka3 imagecache add <IMAGE> --nodes <N1>,<N2>
orka3 imagecache add <IMAGE> --tags <TAG>
orka3 imagecache info <IMAGE>                # Caching status
```

### VM Config Templates
```
orka3 vm-config create <NAME> --image <IMG> --cpu 6 --memory 12
orka3 vm-config create <NAME> --image <IMG> --tag <TAG> --tag-required
orka3 vm deploy --config <NAME>              # Deploy from template
orka3 vm-config list
```

### Nodes
```
orka3 node list -o wide                      # Resources, tags, arch
orka3 node tag <NODE> <TAG>                  # Admin: affinity tagging
orka3 node untag <NODE> <TAG>
orka3 node namespace <NODE> <NS>             # Admin: move to namespace
```

### Namespaces & Access (Admin)
```
orka3 namespace create <NAME>
orka3 namespace list
orka3 rb add-subject --namespace <NS> --user <EMAIL>
orka3 rb add-subject --namespace <NS> --serviceaccount <SA_NS>:<SA_NAME>
orka3 rb list-subjects --namespace <NS>
orka3 sa create <NAME>                       # Service account
orka3 sa token <NAME>                        # Default: 1yr expiry
orka3 sa token <NAME> --no-expiration
```

### Resize & Power
```
orka3 vm resize <VM> <SIZE_GB>                              # ARM: automatic
orka3 vm resize <VM> <SIZE_GB> --user "$U" --password "$P"  # Intel: needs SSH
orka3 vm start|stop|suspend|resume|revert <VM>              # Intel only
```

### Output & Flags
- `-o wide|json` -- wide for details, json for scripting
- `-n <namespace>` -- override namespace
- `--generate-name` -- random suffix for VM name
- Aliases: `vm-config`=`vmc` `serviceaccount`=`sa` `rolebinding`=`rb` `registrycredential`=`regcred` `imagecache`=`ic`

## Reference Files

Most questions are answerable from this file. Load references for full flag details, multi-step workflows, or troubleshooting.

| Query | File |
|-------|------|
| VM deploy/save/push/resize flags | [references/commands/vm-commands.md](references/commands/vm-commands.md) |
| Image & cache commands | [references/commands/image-commands.md](references/commands/image-commands.md) |
| Registry credentials | [references/commands/registry-commands.md](references/commands/registry-commands.md) |
| Namespace, SA, RBAC | [references/commands/admin-commands.md](references/commands/admin-commands.md) |
| Node operations | [references/commands/node-commands.md](references/commands/node-commands.md) |
| Config, auth, completion | [references/commands/config-commands.md](references/commands/config-commands.md) |
| VM config templates | [references/commands/vm-config-commands.md](references/commands/vm-config-commands.md) |
| First-time setup | [references/workflows/getting-started.md](references/workflows/getting-started.md) |
| CI/CD pipelines | [references/workflows/cicd-workflows.md](references/workflows/cicd-workflows.md) |
| Custom images & OCI | [references/workflows/image-workflows.md](references/workflows/image-workflows.md) |
| Multi-namespace & RBAC | [references/workflows/admin-workflows.md](references/workflows/admin-workflows.md) |
| Scaling & optimization | [references/workflows/scaling-workflows.md](references/workflows/scaling-workflows.md) |
| Intel to ARM migration | [references/workflows/migration-workflows.md](references/workflows/migration-workflows.md) |
| Shared disk (v3.5.2+) | [references/workflows/shared-disk-workflows.md](references/workflows/shared-disk-workflows.md) |
| Auth & token issues | [references/troubleshooting/auth-issues.md](references/troubleshooting/auth-issues.md) |
| Deployment failures | [references/troubleshooting/deployment-issues.md](references/troubleshooting/deployment-issues.md) |
| Image operation issues | [references/troubleshooting/image-issues.md](references/troubleshooting/image-issues.md) |
| Network & connectivity | [references/troubleshooting/network-issues.md](references/troubleshooting/network-issues.md) |
