# Newsletter Brainstorm

## What This Does
A conversational writing coach that extracts educational content from your daily experiences and turns it into publish-ready newsletter editions for The Little Blue Report.

## Who It's For
Ed (and eventually Powerhouse members who publish regular content)

## The Problem It Solves
Blank page paralysis. Instead of staring at a cursor, you have a conversation about what you did yesterday—and walk away with headlines, an outline, and a draft.

---

## How To Use

### Quick Start
```
1. Start a conversation (greet the coach or share what you're working on)
2. Answer questions about your recent experiences (one at a time)
3. Choose your audience and headline
4. Walk through the outline section by section
5. Get your draft
```

### Inputs
| Input | Required | Description |
|-------|----------|-------------|
| Your experiences | Yes | What you did, who you talked to, what you learned |
| Audience choice | Yes | Who you want to help (selected from options) |
| Headline choice | Yes | Which of the 10 options resonates |
| Format | Optional | Newsletter, LinkedIn post, article (defaults to newsletter) |

### Outputs
| Output | Description |
|--------|-------------|
| Clarity Statement | The full problem → solution → outcome framework |
| 10 Headlines | Mix of 5 proven headline styles |
| Outline | 4-8 skimmable subheads in the chosen format |
| Expanded sections | Each section developed with your stories and insights |
| Draft | Full content in The Little Blue Report style |

---

## The 7-Phase Process

1. **Get the Actions & Decisions** - Extract what happened through questioning (one question at a time, 3-4 layers deep)
2. **Name an Audience** - Identify who would benefit from this insight
3. **Create the Clarity Statement** - Articulate problem → reason → consequence → outcome
4. **Generate Headlines** - 10 options using 5 proven styles
5. **Generate Outline** - 4-8 skimmable subheads
6. **Expand the Outline** - Develop each section with stories, tips, examples
7. **Write the Content** - Full draft in newsletter format

---

## File Structure

```
newsletter-brainstorm/
├── SKILL.md                          # This file - master documentation
├── prompts/
│   ├── system-prompt.md              # The 7-phase brain
│   └── user-prompt.md                # Opening conversation template
├── artifacts/
│   ├── idea-questions.md             # 10 question categories for extraction
│   ├── outliner.md                   # 5 headline styles + 10 post type formats
│   ├── section-writer.md             # 14 "Magical Ways" to expand sections
│   └── newsletter-format.md          # The Little Blue Report style guide
└── tasks/
    └── todo.md                       # Build log
```

---

## Deploying This Skill

### In a Claude Project
1. Create a new Claude Project
2. Paste the contents of `prompts/system-prompt.md` as the Project Instructions
3. Upload all files from `artifacts/` as Project Knowledge
4. Start chatting

### As a Claude Artifact (Lead Magnet)
1. Use the prompts to build an interactive Artifact in Claude
2. Reference the `newsletter-format.md` for the Substack article about the process

### In Other AI Tools
The prompts are model-agnostic. Adapt the system prompt for ChatGPT, or any LLM that supports system instructions.

---

## Key Design Decisions

**ONE question at a time.** This is the critical differentiator. Most AI tools dump questions. This one has a conversation.

**75% extraction, then move on.** Don't over-extract. Get enough to write, then write.

**Modular artifacts.** Each supporting file can be updated independently without touching the core system prompt.

**Story-driven subheads.** Following The Little Blue Report style - subheads are teases, not descriptions.

---

## Examples

### Example 1: [To be added after first use]

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1 | Dec 2024 | Initial build - prototype |
| 0.2 | Dec 2024 | Full prompt architecture, modular artifacts, 7-phase process |

---

## Notes & Learnings
<!-- What we discovered building this -->

- The "one question at a time" rule is emphasized 3+ times in the original project instructions - it's clearly the make-or-break behavior
- Original project was designed for conversational extraction, not one-shot generation
- Supporting artifacts (Idea Questions, Outliner, Section Writer) are reference materials, not prompts themselves
