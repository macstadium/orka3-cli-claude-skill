# Network and Connectivity Troubleshooting

## Cannot connect via Screen Sharing

Get connection info with `orka3 vm list <VM> -o wide`. Use format `vnc://<VM_IP>:<Screenshare_port>`.

```bash
# Intel VMs may need explicit start
orka3 vm start <VM>

# If Screen Sharing not enabled, connect via SSH and enable:
ssh -p <SSH_PORT> admin@<VM_IP>
sudo /System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart \
  -activate -configure -access -on -restart -agent -privs -all
```

MacStadium base images (`ghcr.io/macstadium/orka-images/*`) have Screen Sharing pre-enabled. First boot can take 5-10 minutes.

## Cannot connect via SSH

```bash
# Use the assigned port (not 22)
ssh -p <SSH_PORT> admin@<VM_IP>
```

If SSH is disabled, enable via Screen Sharing: System Settings > Sharing > Remote Login. MacStadium base images have SSH pre-enabled.

## Port conflicts

Let Orka assign ports automatically (omit `--ports`). If you need custom ports, check which are in use with `orka3 vm list -o wide`, then choose available ones:

```bash
orka3 vm deploy --image <IMAGE> --ports 9100:4000,9101:5000
```

## VM slow or unresponsive

```bash
# Check VM resource allocation and node load
orka3 vm list <VM> -o wide
orka3 node list -o wide
```

Redeploy with more CPU/memory, delete unnecessary VMs on the same node, or use node affinity to target a less loaded node.

## Slow deployments

For Apple Silicon, pre-cache images to eliminate download time:

```bash
orka3 ic add <IMAGE> --all
orka3 ic info <IMAGE>   # Wait for 'ready'
```

Also try deploying to a less loaded node (`--node <NODE>`) or increasing timeout (`--timeout 20`).

## Default Credentials

MacStadium base images (`ghcr.io/macstadium/orka-images/*`): `admin`/`admin`. Change after first login.

## Common Ports

| Service | Port | Notes |
|---------|------|-------|
| SSH | Varies (not 22) | Check `vm list -o wide` |
| Screen Sharing (VNC) | Varies | Check `vm list -o wide` |
| Custom ports | User-defined | `--ports` flag on deploy |
