import React, { useState, useEffect, useRef } from 'react';
import {
  Image as ImageIcon,
  ZoomIn,
  ZoomOut,
  RotateCcw,
  ExternalLink,
  Download,
  Maximize2,
  Minimize2,
  Layers,
  Hand,
  Maximize,
} from 'lucide-react';
import { SubImageItem } from '../types/portal';
import { useAppPreferences } from '../context/AppPreferencesContext';

interface InteractiveImageViewerProps {
  imageUrl: string;
  caption: string;
  width?: number;
  height?: number;
  category?: string;
  subImages?: SubImageItem[];
}

export const InteractiveImageViewer: React.FC<InteractiveImageViewerProps> = ({
  imageUrl,
  caption,
  width,
  height,
  subImages,
}) => {
  const { tx } = useAppPreferences();
  const [activeSubImg, setActiveSubImg] = useState<SubImageItem | null>(null);
  const [scale, setScale] = useState<number>(1);
  const [position, setPosition] = useState<{ x: number; y: number }>({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState<boolean>(false);
  const [dragStart, setDragStart] = useState<{ x: number; y: number }>({ x: 0, y: 0 });
  const [isFullscreen, setIsFullscreen] = useState<boolean>(false);
  const touchStartRef = useRef<{ x: number; y: number } | null>(null);

  const currentUrl = activeSubImg ? activeSubImg.imageUrl : imageUrl;
  const currentW = activeSubImg ? activeSubImg.width : width;
  const currentH = activeSubImg ? activeSubImg.height : height;

  useEffect(() => {
    setScale(1);
    setPosition({ x: 0, y: 0 });
  }, [currentUrl]);

  useEffect(() => {
    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isFullscreen) {
        setIsFullscreen(false);
      }
    };
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [isFullscreen]);

  const handleZoomIn = () => setScale((s) => Math.min(s + 0.25, 4));
  const handleZoomOut = () => setScale((s) => Math.max(s - 0.25, 0.5));
  const handleReset = () => {
    setScale(1);
    setPosition({ x: 0, y: 0 });
  };

  const handleDoubleClick = () => {
    if (scale > 1) {
      handleReset();
    } else {
      setScale(2);
    }
  };

  const handleWheel = (e: React.WheelEvent) => {
    if (e.ctrlKey || e.metaKey || isFullscreen) {
      e.preventDefault();
      const delta = e.deltaY < 0 ? 0.15 : -0.15;
      setScale((s) => Math.min(Math.max(s + delta, 0.5), 4));
    }
  };

  const handleMouseDown = (e: React.MouseEvent) => {
    if (e.button !== 0) return;
    setIsDragging(true);
    setDragStart({ x: e.clientX - position.x, y: e.clientY - position.y });
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!isDragging) return;
    setPosition({
      x: e.clientX - dragStart.x,
      y: e.clientY - dragStart.y,
    });
  };

  const handleMouseUp = () => setIsDragging(false);

  // Touch gestures for mobile & tablet
  const handleTouchStart = (e: React.TouchEvent) => {
    if (e.touches.length === 1) {
      const t = e.touches[0];
      touchStartRef.current = {
        x: t.clientX - position.x,
        y: t.clientY - position.y,
      };
      setIsDragging(true);
    }
  };

  const handleTouchMove = (e: React.TouchEvent) => {
    if (e.touches.length === 1 && touchStartRef.current) {
      const t = e.touches[0];
      setPosition({
        x: t.clientX - touchStartRef.current.x,
        y: t.clientY - touchStartRef.current.y,
      });
    }
  };

  const handleTouchEnd = () => {
    touchStartRef.current = null;
    setIsDragging(false);
  };

  const renderBox = (fullscreen: boolean) => (
    <div
      className={
        fullscreen
          ? 'fixed inset-0 z-50 bg-white dark:bg-slate-950 flex flex-col'
          : 'bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg overflow-hidden shadow-xs transition-colors'
      }
    >
      {/* Toolbar */}
      <div className="flex flex-wrap items-center justify-between gap-2 px-3 sm:px-4 py-2 bg-slate-50 dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 text-xs">
        <div className="flex items-center gap-2 text-slate-600 dark:text-slate-300 tabular-nums">
          <ImageIcon className="w-3.5 h-3.5 text-sky-600 dark:text-sky-400 shrink-0" />
          <span className="font-semibold text-slate-800 dark:text-slate-100">
            {tx('Sơ đồ / Hình ảnh', 'Diagram / Figure')}
          </span>
          {currentW && currentH ? (
            <span className="hidden sm:inline-flex items-center gap-1 text-slate-400 dark:text-slate-500 font-mono">
              <Maximize className="w-3 h-3" />
              <span>
                {currentW}x{currentH}px
              </span>
            </span>
          ) : null}
          <span className="hidden lg:inline-flex items-center gap-1 text-[11px] text-slate-400 dark:text-slate-500 ml-1">
            <Hand className="w-3 h-3" />
            <span>
              {tx(
                'Kéo tay để di chuyển, nhấp đúp để phóng to',
                'Drag to pan, double-click to zoom'
              )}
            </span>
          </span>
        </div>

        <div className="flex flex-wrap items-center gap-1 sm:gap-1.5 tabular-nums">
          <button
            onClick={handleZoomOut}
            aria-label={tx('Thu nhỏ', 'Zoom out')}
            className="interactive-btn inline-flex items-center justify-center p-1.5 rounded border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 cursor-pointer"
          >
            <ZoomOut className="w-3.5 h-3.5" />
          </button>
          <span className="px-1.5 font-mono font-medium text-slate-700 dark:text-slate-200 min-w-[44px] text-center">
            {Math.round(scale * 100)}%
          </span>
          <button
            onClick={handleZoomIn}
            aria-label={tx('Phóng to', 'Zoom in')}
            className="interactive-btn inline-flex items-center justify-center p-1.5 rounded border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 cursor-pointer"
          >
            <ZoomIn className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={handleReset}
            className="interactive-btn inline-flex items-center gap-1 px-2 py-1 rounded border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 cursor-pointer"
          >
            <RotateCcw className="w-3 h-3" />
            <span>100%</span>
          </button>

          <a
            href={currentUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="interactive-btn inline-flex items-center gap-1 px-2 sm:px-2.5 py-1 rounded border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200"
          >
            <ExternalLink className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">{tx('Ảnh gốc', 'Original')}</span>
          </a>

          <a
            href={currentUrl.replace('/upload/', '/upload/fl_attachment/')}
            download
            target="_blank"
            rel="noopener noreferrer"
            className="interactive-btn inline-flex items-center gap-1 px-2 sm:px-2.5 py-1 rounded border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200"
          >
            <Download className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">{tx('Tải xuống', 'Download')}</span>
          </a>

          <button
            onClick={() => setIsFullscreen(!fullscreen)}
            className="interactive-btn inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-sky-600 hover:bg-sky-700 text-white font-medium cursor-pointer"
          >
            {fullscreen ? (
              <>
                <Minimize2 className="w-3.5 h-3.5" />
                <span>{tx('Đóng (Esc)', 'Close (Esc)')}</span>
              </>
            ) : (
              <>
                <Maximize2 className="w-3.5 h-3.5" />
                <span className="hidden sm:inline">
                  {tx('Toàn màn hình', 'Fullscreen')}
                </span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Sub-images selector if Figure 2 */}
      {subImages && subImages.length > 0 && (
        <div className="flex items-center gap-1.5 px-3 sm:px-4 py-2 bg-slate-50/60 dark:bg-slate-900/60 border-b border-slate-200 dark:border-slate-800 overflow-x-auto text-xs">
          <Layers className="w-3.5 h-3.5 text-sky-600 dark:text-sky-400 shrink-0" />
          <span className="text-slate-600 dark:text-slate-300 font-medium shrink-0 mr-1">
            {tx('Phân hệ:', 'Packages:')}
          </span>
          <button
            onClick={() => setActiveSubImg(null)}
            className={`interactive-btn px-2.5 py-1 rounded shrink-0 cursor-pointer ${
              activeSubImg === null
                ? 'bg-sky-600 text-white font-medium'
                : 'bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-700'
            }`}
          >
            {tx('Tổng hợp (9 Phân hệ)', 'Overview (9 Packages)')}
          </button>
          {subImages.map((sub, idx) => (
            <button
              key={sub.id}
              onClick={() => setActiveSubImg(sub)}
              className={`interactive-btn px-2.5 py-1 rounded shrink-0 cursor-pointer tabular-nums ${
                activeSubImg?.id === sub.id
                  ? 'bg-sky-600 text-white font-medium'
                  : 'bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-700'
              }`}
            >
              {idx + 1}. {sub.label}
            </button>
          ))}
        </div>
      )}

      {/* Image Canvas (kept crisp white for high-contrast UML diagram legibility) */}
      <div
        onWheel={handleWheel}
        onDoubleClick={handleDoubleClick}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        onTouchStart={handleTouchStart}
        onTouchMove={handleTouchMove}
        onTouchEnd={handleTouchEnd}
        className={`relative overflow-hidden select-none flex items-center justify-center bg-white ${
          fullscreen ? 'flex-1 min-h-0' : 'min-h-[280px] sm:min-h-[420px] max-h-[720px]'
        } ${isDragging ? 'cursor-grabbing' : 'cursor-grab'}`}
      >
        <div
          style={{
            transform: `translate(${position.x}px, ${position.y}px) scale(${scale})`,
            transformOrigin: 'center center',
            transition: isDragging ? 'none' : 'transform 140ms cubic-bezier(0.16, 1, 0.3, 1)',
          }}
          className="p-2 sm:p-4 flex items-center justify-center"
        >
          <img
            src={currentUrl}
            alt={caption}
            draggable={false}
            className="max-w-full max-h-[650px] object-contain"
            style={fullscreen ? { maxHeight: '85dvh' } : undefined}
          />
        </div>
      </div>

      {/* Caption */}
      <div className="py-2.5 px-4 text-center bg-slate-50 dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800">
        <p className="italic text-slate-700 dark:text-slate-300 text-xs sm:text-sm">
          {activeSubImg ? `${caption} (${activeSubImg.label})` : caption}
        </p>
      </div>
    </div>
  );

  return (
    <>
      {renderBox(false)}
      {isFullscreen && renderBox(true)}
    </>
  );
};
