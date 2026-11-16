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
import { AstryxBadge, AstryxCard, AstryxCode, AstryxHeading } from '../components/astryx';

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
      <AstryxCard
        variant="orange"
        padding={8}
        className="relative overflow-hidden rounded-3xl bg-white border border-orange-200 shadow-sm"
      >
        <div className="relative z-10 flex flex-col lg:flex-row lg:items-center lg:justify-between gap-8">
          <div className="max-w-3xl space-y-4">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-orange-50 border border-orange-200 text-orange-700 text-xs font-semibold">
              <Sparkles className="w-3.5 h-3.5 text-orange-600" />
              <span>SEP490 Capstone Documentation &amp; Interactive Figure Portal</span>
              <span className="text-orange-400">•</span>
              <span className="inline-flex items-center gap-1 text-orange-800">
                <Cloud className="w-3.5 h-3.5" />
                Cloudinary HD CDN ({data.projectInfo.cloudinaryCloudName})
              </span>
            </div>

            <AstryxHeading level={1} className="text-3xl sm:text-4xl font-extrabold tracking-tight leading-tight text-slate-900">
              {data.projectInfo.name}
            </AstryxHeading>

            <p className="text-slate-600 text-sm sm:text-base leading-relaxed">
              Cổng tra cứu tài liệu kỹ thuật dành cho <strong>Hội đồng Chấm Khóa Luận (Ban Giám Khảo)</strong>.
              Mỗi đường link Figure trong tài liệu Word (Report 1–4) dẫn trực tiếp đến trang xem sơ đồ độ phân giải cao (Zoom/Pan/Fullscreen trên Cloudinary CDN) kèm bảng chú thích chi tiết, luồng xử lý, quy tắc nghiệp vụ (<AstryxCode>BR-01</AstryxCode>–<AstryxCode>BR-65</AstryxCode>) và mã thông báo (<AstryxCode>MSG01</AstryxCode>–<AstryxCode>MSG60</AstryxCode>).
            </p>

            <div className="flex flex-wrap items-center gap-3 pt-2">
              <Link
                to="/figures"
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-orange-600 hover:bg-orange-700 text-white font-semibold text-sm shadow-xs transition-all"
              >
                <ImageIcon className="w-4 h-4" />
                Tra cứu {data.projectInfo.totalFigures} Figures &amp; Sơ đồ HD
                <ArrowRight className="w-4 h-4" />
              </Link>
              <Link
                to="/frs"
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-white hover:bg-orange-50 text-slate-800 border border-orange-200 font-semibold text-sm transition-all"
              >
                <FileCode2 className="w-4 h-4 text-orange-600" />
                Xem nhanh {data.projectInfo.totalFrs} Functional Requirements
              </Link>
              <button
                onClick={onOpenSearch}
                className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-white hover:bg-orange-50 text-slate-700 border border-slate-200 text-sm font-medium transition-all cursor-pointer"
              >
                <Search className="w-4 h-4 text-orange-600" />
                Tìm kiếm nhanh (Ctrl + K)
              </button>
            </div>
          </div>

          {/* Quick Stats Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-2 gap-3 shrink-0 lg:w-80">
            <div className="bg-orange-50/60 border border-orange-200 rounded-2xl p-4">
              <div className="text-2xl font-extrabold text-orange-700">
                {data.projectInfo.totalFigures}
              </div>
              <div className="text-xs text-slate-700 mt-0.5 font-medium">Figures &amp; Diagrams</div>
              <div className="text-[11px] text-orange-600 mt-1">100% Cloudinary HD</div>
            </div>
            <div className="bg-white border border-slate-200 rounded-2xl p-4">
              <div className="text-2xl font-extrabold text-slate-900">
                {data.projectInfo.totalFrs}
              </div>
              <div className="text-xs text-slate-600 mt-0.5 font-medium">Atomic CRUD FRs</div>
              <div className="text-[11px] text-orange-600 mt-1">3.2.1 → 3.10.14</div>
            </div>
            <div className="bg-white border border-slate-200 rounded-2xl p-4">
              <div className="text-2xl font-extrabold text-slate-900">
                {data.projectInfo.totalUseCases}
              </div>
              <div className="text-xs text-slate-600 mt-0.5 font-medium">Use Cases</div>
              <div className="text-[11px] text-orange-600 mt-1">UC-001 → UC-141</div>
            </div>
            <div className="bg-white border border-slate-200 rounded-2xl p-4">
              <div className="text-2xl font-extrabold text-slate-900">
                {data.projectInfo.totalBusinessRules} / {data.projectInfo.totalMessages}
              </div>
              <div className="text-xs text-slate-600 mt-0.5 font-medium">Rules &amp; Messages</div>
              <div className="text-[11px] text-orange-600 mt-1">BR-01..65 • MSG01..60</div>
            </div>
          </div>
        </div>
      </AstryxCard>

      {/* Reports 1-4 Navigation Cards */}
      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
              <BookOpen className="w-5 h-5 text-orange-600" />
              Danh mục Tài liệu Báo cáo (Report 1 – Report 4)
            </h2>
            <p className="text-sm text-slate-600">
              Chọn từng cuốn báo cáo để xem toàn bộ danh sách Figure và chú thích tương ứng trong tài liệu Word
            </p>
          </div>
          <Link
            to="/links"
            className="hidden sm:inline-flex items-center gap-1.5 text-xs font-semibold text-orange-700 hover:text-orange-800 bg-orange-50 px-3 py-2 rounded-lg border border-orange-200"
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
              className="group bg-white rounded-2xl border border-slate-200/90 p-5 shadow-2xs hover:shadow-md hover:border-orange-400 transition-all flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between gap-2 mb-3">
                  <AstryxBadge label={report.code} variant="orange" />
                  <span className="text-xs font-semibold text-slate-500">
                    {report.figureCount} Figures
                  </span>
                </div>
                <h3 className="text-base font-bold text-slate-900 group-hover:text-orange-600 transition-colors mb-1.5">
                  {report.title}
                </h3>
                <p className="text-xs text-slate-600 leading-relaxed mb-3">
                  {report.description}
                </p>
              </div>
              <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
                <AstryxCode>{report.fileName}</AstryxCode>
                <span className="inline-flex items-center gap-1 font-semibold text-orange-600 group-hover:translate-x-0.5 transition-transform">
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
              <ImageIcon className="w-5 h-5 text-orange-600" />
              Sơ đồ Kiến trúc &amp; Tổng quan Hệ thống Tiêu biểu
            </h2>
            <p className="text-sm text-slate-600">
              Nhấn vào bất kỳ sơ đồ nào để mở trình xem HD tương tác (Zoom 50%–400%, Kéo thả, Toàn màn hình) và bảng phân tích chi tiết
            </p>
          </div>
          <Link
            to="/figures"
            className="text-xs font-semibold text-orange-600 hover:text-orange-800 inline-flex items-center gap-1"
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
                className="group bg-white rounded-2xl border border-slate-200/90 overflow-hidden shadow-2xs hover:shadow-md hover:border-orange-400 transition-all flex flex-col"
              >
                <div className="aspect-[16/10] bg-slate-100 relative overflow-hidden border-b border-slate-100 flex items-center justify-center p-3">
                  <img
                    src={fig.imageUrl}
                    alt={fig.caption}
                    loading="lazy"
                    className="max-h-full max-w-full object-contain group-hover:scale-105 transition-transform duration-300"
                  />
                  <div className="absolute top-2.5 left-2.5 flex items-center gap-1.5">
                    <AstryxBadge label={`Fig #${fig.figNum}`} variant="neutral" />
                    <AstryxBadge label={fig.reportId.toUpperCase()} variant="orange" />
                  </div>
                </div>
                <div className="p-4 flex-1 flex flex-col justify-between space-y-3">
                  <div>
                    <div className="text-[11px] font-semibold text-orange-600 uppercase tracking-wider mb-1">
                      Section {fig.section}
                    </div>
                    <h3 className="text-sm font-bold text-slate-900 group-hover:text-orange-600 transition-colors line-clamp-1">
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
                    <span className="text-xs font-semibold text-orange-600 inline-flex items-center gap-1">
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
              <Layers className="w-5 h-5 text-orange-600" />
              9 Phân hệ Chức năng Chính ({data.projectInfo.totalFrs} Functional Requirements)
            </h2>
            <p className="text-sm text-slate-600">
              Mỗi phân hệ bao gồm đầy đủ Đặc tả Yêu cầu (SRS 3.2–3.10), Sơ đồ Lớp (Class Diagram), Sơ đồ Tuần tự (Sequence Diagram) và Giao diện Màn hình (Screen Layout)
            </p>
          </div>
          <Link
            to="/frs"
            className="text-xs font-semibold text-orange-600 hover:text-orange-800 inline-flex items-center gap-1"
          >
            Mở bộ lọc 141 FRs
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {data.domains.map((dom) => (
            <AstryxCard
              key={dom.code}
              padding={5}
              className="bg-white rounded-2xl border border-slate-200/90 shadow-2xs hover:border-orange-300 transition-all flex flex-col justify-between space-y-4"
            >
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <AstryxBadge label={`Section ${dom.code}`} variant="orange" />
                  <AstryxBadge
                    label={`${dom.frCount} FRs (${dom.code}.1–${dom.code}.${dom.frCount})`}
                    variant="success"
                  />
                </div>
                <h3 className="text-base font-bold text-slate-900">{dom.title}</h3>
                <p className="text-xs text-slate-600 leading-relaxed">{dom.summary}</p>
              </div>

              <div className="pt-3 border-t border-slate-100 flex flex-wrap items-center gap-2">
                <Link
                  to={`/frs?domain=${dom.code}`}
                  className="px-2.5 py-1.5 rounded-lg bg-orange-600 hover:bg-orange-700 text-white text-xs font-semibold transition-colors"
                >
                  Xem {dom.frCount} FRs
                </Link>
                <Link
                  to={`/figures/cd-${dom.code}`}
                  className="px-2.5 py-1.5 rounded-lg bg-slate-100 hover:bg-orange-50 text-slate-700 hover:text-orange-700 text-xs font-medium transition-colors"
                >
                  Class Diagram
                </Link>
                <Link
                  to={`/figures?domain=${dom.code}`}
                  className="px-2.5 py-1.5 rounded-lg bg-slate-100 hover:bg-orange-50 text-slate-700 hover:text-orange-700 text-xs font-medium transition-colors"
                >
                  All Figures
                </Link>
              </div>
            </AstryxCard>
          ))}
        </div>
      </section>

      {/* 6 Canonical System Roles Section */}
      <AstryxCard padding={6} className="bg-white rounded-2xl border border-slate-200/90 shadow-2xs space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <ShieldCheck className="w-5 h-5 text-orange-600" />
              6 Canonical System Roles (Tác nhân Chuẩn hóa xuyên suốt Codebase &amp; SRS)
            </h2>
            <p className="text-xs text-slate-600 mt-0.5">
              Đồng bộ 100% giữa Database Seeders, RBAC Guards, Use Case Diagrams, Sequence Lifelines và Đặc tả SRS Mục 2.2.1
            </p>
          </div>
          <Link
            to="/matrices"
            className="inline-flex items-center gap-1.5 text-xs font-semibold text-orange-600 hover:text-orange-800"
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
              className="p-4 rounded-xl border border-slate-200/80 hover:border-orange-300 hover:bg-orange-50/30 transition-all space-y-2"
            >
              <div className="flex items-center justify-between">
                <RoleBadge role={actor.role} size="md" />
                <AstryxCode>Role.{actor.role.toUpperCase()}</AstryxCode>
              </div>
              <p className="text-xs text-slate-600 leading-relaxed line-clamp-3">
                {actor.description}
              </p>
              <div className="text-[11px] font-semibold text-orange-600 flex items-center gap-1 pt-1">
                <CheckCircle2 className="w-3.5 h-3.5" />
                Lọc các FR của {actor.role}
              </div>
            </Link>
          ))}
        </div>
      </AstryxCard>
    </div>
  );
};
