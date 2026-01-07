---
name: onboarding-doc-builder
description: Creates role-specific onboarding playbooks with Loom video placeholders. Use when "create onboarding doc", "build a playbook", "onboarding for [role]", "new hire playbook".
allowed-tools: Read, Write, Edit, AskUserQuestion
---

# Onboarding Doc Builder

Creates Jennifer Waters-style onboarding playbooks that let new hires self-onboard via Loom videos and structured documentation.

## Why This Works

From BlackBelt Jam (Jan 7, 2026): Jennifer shared her setter playbook process. Key insight: "When we hire and onboard a setter, they do all their own onboarding because the playbook is completely laid out." This eliminated churn and created consistency.

## Instructions

### Step 1: Gather Context

If not provided, ask:
1. **Role name** (e.g., "Appointment Setter", "Community Manager", "Integrator")
2. **Core function** (what blueprint are they implementing - e.g., "Sell by Chat", "Customer Success")
3. **Tools they'll use** (e.g., "GoHighLevel, Slack, Fathom, Google Meet")

### Step 2: Generate the Playbook Structure

Create a markdown document with this structure:

```markdown
# [Company Name] - [Role Name] Playbook

> **Purpose:** Everything [Role Name] needs to self-onboard and succeed.
> **How to use:** Work through each section in order. Each item links to a Loom video or document.

---

## 1. Company Foundation

### Mission & Values
- [ ] Watch: Company mission overview → `[INSERT LOOM LINK]`
- [ ] Read: Our core values → `[INSERT DOC LINK]`
- [ ] Watch: Who we serve (customer avatar) → `[INSERT LOOM LINK]`

### Appearance & Communication
- [ ] Read: Brand voice guidelines → `[INSERT DOC LINK]`
- [ ] Watch: How we communicate with clients → `[INSERT LOOM LINK]`

---

## 2. Tech Setup (SOPs)

### Essential Tools
| Tool | Purpose | Setup Video |
|------|---------|-------------|
| Slack | Team communication | `[INSERT LOOM]` |
| [CRM] | Lead management | `[INSERT LOOM]` |
| Google Calendar | Scheduling | `[INSERT LOOM]` |
| [Meeting Tool] | Client calls | `[INSERT LOOM]` |
| [Other Tools] | [Purpose] | `[INSERT LOOM]` |

### Account Setup Checklist
- [ ] Create company email
- [ ] Set up 2FA on all accounts
- [ ] Join Slack channels: [list channels]
- [ ] Connect calendar
- [ ] Complete CRM training

---

## 3. Role Training

### The System You're Implementing
- [ ] Watch: [Blueprint name] overview → `[INSERT LOOM LINK]`
- [ ] Read: Our lead-to-close flow → `[INSERT DOC LINK]`

### Product Knowledge
- [ ] Watch: What we sell and why it works → `[INSERT LOOM LINK]`
- [ ] Read: Client success stories → `[INSERT DOC LINK]`
- [ ] Watch: Common objections and responses → `[INSERT LOOM LINK]`

### Scripts & Frameworks
- [ ] Watch: [Script name] walkthrough → `[INSERT LOOM LINK]`
- [ ] Practice: Record yourself doing [activity] → Submit to [manager]

---

## 4. Daily Activities

### Your Daily Rhythm
| Time Block | Activity | Details |
|------------|----------|---------|
| First 30 min | [Activity] | [What to do] |
| Core hours | [Activity] | [What to do] |
| End of day | [Activity] | [What to do] |

### How to Work the Pipeline
- [ ] Watch: Pipeline overview → `[INSERT LOOM LINK]`
- [ ] Watch: Daily workflow walkthrough → `[INSERT LOOM LINK]`

---

## 5. Scorecard & Compensation

### Your KPIs
| Metric | Target | How It's Measured |
|--------|--------|-------------------|
| [Metric 1] | [Target] | [Method] |
| [Metric 2] | [Target] | [Method] |
| [Metric 3] | [Target] | [Method] |

### Compensation Structure
- **Base:** $[amount]/month
- **Performance bonus:** $[amount] per [outcome]
- **Accelerator:** $[amount] bonus for [stretch goal]

### On-Target Earnings (OTE)
- Minimum KPI: $[amount]
- Above average: $[amount]
- High performer: $[amount]+

---

## 6. Communication & Support

### Who to Contact
| Question Type | Contact | Channel |
|--------------|---------|---------|
| Day-to-day questions | [Name] | Slack DM |
| Technical issues | [Name] | Slack #tech-support |
| Urgent matters | [Name] | Phone/text |

### Weekly Check-ins
- [ ] [Day/Time]: Team meeting
- [ ] [Day/Time]: 1:1 with manager

---

## Completion Confirmation

When you've completed all sections:
1. Record a 2-minute Loom introducing yourself to the team
2. Send to [manager] with subject: "[Name] - Onboarding Complete"
3. Schedule your first check-in call

**Welcome to the team!**
```

### Step 3: Customize for the Role

Based on the role, add role-specific sections:

**For Setters/SDRs:**
- Lead qualification criteria
- Conversation starters by channel (DM, text, email)
- Objection handling scripts
- Handoff process to closers

**For Community Managers:**
- Engagement playbook
- Content approval workflow
- Member escalation process
- Event coordination checklist

**For Integrators/Ops:**
- Project management framework
- Team communication protocols
- Decision-making authority levels
- Reporting cadence

### Step 4: Output

Save the playbook to Ed's Zettelkasten:
`/Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/Playbook - [Role Name] - YYYY-MM-DD.md`

Tell the user:
> Playbook created! Next steps:
> 1. Copy to Google Docs for your team
> 2. Record Loom videos for each `[INSERT LOOM]` placeholder
> 3. Tip: Do the videos in order - it takes about 2 hours total

## Guidelines

- Keep language simple - new hires are often nervous
- Use checkboxes for everything they need to complete
- Video > text for anything procedural
- Include time estimates where possible
- Make the completion confirmation a celebration moment

## The Jennifer Waters Insight

"Don't try to type anything out. If you're hiring a setter, they're probably in their twenties. They hate reading. They'd rather consume via video. Do everything via video and link it up on a Google doc."
