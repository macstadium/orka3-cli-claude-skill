# Image Management Workflows

## Contents
- [Custom image preparation](#custom-image-preparation)
- [Image caching (ARM)](#image-caching-apple-silicon)
- [OCI registry integration](#oci-registry-integration)
- [Save vs commit](#vm-save-vs-vm-commit)
- [macOS compatibility](#macos-compatibility-notes-v352)

## Custom Image Preparation

```bash
# 1. Deploy base VM
orka3 vm deploy base-config --image ghcr.io/macstadium/orka-images/sonoma:latest

# 2. Get connection info
orka3 vm list base-config -o wide

# 3. Connect via Screen Sharing: vnc://<VM_IP>:<Screenshare_port>
#    Default credentials: admin/admin
#
#    On the VM:
#    - Change password (System Settings > Users & Groups)
#    - Install software, apply OS updates
#    - Install/upgrade Orka VM Tools: brew install orka-vm-tools

# 4. Save as new image (preserves original)
orka3 vm save base-config my-configured-sonoma
# OR overwrite original
orka3 vm commit base-config -d 'Configured with build tools'

# 5. Check async completion
orka3 image list my-configured-sonoma -o wide

# 6. Test the new image
orka3 vm deploy test-vm --image my-configured-sonoma
# Verify configuration persists, then clean up
orka3 vm delete test-vm
orka3 vm delete base-config
```

## Image Caching (Apple Silicon)

Pre-cache images on nodes for consistent deployment times:

```bash
# Cache on all namespace nodes
orka3 ic add ghcr.io/macstadium/orka-images/sonoma:latest --all

# Cache on specific nodes
orka3 ic add my-configured-image --nodes mini-arm-1,mini-arm-2

# Cache on tagged nodes
orka3 ic add xcode-15-image --tags xcode-15

# Check caching progress (wait for 'ready')
orka3 ic info ghcr.io/macstadium/orka-images/sonoma:latest

# List all cached images
orka3 ic list -o wide
```

## OCI Registry Integration

```bash
# 1. Add registry credentials (admin)
orka3 regcred add https://ghcr.io -u "$USER" -p "$TOKEN"

# 2. Deploy from OCI image
orka3 vm deploy --image ghcr.io/your-org/orka-images/custom-sonoma:v1.2

# 3. Customize VM, then push back (ARM only)
orka3 vm push <VM_NAME> ghcr.io/your-org/orka-images/custom-sonoma:v1.3

# 4. Check push status
orka3 vm get-push-status

# 5. Cache OCI images on nodes (optional)
orka3 ic add ghcr.io/your-org/orka-images/custom-sonoma:v1.3 --all
```

## VM save vs. VM commit

| Operation | Behavior | Use Case |
|-----------|----------|----------|
| `vm save` | Creates new image, preserves original | Creating variants of a base image |
| `vm commit` | Updates original image | Iterative development on single image |

## macOS Compatibility Notes (v3.5.2+)

- **macOS Tahoe (26.0):** Full support with v3.5.2 fixes for image deletion, copying, and tagging
- **macOS Sequoia:** Display resolution fixes require Orka VM Tools v3.5.2
  - New images created with Orka 3.5.2 include updated VM Tools automatically
  - Existing images must have Orka VM Tools updated manually
