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
import { AstryxButton, AstryxIconButton, AstryxCode } from './astryx';

interface InteractiveImageViewerProps {
  imageUrl: string;
  caption: string;
  width?: number;
  height?: number;
  category?: string;
  subImages?: SubImageItem[];
  defaultFullscreen?: boolean;
}

export const InteractiveImageViewer: React.FC<InteractiveImageViewerProps> = ({
  imageUrl,
  caption,
  width,
  height,
  subImages,
  defaultFullscreen = true,
}) => {
  const { tx } = useAppPreferences();
  const [activeSubImg, setActiveSubImg] = useState<SubImageItem | null>(null);
  const [scale, setScale] = useState<number>(1);
  const [position, setPosition] = useState<{ x: number; y: number }>({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState<boolean>(false);
  const [dragStart, setDragStart] = useState<{ x: number; y: number }>({ x: 0, y: 0 });
  const [isFullscreen, setIsFullscreen] = useState<boolean>(defaultFullscreen);
  const touchStartRef = useRef<{ x: number; y: number } | null>(null);
  const dialogRef = useRef<HTMLDialogElement>(null);
  const fullscreenButtonRef = useRef<HTMLButtonElement>(null);
  const exitButtonRef = useRef<HTMLButtonElement>(null);

  const currentUrl = activeSubImg ? activeSubImg.imageUrl : imageUrl;
  const currentW = activeSubImg ? activeSubImg.width : width;
  const currentH = activeSubImg ? activeSubImg.height : height;

  // Reset sub-image and open in fullscreen whenever navigating to a new figure page
  useEffect(() => {
    setActiveSubImg(null);
    setScale(1);
    setPosition({ x: 0, y: 0 });
    setIsFullscreen(defaultFullscreen);
  }, [imageUrl, defaultFullscreen]);

  useEffect(() => {
    setScale(1);
    setPosition({ x: 0, y: 0 });
  }, [currentUrl]);

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;
    if (isFullscreen) {
      if (!dialog.open) dialog.showModal();
      exitButtonRef.current?.focus({ preventScroll: true });
    } else if (dialog.open) {
      dialog.close();
      fullscreenButtonRef.current?.focus({ preventScroll: true });
    }
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
          ? 'flex h-full min-w-0 flex-col bg-white dark:bg-slate-950'
          : 'bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg overflow-hidden shadow-xs transition-colors'
      }
    >
      {/* Toolbar */}
      <div className="flex min-w-0 flex-wrap items-center justify-between gap-2 px-3 sm:px-4 py-2 bg-slate-50 dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 text-xs">
        <div className="flex w-full items-center gap-2 text-slate-600 dark:text-slate-300 tabular-nums min-w-0 sm:w-auto">
          <ImageIcon className="w-3.5 h-3.5 text-orange-600 dark:text-orange-400 shrink-0" />
          <span className="font-semibold text-slate-800 dark:text-slate-100 truncate max-w-[260px] sm:max-w-[460px]">
            {caption || tx('Sơ đồ / Hình ảnh', 'Diagram / Figure')}
          </span>
          {currentW && currentH ? (
            <AstryxCode className="hidden sm:inline-flex items-center gap-1 text-slate-400 dark:text-slate-500 font-mono shrink-0">
              <Maximize className="w-3 h-3" />
              <span>
                {currentW}x{currentH}px
              </span>
            </AstryxCode>
          ) : null}
          <span className="hidden xl:inline-flex items-center gap-1 text-[11px] text-slate-400 dark:text-slate-500 ml-1 shrink-0">
            <Hand className="w-3 h-3" />
            <span>
              {tx(
                'Kéo tay để di chuyển, lăn chuột / nhấp đúp để phóng to',
                'Drag to pan, scroll / double-click to zoom'
              )}
            </span>
          </span>
        </div>

        <div className="flex max-w-full flex-wrap items-center gap-1 sm:gap-1.5 tabular-nums">
          <AstryxIconButton
            size="sm"
            variant="secondary"
            onClick={handleZoomOut}
            label={tx('Thu nhỏ', 'Zoom out')}
            tooltip={tx('Thu nhỏ', 'Zoom out')}
            icon={<ZoomOut className="w-3.5 h-3.5" />}
          />
          <output className="px-1.5 font-mono font-medium text-slate-700 dark:text-slate-200 min-w-[44px] text-center">
            {Math.round(scale * 100)}%
          </output>
          <AstryxIconButton
            size="sm"
            variant="secondary"
            onClick={handleZoomIn}
            label={tx('Phóng to', 'Zoom in')}
            tooltip={tx('Phóng to', 'Zoom in')}
            icon={<ZoomIn className="w-3.5 h-3.5" />}
          />
          <AstryxIconButton
            size="sm"
            variant="secondary"
            onClick={handleReset}
            icon={<RotateCcw className="w-3 h-3" />}
            label={tx('Đặt lại thu phóng', 'Reset zoom')}
            tooltip={tx('Đặt lại thu phóng', 'Reset zoom')}
          />

          <a
            href={currentUrl}
            target="_blank"
            rel="noopener noreferrer"
            aria-label={tx('Mở ảnh gốc', 'Open original image')}
            title={tx('Mở ảnh gốc', 'Open original image')}
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
            aria-label={tx('Tải ảnh xuống', 'Download image')}
            title={tx('Tải ảnh xuống', 'Download image')}
            className="interactive-btn inline-flex items-center gap-1 px-2 sm:px-2.5 py-1 rounded border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200"
          >
            <Download className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">{tx('Tải xuống', 'Download')}</span>
          </a>

          {fullscreen ? (
            <AstryxButton
              ref={exitButtonRef}
              size="sm"
              variant="primary"
              onClick={() => setIsFullscreen(false)}
              icon={<Minimize2 className="w-3.5 h-3.5" />}
              label={tx('Thu nhỏ (Esc)', 'Exit (Esc)')}
            />
          ) : (
            <AstryxIconButton
              ref={fullscreenButtonRef}
              size="sm"
              variant="primary"
              aria-haspopup="dialog"
              onClick={() => setIsFullscreen(true)}
              icon={<Maximize2 className="w-3.5 h-3.5" />}
              label={tx('Toàn màn hình', 'Fullscreen')}
              tooltip={tx('Toàn màn hình', 'Fullscreen')}
            />
          )}
        </div>
      </div>

      {/* Sub-images selector if Figure 2 */}
      {subImages && subImages.length > 0 && (
        <div className="flex items-center gap-1.5 px-3 sm:px-4 py-2 bg-slate-50/60 dark:bg-slate-900/60 border-b border-slate-200 dark:border-slate-800 overflow-x-auto text-xs">
          <Layers className="w-3.5 h-3.5 text-orange-600 dark:text-orange-400 shrink-0" />
          <span className="text-slate-600 dark:text-slate-300 font-medium shrink-0 mr-1">
            {tx('Phân hệ:', 'Packages:')}
          </span>
          <button
            onClick={() => setActiveSubImg(null)}
            className={`interactive-btn px-2.5 py-1 rounded shrink-0 cursor-pointer ${
              activeSubImg === null
                ? 'bg-orange-600 text-white font-medium'
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
                  ? 'bg-orange-600 text-white font-medium'
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
          fullscreen ? 'flex-1 min-h-0' : 'min-h-[420px] sm:min-h-[600px] max-h-[82vh]'
        } ${isDragging ? 'cursor-grabbing' : 'cursor-grab'}`}
      >
        <div
          style={{
            transform: `translate(${position.x}px, ${position.y}px) scale(${scale})`,
            transformOrigin: 'center center',
            transition: isDragging ? 'none' : 'transform 140ms cubic-bezier(0.16, 1, 0.3, 1)',
          }}
          className="p-2 sm:p-4 flex items-center justify-center w-full h-full"
        >
          <img
            src={currentUrl}
            alt={caption}
            draggable={false}
            className={
              fullscreen
                ? 'max-w-[96vw] max-h-[85dvh] w-auto h-auto object-contain'
                : 'max-w-full max-h-[76vh] object-contain'
            }
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
      <dialog
        ref={dialogRef}
        aria-label={caption || tx('Sơ đồ / Hình ảnh', 'Diagram / Figure')}
        className="fixed inset-0 m-0 h-dvh w-full max-h-none max-w-none overflow-hidden border-0 p-0"
        onKeyDown={(event) => {
          if (event.key === 'Escape') {
            event.preventDefault();
            setIsFullscreen(false);
          }
        }}
        onCancel={(event) => {
          event.preventDefault();
          setIsFullscreen(false);
        }}
      >
        {isFullscreen && renderBox(true)}
      </dialog>
    </>
  );
};
