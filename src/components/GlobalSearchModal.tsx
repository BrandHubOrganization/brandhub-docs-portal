import React, { useState, useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Image, FileText, ArrowRight } from 'lucide-react';
import { PortalData } from '../types/portal';
import { useAppPreferences } from '../context/AppPreferencesContext';
import { AstryxBadge, AstryxButton, AstryxCard, AstryxCode } from './astryx';

interface GlobalSearchModalProps {
  isOpen: boolean;
  onClose: () => void;
  data: PortalData;
}

export const GlobalSearchModal: React.FC<GlobalSearchModalProps> = ({
  isOpen,
  onClose,
  data,
}) => {
  const [query, setQuery] = useState('');
  const navigate = useNavigate();
  const { tx } = useAppPreferences();

  useEffect(() => {
    if (isOpen) setQuery('');
  }, [isOpen]);

  useEffect(() => {
    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) onClose();
    };
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [isOpen, onClose]);

  const results = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) {
      return {
        figures: data.figures.slice(0, 6),
        frs: data.frs.slice(0, 5),
      };
    }
    return {
      figures: data.figures
        .filter((f) =>
          `${f.id} Figure ${f.figNum} ${f.caption} ${f.section} ${f.frCode || ''}`
            .toLowerCase()
            .includes(q)
        )
        .slice(0, 10),
      frs: data.frs
        .filter((fr) =>
          `${fr.code} ${fr.title} ${fr.ucId} ${fr.viSummary}`.toLowerCase().includes(q)
        )
        .slice(0, 8),
    };
  }, [query, data]);

  if (!isOpen) return null;

  const go = (path: string) => {
    navigate(path);
    onClose();
  };

  return (
    <div
      className="fixed inset-0 z-50 bg-slate-900/50 dark:bg-black/70 backdrop-blur-xs flex items-start justify-center pt-14 sm:pt-20 px-3 sm:px-4"
      onClick={onClose}
    >
      <div
        className="w-full max-w-2xl animate-page-in"
        onClick={(e) => e.stopPropagation()}
      >
        <AstryxCard padding={0} className="bg-white dark:bg-slate-900 border border-orange-200 dark:border-slate-800 rounded-xl shadow-xl overflow-hidden">
          <div className="p-3 bg-orange-50/40 dark:bg-slate-900 border-b border-orange-100 dark:border-slate-800 flex items-center gap-2">
            <div className="relative flex-1">
              <Search className="w-4 h-4 text-orange-600 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
              <input
                type="text"
                autoFocus
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder={tx(
                  'Nhập số Figure (VD: Figure 12), mã r3-fig-12, mã FR (3.6.11) hoặc tên chức năng...',
                  'Search Figure (e.g., Figure 12), r3-fig-12, FR code (3.6.11) or function name...'
                )}
                className="w-full text-sm text-slate-900 dark:text-slate-100 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-md pl-9 pr-3 py-1.5 placeholder:text-slate-400 outline-none focus:border-orange-500"
              />
            </div>
            <AstryxButton
              label="Esc"
              variant="secondary"
              size="sm"
              onClick={onClose}
            />
          </div>

          <div className="max-h-[65dvh] overflow-y-auto divide-y divide-slate-100 dark:divide-slate-800 text-xs">
            {results.figures.length > 0 && (
              <div className="p-3 space-y-1">
                <div className="inline-flex items-center gap-1.5 font-semibold text-slate-500 dark:text-slate-400 px-2 pb-1">
                  <Image className="w-3.5 h-3.5 text-orange-600 dark:text-orange-400" />
                  <span>Figures</span>
                </div>
                {results.figures.map((fig) => (
                  <button
                    key={fig.id}
                    onClick={() => go(`/figures/${fig.id}`)}
                    className="interactive-btn w-full text-left px-2.5 py-2 rounded-md hover:bg-orange-50/50 dark:hover:bg-slate-800/80 flex items-center justify-between gap-3 cursor-pointer group"
                  >
                    <div className="truncate flex items-center gap-2">
                      <AstryxCode>{fig.id}</AstryxCode>
                      <span className="font-medium text-slate-900 dark:text-slate-100 truncate">
                        {fig.caption}
                      </span>
                    </div>
                    <div className="inline-flex items-center gap-1.5 font-mono text-slate-400 shrink-0">
                      <AstryxBadge label={fig.reportId.toUpperCase()} variant="orange" />
                      <ArrowRight className="w-3.5 h-3.5 text-slate-300 dark:text-slate-600 group-hover:text-orange-600 transition-transform group-hover:translate-x-0.5" />
                    </div>
                  </button>
                ))}
              </div>
            )}

            {results.frs.length > 0 && (
              <div className="p-3 space-y-1">
                <div className="inline-flex items-center gap-1.5 font-semibold text-slate-500 dark:text-slate-400 px-2 pb-1">
                  <FileText className="w-3.5 h-3.5 text-orange-600 dark:text-orange-400" />
                  <span>Functional Requirements</span>
                </div>
                {results.frs.map((fr) => (
                  <button
                    key={fr.code}
                    onClick={() => go(`/frs/${fr.code}`)}
                    className="interactive-btn w-full text-left px-2.5 py-2 rounded-md hover:bg-orange-50/50 dark:hover:bg-slate-800/80 flex items-center justify-between gap-3 cursor-pointer group"
                  >
                    <div className="truncate flex items-center gap-2">
                      <AstryxBadge label={fr.code} variant="orange" />
                      <span className="text-slate-800 dark:text-slate-100 truncate">{fr.title}</span>
                    </div>
                    <div className="inline-flex items-center gap-1.5 font-mono text-slate-400 shrink-0">
                      <AstryxCode>{fr.ucId}</AstryxCode>
                      <ArrowRight className="w-3.5 h-3.5 text-slate-300 dark:text-slate-600 group-hover:text-orange-600 transition-transform group-hover:translate-x-0.5" />
                    </div>
                  </button>
                ))}
              </div>
            )}
          </div>
        </AstryxCard>
      </div>
    </div>
  );
};
