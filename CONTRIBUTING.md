# Contributing to Claude Plugins

Thanks for your interest in contributing! This document outlines how to add new plugins or improve existing ones.

## Adding a New Plugin

### 1. Create the Plugin Structure

```bash
mkdir -p my-plugin/{references,examples}
touch my-plugin/SKILL.md
```

### 2. Write Your SKILL.md

Every plugin needs a `SKILL.md` with:

**Required YAML frontmatter:**
```yaml
---
name: my-plugin
description: This skill should be used when the user asks to "specific phrase 1", "specific phrase 2", or mentions specific-topic.
version: 1.0.0
---
```

**Key sections to include:**
- Quick start / overview
- Step-by-step workflow
- Code examples (curl, API calls, etc.)
- Common patterns and gotchas
- Troubleshooting guide

### 3. Add Supporting Files

- `references/*.md` - Detailed documentation (loaded on demand)
- `examples/*.py, *.sh, etc.` - Working code snippets

### 4. Test Your Plugin

1. Copy the plugin to a project's `.claude/plugins/` directory
2. Ask Claude questions that should trigger it
3. Verify Claude follows the workflow correctly
4. Check that examples actually work

### 5. Submit a PR

1. Fork this repo
2. Add your plugin folder
3. Update the README's plugin table
4. Update CHANGELOG.md with your additions
5. Submit a PR with a clear description

## Plugin Quality Guidelines

### Do

- **Verify information**: If your skill references an API, test that endpoints and field names are correct
- **Use specific triggers**: Include exact phrases users would say (e.g., "query X data", "find Y dataset")
- **Provide working examples**: Curl commands, code snippets that actually run
- **Document edge cases**: What happens with empty results, rate limits, auth errors?
- **Keep it focused**: One plugin = one domain/API/workflow

### Don't

- **Guess at APIs**: Always verify endpoints, field names, and response formats
- **Overload context**: Keep SKILL.md concise; put detailed docs in `references/`
- **Ignore errors**: Include troubleshooting for common failure modes
- **Hardcode secrets**: Never include API keys; show placeholder patterns instead

## Versioning

We use [Semantic Versioning](https://semver.org/):

- **PATCH** (1.0.x): Bug fixes, typo corrections, minor clarifications
- **MINOR** (1.x.0): New features, new reference files, new examples
- **MAJOR** (x.0.0): Breaking changes to plugin structure or behavior

## Code of Conduct

Be respectful and constructive. We're all here to make Claude more useful.

## Questions?

Open an issue if you're unsure about anything.
