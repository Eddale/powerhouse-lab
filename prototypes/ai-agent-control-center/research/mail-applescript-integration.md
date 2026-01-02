# Apple Mail AppleScript Integration Research

**Research Date:** January 2, 2026
**Purpose:** Document practical patterns for Claude Code integration with Apple Mail

---

## EXECUTIVE SUMMARY

**The Bottom Line:**
- **Sending emails:** AppleScript is EXCELLENT - fast, reliable, flexible
- **Searching emails:** AppleScript is SLOW - use mdfind (Spotlight) instead
- **Reading emails:** AppleScript is GOOD - fast for individual messages
- **Draft workflow:** Create draft → review in Mail → send (RECOMMENDED)

**Best Pattern for Claude Code:**
```
Claude generates content → AppleScript creates draft → Human reviews → Human sends
```

---

## 1. SENDING EMAILS

### Performance: Excellent (< 1 second)

AppleScript is the best way to send emails from command line on macOS.

### Basic Pattern: Create Draft for Review (RECOMMENDED)

```bash
osascript <<EOF
tell application "Mail"
    activate
    set newMessage to make new outgoing message with properties {subject:"Subject", content:"Body text", visible:true}
    tell newMessage
        make new to recipient at end of to recipients with properties {address:"recipient@example.com"}
    end tell
end tell
EOF
```

**Why this is the best pattern:**
- Creates draft and opens Mail.app
- Human reviews before sending (safety)
- Can edit in familiar interface
- Email appears in Sent folder after manual send
- Works with signatures, formatting, etc.

### Advanced: Multiple Recipients

```bash
osascript <<EOF
tell application "Mail"
    activate
    set newMessage to make new outgoing message with properties {subject:"Subject", content:"Body", visible:true}
    tell newMessage
        make new to recipient at end of to recipients with properties {address:"to@example.com"}
        make new cc recipient at end of cc recipients with properties {address:"cc@example.com"}
        make new bcc recipient at end of bcc recipients with properties {address:"bcc@example.com"}
    end tell
end tell
EOF
```

### Auto-Send (Use with Caution)

```bash
osascript <<EOF
tell application "Mail"
    set newMessage to make new outgoing message with properties {subject:"Subject", content:"Body", visible:true}
    tell newMessage
        make new to recipient at end of to recipients with properties {address:"recipient@example.com"}
        send
    end tell
end tell
EOF
```

**Warning:** Only use auto-send for:
- Known, safe recipients
- Automated notifications
- After explicit user confirmation

**Never auto-send:**
- Customer-facing emails
- First-time emails to new contacts
- Anything that could be embarrassing if wrong

### Key Properties

| Property | Description | Example |
|----------|-------------|---------|
| `subject` | Email subject line | "Follow-up on meeting" |
| `content` | Email body (plain text or HTML) | "Hi,\n\nThanks for..." |
| `visible` | Show compose window | `true` or `false` |
| `sender` | From address (if multiple accounts) | "work@example.com" |

### Use Cases for Claude Code

**1. Draft support emails**
```
User: "Draft an email to support about account access"
Claude: Analyzes context, generates email, creates draft in Mail
User: Reviews, edits, sends
```

**2. Draft follow-ups**
```
User: "Follow up with John about the proposal"
Claude: Checks context, drafts follow-up, creates draft
User: Reviews and sends
```

**3. Template-based emails**
```
User: "Send weekly report to team"
Claude: Populates template with data, creates draft
User: Quick review and send
```

---

## 2. SEARCHING EMAILS

### AppleScript Search: SLOW (Don't Use for Large Mailboxes)

**Problem:** AppleScript must iterate through every message one by one.

**Performance:**
- 1,000 messages: ~5-10 seconds
- 10,000 messages: ~50-100 seconds
- 100,000 messages: Minutes (unusable)

**Example (SLOW):**
```bash
osascript <<EOF
tell application "Mail"
    set matchingMessages to {}
    set allMessages to every message of inbox

    repeat with theMessage in allMessages
        if subject of theMessage contains "search term" then
            set end of matchingMessages to theMessage
        end if
    end repeat

    return matchingMessages
end tell
EOF
```

**Why it's slow:**
- No indexed search
- Iterates ALL messages
- Fetches each message's properties
- Runs in single-threaded AppleScript

**Verdict:** DO NOT USE for search. Use mdfind instead.

### mdfind Search: FAST (RECOMMENDED)

**Performance:** Near-instant even on 100,000+ messages

**Why it's fast:**
- Uses Spotlight index
- Optimized by macOS
- No iteration required
- Returns results immediately

**Basic Search Examples:**

```bash
# Search by subject
mdfind "kMDItemContentType == 'com.apple.mail.emlx' && kMDItemSubject == '*keyword*'c"

# Search by sender
mdfind "kMDItemContentType == 'com.apple.mail.emlx' && kMDItemAuthors == '*sender@example.com*'c"

# Search email content
mdfind "kMDItemContentType == 'com.apple.mail.emlx' && kMDItemTextContent == '*text in body*'c"

# Combined search (AND)
mdfind "kMDItemContentType == 'com.apple.mail.emlx' && kMDItemSubject == '*urgent*'c && kMDItemAuthors == '*boss@example.com*'c"
```

**Spotlight Attributes for Mail:**

| Attribute | Description | Example |
|-----------|-------------|---------|
| `kMDItemContentType` | File type (always 'com.apple.mail.emlx') | Required for all queries |
| `kMDItemSubject` | Email subject | "Meeting notes" |
| `kMDItemAuthors` | Sender email | "sender@example.com" |
| `kMDItemRecipients` | To/CC recipients | "recipient@example.com" |
| `kMDItemTextContent` | Email body text | "quarterly report" |
| `kMDItemContentCreationDate` | Date received | Date object |
| `kMDItemDisplayName` | Email filename | Rarely used |

**Search Syntax:**

| Pattern | Description | Example |
|---------|-------------|---------|
| `== 'exact'` | Exact match | `kMDItemSubject == 'Welcome'` |
| `== '*partial*'c` | Contains (case-insensitive) | `kMDItemSubject == '*test*'c` |
| `&&` | AND operator | `subject && sender` |
| `\|\|` | OR operator | `subject1 \|\| subject2` |
| `!=` | NOT operator | `!= 'spam'` |

**Get Metadata from Search Results:**

```bash
# Search and get metadata
email_file=$(mdfind "kMDItemContentType == 'com.apple.mail.emlx' && kMDItemSubject == '*test*'c" | head -1)

# Get all metadata
mdls "$email_file"

# Get specific fields
mdls -name kMDItemSubject -name kMDItemAuthors -name kMDItemContentCreationDate "$email_file"
```

**Recommended Workflow:**

```bash
# 1. Search with mdfind (FAST)
results=$(mdfind "kMDItemContentType == 'com.apple.mail.emlx' && kMDItemSubject == '*invoice*'c")

# 2. Get metadata with mdls (if needed)
for file in $results; do
    mdls -name kMDItemSubject -name kMDItemAuthors "$file"
done

# 3. Read full content with AppleScript (if needed)
# See "Reading Emails" section
```

---

## 3. READING EMAIL CONTENT

### Performance: Good (< 1 second per message)

Reading individual emails with AppleScript is fast and reliable.

### Basic Read

```bash
osascript <<EOF
tell application "Mail"
    set theMessage to message 1 of inbox

    set emailData to {¬
        subject:(subject of theMessage), ¬
        sender:(sender of theMessage), ¬
        dateReceived:(date received of theMessage), ¬
        content:(content of theMessage) ¬
    }

    return emailData
end tell
EOF
```

### Read by Index

```bash
# Read 5th most recent email
osascript <<EOF
tell application "Mail"
    set theMessage to message 5 of inbox
    return content of theMessage
end tell
EOF
```

### Get Full Metadata

```bash
osascript <<EOF
tell application "Mail"
    set theMessage to message 1 of inbox

    set emailData to {¬
        subject:(subject of theMessage), ¬
        sender:(sender of theMessage), ¬
        dateReceived:(date received of theMessage), ¬
        dateSent:(date sent of theMessage), ¬
        toRecipients:(to recipients of theMessage as string), ¬
        ccRecipients:(cc recipients of theMessage as string), ¬
        messageID:(message id of theMessage), ¬
        wasRead:(read status of theMessage), ¬
        isFlagged:(flagged status of theMessage) ¬
    }

    return emailData
end tell
EOF
```

### Check for Attachments

```bash
osascript <<EOF
tell application "Mail"
    set theMessage to message 1 of inbox
    set attachmentsList to {}

    tell theMessage
        set msgAttachments to mail attachments

        repeat with theAttachment in msgAttachments
            set attachmentInfo to {¬
                name:(name of theAttachment), ¬
                size:(file size of theAttachment) ¬
            }
            set end of attachmentsList to attachmentInfo
        end repeat
    end tell

    return attachmentsList
end tell
EOF
```

### Save Email to File

```bash
osascript <<EOF
tell application "Mail"
    set theMessage to message 1 of inbox

    set theSubject to subject of theMessage
    set theSender to sender of theMessage
    set theContent to content of theMessage

    set outputText to "Subject: " & theSubject & return & ¬
        "From: " & theSender & return & ¬
        return & ¬
        "---" & return & ¬
        return & ¬
        theContent

    set fileRef to open for access POSIX file "/tmp/email.txt" with write permission
    set eof fileRef to 0
    write outputText to fileRef as «class utf8»
    close access fileRef
end tell
EOF
```

### Available Properties

| Property | Type | Description |
|----------|------|-------------|
| `subject` | text | Subject line |
| `sender` | text | Sender email address |
| `content` | text | Email body (may include HTML) |
| `date received` | date | When email arrived |
| `date sent` | date | When email was sent |
| `to recipients` | list | To addresses |
| `cc recipients` | list | CC addresses |
| `bcc recipients` | list | BCC addresses |
| `message id` | text | Unique message identifier |
| `read status` | boolean | Has been read |
| `flagged status` | boolean | Is flagged |
| `mail attachments` | list | Attachment objects |
| `mailbox` | mailbox | Containing mailbox |

### Limitations

**HTML Content:**
- Rich emails may include HTML tags in content
- No built-in HTML-to-plain-text conversion
- May need post-processing to clean up

**Large Emails:**
- Very long emails work fine
- No practical size limit observed

**Attachments:**
- Can get metadata (name, size)
- Can save attachments to disk
- Cannot read attachment content directly in AppleScript

---

## 4. OPENING MAIL APP

### Basic: Activate Mail

```bash
osascript -e 'tell application "Mail" to activate'
```

**Or:**

```bash
open -a Mail
```

### Open with Draft (Recommended Pattern)

This is already covered in "Sending Emails" section with `visible:true`:

```bash
osascript <<EOF
tell application "Mail"
    activate
    set newMessage to make new outgoing message with properties {subject:"Subject", content:"Body", visible:true}
    tell newMessage
        make new to recipient at end of to recipients with properties {address:"recipient@example.com"}
    end tell
end tell
EOF
```

### Check if Mail is Running

```bash
if pgrep -x "Mail" > /dev/null; then
    echo "Mail is running"
else
    echo "Mail is not running"
    open -a Mail
fi
```

### Focus Specific Mailbox

```bash
osascript <<EOF
tell application "Mail"
    activate
    set visible of front message viewer to true
    set mailbox of front message viewer to mailbox "Inbox"
end tell
EOF
```

---

## 5. RECOMMENDED PATTERNS FOR CLAUDE CODE

### Pattern 1: Draft Email Workflow (BEST)

**Use case:** User asks Claude to draft an email

```
1. User: "Draft an email to support about my account issue"
2. Claude:
   - Analyzes context (previous conversations, task notes, etc.)
   - Identifies recipient (support@example.com)
   - Generates appropriate email body
   - Runs AppleScript to create draft in Mail
3. Mail.app opens with draft ready for review
4. User reviews, edits if needed, and sends
```

**Code example:**

```bash
#!/bin/bash
# Draft email in Mail.app for review

TO="support@example.com"
SUBJECT="Account Access Issue"
BODY="Hi Support,

I'm experiencing an issue with...

[Claude generates context-aware content]

Thanks,
Ed"

osascript <<EOF
tell application "Mail"
    activate
    set newMessage to make new outgoing message with properties {subject:"$SUBJECT", content:"$BODY", visible:true}
    tell newMessage
        make new to recipient at end of to recipients with properties {address:"$TO"}
    end tell
end tell
EOF
```

### Pattern 2: Search and Summarize

**Use case:** User asks Claude to find and summarize recent emails

```
1. User: "Summarize recent emails from John"
2. Claude:
   - Uses mdfind to search for sender:john@example.com
   - Uses AppleScript to read content of results
   - Processes with Claude to generate summary
   - Returns summary to user
```

**Code example:**

```bash
#!/bin/bash
# Search for emails from specific sender and read content

SENDER="john@example.com"

# Step 1: Search with mdfind (FAST)
echo "Searching for emails from $SENDER..."
email_files=$(mdfind "kMDItemContentType == 'com.apple.mail.emlx' && kMDItemAuthors == '*$SENDER*'c" | head -5)

# Step 2: Read each email with AppleScript
for i in {1..5}; do
    content=$(osascript <<EOF
tell application "Mail"
    try
        set theMessage to message $i of inbox
        set theSender to sender of theMessage

        if theSender contains "$SENDER" then
            return {subject:(subject of theMessage), content:(content of theMessage)}
        else
            return ""
        end if
    on error
        return ""
    end try
end tell
EOF
    )

    if [ ! -z "$content" ]; then
        echo "Email $i:"
        echo "$content"
        echo "---"
    fi
done

# Step 3: Claude processes and summarizes
# (This would be done by Claude Code internally)
```

### Pattern 3: Template-Based Emails

**Use case:** Recurring emails with standard formats

```bash
#!/bin/bash
# Generate email from template

generate_support_email() {
    local issue_description="$1"

    BODY="Hi Support Team,

I need assistance with the following:

$issue_description

Account email: ed@example.com
Date: $(date '+%Y-%m-%d %H:%M')

Please let me know if you need any additional information.

Thanks,
Ed Dale"

    osascript <<EOF
tell application "Mail"
    activate
    set newMessage to make new outgoing message with properties {subject:"Support Request", content:"$BODY", visible:true}
    tell newMessage
        make new to recipient at end of to recipients with properties {address:"support@example.com"}
    end tell
end tell
EOF
}

# Usage
generate_support_email "Cannot access my account - password reset not working"
```

### Pattern 4: Read and Extract Information

**Use case:** Extract specific data from emails (tracking numbers, dates, etc.)

```bash
#!/bin/bash
# Read recent emails and extract information

# Get most recent order confirmation emails
results=$(mdfind "kMDItemContentType == 'com.apple.mail.emlx' && kMDItemSubject == '*Order Confirmation*'c" | head -5)

# Read each and extract tracking number
for email_file in $results; do
    # Get subject
    subject=$(mdls -name kMDItemSubject -raw "$email_file")

    # Read content with AppleScript
    content=$(osascript <<EOF
tell application "Mail"
    set allMessages to every message of inbox
    repeat with theMessage in allMessages
        -- Match by subject since we can't directly open file
        if subject of theMessage is "$subject" then
            return content of theMessage
        end if
    end repeat
end tell
EOF
    )

    # Extract tracking number (example pattern)
    tracking=$(echo "$content" | grep -o 'Tracking: [A-Z0-9]*' | cut -d' ' -f2)

    echo "Order: $subject"
    echo "Tracking: $tracking"
    echo "---"
done
```

---

## 6. LIMITATIONS AND GOTCHAS

### AppleScript Limitations

**1. Mail.app Must Be Configured**
- At least one email account must be set up
- If no accounts, AppleScript will fail
- Cannot configure accounts via AppleScript

**2. HTML Content**
- Rich emails include HTML tags in content
- No built-in way to strip HTML
- May need external tool (pandoc, textutil, etc.)

**3. No Direct File Access**
- Cannot directly read .emlx files
- Must go through Mail.app application
- Spotlight (mdfind) can access files directly for search

**4. Performance**
- Fast for individual operations
- Slow for bulk operations (use mdfind instead)
- No parallel processing in AppleScript

### mdfind Limitations

**1. Spotlight Indexing Required**
- Relies on Spotlight being enabled
- New emails may have ~1 minute delay before indexed
- If Spotlight disabled, mdfind won't work

**2. Returns File Paths, Not Objects**
- Get file paths, not Mail message objects
- Need mdls or AppleScript to read content
- Cannot directly manipulate messages

**3. Query Syntax**
- Complex queries require specific syntax
- Case sensitivity can be tricky
- Date queries are verbose

### General Considerations

**1. Privacy**
- Scripts can read all email content
- Be cautious with logging/storing email data
- Consider security implications

**2. Error Handling**
- Mail.app might not be running
- Mailbox might be empty
- Search might return no results
- Always include error handling

**3. Account Selection**
- If multiple accounts, specify sender address
- Default account is used if not specified
- Cannot change account configuration

---

## 7. TESTING SCRIPTS

All test scripts are available in:
`/Users/eddale/Documents/GitHub/powerhouse-lab/prototypes/ai-agent-control-center/research/mail-applescript-tests/`

**Available Tests:**

1. `01-send-email-test.sh` - Sending emails and creating drafts
2. `02-search-emails-test.sh` - AppleScript search (demonstrates slowness)
3. `03-read-email-content-test.sh` - Reading email content
4. `04-draft-review-workflow-test.sh` - Recommended draft workflow
5. `05-mdfind-search-test.sh` - Fast search with Spotlight

**To run tests:**

```bash
cd research/mail-applescript-tests
chmod +x *.sh
./01-send-email-test.sh
```

**Note:** Some tests create drafts in Mail.app - these are safe to run.

---

## 8. QUICK REFERENCE

### Send Email (Draft for Review)
```bash
osascript -e 'tell application "Mail" to activate' \
-e 'set newMessage to make new outgoing message with properties {subject:"Subject", content:"Body", visible:true}' \
-e 'tell newMessage to make new to recipient with properties {address:"to@example.com"}'
```

### Search Emails (Fast)
```bash
mdfind "kMDItemContentType == 'com.apple.mail.emlx' && kMDItemSubject == '*keyword*'c"
```

### Read Recent Email
```bash
osascript -e 'tell application "Mail" to return content of message 1 of inbox'
```

### Count Inbox
```bash
osascript -e 'tell application "Mail" to count of messages of inbox'
```

### Get Email Metadata
```bash
mdls -name kMDItemSubject -name kMDItemAuthors "$email_file_path"
```

---

## 9. CLAUDE CODE INTEGRATION EXAMPLES

### Example 1: User Asks to Draft Email

**User:** "Draft an email to support about my account access issue"

**Claude Code Workflow:**

1. Parse request → identify task: draft email
2. Extract details:
   - Recipient: support (maps to support@example.com from context)
   - Topic: account access issue
   - Urgency: normal
3. Search for context:
   - Recent notes about account issues
   - Previous support emails
   - Account details
4. Generate email body with context
5. Run AppleScript to create draft
6. Confirm to user: "Draft created in Mail.app - please review and send"

### Example 2: User Asks to Find Information

**User:** "What did John say about the proposal in his last email?"

**Claude Code Workflow:**

1. Parse request → identify task: search and extract
2. Extract details:
   - Sender: John (need to resolve email)
   - Topic: proposal
   - Scope: most recent
3. Search with mdfind:
   ```bash
   mdfind "kMDItemContentType == 'com.apple.mail.emlx' && kMDItemAuthors == '*john@example.com*'c && kMDItemSubject == '*proposal*'c"
   ```
4. Read content with AppleScript
5. Process with Claude to extract relevant information
6. Return summary: "John said the proposal looks good but wants to discuss pricing..."

### Example 3: Automated Weekly Summary

**User:** "Summarize this week's support emails"

**Claude Code Workflow:**

1. Calculate date range (last 7 days)
2. Search with mdfind for support emails in range
3. Read each email with AppleScript
4. Categorize by issue type
5. Generate summary:
   - Total emails: X
   - By category: Y account issues, Z feature requests
   - Urgent items: [list]
   - Follow-ups needed: [list]

---

## 10. BEST PRACTICES

### DO:
- ✅ Create drafts for review (don't auto-send)
- ✅ Use mdfind for search (not AppleScript iteration)
- ✅ Include context in generated emails
- ✅ Check if Mail.app is configured before running scripts
- ✅ Handle errors gracefully
- ✅ Use `visible:true` to show compose window
- ✅ Activate Mail.app when creating drafts

### DON'T:
- ❌ Auto-send emails without explicit user confirmation
- ❌ Use AppleScript iteration to search large mailboxes
- ❌ Store email content in logs or temp files unnecessarily
- ❌ Assume Mail.app is running
- ❌ Forget to escape special characters in email content
- ❌ Read every email when you only need recent ones

### Security Considerations:
- Be careful with email addresses (typos can send to wrong person)
- Don't log email content unnecessarily
- Consider privacy when processing email data
- Validate recipient addresses when possible
- Use draft workflow for anything sensitive

---

## CONCLUSION

**AppleScript + mdfind = Powerful Email Integration**

**Key Takeaways:**

1. **Sending:** AppleScript is excellent - fast, reliable, flexible
2. **Searching:** Use mdfind (Spotlight), not AppleScript
3. **Reading:** AppleScript is good for individual messages
4. **Best Pattern:** Draft → Review → Send

**Recommended for Claude Code:**
- Email drafting and composition: ⭐⭐⭐⭐⭐
- Email search and filtering: ⭐⭐⭐⭐⭐ (with mdfind)
- Email content extraction: ⭐⭐⭐⭐
- Automated sending: ⭐⭐⭐ (with caution)

**The draft-for-review workflow is the killer feature:**
- Claude generates smart, context-aware email content
- AppleScript creates draft in Mail.app instantly
- Human reviews and sends (safety + control)
- Best of both worlds: AI assistance + human oversight

---

**Document Status:** Complete
**Test Scripts:** Available in `research/mail-applescript-tests/`
**Last Updated:** January 2, 2026
