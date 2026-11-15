import React, { useState, useMemo } from 'react';
import { Link } from 'react-router-dom';
import {
  Search,
  Check,
  Minus,
  Layers,
  ShieldCheck,
  Monitor,
  Database,
  Layout,
  GitCommitHorizontal,
  ArrowUpRight,
  Hash,
  Cpu,
} from 'lucide-react';
import type { PortalData, CanonicalRole } from '../types/portal';
import { RoleBadge, CANONICAL_ROLES } from '../components/RoleBadge';
import { useAppPreferences } from '../context/AppPreferencesContext';
import {
  AstryxBadge,
  AstryxCard,
  AstryxCode,
  AstryxHeading,
  AstryxTabList,
  AstryxTab,
} from '../components/astryx';

interface SystemMatrixPageProps {
  data: PortalData;
}

export const SystemMatrixPage: React.FC<SystemMatrixPageProps> = ({ data }) => {
  const [activeTab, setActiveTab] = useState<'uc' | 'auth' | 'screens' | 'erd'>('uc');
  const [query, setQuery] = useState('');
  const [selectedRole, setSelectedRole] = useState<string>('all');
  const { tx } = useAppPreferences();

  const filteredUseCases = useMemo(() => {
    const q = query.trim().toLowerCase();
    return data.useCases.filter((uc) => {
      if (selectedRole !== 'all' && !uc.actors.includes(selectedRole as CanonicalRole)) {
        return false;
      }
      if (q) {
        return `${uc.id} ${uc.frCode || ''} ${uc.name} ${uc.description}`
          .toLowerCase()
          .includes(q);
      }
      return true;
    });
  }, [data.useCases, query, selectedRole]);

  return (
    <div className="max-w-6xl mx-auto px-3 sm:px-4 py-5 sm:py-6 space-y-5 sm:space-y-6">
      <div className="space-y-4 border-b border-slate-200 dark:border-slate-800 pb-5">
        <div>
          <AstryxHeading
            level={1}
            className="inline-flex items-center gap-2 text-lg sm:text-xl font-bold text-slate-900 dark:text-slate-100 text-balance"
          >
            <ShieldCheck className="w-5 h-5 text-orange-600 dark:text-orange-400 shrink-0" />
            <span>
              {tx(
                'Ma trận Use Cases, Phân quyền RBAC & Thực thể ERD',
                'Use Cases, RBAC Authorization Matrix & ERD Entities'
              )}
            </span>
          </AstryxHeading>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 text-pretty">
            {tx('Dữ liệu được lưu tại', 'Data stored in')}{' '}
            <AstryxCode>src/data/useCases.json</AstryxCode>{' '}
            {tx('và', 'and')}{' '}
            <AstryxCode>src/data/matrices.json</AstryxCode>.
          </p>
        </div>

        <div className="overflow-x-auto">
          <AstryxTabList
            value={activeTab}
            onChange={(val) => setActiveTab(val as 'uc' | 'auth' | 'screens' | 'erd')}
            size="sm"
            hasDivider
          >
            <AstryxTab
              value="uc"
              label="141 Use Cases (UC-001 – UC-141)"
              icon={<Layers className="w-3.5 h-3.5" />}
            />
            <AstryxTab
              value="auth"
              label={tx(
                'Ma trận Phân quyền (38 Màn hình × 6 Roles)',
                'RBAC Matrix (38 Screens × 6 Roles)'
              )}
              icon={<ShieldCheck className="w-3.5 h-3.5" />}
            />
            <AstryxTab
              value="screens"
              label={tx(
                '38 Màn hình & 12 Tác vụ Ngầm',
                '38 Screens & 12 Background Tasks'
              )}
              icon={<Monitor className="w-3.5 h-3.5" />}
            />
            <AstryxTab
              value="erd"
              label={tx('28 Thực thể CSDL (ERD)', '28 Database Entities (ERD)')}
              icon={<Database className="w-3.5 h-3.5" />}
            />
          </AstryxTabList>
        </div>
      </div>

      {/* TAB 1: Use Cases */}
      {activeTab === 'uc' && (
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-2.5">
            <div className="relative flex-1 max-w-md">
              <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder={tx(
                  'Tìm UC-001, 3.2.1, tên Use Case...',
                  'Search UC-001, 3.2.1, Use Case name...'
                )}
                className="w-full pl-8 pr-3 py-1.5 text-xs sm:text-sm rounded-md border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 focus:border-orange-600 outline-none"
              />
            </div>
            <div className="flex flex-wrap items-center gap-1 text-xs">
              <button
                onClick={() => setSelectedRole('all')}
                className={`interactive-btn px-2.5 py-1 rounded border cursor-pointer ${
                  selectedRole === 'all'
                    ? 'bg-orange-600 text-white border-orange-600 font-medium'
                    : 'bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 hover:bg-orange-50 dark:hover:bg-slate-800'
                }`}
              >
                {tx('Tất cả', 'All')} ({data.useCases.length})
              </button>
              {CANONICAL_ROLES.map((r) => (
                <button
                  key={r}
                  onClick={() => setSelectedRole(r === selectedRole ? 'all' : r)}
                  className={`interactive-btn px-2.5 py-1 rounded border cursor-pointer ${
                    selectedRole === r
                      ? 'bg-orange-600 text-white border-orange-600 font-medium'
                      : 'bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 hover:bg-orange-50 dark:hover:bg-slate-800'
                  }`}
                >
                  {r}
                </button>
              ))}
            </div>
          </div>

          <AstryxCard padding={0} className="border border-slate-200 dark:border-slate-800 rounded-xl overflow-hidden bg-white dark:bg-slate-900 shadow-2xs">
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse text-xs sm:text-sm">
                <thead>
                  <tr className="bg-orange-50/40 dark:bg-slate-800/70 border-b border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 text-xs font-semibold">
                    <th className="py-2.5 px-3 w-20">UC ID</th>
                    <th className="py-2.5 px-3 w-20">{tx('Mã FR', 'FR Code')}</th>
                    <th className="py-2.5 px-3">
                      {tx('Tên Use Case & Mô tả', 'Use Case Name & Description')}
                    </th>
                    <th className="py-2.5 px-3 w-40 hidden md:table-cell">Actors</th>
                    <th className="py-2.5 px-3 w-32 text-right">Figures</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-200 dark:divide-slate-800 tabular-nums">
                  {filteredUseCases.map((uc) => {
                    const frObj = data.frs.find((f) => f.code === uc.frCode);
                    return (
                      <tr
                        key={uc.id}
                        className="hover:bg-orange-50/30 dark:hover:bg-slate-800/50 transition-colors"
                      >
                        <td className="py-2.5 px-3 font-mono text-slate-700 dark:text-slate-300 whitespace-nowrap align-top">
                          <AstryxCode>{uc.id}</AstryxCode>
                        </td>
                        <td className="py-2.5 px-3 font-mono whitespace-nowrap align-top">
                          {uc.frCode ? (
                            <Link
                              to={`/frs/${uc.frCode}`}
                              className="hover:underline"
                            >
                              <AstryxBadge label={uc.frCode} variant="orange" />
                            </Link>
                          ) : (
                            <Minus className="w-3.5 h-3.5 text-slate-300" />
                          )}
                        </td>
                        <td className="py-2.5 px-3 align-top">
                          <Link
                            to={uc.frCode ? `/frs/${uc.frCode}` : '/frs'}
                            className="font-semibold text-slate-900 dark:text-slate-100 hover:text-orange-600 dark:hover:text-orange-400 hover:underline block"
                          >
                            {uc.name}
                          </Link>
                          <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5 text-pretty">
                            {uc.description}
                          </p>
                          <div className="flex flex-wrap gap-1 mt-1 md:hidden">
                            {uc.actors.map((a) => (
                              <RoleBadge key={a} role={a} size="sm" />
                            ))}
                          </div>
                        </td>
                        <td className="py-2.5 px-3 align-top hidden md:table-cell">
                          <div className="flex flex-wrap gap-1">
                            {uc.actors.map((a) => (
                              <RoleBadge key={a} role={a} size="sm" />
                            ))}
                          </div>
                        </td>
                        <td className="py-2.5 px-3 text-right whitespace-nowrap align-top">
                          {frObj && (
                            <div className="inline-flex items-center gap-1 text-xs">
                              <Link
                                to={`/figures/${frObj.figureId}`}
                                className="interactive-btn inline-flex items-center gap-1 px-2 py-1 rounded border border-slate-200 dark:border-slate-700 hover:bg-orange-50 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200"
                              >
                                <Layout className="w-3 h-3 text-slate-500 dark:text-slate-400" />
                                <span>Fig {frObj.figureNumber}</span>
                              </Link>
                              <Link
                                to={`/figures/${frObj.sequenceFigureId}`}
                                className="interactive-btn inline-flex items-center gap-1 px-2 py-1 rounded border border-slate-200 dark:border-slate-700 hover:bg-orange-50 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200"
                              >
                                <GitCommitHorizontal className="w-3 h-3 text-slate-500 dark:text-slate-400" />
                                <span>Seq</span>
                              </Link>
                            </div>
                          )}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </AstryxCard>
        </div>
      )}

      {/* TAB 2: Screen Auth Matrix */}
      {activeTab === 'auth' && (
        <AstryxCard padding={0} className="border border-slate-200 dark:border-slate-800 rounded-xl overflow-hidden bg-white dark:bg-slate-900 shadow-2xs">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs sm:text-sm">
              <thead>
                <tr className="bg-orange-50/40 dark:bg-slate-800/70 border-b border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 text-xs font-semibold">
                  <th className="py-2.5 px-3 w-10">
                    <Hash className="w-3.5 h-3.5 text-slate-400" />
                  </th>
                  <th className="py-2.5 px-3">{tx('Màn hình (Screen)', 'Screen')}</th>
                  {CANONICAL_ROLES.map((r) => (
                    <th key={r} className="py-2.5 px-3 text-center">
                      {r}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200 dark:divide-slate-800 tabular-nums">
                {data.screenAuthorization.map((row, idx) => (
                  <tr
                    key={row.screen}
                    className="hover:bg-orange-50/30 dark:hover:bg-slate-800/50 transition-colors"
                  >
                    <td className="py-2 px-3 font-mono text-slate-400">{idx + 1}</td>
                    <td className="py-2 px-3 font-medium text-slate-900 dark:text-slate-100">
                      {row.screen}
                    </td>
                    {(['Guest', 'Owner', 'Manager', 'Creator', 'Client', 'Admin'] as const).map(
                      (roleKey) => {
                        const val = row[roleKey];
                        const hasAccess =
                          val && val !== '-' && val.trim() !== '';
                        return (
                          <td key={roleKey} className="py-2 px-3 text-center">
                            {hasAccess ? (
                              <Check className="w-4 h-4 text-orange-600 dark:text-orange-400 mx-auto" />
                            ) : (
                              <Minus className="w-3.5 h-3.5 text-slate-300 dark:text-slate-700 mx-auto" />
                            )}
                          </td>
                        );
                      }
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </AstryxCard>
      )}

      {/* TAB 3: Screens & Non-Screen Functions */}
      {activeTab === 'screens' && (
        <div className="space-y-6">
          <AstryxCard padding={0} className="border border-slate-200 dark:border-slate-800 rounded-xl overflow-hidden bg-white dark:bg-slate-900">
            <div className="p-3 bg-orange-50/40 dark:bg-slate-800/70 border-b border-slate-200 dark:border-slate-800 text-xs font-semibold text-slate-800 dark:text-slate-200 inline-flex items-center gap-2 w-full">
              <Monitor className="w-4 h-4 text-orange-600 dark:text-orange-400" />
              <span>
                {tx('38 Màn hình Ứng dụng (SRS 2.4.2)', '38 Application Screens (SRS 2.4.2)')}
              </span>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse text-xs sm:text-sm">
                <thead>
                  <tr className="border-b border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-300 text-xs font-medium bg-slate-50/50 dark:bg-slate-800/40">
                    <th className="py-2 px-3 w-12">
                      <Hash className="w-3.5 h-3.5 text-slate-400" />
                    </th>
                    <th className="py-2 px-3 w-48">{tx('Phân hệ', 'Feature')}</th>
                    <th className="py-2 px-3 w-56">{tx('Tên màn hình', 'Screen Name')}</th>
                    <th className="py-2 px-3">{tx('Mô tả thực tế', 'Practical Description')}</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-200 dark:divide-slate-800 tabular-nums">
                  {data.screenDescriptions.map((sc) => (
                    <tr
                      key={sc.index}
                      className="hover:bg-orange-50/30 dark:hover:bg-slate-800/50 transition-colors"
                    >
                      <td className="py-2 px-3 font-mono text-slate-400">{sc.index}</td>
                      <td className="py-2 px-3 text-slate-600 dark:text-slate-300">
                        {sc.feature}
                      </td>
                      <td className="py-2 px-3 font-medium text-slate-900 dark:text-slate-100">
                        {sc.screen}
                      </td>
                      <td className="py-2 px-3 text-slate-600 dark:text-slate-300 text-pretty">
                        {sc.description}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </AstryxCard>

          <AstryxCard padding={0} className="border border-slate-200 dark:border-slate-800 rounded-xl overflow-hidden bg-white dark:bg-slate-900">
            <div className="p-3 bg-orange-50/40 dark:bg-slate-800/70 border-b border-slate-200 dark:border-slate-800 text-xs font-semibold text-slate-800 dark:text-slate-200 inline-flex items-center gap-2 w-full">
              <Cpu className="w-4 h-4 text-orange-600 dark:text-orange-400" />
              <span>
                {tx(
                  '12 Tác vụ Ngầm & Hệ thống (SRS 2.4.4)',
                  '12 Background & System Functions (SRS 2.4.4)'
                )}
              </span>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse text-xs sm:text-sm">
                <thead>
                  <tr className="border-b border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-300 text-xs font-medium bg-slate-50/50 dark:bg-slate-800/40">
                    <th className="py-2 px-3 w-12">
                      <Hash className="w-3.5 h-3.5 text-slate-400" />
                    </th>
                    <th className="py-2 px-3 w-48">{tx('Phân hệ', 'Feature')}</th>
                    <th className="py-2 px-3 w-56">{tx('Tên tác vụ', 'Task Name')}</th>
                    <th className="py-2 px-3">{tx('Mô tả thực tế', 'Practical Description')}</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-200 dark:divide-slate-800 tabular-nums">
                  {data.nonScreenFunctions.map((fn) => (
                    <tr
                      key={fn.index}
                      className="hover:bg-orange-50/30 dark:hover:bg-slate-800/50 transition-colors"
                    >
                      <td className="py-2 px-3 font-mono text-slate-400">{fn.index}</td>
                      <td className="py-2 px-3 text-slate-600 dark:text-slate-300">
                        {fn.feature}
                      </td>
                      <td className="py-2 px-3 font-medium text-slate-900 dark:text-slate-100">
                        {fn.systemFunction}
                      </td>
                      <td className="py-2 px-3 text-slate-600 dark:text-slate-300 text-pretty">
                        {fn.description}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </AstryxCard>
        </div>
      )}

      {/* TAB 4: ERD */}
      {activeTab === 'erd' && (
        <div className="space-y-3">
          <div className="flex flex-wrap items-center justify-between gap-2 text-xs">
            <span className="text-slate-600 dark:text-slate-400">
              {tx(
                'Danh sách 28 bảng thực thể trong cơ sở dữ liệu (SRS 2.5.1)',
                '28 Database Entities in PostgreSQL Schema (SRS 2.5.1)'
              )}
            </span>
            <Link
              to="/figures/r3-fig-9"
              className="interactive-btn inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-orange-600 hover:bg-orange-700 text-white font-medium"
            >
              <span>{tx('Xem Sơ đồ ERD (Figure 9)', 'View ERD Diagram (Figure 9)')}</span>
              <ArrowUpRight className="w-3.5 h-3.5" />
            </Link>
          </div>
          <AstryxCard padding={0} className="border border-slate-200 dark:border-slate-800 rounded-xl overflow-hidden bg-white dark:bg-slate-900">
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse text-xs sm:text-sm">
                <thead>
                  <tr className="bg-orange-50/40 dark:bg-slate-800/70 border-b border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 text-xs font-semibold">
                    <th className="py-2.5 px-3 w-12">
                      <Hash className="w-3.5 h-3.5 text-slate-400" />
                    </th>
                    <th className="py-2.5 px-3 w-64">
                      {tx('Tên Bảng / Thực thể', 'Entity / Table Name')}
                    </th>
                    <th className="py-2.5 px-3">
                      {tx('Mô tả & Quan hệ', 'Description & Relationships')}
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-200 dark:divide-slate-800 tabular-nums">
                  {data.entities.map((ent) => (
                    <tr
                      key={ent.index}
                      className="hover:bg-orange-50/30 dark:hover:bg-slate-800/50 transition-colors"
                    >
                      <td className="py-2.5 px-3 font-mono text-slate-400">{ent.index}</td>
                      <td className="py-2.5 px-3 font-mono font-semibold">
                        <AstryxBadge label={ent.entity} variant="orange" />
                      </td>
                      <td className="py-2.5 px-3 text-slate-700 dark:text-slate-300 text-pretty">
                        {ent.description}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </AstryxCard>
        </div>
      )}
    </div>
  );
};
