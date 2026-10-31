import React, { useState } from 'react';
import { Copy, Check, Link2, ExternalLink } from 'lucide-react';

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
    <div className="flex flex-wrap items-center justify-between gap-3 bg-indigo-50/80 border border-indigo-200/80 rounded-xl px-4 py-2.5">
      <div className="flex items-center gap-2.5 min-w-0 flex-1">
        <div className="p-1.5 rounded-lg bg-indigo-600 text-white shrink-0">
          <Link2 className="w-4 h-4" />
        </div>
        <div className="min-w-0 flex-1">
          <div className="text-[11px] font-semibold uppercase tracking-wider text-indigo-700">
            Deep-Link URL gắn vào Tài liệu Word ({label})
          </div>
          <div className="text-xs font-mono text-slate-700 truncate select-all">
            {fullUrl}
          </div>
        </div>
      </div>

      <div className="flex items-center gap-2 shrink-0">
        <button
          onClick={handleCopyPage}
          className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-indigo-600 hover:bg-indigo-700 text-white shadow-xs transition cursor-pointer"
        >
          {copiedPage ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
          {copiedPage ? 'Đã Copy Link Trang!' : 'Copy Link gắn Word'}
        </button>

        {cloudinaryUrl && (
          <button
            onClick={handleCopyImg}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-white hover:bg-slate-50 text-slate-700 border border-slate-300 transition cursor-pointer"
            title="Copy link ảnh gốc độ phân giải cao trên Cloudinary"
          >
            {copiedImg ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <ExternalLink className="w-3.5 h-3.5 text-slate-500" />}
            {copiedImg ? 'Đã Copy URL Ảnh!' : 'Copy URL Ảnh Cloudinary'}
          </button>
        )}
      </div>
    </div>
  );
};
