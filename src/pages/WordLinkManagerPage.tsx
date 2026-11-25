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
import { ClipboardFeedback, useLinkClipboard } from '../components/ClipboardFeedback';
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
  const { copyLink, isCopied, failedUrl } = useLinkClipboard();
  const { tx } = useAppPreferences();

  const activeBase = baseUrlInput.trim().replace(/\/+$/, '') || getPortalBaseUrl();
  const reportScope = data.reports.find((report) => report.id === selectedReport)?.code
    ?? tx('Tất cả báo cáo', 'All reports');

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

  const reportCounts = useMemo(() => {
    const counts = new Map<string, number>();
    for (const figure of data.figures) {
      counts.set(figure.reportId, (counts.get(figure.reportId) ?? 0) + 1);
    }
    return counts;
  }, [data.figures]);

  const renderCopyButton = (key: string, url: string, label: string) => {
    const copied = isCopied(key);
    return (
      <button
        type="button"
        onClick={() => copyLink(key, url)}
        className="interactive-btn inline-flex shrink-0 items-center gap-1 whitespace-nowrap rounded border border-slate-200 px-2 py-1 text-xs text-slate-700 dark:border-slate-700 dark:text-slate-200 bg-white dark:bg-slate-800 hover:bg-orange-50 dark:hover:bg-slate-700 cursor-pointer"
      >
        {copied ? (
          <Check aria-hidden="true" className="w-3 h-3 text-emerald-600" />
        ) : (
          <Copy aria-hidden="true" className="w-3 h-3 text-orange-600 dark:text-orange-400" />
        )}
        <span>{copied ? tx('Đã copy', 'Copied') : label}</span>
      </button>
    );
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
          <div className="inline-flex min-w-0 items-center gap-2 text-xs text-slate-600 dark:text-slate-300">
            <Globe className="w-4 h-4 text-orange-600 dark:text-orange-400 shrink-0" />
            <span>
              <label htmlFor="portal-base-url" className="font-semibold text-slate-900 dark:text-white">
                {tx('Tên miền gốc (Base URL):', 'Portal Base URL:')}
              </label>{' '}
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
          <div className="flex w-full min-w-0 flex-wrap items-center gap-2 sm:w-72 sm:shrink-0 sm:flex-nowrap">
            <input
              id="portal-base-url"
              type="text"
              value={baseUrlInput}
              onChange={(e) => setBaseUrlInput(e.target.value)}
              className="min-w-0 flex-[1_1_10rem] px-3 py-1.5 text-xs font-mono rounded-md border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 outline-none focus:border-orange-600"
            />
            <AstryxButton
              type="submit"
              label={savedToast ? tx('Đã lưu', 'Saved') : tx('Lưu', 'Save')}
              variant="primary"
              size="sm"
              className="shrink-0"
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
                  label={`${rep.code} (${reportCounts.get(rep.id) ?? 0})`}
                />
              ))}
            </AstryxTabList>
          </div>

          <div className="relative w-full sm:w-72">
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
            <input
              type="text"
              aria-label={tx('Tìm Figure', 'Search figures')}
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
        <p role="status" className="text-xs text-slate-600 dark:text-slate-300">
          {tx(
            `${reportScope} · ${filteredFigures.length} kết quả`,
            `${reportScope} · ${filteredFigures.length} results`
          )}
        </p>
      </div>

      {/* Links Table */}
      <AstryxCard padding={0} className="border border-slate-200 dark:border-slate-800 rounded-xl overflow-hidden bg-white dark:bg-slate-900 shadow-2xs">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse text-xs sm:text-sm">
            <thead>
              <tr className="bg-orange-50/40 dark:bg-slate-800/70 border-b border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 text-xs font-semibold">
                <th scope="col" className="hidden w-28 px-3 py-2.5 sm:table-cell">{tx('Mã Figure', 'Figure ID')}</th>
                <th scope="col" className="py-2.5 px-3">
                  {tx('Caption trong Word', 'Word Caption')}
                </th>
                <th scope="col" className="py-2.5 px-3">
                  <span className="sm:hidden">{tx('Link Word', 'Word Link')}</span>
                  <span className="hidden sm:inline">
                    {tx('Link Trang Web (Gắn vào Word)', 'Portal Deep-Link (For Word)')}
                  </span>
                </th>
                <th scope="col" className="py-2.5 px-3 w-36 text-right hidden sm:table-cell">
                  {tx('Ảnh Cloudinary', 'Cloudinary Image')}
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 dark:divide-slate-800 tabular-nums">
              {filteredFigures.map((fig) => {
                const portalUrl = `${activeBase}/figures/${fig.id}`;
                const portalKey = `portal-${fig.id}`;
                const cloudKey = `cloud-${fig.id}`;
                const manualUrl = failedUrl(portalKey) ?? failedUrl(cloudKey);
                return (
                  <React.Fragment key={fig.id}>
                    <tr
                      className="hover:bg-orange-50/30 dark:hover:bg-slate-800/50 transition-colors"
                    >
                      <td className="hidden py-2.5 px-3 font-mono text-xs whitespace-nowrap sm:table-cell">
                        <AstryxCode>{fig.id}</AstryxCode>
                      </td>
                      <td className="py-2.5 px-3">
                        <div className="mb-1 sm:hidden"><AstryxCode>{fig.id}</AstryxCode></div>
                        <Link
                          to={`/figures/${fig.id}`}
                          className="font-medium [overflow-wrap:anywhere] text-slate-900 dark:text-slate-100 hover:text-orange-600 dark:hover:text-orange-400 hover:underline"
                        >
                          {fig.caption}
                        </Link>
                      </td>
                      <td className="w-px py-2.5 px-3 sm:w-auto">
                        <div className="flex items-center justify-end gap-2 sm:justify-start">
                          <code className="hidden font-mono text-xs text-slate-600 dark:text-slate-400 truncate max-w-[260px] sm:block">
                            {portalUrl}
                          </code>
                          {renderCopyButton(portalKey, portalUrl, 'Copy link')}
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
                          {renderCopyButton(cloudKey, fig.imageUrl, 'Copy URL')}
                        </div>
                      </td>
                    </tr>
                    {manualUrl && (
                      <tr>
                        <td colSpan={4} className="px-3 pb-3">
                          <ClipboardFeedback url={manualUrl} />
                        </td>
                      </tr>
                    )}
                  </React.Fragment>
                );
              })}
            </tbody>
          </table>
        </div>
      </AstryxCard>
    </div>
  );
};
