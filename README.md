# Orka3 CLI Claude Skill

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill that enables Claude to **execute** Orka3 CLI commands for managing macOS virtual machines. When used with Claude Code, this skill provides hands-on automation of MacStadium's virtualization infrastructure—deploying VMs, managing images, and configuring clusters directly from natural language requests.

## Features

- Natural language to Orka3 CLI command translation
- VM lifecycle management (deploy, save, delete, resize)
- Image management (local and OCI registries)
- Node operations and tagging
- Namespace and access control (RBAC)
- Service account management for CI/CD
- VM shared attached disk configuration (v3.5.2+)
- Automatic namespace detection from kubeconfig (v3.5.2+)
- Log sources reference for troubleshooting (v3.4+)
- macOS Tahoe and Sequoia compatibility guidance

## How It Works

This skill behaves differently depending on how you access Claude:

| Environment | Capabilities | Use Case |
|-------------|--------------|----------|
| **Claude Code (CLI)** | Executes `orka3` commands directly on your machine. Deploys VMs, manages images, and interacts with your cluster in real-time. | Automation, hands-on management |
| **Regular Claude (claude.ai)** | Provides documentation, explains commands, and helps plan workflows. Cannot execute commands or interact with your cluster. | Learning, planning, troubleshooting |

**With Claude Code**, you can say "Create 3 VMs with macOS Sonoma" and Claude will actually deploy them to your cluster.

> **Note:** When using Claude Code to interact with your Orka cluster, make sure you're connected via VPN using the connection details from your IP plan.

**With regular Claude**, the same request will explain the commands needed, but you'll need to copy and run them yourself.

## Prerequisites

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) installed
- Access to an Orka3 cluster
- Orka3 CLI installed (`orka3`)

## Installation

**Option 1: Download from GitHub Releases (recommended)**

```bash
# Download the latest .skill archive from GitHub Releases
# https://github.com/macstadium/orka3-cli-claude-skill/releases

# Extract to the skills directory
unzip orka3-cli-v*.skill -d ~/.claude/skills/orka3-cli
```

**Option 2: Clone and copy**

```bash
# Clone the repository
git clone https://github.com/macstadium/orka3-cli-claude-skill.git

# Copy skill content to the skills directory
cp -r orka3-cli-claude-skill/skill/* ~/.claude/skills/orka3-cli/
```

**Verify installation**

After installation, your skill directory should look like this:

```
~/.claude/skills/orka3-cli/
├── SKILL.md
└── references/
    ├── commands/
    │   ├── vm-commands.md
    │   ├── image-commands.md
    │   ├── registry-commands.md
    │   ├── admin-commands.md
    │   ├── node-commands.md
    │   ├── config-commands.md
    │   └── vm-config-commands.md
    ├── workflows/
    │   ├── getting-started.md
    │   ├── cicd-workflows.md
    │   ├── image-workflows.md
    │   ├── admin-workflows.md
    │   ├── scaling-workflows.md
    │   ├── migration-workflows.md
    │   └── shared-disk-workflows.md
    └── troubleshooting/
        ├── auth-issues.md
        ├── deployment-issues.md
        ├── image-issues.md
        └── network-issues.md
```

Restart Claude Code after installation for the skill to be detected.

### Claude Desktop

For Claude Desktop (the macOS/Windows app):

1. Download the `.skill` archive from [GitHub Releases](https://github.com/macstadium/orka3-cli-claude-skill/releases)
2. Open Settings > Capabilities > Skills
3. Upload the `.skill` archive

Alternatively, use a Project with custom instructions:

1. Create a new Project in Claude Desktop
2. Open project settings and add custom instructions
3. Copy the contents of `skill/SKILL.md` into the custom instructions field
4. Upload specific reference files from `skill/references/` as project knowledge

> **Note:** Claude Desktop cannot execute commands. It will provide guidance and explain commands, but you'll need to run them in your terminal.

## Usage

Once installed, Claude Code will automatically detect the skill when you ask questions about Orka3 or macOS VM management.

### With Claude Code (Command Execution)

Claude Code can execute commands directly on your machine:

```
"Create 3 VMs with macOS Sonoma"        → Deploys 3 VMs to your cluster
"Show me all running VMs"               → Runs orka3 vm list and displays results
"Delete all VMs in namespace dev"       → Removes the VMs after confirmation
"Cache the Sequoia image on all nodes"  → Executes caching across your cluster
```

### With Regular Claude (Guidance Only)

When using claude.ai without Claude Code, you'll receive documentation and command explanations:

```
"How do I create VMs?"                  → Explains orka3 vm deploy syntax and options
"What's the command to list images?"    → Shows orka3 image list usage
"Help me plan a CI/CD pipeline"         → Provides step-by-step workflow guidance
"Troubleshoot VM connectivity issues"   → Suggests diagnostic commands to run
```

You'll need to copy the provided commands and run them in your own terminal.

## Skill Contents

| Path | Description |
|------|-------------|
| `skill/SKILL.md` | Main skill definition with core concepts, quick reference, v3.5.2 features, log sources, and documentation guidelines |
| `skill/references/commands/` | Command syntax organized by domain (VM, image, node, admin, config, registry, vm-config) |
| `skill/references/workflows/` | Step-by-step guides for CI/CD, scaling, migration, image prep, admin setup, shared disk config, and getting started |
| `skill/references/troubleshooting/` | Solutions for auth, deployment, image, and network issues |

## Capabilities

### VM Management
- Deploy VMs from local or OCI images
- Configure CPU, memory, and disk resources
- Save and commit VM states to images
- Resize VM disks
- Power operations (Intel: start/stop/suspend/resume)

### Image Management
- List, copy, and delete local images
- Cache images on nodes (Apple Silicon)
- Push images to OCI registries
- Generate empty images for OS installs (Intel)

### Infrastructure
- View and manage cluster nodes
- Tag nodes for workload affinity
- Create and manage namespaces
- Configure access control with rolebindings
- VM shared attached disk configuration (AWS and on-prem)
- Log sources for deep troubleshooting (v3.4+)

### Automation
- Create and manage service accounts
- Generate authentication tokens
- Create VM configuration templates
- Set up CI/CD pipelines

## Architecture Support

| Feature | Intel (amd64) | Apple Silicon (arm64) |
|---------|---------------|----------------------|
| VM Deploy | Yes | Yes |
| Power Operations | Yes | No |
| GPU Passthrough | Yes | No |
| ISO Attach | Yes | No |
| Image Cache | No | Yes |
| OCI Push | No | Yes |

## Building from Source

To build a `.skill` archive locally:

```bash
# Build with an explicit version
./scripts/build-skill.sh 1.2.0

# Or let it use the latest git tag
./scripts/build-skill.sh
```

The archive is written to `dist/orka3-cli-v<VERSION>.skill`.

## Documentation

- [MacStadium Orka Documentation](https://support.macstadium.com/)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Changelog](CHANGELOG.md) - Version history and notable changes

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Support

- For Orka3 CLI issues: [MacStadium Support](https://support.macstadium.com)
- For skill issues: [GitHub Issues](https://github.com/macstadium/orka3-cli-claude-skill/issues)
