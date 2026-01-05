# Skill Testing Checklist

Use this checklist when building or modifying skills. Copy to your skill's folder or reference
during development.

---

## Level 1: Structure Validation

- [ ] SKILL.md exists with valid YAML frontmatter
- [ ] `name:` matches folder name (kebab-case)
- [ ] `description:` includes trigger phrases users would say
- [ ] `allowed-tools:` lists only actual tools needed (Read, Write, Edit, Glob, Grep, Bash, WebFetch, WebSearch)
- [ ] No skills listed in allowed-tools (skills chain via instructions, not permissions)

## Level 2: Registration Check

- [ ] Symlinks created: `./scripts/setup-skills.sh`
- [ ] Registered in `.claude/settings.local.json`: `"Skill(skill-name)"`
- [ ] New terminal session started (Claude Code caches definitions)

## Level 3: Functional Test

- [ ] Trigger phrase invokes skill correctly
- [ ] Output format matches SKILL.md specification
- [ ] Error handling works (test with bad input)
- [ ] Integration points work (chained skills invoke correctly)

## Level 4: Documentation

- [ ] Examples in SKILL.md are accurate and current
- [ ] Edge cases documented
- [ ] Version History updated with changes

---

## Test Cases Template

Copy this section to your SKILL.md if needed:

```markdown
## Test Cases

| Input | Expected Output | Pass/Fail |
|-------|-----------------|-----------|
| [trigger phrase 1] | [expected behavior] | |
| [trigger phrase 2] | [expected behavior] | |
| [bad input] | [error handling] | |
```

---

## Agent Testing Addendum

When building agents (`.claude/agents/*.md`), also verify:

- [ ] All skills in `skills:` list are registered in settings.local.json
- [ ] Agent has tools required by referenced skills in its `tools:` list
- [ ] Prompt produces expected workflow
- [ ] Edge cases documented

---

## Graduation Path

```
Manual Checklist (Now)
    ↓
Git Hook Validation (Week 3-4)
    ↓
Subagent Reviewer (Month 2)
    ↓
GitHub Actions + Playwright (Month 3+)
```

---

## Quick Reference: Common Failures

| Symptom | Cause | Fix |
|---------|-------|-----|
| Skill doesn't trigger | Not in settings.local.json | Add `"Skill(name)"` to permissions.allow |
| "Tool not available" error | Agent missing required tool | Add tool to agent's `tools:` frontmatter |
| Skill works in CLI, fails in Claude.ai | Sandbox restrictions | Add MCP fallback or manual paste option |
| Changes don't take effect | Session caching | Start new terminal session |

---

*Based on Research - Claude Code Testing Infrastructure - 2026-01-06*
