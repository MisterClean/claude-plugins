# Housing Copywriter

Write authentic, human-sounding marketing copy and pro-housing advocacy messaging. This skill prevents AI-sounding text and applies copywriting best practices.

## Triggers

This skill activates when you ask Claude to:
- "write marketing copy"
- "create social media posts"
- "write a blog post"
- "draft an email"
- "write product descriptions"
- "write ad copy"
- "draft a landing page"

Or for pro-housing content:
- "write about housing"
- "create YIMBY content"
- "draft zoning reform messaging"
- "write about parking reform"
- "write to a politician about housing"

## Installation

Copy this skill folder to your project's `.claude/plugins/` directory:

```bash
cp -r skills/housing-copywriter /path/to/your/project/.claude/plugins/
```

Or clone the entire repo and reference it in your Claude Code settings for global access.

## Usage

Once installed, just ask Claude naturally:

> "Write a tweet thread about why we need more housing near transit"

> "Draft an email to my alderman supporting the zoning change"

> "Write product copy for our new feature launch"

Claude will automatically apply the copywriting guardrails to produce clear, authentic writing that doesn't sound AI-generated.

## Contents

| File | Description |
|------|-------------|
| [SKILL.md](./SKILL.md) | Core copywriting principles and workflow |
| [references/avoid-list.md](./references/avoid-list.md) | Words and phrases to avoid |
| [references/pro-housing-messaging.md](./references/pro-housing-messaging.md) | Housing advocacy messaging guide |

## Key Principles

1. **Specificity over generality** - Replace abstract claims with concrete details
2. **Cut ruthlessly** - Delete filler words; one strong sentence beats three weak ones
3. **Write like you talk** - If it sounds stiff, rewrite it
4. **Show, don't announce** - Don't say "we're excited to announce"—just announce it
5. **Earn every adjective** - Strip all adjectives, add back only essential ones

## Resources

- [Main Repository](../../README.md)
