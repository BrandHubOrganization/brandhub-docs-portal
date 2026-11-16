import React, { useState, useMemo, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  ArrowLeft,
  ChevronLeft,
  ChevronRight,
  Layout,
  GitCommitHorizontal,
  Network,
  ArrowUpRight,
  FileText,
  Database,
  ListChecks,
  AlertTriangle,
  BookOpen,
} from 'lucide-react';
import type { PortalData } from '../types/portal';
import { InteractiveImageViewer } from '../components/InteractiveImageViewer';
import { RoleBadge } from '../components/RoleBadge';
import { useAppPreferences } from '../context/AppPreferencesContext';
import {
  AstryxBadge,
  AstryxCard,
  AstryxCode,
  AstryxHeading,
  AstryxSegmentedControl,
  AstryxSegmentedControlItem,
  BhEmptyState,
} from '../components/astryx';

interface FrDetailPageProps {
  data: PortalData;
}

export const FrDetailPage: React.FC<FrDetailPageProps> = ({ data }) => {
  const { frCode } = useParams<{ frCode: string }>();
  const [activeTab, setActiveTab] = useState<'screen' | 'sequence' | 'class'>('screen');
  const { tx } = useAppPreferences();

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [frCode]);

  const frIndex = useMemo(
    () => data.frs.findIndex((f) => f.code === frCode),
    [data.frs, frCode]
  );

  const fr = frIndex >= 0 ? data.frs[frIndex] : undefined;
  const prevFr = frIndex > 0 ? data.frs[frIndex - 1] : undefined;
  const nextFr =
    frIndex >= 0 && frIndex < data.frs.length - 1 ? data.frs[frIndex + 1] : undefined;

  const screenFig = useMemo(
    () => (fr ? data.figures.find((f) => f.id === fr.figureId) : undefined),
    [data.figures, fr]
  );
  const seqFig = useMemo(
    () => (fr ? data.figures.find((f) => f.id === fr.sequenceFigureId) : undefined),
    [data.figures, fr]
  );
  const classFig = useMemo(
    () => (fr ? data.figures.find((f) => f.id === fr.classDiagramFigureId) : undefined),
    [data.figures, fr]
  );

  const linkedBRDetails = useMemo(() => {
    if (!fr) return [];
    const set = new Set(fr.linkedBrCodes);
    return data.businessRules.filter((b) => set.has(b.code));
  }, [data.businessRules, fr]);

  const linkedMSGDetails = useMemo(() => {
    if (!fr) return [];
    const set = new Set(fr.linkedMsgCodes);
    return data.messages.filter((m) => set.has(m.code));
  }, [data.messages, fr]);

  if (!fr) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12 text-center">
        <BhEmptyState
          title={`${tx('Không tìm thấy FR', 'FR not found')} "${frCode}"`}
          actions={
            <Link
              to="/frs"
              className="interactive-btn inline-flex items-center gap-1.5 px-4 py-2 rounded-md bg-orange-600 text-white text-xs font-medium"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              <span>{tx('Quay lại danh sách 141 FRs', 'Back to 141 FRs')}</span>
            </Link>
          }
        />
      </div>
    );
  }

  const activeFig =
    activeTab === 'screen' ? screenFig : activeTab === 'sequence' ? seqFig : classFig;

  return (
    <div className="max-w-6xl mx-auto px-3 sm:px-4 py-5 sm:py-6 space-y-5 sm:space-y-6">
      {/* Top Bar */}
      <div className="flex flex-wrap items-center justify-between gap-3 text-xs border-b border-slate-200 dark:border-slate-800 pb-3">
        <div className="flex items-center gap-1.5 text-slate-500 dark:text-slate-400 flex-wrap">
          <Link
            to="/frs"
            className="interactive-btn inline-flex items-center gap-1.5 text-orange-700 dark:text-orange-400 hover:underline font-medium"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>{tx('Danh sách 141 FRs', '141 FRs List')}</span>
          </Link>
          <ChevronRight className="w-3.5 h-3.5 text-slate-400" />
          <Link
            to={`/frs?domain=${fr.domainCode}`}
            className="hover:underline text-slate-700 dark:text-slate-300 hidden sm:inline"
          >
            {fr.domainCode} {fr.domainTitle}
          </Link>
          <ChevronRight className="w-3.5 h-3.5 text-slate-400 hidden sm:inline" />
          <AstryxCode>{fr.code}</AstryxCode>
        </div>

        <div className="flex items-center gap-2">
          {prevFr && (
            <Link
              to={`/frs/${prevFr.code}`}
              className="interactive-btn inline-flex items-center gap-1 px-2.5 py-1 rounded-md border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 hover:bg-orange-50 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300"
            >
              <ChevronLeft className="w-3.5 h-3.5" />
              <span>{prevFr.code}</span>
            </Link>
          )}
          {nextFr && (
            <Link
              to={`/frs/${nextFr.code}`}
              className="interactive-btn inline-flex items-center gap-1 px-2.5 py-1 rounded-md border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 hover:bg-orange-50 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300"
            >
              <span>{nextFr.code}</span>
              <ChevronRight className="w-3.5 h-3.5" />
            </Link>
          )}
        </div>
      </div>

      {/* Header */}
      <div className="space-y-2">
        <div className="flex flex-wrap items-center justify-between gap-2 text-xs text-slate-500 dark:text-slate-400">
          <div className="flex items-center gap-2 font-mono flex-wrap">
            <AstryxBadge label={`SRS ${fr.code}`} variant="orange" />
            <AstryxCode>{fr.ucId}</AstryxCode>
            <AstryxBadge label={`${fr.domainCode} ${fr.domainTitle}`} variant="neutral" />
          </div>
          <div className="flex flex-wrap gap-1">
            {fr.actors.map((actor) => (
              <RoleBadge key={actor} role={actor} size="sm" />
            ))}
          </div>
        </div>

        <AstryxHeading
          level={1}
          className="text-xl sm:text-2xl font-bold text-slate-900 dark:text-slate-100 text-balance"
        >
          {fr.code} ({fr.ucId}) - {fr.title}
        </AstryxHeading>
        {fr.viSummary && (
          <p className="text-sm text-slate-600 dark:text-slate-300 text-pretty">
            {fr.viSummary}
          </p>
        )}
      </div>

      {/* 3-Diagram Switcher via Meta Astryx SegmentedControl */}
      <div className="space-y-3">
        <div className="flex flex-wrap items-center justify-between gap-2 text-xs">
          <AstryxSegmentedControl
            label={tx('Chuyển đổi loại sơ đồ', 'Switch diagram type')}
            size="sm"
            value={activeTab}
            onChange={(val) => setActiveTab(val as 'screen' | 'sequence' | 'class')}
          >
            <AstryxSegmentedControlItem
              value="screen"
              label={`1. Screen Layout (Figure ${fr.figureNumber})`}
              icon={<Layout className="w-3.5 h-3.5" />}
            />
            <AstryxSegmentedControlItem
              value="sequence"
              label={`2. Sequence Diagram (${fr.code})`}
              icon={<GitCommitHorizontal className="w-3.5 h-3.5" />}
            />
            <AstryxSegmentedControlItem
              value="class"
              label={`3. Class Diagram (${fr.domainCode})`}
              icon={<Network className="w-3.5 h-3.5" />}
            />
          </AstryxSegmentedControl>

          {activeFig && (
            <Link
              to={`/figures/${activeFig.id}`}
              className="interactive-btn inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md border border-orange-200 dark:border-slate-800 bg-orange-50/60 dark:bg-slate-900 hover:bg-orange-100 dark:hover:bg-slate-800 text-orange-700 dark:text-orange-400 font-medium"
            >
              <span>
                {tx(
                  `Mở trang riêng (/figures/${activeFig.id})`,
                  `Open Dedicated Page (/figures/${activeFig.id})`
                )}
              </span>
              <ArrowUpRight className="w-3.5 h-3.5" />
            </Link>
          )}
        </div>

        {activeFig && (
          <InteractiveImageViewer
            imageUrl={activeFig.imageUrl}
            caption={activeFig.caption}
            width={activeFig.imageWidth}
            height={activeFig.imageHeight}
            category={activeFig.category}
          />
        )}
      </div>

      {/* SRS Details */}
      <div className="border-t border-slate-200 dark:border-slate-800 pt-6 space-y-6 text-sm">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <AstryxCard padding={4} className="space-y-3 border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 rounded-xl">
            <h2 className="inline-flex items-center gap-2 font-bold text-slate-900 dark:text-slate-100">
              <FileText className="w-4 h-4 text-orange-600 dark:text-orange-400" />
              <span>
                {tx(
                  '1. Giải thích Chức năng & Màn hình',
                  '1. Function & Screen Explanation'
                )}
              </span>
            </h2>
            <dl className="space-y-2.5 text-xs sm:text-sm text-slate-700 dark:text-slate-300">
              <div>
                <dt className="font-semibold text-slate-900 dark:text-white">
                  {tx('Khi nào sử dụng:', 'When Used (Trigger):')}
                </dt>
                <dd className="text-pretty">{fr.trigger}</dd>
              </div>
              <div>
                <dt className="font-semibold text-slate-900 dark:text-white">
                  {tx('Mục đích thực tế:', 'Practical Purpose:')}
                </dt>
                <dd className="text-pretty">{fr.purpose}</dd>
              </div>
              <div>
                <dt className="font-semibold text-slate-900 dark:text-white">
                  {tx('Trên màn hình có gì:', 'Screen Layout & Controls:')}
                </dt>
                <dd className="text-pretty">{fr.interface}</dd>
              </div>
              <div>
                <dt className="font-semibold text-slate-900 dark:text-white">
                  {tx('Hệ thống xử lý thế nào:', 'System Validation & Processing:')}
                </dt>
                <dd className="text-pretty">{fr.dataProcessing}</dd>
              </div>
            </dl>
          </AstryxCard>

          <AstryxCard padding={4} className="space-y-3 border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 rounded-xl">
            <h2 className="inline-flex items-center gap-2 font-bold text-slate-900 dark:text-slate-100">
              <Database className="w-4 h-4 text-orange-600 dark:text-orange-400" />
              <span>
                {tx('2. Thông tin Đầu vào & Đầu ra', '2. Input & Output Data')}
              </span>
            </h2>
            <dl className="space-y-2.5 text-xs sm:text-sm text-slate-700 dark:text-slate-300">
              <div>
                <dt className="font-semibold text-slate-900 dark:text-white">
                  {tx('Thông tin cần nhập / chọn:', 'Required Input:')}
                </dt>
                <dd className="text-pretty">{fr.dataSpecs.inputRequired}</dd>
              </div>
              <div>
                <dt className="font-semibold text-slate-900 dark:text-white">
                  {tx('Tùy chọn thêm:', 'Optional Input:')}
                </dt>
                <dd className="text-pretty">{fr.dataSpecs.inputOptional}</dd>
              </div>
              <div>
                <dt className="font-semibold text-slate-900 dark:text-white">
                  {tx('Hệ thống tự động ghi nhận:', 'System-Generated Data:')}
                </dt>
                <dd className="text-pretty">{fr.dataSpecs.systemData}</dd>
              </div>
              <div>
                <dt className="font-semibold text-slate-900 dark:text-white">
                  {tx('Kết quả nhận được:', 'Output & Feedback:')}
                </dt>
                <dd className="text-pretty">{fr.dataSpecs.output}</dd>
              </div>
            </dl>
          </AstryxCard>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <h2 className="inline-flex items-center gap-2 font-bold text-slate-900 dark:text-slate-100">
              <ListChecks className="w-4 h-4 text-orange-600 dark:text-orange-400" />
              <span>{tx('3. Các bước thực hiện', '3. Execution Steps')}</span>
            </h2>
            <ol className="list-decimal list-inside space-y-1.5 text-xs sm:text-sm text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 rounded-xl p-4">
              {fr.normalFlow.map((step, idx) => (
                <li key={idx} className="leading-relaxed text-pretty">
                  {step}
                </li>
              ))}
            </ol>
          </div>

          <div className="space-y-2">
            <h2 className="inline-flex items-center gap-2 font-bold text-slate-900 dark:text-slate-100">
              <AlertTriangle className="w-4 h-4 text-amber-600 dark:text-amber-400" />
              <span>
                {tx('4. Xử lý khi có lỗi', '4. Error & Exception Handling')}
              </span>
            </h2>
            <ul className="list-disc list-inside space-y-1.5 text-xs sm:text-sm text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 rounded-xl p-4">
              {fr.abnormalCases.map((ab, idx) => (
                <li key={idx} className="leading-relaxed text-pretty">
                  {ab}
                </li>
              ))}
            </ul>
          </div>
        </div>

        {(linkedBRDetails.length > 0 || linkedMSGDetails.length > 0) && (
          <div className="space-y-2">
            <h2 className="inline-flex items-center gap-2 font-bold text-slate-900 dark:text-slate-100">
              <BookOpen className="w-4 h-4 text-orange-600 dark:text-orange-400" />
              <span>
                {tx(
                  '5. Quy tắc (BR) & Thông báo (MSG) liên quan',
                  '5. Related Business Rules (BR) & Messages (MSG)'
                )}
              </span>
            </h2>
            <AstryxCard padding={0} className="border border-slate-200 dark:border-slate-800 rounded-xl divide-y divide-slate-200 dark:divide-slate-800 bg-white dark:bg-slate-900 text-xs sm:text-sm">
              {linkedBRDetails.map((br) => (
                <div key={br.code} className="p-3 flex items-start gap-2">
                  <AstryxBadge label={br.code} variant="orange" />
                  <span className="text-slate-700 dark:text-slate-300">
                    {br.definition}
                  </span>
                </div>
              ))}
              {linkedMSGDetails.map((msg) => (
                <div key={msg.code} className="p-3 flex items-start gap-2">
                  <AstryxBadge label={`${msg.code} (${msg.type})`} variant="info" />
                  <span className="text-slate-700 dark:text-slate-300">
                    &ldquo;{msg.content}&rdquo;
                  </span>
                </div>
              ))}
            </AstryxCard>
          </div>
        )}
      </div>
    </div>
  );
};
