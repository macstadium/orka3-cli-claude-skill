# Archived Reference Files

This directory contains the original monolithic reference files that have been split into smaller, focused documents for better performance and organization.

## Archived Files

| Original File | Replacement Files |
|---------------|-------------------|
| `command-reference.md` | `commands/vm-commands.md`, `commands/image-commands.md`, `commands/registry-commands.md`, `commands/admin-commands.md`, `commands/node-commands.md`, `commands/config-commands.md`, `commands/vm-config-commands.md` |
| `workflows.md` | `workflows/getting-started.md`, `workflows/cicd-workflows.md`, `workflows/image-workflows.md`, `workflows/admin-workflows.md`, `workflows/scaling-workflows.md`, `workflows/migration-workflows.md` |
| `troubleshooting.md` | `troubleshooting/auth-issues.md`, `troubleshooting/deployment-issues.md`, `troubleshooting/image-issues.md`, `troubleshooting/network-issues.md` |

## Why Files Were Split

The original files were split to:
1. **Improve performance** - Smaller files load faster and reduce token usage
2. **Better organization** - Content is grouped by domain and topic
3. **Easier maintenance** - Updates can be made to specific areas without affecting others
4. **Focused context** - Claude can load only the relevant reference for a given query

## Using the New Structure

Instead of loading the full reference files, load only the specific file needed:
- For VM commands: `references/commands/vm-commands.md`
- For authentication issues: `references/troubleshooting/auth-issues.md`
- For CI/CD setup: `references/workflows/cicd-workflows.md`

## Note

These archived files are kept for reference and backup purposes. The active documentation is in the parent directories:
- `references/commands/`
- `references/workflows/`
- `references/troubleshooting/`
