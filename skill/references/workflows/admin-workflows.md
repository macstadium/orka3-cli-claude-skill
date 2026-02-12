# Administrative Workflows

## Contents
- [Multi-namespace setup](#multi-namespace-team-setup)
- [Node tagging](#node-affinity-and-tagging)
- [Access control](#access-control)
- [Namespace lifecycle](#namespace-lifecycle)

## Multi-Namespace Team Setup

```bash
# 1. Create namespaces
orka3 namespace create orka-dev-team
orka3 namespace create orka-qa-team
orka3 namespace create orka-prod

# 2. Dedicate nodes to namespaces
orka3 node namespace mini-arm-1 orka-dev-team
orka3 node namespace mini-arm-2 orka-dev-team
orka3 node namespace mini-arm-3 orka-qa-team
orka3 node namespace mini-arm-4 orka-qa-team
orka3 node namespace mini-arm-5 orka-prod
orka3 node namespace mini-arm-6 orka-prod

# 3. Grant team members access
orka3 rb add-subject --namespace orka-dev-team --user dev1@company.com,dev2@company.com
orka3 rb add-subject --namespace orka-qa-team --user qa1@company.com,qa2@company.com

# Production: admin + service accounts only
orka3 sa create sa-prod-deploy
orka3 rb add-subject --namespace orka-prod --serviceaccount orka-default:sa-prod-deploy

# 4. Verify
orka3 namespace list
orka3 rb list-subjects --namespace orka-dev-team
orka3 node list -n orka-dev-team
```

## Node Affinity and Tagging

```bash
# Tag nodes by capability or workload type
orka3 node tag mac-studio-1 high-performance
orka3 node tag mini-m1-3 ci-builds

# Create VM configs with affinity
orka3 vmc create ci-vm --image sonoma-ci --cpu 4 --tag ci-builds          # Flexible: prefers tagged
orka3 vmc create render-vm --image sonoma-render --cpu 8 --tag rendering --tag-required  # Strict: tagged only

# Verify placement after deploy
orka3 vm list -o wide

# View node tags
orka3 node list -o wide

# Remove tags
orka3 node untag mini-m1-3 ci-builds
```

## Access Control

```bash
# Grant user access
orka3 rb add-subject --namespace orka-team --user user@company.com
orka3 rb add-subject --namespace orka-team --user user1@company.com,user2@company.com

# Grant service account access (format: <sa-namespace>:<sa-name>)
orka3 rb add-subject --namespace orka-team --serviceaccount orka-team:sa-builds
orka3 rb add-subject --namespace orka-prod --serviceaccount orka-ci:sa-deploy

# Revoke access
orka3 rb remove-subject --namespace orka-team --user user@company.com
orka3 rb remove-subject --namespace orka-team --serviceaccount orka-ci:sa-deploy

# Audit
orka3 rb list-subjects --namespace orka-team
```

## Namespace Lifecycle

```bash
# Create standard namespace
orka3 namespace create orka-newteam

# Create namespace for custom Kubernetes pods (no VMs)
orka3 namespace create orka-custom --enable-custom-pods
```

Before deleting a namespace, all VMs must be deleted and nodes moved out:

```bash
# Check contents
orka3 vm list -n orka-oldteam
orka3 node list -n orka-oldteam

# Clean up
orka3 vm delete <VM1> <VM2> -n orka-oldteam
orka3 node namespace mini-arm-1 orka-default -n orka-oldteam

# Delete
orka3 namespace delete orka-oldteam
```
