import React from 'react';
import { Badge as AstryxBadge, type BadgeProps as AstryxBadgeProps, type BadgeVariant as AstryxBadgeVariant } from '@astryxdesign/core/Badge';
import { Banner as AstryxBanner, type BannerProps as AstryxBannerProps, type BannerStatus as AstryxBannerStatus } from '@astryxdesign/core/Banner';
import { Button as AstryxButton, type ButtonProps as AstryxButtonProps } from '@astryxdesign/core/Button';
import { IconButton as AstryxIconButton, type IconButtonProps as AstryxIconButtonProps } from '@astryxdesign/core/IconButton';
import { ButtonGroup as AstryxButtonGroup } from '@astryxdesign/core/ButtonGroup';
import { Card as AstryxCard, type CardProps as AstryxCardProps } from '@astryxdesign/core/Card';
import { ClickableCard as AstryxClickableCard } from '@astryxdesign/core/ClickableCard';
import { SelectableCard as AstryxSelectableCard } from '@astryxdesign/core/SelectableCard';
import { EmptyState as AstryxEmptyState, type EmptyStateProps as AstryxEmptyStateProps } from '@astryxdesign/core/EmptyState';
import { Spinner as AstryxSpinner, type SpinnerProps as AstryxSpinnerProps } from '@astryxdesign/core/Spinner';
import { Skeleton as AstryxSkeleton, type SkeletonProps as AstryxSkeletonProps } from '@astryxdesign/core/Skeleton';
import { StatusDot as AstryxStatusDot, type StatusDotProps as AstryxStatusDotProps, type StatusDotVariant as AstryxStatusDotVariant } from '@astryxdesign/core/StatusDot';
import { ProgressBar as AstryxProgressBar, type ProgressBarProps as AstryxProgressBarProps } from '@astryxdesign/core/ProgressBar';
import { Divider as AstryxDivider, type DividerProps as AstryxDividerProps } from '@astryxdesign/core/Divider';
import { Collapsible as AstryxCollapsible, CollapsibleGroup as AstryxCollapsibleGroup } from '@astryxdesign/core/Collapsible';
import { SegmentedControl as AstryxSegmentedControl, SegmentedControlItem as AstryxSegmentedControlItem } from '@astryxdesign/core/SegmentedControl';
import { Switch as AstryxSwitch } from '@astryxdesign/core/Switch';
import { CheckboxInput as AstryxCheckboxInput } from '@astryxdesign/core/CheckboxInput';
import { TextInput as AstryxTextInput } from '@astryxdesign/core/TextInput';
import { TextArea as AstryxTextArea } from '@astryxdesign/core/TextArea';
import { Tooltip as AstryxTooltip } from '@astryxdesign/core/Tooltip';
import { InfoTip as AstryxInfoTip } from '@astryxdesign/core/InfoTip';
import { Popover as AstryxPopover } from '@astryxdesign/core/Popover';
import { Dialog as AstryxDialog } from '@astryxdesign/core/Dialog';
import { Drawer as AstryxDrawer } from '@astryxdesign/core/Drawer';
import { TabList as AstryxTabList, Tab as AstryxTab } from '@astryxdesign/core/TabList';
import { Table as AstryxTable } from '@astryxdesign/core/Table';
import { Pagination as AstryxPagination } from '@astryxdesign/core/Pagination';
import { Breadcrumbs as AstryxBreadcrumbs, BreadcrumbItem as AstryxBreadcrumbItem } from '@astryxdesign/core/Breadcrumbs';
import { Avatar as AstryxAvatar } from '@astryxdesign/core/Avatar';
import { AvatarGroup as AstryxAvatarGroup } from '@astryxdesign/core/AvatarGroup';
import { Stepper as AstryxStepper, Step as AstryxStep } from '@astryxdesign/core/Stepper';
import { Kbd as AstryxKbd } from '@astryxdesign/core/Kbd';
import { Code as AstryxCode } from '@astryxdesign/core/Code';
import { HStack as AstryxHStack } from '@astryxdesign/core/HStack';
import { VStack as AstryxVStack } from '@astryxdesign/core/VStack';
import { Stack as AstryxStack } from '@astryxdesign/core/Stack';
import { Grid as AstryxGrid } from '@astryxdesign/core/Grid';
import { Section as AstryxSection } from '@astryxdesign/core/Section';
import { Toolbar as AstryxToolbar } from '@astryxdesign/core/Toolbar';
import { Heading as AstryxHeading } from '@astryxdesign/core/Heading';
import { Text as AstryxText } from '@astryxdesign/core/Text';
import { MetadataList as AstryxMetadataList, MetadataListItem as AstryxMetadataListItem } from '@astryxdesign/core/MetadataList';

export {
  AstryxBadge,
  AstryxBanner,
  AstryxButton,
  AstryxIconButton,
  AstryxButtonGroup,
  AstryxCard,
  AstryxClickableCard,
  AstryxSelectableCard,
  AstryxEmptyState,
  AstryxSpinner,
  AstryxSkeleton,
  AstryxStatusDot,
  AstryxProgressBar,
  AstryxDivider,
  AstryxCollapsible,
  AstryxCollapsibleGroup,
  AstryxSegmentedControl,
  AstryxSegmentedControlItem,
  AstryxSwitch,
  AstryxCheckboxInput,
  AstryxTextInput,
  AstryxTextArea,
  AstryxTooltip,
  AstryxInfoTip,
  AstryxPopover,
  AstryxDialog,
  AstryxDrawer,
  AstryxTabList,
  AstryxTab,
  AstryxTable,
  AstryxPagination,
  AstryxBreadcrumbs,
  AstryxBreadcrumbItem,
  AstryxAvatar,
  AstryxAvatarGroup,
  AstryxStepper,
  AstryxStep,
  AstryxKbd,
  AstryxCode,
  AstryxHStack,
  AstryxVStack,
  AstryxStack,
  AstryxGrid,
  AstryxSection,
  AstryxToolbar,
  AstryxHeading,
  AstryxText,
  AstryxMetadataList,
  AstryxMetadataListItem,
};

export type {
  AstryxBadgeProps,
  AstryxBadgeVariant,
  AstryxBannerProps,
  AstryxBannerStatus,
  AstryxButtonProps,
  AstryxIconButtonProps,
  AstryxCardProps,
  AstryxEmptyStateProps,
  AstryxSpinnerProps,
  AstryxSkeletonProps,
  AstryxStatusDotProps,
  AstryxStatusDotVariant,
  AstryxProgressBarProps,
  AstryxDividerProps,
};

export const BhEmptyState: React.FC<{
  title: string;
  description?: string;
  icon?: React.ReactNode;
  actions?: React.ReactNode;
  isCompact?: boolean;
  className?: string;
}> = ({ title, description, icon, actions, isCompact = false, className = '' }) => (
  <div className={`rounded-xl border border-dashed border-orange-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 ${className}`}>
    <AstryxEmptyState
      title={title}
      description={description}
      icon={
        icon ? (
          <span className="inline-flex w-10 h-10 items-center justify-center rounded-xl border border-orange-200 bg-orange-50 text-orange-600">
            {icon}
          </span>
        ) : undefined
      }
      actions={actions}
      isCompact={isCompact}
    />
  </div>
);

export const BhBanner: React.FC<{
  status?: AstryxBannerStatus;
  title: React.ReactNode;
  description?: React.ReactNode;
  icon?: React.ReactNode;
  isDismissable?: boolean;
  onDismiss?: () => void;
  className?: string;
  children?: React.ReactNode;
}> = ({
  status = 'info',
  title,
  description,
  icon,
  isDismissable = false,
  onDismiss,
  className = '',
  children,
}) => (
  <div className={`w-full min-w-0 ${className}`}>
    <AstryxBanner
      status={status}
      title={title}
      description={description}
      icon={icon}
      isDismissable={isDismissable}
      onDismiss={onDismiss}
      collapsible={false}
    >
      {children}
    </AstryxBanner>
  </div>
);
