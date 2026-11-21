import React, { useState, useEffect, useCallback, useRef } from 'react';
import { Link } from 'react-router-dom';
import {
  Play,
  RotateCcw,
  Users,
  Copy,
  Check,
  Terminal,
  Sparkles,
  ShieldAlert,
  CheckCircle2,
  Send,
  Layers,
  Award,
  ExternalLink,
  RefreshCw,
      Database,
  Globe,
  GitCompare,
  FileText,
  Handshake,
  Image,
  FolderOpen,
  MessageSquare,
  Calendar,
  Hash,
  Mail,
  ClipboardList,
  Columns2,
  Maximize2,
  Compass,
  ClipboardCheck,
  MousePointerClick,
  ArrowRight,
  CheckCheck,
  Trash2,
  HelpCircle,
  ArrowLeft,
  Video,
  Megaphone,
  Newspaper,
  Presentation,
} from 'lucide-react';
import {
  AstryxBadge,
  AstryxBanner,
  AstryxButton,
  AstryxCard,
  AstryxStatusDot,
  AstryxProgressBar,
  AstryxDivider,
  AstryxCode,
  AstryxHeading,
    AstryxCollapsible,
  AstryxDialog,
  AstryxKbd,
  } from '../components/astryx';

interface RoleStatus {
  alive: boolean;
  email: string;
  full_name: string;
  badge_color: string;
  current_url: string;
}

interface MonitorStatus {
  ok: boolean;
  app_url: string;
  window_mode?: string;
  ids: {
    agency_id: string;
    workspace_id: string;
    package_id: string;
    ws_package_id: string;
    campaign_id: string;
    task_id: string;
  };
  texts: Record<string, string>;
  roles: Record<string, RoleStatus>;
}

interface FieldGuideItem {
  field: string;
  actionType: 'Nhập text' | 'Chọn dropdown' | 'Tự động điền sẵn' | 'Bấm nút' | 'Mở ngăn đối chiếu';
  value: string;
  note?: string;
  copyKey?: string;
}

interface SubActionButton {
  id: string;
  label: string;
  description: string;
  variant: 'primary' | 'outline' | 'subtle';
  icon: React.ReactNode;
  localOnly?: boolean;
}

interface DemoStep {
  stepNumber: number;
  code: string;
  stage: string;
  stageShort: string;
  timeBudget: string;
  title: string;
  shortTitle: string;
  frCode: string;
  role: 'Guest' | 'Owner' | 'Manager' | 'Creator' | 'Client' | 'Admin';
  actorName: string;
  actorEmail: string;
  routeTemplate: string;
  manualBrowserCue: string;
  talkingPoints: string[];
  presenterScript: string;
  expectedOutcome: string;
  fields: FieldGuideItem[];
  actions: SubActionButton[];
}

const CANONICAL_ROLES: Array<{
  role: 'Guest' | 'Owner' | 'Manager' | 'Creator' | 'Client' | 'Admin';
  shortLabel: string;
  fullName: string;
  email: string;
  desc: string;
}> = [
  {
    role: 'Guest',
    shortLabel: 'Khách',
    fullName: 'Khách truy cập công khai',
    email: 'Chưa đăng nhập',
    desc: 'Khách truy cập công khai: Trang chủ giới thiệu BrandHub, link chia sẻ báo giá Gói truyền thông & biểu mẫu khảo sát THPT.',
  },
  {
    role: 'Owner',
    shortLabel: 'Trung',
    fullName: 'Lê Trí Trung',
    email: 'user177@demo.brandhub.test',
    desc: 'Giám đốc SE08 Digital Agency: Xây dựng 7 gói truyền thông đa lĩnh vực, gắn gói vào Workspace ĐH FPT 2027 và nâng cấp gói cước.',
  },
  {
    role: 'Manager',
    shortLabel: 'Lộc',
    fullName: 'Nguyễn Thành Lộc',
    email: 'user1@demo.brandhub.test',
    desc: 'Quản lý chiến dịch SE08: Điều phối Chiến dịch 4 tuần (20 công việc, 6 đối tác), phân việc cho 3 Creator và duyệt nội bộ.',
  },
  {
    role: 'Creator',
    shortLabel: 'Phước',
    fullName: 'Nguyễn Chơn Phước',
    email: 'user13@demo.brandhub.test',
    desc: 'Nhóm Creator SE08 (cùng Nguyễn Minh Tuấn & Hà Văn Ân): Bắn ảnh Key Visual Gemini, gọi AI soạn bài trên /editor và xuất bản đa kênh.',
  },
  {
    role: 'Client',
    shortLabel: 'ĐH FPT',
    fullName: 'Ban Tuyển sinh Đại học FPT',
    email: 'user59@demo.brandhub.test',
    desc: 'Khách hàng Trường Đại học FPT: Nghiệm thu từng phần đầu ra, yêu cầu bổ sung 3 mức Học bổng 2027 cùng kỳ OJT và duyệt đăng.',
  },
  {
    role: 'Admin',
    shortLabel: 'Admin',
    fullName: 'Quản trị viên BrandHub',
    email: 'admin@demo.brandhub.test',
    desc: 'Quản trị hệ thống BrandHub: Giám sát doanh thu gói cước toàn nền tảng và xử lý hàng đợi kiểm duyệt an toàn nội dung.',
  },
];

const DEFAULT_DEMO_TEXTS: Record<string, string> = {
  out_of_scope_title: '[Tuần 3 - Phát sinh] Tổng hợp lịch xe đưa đón học sinh THPT dự Ngày hội FPTU Open Day 2027',
  out_of_scope_desc:
    'Bài thông báo chi tiết 08 điểm đón xe buýt miễn phí dành cho học sinh lớp 12 và phụ huynh tham gia trải nghiệm phòng Lab Thiết kế Vi mạch bán dẫn, thư viện xanh và tư vấn Học bổng Nguyễn Văn Đạo năm 2027.',
  out_of_scope_criteria:
    'Ghi rõ khung giờ đón tại từng trường THPT, đầu mối sinh viên tình nguyện phụ trách mỗi tuyến xe và đính kèm đường dẫn đăng ký https://tuyensinh.fpt.edu.vn.',
  subtask_desc:
    'Biên soạn nội dung bài đăng tổng hợp điểm nhấn chuỗi Workshop phổ biến tiện ích học đường ĐH FPT tại các trường THPT và thông báo mở cổng xét Học bổng Nguyễn Văn Đạo năm 2027 cho khóa K23.',
  subtask_criteria:
    'Nêu rõ trải nghiệm kính VR và Robotics tại buổi Workshop, 3 mức học bổng 50%, 70%, 100% học phí, lộ trình thực tập doanh nghiệp OJT từ học kỳ 6 và đường dẫn https://tuyensinh.fpt.edu.vn.',
  brief_notes:
    '1. Phản ánh không khí hào hứng của học sinh lớp 12 tại chuỗi Workshop trải nghiệm tiện ích học đường Đại học FPT.\n2. Cung cấp chính xác 3 mức Học bổng Nguyễn Văn Đạo năm 2027: 50%, 70% và 100% học phí toàn khóa.\n3. Nhấn mạnh kỳ thực tập doanh nghiệp (On-the-Job Training - OJT) từ học kỳ 6 tại FPT Software và FPT Smart Cloud.\n4. Hướng dẫn nộp hồ sơ xét tuyển đợt 1 trực tuyến tại https://tuyensinh.fpt.edu.vn.',
  brief_source_url: 'https://tuyensinh.fpt.edu.vn',
  ai_topic:
    'Tổng hợp điểm nhấn chuỗi Workshop trải nghiệm tiện ích học đường Đại học FPT dành cho học sinh THPT (đeo kính VR tham quan phòng Lab bán dẫn, điều khiển Robotics, tìm hiểu thư viện xanh, sân Vovinam và 40 CLB) kết hợp thông báo mở đăng ký xét Học bổng Nguyễn Văn Đạo năm 2027 tại 5 cơ sở Hà Nội, Đà Nẵng, Quy Nhơn, TP.HCM, Cần Thơ.',
  ai_tone_label: 'Chuyên nghiệp',
  ai_platform_label: 'Facebook',
  ai_language_label: 'Tiếng Việt',
  ai_hashtag_count: '6',
  pkg_name: "Gói Tuyển sinh Thạc sĩ FPT 2027",
  pkg_desc: "Chiến dịch 4 tuần tuyển sinh chương trình Thạc sĩ FPT 2027: bài đăng mạng xã hội, Reels, Workshop online, PR báo điện tử và bản tin Email.",
  violation_sample:
    'Học sinh trường khác toàn lũ ngu, đáng bị đánh cho chết hết.',
  caption_v1_clean:
    'TỪ SÂN TRƯỜNG THPT ĐẾN PHÒNG LAB CÔNG NGHỆ CAO: MỞ ĐĂNG KÝ XÉT HỌC BỔNG ĐẠI HỌC FPT 2027\n\nSau chuỗi Workshop phổ biến tiện ích học đường sôi nổi tại các trường THPT, hàng trăm bạn học sinh lớp 12 đã trực tiếp đeo kính VR khám phá khuôn viên 5 cơ sở, điều khiển cánh tay Robotics và trò chuyện cùng giảng viên ngành Thiết kế Vi mạch bán dẫn, Trí tuệ nhân tạo (AI).\n\nHệ sinh thái học tập thực tiễn đang chờ đón tân sinh viên khóa K23 tại Trường Đại học FPT:\n- Môi trường học tập hiện đại tại Hà Nội, Đà Nẵng, Quy Nhơn, TP.HCM và Cần Thơ với thư viện xanh, ký túc xá tiện nghi, sân Vovinam và hơn 40 CLB sinh viên.\n- Giáo trình chuẩn quốc tế, chú trọng tiếng Anh và kỹ năng làm việc trong dự án công nghệ thực tế.\n- Cổng nhận hồ sơ đăng ký xét Học bổng Nguyễn Văn Đạo đợt 1 năm 2027 đã chính thức mở.\n\nĐăng ký tư vấn và nộp hồ sơ trực tuyến tại: https://tuyensinh.fpt.edu.vn',
  client_reject_note:
    'Nội dung bản thảo v1 đã truyền tải rất tốt không khí thực tế của chuỗi Workshop tại các trường THPT. Tuy nhiên, Ban Tuyển sinh đề nghị bổ sung rõ 3 mức Học bổng Nguyễn Văn Đạo năm 2027 cụ thể (50%, 70% và 100% học phí toàn khóa) cùng thông tin học kỳ thực tập doanh nghiệp (On-the-Job Training - OJT) từ học kỳ 6 tại FPT Software và FPT Smart Cloud để phụ huynh và học sinh lớp 12 nắm đầy đủ quyền lợi trước khi duyệt xuất bản.',
  caption_v2_addition:
    '\n\nQuyền lợi học bổng và lộ trình thực tập doanh nghiệp dành cho khóa K23 (2027):\n- Chương trình Học bổng Nguyễn Văn Đạo năm 2027: Trao tặng các mức 50%, 70% và 100% học phí toàn khóa học cho học sinh THPT có thành tích học tập và năng lực nổi trội.\n- Học kỳ doanh nghiệp (On-the-Job Training - OJT): 100% sinh viên tham gia làm việc thực tế từ học kỳ 6 tại FPT Software, FPT Smart Cloud và mạng lưới doanh nghiệp đối tác trong và ngoài nước.',
};

const DEMO_STEPS: DemoStep[] = [
  {
    stepNumber: 0,
    code: 'B0',
    stage: 'Chuẩn bị trước khi thuyết trình',
    stageShort: 'GĐ 0: Chuẩn bị',
    timeBudget: 'Trước 00:00',
    title: 'Checklist chuẩn bị trước khi bắt đầu thuyết trình trước Hội đồng',
    shortTitle: 'Checklist chuẩn bị',
    frCode: '—',
    role: 'Owner',
    actorName: 'Lê Trí Trung',
    actorEmail: 'user177@demo.brandhub.test',
    routeTemplate: '',
    manualBrowserCue:
      'Tick từng việc trong danh sách sau khi đã xác nhận xong, tránh quên bước nào trước khi vào B1.',
    talkingPoints: [],
    presenterScript: '',
    expectedOutcome: 'Tất cả 5 mục chuẩn bị đều được tick Đã xong trước khi bấm Tiếp để vào B1.',
    fields: [],
    actions: [
      {
        id: 'B0_OPEN_5_CHROME',
        label: 'Mở 6 cửa sổ Chrome & Đăng nhập đủ 6 vai trò (kèm Banner HUD Socket)',
        description: 'Dùng nút "Mở 6 Vai trò" trên thanh header; kiểm tra thanh HUD góc trái dưới xuất hiện và đồng bộ WebSocket trên đủ 6 cửa sổ',
        variant: 'primary',
        icon: <Users className="size-4" />,
        localOnly: true,
      },
      {
        id: 'B0_RESTORE_DB',
        label: 'Khôi phục DB về trạng thái demo chuẩn',
        description: 'Dùng nút "Khôi phục DB" trên thanh header để nạp lại dữ liệu nền B1',
        variant: 'outline',
        icon: <RefreshCw className="size-4" />,
        localOnly: true,
      },
      {
        id: 'B0_CHECK_NETWORK',
        label: 'Kiểm tra mạng ổn định & tắt VPN lạ',
        description: 'Đảm bảo Wi-Fi/mạng phòng bảo vệ đủ mạnh cho 5 cửa sổ Chrome chạy song song',
        variant: 'outline',
        icon: <Play className="size-4" />,
        localOnly: true,
      },
      {
        id: 'B0_OPEN_BANK_APP',
        label: 'Mở sẵn app ngân hàng (demo thanh toán SePay)',
        description: 'Đăng nhập sẵn app ngân hàng trên điện thoại cho phần quét VietQR ở các bước thanh toán',
        variant: 'outline',
        icon: <FileText className="size-4" />,
        localOnly: true,
      },
      {
        id: 'B0_SILENCE_NOTIFICATIONS',
        label: 'Tắt thông báo Windows & khóa màn hình',
        description: 'Bật chế độ Tập trung (Focus Assist / Do Not Disturb), tắt thông báo chat/email nổi lên khi demo',
        variant: 'outline',
        icon: <CheckCheck className="size-4" />,
        localOnly: true,
      },
    ],
  },
  {
    stepNumber: 1,
    code: "B1",
    stage: "Giai đoạn 1: Gói dịch vụ, Chiến dịch 4 tuần & Công việc",
    stageShort: "GĐ 1: Gói dịch vụ",
    timeBudget: "00:00 - 02:30",
    title: "Danh mục 7 Gói đa ngành & Tạo gói Tuyển sinh Thạc sĩ FPT 2027",
    shortTitle: "Gói dịch vụ & Tạo gói mới",
    frCode: "FR 3.5.1 - 3.5.4",
    role: "Owner",
    actorName: "Lê Trí Trung",
    actorEmail: "user177@demo.brandhub.test",
    routeTemplate: "/agency/359a1839-18c7-48e2-8a68-f5f68c3375b6/media-packages",
    manualBrowserCue: "Bấm Tiếp lần lượt: [1] Mở Danh mục 7 Gói truyền thông → [2] Điền gói Tuyển sinh Thạc sĩ FPT 2027 → [3] Lưu gói mới → [4] Mở Gói ĐH FPT 2027 trong Workspace. Không cần thao tác tay.",
    talkingPoints: ["SE08 Digital chuẩn hóa 7 gói truyền thông cho 7 ngành.","Owner tạo trực tiếp gói mới: tên, ngân sách 85 triệu, 4 tuần, 5 hạng mục có số lượng."],
    presenterScript: "Owner Lê Trí Trung quản lý danh mục 7 gói đa ngành và tạo ngay một gói mới cho chương trình Thạc sĩ FPT 2027, gồm 5 hạng mục có số lượng cụ thể.",
    expectedOutcome: "Gói Tuyển sinh Thạc sĩ FPT 2027 xuất hiện trong danh mục; mở gói ĐH FPT 2027 đã chốt trong Workspace.",
    fields: [
      { field: "Tên gói", actionType: 'Tự động điền sẵn', value: DEFAULT_DEMO_TEXTS.pkg_name.trim(), copyKey: "pkg_name" },
      { field: "Mô tả gói", actionType: 'Tự động điền sẵn', value: DEFAULT_DEMO_TEXTS.pkg_desc.trim(), copyKey: "pkg_desc" },
      { field: "Hạng mục", actionType: 'Tự động điền sẵn', value: "12 bài MXH · 2 bài báo · 2 Workshop · 4 video ngắn · 2 Email" },
    ],
    actions: [
      { id: "B1_NAV", label: "Mở Danh mục 7 Gói truyền thông", description: "Lướt 7 thẻ gói đa ngành", variant: 'primary', icon: <Play className="size-4" /> },
      { id: "PKG_FILL", label: "Điền gói Tuyển sinh Thạc sĩ FPT 2027", description: "Tự gõ tên, 85 triệu, 4 tuần, mô tả & 5 hạng mục", variant: 'outline', icon: <Play className="size-4" /> },
      { id: "PKG_SAVE", label: "Lưu gói mới", description: "Tự bấm 'Lưu gói' và tô sáng gói vừa tạo", variant: 'outline', icon: <Play className="size-4" /> },
      { id: "B1_NAV_WS_PACKAGE", label: "Mở Gói ĐH FPT 2027 trong Workspace", description: "Gói 185 triệu, 19 hạng mục đã chốt", variant: 'outline', icon: <Play className="size-4" /> },
    ],
  },
  {
    stepNumber: 2,
    code: "B2",
    stage: "Giai đoạn 1: Gói dịch vụ, Chiến dịch 4 tuần & Công việc",
    stageShort: "GĐ 1: Gói dịch vụ",
    timeBudget: "02:30 - 04:00",
    title: "Điều phối Chiến dịch Tuyển sinh 4 Tuần (Brief, Timeline, 6 Đối tác)",
    shortTitle: "Chiến dịch 4 tuần",
    frCode: "FR 3.5.6 - 3.5.13",
    role: "Manager",
    actorName: "Nguyễn Thành Lộc",
    actorEmail: "user1@demo.brandhub.test",
    routeTemplate: "/workspaces/b47477c4-13ad-44ff-8c49-f73f1837461b/campaigns",
    manualBrowserCue: "Bấm Tiếp lần lượt: [1] Bước 1: Lộ trình 4 tuần & Master Brief → [2] Bước 2: Timeline 19 hạng mục → [3] Bước 3: 6 Đối tác Báo chí / KOL. Không cần thao tác tay.",
    talkingPoints: ["Master Brief 6 khối vạch rõ 4 tuần: Coming Soon → Ngành học → Workshop & Open Day → Báo chí.","Timeline 19 hạng mục gói và 6 đối tác báo chí, truyền hình, KOL, LED THPT."],
    presenterScript: "Manager Nguyễn Thành Lộc điều phối chiến dịch 4 tuần: Master Brief, timeline 19 hạng mục và 6 đối tác truyền thông.",
    expectedOutcome: "Trình diễn đủ 3 bước của Chiến dịch 4 tuần.",
    fields: [

    ],
    actions: [
      { id: "B3_STEP_INFO", label: "Bước 1: Lộ trình 4 tuần & Master Brief", description: "6/6 khối Brief", variant: 'primary', icon: <Play className="size-4" /> },
      { id: "B3_STEP_TASKS", label: "Bước 2: Timeline 19 hạng mục", description: "Lịch trình 4 tuần", variant: 'outline', icon: <Play className="size-4" /> },
      { id: "B3_STEP_PARTNERS", label: "Bước 3: 6 Đối tác Báo chí / KOL", description: "VnExpress, Thanh Niên, Dân Trí, VTV1, Schannel, LED", variant: 'outline', icon: <Play className="size-4" /> },
    ],
  },
  {
    stepNumber: 3,
    code: "B3",
    stage: "Giai đoạn 1: Gói dịch vụ, Chiến dịch 4 tuần & Công việc",
    stageShort: "GĐ 1: Gói dịch vụ",
    timeBudget: "04:00 - 05:00",
    title: "Phân bổ 20 Công việc cho 3 Creator & 5 Subtask bài Tuần 3",
    shortTitle: "20 Công việc & 5 Subtask",
    frCode: "FR 3.6.1 - 3.6.10",
    role: "Manager",
    actorName: "Nguyễn Thành Lộc",
    actorEmail: "user1@demo.brandhub.test",
    routeTemplate: "/workspaces/b47477c4-13ad-44ff-8c49-f73f1837461b/tasks",
    manualBrowserCue: "Bấm Tiếp lần lượt: [1] Mở 20 Công việc & 5 Subtask Tuần 3. Không cần thao tác tay.",
    talkingPoints: ["20 công việc chia theo thế mạnh của Phước, Tuấn, Ân.","Bài trọng điểm Tuần 3 có 5 Subtask phối hợp chéo; Nghiên cứu và Key Visual đã xong."],
    presenterScript: "20 công việc trong 4 tuần được giao theo chuyên môn; bài trọng điểm Tuần 3 có 5 Subtask liên kết giữa 3 thành viên.",
    expectedOutcome: "Hiển thị 20 công việc và 5 Subtask của bài Tuần 3.",
    fields: [

    ],
    actions: [
      { id: "B4_NAV", label: "Mở 20 Công việc & 5 Subtask Tuần 3", description: "Chi tiết [Tuần 3 - Bài trọng điểm]", variant: 'primary', icon: <Play className="size-4" /> },
    ],
  },
  {
    stepNumber: 4,
    code: "B4",
    stage: "Giai đoạn 2: Soạn bài, AI, Kiểm duyệt & Duyệt 2 tầng v1 → v2",
    stageShort: "GĐ 2: Soạn bài",
    timeBudget: "05:00 - 08:00",
    title: "Creator nhận bài Tuần 3, mở /editor & gọi Gemini tạo caption",
    shortTitle: "Soạn bài & AI caption",
    frCode: "FR 3.6.3, 3.6.11, 3.6.25, 3.7.1 - 3.7.2",
    role: "Creator",
    actorName: "Nguyễn Chơn Phước",
    actorEmail: "user13@demo.brandhub.test",
    routeTemplate: "/workspaces/b47477c4-13ad-44ff-8c49-f73f1837461b/editor?taskId=c6453698-cf56-38c1-96d2-90ccdd985228",
    manualBrowserCue: "Bấm Tiếp lần lượt: [1] Mở việc [Tuần 3 - Bài trọng điểm] → [2] Mở Trình soạn thảo /editor → [3] Xem Key Visual Gemini trong Kho tài nguyên → [4] Điền form AI tạo caption → [5] Tạo caption & Chèn vào bài. Không cần thao tác tay.",
    talkingPoints: ["/editor tách bài thành 4 phần độc lập: Brief, Hình ảnh, Kênh đăng, Nội dung.","Gemini tạo 3 phương án caption theo Mục tiêu, Giọng điệu, Nền tảng, Độ dài; chèn phương án 1 vào bài."],
    presenterScript: "Creator Nguyễn Chơn Phước mở bài Tuần 3, xem Key Visual Gemini trong Kho tài nguyên và gọi AI tạo 3 phương án caption.",
    expectedOutcome: "Phần Nội dung bài viết có caption do AI tạo (hoặc caption dự phòng nếu AI chậm).",
    fields: [
      { field: "Chủ đề AI", actionType: 'Tự động điền sẵn', value: DEFAULT_DEMO_TEXTS.ai_topic.trim(), copyKey: "ai_topic" },
      { field: "Tham số AI", actionType: 'Tự động điền sẵn', value: "Thông báo · Chuyên nghiệp · Facebook · Vừa" },
    ],
    actions: [
      { id: "B5_NAV", label: "Mở việc [Tuần 3 - Bài trọng điểm]", description: "Nghiên cứu & Key Visual đã xong", variant: 'primary', icon: <Play className="size-4" /> },
      { id: "B6_NAV_EDITOR", label: "Mở Trình soạn thảo /editor", description: "4 phần độc lập", variant: 'outline', icon: <Play className="size-4" /> },
      { id: "B6_PUSH_KEY_VISUAL", label: "Xem Key Visual Gemini trong Kho tài nguyên", description: "Ảnh đã Client duyệt, không thay", variant: 'outline', icon: <Play className="size-4" /> },
      { id: "AI_FILL", label: "Điền form AI tạo caption", description: "Chủ đề, Thông báo, Chuyên nghiệp, Facebook, Vừa", variant: 'outline', icon: <Play className="size-4" /> },
      { id: "AI_GENERATE", label: "Tạo caption & Chèn vào bài", description: "Gemini tạo 3 phương án, tự chèn phương án 1", variant: 'outline', icon: <Play className="size-4" /> },
    ],
  },
  {
    stepNumber: 5,
    code: "B5",
    stage: "Giai đoạn 2: Soạn bài, AI, Kiểm duyệt & Duyệt 2 tầng v1 → v2",
    stageShort: "GĐ 2: Soạn bài",
    timeBudget: "08:00 - 09:30",
    title: "Kiểm tra an toàn nội dung (3.6.33) & Nộp phần Nội dung v1",
    shortTitle: "Kiểm duyệt & Nộp v1",
    frCode: "FR 3.6.33, 3.6.18",
    role: "Creator",
    actorName: "Nguyễn Chơn Phước",
    actorEmail: "user13@demo.brandhub.test",
    routeTemplate: "/workspaces/b47477c4-13ad-44ff-8c49-f73f1837461b/editor?taskId=c6453698-cf56-38c1-96d2-90ccdd985228",
    manualBrowserCue: "Bấm Tiếp lần lượt: [1] Chèn câu vi phạm & xem cảnh báo → [2] Điền bản sạch v1 → [3] Định dạng chữ → [4] Nhập bộ hashtag → [5] Nộp phần Nội dung (v1). Không cần thao tác tay.",
    talkingPoints: ["Chèn câu bắt nạt/bạo lực: hệ thống tự kiểm tra sau 3 giây và gắn cảnh báo.","Thay bằng bản sạch v1 (chủ đích chưa ghi 3 mức học bổng & OJT).","Trình soạn thảo: in đậm tiêu đề bọc 【 】, in nghiêng câu dẫn, danh sách gạch đầu dòng; khi đăng, chữ tiếng Việt có dấu giữ nguyên để Facebook / Instagram / TikTok / Threads hiển thị đúng dấu.","Hashtag tách khỏi caption, nhập vào Bộ Hashtags bài viết; khi xuất bản hệ thống tự nối vào cuối bài."],
    presenterScript: "Creator chèn thử một câu bạo lực để thấy bộ kiểm tra an toàn tự cảnh báo, sau đó điền bản sạch v1 và nộp phần Nội dung.",
    expectedOutcome: "Phần Nội dung bài viết chuyển sang Đã nộp (v1).",
    fields: [
      { field: "Câu thử bộ lọc", actionType: 'Tự động điền sẵn', value: DEFAULT_DEMO_TEXTS.violation_sample.trim(), copyKey: "violation_sample" },
      { field: "Bản sạch v1", actionType: 'Tự động điền sẵn', value: DEFAULT_DEMO_TEXTS.caption_v1_clean.trim(), copyKey: "caption_v1_clean" },
      { field: "Bộ hashtag", actionType: 'Tự động điền sẵn', value: "#DaiHocFPT #TuyenSinhFPTU2027 #WorkshopTHPT2027 #HocBongNguyenVanDao #ViMachBanDan #FPTUniversity" },
    ],
    actions: [
      { id: "B7_FILL_VIOLATION", label: "Chèn câu vi phạm & xem cảnh báo", description: "Tự chờ kết quả kiểm tra an toàn", variant: 'primary', icon: <Play className="size-4" /> },
      { id: "V1_FILL", label: "Điền bản sạch v1", description: "Thay toàn bộ caption bằng bản v1", variant: 'outline', icon: <Play className="size-4" /> },
      { id: "V1_FORMAT", label: "Định dạng chữ (đậm, nghiêng, 【 】, danh sách)", description: "Bôi đen rồi bấm B / I, bọc 【 】 tiêu đề, tạo danh sách", variant: 'outline', icon: <Play className="size-4" /> },
      { id: "V1_HASHTAGS", label: "Nhập bộ hashtag", description: "Xoá bộ cũ, gõ 6 hashtag + Enter", variant: 'outline', icon: <Play className="size-4" /> },
      { id: "V1_SUBMIT", label: "Nộp phần Nội dung (v1)", description: "Tự bấm 'Nộp phần'", variant: 'outline', icon: <Play className="size-4" /> },
    ],
  },
  {
    stepNumber: 6,
    code: "B6",
    stage: "Giai đoạn 2: Soạn bài, AI, Kiểm duyệt & Duyệt 2 tầng v1 → v2",
    stageShort: "GĐ 2: Soạn bài",
    timeBudget: "09:30 - 10:30",
    title: "Manager Nguyễn Thành Lộc duyệt nội bộ phần Nội dung (v1)",
    shortTitle: "Manager duyệt v1",
    frCode: "FR 3.6.19",
    role: "Manager",
    actorName: "Nguyễn Thành Lộc",
    actorEmail: "user1@demo.brandhub.test",
    routeTemplate: "/workspaces/b47477c4-13ad-44ff-8c49-f73f1837461b/task-approvals?task=c6453698-cf56-38c1-96d2-90ccdd985228",
    manualBrowserCue: "Bấm Tiếp lần lượt: [1] Mở màn Duyệt bài của Manager → [2] Duyệt phần Nội dung (v1). Không cần thao tác tay.",
    talkingPoints: ["Manager chỉ duyệt riêng phần vừa nộp; các phần khác đã duyệt từ trước."],
    presenterScript: "Manager mở màn Duyệt bài, rà phần Nội dung v1 và duyệt để chuyển sang Ban Tuyển sinh ĐH FPT.",
    expectedOutcome: "Phần Nội dung chuyển sang Đã duyệt nội bộ.",
    fields: [

    ],
    actions: [
      { id: "B8_NAV_MANAGER_APPROVAL", label: "Mở màn Duyệt bài của Manager", description: "/task-approvals", variant: 'primary', icon: <Play className="size-4" /> },
      { id: "MGR_APPROVE_V1", label: "Duyệt phần Nội dung (v1)", description: "Tự bấm 'Duyệt'", variant: 'outline', icon: <Play className="size-4" /> },
    ],
  },
  {
    stepNumber: 7,
    code: "B7",
    stage: "Giai đoạn 2: Soạn bài, AI, Kiểm duyệt & Duyệt 2 tầng v1 → v2",
    stageShort: "GĐ 2: Soạn bài",
    timeBudget: "10:30 - 12:00",
    title: "Ban Tuyển sinh ĐH FPT trả lại v1, yêu cầu bổ sung Học bổng + OJT",
    shortTitle: "Client trả lại v1",
    frCode: "FR 3.6.20, 3.6.21",
    role: "Client",
    actorName: "Ban Tuyển sinh Đại học FPT",
    actorEmail: "user59@demo.brandhub.test",
    routeTemplate: "/workspaces/b47477c4-13ad-44ff-8c49-f73f1837461b/task-approvals?task=c6453698-cf56-38c1-96d2-90ccdd985228",
    manualBrowserCue: "Bấm Tiếp lần lượt: [1] Mở màn Nghiệm thu của Client → [2] Điền góp ý Học bổng 2027 + OJT → [3] Xác nhận Trả lại cho Creator. Không cần thao tác tay.",
    talkingPoints: ["Client chỉ thấy phần đầu ra, không thấy Brief nội bộ.","Trả lại riêng phần Nội dung kèm góp ý; Hình ảnh và Kênh đăng giữ nguyên đã duyệt."],
    presenterScript: "Ban Tuyển sinh ĐH FPT trả lại phần Nội dung, đề nghị bổ sung 3 mức Học bổng 2027 và kỳ OJT từ học kỳ 6.",
    expectedOutcome: "Phần Nội dung quay về Bị trả lại kèm góp ý.",
    fields: [
      { field: "Góp ý của Ban Tuyển sinh", actionType: 'Tự động điền sẵn', value: DEFAULT_DEMO_TEXTS.client_reject_note.trim(), copyKey: "client_reject_note" },
    ],
    actions: [
      { id: "B9_NAV_CLIENT_APPROVAL", label: "Mở màn Nghiệm thu của Client", description: "Chỉ thấy phần OUTPUT", variant: 'primary', icon: <Play className="size-4" /> },
      { id: "CLIENT_FILL_NOTE", label: "Điền góp ý Học bổng 2027 + OJT", description: "Tự mở hộp Trả lại và gõ góp ý", variant: 'outline', icon: <Play className="size-4" /> },
      { id: "CLIENT_RETURN", label: "Xác nhận Trả lại cho Creator", description: "Tự bấm 'Trả lại'", variant: 'outline', icon: <Play className="size-4" /> },
    ],
  },
  {
    stepNumber: 8,
    code: "B8",
    stage: "Giai đoạn 2: Soạn bài, AI, Kiểm duyệt & Duyệt 2 tầng v1 → v2",
    stageShort: "GĐ 2: Soạn bài",
    timeBudget: "12:00 - 14:00",
    title: "Creator bổ sung v2, nộp lại & đối chiếu Diff v1 / v2",
    shortTitle: "Sửa v2, Nộp & Diff",
    frCode: "FR 3.6.11, 3.6.18",
    role: "Creator",
    actorName: "Nguyễn Chơn Phước",
    actorEmail: "user13@demo.brandhub.test",
    routeTemplate: "/workspaces/b47477c4-13ad-44ff-8c49-f73f1837461b/editor?taskId=c6453698-cf56-38c1-96d2-90ccdd985228",
    manualBrowserCue: "Bấm Tiếp lần lượt: [1] Mở /editor xem góp ý → [2] Bổ sung Học bổng 50%-100% & OJT (v2) → [3] Nộp lại phần Nội dung (v2) → [4] Mở Diff v1 / v2. Không cần thao tác tay.",
    talkingPoints: ["Góp ý hiện ngay trên phần Nội dung.","Lịch sử phiên bản đối chiếu từng dòng thêm mới giữa v1 và v2."],
    presenterScript: "Creator đọc góp ý, bổ sung 3 mức Học bổng Nguyễn Văn Đạo 2027 và kỳ OJT, nộp lại v2 rồi mở bảng Diff.",
    expectedOutcome: "Phần Nội dung Đã nộp (v2); ngăn Lịch sử phiên bản hiện dòng mới thêm.",
    fields: [
      { field: "Đoạn bổ sung v2", actionType: 'Tự động điền sẵn', value: DEFAULT_DEMO_TEXTS.caption_v2_addition.trim(), copyKey: "caption_v2_addition" },
    ],
    actions: [
      { id: "B10_NAV_CREATOR_FIX", label: "Mở /editor xem góp ý", description: "Phần Nội dung bị trả lại", variant: 'primary', icon: <Play className="size-4" /> },
      { id: "V2_FILL", label: "Bổ sung Học bổng 50%-100% & OJT (v2)", description: "Tự gõ nối tiếp đoạn v2, in đậm tiêu đề mục & tạo danh sách", variant: 'outline', icon: <Play className="size-4" /> },
      { id: "V2_SUBMIT", label: "Nộp lại phần Nội dung (v2)", description: "Tự bấm 'Nộp phần'", variant: 'outline', icon: <Play className="size-4" /> },
      { id: "B10_OPEN_VERSION_DIFF", label: "Mở Diff v1 / v2", description: "Lịch sử phiên bản", variant: 'outline', icon: <Play className="size-4" /> },
    ],
  },
  {
    stepNumber: 9,
    code: "B9",
    stage: "Giai đoạn 2: Soạn bài, AI, Kiểm duyệt & Duyệt 2 tầng v1 → v2",
    stageShort: "GĐ 2: Soạn bài",
    timeBudget: "14:00 - 15:00",
    title: "Manager & Ban Tuyển sinh ĐH FPT duyệt hoàn tất v2",
    shortTitle: "Duyệt v2 → FINISHED",
    frCode: "FR 3.6.19, 3.6.20",
    role: "Client",
    actorName: "Ban Tuyển sinh Đại học FPT",
    actorEmail: "user59@demo.brandhub.test",
    routeTemplate: "/workspaces/b47477c4-13ad-44ff-8c49-f73f1837461b/task-approvals?task=c6453698-cf56-38c1-96d2-90ccdd985228",
    manualBrowserCue: "Bấm Tiếp lần lượt: [1] Manager duyệt v2 → [2] Client duyệt v2 → Task FINISHED. Không cần thao tác tay.",
    talkingPoints: ["Manager duyệt nội bộ v2, Client duyệt chính thức.","Đủ phần được duyệt: Task tự chuyển FINISHED, bài đăng sang APPROVED."],
    presenterScript: "Manager duyệt v2, Ban Tuyển sinh ĐH FPT duyệt chính thức; Task hoàn tất và bài đăng sẵn sàng xuất bản.",
    expectedOutcome: "Task FINISHED, bài đăng APPROVED.",
    fields: [

    ],
    actions: [
      { id: "B11_NAV_MANAGER_V2", label: "Manager duyệt v2", description: "Tự mở & bấm 'Duyệt'", variant: 'primary', icon: <Play className="size-4" /> },
      { id: "B11_NAV_CLIENT_V2", label: "Client duyệt v2 → Task FINISHED", description: "Tự bấm 'Duyệt' & hoàn tất Task", variant: 'outline', icon: <Play className="size-4" /> },
    ],
  },
  {
    stepNumber: 10,
    code: "B10",
    stage: "Giai đoạn 3: Xuất bản 4 nền tảng, Lịch & Dashboard",
    stageShort: "GĐ 3: Xuất bản 4 nền tảng",
    timeBudget: "15:00 - 17:00",
    title: "Đăng ngay lên Facebook, Instagram, TikTok, Threads · Lịch 4 tuần · Dashboard",
    shortTitle: "Xuất bản, Lịch & Dashboard",
    frCode: "FR 3.8.1 - 3.8.15",
    role: "Creator",
    actorName: "Nguyễn Chơn Phước",
    actorEmail: "user13@demo.brandhub.test",
    routeTemplate: "/workspaces/b47477c4-13ad-44ff-8c49-f73f1837461b/social-accounts",
    manualBrowserCue: "Bấm Tiếp lần lượt: [1] Mở Kết nối 4 nền tảng MXH → [2] Mở bài [Tuần 3] đã duyệt → [3] Đăng ngay lên 4 nền tảng → [4] Mở Lịch xuất bản 4 tuần → [5] Mở Dashboard tương tác. Không cần thao tác tay.",
    talkingPoints: ["4 tài khoản chính thức kết nối OAuth.","Đăng ngay bài vừa duyệt; kết quả từng nền tảng hiện trực tiếp (kể cả lỗi thật nếu có)."],
    presenterScript: "Manager kiểm tra 4 kết nối mạng xã hội, Creator đăng ngay bài Tuần 3, rồi xem lịch 4 tuần và dashboard tương tác.",
    expectedOutcome: "Bài Tuần 3 có trạng thái từng nền tảng; lịch và dashboard hiển thị đủ 4 tuần.",
    fields: [

    ],
    actions: [
      { id: "B12_NAV_SOCIAL", label: "Mở Kết nối 4 nền tảng MXH", description: "/social-accounts", variant: 'primary', icon: <Play className="size-4" /> },
      { id: "PUBLISH_OPEN", label: "Mở bài [Tuần 3] đã duyệt", description: "Chi tiết bài đăng", variant: 'outline', icon: <Play className="size-4" /> },
      { id: "PUBLISH_NOW", label: "Đăng ngay lên 4 nền tảng", description: "Gửi lệnh đăng & chờ kết quả", variant: 'outline', icon: <Play className="size-4" /> },
      { id: "B13_NAV_CALENDAR", label: "Mở Lịch xuất bản 4 tuần", description: "/calendar", variant: 'outline', icon: <Play className="size-4" /> },
      { id: "B13_NAV_DASHBOARD", label: "Mở Dashboard tương tác", description: "/dashboard", variant: 'outline', icon: <Play className="size-4" /> },
    ],
  },
  {
    stepNumber: 11,
    code: "B11",
    stage: "Giai đoạn 4: Thanh toán SePay (VietQR) & Quản trị",
    stageShort: "GĐ 4: Thanh toán SePay (VietQR)",
    timeBudget: "17:00 - 18:30",
    title: "Owner thanh toán Agency Plus · 1 tháng qua SePay (VietQR)",
    shortTitle: "SePay VietQR",
    frCode: "FR 3.9.1 - 3.9.4",
    role: "Owner",
    actorName: "Lê Trí Trung",
    actorEmail: "user177@demo.brandhub.test",
    routeTemplate: "/subscription/plans",
    manualBrowserCue: "Bấm Tiếp lần lượt: [1] Chọn Plus · 1 tháng → VietQR → [2] SePay xác nhận thanh toán. Không cần thao tác tay.",
    talkingPoints: ["Chọn chu kỳ 1 tháng, hệ thống sinh mã VietQR động qua SePay.","SePay gửi webhook xác nhận, gói được ghi nhận tự động."],
    presenterScript: "Owner chọn Agency Plus 1 tháng, hệ thống sinh mã VietQR; khi SePay xác nhận chuyển khoản, gói được kích hoạt tự động.",
    expectedOutcome: "Popup thanh toán chuyển trạng thái Đã ghi nhận.",
    fields: [
      { field: "Gói", actionType: 'Tự động điền sẵn', value: "Agency Plus · 1 tháng · 990.000 VND · SePay (VietQR)" },
    ],
    actions: [
      { id: "PLAN_CHECKOUT", label: "Chọn Plus · 1 tháng → VietQR", description: "Tự chọn chu kỳ & bấm Nâng cấp/Gia hạn", variant: 'primary', icon: <Play className="size-4" /> },
      { id: "SEPAY_PAY", label: "SePay xác nhận thanh toán", description: "Gửi webhook SePay, chờ trang cập nhật", variant: 'outline', icon: <Play className="size-4" /> },
    ],
  },
  {
    stepNumber: 12,
    code: "B12",
    stage: "Giai đoạn 4: Thanh toán SePay (VietQR) & Quản trị",
    stageShort: "GĐ 4: Thanh toán SePay (VietQR)",
    timeBudget: "18:30 - 20:00",
    title: "Admin giám sát doanh thu & Hàng đợi kiểm duyệt (3.10.4)",
    shortTitle: "Admin Doanh thu & Kiểm duyệt",
    frCode: "FR 3.10.1 - 3.10.4",
    role: "Admin",
    actorName: "Quản trị viên BrandHub",
    actorEmail: "admin@demo.brandhub.test",
    routeTemplate: "/admin?view=revenue",
    manualBrowserCue: "Bấm Tiếp lần lượt: [1] Mở Doanh thu toàn hệ thống → [2] Mở Hàng đợi kiểm duyệt (3.10.4). Không cần thao tác tay.",
    talkingPoints: ["Admin theo dõi doanh thu gói SaaS toàn nền tảng, gồm giao dịch SePay vừa xong.","Hàng đợi kiểm duyệt nội dung cộng đồng (FR 3.10.4) khép lại demo."],
    presenterScript: "Quản trị viên BrandHub giám sát doanh thu toàn hệ thống và rà soát hàng đợi kiểm duyệt nội dung.",
    expectedOutcome: "Dashboard doanh thu và hàng đợi kiểm duyệt hiển thị.",
    fields: [

    ],
    actions: [
      { id: "B15_NAV_ADMIN_REVENUE", label: "Mở Doanh thu toàn hệ thống", description: "/admin?view=revenue", variant: 'primary', icon: <Play className="size-4" /> },
      { id: "B15_NAV_ADMIN_MODERATION", label: "Mở Hàng đợi kiểm duyệt (3.10.4)", description: "/admin?view=moderation", variant: 'outline', icon: <Play className="size-4" /> },
    ],
  },
];

const QA_QUICK_LINKS: Array<{
  id: string;
  label: string;
  role: string;
  desc: string;
}> = [
  { id: 'QA_VIDEO_EDITOR', label: 'Video ngắn Reels/TikTok (/editor)', role: 'Creator', desc: 'Kịch bản, Quay, Dựng & Caption' },
  { id: 'QA_EVENT_EDITOR', label: 'Sự kiện FPTU Open Day (/event)', role: 'Creator', desc: '5 phân khu sự kiện lớn + Runsheet' },
  { id: 'QA_WORKSHOP_EDITOR', label: 'Chuỗi Workshop THPT (/workshop)', role: 'Creator', desc: 'Diễn giả, Lịch trình & Phiếu đăng ký' },
  { id: 'QA_PRESS_EDITOR', label: 'PR Báo chí VnExpress (/press)', role: 'Creator', desc: 'Thông cáo báo chí & Liên hệ phóng viên' },
  { id: 'QA_KOL_EDITOR', label: 'Booking KOL Schannel (/kol)', role: 'Creator', desc: 'Shortlist, Chi phí & Báo cáo nghiệm thu' },
  { id: 'QA_NEWSLETTER_EDITOR', label: 'Bản tin Email (/newsletter)', role: 'Creator', desc: 'Thiết kế khối Email Cẩm nang 2027' },
  { id: 'QA_AI_TRENDS', label: 'AI Xu hướng MXH (/ai-studio/trends)', role: 'Manager', desc: '6 xu hướng tuyển sinh trực tiếp từ Redis' },
  { id: 'QA_AI_RAG', label: 'AI Tri thức RAG (/ai-studio/knowledge-base)', role: 'Manager', desc: 'Tài liệu quy chế & học bổng ĐH FPT' },
  { id: 'QA_AI_AMBASSADORS', label: 'AI Đại sứ ảo (/ai-studio/ambassadors)', role: 'Creator', desc: 'Nhân vật Minh Anh & Hoàng Khôi K23' },
  { id: 'QA_CLIENT_PORTAL', label: 'Cổng Khách hàng (/portal)', role: 'Client', desc: '2 hạng mục Open Day chờ ĐH FPT duyệt' },
  { id: 'QA_CLIENT_VAULT', label: 'Kho riêng Client Vault (/library)', role: 'Client', desc: 'Tư liệu gốc ĐH FPT chia sẻ sang SE08' },
  { id: 'QA_COLLABORATORS', label: 'Danh bạ 10 Đối tác (/collaborators)', role: 'Owner', desc: '6 đối tác ĐH FPT + 4 đối tác đa ngành' },
  { id: 'QA_PUBLIC_PACKAGE', label: 'Link Chào giá Gói (Guest)', role: 'Guest', desc: '/packages/share/goi-tuyen-sinh-dh-fpt-2027' },
  { id: 'QA_PUBLIC_SURVEY', label: 'Link Khảo sát THPT (Guest)', role: 'Guest', desc: '/public/surveys/khao-sat-chon-nganh-fptu-2027' },
  { id: 'QA_ADMIN_CREDIT_PRICES', label: 'Bảng giá AI Credit (/admin/credit-prices)', role: 'Admin', desc: 'Cấu hình đơn giá 7 nghiệp vụ AI' },
];

export const DemoMonitorPage: React.FC = () => {
  const [monitorUrl] = useState<string>('http://127.0.0.1:3999');
  const [status, setStatus] = useState<MonitorStatus | null>(null);
  const [connected, setConnected] = useState<boolean>(false);
  const [wsConnected, setWsConnected] = useState<boolean>(false);
  const [wsClientsCount, setWsClientsCount] = useState<number>(0);
  const [activeStepIndex, setActiveStepIndex] = useState<number>(0);
  const [busyAction, setBusyAction] = useState<string | null>(null);
  const [toastMessage, setToastMessage] = useState<{ text: string; isError?: boolean } | null>(null);
  const [copiedKey, setCopiedKey] = useState<string | null>(null);
  const [showResetConfirm, setShowResetConfirm] = useState<boolean>(false);
  const [showCleanConfirm, setShowCleanConfirm] = useState<boolean>(false);
  const [showGuideModal, setShowGuideModal] = useState<boolean>(false);
  const [doneActions, setDoneActions] = useState<Record<string, boolean>>({});

  const [customTexts, setCustomTexts] = useState<Record<string, string>>(DEFAULT_DEMO_TEXTS);
  const [configIds, setConfigIds] = useState({
    app_url: 'http://localhost:3000',
    agency_id: '359a1839-18c7-48e2-8a68-f5f68c3375b6',
    workspace_id: 'b47477c4-13ad-44ff-8c49-f73f1837461b',
    campaign_id: 'd7e00000-0000-4000-8000-000000000301',
    task_id: 'c6453698-cf56-38c1-96d2-90ccdd985228',
  });

  const activePillRef = useRef<HTMLButtonElement | null>(null);
  const wsRef = useRef<WebSocket | null>(null);

  const sendWsCommand = useCallback((payload: Record<string, unknown>) => {
    const ws = wsRef.current;
    if (ws && ws.readyState === WebSocket.OPEN) {
      try {
        ws.send(JSON.stringify(payload));
      } catch {
        // Bỏ qua lỗi tạm thời khi socket đang tái kết nối
      }
    }
  }, []);

  const selectStepWithSync = useCallback(
    (nextIndexOrUpdater: number | ((prev: number) => number)) => {
      setActiveStepIndex((prev) => {
        const raw = typeof nextIndexOrUpdater === 'function' ? nextIndexOrUpdater(prev) : nextIndexOrUpdater;
        const clamped = Math.max(0, Math.min(DEMO_STEPS.length - 1, raw));
        const targetStep = DEMO_STEPS[clamped];
        if (targetStep && clamped !== prev) {
          sendWsCommand({ type: 'goto_step_code', step_code: targetStep.code, execute: false });
        }
        return clamped;
      });
    },
    [sendWsCommand]
  );

  const showToast = useCallback((text: string, isError = false) => {
    setToastMessage({ text, isError });
    setTimeout(() => {
      setToastMessage((prev) => (prev?.text === text ? null : prev));
    }, 4500);
  }, []);

  const fetchMonitorStatus = useCallback(async () => {
    try {
      const res = await fetch(`${monitorUrl}/api/status`);
      if (!res.ok) throw new Error('Status check failed');
      const data: MonitorStatus = await res.json();
      setStatus(data);
      setConnected(true);
      if (data.ids) {
        setConfigIds({
          app_url: data.app_url || 'http://localhost:3000',
          agency_id: data.ids.agency_id || '359a1839-18c7-48e2-8a68-f5f68c3375b6',
          workspace_id: data.ids.workspace_id || 'b47477c4-13ad-44ff-8c49-f73f1837461b',
          campaign_id: data.ids.campaign_id || 'd7e00000-0000-4000-8000-000000000301',
          task_id: data.ids.task_id || 'c6453698-cf56-38c1-96d2-90ccdd985228',
        });
      }
    } catch {
      setConnected(false);
    }
  }, [monitorUrl]);

  useEffect(() => {
    fetchMonitorStatus();
    const timer = setInterval(fetchMonitorStatus, 4000);
    return () => clearInterval(timer);
  }, [fetchMonitorStatus]);

  // Kết nối WebSocket thời gian thực với Selenium Demo Monitor (:3999/ws) để đồng bộ hai chiều với cả 6 cửa sổ Chrome
  useEffect(() => {
    let disposed = false;
    let reconnectTimer: number | null = null;
    let pingTimer: number | null = null;
    const wsUrl = monitorUrl.replace(/^http/i, 'ws') + '/ws';

    const connect = () => {
      if (disposed) return;
      try {
        const ws = new WebSocket(wsUrl);
        wsRef.current = ws;
        ws.onopen = () => {
          if (disposed) return;
          setWsConnected(true);
          setConnected(true);
          try {
            ws.send(JSON.stringify({ type: 'hello', window_role: 'Monitor' }));
          } catch {
            // ignore
          }
          if (pingTimer) window.clearInterval(pingTimer);
          pingTimer = window.setInterval(() => {
            if (ws.readyState === WebSocket.OPEN) {
              try {
                ws.send(JSON.stringify({ type: 'ping' }));
              } catch {
                // ignore
              }
            }
          }, 15000);
        };
        ws.onmessage = (ev) => {
          if (disposed) return;
          try {
            const msg = JSON.parse(ev.data);
            if (msg?.type === 'state') {
              if (typeof msg.connected_clients === 'number') {
                setWsClientsCount(msg.connected_clients);
              }
              if (Array.isArray(msg.done_actions)) {
                setDoneActions((prev) => {
                  const next = { ...prev };
                  msg.done_actions.forEach((aid: string) => {
                    next[aid] = true;
                  });
                  return next;
                });
              }
              if (msg.current?.step_code) {
                const matchedIdx = DEMO_STEPS.findIndex((s) => s.code === msg.current.step_code);
                if (matchedIdx >= 0) {
                  setActiveStepIndex(matchedIdx);
                }
              }
              if (msg.roles) {
                setStatus((prev) =>
                  prev
                    ? {
                        ...prev,
                        window_mode: msg.window_mode ?? prev.window_mode,
                        roles: Object.fromEntries(
                          Object.entries(msg.roles).map(([rKey, rVal]) => {
                            const typed = rVal as { alive?: boolean; full_name?: string; email?: string };
                            const oldR = prev.roles?.[rKey];
                            return [
                              rKey,
                              {
                                alive: Boolean(typed.alive),
                                email: typed.email || oldR?.email || '',
                                full_name: typed.full_name || oldR?.full_name || rKey,
                                badge_color: oldR?.badge_color || '#ea6c3b',
                                current_url: oldR?.current_url || '',
                              },
                            ];
                          })
                        ),
                      }
                    : prev
                );
              }
            }
          } catch {
            // ignore malformed frames
          }
        };
        ws.onclose = () => {
          setWsConnected(false);
          if (pingTimer) {
            window.clearInterval(pingTimer);
            pingTimer = null;
          }
          if (!disposed) {
            reconnectTimer = window.setTimeout(connect, 1500);
          }
        };
        ws.onerror = () => {
          try {
            ws.close();
          } catch {
            // ignore
          }
        };
      } catch {
        if (!disposed) {
          reconnectTimer = window.setTimeout(connect, 2000);
        }
      }
    };

    connect();
    return () => {
      disposed = true;
      if (reconnectTimer) window.clearTimeout(reconnectTimer);
      if (pingTimer) window.clearInterval(pingTimer);
      if (wsRef.current) {
        try {
          wsRef.current.close();
        } catch {
          // ignore
        }
        wsRef.current = null;
      }
    };
  }, [monitorUrl]);

  useEffect(() => {
    activePillRef.current?.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
  }, [activeStepIndex]);

  const currentStep = DEMO_STEPS[activeStepIndex];
  const prevStep = activeStepIndex > 0 ? DEMO_STEPS[activeStepIndex - 1] : null;
  const roleChangedFromPrev = prevStep !== null && prevStep.role !== currentStep.role;

  // Tìm thao tác tiếp theo chưa chạy trong bước hiện tại
  const nextPendingAction = currentStep.actions.find((a) => !doneActions[a.id]) ?? null;
  const completedStepsCount = DEMO_STEPS.filter((step) =>
    step.actions.every((a) => Boolean(doneActions[a.id]))
  ).length;

  const triggerStepAction = useCallback(
    async (actionId: string) => {
      if (busyAction !== null) return;
      const actionDef = DEMO_STEPS.flatMap((s) => s.actions).find((a) => a.id === actionId);
      if (actionDef?.localOnly) {
        setDoneActions((prev) => ({ ...prev, [actionId]: !prev[actionId] }));
        return;
      }
      setBusyAction(actionId);
      try {
        const res = await fetch(`${monitorUrl}/api/step-action`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            action_id: actionId,
            payload: customTexts,
          }),
        });
        const data = await res.json();
        if (data.ok) {
          setDoneActions((prev) => ({ ...prev, [actionId]: true }));
          showToast(data.message || `Đã thực thi ${actionId}.`);
        } else {
          showToast(data.error || `Không thể thực thi ${actionId}.`, true);
        }
        await fetchMonitorStatus();
      } catch {
        showToast(
          'Chưa kết nối được với Selenium Demo Monitor ở cổng 3999. Hãy chạy: python brandhub-docs-portal/scripts/demo/selenium_demo_monitor.py',
          true
        );
      } finally {
        setBusyAction(null);
      }
    },
    [busyAction, customTexts, fetchMonitorStatus, monitorUrl, showToast]
  );

  // Nút dẫn dắt thông minh 1 chạm (Phím Space): Chạy thao tác kế tiếp trong bước, nếu xong hết thì sang bước sau
  const handleSmartAdvance = useCallback(() => {
    if (busyAction !== null) return;
    if (nextPendingAction) {
      triggerStepAction(nextPendingAction.id);
    } else if (activeStepIndex < DEMO_STEPS.length - 1) {
      selectStepWithSync((i) => Math.min(DEMO_STEPS.length - 1, i + 1));
    }
  }, [activeStepIndex, busyAction, nextPendingAction, selectStepWithSync, triggerStepAction]);

  const handleLoginSingleRole = useCallback(
    async (role: string) => {
      if (busyAction !== null) return;
      setBusyAction(`LOGIN_${role}`);
      try {
        const res = await fetch(`${monitorUrl}/api/login-role`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ role, step_label: `Chuyển nhanh sang ${role}` }),
        });
        const data = await res.json();
        if (data.ok) {
          showToast(`Đã đưa cửa sổ ${role} (${data.full_name}) lên trước màn hình.`);
        } else {
          showToast(data.error || `Lỗi khi mở cửa sổ ${role}.`, true);
        }
        await fetchMonitorStatus();
      } catch {
        showToast('Không kết nối được tới máy chủ Selenium (cổng 3999).', true);
      } finally {
        setBusyAction(null);
      }
    },
    [busyAction, fetchMonitorStatus, monitorUrl, showToast]
  );

  // Xử lý sự cố 2: Hủy kẹt khẩn cấp (Phím Esc)
  const handleCancelBusy = useCallback(() => {
    if (busyAction !== null) {
      setBusyAction(null);
      showToast('Đã hủy trạng thái chờ khẩn cấp. Bạn có thể tiếp tục điều khiển.');
    }
  }, [busyAction, showToast]);

  // Hỗ trợ phím tắt rảnh tay trên sân khấu & bút trình chiếu (PageUp / PageDown / Space / 1-4 / Mũi tên)
  useEffect(() => {
    const onKeyDown = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement | null;
      if (
        target &&
        (target.tagName === 'INPUT' ||
          target.tagName === 'TEXTAREA' ||
          target.tagName === 'SELECT' ||
          target.isContentEditable)
      ) {
        return;
      }
      if (showResetConfirm || showCleanConfirm || showGuideModal) return;

      if (e.key === 'Escape') {
        if (busyAction !== null) {
          e.preventDefault();
          handleCancelBusy();
          return;
        }
      }
      if (e.code === 'Space') {
        e.preventDefault();
        handleSmartAdvance();
        return;
      }
      if (e.key === 'ArrowRight' || e.key === 'PageDown') {
        e.preventDefault();
        selectStepWithSync((i) => Math.min(DEMO_STEPS.length - 1, i + 1));
        return;
      }
      if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        e.preventDefault();
        selectStepWithSync((i) => Math.max(0, i - 1));
        return;
      }
      if (['1', '2', '3', '4'].includes(e.key)) {
        const idx = Number(e.key) - 1;
        const act = currentStep.actions[idx];
        if (act) {
          e.preventDefault();
          triggerStepAction(act.id);
        }
        return;
      }
      if (e.key === 'r' || e.key === 'R') {
        e.preventDefault();
        handleLoginSingleRole(currentStep.role);
      }
    };
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [
    busyAction,
    currentStep,
    handleLoginSingleRole,
    handleSmartAdvance,
    handleCancelBusy,
    selectStepWithSync,
    showResetConfirm,
    showCleanConfirm,
    showGuideModal,
    triggerStepAction,
  ]);

  const handleCopy = (text: string, key: string) => {
    navigator.clipboard.writeText(text);
    setCopiedKey(key);
    showToast('Đã sao chép nội dung vào bộ nhớ tạm.');
    setTimeout(() => setCopiedKey(null), 1800);
  };

  const handleLoginAll = async () => {
    setBusyAction('LOGIN_ALL');
    try {
      const res = await fetch(`${monitorUrl}/api/login-all`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      });
      const data = await res.json();
      if (data.ok) {
        setDoneActions((prev) => ({ ...prev, B0_OPEN_5_CHROME: true }));
        showToast('Đã mở & đồng bộ WebSocket đủ 6 cửa sổ Chrome (Guest, Owner, Manager, Creator, Client, Admin)!');
      } else {
        showToast(data.error || 'Có lỗi khi mở 6 cửa sổ vai trò.', true);
      }
      await fetchMonitorStatus();
    } catch {
      showToast('Không kết nối được tới máy chủ Selenium (cổng 3999).', true);
    } finally {
      setBusyAction(null);
    }
  };

  const handleArrangeWindows = async (mode: 'split' | 'maximize' = 'split') => {
    setBusyAction(`ARRANGE_${mode}`);
    try {
      const res = await fetch(`${monitorUrl}/api/arrange-windows`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mode }),
      });
      const data = await res.json();
      if (data.ok) {
        showToast(data.message);
      } else {
        showToast(data.error || 'Không thể sắp xếp cửa sổ Chrome.', true);
      }
      await fetchMonitorStatus();
    } catch {
      showToast('Không kết nối được tới máy chủ Selenium (cổng 3999).', true);
    } finally {
      setBusyAction(null);
    }
  };

  const handleResetDatabase = async () => {
    setShowResetConfirm(false);
    setBusyAction('RESET_DB');
    try {
      const res = await fetch(`${monitorUrl}/api/reset-data`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      });
      const data = await res.json();
      if (data.ok) {
        setDoneActions((prev) => ({
          ...Object.fromEntries(Object.entries(prev).filter(([k]) => k.startsWith('B0_'))),
          B0_RESTORE_DB: true,
        }));
        setActiveStepIndex(0);
        showToast(data.message || 'Đã khôi phục dữ liệu PostgreSQL, MongoDB & Redis về trạng thái chuẩn B1.');
      } else {
        showToast(data.error || 'Lỗi khi nạp lại dữ liệu mẫu.', true);
      }
    } catch {
      showToast('Không kết nối được tới máy chủ Selenium (cổng 3999).', true);
    } finally {
      setBusyAction(null);
    }
  };

  const handleCleanDatabase = async () => {
    setShowCleanConfirm(false);
    setBusyAction('CLEAN_DB');
    try {
      const res = await fetch(`${monitorUrl}/api/clean-data`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      });
      const data = await res.json();
      if (data.ok) {
        setDoneActions({});
        setActiveStepIndex(0);
        showToast(
          data.message ||
            'Đã xóa sạch toàn bộ dữ liệu mẫu và các bản ghi phát sinh sau buổi demo.'
        );
      } else {
        showToast(data.error || 'Lỗi khi xóa dữ liệu demo.', true);
      }
    } catch {
      showToast('Không kết nối được tới máy chủ Selenium (cổng 3999).', true);
    } finally {
      setBusyAction(null);
    }
  };

  const resolvedRoute = currentStep.routeTemplate
    .replace('{agency_id}', configIds.agency_id)
    .replace('{workspace_id}', configIds.workspace_id)
    .replace('{campaign_id}', configIds.campaign_id)
    .replace('{task_id}', configIds.task_id);

  const formatReadableDescription = (desc: string): string =>
    desc
      .replace('/agency/{agency_id}', '/agency/se08-digital')
      .replace('/workspaces/{workspace_id}', '/workspaces/dh-fpt-2027')
      .replace('{agency_id}', configIds.agency_id.slice(0, 8))
      .replace('{workspace_id}', configIds.workspace_id.slice(0, 8))
      .replace('{campaign_id}', configIds.campaign_id.slice(0, 8))
      .replace('{task_id}', configIds.task_id.slice(0, 8));

  // Xử lý sự cố 3: Đồng bộ URL Chrome ngay tới bước đang chọn (Teleport Tab)
  const handleSyncCurrentStepRoute = useCallback(async () => {
    if (busyAction !== null) return;
    setBusyAction(`SYNC_${currentStep.code}`);
    try {
      const res = await fetch(`${monitorUrl}/api/login-role`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          role: currentStep.role,
          route: resolvedRoute,
          step_label: `Đồng bộ tới ${currentStep.code}`,
        }),
      });
      const data = await res.json();
      if (data.ok) {
        showToast(`Đã đưa cửa sổ ${currentStep.role} (${data.full_name || currentStep.actorName}) tới ${resolvedRoute}.`);
      } else {
        showToast(data.error || 'Lỗi khi đồng bộ trang Chrome.', true);
      }
      await fetchMonitorStatus();
    } catch {
      showToast('Không kết nối được tới máy chủ Selenium (cổng 3999).', true);
    } finally {
      setBusyAction(null);
    }
  }, [busyAction, currentStep.actorName, currentStep.code, currentStep.role, fetchMonitorStatus, monitorUrl, resolvedRoute, showToast]);

  // Xử lý sự cố 4: Diễn tập lại riêng bước này (Single Step Rollback)
  const handleResetCurrentStep = useCallback(() => {
    setDoneActions((prev) => {
      const next = { ...prev };
      currentStep.actions.forEach((a) => {
        delete next[a.id];
      });
      return next;
    });
    showToast(`Đã làm mới bước ${currentStep.code}. Sẵn sàng chạy lại từ đầu.`);
    handleSyncCurrentStepRoute();
  }, [currentStep.actions, currentStep.code, handleSyncCurrentStepRoute, showToast]);

  // Xử lý sự cố 5: Chế độ Dự phòng thao tác tay 1-chạm (Copy-All-to-Clipboard)
  const handleCopyAllStepData = useCallback(() => {
    if (!currentStep.fields.length) {
      showToast('Bước này không có trường dữ liệu cần nhập.');
      return;
    }
    const lines = currentStep.fields.map((f) => {
      const val = f.copyKey ? customTexts[f.copyKey] ?? f.value : f.value;
      return `[${f.field}] (${f.actionType}):\n${val}`;
    });
    const allText = lines.join('\n\n---\n\n');
    navigator.clipboard.writeText(allText);
    showToast(`Đã chép trọn bộ ${currentStep.fields.length} trường dữ liệu bước ${currentStep.code} vào Clipboard. Bạn có thể dán tay trên Chrome.`);
  }, [currentStep.code, currentStep.fields, customTexts, showToast]);

  const renderFieldsTable = () => (
    <div className="divide-y divide-slate-100 border border-slate-200 rounded-none overflow-hidden">
      {currentStep.fields.map((f, i) => {
        const liveValue = f.copyKey ? customTexts[f.copyKey] ?? f.value : f.value;
        const isCopied = copiedKey === `${currentStep.code}_${i}`;
        return (
          <div key={i} className="p-3.5 bg-white hover:bg-slate-50/50 space-y-2">
            <div className="flex flex-wrap items-center justify-between gap-2">
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold text-slate-900">{f.field}</span>
                <span className="px-2 py-0.5 text-[11px] font-semibold bg-orange-50 text-orange-800 border border-orange-200 rounded-none">
                  {f.actionType}
                </span>
              </div>

              <AstryxButton
                label={isCopied ? 'Đã chép' : 'Sao chép'}
                variant="secondary"
                size="sm"
                icon={
                  isCopied ? (
                    <Check className="size-3 text-[#ea6c3b]" />
                  ) : (
                    <Copy className="size-3 text-slate-600" />
                  )
                }
                onClick={() => handleCopy(liveValue, `${currentStep.code}_${i}`)}
              />
            </div>

            {f.copyKey ? (
              <textarea
                rows={Math.min(5, Math.max(2, Math.ceil(liveValue.length / 110)))}
                value={liveValue}
                onChange={(e) =>
                  setCustomTexts((prev) => ({
                    ...prev,
                    [f.copyKey!]: e.target.value,
                  }))
                }
                className="w-full p-2.5 text-xs text-slate-800 bg-slate-50 border border-slate-200 rounded-none focus:bg-white focus:border-orange-300 focus:outline-none leading-relaxed font-mono"
              />
            ) : (
              <div className="p-2.5 text-xs text-slate-700 bg-slate-50 rounded-none border border-slate-200/80 whitespace-pre-wrap leading-relaxed font-mono">
                {liveValue}
              </div>
            )}

            {f.note && <div className="text-[11px] text-slate-600 font-medium">Lưu ý: {f.note}</div>}
          </div>
        );
      })}
    </div>
  );

  return (
    <div className="demo-monitor-root min-h-dvh bg-slate-50/50 text-slate-900 font-sans">
      {/* Hộp thoại xác nhận trước khi khôi phục DB để tránh bấm nhầm trên sân khấu */}
      <AstryxDialog
        isOpen={showResetConfirm}
        onOpenChange={setShowResetConfirm}
        width={460}
        padding={5}
        aria-label="Xác nhận khôi phục dữ liệu gốc"
      >
        <div className="space-y-4 rounded-none">
          <div className="flex items-start gap-3">
            <div className="size-10 rounded-none bg-orange-50 text-[#ea6c3b] border border-orange-200 flex items-center justify-center shrink-0">
              <Database className="size-5" />
            </div>
            <div className="space-y-1">
              <AstryxHeading level={3} className="text-base font-bold text-slate-900 text-balance">
                Khôi phục toàn bộ dữ liệu mẫu chuẩn Bước B1?
              </AstryxHeading>
              <p className="text-xs text-slate-600 leading-relaxed text-pretty">
                Hệ thống sẽ dọn sạch các thao tác vừa chạy thử và nạp lại trọn bộ kịch bản Chiến dịch Tuyển sinh ĐH FPT 2027 (4 tuần, 20 công việc, 7 gói đa ngành) về trạng thái khởi điểm B1.
              </p>
            </div>
          </div>
          <div className="flex items-center justify-end gap-2 pt-2">
            <AstryxButton
              label="Hủy"
              variant="secondary"
              size="sm"
              onClick={() => setShowResetConfirm(false)}
            />
            <AstryxButton
              label="Đồng ý khôi phục"
              variant="primary"
              size="sm"
              onClick={handleResetDatabase}
            />
          </div>
        </div>
      </AstryxDialog>

      {/* Hộp thoại xác nhận Xóa sạch toàn bộ dữ liệu vừa Demo (--clean) */}
      <AstryxDialog
        isOpen={showCleanConfirm}
        onOpenChange={setShowCleanConfirm}
        width={480}
        padding={5}
        aria-label="Xác nhận xóa sạch dữ liệu demo"
      >
        <div className="space-y-4 rounded-none">
          <div className="flex items-start gap-3">
            <div className="size-10 rounded-none bg-red-50 text-red-600 border border-red-200 flex items-center justify-center shrink-0">
              <Trash2 className="size-5" />
            </div>
            <div className="space-y-1.5">
              <AstryxHeading level={3} className="text-base font-bold text-slate-900 text-balance">
                Xóa sạch toàn bộ dữ liệu mẫu và dữ liệu vừa Demo?
              </AstryxHeading>
              <p className="text-xs text-slate-600 leading-relaxed text-pretty">
                Thao tác này sẽ xóa toàn bộ 7 gói truyền thông mẫu, chiến dịch 4 tuần, 20 công việc, bài viết, nhật ký xuất bản và khảo sát đã tạo. Đưa Agency và Workspace về trạng thái hoàn toàn trống để sẵn sàng cho lần diễn tập hoặc chấm thi tiếp theo.
              </p>
              <div className="p-2.5 rounded-none bg-slate-50 border border-slate-200 text-[11px] text-slate-600 leading-relaxed">
                7 tài khoản đăng nhập vẫn được giữ nguyên. Lần tới khi cần diễn tập lại, bạn chỉ cần nhấn nút <strong>Khôi phục DB</strong> để nạp lại đầy đủ dữ liệu trong 3 giây.
              </div>
            </div>
          </div>
          <div className="flex items-center justify-end gap-2 pt-1">
            <AstryxButton
              label="Hủy"
              variant="secondary"
              size="sm"
              onClick={() => setShowCleanConfirm(false)}
            />
            <AstryxButton
              label="Xóa sạch dữ liệu Demo"
              variant="primary"
              size="sm"
              onClick={handleCleanDatabase}
            />
          </div>
        </div>
      </AstryxDialog>

      {/* Hộp thoại Hướng dẫn sử dụng nhanh ngay trên Bàn điều khiển */}
      <AstryxDialog
        isOpen={showGuideModal}
        onOpenChange={setShowGuideModal}
        width={560}
        padding={5}
        aria-label="Hướng dẫn sử dụng Bàn điều khiển thuyết trình"
      >
        <div className="space-y-4 rounded-none">
          <div className="flex items-start gap-3">
            <div className="size-10 rounded-none bg-orange-50 text-[#ea6c3b] border border-orange-200 flex items-center justify-center shrink-0">
              <HelpCircle className="size-5" />
            </div>
            <div className="space-y-1">
              <AstryxHeading level={3} className="text-base font-bold text-slate-900">
                Hướng dẫn sử dụng Bàn điều khiển Thuyết trình (SE08)
              </AstryxHeading>
              <p className="text-xs text-slate-600 leading-relaxed">
                Quy trình vận hành gọn nhẹ giúp nhóm điều phối mượt toàn bộ 15 bước bảo vệ trong 20 phút.
              </p>
            </div>
          </div>

          <div className="space-y-2.5 text-xs text-slate-700 leading-relaxed">
            <div className="p-3 rounded-none bg-slate-50 border border-slate-200 space-y-1">
              <div className="font-bold text-slate-900">1. Chuẩn bị 2 phút trước giờ lên sân khấu</div>
              <p>
                Đảm bảo đèn trạng thái hiện <strong>Socket</strong> (:3999). Nhấn <strong>Khôi phục DB</strong> để nạp dữ liệu chuẩn, sau đó nhấn <strong>Mở 6 Vai trò</strong> để tự mở đủ 6 cửa sổ Chrome (Guest, Owner, Manager, Creator, Client, Admin) kèm thanh HUD đồng bộ ở góc trái bên dưới.
              </p>
            </div>

            <div className="p-3 rounded-none bg-slate-50 border border-slate-200 space-y-1">
              <div className="font-bold text-slate-900">2. Chiếu song song Laptop &amp; TV (Thao tác thẳng trên Chrome)</div>
              <p>
                Bấm <strong>Toàn màn hình TV</strong> rồi ẩn Bàn điều khiển. Khi thuyết trình, bấm trực tiếp nút <strong>Tiếp ▶</strong> / <strong>◀ Trước</strong> (hoặc phím <strong>Alt + ←/→</strong>) ngay trên thanh HUD nhỏ góc trái dưới màn hình Chrome — cả 6 cửa sổ Chrome tự đồng bộ tức thì qua WebSocket và tự bật đúng cửa sổ vai trò lên trên cùng.
              </p>
            </div>

            <div className="p-3 rounded-none bg-slate-50 border border-slate-200 space-y-1">
              <div className="font-bold text-slate-900">3. Trả lời Hội đồng (Q&amp;A) &amp; Dọn dữ liệu sau buổi bảo vệ</div>
              <p>
                Nhấn nút <strong>☰</strong> ngay trên thanh HUD góc trái dưới (hoặc mục <strong>Q&amp;A Hội đồng</strong>) để mở nhanh 15 màn hình chuyên sâu và chuyển tức thì qua 6 vai trò. Khi bảo vệ xong, bấm <strong>Xóa dữ liệu Demo</strong> để làm sạch hệ thống.
              </p>
            </div>
          </div>

          <div className="flex items-center justify-end pt-1">
            <AstryxButton
              label="Đã hiểu, bắt đầu ngay"
              variant="primary"
              size="sm"
              onClick={() => setShowGuideModal(false)}
            />
          </div>
        </div>
      </AstryxDialog>

      {/* Thanh thông báo nổi (Toast) */}
      {toastMessage && (
        <div className="fixed bottom-4 right-4 z-50 max-w-md shadow-md rounded-none overflow-hidden border border-slate-200">
          <AstryxBanner
            status={toastMessage.isError ? 'warning' : 'info'}
            title={toastMessage.isError ? 'Thông báo điều khiển' : 'Đã thực thi'}
            description={toastMessage.text}
            isDismissable
            onDismiss={() => setToastMessage(null)}
          />
        </div>
      )}

      {/* Thanh Header chuẩn Minimalist: Màu trắng thanh lịch, điểm cam ấm nhẹ, góc vuông sắc nét */}
      <header className="sticky top-0 z-30 bg-white/95 backdrop-blur-md border-b border-slate-200 shadow-xs">
        <div className="max-w-[1600px] mx-auto px-3 sm:px-4 py-2 flex flex-wrap items-center justify-between gap-2.5">
          {/* Cụm thương hiệu + Nút về Docs */}
          <div className="flex items-center gap-2.5 min-w-0">
            <Link
              to="/"
              title="Quay về cổng tài liệu BrandHub Docs"
              className="inline-flex items-center gap-1 px-2 py-1 rounded-none border border-slate-200 hover:border-orange-200 bg-white hover:bg-slate-50 text-slate-700 text-xs font-semibold cursor-pointer transition-colors"
            >
              <ArrowLeft className="size-3.5" />
              <span className="hidden sm:inline">Docs</span>
            </Link>

            <div className="flex items-center gap-2 min-w-0">
              <div className="size-8 rounded-none bg-[#ea6c3b] flex items-center justify-center text-white font-extrabold text-sm shadow-xs">
                BH
              </div>
              <div className="flex items-center gap-2 min-w-0">
                <AstryxHeading level={1} className="text-sm sm:text-base font-bold text-slate-900 truncate">
                  Điều Khiển Thuyết Trình SE08
                </AstryxHeading>
                <span className="hidden xl:inline-flex px-2 py-0.5 text-[11px] font-semibold bg-orange-50 text-orange-800 border border-orange-200 rounded-none">
                  ĐH FPT 2027 • 4 Tuần
                </span>
              </div>
            </div>
          </div>

          {/* Cụm Chia màn hình + Đăng nhập 5 vai trò + Khôi phục / Xóa DB */}
          <div className="flex flex-wrap items-center gap-1.5">
            {/* Trạng thái Selenium & WebSocket đồng bộ 6 cửa sổ Chrome */}
            <div
              className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-none bg-white border border-slate-200 text-xs"
              title={
                wsConnected
                  ? `WebSocket :3999/ws đang đồng bộ tức thì (${wsClientsCount} kết nối)`
                  : 'Trạng thái kết nối tới Selenium Demo Monitor :3999'
              }
            >
              <AstryxStatusDot
                variant={connected ? 'accent' : 'neutral'}
                label={connected ? 'Selenium đã kết nối' : 'Selenium chưa bật'}
                isPulsing={connected}
              />
              <span className="text-slate-700 font-medium">
                {connected
                  ? wsConnected
                    ? `Socket · ${wsClientsCount}`
                    : 'Đã kết nối'
                  : 'Chưa bật :3999'}
              </span>
            </div>

            {/* Xử lý sự cố 6: Tùy chọn hiển thị 1 Màn hình (70/30) vs 2 Màn hình (Chiếu ngoài) */}
            <div className="inline-flex items-center border border-slate-200 bg-white">
              <button
                type="button"
                onClick={() => handleArrangeWindows('split')}
                disabled={busyAction !== null}
                title="1 Màn hình laptop: Xếp 6 cửa sổ Chrome gọn bên trái 71%, chừa 29% bên phải cho Bàn điều khiển"
                className={`inline-flex items-center gap-1 px-2.5 py-1.5 rounded-none text-xs font-semibold cursor-pointer transition-colors ${
                  status?.window_mode === 'split'
                    ? 'bg-orange-50 text-orange-950 font-bold'
                    : 'text-slate-700 hover:bg-slate-50'
                }`}
              >
                <Columns2 className="size-3.5 text-slate-600" />
                <span>Chia màn hình (70/30)</span>
              </button>
              <button
                type="button"
                onClick={() => handleArrangeWindows('maximize')}
                disabled={busyAction !== null}
                title="Chiếu song song TV / HDMI: Phóng to toàn màn hình cả 6 cửa sổ Chrome, điều khiển trực tiếp qua thanh HUD góc trái dưới"
                className={`inline-flex items-center gap-1 px-2 py-1.5 rounded-none text-xs font-semibold cursor-pointer transition-colors border-l border-slate-200 ${
                  status?.window_mode === 'maximize'
                    ? 'bg-orange-50 text-orange-950 font-bold'
                    : 'text-slate-700 hover:bg-slate-50'
                }`}
              >
                <Maximize2 className="size-3.5 text-slate-600" />
                <span className="hidden xl:inline">Toàn màn hình TV</span>
              </button>
            </div>

            {/* Nút Mở & Đăng nhập 6 Vai trò: Cam ấm dịu, góc vuông */}
            <button
              type="button"
              disabled={busyAction !== null}
              onClick={handleLoginAll}
              title="Mở 6 cửa sổ Chrome kèm thanh HUD Socket góc trái dưới cho Guest, Owner, Manager, Creator, Client, Admin"
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-none bg-[#ea6c3b] hover:bg-[#d95d2c] text-white text-xs font-semibold border border-[#ea6c3b] cursor-pointer shadow-xs transition-colors disabled:opacity-50"
            >
              {busyAction === 'LOGIN_ALL' ? (
                <RefreshCw className="size-3.5 animate-spin" />
              ) : (
                <Users className="size-3.5" />
              )}
              <span>Mở 6 Vai trò</span>
            </button>

            {/* Khôi phục DB */}
            <button
              type="button"
              disabled={busyAction !== null}
              onClick={() => setShowResetConfirm(true)}
              title="Nạp lại dữ liệu mẫu chuẩn Bước B1 (Agency, 7 Gói truyền thông, Chiến dịch 4 tuần)"
              className="inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-none bg-white hover:bg-slate-50 border border-slate-200 text-xs font-semibold text-slate-700 cursor-pointer transition-colors disabled:opacity-50"
            >
              {busyAction === 'RESET_DB' ? (
                <RefreshCw className="size-3.5 animate-spin" />
              ) : (
                <Database className="size-3.5 text-slate-600" />
              )}
              <span>Khôi phục DB</span>
            </button>

            {/* Xóa dữ liệu Demo */}
            <button
              type="button"
              disabled={busyAction !== null}
              onClick={() => setShowCleanConfirm(true)}
              title="Xóa sạch toàn bộ dữ liệu mẫu và mọi bản ghi phát sinh lúc demo"
              className="inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-none bg-white hover:bg-red-50 border border-slate-200 hover:border-red-300 text-xs font-semibold text-slate-700 hover:text-red-700 cursor-pointer transition-colors disabled:opacity-50"
            >
              {busyAction === 'CLEAN_DB' ? (
                <RefreshCw className="size-3.5 animate-spin" />
              ) : (
                <Trash2 className="size-3.5 text-slate-600 hover:text-red-600" />
              )}
              <span>Xóa dữ liệu Demo</span>
            </button>

            {/* Hướng dẫn */}
            <button
              type="button"
              title="Xem hướng dẫn sử dụng nhanh"
              aria-label="Hướng dẫn sử dụng"
              onClick={() => setShowGuideModal(true)}
              className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-none border border-slate-200 hover:border-orange-200 bg-white hover:bg-slate-50 text-slate-700 text-xs font-semibold cursor-pointer transition-colors"
            >
              <HelpCircle className="size-3.5 text-slate-600" />
              <span className="hidden lg:inline">Hướng dẫn</span>
            </button>
          </div>
        </div>

        {/* Dải 5 Vai trò: Nền sáng thanh lịch, góc vuông sắc nét, không chói gắt */}
        <div className="bg-slate-50 border-t border-slate-200">
          <div className="max-w-[1600px] mx-auto px-3 sm:px-4 py-1.5 flex items-center justify-between gap-2 overflow-x-auto no-scrollbar">
            <div className="flex items-center gap-1.5 min-w-0">
              <span className="text-[11px] font-bold text-slate-500 shrink-0 hidden sm:inline mr-1">
                Cửa sổ Chrome:
              </span>
              {CANONICAL_ROLES.map((item) => {
                const roleStat = status?.roles?.[item.role];
                const isCurrentStepRole = currentStep.role === item.role;
                return (
                  <button
                    key={item.role}
                    type="button"
                    disabled={busyAction !== null}
                    onClick={() => handleLoginSingleRole(item.role)}
                    title={`${item.role}: ${item.fullName} (${item.email}) - Bấm để đưa cửa sổ lên trước`}
                    className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-none border text-xs cursor-pointer transition-colors ${
                      isCurrentStepRole
                        ? 'bg-orange-50 text-orange-950 border-orange-400 font-bold shadow-xs'
                        : 'bg-white text-slate-700 border-slate-200 hover:border-orange-200 hover:bg-slate-50'
                    }`}
                  >
                    <span
                      className={`size-2 rounded-none shrink-0 ${
                        roleStat?.alive
                          ? isCurrentStepRole
                            ? 'bg-[#ea6c3b]'
                            : 'bg-amber-500'
                          : 'bg-slate-300'
                      }`}
                    />
                    <span className="font-bold">{item.role}</span>
                    <span className={isCurrentStepRole ? 'text-orange-800' : 'text-slate-500'}>
                      · {item.shortLabel}
                    </span>
                    {!roleStat?.alive && (
                      <span className="text-red-500 font-semibold text-[10px] ml-0.5">
                        (Mở lại)
                      </span>
                    )}
                  </button>
                );
              })}
            </div>

            <div className="hidden xl:flex items-center gap-1.5 text-[11px] text-slate-500 shrink-0">
              <span>Phím nhanh:</span>
              <AstryxKbd keys="space" />
              <span>chạy tiếp</span>
              <AstryxKbd keys="left" />
              <AstryxKbd keys="right" />
              <span>đổi bước</span>
              <AstryxKbd keys="1" />
              <span>-</span>
              <AstryxKbd keys="4" />
              <span>nút con</span>
            </div>
          </div>
        </div>

      </header>

      {/* Bố cục chính: Sidebar dọc 15 bước bên trái + nội dung bước hiện tại bên phải */}
      <div className="flex items-start">
        {/* Sidebar dọc B1 -> B14: liệt kê đủ cả quy trình cho Hội đồng theo dõi tổng quan */}
        <nav
          aria-label="Danh sách 15 bước demo"
          className="hidden lg:block w-[280px] shrink-0 self-start sticky top-0 max-h-dvh overflow-y-auto border-r border-slate-200 bg-white"
        >
          <div className="divide-y divide-slate-100">
            {DEMO_STEPS.map((step, idx) => {
              const isSelected = idx === activeStepIndex;
              const isDone = step.actions.every((a) => Boolean(doneActions[a.id]));
              const hasSomeDone = !isDone && step.actions.some((a) => Boolean(doneActions[a.id]));
              return (
                <button
                  key={step.code}
                  ref={isSelected ? activePillRef : null}
                  type="button"
                  onClick={() => selectStepWithSync(idx)}
                  title={`Bước ${step.stepNumber}: ${step.title} (${step.role})`}
                  className={`w-full flex items-start gap-2.5 px-3.5 py-2.5 text-left cursor-pointer transition-colors border-l-2 ${
                    isSelected
                      ? 'bg-orange-50 border-l-[#ea6c3b]'
                      : hasSomeDone
                      ? 'bg-slate-50 border-l-transparent hover:bg-slate-100'
                      : 'bg-white border-l-transparent hover:bg-slate-50'
                  }`}
                >
                  <span
                    className={`font-mono text-[11px] font-bold shrink-0 mt-0.5 ${
                      isSelected ? 'text-[#ea6c3b]' : isDone ? 'text-blue-600' : 'text-slate-400'
                    }`}
                  >
                    {isDone ? '✓' : step.code}
                  </span>
                  <span className="min-w-0 flex-1">
                    <span
                      className={`block text-xs leading-snug text-pretty ${
                        isSelected ? 'font-bold text-orange-950' : isDone ? 'font-medium text-slate-600' : 'font-medium text-slate-700'
                      }`}
                    >
                      {step.shortTitle}
                    </span>
                    <span className="block text-[11px] text-slate-500 mt-0.5">{step.role}</span>
                  </span>
                </button>
              );
            })}
          </div>
        </nav>

        <main className="flex-1 min-w-0 max-w-[1040px] mx-auto px-4 py-4 space-y-4">
        {/* Khu vực Điều khiển Chính của Bước Hiện Tại */}
        <AstryxCard padding={4} className="rounded-none bg-white border border-slate-200 shadow-xs space-y-4">
          {/* Hàng 1: Định danh Bước + Báo đổi vai + Nút Trước/Tiếp */}
          <div className="flex flex-wrap items-start justify-between gap-3">
            <div className="space-y-1.5 min-w-0 flex-1">
              <div className="flex flex-wrap items-center gap-1.5">
                <span className="px-2 py-0.5 text-xs font-bold bg-slate-100 text-slate-800 border border-slate-200 rounded-none">
                  Bước {currentStep.stepNumber}/15 · {currentStep.code}
                </span>
                <span className="px-2 py-0.5 text-xs font-semibold bg-orange-50 text-orange-900 border border-orange-200 rounded-none">
                  {currentStep.role}: {currentStep.actorName}
                </span>
                <span className="px-2 py-0.5 text-xs font-medium bg-slate-50 text-slate-600 border border-slate-200 rounded-none">
                  Khung giờ: {currentStep.timeBudget}
                </span>
                <span className="px-2 py-0.5 text-xs font-medium bg-slate-50 text-slate-600 border border-slate-200 rounded-none">
                  {currentStep.frCode}
                </span>
                {roleChangedFromPrev && (
                  <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-none text-xs font-bold bg-amber-50 text-amber-900 border border-amber-300">
                    Chuyển cửa sổ sang {currentStep.role}
                  </span>
                )}
              </div>

              <AstryxHeading level={2} className="text-lg sm:text-xl font-bold text-slate-900 text-balance">
                {currentStep.title}
              </AstryxHeading>

              <div className="flex flex-wrap items-center gap-2 text-xs text-slate-500">
                <span className="font-medium">Trang đích:</span>
                <a
                  href={`${configIds.app_url}${resolvedRoute}`}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-none bg-slate-50 hover:bg-slate-100 text-slate-700 border border-slate-200 font-mono"
                >
                  <span>{resolvedRoute}</span>
                  <ExternalLink className="size-3 shrink-0 text-slate-500" />
                </a>
                <button
                  type="button"
                  onClick={handleSyncCurrentStepRoute}
                  disabled={busyAction !== null}
                  title="Xử lý sự cố: Đưa ngay cửa sổ Chrome của vai trò này tới đúng trang đích của bước hiện tại"
                  className="inline-flex items-center gap-1 px-2 py-0.5 rounded-none bg-white hover:bg-orange-50 text-slate-700 hover:text-orange-950 border border-slate-200 text-xs font-semibold cursor-pointer transition-colors"
                >
                  <Compass className="size-3 text-[#ea6c3b]" />
                  <span>Đồng bộ Chrome tới bước này</span>
                </button>
              </div>
            </div>

            <div className="flex flex-wrap items-center gap-1.5 shrink-0">
              <button
                type="button"
                onClick={handleResetCurrentStep}
                title="Xử lý sự cố: Xóa dấu tích đã chạy của riêng bước này và điều hướng Chrome về lại trạng thái chuẩn bị để diễn tập lại"
                className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-none bg-white hover:bg-slate-50 border border-slate-200 text-xs font-semibold text-slate-700 cursor-pointer transition-colors"
              >
                <RotateCcw className="size-3 text-slate-600" />
                <span className="hidden sm:inline">Chạy lại bước</span>
              </button>
              <button
                type="button"
                onClick={handleCopyAllStepData}
                title="Xử lý sự cố: Sao chép toàn bộ dữ liệu mẫu của bước này vào Clipboard để dán tay nhanh trên Chrome"
                className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-none bg-white hover:bg-slate-50 border border-slate-200 text-xs font-semibold text-slate-700 cursor-pointer transition-colors"
              >
                <ClipboardCheck className="size-3 text-slate-600" />
                <span className="hidden sm:inline">Chép dữ liệu bước</span>
              </button>
              <AstryxButton
                label="← Trước"
                tooltip="Lùi về bước demo trước đó (phím mũi tên trái)"
                variant="secondary"
                size="sm"
                isDisabled={activeStepIndex === 0}
                onClick={() => selectStepWithSync((i) => Math.max(0, i - 1))}
              />
              <AstryxButton
                label="Tiếp →"
                tooltip="Qua bước demo kế tiếp (phím mũi tên phải)"
                variant="secondary"
                size="sm"
                isDisabled={activeStepIndex === DEMO_STEPS.length - 1}
                onClick={() => selectStepWithSync((i) => Math.min(DEMO_STEPS.length - 1, i + 1))}
              />
            </div>
          </div>

          {/* Hàng 2: NÚT DẪN THUYẾT TRÌNH 1 CHẠM (SPACE) */}
          <div className="p-3 rounded-none bg-slate-50 border border-slate-200 flex flex-wrap items-center justify-between gap-3">
            <div className="min-w-0 flex-1">
              <div className="text-[11px] font-bold uppercase text-slate-600 flex items-center gap-1.5">
                <Sparkles className="size-3.5 text-[#ea6c3b] shrink-0" />
                <span>Điều khiển 1 chạm (nhấn phím Space hoặc bút trình chiếu)</span>
              </div>
              <div className="text-sm font-bold text-slate-900 mt-0.5 truncate">
                {nextPendingAction
                  ? `Sẵn sàng chạy: [${
                      currentStep.actions.findIndex((a) => a.id === nextPendingAction.id) + 1
                    }/${currentStep.actions.length}] ${nextPendingAction.label}`
                  : activeStepIndex < DEMO_STEPS.length - 1
                  ? `Đã chạy đủ thao tác ${currentStep.code}! Nhấn để chuyển sang ${
                      DEMO_STEPS[activeStepIndex + 1].code
                    }: ${DEMO_STEPS[activeStepIndex + 1].shortTitle}`
                  : 'Đã hoàn thành trọn vẹn cả 15 bước thuyết trình!'}
              </div>
            </div>

            <div className="flex items-center gap-2">
              {busyAction !== null && (
                <button
                  type="button"
                  onClick={handleCancelBusy}
                  title="Xử lý sự cố: Hủy ngay lập tức trạng thái chờ nếu thao tác bị treo hoặc lag mạng"
                  className="px-3 py-2 rounded-none bg-red-600 hover:bg-red-700 text-white font-bold text-xs shadow-xs cursor-pointer transition-colors"
                >
                  Hủy kẹt (Esc)
                </button>
              )}
              <button
                type="button"
                disabled={
                  busyAction !== null ||
                  (!nextPendingAction && activeStepIndex === DEMO_STEPS.length - 1)
                }
                onClick={handleSmartAdvance}
                className="inline-flex items-center gap-2.5 px-5 py-2.5 rounded-none bg-[#ea6c3b] hover:bg-[#d95d2c] text-white font-bold text-xs sm:text-sm border border-[#ea6c3b] shadow-xs cursor-pointer transition-colors disabled:opacity-50"
              >
              {busyAction !== null ? (
                <RefreshCw className="size-4 animate-spin" />
              ) : nextPendingAction ? (
                <Play className="size-4" />
              ) : (
                <ArrowRight className="size-4" />
              )}
              <span>
                {nextPendingAction
                  ? `Thực thi ngay (${
                      currentStep.actions.findIndex((a) => a.id === nextPendingAction.id) + 1
                    }/${currentStep.actions.length})`
                  : activeStepIndex < DEMO_STEPS.length - 1
                  ? `Sang bước ${DEMO_STEPS[activeStepIndex + 1].code} →`
                  : 'Đã hoàn tất 15/15'}
              </span>
              <span className="bg-white/20 text-white px-1.5 py-0.5 rounded-none text-[11px] font-mono">
                Space
              </span>
            </button>
          </div>
          </div>

          {/* Hàng 3: Các nút con đánh số rõ [1] [2] [3] [4] kèm trạng thái Đã chạy */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2.5">
            {currentStep.actions.map((act, idx) => {
              const isRunning = busyAction === act.id;
              const isDone = Boolean(doneActions[act.id]);
              const isNextRecommended = nextPendingAction?.id === act.id;
              const numKey = String(idx + 1);

              return (
                <button
                  key={act.id}
                  type="button"
                  onClick={() => triggerStepAction(act.id)}
                  disabled={busyAction !== null}
                  className={`p-3.5 rounded-none border text-left flex items-start gap-3 cursor-pointer transition-colors ${
                    isNextRecommended
                      ? 'bg-orange-50/60 text-slate-900 border-orange-400 hover:bg-orange-50 shadow-xs'
                      : isDone
                      ? 'bg-slate-50 text-slate-600 border-slate-200'
                      : 'bg-white text-slate-900 border-slate-200 hover:border-orange-200 hover:bg-slate-50'
                  }`}
                >
                  <div
                    className={`size-8 rounded-none shrink-0 flex items-center justify-center font-extrabold text-sm ${
                      isNextRecommended
                        ? 'bg-[#ea6c3b] text-white'
                        : isDone
                        ? 'bg-slate-200 text-slate-700'
                        : 'bg-slate-100 text-slate-700 border border-slate-200'
                    }`}
                  >
                    {isRunning ? (
                      <RefreshCw className="size-4 animate-spin" />
                    ) : isDone ? (
                      <CheckCheck className="size-4" />
                    ) : (
                      numKey
                    )}
                  </div>

                  <div className="min-w-0 flex-1">
                    <div className="flex items-start justify-between gap-2.5">
                      <span className="text-xs sm:text-sm font-bold leading-snug text-pretty">
                        {idx + 1}. {act.label}
                      </span>
                      <span
                        className={`px-2 py-0.5 rounded-none text-[10px] font-bold shrink-0 whitespace-nowrap ${
                          isNextRecommended
                            ? 'bg-orange-100 text-orange-900 border border-orange-200'
                            : isDone
                            ? 'bg-slate-200 text-slate-700'
                            : 'bg-slate-100 text-slate-600'
                        }`}
                      >
                        {isNextRecommended ? `Phím ${numKey} · Tiếp theo` : isDone ? 'Đã chạy' : `Phím ${numKey}`}
                      </span>
                    </div>
                    <div
                      className={`text-xs mt-1 leading-relaxed ${
                        isNextRecommended ? 'text-slate-700' : 'text-slate-600'
                      }`}
                    >
                      {formatReadableDescription(act.description)}
                    </div>
                  </div>
                </button>
              );
            })}
          </div>

          {/* Hàng 4: Chỉ dẫn thao tác tay trên Chrome chuẩn Craft Floor (1px border thanh lịch) */}
          <div className="px-3.5 py-2.5 rounded-none bg-slate-50 border border-slate-200 flex items-start gap-2.5">
            <span className="px-1.5 py-0.5 rounded-none text-[10px] font-bold bg-orange-100 text-orange-900 border border-orange-200 shrink-0 mt-0.5 font-mono">
              CHROME CUE
            </span>
            <div className="text-xs sm:text-sm text-slate-800 leading-relaxed text-pretty">
              <strong className="text-slate-900 font-bold">Thao tác kết hợp: </strong>
              <span className="text-slate-700">{currentStep.manualBrowserCue}</span>
            </div>
          </div>

          <AstryxDivider variant="subtle" />

          {/* Hàng 5: Máy nhắc chữ sân khấu (Teleprompter) sắc nét, dễ đọc */}
          <div className="space-y-3">
            <div className="flex flex-wrap items-center justify-between gap-2">
              <div className="text-xs font-bold uppercase text-slate-700 flex items-center gap-1.5">
                <span>Ý chính trình bày trước Hội đồng ({currentStep.code})</span>
              </div>
              {Object.keys(doneActions).length > 0 && (
                <button
                  type="button"
                  title="Bỏ hết dấu tích 'đã chạy' trên các thao tác, không ảnh hưởng dữ liệu thật"
                  onClick={() => setDoneActions({})}
                  className="text-xs text-slate-500 hover:text-orange-700 underline cursor-pointer"
                >
                  Xóa dấu tích đã chạy
                </button>
              )}
            </div>

            {/* 3 gạch đầu dòng ngắn gọn để liếc mắt 1 giây nắm ý */}
            <div className="grid grid-cols-1 gap-2">
              {currentStep.talkingPoints.map((pt, i) => (
                <div
                  key={i}
                  className="px-3.5 py-2.5 rounded-none bg-slate-50 border border-slate-200 text-sm leading-relaxed flex items-start gap-2.5"
                >
                  <span className="size-5 rounded-none bg-orange-100 text-orange-900 border border-orange-200 text-xs font-bold shrink-0 mt-0.5 flex items-center justify-center">
                    {i + 1}
                  </span>
                  <span className="text-pretty font-medium text-slate-800">{pt}</span>
                </div>
              ))}
            </div>

            {/* Lời dẫn nguyên văn đầy đủ & Kết quả màn hình */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 pt-1">
              <div className="md:col-span-2 p-3.5 rounded-none bg-white border border-slate-200 space-y-1">
                <div className="text-[11px] font-bold text-slate-500 uppercase">
                  Lời dẫn gợi ý đầy đủ
                </div>
                <p className="text-sm text-slate-700 leading-relaxed text-pretty">
                  {currentStep.presenterScript}
                </p>
              </div>
              <div className="p-3.5 rounded-none bg-slate-50 border border-slate-200 space-y-1">
                <div className="text-[11px] font-bold text-slate-600 uppercase">
                  Kết quả trên màn hình
                </div>
                <p className="text-xs text-slate-600 leading-relaxed text-pretty">
                  {currentStep.expectedOutcome}
                </p>
              </div>
            </div>
          </div>
        </AstryxCard>

        {/* Bảng Dữ liệu Quick-Fill & Copy dự phòng (Thu gọn sẵn) */}
        <AstryxCard padding={4} className="rounded-none bg-white border border-slate-200 shadow-xs">
          <AstryxCollapsible
            defaultIsOpen={false}
            trigger={
              <div className="flex flex-wrap items-center justify-between gap-2 pr-2">
                <span className="text-xs sm:text-sm font-bold text-slate-800">
                  Dữ liệu điền tự động &amp; Sao chép thủ công dự phòng ({currentStep.fields.length} trường)
                </span>
                <span className="px-2 py-0.5 text-[11px] font-medium bg-slate-100 text-slate-600 border border-slate-200 rounded-none">
                  Bấm để mở khi cần sửa tay
                </span>
              </div>
            }
          >
            <div className="pt-3">{renderFieldsTable()}</div>
          </AstryxCollapsible>
        </AstryxCard>

        {/* Ngăn Truy cập nhanh Q&A Hội đồng: Phủ kín 14 màn hình tính năng chuyên sâu */}
        <AstryxCard padding={4} className="rounded-none bg-white border border-slate-200 shadow-xs">
          <AstryxCollapsible
            defaultIsOpen={false}
            trigger={
              <div className="flex flex-wrap items-center justify-between gap-2 pr-2">
                <span className="text-xs sm:text-sm font-bold text-slate-900 flex items-center gap-2">
                  <Sparkles className="size-4 text-[#ea6c3b] shrink-0" />
                  <span>Truy cập nhanh Q&amp;A Hội đồng: 14 Màn hình Chuyên sâu (Event, Workshop, Báo chí, KOL...)</span>
                </span>
                <span className="px-2 py-0.5 text-[11px] font-medium bg-orange-50 text-orange-800 border border-orange-200 rounded-none">
                  1 chạm mở đúng vai trò
                </span>
              </div>
            }
          >
            <div className="pt-3 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
              {QA_QUICK_LINKS.map((item) => (
                <button
                  key={item.id}
                  type="button"
                  disabled={busyAction !== null}
                  title={`${item.label} (vai trò ${item.role}) — bấm để tự mở đúng trang và vai trò`}
                  onClick={() => triggerStepAction(item.id)}
                  className="p-2.5 rounded-none border border-slate-200 bg-white hover:border-orange-300 hover:bg-slate-50 text-left flex items-start justify-between gap-2 cursor-pointer transition-colors"
                >
                  <div className="min-w-0">
                    <div className="text-xs font-bold text-slate-900 truncate">{item.label}</div>
                    <div className="text-[11px] text-slate-600 truncate mt-0.5">{item.desc}</div>
                  </div>
                  <span className="px-1.5 py-0.5 rounded-none bg-orange-50 text-orange-800 border border-orange-200 font-mono text-[10px] font-bold shrink-0">
                    {item.role}
                  </span>
                </button>
              ))}
            </div>
          </AstryxCollapsible>
        </AstryxCard>

        {/* Chân trang thanh lịch */}
        <div className="px-4 py-3 rounded-none bg-slate-50 border border-slate-200 flex flex-wrap items-center justify-between gap-3 text-xs text-slate-600">
          <div className="flex items-center gap-2">
            <span className="font-semibold text-slate-700">Selenium Bridge (:3999)</span>
            <span>•</span>
            <span>Bàn điều khiển thuyết trình tự động BrandHub SE08</span>
          </div>
          <a
            href="http://localhost:3999"
            target="_blank"
            rel="noreferrer"
            title="Mở trực tiếp giao diện Bàn điều khiển HTML tĩnh phục vụ từ cổng 3999 (bản dự phòng)"
            className="font-semibold text-[#ea6c3b] hover:underline inline-flex items-center gap-1"
          >
            <span>Mở bản HTML độc lập (:3999)</span>
            <ExternalLink className="size-3.5" />
          </a>
        </div>
        </main>
      </div>
    </div>
  );
};

export default DemoMonitorPage;
