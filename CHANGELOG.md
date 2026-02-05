# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-02-05

### Added

- Documentation & Troubleshooting Guidelines section in `SKILL.md` with:
  - CLI patterns: Use built-in filtering instead of piping to grep
  - CI/CD authentication: Always use service accounts, never user tokens
  - Environment variables: Must be in CI/CD settings, not shell export
  - Network connectivity: Use curl to `/api/v1/cluster-info`, avoid ping
  - Troubleshooting structure: Trust CLI errors, understand execution context
  - Example patterns for SSH troubleshooting in CI/CD environments

### Security

- Updated OCI registry credential examples to use environment variables instead of inline tokens
- Updated VM resize examples to use environment variables for credentials
- Added security notes explaining that MacStadium base images use default credentials (`admin`/`admin`) which should be changed for production

### Documentation

- Added "Problem-Solving Approach" section with guidelines:
  - Define the problem first - push back on vague requests
  - Map the user journey before jumping to solutions
  - For Orka integrations: READ THE REPO ARCHITECTURE FIRST
  - Design/stub before implementing
  - Verify context and source of truth
  - Humans review every output

- Added "Pre-Flight Checklist for Documentation" with verification steps:
  - Problem definition and scope
  - Read the integration code first
  - Authentication patterns (service accounts only for CI/CD)
  - CLI patterns (no grep, use built-in filtering)
  - Execution context awareness
  - Content structure (one approach per problem)
  - Security (no hardcoded credentials)
  - Coherence check (cascade through all sections)

## [1.0.0] - 2025-01-29

### Added

- Initial release of the Orka3 CLI Claude Skill
- Main skill definition (`SKILL.md`) with:
  - Core concepts (architecture types, components, authentication)
  - Getting started workflow
  - Quick VM operations reference
  - Image management commands
  - VM lifecycle operations
  - VM configuration templates
  - Node management
  - Namespace management
  - Access control (RBAC)
  - Common workflow summaries
  - Command patterns and flags
  - Architecture-specific features
  - Best practices

- Complete command reference (`references/command-reference.md`) with:
  - Configuration commands
  - Authentication commands
  - Service account commands
  - Image commands
  - Image cache commands (Apple Silicon)
  - OCI registry commands
  - VM commands (deploy, list, delete, save, commit, push, resize, power ops)
  - VM configuration commands
  - Node commands
  - Namespace commands
  - RBAC commands
  - Utility commands

- Workflow documentation (`references/workflows.md`) with:
  - Initial setup workflow
  - CI/CD pipeline setup
  - Custom image preparation
  - Multi-namespace team setup
  - Image caching for fast deployments
  - OCI registry integration
  - Scaling VMs for load testing
  - VM disk management
  - Node affinity and tagging strategy
  - Disaster recovery and backup
  - Troubleshooting deployment issues
  - Migration from Intel to Apple Silicon
  - Resource optimization

- Troubleshooting guide (`references/troubleshooting.md`) with:
  - Authentication issues
  - VM deployment issues
  - Image management issues
  - Namespace and access issues
  - Network and connectivity issues
  - Performance issues
  - Common error messages
  - Prevention tips

### Features

- Natural language to Orka3 CLI command translation
- Support for both Intel (amd64) and Apple Silicon (arm64) architectures
- VM lifecycle management
- Image management (local and OCI)
- Node operations and tagging
- Namespace and RBAC management
- Service account management for CI/CD automation
