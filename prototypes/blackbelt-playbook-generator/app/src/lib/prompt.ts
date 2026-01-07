import { PlaybookFormData } from './types';

export function buildPrompt(data: PlaybookFormData): string {
  const functionName = getFunctionName(data.coreFunction);
  const toolsList = data.tools.length > 0
    ? data.tools.map(t => `| ${t} | [Purpose] | [INSERT LOOM] |`).join('\n')
    : '| [Tool] | [Purpose] | [INSERT LOOM] |';

  return `You are creating a professional onboarding playbook for a coaching business.

Generate a comprehensive, ready-to-use playbook in Markdown format for the following role:

**Company:** ${data.company}
**Role:** ${data.role}
**Core Function:** ${functionName}
**Tools:** ${data.tools.join(', ') || 'To be configured'}
**Manager/Contact:** ${data.contact || '[To be assigned]'}

**Compensation Details:**
- Base Pay: ${data.basePay || '[To be set]'}
- Close Bonus: ${data.closeBonus || '[To be set]'}
- Performance Threshold: ${data.performanceThreshold || '[To be set]'}
- Performance Bonus: ${data.performanceBonus || '[To be set]'}

**Time Expectations:**
- Hours per Week: ${data.hoursPerWeek || '[To be set]'}
- Working Hours: ${data.workingHours || '[To be set]'}
- Remote Requirements: ${data.remoteRequirements || '[To be set]'}

**Culture:**
- Wins Channel: ${data.winsChannel || '#wins'}

Create a playbook with the following structure. Use [INSERT LOOM] or [INSERT DOC] placeholders where video/document links should go. Make it practical and actionable.

## Required Sections:

1. **Company Foundation**
   - Mission & Values (3-4 checklist items with Loom/doc placeholders)
   - Appearance & Communication (3-4 items)

2. **Tech Setup (SOPs)**
   - Essential Tools table with columns: Tool | Purpose | Setup Video
   - Account Setup Checklist (5-7 items)

3. **Role Training: ${data.role}**
   - The System You're Implementing (based on ${functionName})
   - Product Knowledge (4-5 items)
   - Scripts & Frameworks (4-5 items including practice tasks)

4. **Daily Activities**
   - Daily Rhythm table (time blocks from start to end of day)
   - Pipeline Training items

5. **Scorecard & Compensation**
   - KPIs table (Metric | Daily | Weekly | Monthly targets)
   - Compensation Structure (use the provided details or placeholders)
   - Time Expectations (use provided details)
   - Client Success & Social Proof section

6. **Communication & Support**
   - Who to Contact table (Question Type | Contact | Channel)
   - Meeting Schedule checklist

7. **Completion Confirmation**
   - 4-5 step checklist to confirm onboarding is complete
   - Include recording a Loom intro and scheduling first 1:1

Format guidelines:
- Use proper Markdown with headers, tables, and checklists
- Checklist items should use "- [ ]" format
- Keep it professional but warm
- Add a "Welcome to the team!" message at the end
- Make KPI targets realistic for the role type`;
}

function getFunctionName(func: string): string {
  const names: Record<string, string> = {
    'sell-by-chat': 'Sell by Chat',
    'customer-success': 'Customer Success',
    'community': 'Community Management',
    'operations': 'Operations',
    'closer': 'Sales Closing',
    'other': 'General Role',
  };
  return names[func] || 'General Role';
}
