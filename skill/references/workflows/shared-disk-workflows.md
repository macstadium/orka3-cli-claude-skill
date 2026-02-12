# VM Shared Attached Disk (v3.5.2+)

**Critical limitation:** When shared attached disk is enabled, only **one VM may run per Apple Silicon node**. Disabled by default.

## AWS Deployment

### Step 1: Enable globally via CodeBuild/Ansible

```yaml
vm_shared_disk_enabled: true
```

Run your CodeBuild project to apply.

### Step 2: Configure each EC2 Mac instance

Add to instance user data:

```bash
#!/bin/bash
export VM_SHARED_DISK_SIZE=500
/usr/local/bin/bootstrap-orka <eks-cluster-name> <aws-region> <orka-engine-license-key>
```

Replace placeholders with your EKS cluster name, AWS region, Orka license key, and desired disk size in GB.

### Disabling on AWS

1. Set `vm_shared_disk_enabled: false` in Ansible
2. Re-run CodeBuild
3. Terminate and re-create EC2 Mac instances without `VM_SHARED_DISK_SIZE`

## On-Premises / MSDC Deployment

Set in Ansible configuration:

```yaml
vm_shared_disk_enabled: true
osx_node_orka_vm_shared_disk_size: 500   # GB, optional
```

Run your Ansible playbook to apply. To disable, set `vm_shared_disk_enabled: false` and re-run.

## Requirements

- Orka cluster v3.5.2+ (upgraded from Orka 3.4+ / k8s v1.33+)
- Understand the 1-VM-per-node limitation on Apple Silicon

## Troubleshooting

**VMs not using shared disk:** Verify `vm_shared_disk_enabled: true` in Ansible. On AWS, confirm `VM_SHARED_DISK_SIZE` was set in user data; instance may need re-creation after enabling.

**Config changes not taking effect:** Re-run CodeBuild/Ansible. On AWS, terminate and re-create affected instances.
