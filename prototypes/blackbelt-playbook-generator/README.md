# BlackBelt Playbook Generator

**Live:** https://app-eight-indol-52.vercel.app

Generate professional onboarding playbooks for any role in 30 seconds. No Claude.ai account needed - just fill out a form and download.

---

## What This Does

Think of it like a merge tag system for onboarding docs. You fill in the blanks (company name, role, tools they'll use), Claude writes a complete playbook in Jennifer Waters' style, and you download it as a Word doc or Markdown file.

**The problem it solves:** Every time you hire someone new, you need an onboarding playbook. Writing these from scratch takes hours. This tool does it in 30 seconds.

---

## How It Works (The Simple Version)

```
You fill form → Claude writes playbook → You download DOCX or Markdown
```

That's it. No login, no account, no friction.

### Behind the Scenes

1. **Form** - Captures company name, role, core function, tools, manager name, etc.
2. **API Route** - Sends your inputs to Claude with a detailed prompt template
3. **Claude** - Writes a complete playbook with all sections (Welcome, Tech Setup, Role Training, Daily Activities, Scorecard, Communication, Completion Checklist)
4. **Download** - Converts the markdown to a properly formatted Word doc with:
   - Real headings (H1, H2, H3)
   - Formatted tables
   - Checkboxes
   - Page breaks before each section

---

## The Tech Stack (For Reference)

| Layer | What It Is |
|-------|------------|
| Frontend | Next.js 16 + React + Tailwind |
| AI | Claude API via server-side route |
| PDF/DOCX | docx library (client-side generation) |
| Hosting | Vercel (free tier) |

**Cost:** ~$0.01 per playbook generation. A thousand playbooks = $10.

---

## Form Fields

| Field | What It's For |
|-------|---------------|
| Company Name | Appears throughout the playbook |
| Role Name | The job title (e.g., "Appointment Setter") |
| Core Function | Dropdown - shapes the content focus |
| Tools Used | Multi-select chips - generates tool-specific training |
| Other Tools | Free text for tools not in the list |
| Manager/Contact | Who the new hire reports to |
| Wins Channel | Where they post wins (e.g., #wins) |

---

## Output Format

The generated playbook includes:

1. **Welcome** - Personalized intro with company and manager name
2. **Company Foundation** - Mission, values, appearance standards
3. **Tech Setup** - Tool-by-tool setup checklist with tables
4. **Role Training** - Scripts, frameworks, product knowledge
5. **Daily Activities** - Time blocks, pipeline training
6. **Scorecard & Compensation** - KPIs, targets, pay structure
7. **Communication & Support** - Who to contact, meeting schedule
8. **Completion Confirmation** - Checkbox checklist

Each major section starts on its own page in the DOCX.

---

## File Structure

```
blackbelt-playbook-generator/
├── app/                    # Next.js application
│   ├── src/app/
│   │   ├── page.tsx       # Main UI (form → loading → preview)
│   │   ├── layout.tsx     # Metadata and fonts
│   │   ├── globals.css    # Styling
│   │   ├── opengraph-image.tsx  # Social preview image
│   │   └── api/generate/route.ts  # Claude API endpoint
│   └── public/
│       └── blackbelt-logo-*.png  # Logos
├── assets/                 # Source assets
└── README.md              # You're reading it
```

---

## Deploying Changes

The app is connected to Vercel. To deploy updates:

```bash
cd prototypes/blackbelt-playbook-generator/app
npx vercel --prod
```

Or push to GitHub and Vercel will auto-deploy.

---

## Environment Variables

One secret needed on Vercel:

```
ANTHROPIC_API_KEY=sk-ant-...
```

This is the Claude API key. Set it in Vercel → Settings → Environment Variables.

---

## Customizing the Prompt

The magic is in the prompt template. It lives in:

```
app/src/app/api/generate/route.ts
```

The prompt tells Claude:
- Write in Jennifer Waters' style
- Include specific sections
- Use markdown formatting (headers, tables, checkboxes)
- Make it comprehensive but not bloated

To change what the playbook includes, edit the prompt template in that file.

---

## Future Ideas (Out of Scope for V1)

- [ ] Google Docs export
- [ ] Save playbooks to library
- [ ] Custom branding upload
- [ ] Inline editing before download
- [ ] Multiple language support

---

## Credits

- **Built by:** Ed Dale using Claude Code
- **Style:** Based on Jennifer Waters' onboarding playbook format
- **For:** BlackBelt coaching members

---

*Built for coaches who ship.*
