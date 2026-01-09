# Kindle Sender - How It Works

## The One-Sentence Version

It's like having an assistant who takes your research notes, formats them nicely, and drops them on your Kindle so you can read them on the couch.

## Why This Exists

You do a research swarm. Claude generates a beautiful 500-line markdown document packed with insights. It sits in your Zettelkasten.

When do you actually read it? Never. It's on your computer. Your computer is for working. Your Kindle is for reading.

This skill bridges the gap. Research goes in, Kindle-ready documents come out. Now you can review your own research while drinking coffee, waiting for a flight, or lying in bed.

## The Self-Regulating Loop

Here's the magic: you can send your Someday-Maybe.md file to Kindle.

That file is your parking lot - all the projects and tasks you've deferred. Sending it to Kindle means you review your own backlog during downtime. You come back with clarity on what to actually work on next.

Build tools -> Use tools to review your backlog -> Decide what to build next -> Repeat.

## How You Use It

**For research documents:**
1. Say "Send my research to Kindle"
2. Claude finds today's Research Swarm docs
3. You confirm
4. Documents appear on your Kindle in minutes

**For backlog review:**
1. Say "Send someday-maybe to Kindle"
2. Claude sends your parked projects list
3. Read it later, decide what's worth doing

## What Happens Under the Hood

1. Claude reads your daily note
2. Finds all the `[[Research Swarm - *]]` links in Captures
3. Converts each markdown file to EPUB (Kindle's preferred format)
4. Emails them to your Kindle address
5. Amazon's servers convert to proper Kindle format
6. Documents appear in your Kindle library

The "Convert" subject line is the magic word that tells Amazon to make it readable (proper fonts, resizable text, etc.) instead of just dumping a raw file.

## One-Time Setup

You need three things configured:
1. Your Kindle email (find it in Amazon settings)
2. Your Gmail whitelisted as a sender (also in Amazon settings)
3. A Gmail app password (not your regular password)

Takes 5 minutes, then you never think about it again.

## The Philosophy

Your computer is for creating. Your Kindle is for consuming.

Don't try to read research docs on the same machine where you write code. Context switching kills focus.

Ship research to Kindle, read it during downtime, come back with insights.
