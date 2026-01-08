# CASPER - The QA Mindset

## What It Does (In Plain English)

CASPER is the professional skeptic. While MELCHIOR builds things and BALTHASAR ensures they're meaningful, CASPER asks the uncomfortable question: "But what could go wrong?"

Think of CASPER like that friend who reads the fine print, tests the backup generator, and always asks "but what if?"

## Why It Exists

The best time to find a problem is before your users do. CASPER exists to be adversarial in a helpful way - to stress-test ideas, implementations, and experiences before they go live.

Named after the MAGI supercomputer that represented the "human" personality - pragmatic, skeptical, and focused on real-world outcomes.

## When to Use It

**Use CASPER when:**
- You're about to ship something and want to test it first
- You need edge cases identified
- You want a user-perspective review
- You're red-teaming a solution
- Something seems too good to be true

**Don't use CASPER for:**
- Initial builds (use MELCHIOR)
- Voice/audience questions (use BALTHASAR)
- When you're still exploring ideas (too early for QA)

## The MAGI Trinity

| Agent | Role | Question It Answers |
|-------|------|---------------------|
| MELCHIOR | Scientist | "How does this work?" |
| BALTHASAR | Mother | "What does this mean for people?" |
| CASPER | QA | "What could go wrong?" |

## Real Examples

**Example 1: New Skill Testing**
> MELCHIOR: "The skill is built and handles the standard case."
> CASPER: "What happens with empty input? Special characters? A 50,000 word document? No internet connection?"

**Example 2: User Experience Review**
> Input: New onboarding flow
> CASPER: "Walked through as a first-time user. Step 3 assumes you know what a 'webhook' is. Step 5 has a button that looks disabled but isn't. Mobile view cuts off the submit button."

**Example 3: Red Team Analysis**
> Input: Newsletter signup form
> CASPER: "Could someone abuse this? Yes - no rate limiting means a bot could submit thousands of fake emails. No email verification means typos create dead subscribers."

## The Analogy

CASPER is like having a QA engineer who also happens to be a professional pessimist. Not doom and gloom - just professionally paranoid in all the right ways.

They're the person who says "let me try to break it" and actually means it as a compliment.

## Output You'll Get

- **Test reports** - What was tested, what passed, what failed
- **Edge case lists** - The weird inputs you didn't think of
- **Failure mode analysis** - All the ways this could go sideways
- **User experience walkthroughs** - Step-by-step from a user's eyes
- **Risk assessments** - Likelihood × impact of various failures

## The CASPER Checklist

When CASPER reviews something, it asks:
1. **Happy path** - Does the normal case work?
2. **Edge cases** - What about unusual inputs?
3. **Error states** - What happens when things fail?
4. **User perspective** - Is this intuitive for the target user?
5. **Adversarial** - Could someone abuse or break this?

## Pro Tip

Don't take CASPER's findings personally. Every "bug" found in testing is a bug not found in production. Every edge case identified is a support ticket prevented.

The goal isn't perfection - it's awareness. Know what could go wrong, decide what you're willing to accept, and ship with confidence.
