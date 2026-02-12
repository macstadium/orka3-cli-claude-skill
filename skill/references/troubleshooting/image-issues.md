# Image Management Troubleshooting

## Async operation stuck in progress

Large images (90GB+) can take 10-30+ minutes for save/commit/copy. Check status with `orka3 image list <IMAGE> -o wide`. Avoid concurrent operations on the same image. If stuck for hours, contact MacStadium support.

## Cannot delete image (in use)

The image is referenced by running VMs or VM configs. Delete the VMs and/or VM configs first, then retry:

```bash
orka3 vm list -o json | jq -r '.items[] | select(.image == "<IMAGE>") | .name'
orka3 vmc list -o wide
```

For Intel, the image must not be in use by any VM.

## Image cache not working (Apple Silicon)

```bash
# Check caching status
orka3 ic info <IMAGE>

# Verify registry credentials exist for private OCI images
orka3 regcred list

# Try caching on specific node
orka3 ic add <IMAGE> --nodes <NODE>
```

Large images take time to cache. Check node storage with `orka3 node list -o wide`.

## Invalid image format

Use the full OCI path: `ghcr.io/org/repo/image:tag`. Verify registry credentials exist with `orka3 regcred list`.

## Image push fails (Apple Silicon)

```bash
# Check push status
orka3 vm get-push-status -o wide

# Verify registry credentials are in the same namespace as the VM
orka3 regcred list -n <VM_NAMESPACE>

# Verify image format: server.com/repository/image:tag
orka3 vm push <VM> ghcr.io/org/repo/image:tag
```

## Image copy slow or failing

Large images take 30+ minutes. Monitor progress with `orka3 image list <DEST_IMAGE> -o wide`. Avoid multiple concurrent copy operations.

## Operation Timing Reference

| Operation | Typical Duration | Factors |
|-----------|-----------------|---------|
| image list | Instant | - |
| image copy | 5-30+ minutes | Image size |
| image delete | Instant | - |
| vm save | 5-30+ minutes | Image size, VM disk usage |
| vm commit | 5-30+ minutes | Image size, VM disk usage |
| vm push | 10-60+ minutes | Image size, network speed |
| imagecache add | 5-30+ minutes | Image size, number of nodes |
