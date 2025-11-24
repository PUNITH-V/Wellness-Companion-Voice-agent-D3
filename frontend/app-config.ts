export interface AppConfig {
  pageTitle: string;
  pageDescription: string;
  companyName: string;

  supportsChatInput: boolean;
  supportsVideoInput: boolean;
  supportsScreenShare: boolean;
  isPreConnectBufferEnabled: boolean;

  logo: string;
  startButtonText: string;
  accent?: string;
  logoDark?: string;
  accentDark?: string;

  // for LiveKit Cloud Sandbox
  sandboxId?: string;
  agentName?: string;
}

export const APP_CONFIG_DEFAULTS: AppConfig = {
  companyName: 'Wellness Companion',
  pageTitle: 'Wellness Companion - Daily Check-in',
  pageDescription: 'Your AI-powered wellness companion for daily mood tracking and goal setting',

  supportsChatInput: true,
  supportsVideoInput: false,
  supportsScreenShare: false,
  isPreConnectBufferEnabled: true,

  logo: '/lk-logo.svg',
  accent: '#84a98c',
  logoDark: '/lk-logo-dark.svg',
  accentDark: '#a8c5b8',
  startButtonText: 'Begin Check-in',

  // for LiveKit Cloud Sandbox
  sandboxId: undefined,
  agentName: undefined,
};
