import React from 'react';
import {
  User,
  Crown,
  Briefcase,
  PenTool,
  Building2,
  Shield,
  type LucideIcon,
} from 'lucide-react';
import { CanonicalRole } from '../types/portal';

export const CANONICAL_ROLES: CanonicalRole[] = [
  'Guest',
  'Owner',
  'Manager',
  'Creator',
  'Client',
  'Admin',
];

interface RoleBadgeProps {
  role: CanonicalRole | string;
  size?: 'sm' | 'md';
}

const ROLE_STYLES: Record<string, string> = {
  Owner:
    'border-sky-200 bg-sky-50 text-sky-800 dark:border-sky-800/70 dark:bg-sky-950/60 dark:text-sky-300',
  Manager:
    'border-sky-200 bg-sky-50/70 text-sky-700 dark:border-sky-800/50 dark:bg-sky-950/40 dark:text-sky-300',
  Creator:
    'border-slate-200 bg-slate-100 text-slate-700 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300',
  Client:
    'border-slate-200 bg-slate-100 text-slate-700 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300',
  Admin:
    'border-slate-700 bg-slate-800 text-white dark:border-sky-500/40 dark:bg-sky-600 dark:text-white',
  Guest:
    'border-slate-200 bg-slate-50 text-slate-500 dark:border-slate-800 dark:bg-slate-900 dark:text-slate-400',
};

const ROLE_ICONS: Record<string, LucideIcon> = {
  Owner: Crown,
  Manager: Briefcase,
  Creator: PenTool,
  Client: Building2,
  Admin: Shield,
  Guest: User,
};

export const RoleBadge: React.FC<RoleBadgeProps> = ({ role, size = 'sm' }) => {
  const sizeCls =
    size === 'sm' ? 'px-2 py-0.5 text-[11px] gap-1' : 'px-2.5 py-0.5 text-xs gap-1.5';
  const colorCls =
    ROLE_STYLES[role] ||
    'border-slate-200 bg-slate-100 text-slate-700 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300';
  const Icon = ROLE_ICONS[role] || User;

  return (
    <span
      className={`inline-flex items-center font-mono font-medium rounded border transition-colors ${colorCls} ${sizeCls}`}
    >
      <Icon className="w-2.5 h-2.5 shrink-0 opacity-80" />
      <span>{role}</span>
    </span>
  );
};
