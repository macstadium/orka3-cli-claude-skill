# Node Commands Reference

## orka3 node list

```bash
orka3 node list [<NAME>] [-n <NAMESPACE>] [-o table|wide|json]
```

```bash
orka3 node list
orka3 node list -o wide
orka3 node list mini-1
orka3 node list -n orka-test
```

## orka3 node tag (Admin)

```bash
orka3 node tag <NODE_NAME> <TAG> [-n <NAMESPACE>]
```

**Tag requirements:** Max 63 chars, alphanumeric/dashes/underscores/periods, starts and ends alphanumeric. One tag per call.

```bash
orka3 node tag mini-1 jenkins
orka3 node list mini-1 -o wide  # Verify tag
```

## orka3 node untag (Admin)

```bash
orka3 node untag <NODE_NAME> <TAG> [-n <NAMESPACE>]
```

## orka3 node namespace (Admin)

```bash
orka3 node namespace <NODE> [-n <CURRENT_NS>] <TARGET_NS>
```

```bash
orka3 node namespace mini-1 orka-test
orka3 node namespace mini-1 -n orka-test orka-production
```
