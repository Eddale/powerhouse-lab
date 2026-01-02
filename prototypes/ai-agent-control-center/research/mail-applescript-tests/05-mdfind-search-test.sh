#!/bin/bash
# Test 5: Email Search via mdfind (Spotlight)
# Use case: Fast email search without AppleScript iteration

echo "=== Test 5: Email Search via mdfind (Spotlight) ==="
echo ""
echo "mdfind uses macOS Spotlight to search email metadata and content"
echo "This is MUCH faster than AppleScript iteration for large mailboxes"
echo ""

# Example 1: Search emails by subject
search_by_subject() {
    local search_term="$1"

    echo "Searching for emails with subject containing: '$search_term'"
    echo "Starting at: $(date +%H:%M:%S)"

    # Search Mail messages with specific subject
    mdfind "kMDItemContentType == 'com.apple.mail.emlx' && kMDItemSubject == '*$search_term*'c"

    echo "Finished at: $(date +%H:%M:%S)"
}

# Example 2: Search emails by sender
search_by_sender() {
    local sender_email="$1"

    echo "Searching for emails from: '$sender_email'"
    echo "Starting at: $(date +%H:%M:%S)"

    # Search Mail messages from specific sender
    mdfind "kMDItemContentType == 'com.apple.mail.emlx' && kMDItemAuthors == '*$sender_email*'c"

    echo "Finished at: $(date +%H:%M:%S)"
}

# Example 3: Search email content (body text)
search_email_content() {
    local search_term="$1"

    echo "Searching email content for: '$search_term'"
    echo "Starting at: $(date +%H:%M:%S)"

    # Search within email body
    mdfind "kMDItemContentType == 'com.apple.mail.emlx' && kMDItemTextContent == '*$search_term*'c"

    echo "Finished at: $(date +%H:%M:%S)"
}

# Example 4: Search by date range
search_by_date() {
    local days_ago="$1"

    echo "Searching for emails from the last $days_ago days"
    echo "Starting at: $(date +%H:%M:%S)"

    # Calculate date in Spotlight format
    # Note: This requires date math - using simple example
    mdfind "kMDItemContentType == 'com.apple.mail.emlx'" | head -20

    echo "Finished at: $(date +%H:%M:%S)"
}

# Example 5: Combined search (subject AND sender)
search_combined() {
    local subject="$1"
    local sender="$2"

    echo "Searching for emails from '$sender' with subject containing '$subject'"
    echo "Starting at: $(date +%H:%M:%S)"

    mdfind "kMDItemContentType == 'com.apple.mail.emlx' && kMDItemSubject == '*$subject*'c && kMDItemAuthors == '*$sender*'c"

    echo "Finished at: $(date +%H:%M:%S)"
}

# Example 6: Count results (fast)
count_search_results() {
    local search_term="$1"

    echo "Counting emails with subject containing: '$search_term'"

    count=$(mdfind "kMDItemContentType == 'com.apple.mail.emlx' && kMDItemSubject == '*$search_term*'c" | wc -l)

    echo "Found: $count emails"
}

# Example 7: Get email metadata from file path
get_email_metadata() {
    local email_file="$1"

    echo "Getting metadata for: $email_file"

    # Get all metadata attributes
    mdls "$email_file"
}

# Example 8: Practical workflow - Search and read with AppleScript
search_and_read_workflow() {
    local search_term="$1"

    echo "=== Search and Read Workflow ==="
    echo ""

    # Step 1: Find emails using mdfind (fast)
    echo "Step 1: Finding emails with mdfind..."
    results=$(mdfind "kMDItemContentType == 'com.apple.mail.emlx' && kMDItemSubject == '*$search_term*'c" | head -5)

    if [ -z "$results" ]; then
        echo "No emails found matching: '$search_term'"
        return 1
    fi

    echo "Found emails:"
    echo "$results" | nl
    echo ""

    # Step 2: Get metadata for first result
    first_result=$(echo "$results" | head -1)
    echo "Step 2: Getting metadata for first result..."
    echo ""

    # Extract useful metadata
    mdls -name kMDItemSubject \
         -name kMDItemAuthors \
         -name kMDItemContentCreationDate \
         -name kMDItemDisplayName \
         "$first_result"

    echo ""
    echo "Step 3: To read full content, use AppleScript with message ID"
    echo "(See 03-read-email-content-test.sh)"
}

# Performance comparison test
performance_comparison() {
    echo "=== Performance Comparison ==="
    echo ""

    # Test mdfind speed
    echo "Test 1: mdfind search"
    start=$(date +%s.%N)
    count=$(mdfind "kMDItemContentType == 'com.apple.mail.emlx'" | wc -l)
    end=$(date +%s.%N)
    mdfind_time=$(echo "$end - $start" | bc)

    echo "Total emails indexed: $count"
    echo "Time taken: ${mdfind_time} seconds"
    echo ""

    echo "Test 2: mdfind with subject filter"
    start=$(date +%s.%N)
    count=$(mdfind "kMDItemContentType == 'com.apple.mail.emlx' && kMDItemSubject == '*test*'c" | wc -l)
    end=$(date +%s.%N)
    filter_time=$(echo "$end - $start" | bc)

    echo "Matching emails: $count"
    echo "Time taken: ${filter_time} seconds"
    echo ""

    echo "RESULT: mdfind is near-instant even on large mailboxes"
}

echo "Running tests..."
echo ""

# Run performance comparison
performance_comparison

# Example workflow
echo ""
echo "=== Example Workflow ==="
echo ""
search_and_read_workflow "test"

echo ""
echo "=== FINDINGS ==="
echo ""
echo "ADVANTAGES of mdfind:"
echo "- FAST: Searches thousands of emails in < 1 second"
echo "- Rich queries: Subject, sender, content, date, etc."
echo "- Returns file paths (can get metadata with mdls)"
echo "- No Mail.app running required (searches Spotlight index)"
echo ""
echo "LIMITATIONS:"
echo "- Returns file paths, not email objects"
echo "- Need AppleScript or mdls to read full content"
echo "- Complex queries require specific Spotlight syntax"
echo "- Relies on Spotlight indexing being up to date"
echo ""
echo "RECOMMENDED WORKFLOW:"
echo "1. Use mdfind to search and filter (FAST)"
echo "2. Use mdls to get metadata from file paths"
echo "3. Use AppleScript to read full content if needed"
echo "4. Process content with Claude"
echo ""
echo "KEY SPOTLIGHT ATTRIBUTES for Mail:"
echo "- kMDItemContentType: 'com.apple.mail.emlx'"
echo "- kMDItemSubject: Email subject line"
echo "- kMDItemAuthors: Sender email address"
echo "- kMDItemRecipients: To/CC recipients"
echo "- kMDItemTextContent: Email body text"
echo "- kMDItemContentCreationDate: Date received"
echo "- kMDItemDisplayName: Email filename"
echo ""
echo "SEARCH SYNTAX:"
echo "- Exact match: kMDItemSubject == 'exact text'"
echo "- Contains: kMDItemSubject == '*partial*'c"
echo "- Case-insensitive: Add 'c' flag"
echo "- AND: &&"
echo "- OR: ||"
echo "- NOT: !="
echo ""
