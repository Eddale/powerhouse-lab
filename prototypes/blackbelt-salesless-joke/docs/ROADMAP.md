# Black Belt Salesless Joke - Roadmap

## The Vision

A shareable, memorable way to tell the Salesless story. The interaction IS the message.

**Current state:** Live at https://blackbelt-salesless-joke.vercel.app

---

## Shipped

| Version | Date | What Changed |
|---------|------|--------------|
| v1.1 | 2026-01-09 | Smarter escape algorithm (multi-angle), 2-second explosion delay |
| v1.0 | 2026-01-09 | Initial release - runaway button, karate taunts, explosion modal |

### What V1.1 Does

- Runaway "Book A Call" button with physics animation
- **Multi-angle escape algorithm** - tests 10 angles to find best escape route (inspired by riomadeit/evasive-button)
- 8 karate-themed taunts in iMessage-style bubbles
- Smart edge detection - button slips sideways along edges instead of just bouncing to center
- Exhaustion mechanic - catchable after 10 jumps
- Caught modal with 2-second delayed explosion effect
- CTA links to http://bit.ly/BlackBeltDeets
- Mobile blocker with friendly message
- Consistent Black Belt branding throughout

---

## Planned Improvements

These are on the list - not "someday maybe."

- [ ] **Analytics Integration** - Track how many people catch the button, how many click through to doc
- [ ] **Social Share Button** - "I caught the uncatchable button" shareable moment
- [ ] **Leaderboard** - Fastest catch times (if we add a timer)

---

## Ideas (Not Committed)

Parking lot stuff. Interesting but not proven necessary yet.

- **Sound Effects** - Whoosh on jump, taunt voice lines
- **Difficulty Modes** - Easy (5 jumps), Normal (10), Impossible (never catchable)
- **Multi-language** - Spanish/Portuguese for international coaches
- **Confetti on Catch** - Extra celebration when you finally get it
- **Easter Eggs** - Secret taunts for catching it in specific locations

---

## What We Learned

Building this taught us a few things:

**The physics matter more than you'd think.** Early versions had linear movement - felt robotic. Adding arc motion, squash/stretch, and screen shake made it feel alive. The button has personality now.

**Edge detection is crucial.** Without it, the button gets stuck in corners and the joke dies. The "jump back to center" mechanic keeps the game playable.

**The exhaustion mechanic creates narrative.** Jumps 8-10 telling you it's getting tired transforms a frustrating experience into a satisfying chase with a conclusion.

**Two-second delay on explosion matters.** Immediate reveal felt cheap. The pause creates anticipation, makes the punchline land harder. (Originally 1 second, bumped to 2 for better comedic timing.)

**Single HTML file = instant deploys.** No build step means iterate in 45 seconds. Test live, fix, redeploy.

**Steal algorithms, not libraries.** Found riomadeit/evasive-button with sophisticated multi-angle escape logic. Instead of importing the whole TypeScript package (would need build step), we lifted the core algorithm concept and adapted it. Best of both worlds: smarter behavior, zero dependencies.

---

## The Leverage Asset Pattern

This tool demonstrates the "content as experience" pattern:

1. **Identify the message** → "Sales calls are obsolete, docs work better"
2. **Make it interactive** → Can't book a call because button escapes
3. **Add personality** → Karate taunts match Black Belt brand
4. **Create shareability** → Screenshots of taunts spread organically
5. **Funnel to real CTA** → Only working link is the offer doc

**Replicable for:** Product launches, counter-positioning campaigns, philosophical points that need visceral demonstration.

---

## Decision Log

When we make significant changes, the plan lives in `docs/plans/current.md` and gets archived to `docs/plans/archive/` when complete.

---

## Success Signals

How we know it's working:

- [ ] People share screenshots of the taunts
- [ ] Click-through rate to offer doc is meaningful
- [ ] Taki/Black Belt team thinks it's funny
- [ ] Creates conversation around Salesless methodology

---

## Kill Rules

When to stop and reconsider:

- If joke stops being funny (novelty wore off)
- If it confuses rather than entertains
- If click-through to doc is near-zero (people bounce instead)
- If Black Belt brand team has concerns
