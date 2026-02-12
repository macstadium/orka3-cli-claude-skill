# VM Deployment Troubleshooting

## Insufficient resources

```bash
# Check available resources
orka3 node list -o wide
orka3 vm list -o wide

# Check namespace has nodes
orka3 node list -n <NAMESPACE>
```

Reduce VM CPU/memory, delete unused VMs to free resources, or ask admin to move additional nodes into your namespace with `orka3 node namespace <NODE> <NAMESPACE>`.

## VM deployed but unresponsive

Allow several minutes for macOS to boot (first boot can take 5-10 minutes). Verify IP and ports are assigned with `orka3 vm list <VM> -o wide`.

For Intel VMs, try `orka3 vm start <VM>`. If still unresponsive, delete and redeploy with a known-good image (e.g. `ghcr.io/macstadium/orka-images/sonoma:latest`).

## Image not found

```bash
# Check local images
orka3 image list

# For OCI images, use full path
orka3 vm deploy --image ghcr.io/macstadium/orka-images/sonoma:latest

# Cache OCI image if needed (ARM)
orka3 ic add <IMAGE> --all
orka3 ic info <IMAGE>   # Wait for 'ready'
```

## VM name already exists

Use `--generate-name` for a unique suffix, omit the name for a random name, or delete the existing VM first.

```bash
orka3 vm deploy my-vm --image <IMAGE> --generate-name
```

## Namespace has no nodes

```bash
orka3 node list -n <NAMESPACE>

# Admin: move nodes into namespace
orka3 node namespace <NODE> <NAMESPACE>
```

## Tag required but no tagged nodes

```bash
# Check tagged nodes
orka3 node list -o wide

# Options: tag nodes, use --tag-required=false, or deploy without --tag
orka3 node tag <NODE> <TAG>
```

## Log Sources (v3.4+)

| Log Type | Location | When to Check |
|----------|----------|---------------|
| Orka VM Logs | `/opt/orka/logs/vm/` on Mac node | VM won't start, lifecycle issues |
| Virtual Kubelet | `/var/log/virtual-kubelet/vk.log` on Mac node | Node not responding, scheduling |
| Orka Engine | `/opt/orka/logs/com.macstadium.orka-engine.server.managed.log` | Engine-level errors |
| Pod Logs | Kubernetes dashboard or kubectl | Orchestration issues |
