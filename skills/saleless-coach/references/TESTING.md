# Testing Plan for saleless-coach

## Pre-flight Checks
- [ ] Skill appears in `.claude/skills/` symlinks
- [ ] Skill registered in `settings.local.json`
- [ ] New terminal session started (settings refresh)

## Skill Discovery Test
- [ ] Run: "What skills are available?"
- [ ] Expected: saleless-coach appears in list with correct description

## Basic Invocation Test
- [ ] Run: "How does the Salesless approach work?"
- [ ] Expected: Skill activates, explains Doc/Demand/Deadline and 90-day experiment

## Framework Tests

### Context Fulcrum
- [ ] Input: "Explain the Context Fulcrum"
- [ ] Expected: Mentions Hutto, explains seesaw (Disbelief + Price vs Offer + Sales Ability), emphasizes Brand as the fulcrum

### Offer Diamond
- [ ] Input: "What's the Offer Diamond?"
- [ ] Expected: Lists all 5 components (Promise, Guarantee, Bonuses, Pay Plan, Urgency/Scarcity)

### Weekly Email Campaign
- [ ] Input: "How do I write a weekly email campaign?"
- [ ] Expected: Describes 5 emails (Announcement, Problem, Proof, Philosophy, Plan)

### System 2025
- [ ] Input: "What's the full Salesless system?"
- [ ] Expected: Covers Attract → Nurture → Convert → Deliver with specific components

## Edge Case Tests

### Open-ended coaching question
- [ ] Input: "Should I go salesless?"
- [ ] Expected: Does NOT prescribe one path - explains it depends on preferences

### Comparison question
- [ ] Input: "What's the difference between the Offer Doc and the Offer Diamond?"
- [ ] Expected: Doc is the vehicle/format, Diamond is the content framework

## Integration Test
- [ ] If offer-diamond-review skill exists, verify they complement each other
- [ ] Test: "Review my offer using the Offer Diamond framework"
