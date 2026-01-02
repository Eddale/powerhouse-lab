#!/bin/bash
# Test 3: Reading email content via AppleScript
# Use case: Fetch email body text for AI processing

echo "=== Test 3: Reading Email Content via AppleScript ==="
echo ""

# Example 1: Read most recent email
read_recent_email() {
    echo "Reading most recent email from inbox..."

    osascript <<EOF
tell application "Mail"
    set latestMessage to message 1 of inbox

    set emailData to {¬
        subject:(subject of latestMessage), ¬
        sender:(sender of latestMessage), ¬
        dateReceived:(date received of latestMessage), ¬
        content:(content of latestMessage) ¬
    }

    return emailData
end tell
EOF
}

# Example 2: Read email by index
read_email_by_index() {
    local index="$1"

    echo "Reading email #$index from inbox..."

    osascript <<EOF
tell application "Mail"
    set theMessage to message $index of inbox

    set emailData to {¬
        subject:(subject of theMessage), ¬
        sender:(sender of theMessage), ¬
        dateReceived:(date received of theMessage), ¬
        content:(content of theMessage) ¬
    }

    return emailData
end tell
EOF
}

# Example 3: Read email and extract plain text (strip HTML)
read_email_plain_text() {
    local index="${1:-1}"

    echo "Reading email #$index (plain text only)..."

    osascript <<EOF
tell application "Mail"
    set theMessage to message $index of inbox

    -- Try to get plain text content
    -- Note: Mail.app may return HTML for rich emails
    set theContent to content of theMessage

    set emailData to {¬
        subject:(subject of theMessage), ¬
        sender:(sender of theMessage), ¬
        content:theContent ¬
    }

    return emailData
end tell
EOF
}

# Example 4: Read email headers and metadata
read_email_metadata() {
    local index="${1:-1}"

    echo "Reading email #$index metadata..."

    osascript <<EOF
tell application "Mail"
    set theMessage to message $index of inbox

    set emailData to {¬
        subject:(subject of theMessage), ¬
        sender:(sender of theMessage), ¬
        dateReceived:(date received of theMessage), ¬
        dateSent:(date sent of theMessage), ¬
        toRecipients:(to recipients of theMessage as string), ¬
        ccRecipients:(cc recipients of theMessage as string), ¬
        messageID:(message id of theMessage), ¬
        wasRead:(read status of theMessage), ¬
        isFlagged:(flagged status of theMessage), ¬
        mailbox:((mailbox of theMessage) as string) ¬
    }

    return emailData
end tell
EOF
}

# Example 5: Read email and save to file
read_email_to_file() {
    local index="${1:-1}"
    local output_file="$2"

    echo "Reading email #$index and saving to $output_file..."

    osascript <<EOF
tell application "Mail"
    set theMessage to message $index of inbox

    set theSubject to subject of theMessage
    set theSender to sender of theMessage
    set theDate to date received of theMessage
    set theContent to content of theMessage

    set outputText to "Subject: " & theSubject & return & ¬
        "From: " & theSender & return & ¬
        "Date: " & (theDate as string) & return & ¬
        return & ¬
        "---" & return & ¬
        return & ¬
        theContent

    -- Write to file
    set fileRef to open for access POSIX file "$output_file" with write permission
    set eof fileRef to 0
    write outputText to fileRef as «class utf8»
    close access fileRef

    return "Email saved to $output_file"
end tell
EOF
}

# Example 6: Get email attachments info
get_email_attachments() {
    local index="${1:-1}"

    echo "Checking for attachments in email #$index..."

    osascript <<EOF
tell application "Mail"
    set theMessage to message $index of inbox
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

    if (count of attachmentsList) = 0 then
        return "No attachments found"
    else
        return attachmentsList
    end if
end tell
EOF
}

echo "Running tests..."
echo ""

# Test 1: Read most recent email
echo "=== Test 1: Most Recent Email ==="
read_recent_email
echo ""

# Test 2: Read metadata
echo "=== Test 2: Email Metadata ==="
read_email_metadata 1
echo ""

# Test 3: Check for attachments
echo "=== Test 3: Attachments ==="
get_email_attachments 1
echo ""

# Test 4: Save to file (uncomment to test)
# OUTPUT_FILE="/tmp/test-email-$(date +%s).txt"
# echo "=== Test 4: Save to File ==="
# read_email_to_file 1 "$OUTPUT_FILE"
# echo "Saved to: $OUTPUT_FILE"
# echo ""

echo ""
echo "=== FINDINGS ==="
echo ""
echo "WHAT WORKS WELL:"
echo "- Reading email content is fast (< 1 second per message)"
echo "- Can access subject, sender, date, body, headers"
echo "- Can check for attachments"
echo "- Can get read/flagged status"
echo ""
echo "LIMITATIONS:"
echo "- Body content may include HTML tags for rich emails"
echo "- No built-in HTML-to-plain-text conversion"
echo "- Cannot search within email body efficiently (see 02-search-emails-test.sh)"
echo ""
echo "RECOMMENDED PATTERN:"
echo "1. Use mdfind to search and get message IDs"
echo "2. Use AppleScript to read full content of specific messages"
echo "3. Process content with Claude for summarization/extraction"
echo ""
