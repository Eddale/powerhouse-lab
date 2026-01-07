# How the Playbook Generator Works
## A Guide for the Vibe Coder

---

## The One-Sentence Version

Fill out a form, Claude writes the playbook, download as Word doc.

---

## Why This Exists

Every time you onboard someone new into a coaching business, they need a playbook. Not just "here's your login" but a proper "here's how we do things here" document.

Writing these manually takes hours. You're copying from old docs, updating names, changing tools, reformatting tables... it's grunt work that doesn't need a human brain.

**This tool does it in 30 seconds.**

---

## The User Experience

### Step 1: Fill the Form (30 seconds)
- Company name
- Role they're hiring for
- What core function (sales, support, community, etc.)
- Which tools they use (GHL, Slack, Zoom, etc.)
- Who's their manager
- Where to post wins

### Step 2: Click Generate
- Loading animation plays
- Claude writes the playbook in the background
- Takes about 10-15 seconds

### Step 3: Download
- Preview the markdown on screen
- Copy to clipboard (top right button)
- Download as Word doc (DOCX) - properly formatted with tables, headers, page breaks
- Download as Markdown - for Notion, Obsidian, etc.

---

## The Architecture (In Human Terms)

Think of it like a mail merge for onboarding docs.

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   FORM      │────▶│   CLAUDE    │────▶│  DOWNLOAD   │
│  (inputs)   │     │  (writer)   │     │  (outputs)  │
└─────────────┘     └─────────────┘     └─────────────┘
```

**Form = Your merge tags.** Company name, role, tools - all the variable bits.

**Claude = Your copywriter.** Given a detailed prompt template and your inputs, writes a complete playbook.

**Download = Your delivery.** Converts Claude's markdown output into a properly formatted Word doc.

---

## The Prompt Template (The Secret Sauce)

Claude doesn't just make stuff up. It follows a detailed prompt that says:

> "Write an onboarding playbook in Jennifer Waters' style. Include these sections: Welcome, Company Foundation, Tech Setup, Role Training, Daily Activities, Scorecard, Communication, Completion Checklist. Use markdown formatting with headers, tables, and checkboxes."

The prompt is ~2000 words of instructions. It's specific about:
- Tone (professional but warm)
- Structure (exact sections in exact order)
- Formatting (H2 for sections, H3 for subsections, tables for schedules)
- Content (what to include in each section)

**To change what playbooks look like**, you edit this prompt template in the API route file.

---

## The DOCX Magic

The tricky part wasn't getting Claude to write - it was getting Word to look right.

Claude outputs markdown:
```
## Welcome
| Tool | Purpose |
|------|---------|
| GHL  | CRM     |
```

But Word needs actual Word formatting. So the app:

1. **Parses the markdown** - Finds headers, tables, checkboxes, bullets
2. **Converts to Word objects** - H2 becomes Heading 2, `| table |` becomes a real Word table
3. **Adds page breaks** - Each major section (## heading) starts on a new page
4. **Packages as DOCX** - Downloads as a real Word doc you can edit

---

## Where Everything Lives

```
blackbelt-playbook-generator/
│
├── app/                      # The actual web app
│   └── src/app/
│       ├── page.tsx         # The UI - form, loading, preview screens
│       ├── api/generate/    # The API that talks to Claude
│       └── opengraph-image  # The social preview image
│
├── assets/                   # Logos and brand stuff
└── README.md                # Technical docs
```

**page.tsx** - All the visual stuff. Form fields, buttons, animations, the preview pane.

**api/generate/route.ts** - The backend. Takes form inputs, builds the prompt, calls Claude, returns the playbook.

**opengraph-image.tsx** - What shows up when you share the link on LinkedIn/Twitter.

---

## Hosting on Vercel

The app runs on Vercel's free tier. When you visit the URL:

1. Vercel serves the page (static HTML + React)
2. You fill the form
3. Form submits to the API route (server-side)
4. API route calls Claude (needs the API key)
5. Playbook comes back
6. Word doc generates in your browser (client-side)

**The API key lives on Vercel**, not in your browser. That's important - it means the key stays secret.

---

## Cost

- **Claude API:** ~$0.01 per playbook
- **Vercel hosting:** Free (100k requests/month)
- **Running this for BlackBelt:** Maybe $10/month if heavily used

---

## Making Changes

### To change the playbook content/style:
Edit the prompt template in `app/src/app/api/generate/route.ts`

### To change the form fields:
Edit `app/src/app/page.tsx` (search for "FormData")

### To change the look:
Edit `app/src/app/globals.css` or the Tailwind classes in page.tsx

### To deploy changes:
```bash
cd prototypes/blackbelt-playbook-generator/app
npx vercel --prod
```

---

## What's NOT In V1

- **No accounts** - Anyone with the link can use it
- **No saving** - Generate, download, done
- **No editing** - Download and edit in Word
- **No Google Docs** - Just DOCX and Markdown
- **No custom branding** - BlackBelt branding only

These could all be added later. V1 is about shipping something useful fast.

---

## The Pattern This Demonstrates

This is a **Leverage Asset** - a tool that does the lifting.

The pattern:
1. **Identify grunt work** - Writing onboarding docs manually
2. **Template it** - Create a prompt that produces consistent output
3. **Wrap it in UI** - Make it easy to use (form → download)
4. **Deploy it** - Put it where people can use it

Same pattern works for:
- SOPs
- Email sequences
- Workshop outlines
- Client intake forms
- Coaching frameworks

**If you're writing the same type of document repeatedly, it's a candidate for this pattern.**

---

*Built with Claude Code. Shipped in a day.*
