import React, { useState, useMemo, useEffect } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import {
  Search,
  RotateCcw,
  Layout,
  GitCommitHorizontal,
  ArrowUpRight,
  FileText,
  Users,
} from 'lucide-react';
import type { PortalData, CanonicalRole } from '../types/portal';
import { RoleBadge, CANONICAL_ROLES } from '../components/RoleBadge';
import { useAppPreferences } from '../context/AppPreferencesContext';
import {
  AstryxBadge,
  AstryxButton,
  AstryxCard,
  AstryxCode,
  AstryxHeading,
  AstryxTabList,
  AstryxTab,
} from '../components/astryx';

interface FrExplorerPageProps {
  data: PortalData;
}

export const FrExplorerPage: React.FC<FrExplorerPageProps> = ({ data }) => {
  const [searchParams, setSearchParams] = useSearchParams();
  const { tx } = useAppPreferences();
  const [selectedDomain, setSelectedDomain] = useState<string>(
    searchParams.get('domain') || 'all'
  );
  const [selectedRole, setSelectedRole] = useState<string>(
    searchParams.get('role') || 'all'
  );
  const [query, setQuery] = useState<string>(searchParams.get('q') || '');

  useEffect(() => {
    const dom = searchParams.get('domain');
    const role = searchParams.get('role');
    if (dom) setSelectedDomain(dom);
    if (role) setSelectedRole(role);
  }, [searchParams]);

  const filteredFRs = useMemo(() => {
    const q = query.trim().toLowerCase();
    return data.frs.filter((fr) => {
      if (selectedDomain !== 'all' && fr.domainCode !== selectedDomain) return false;
      if (selectedRole !== 'all' && !fr.actors.includes(selectedRole as CanonicalRole)) {
        return false;
      }
      if (q) {
        const hay = `${fr.code} ${fr.title} ${fr.ucId} ${fr.domainTitle} ${fr.viSummary} ${
          fr.purpose
        } ${fr.linkedBrCodes.join(' ')} ${fr.linkedMsgCodes.join(' ')}`.toLowerCase();
        return hay.includes(q);
      }
      return true;
    });
  }, [data.frs, selectedDomain, selectedRole, query]);

  const resetFilters = () => {
    setSelectedDomain('all');
    setSelectedRole('all');
    setQuery('');
    setSearchParams({});
  };

  return (
    <div className="max-w-6xl mx-auto px-3 sm:px-4 py-5 sm:py-6 space-y-5 sm:space-y-6">
      <div className="space-y-4 border-b border-slate-200 dark:border-slate-800 pb-5">
        <div>
          <AstryxHeading
            level={1}
            className="inline-flex items-center gap-2 text-lg sm:text-xl font-bold text-slate-900 dark:text-slate-100 text-balance"
          >
            <FileText className="w-5 h-5 text-orange-600 dark:text-orange-400 shrink-0" />
            <span>
              {tx(
                'Danh sách 141 Functional Requirements (3.2.1 – 3.10.14)',
                '141 Atomic Functional Requirements (3.2.1 – 3.10.14)'
              )}
            </span>
          </AstryxHeading>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 text-pretty">
            {tx('Hiển thị', 'Showing')}{' '}
            <span className="font-mono font-semibold text-orange-700 dark:text-orange-400 tabular-nums">
              {filteredFRs.length}
            </span>{' '}
            {tx('trên tổng số', 'of')}{' '}
            <span className="font-mono tabular-nums">{data.frs.length}</span>{' '}
            {tx(
              'yêu cầu chức năng. Dữ liệu từng phân hệ nằm trong',
              'functional requirements. Modular data stored in'
            )}{' '}
            <AstryxCode>src/data/frs/domain-3.x.json</AstryxCode>.
          </p>
        </div>

        {/* Domain Filter Tabs via Meta Astryx TabList */}
        <div className="overflow-x-auto">
          <AstryxTabList
            value={selectedDomain}
            onChange={setSelectedDomain}
            size="sm"
            hasDivider
          >
            <AstryxTab
              value="all"
              label={`${tx('Tất cả', 'All')} (${data.frs.length})`}
            />
            {data.domains.map((dom) => (
              <AstryxTab
                key={dom.code}
                value={dom.code}
                label={`${dom.code} ${dom.title} (${dom.frCount})`}
              />
            ))}
          </AstryxTabList>
        </div>

        {/* Search & Role Select */}
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-2.5">
          <div className="relative flex-1">
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder={tx(
                'Tìm theo mã FR (VD: 3.6.11), Use Case (UC-072), tên chức năng, BR-15, MSG20...',
                'Search by FR code (3.6.11), Use Case (UC-072), title, BR-15, MSG20...'
              )}
              className="w-full pl-8 pr-3 py-1.5 text-xs sm:text-sm rounded-md border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 focus:border-orange-600 outline-none"
            />
          </div>

          <div className="flex items-center gap-2">
            <div className="relative flex-1 sm:flex-none">
              <Users className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
              <select
                value={selectedRole}
                onChange={(e) => setSelectedRole(e.target.value)}
                className="w-full pl-8 pr-3 py-1.5 text-xs sm:text-sm rounded-md border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-200 outline-none focus:border-orange-600"
              >
                <option value="all">{tx('Tất cả Role', 'All Roles')}</option>
                {CANONICAL_ROLES.map((role) => (
                  <option key={role} value={role}>
                    {role}
                  </option>
                ))}
              </select>
            </div>

            {(selectedDomain !== 'all' || selectedRole !== 'all' || query) && (
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

      {/* Table of FRs */}
      <AstryxCard padding={0} className="border border-slate-200 dark:border-slate-800 rounded-xl overflow-hidden bg-white dark:bg-slate-900 shadow-2xs">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse text-xs sm:text-sm">
            <thead>
              <tr className="bg-orange-50/40 dark:bg-slate-800/70 border-b border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 text-xs font-semibold">
                <th className="py-2.5 px-3 w-20">{tx('Mã FR', 'FR Code')}</th>
                <th className="py-2.5 px-3 w-20 hidden sm:table-cell">Use Case</th>
                <th className="py-2.5 px-3">
                  {tx('Tên chức năng & Mô tả thực tế', 'Function Name & Practical Summary')}
                </th>
                <th className="py-2.5 px-3 w-40 hidden md:table-cell">Actors</th>
                <th className="py-2.5 px-3 w-48 text-right">
                  {tx('Sơ đồ', 'Diagrams')}
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 dark:divide-slate-800 tabular-nums">
              {filteredFRs.map((fr) => (
                <tr
                  key={fr.code}
                  className="hover:bg-orange-50/30 dark:hover:bg-slate-800/50 transition-colors group"
                >
                  <td className="py-3 px-3 whitespace-nowrap align-top">
                    <Link to={`/frs/${fr.code}`} className="hover:underline">
                      <AstryxBadge label={fr.code} variant="orange" />
                    </Link>
                  </td>
                  <td className="py-3 px-3 font-mono text-xs text-slate-500 dark:text-slate-400 whitespace-nowrap align-top hidden sm:table-cell">
                    <AstryxCode>{fr.ucId}</AstryxCode>
                  </td>
                  <td className="py-3 px-3 align-top space-y-1">
                    <Link
                      to={`/frs/${fr.code}`}
                      className="font-semibold text-slate-900 dark:text-slate-100 group-hover:text-orange-600 dark:group-hover:text-orange-400 hover:underline block transition-colors"
                    >
                      {fr.title}
                    </Link>
                    <p className="text-xs text-slate-600 dark:text-slate-400 text-pretty">
                      {fr.viSummary || fr.purpose}
                    </p>
                    <div className="flex flex-wrap gap-1 mt-1 md:hidden">
                      {fr.actors.map((actor) => (
                        <RoleBadge key={actor} role={actor} size="sm" />
                      ))}
                    </div>
                    {(fr.linkedBrCodes.length > 0 || fr.linkedMsgCodes.length > 0) && (
                      <div className="flex flex-wrap gap-1 pt-0.5">
                        {fr.linkedBrCodes.map((br) => (
                          <Link
                            key={br}
                            to={`/rules?code=${br}`}
                            className="font-mono text-[11px] text-slate-500 dark:text-slate-400 hover:text-orange-700 dark:hover:text-orange-400 hover:underline"
                          >
                            {br}
                          </Link>
                        ))}
                        {fr.linkedMsgCodes.map((msg) => (
                          <Link
                            key={msg}
                            to={`/rules?code=${msg}`}
                            className="font-mono text-[11px] text-slate-500 dark:text-slate-400 hover:text-orange-700 dark:hover:text-orange-400 hover:underline"
                          >
                            {msg}
                          </Link>
                        ))}
                      </div>
                    )}
                  </td>
                  <td className="py-3 px-3 align-top hidden md:table-cell">
                    <div className="flex flex-wrap gap-1">
                      {fr.actors.map((actor) => (
                        <RoleBadge key={actor} role={actor} size="sm" />
                      ))}
                    </div>
                  </td>
                  <td className="py-3 px-3 text-right whitespace-nowrap align-top">
                    <div className="inline-flex items-center gap-1 text-xs">
                      <Link
                        to={`/figures/${fr.figureId}`}
                        className="interactive-btn hidden sm:inline-flex items-center gap-1 px-2 py-1 rounded border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 hover:bg-orange-50 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200"
                      >
                        <Layout className="w-3 h-3 text-slate-500 dark:text-slate-400" />
                        <span>Fig {fr.figureNumber}</span>
                      </Link>
                      <Link
                        to={`/figures/${fr.sequenceFigureId}`}
                        className="interactive-btn hidden sm:inline-flex items-center gap-1 px-2 py-1 rounded border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 hover:bg-orange-50 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200"
                      >
                        <GitCommitHorizontal className="w-3 h-3 text-slate-500 dark:text-slate-400" />
                        <span>Seq</span>
                      </Link>
                      <Link
                        to={`/frs/${fr.code}`}
                        className="interactive-btn inline-flex items-center gap-1 px-2.5 py-1 rounded bg-orange-600 hover:bg-orange-700 text-white font-medium shadow-2xs"
                      >
                        <span>{tx('Chi tiết', 'Details')}</span>
                        <ArrowUpRight className="w-3.5 h-3.5" />
                      </Link>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </AstryxCard>
    </div>
  );
};
