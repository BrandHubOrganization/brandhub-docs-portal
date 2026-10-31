import React from 'react';
import { Link } from 'react-router-dom';
import {
  Image as ImageIcon,
  FileCode2,
  BookOpen,
  ShieldCheck,
  Table2,
  Link2,
  ArrowRight,
  Layers,
  Cloud,
  CheckCircle2,
  Sparkles,
  ExternalLink,
  Search,
} from 'lucide-react';
import type { PortalData, CanonicalRole } from '../types/portal';
import { RoleBadge } from '../components/RoleBadge';

interface OverviewPageProps {
  data: PortalData;
  onOpenSearch: () => void;
}

export const OverviewPage: React.FC<OverviewPageProps> = ({ data, onOpenSearch }) => {
  const featuredFigures = [
    data.figures.find((f) => f.id === 'r3-fig-1'),
    data.figures.find((f) => f.id === 'r3-fig-2'),
    data.figures.find((f) => f.id === 'r3-fig-9'),
    data.figures.find((f) => f.id === 'r2-fig-2.1'),
    data.figures.find((f) => f.id === 'cd-3.6'),
    data.figures.find((f) => f.id === 'seq-3.6.11'),
  ].filter(Boolean);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-10">
      {/* Hero Banner */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 text-white p-8 sm:p-10 shadow-xl border border-indigo-500/20">
        <div className="absolute -top-24 -right-24 w-96 h-96 rounded-full bg-indigo-500/15 blur-3xl pointer-events-none" />
        <div className="absolute -bottom-24 -left-24 w-80 h-80 rounded-full bg-violet-500/15 blur-3xl pointer-events-none" />

        <div className="relative z-10 flex flex-col lg:flex-row lg:items-center lg:justify-between gap-8">
          <div className="max-w-3xl space-y-4">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/20 border border-indigo-400/30 text-indigo-200 text-xs font-semibold">
              <Sparkles className="w-3.5 h-3.5 text-indigo-300" />
              <span>SEP490 Capstone Documentation &amp; Interactive Figure Portal</span>
              <span className="text-indigo-400">•</span>
              <span className="inline-flex items-center gap-1 text-emerald-300">
                <Cloud className="w-3.5 h-3.5" />
                Cloudinary HD CDN ({data.projectInfo.cloudinaryCloudName})
              </span>
            </div>

            <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight leading-tight">
              {data.projectInfo.name}
            </h1>

            <p className="text-slate-300 text-sm sm:text-base leading-relaxed">
              Cổng tra cứu tài liệu kỹ thuật dành cho <strong>Hội đồng Chấm Khóa Luận (Ban Giám Khảo)</strong>.
              Mỗi đường link Figure trong tài liệu Word (Report 1–4) dẫn trực tiếp đến trang xem sơ đồ độ phân giải cao (Zoom/Pan/Fullscreen trên Cloudinary CDN) kèm bảng chú thích chi tiết, luồng xử lý, quy tắc nghiệp vụ (<code className="text-indigo-200 font-mono">BR-01</code>–<code className="text-indigo-200 font-mono">BR-65</code>) và mã thông báo (<code className="text-indigo-200 font-mono">MSG01</code>–<code className="text-indigo-200 font-mono">MSG60</code>).
            </p>

            <div className="flex flex-wrap items-center gap-3 pt-2">
              <Link
                to="/figures"
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm shadow-lg shadow-indigo-600/30 transition-all"
              >
                <ImageIcon className="w-4 h-4" />
                Tra cứu {data.projectInfo.totalFigures} Figures &amp; Sơ đồ HD
                <ArrowRight className="w-4 h-4" />
              </Link>
              <Link
                to="/frs"
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-white/10 hover:bg-white/15 text-white border border-white/15 font-semibold text-sm transition-all"
              >
                <FileCode2 className="w-4 h-4 text-emerald-300" />
                Xem nhanh {data.projectInfo.totalFrs} Functional Requirements
              </Link>
              <button
                onClick={onOpenSearch}
                className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-slate-800/80 hover:bg-slate-800 text-slate-200 border border-slate-700 text-sm font-medium transition-all cursor-pointer"
              >
                <Search className="w-4 h-4 text-indigo-400" />
                Tìm kiếm nhanh (Ctrl + K)
              </button>
            </div>
          </div>

          {/* Quick Stats Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-2 gap-3 shrink-0 lg:w-80">
            <div className="bg-white/5 border border-white/10 rounded-2xl p-4 backdrop-blur-sm">
              <div className="text-2xl font-extrabold text-white">
                {data.projectInfo.totalFigures}
              </div>
              <div className="text-xs text-slate-300 mt-0.5">Figures &amp; Diagrams</div>
              <div className="text-[11px] text-indigo-300 mt-1">100% Cloudinary HD</div>
            </div>
            <div className="bg-white/5 border border-white/10 rounded-2xl p-4 backdrop-blur-sm">
              <div className="text-2xl font-extrabold text-emerald-400">
                {data.projectInfo.totalFrs}
              </div>
              <div className="text-xs text-slate-300 mt-0.5">Atomic CRUD FRs</div>
              <div className="text-[11px] text-emerald-300 mt-1">3.2.1 → 3.10.14</div>
            </div>
            <div className="bg-white/5 border border-white/10 rounded-2xl p-4 backdrop-blur-sm">
              <div className="text-2xl font-extrabold text-amber-400">
                {data.projectInfo.totalUseCases}
              </div>
              <div className="text-xs text-slate-300 mt-0.5">Use Cases</div>
              <div className="text-[11px] text-amber-300 mt-1">UC-001 → UC-141</div>
            </div>
            <div className="bg-white/5 border border-white/10 rounded-2xl p-4 backdrop-blur-sm">
              <div className="text-2xl font-extrabold text-sky-400">
                {data.projectInfo.totalBusinessRules} / {data.projectInfo.totalMessages}
              </div>
              <div className="text-xs text-slate-300 mt-0.5">Rules &amp; Messages</div>
              <div className="text-[11px] text-sky-300 mt-1">BR-01..65 • MSG01..60</div>
            </div>
          </div>
        </div>
      </div>

      {/* Reports 1-4 Navigation Cards */}
      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
              <BookOpen className="w-5 h-5 text-indigo-600" />
              Danh mục Tài liệu Báo cáo (Report 1 – Report 4)
            </h2>
            <p className="text-sm text-slate-600">
              Chọn từng cuốn báo cáo để xem toàn bộ danh sách Figure và chú thích tương ứng trong tài liệu Word
            </p>
          </div>
          <Link
            to="/links"
            className="hidden sm:inline-flex items-center gap-1.5 text-xs font-semibold text-indigo-600 hover:text-indigo-800 bg-indigo-50 px-3 py-2 rounded-lg border border-indigo-200/60"
          >
            <Link2 className="w-3.5 h-3.5" />
            Quản lý &amp; Copy Link gắn vào Word
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {data.reports.map((report) => (
            <Link
              key={report.id}
              to={`/reports/${report.id}`}
              className="group bg-white rounded-2xl border border-slate-200/90 p-5 shadow-sm hover:shadow-md hover:border-indigo-400 transition-all flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between gap-2 mb-3">
                  <span className="px-2.5 py-1 rounded-md text-xs font-bold bg-indigo-50 text-indigo-700 border border-indigo-200/60">
                    {report.code}
                  </span>
                  <span className="text-xs font-semibold text-slate-500">
                    {report.figureCount} Figures
                  </span>
                </div>
                <h3 className="text-base font-bold text-slate-900 group-hover:text-indigo-600 transition-colors mb-1.5">
                  {report.title}
                </h3>
                <p className="text-xs text-slate-600 leading-relaxed mb-3">
                  {report.description}
                </p>
              </div>
              <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
                <code className="text-[11px] text-slate-500 font-mono truncate max-w-[170px]">
                  {report.fileName}
                </code>
                <span className="inline-flex items-center gap-1 font-semibold text-indigo-600 group-hover:translate-x-0.5 transition-transform">
                  Xem Figures
                  <ArrowRight className="w-3.5 h-3.5" />
                </span>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* Featured System Overview Figures */}
      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
              <ImageIcon className="w-5 h-5 text-indigo-600" />
              Sơ đồ Kiến trúc &amp; Tổng quan Hệ thống Tiêu biểu
            </h2>
            <p className="text-sm text-slate-600">
              Nhấn vào bất kỳ sơ đồ nào để mở trình xem HD tương tác (Zoom 50%–400%, Kéo thả, Toàn màn hình) và bảng phân tích chi tiết
            </p>
          </div>
          <Link
            to="/figures"
            className="text-xs font-semibold text-indigo-600 hover:text-indigo-800 inline-flex items-center gap-1"
          >
            Xem tất cả {data.projectInfo.totalFigures} Figures
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {featuredFigures.map((fig) =>
            fig ? (
              <Link
                key={fig.id}
                to={`/figures/${fig.id}`}
                className="group bg-white rounded-2xl border border-slate-200/90 overflow-hidden shadow-sm hover:shadow-md hover:border-indigo-400 transition-all flex flex-col"
              >
                <div className="aspect-[16/10] bg-slate-100 relative overflow-hidden border-b border-slate-100 flex items-center justify-center p-3">
                  <img
                    src={fig.imageUrl}
                    alt={fig.caption}
                    loading="lazy"
                    className="max-h-full max-w-full object-contain group-hover:scale-105 transition-transform duration-300"
                  />
                  <div className="absolute top-2.5 left-2.5 flex items-center gap-1.5">
                    <span className="px-2 py-0.5 rounded-md text-[11px] font-bold bg-slate-900/80 text-white backdrop-blur-sm">
                      Fig #{fig.figNum}
                    </span>
                    <span className="px-2 py-0.5 rounded-md text-[10px] font-semibold bg-indigo-600/90 text-white backdrop-blur-sm">
                      {fig.reportId.toUpperCase()}
                    </span>
                  </div>
                </div>
                <div className="p-4 flex-1 flex flex-col justify-between space-y-3">
                  <div>
                    <div className="text-[11px] font-semibold text-indigo-600 uppercase tracking-wider mb-1">
                      Section {fig.section}
                    </div>
                    <h3 className="text-sm font-bold text-slate-900 group-hover:text-indigo-600 transition-colors line-clamp-1">
                      {fig.caption}
                    </h3>
                    <p className="text-xs text-slate-600 mt-1 line-clamp-2 leading-relaxed">
                      {fig.viSummary || fig.summary}
                    </p>
                  </div>
                  <div className="flex items-center justify-between pt-2 border-t border-slate-100">
                    <div className="flex flex-wrap gap-1">
                      {fig.actors?.slice(0, 3).map((actor) => (
                        <RoleBadge key={actor} role={actor as CanonicalRole} size="sm" />
                      ))}
                    </div>
                    <span className="text-xs font-semibold text-indigo-600 inline-flex items-center gap-1">
                      Chi tiết
                      <ExternalLink className="w-3 h-3" />
                    </span>
                  </div>
                </div>
              </Link>
            ) : null
          )}
        </div>
      </section>

      {/* 9 Functional Domains (141 Atomic CRUD FRs) */}
      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
              <Layers className="w-5 h-5 text-indigo-600" />
              9 Phân hệ Chức năng Chính ({data.projectInfo.totalFrs} Functional Requirements)
            </h2>
            <p className="text-sm text-slate-600">
              Mỗi phân hệ bao gồm đầy đủ Đặc tả Yêu cầu (SRS 3.2–3.10), Sơ đồ Lớp (Class Diagram), Sơ đồ Tuần tự (Sequence Diagram) và Giao diện Màn hình (Screen Layout)
            </p>
          </div>
          <Link
            to="/frs"
            className="text-xs font-semibold text-indigo-600 hover:text-indigo-800 inline-flex items-center gap-1"
          >
            Mở bộ lọc 141 FRs
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {data.domains.map((dom) => (
            <div
              key={dom.code}
              className="bg-white rounded-2xl border border-slate-200/90 p-5 shadow-sm hover:border-indigo-300 transition-all flex flex-col justify-between space-y-4"
            >
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="px-2.5 py-1 rounded-lg bg-indigo-50 text-indigo-700 font-mono text-xs font-bold border border-indigo-200/60">
                    Section {dom.code}
                  </span>
                  <span className="px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-700 text-xs font-bold border border-emerald-200">
                    {dom.frCount} FRs ({dom.code}.1–{dom.code}.{dom.frCount})
                  </span>
                </div>
                <h3 className="text-base font-bold text-slate-900">{dom.title}</h3>
                <p className="text-xs text-slate-600 leading-relaxed">{dom.summary}</p>
              </div>

              <div className="pt-3 border-t border-slate-100 flex flex-wrap items-center gap-2">
                <Link
                  to={`/frs?domain=${dom.code}`}
                  className="px-2.5 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold transition-colors"
                >
                  Xem {dom.frCount} FRs
                </Link>
                <Link
                  to={`/figures/cd-${dom.code}`}
                  className="px-2.5 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-medium transition-colors"
                >
                  Class Diagram
                </Link>
                <Link
                  to={`/figures?domain=${dom.code}`}
                  className="px-2.5 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-medium transition-colors"
                >
                  All Figures
                </Link>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* 6 Canonical System Roles Section */}
      <section className="bg-white rounded-2xl border border-slate-200/90 p-6 shadow-sm space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <ShieldCheck className="w-5 h-5 text-indigo-600" />
              6 Canonical System Roles (Tác nhân Chuẩn hóa xuyên suốt Codebase &amp; SRS)
            </h2>
            <p className="text-xs text-slate-600 mt-0.5">
              Đồng bộ 100% giữa Database Seeders, RBAC Guards, Use Case Diagrams, Sequence Lifelines và Đặc tả SRS Mục 2.2.1
            </p>
          </div>
          <Link
            to="/matrices"
            className="inline-flex items-center gap-1.5 text-xs font-semibold text-indigo-600 hover:text-indigo-800"
          >
            <Table2 className="w-4 h-4" />
            Xem Ma trận Phân quyền 38 Màn hình × 6 Roles
          </Link>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3.5">
          {data.actors.map((actor) => (
            <Link
              key={actor.role}
              to={`/frs?role=${actor.role}`}
              className="p-4 rounded-xl border border-slate-200/80 hover:border-indigo-300 hover:bg-slate-50/70 transition-all space-y-2"
            >
              <div className="flex items-center justify-between">
                <RoleBadge role={actor.role} size="md" />
                <code className="text-[11px] font-mono text-slate-400 bg-slate-100 px-2 py-0.5 rounded">
                  Role.{actor.role.toUpperCase()}
                </code>
              </div>
              <p className="text-xs text-slate-600 leading-relaxed line-clamp-3">
                {actor.description}
              </p>
              <div className="text-[11px] font-semibold text-indigo-600 flex items-center gap-1 pt-1">
                <CheckCircle2 className="w-3.5 h-3.5" />
                Lọc các FR của {actor.role}
              </div>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
};
