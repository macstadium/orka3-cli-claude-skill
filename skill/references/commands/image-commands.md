# Image Commands Reference

## Contents
- [Local image commands](#local-image-commands)
- [Image cache commands (Apple Silicon)](#image-cache-commands-apple-silicon-only)

## Local Image Commands

### orka3 image list

```bash
orka3 image list [<NAME>] [-o table|wide|json]
```

```bash
orka3 image list
orka3 image list sonoma-90gb-orka3-arm
orka3 image list -o json
```

### orka3 image copy

```bash
orka3 image copy <SOURCE> <DESTINATION> [--description '<DESC>']
```

Async operation -- check status with `orka3 image list <DESTINATION>`.

### orka3 image generate (Intel only)

```bash
orka3 image generate <NAME> <SIZE> [--description '<DESC>']
```

Creates empty image for fresh macOS installs from ISO. Async operation.

```bash
orka3 image generate 120gbemptyimage 120G
```

### orka3 image set-description

```bash
orka3 image set-description <NAME> <DESCRIPTION>
```

**CAUTION:** Overrides existing description.

### orka3 image delete

```bash
orka3 image delete <NAME> [<NAME2> ...]
```

**CAUTION:** Cannot be undone. Affects VMs/configs using this image.

## Image Cache Commands (Apple Silicon only)

### orka3 imagecache add (alias: ic)

```bash
orka3 ic add <IMAGE> {--nodes <N1>,<N2> | --tags <TAG> | --all} [-n <NAMESPACE>]
```

- `--nodes`, `--tags`, and `--all` are mutually exclusive
- Async operation

```bash
orka3 ic add ghcr.io/macstadium/orka-images/sequoia:latest --nodes mini-arm-10
orka3 ic add sonoma-90gb-orka3-arm --nodes mini-arm-10,mini-arm-11
orka3 ic add sequoia:latest --all
orka3 ic add sonoma:latest --tags jenkins-builds
```

### orka3 imagecache info (alias: ic)

```bash
orka3 ic info <IMAGE> [-n <NAMESPACE>] [-o table|wide|json]
```

Status values: `ready` (available), `caching` (in progress).

### orka3 imagecache list (alias: ic)

```bash
orka3 ic list [<IMAGE>] [-n <NAMESPACE>] [-o table|wide|json]
```

```bash
orka3 ic list
orka3 ic list sonoma-90gb-orka3-arm
orka3 ic list ghcr.io/macstadium/orka-images/sonoma:14.0
```
