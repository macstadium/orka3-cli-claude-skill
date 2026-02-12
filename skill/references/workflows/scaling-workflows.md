# Scaling and Resource Optimization

## Contents
- [Parallel VM deployment](#scaling-vms-for-parallel-workloads)
- [Disk management](#vm-disk-management)
- [Resource optimization](#resource-optimization)
- [Scheduler options](#scheduler-options)
- [Scripting patterns](#scripting-patterns)

## Scaling VMs for Parallel Workloads

```bash
# 1. Create VM config
orka3 vmc create load-test-vm --image sonoma-configured --cpu 4 --memory 8

# 2. Tag nodes for workload (optional)
orka3 node tag mini-arm-1 load-testing
orka3 node tag mini-arm-2 load-testing

# 3. Deploy multiple VMs
for i in {1..10}; do
  orka3 vm deploy load-test --config load-test-vm --generate-name
done

# 4. Get VM IPs for scripting
orka3 vm list -o json | jq -r '.items[] | select(.name | startswith("load-test")) | .ip'

# 5. Clean up
orka3 vm list -o json | jq -r '.items[] | select(.name | startswith("load-test")) | .name' | \
  while read vm; do orka3 vm delete $vm; done
```

## VM Disk Management

### Apple Silicon

```bash
orka3 vm resize my-vm 150   # Automatic, restarts VM
```

### Intel

```bash
# Automatic repartition (requires SSH)
orka3 vm resize intel-vm 150 --user "$VM_USER" --password "$VM_PASSWORD"

# Or resize without repartition, then manually repartition via Disk Utility
orka3 vm resize intel-vm 150
```

Size is in GB, can only increase. VM restarts after resize.

## Resource Optimization

```bash
# Check cluster resources
orka3 node list -o wide

# Check VM distribution
orka3 vm list -o wide

# Right-size VM configs
orka3 vmc create small-vm --image sonoma --cpu 2 --memory 4
orka3 vmc create medium-vm --image sonoma --cpu 4 --memory 8
orka3 vmc create large-vm --image sonoma --cpu 6 --memory 12

# Use most-allocated scheduler to pack VMs on fewer nodes
orka3 vmc create packed-vm --image sonoma --cpu 4 --scheduler most-allocated

# Clean up unused resources
orka3 image list -o wide     # Identify old images
orka3 image delete <OLD_IMAGE>
orka3 vmc list               # Identify obsolete configs
orka3 vmc delete <OLD_CONFIG>
```

## Scheduler Options

| Scheduler | Behavior | Use Case |
|-----------|----------|----------|
| `default` | Spreads VMs across nodes | General workloads, high availability |
| `most-allocated` | Packs VMs on fewest nodes | Cost optimization, power savings |

## Scripting Patterns

```bash
# Deploy multiple VMs with generated names
for i in {1..5}; do
  orka3 vm deploy build --image sonoma:latest --cpu 4 --generate-name
done

# Get all VM IPs
orka3 vm list -o json | jq -r '.items[].ip'

# Get IPs filtered by name prefix
orka3 vm list -o json | jq -r '.items[] | select(.name | startswith("build")) | .ip'

# Get name + IP pairs
orka3 vm list -o json | jq -r '.items[] | "\(.name) \(.ip)"'
```
