# Migration and Backup Workflows

## Contents
- [Intel to ARM migration](#migration-from-intel-to-apple-silicon)
- [Feature comparison](#intel-vs-apple-silicon-feature-comparison)
- [Disaster recovery](#disaster-recovery-and-backup)
- [Recovery procedures](#recovery-procedures)

## Migration from Intel to Apple Silicon

There is no direct image conversion between architectures. Each ARM VM must be configured from scratch using an ARM base image.

```bash
# 1. Audit current Intel VMs
orka3 vm list -o json | jq '.items[] | select(.arch == "amd64") | {name, image, cpu, memory}'

# 2. For each Intel VM, recreate on ARM:
orka3 vm deploy arm-vm --image ghcr.io/macstadium/orka-images/sonoma:latest
# Connect, install same software, configure, then save:
orka3 vm save arm-vm arm-configured-image

# 3. Create VM config for ARM version
orka3 vmc create arm-version --image arm-configured-image --cpu 4 --memory 8

# 4. Update CI/CD pipelines to use ARM configs
# 5. Validate, then decommission Intel VMs
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

## Disaster Recovery and Backup

### Export configuration

```bash
orka3 image list -o json > images-backup-$(date +%Y%m%d).json
orka3 vmc list -o json > vm-configs-backup-$(date +%Y%m%d).json
orka3 namespace list -o json > namespaces-backup-$(date +%Y%m%d).json
orka3 node list -o wide > nodes-layout-$(date +%Y%m%d).txt
```

### Push images to OCI registry (ARM)

```bash
orka3 vm deploy backup-vm --image important-image
orka3 vm push backup-vm ghcr.io/company/backups/important-image:$(date +%Y%m%d)
orka3 vm get-push-status   # Wait for completion
orka3 vm delete backup-vm
```

## Recovery Procedures

### Restore from OCI registry

```bash
orka3 regcred add https://ghcr.io -u "$USER" -p "$TOKEN"
orka3 vm deploy restored-vm --image ghcr.io/company/backups/<IMAGE>:<DATE>
orka3 vm save restored-vm <LOCAL_IMAGE_NAME>   # Optional: save locally
orka3 vm delete restored-vm
```

### Recreate namespace configuration

```bash
# Using saved backup files as reference:
orka3 namespace create <NAMESPACE>
orka3 node namespace <NODE> <NAMESPACE>
orka3 rb add-subject --namespace <NS> --user <EMAIL>
orka3 rb add-subject --namespace <NS> --serviceaccount <SA_NS>:<SA_NAME>
```
