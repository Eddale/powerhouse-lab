/**
 * DOCX Template for BlackBelt Playbook Generator
 *
 * Uses docx.js library: https://docx.js.org/
 * npm install docx
 *
 * Key principle: Each section starts on its own page
 */

const {
  Document,
  Packer,
  Paragraph,
  TextRun,
  Table,
  TableRow,
  TableCell,
  HeadingLevel,
  AlignmentType,
  WidthType,
  BorderStyle,
  PageBreak,
  CheckBox,
  ShadingType,
} = require('docx');

// Brand colors
const COLORS = {
  black: '000000',
  gold: 'EFBB39',
  blue: '00A2FF',
  white: 'FFFFFF',
  gray: '666666',
};

/**
 * Generate a BlackBelt Playbook DOCX
 * @param {Object} data - Form data
 * @returns {Document} - docx Document object
 */
function generatePlaybookDocx(data) {
  const {
    company,
    role,
    coreFunction,
    tools,
    contact,
    compensation,
  } = data;

  const doc = new Document({
    styles: {
      paragraphStyles: [
        {
          id: 'Normal',
          name: 'Normal',
          basedOn: 'Normal',
          run: {
            font: 'Montserrat',
            size: 22, // 11pt
          },
          paragraph: {
            spacing: { after: 120 },
          },
        },
        {
          id: 'SectionTitle',
          name: 'Section Title',
          basedOn: 'Heading1',
          run: {
            font: 'Montserrat',
            size: 28, // 14pt
            bold: true,
            color: COLORS.black,
          },
          paragraph: {
            spacing: { before: 240, after: 120 },
            border: {
              bottom: { style: BorderStyle.SINGLE, size: 12, color: COLORS.gold },
            },
          },
        },
        {
          id: 'SubsectionTitle',
          name: 'Subsection Title',
          basedOn: 'Heading2',
          run: {
            font: 'Montserrat',
            size: 24, // 12pt
            bold: true,
            color: COLORS.black,
          },
          paragraph: {
            spacing: { before: 200, after: 80 },
          },
        },
      ],
    },
    sections: [
      {
        properties: {
          page: {
            margin: {
              top: 1134, // ~20mm
              right: 850, // ~15mm
              bottom: 1134,
              left: 850,
            },
          },
        },
        children: [
          // === HEADER ===
          createHeader(company, role),

          // === PURPOSE BOX ===
          createPurposeBox(role),

          // === SECTION 1: Company Foundation ===
          ...createSection1(),

          // === PAGE BREAK + SECTION 2: Tech Setup ===
          new Paragraph({ children: [new PageBreak()] }),
          ...createSection2(tools),

          // === PAGE BREAK + SECTION 3: Role Training ===
          new Paragraph({ children: [new PageBreak()] }),
          ...createSection3(role, coreFunction),

          // === PAGE BREAK + SECTION 4: Daily Activities ===
          new Paragraph({ children: [new PageBreak()] }),
          ...createSection4(),

          // === PAGE BREAK + SECTION 5: Scorecard ===
          new Paragraph({ children: [new PageBreak()] }),
          ...createSection5(compensation),

          // === PAGE BREAK + SECTION 6: Communication ===
          new Paragraph({ children: [new PageBreak()] }),
          ...createSection6(contact),

          // === COMPLETION BOX ===
          ...createCompletionBox(contact),
        ],
      },
    ],
  });

  return doc;
}

// === HELPER FUNCTIONS ===

function createHeader(company, role) {
  return new Paragraph({
    children: [
      new TextRun({
        text: company,
        bold: true,
        size: 48, // 24pt
        font: 'Montserrat',
      }),
      new TextRun({
        text: `\n${role} Playbook`,
        bold: true,
        size: 28, // 14pt
        color: COLORS.gold,
        font: 'Montserrat',
        break: 1,
      }),
    ],
    spacing: { after: 400 },
    border: {
      bottom: { style: BorderStyle.SINGLE, size: 18, color: COLORS.gold },
    },
  });
}

function createPurposeBox(role) {
  return new Paragraph({
    children: [
      new TextRun({ text: 'Purpose: ', bold: true }),
      new TextRun({ text: `Everything your ${role} needs to self-onboard and succeed.` }),
      new TextRun({ text: '\nHow to use: ', bold: true, break: 1 }),
      new TextRun({ text: 'Work through each section in order. Each item links to a Loom video or document.' }),
    ],
    shading: { type: ShadingType.SOLID, color: 'F8F8F8' },
    border: {
      left: { style: BorderStyle.SINGLE, size: 24, color: COLORS.gold },
    },
    spacing: { before: 200, after: 400 },
    indent: { left: 200 },
  });
}

function createSectionHeader(number, title) {
  return new Paragraph({
    children: [
      new TextRun({
        text: `${number}  `,
        bold: true,
        size: 28,
        color: COLORS.gold,
        highlight: 'black',
      }),
      new TextRun({
        text: title,
        bold: true,
        size: 28,
      }),
    ],
    border: {
      bottom: { style: BorderStyle.SINGLE, size: 12, color: COLORS.gold },
    },
    spacing: { after: 200 },
  });
}

function createSubsectionTitle(title) {
  return new Paragraph({
    children: [
      new TextRun({ text: title, bold: true, size: 24 }),
    ],
    spacing: { before: 200, after: 100 },
  });
}

function createChecklistItem(text, isLoomLink = false) {
  const children = [
    new TextRun({ text: '☐  ' }),
    new TextRun({ text: text }),
  ];

  if (isLoomLink) {
    children.push(
      new TextRun({ text: ' → ', color: COLORS.gray }),
      new TextRun({ text: '[INSERT LOOM]', color: COLORS.blue, italics: true })
    );
  }

  return new Paragraph({
    children,
    spacing: { after: 80 },
    indent: { left: 400 },
  });
}

function createSection1() {
  return [
    createSectionHeader('1', 'Company Foundation'),
    createSubsectionTitle('Mission & Values'),
    createChecklistItem('Watch: Company mission overview', true),
    createChecklistItem('Read: Our core values → [INSERT DOC]'),
    createChecklistItem('Watch: Who we serve (customer avatar)', true),
    createSubsectionTitle('Appearance & Communication'),
    createChecklistItem('Read: Brand voice guidelines → [INSERT DOC]'),
    createChecklistItem('Watch: How we communicate with clients', true),
  ];
}

function createSection2(tools) {
  const toolRows = (tools || ['GoHighLevel', 'Slack', 'Google Meet']).map(tool =>
    new TableRow({
      children: [
        new TableCell({ children: [new Paragraph(tool)], width: { size: 25, type: WidthType.PERCENTAGE } }),
        new TableCell({ children: [new Paragraph('Setup & usage')], width: { size: 35, type: WidthType.PERCENTAGE } }),
        new TableCell({
          children: [new Paragraph({
            children: [new TextRun({ text: '[INSERT LOOM]', color: COLORS.blue, italics: true })]
          })],
          width: { size: 40, type: WidthType.PERCENTAGE },
        }),
      ],
    })
  );

  return [
    createSectionHeader('2', 'Tech Setup (SOPs)'),
    createSubsectionTitle('Essential Tools'),
    new Table({
      rows: [
        // Header row
        new TableRow({
          children: [
            new TableCell({
              children: [new Paragraph({ children: [new TextRun({ text: 'TOOL', bold: true, color: COLORS.gold })] })],
              shading: { type: ShadingType.SOLID, color: COLORS.black },
            }),
            new TableCell({
              children: [new Paragraph({ children: [new TextRun({ text: 'PURPOSE', bold: true, color: COLORS.gold })] })],
              shading: { type: ShadingType.SOLID, color: COLORS.black },
            }),
            new TableCell({
              children: [new Paragraph({ children: [new TextRun({ text: 'SETUP VIDEO', bold: true, color: COLORS.gold })] })],
              shading: { type: ShadingType.SOLID, color: COLORS.black },
            }),
          ],
        }),
        ...toolRows,
      ],
      width: { size: 100, type: WidthType.PERCENTAGE },
    }),
    new Paragraph({ spacing: { after: 200 } }),
    createSubsectionTitle('Account Setup Checklist'),
    createChecklistItem('Create company email'),
    createChecklistItem('Set up 2FA on all accounts'),
    createChecklistItem('Join relevant Slack channels'),
    createChecklistItem('Connect calendar'),
    createChecklistItem('Complete CRM training'),
  ];
}

function createSection3(role, coreFunction) {
  const functionName = {
    'sell-by-chat': 'Sell by Chat',
    'customer-success': 'Customer Success',
    'community': 'Community Management',
    'operations': 'Operations',
    'closer': 'Sales Closing',
  }[coreFunction] || 'Role';

  return [
    createSectionHeader('3', `Role Training: ${role}`),
    createSubsectionTitle('The System You\'re Implementing'),
    createChecklistItem(`Watch: ${functionName} overview`, true),
    createChecklistItem('Read: Our lead-to-close flow → [INSERT DOC]'),
    createSubsectionTitle('Product Knowledge'),
    createChecklistItem('Watch: What we sell and why it works', true),
    createChecklistItem('Read: Client success stories → [INSERT DOC]'),
    createChecklistItem('Watch: Common objections and responses', true),
    createSubsectionTitle('Scripts & Frameworks'),
    createChecklistItem('Watch: Script walkthrough', true),
    new Paragraph({
      children: [
        new TextRun({ text: '☐  ' }),
        new TextRun({ text: 'Practice: Record yourself doing outreach → Submit to manager', italics: true, color: COLORS.gray }),
      ],
      spacing: { after: 80 },
      indent: { left: 400 },
    }),
  ];
}

function createSection4() {
  return [
    createSectionHeader('4', 'Daily Activities'),
    createSubsectionTitle('Your Daily Rhythm'),
    new Table({
      rows: [
        new TableRow({
          children: [
            new TableCell({
              children: [new Paragraph({ children: [new TextRun({ text: 'TIME BLOCK', bold: true, color: COLORS.gold })] })],
              shading: { type: ShadingType.SOLID, color: COLORS.black },
            }),
            new TableCell({
              children: [new Paragraph({ children: [new TextRun({ text: 'ACTIVITY', bold: true, color: COLORS.gold })] })],
              shading: { type: ShadingType.SOLID, color: COLORS.black },
            }),
            new TableCell({
              children: [new Paragraph({ children: [new TextRun({ text: 'DETAILS', bold: true, color: COLORS.gold })] })],
              shading: { type: ShadingType.SOLID, color: COLORS.black },
            }),
          ],
        }),
        new TableRow({
          children: [
            new TableCell({ children: [new Paragraph('First 30 min')] }),
            new TableCell({ children: [new Paragraph('Pipeline Review')] }),
            new TableCell({ children: [new Paragraph('Prioritize leads for the day')] }),
          ],
        }),
        new TableRow({
          children: [
            new TableCell({ children: [new Paragraph('Core hours')] }),
            new TableCell({ children: [new Paragraph('Outreach')] }),
            new TableCell({ children: [new Paragraph('Execute follow-ups and conversations')] }),
          ],
        }),
        new TableRow({
          children: [
            new TableCell({ children: [new Paragraph('End of day')] }),
            new TableCell({ children: [new Paragraph('Reporting')] }),
            new TableCell({ children: [new Paragraph('Update CRM and submit daily report')] }),
          ],
        }),
      ],
      width: { size: 100, type: WidthType.PERCENTAGE },
    }),
    new Paragraph({ spacing: { after: 200 } }),
    createChecklistItem('Watch: Pipeline overview', true),
    createChecklistItem('Watch: Daily workflow walkthrough', true),
  ];
}

function createSection5(compensation) {
  return [
    createSectionHeader('5', 'Scorecard & Compensation'),
    createSubsectionTitle('Your KPIs'),
    new Table({
      rows: [
        new TableRow({
          children: [
            new TableCell({
              children: [new Paragraph({ children: [new TextRun({ text: 'METRIC', bold: true, color: COLORS.gold })] })],
              shading: { type: ShadingType.SOLID, color: COLORS.black },
            }),
            new TableCell({
              children: [new Paragraph({ children: [new TextRun({ text: 'TARGET', bold: true, color: COLORS.gold })] })],
              shading: { type: ShadingType.SOLID, color: COLORS.black },
            }),
            new TableCell({
              children: [new Paragraph({ children: [new TextRun({ text: 'HOW MEASURED', bold: true, color: COLORS.gold })] })],
              shading: { type: ShadingType.SOLID, color: COLORS.black },
            }),
          ],
        }),
        new TableRow({
          children: [
            new TableCell({ children: [new Paragraph('Monthly conversations')] }),
            new TableCell({ children: [new Paragraph('[SET TARGET]')] }),
            new TableCell({ children: [new Paragraph('CRM tracking')] }),
          ],
        }),
        new TableRow({
          children: [
            new TableCell({ children: [new Paragraph('Appointments set')] }),
            new TableCell({ children: [new Paragraph('[SET TARGET]')] }),
            new TableCell({ children: [new Paragraph('Calendar bookings')] }),
          ],
        }),
        new TableRow({
          children: [
            new TableCell({ children: [new Paragraph('Show rate')] }),
            new TableCell({ children: [new Paragraph('65%+')] }),
            new TableCell({ children: [new Paragraph('Appointments kept / booked')] }),
          ],
        }),
      ],
      width: { size: 100, type: WidthType.PERCENTAGE },
    }),
    new Paragraph({ spacing: { after: 200 } }),
    createSubsectionTitle('Compensation'),
    new Paragraph({
      children: [new TextRun({ text: compensation || '[SET COMPENSATION STRUCTURE]' })],
      indent: { left: 400 },
    }),
  ];
}

function createSection6(contact) {
  const contactName = contact || '[SET NAME]';
  return [
    createSectionHeader('6', 'Communication & Support'),
    createSubsectionTitle('Who to Contact'),
    new Table({
      rows: [
        new TableRow({
          children: [
            new TableCell({
              children: [new Paragraph({ children: [new TextRun({ text: 'QUESTION TYPE', bold: true, color: COLORS.gold })] })],
              shading: { type: ShadingType.SOLID, color: COLORS.black },
            }),
            new TableCell({
              children: [new Paragraph({ children: [new TextRun({ text: 'CONTACT', bold: true, color: COLORS.gold })] })],
              shading: { type: ShadingType.SOLID, color: COLORS.black },
            }),
            new TableCell({
              children: [new Paragraph({ children: [new TextRun({ text: 'CHANNEL', bold: true, color: COLORS.gold })] })],
              shading: { type: ShadingType.SOLID, color: COLORS.black },
            }),
          ],
        }),
        new TableRow({
          children: [
            new TableCell({ children: [new Paragraph('Day-to-day questions')] }),
            new TableCell({ children: [new Paragraph(contactName)] }),
            new TableCell({ children: [new Paragraph('Slack DM')] }),
          ],
        }),
        new TableRow({
          children: [
            new TableCell({ children: [new Paragraph('Technical issues')] }),
            new TableCell({ children: [new Paragraph('[SET NAME]')] }),
            new TableCell({ children: [new Paragraph('Slack #tech-support')] }),
          ],
        }),
        new TableRow({
          children: [
            new TableCell({ children: [new Paragraph('Urgent matters')] }),
            new TableCell({ children: [new Paragraph(contactName)] }),
            new TableCell({ children: [new Paragraph('Phone/text')] }),
          ],
        }),
      ],
      width: { size: 100, type: WidthType.PERCENTAGE },
    }),
    new Paragraph({ spacing: { after: 200 } }),
    createSubsectionTitle('Weekly Check-ins'),
    createChecklistItem('[Day/Time]: Team meeting'),
    createChecklistItem('[Day/Time]: 1:1 with manager'),
  ];
}

function createCompletionBox(contact) {
  const contactName = contact || '[manager]';
  return [
    new Paragraph({ spacing: { before: 400 } }),
    new Paragraph({
      children: [
        new TextRun({ text: '✓ Completion Confirmation', bold: true, color: COLORS.gold, size: 24 }),
      ],
      shading: { type: ShadingType.SOLID, color: COLORS.black },
      spacing: { after: 100 },
    }),
    new Paragraph({
      children: [
        new TextRun({ text: '1. Complete all checklist items above\n', color: COLORS.white }),
        new TextRun({ text: `2. Record a 2-minute Loom introducing yourself to the team\n`, color: COLORS.white }),
        new TextRun({ text: `3. Send to ${contactName} with subject: "[Your Name] - Onboarding Complete"\n`, color: COLORS.white }),
        new TextRun({ text: '4. Schedule your first check-in call', color: COLORS.white }),
      ],
      shading: { type: ShadingType.SOLID, color: COLORS.black },
      spacing: { after: 100 },
    }),
    new Paragraph({
      children: [
        new TextRun({ text: 'Welcome to the team!', bold: true, color: COLORS.gold, size: 26 }),
      ],
      shading: { type: ShadingType.SOLID, color: COLORS.black },
    }),
  ];
}

// === EXPORT ===
module.exports = { generatePlaybookDocx };

// === USAGE EXAMPLE ===
/*
const { Packer } = require('docx');
const fs = require('fs');

const doc = generatePlaybookDocx({
  company: 'Acme Coaching',
  role: 'Appointment Setter',
  coreFunction: 'sell-by-chat',
  tools: ['GoHighLevel', 'Slack', 'Google Meet', 'Fathom'],
  contact: 'Sarah Johnson',
  compensation: '$1,250 base + $175 per close',
});

Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync('playbook.docx', buffer);
  console.log('DOCX generated!');
});
*/
