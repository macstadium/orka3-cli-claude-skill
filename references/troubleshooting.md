# Orka3 CLI Troubleshooting Guide

This reference provides solutions to common issues encountered when using the Orka3 CLI. Load this when you need to diagnose and resolve problems.

## Authentication Issues

### Problem: "Authentication token expired"

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

### Problem: "Unable to connect to Orka cluster"

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

### Problem: "Forbidden" or "Insufficient permissions"

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

## VM Deployment Issues

### Problem: VM deployment fails with "Insufficient resources"

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

### Problem: VM deployment succeeds but VM is unresponsive

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

### Problem: VM deployment fails with "Image not found"

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

### Problem: VM name already exists

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

## Image Management Issues

### Problem: Async image operations stuck in progress

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

### Problem: Cannot delete image (in use)

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

### Problem: Image cache not working (Apple Silicon)

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

## Namespace and Access Issues

### Problem: "Namespace has no nodes"

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

### Problem: Cannot create namespace / admin commands fail

**Symptoms:**
- "Requires administrative privileges"
- "Forbidden" on admin operations

**Cause:**
- Only admin users can perform certain operations:
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

### Problem: Service account token not working

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

## Network and Connectivity Issues

### Problem: Cannot connect to VM via Screen Sharing

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

### Problem: Port conflicts

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

## Performance Issues

### Problem: VM deployments are very slow

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

### Problem: VM is slow/unresponsive during use

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

## Common Error Messages

### "VM config not found"

**Cause:** Trying to deploy from non-existent template

**Solution:**
```bash
# List available configs
orka3 vmc list

# Use correct config name
orka3 vm deploy --config <CORRECT_NAME>
```

### "Invalid image format"

**Cause:** Incorrect OCI image path

**Solution:**
```bash
# Use full OCI path with registry
orka3 vm deploy --image ghcr.io/org/repo/image:tag

# Verify registry credentials exist
orka3 regcred list
```

### "Tag required but no tagged nodes available"

**Cause:** VM config requires tagged nodes but none exist

**Solution:**
```bash
# Check if tagged nodes exist
orka3 node list --output wide | grep <TAG>

# Ask admin to tag nodes or set tag-required=false
orka3 vm deploy --config <CONFIG> --tag-required=false
```

### "Namespace not found"

**Cause:** Trying to access non-existent namespace

**Solution:**
```bash
# List available namespaces
orka3 namespace list

# Use correct namespace
orka3 vm list --namespace <CORRECT_NAMESPACE>

# Or ask admin to create namespace
# Admin runs:
orka3 namespace create orka-<NAME>
```

## Getting Help

If you cannot resolve an issue using this guide:

1. **Check MacStadium Documentation:**
   - https://support.macstadium.com

2. **Get Verbose Output:**
   ```bash
   orka3 <command> --output json
   ```

3. **Collect Diagnostic Information:**
   ```bash
   orka3 version
   orka3 config view
   orka3 node list --output wide
   orka3 vm list --output wide
   orka3 namespace list
   ```

4. **Contact MacStadium Support:**
   - Provide CLI version, cluster version, and error messages
   - Include diagnostic output from above
   - Describe what you were trying to accomplish

5. **Check Cluster Status:**
   - Contact your admin about cluster health
   - Verify no ongoing maintenance

## Prevention Tips

**Best Practices to Avoid Common Issues:**

1. **Always specify namespace explicitly** when working with multiple namespaces
2. **Use --output wide** when troubleshooting to see all details
3. **Cache images** before mass deployments (Apple Silicon)
4. **Use VM configs** for consistency and repeatability
5. **Monitor node resources** regularly
6. **Clean up unused VMs** promptly
7. **Use service accounts** for automation, not user credentials
8. **Test with single VM** before deploying at scale
9. **Document your naming conventions** to avoid conflicts
10. **Keep CLI updated** to latest version matching your cluster
