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
        <div className="border border-slate-200 dark:border-slate-800 rounded-lg p-8 space-y-3 bg-white dark:bg-slate-900">
          <h1 className="text-lg font-bold text-slate-900 dark:text-slate-100">
            {tx('Không tìm thấy FR', 'FR not found')} &ldquo;{frCode}&rdquo;
          </h1>
          <Link
            to="/frs"
            className="interactive-btn inline-flex items-center gap-1.5 px-4 py-2 rounded-md bg-sky-600 text-white text-xs font-medium"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>{tx('Quay lại danh sách 141 FRs', 'Back to 141 FRs')}</span>
          </Link>
        </div>
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
            className="interactive-btn inline-flex items-center gap-1.5 text-sky-700 dark:text-sky-400 hover:underline font-medium"
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
          <span className="font-mono text-slate-800 dark:text-slate-200 font-semibold">
            {fr.code}
          </span>
        </div>

        <div className="flex items-center gap-2">
          {prevFr && (
            <Link
              to={`/frs/${prevFr.code}`}
              className="interactive-btn inline-flex items-center gap-1 px-2.5 py-1 rounded-md border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300"
            >
              <ChevronLeft className="w-3.5 h-3.5" />
              <span>{prevFr.code}</span>
            </Link>
          )}
          {nextFr && (
            <Link
              to={`/frs/${nextFr.code}`}
              className="interactive-btn inline-flex items-center gap-1 px-2.5 py-1 rounded-md border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300"
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
            <span className="font-semibold text-sky-700 dark:text-sky-400">
              SRS {fr.code}
            </span>
            <ChevronRight className="w-3 h-3 text-slate-400" />
            <span>{fr.ucId}</span>
            <ChevronRight className="w-3 h-3 text-slate-400" />
            <span>
              {fr.domainCode} {fr.domainTitle}
            </span>
          </div>
          <div className="flex flex-wrap gap-1">
            {fr.actors.map((actor) => (
              <RoleBadge key={actor} role={actor} size="sm" />
            ))}
          </div>
        </div>

        <h1 className="text-xl sm:text-2xl font-bold text-slate-900 dark:text-slate-100 text-balance">
          {fr.code} ({fr.ucId}) — {fr.title}
        </h1>
        {fr.viSummary && (
          <p className="text-sm text-slate-600 dark:text-slate-300 text-pretty">
            {fr.viSummary}
          </p>
        )}
      </div>

      {/* 3-Diagram Switcher */}
      <div className="space-y-3">
        <div className="flex flex-wrap items-center justify-between gap-2 text-xs">
          <div className="flex flex-wrap items-center gap-1.5">
            <button
              onClick={() => setActiveTab('screen')}
              className={`interactive-btn inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md border cursor-pointer ${
                activeTab === 'screen'
                  ? 'bg-sky-600 text-white border-sky-600 font-medium shadow-xs'
                  : 'bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800'
              }`}
            >
              <Layout className="w-3.5 h-3.5" />
              <span>1. Screen Layout (Figure {fr.figureNumber})</span>
            </button>
            <button
              onClick={() => setActiveTab('sequence')}
              className={`interactive-btn inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md border cursor-pointer ${
                activeTab === 'sequence'
                  ? 'bg-sky-600 text-white border-sky-600 font-medium shadow-xs'
                  : 'bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800'
              }`}
            >
              <GitCommitHorizontal className="w-3.5 h-3.5" />
              <span>2. Sequence Diagram ({fr.code})</span>
            </button>
            <button
              onClick={() => setActiveTab('class')}
              className={`interactive-btn inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md border cursor-pointer ${
                activeTab === 'class'
                  ? 'bg-sky-600 text-white border-sky-600 font-medium shadow-xs'
                  : 'bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800'
              }`}
            >
              <Network className="w-3.5 h-3.5" />
              <span>3. Class Diagram ({fr.domainCode})</span>
            </button>
          </div>

          {activeFig && (
            <Link
              to={`/figures/${activeFig.id}`}
              className="interactive-btn inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 hover:bg-slate-50 dark:hover:bg-slate-800 text-sky-700 dark:text-sky-400 font-medium"
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
          <div className="space-y-3 border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 rounded-lg p-4">
            <h2 className="inline-flex items-center gap-2 font-bold text-slate-900 dark:text-slate-100">
              <FileText className="w-4 h-4 text-sky-600 dark:text-sky-400" />
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
          </div>

          <div className="space-y-3 border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 rounded-lg p-4">
            <h2 className="inline-flex items-center gap-2 font-bold text-slate-900 dark:text-slate-100">
              <Database className="w-4 h-4 text-sky-600 dark:text-sky-400" />
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
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <h2 className="inline-flex items-center gap-2 font-bold text-slate-900 dark:text-slate-100">
              <ListChecks className="w-4 h-4 text-sky-600 dark:text-sky-400" />
              <span>{tx('3. Các bước thực hiện', '3. Execution Steps')}</span>
            </h2>
            <ol className="list-decimal list-inside space-y-1.5 text-xs sm:text-sm text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 rounded-lg p-4">
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
            <ul className="list-disc list-inside space-y-1.5 text-xs sm:text-sm text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 rounded-lg p-4">
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
              <BookOpen className="w-4 h-4 text-sky-600 dark:text-sky-400" />
              <span>
                {tx(
                  '5. Quy tắc (BR) & Thông báo (MSG) liên quan',
                  '5. Related Business Rules (BR) & Messages (MSG)'
                )}
              </span>
            </h2>
            <div className="border border-slate-200 dark:border-slate-800 rounded-lg divide-y divide-slate-200 dark:divide-slate-800 bg-white dark:bg-slate-900 text-xs sm:text-sm">
              {linkedBRDetails.map((br) => (
                <div key={br.code} className="p-3">
                  <span className="font-mono font-semibold text-sky-700 dark:text-sky-400">
                    {br.code}:{' '}
                  </span>
                  <span className="text-slate-700 dark:text-slate-300">
                    {br.definition}
                  </span>
                </div>
              ))}
              {linkedMSGDetails.map((msg) => (
                <div key={msg.code} className="p-3">
                  <span className="font-mono font-semibold text-sky-700 dark:text-sky-400">
                    {msg.code} ({msg.type}):{' '}
                  </span>
                  <span className="text-slate-700 dark:text-slate-300">
                    &ldquo;{msg.content}&rdquo;
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
