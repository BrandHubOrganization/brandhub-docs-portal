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
import { AstryxBadge, type AstryxBadgeVariant } from './astryx';

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

const ROLE_ASTRYX_VARIANTS: Record<string, AstryxBadgeVariant> = {
  Owner: 'orange',
  Manager: 'info',
  Creator: 'teal',
  Client: 'purple',
  Admin: 'red',
  Guest: 'neutral',
};

const ROLE_ICONS: Record<string, LucideIcon> = {
  Owner: Crown,
  Manager: Briefcase,
  Creator: PenTool,
  Client: Building2,
  Admin: Shield,
  Guest: User,
};

export const RoleBadge: React.FC<RoleBadgeProps> = ({ role }) => {
  const variant = ROLE_ASTRYX_VARIANTS[role] || 'neutral';
  const Icon = ROLE_ICONS[role] || User;

  return (
    <span className="inline-flex items-center">
      <AstryxBadge
        label={role}
        variant={variant}
        icon={<Icon className="w-3 h-3 shrink-0" />}
      />
    </span>
  );
};
