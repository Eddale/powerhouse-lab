export interface PlaybookFormData {
  company: string;
  role: string;
  coreFunction: string;
  tools: string[];
  contact: string;
  // Compensation
  basePay: string;
  closeBonus: string;
  performanceThreshold: string;
  performanceBonus: string;
  // Time
  hoursPerWeek: string;
  workingHours: string;
  remoteRequirements: string;
  // Culture
  winsChannel: string;
}

export interface GenerateResponse {
  success: boolean;
  content?: string;
  error?: string;
}

export const CORE_FUNCTIONS = [
  { value: 'sell-by-chat', label: 'Sell by Chat' },
  { value: 'customer-success', label: 'Customer Success' },
  { value: 'community', label: 'Community Management' },
  { value: 'operations', label: 'Operations / Integrator' },
  { value: 'closer', label: 'Sales Closer' },
  { value: 'other', label: 'Other' },
] as const;

export const DEFAULT_TOOLS = [
  'GoHighLevel',
  'Slack',
  'Google Meet',
  'Fathom',
  'Calendly',
  'Zoom',
  'Notion',
  'ClickUp',
] as const;
