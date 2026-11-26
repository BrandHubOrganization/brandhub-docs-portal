import React, { useState, useMemo, useEffect } from 'react';
import { Link, useParams, useSearchParams } from 'react-router-dom';
import {
  Search,
  RotateCcw,
  Table2,
  LayoutGrid,
  Copy,
  Check,
  ArrowUpRight,
  ChevronDown,
  FolderKanban,
  Users,
  Image as ImageIcon,
} from 'lucide-react';
import type { PortalData, CanonicalRole } from '../types/portal';
import { RoleBadge, CANONICAL_ROLES } from '../components/RoleBadge';
import { getPortalBaseUrl } from '../components/CopyLinkBar';
import { ClipboardFeedback, useLinkClipboard } from '../components/ClipboardFeedback';
import { useAppPreferences } from '../context/AppPreferencesContext';
import {
  AstryxBadge,
  AstryxButton,
  AstryxCard,
  AstryxCode,
  AstryxHeading,
  AstryxSegmentedControl,
  AstryxSegmentedControlItem,
  AstryxTabList,
  AstryxTab,
  BhEmptyState,
} from '../components/astryx';

interface FiguresCatalogPageProps {
  data: PortalData;
}

export const FiguresCatalogPage: React.FC<FiguresCatalogPageProps> = ({ data }) => {
  const { reportId: routeReportId } = useParams<{ reportId?: string }>();
  const [searchParams, setSearchParams] = useSearchParams();
  const { tx } = useAppPreferences();

  const [selectedReport, setSelectedReport] = useState<string>(
    routeReportId || searchParams.get('report') || 'all'
  );
  const [selectedDomain, setSelectedDomain] = useState<string>(
    searchParams.get('domain') || 'all'
  );
  const [selectedRole, setSelectedRole] = useState<string>(
    searchParams.get('role') || 'all'
  );
  const [query, setQuery] = useState<string>(searchParams.get('q') || '');
  const [viewMode, setViewMode] = useState<'table' | 'grid'>('table');
  const { copyLink, isCopied, failedUrl } = useLinkClipboard();
  const [visibleCount, setVisibleCount] = useState<number>(60);

  useEffect(() => {
    if (routeReportId) {
      setSelectedReport(routeReportId);
    }
  }, [routeReportId]);

  useEffect(() => {
    setVisibleCount(60);
  }, [selectedReport, selectedDomain, selectedRole, query]);

  const filteredFigures = useMemo(() => {
    const q = query.trim().toLowerCase();
    return data.figures.filter((f) => {
      if (selectedReport !== 'all' && f.reportId !== selectedReport) return false;
      if (selectedDomain !== 'all' && f.domainCode !== selectedDomain) return false;
      if (
        selectedRole !== 'all' &&
        (!f.actors || !f.actors.includes(selectedRole as CanonicalRole))
      ) {
        return false;
      }
      if (q) {
        const hay = `${f.id} Figure ${f.figNum} ${f.caption} ${f.title} ${f.section} ${
          f.frCode || ''
        } ${f.ucId || ''} ${f.viSummary || ''} ${f.summary || ''}`.toLowerCase();
        return hay.includes(q);
      }
      return true;
    });
  }, [data.figures, selectedReport, selectedDomain, selectedRole, query]);

  const handleCopyDeepLink = (figId: string) =>
    copyLink(figId, `${getPortalBaseUrl()}/figures/${figId}`);

  const resetFilters = () => {
    setSelectedReport(routeReportId || 'all');
    setSelectedDomain('all');
    setSelectedRole('all');
    setQuery('');
    setSearchParams({});
  };

  return (
    <div className="max-w-6xl mx-auto px-3 sm:px-4 py-5 sm:py-6 space-y-5 sm:space-y-6">
      {/* Header & Filter Controls */}
      <div className="space-y-4 border-b border-slate-200 dark:border-slate-800 pb-5">
        <div className="flex flex-col sm:flex-row sm:items-baseline justify-between gap-3">
          <div>
            <AstryxHeading
              level={1}
              className="inline-flex items-center gap-2 text-lg sm:text-xl font-bold text-slate-900 dark:text-slate-100 text-balance"
            >
              <ImageIcon className="w-5 h-5 text-orange-600 dark:text-orange-400 shrink-0" />
              <span>
                {tx(
                  'Danh mục Figure & Sơ đồ Hệ thống',
                  'System Figures & UML Diagrams Catalog'
                )}
              </span>
            </AstryxHeading>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 text-pretty">
              {tx('Hiển thị', 'Showing')}{' '}
              <span className="font-mono font-semibold text-orange-700 dark:text-orange-400 tabular-nums">
                {filteredFigures.length}
              </span>{' '}
              {tx('trên tổng số', 'of')}{' '}
              <span className="font-mono tabular-nums">{data.figures.length}</span>{' '}
              {tx(
                'sơ đồ. Nhấn vào tên Figure để xem ảnh gốc độ phân giải cao và bảng giải thích.',
                'diagrams. Click any Figure to view the high-resolution diagram and detailed explanation.'
              )}
            </p>
          </div>

          <div className="self-start sm:self-auto">
            <AstryxSegmentedControl
              label={tx('Chế độ xem', 'View mode')}
              size="sm"
              value={viewMode}
              onChange={(val) => setViewMode(val as 'table' | 'grid')}
            >
              <AstryxSegmentedControlItem
                value="table"
                label={tx('Dạng bảng', 'Table View')}
                icon={<Table2 className="w-3.5 h-3.5" />}
              />
              <AstryxSegmentedControlItem
                value="grid"
                label={tx('Dạng lưới ảnh', 'Grid View')}
                icon={<LayoutGrid className="w-3.5 h-3.5" />}
              />
            </AstryxSegmentedControl>
          </div>
        </div>

        {/* Report Tabs via Meta Astryx TabList */}
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
                label={`${rep.code}: ${rep.title.split('(')[0].trim()} (${rep.figureCount})`}
              />
            ))}
          </AstryxTabList>
        </div>

        {/* Search + Dropdowns */}
        <div className="grid grid-cols-1 sm:grid-cols-12 gap-2.5">
          <div className="sm:col-span-6 relative">
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder={tx(
                'Tìm theo tên Figure (VD: Figure 10), mã r3-fig-10, mã FR 3.2.1...',
                'Search by Figure name (e.g., Figure 10), r3-fig-10, FR 3.2.1...'
              )}
              className="w-full pl-8 pr-3 py-1.5 text-xs sm:text-sm rounded-md border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 focus:border-orange-600 outline-none"
            />
          </div>

          <div className="sm:col-span-3 relative">
            <FolderKanban className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
            <select
              value={selectedDomain}
              onChange={(e) => setSelectedDomain(e.target.value)}
              className="w-full pl-8 pr-3 py-1.5 text-xs sm:text-sm rounded-md border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-200 outline-none focus:border-orange-600"
            >
              <option value="all">
                {tx('Tất cả phân hệ (3.2–3.10)', 'All Domains (3.2–3.10)')}
              </option>
              {data.domains.map((d) => (
                <option key={d.code} value={d.code}>
                  {d.code} - {d.title} ({d.frCount})
                </option>
              ))}
            </select>
          </div>

          <div className="sm:col-span-3 flex items-center gap-2">
            <div className="relative flex-1">
              <Users className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
              <select
                value={selectedRole}
                onChange={(e) => setSelectedRole(e.target.value)}
                className="w-full pl-8 pr-3 py-1.5 text-xs sm:text-sm rounded-md border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-200 outline-none focus:border-orange-600"
              >
                <option value="all">
                  {tx('Tất cả Actor / Role', 'All Actors / Roles')}
                </option>
                {CANONICAL_ROLES.map((r) => (
                  <option key={r} value={r}>
                    {r}
                  </option>
                ))}
              </select>
            </div>

            {(selectedReport !== 'all' ||
              selectedDomain !== 'all' ||
              selectedRole !== 'all' ||
              query) && (
              <AstryxButton
                label={tx('Xóa lọc', 'Reset')}
                variant="secondary"
                size="sm"
                icon={<RotateCcw className="w-3 h-3" />}
                onClick={resetFilters}
              />
            )}
          </div>
        </div>
      </div>

      {/* Results */}
      {filteredFigures.length === 0 ? (
        <BhEmptyState
          title={tx(
            'Không có Figure nào khớp với điều kiện tìm kiếm.',
            'No figures match the current filters.'
          )}
          icon={<ImageIcon className="w-5 h-5" />}
          actions={
            <AstryxButton
              label={tx('Hiển thị lại toàn bộ Figures', 'Show all Figures')}
              variant="primary"
              size="sm"
              icon={<RotateCcw className="w-3.5 h-3.5" />}
              onClick={resetFilters}
            />
          }
        />
      ) : viewMode === 'table' ? (
        <AstryxCard padding={0} className="border border-slate-200 dark:border-slate-800 rounded-xl overflow-hidden bg-white dark:bg-slate-900 shadow-2xs">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs sm:text-sm">
              <thead>
                <tr className="bg-orange-50/40 dark:bg-slate-800/70 border-b border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 text-xs font-semibold">
                  <th className="py-2.5 px-3 w-28">{tx('Mã Figure', 'Figure ID')}</th>
                  <th className="py-2.5 px-3 w-24 hidden sm:table-cell">
                    {tx('Tài liệu', 'Report')}
                  </th>
                  <th className="py-2.5 px-3">
                    {tx('Caption & Mô tả tóm tắt', 'Caption & Summary')}
                  </th>
                  <th className="py-2.5 px-3 w-44 hidden md:table-cell">Actors</th>
                  <th className="py-2.5 px-3 w-36 text-right">
                    {tx('Đường link', 'Deep-Link')}
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200 dark:divide-slate-800 tabular-nums">
                {filteredFigures.slice(0, visibleCount).map((fig) => (
                  <React.Fragment key={fig.id}>
                    <tr
                      className="hover:bg-orange-50/30 dark:hover:bg-slate-800/50 transition-colors group"
                    >
                      <td className="py-2.5 px-3 font-mono text-xs whitespace-nowrap align-top">
                        <AstryxCode>{fig.id}</AstryxCode>
                      </td>
                      <td className="py-2.5 px-3 text-xs whitespace-nowrap align-top hidden sm:table-cell">
                        <AstryxBadge label={fig.reportId.toUpperCase()} variant="orange" />
                      </td>
                      <td className="py-2.5 px-3 align-top">
                        <Link
                          to={`/figures/${fig.id}`}
                          className="font-semibold text-slate-900 dark:text-slate-100 group-hover:text-orange-600 dark:group-hover:text-orange-400 hover:underline block transition-colors"
                        >
                          {fig.caption}
                        </Link>
                        <p className="text-xs text-slate-500 dark:text-slate-400 line-clamp-1 mt-0.5 text-pretty">
                          {fig.viSummary || fig.summary}
                        </p>
                        <div className="flex flex-wrap gap-1 mt-1.5 md:hidden">
                          {fig.actors?.map((actor) => (
                            <RoleBadge key={actor} role={actor} size="sm" />
                          ))}
                        </div>
                      </td>
                      <td className="py-2.5 px-3 align-top hidden md:table-cell">
                        <div className="flex flex-wrap gap-1">
                          {fig.actors?.map((actor) => (
                            <RoleBadge key={actor} role={actor} size="sm" />
                          ))}
                        </div>
                      </td>
                      <td className="py-2.5 px-3 text-right whitespace-nowrap align-top">
                        <div className="inline-flex items-center gap-1.5">
                          <button
                            type="button"
                            aria-label={isCopied(fig.id) ? tx('Đã copy', 'Copied') : tx('Copy link', 'Copy')}
                            onClick={() => handleCopyDeepLink(fig.id)}
                            className="interactive-btn inline-flex items-center gap-1 px-2 py-1 rounded border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 hover:bg-orange-50 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 text-xs cursor-pointer"
                          >
                            {isCopied(fig.id) ? (
                              <>
                                <Check className="w-3 h-3 text-emerald-600" />
                                <span className="hidden sm:inline">
                                  {tx('Đã copy', 'Copied')}
                                </span>
                              </>
                            ) : (
                              <>
                                <Copy className="w-3 h-3 text-orange-600 dark:text-orange-400" />
                                <span className="hidden sm:inline">
                                  {tx('Copy link', 'Copy')}
                                </span>
                              </>
                            )}
                          </button>
                          <Link
                            to={`/figures/${fig.id}`}
                            className="interactive-btn inline-flex items-center gap-1 px-2.5 py-1 rounded bg-orange-600 hover:bg-orange-700 text-white text-xs font-medium shadow-2xs"
                          >
                            <span>{tx('Mở', 'Open')}</span>
                            <ArrowUpRight className="w-3.5 h-3.5" />
                          </Link>
                        </div>
                      </td>
                    </tr>
                    {failedUrl(fig.id) && (
                      <tr>
                        <td colSpan={5} className="px-3 pb-3">
                          <ClipboardFeedback url={failedUrl(fig.id)} />
                        </td>
                      </tr>
                    )}
                  </React.Fragment>
                ))}
              </tbody>
            </table>
          </div>
        </AstryxCard>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredFigures.slice(0, visibleCount).map((fig) => (
            <article
              key={fig.id}
              className="interactive-card group relative bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl overflow-hidden hover:border-orange-500 dark:hover:border-orange-500 hover:shadow-md flex flex-col"
            >
              <div className="aspect-[16/10] bg-white border-b border-slate-200 dark:border-slate-800 flex items-center justify-center p-2 relative">
                <img
                  src={fig.imageUrl}
                  alt={fig.caption}
                  loading="lazy"
                  className="max-h-full max-w-full object-contain transition-transform duration-200 group-hover:scale-[1.02]"
                />
                <button
                  type="button"
                  onClick={() => handleCopyDeepLink(fig.id)}
                  className="interactive-btn absolute top-2 right-2 z-10 inline-flex items-center gap-1 px-2 py-1 rounded bg-white/95 dark:bg-slate-900/95 hover:bg-orange-600 dark:hover:bg-orange-600 text-slate-700 dark:text-slate-200 hover:text-white border border-slate-200 dark:border-slate-700 text-[11px] font-medium cursor-pointer shadow-xs"
                >
                  {isCopied(fig.id) ? (
                    <>
                      <Check className="w-3 h-3" />
                      <span>{tx('Đã copy', 'Copied')}</span>
                    </>
                  ) : (
                    <>
                      <Copy className="w-3 h-3" />
                      <span>{tx('Copy link', 'Copy')}</span>
                    </>
                  )}
                </button>
              </div>

              <div className="p-3.5 flex-1 flex flex-col justify-between space-y-2">
                <div>
                  <div className="flex items-center justify-between text-[11px] text-slate-500 dark:text-slate-400 font-mono mb-1 tabular-nums">
                    <AstryxBadge label={fig.reportId.toUpperCase()} variant="orange" />
                    <AstryxCode>{fig.id}</AstryxCode>
                  </div>
                  <h3 className="text-sm font-semibold text-slate-900 dark:text-slate-100 group-hover:text-orange-600 dark:group-hover:text-orange-400 group-hover:underline line-clamp-2">
                    <Link to={`/figures/${fig.id}`} className="after:absolute after:inset-0">
                      {fig.caption}
                    </Link>
                  </h3>
                  <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 line-clamp-2 text-pretty">
                    {fig.viSummary || fig.summary}
                  </p>
                </div>

                <div className="pt-2 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between">
                  <div className="flex flex-wrap gap-1">
                    {fig.actors?.slice(0, 3).map((actor) => (
                      <RoleBadge key={actor} role={actor as CanonicalRole} size="sm" />
                    ))}
                  </div>
                  <span className="inline-flex items-center gap-1 text-xs font-medium text-orange-700 dark:text-orange-400">
                    <span>{tx('Xem', 'View')}</span>
                    <ArrowUpRight className="w-3.5 h-3.5 transition-transform group-hover:translate-x-0.5 group-hover:-translate-y-0.5" />
                  </span>
                </div>
              </div>
              {failedUrl(fig.id) && (
                <div className="relative z-10 px-3.5 pb-3.5">
                  <ClipboardFeedback url={failedUrl(fig.id)} />
                </div>
              )}
            </article>
          ))}
        </div>
      )}

      {visibleCount < filteredFigures.length && (
        <div className="text-center pt-2">
          <AstryxButton
            label={tx(
              `Tải thêm (${filteredFigures.length - visibleCount} Figures còn lại)`,
              `Load more (${filteredFigures.length - visibleCount} remaining)`
            )}
            variant="secondary"
            size="sm"
            icon={<ChevronDown className="w-3.5 h-3.5" />}
            onClick={() => setVisibleCount((prev) => prev + 60)}
          />
        </div>
      )}
    </div>
  );
};
