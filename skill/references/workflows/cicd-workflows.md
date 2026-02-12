# CI/CD Pipeline Workflows

## Contents
- [Pipeline setup](#cicd-pipeline-setup)
- [Pipeline commands](#cicd-pipeline-commands)
- [Token options](#service-account-token-options)
- [Multiple pipelines](#multiple-pipeline-setup)

## CI/CD Pipeline Setup

```bash
# 1. Create service account (admin)
orka3 sa create sa-ci-pipeline

# 2. Get long-lived token (1 year default)
orka3 sa token sa-ci-pipeline

# 3. (Optional) Create namespace for CI workloads
orka3 namespace create orka-ci

# 4. Move dedicated nodes to CI namespace
orka3 node namespace mini-arm-10 orka-ci
orka3 node namespace mini-arm-11 orka-ci

# 5. Grant service account access
orka3 rb add-subject --namespace orka-ci --serviceaccount orka-default:sa-ci-pipeline

# 6. Create VM config for consistent builds
orka3 vmc create ci-build \
  --image ghcr.io/macstadium/orka-images/sonoma:latest \
  --cpu 4 --memory 8

# 7. (Optional) Tag nodes and create tagged configs
orka3 node tag mini-arm-10 fast-builds
orka3 vmc create fast-build \
  --image sonoma:latest --cpu 6 \
  --tag fast-builds --tag-required
```

## CI/CD Pipeline Commands

In your CI script, authenticate with the service account token (injected as a secret by your CI platform):

```bash
orka3 user set-token $SA_TOKEN

# Deploy VM
VM_NAME=$(orka3 vm deploy --config ci-build -n orka-ci --generate-name -o json | jq -r '.name')

# Get connection info
VM_INFO=$(orka3 vm list $VM_NAME -n orka-ci -o json)
VM_IP=$(echo $VM_INFO | jq -r '.items[0].ip')
VM_SSH_PORT=$(echo $VM_INFO | jq -r '.items[0].ssh')

# Run build
ssh -p $VM_SSH_PORT admin@$VM_IP 'cd /path/to/project && make test'

# Clean up
orka3 vm delete $VM_NAME -n orka-ci
```

## Service Account Token Options

```bash
orka3 sa token sa-jenkins                    # Default: 1 year
orka3 sa token sa-jenkins --duration 24h     # Custom duration
orka3 sa token sa-jenkins --no-expiration    # Never expires
```

## Multiple Pipeline Setup

```bash
# Create service accounts per pipeline
orka3 sa create sa-jenkins --namespace orka-ci
orka3 sa create sa-github-actions --namespace orka-ci
orka3 sa create sa-gitlab-runner --namespace orka-ci

# Grant access to each
orka3 rb add-subject --namespace orka-ci --serviceaccount orka-ci:sa-jenkins
orka3 rb add-subject --namespace orka-ci --serviceaccount orka-ci:sa-github-actions
orka3 rb add-subject --namespace orka-ci --serviceaccount orka-ci:sa-gitlab-runner

# Create different VM configs per workload type
orka3 vmc create unit-tests --image sonoma:latest --cpu 4 --memory 8
orka3 vmc create integration-tests --image sonoma:latest --cpu 6 --memory 12
orka3 vmc create ui-tests --image sonoma:latest --cpu 4 --memory 16
```
