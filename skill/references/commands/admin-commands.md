# Admin Commands Reference

## Contents
- [Namespace commands](#namespace-commands)
- [Service account commands](#service-account-commands)
- [RBAC commands](#rbac-commands-rolebinding)

## Namespace Commands

### orka3 namespace create

```bash
orka3 namespace create <NAME> [--enable-custom-pods] [flags]
```

- `--enable-custom-pods` -- Configure for custom K8s resources (cannot run Orka VMs)

**Name requirements:** `orka-` prefix, max 63 chars, lowercase alphanumeric/dashes, ends alphanumeric, unique to cluster.

After creation: move nodes (`node namespace`), grant access (`rb add-subject`).

```bash
orka3 namespace create orka-test
orka3 namespace create orka-cp --enable-custom-pods
```

### orka3 namespace list

```bash
orka3 namespace list [<NAME>] [-o table|wide|json]
```

### orka3 namespace delete

```bash
orka3 namespace delete <NAME> [<NAME2> ...] [--timeout <DURATION>]
```

- `--timeout` -- Default: 1h0m0s
- Prerequisites: all VMs/pods removed, all nodes moved out
- **CAUTION:** Destructive, cannot be undone.

## Service Account Commands

### orka3 serviceaccount create (alias: sa)

```bash
orka3 sa create <NAME> [-n <NAMESPACE>]
```

**Name requirements:** Max 253 chars, lowercase alphanumeric/dashes/periods, unique to namespace.

### orka3 serviceaccount token (alias: sa)

```bash
orka3 sa token <NAME> [--duration <DURATION>] [--no-expiration] [-n <NAMESPACE>]
```

- `--duration` -- Token lifetime (default: 8760h = 1 year)
- `--no-expiration` -- Token never expires

```bash
orka3 sa token sa-jenkins
orka3 sa token sa-jenkins --duration 1h
orka3 sa token sa-jenkins --no-expiration
```

### orka3 serviceaccount list (alias: sa)

```bash
orka3 sa list [<NAME>] [-n <NAMESPACE>] [-o table|wide|json]
```

### orka3 serviceaccount delete (alias: sa)

```bash
orka3 sa delete <NAME> [<NAME2> ...] [-n <NAMESPACE>]
```

**CAUTION:** Deleting a service account invalidates all associated tokens.

## RBAC Commands (Rolebinding)

### orka3 rolebinding add-subject (alias: rb)

```bash
orka3 rb add-subject -n <NS> --user <EMAIL>[,<EMAIL2>] --serviceaccount <SA_NS>:<SA_NAME>[,...]
```

- `--user` -- Email addresses, comma-separated
- `--serviceaccount` -- NAMESPACE:NAME format, comma-separated
- Can combine `--user` and `--serviceaccount` in one call

```bash
orka3 rb add-subject -n orka-test --user user@company.com
orka3 rb add-subject -n orka-test --user user1@company.com,user2@company.com
orka3 rb add-subject -n orka-test --serviceaccount orka-default:sa-jenkins
orka3 rb add-subject -n orka-test --user user@company.com --serviceaccount orka-default:sa-jenkins
```

### orka3 rolebinding list-subjects (alias: rb)

```bash
orka3 rb list-subjects [-n <NAMESPACE>] [-o table|wide|json]
```

### orka3 rolebinding remove-subject (alias: rb)

```bash
orka3 rb remove-subject -n <NS> --user <EMAIL>[,...] --serviceaccount <SA_NS>:<SA_NAME>[,...]
```

```bash
orka3 rb remove-subject -n orka-test --user user@company.com
orka3 rb remove-subject -n orka-test --serviceaccount orka-default:sa-jenkins
```
