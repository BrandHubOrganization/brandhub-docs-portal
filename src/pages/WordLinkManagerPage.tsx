import React, { useState, useMemo } from 'react';
import { Link } from 'react-router-dom';
import {
  Download,
  Globe,
  Save,
  Check,
  Copy,
  ExternalLink,
  Search,
  Link2,
} from 'lucide-react';
import type { PortalData } from '../types/portal';
import { getPortalBaseUrl, setPortalBaseUrl } from '../components/CopyLinkBar';
import { useAppPreferences } from '../context/AppPreferencesContext';
import {
  AstryxButton,
  AstryxCard,
  AstryxCode,
  AstryxHeading,
  AstryxTabList,
  AstryxTab,
} from '../components/astryx';

interface WordLinkManagerPageProps {
  data: PortalData;
}

export const WordLinkManagerPage: React.FC<WordLinkManagerPageProps> = ({ data }) => {
  const [baseUrlInput, setBaseUrlInput] = useState<string>(getPortalBaseUrl());
  const [savedToast, setSavedToast] = useState(false);
  const [selectedReport, setSelectedReport] = useState<string>('all');
  const [query, setQuery] = useState<string>('');
  const [copiedKey, setCopiedKey] = useState<string | null>(null);
  const { tx } = useAppPreferences();

  const activeBase = baseUrlInput.trim().replace(/\/+$/, '') || getPortalBaseUrl();

  const handleSaveBaseUrl = (e: React.FormEvent) => {
    e.preventDefault();
    setPortalBaseUrl(activeBase);
    setSavedToast(true);
    setTimeout(() => setSavedToast(false), 1800);
  };

  const filteredFigures = useMemo(() => {
    const q = query.trim().toLowerCase();
    return data.figures.filter((f) => {
      if (selectedReport !== 'all' && f.reportId !== selectedReport) return false;
      if (q) {
        return `${f.id} Figure ${f.figNum} ${f.caption} ${f.section} ${f.frCode || ''}`
          .toLowerCase()
          .includes(q);
      }
      return true;
    });
  }, [data.figures, selectedReport, query]);

  const copyText = (key: string, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedKey(key);
    setTimeout(() => setCopiedKey(null), 1500);
  };

  const handleDownloadCsv = () => {
    const headers = [
      'Figure ID',
      'Report',
      'Section',
      'Figure Number',
      'Caption (Word)',
      'Portal Deep-Link URL',
      'Cloudinary HD Image URL',
    ];
    const rows = filteredFigures.map((f) => [
      f.id,
      f.reportId.toUpperCase(),
      f.section,
      `Figure ${f.figNum}`,
      `"${f.caption.replace(/"/g, '""')}"`,
      `${activeBase}/figures/${f.id}`,
      f.imageUrl,
    ]);
    const csvContent =
      '\uFEFF' + [headers.join(','), ...rows.map((r) => r.join(','))].join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `brandhub-figure-links-${selectedReport}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="max-w-6xl mx-auto px-3 sm:px-4 py-5 sm:py-6 space-y-5 sm:space-y-6">
      <div className="space-y-4 border-b border-slate-200 dark:border-slate-800 pb-5">
        <div className="flex flex-col sm:flex-row sm:items-baseline justify-between gap-3">
          <div>
            <AstryxHeading
              level={1}
              className="inline-flex items-center gap-2 text-lg sm:text-xl font-bold text-slate-900 dark:text-slate-100 text-balance"
            >
              <Link2 className="w-5 h-5 text-orange-600 dark:text-orange-400 shrink-0" />
              <span>
                {tx(
                  `Danh sách Đường Link Gắn vào Tài liệu Word (${filteredFigures.length} Figures)`,
                  `Word Document Deep-Link Manager (${filteredFigures.length} Figures)`
                )}
              </span>
            </AstryxHeading>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 text-pretty">
              {tx(
                'Sao chép từng đường link hoặc xuất file CSV để gắn vào các dòng chữ',
                'Copy individual links or export CSV to attach to'
              )}{' '}
              <AstryxCode>Figure X - ...</AstryxCode>{' '}
              {tx('trong báo cáo Word.', 'captions in Word reports.')}
            </p>
          </div>

          <AstryxButton
            label={tx(
              `Xuất file CSV (${filteredFigures.length} links)`,
              `Export CSV (${filteredFigures.length} links)`
            )}
            variant="primary"
            size="sm"
            icon={<Download className="w-3.5 h-3.5" />}
            onClick={handleDownloadCsv}
          />
        </div>

        {/* Base URL Config */}
        <form
          onSubmit={handleSaveBaseUrl}
          className="p-3.5 rounded-xl bg-white dark:bg-slate-900 border border-orange-200 dark:border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3"
        >
          <div className="inline-flex items-center gap-2 text-xs text-slate-600 dark:text-slate-300">
            <Globe className="w-4 h-4 text-orange-600 dark:text-orange-400 shrink-0" />
            <span>
              <strong className="text-slate-900 dark:text-white">
                {tx('Tên miền gốc (Base URL):', 'Portal Base URL:')}
              </strong>{' '}
              {tx(
                'Nhập domain sau khi deploy (VD:',
                'Enter your deployed domain (e.g.,'
              )}{' '}
              <AstryxCode>https://brandhub-docs.vercel.app</AstryxCode>
              {tx(
                ') để cập nhật toàn bộ đường link bên dưới.',
                ') to update all generated deep-links below.'
              )}
            </span>
          </div>
          <div className="flex items-center gap-2 shrink-0">
            <input
              type="text"
              value={baseUrlInput}
              onChange={(e) => setBaseUrlInput(e.target.value)}
              className="w-full sm:w-72 px-3 py-1.5 text-xs font-mono rounded-md border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 outline-none focus:border-orange-600"
            />
            <AstryxButton
              type="submit"
              label={savedToast ? tx('Đã lưu', 'Saved') : tx('Lưu', 'Save')}
              variant="primary"
              size="sm"
              icon={savedToast ? <Check className="w-3.5 h-3.5" /> : <Save className="w-3.5 h-3.5" />}
            />
          </div>
        </form>

        {/* Filter Bar */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2.5">
          <div className="overflow-x-auto">
            <AstryxTabList
              value={selectedReport}
              onChange={setSelectedReport}
              size="sm"
              hasDivider
            >
              <AstryxTab
                value="all"
                label={`${tx('Tất cả', 'All')} (${data.figures.length})`}
              />
              {data.reports.map((rep) => (
                <AstryxTab
                  key={rep.id}
                  value={rep.id}
                  label={`${rep.code} (${rep.figureCount})`}
                />
              ))}
            </AstryxTabList>
          </div>

          <div className="relative w-full sm:w-72">
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder={tx(
                'Tìm Figure 10, r3-fig-10, 3.2.1...',
                'Search Figure 10, r3-fig-10, 3.2.1...'
              )}
              className="w-full pl-8 pr-3 py-1.5 text-xs sm:text-sm rounded-md border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 focus:border-orange-600 outline-none"
            />
          </div>
        </div>
      </div>

      {/* Links Table */}
      <AstryxCard padding={0} className="border border-slate-200 dark:border-slate-800 rounded-xl overflow-hidden bg-white dark:bg-slate-900 shadow-2xs">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse text-xs sm:text-sm">
            <thead>
              <tr className="bg-orange-50/40 dark:bg-slate-800/70 border-b border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 text-xs font-semibold">
                <th className="py-2.5 px-3 w-28">{tx('Mã Figure', 'Figure ID')}</th>
                <th className="py-2.5 px-3">
                  {tx('Caption trong Word', 'Word Caption')}
                </th>
                <th className="py-2.5 px-3">
                  {tx('Link Trang Web (Gắn vào Word)', 'Portal Deep-Link (For Word)')}
                </th>
                <th className="py-2.5 px-3 w-36 text-right hidden sm:table-cell">
                  {tx('Ảnh Cloudinary', 'Cloudinary Image')}
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 dark:divide-slate-800 tabular-nums">
              {filteredFigures.map((fig) => {
                const portalUrl = `${activeBase}/figures/${fig.id}`;
                return (
                  <tr
                    key={fig.id}
                    className="hover:bg-orange-50/30 dark:hover:bg-slate-800/50 transition-colors"
                  >
                    <td className="py-2.5 px-3 font-mono text-xs whitespace-nowrap">
                      <AstryxCode>{fig.id}</AstryxCode>
                    </td>
                    <td className="py-2.5 px-3">
                      <Link
                        to={`/figures/${fig.id}`}
                        className="font-medium text-slate-900 dark:text-slate-100 hover:text-orange-600 dark:hover:text-orange-400 hover:underline"
                      >
                        {fig.caption}
                      </Link>
                    </td>
                    <td className="py-2.5 px-3">
                      <div className="flex items-center gap-2">
                        <code className="font-mono text-xs text-slate-600 dark:text-slate-400 truncate max-w-[160px] sm:max-w-[260px]">
                          {portalUrl}
                        </code>
                        <button
                          onClick={() => copyText(`portal-${fig.id}`, portalUrl)}
                          className="interactive-btn inline-flex items-center gap-1 px-2 py-1 rounded border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 hover:bg-orange-50 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 text-xs shrink-0 cursor-pointer"
                        >
                          {copiedKey === `portal-${fig.id}` ? (
                            <>
                              <Check className="w-3 h-3 text-emerald-600" />
                              <span>{tx('Đã copy', 'Copied')}</span>
                            </>
                          ) : (
                            <>
                              <Copy className="w-3 h-3 text-orange-600 dark:text-orange-400" />
                              <span>{tx('Copy link', 'Copy')}</span>
                            </>
                          )}
                        </button>
                      </div>
                    </td>
                    <td className="py-2.5 px-3 text-right whitespace-nowrap hidden sm:table-cell">
                      <div className="inline-flex items-center gap-1.5 text-xs">
                        <a
                          href={fig.imageUrl}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="interactive-btn inline-flex items-center gap-1 px-2 py-1 rounded border border-slate-200 dark:border-slate-700 hover:bg-orange-50 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200"
                        >
                          <ExternalLink className="w-3 h-3 text-slate-500 dark:text-slate-400" />
                          <span>{tx('Mở ảnh', 'Open')}</span>
                        </a>
                        <button
                          onClick={() => copyText(`cloud-${fig.id}`, fig.imageUrl)}
                          className="interactive-btn inline-flex items-center gap-1 px-2 py-1 rounded border border-slate-200 dark:border-slate-700 hover:bg-orange-50 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200 cursor-pointer"
                        >
                          {copiedKey === `cloud-${fig.id}` ? (
                            <>
                              <Check className="w-3 h-3 text-emerald-600" />
                              <span>{tx('Đã copy', 'Copied')}</span>
                            </>
                          ) : (
                            <>
                              <Copy className="w-3 h-3 text-orange-600 dark:text-orange-400" />
                              <span>Copy URL</span>
                            </>
                          )}
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </AstryxCard>
    </div>
  );
};
