# VM Config Commands Reference

## orka3 vm-config create (alias: vmc)

```bash
orka3 vmc create <NAME> --image <IMAGE> [flags]
```

**Options:**
- `-i, --image string` -- Base image (required)
- `-c, --cpu int` -- CPU cores (default: 3)
- `-m, --memory float` -- RAM in GB
- `--scheduler string` -- `default` or `most-allocated`
- `--tag string` -- Node affinity tag
- `--tag-required` -- Require tagged nodes
- `--disable-vnc` -- Disable VNC

**Intel-only options:**
- `--iso string` -- ISO to attach
- `--gpu` -- GPU passthrough
- `--system-serial string` -- Custom serial number
- `--disable-net-boost` -- Disable network boost

**Name requirements:** Max 50 chars, lowercase alphanumeric/dashes, starts alphabetic, ends alphanumeric, unique to cluster.

```bash
orka3 vmc create medium-ventura-vm --image 90gbventurassh.img --cpu 6
orka3 vmc create small-arm-vm -i ghcr.io/org/orka-images/orka-arm:latest --cpu 4
orka3 vmc create build-vm --image sonoma.orkasi --tag jenkins-builds --tag-required
```

## orka3 vm-config list (alias: vmc)

```bash
orka3 vmc list [<NAME>] [-o table|wide|json]
```

## orka3 vm-config delete (alias: vmc)

```bash
orka3 vmc delete <NAME> [<NAME2> ...]
```
