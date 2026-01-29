# Orka3 CLI Claude Skill

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill for managing macOS virtual machines with the Orka3 CLI. This skill provides expert guidance for using MacStadium's command-line tool for macOS virtualization infrastructure.

## Features

- Natural language to Orka3 CLI command translation
- VM lifecycle management (deploy, save, delete, resize)
- Image management (local and OCI registries)
- Node operations and tagging
- Namespace and access control (RBAC)
- Service account management for CI/CD
- Troubleshooting guidance

## Prerequisites

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) installed
- Access to an Orka3 cluster
- Orka3 CLI installed (`orka3`)

## Installation

**Option 1: Clone directly (recommended)**

```bash
# Clone directly to the skills directory
git clone https://github.com/macstadium/orka3-cli-claude-skill.git ~/.claude/skills/orka3-cli
```

**Option 2: Manual copy**

```bash
# Clone the repository
git clone https://github.com/macstadium/orka3-cli-claude-skill.git

# Create skills directory and copy skill files
mkdir -p ~/.claude/skills/orka3-cli/references
cp orka3-cli-claude-skill/SKILL.md ~/.claude/skills/orka3-cli/
cp orka3-cli-claude-skill/references/*.md ~/.claude/skills/orka3-cli/references/
```

**Verify installation**

After installation, your skill directory should look like this:

```
~/.claude/skills/orka3-cli/
├── SKILL.md
└── references/
    ├── command-reference.md
    ├── workflows.md
    └── troubleshooting.md
```

Restart Claude Code after installation for the skill to be detected.

## Usage

Once installed, Claude Code will automatically detect the skill when you ask questions about Orka3 or macOS VM management. Example prompts:

```
"Create 3 VMs with macOS Sonoma"
"Show me all running VMs"
"How do I configure VM networking?"
"Set up a CI/CD pipeline with service accounts"
"Cache an image on all nodes"
"Create a namespace for my team"
```

## Skill Contents

| File | Description |
|------|-------------|
| `SKILL.md` | Main skill definition with core concepts and quick reference |
| `references/command-reference.md` | Complete command syntax for all Orka3 CLI operations |
| `references/workflows.md` | Step-by-step guides for common multi-step tasks |
| `references/troubleshooting.md` | Solutions to common issues and error messages |

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

## Documentation

- [MacStadium Orka Documentation](https://support.macstadium.com/)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Support

- For Orka3 CLI issues: [MacStadium Support](https://support.macstadium.com)
- For skill issues: [GitHub Issues](https://github.com/macstadium/orka3-cli-claude-skill/issues)
