import React, { useMemo, useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  ArrowLeft,
  ChevronLeft,
  ChevronRight,
  Copy,
  Check,
  Layout,
  GitCommitHorizontal,
  Network,
  ArrowUpRight,
  Info,
  Layers,
  ListChecks,
  AlertTriangle,
  BookOpen,
  Hash,
} from 'lucide-react';
import { PortalData } from '../types/portal';
import { InteractiveImageViewer } from '../components/InteractiveImageViewer';
import { RoleBadge } from '../components/RoleBadge';
import { getPortalBaseUrl } from '../components/CopyLinkBar';
import { useAppPreferences } from '../context/AppPreferencesContext';

interface FigureDetailPageProps {
  data: PortalData;
}

export const FigureDetailPage: React.FC<FigureDetailPageProps> = ({ data }) => {
  const { figureId } = useParams<{ figureId: string }>();
  const [copied, setCopied] = useState(false);
  const { tx } = useAppPreferences();

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [figureId]);

  const figIndex = useMemo(
    () =>
      data.figures.findIndex(
        (f) => f.id.toLowerCase() === (figureId || '').toLowerCase()
      ),
    [data.figures, figureId]
  );

  const fig = figIndex >= 0 ? data.figures[figIndex] : undefined;
  const prevFig = figIndex > 0 ? data.figures[figIndex - 1] : undefined;
  const nextFig =
    figIndex >= 0 && figIndex < data.figures.length - 1
      ? data.figures[figIndex + 1]
      : undefined;

  const linkedFr = useMemo(
    () => (fig?.frCode ? data.frs.find((f) => f.code === fig.frCode) : undefined),
    [data.frs, fig]
  );

  const linkedBrItems = useMemo(() => {
    if (!fig?.linkedBrCodes?.length) return [];
    const set = new Set(fig.linkedBrCodes);
    return data.businessRules.filter((b) => set.has(b.code));
  }, [data.businessRules, fig]);

  const linkedMsgItems = useMemo(() => {
    if (!fig?.linkedMsgCodes?.length) return [];
    const set = new Set(fig.linkedMsgCodes);
    return data.messages.filter((m) => set.has(m.code));
  }, [data.messages, fig]);

  if (!fig) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12 text-center">
        <div className="border border-slate-200 dark:border-slate-800 rounded-lg p-8 space-y-3 bg-white dark:bg-slate-900">
          <h1 className="text-lg font-bold text-slate-900 dark:text-slate-100">
            {tx('Không tìm thấy Figure', 'Figure not found')} &ldquo;{figureId}&rdquo;
          </h1>
          <Link
            to="/"
            className="interactive-btn inline-flex items-center gap-1.5 px-4 py-2 rounded-md bg-sky-600 text-white text-xs font-medium"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>{tx('Quay lại danh sách Figures', 'Back to Figures Catalog')}</span>
          </Link>
        </div>
      </div>
    );
  }

  const pageUrl = `${getPortalBaseUrl()}/figures/${fig.id}`;
  const handleCopy = () => {
    navigator.clipboard.writeText(pageUrl);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  return (
    <div className="max-w-6xl mx-auto px-3 sm:px-4 py-5 sm:py-6 space-y-5 sm:space-y-6">
      {/* Top Bar: Breadcrumb + Copy Link + Prev/Next */}
      <div className="flex flex-wrap items-center justify-between gap-3 text-xs border-b border-slate-200 dark:border-slate-800 pb-3">
        <div className="flex items-center gap-1.5 text-slate-500 dark:text-slate-400 flex-wrap">
          <Link
            to="/"
            className="interactive-btn inline-flex items-center gap-1.5 text-sky-700 dark:text-sky-400 hover:underline font-medium"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>{tx('Danh sách Figures', 'Figures Catalog')}</span>
          </Link>
          <ChevronRight className="w-3.5 h-3.5 text-slate-400" />
          <span className="hidden sm:inline">{fig.reportName}</span>
          <ChevronRight className="w-3.5 h-3.5 text-slate-400 hidden sm:inline" />
          <span className="font-mono text-slate-800 dark:text-slate-200 font-medium">
            {fig.id}
          </span>
        </div>

        <div className="flex flex-wrap items-center gap-1.5 sm:gap-2">
          <button
            onClick={handleCopy}
            className="interactive-btn inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md border border-sky-200 dark:border-sky-800 bg-sky-50 dark:bg-sky-950/60 hover:bg-sky-100 dark:hover:bg-sky-900/60 text-sky-800 dark:text-sky-300 font-medium cursor-pointer"
          >
            {copied ? (
              <>
                <Check className="w-3.5 h-3.5 text-emerald-600" />
                <span>{tx('Đã copy đường link', 'Link Copied')}</span>
              </>
            ) : (
              <>
                <Copy className="w-3.5 h-3.5" />
                <span>{tx('Copy link gắn Word', 'Copy Word Deep-Link')}</span>
              </>
            )}
          </button>

          {prevFig && (
            <Link
              to={`/figures/${prevFig.id}`}
              className="interactive-btn inline-flex items-center gap-1 px-2.5 py-1.5 rounded-md border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300"
              title={prevFig.caption}
            >
              <ChevronLeft className="w-3.5 h-3.5" />
              <span>{tx('Trước', 'Prev')}</span>
            </Link>
          )}
          {nextFig && (
            <Link
              to={`/figures/${nextFig.id}`}
              className="interactive-btn inline-flex items-center gap-1 px-2.5 py-1.5 rounded-md border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300"
              title={nextFig.caption}
            >
              <span>{tx('Tiếp', 'Next')}</span>
              <ChevronRight className="w-3.5 h-3.5" />
            </Link>
          )}
        </div>
      </div>

      {/* Title & Metadata */}
      <div className="space-y-3">
        <div className="flex flex-wrap items-center justify-between gap-2 text-xs text-slate-500 dark:text-slate-400">
          <div className="flex flex-wrap items-center gap-2">
            <span className="font-mono font-semibold text-slate-700 dark:text-slate-300">
              [{fig.reportId.toUpperCase()}]
            </span>
            <span>
              {tx('Mục', 'Section')} {fig.section}
            </span>
            {fig.frCode && (
              <Link
                to={`/frs/${fig.frCode}`}
                className="font-mono font-semibold text-sky-700 dark:text-sky-400 underline"
              >
                FR {fig.frCode} ({fig.ucId})
              </Link>
            )}
          </div>

          <div className="flex flex-wrap items-center gap-1">
            {fig.actors?.map((role) => (
              <RoleBadge key={role} role={role} size="sm" />
            ))}
          </div>
        </div>

        <h1 className="text-xl sm:text-2xl font-bold text-slate-900 dark:text-slate-100 text-balance">
          {fig.caption}
        </h1>

        {/* Quick Related Diagrams Switcher if linked to an FR */}
        {(fig.frCode ||
          fig.screenFigureId ||
          fig.sequenceFigureId ||
          fig.classDiagramFigureId) && (
          <div className="pt-1 flex flex-wrap items-center gap-1.5 text-xs">
            <span className="text-slate-500 dark:text-slate-400 mr-1">
              {tx('Sơ đồ cùng chức năng:', 'Related Diagrams:')}
            </span>
            {(fig.screenFigureId || (fig.id.startsWith('r3-fig-') && fig.frCode)) && (
              <Link
                to={`/figures/${fig.screenFigureId || fig.id}`}
                className={`interactive-btn inline-flex items-center gap-1.5 px-2.5 py-1 rounded border ${
                  fig.id === (fig.screenFigureId || fig.id)
                    ? 'bg-sky-600 text-white border-sky-600 font-medium shadow-2xs'
                    : 'bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800'
                }`}
              >
                <Layout className="w-3.5 h-3.5" />
                <span>Screen Layout</span>
              </Link>
            )}
            {(fig.sequenceFigureId || fig.id.startsWith('seq-')) && (
              <Link
                to={`/figures/${fig.sequenceFigureId || fig.id}`}
                className={`interactive-btn inline-flex items-center gap-1.5 px-2.5 py-1 rounded border ${
                  fig.id === (fig.sequenceFigureId || fig.id)
                    ? 'bg-sky-600 text-white border-sky-600 font-medium shadow-2xs'
                    : 'bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800'
                }`}
              >
                <GitCommitHorizontal className="w-3.5 h-3.5" />
                <span>Sequence Diagram</span>
              </Link>
            )}
            {fig.classDiagramFigureId && (
              <Link
                to={`/figures/${fig.classDiagramFigureId}`}
                className={`interactive-btn inline-flex items-center gap-1.5 px-2.5 py-1 rounded border ${
                  fig.id === fig.classDiagramFigureId
                    ? 'bg-sky-600 text-white border-sky-600 font-medium shadow-2xs'
                    : 'bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800'
                }`}
              >
                <Network className="w-3.5 h-3.5" />
                <span>Class Diagram ({fig.domainCode})</span>
              </Link>
            )}
            {fig.frCode && (
              <Link
                to={`/frs/${fig.frCode}`}
                className="interactive-btn inline-flex items-center gap-1 px-2.5 py-1 rounded border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 hover:bg-slate-50 dark:hover:bg-slate-800 text-sky-700 dark:text-sky-400 font-medium sm:ml-auto"
              >
                <span>
                  {tx(`Xem đặc tả FR ${fig.frCode}`, `View FR ${fig.frCode} Spec`)}
                </span>
                <ArrowUpRight className="w-3.5 h-3.5" />
              </Link>
            )}
          </div>
        )}
      </div>

      {/* 1. Hình ảnh Figure từ Cloudinary */}
      <InteractiveImageViewer
        imageUrl={fig.imageUrl}
        caption={fig.caption}
        width={fig.imageWidth}
        height={fig.imageHeight}
        category={fig.category}
        subImages={fig.subImages}
      />

      {/* 2. Phần Chú thích & Giải thích bên dưới */}
      <div className="border-t border-slate-200 dark:border-slate-800 pt-6 space-y-6">
        <div className="space-y-2">
          <h2 className="inline-flex items-center gap-2 text-base font-bold text-slate-900 dark:text-slate-100">
            <Info className="w-4 h-4 text-sky-600 dark:text-sky-400" />
            <span>{tx('Giải thích sơ đồ', 'Diagram Explanation')}</span>
          </h2>
          <div className="space-y-2.5 text-sm text-slate-700 dark:text-slate-300 leading-relaxed text-pretty">
            <p className="p-3.5 rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 border-l-4 border-l-sky-600 text-slate-800 dark:text-slate-200">
              <strong className="text-slate-900 dark:text-white">
                {tx('Tóm tắt ý nghĩa:', 'Overview:')}
              </strong>{' '}
              {fig.viSummary || fig.summary}
            </p>
            {fig.summary && fig.viSummary && fig.summary !== fig.viSummary && (
              <p>
                <strong className="text-slate-900 dark:text-white">
                  {tx('Chi tiết:', 'Details:')}
                </strong>{' '}
                {fig.summary}
              </p>
            )}
            {(fig.trigger || linkedFr?.trigger) && (
              <p>
                <strong className="text-slate-900 dark:text-white">
                  {tx('Khi nào sử dụng:', 'When Used:')}
                </strong>{' '}
                {fig.trigger || linkedFr?.trigger}
              </p>
            )}
          </div>
        </div>

        {/* Bảng chú thích các thành phần */}
        {fig.components && fig.components.length > 0 && (
          <div className="space-y-2">
            <h3 className="inline-flex items-center gap-2 text-sm font-bold text-slate-900 dark:text-slate-100">
              <Layers className="w-4 h-4 text-sky-600 dark:text-sky-400" />
              <span>
                {tx(
                  `Các phần chính trong hình (${fig.components.length})`,
                  `Key Components in Diagram (${fig.components.length})`
                )}
              </span>
            </h3>
            <div className="overflow-x-auto border border-slate-200 dark:border-slate-800 rounded-lg bg-white dark:bg-slate-900">
              <table className="w-full text-left border-collapse text-xs sm:text-sm">
                <thead>
                  <tr className="bg-slate-50 dark:bg-slate-800/70 border-b border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 font-semibold">
                    <th className="py-2 px-3 w-10">
                      <Hash className="w-3.5 h-3.5 text-slate-400" />
                    </th>
                    <th className="py-2 px-3 w-1/4">
                      {tx('Thành phần', 'Component')}
                    </th>
                    <th className="py-2 px-3 w-40">
                      {tx('Nhóm / Loại', 'Type / Layer')}
                    </th>
                    <th className="py-2 px-3">
                      {tx('Giải thích thực tế', 'Practical Explanation')}
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-200 dark:divide-slate-800 tabular-nums">
                  {fig.components.map((comp, idx) => (
                    <tr
                      key={idx}
                      className="hover:bg-slate-50/70 dark:hover:bg-slate-800/50 transition-colors"
                    >
                      <td className="py-2 px-3 font-mono text-slate-400">{idx + 1}</td>
                      <td className="py-2 px-3 font-medium text-slate-900 dark:text-slate-100">
                        {comp.name}
                      </td>
                      <td className="py-2 px-3 font-mono text-xs text-sky-700 dark:text-sky-400">
                        {comp.type}
                      </td>
                      <td className="py-2 px-3 text-slate-700 dark:text-slate-300 leading-relaxed text-pretty">
                        {comp.description}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Sequence Messages */}
        {fig.sequenceMessages && fig.sequenceMessages.length > 0 && (
          <div className="space-y-2">
            <h3 className="inline-flex items-center gap-2 text-sm font-bold text-slate-900 dark:text-slate-100">
              <GitCommitHorizontal className="w-4 h-4 text-sky-600 dark:text-sky-400" />
              <span>
                {tx(
                  'Trình tự các lời gọi trong sơ đồ tuần tự (Sequence Messages)',
                  'Sequence Diagram Call Order (Sequence Messages)'
                )}
              </span>
            </h3>
            <div className="overflow-x-auto border border-slate-200 dark:border-slate-800 rounded-lg bg-white dark:bg-slate-900">
              <table className="w-full text-left border-collapse text-xs sm:text-sm">
                <thead>
                  <tr className="bg-slate-50 dark:bg-slate-800/70 border-b border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 font-semibold">
                    <th className="py-2 px-3 w-14">{tx('Bước', 'Step')}</th>
                    <th className="py-2 px-3">{tx('Từ (Gửi)', 'Sender')}</th>
                    <th className="py-2 px-3">{tx('Đến (Nhận)', 'Receiver')}</th>
                    <th className="py-2 px-3">
                      {tx('Nội dung gọi / Trả về', 'Message / Return')}
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-200 dark:divide-slate-800 tabular-nums">
                  {fig.sequenceMessages.map((msg) => (
                    <tr
                      key={msg.step}
                      className="hover:bg-slate-50/70 dark:hover:bg-slate-800/50 transition-colors"
                    >
                      <td className="py-2 px-3 font-mono text-sky-700 dark:text-sky-400 font-medium">
                        {msg.step}
                      </td>
                      <td className="py-2 px-3 font-mono text-slate-800 dark:text-slate-200">
                        {msg.from}
                      </td>
                      <td className="py-2 px-3 font-mono text-slate-700 dark:text-slate-300">
                        {msg.to}
                      </td>
                      <td className="py-2 px-3 font-mono text-slate-600 dark:text-slate-400">
                        {msg.label}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Normal Flow & Abnormal Cases */}
        {((fig.normalFlow && fig.normalFlow.length > 0) ||
          (fig.abnormalCases && fig.abnormalCases.length > 0)) && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {fig.normalFlow && fig.normalFlow.length > 0 && (
              <div className="space-y-2">
                <h3 className="inline-flex items-center gap-2 text-sm font-bold text-slate-900 dark:text-slate-100">
                  <ListChecks className="w-4 h-4 text-sky-600 dark:text-sky-400" />
                  <span>{tx('Các bước thực hiện', 'Execution Steps')}</span>
                </h3>
                <ol className="list-decimal list-inside space-y-1.5 text-xs sm:text-sm text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 rounded-lg p-4">
                  {fig.normalFlow.map((step, i) => (
                    <li key={i} className="leading-relaxed text-pretty">
                      {step}
                    </li>
                  ))}
                </ol>
              </div>
            )}

            {fig.abnormalCases && fig.abnormalCases.length > 0 && (
              <div className="space-y-2">
                <h3 className="inline-flex items-center gap-2 text-sm font-bold text-slate-900 dark:text-slate-100">
                  <AlertTriangle className="w-4 h-4 text-amber-600 dark:text-amber-400" />
                  <span>{tx('Xử lý khi có lỗi', 'Error & Exception Handling')}</span>
                </h3>
                <ul className="list-disc list-inside space-y-1.5 text-xs sm:text-sm text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 rounded-lg p-4">
                  {fig.abnormalCases.map((ab, i) => (
                    <li key={i} className="leading-relaxed text-pretty">
                      {ab}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {/* Linked Business Rules & Messages */}
        {(linkedBrItems.length > 0 || linkedMsgItems.length > 0) && (
          <div className="space-y-2">
            <h3 className="inline-flex items-center gap-2 text-sm font-bold text-slate-900 dark:text-slate-100">
              <BookOpen className="w-4 h-4 text-sky-600 dark:text-sky-400" />
              <span>
                {tx(
                  'Quy tắc (BR) & Thông báo (MSG) liên quan',
                  'Related Business Rules (BR) & Messages (MSG)'
                )}
              </span>
            </h3>
            <div className="border border-slate-200 dark:border-slate-800 rounded-lg divide-y divide-slate-200 dark:divide-slate-800 bg-white dark:bg-slate-900 text-xs sm:text-sm">
              {linkedBrItems.map((br) => (
                <div key={br.code} className="p-3">
                  <span className="font-mono font-semibold text-sky-700 dark:text-sky-400">
                    {br.code}:{' '}
                  </span>
                  <span className="text-slate-700 dark:text-slate-300">
                    {br.definition}
                  </span>
                </div>
              ))}
              {linkedMsgItems.map((m) => (
                <div key={m.code} className="p-3">
                  <span className="font-mono font-semibold text-sky-700 dark:text-sky-400">
                    {m.code} ({m.type}):{' '}
                  </span>
                  <span className="text-slate-700 dark:text-slate-300">
                    &ldquo;{m.content}&rdquo;
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
