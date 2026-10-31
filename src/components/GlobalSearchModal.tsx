import React, { useState, useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, X, Image, FileText, ArrowRight } from 'lucide-react';
import { PortalData } from '../types/portal';
import { useAppPreferences } from '../context/AppPreferencesContext';

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
        className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg shadow-xl w-full max-w-2xl overflow-hidden animate-page-in"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="p-3 bg-slate-50 dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 flex items-center gap-2">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
            <input
              type="text"
              autoFocus
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder={tx(
                'Nhập số Figure (VD: Figure 12), mã r3-fig-12, mã FR (3.6.11) hoặc tên chức năng...',
                'Search Figure (e.g., Figure 12), r3-fig-12, FR code (3.6.11) or function name...'
              )}
              className="w-full text-sm text-slate-900 dark:text-slate-100 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-md pl-9 pr-3 py-1.5 placeholder:text-slate-400 outline-none focus:border-sky-600"
            />
          </div>
          <button
            onClick={onClose}
            className="interactive-btn inline-flex items-center gap-1 px-2.5 py-1.5 text-xs font-mono text-slate-600 dark:text-slate-300 bg-white dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700 border border-slate-200 dark:border-slate-700 rounded-md cursor-pointer"
          >
            <X className="w-3.5 h-3.5" />
            <span>Esc</span>
          </button>
        </div>

        <div className="max-h-[65dvh] overflow-y-auto divide-y divide-slate-100 dark:divide-slate-800 text-xs">
          {results.figures.length > 0 && (
            <div className="p-3 space-y-1">
              <div className="inline-flex items-center gap-1.5 font-semibold text-slate-500 dark:text-slate-400 px-2 pb-1">
                <Image className="w-3.5 h-3.5 text-sky-600 dark:text-sky-400" />
                <span>Figures</span>
              </div>
              {results.figures.map((fig) => (
                <button
                  key={fig.id}
                  onClick={() => go(`/figures/${fig.id}`)}
                  className="interactive-btn w-full text-left px-2.5 py-2 rounded-md hover:bg-slate-50 dark:hover:bg-slate-800/80 flex items-center justify-between gap-3 cursor-pointer group"
                >
                  <div className="truncate">
                    <span className="font-mono font-medium text-sky-700 dark:text-sky-400 mr-2">
                      [{fig.id}]
                    </span>
                    <span className="font-medium text-slate-900 dark:text-slate-100">
                      {fig.caption}
                    </span>
                  </div>
                  <div className="inline-flex items-center gap-1.5 font-mono text-slate-400 shrink-0">
                    <span>{fig.reportId.toUpperCase()}</span>
                    <ArrowRight className="w-3.5 h-3.5 text-slate-300 dark:text-slate-600 group-hover:text-sky-600 dark:group-hover:text-sky-400 transition-transform group-hover:translate-x-0.5" />
                  </div>
                </button>
              ))}
            </div>
          )}

          {results.frs.length > 0 && (
            <div className="p-3 space-y-1">
              <div className="inline-flex items-center gap-1.5 font-semibold text-slate-500 dark:text-slate-400 px-2 pb-1">
                <FileText className="w-3.5 h-3.5 text-sky-600 dark:text-sky-400" />
                <span>Functional Requirements</span>
              </div>
              {results.frs.map((fr) => (
                <button
                  key={fr.code}
                  onClick={() => go(`/frs/${fr.code}`)}
                  className="interactive-btn w-full text-left px-2.5 py-2 rounded-md hover:bg-slate-50 dark:hover:bg-slate-800/80 flex items-center justify-between gap-3 cursor-pointer group"
                >
                  <div className="truncate">
                    <span className="font-mono font-semibold text-sky-700 dark:text-sky-400 mr-2">
                      {fr.code}
                    </span>
                    <span className="text-slate-800 dark:text-slate-100">{fr.title}</span>
                  </div>
                  <div className="inline-flex items-center gap-1.5 font-mono text-slate-400 shrink-0">
                    <span>{fr.ucId}</span>
                    <ArrowRight className="w-3.5 h-3.5 text-slate-300 dark:text-slate-600 group-hover:text-sky-600 dark:group-hover:text-sky-400 transition-transform group-hover:translate-x-0.5" />
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
