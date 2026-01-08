# Black Belt Salesless Joke

A parody landing page celebrating Black Belt's "Salesless" experiment - where Taki Moore fired his 9-person sales team and now signs new members purely through documents.

## Live URL

**Production:** https://blackbelt-salesless-joke.vercel.app

## What It Does

A "Book A Call" button that literally runs away from your cursor. After 10 escapes, the button gets tired and lets you catch it - revealing a modal that redirects to the actual offer document.

## Tech Stack

- Single HTML file (no build step)
- Vanilla JavaScript for animations
- CSS animations for particles/explosions
- Hosted on Vercel

## File Structure

```
blackbelt-salesless-joke/
├── index.html          # Main page - everything in one file
├── assets/
│   ├── logo.png        # Black Belt logo (black version)
│   └── logo-white.png  # Black Belt logo (white version)
├── README.md           # This file
├── HOW-IT-WORKS.md     # Business-friendly explanation
└── docs/
    ├── ROADMAP.md      # Future ideas
    └── plans/          # Improvement plans
```

## Key Features

1. **Runaway Button** - Escapes when cursor gets within 140px
2. **Physics Animation** - Arc motion with squash/stretch
3. **Karate Taunts** - iMessage-style bubbles with Black Belt themed messages
4. **Edge Detection** - Button jumps back to center when near edges
5. **Exhaustion Mechanic** - After 10 jumps, button surrenders
6. **Caught Modal** - Explosion effect reveals CTA after 1 second delay
7. **Mobile Blocker** - Friendly message for mobile users (requires mouse)

## Branding

- **Primary:** Gold (#fabf19)
- **Dark:** Black (#0A0A0A)
- **Font:** DM Sans
- **Tone:** Playful, anti-sales-pressure, karate/martial arts themed

## Links

- **Offer Document:** http://bit.ly/BlackBeltDeets
- **Inspiration:** didicook-studio.vercel.app (original runaway button concept)

## Deployment

```bash
vercel --prod
```

## Local Development

```bash
cd prototypes/blackbelt-salesless-joke
python3 -m http.server 8765
# Open http://localhost:8765
```
