# MAGI System Design v2.0

**Core Philosophy**: "Plan, Do, Review" (PDR) Loop.
Every significant task passes through this cycle to ensure quality and constant improvement of our skills.

## 🧠 The Agent Archetypes (The "Three Wise Men")

| Agent | Archetype | Role & Focus |
| :--- | :--- | :--- |
| **MELCHIOR** | The Scientist | **Logic & Tools**. Handles GHL (GoHighLevel) APIs, code structure, file organization, and specific implementations. |
| **BALTHASAR** | The Mother | **Context & Brand**. Coaching voice, empathy, brand guidelines (fonts/logos/tone), and human connection. |
| **CASPER** | The Woman | **QA & QA**. Testing *everything*. From red-teaming skills to verifying landing pages. The "User Proxy". |

## 🔄 The PDR Operational Loop
For any request (e.g., "Create Landing Page"), the workflow is:

1.  **PLAN (Context & Architect)**
    *   **Balthasar** gathers context (Brand voice, target audience).
    *   **Melchior** outlines the structure (GHL funnel steps, required assets).
    *   *Human Checkpoint (You)*: Approve the plan.

2.  **DO (Execution)**
    *   **Melchior** builds the funnel/script using GHL APIs.
    *   **Balthasar** writes the copy using the `brand-synthesizer` skill.

3.  **REVIEW (Verification)**
    *   **Casper** tests the page/funnel. Clicks all links, checks mobile view.
    *   **The Learner**: We extract "What went wrong?" to upgrade the underlying `SKILL.md`.

## 📋 Task Breakdown & Skill Mapping

| Task Category | Owner | Skill Needed | Notes |
| :--- | :--- | :--- | :--- |
| **Inbox Processing** | Melchior | `inbox-listener` | Watches `../Zettelkasten/YYYY-MM-DD.md` for tags. |
| **Offer/Model Creation** | Melchior | `skill-extractor` | **PRIORITY 1**. Turns chat logs -> `SKILL.md`. |
| **GHL / CMM Setup** | Melchior | `ghl-architect` | Requires GHL API knowledge. Melchior acts as DevOps. |
| **Video/Scenes** | Hybrid | `media-editor` | "Scene Generation" with VEO. Melchior indexes, You create. |
| **Brand/Design** | Balthasar | `brand-synthesizer` | Evolving doc. Fonts, Voice, Visuals. |
| **Daily Learning** | Melchior | `knowledge-gardener` | Extract insights from AI chats -> Zettelkasten daily. |

## 🛠️ The "Skill Extractor" (First Build)
**Goal**: Turn your "Offer Diamond" and "Triangle Model" chats into reusable skills.

**Input**:
-   A chat export (PDF or Markdown) where you discussed the model.
-   Your notes on the "Key Steps".

**Process**:
1.  **Plan**: Analyze the chat to find the "Algorithm" of the thought process.
2.  **Do**: Write a `SKILL.md` prompt that replicates that thinking.
3.  **Review**: Run a *new* idea through the skill to see if it acts like you.

## ❓ Open Questions for Ed
1.  **GHL Access**: Do we have an API Key or do you use the web UI for Go High Level? (Planning the `ghl-architect` skill).
2.  **Brand Assets**: Do you have a starting "Brand Guide" PDF or doc, or are we building Balthasar's brain from scratch?
