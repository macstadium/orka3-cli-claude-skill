# Contributing to Orka3 CLI Claude Skill

Thank you for your interest in contributing to the Orka3 CLI Claude Skill! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion for improvement:

1. Check existing [GitHub Issues](https://github.com/macstadium/orka3-cli-claude-skill/issues) to see if it's already reported
2. If not, create a new issue with:
   - A clear, descriptive title
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Your environment (Claude Code version, Orka3 CLI version)

### Suggesting Improvements

We welcome suggestions for:

- New command examples
- Additional workflow documentation
- Improved troubleshooting guidance
- Better natural language patterns
- Documentation clarifications

Please open an issue to discuss your idea before submitting a pull request.

### Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Test the skill locally by copying to `~/.claude/skills/orka3-cli`
5. Commit your changes with a clear message
6. Push to your fork
7. Open a pull request

### Pull Request Guidelines

- Keep changes focused and atomic
- Update documentation if adding new features
- Follow existing formatting and style
- Add examples where appropriate
- Test your changes with Claude Code

## File Structure

When contributing, understand the purpose of each file:

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition - core concepts, quick reference |
| `references/command-reference.md` | Complete CLI syntax documentation |
| `references/workflows.md` | Multi-step task guides |
| `references/troubleshooting.md` | Problem diagnosis and solutions |

## Style Guidelines

### Markdown

- Use ATX-style headers (`#`, `##`, `###`)
- Use fenced code blocks with language hints (```bash)
- Keep lines under 100 characters when practical
- Use consistent indentation (2 spaces)

### Code Examples

- Always test commands before documenting
- Include both common and advanced usage
- Show expected output where helpful
- Note architecture-specific commands (Intel vs Apple Silicon)

### Documentation

- Write in clear, concise English
- Use active voice
- Explain the "why" not just the "how"
- Include practical examples

## Testing Changes

Before submitting a pull request:

1. Copy the skill to your Claude Code skills directory:
   ```bash
   cp -r . ~/.claude/skills/orka3-cli
   ```

2. Test with Claude Code by asking questions like:
   - "How do I deploy a VM with Orka3?"
   - "Show me how to set up CI/CD"
   - "What's the command to cache images?"

3. Verify the skill provides accurate, helpful responses

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy toward other contributors

### Unacceptable Behavior

- Harassment or discriminatory language
- Personal attacks
- Publishing others' private information
- Other unprofessional conduct

### Enforcement

Project maintainers may remove, edit, or reject contributions that don't align with this Code of Conduct.

## Questions?

If you have questions about contributing:

- Open a GitHub issue for project-related questions
- Contact [MacStadium Support](https://support.macstadium.com) for Orka3-specific questions

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.
