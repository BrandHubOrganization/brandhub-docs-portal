import React, { useState, useMemo, useEffect } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import {
  BookOpen,
  MessageSquare,
  Search,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  Info,
} from 'lucide-react';
import type { PortalData } from '../types/portal';
import { useAppPreferences } from '../context/AppPreferencesContext';

interface RulesAndMessagesPageProps {
  data: PortalData;
}

export const RulesAndMessagesPage: React.FC<RulesAndMessagesPageProps> = ({ data }) => {
  const [searchParams] = useSearchParams();
  const initialCode = searchParams.get('code') || '';
  const { tx } = useAppPreferences();

  const [activeTab, setActiveTab] = useState<'br' | 'msg'>(
    initialCode.startsWith('MSG') ? 'msg' : 'br'
  );
  const [query, setQuery] = useState(initialCode);

  useEffect(() => {
    const code = searchParams.get('code');
    if (code) {
      setQuery(code);
      if (code.startsWith('MSG')) setActiveTab('msg');
      else if (code.startsWith('BR')) setActiveTab('br');
    }
  }, [searchParams]);

  const brToFRs = useMemo(() => {
    const map: Record<string, { code: string; name: string }[]> = {};
    for (const fr of data.frs) {
      for (const br of fr.linkedBrCodes) {
        if (!map[br]) map[br] = [];
        map[br].push({ code: fr.code, name: fr.title });
      }
    }
    return map;
  }, [data.frs]);

  const msgToFRs = useMemo(() => {
    const map: Record<string, { code: string; name: string }[]> = {};
    for (const fr of data.frs) {
      for (const msg of fr.linkedMsgCodes) {
        if (!map[msg]) map[msg] = [];
        map[msg].push({ code: fr.code, name: fr.title });
      }
    }
    return map;
  }, [data.frs]);

  const filteredBRs = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return data.businessRules;
    return data.businessRules.filter((b) =>
      `${b.code} ${b.definition}`.toLowerCase().includes(q)
    );
  }, [data.businessRules, query]);

  const filteredMSGs = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return data.messages;
    return data.messages.filter((m) =>
      `${m.code} ${m.type} ${m.context} ${m.content}`.toLowerCase().includes(q)
    );
  }, [data.messages, query]);

  const renderMsgTypeBadge = (type: string) => {
    const lower = type.toLowerCase();
    if (lower.includes('success')) {
      return (
        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded border border-emerald-200 dark:border-emerald-800/70 bg-emerald-50 dark:bg-emerald-950/50 text-emerald-700 dark:text-emerald-300 font-mono text-[11px]">
          <CheckCircle2 className="w-3 h-3 shrink-0" />
          <span>{type}</span>
        </span>
      );
    }
    if (lower.includes('error')) {
      return (
        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded border border-rose-200 dark:border-rose-800/70 bg-rose-50 dark:bg-rose-950/50 text-rose-700 dark:text-rose-300 font-mono text-[11px]">
          <XCircle className="w-3 h-3 shrink-0" />
          <span>{type}</span>
        </span>
      );
    }
    if (lower.includes('warning')) {
      return (
        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded border border-amber-200 dark:border-amber-800/70 bg-amber-50 dark:bg-amber-950/50 text-amber-700 dark:text-amber-300 font-mono text-[11px]">
          <AlertTriangle className="w-3 h-3 shrink-0" />
          <span>{type}</span>
        </span>
      );
    }
    return (
      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded border border-sky-200 dark:border-sky-800/70 bg-sky-50 dark:bg-sky-950/50 text-sky-700 dark:text-sky-300 font-mono text-[11px]">
        <Info className="w-3 h-3 shrink-0" />
        <span>{type}</span>
      </span>
    );
  };

  return (
    <div className="max-w-6xl mx-auto px-3 sm:px-4 py-5 sm:py-6 space-y-5 sm:space-y-6">
      <div className="space-y-4 border-b border-slate-200 dark:border-slate-800 pb-5">
        <div>
          <h1 className="inline-flex items-center gap-2 text-lg sm:text-xl font-bold text-slate-900 dark:text-slate-100 text-balance">
            <BookOpen className="w-5 h-5 text-sky-600 dark:text-sky-400 shrink-0" />
            <span>
              65 Business Rules (BR-01 – BR-65) &amp; 60 System Messages (MSG01 – MSG60)
            </span>
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 text-pretty">
            {tx('Dữ liệu nằm tại', 'Data stored in')}{' '}
            <code className="font-mono text-slate-700 dark:text-slate-300">
              src/data/rulesAndMessages.json
            </code>
            .
          </p>
        </div>

        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center gap-1.5 text-xs tabular-nums">
            <button
              onClick={() => setActiveTab('br')}
              className={`interactive-btn inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md border cursor-pointer ${
                activeTab === 'br'
                  ? 'bg-sky-600 text-white border-sky-600 font-medium shadow-xs'
                  : 'bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800'
              }`}
            >
              <BookOpen className="w-3.5 h-3.5" />
              <span>Business Rules ({filteredBRs.length})</span>
            </button>
            <button
              onClick={() => setActiveTab('msg')}
              className={`interactive-btn inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md border cursor-pointer ${
                activeTab === 'msg'
                  ? 'bg-sky-600 text-white border-sky-600 font-medium shadow-xs'
                  : 'bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800'
              }`}
            >
              <MessageSquare className="w-3.5 h-3.5" />
              <span>System Messages ({filteredMSGs.length})</span>
            </button>
          </div>

          <div className="relative w-full sm:w-80">
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder={tx(
                'Tìm BR-01, MSG05, từ khóa...',
                'Search BR-01, MSG05, keyword...'
              )}
              className="w-full pl-8 pr-3 py-1.5 text-xs sm:text-sm rounded-md border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 focus:border-sky-600 outline-none"
            />
          </div>
        </div>
      </div>

      {activeTab === 'br' ? (
        <div className="border border-slate-200 dark:border-slate-800 rounded-lg overflow-hidden bg-white dark:bg-slate-900 shadow-2xs">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs sm:text-sm">
              <thead>
                <tr className="bg-slate-50 dark:bg-slate-800/70 border-b border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 text-xs font-semibold">
                  <th className="py-2.5 px-3 w-24">{tx('Mã BR', 'BR Code')}</th>
                  <th className="py-2.5 px-3">
                    {tx('Nội dung Quy tắc Nghiệp vụ', 'Business Rule Definition')}
                  </th>
                  <th className="py-2.5 px-3 w-64">
                    {tx('Áp dụng tại các FR', 'Referenced in FRs')}
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200 dark:divide-slate-800 tabular-nums">
                {filteredBRs.map((br) => {
                  const refs = brToFRs[br.code] || [];
                  return (
                    <tr
                      key={br.code}
                      className="hover:bg-slate-50/80 dark:hover:bg-slate-800/50 transition-colors"
                    >
                      <td className="py-3 px-3 font-mono font-semibold text-sky-700 dark:text-sky-400 align-top">
                        {br.code}
                      </td>
                      <td className="py-3 px-3 text-slate-700 dark:text-slate-300 leading-relaxed text-pretty align-top">
                        {br.definition}
                      </td>
                      <td className="py-3 px-3 align-top">
                        <div className="flex flex-wrap gap-1">
                          {refs.map((r) => (
                            <Link
                              key={r.code}
                              to={`/frs/${r.code}`}
                              title={r.name}
                              className="interactive-btn px-1.5 py-0.5 rounded border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 hover:bg-sky-50 dark:hover:bg-sky-950 hover:border-sky-200 dark:hover:border-sky-800 font-mono text-[11px] text-slate-700 dark:text-slate-300 hover:text-sky-700 dark:hover:text-sky-400"
                            >
                              {r.code}
                            </Link>
                          ))}
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        <div className="border border-slate-200 dark:border-slate-800 rounded-lg overflow-hidden bg-white dark:bg-slate-900 shadow-2xs">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs sm:text-sm">
              <thead>
                <tr className="bg-slate-50 dark:bg-slate-800/70 border-b border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 text-xs font-semibold">
                  <th className="py-2.5 px-3 w-20">{tx('Mã MSG', 'MSG Code')}</th>
                  <th className="py-2.5 px-3 w-32">{tx('Loại', 'Type')}</th>
                  <th className="py-2.5 px-3">
                    {tx('Nội dung Thông báo & Ngữ cảnh', 'Message Content & Context')}
                  </th>
                  <th className="py-2.5 px-3 w-56">
                    {tx('Áp dụng tại các FR', 'Referenced in FRs')}
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200 dark:divide-slate-800 tabular-nums">
                {filteredMSGs.map((msg) => {
                  const refs = msgToFRs[msg.code] || [];
                  return (
                    <tr
                      key={msg.code}
                      className="hover:bg-slate-50/80 dark:hover:bg-slate-800/50 transition-colors"
                    >
                      <td className="py-3 px-3 font-mono font-semibold text-sky-700 dark:text-sky-400 align-top">
                        {msg.code}
                      </td>
                      <td className="py-3 px-3 align-top">
                        {renderMsgTypeBadge(msg.type)}
                      </td>
                      <td className="py-3 px-3 align-top space-y-1">
                        <div className="font-medium text-slate-900 dark:text-slate-100 text-pretty">
                          &ldquo;{msg.content}&rdquo;
                        </div>
                        <div className="text-xs text-slate-500 dark:text-slate-400 text-pretty">
                          {tx('Ngữ cảnh:', 'Context:')} {msg.context}
                        </div>
                      </td>
                      <td className="py-3 px-3 align-top">
                        <div className="flex flex-wrap gap-1">
                          {refs.map((r) => (
                            <Link
                              key={r.code}
                              to={`/frs/${r.code}`}
                              title={r.name}
                              className="interactive-btn px-1.5 py-0.5 rounded border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 hover:bg-sky-50 dark:hover:bg-sky-950 hover:border-sky-200 dark:hover:border-sky-800 font-mono text-[11px] text-slate-700 dark:text-slate-300 hover:text-sky-700 dark:hover:text-sky-400"
                            >
                              {r.code}
                            </Link>
                          ))}
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};
