# VM Commands Reference

## Contents
- [vm deploy](#orka3-vm-deploy)
- [vm list](#orka3-vm-list)
- [vm delete](#orka3-vm-delete)
- [vm save](#orka3-vm-save)
- [vm commit](#orka3-vm-commit)
- [vm push (ARM)](#orka3-vm-push-apple-silicon-only)
- [vm get-push-status (ARM)](#orka3-vm-get-push-status-apple-silicon-only)
- [vm resize](#orka3-vm-resize)
- [Power operations (Intel)](#power-operations-intel-only)

## orka3 vm deploy

```bash
orka3 vm deploy [<NAME>] --image <IMAGE> [flags]
orka3 vm deploy [<NAME>] --config <TEMPLATE> [flags]
```

**Options:**
- `-i, --image string` -- Base image (local or OCI). Required if no `--config`
- `--config string` -- VM configuration template
- `-c, --cpu int` -- CPU cores (default: 3)
- `-m, --memory float` -- RAM in GB
- `--node string` -- Deploy to specific node
- `--tag string` -- Node affinity tag
- `--tag-required` -- Require tagged nodes (default: false)
- `--generate-name` -- Append random suffix to name
- `--scheduler string` -- `default` (spread) or `most-allocated` (pack)
- `--metadata stringToString` -- Custom metadata (key1=value1,key2=value2)
- `-p, --ports strings` -- Port mapping (NODE_PORT:VM_PORT)
- `--timeout int` -- Minutes (default: 10)
- `-n, --namespace string` -- Target namespace
- `-o, --output string` -- json|wide

**Intel-only options:**
- `--iso string` -- ISO to attach
- `--gpu` -- GPU passthrough (requires `--disable-vnc`)
- `--system-serial string` -- Custom serial number
- `--disable-net-boost` -- Disable network boost
- `--disable-vnc` -- Disable VNC

**Name requirements:** Max 63 chars (including generated suffix), lowercase alphanumeric/dashes, starts alphabetic, ends alphanumeric, unique to namespace.

```bash
# Basic
orka3 vm deploy --image ghcr.io/macstadium/orka-images/sonoma:latest
orka3 vm deploy my-vm --image sonoma-90gb-orka3-arm --cpu 4
orka3 vm deploy --image sonoma:latest --generate-name

# Targeted
orka3 vm deploy --image sonoma:latest --node mini-arm-14
orka3 vm deploy --image sonoma:latest --tag jenkins-builds --tag-required
orka3 vm deploy --image sonoma:latest -n orka-test

# Advanced
orka3 vm deploy --image sonoma:latest --metadata 'foo=1,baz=https://example.com'
orka3 vm deploy --image sonoma:latest --ports 9000:4000,9001:4001

# Intel-only
orka3 vm deploy --image emptydisk.img --iso ventura.iso
orka3 vm deploy --image ventura.img --gpu=true --disable-vnc

# From template
orka3 vm deploy --config small-ventura-config
orka3 vm deploy --config small-ventura-config --cpu 6 --memory 16
```

## orka3 vm list

```bash
orka3 vm list [<NAME>] [-n <NAMESPACE>] [-o table|wide|json]
```

**Note:** Stopped/suspended Intel VMs still appear as 'Running'.

```bash
orka3 vm list
orka3 vm list -o wide
orka3 vm list my-vm
orka3 vm list -o json | jq '.items[] | select(.node == "mini-arm-14")'
```

## orka3 vm delete

```bash
orka3 vm delete <NAME> [<NAME2> ...] [-n <NAMESPACE>]
```

**CAUTION:** Cannot be undone. Unsaved/uncommitted data is lost.

## orka3 vm save

```bash
orka3 vm save <VM_NAME> <NEW_IMAGE_NAME> [-d '<DESC>'] [-n <NAMESPACE>]
```

Preserves original image. Async -- check with `image list <NAME>`. Restarts the VM.

## orka3 vm commit

```bash
orka3 vm commit <VM_NAME> [-d '<DESC>'] [-n <NAMESPACE>]
```

Overwrites original image. Intel: image must not be in use by other VMs. Async. Restarts the VM.

## orka3 vm push (Apple Silicon only)

```bash
orka3 vm push <VM_NAME> <IMAGE[:TAG]> [-n <NAMESPACE>]
```

- Image format: `server.com/repository/image:tag` (tag defaults to `latest`)
- Registry credentials must exist in the same namespace
- Async -- check with `vm get-push-status`

```bash
orka3 vm push vm-5rjn4 ghcr.io/myorg/orka-images/base:latest
orka3 vm push vm-fxwj5 ghcr.io/myorg/orka-images/base:1.0 -n orka-test
```

## orka3 vm get-push-status (Apple Silicon only)

```bash
orka3 vm get-push-status [<JOB_NAME>] [-n <NAMESPACE>] [-o table|wide|json]
```

Status viewable for 1 hour after completion. Lists all pushes if no job name given.

## orka3 vm resize

```bash
orka3 vm resize <VM_NAME> <NEW_SIZE_GB> [-u <SSH_USER>] [-p <SSH_PASS>] [-n <NAMESPACE>]
```

- **Apple Silicon:** Automatic, no SSH needed
- **Intel:** Provide `-u`/`-p` for automatic repartition, or repartition manually via Disk Utility
- Size in GB, can only increase, restarts the VM

```bash
orka3 vm resize my-vm 100                                # ARM
orka3 vm resize intel-vm 100 --user admin --password admin  # Intel
```

## Power Operations (Intel only)

```bash
orka3 vm start <VM_NAME> [-n <NAMESPACE>]
orka3 vm stop <VM_NAME> [-n <NAMESPACE>]
orka3 vm suspend <VM_NAME> [-n <NAMESPACE>]
orka3 vm resume <VM_NAME> [-n <NAMESPACE>]
orka3 vm revert <VM_NAME> [-n <NAMESPACE>]    # CAUTION: loses unsaved data
```
