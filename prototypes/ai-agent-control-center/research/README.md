# AI Agent Control Center - Research

**Repository:** powerhouse-lab/prototypes/ai-agent-control-center/research
**Last Updated:** 2026-01-02

This directory contains research findings, technical documentation, and production-ready code for building AI agent capabilities.

---

## Quick Navigation

| Research Topic | Quick Start | Full Docs | Production Code |
|----------------|-------------|-----------|-----------------|
| **YouTube Transcripts** | [QUICK-START.md](./QUICK-START.md) | [Full Research](./youtube-transcript-extraction.md) | [Python Module](./youtube_transcript_extractor.py) |
| **Gmail Integration** | [Quick Start](./gmail-quick-start-guide.md) | [API Integration](./gmail-api-integration.md) | See spec doc |

---

## YouTube Transcript Extraction (NEW - 2026-01-02)

Complete research on extracting YouTube transcripts for AI agents. Includes production-ready Python code, comparison of 3 methods, and decision matrix.

### Files
- **[QUICK-START.md](./QUICK-START.md)** - Get transcripts in 60 seconds
- **[youtube-transcript-extraction.md](./youtube-transcript-extraction.md)** - Comprehensive analysis
- **[COMPARISON-CHART.md](./COMPARISON-CHART.md)** - Decision matrix
- **[youtube_transcript_extractor.py](./youtube_transcript_extractor.py)** - Production code
- **[test-transcript-methods.py](./test-transcript-methods.py)** - Test suite
- **[requirements-transcript.txt](./requirements-transcript.txt)** - Dependencies

### Quick Usage
```bash
# Install
pip install -r requirements-transcript.txt

# Use production module
python youtube_transcript_extractor.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

```python
# Use in code
from youtube_transcript_extractor import extract_transcript

result = extract_transcript("https://www.youtube.com/watch?v=VIDEO_ID")
if result['success']:
    print(result['transcript'])
```

### Key Findings
- **Recommended method:** youtube-transcript-api (simple, fast, no auth)
- **Fallback method:** yt-dlp (more robust)
- **Official method:** YouTube Data API v3 (requires OAuth, quota limits)
- **Speed:** 0.5-1s per video (youtube-transcript-api)
- **Rate limits:** ~100-200 requests/minute (practical limit)
- **Success rate:** 87% (youtube-transcript-api alone), 95%+ (with fallback)

---

## Gmail API Integration (2026-01-02)

**Background:**
Previous research (Dec 31, 2025) identified email search as a limitation:
- AppleScript too slow for large mailboxes
- Spotlight/mdfind broken since Catalina
- Recommendation: Python IMAP or Gmail API

This research explores **Gmail API** as the solution.

### Research Documents

### 1. [gmail-api-integration.md](./gmail-api-integration.md)
**Comprehensive API research covering:**
- Authentication options (OAuth2, Service Account, App Passwords)
- Search capabilities and query syntax
- Reading emails (formats, attachments, threads)
- Sending emails (simple, draft, reply)
- Labels and filters management
- Rate limits and performance benchmarks
- Full code examples for each capability

**Key findings:**
- OAuth2 recommended for personal Gmail
- Search speed: 200-500ms (fast enough for Claude Code)
- Same query syntax as Gmail web interface
- Supports "Waiting For" tracking via labels
- Can draft emails for review before sending

### 2. [claude-code-gmail-tool-spec.md](./claude-code-gmail-tool-spec.md)
**Technical specification for building the tool:**
- Complete CLI interface design
- JSON output format for Claude parsing
- Full Python implementation (auth, search, send, tracking)
- Error handling and security measures
- Integration patterns with Claude Code workflow
- Testing plan and future enhancements

**Architecture:**
```
tools/gmail/
├── gmail_tool.py      # Main CLI
├── auth.py           # OAuth2 handler
├── search.py         # Search logic
├── send.py           # Send/draft emails
├── tracking.py       # "Waiting For" system
└── config.py         # Configuration
```

### 3. [gmail-quick-start-guide.md](./gmail-quick-start-guide.md)
**30-minute implementation guide:**
- Step-by-step Google Cloud Console setup
- OAuth2 credentials download
- Python client installation
- Test authentication script
- Simple search script
- Common query cheat sheet
- Troubleshooting guide

**Perfect for:** Getting started quickly without reading full docs

---

## Use Cases for Ed's Workflow

### 1. Fast Email Search
**Current:** AppleScript too slow, Spotlight broken
**With Gmail API:** 200-500ms searches using Gmail query syntax

```bash
# Find emails from specific client
gmail search "from:client@example.com newer_than:7d"

# Find proposals with attachments
gmail search "subject:proposal has:attachment"
```

### 2. "Waiting For" Tracking
**Current:** Manual tracking or none
**With Gmail API:** Automated system with labels

```bash
# Send email and auto-track
gmail send --to="client@example.com" --subject="Proposal" --body="..." --track

# Check for replies
gmail waiting-for check
# → Automatically moves replied emails to "Responded" label
```

### 3. Email Drafting in Ed's Voice
**Current:** Manual composition
**With Gmail API:** Claude drafts, Ed reviews before sending

```bash
# Claude creates draft
gmail draft --to="client@example.com" --subject="Follow-up" --body="[Claude-generated text]"
# → Opens in Gmail for Ed to review and edit before sending
```

---

## Implementation Roadmap

### Phase 1: Foundation (2 hours)
- [x] Research Gmail API capabilities
- [x] Document authentication methods
- [x] Create implementation spec
- [ ] Set up Google Cloud project
- [ ] Implement OAuth2 authentication
- [ ] Test basic search functionality

### Phase 2: Core Features (3 hours)
- [ ] Build search module with query parsing
- [ ] Implement email reading (subjects, bodies, attachments)
- [ ] Create send/draft functionality
- [ ] Add JSON output formatting
- [ ] Test with real Gmail account

### Phase 3: "Waiting For" System (2 hours)
- [ ] Build label management
- [ ] Implement tracking logic
- [ ] Create reply checker
- [ ] Test full workflow
- [ ] Document usage patterns

### Phase 4: Claude Code Integration (1 hour)
- [ ] Create CLI wrapper
- [ ] Add to Claude Code tools directory
- [ ] Test from Claude Code context
- [ ] Create usage examples
- [ ] Document in mission-context

**Total estimated time:** 8 hours (1 day)

---

## Key Technical Decisions

### Why Gmail API over IMAP?
1. **Speed:** Gmail API is faster (indexed search vs. sequential scan)
2. **Features:** Label management, drafts, threading built-in
3. **Reliability:** Official Google API vs. third-party IMAP
4. **Security:** OAuth2 vs. app passwords or raw credentials

### Why OAuth2 over Service Account?
1. **Personal Gmail:** Service accounts only work with Workspace
2. **User context:** Ed's personal email access
3. **Simplicity:** One-time setup, auto-refresh tokens

### Why Python over AppleScript?
1. **Performance:** 200-500ms vs. 30+ seconds for large mailboxes
2. **Reliability:** API-based vs. UI scripting
3. **Portability:** Works anywhere, not just Mac
4. **Maintainability:** Well-documented Google API vs. fragile AppleScript

---

## Performance Benchmarks

| Operation | Speed | Quota Cost |
|-----------|-------|------------|
| Search query | 200-500ms | 5 units |
| Fetch message | 100-200ms | 5 units |
| Send email | 300-600ms | 100 units |
| Create draft | 200-400ms | 50 units |
| List labels | 50-100ms | 5 units |

**Daily limits (free tier):**
- 1 billion API calls (effectively unlimited for personal use)
- 250 quota units per second per user

---

## Security Considerations

### Credentials Storage
```bash
# Secure location
~/.config/gmail-tool/credentials.json  # OAuth2 client credentials
~/.config/gmail-tool/token.pickle      # Access/refresh tokens

# Permissions
chmod 600 ~/.config/gmail-tool/*

# Git ignore
echo "credentials.json" >> .gitignore
echo "token.pickle" >> .gitignore
```

### OAuth2 Scopes
```python
# Minimal scopes for Ed's use case:
'https://www.googleapis.com/auth/gmail.modify'  # Read, send, labels
'https://www.googleapis.com/auth/gmail.send'    # Send only (if preferred)
```

### Token Lifecycle
- **Access tokens:** Expire in 1 hour, auto-refresh
- **Refresh tokens:** Long-lived until revoked
- **Revocation:** https://myaccount.google.com/permissions

---

## Example Workflows

### Morning Email Check
```bash
# Check unread
gmail search "is:unread"

# Check waiting-for status
gmail waiting-for list

# Check for new replies
gmail waiting-for check
```

### Client Follow-up
```bash
# Search client history
gmail search "from:client@example.com OR to:client@example.com"

# Draft follow-up (Claude generates text)
gmail draft --to="client@example.com" --subject="Q1 Planning" --body="..."

# Review in Gmail, edit if needed, then send
```

### Proposal Tracking
```bash
# Send proposal with tracking
gmail send --to="prospect@example.com" --subject="Proposal: AI Coaching" --body="..." --track

# Later: Check if replied
gmail waiting-for check
# → Auto-updates label when reply received
```

---

## Next Steps

1. **Immediate:**
   - Follow [gmail-quick-start-guide.md](./gmail-quick-start-guide.md)
   - Set up Google Cloud project
   - Test authentication

2. **Short-term:**
   - Implement core modules from [claude-code-gmail-tool-spec.md](./claude-code-gmail-tool-spec.md)
   - Test with Ed's Gmail account
   - Document usage patterns

3. **Long-term:**
   - Integrate with Claude Code workflow
   - Build "Waiting For" automation
   - Add email voice analysis (learn Ed's style)
   - Create email templates

---

## Questions for Ed

1. **Priority:** Which feature is most valuable first?
   - [ ] Fast search
   - [ ] "Waiting For" tracking
   - [ ] Email drafting

2. **Integration:** Where should this live?
   - [ ] Part of ai-agent-control-center
   - [ ] Standalone skill
   - [ ] Own repository

3. **Workflow:** How do you want to use it?
   - [ ] Direct commands from Claude Code
   - [ ] Automated checks (cron job)
   - [ ] Both

4. **Scope:** Start small or build full system?
   - [ ] Search only (MVP)
   - [ ] Search + Send (basic)
   - [ ] Full system with tracking (complete)

---

## Resources

- **Gmail API Docs:** https://developers.google.com/gmail/api
- **Python Client:** https://github.com/googleapis/google-api-python-client
- **Query Syntax:** https://support.google.com/mail/answer/7190
- **OAuth2 Guide:** https://developers.google.com/gmail/api/auth/about-auth

---

**Status:** Research complete, ready to implement
**Confidence:** High - well-documented API, clear implementation path
**Risk:** Low - OAuth2 setup is one-time, API is stable and fast

---

## Additional Research Topics

### Mobile Claude Integration
Research on using Claude AI on mobile devices (iOS).

**Files:**
- [mobile-claude-api-integration.md](./mobile-claude-api-integration.md)
- [mobile-claude-tools-matrix.md](./mobile-claude-tools-matrix.md)
- [quick-start-ios-shortcut-make.md](./quick-start-ios-shortcut-make.md)
- [code-snippets-mobile-claude.md](./code-snippets-mobile-claude.md)

### Drafts App Capabilities
Analysis of Drafts app for text capture and AI integration on iOS.

**Files:**
- [drafts-app-capabilities.md](./drafts-app-capabilities.md)

### Waiting For Implementation
Research on building "waiting for" tracking systems.

**Files:**
- [waiting-for-tracking-research.md](./waiting-for-tracking-research.md)
- [waiting-for-implementation-guide.md](./waiting-for-implementation-guide.md)

### Obsidian Templates
Templates for knowledge management.

**Files:**
- [obsidian-templates/](./obsidian-templates/)

---

## Research Standards

All research documents in this directory include:

- **Date**: When the research was conducted
- **Purpose**: What problem it solves
- **Methods**: Approaches evaluated
- **Code examples**: Working implementations
- **Pros/Cons**: Honest evaluation
- **Recommendations**: Clear guidance
- **Next steps**: What to do with findings

---

## How to Use This Research

### For Quick Prototyping
1. Check the QUICK-START guides
2. Copy production code files
3. Run test scripts to validate
4. Build your prototype

### For Production Implementation
1. Read full research documents
2. Review comparison charts
3. Implement error handling
4. Add monitoring and logging
5. Set up proper authentication

### For Learning
1. Start with implementation guides
2. Read the research docs
3. Run test scripts
4. Experiment with variations

---

## Contributing New Research

When adding research to this directory:

1. **Create the main research document**
   - Comprehensive analysis
   - Code examples
   - Pros/cons evaluation

2. **Add a quick start guide** (for complex topics)
   - Get started in < 5 minutes
   - Minimal setup
   - Working example

3. **Include production code** (when applicable)
   - Error handling
   - Documentation
   - Test suite

4. **Update this README**
   - Add to appropriate section
   - Update Quick Navigation table

---

## Most Recent Research

**2026-01-02**: YouTube Transcript Extraction
- Complete analysis of 3 extraction methods
- Production-ready Python module with caching and fallback
- Decision matrix and comparison chart
- Test suite included
- Recommended for AI agent use

---

**Research maintained by:** Ed Dale (Vibe Coder)
**Repository:** powerhouse-lab/prototypes/ai-agent-control-center
