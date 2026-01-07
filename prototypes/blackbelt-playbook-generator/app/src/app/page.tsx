'use client';

import { useState } from 'react';
import Image from 'next/image';
import { PlaybookFormData, CORE_FUNCTIONS, DEFAULT_TOOLS, GenerateResponse } from '@/lib/types';
import { Document, Packer, Paragraph, TextRun, BorderStyle, HeadingLevel, Table, TableRow, TableCell, WidthType, PageBreak } from 'docx';
import { saveAs } from 'file-saver';

type Screen = 'form' | 'loading' | 'success';

export default function Home() {
  const [screen, setScreen] = useState<Screen>('form');
  const [selectedTools, setSelectedTools] = useState<string[]>([]);
  const [otherTools, setOtherTools] = useState('');
  const [generatedContent, setGeneratedContent] = useState('');
  const [loadingStep, setLoadingStep] = useState(0);
  const [copied, setCopied] = useState(false);
  const [formData, setFormData] = useState<PlaybookFormData>({
    company: '',
    role: '',
    coreFunction: '',
    tools: [],
    contact: '',
    basePay: '',
    closeBonus: '',
    performanceThreshold: '',
    performanceBonus: '',
    hoursPerWeek: '',
    workingHours: '',
    remoteRequirements: '',
    winsChannel: '',
  });

  const toggleTool = (tool: string) => {
    setSelectedTools(prev =>
      prev.includes(tool) ? prev.filter(t => t !== tool) : [...prev, tool]
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const allTools = [
      ...selectedTools,
      ...otherTools.split(',').map(t => t.trim()).filter(Boolean),
    ];

    const submitData: PlaybookFormData = {
      ...formData,
      tools: allTools,
    };

    setScreen('loading');
    setLoadingStep(0);

    try {
      // Simulate step progress
      setTimeout(() => setLoadingStep(1), 500);
      setTimeout(() => setLoadingStep(2), 1500);
      setTimeout(() => setLoadingStep(3), 2500);

      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(submitData),
      });

      const result: GenerateResponse = await response.json();

      if (result.success && result.content) {
        setGeneratedContent(result.content);
        setTimeout(() => setScreen('success'), 500);
      } else {
        alert(result.error || 'Failed to generate playbook');
        setScreen('form');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to generate playbook. Please try again.');
      setScreen('form');
    }
  };

  const downloadMarkdown = () => {
    const blob = new Blob([generatedContent], { type: 'text/markdown' });
    const filename = `${formData.company.replace(/\s+/g, '-')}-${formData.role.replace(/\s+/g, '-')}-Playbook.md`;
    saveAs(blob, filename);
  };

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(generatedContent);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Fallback for older browsers
      const textArea = document.createElement('textarea');
      textArea.value = generatedContent;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  // Parse markdown and convert to docx elements (paragraphs + tables)
  const parseMarkdownToDocx = (markdown: string): (Paragraph | Table)[] => {
    const elements: (Paragraph | Table)[] = [];
    const lines = markdown.split('\n');
    let isFirstH2 = true;

    // Helper to parse inline formatting (bold, etc.)
    const parseInlineFormatting = (text: string): TextRun[] => {
      const runs: TextRun[] = [];
      const parts = text.split(/(\*\*[^*]+\*\*)/g);

      for (const part of parts) {
        if (part.startsWith('**') && part.endsWith('**')) {
          runs.push(new TextRun({ text: part.slice(2, -2), bold: true, font: 'Arial', size: 22 }));
        } else if (part) {
          runs.push(new TextRun({ text: part, font: 'Arial', size: 22 }));
        }
      }
      return runs;
    };

    // Helper to parse a markdown table row into cells
    const parseTableRow = (line: string): string[] => {
      return line.split('|').slice(1, -1).map(cell => cell.trim());
    };

    // Helper to check if line is a table separator (|---|---|)
    const isTableSeparator = (line: string): boolean => {
      return /^\|[\s\-:]+\|/.test(line) && line.includes('---');
    };

    let i = 0;
    while (i < lines.length) {
      const line = lines[i];

      // Skip empty lines
      if (!line.trim()) {
        elements.push(new Paragraph({ children: [], spacing: { after: 120 } }));
        i++;
        continue;
      }

      // H1: # Header
      if (line.startsWith('# ')) {
        elements.push(new Paragraph({
          children: [new TextRun({ text: line.slice(2), bold: true, font: 'Arial', size: 36 })],
          heading: HeadingLevel.HEADING_1,
          spacing: { before: 400, after: 200 },
        }));
        i++;
        continue;
      }

      // H2: ## Header - Add page break before (except first)
      if (line.startsWith('## ')) {
        if (!isFirstH2) {
          // Add page break before this section
          elements.push(new Paragraph({
            children: [new PageBreak()],
          }));
        }
        isFirstH2 = false;

        elements.push(new Paragraph({
          children: [new TextRun({ text: line.slice(3), bold: true, font: 'Arial', size: 28, color: 'EFBB39' })],
          heading: HeadingLevel.HEADING_2,
          spacing: { before: 300, after: 160 },
        }));
        i++;
        continue;
      }

      // H3: ### Header
      if (line.startsWith('### ')) {
        elements.push(new Paragraph({
          children: [new TextRun({ text: line.slice(4), bold: true, font: 'Arial', size: 24 })],
          heading: HeadingLevel.HEADING_3,
          spacing: { before: 240, after: 120 },
        }));
        i++;
        continue;
      }

      // Horizontal rule: ---
      if (line.trim() === '---') {
        elements.push(new Paragraph({
          children: [],
          border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: 'CCCCCC' } },
          spacing: { before: 200, after: 200 },
        }));
        i++;
        continue;
      }

      // Table: starts with | and has more content
      if (line.trim().startsWith('|') && line.trim().endsWith('|')) {
        const tableLines: string[] = [];

        // Collect all table lines
        while (i < lines.length && lines[i].trim().startsWith('|') && lines[i].trim().endsWith('|')) {
          tableLines.push(lines[i]);
          i++;
        }

        if (tableLines.length >= 2) {
          const headerCells = parseTableRow(tableLines[0]);
          const dataRows: string[][] = [];

          // Skip separator line (index 1), collect data rows
          for (let j = 2; j < tableLines.length; j++) {
            if (!isTableSeparator(tableLines[j])) {
              dataRows.push(parseTableRow(tableLines[j]));
            }
          }

          // Create Word table
          const table = new Table({
            width: { size: 100, type: WidthType.PERCENTAGE },
            rows: [
              // Header row
              new TableRow({
                children: headerCells.map(cell => new TableCell({
                  children: [new Paragraph({
                    children: [new TextRun({ text: cell, bold: true, font: 'Arial', size: 20 })],
                  })],
                  shading: { fill: 'F5F5F5' },
                })),
              }),
              // Data rows
              ...dataRows.map(row => new TableRow({
                children: row.map(cell => new TableCell({
                  children: [new Paragraph({
                    children: parseInlineFormatting(cell),
                  })],
                })),
              })),
            ],
          });

          elements.push(table);
          elements.push(new Paragraph({ children: [], spacing: { after: 200 } })); // Space after table
        }
        continue;
      }

      // Checkbox: - [ ] or - [x]
      if (line.match(/^-\s*\[\s*[xX]?\s*\]/)) {
        const isChecked = line.match(/^-\s*\[\s*[xX]\s*\]/);
        const content = line.replace(/^-\s*\[\s*[xX]?\s*\]\s*/, '');
        const checkMark = isChecked ? '☑' : '☐';
        elements.push(new Paragraph({
          children: [
            new TextRun({ text: `${checkMark}  `, font: 'Arial', size: 22 }),
            ...parseInlineFormatting(content),
          ],
          spacing: { after: 80 },
          indent: { left: 360 },
        }));
        i++;
        continue;
      }

      // Bullet point: - item
      if (line.startsWith('- ')) {
        elements.push(new Paragraph({
          children: [
            new TextRun({ text: '•  ', font: 'Arial', size: 22 }),
            ...parseInlineFormatting(line.slice(2)),
          ],
          spacing: { after: 80 },
          indent: { left: 360 },
        }));
        i++;
        continue;
      }

      // Regular paragraph with inline formatting
      elements.push(new Paragraph({
        children: parseInlineFormatting(line),
        spacing: { after: 120 },
      }));
      i++;
    }

    return elements;
  };

  const downloadDocx = async () => {
    const contentParagraphs = parseMarkdownToDocx(generatedContent);

    const doc = new Document({
      styles: {
        default: {
          document: {
            run: { font: 'Arial', size: 22 },
          },
        },
      },
      sections: [{
        properties: {
          page: { margin: { top: 1134, right: 850, bottom: 1134, left: 850 } },
        },
        children: [
          // Header: Company Name
          new Paragraph({
            children: [new TextRun({ text: formData.company, bold: true, font: 'Arial', size: 48 })],
            spacing: { after: 120 },
          }),
          // Subheader: Role Playbook with gold underline
          new Paragraph({
            children: [new TextRun({ text: `${formData.role} Playbook`, bold: true, font: 'Arial', size: 28, color: 'EFBB39' })],
            border: { bottom: { style: BorderStyle.SINGLE, size: 18, color: 'EFBB39' } },
            spacing: { after: 400 },
          }),
          // Parsed markdown content
          ...contentParagraphs,
        ],
      }],
    });

    const buffer = await Packer.toBlob(doc);
    const filename = `${formData.company.replace(/\s+/g, '-')}-${formData.role.replace(/\s+/g, '-')}-Playbook.docx`;
    saveAs(buffer, filename);
  };

  const resetForm = () => {
    setScreen('form');
    setSelectedTools([]);
    setOtherTools('');
    setGeneratedContent('');
    setLoadingStep(0);
    setFormData({
      company: '',
      role: '',
      coreFunction: '',
      tools: [],
      contact: '',
      basePay: '',
      closeBonus: '',
      performanceThreshold: '',
      performanceBonus: '',
      hoursPerWeek: '',
      workingHours: '',
      remoteRequirements: '',
      winsChannel: '',
    });
  };

  return (
    <main className="min-h-screen bg-black text-white">
      {/* Background pattern */}
      <div className="fixed inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:60px_60px] pointer-events-none" />

      {/* Gold glow */}
      <div className="fixed w-[600px] h-[600px] bg-[radial-gradient(circle,rgba(239,187,57,0.3)_0%,transparent_70%)] rounded-full -top-[200px] -right-[200px] pointer-events-none animate-pulse" />

      <div className="relative z-10 max-w-[720px] mx-auto px-6 py-16">
        {/* Header */}
        <header className="text-center mb-16 animate-fade-in">
          <div className="flex justify-center mb-8">
            <Image src="/blackbelt-logo-white.png" alt="BlackBelt" width={180} height={58} priority />
          </div>
          <h1 className="text-4xl md:text-5xl font-black tracking-tight mb-4">
            Build Your <span className="text-[#EFBB39]">Playbook</span>
          </h1>
          <p className="text-lg text-gray-400 max-w-md mx-auto">
            Generate a professional onboarding playbook for any role in 30 seconds. No more reinventing the wheel.
          </p>
        </header>

        {/* Form Screen */}
        {screen === 'form' && (
          <div className="bg-gradient-to-b from-[#141414] to-[#0A0A0A] border border-[#1F1F1F] rounded-2xl p-10 shadow-2xl animate-slide-up">
            <form onSubmit={handleSubmit}>
              {/* The Basics */}
              <div className="mb-8">
                <div className="text-xs font-bold tracking-widest text-[#EFBB39] mb-5 flex items-center gap-3">
                  THE BASICS <span className="flex-1 h-px bg-[#1F1F1F]" />
                </div>
                <div className="grid grid-cols-2 gap-5">
                  <div>
                    <label className="block text-sm font-semibold mb-2">Company Name</label>
                    <input
                      type="text"
                      required
                      placeholder="e.g., Acme Coaching"
                      value={formData.company}
                      onChange={e => setFormData(prev => ({ ...prev, company: e.target.value }))}
                      className="w-full px-4 py-3.5 bg-white/5 border-2 border-gray-500 rounded-lg text-white placeholder-gray-500 focus:border-[#EFBB39] focus:bg-[rgba(239,187,57,0.05)] focus:outline-none transition-all"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold mb-2">Role Name</label>
                    <input
                      type="text"
                      required
                      placeholder="e.g., Appointment Setter"
                      value={formData.role}
                      onChange={e => setFormData(prev => ({ ...prev, role: e.target.value }))}
                      className="w-full px-4 py-3.5 bg-white/5 border-2 border-gray-500 rounded-lg text-white placeholder-gray-500 focus:border-[#EFBB39] focus:bg-[rgba(239,187,57,0.05)] focus:outline-none transition-all"
                    />
                  </div>
                </div>
              </div>

              {/* Role Details */}
              <div className="mb-8">
                <div className="text-xs font-bold tracking-widest text-[#EFBB39] mb-5 flex items-center gap-3">
                  ROLE DETAILS <span className="flex-1 h-px bg-[#1F1F1F]" />
                </div>
                <label className="block text-sm font-semibold mb-2">Core Function</label>
                <select
                  required
                  value={formData.coreFunction}
                  onChange={e => setFormData(prev => ({ ...prev, coreFunction: e.target.value }))}
                  className="w-full px-4 py-3.5 bg-white/5 border-2 border-gray-500 rounded-lg text-white focus:border-[#EFBB39] focus:outline-none transition-all cursor-pointer appearance-none bg-no-repeat bg-[right_16px_center] pr-12"
                  style={{ backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23666666' stroke-width='2'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E")` }}
                >
                  <option value="" disabled>Select their primary function...</option>
                  {CORE_FUNCTIONS.map(func => (
                    <option key={func.value} value={func.value}>{func.label}</option>
                  ))}
                </select>
              </div>

              {/* Tech Stack */}
              <div className="mb-8">
                <div className="text-xs font-bold tracking-widest text-[#EFBB39] mb-5 flex items-center gap-3">
                  TECH STACK <span className="flex-1 h-px bg-[#1F1F1F]" />
                </div>
                <label className="block text-sm font-semibold mb-3">Tools They&apos;ll Use</label>
                <div className="flex flex-wrap gap-2.5 mb-4">
                  {DEFAULT_TOOLS.map(tool => (
                    <button
                      key={tool}
                      type="button"
                      onClick={() => toggleTool(tool)}
                      className={`px-4 py-2.5 rounded-full text-sm font-medium transition-all flex items-center gap-2 ${
                        selectedTools.includes(tool)
                          ? 'bg-[#EFBB39] text-black border border-[#EFBB39]'
                          : 'bg-[#0A0A0A] text-gray-400 border border-[#2A2A2A] hover:border-gray-500 hover:text-white'
                      }`}
                    >
                      <span className={`w-4 h-4 border-2 rounded flex items-center justify-center text-xs ${
                        selectedTools.includes(tool) ? 'border-black bg-black text-[#EFBB39]' : 'border-current'
                      }`}>
                        {selectedTools.includes(tool) && '✓'}
                      </span>
                      {tool}
                    </button>
                  ))}
                </div>
                <label className="block text-sm font-semibold mb-2">
                  Other Tools <span className="font-normal text-gray-500 text-xs ml-2">Comma-separated</span>
                </label>
                <input
                  type="text"
                  placeholder="e.g., Asana, Monday, Hubspot"
                  value={otherTools}
                  onChange={e => setOtherTools(e.target.value)}
                  className="w-full px-4 py-3.5 bg-white/5 border-2 border-gray-500 rounded-lg text-white placeholder-gray-500 focus:border-[#EFBB39] focus:outline-none transition-all"
                />
              </div>

              {/* Compensation */}
              <div className="mb-8">
                <div className="text-xs font-bold tracking-widest text-[#EFBB39] mb-5 flex items-center gap-3">
                  COMPENSATION STRUCTURE <span className="font-normal text-gray-500 tracking-normal text-[10px]">Optional</span> <span className="flex-1 h-px bg-[#1F1F1F]" />
                </div>
                <div className="grid grid-cols-2 gap-5 mb-4">
                  <div>
                    <label className="block text-sm font-semibold mb-2">
                      Base Pay <span className="font-normal text-gray-500 text-xs">per month</span>
                    </label>
                    <input
                      type="text"
                      placeholder="e.g., $1,250"
                      value={formData.basePay}
                      onChange={e => setFormData(prev => ({ ...prev, basePay: e.target.value }))}
                      className="w-full px-4 py-3.5 bg-white/5 border-2 border-gray-500 rounded-lg text-white placeholder-gray-500 focus:border-[#EFBB39] focus:outline-none transition-all"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold mb-2">
                      Close Bonus <span className="font-normal text-gray-500 text-xs">per sale</span>
                    </label>
                    <input
                      type="text"
                      placeholder="e.g., $175"
                      value={formData.closeBonus}
                      onChange={e => setFormData(prev => ({ ...prev, closeBonus: e.target.value }))}
                      className="w-full px-4 py-3.5 bg-white/5 border-2 border-gray-500 rounded-lg text-white placeholder-gray-500 focus:border-[#EFBB39] focus:outline-none transition-all"
                    />
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-5">
                  <div>
                    <label className="block text-sm font-semibold mb-2">
                      Performance Threshold <span className="font-normal text-gray-500 text-xs">closes to hit</span>
                    </label>
                    <input
                      type="text"
                      placeholder="e.g., 6 closes"
                      value={formData.performanceThreshold}
                      onChange={e => setFormData(prev => ({ ...prev, performanceThreshold: e.target.value }))}
                      className="w-full px-4 py-3.5 bg-white/5 border-2 border-gray-500 rounded-lg text-white placeholder-gray-500 focus:border-[#EFBB39] focus:outline-none transition-all"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold mb-2">
                      Performance Bonus <span className="font-normal text-gray-500 text-xs">at threshold</span>
                    </label>
                    <input
                      type="text"
                      placeholder="e.g., $200"
                      value={formData.performanceBonus}
                      onChange={e => setFormData(prev => ({ ...prev, performanceBonus: e.target.value }))}
                      className="w-full px-4 py-3.5 bg-white/5 border-2 border-gray-500 rounded-lg text-white placeholder-gray-500 focus:border-[#EFBB39] focus:outline-none transition-all"
                    />
                  </div>
                </div>
              </div>

              {/* Time Expectations */}
              <div className="mb-8">
                <div className="text-xs font-bold tracking-widest text-[#EFBB39] mb-5 flex items-center gap-3">
                  TIME EXPECTATIONS <span className="font-normal text-gray-500 tracking-normal text-[10px]">Optional</span> <span className="flex-1 h-px bg-[#1F1F1F]" />
                </div>
                <div className="grid grid-cols-2 gap-5 mb-4">
                  <div>
                    <label className="block text-sm font-semibold mb-2">Hours Per Week</label>
                    <input
                      type="text"
                      placeholder="e.g., 40-50"
                      value={formData.hoursPerWeek}
                      onChange={e => setFormData(prev => ({ ...prev, hoursPerWeek: e.target.value }))}
                      className="w-full px-4 py-3.5 bg-white/5 border-2 border-gray-500 rounded-lg text-white placeholder-gray-500 focus:border-[#EFBB39] focus:outline-none transition-all"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold mb-2">Working Hours</label>
                    <input
                      type="text"
                      placeholder="e.g., 8 AM - 5 PM EST"
                      value={formData.workingHours}
                      onChange={e => setFormData(prev => ({ ...prev, workingHours: e.target.value }))}
                      className="w-full px-4 py-3.5 bg-white/5 border-2 border-gray-500 rounded-lg text-white placeholder-gray-500 focus:border-[#EFBB39] focus:outline-none transition-all"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-semibold mb-2">
                    Remote Requirements <span className="font-normal text-gray-500 text-xs">Optional</span>
                  </label>
                  <input
                    type="text"
                    placeholder="e.g., Strong Wi-Fi and quiet environment required"
                    value={formData.remoteRequirements}
                    onChange={e => setFormData(prev => ({ ...prev, remoteRequirements: e.target.value }))}
                    className="w-full px-4 py-3.5 bg-white/5 border-2 border-gray-500 rounded-lg text-white placeholder-gray-500 focus:border-[#EFBB39] focus:outline-none transition-all"
                  />
                </div>
              </div>

              {/* Contact & Culture */}
              <div className="mb-8">
                <div className="text-xs font-bold tracking-widest text-[#EFBB39] mb-5 flex items-center gap-3">
                  CONTACT & CULTURE <span className="font-normal text-gray-500 tracking-normal text-[10px]">Optional</span> <span className="flex-1 h-px bg-[#1F1F1F]" />
                </div>
                <div className="grid grid-cols-2 gap-5">
                  <div>
                    <label className="block text-sm font-semibold mb-2">Manager / Contact</label>
                    <input
                      type="text"
                      placeholder="e.g., Sarah Johnson"
                      value={formData.contact}
                      onChange={e => setFormData(prev => ({ ...prev, contact: e.target.value }))}
                      className="w-full px-4 py-3.5 bg-white/5 border-2 border-gray-500 rounded-lg text-white placeholder-gray-500 focus:border-[#EFBB39] focus:outline-none transition-all"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold mb-2">
                      Wins Channel <span className="font-normal text-gray-500 text-xs">Slack channel</span>
                    </label>
                    <input
                      type="text"
                      placeholder="e.g., #wins"
                      value={formData.winsChannel}
                      onChange={e => setFormData(prev => ({ ...prev, winsChannel: e.target.value }))}
                      className="w-full px-4 py-3.5 bg-white/5 border-2 border-gray-500 rounded-lg text-white placeholder-gray-500 focus:border-[#EFBB39] focus:outline-none transition-all"
                    />
                  </div>
                </div>
              </div>

              <button
                type="submit"
                className="w-full py-4 bg-[#EFBB39] hover:bg-[#D4A62F] text-black font-bold rounded-lg flex items-center justify-center gap-3 transition-all hover:-translate-y-0.5 hover:shadow-[0_8px_24px_rgba(239,187,57,0.3)]"
              >
                <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
                </svg>
                Generate Playbook
              </button>
            </form>
          </div>
        )}

        {/* Loading Screen */}
        {screen === 'loading' && (
          <div className="bg-gradient-to-b from-[#141414] to-[#0A0A0A] border border-[#1F1F1F] rounded-2xl p-20 text-center">
            <div className="w-20 h-20 mx-auto mb-8 relative">
              <div className="absolute inset-0 border-4 border-[#1F1F1F] border-t-[#EFBB39] rounded-full animate-spin" />
              <div className="absolute inset-2 border-4 border-[#1F1F1F] border-t-[#00A2FF] rounded-full animate-spin" style={{ animationDirection: 'reverse', animationDuration: '1.5s' }} />
            </div>
            <h2 className="text-xl font-bold mb-3">Building Your Playbook</h2>
            <p className="text-gray-500 text-sm mb-10">This takes about 10-15 seconds...</p>

            <div className="flex flex-col gap-4 max-w-[300px] mx-auto">
              {[
                'Analyzing role requirements...',
                'Generating onboarding structure...',
                'Finalizing your playbook...',
              ].map((text, i) => (
                <div
                  key={i}
                  className={`flex items-center gap-3 px-4 py-3 bg-[#141414] rounded-lg text-sm transition-all duration-500 ${
                    loadingStep > i ? 'text-[#EFBB39]' : 'text-gray-500'
                  } ${loadingStep >= i ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-5'}`}
                >
                  <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${
                    loadingStep > i ? 'bg-[#EFBB39] text-black' : 'bg-[#1F1F1F]'
                  }`}>
                    {loadingStep > i ? '✓' : i + 1}
                  </span>
                  {text}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Success Screen */}
        {screen === 'success' && (
          <div>
            <div className="text-center mb-8">
              <span className="inline-flex items-center gap-2 px-4 py-2 bg-[rgba(239,187,57,0.1)] border border-[#EFBB39] rounded-full text-[#EFBB39] text-sm font-semibold mb-4">
                <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                  <polyline points="22,4 12,14.01 9,11.01"/>
                </svg>
                Playbook Ready
              </span>
              <h2 className="text-2xl font-extrabold mb-2">{formData.company} - {formData.role} Playbook Ready!</h2>
              <p className="text-gray-500">Download in your preferred format below.</p>
            </div>

            <div className="grid grid-cols-2 gap-4 mb-8">
              <button
                onClick={downloadDocx}
                className="py-4 bg-[#EFBB39] hover:bg-[#D4A62F] text-black font-semibold rounded-lg flex items-center justify-center gap-2.5 transition-all hover:-translate-y-0.5 hover:shadow-[0_8px_24px_rgba(239,187,57,0.3)]"
              >
                <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14,2 14,8 20,8"/>
                </svg>
                Download DOCX
              </button>
              <button
                onClick={downloadMarkdown}
                className="py-4 bg-transparent border border-[#2A2A2A] hover:border-white hover:bg-[#141414] text-white font-semibold rounded-lg flex items-center justify-center gap-2.5 transition-all"
              >
                <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14,2 14,8 20,8"/>
                  <line x1="16" y1="13" x2="8" y2="13"/>
                  <line x1="16" y1="17" x2="8" y2="17"/>
                </svg>
                Download Markdown
              </button>
            </div>

            {/* Preview */}
            <div className="relative bg-[#141414] border border-[#1F1F1F] rounded-xl p-6 mb-8 max-h-[400px] overflow-y-auto">
              {/* Copy button */}
              <button
                onClick={copyToClipboard}
                className="absolute top-4 right-4 p-2 bg-[#1F1F1F] hover:bg-[#2A2A2A] border border-[#2A2A2A] rounded-lg text-gray-400 hover:text-white transition-all"
                title="Copy to clipboard"
              >
                {copied ? (
                  <svg className="w-5 h-5 text-[#EFBB39]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="20,6 9,17 4,12"/>
                  </svg>
                ) : (
                  <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
                    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
                  </svg>
                )}
              </button>
              <pre className="whitespace-pre-wrap text-sm text-gray-300 font-mono pr-12">{generatedContent}</pre>
            </div>

            <button
              onClick={resetForm}
              className="flex items-center gap-2 text-gray-500 hover:text-white transition-colors text-sm"
            >
              <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="19" y1="12" x2="5" y2="12"/>
                <polyline points="12,19 5,12 12,5"/>
              </svg>
              Generate another playbook
            </button>
          </div>
        )}

        {/* Footer */}
        <footer className="text-center mt-16 pt-8 border-t border-[#141414] text-gray-500 text-sm">
          Powered by <span className="text-[#EFBB39]">BlackBelt</span> • Built for coaches who ship
        </footer>
      </div>
    </main>
  );
}
