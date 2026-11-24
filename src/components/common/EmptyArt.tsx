import React from 'react';

export type EmptyArtKind = 'search' | 'content' | 'media' | 'error' | 'not-found';

export function inferEmptyArtKind(title?: string): EmptyArtKind {
  const lower = (title ?? '').toLowerCase();
  if (lower.includes('404') || lower.includes('không tìm thấy trang') || lower.includes('page not found')) {
    return 'not-found';
  }
  if (lower.includes('lỗi') || lower.includes('error') || lower.includes('thất bại')) {
    return 'error';
  }
  if (lower.includes('tìm') || lower.includes('search') || lower.includes('không có kết quả') || lower.includes('filter')) {
    return 'search';
  }
  if (lower.includes('figure') || lower.includes('hình') || lower.includes('ảnh') || lower.includes('media')) {
    return 'media';
  }
  return 'content';
}

const ART: Record<EmptyArtKind, React.ReactNode> = {
  search: (
    <>
      <rect x={24} y={14} width={72} height={54} stroke="currentColor" strokeOpacity={0.28} />
      <path d="M34 26h52M34 36h36M34 46h28" stroke="currentColor" strokeOpacity={0.35} />
      <g className="text-orange-600 dark:text-orange-400">
        <circle cx={68} cy={46} r={13} stroke="currentColor" fill="currentColor" fillOpacity={0.08} />
        <path d="M77.5 55.5L88 66" stroke="currentColor" strokeWidth={2} />
        <path d="M64 42l8 8M72 42l-8 8" stroke="currentColor" strokeWidth={1.5} />
      </g>
    </>
  ),
  media: (
    <>
      <rect x={20} y={14} width={80} height={52} stroke="currentColor" strokeOpacity={0.35} />
      <path d="M22 56l20-16 14 11 18-20 24 25" stroke="currentColor" strokeOpacity={0.45} />
      <g className="text-orange-600 dark:text-orange-400">
        <rect x={30} y={22} width={10} height={10} fill="currentColor" fillOpacity={0.14} stroke="currentColor" />
        <path d="M84 18h10v10" stroke="currentColor" />
      </g>
    </>
  ),
  error: (
    <>
      <path d="M24 20h72v44H24z" stroke="currentColor" strokeOpacity={0.32} />
      <path d="M24 30h72" stroke="currentColor" strokeOpacity={0.25} />
      <g className="text-orange-600 dark:text-orange-400">
        <path d="M60 36L46 60h28L60 36z" fill="currentColor" fillOpacity={0.1} stroke="currentColor" />
        <path d="M60 44v7M60 54.5v1.5" stroke="currentColor" strokeWidth={2} />
      </g>
    </>
  ),
  'not-found': (
    <>
      <rect x={22} y={16} width={76} height={50} stroke="currentColor" strokeOpacity={0.3} />
      <path d="M22 26h76" stroke="currentColor" strokeOpacity={0.22} />
      <path d="M28 21h4M36 21h4M44 21h4" stroke="currentColor" strokeOpacity={0.45} />
      <g className="text-orange-600 dark:text-orange-400">
        <rect x={38} y={34} width={44} height={22} fill="currentColor" fillOpacity={0.08} stroke="currentColor" strokeDasharray="3 2" />
        <path d="M51 39v12M51 45h7M58 39v12M69 39l-8 12M61 39l8 12" stroke="currentColor" strokeWidth={1.6} />
      </g>
    </>
  ),
  content: (
    <>
      <rect x={26} y={12} width={68} height={58} stroke="currentColor" strokeOpacity={0.32} />
      <path d="M36 24h48M36 34h40M36 44h32M36 54h24" stroke="currentColor" strokeOpacity={0.4} />
      <g className="text-orange-600 dark:text-orange-400">
        <rect x={68} y={42} width={20} height={20} fill="currentColor" fillOpacity={0.12} stroke="currentColor" />
        <path d="M74 52h8M78 48v8" stroke="currentColor" strokeWidth={1.6} />
      </g>
    </>
  ),
};

export const EmptyArt: React.FC<{
  kind?: EmptyArtKind;
  className?: string;
}> = ({ kind = 'content', className = '' }) => (
  <svg
    viewBox="0 0 120 88"
    fill="none"
    aria-hidden="true"
    focusable="false"
    strokeWidth={1.5}
    strokeLinecap="square"
    className={`h-20 w-auto shrink-0 select-none text-slate-400 dark:text-slate-500 motion-safe:transition-transform motion-safe:duration-300 motion-safe:hover:-translate-y-0.5 ${className}`}
  >
    <rect x={12} y={6} width={96} height={72} fill="currentColor" fillOpacity={0.04} />
    <path
      d="M6 12V4h8M114 12V4h-8M6 72v8h8M114 72v8h-8"
      stroke="currentColor"
      strokeOpacity={0.35}
      strokeWidth={1.25}
    />
    <path d="M8 80h104" stroke="currentColor" strokeDasharray="2 4" strokeOpacity={0.55} />
    <path d="M26 84h68" stroke="currentColor" strokeDasharray="1 5" strokeOpacity={0.28} />
    {ART[kind]}
  </svg>
);
