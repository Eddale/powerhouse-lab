/**
 * Test script - generates a sample DOCX playbook
 * Run: node test-docx.js
 */

const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, PageBreak, ShadingType, BorderStyle, WidthType } = require('docx');
const fs = require('fs');

// Brand colors
const COLORS = {
  black: '000000',
  gold: 'EFBB39',
  blue: '00A2FF',
  white: 'FFFFFF',
  gray: '666666',
};

// Test data - expanded with Jennifer's fields
const testData = {
  company: 'Premium Coaching Co',
  role: 'Appointment Setter',
  coreFunction: 'sell-by-chat',
  tools: ['GoHighLevel', 'Slack', 'Google Meet', 'Fathom', 'Calendly', 'Notion'],
  contact: 'Sarah Johnson',
  // Compensation details
  basePay: '$1,250',
  closeBonus: '$175',
  performanceThreshold: '6 closes',
  performanceBonus: '$200',
  // Time expectations
  hoursPerWeek: '40-50',
  workingHours: '8 AM - 5 PM EST',
  remoteRequirements: 'Strong Wi-Fi and a quiet, professional environment required',
  // Social proof
  winsChannel: '#wins',
};

// Helper functions
function createSectionHeader(number, title) {
  return new Paragraph({
    children: [
      new TextRun({ text: ` ${number} `, bold: true, size: 28, color: COLORS.gold, shading: { type: ShadingType.SOLID, color: COLORS.black } }),
      new TextRun({ text: `  ${title}`, bold: true, size: 28 }),
    ],
    border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: COLORS.gold } },
    spacing: { after: 240 },
  });
}

function createSubsectionTitle(title, keepWithNext = true) {
  return new Paragraph({
    children: [new TextRun({ text: title, bold: true, size: 24 })],
    spacing: { before: 240, after: 120 },
    keepNext: keepWithNext, // Keep this title with the following content
    keepLines: true,
  });
}

function createChecklistItem(text, hasLoomLink = false) {
  const children = [new TextRun({ text: `☐  ${text}` })];
  if (hasLoomLink) {
    children.push(
      new TextRun({ text: ' → ' }),
      new TextRun({ text: '[INSERT LOOM]', color: COLORS.blue, italics: true })
    );
  }
  return new Paragraph({ children, spacing: { after: 80 }, indent: { left: 400 } });
}

// Helper for example/placeholder text in grey italics
function createExampleText(text) {
  return new Paragraph({
    children: [new TextRun({ text: `e.g., ${text}`, color: COLORS.gray, italics: true, size: 20 })],
    spacing: { after: 80 },
    indent: { left: 400 },
  });
}

// Helper for bullet point
function createBulletPoint(text, indent = 400) {
  return new Paragraph({
    children: [new TextRun({ text: `•  ${text}` })],
    spacing: { after: 80 },
    indent: { left: indent },
  });
}

function createTableHeader(columns) {
  return new TableRow({
    tableHeader: true,
    cantSplit: true,
    children: columns.map(col =>
      new TableCell({
        children: [new Paragraph({ children: [new TextRun({ text: col, bold: true, color: COLORS.gold })] })],
        shading: { type: ShadingType.SOLID, color: COLORS.black },
      })
    ),
  });
}

function createTableRow(cells) {
  return new TableRow({
    cantSplit: true,
    children: cells.map(cell =>
      new TableCell({ children: [new Paragraph(cell)] })
    ),
  });
}

// Helper to create a table that stays together on one page
function createKeepTogetherTable(rows) {
  return new Table({
    rows: rows,
    width: { size: 100, type: WidthType.PERCENTAGE },
    // The cantSplit on rows helps, but we also need the preceding
    // subsection title to have keepNext to pull the table with it
  });
}

// Default font for the whole document
const DEFAULT_FONT = 'Arial';

// Build the document
const doc = new Document({
  styles: {
    default: {
      document: {
        run: {
          font: DEFAULT_FONT,
          size: 22, // 11pt
        },
      },
    },
  },
  sections: [{
    properties: {
      page: {
        margin: { top: 1134, right: 850, bottom: 1134, left: 850 },
      },
    },
    children: [
      // === HEADER ===
      new Paragraph({
        children: [
          new TextRun({ text: testData.company, bold: true, size: 48 }),
        ],
        spacing: { after: 120 },
      }),
      new Paragraph({
        children: [
          new TextRun({ text: `${testData.role} Playbook`, bold: true, size: 28, color: COLORS.gold }),
        ],
        border: { bottom: { style: BorderStyle.SINGLE, size: 18, color: COLORS.gold } },
        spacing: { after: 400 },
      }),

      // === PURPOSE BOX ===
      new Paragraph({
        children: [
          new TextRun({ text: 'Purpose: ', bold: true }),
          new TextRun({ text: `Everything your ${testData.role} needs to self-onboard and succeed.` }),
        ],
        shading: { type: ShadingType.SOLID, color: 'F5F5F5' },
        spacing: { after: 80 },
        indent: { left: 200, right: 200 },
      }),
      new Paragraph({
        children: [
          new TextRun({ text: 'How to use: ', bold: true }),
          new TextRun({ text: 'Work through each section in order. Each item links to a Loom video or document.' }),
        ],
        shading: { type: ShadingType.SOLID, color: 'F5F5F5' },
        spacing: { after: 400 },
        indent: { left: 200, right: 200 },
      }),

      // === SECTION 1 ===
      createSectionHeader('1', 'Company Foundation'),
      createSubsectionTitle('Mission & Values'),
      createChecklistItem('Watch: Company mission overview', true),
      createChecklistItem('Read: Our core values → [INSERT DOC]'),
      createChecklistItem('Watch: Who we serve (customer avatar)', true),
      createChecklistItem('Watch: Our origin story', true),
      createSubsectionTitle('Appearance & Communication'),
      createChecklistItem('Read: Brand voice guidelines → [INSERT DOC]'),
      createChecklistItem('Watch: How we communicate with clients', true),
      createChecklistItem('Read: Email templates → [INSERT DOC]'),

      // === PAGE BREAK + SECTION 2 ===
      new Paragraph({ children: [new PageBreak()] }),
      createSectionHeader('2', 'Tech Setup (SOPs)'),
      createSubsectionTitle('Essential Tools'),
      new Table({
        rows: [
          createTableHeader(['TOOL', 'PURPOSE', 'SETUP VIDEO']),
          ...testData.tools.map(tool => createTableRow([tool, 'Setup & daily use', '[INSERT LOOM]'])),
        ],
        width: { size: 100, type: WidthType.PERCENTAGE },
      }),
      new Paragraph({ spacing: { after: 200 } }),
      createSubsectionTitle('Account Setup Checklist'),
      createChecklistItem('Create company email'),
      createChecklistItem('Set up 2FA on all accounts'),
      createChecklistItem('Join Slack channels: #general, #setters, #wins'),
      createChecklistItem('Connect Google Calendar'),
      createChecklistItem('Complete CRM training'),

      // === PAGE BREAK + SECTION 3 ===
      new Paragraph({ children: [new PageBreak()] }),
      createSectionHeader('3', `Role Training: ${testData.role}`),
      createSubsectionTitle('The System You\'re Implementing'),
      createChecklistItem('Watch: Sell by Chat system overview', true),
      createChecklistItem('Read: Our lead-to-close flow → [INSERT DOC]'),
      createChecklistItem('Watch: Understanding the customer journey', true),
      createSubsectionTitle('Product Knowledge'),
      createChecklistItem('Watch: What we sell and why it works', true),
      createChecklistItem('Read: Client success stories → [INSERT DOC]'),
      createChecklistItem('Watch: Common objections and responses', true),
      createSubsectionTitle('Scripts & Frameworks'),
      createChecklistItem('Watch: DM opener script walkthrough', true),
      createChecklistItem('Watch: Qualification questions framework', true),
      createChecklistItem('Watch: Booking the call script', true),
      new Paragraph({
        children: [
          new TextRun({ text: '☐  ' }),
          new TextRun({ text: 'Practice: Record yourself doing 5 mock DM conversations → Submit to manager', italics: true, color: COLORS.gray }),
        ],
        spacing: { after: 80 },
        indent: { left: 400 },
      }),

      // === PAGE BREAK + SECTION 4 ===
      new Paragraph({ children: [new PageBreak()] }),
      createSectionHeader('4', 'Daily Activities'),
      createSubsectionTitle('Your Daily Rhythm'),
      new Table({
        rows: [
          createTableHeader(['TIME BLOCK', 'ACTIVITY', 'DETAILS']),
          createTableRow(['8:00 - 8:30', 'Pipeline Review', 'Check overnight responses, prioritize hot leads']),
          createTableRow(['8:30 - 9:00', 'Team Standup', 'Daily sync in Slack #setters']),
          createTableRow(['9:00 - 12:00', 'Outreach Block 1', 'New outreach + follow-ups']),
          createTableRow(['12:00 - 1:00', 'Lunch', 'Step away, recharge']),
          createTableRow(['1:00 - 4:00', 'Outreach Block 2', 'Continue conversations + book calls']),
          createTableRow(['4:00 - 4:30', 'CRM Cleanup', 'Update all lead statuses']),
          createTableRow(['4:30 - 5:00', 'Daily Report', 'Submit numbers, plan tomorrow']),
        ],
        width: { size: 100, type: WidthType.PERCENTAGE },
      }),
      new Paragraph({ spacing: { after: 200 } }),
      createChecklistItem('Watch: Pipeline overview', true),
      createChecklistItem('Watch: Daily workflow walkthrough', true),

      // === PAGE BREAK + SECTION 5 ===
      new Paragraph({ children: [new PageBreak()] }),
      createSectionHeader('5', 'Scorecard & Compensation'),
      createSubsectionTitle('Your KPIs'),
      new Table({
        rows: [
          createTableHeader(['METRIC', 'TARGET', 'HOW MEASURED']),
          createTableRow(['Conversations/month', '125+', 'CRM tracking']),
          createTableRow(['Appointments set', '25+', 'Calendar bookings']),
          createTableRow(['Show rate', '65%+', 'Appointments kept / booked']),
        ],
        width: { size: 100, type: WidthType.PERCENTAGE },
      }),
      new Paragraph({ spacing: { after: 200 } }),

      createSubsectionTitle('Compensation Structure'),
      createBulletPoint(`Base Pay: ${testData.basePay}/month (paid bi-monthly)`),
      createExampleText('Jennifer: $1,250/month guaranteed base'),
      createBulletPoint(`Close Bonus: ${testData.closeBonus} per sale from your booked appointments`),
      createExampleText('Jennifer: $175 per close'),
      createBulletPoint(`Performance Accelerator: Hit ${testData.performanceThreshold} in one month → ${testData.performanceBonus} bonus`),
      createExampleText('Jennifer: 6 closes = extra $200'),
      new Paragraph({
        children: [new TextRun({ text: '** Commissions are never capped. Close more, earn more.', italics: true })],
        spacing: { before: 120, after: 200 },
        indent: { left: 400 },
      }),

      createSubsectionTitle('OTE Examples'),
      new Paragraph({
        children: [new TextRun({ text: 'Average Performer:', bold: true })],
        spacing: { after: 80 },
        indent: { left: 400 },
      }),
      createBulletPoint(`Base: ${testData.basePay}`, 600),
      createBulletPoint(`Close Bonuses: 5 × ${testData.closeBonus} = $875`, 600),
      createBulletPoint('Total OTE: ~$2,125/month', 600),
      createExampleText('Jennifer: 5 closes/month average'),
      new Paragraph({
        children: [new TextRun({ text: 'High Performer:', bold: true })],
        spacing: { before: 120, after: 80 },
        indent: { left: 400 },
      }),
      createBulletPoint(`Base: ${testData.basePay}`, 600),
      createBulletPoint(`Close Bonuses: 6 × ${testData.closeBonus} = $1,050`, 600),
      createBulletPoint(`Performance Bonus: ${testData.performanceBonus}`, 600),
      createBulletPoint('Total OTE: ~$2,500/month', 600),
      createExampleText('Jennifer: 6+ closes unlocks accelerator'),
      new Paragraph({ spacing: { after: 200 } }),

      createSubsectionTitle('Time Expectations'),
      createBulletPoint(`This is a full-time role: ${testData.hoursPerWeek} hours per week`),
      createBulletPoint(`Working hours: ${testData.workingHours}`),
      createExampleText('Jennifer: 8 AM - 5 PM EST (1 hour break for lunch)'),
      createBulletPoint(testData.remoteRequirements),
      createExampleText('Jennifer: Remote position; strong Wi-Fi and quiet environment required'),
      new Paragraph({ spacing: { after: 200 } }),

      createSubsectionTitle('Client Success & Social Proof'),
      createChecklistItem('Read: Client success stories → [INSERT DOC]'),
      createChecklistItem(`Join the wins channel: Slack ${testData.winsChannel}`),
      createExampleText('Jennifer: #wins channel on Slack for celebrating closes'),

      // === PAGE BREAK + SECTION 6 ===
      new Paragraph({ children: [new PageBreak()] }),
      createSectionHeader('6', 'Communication & Support'),
      createSubsectionTitle('Who to Contact'),
      new Table({
        rows: [
          createTableHeader(['QUESTION TYPE', 'CONTACT', 'CHANNEL']),
          createTableRow(['Day-to-day questions', testData.contact, 'Slack DM']),
          createTableRow(['Technical issues', 'Tech Support', 'Slack #tech-support']),
          createTableRow(['Urgent matters', testData.contact, 'Phone/text']),
        ],
        width: { size: 100, type: WidthType.PERCENTAGE },
      }),
      new Paragraph({ spacing: { after: 200 } }),
      createSubsectionTitle('Weekly Check-ins'),
      createChecklistItem('Monday 10am: Team meeting'),
      createChecklistItem('Friday 4pm: 1:1 with manager'),

      // === COMPLETION BOX ===
      new Paragraph({ spacing: { before: 400 } }),
      new Paragraph({
        children: [new TextRun({ text: '  ✓ Completion Confirmation', bold: true, color: COLORS.gold, size: 24 })],
        shading: { type: ShadingType.SOLID, color: COLORS.black },
        spacing: { after: 120 },
      }),
      new Paragraph({
        children: [new TextRun({ text: '  1. Complete all checklist items above (2-3 days)', color: COLORS.white })],
        shading: { type: ShadingType.SOLID, color: COLORS.black },
        spacing: { after: 80 },
      }),
      new Paragraph({
        children: [new TextRun({ text: '  2. Record a 2-minute Loom introducing yourself', color: COLORS.white })],
        shading: { type: ShadingType.SOLID, color: COLORS.black },
        spacing: { after: 80 },
      }),
      new Paragraph({
        children: [new TextRun({ text: `  3. Send to ${testData.contact} with subject: "[Name] - Onboarding Complete"`, color: COLORS.white })],
        shading: { type: ShadingType.SOLID, color: COLORS.black },
        spacing: { after: 80 },
      }),
      new Paragraph({
        children: [new TextRun({ text: '  4. Schedule your first 1:1 check-in call', color: COLORS.white })],
        shading: { type: ShadingType.SOLID, color: COLORS.black },
        spacing: { after: 120 },
      }),
      new Paragraph({
        children: [new TextRun({ text: '  Welcome to the team! 🎯', bold: true, color: COLORS.gold, size: 26 })],
        shading: { type: ShadingType.SOLID, color: COLORS.black },
        spacing: { after: 120 },
      }),
    ],
  }],
});

// Generate the file
Packer.toBuffer(doc).then((buffer) => {
  const outputPath = './test-playbook.docx';
  fs.writeFileSync(outputPath, buffer);
  console.log(`✅ DOCX generated: ${outputPath}`);
  console.log('Open it in Word or Google Docs to check the formatting!');
}).catch(err => {
  console.error('Error generating DOCX:', err);
});
