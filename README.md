# Claude Skills

A collection of custom skills for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) that extend Claude's capabilities with domain-specific knowledge and workflows.

## What Are Skills?

Skills are markdown-based instruction sets that teach Claude how to handle specialized tasks. When you ask Claude something that matches a skill's triggers, it automatically loads the relevant knowledge and follows proven workflows.

Think of skills as **expert playbooks** — they encode domain expertise, API patterns, best practices, and common pitfalls so Claude can reliably execute complex tasks without hallucinating details.

## Available Skills

| Skill | Description | Triggers |
|-------|-------------|----------|
| [chicago-data-portal](./chicago-data-portal/) | Query Chicago's open data using Socrata/SODA API | "query Chicago data", "find Chicago datasets", "Chicago crime data" |

## Installation

### Option 1: Add to Your Project

Copy the skill folder(s) you want into your project's `.claude/skills/` directory:

```bash
cp -r chicago-data-portal /path/to/your/project/.claude/skills/
```

### Option 2: Global Skills (via Claude Code settings)

Add this repository path to your Claude Code configuration to make skills available across all projects.

## Skill Structure

Each skill follows Claude Code's standard format:

```
skill-name/
├── SKILL.md              # Core instructions (loaded into context)
├── references/           # Detailed docs (loaded on demand)
│   └── *.md
└── examples/             # Code snippets and templates
    └── *.py, *.sh, etc.
```

- **SKILL.md**: The main file with triggers, workflows, and essential knowledge
- **references/**: Deep-dive documentation loaded when Claude needs more detail
- **examples/**: Ready-to-use code that Claude can adapt for the user

## Creating New Skills

1. Create a new folder with your skill name
2. Add a `SKILL.md` with YAML frontmatter:

```yaml
---
name: my-skill
description: This skill should be used when the user asks to "do X", "query Y", or mentions Z.
version: 1.0.0
---

# My Skill

Instructions and workflows...
```

3. Add `references/` and `examples/` as needed
4. Test by asking Claude questions that should trigger the skill

### Best Practices

- **Specific triggers**: Use exact phrases users would say, not vague descriptions
- **Verify, don't assume**: Skills should tell Claude to check APIs/docs rather than guess
- **Include examples**: Real curl commands, code snippets, and expected outputs
- **Document pitfalls**: Common errors, edge cases, and how to handle them

## Contributing

PRs welcome! If you've built a skill that others might find useful:

1. Fork this repo
2. Add your skill folder
3. Update this README's skill table
4. Submit a PR with a description of what the skill does

## License

MIT
