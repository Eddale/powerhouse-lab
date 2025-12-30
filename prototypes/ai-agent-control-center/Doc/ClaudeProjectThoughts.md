# ClaudeProjectThoughts.md
> Living document for AI Agent Control Center brainstorming

---

## THE BIG IDEA

**What we're building:** A "Personal AI Operating System" - the central hub for managing multiple autonomous AI agents that work in Obsidian, pull skills from GitHub, and report back.

**The headline version:**
> One dashboard. Multiple agents. Zero chaos.

**Why this matters:**
- Right now: Agents scattered, no central view, context lost between sessions
- After this: Centralized command, standardized triggers, scalable to any number of agents

**The Core Mindset:**
> "Is there a way I can substantially move the ball on this todo
> while keeping Ed in the loop?"

This isn't about AI doing everything autonomously. It's about:
1. **Clarify** - Flag what's unclear, suggest what's missing
2. **Rewrite** - Make tasks agentic-ready (with approval, modify the actual file)
3. **Plan** - Show Ed what could be done before doing it
4. **Do** - Execute with approval
5. **Learn** - Capture what worked

**Measure twice, cut once.** The agent's job is to make the cutting easy.

---

## LEVERAGE OPPORTUNITIES

What this enables (map to the Triangle Model):

| Opportunity | Leverage Created |
|-------------|------------------|
| Agent Inbox | Drop task → agent picks it up → you move on |
| Active Agents Dashboard | See what's running without context-switching |
| Skill Dispatcher | Right skill, right agent, automatic routing |
| Manager Agent | Orchestrates the others - you talk to one, it coordinates many |

**Riskiest assumption to test first:**
- Can agents reliably pick up tasks from a markdown inbox?
- Or does this need more infrastructure?

---

## OPEN QUESTIONS

Strategic questions to resolve:

1. **Agent Discovery:** How does the Manager know which agents exist?
   - Hardcoded list?
   - Scan a folder?
   - Skills define which agent handles them?

2. **State Persistence:** Where does agent state live between sessions?
   - In Obsidian notes?
   - In a separate JSON file?
   - In the skill itself?

3. **Error Handling:** When an agent fails, who catches it?
   - Manager retries?
   - Escalate to human?
   - Log and move on?

4. **Integration with Skills Architecture:**
   - Does this live inside the portable skills system?
   - Or is it a separate "orchestration layer" above skills?

5. **Agent vs Sub-agent terminology:**
   - In Claude Code: Both are Task tool invocations
   - Main agent: The scanner that reads and suggests
   - Sub-agent: Spawned for specific deep work (research, execution)
   - For now: Keep it simple - one skill, one job

---

## IDEAS PARKING LOT

Quick captures - add here as ideas surface:

### Promoted to MVP
- [x] **Task Clarity Scanner skill** - Scan daily file → flag unclear → suggest rewrite → **modify file with approval**

### Future Ideas
- [ ] **Idea:** "Research this" sub-agent - triggered by hybrid approval when scanner flags unknowns
- [ ] **Idea:** Someday/Maybe file - park tasks you don't want today, agent reviews periodically
- [ ] **Idea:** Agent templates (like the skill template) for spinning up new agents fast
- [ ] **Idea:** "Agent Heartbeat" - periodic status checks so you know what's alive
- [ ] **Idea:** "Task Handoff" protocol - how one agent passes work to another
- [ ] **Idea:** "Agent Memory" - persistent context that survives session restarts
- [ ] **Idea:** Visual status board (could be a simple Obsidian dashboard)
- [ ] **Idea:** Standalone tool version (graduation path from prototype → own repo)

---

## DECISIONS LOG

| Date | Decision | Why |
|------|----------|-----|
| 2025-12-30 | Started with Doc folder for thoughts | Keep brainstorming organized, separate from task tracking |
| 2025-12-30 | MVP: Task Clarity Scanner skill first | Prove the scan/flag/suggest/rewrite loop before adding complexity |
| 2025-12-30 | Scanner can rewrite tasks AND modify the file | Real leverage = actually fixing, not just flagging |
| 2025-12-30 | Hybrid trigger for future research sub-agents | Scanner suggests research, Ed approves - keeps human in the loop |
| 2025-12-30 | Use new-skill-wizard when building skills | Dogfood our own tools |

---

## KILL RULES

When to pivot away from this prototype:

- [ ] 3+ loops on the same integration bug (Obsidian ↔ GitHub)
- [ ] 90 minutes trying to get basic agent communication working
- [ ] The "simple inbox" pattern turns into a complex queue system
- [ ] Energy drops and it feels like fighting the tools

**If killed:** Capture what worked, archive with postmortem, extract any reusable pieces to skills/
