import React, { useState } from 'react';
import { Copy, Check, Link2, ExternalLink } from 'lucide-react';
import { AstryxButton, AstryxCard, AstryxCode } from './astryx';

interface CopyLinkBarProps {
  path: string;
  label: string;
  cloudinaryUrl?: string;
}

export function getPortalBaseUrl(): string {
  if (typeof window === 'undefined') return 'http://localhost:5180';
  const saved = localStorage.getItem('brandhub_portal_base_url');
  if (saved && saved.trim()) {
    return saved.trim().replace(/\/+$/, '');
  }
  return window.location.origin;
}

export function setPortalBaseUrl(url: string): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem('brandhub_portal_base_url', url.trim().replace(/\/+$/, ''));
}

export const CopyLinkBar: React.FC<CopyLinkBarProps> = ({ path, label, cloudinaryUrl }) => {
  const [copiedPage, setCopiedPage] = useState(false);
  const [copiedImg, setCopiedImg] = useState(false);

  const fullUrl = `${getPortalBaseUrl()}${path.startsWith('/') ? path : '/' + path}`;

  const handleCopyPage = () => {
    navigator.clipboard.writeText(fullUrl);
    setCopiedPage(true);
    setTimeout(() => setCopiedPage(false), 2000);
  };

  const handleCopyImg = () => {
    if (!cloudinaryUrl) return;
    navigator.clipboard.writeText(cloudinaryUrl);
    setCopiedImg(true);
    setTimeout(() => setCopiedImg(false), 2000);
  };

  return (
    <AstryxCard
      variant="orange"
      padding={3}
      className="flex flex-wrap items-center justify-between gap-3 bg-orange-50/70 border border-orange-200 rounded-xl px-4 py-2.5"
    >
      <div className="flex items-center gap-2.5 min-w-0 flex-1">
        <div className="p-1.5 rounded-lg bg-orange-600 text-white shrink-0">
          <Link2 className="w-4 h-4" />
        </div>
        <div className="min-w-0 flex-1">
          <div className="text-[11px] font-semibold uppercase tracking-wider text-orange-700">
            Deep-Link URL gắn vào Tài liệu Word ({label})
          </div>
          <div className="text-xs font-mono text-slate-700 truncate select-all mt-0.5">
            <AstryxCode>{fullUrl}</AstryxCode>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-2 shrink-0">
        <AstryxButton
          label={copiedPage ? 'Đã Copy Link Trang!' : 'Copy Link gắn Word'}
          variant="primary"
          size="sm"
          icon={copiedPage ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
          onClick={handleCopyPage}
        />

        {cloudinaryUrl && (
          <AstryxButton
            label={copiedImg ? 'Đã Copy URL Ảnh!' : 'Copy URL Ảnh Cloudinary'}
            variant="secondary"
            size="sm"
            icon={
              copiedImg ? (
                <Check className="w-3.5 h-3.5 text-emerald-600" />
              ) : (
                <ExternalLink className="w-3.5 h-3.5 text-slate-500" />
              )
            }
            onClick={handleCopyImg}
          />
        )}
      </div>
    </AstryxCard>
  );
};
