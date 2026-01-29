# Common Orka3 CLI Workflows

This reference provides detailed workflows for common Orka3 CLI operations. Load this when you need step-by-step guidance for complex multi-step tasks.

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

**CI/CD Pipeline Commands (in your CI script):**

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

```bash
# Apple Silicon - Simple resize
# 1. Deploy VM
orka3 vm deploy my-vm --image sonoma-90gb --cpu 4

# 2. Resize to 150GB (automatic)
orka3 vm resize my-vm 150

# 3. Verify resize (VM will restart)
orka3 vm list my-vm --output wide

# Intel - Resize with repartition
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

## Troubleshooting Deployment Issues

**Debug VM deployment failures:**

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
