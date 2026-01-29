# Orka3 CLI Complete Command Reference

This reference provides detailed syntax, options, and examples for all Orka3 CLI commands. Load this when you need specific command syntax or parameter details.

## Configuration Commands

### orka3 config set
Set the Orka service URL for your environment.

**Syntax:**
```bash
orka3 config set --api-url <URL> [flags]
```

**Options:**
- `-a, --api-url string` - (Required) The Orka service URL
- `-h, --help` - Display help

**Examples:**
```bash
orka3 config set --api-url http://10.221.188.20
orka3 config set --api-url https://company.orka.app
```

### orka3 config view
View the current local Orka CLI configuration.

**Syntax:**
```bash
orka3 config view [flags]
```

## Authentication Commands

### orka3 login
Log in to your Orka cluster with MacStadium Customer Portal credentials.

**Syntax:**
```bash
orka3 login [flags]
```

**Notes:**
- Opens browser for authentication
- Token stored in `~/.kube/config`
- Token valid for 1 hour

### orka3 user get-token
Print your authentication token from ~/.kube/config.

**Syntax:**
```bash
orka3 user get-token [flags]
```

### orka3 user set-token
Log in with a valid authentication token.

**Syntax:**
```bash
orka3 user set-token <TOKEN> [flags]
```

## Service Account Commands (Admin)

### orka3 serviceaccount create (alias: sa)
Create a service account in the specified namespace.

**Syntax:**
```bash
orka3 serviceaccount create <NAME> [--namespace <NS>] [flags]
```

**Options:**
- `-n, --namespace string` - Target namespace (default: "orka-default")
- `-h, --help` - Display help

**Name Requirements:**
- Max 253 characters
- Lowercase alphanumeric, dashes, or periods
- Begins and ends with lowercase alphanumeric
- Unique to namespace

### orka3 serviceaccount token (alias: sa)
Obtain an authentication token for a service account.

**Syntax:**
```bash
orka3 serviceaccount token <NAME> [--duration <DURATION>] [--namespace <NS>] [flags]
```

**Options:**
- `--duration duration` - Token lifetime (default: 8760h = 1 year)
- `--no-expiration` - Create token with no expiration
- `-n, --namespace string` - Target namespace (default: "orka-default")

**Examples:**
```bash
orka3 sa token sa-jenkins
orka3 sa token sa-jenkins --duration 1h
orka3 sa token sa-jenkins --no-expiration
```

### orka3 serviceaccount list (alias: sa)
List service accounts in the specified namespace.

**Syntax:**
```bash
orka3 serviceaccount list [<NAME>] [--namespace <NS>] [--output <FORMAT>] [flags]
```

**Options:**
- `-o, --output string` - Output format: table|wide|json
- `-n, --namespace string` - Target namespace

### orka3 serviceaccount delete (alias: sa)
Delete one or more service accounts.

**Syntax:**
```bash
orka3 serviceaccount delete <NAME> [<NAME2> ...] [--namespace <NS>] [flags]
```

**⚠️ CAUTION:** Deleting a service account invalidates all associated tokens.

## Image Commands

### orka3 image list
List locally stored images in your Orka cluster.

**Syntax:**
```bash
orka3 image list [<NAME>] [--output <FORMAT>] [flags]
```

**Options:**
- `-o, --output string` - Output format: table|wide|json

**Examples:**
```bash
orka3 image list
orka3 image list sonoma-90gb-orka3-arm
orka3 image list --output json
orka3 image list | grep 'amd64'
```

### orka3 image copy
Copy an image and set a new name for the copy.

**Syntax:**
```bash
orka3 image copy <SOURCE> <DESTINATION> [--description '<DESC>'] [flags]
```

**Options:**
- `-d, --description string` - Custom description for the copy

**Notes:**
- Async operation - check status with `orka3 image list <NAME>`
- Copies description from source by default

### orka3 image generate (Intel only)
Generate a new empty image with the specified size.

**Syntax:**
```bash
orka3 image generate <NAME> <SIZE> [--description '<DESC>'] [flags]
```

**Options:**
- `-d, --description string` - Custom description

**Examples:**
```bash
orka3 image generate 120gbemptyimage 120G
```

**Notes:**
- Intel-only (amd64 architecture)
- Async operation
- Used for fresh macOS installs from ISO

### orka3 image set-description
Set a custom description for an image.

**Syntax:**
```bash
orka3 image set-description <NAME> <DESCRIPTION> [flags]
```

**⚠️ CAUTION:** Overrides existing description (cannot be undone).

### orka3 image delete
Delete the specified locally stored images.

**Syntax:**
```bash
orka3 image delete <NAME> [<NAME2> ...] [flags]
```

**⚠️ CAUTION:** Cannot be undone. Affects VMs/configs using this image.

## Image Cache Commands (Apple Silicon only)

### orka3 imagecache add (alias: ic)
Cache an image on specified node(s).

**Syntax:**
```bash
orka3 imagecache add <IMAGE> {--nodes|--tags|--all} [--namespace <NS>] [flags]
```

**Options:**
- `--nodes string` - Specific nodes (comma-separated)
- `--tags string` - Node tags to filter by (comma-separated)
- `--all` - Cache on all nodes in namespace
- `-n, --namespace string` - Target namespace

**Examples:**
```bash
orka3 ic add ghcr.io/macstadium/orka-images/sequoia:latest --nodes mini-arm-10
orka3 ic add sonoma-90gb-orka3-arm --nodes mini-arm-10,mini-arm-11
orka3 ic add sequoia:latest --all
orka3 ic add sonoma:latest --tags jenkins-builds
```

**Notes:**
- Async operation
- Image must be pulled first (or be an OCI image)
- `--nodes`, `--tags`, and `--all` are mutually exclusive

### orka3 imagecache info (alias: ic)
Display the caching status of an image across nodes.

**Syntax:**
```bash
orka3 imagecache info <IMAGE> [--namespace <NS>] [--output <FORMAT>] [flags]
```

**Options:**
- `-o, --output string` - Output format: table|wide|json
- `-n, --namespace string` - Target namespace

**Status Values:**
- `ready` - Available for deployment
- `caching` - Operation still active

### orka3 imagecache list (alias: ic)
List cached images across nodes.

**Syntax:**
```bash
orka3 imagecache list [<IMAGE>] [--namespace <NS>] [--output <FORMAT>] [flags]
```

**Options:**
- `-o, --output string` - Output format: table|wide|json
- `-n, --namespace string` - Target namespace

**Examples:**
```bash
orka3 ic list
orka3 ic list sonoma-90gb-orka3-arm
orka3 ic list ghcr.io/macstadium/orka-images/sequoia
orka3 ic list ghcr.io/macstadium/orka-images/sonoma:14.0
```

## OCI Registry Commands (Admin)

### orka3 registrycredential add (alias: regcred)
Add credentials for an OCI registry server.

**Syntax:**
```bash
orka3 registrycredential add <SERVER> --username <USER> {--password <PASS>|--password-stdin} [--replace] [--allow-insecure] [--namespace <NS>] [flags]
```

**Options:**
- `-u, --username string` - (Required) Username
- `-p, --password string` - Password
- `--password-stdin` - Read password from stdin
- `--replace` - Replace existing credentials
- `--allow-insecure` - Fall back to HTTP if HTTPS unavailable
- `-n, --namespace string` - Target namespace

**Server Address Requirements:**
- Must include scheme and hostname (and optionally port)
- Examples: `https://ghcr.io`, `https://10.221.188.5:30080`

**Examples:**
```bash
orka3 regcred add https://ghcr.io --username whoami --password ghp_***
echo -n "$PASSWORD" | orka3 regcred add https://ghcr.io --username whoami --password-stdin
orka3 regcred add --allow-insecure http://10.221.188.5:30080 --username admin --password p@ssw0rd
orka3 regcred add --replace https://ghcr.io --username whoami --password ghp_***
```

### orka3 registrycredential list (alias: regcred)
List OCI registry servers with stored credentials.

**Syntax:**
```bash
orka3 registrycredential list [--namespace <NS>] [--output <FORMAT>] [flags]
```

### orka3 registrycredential remove (alias: regcred)
Remove authentication credentials for a registry server.

**Syntax:**
```bash
orka3 registrycredential remove <SERVER> [--namespace <NS>] [flags]
```

## VM Commands

### orka3 vm deploy
Deploy a VM with specified configuration.

**Syntax:**
```bash
orka3 vm deploy [<NAME>] --image <IMAGE> [flags]
orka3 vm deploy [<NAME>] --config <TEMPLATE> [flags]
```

**Options:**
- `-i, --image string` - (Required if no --config) Base image (local or OCI)
- `--config string` - VM configuration template
- `-c, --cpu int` - Number of CPU cores (default: 3)
- `-m, --memory float` - RAM in gigabytes
- `--node string` - Specific node for deployment
- `--tag string` - Node affinity tag
- `--tag-required` - Require tagged nodes
- `--generate-name` - Generate unique name with suffix
- `--scheduler string` - Scheduler: 'default' or 'most-allocated'
- `--metadata stringToString` - Custom metadata (key1=value1,key2=value2)
- `-p, --ports strings` - Port mapping (NODE_PORT:VM_PORT)
- `--timeout int` - Deployment timeout in minutes (default: 10)
- `-n, --namespace string` - Target namespace
- `-o, --output string` - Output format: json|wide

**Intel-only Options:**
- `--iso string` - ISO name to attach
- `--gpu` - Enable GPU passthrough (requires --disable-vnc)
- `--system-serial string` - Custom serial number
- `--disable-net-boost` - Disable network performance boost
- `--disable-vnc` - Disable VNC

**VM Name Requirements:**
- Max 63 characters (including generated suffix)
- Lowercase alphanumeric or dashes
- Starts with alphabetic, ends with alphanumeric
- Unique to namespace

**Examples:**
```bash
# Basic deployments
orka3 vm deploy --image ghcr.io/macstadium/orka-images/sonoma:latest
orka3 vm deploy my-vm --image sonoma-90gb-orka3-arm --cpu 4
orka3 vm deploy --image sonoma:latest --memory 10
orka3 vm deploy --image sonoma:latest --generate-name

# Targeted deployments
orka3 vm deploy --image sonoma:latest --node mini-arm-14
orka3 vm deploy --image sonoma:latest --tag jenkins-builds --tag-required
orka3 vm deploy --image sonoma:latest --namespace orka-test

# Advanced deployments
orka3 vm deploy --image sonoma:latest --metadata 'foo=1,baz=https://example.com'
orka3 vm deploy --image sonoma:latest --ports 9000:4000,9001:4001

# Intel-only deployments
orka3 vm deploy --image emptydisk.img --iso ventura.iso
orka3 vm deploy --image ventura.img --gpu=true --disable-vnc
orka3 vm deploy --image ventura.img --system-serial A00BC123D4

# Template deployments
orka3 vm deploy --config small-ventura-config
orka3 vm deploy my-vm --config small-ventura-config
orka3 vm deploy --config small-ventura-config --cpu 6 --memory 16
```

### orka3 vm list
Show information about VMs.

**Syntax:**
```bash
orka3 vm list [<NAME>] [--namespace <NS>] [--output <FORMAT>] [flags]
```

**Options:**
- `-o, --output string` - Output format: table|wide|json
- `-n, --namespace string` - Target namespace

**Examples:**
```bash
orka3 vm list
orka3 vm list --output wide
orka3 vm list my-vm
orka3 vm list --namespace orka-test
orka3 vm list --output wide | grep 'mini-arm-14'
```

**Note:** Stopped/suspended VMs appear as 'Running' when listed.

### orka3 vm delete
Delete specified VMs.

**Syntax:**
```bash
orka3 vm delete <NAME> [<NAME2> ...] [--namespace <NS>] [flags]
```

**⚠️ CAUTION:** Cannot be undone. Unsaved/uncommitted data will be lost.

### orka3 vm save
Save a new image from a running VM.

**Syntax:**
```bash
orka3 vm save <VM_NAME> <NEW_IMAGE_NAME> [--description '<DESC>'] [--namespace <NS>] [flags]
```

**Options:**
- `-d, --description string` - Custom description for new image
- `-n, --namespace string` - Target namespace

**Notes:**
- Preserves original image
- Async operation (check with `orka3 image list <NAME>`)
- Restarts the VM

### orka3 vm commit
Update an existing image from a running VM.

**Syntax:**
```bash
orka3 vm commit <VM_NAME> [--description '<DESC>'] [--namespace <NS>] [flags]
```

**Options:**
- `-d, --description string` - New description for original image
- `-n, --namespace string` - Target namespace

**Notes:**
- Modifies original image
- Intel: image must not be in use by other VMs
- Async operation
- Restarts the VM

### orka3 vm push (Apple Silicon only)
Push VM state to an OCI-compatible registry.

**Syntax:**
```bash
orka3 vm push <VM_NAME> <IMAGE[:TAG]> [--namespace <NS>] [flags]
```

**Notes:**
- Image format: `server.com/repository/image:tag`
- Tag defaults to `latest` if not provided
- Registry credentials required in same namespace
- Async operation (check with `orka3 vm get-push-status`)

**Examples:**
```bash
orka3 vm push vm-5rjn4 ghcr.io/myorg/orka-images/base:latest
orka3 vm push vm-fxwj5 ghcr.io/myorg/orka-images/base:1.0 --namespace orka-test
```

### orka3 vm get-push-status (Apple Silicon only)
View status of image push to OCI registry.

**Syntax:**
```bash
orka3 vm get-push-status [<JOB_NAME>] [--namespace <NS>] [--output <FORMAT>] [flags]
```

**Notes:**
- Job name from push operation
- Status viewable for 1 hour after completion
- Lists all pushes if no job name provided

### orka3 vm resize
Resize the disk of a running VM (increase only).

**Syntax:**
```bash
orka3 vm resize <VM_NAME> <NEW_SIZE_GB> [--user <SSH_USER>] [--password <SSH_PASS>] [--namespace <NS>] [flags]
```

**Options:**
- `-u, --user string` - (Intel-only) SSH user for automatic repartition
- `-p, --password string` - (Intel-only) SSH password for automatic repartition
- `-n, --namespace string` - Target namespace

**Architecture Behavior:**
- **Apple Silicon**: Automatic - no additional steps needed
- **Intel**: Provide SSH credentials for automatic repartition, or manually complete

**Notes:**
- Size always in GB
- Restarts the VM
- Can only increase size

**Examples:**
```bash
orka3 vm resize my-vm 100
orka3 vm resize intel-vm 100 --user admin --password admin
```

### orka3 vm start (Intel only)
Power ON a stopped VM.

**Syntax:**
```bash
orka3 vm start <VM_NAME> [--namespace <NS>] [flags]
```

### orka3 vm stop (Intel only)
Power OFF a running VM.

**Syntax:**
```bash
orka3 vm stop <VM_NAME> [--namespace <NS>] [flags]
```

### orka3 vm suspend (Intel only)
Suspend a running VM (freezes processes).

**Syntax:**
```bash
orka3 vm suspend <VM_NAME> [--namespace <NS>] [flags]
```

### orka3 vm resume (Intel only)
Resume a suspended VM.

**Syntax:**
```bash
orka3 vm resume <VM_NAME> [--namespace <NS>] [flags]
```

### orka3 vm revert (Intel only)
Revert a VM to the latest state of its image.

**Syntax:**
```bash
orka3 vm revert <VM_NAME> [--namespace <NS>] [flags]
```

**⚠️ CAUTION:** Cannot be undone. All unsaved/uncommitted data will be lost.

## VM Configuration Commands

### orka3 vm-config create (alias: vmc)
Create a VM configuration template.

**Syntax:**
```bash
orka3 vm-config create <NAME> [flags]
```

**Options:**
- `-i, --image string` - (Required) Base image (local or OCI)
- `-c, --cpu int` - Number of CPU cores (default: 3)
- `-m, --memory float` - RAM in gigabytes
- `--scheduler string` - Scheduler: 'default' or 'most-allocated'
- `--tag string` - Node affinity tag
- `--tag-required` - Require tagged nodes
- `--disable-vnc` - Disable VNC

**Intel-only Options:**
- `--iso string` - ISO name to attach
- `--gpu` - Enable GPU passthrough
- `--system-serial string` - Custom serial number
- `--disable-net-boost` - Disable network boost

**Config Name Requirements:**
- Max 50 characters
- Lowercase alphanumeric or dashes
- Starts with alphabetic, ends with alphanumeric
- Unique to cluster

**Examples:**
```bash
orka3 vmc create medium-ventura-vm --image 90gbventurassh.img --cpu 6
orka3 vmc create small-arm-vm -i ghcr.io/org/orka-images/orka-arm:latest --cpu 4
orka3 vmc create medium-vm --image sonoma.orkasi --memory 5
orka3 vmc create build-vm --image sonoma.orkasi --tag jenkins-builds --tag-required
```

### orka3 vm-config list (alias: vmc)
Show information about VM configurations.

**Syntax:**
```bash
orka3 vm-config list [<NAME>] [--output <FORMAT>] [flags]
```

**Options:**
- `-o, --output string` - Output format: table|wide|json

**Examples:**
```bash
orka3 vmc list
orka3 vmc list --output wide
orka3 vmc list small-ventura-vm
orka3 vmc list --output wide | grep 'user@company.com'
```

### orka3 vm-config delete (alias: vmc)
Delete VM configuration templates.

**Syntax:**
```bash
orka3 vm-config delete <NAME> [<NAME2> ...] [flags]
```

## Node Commands

### orka3 node list
Show information about Orka nodes.

**Syntax:**
```bash
orka3 node list [<NAME>] [--namespace <NS>] [--output <FORMAT>] [flags]
```

**Options:**
- `-o, --output string` - Output format: table|wide|json
- `-n, --namespace string` - Target namespace

**Examples:**
```bash
orka3 node list
orka3 node list --output wide
orka3 node list mini-1
orka3 node list --namespace orka-test
orka3 node list --output wide | grep 'mini-arm'
```

### orka3 node tag (Admin)
Tag a node for targeted VM deployment (set node affinity).

**Syntax:**
```bash
orka3 node tag <NODE_NAME> <TAG> [--namespace <NS>] [flags]
```

**Tag Requirements:**
- Max 63 characters
- Alphanumeric, dashes, underscores, or periods
- Begins and ends with alphanumeric
- One tag at a time

**Examples:**
```bash
orka3 node tag mini-1 jenkins
orka3 node tag mini-1 jenkins --namespace orka-test
orka3 node list mini-1 --output wide  # Verify tag
```

### orka3 node untag (Admin)
Remove a tag from a node.

**Syntax:**
```bash
orka3 node untag <NODE_NAME> <TAG> [--namespace <NS>] [flags]
```

**Examples:**
```bash
orka3 node untag mini-1 my-tag
orka3 node untag mini-1 my-tag --namespace orka-test
```

### orka3 node namespace (Admin)
Move Orka nodes across namespaces.

**Syntax:**
```bash
orka3 node namespace <NODE> [--namespace <CURRENT_NS>] <TARGET_NS> [flags]
```

**Options:**
- `-n, --namespace string` - Current namespace (default: "orka-default")

**Examples:**
```bash
orka3 node namespace mini-1 orka-test
orka3 node namespace mini-1 --namespace orka-test orka-production
orka3 node namespace mini-1 --namespace orka-production orka-default
```

## Namespace Commands (Admin)

### orka3 namespace create
Create a new namespace.

**Syntax:**
```bash
orka3 namespace create <NAME> [--enable-custom-pods] [flags]
```

**Options:**
- `--enable-custom-pods` - Configure for custom K8s resources (cannot run Orka VMs)

**Name Requirements:**
- Begins with `orka-` prefix
- Max 63 characters (including prefix)
- Lowercase alphanumeric or dashes
- Ends with alphanumeric
- Unique to cluster

**Post-Creation Steps:**
1. Move nodes: `orka3 node namespace <NODE> <NAMESPACE>`
2. Grant access: `orka3 rb add-subject --namespace <NS> --user <EMAIL>`

**Examples:**
```bash
orka3 namespace create orka-test
orka3 namespace create orka-cp --enable-custom-pods
```

### orka3 namespace list
List all namespaces.

**Syntax:**
```bash
orka3 namespace list [<NAME>] [--output <FORMAT>] [flags]
```

**Options:**
- `-o, --output string` - Output format: table|wide|json

### orka3 namespace delete
Delete specified namespaces.

**Syntax:**
```bash
orka3 namespace delete <NAME> [<NAME2> ...] [--timeout <DURATION>] [flags]
```

**Options:**
- `-t, --timeout duration` - Time to wait before giving up (default: 1h0m0s)

**Prerequisites:**
- All VMs/pods must be removed
- All nodes must be moved out

**⚠️ CAUTION:** Destructive operation - cannot be undone.

## RBAC Commands (Admin)

### orka3 rolebinding add-subject (alias: rb)
Add a subject to a namespace rolebinding (grant access).

**Syntax:**
```bash
orka3 rolebinding add-subject --namespace <NS> --user <EMAIL>[,<EMAIL2>,...] AND/OR --serviceaccount <SA_NS>:<SA_NAME>[,<SA_NS2>:<SA_NAME2>,...] [flags]
```

**Options:**
- `-u, --user strings` - Users (email addresses, comma-separated)
- `-s, --serviceaccount strings` - Service accounts (NAMESPACE:NAME format, comma-separated)
- `-n, --namespace string` - Target namespace (default: "orka-default")

**Examples:**
```bash
orka3 rb add-subject --namespace orka-test --user user@company.com
orka3 rb add-subject --namespace orka-test --user user1@company.com,user2@company.com
orka3 rb add-subject --namespace orka-test --serviceaccount orka-default:sa-jenkins
orka3 rb add-subject --namespace orka-test --serviceaccount orka-default:sa-jenkins,orka-production:sa-release
orka3 rb add-subject --namespace orka-test --user user@company.com --serviceaccount orka-default:sa-jenkins
```

### orka3 rolebinding list-subjects (alias: rb)
List all rolebinding subjects in a namespace.

**Syntax:**
```bash
orka3 rolebinding list-subjects [--namespace <NS>] [--output <FORMAT>] [flags]
```

**Options:**
- `-o, --output string` - Output format: table|wide|json
- `-n, --namespace string` - Target namespace (default: "orka-default")

**Examples:**
```bash
orka3 rb list-subjects
orka3 rb list-subjects --namespace orka-test
orka3 rb list-subjects | grep 'ServiceAccount'
```

### orka3 rolebinding remove-subject (alias: rb)
Remove a subject from a namespace rolebinding (revoke access).

**Syntax:**
```bash
orka3 rolebinding remove-subject --user <EMAIL>[,<EMAIL2>,...] AND/OR --serviceaccount <SA_NS>:<SA_NAME>[,<SA_NS2>:<SA_NAME2>,...] [--namespace <NS>] [flags]
```

**Options:**
- `-u, --user strings` - Users to remove (email addresses, comma-separated)
- `-s, --serviceaccount strings` - Service accounts to remove (NAMESPACE:NAME format, comma-separated)
- `-n, --namespace string` - Target namespace (default: "orka-default")

**Examples:**
```bash
orka3 rb remove-subject --namespace orka-test --user user@company.com
orka3 rb remove-subject --namespace orka-test --user user1@company.com,user2@company.com
orka3 rb remove-subject --namespace orka-test --serviceaccount orka-default:sa-jenkins
orka3 rb remove-subject --namespace orka-test --user user@company.com --serviceaccount orka-default:sa-jenkins
```

## Utility Commands

### orka3 completion
Generate shell autocompletion scripts.

**Syntax:**
```bash
orka3 completion {bash|fish|powershell|zsh} [flags]
```

**Examples:**
```bash
# Bash (load current session)
source <(orka3 completion bash)

# Bash (persist - Linux)
orka3 completion bash > /etc/bash_completion.d/orka3

# Bash (persist - macOS)
orka3 completion bash > $(brew --prefix)/etc/bash_completion.d/orka3

# Zsh (load current session)
source <(orka3 completion zsh)

# Zsh (persist - Linux)
orka3 completion zsh > "${fpath[1]}/_orka3"

# Zsh (persist - macOS)
orka3 completion zsh > $(brew --prefix)/share/zsh/site-functions/_orka3
```

### orka3 version
Print the current version of the Orka CLI.

**Syntax:**
```bash
orka3 version [flags]
```

**Output Includes:**
- CLI build information
- Compatibility with Orka cluster
