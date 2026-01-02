#!/bin/bash
# Test 4: Draft Review Workflow
# Use case: Claude drafts email → human reviews in Mail → sends

echo "=== Test 4: Draft Review Workflow ==="
echo ""
echo "This demonstrates the recommended pattern:"
echo "1. Claude generates email content"
echo "2. AppleScript creates draft in Mail.app"
echo "3. Human reviews and edits in Mail"
echo "4. Human decides to send or discard"
echo ""

# The recommended function: Create draft for review
create_draft_for_review() {
    local to_address="$1"
    local subject="$2"
    local body="$3"
    local cc_address="${4:-}"
    local bcc_address="${5:-}"

    echo "Creating draft email..."
    echo "To: $to_address"
    echo "Subject: $subject"
    echo ""

    osascript <<EOF
tell application "Mail"
    activate
    set newMessage to make new outgoing message with properties {subject:"$subject", content:"$body", visible:true}

    tell newMessage
        make new to recipient at end of to recipients with properties {address:"$to_address"}

        -- Add CC if provided
        if "$cc_address" is not "" then
            make new cc recipient at end of cc recipients with properties {address:"$cc_address"}
        end if

        -- Add BCC if provided
        if "$bcc_address" is not "" then
            make new bcc recipient at end of bcc recipients with properties {address:"$bcc_address"}
        end if
    end tell
end tell
EOF

    echo "Draft created and opened in Mail.app for review"
}

# Advanced: Create draft with signature
create_draft_with_signature() {
    local to_address="$1"
    local subject="$2"
    local body="$3"
    local signature_name="${4:-}"  # Optional: name of Mail signature to use

    osascript <<EOF
tell application "Mail"
    activate
    set newMessage to make new outgoing message with properties {subject:"$subject", content:"$body", visible:true}

    tell newMessage
        make new to recipient at end of to recipients with properties {address:"$to_address"}

        -- Set signature if specified
        if "$signature_name" is not "" then
            set message signature of newMessage to signature "$signature_name"
        end if
    end tell
end tell
EOF
}

# Workflow helper: Generate email from template
generate_from_template() {
    local template_type="$1"
    local recipient="$2"

    case "$template_type" in
        "support")
            create_draft_for_review \
                "$recipient" \
                "Support Request" \
                "Hi,

I'm reaching out regarding...

[Claude would generate context here based on the task]

Thanks,
Ed"
            ;;

        "followup")
            create_draft_for_review \
                "$recipient" \
                "Following up" \
                "Hi,

Following up on our previous conversation about...

[Claude fills in details]

Looking forward to your thoughts.

Ed"
            ;;

        "intro")
            create_draft_for_review \
                "$recipient" \
                "Introduction" \
                "Hi,

[Claude generates personalized intro based on context]

Best,
Ed"
            ;;

        *)
            echo "Unknown template type: $template_type"
            echo "Available: support, followup, intro"
            return 1
            ;;
    esac
}

# Example: Multi-step workflow
workflow_example() {
    echo "=== Multi-step Workflow Example ==="
    echo ""
    echo "Scenario: Claude helps draft a support email"
    echo ""

    # Step 1: Claude would analyze the task and extract details
    echo "Step 1: Claude analyzes task and identifies:"
    echo "  - Recipient: support@example.com"
    echo "  - Issue: Account access problem"
    echo "  - Relevant details: Account email, last login attempt"
    echo ""

    # Step 2: Claude generates email content
    echo "Step 2: Claude generates email content using context"
    local email_body="Hi Support Team,

I'm experiencing an issue accessing my account. Here are the details:

Account email: ed@example.com
Issue: Cannot log in despite correct password
Last attempt: $(date '+%Y-%m-%d %H:%M')
Error message: 'Invalid credentials'

I've tried:
- Password reset (didn't receive email)
- Different browsers
- Clearing cache and cookies

Could you please help me regain access to my account?

Thanks,
Ed Dale"

    echo "Step 3: Creating draft in Mail.app for review..."
    create_draft_for_review \
        "support@example.com" \
        "Account Access Issue - Ed Dale" \
        "$email_body"

    echo ""
    echo "Step 4: Mail.app is now open with draft"
    echo "Step 5: You review, edit if needed, and send (or discard)"
}

# Safety features
check_mail_running() {
    if pgrep -x "Mail" > /dev/null; then
        echo "✓ Mail.app is running"
        return 0
    else
        echo "✗ Mail.app is not running"
        echo "  Starting Mail.app..."
        open -a Mail
        sleep 2
        return 0
    fi
}

echo "Checking Mail.app status..."
check_mail_running
echo ""

# Run the workflow example
workflow_example

echo ""
echo "=== FINDINGS ==="
echo ""
echo "ADVANTAGES of this pattern:"
echo "- Human reviews before sending (safety)"
echo "- Can edit in familiar Mail interface"
echo "- Uses Mail's signature, formatting, etc."
echo "- Email appears in Sent folder after sending"
echo "- Works with all Mail.app features (rich text, attachments, etc.)"
echo ""
echo "BEST PRACTICES:"
echo "1. Always set visible:true (shows compose window)"
echo "2. Always activate Mail.app (brings to front)"
echo "3. Never send automatically without explicit user request"
echo "4. Include context in email body so human understands why it was drafted"
echo ""
echo "INTEGRATION with Claude Code:"
echo "1. User: 'Draft an email to support about X'"
echo "2. Claude: Analyzes context, identifies recipient and key points"
echo "3. Claude: Generates appropriate email body"
echo "4. Claude: Runs this script to create draft in Mail"
echo "5. User: Reviews in Mail, edits if needed, sends"
echo ""
