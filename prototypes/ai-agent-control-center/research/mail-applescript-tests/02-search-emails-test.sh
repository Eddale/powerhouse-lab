#!/bin/bash
# Test 2: Searching emails via AppleScript
# Use case: Find specific emails in Mail.app

echo "=== Test 2: Searching Emails via AppleScript ==="
echo ""
echo "WARNING: AppleScript email search is SLOW on large mailboxes"
echo "This will iterate through messages one by one"
echo ""

# Example 1: Search by subject
search_by_subject() {
    local search_term="$1"
    local limit="${2:-10}"  # Default to 10 results

    echo "Searching for emails with subject containing: '$search_term'"
    echo "Starting at: $(date +%H:%M:%S)"

    osascript <<EOF
tell application "Mail"
    set matchingMessages to {}
    set allMessages to every message of inbox
    set messageCount to count of allMessages

    repeat with i from 1 to messageCount
        set theMessage to item i of allMessages
        set theSubject to subject of theMessage

        if theSubject contains "$search_term" then
            set end of matchingMessages to {subject:theSubject, sender:(sender of theMessage), dateReceived:(date received of theMessage)}

            -- Limit results
            if (count of matchingMessages) ≥ $limit then
                exit repeat
            end if
        end if

        -- Progress indicator every 100 messages
        if i mod 100 = 0 then
            log "Processed " & i & " of " & messageCount & " messages..."
        end if
    end repeat

    return matchingMessages
end tell
EOF

    echo "Finished at: $(date +%H:%M:%S)"
}

# Example 2: Search by sender
search_by_sender() {
    local sender_email="$1"
    local limit="${2:-10}"

    echo "Searching for emails from: '$sender_email'"
    echo "Starting at: $(date +%H:%M:%S)"

    osascript <<EOF
tell application "Mail"
    set matchingMessages to {}
    set allMessages to every message of inbox

    repeat with theMessage in allMessages
        set theSender to sender of theMessage

        if theSender contains "$sender_email" then
            set end of matchingMessages to {subject:(subject of theMessage), sender:theSender, dateReceived:(date received of theMessage)}

            if (count of matchingMessages) ≥ $limit then
                exit repeat
            end if
        end if
    end repeat

    return matchingMessages
end tell
EOF

    echo "Finished at: $(date +%H:%M:%S)"
}

# Example 3: Count messages in inbox (performance test)
count_inbox_messages() {
    echo "Counting inbox messages..."
    start_time=$(date +%s)

    count=$(osascript <<EOF
tell application "Mail"
    count of messages of inbox
end tell
EOF
)

    end_time=$(date +%s)
    elapsed=$((end_time - start_time))

    echo "Total messages in inbox: $count"
    echo "Time to count: ${elapsed} seconds"
    echo ""
    echo "NOTE: Counting is fast. Searching/filtering is slow."
}

# Example 4: Get recent N messages (faster than search)
get_recent_messages() {
    local count="${1:-10}"

    echo "Getting $count most recent messages..."

    osascript <<EOF
tell application "Mail"
    set recentMessages to {}
    set allMessages to messages 1 thru $count of inbox

    repeat with theMessage in allMessages
        set end of recentMessages to {subject:(subject of theMessage), sender:(sender of theMessage), dateReceived:(date received of theMessage)}
    end repeat

    return recentMessages
end tell
EOF
}

echo "Running performance tests..."
echo ""

# Test 1: Count messages (fast)
count_inbox_messages

# Test 2: Get recent messages (fast)
echo "Test: Get 5 most recent messages"
start=$(date +%s)
get_recent_messages 5
end=$(date +%s)
echo "Time: $((end - start)) seconds"
echo ""

# Test 3: Search (slow on large mailboxes)
# UNCOMMENT to test - this WILL be slow if you have many messages
# echo "Test: Search for subject containing 'test'"
# search_by_subject "test" 5

echo ""
echo "=== FINDINGS ==="
echo ""
echo "FAST operations (< 1 second):"
echo "- Count messages"
echo "- Get N most recent messages"
echo "- Access messages by index"
echo ""
echo "SLOW operations (scales with mailbox size):"
echo "- Search by subject/sender (iterates all messages)"
echo "- Filter by date range"
echo "- Search message content/body"
echo ""
echo "RECOMMENDATION: Use mdfind (Spotlight) for search instead"
echo "See: 05-mdfind-search-test.sh"
echo ""
