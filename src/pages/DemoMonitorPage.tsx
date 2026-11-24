import React, { useState, useEffect, useCallback, useRef, useMemo } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import {
  Play,
  RotateCcw,
  Users,
  Copy,
  Check,
  Sparkles,
  ExternalLink,
  RefreshCw,
  Database,
  Columns2,
  Maximize2,
  Compass,
  ClipboardCheck,
  ArrowRight,
  CheckCheck,
  Trash2,
  HelpCircle,
  ArrowLeft,
  BookOpen,
  LayoutGrid,
  ListOrdered,
  PlusSquare,
  Sun,
  Moon,
  Clock,
  AlertTriangle,
  KeyRound,
} from 'lucide-react';
import { useAppPreferences } from '../context/AppPreferencesContext';
import {
  AstryxBanner,
  AstryxButton,
  AstryxCard,
  AstryxStatusDot,
  AstryxDivider,
  AstryxHeading,
  AstryxCollapsible,
  AstryxDialog,
  AstryxKbd,
} from '../components/astryx';

type CanonicalRoleName = 'Guest' | 'Owner' | 'Manager' | 'Creator' | 'Client' | 'Admin';
type StageMode = 'auto' | 'manual';
type ManualSubView = 'step' | 'sheet' | 'create';

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
  actionType: 'Dán Ctrl+V' | 'Chọn trên UI' | 'Tham chiếu' | 'Bấm nút';
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

interface StepRouteLink {
  label: string;
  role: CanonicalRoleName;
  routeTemplate: string;
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
  role: CanonicalRoleName;
  actorName: string;
  actorEmail: string;
  routeTemplate: string;
  extraRoutes?: StepRouteLink[];
  manualBrowserCue: string;
  manualChecklist: string[];
  trapWarning?: string;
  talkingPoints: string[];
  presenterScript: string;
  expectedOutcome: string;
  fields: FieldGuideItem[];
  actions: SubActionButton[];
}

interface CreateLivePack {
  id: string;
  title: string;
  role: CanonicalRoleName;
  actorName: string;
  routeTemplate: string;
  whenAsked: string;
  steps: string[];
  fields: Array<{
    id: string;
    label: string;
    actionType: 'Dán Ctrl+V' | 'Chọn trên UI';
    value: string;
    note?: string;
  }>;
}

// This page is public; the demo password is typed once on the demo machine.
function getDemoPassword(): string {
  const saved = localStorage.getItem('bh_demo_pwd');
  if (saved) return saved;
  const entered = window.prompt('Nhập mật khẩu tài khoản demo (chỉ lưu trên máy này)') ?? '';
  if (entered) localStorage.setItem('bh_demo_pwd', entered);
  return entered;
}
const DEFAULT_POST_ID = 'd7e00000-0000-4000-8000-000000000401';
const EVENT_TASK_ID = '85a66c1c-b49b-3788-8bc3-a21336649041';
const WORKSHOP_TASK_ID = 'c1176d26-249c-3d32-bbad-f720b3a518a4';
const PRESS_TASK_ID = 'b8585f25-6a26-3a5e-9199-19c2e9fb3f06';
const KOL_TASK_ID = '3f1ae3a9-6518-35df-a596-1013c055e279';
const NEWSLETTER_TASK_ID = 'b6a13469-05c4-3af0-88b1-ba2ca510d18f';
const VIDEO_TASK_ID = '31a69211-9cec-30f0-b3f0-4e01ac3315a1';

const CANONICAL_ROLES: Array<{
  role: CanonicalRoleName;
  shortLabel: string;
  fullName: string;
  email: string;
  defaultRoute: string;
  desc: string;
}> = [
  {
    role: 'Guest',
    shortLabel: 'Khách',
    fullName: 'Khách truy cập công khai',
    email: 'Chưa đăng nhập',
    defaultRoute: '/packages/share/goi-tuyen-sinh-dh-fpt-2027',
    desc: 'Trang chủ giới thiệu BrandHub, đường dẫn chào giá Gói truyền thông công khai và biểu mẫu khảo sát học sinh THPT.',
  },
  {
    role: 'Owner',
    shortLabel: 'Trung',
    fullName: 'Lê Trí Trung',
    email: 'letritrung2605@gmail.com',
    defaultRoute: '/agency/{agency_id}/media-packages',
    desc: 'Giám đốc SE08 Digital Agency: Quản lý 7 gói truyền thông đa ngành, tạo gói mới, gắn gói vào Workspace và thanh toán SePay (VietQR).',
  },
  {
    role: 'Manager',
    shortLabel: 'Lộc',
    fullName: 'Nguyễn Thành Lộc',
    email: 'nguyenthanhloc20092004@gmail.com',
    defaultRoute: '/workspaces/{workspace_id}/campaigns',
    desc: 'Quản lý chiến dịch SE08: Điều phối Chiến dịch 4 tuần (Brief, 19 hạng mục, 6 đối tác), phân 20 công việc và duyệt nội bộ.',
  },
  {
    role: 'Creator',
    shortLabel: 'Phước',
    fullName: 'Nguyễn Chơn Phước',
    email: 'chontem123@gmail.com',
    defaultRoute: '/workspaces/{workspace_id}/tasks',
    desc: 'Chuyên viên nội dung SE08 (phối hợp Nguyễn Minh Tuấn & Hà Văn Ân): Gọi Gemini AI soạn bài trên /editor, kiểm duyệt và xuất bản 4 nền tảng.',
  },
  {
    role: 'Client',
    shortLabel: 'ĐH FPT',
    fullName: 'Ban Tuyển sinh Đại học FPT',
    email: 'winhtuan@gmail.com',
    defaultRoute: '/workspaces/{workspace_id}/task-approvals?task={task_id}',
    desc: 'Khách hàng Trường Đại học FPT: Nghiệm thu đầu ra OUTPUT, yêu cầu bổ sung 3 mức Học bổng 2027 cùng kỳ OJT và duyệt xuất bản.',
  },
  {
    role: 'Admin',
    shortLabel: 'Admin',
    fullName: 'Quản trị viên BrandHub',
    email: 'admin@brandhub.com',
    defaultRoute: '/admin?view=revenue',
    desc: 'Quản trị nền tảng BrandHub: Giám sát doanh thu gói SaaS, cấu hình bảng giá AI Credit và xử lý Hàng đợi kiểm duyệt (FR 3.10.4).',
  },
];

export const DEFAULT_DEMO_TEXTS: Record<string, string> = {
  pkg_name: 'Gói Tuyển sinh Thạc sĩ FPT 2027',
  pkg_budget: '85000000',
  pkg_weeks: '4',
  pkg_desc:
    'Chiến dịch 4 tuần tuyển sinh chương trình Thạc sĩ FPT 2027: bài đăng mạng xã hội, Reels, Workshop online, PR báo điện tử và bản tin Email.',
  pkg_items_guide:
    'Bài đăng mạng xã hội: 12 · Bài báo điện tử: 2 · Workshop: 2 · Video ngắn: 4 · Email/Bản tin: 2',
  out_of_scope_title:
    '[Tuần 3 - Phát sinh] Tổng hợp lịch xe đưa đón học sinh THPT dự Ngày hội FPTU Open Day 2027',
  out_of_scope_desc:
    'Bài thông báo chi tiết 08 điểm đón xe buýt miễn phí dành cho học sinh lớp 12 và phụ huynh tham gia trải nghiệm phòng Lab Thiết kế Vi mạch bán dẫn, thư viện xanh và tư vấn Học bổng Nguyễn Văn Đạo năm 2027.',
  out_of_scope_criteria:
    'Ghi rõ khung giờ đón tại từng trường THPT, đầu mối sinh viên tình nguyện phụ trách mỗi tuyến xe và đính kèm đường dẫn đăng ký https://tuyensinh.fpt.edu.vn.',
  subtask_desc:
    'Biên soạn nội dung bài đăng tổng hợp điểm nhấn chuỗi Workshop phổ biến tiện ích học đường ĐH FPT tại các trường THPT và thông báo mở cổng xét Học bổng Nguyễn Văn Đạo năm 2027 cho khóa K23.',
  subtask_criteria:
    'Nêu rõ trải nghiệm kính VR và Robotics tại buổi Workshop, 3 mức học bổng 50%, 70%, 100% học phí, lộ trình thực tập doanh nghiệp OJT từ học kỳ 6 và đường dẫn https://tuyensinh.fpt.edu.vn.',
  ai_topic:
    'Tổng hợp điểm nhấn chuỗi Workshop trải nghiệm tiện ích học đường Đại học FPT dành cho học sinh THPT (đeo kính VR tham quan phòng Lab bán dẫn, điều khiển Robotics, tìm hiểu thư viện xanh, sân Vovinam và 40 CLB) kết hợp thông báo mở đăng ký xét Học bổng Nguyễn Văn Đạo năm 2027 tại 5 cơ sở Hà Nội, Đà Nẵng, Quy Nhơn, TP.HCM, Cần Thơ.',
  violation_sample:
    'Bài đăng kích động kỳ thị, thù ghét vùng miền, kêu gọi đánh đập đối thủ và dẫn dụ học sinh tham gia hội nhóm lừa đảo đa cấp trái phép, cá độ trực tuyến.',
  caption_v1_clean:
    'TỪ SÂN TRƯỜNG THPT ĐẾN PHÒNG LAB CÔNG NGHỆ CAO: MỞ ĐĂNG KÝ XÉT HỌC BỔNG ĐẠI HỌC FPT 2027\n\nSau chuỗi Workshop phổ biến tiện ích học đường sôi nổi tại các trường THPT, hàng trăm bạn học sinh lớp 12 đã trực tiếp đeo kính VR khám phá khuôn viên 5 cơ sở, điều khiển cánh tay Robotics và trò chuyện cùng giảng viên ngành Thiết kế Vi mạch bán dẫn, Trí tuệ nhân tạo (AI).\n\nHệ sinh thái học tập thực tiễn đang chờ đón tân sinh viên khóa K23 tại Trường Đại học FPT:\n- Môi trường học tập hiện đại tại Hà Nội, Đà Nẵng, Quy Nhơn, TP.HCM và Cần Thơ với thư viện xanh, ký túc xá tiện nghi, sân Vovinam và hơn 40 CLB sinh viên.\n- Giáo trình chuẩn quốc tế, chú trọng tiếng Anh và kỹ năng làm việc trong dự án công nghệ thực tế.\n- Cổng nhận hồ sơ đăng ký xét Học bổng Nguyễn Văn Đạo đợt 1 năm 2027 đã chính thức mở.\n\nĐăng ký tư vấn và nộp hồ sơ trực tuyến tại: https://tuyensinh.fpt.edu.vn',
  hashtags_line:
    '#DaiHocFPT #TuyenSinhFPTU2027 #WorkshopTHPT2027 #HocBongNguyenVanDao #ViMachBanDan #FPTUniversity',
  client_reject_note:
    'Nội dung bản thảo v1 đã truyền tải rất tốt không khí thực tế của chuỗi Workshop tại các trường THPT. Tuy nhiên, Ban Tuyển sinh đề nghị bổ sung rõ 3 mức Học bổng Nguyễn Văn Đạo năm 2027 cụ thể (50%, 70% và 100% học phí toàn khóa) cùng thông tin học kỳ thực tập doanh nghiệp (On-the-Job Training - OJT) từ học kỳ 6 tại FPT Software và FPT Smart Cloud để phụ huynh và học sinh lớp 12 nắm đầy đủ quyền lợi trước khi duyệt xuất bản.',
  caption_v2_addition:
    '\n\nQuyền lợi học bổng và lộ trình thực tập doanh nghiệp dành cho khóa K23 (2027):\n- Chương trình Học bổng Nguyễn Văn Đạo năm 2027: Trao tặng các mức 50%, 70% và 100% học phí toàn khóa học cho học sinh THPT có thành tích học tập và năng lực nổi trội.\n- Học kỳ doanh nghiệp (On-the-Job Training - OJT): 100% sinh viên tham gia làm việc thực tế từ học kỳ 6 tại FPT Software, FPT Smart Cloud và mạng lưới doanh nghiệp đối tác trong và ngoài nước.',
  caption_v2_full:
    '【TỪ SÂN TRƯỜNG THPT ĐẾN PHÒNG LAB CÔNG NGHỆ CAO: MỞ ĐĂNG KÝ XÉT HỌC BỔNG ĐẠI HỌC FPT 2027】\n\nSau chuỗi Workshop phổ biến tiện ích học đường sôi nổi tại các trường THPT, hàng trăm bạn học sinh lớp 12 đã trực tiếp đeo kính VR khám phá khuôn viên 5 cơ sở, điều khiển cánh tay Robotics và trò chuyện cùng giảng viên ngành Thiết kế Vi mạch bán dẫn, Trí tuệ nhân tạo (AI).\n\nHệ sinh thái học tập thực tiễn đang chờ đón tân sinh viên khóa K23 tại Trường Đại học FPT:\n- Môi trường học tập hiện đại tại Hà Nội, Đà Nẵng, Quy Nhơn, TP.HCM và Cần Thơ với thư viện xanh, ký túc xá tiện nghi, sân Vovinam và hơn 40 CLB sinh viên.\n- Giáo trình chuẩn quốc tế, chú trọng tiếng Anh và kỹ năng làm việc trong dự án công nghệ thực tế.\n- Cổng nhận hồ sơ đăng ký xét Học bổng Nguyễn Văn Đạo đợt 1 năm 2027 đã chính thức mở.\n\nQuyền lợi học bổng và lộ trình thực tập doanh nghiệp dành cho khóa K23 (2027):\n- Chương trình Học bổng Nguyễn Văn Đạo năm 2027: Trao tặng các mức 50%, 70% và 100% học phí toàn khóa học cho học sinh THPT có thành tích học tập và năng lực nổi trội.\n- Học kỳ doanh nghiệp (On-the-Job Training - OJT): 100% sinh viên tham gia làm việc thực tế từ học kỳ 6 tại FPT Software, FPT Smart Cloud và mạng lưới doanh nghiệp đối tác trong và ngoài nước.\n\nĐăng ký tư vấn và nộp hồ sơ trực tuyến tại: https://tuyensinh.fpt.edu.vn',
};

const CREATE_LIVE_PACKS: CreateLivePack[] = [
  {
    id: 'pack_campaign',
    title: '1. Tạo Chiến dịch Truyền thông Mới (CampaignForm)',
    role: 'Manager',
    actorName: 'Nguyễn Thành Lộc',
    routeTemplate: '/workspaces/{workspace_id}/campaigns',
    whenAsked: 'Khi Hội đồng yêu cầu tạo mới một Chiến dịch truyền thông hoặc chỉnh sửa kế hoạch chiến dịch ngay tại chỗ.',
    steps: [
      'Trên cửa sổ Manager, mở trang Chiến dịch (/campaigns) và nhấn nút Tạo chiến dịch / Chỉnh sửa kế hoạch.',
      'Dán Tên chiến dịch, chọn Ngày bắt đầu (01/06/2027) và Ngày kết thúc (28/06/2027).',
      'Dán Chiến lược tổng thể (Strategy) vào khung bên phải, thêm hạng mục công việc rồi nhấn Lưu.',
    ],
    fields: [
      {
        id: 'new_camp_name',
        label: 'Tên chiến dịch (Campaign Name)',
        actionType: 'Dán Ctrl+V',
        value: 'Chiến dịch Tuyển sinh Đợt 2 ĐH FPT 2027: Trải nghiệm Lab Bán dẫn & Ngày hội Open Day',
      },
      {
        id: 'new_camp_strategy',
        label: 'Chiến lược tổng thể (Campaign Strategy)',
        actionType: 'Dán Ctrl+V',
        value:
          'Triển khai truyền thông đa kênh 4 tuần trên Facebook, Instagram, TikTok và Threads tập trung vào 3 trụ cột: (1) Trải nghiệm thực tế phòng Lab Vi mạch bán dẫn & AI tại 5 cơ sở; (2) Chính sách Học bổng Nguyễn Văn Đạo 50%-70%-100%; (3) Kỳ thực tập doanh nghiệp OJT từ học kỳ 6 tại FPT Software.',
      },
      {
        id: 'new_camp_workitem',
        label: 'Tên hạng mục công việc mẫu trong Chiến dịch',
        actionType: 'Dán Ctrl+V',
        value: '[Đợt 2 - Tuần 1] Bài công bố lịch trải nghiệm phòng Lab Bán dẫn & Tư vấn học bổng K23',
      },
    ],
  },
  {
    id: 'pack_task',
    title: '2. Tạo Nhanh Công việc & Subtask Phát sinh (QuickCreateTaskDialog)',
    role: 'Manager',
    actorName: 'Nguyễn Thành Lộc',
    routeTemplate: '/workspaces/{workspace_id}/tasks',
    whenAsked: 'Khi Hội đồng yêu cầu tạo mới 1 Task độc lập trên Kanban hoặc thêm công việc phát sinh ngoài gói.',
    steps: [
      'Trên cửa sổ Manager tại /tasks, bấm nút "+ Tạo công việc" (hoặc "Thêm công việc phát sinh" ở Bước 2 Chiến dịch).',
      'Chọn loại tác vụ "Bài đăng (POST)", mức ưu tiên "Cao (HIGH)", tích chọn 4 nền tảng Facebook, Instagram, TikTok, Threads.',
      'Dán Tiêu đề, Mô tả chi tiết rồi nhấn "Tạo & Mở trình soạn thảo".',
    ],
    fields: [
      {
        id: 'new_task_title',
        label: 'Tiêu đề công việc (Task Title)',
        actionType: 'Dán Ctrl+V',
        value: '[Tuần 3 - Phát sinh] Tổng hợp lịch xe đưa đón học sinh THPT dự Ngày hội FPTU Open Day 2027',
      },
      {
        id: 'new_task_desc',
        label: 'Mô tả công việc (Description)',
        actionType: 'Dán Ctrl+V',
        value:
          'Thông báo chi tiết 08 điểm đón xe buýt miễn phí dành cho học sinh lớp 12 và phụ huynh tham quan phòng Lab Thiết kế Vi mạch bán dẫn, thư viện xanh và tư vấn Học bổng Nguyễn Văn Đạo năm 2027.',
      },
      {
        id: 'new_task_criteria',
        label: 'Tiêu chí nghiệm thu / Ghi chú Subtask',
        actionType: 'Dán Ctrl+V',
        value:
          'Đảm bảo ghi đủ khung giờ đón tại 08 điểm trường THPT, thông tin đầu mối tình nguyện viên phụ trách và đường dẫn đăng ký https://tuyensinh.fpt.edu.vn.',
      },
    ],
  },
  {
    id: 'pack_survey',
    title: '3. Tạo Biểu mẫu Khảo sát Học sinh Mới (Loại SURVEY)',
    role: 'Creator',
    actorName: 'Nguyễn Chơn Phước',
    routeTemplate: '/workspaces/{workspace_id}/tasks',
    whenAsked: 'Khi Hội đồng yêu cầu tạo thử một biểu mẫu khảo sát mới và lấy đường dẫn công khai cho Guest điền.',
    steps: [
      'Tại trang /tasks, bấm "+ Tạo công việc" -> chọn loại "Khảo sát (SURVEY)" -> dán tên rồi bấm "Tạo & Mở trình soạn thảo".',
      'Trong trình thiết kế khảo sát (/survey), dán Tiêu đề, Mô tả và thêm 2 câu hỏi mẫu bên dưới.',
      'Nhấn Xuất bản / Chia sẻ để mở đường dẫn công khai trên cửa sổ Guest.',
    ],
    fields: [
      {
        id: 'new_survey_title',
        label: 'Tên công việc / Tiêu đề biểu mẫu Khảo sát',
        actionType: 'Dán Ctrl+V',
        value: 'Khảo sát nhu cầu tham quan Lab Vi mạch Bán dẫn & Tư vấn Học bổng ĐH FPT 2027',
      },
      {
        id: 'new_survey_desc',
        label: 'Lời giới thiệu biểu mẫu',
        actionType: 'Dán Ctrl+V',
        value:
          'Phiếu đăng ký và khảo sát nguyện vọng dành cho học sinh lớp 12 tham dự chuỗi trải nghiệm thực tế công nghệ Bán dẫn, AI và xét Học bổng Nguyễn Văn Đạo năm 2027 tại Trường Đại học FPT.',
      },
      {
        id: 'new_survey_q1',
        label: 'Câu hỏi 1 (Trắc nghiệm 1 lựa chọn)',
        actionType: 'Dán Ctrl+V',
        value: 'Bạn quan tâm nhất đến nhóm ngành đào tạo nào tại Trường Đại học FPT năm 2027?',
        note: '4 lựa chọn gợi ý: Thiết kế Vi mạch bán dẫn | Trí tuệ nhân tạo (AI) | Kỹ thuật phần mềm | Quản trị kinh doanh số',
      },
      {
        id: 'new_survey_q2',
        label: 'Câu hỏi 2 (Tự luận ngắn)',
        actionType: 'Dán Ctrl+V',
        value: 'Bạn muốn đặt câu hỏi nào cho giảng viên và sinh viên khóa trên về kỳ thực tập doanh nghiệp OJT học kỳ 6?',
      },
    ],
  },
  {
    id: 'pack_partner',
    title: '4. Thêm Đối tác Báo chí / KOL Mới (PartnerForm)',
    role: 'Owner',
    actorName: 'Lê Trí Trung',
    routeTemplate: '/agency/{agency_id}/collaborators',
    whenAsked: 'Khi Hội đồng yêu cầu thêm mới 1 đối tác bên thứ ba vào Danh bạ Đối tác của Agency.',
    steps: [
      'Trên cửa sổ Owner, mở Danh bạ Đối tác (/agency/.../collaborators) và bấm nút "Thêm đối tác".',
      'Chọn phân loại "Báo điện tử (NEWSPAPER)", sau đó dán lần lượt Tên đơn vị, Người liên hệ, Email, SĐT, Website và Ghi chú.',
      'Nhấn Lưu để hoàn tất.',
    ],
    fields: [
      {
        id: 'new_partner_name',
        label: 'Tên đối tác (Partner Name)',
        actionType: 'Dán Ctrl+V',
        value: 'Chuyên trang Giáo dục - Báo Tuổi Trẻ Online',
      },
      {
        id: 'new_partner_contact',
        label: 'Người liên hệ (Contact Name)',
        actionType: 'Dán Ctrl+V',
        value: 'Nhà báo Trần Minh Hoàng',
      },
      {
        id: 'new_partner_email',
        label: 'Email liên hệ',
        actionType: 'Dán Ctrl+V',
        value: 'giaoduc.hop-tac@tuoitre.com.vn',
      },
      {
        id: 'new_partner_phone',
        label: 'Số điện thoại',
        actionType: 'Dán Ctrl+V',
        value: '0903812689',
      },
      {
        id: 'new_partner_web',
        label: 'Website',
        actionType: 'Dán Ctrl+V',
        value: 'https://tuoitre.vn/giao-duc.htm',
      },
      {
        id: 'new_partner_notes',
        label: 'Ghi chú hợp tác (Notes)',
        actionType: 'Dán Ctrl+V',
        value:
          'Phụ trách đăng tải tuyến bài chuyên sâu về chương trình Học bổng Nguyễn Văn Đạo và mô hình thực tập doanh nghiệp OJT mùa tuyển sinh 2027 (SLA duyệt bài 24h).',
      },
    ],
  },
];

const DEMO_STEPS: DemoStep[] = [
  {
    stepNumber: 0,
    code: 'B0',
    stage: 'Chuẩn bị trước khi thuyết trình',
    stageShort: 'GĐ 0: Chuẩn bị',
    timeBudget: 'Trước 00:00',
    title: 'Checklist sẵn sàng hệ thống & 6 cửa sổ vai trò trước giờ bảo vệ',
    shortTitle: 'Checklist chuẩn bị',
    frCode: '6 Roles',
    role: 'Owner',
    actorName: 'Lê Trí Trung',
    actorEmail: 'letritrung2605@gmail.com',
    routeTemplate: '/agency/{agency_id}/media-packages',
    manualBrowserCue:
      'Nguyễn Thành Lộc chạy open_clean_chrome_roles.bat (mặc định trỏ https://brandhub.id.vn, dự phòng rớt mạng: open_clean_chrome_roles_local.bat) để mở 6 cửa sổ Chrome gốc (0% Selenium) và chạy preload_clipboard_win_v.bat nạp lịch sử Win + V; Lê Trí Trung đứng sân khấu thuyết trình xuyên suốt B1–B12.',
    manualChecklist: [
      'Đảm bảo dữ liệu mẫu ĐH FPT 2027 đã nạp sạch về trạng thái khởi điểm B1 (python prepare_demo_data_template.py --apply, gói Agency Plus = 990.000 VNĐ/tháng).',
      'Mở sẵn 6 cửa sổ Chrome tách biệt trên https://brandhub.id.vn (dự phòng localhost:3000) cho Guest, Owner, Manager, Creator, Client, Admin (mật khẩu chung do trưởng nhóm cung cấp riêng).',
      'Kết nối sẵn 1 Fanpage Facebook thật (hoặc Threads thật) qua OAuth tại /workspaces/.../social-accounts trên https://brandhub.id.vn và mở sẵn tab trang MXH đó để đối chiếu trực tiếp ở B10.',
      'Bật Lịch sử bộ nhớ tạm Windows (Win + V -> Bật) và chạy preload_clipboard_win_v.bat; đăng nhập sẵn ứng dụng ngân hàng trên điện thoại để quét nạp lẻ 10 AI Credits (2.000 VNĐ) thật ở B11.',
      'Bật Do Not Disturb trên Windows trước khi cắm cáp HDMI Duplicate (Nguyễn Thành Lộc bấm máy · Lê Trí Trung đứng thuyết trình xuyên suốt sang Slide 16–17).',
    ],
    talkingPoints: [
      'Kịch bản thực chiến 20 phút trên https://brandhub.id.vn: SE08 Digital Agency triển khai Chiến dịch Tuyển sinh Đại học FPT 2027 (Khóa K23 - 4 tuần).',
      'Phối hợp nhịp nhàng: Lê Trí Trung đứng thuyết trình · Nguyễn Thành Lộc điều khiển 6 cửa sổ trình duyệt đại diện 6 Canonical Roles (Guest, Owner, Manager, Creator, Client, Admin).',
    ],
    presenterScript:
      'Em (Lê Trí Trung) cùng bạn Nguyễn Thành Lộc xin phép mở 6 cửa sổ trình duyệt trên https://brandhub.id.vn đại diện cho 6 vai trò chuẩn của hệ thống để bắt đầu luồng nghiệp vụ khép kín từ B1 đến B12 của Chiến dịch Tuyển sinh Đại học FPT 2027.',
    expectedOutcome: 'Cả 5 mục chuẩn bị đều sẵn sàng trước khi bước vào B1.',
    fields: [
      {
        field: 'Mật khẩu chung toàn bộ tài khoản Demo',
        actionType: 'Dán Ctrl+V',
        value: '',
        note: 'Áp dụng cho Owner (user177), Manager (user1), Creator (user13, user14, user15), Client (user59) và Admin. Dùng nút MK để nhập/sao chép.',
      },
    ],
    actions: [
      {
        id: 'B0_OPEN_5_CHROME',
        label: 'Mở 6 cửa sổ Chrome & Đăng nhập đủ 6 vai trò',
        description: 'Mở sẵn Guest, Owner, Manager, Creator, Client, Admin',
        variant: 'primary',
        icon: <Users className="size-4" />,
        localOnly: true,
      },
      {
        id: 'B0_RESTORE_DB',
        label: 'Khôi phục DB về trạng thái chuẩn B1',
        description: 'Đảm bảo dữ liệu gốc Chiến dịch ĐH FPT 2027 sạch sẽ',
        variant: 'outline',
        icon: <RefreshCw className="size-4" />,
        localOnly: true,
      },
      {
        id: 'B0_CHECK_NETWORK',
        label: 'Kiểm tra kết nối mạng & tắt VPN lạ',
        description: 'Đảm bảo mạng ổn định cho Gemini AI và SePay',
        variant: 'outline',
        icon: <Play className="size-4" />,
        localOnly: true,
      },
      {
        id: 'B0_OPEN_BANK_APP',
        label: 'Mở sẵn ứng dụng ngân hàng (quét VietQR B11)',
        description: 'Chuẩn bị điện thoại cho bước thanh toán SePay',
        variant: 'outline',
        icon: <KeyRound className="size-4" />,
        localOnly: true,
      },
      {
        id: 'B0_SILENCE_NOTIFICATIONS',
        label: 'Bật Do Not Disturb trên Windows',
        description: 'Chặn thông báo nổi lên màn chiếu Duplicate',
        variant: 'outline',
        icon: <CheckCheck className="size-4" />,
        localOnly: true,
      },
    ],
  },
  {
    stepNumber: 1,
    code: 'B1',
    stage: 'Giai đoạn 1: Gói dịch vụ, Chiến dịch 4 tuần & Công việc',
    stageShort: 'GĐ 1: Gói dịch vụ',
    timeBudget: '00:00 - 02:30',
    title: 'Danh mục 7 Gói đa ngành & Tạo gói Tuyển sinh Thạc sĩ FPT 2027',
    shortTitle: 'Gói dịch vụ & Tạo gói mới',
    frCode: 'FR 3.5.1 - 3.5.4',
    role: 'Owner',
    actorName: 'Lê Trí Trung',
    actorEmail: 'letritrung2605@gmail.com',
    routeTemplate: '/agency/{agency_id}/media-packages',
    extraRoutes: [
      {
        label: 'Gói ĐH FPT 2027 trong Workspace (185M)',
        role: 'Owner',
        routeTemplate: '/workspaces/{workspace_id}/media-package',
      },
    ],
    manualBrowserCue:
      'Cửa sổ Owner: lướt 7 gói đa ngành -> bấm "Tạo gói mới" -> dán Tên gói, Ngân sách (85000000), Thời lượng (4), Mô tả -> tích 5 hạng mục kèm số lượng (12, 2, 2, 4, 2) -> bấm "Lưu gói" -> chuyển sang xem Gói ĐH FPT 2027 (185 triệu) đã chốt trong Workspace.',
    manualChecklist: [
      'Tại /agency/.../media-packages (Owner), giới thiệu 7 gói chuẩn hóa đa lĩnh vực, nhấn nút "Tạo gói".',
      'Dán lần lượt Tên gói, Ngân sách 85000000, Thời lượng 4 tuần và Mô tả gói từ các thẻ bên dưới (nhấn phím C để chép nhanh từng ô).',
      'Tích chọn 5 hạng mục: Bài đăng mạng xã hội (12), Bài báo điện tử (2), Workshop (2), Video ngắn (4), Email/Bản tin (2) rồi bấm "Lưu gói".',
      'Mở trang /workspaces/.../media-package để chỉ rõ Gói ĐH FPT 2027 (185.000.000 VNĐ, 19 hạng mục, khóa terms_version) đã thương thảo & phê duyệt.',
    ],
    talkingPoints: [
      'SE08 Digital chuẩn hóa 7 gói truyền thông cho 7 ngành; hỗ trợ thương thảo hai chiều và khóa phiên bản điều khoản terms_version.',
      'Owner tạo trực tiếp gói mới: tên, ngân sách 85 triệu, 4 tuần, 5 hạng mục có số lượng cụ thể.',
    ],
    presenterScript:
      'Trong vai trò Owner Lê Trí Trung, SE08 Digital quản lý danh mục 7 gói đa ngành và tạo trực tiếp gói mới cho chương trình Thạc sĩ FPT 2027 gồm 5 hạng mục định lượng rõ ràng, sau đó đối chiếu gói Đại học FPT 2027 trị giá 185 triệu VNĐ đã chốt trong Workspace.',
    expectedOutcome: 'Gói Tuyển sinh Thạc sĩ FPT 2027 xuất hiện trong danh mục; hiển thị gói ĐH FPT 2027 đã phê duyệt trong Workspace.',
    fields: [
      {
        field: '1. Tên gói (Package Name)',
        actionType: 'Dán Ctrl+V',
        value: DEFAULT_DEMO_TEXTS.pkg_name,
        copyKey: 'pkg_name',
      },
      {
        field: '2. Ngân sách dự kiến (VNĐ)',
        actionType: 'Dán Ctrl+V',
        value: DEFAULT_DEMO_TEXTS.pkg_budget,
        copyKey: 'pkg_budget',
        note: '85.000.000 VNĐ (nhập số nguyên không dấu chấm)',
      },
      {
        field: '3. Thời lượng triển khai (Tuần)',
        actionType: 'Dán Ctrl+V',
        value: DEFAULT_DEMO_TEXTS.pkg_weeks,
        copyKey: 'pkg_weeks',
      },
      {
        field: '4. Mô tả gói truyền thông',
        actionType: 'Dán Ctrl+V',
        value: DEFAULT_DEMO_TEXTS.pkg_desc,
        copyKey: 'pkg_desc',
      },
      {
        field: '5. Năm hạng mục & Số lượng tích chọn',
        actionType: 'Chọn trên UI',
        value: DEFAULT_DEMO_TEXTS.pkg_items_guide,
        copyKey: 'pkg_items_guide',
      },
    ],
    actions: [
      { id: 'B1_NAV', label: 'Mở Danh mục 7 Gói truyền thông', description: 'Lướt 7 thẻ gói đa ngành', variant: 'primary', icon: <Play className="size-4" /> },
      { id: 'PKG_FILL', label: 'Điền gói Tuyển sinh Thạc sĩ FPT 2027', description: 'Tự gõ tên, 85 triệu, 4 tuần, mô tả & 5 hạng mục', variant: 'outline', icon: <Play className="size-4" /> },
      { id: 'PKG_SAVE', label: 'Lưu gói mới', description: "Tự bấm 'Lưu gói' và tô sáng gói vừa tạo", variant: 'outline', icon: <Play className="size-4" /> },
      { id: 'B1_NAV_WS_PACKAGE', label: 'Mở Gói ĐH FPT 2027 trong Workspace', description: 'Gói 185 triệu, 19 hạng mục đã chốt', variant: 'outline', icon: <Play className="size-4" /> },
    ],
  },
  {
    stepNumber: 2,
    code: 'B2',
    stage: 'Giai đoạn 1: Gói dịch vụ, Chiến dịch 4 tuần & Công việc',
    stageShort: 'GĐ 1: Chiến dịch',
    timeBudget: '02:30 - 04:00',
    title: 'Điều phối Chiến dịch Tuyển sinh 4 Tuần (Brief, Timeline, 6 Đối tác)',
    shortTitle: 'Chiến dịch 4 tuần',
    frCode: 'FR 3.5.6 - 3.5.13',
    role: 'Manager',
    actorName: 'Nguyễn Thành Lộc',
    actorEmail: 'nguyenthanhloc20092004@gmail.com',
    routeTemplate: '/workspaces/{workspace_id}/campaigns',
    manualBrowserCue:
      'Chuyển sang cửa sổ Manager tại /campaigns: bấm lần lượt tab [1. Thông tin] xem Master Brief 6 khối -> tab [2. Công việc] xem Timeline 19 hạng mục -> tab [3. Đối tác] xem 6 đối tác báo chí & KOL.',
    manualChecklist: [
      'Chuyển sang cửa sổ Manager (Nguyễn Thành Lộc) tại /workspaces/.../campaigns.',
      'Ở Bước 1 (Thông tin): chỉ rõ lộ trình 4 tuần và Master Brief 6 khối.',
      'Chuyển sang Bước 2 (Công việc): lướt Timeline 19 hạng mục sinh từ gói (nếu cần demo thêm việc phát sinh ngoài gói, dùng 3 thẻ Copy dự phòng bên dưới).',
      'Chuyển sang Bước 3 (Đối tác): điểm qua 6 đơn vị VnExpress, Thanh Niên, Dân Trí, VTV1, Schannel và Màn hình LED THPT.',
    ],
    talkingPoints: [
      'Master Brief 6 khối vạch rõ 4 tuần: Coming Soon -> Ngành học -> Workshop & Open Day -> Báo chí.',
      'Timeline 19 hạng mục gói và 6 đối tác báo chí, truyền hình, KOL, LED THPT.',
    ],
    presenterScript:
      'Manager Nguyễn Thành Lộc điều phối chiến dịch 4 tuần từ hợp đồng gói đã duyệt: chuẩn hóa Master Brief 6 khối, rà soát timeline 19 hạng mục và gắn kết 6 đối tác truyền thông.',
    expectedOutcome: 'Trình diễn trọn vẹn 3 bước cấu trúc của Chiến dịch 4 tuần.',
    fields: [
      {
        field: '(Tùy chọn) Tên công việc phát sinh ngoài gói',
        actionType: 'Dán Ctrl+V',
        value: DEFAULT_DEMO_TEXTS.out_of_scope_title,
        copyKey: 'out_of_scope_title',
        note: 'Chỉ dùng nếu muốn bấm thử nút "Thêm công việc phát sinh" ở Bước 2 Chiến dịch.',
      },
      {
        field: '(Tùy chọn) Mô tả công việc phát sinh',
        actionType: 'Dán Ctrl+V',
        value: DEFAULT_DEMO_TEXTS.out_of_scope_desc,
        copyKey: 'out_of_scope_desc',
      },
      {
        field: '(Tùy chọn) Tiêu chí nghiệm thu phát sinh',
        actionType: 'Dán Ctrl+V',
        value: DEFAULT_DEMO_TEXTS.out_of_scope_criteria,
        copyKey: 'out_of_scope_criteria',
      },
    ],
    actions: [
      { id: 'B3_STEP_INFO', label: 'Bước 1: Lộ trình 4 tuần & Master Brief', description: '6/6 khối Brief', variant: 'primary', icon: <Play className="size-4" /> },
      { id: 'B3_STEP_TASKS', label: 'Bước 2: Timeline 19 hạng mục', description: 'Lịch trình 4 tuần', variant: 'outline', icon: <Play className="size-4" /> },
      { id: 'B3_STEP_PARTNERS', label: 'Bước 3: 6 Đối tác Báo chí / KOL', description: 'VnExpress, Thanh Niên, Dân Trí, VTV1, Schannel, LED', variant: 'outline', icon: <Play className="size-4" /> },
    ],
  },
  {
    stepNumber: 3,
    code: 'B3',
    stage: 'Giai đoạn 1: Gói dịch vụ, Chiến dịch 4 tuần & Công việc',
    stageShort: 'GĐ 1: Công việc',
    timeBudget: '04:00 - 05:00',
    title: 'Phân bổ 20 Công việc cho 3 Creator & 5 Subtask bài Tuần 3',
    shortTitle: '20 Công việc & 5 Subtask',
    frCode: 'FR 3.6.1 - 3.6.10',
    role: 'Manager',
    actorName: 'Nguyễn Thành Lộc',
    actorEmail: 'nguyenthanhloc20092004@gmail.com',
    routeTemplate: '/workspaces/{workspace_id}/tasks',
    manualBrowserCue:
      'Trên cửa sổ Manager tại /tasks: lướt bảng 20 công việc chia cho Phước, Tuấn, Ân -> nhấp vào dòng "[Tuần 3 - Bài trọng điểm]" để mở ngăn chi tiết hiển thị 5 Subtask phối hợp chéo.',
    manualChecklist: [
      'Tại /workspaces/.../tasks (Manager), giới thiệu 20 công việc phủ đủ 8 loại tác vụ chia cho Phước, Tuấn, Ân.',
      'Nhấp mở "[Tuần 3 - Bài trọng điểm] Điểm nhấn Chuỗi Workshop THPT & Mở đăng ký Học bổng..." để chỉ ra 5 Role Subtasks (Nghiên cứu & Key Visual đã hoàn tất).',
    ],
    talkingPoints: [
      '20 công việc chia theo thế mạnh của Nguyễn Chơn Phước, Nguyễn Minh Tuấn và Hà Văn Ân.',
      'Bài trọng điểm Tuần 3 có 5 Subtask phối hợp chéo; phần Nghiên cứu và Key Visual đã duyệt sẵn.',
    ],
    presenterScript:
      '20 công việc trong 4 tuần được giao theo chuyên môn cho 3 thành viên Creator; riêng bài trọng điểm Tuần 3 có 5 Subtask liên kết chặt chẽ giữa nghiên cứu, thiết kế và biên tập.',
    expectedOutcome: 'Hiển thị bảng 20 công việc và ngăn chi tiết 5 Subtask của bài Tuần 3.',
    fields: [
      {
        field: '(Tùy chọn) Mô tả Subtask mẫu',
        actionType: 'Dán Ctrl+V',
        value: DEFAULT_DEMO_TEXTS.subtask_desc,
        copyKey: 'subtask_desc',
        note: 'Dự phòng khi Hội đồng yêu cầu sửa/thêm mô tả cho Subtask.',
      },
      {
        field: '(Tùy chọn) Tiêu chí nghiệm thu Subtask',
        actionType: 'Dán Ctrl+V',
        value: DEFAULT_DEMO_TEXTS.subtask_criteria,
        copyKey: 'subtask_criteria',
      },
    ],
    actions: [
      { id: 'B4_NAV', label: 'Mở 20 Công việc & 5 Subtask Tuần 3', description: 'Chi tiết [Tuần 3 - Bài trọng điểm]', variant: 'primary', icon: <Play className="size-4" /> },
    ],
  },
  {
    stepNumber: 4,
    code: 'B4',
    stage: 'Giai đoạn 2: Soạn bài, AI, Kiểm duyệt & Duyệt 2 tầng v1 → v2',
    stageShort: 'GĐ 2: AI Caption',
    timeBudget: '05:00 - 08:00',
    title: 'Creator nhận bài Tuần 3, mở /editor & gọi Gemini tạo caption',
    shortTitle: 'Soạn bài & AI caption',
    frCode: 'FR 3.6.3, 3.6.11, 3.6.25, 3.7.1 - 3.7.2',
    role: 'Creator',
    actorName: 'Nguyễn Chơn Phước',
    actorEmail: 'chontem123@gmail.com',
    routeTemplate: '/workspaces/{workspace_id}/editor?taskId={task_id}',
    extraRoutes: [
      {
        label: 'Bảng việc của Creator (/tasks)',
        role: 'Creator',
        routeTemplate: '/workspaces/{workspace_id}/tasks',
      },
    ],
    manualBrowserCue:
      'Cửa sổ Creator: mở /editor của bài Tuần 3 -> chỉ 4 khối độc lập (Brief, Hình ảnh Key Visual Gemini đã duyệt, Kênh đăng, Nội dung) -> bấm "AI tạo 3 phương án caption" -> dán Chủ đề, chọn Thông báo / Chuyên nghiệp / Facebook / Vừa -> bấm "Tạo caption" -> bấm "Chèn" ở phương án 1.',
    manualChecklist: [
      'Chuyển sang cửa sổ Creator (Nguyễn Chơn Phước), mở /editor của [Tuần 3 - Bài trọng điểm].',
      'Chỉ nhanh 4 khối độc lập (Brief, Hình ảnh Key Visual Gemini đã được Client duyệt, 4 Kênh đăng, Nội dung) và khung Preview điện thoại bên phải.',
      'Nhấn nút "AI tạo 3 phương án caption" -> Dán Chủ đề AI bên dưới -> Chọn Mục tiêu: Thông báo, Giọng điệu: Chuyên nghiệp, Nền tảng: Facebook, Độ dài: Vừa.',
      'Nhấn "Tạo caption", chờ Gemini trả về 3 phương án rồi nhấn "Chèn" tại phương án 1.',
    ],
    trapWarning:
      'Dự phòng mạng chậm: Nếu API AI ngoài hội trường phản hồi quá 15 giây, đóng hộp AI và chuyển ngay sang bước B5 dán trực tiếp Bản thảo sạch v1 để giữ nhịp 20 phút.',
    talkingPoints: [
      '/editor tách bài thành 4 phần độc lập: Brief, Hình ảnh, Kênh đăng và Nội dung.',
      'AI GraphRAG rút trích ngữ cảnh thương hiệu ĐH FPT để sinh 3 phương án caption theo Mục tiêu, Giọng điệu, Nền tảng và Độ dài.',
    ],
    presenterScript:
      'Creator Nguyễn Chơn Phước mở bài Tuần 3 trên /editor, kiểm tra Key Visual Gemini đã duyệt và gọi AI GraphRAG tạo 3 phương án caption sát ngữ cảnh tuyển sinh Đại học FPT.',
    expectedOutcome: 'Phần Nội dung bài viết được điền phương án caption từ Gemini AI.',
    fields: [
      {
        field: '1. Chủ đề bài viết (AI Topic)',
        actionType: 'Dán Ctrl+V',
        value: DEFAULT_DEMO_TEXTS.ai_topic,
        copyKey: 'ai_topic',
      },
      {
        field: '2. Bốn tham số chọn trên hộp thoại AI',
        actionType: 'Chọn trên UI',
        value: 'Mục tiêu: Thông báo · Giọng điệu: Chuyên nghiệp · Nền tảng: Facebook · Độ dài: Vừa',
      },
    ],
    actions: [
      { id: 'B5_NAV', label: 'Mở việc [Tuần 3 - Bài trọng điểm]', description: 'Nghiên cứu & Key Visual đã xong', variant: 'primary', icon: <Play className="size-4" /> },
      { id: 'B6_NAV_EDITOR', label: 'Mở Trình soạn thảo /editor', description: '4 phần độc lập', variant: 'outline', icon: <Play className="size-4" /> },
      { id: 'B6_PUSH_KEY_VISUAL', label: 'Xem Key Visual Gemini trong Kho tài nguyên', description: 'Ảnh đã Client duyệt, không thay', variant: 'outline', icon: <Play className="size-4" /> },
      { id: 'AI_FILL', label: 'Điền form AI tạo caption', description: 'Chủ đề, Thông báo, Chuyên nghiệp, Facebook, Vừa', variant: 'outline', icon: <Play className="size-4" /> },
      { id: 'AI_GENERATE', label: 'Tạo caption & Chèn vào bài', description: 'Gemini tạo 3 phương án, tự chèn phương án 1', variant: 'outline', icon: <Play className="size-4" /> },
    ],
  },
  {
    stepNumber: 5,
    code: 'B5',
    stage: 'Giai đoạn 2: Soạn bài, AI, Kiểm duyệt & Duyệt 2 tầng v1 → v2',
    stageShort: 'GĐ 2: Kiểm duyệt & v1',
    timeBudget: '08:00 - 09:30',
    title: 'Kiểm tra an toàn nội dung (3.6.33) & Nộp phần Nội dung v1',
    shortTitle: 'Kiểm duyệt & Nộp v1',
    frCode: 'FR 3.6.33, 3.6.18',
    role: 'Creator',
    actorName: 'Nguyễn Chơn Phước',
    actorEmail: 'chontem123@gmail.com',
    routeTemplate: '/workspaces/{workspace_id}/editor?taskId={task_id}',
    manualBrowserCue:
      'Trên /editor của Creator: [1] Dán đè Câu kiểm thử vi phạm vào ô Nội dung, ngừng gõ 3 giây để hiện cảnh báo đỏ FR 3.6.33 -> [2] Ctrl+A dán đè Bản sạch v1 -> [3] Tô đậm tiêu đề / tạo danh sách -> [4] Dán 6 Hashtags vào ô Bộ Hashtags + Enter -> [5] Nhấn nút "Nộp phần" ở khung Nội dung.',
    manualChecklist: [
      'Chép thẻ [1. Câu kiểm thử vi phạm], Ctrl+A dán vào ô Nội dung bài viết, dừng tay 3 giây để hệ thống tự kích hoạt kiểm duyệt an toàn (FR 3.6.33) và báo chặn.',
      'Chép thẻ [2. Bản thảo sạch v1], Ctrl+A dán thay thế toàn bộ ô Nội dung (bản v1 chủ đích chưa nêu 3 mức học bổng & OJT để demo luồng trả bài ở B7).',
      'Bôi đen dòng tiêu đề 【...】 bấm In đậm (B), định dạng danh sách gạch đầu dòng nếu muốn.',
      'Chép thẻ [3. Bộ 6 Hashtags], dán vào ô "Bộ Hashtags bài viết" bên dưới rồi nhấn Enter.',
      'Chờ trạng thái kiểm duyệt báo An toàn (PASSED), sau đó nhấn nút "Nộp phần" ngay trên khung POST.CAPTION.',
    ],
    talkingPoints: [
      'Cổng kiểm duyệt kép FR 3.6.33 tự động quét sau 3 giây ngừng gõ, chặn ngay ngôn từ kỳ thị, bạo lực và lừa đảo.',
      'Thay bằng bản sạch v1 (chủ đích chưa ghi 3 mức học bổng & OJT), tách riêng Bộ 6 Hashtags và nộp duyệt riêng phần Nội dung.',
    ],
    presenterScript:
      'Creator dán thử một câu chứa nội dung kỳ thị và lừa đảo để chứng minh cổng an toàn FR 3.6.33 tự động phát hiện và chặn nộp; sau đó khôi phục bản sạch v1, gắn bộ 6 hashtag chiến dịch và bấm Nộp phần Nội dung.',
    expectedOutcome: 'Phần Nội dung bài viết (POST.CAPTION) chuyển sang trạng thái Đã nộp (v1).',
    fields: [
      {
        field: '1. Câu mẫu kiểm thử an toàn nội dung (FR 3.6.33)',
        actionType: 'Dán Ctrl+V',
        value: DEFAULT_DEMO_TEXTS.violation_sample,
        copyKey: 'violation_sample',
        note: 'Bắt nhạy 100% cả Hive AI lẫn tập quy tắc dự phòng (hate, violence, spam) và giữ ngôn từ nghiêm túc trước Hội đồng.',
      },
      {
        field: '2. Bản thảo sạch v1 (Chưa có 3 mức Học bổng & OJT)',
        actionType: 'Dán Ctrl+V',
        value: DEFAULT_DEMO_TEXTS.caption_v1_clean,
        copyKey: 'caption_v1_clean',
      },
      {
        field: '3. Bộ 6 Hashtags bài viết',
        actionType: 'Dán Ctrl+V',
        value: DEFAULT_DEMO_TEXTS.hashtags_line,
        copyKey: 'hashtags_line',
        note: 'Dán vào ô nhập Hashtag rồi nhấn phím Enter.',
      },
    ],
    actions: [
      { id: 'B7_FILL_VIOLATION', label: 'Chèn câu vi phạm & xem cảnh báo', description: 'Tự chờ kết quả kiểm tra an toàn', variant: 'primary', icon: <Play className="size-4" /> },
      { id: 'V1_FILL', label: 'Điền bản sạch v1', description: 'Thay toàn bộ caption bằng bản v1', variant: 'outline', icon: <Play className="size-4" /> },
      { id: 'V1_FORMAT', label: 'Định dạng chữ (đậm, nghiêng, 【 】, danh sách)', description: 'Bôi đen rồi bấm B / I, bọc 【 】 tiêu đề, tạo danh sách', variant: 'outline', icon: <Play className="size-4" /> },
      { id: 'V1_HASHTAGS', label: 'Nhập bộ hashtag', description: 'Xoá bộ cũ, gõ 6 hashtag + Enter', variant: 'outline', icon: <Play className="size-4" /> },
      { id: 'V1_SUBMIT', label: 'Nộp phần Nội dung (v1)', description: "Tự bấm 'Nộp phần'", variant: 'outline', icon: <Play className="size-4" /> },
    ],
  },
  {
    stepNumber: 6,
    code: 'B6',
    stage: 'Giai đoạn 2: Soạn bài, AI, Kiểm duyệt & Duyệt 2 tầng v1 → v2',
    stageShort: 'GĐ 2: Manager duyệt v1',
    timeBudget: '09:30 - 10:30',
    title: 'Manager Nguyễn Thành Lộc duyệt nội bộ phần Nội dung (v1)',
    shortTitle: 'Manager duyệt v1',
    frCode: 'FR 3.6.19',
    role: 'Manager',
    actorName: 'Nguyễn Thành Lộc',
    actorEmail: 'nguyenthanhloc20092004@gmail.com',
    routeTemplate: '/workspaces/{workspace_id}/task-approvals?task={task_id}',
    manualBrowserCue:
      'Chuyển sang cửa sổ Manager tại /task-approvals?task=... (F5 nếu cần) -> Tìm thẻ "Nội dung bài đăng (POST.CAPTION)" -> Nhấn nút "Duyệt".',
    manualChecklist: [
      'Chuyển sang cửa sổ Manager (Nguyễn Thành Lộc), mở /workspaces/.../task-approvals?task=...',
      'Chỉ rõ cơ chế duyệt từng phần: Hình ảnh & Kênh đăng đã duyệt giữ nguyên, Manager chỉ cần bấm "Duyệt" ở phần Nội dung (v1) để đẩy sang hàng đợi Client.',
    ],
    talkingPoints: [
      'Phê duyệt tuần tự 2 lớp (Biên tập nội bộ Manager -> Khách hàng Client) chuẩn quy trình tòa soạn & Agency.',
      'Manager chỉ duyệt riêng phần vừa nộp; các phần khác đã duyệt không bị reset.',
    ],
    presenterScript:
      'Manager Nguyễn Thành Lộc mở màn hình Duyệt bài, rà soát phần Nội dung v1 ở tầng nội bộ và bấm Duyệt để chuyển tiếp sang Ban Tuyển sinh Đại học FPT.',
    expectedOutcome: 'Phần Nội dung chuyển sang Đã duyệt nội bộ (INTERNAL_APPROVED).',
    fields: [
      {
        field: 'Thao tác trên màn hình Manager',
        actionType: 'Bấm nút',
        value: 'Nhấn nút "Duyệt" tại thẻ Nội dung bài đăng (POST.CAPTION - Phiên bản v1)',
      },
    ],
    actions: [
      { id: 'B8_NAV_MANAGER_APPROVAL', label: 'Mở màn Duyệt bài của Manager', description: '/task-approvals', variant: 'primary', icon: <Play className="size-4" /> },
      { id: 'MGR_APPROVE_V1', label: 'Duyệt phần Nội dung (v1)', description: "Tự bấm 'Duyệt'", variant: 'outline', icon: <Play className="size-4" /> },
    ],
  },
  {
    stepNumber: 7,
    code: 'B7',
    stage: 'Giai đoạn 2: Soạn bài, AI, Kiểm duyệt & Duyệt 2 tầng v1 → v2',
    stageShort: 'GĐ 2: Client trả v1',
    timeBudget: '10:30 - 12:00',
    title: 'Ban Tuyển sinh ĐH FPT trả lại v1, yêu cầu bổ sung Học bổng + OJT',
    shortTitle: 'Client trả lại v1',
    frCode: 'FR 3.6.20, 3.6.21',
    role: 'Client',
    actorName: 'Ban Tuyển sinh Đại học FPT',
    actorEmail: 'winhtuan@gmail.com',
    routeTemplate: '/workspaces/{workspace_id}/task-approvals?task={task_id}',
    manualBrowserCue:
      'Chuyển sang cửa sổ Client tại /task-approvals?task=... -> Chỉ rõ Client chỉ thấy OUTPUT (ẩn Brief nội bộ) -> Bấm nút "Trả lại" trên thẻ POST.CAPTION -> Dán góp ý Học bổng 2027 + OJT -> Bấm xác nhận "Trả lại".',
    manualChecklist: [
      'Chuyển sang cửa sổ Client (Ban Tuyển sinh Đại học FPT) tại /task-approvals?task=... (nhấn F5 nếu vừa duyệt ở B6).',
      'Nhấn mạnh phân quyền bảo mật thông tin: Client chỉ thấy các phần đầu ra OUTPUT, hoàn toàn không thấy POST.BRIEF nội bộ của Agency.',
      'Nhấn nút "Trả lại" ở thẻ Nội dung bài đăng -> Dán góp ý bên dưới -> Nhấn xác nhận "Trả lại".',
    ],
    talkingPoints: [
      'Client chỉ thấy phần đầu ra OUTPUT, ẩn hoàn toàn ghi chú Brief nội bộ của Agency.',
      'Trả lại riêng phần Nội dung kèm góp ý cụ thể; phần Hình ảnh và Kênh đăng vẫn giữ nguyên trạng thái đã duyệt.',
    ],
    presenterScript:
      'Ban Tuyển sinh Đại học FPT kiểm tra đầu ra, bấm Trả lại riêng phần Nội dung và đề nghị bổ sung rõ 3 mức Học bổng Nguyễn Văn Đạo 50%-70%-100% cùng kỳ thực tập doanh nghiệp OJT từ học kỳ 6.',
    expectedOutcome: 'Riêng phần Nội dung quay về trạng thái Bị trả lại (RETURNED) kèm hộp góp ý của nhà trường.',
    fields: [
      {
        field: 'Góp ý yêu cầu bổ sung của Ban Tuyển sinh ĐH FPT',
        actionType: 'Dán Ctrl+V',
        value: DEFAULT_DEMO_TEXTS.client_reject_note,
        copyKey: 'client_reject_note',
      },
    ],
    actions: [
      { id: 'B9_NAV_CLIENT_APPROVAL', label: 'Mở màn Nghiệm thu của Client', description: 'Chỉ thấy phần OUTPUT', variant: 'primary', icon: <Play className="size-4" /> },
      { id: 'CLIENT_FILL_NOTE', label: 'Điền góp ý Học bổng 2027 + OJT', description: 'Tự mở hộp Trả lại và gõ góp ý', variant: 'outline', icon: <Play className="size-4" /> },
      { id: 'CLIENT_RETURN', label: 'Xác nhận Trả lại cho Creator', description: "Tự bấm 'Trả lại'", variant: 'outline', icon: <Play className="size-4" /> },
    ],
  },
  {
    stepNumber: 8,
    code: 'B8',
    stage: 'Giai đoạn 2: Soạn bài, AI, Kiểm duyệt & Duyệt 2 tầng v1 → v2',
    stageShort: 'GĐ 2: Sửa v2 & Diff',
    timeBudget: '12:00 - 14:00',
    title: 'Creator bổ sung v2, nộp lại & đối chiếu Diff v1 / v2',
    shortTitle: 'Sửa v2, Nộp & Diff',
    frCode: 'FR 3.6.11, 3.6.18',
    role: 'Creator',
    actorName: 'Nguyễn Chơn Phước',
    actorEmail: 'chontem123@gmail.com',
    routeTemplate: '/workspaces/{workspace_id}/editor?taskId={task_id}',
    manualBrowserCue:
      'Quay lại cửa sổ Creator trên /editor (nhấn F5 để tải trạng thái bị trả lại) -> Đặt con trỏ cuối bài viết dán nối tiếp Đoạn bổ sung v2 -> Chờ kiểm duyệt báo An toàn rồi bấm "Nộp phần" -> Bấm nút đồng hồ "Lịch sử phiên bản" để mở bảng so sánh Word-Level Diff v1 vs v2.',
    manualChecklist: [
      'Chuyển sang cửa sổ Creator trên /editor, nhấn F5 làm mới để thấy thẻ góp ý màu cam của Ban Tuyển sinh gắn ngay trên POST.CAPTION.',
      'Đặt con trỏ ở cuối đoạn văn bản hiện tại, dán thẻ [1. Đoạn bổ sung nối tiếp vào v2] (hoặc nếu lỡ xóa bài cũ thì Ctrl+A dán thẻ [2. Trọn bộ bài viết v2 dự phòng]).',
      'Chờ 3 giây để kiểm duyệt báo An toàn rồi nhấn nút "Nộp phần" để tạo phiên bản v2.',
      'Nhấn biểu tượng "Lịch sử phiên bản" trên thanh tiêu đề khối Nội dung để mở ngăn đối chiếu Diff từng từ giữa v1 và v2.',
    ],
    talkingPoints: [
      'Góp ý của Client hiển thị trực tiếp ngay trên khối Nội dung cần sửa.',
      'Ngăn Lịch sử phiên bản lưu trên MongoDB đối chiếu trực quan từng từ (Word-Level Diff) giữa v1 và v2.',
    ],
    presenterScript:
      'Creator đọc góp ý ngay trên khung Nội dung, bổ sung 3 mức Học bổng Nguyễn Văn Đạo 2027 và kỳ OJT vào bản v2, nộp duyệt lại rồi mở Lịch sử phiên bản để Hội đồng thấy rõ phần văn bản vừa thêm mới giữa v1 và v2.',
    expectedOutcome: 'Phần Nội dung chuyển sang Đã nộp (v2); ngăn Lịch sử phiên bản tô xanh rõ đoạn Học bổng & OJT mới bổ sung.',
    fields: [
      {
        field: '1. Đoạn bổ sung nối tiếp vào cuối bài (v2)',
        actionType: 'Dán Ctrl+V',
        value: DEFAULT_DEMO_TEXTS.caption_v2_addition.trim(),
        copyKey: 'caption_v2_addition',
        note: 'Đặt con trỏ xuống cuối bài v1 rồi nhấn Ctrl+V.',
      },
      {
        field: '2. (Dự phòng an toàn) Trọn bộ bài viết hoàn chỉnh v2',
        actionType: 'Dán Ctrl+V',
        value: DEFAULT_DEMO_TEXTS.caption_v2_full,
        copyKey: 'caption_v2_full',
        note: 'Dùng để Ctrl+A -> Ctrl+V thay toàn bộ nếu lỡ tay xóa mất nội dung v1 trước đó.',
      },
    ],
    actions: [
      { id: 'B10_NAV_CREATOR_FIX', label: 'Mở /editor xem góp ý', description: 'Phần Nội dung bị trả lại', variant: 'primary', icon: <Play className="size-4" /> },
      { id: 'V2_FILL', label: 'Bổ sung Học bổng 50%-100% & OJT (v2)', description: 'Tự gõ nối tiếp đoạn v2, in đậm tiêu đề mục & tạo danh sách', variant: 'outline', icon: <Play className="size-4" /> },
      { id: 'V2_SUBMIT', label: 'Nộp lại phần Nội dung (v2)', description: "Tự bấm 'Nộp phần'", variant: 'outline', icon: <Play className="size-4" /> },
      { id: 'B10_OPEN_VERSION_DIFF', label: 'Mở Diff v1 / v2', description: 'Lịch sử phiên bản', variant: 'outline', icon: <Play className="size-4" /> },
    ],
  },
  {
    stepNumber: 9,
    code: 'B9',
    stage: 'Giai đoạn 2: Soạn bài, AI, Kiểm duyệt & Duyệt 2 tầng v1 → v2',
    stageShort: 'GĐ 2: Chốt FINISHED',
    timeBudget: '14:00 - 15:00',
    title: 'Manager & Ban Tuyển sinh ĐH FPT duyệt hoàn tất v2',
    shortTitle: 'Duyệt v2 → FINISHED',
    frCode: 'FR 3.6.19, 3.6.20',
    role: 'Client',
    actorName: 'Ban Tuyển sinh Đại học FPT',
    actorEmail: 'winhtuan@gmail.com',
    routeTemplate: '/workspaces/{workspace_id}/task-approvals?task={task_id}',
    extraRoutes: [
      {
        label: '1. Manager duyệt v2 (/task-approvals)',
        role: 'Manager',
        routeTemplate: '/workspaces/{workspace_id}/task-approvals?task={task_id}',
      },
      {
        label: '3. Creator bấm Gửi phê duyệt (/editor)',
        role: 'Creator',
        routeTemplate: '/workspaces/{workspace_id}/editor?taskId={task_id}',
      },
    ],
    manualBrowserCue:
      'Thao tác 3 cú nhấp chuẩn: [1] Cửa sổ Manager (F5) bấm "Duyệt" v2 -> [2] Cửa sổ Client (F5) bấm "Duyệt" v2 -> [3] Quay về cửa sổ Creator (/editor, F5) bấm nút cam "Gửi phê duyệt" ở thanh trên cùng để chốt Task FINISHED & Post APPROVED!',
    manualChecklist: [
      'Bước 1 (Manager): Tại /task-approvals?task=..., nhấn F5 rồi bấm "Duyệt" phần Nội dung (v2).',
      'Bước 2 (Client): Tại /task-approvals?task=..., nhấn F5 rồi bấm "Duyệt" nghiệm thu chính thức phần Nội dung (v2).',
      'Bước 3 BẮT BUỘC (Creator): Quay lại cửa sổ Creator tại /editor?taskId=..., nhấn F5 rồi bấm nút "Gửi phê duyệt" ở góc phải trên cùng -> Thông báo thành công hiện lên, Task sang FINISHED và Bài đăng sang APPROVED!',
    ],
    trapWarning:
      'Lưu ý quan trọng khi thao tác tay: Sau khi Client bấm Duyệt phần cuối cùng, nhớ quay sang cửa sổ Creator trên /editor bấm nút "Gửi phê duyệt" để chốt toàn bộ Công việc sang FINISHED trước khi qua B10 đăng bài!',
    talkingPoints: [
      'Manager duyệt nội bộ v2, sau đó Ban Tuyển sinh ĐH FPT duyệt nghiệm thu chính thức.',
      'Khi toàn bộ các khối OUTPUT đạt CLIENT_APPROVED và Creator xác nhận gửi hoàn tất, Task tự đóng FINISHED và Post mở khóa APPROVED.',
    ],
    presenterScript:
      'Manager duyệt bản v2, Ban Tuyển sinh ĐH FPT bấm duyệt nghiệm thu chính thức và Creator hoàn tất gửi phê duyệt; ngay lập tức Công việc chuyển sang FINISHED và bài đăng mở khóa APPROVED sẵn sàng xuất bản.',
    expectedOutcome: 'Task chuyển sang FINISHED, toàn bộ 5 Subtask hoàn tất và bài đăng chuyển sang APPROVED.',
    fields: [
      {
        field: 'Chuỗi 3 nút bấm hoàn tất quy trình duyệt',
        actionType: 'Bấm nút',
        value: '1. Manager bấm "Duyệt" -> 2. Client bấm "Duyệt" -> 3. Creator (/editor) bấm "Gửi phê duyệt"',
      },
    ],
    actions: [
      { id: 'B11_NAV_MANAGER_V2', label: 'Manager duyệt v2', description: "Tự mở & bấm 'Duyệt'", variant: 'primary', icon: <Play className="size-4" /> },
      { id: 'B11_NAV_CLIENT_V2', label: 'Client duyệt v2 → Task FINISHED', description: "Tự bấm 'Duyệt' & hoàn tất Task", variant: 'outline', icon: <Play className="size-4" /> },
    ],
  },
  {
    stepNumber: 10,
    code: 'B10',
    stage: 'Giai đoạn 3: Xuất bản 4 nền tảng, Lịch & Dashboard',
    stageShort: 'GĐ 3: Xuất bản 4 kênh',
    timeBudget: '15:00 - 17:00',
    title: 'Đăng ngay lên Facebook, Instagram, TikTok, Threads · Lịch 4 tuần · Dashboard',
    shortTitle: 'Xuất bản, Lịch & Dashboard',
    frCode: 'FR 3.8.1 - 3.8.15',
    role: 'Creator',
    actorName: 'Nguyễn Chơn Phước',
    actorEmail: 'chontem123@gmail.com',
    routeTemplate: `/workspaces/{workspace_id}/posts/${DEFAULT_POST_ID}`,
    extraRoutes: [
      {
        label: 'Kết nối 4 MXH (Manager)',
        role: 'Manager',
        routeTemplate: '/workspaces/{workspace_id}/social-accounts',
      },
      {
        label: 'Lịch xuất bản 4 tuần (/calendar)',
        role: 'Creator',
        routeTemplate: '/workspaces/{workspace_id}/calendar',
      },
      {
        label: 'Dashboard tương tác (/dashboard)',
        role: 'Creator',
        routeTemplate: '/workspaces/{workspace_id}/dashboard',
      },
    ],
    manualBrowserCue:
      'Mở /social-accounts (Manager) chỉ 4 kênh OAuth (trong đó đã liên kết thật 1 Fanpage Facebook / tài khoản Threads) -> Mở chi tiết bài Tuần 3 trên Creator (/posts/...401), tích chọn đúng 1 kênh thật vừa kết nối và bấm "Đăng ngay" -> Mở ngay tab Facebook Fanpage / Threads thật cho Hội đồng thấy bài vừa lên sóng -> Lướt Lịch 4 tuần (/calendar) & Dashboard (/dashboard).',
    manualChecklist: [
      'Trên cửa sổ Manager, mở /workspaces/.../social-accounts giới thiệu 4 kết nối OAuth chuẩn (Facebook, Instagram, TikTok, Threads) và chỉ rõ kênh Fanpage Facebook / Threads thật đang kết nối OAuth.',
      'Chuyển sang cửa sổ Creator, mở chi tiết bài [Tuần 3 - Bài trọng điểm] đã APPROVED, tích chọn đúng 1 kênh MXH thật đó và bấm "Đăng ngay" (xử lý bất đồng bộ qua RabbitMQ & publisher-service).',
      'Chuyển sang tab Facebook Fanpage / Threads thật mở sẵn để Hội đồng thấy bài viết kèm Key Visual và 6 hashtag vừa xuất hiện ngoài đời thực.',
      'Mở /workspaces/.../calendar xem Lịch phủ sóng 4 tuần và mở /workspaces/.../dashboard trình bày chỉ số Reach, Impressions, Reactions tổng hợp 4 kênh.',
    ],
    talkingPoints: [
      'Đồng bộ 4 nền tảng mạng xã hội chuẩn (Facebook, Instagram, TikTok, Threads) qua hàng đợi RabbitMQ với khóa chống trùng ghép processingPostIds:{postId}:{platform} trên Redis (TTL 30 phút); đăng thật trực tiếp lên Fanpage Facebook / Threads qua OAuth 2.0 (AES-256-GCM).',
      'Theo dõi trực quan mật độ phủ sóng trên Lịch 4 tuần (/calendar) và biểu đồ tương tác thực tế trên /dashboard.',
    ],
    presenterScript:
      'Manager kiểm tra kết nối OAuth 4 nền tảng, sau đó Creator bấm Đăng ngay bài trọng điểm Tuần 3 lên kênh Facebook Fanpage / Threads thật và mở trực tiếp trang mạng xã hội để Quý Thầy Cô đối chiếu bài đăng vừa lên sóng, kèm Lịch 4 tuần và Dashboard phân tích.',
    expectedOutcome: 'Bài Tuần 3 xuất hiện trực tiếp trên Fanpage Facebook / Threads thật; Lịch 4 tuần và Dashboard hiển thị đầy đủ dữ liệu.',
    fields: [
      {
        field: '4 nền tảng chuẩn & Kênh OAuth đăng thật trên sân khấu',
        actionType: 'Tham chiếu',
        value: '4 kênh chuẩn: Facebook · Instagram · TikTok · Threads | Bấm "Đăng ngay" trên 1 kênh thật đã nối OAuth (Facebook Fanpage / Threads) rồi mở tab thật kiểm chứng',
      },
    ],
    actions: [
      { id: 'B12_NAV_SOCIAL', label: 'Mở Kết nối 4 nền tảng MXH', description: '/social-accounts', variant: 'primary', icon: <Play className="size-4" /> },
      { id: 'PUBLISH_OPEN', label: 'Mở bài [Tuần 3] đã duyệt', description: 'Chi tiết bài đăng', variant: 'outline', icon: <Play className="size-4" /> },
      { id: 'PUBLISH_NOW', label: 'Đăng ngay lên 4 nền tảng', description: 'Gửi lệnh đăng & chờ kết quả', variant: 'outline', icon: <Play className="size-4" /> },
      { id: 'B13_NAV_CALENDAR', label: 'Mở Lịch xuất bản 4 tuần', description: '/calendar', variant: 'outline', icon: <Play className="size-4" /> },
      { id: 'B13_NAV_DASHBOARD', label: 'Mở Dashboard tương tác', description: '/dashboard', variant: 'outline', icon: <Play className="size-4" /> },
    ],
  },
  {
    stepNumber: 11,
    code: 'B11',
    stage: 'Giai đoạn 4: Thanh toán SePay (VietQR) & Quản trị',
    stageShort: 'GĐ 4: SePay VietQR',
    timeBudget: '17:00 - 18:30',
    title: 'Owner đối chiếu gói Plus (990.000đ) & quét VietQR SePay nạp AI Credit thật',
    shortTitle: 'SePay (VietQR)',
    frCode: 'FR 3.9.1 - 3.9.6',
    role: 'Owner',
    actorName: 'Lê Trí Trung',
    actorEmail: 'letritrung2605@gmail.com',
    routeTemplate: '/subscription/plans',
    extraRoutes: [
      {
        label: 'Nạp lẻ AI Credit & Ví 8.500 điểm (/credit)',
        role: 'Owner',
        routeTemplate: '/agency/{agency_id}/credit',
      },
    ],
    manualBrowserCue:
      'Cửa sổ Owner: [1] Mở /subscription/plans chỉ rõ gói Plus giá chuẩn 990.000 VNĐ/tháng (khớp Slide 16) & bấm xem mã VietQR -> [2] Chuyển sang /agency/.../credit bấm "Nạp thêm Credit" -> chọn "Số lượng tùy chỉnh" -> nhập 10 (= 2.000 VNĐ) -> quét VietQR ngân hàng thật trên sân khấu để nhận webhook SePay cộng +10 Credits tức thì!',
    manualChecklist: [
      'Tại /subscription/plans (Owner), giới thiệu bảng giá thương mại chính thức: gói Agency Plus 990.000 VNĐ/tháng (10 Workspaces, 15 thành viên, 100 GB S3, 5.000 AI Credits) khớp 100% với Slide 16.',
      'Chuyển sang trang Ví AI Credit (/agency/.../credit), chỉ rõ số dư 8.500 điểm và hạn mức trần Workspace ĐH FPT 5.000 điểm (FR 3.9.6).',
      'Nhấn nút "Nạp thêm Credit" -> chọn ô "Số lượng tùy chỉnh" -> dán số 10 (10 Credits × 200đ = 2.000 VNĐ) -> nhấn "Thanh toán 2.000 VND" để sinh mã VietQR động kèm mã đối soát BH...',
      'Dùng ứng dụng ngân hàng quét chuyển khoản thật 2.000 VNĐ ngay trên sân khấu -> Webhook SePay đối soát tự động trong vài giây và cộng +10 Credits vào sổ cái!',
    ],
    talkingPoints: [
      'Hệ thống có 2 dòng gói cước: Cá nhân Studio (Free 0đ / Plus 99k / Pro 299k) và Doanh nghiệp Agency (Basic 0đ / Plus 990.000đ / Enterprise 3.990.000đ) thanh toán qua SePay (VietQR) 0% phí thẻ quốc tế, khớp 100% với Slide 16.',
      'Quét chuyển khoản thật ngay trên sân khấu với gói nạp lẻ tùy chỉnh 10 AI Credits = 2.000 VNĐ (đơn giá 200đ/credit), đối soát tự động bằng Idempotency-Key và mã BH...',
    ],
    presenterScript:
      'Trong vai trò Owner Lê Trí Trung, trên trang Gói thuê bao là mức giá thương mại chuẩn 990.000 VNĐ/tháng của gói Agency Plus (cùng gói Enterprise 3.990.000 VNĐ/tháng và dòng Studio cá nhân 0đ / 99k / 299k). Để chứng minh luồng đối soát ngân hàng thật qua SePay VietQR ngay trên sân khấu mà không cần sửa giả giá gói, em chuyển sang Ví AI Credit, chọn nạp tùy chỉnh 10 Credits tương ứng đúng 2.000 VNĐ theo đơn giá 200đ/credit và quét chuyển khoản trực tiếp để hệ thống tự động cộng điểm tức thì.',
    expectedOutcome: 'Gói Plus hiển thị đúng 990.000 VNĐ/tháng; đơn nạp lẻ 10 Credits (2.000 VNĐ) chuyển sang FULFILLED và cộng +10 Credits ngay khi quét VietQR.',
    fields: [
      {
        field: '1. Số lượng AI Credit nạp lẻ tùy chỉnh (= 2.000 VNĐ quét thật)',
        actionType: 'Dán Ctrl+V',
        value: '10',
        note: 'Tại /agency/.../credit -> Bấm "Nạp thêm Credit" -> Chọn "Số lượng tùy chỉnh" -> Nhập 10 (10 × 200đ = 2.000 VNĐ).',
      },
      {
        field: '2. Thông tin 6 Gói cước & Ví AI Credit chuẩn',
        actionType: 'Tham chiếu',
        value: 'Agency Plus: 990.000 VNĐ/tháng (Enterprise 3.990.000đ, 500GB) · Studio: 0đ / 99k / 299k · Nạp lẻ: 200 VNĐ/credit · Ví SE08: 8.500 credits',
      },
    ],
    actions: [
      { id: 'CREDIT_TOPUP_10', label: 'Nạp lẻ 10 Credits (2.000đ) → VietQR thật', description: 'Tự mở /credit, chọn tùy chỉnh 10 Credits & sinh VietQR 2.000đ', variant: 'primary', icon: <Play className="size-4" /> },
      { id: 'PLAN_CHECKOUT', label: 'Chọn Agency Plus · 1 tháng (990k) → VietQR', description: 'Tự chọn chu kỳ & bấm Nâng cấp/Gia hạn Agency Plus', variant: 'outline', icon: <Play className="size-4" /> },
      { id: 'SEPAY_PAY', label: 'SePay xác nhận thanh toán', description: 'Đối soát Webhook SePay, cập nhật trạng thái thành công', variant: 'outline', icon: <Play className="size-4" /> },
    ],
  },
  {
    stepNumber: 12,
    code: 'B12',
    stage: 'Giai đoạn 4: Thanh toán SePay (VietQR) & Quản trị',
    stageShort: 'GĐ 4: Admin',
    timeBudget: '18:30 - 20:00',
    title: 'Admin giám sát doanh thu & Hàng đợi kiểm duyệt (3.10.4)',
    shortTitle: 'Admin Doanh thu & Kiểm duyệt',
    frCode: 'FR 3.10.1 - 3.10.14',
    role: 'Admin',
    actorName: 'Quản trị viên BrandHub',
    actorEmail: 'admin@brandhub.com',
    routeTemplate: '/admin?view=revenue',
    extraRoutes: [
      {
        label: 'Hàng đợi kiểm duyệt (FR 3.10.4)',
        role: 'Admin',
        routeTemplate: '/admin?view=moderation',
      },
      {
        label: 'Bảng giá AI Credit (/admin/credit-prices)',
        role: 'Admin',
        routeTemplate: '/admin/credit-prices',
      },
    ],
    manualBrowserCue:
      'Chuyển sang cửa sổ Admin: mở /admin?view=revenue xem biểu đồ doanh thu gói SaaS & giao dịch SePay vừa phát sinh -> chuyển sang /admin?view=moderation xử lý Hàng đợi kiểm duyệt cộng đồng (FR 3.10.4) khép lại trọn vẹn 20 phút Demo.',
    manualChecklist: [
      'Chuyển sang cửa sổ Admin (Quản trị viên BrandHub) tại /admin?view=revenue xem tổng quan doanh thu toàn nền tảng.',
      'Chuyển sang tab /admin?view=moderation trình bày Hàng đợi kiểm duyệt nội dung cộng đồng (FR 3.10.4) với 3 bản ghi cảnh báo thực tế — khép lại 12 bước Live Demo và chuyển sang Slide 16.',
    ],
    talkingPoints: [
      'Admin giám sát tập trung doanh thu các gói thuê bao SaaS và đối soát lịch sử giao dịch SePay toàn hệ thống.',
      'Rà soát và ra quyết định xử lý tại Hàng đợi kiểm duyệt an toàn nội dung cộng đồng (FR 3.10.4).',
    ],
    presenterScript:
      'Cuối cùng ở vai trò Admin, hệ thống cung cấp bức tranh toàn cảnh về doanh thu gói SaaS vừa đối soát qua SePay cùng Hàng đợi kiểm duyệt nội dung cộng đồng FR 3.10.4 — khép lại vòng nghiệp vụ khép kín trên 6 vai trò của BrandHub.',
    expectedOutcome: 'Hiển thị Dashboard doanh thu Admin và Hàng đợi kiểm duyệt nội dung (FR 3.10.4).',
    fields: [
      {
        field: 'Phạm vi quản trị của Admin',
        actionType: 'Tham chiếu',
        value: 'Doanh thu SaaS (/admin?view=revenue) · Hàng đợi kiểm duyệt (/admin?view=moderation) · Bảng giá 7 tác vụ AI (/admin/credit-prices)',
      },
    ],
    actions: [
      { id: 'B15_NAV_ADMIN_REVENUE', label: 'Mở Doanh thu toàn hệ thống', description: '/admin?view=revenue', variant: 'primary', icon: <Play className="size-4" /> },
      { id: 'B15_NAV_ADMIN_MODERATION', label: 'Mở Hàng đợi kiểm duyệt (3.10.4)', description: '/admin?view=moderation', variant: 'outline', icon: <Play className="size-4" /> },
    ],
  },
];

const MAIN_STEPS_COUNT = DEMO_STEPS.filter((s) => s.stepNumber > 0).length;

const QA_QUICK_LINKS: Array<{
  id: string;
  label: string;
  role: CanonicalRoleName;
  desc: string;
  routeTemplate: string;
}> = [
  { id: 'QA_VIDEO_EDITOR', label: 'Video ngắn Reels/TikTok (/editor)', role: 'Creator', desc: 'Kịch bản, Quay, Dựng & Caption', routeTemplate: `/workspaces/{workspace_id}/editor?taskId=${VIDEO_TASK_ID}` },
  { id: 'QA_EVENT_EDITOR', label: 'Sự kiện FPTU Open Day (/event)', role: 'Creator', desc: '5 phân khu sự kiện lớn + Runsheet', routeTemplate: `/workspaces/{workspace_id}/tasks/${EVENT_TASK_ID}/event` },
  { id: 'QA_WORKSHOP_EDITOR', label: 'Chuỗi Workshop THPT (/workshop)', role: 'Creator', desc: 'Diễn giả, Lịch trình & Phiếu đăng ký', routeTemplate: `/workspaces/{workspace_id}/tasks/${WORKSHOP_TASK_ID}/workshop` },
  { id: 'QA_PRESS_EDITOR', label: 'PR Báo chí VnExpress (/press)', role: 'Creator', desc: 'Thông cáo báo chí & Liên hệ phóng viên', routeTemplate: `/workspaces/{workspace_id}/tasks/${PRESS_TASK_ID}/press` },
  { id: 'QA_KOL_EDITOR', label: 'Booking KOL Schannel (/kol)', role: 'Creator', desc: 'Shortlist, Chi phí & Báo cáo nghiệm thu', routeTemplate: `/workspaces/{workspace_id}/tasks/${KOL_TASK_ID}/kol` },
  { id: 'QA_NEWSLETTER_EDITOR', label: 'Bản tin Email (/newsletter)', role: 'Creator', desc: 'Thiết kế khối Email Cẩm nang 2027', routeTemplate: `/workspaces/{workspace_id}/tasks/${NEWSLETTER_TASK_ID}/newsletter` },
  { id: 'QA_AI_TRENDS', label: 'AI Xu hướng MXH (/ai-studio/trends)', role: 'Manager', desc: '6 xu hướng tuyển sinh trực tiếp từ Redis', routeTemplate: '/ai-studio/trends' },
  { id: 'QA_AI_RAG', label: 'AI Tri thức RAG (/ai-studio/knowledge-base)', role: 'Manager', desc: 'Tài liệu quy chế & học bổng ĐH FPT', routeTemplate: '/ai-studio/knowledge-base' },
  { id: 'QA_AI_AMBASSADORS', label: 'AI Đại sứ ảo (/ai-studio/ambassadors)', role: 'Creator', desc: 'Nhân vật Minh Anh & Hoàng Khôi K23', routeTemplate: '/ai-studio/ambassadors' },
  { id: 'QA_CLIENT_PORTAL', label: 'Cổng Khách hàng (/portal)', role: 'Client', desc: '2 hạng mục Open Day chờ ĐH FPT duyệt', routeTemplate: '/workspaces/{workspace_id}/portal' },
  { id: 'QA_CLIENT_VAULT', label: 'Kho riêng Client Vault (/library)', role: 'Client', desc: 'Tư liệu gốc ĐH FPT chia sẻ sang SE08', routeTemplate: '/workspaces/{workspace_id}/library' },
  { id: 'QA_COLLABORATORS', label: 'Danh bạ 10 Đối tác (/collaborators)', role: 'Owner', desc: '6 đối tác ĐH FPT + 4 đối tác đa ngành', routeTemplate: '/agency/{agency_id}/collaborators' },
  { id: 'QA_PUBLIC_PACKAGE', label: 'Link Chào giá Gói (Guest)', role: 'Guest', desc: '/packages/share/goi-tuyen-sinh-dh-fpt-2027', routeTemplate: '/packages/share/goi-tuyen-sinh-dh-fpt-2027' },
  { id: 'QA_PUBLIC_SURVEY', label: 'Link Khảo sát THPT (Guest)', role: 'Guest', desc: '/public/surveys/khao-sat-chon-nganh-fptu-2027', routeTemplate: '/public/surveys/khao-sat-chon-nganh-fptu-2027' },
  { id: 'QA_ADMIN_CREDIT_PRICES', label: 'Bảng giá AI Credit (/admin/credit-prices)', role: 'Admin', desc: 'Cấu hình đơn giá 7 nghiệp vụ AI', routeTemplate: '/admin/credit-prices' },
];

const STAGE_MODE_STORAGE_KEY = 'brandhub_demo_stage_mode_v1';
const APP_URL_STORAGE_KEY = 'brandhub_demo_target_url_v1';
const PROD_APP_URL = 'https://brandhub.id.vn';
const LOCAL_APP_URL = 'http://localhost:3000';

function safeCopyToClipboard(text: string): void {
  if (typeof navigator !== 'undefined' && navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(text).catch(() => {
      fallbackExecCopy(text);
    });
    return;
  }
  fallbackExecCopy(text);
}

function fallbackExecCopy(text: string): void {
  if (typeof document === 'undefined') return;
  const ta = document.createElement('textarea');
  ta.value = text;
  ta.setAttribute('readonly', 'true');
  ta.style.position = 'fixed';
  ta.style.left = '-9999px';
  ta.style.top = '0';
  document.body.appendChild(ta);
  ta.focus();
  ta.select();
  try {
    document.execCommand('copy');
  } catch {
    // ignore
  }
  document.body.removeChild(ta);
}

export const DemoMonitorPage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const { resolvedTheme, setTheme } = useAppPreferences();

  const [stageMode, setStageModeState] = useState<StageMode>(() => {
    const qMode = searchParams.get('mode');
    if (qMode === 'manual' || qMode === 'auto') return qMode;
    if (typeof window !== 'undefined') {
      const saved = window.localStorage.getItem(STAGE_MODE_STORAGE_KEY);
      if (saved === 'manual' || saved === 'auto') return saved;
    }
    return 'manual';
  });
  const [manualSubView, setManualSubView] = useState<ManualSubView>('step');

  const [monitorUrl] = useState<string>('http://127.0.0.1:3999');
  const [status, setStatus] = useState<MonitorStatus | null>(null);
  const [connected, setConnected] = useState<boolean>(false);
  const [wsConnected, setWsConnected] = useState<boolean>(false);
  const [wsClientsCount, setWsClientsCount] = useState<number>(0);
  const [activeStepIndex, setActiveStepIndex] = useState<number>(1);
  const [busyAction, setBusyAction] = useState<string | null>(null);
  const [toastMessage, setToastMessage] = useState<{ text: string; isError?: boolean } | null>(null);
  const [copiedKey, setCopiedKey] = useState<string | null>(null);
  const [copiedHistory, setCopiedHistory] = useState<Record<string, boolean>>({});
  const [manualCheckDone, setManualCheckDone] = useState<Record<string, boolean>>({});
  const [showResetConfirm, setShowResetConfirm] = useState<boolean>(false);
  const [showCleanConfirm, setShowCleanConfirm] = useState<boolean>(false);
  const [showGuideModal, setShowGuideModal] = useState<boolean>(false);
  const [doneActions, setDoneActions] = useState<Record<string, boolean>>({});
  const [paceLabel, setPaceLabel] = useState<string>('Vừa');

  // Đồng hồ đếm giờ 20 phút ngay trên thanh Header
  const [elapsedSec, setElapsedSec] = useState<number>(0);
  const [timerRunning, setTimerRunning] = useState<boolean>(false);

  const [customTexts, setCustomTexts] = useState<Record<string, string>>(DEFAULT_DEMO_TEXTS);
  const [configIds, setConfigIds] = useState(() => {
    const qEnv = searchParams.get('env');
    let initialUrl = PROD_APP_URL;
    if (qEnv === 'local') {
      initialUrl = LOCAL_APP_URL;
    } else if (qEnv === 'cloud' || qEnv === 'prod') {
      initialUrl = PROD_APP_URL;
    } else if (typeof window !== 'undefined') {
      const savedUrl = window.localStorage.getItem(APP_URL_STORAGE_KEY);
      if (savedUrl) initialUrl = savedUrl;
    }
    return {
      app_url: initialUrl,
      agency_id: '359a1839-18c7-48e2-8a68-f5f68c3375b6',
      workspace_id: 'b47477c4-13ad-44ff-8c49-f73f1837461b',
      campaign_id: 'd7e00000-0000-4000-8000-000000000301',
      task_id: 'c6453698-cf56-38c1-96d2-90ccdd985228',
    };
  });

  const setTargetAppUrl = useCallback(
    (nextUrl: string) => {
      const cleaned = (nextUrl || PROD_APP_URL).trim().replace(/\/+$/, '');
      setConfigIds((prev) => ({ ...prev, app_url: cleaned }));
      if (typeof window !== 'undefined') {
        window.localStorage.setItem(APP_URL_STORAGE_KEY, cleaned);
      }
      if (stageMode === 'auto') {
        fetch(`${monitorUrl}/api/config`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ app_url: cleaned }),
        }).catch(() => {
          // ignore if :3999 not started yet
        });
      }
    },
    [monitorUrl, stageMode]
  );

  const activePillRef = useRef<HTMLButtonElement | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const lastWsErrVerRef = useRef<number>(0);

  const setStageMode = useCallback(
    (mode: StageMode) => {
      setStageModeState(mode);
      if (typeof window !== 'undefined') {
        window.localStorage.setItem(STAGE_MODE_STORAGE_KEY, mode);
      }
      const nextParams = new URLSearchParams(searchParams);
      nextParams.set('mode', mode);
      setSearchParams(nextParams, { replace: true });
    },
    [searchParams, setSearchParams]
  );

  useEffect(() => {
    if (!timerRunning) return;
    const id = window.setInterval(() => {
      setElapsedSec((prev) => prev + 1);
    }, 1000);
    return () => window.clearInterval(id);
  }, [timerRunning]);

  const formatClock = (sec: number): string => {
    const m = Math.floor(sec / 60);
    const s = sec % 60;
    return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
  };

  const resolveRoute = useCallback(
    (tpl: string): string =>
      tpl
        .replace('{agency_id}', configIds.agency_id)
        .replace('{workspace_id}', configIds.workspace_id)
        .replace('{campaign_id}', configIds.campaign_id)
        .replace('{task_id}', configIds.task_id),
    [configIds]
  );

  const sendWsCommand = useCallback(
    (payload: Record<string, unknown>) => {
      if (stageMode !== 'auto') return;
      const ws = wsRef.current;
      if (ws && ws.readyState === WebSocket.OPEN) {
        try {
          ws.send(JSON.stringify(payload));
        } catch {
          // ignore transient socket errors
        }
      }
    },
    [stageMode]
  );

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
    }, 3800);
  }, []);

  const fetchMonitorStatus = useCallback(async () => {
    if (stageMode !== 'auto') return;
    try {
      const res = await fetch(`${monitorUrl}/api/status`);
      if (!res.ok) throw new Error('Status check failed');
      const data: MonitorStatus & { sync?: { pace_label?: string } } = await res.json();
      setStatus(data);
      setConnected(true);
      if (data.sync?.pace_label) {
        setPaceLabel(data.sync.pace_label);
      }
      if (data.ids) {
        setConfigIds((prev) => {
          // Nếu máy chủ :3999 đang khác URL mà người điều khiển đã chọn trên giao diện, tự đồng bộ xuống :3999
          if (data.app_url && prev.app_url && data.app_url !== prev.app_url) {
            fetch(`${monitorUrl}/api/config`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ app_url: prev.app_url }),
            }).catch(() => {});
          }
          return {
            app_url: prev.app_url || data.app_url || PROD_APP_URL,
            agency_id: data.ids.agency_id || '359a1839-18c7-48e2-8a68-f5f68c3375b6',
            workspace_id: data.ids.workspace_id || 'b47477c4-13ad-44ff-8c49-f73f1837461b',
            campaign_id: data.ids.campaign_id || 'd7e00000-0000-4000-8000-000000000301',
            task_id: data.ids.task_id || 'c6453698-cf56-38c1-96d2-90ccdd985228',
          };
        });
      }
    } catch {
      setConnected(false);
    }
  }, [monitorUrl, stageMode]);

  useEffect(() => {
    if (stageMode !== 'auto') {
      setConnected(false);
      setWsConnected(false);
      return;
    }
    fetchMonitorStatus();
    const timer = setInterval(fetchMonitorStatus, 4000);
    return () => clearInterval(timer);
  }, [fetchMonitorStatus, stageMode]);

  // Chỉ kết nối WebSocket :3999 khi đang ở chế độ Auto (trong Manual Mode không gọi bất kỳ kết nối Selenium nào)
  useEffect(() => {
    if (stageMode !== 'auto') return;
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
              if (typeof msg.pace_label === 'string' && msg.pace_label) {
                setPaceLabel(msg.pace_label);
              }
              if (msg.last_error && typeof msg.version === 'number' && msg.version !== lastWsErrVerRef.current) {
                lastWsErrVerRef.current = msg.version;
                showToast(String(msg.last_error), true);
              }
              if (Array.isArray(msg.done_actions)) {
                const next: Record<string, boolean> = {};
                msg.done_actions.forEach((aid: string) => {
                  next[aid] = true;
                });
                setDoneActions((prev) => ({
                  ...Object.fromEntries(Object.entries(prev).filter(([k]) => k.startsWith('B0_'))),
                  ...next,
                }));
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
  }, [monitorUrl, stageMode]);

  useEffect(() => {
    activePillRef.current?.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
  }, [activeStepIndex]);

  const currentStep = DEMO_STEPS[activeStepIndex];
  const prevStep = activeStepIndex > 0 ? DEMO_STEPS[activeStepIndex - 1] : null;
  const roleChangedFromPrev = prevStep !== null && prevStep.role !== currentStep.role;
  const resolvedRoute = resolveRoute(currentStep.routeTemplate);

  const nextPendingAction = currentStep.actions.find((a) => !doneActions[a.id]) ?? null;

  const handleCopy = useCallback(
    (text: string, key: string, label?: string) => {
      if (!timerRunning && elapsedSec === 0) {
        setTimerRunning(true);
      }
      safeCopyToClipboard(text);
      setCopiedKey(key);
      setCopiedHistory((prev) => ({ ...prev, [key]: true }));
      showToast(label ? `Đã sao chép "${label}" — nhấn Ctrl+V để dán.` : 'Đã sao chép vào bộ nhớ tạm.');
      setTimeout(() => {
        setCopiedKey((prev) => (prev === key ? null : prev));
      }, 1800);
    },
    [elapsedSec, showToast, timerRunning]
  );

  // Phím C: Sao chép thông minh trường tiếp theo chưa chép trong bước hiện tại
  const handleCopyNextStepField = useCallback(() => {
    const copyable = currentStep.fields
      .map((f, idx) => ({ f, idx, key: `${currentStep.code}_field_${idx}` }))
      .filter(({ f }) => f.actionType === 'Dán Ctrl+V' || Boolean(f.copyKey));
    const pool = copyable.length > 0
      ? copyable
      : currentStep.fields.map((f, idx) => ({ f, idx, key: `${currentStep.code}_field_${idx}` }));
    if (pool.length === 0) {
      showToast(`Bước ${currentStep.code} chỉ cần thao tác nhấp chuột, không có ô cần dán.`);
      return;
    }
    const target = pool.find((item) => !copiedHistory[item.key]) ?? pool[0];
    const liveVal = target.f.copyKey ? customTexts[target.f.copyKey] ?? target.f.value : target.f.value;
    handleCopy(liveVal, target.key, target.f.field);
  }, [copiedHistory, currentStep.code, currentStep.fields, customTexts, handleCopy, showToast]);

  const handleLoginAll = useCallback(async () => {
    setBusyAction('LOGIN_ALL');
    try {
      await fetch(`${monitorUrl}/api/config`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ app_url: configIds.app_url }),
      }).catch(() => {});
      const res = await fetch(`${monitorUrl}/api/login-all`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      });
      const data = await res.json();
      if (data.ok) {
        setDoneActions((prev) => ({ ...prev, B0_OPEN_5_CHROME: true }));
        showToast(`Đã mở & đồng bộ đủ 6 cửa sổ Chrome trên ${configIds.app_url}!`);
      } else {
        showToast(data.error || 'Có lỗi khi mở 6 cửa sổ vai trò.', true);
      }
      await fetchMonitorStatus();
    } catch {
      showToast('Không kết nối được dịch vụ điều khiển cổng 3999.', true);
    } finally {
      setBusyAction(null);
    }
  }, [configIds.app_url, fetchMonitorStatus, monitorUrl, showToast]);

  const handleCyclePace = useCallback(async () => {
    try {
      const res = await fetch(`${monitorUrl}/api/hud/command`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type: 'cycle_pace' }),
      });
      const data = await res.json();
      if (data?.state?.pace_label) {
        setPaceLabel(data.state.pace_label);
        showToast(`Đã chuyển tốc độ tự động sang: ${data.state.pace_label}`);
      }
    } catch {
      showToast('Không kết nối được cổng 3999 để đổi tốc độ.', true);
    }
  }, [monitorUrl, showToast]);

  const handleKillChrome = useCallback(async () => {
    setBusyAction(null);
    try {
      const res = await fetch(`${monitorUrl}/api/kill-chrome`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      });
      const data = await res.json();
      showToast(data.message || 'Đã đóng toàn bộ Chrome để mở lại sạch sẽ.');
      await fetchMonitorStatus();
    } catch {
      showToast('Không kết nối được cổng 3999.', true);
    }
  }, [fetchMonitorStatus, monitorUrl, showToast]);

  const triggerStepAction = useCallback(
    async (actionId: string) => {
      if (busyAction !== null) return;
      if (!timerRunning && elapsedSec === 0) {
        setTimerRunning(true);
      }
      // Trong chế độ Tự động, nút B0 mở thật 6 Chrome hoặc khôi phục DB thay vì chỉ đánh dấu tích
      if (stageMode === 'auto' && actionId === 'B0_OPEN_5_CHROME') {
        await handleLoginAll();
        return;
      }
      if (stageMode === 'auto' && actionId === 'B0_RESTORE_DB') {
        setShowResetConfirm(true);
        return;
      }
      const actionDef = DEMO_STEPS.flatMap((s) => s.actions).find((a) => a.id === actionId);
      if (actionDef?.localOnly) {
        setDoneActions((prev) => ({ ...prev, [actionId]: !prev[actionId] }));
        return;
      }
      if (stageMode === 'manual') {
        const qaMatch = QA_QUICK_LINKS.find((q) => q.id === actionId);
        if (qaMatch) {
          const fullUrl = `${configIds.app_url}${resolveRoute(qaMatch.routeTemplate)}`;
          window.open(fullUrl, '_blank', 'noopener,noreferrer');
          showToast(`Đã mở tab mới cho ${qaMatch.label} (hãy mở trên cửa sổ ${qaMatch.role} nếu khác phiên).`);
        }
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
          'Chưa kết nối được dịch vụ điều khiển tự động (:3999). Bạn có thể chuyển sang chế độ "Tài liệu & Copy mẫu" trên thanh tiêu đề để thao tác tay ngay.',
          true
        );
      } finally {
        setBusyAction(null);
      }
    },
    [busyAction, configIds.app_url, customTexts, elapsedSec, fetchMonitorStatus, handleLoginAll, monitorUrl, resolveRoute, showToast, stageMode, timerRunning]
  );

  const handleSmartAdvance = useCallback(() => {
    if (stageMode === 'manual') {
      selectStepWithSync((i) => Math.min(DEMO_STEPS.length - 1, i + 1));
      return;
    }
    if (busyAction !== null) return;
    if (nextPendingAction) {
      triggerStepAction(nextPendingAction.id);
    } else if (activeStepIndex < DEMO_STEPS.length - 1) {
      selectStepWithSync((i) => Math.min(DEMO_STEPS.length - 1, i + 1));
    }
  }, [activeStepIndex, busyAction, nextPendingAction, selectStepWithSync, stageMode, triggerStepAction]);

  const handleLoginSingleRole = useCallback(
    async (role: CanonicalRoleName) => {
      if (stageMode === 'manual') {
        const roleMeta = CANONICAL_ROLES.find((r) => r.role === role);
        if (!roleMeta) return;
        if (role === 'Guest') {
          const url = `${configIds.app_url}${resolveRoute(roleMeta.defaultRoute)}`;
          handleCopy(url, `role_copy_${role}`, `URL ${role}`);
        } else {
          handleCopy(roleMeta.email, `role_copy_${role}`, `Email ${role} (${roleMeta.shortLabel})`);
        }
        return;
      }
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
        showToast('Không kết nối được dịch vụ điều khiển cổng 3999.', true);
      } finally {
        setBusyAction(null);
      }
    },
    [busyAction, configIds.app_url, fetchMonitorStatus, handleCopy, monitorUrl, resolveRoute, showToast, stageMode]
  );

  const handleCancelBusy = useCallback(() => {
    fetch(`${monitorUrl}/api/hud/command`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type: 'skip_step' }),
    }).catch(() => {});
    if (busyAction !== null) {
      setBusyAction(null);
    }
    showToast('Đã bỏ qua bước đang chờ khẩn cấp. Bạn có thể tiếp tục điều khiển ngay.');
  }, [busyAction, monitorUrl, showToast]);

  // Hỗ trợ phím tắt sân khấu (1-5 cho đủ 5 nút con, Space, C sao chép nhanh, ←/→/PageUp/PageDown)
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
      if ((e.key === 'c' || e.key === 'C') && !e.ctrlKey && !e.metaKey && !e.altKey) {
        e.preventDefault();
        handleCopyNextStepField();
        return;
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
      if (['1', '2', '3', '4', '5'].includes(e.key)) {
        const idx = Number(e.key) - 1;
        if (stageMode === 'manual') {
          const fld = currentStep.fields[idx];
          if (fld) {
            e.preventDefault();
            const val = fld.copyKey ? customTexts[fld.copyKey] ?? fld.value : fld.value;
            handleCopy(val, `${currentStep.code}_field_${idx}`, fld.field);
          }
          return;
        }
        const act = currentStep.actions[idx];
        if (act) {
          e.preventDefault();
          triggerStepAction(act.id);
        }
        return;
      }
      if ((e.key === 'r' || e.key === 'R') && !e.ctrlKey && !e.metaKey && stageMode === 'auto') {
        e.preventDefault();
        handleLoginSingleRole(currentStep.role);
      }
    };
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [
    busyAction,
    currentStep,
    customTexts,
    handleCancelBusy,
    handleCopy,
    handleCopyNextStepField,
    handleLoginSingleRole,
    handleSmartAdvance,
    selectStepWithSync,
    showCleanConfirm,
    showGuideModal,
    showResetConfirm,
    stageMode,
    triggerStepAction,
  ]);

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
      showToast('Không kết nối được dịch vụ điều khiển cổng 3999.', true);
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
        setActiveStepIndex(1);
        showToast(data.message || 'Đã khôi phục dữ liệu PostgreSQL, MongoDB & Redis về trạng thái chuẩn B1.');
      } else {
        showToast(data.error || 'Lỗi khi nạp lại dữ liệu mẫu.', true);
      }
    } catch {
      showToast('Không kết nối được cổng 3999. Nếu không dùng Selenium, hãy chạy: python prepare_demo_data_template.py --apply', true);
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
        showToast(data.message || 'Đã xóa sạch toàn bộ dữ liệu mẫu và các bản ghi phát sinh sau buổi demo.');
      } else {
        showToast(data.error || 'Lỗi khi xóa dữ liệu demo.', true);
      }
    } catch {
      showToast('Không kết nối được cổng 3999. Bạn có thể chạy: python prepare_demo_data_template.py --clean', true);
    } finally {
      setBusyAction(null);
    }
  };

  const formatReadableDescription = (desc: string): string =>
    desc
      .replace('/agency/{agency_id}', '/agency/se08-digital')
      .replace('/workspaces/{workspace_id}', '/workspaces/dh-fpt-2027')
      .replace('{agency_id}', configIds.agency_id.slice(0, 8))
      .replace('{workspace_id}', configIds.workspace_id.slice(0, 8))
      .replace('{campaign_id}', configIds.campaign_id.slice(0, 8))
      .replace('{task_id}', configIds.task_id.slice(0, 8));

  const handleSyncCurrentStepRoute = useCallback(async () => {
    if (stageMode === 'manual') {
      const url = `${configIds.app_url}${resolvedRoute}`;
      handleCopy(url, `route_${currentStep.code}`, `URL ${currentStep.code}`);
      return;
    }
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
      showToast('Không kết nối được cổng 3999.', true);
    } finally {
      setBusyAction(null);
    }
  }, [busyAction, configIds.app_url, currentStep.actorName, currentStep.code, currentStep.role, fetchMonitorStatus, handleCopy, monitorUrl, resolvedRoute, showToast, stageMode]);

  const handleResetCurrentStep = useCallback(() => {
    setDoneActions((prev) => {
      const next = { ...prev };
      currentStep.actions.forEach((a) => {
        delete next[a.id];
      });
      return next;
    });
    setCopiedHistory((prev) => {
      const next = { ...prev };
      Object.keys(next).forEach((k) => {
        if (k.startsWith(`${currentStep.code}_`)) delete next[k];
      });
      return next;
    });
    setManualCheckDone((prev) => {
      const next = { ...prev };
      Object.keys(next).forEach((k) => {
        if (k.startsWith(`${currentStep.code}_`)) delete next[k];
      });
      return next;
    });
    showToast(`Đã đặt lại dấu tích của bước ${currentStep.code}.`);
    if (stageMode === 'auto') {
      handleSyncCurrentStepRoute();
    }
  }, [currentStep.actions, currentStep.code, handleSyncCurrentStepRoute, showToast, stageMode]);

  const handleCopyAllStepData = useCallback(() => {
    if (!currentStep.fields.length) {
      showToast('Bước này không có trường văn bản cần nhập.');
      return;
    }
    const lines = currentStep.fields.map((f) => {
      const val = f.copyKey ? customTexts[f.copyKey] ?? f.value : f.value;
      return `[${f.field}] (${f.actionType}):\n${val}`;
    });
    const allText = lines.join('\n\n---\n\n');
    safeCopyToClipboard(allText);
    showToast(`Đã chép trọn bộ ${currentStep.fields.length} mục của bước ${currentStep.code} vào Clipboard.`);
  }, [currentStep.code, currentStep.fields, customTexts, showToast]);

  // Danh sách các trường nhập liệu chính xuyên suốt B1 -> B8 cho chế độ Bảng Phẳng 1 Trang
  const allMainCopyItems = useMemo(
    () => [
      { step: 'B1', role: 'Owner' as CanonicalRoleName, label: 'Tên gói mới (Thạc sĩ FPT 2027)', copyKey: 'pkg_name', note: 'Ô #package-field-name' },
      { step: 'B1', role: 'Owner' as CanonicalRoleName, label: 'Ngân sách gói (85 triệu VNĐ)', copyKey: 'pkg_budget', note: 'Ô #package-field-budgetAmount · Thời lượng: 4 tuần' },
      { step: 'B1', role: 'Owner' as CanonicalRoleName, label: 'Mô tả gói truyền thông', copyKey: 'pkg_desc', note: '5 hạng mục: MXH 12 · Báo 2 · Workshop 2 · Video 4 · Email 2' },
      { step: 'B4', role: 'Creator' as CanonicalRoleName, label: 'Chủ đề gọi Gemini AI Tạo Caption', copyKey: 'ai_topic', note: 'Chọn: Thông báo · Chuyên nghiệp · Facebook · Vừa' },
      { step: 'B5', role: 'Creator' as CanonicalRoleName, label: 'Câu kiểm thử vi phạm an toàn (FR 3.6.33)', copyKey: 'violation_sample', note: 'Dán vào ô Nội dung -> chờ 3 giây hiện cảnh báo đỏ' },
      { step: 'B5', role: 'Creator' as CanonicalRoleName, label: 'Bản thảo sạch v1 (Thay câu vi phạm)', copyKey: 'caption_v1_clean', note: 'Ctrl+A -> Ctrl+V đè toàn bộ ô Nội dung' },
      { step: 'B5', role: 'Creator' as CanonicalRoleName, label: 'Bộ 6 Hashtags bài viết', copyKey: 'hashtags_line', note: 'Dán vào ô Bộ Hashtags + nhấn Enter -> bấm Nộp phần' },
      { step: 'B7', role: 'Client' as CanonicalRoleName, label: 'Góp ý trả lại của Ban Tuyển sinh ĐH FPT', copyKey: 'client_reject_note', note: 'Client bấm Trả lại phần POST.CAPTION -> Dán góp ý' },
      { step: 'B8', role: 'Creator' as CanonicalRoleName, label: 'Đoạn bổ sung Học bổng 50%-100% & OJT (v2)', copyKey: 'caption_v2_addition', note: 'Đặt con trỏ cuối bài v1 -> Ctrl+V -> Nộp phần -> Xem Diff' },
      { step: 'B8', role: 'Creator' as CanonicalRoleName, label: '(Dự phòng) Trọn bộ bài viết hoàn chỉnh v2', copyKey: 'caption_v2_full', note: 'Dùng nếu lỡ xóa nội dung v1 trước đó' },
    ],
    []
  );

  const renderStepFieldsCards = () => (
    <div className="grid grid-cols-1 gap-2.5">
      {currentStep.fields.map((f, i) => {
        const fieldKey = `${currentStep.code}_field_${i}`;
        const liveValue = f.copyKey ? customTexts[f.copyKey] ?? f.value : f.value;
        const isJustCopied = copiedKey === fieldKey;
        const wasCopied = Boolean(copiedHistory[fieldKey]);

        return (
          <div
            key={fieldKey}
            className={`p-3.5 border transition-colors space-y-2 ${
              isJustCopied || wasCopied
                ? 'bg-emerald-50/60 border-emerald-400'
                : 'bg-white border-slate-200 hover:border-orange-300'
            }`}
          >
            <div className="flex flex-wrap items-center justify-between gap-2">
              <div className="flex flex-wrap items-center gap-2 min-w-0">
                <span className="size-6 bg-orange-50 text-orange-900 border border-orange-200 font-mono tabular-nums text-xs font-bold inline-flex items-center justify-center shrink-0">
                  {i + 1}
                </span>
                <span className="text-xs sm:text-sm font-bold text-slate-900">{f.field}</span>
                <span className="px-2 py-0.5 text-[11px] font-semibold bg-orange-50 text-orange-800 border border-orange-200">
                  {f.actionType}
                </span>
                {i < 5 && stageMode === 'manual' && (
                  <span className="px-1.5 py-0.5 text-[10px] font-mono tabular-nums font-semibold bg-slate-100 text-slate-600 border border-slate-200">
                    Phím {i + 1}
                  </span>
                )}
              </div>

              <button
                type="button"
                onClick={() => handleCopy(liveValue, fieldKey, f.field)}
                className={`min-h-7 px-3 py-1 text-xs font-bold border inline-flex items-center gap-1.5 cursor-pointer transition-colors ${
                  isJustCopied || wasCopied
                    ? 'bg-emerald-50 text-emerald-900 border-emerald-400 hover:bg-emerald-100'
                    : 'bg-[#ea6c3b] hover:bg-[#d95d2c] text-white border-[#ea6c3b]'
                }`}
              >
                {isJustCopied || wasCopied ? (
                  <>
                    <Check className="size-3.5 shrink-0" />
                    <span>{isJustCopied ? 'Vừa sao chép!' : 'Đã chép · Chép lại'}</span>
                  </>
                ) : (
                  <>
                    <Copy className="size-3.5 shrink-0" />
                    <span>Sao chép ngay</span>
                  </>
                )}
              </button>
            </div>

            {f.copyKey ? (
              <textarea
                rows={Math.min(5, Math.max(2, Math.ceil(liveValue.length / 105)))}
                value={liveValue}
                onChange={(e) =>
                  setCustomTexts((prev) => ({
                    ...prev,
                    [f.copyKey!]: e.target.value,
                  }))
                }
                className="w-full p-2.5 text-xs text-slate-800 bg-slate-50 border border-slate-200 focus:bg-white focus:border-orange-400 focus:outline-none leading-relaxed font-mono"
              />
            ) : (
              <div
                onClick={() => handleCopy(liveValue, fieldKey, f.field)}
                title="Nhấp vào ô để sao chép nhanh"
                className="p-2.5 text-xs text-slate-800 bg-slate-50 border border-slate-200 whitespace-pre-wrap leading-relaxed font-mono cursor-pointer hover:border-orange-300"
              >
                {liveValue}
              </div>
            )}

            {f.note && <div className="text-[11px] text-slate-600 font-medium">{f.note}</div>}
          </div>
        );
      })}
    </div>
  );

  const renderQaGridSection = (defaultOpen = false) => (
    <AstryxCard padding={4} className="bg-white border border-slate-200 shadow-xs">
      <AstryxCollapsible
        defaultIsOpen={defaultOpen}
        trigger={
          <div className="flex flex-wrap items-center justify-between gap-2 pr-2 min-h-7">
            <span className="text-xs sm:text-sm font-bold text-slate-900 flex items-center gap-2">
              <Sparkles className="size-4 text-[#ea6c3b] shrink-0" />
              <span>
                Truy cập nhanh Q&amp;A Hội đồng: {QA_QUICK_LINKS.length} Màn hình Chuyên sâu (Event, Workshop, Báo chí, KOL, AI Studio, Client Vault)
              </span>
            </span>
            <span className="px-2 py-0.5 text-[11px] font-mono tabular-nums font-semibold bg-orange-50 text-orange-800 border border-orange-200">
              {stageMode === 'manual' ? 'Mở trực tiếp URL hoặc Copy' : '1 chạm mở đúng vai trò'}
            </span>
          </div>
        }
      >
        <div className="pt-3 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
          {QA_QUICK_LINKS.map((item) => {
            const fullUrl = `${configIds.app_url}${resolveRoute(item.routeTemplate)}`;
            const copyId = `qa_copy_${item.id}`;
            const isCopied = copiedKey === copyId;
            if (stageMode === 'manual') {
              return (
                <div
                  key={item.id}
                  className="p-2.5 border border-slate-200 bg-white hover:border-orange-300 flex flex-col justify-between gap-2 transition-colors"
                >
                  <div className="flex items-start justify-between gap-2">
                    <div className="min-w-0">
                      <div className="text-xs font-bold text-slate-900 truncate">{item.label}</div>
                      <div className="text-[11px] text-slate-600 truncate mt-0.5">{item.desc}</div>
                    </div>
                    <span className="px-1.5 py-0.5 bg-orange-50 text-orange-800 border border-orange-200 font-mono text-[10px] font-bold shrink-0">
                      {item.role}
                    </span>
                  </div>
                  <div className="flex items-center gap-1.5 pt-1 border-t border-slate-100">
                    <a
                      href={fullUrl}
                      target="_blank"
                      rel="noreferrer"
                      className="min-h-7 px-2.5 py-1 flex-1 bg-slate-50 hover:bg-orange-50 text-slate-800 border border-slate-200 text-[11px] font-semibold inline-flex items-center justify-center gap-1"
                    >
                      <span>Mở trang</span>
                      <ExternalLink className="size-3 shrink-0 text-[#ea6c3b]" />
                    </a>
                    <button
                      type="button"
                      onClick={() => handleCopy(fullUrl, copyId, item.label)}
                      className="min-h-7 px-2.5 py-1 bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 text-[11px] font-semibold inline-flex items-center gap-1 cursor-pointer"
                    >
                      {isCopied ? <Check className="size-3 text-emerald-600" /> : <Copy className="size-3" />}
                      <span>{isCopied ? 'Đã chép' : 'Copy URL'}</span>
                    </button>
                  </div>
                </div>
              );
            }
            return (
              <button
                key={item.id}
                type="button"
                disabled={busyAction !== null}
                title={`${item.label} (vai trò ${item.role}) — bấm để tự mở đúng trang và vai trò`}
                onClick={() => triggerStepAction(item.id)}
                className="min-h-7 p-2.5 border border-slate-200 bg-white hover:border-orange-300 hover:bg-slate-50 text-left flex items-start justify-between gap-2 cursor-pointer transition-colors"
              >
                <div className="min-w-0">
                  <div className="text-xs font-bold text-slate-900 truncate">{item.label}</div>
                  <div className="text-[11px] text-slate-600 truncate mt-0.5">{item.desc}</div>
                </div>
                <span className="px-1.5 py-0.5 bg-orange-50 text-orange-800 border border-orange-200 font-mono text-[10px] font-bold shrink-0">
                  {item.role}
                </span>
              </button>
            );
          })}
        </div>
      </AstryxCollapsible>
    </AstryxCard>
  );

  return (
    <div className="demo-monitor-root min-h-dvh bg-slate-50/50 text-slate-900 font-sans">
      {/* Hộp thoại xác nhận khôi phục DB */}
      <AstryxDialog
        isOpen={showResetConfirm}
        onOpenChange={setShowResetConfirm}
        width={460}
        padding={5}
        aria-label="Xác nhận khôi phục dữ liệu gốc"
      >
        <div className="space-y-4">
          <div className="flex items-start gap-3">
            <div className="size-10 bg-orange-50 text-[#ea6c3b] border border-orange-200 flex items-center justify-center shrink-0">
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
            <AstryxButton label="Hủy" variant="secondary" size="sm" onClick={() => setShowResetConfirm(false)} />
            <AstryxButton label="Đồng ý khôi phục" variant="primary" size="sm" onClick={handleResetDatabase} />
          </div>
        </div>
      </AstryxDialog>

      {/* Hộp thoại xác nhận Xóa sạch dữ liệu Demo */}
      <AstryxDialog
        isOpen={showCleanConfirm}
        onOpenChange={setShowCleanConfirm}
        width={480}
        padding={5}
        aria-label="Xác nhận xóa sạch dữ liệu demo"
      >
        <div className="space-y-4">
          <div className="flex items-start gap-3">
            <div className="size-10 bg-red-50 text-red-600 border border-red-200 flex items-center justify-center shrink-0">
              <Trash2 className="size-5" />
            </div>
            <div className="space-y-1.5">
              <AstryxHeading level={3} className="text-base font-bold text-slate-900 text-balance">
                Xóa sạch toàn bộ dữ liệu mẫu và dữ liệu vừa Demo?
              </AstryxHeading>
              <p className="text-xs text-slate-600 leading-relaxed text-pretty">
                Thao tác này sẽ xóa toàn bộ 7 gói truyền thông mẫu, chiến dịch 4 tuần, 20 công việc, bài viết, nhật ký xuất bản và khảo sát đã tạo.
              </p>
              <div className="p-2.5 bg-slate-50 border border-slate-200 text-[11px] text-slate-600 leading-relaxed">
                7 tài khoản đăng nhập vẫn được giữ nguyên. Lần tới khi cần diễn tập lại, nhấn <strong>Khôi phục DB</strong> để nạp lại trong 3 giây.
              </div>
            </div>
          </div>
          <div className="flex items-center justify-end gap-2 pt-1">
            <AstryxButton label="Hủy" variant="secondary" size="sm" onClick={() => setShowCleanConfirm(false)} />
            <AstryxButton label="Xóa sạch dữ liệu Demo" variant="primary" size="sm" onClick={handleCleanDatabase} />
          </div>
        </div>
      </AstryxDialog>

      {/* Hộp thoại Hướng dẫn cả 2 kịch bản (Có / Không dùng điều khiển tự động) */}
      <AstryxDialog
        isOpen={showGuideModal}
        onOpenChange={setShowGuideModal}
        width={600}
        padding={5}
        aria-label="Hướng dẫn vận hành Demo SE08"
      >
        <div className="space-y-4">
          <div className="flex items-start gap-3">
            <div className="size-10 bg-orange-50 text-[#ea6c3b] border border-orange-200 flex items-center justify-center shrink-0">
              <HelpCircle className="size-5" />
            </div>
            <div className="space-y-1">
              <AstryxHeading level={3} className="text-base font-bold text-slate-900">
                Hướng dẫn Vận hành 12 Bước Bảo vệ (B1 – B12 · 20 Phút)
              </AstryxHeading>
              <p className="text-xs text-slate-600 leading-relaxed">
                Thiết kế linh hoạt cho màn chiếu nhân bản (Duplicate) trong cả 2 trường hợp tại phòng bảo vệ.
              </p>
            </div>
          </div>

          <div className="space-y-2.5 text-xs text-slate-700 leading-relaxed">
            <div className="p-3 bg-slate-50 border border-slate-200 space-y-1">
              <div className="font-bold text-slate-900">
                Phân công Sân khấu &amp; Môi trường (Đã chốt)
              </div>
              <p>
                • <strong>Người đứng thuyết trình</strong>: <strong>Lê Trí Trung</strong> dẫn dắt xuyên suốt 20 phút Live Demo rồi nối thẳng sang <code className="font-mono">Slide 16–17</code>.
                <br />• <strong>Người điều khiển máy</strong>: <strong>Nguyễn Thành Lộc</strong> ngồi laptop thao tác 6 cửa sổ trình duyệt (HDMI Duplicate).
                <br />• <strong>Môi trường chính</strong>: <code className="font-mono">https://brandhub.id.vn</code> (1-click chuyển về <code className="font-mono">http://localhost:3000</code> ngay trên thanh tiêu đề nếu rớt mạng hội trường).
              </p>
            </div>

            <div className="p-3 bg-orange-50/60 border border-orange-200 space-y-1">
              <div className="font-bold text-slate-900">
                Trường hợp A — Thao tác tay hoàn toàn (Chế độ "Tài liệu &amp; Copy mẫu")
              </div>
              <p>
                1. Chạy <code className="font-mono">open_clean_chrome_roles.bat</code> trước giờ thi để mở 6 cửa sổ Chrome gốc trên <code className="font-mono">https://brandhub.id.vn</code> (dự phòng local: <code className="font-mono">open_clean_chrome_roles_local.bat</code>) và chạy <code className="font-mono">preload_clipboard_win_v.bat</code> để nạp sẵn vào <strong>Win + V</strong>.
              </p>
              <p>
                2. Trên trang này, nhấn phím <strong>C</strong> (hoặc phím <strong>1–5</strong> / nút <strong>Sao chép ngay</strong>) để chép từng ô dữ liệu chuẩn rồi dán <strong>Ctrl + V</strong> sang Chrome.
              </p>
            </div>

            <div className="p-3 bg-slate-50 border border-slate-200 space-y-1">
              <div className="font-bold text-slate-900">
                Trường hợp B — Được phép dùng Điều khiển tự động (Chế độ "Tự động")
              </div>
              <p>
                Bật công tắc sang <strong>Tự động</strong>, đảm bảo đèn báo <strong>Socket</strong> sáng, bấm <strong>Mở 6 Vai trò</strong> rồi nhấn phím <strong>Space</strong> (hoặc phím <strong>1–5</strong>) để đi tuần tự qua toàn bộ 12 bước B1 – B12.
              </p>
            </div>

            <div className="p-3 bg-slate-50 border border-slate-200 space-y-1">
              <div className="font-bold text-slate-900">
                Ba điểm chốt ở B9, B10 &amp; B11
              </div>
              <p>
                • <strong>Tại B9</strong>: Sau khi Client bấm Duyệt bản v2, chuyển về cửa sổ Creator trên <code className="font-mono">/editor</code> bấm nút cam <strong>"Gửi phê duyệt"</strong> góc trên bên phải để chốt <code className="font-mono">Task FINISHED</code>.
                <br />• <strong>Tại B10</strong>: Bấm <strong>Đăng ngay</strong> trên đúng <strong>1 kênh thật đã kết nối OAuth</strong> (Facebook Fanpage / Threads) rồi mở ngay tab trang thật đối chiếu.
                <br />• <strong>Tại B11</strong>: Chỉ rõ gói <code className="font-mono">Agency Plus = 990.000 VNĐ/tháng</code>, sau đó qua <code className="font-mono">/credit</code> bấm <strong>Nạp thêm Credit → Số lượng tùy chỉnh: 10 (= 2.000 VNĐ)</strong> để quét VietQR ngân hàng thật!
              </p>
            </div>
          </div>

          <div className="flex items-center justify-end pt-1">
            <AstryxButton label="Đã sẵn sàng" variant="primary" size="sm" onClick={() => setShowGuideModal(false)} />
          </div>
        </div>
      </AstryxDialog>

      {/* Toast */}
      {toastMessage && (
        <div className="fixed bottom-4 right-4 z-50 max-w-md shadow-md overflow-hidden border border-slate-200">
          <AstryxBanner
            status={toastMessage.isError ? 'warning' : 'info'}
            title={toastMessage.isError ? 'Lưu ý' : 'Đã sao chép / Thực thi'}
            description={toastMessage.text}
            isDismissable
            onDismiss={() => setToastMessage(null)}
          />
        </div>
      )}

      {/* Thanh Header dính trên cùng */}
      <header className="sticky top-0 z-30 bg-white/95 backdrop-blur-md border-b border-slate-200 shadow-xs">
        <div className="max-w-[1600px] mx-auto px-3 sm:px-4 py-2 flex flex-wrap items-center justify-between gap-2.5">
          {/* Cụm Thương hiệu + Chuyển chế độ */}
          <div className="flex flex-wrap items-center gap-2.5 min-w-0">
            <Link
              to="/"
              title="Quay về cổng tài liệu BrandHub Docs"
              className="min-h-7 inline-flex items-center gap-1 px-2.5 py-1 border border-slate-200 hover:border-orange-300 bg-white hover:bg-slate-50 text-slate-700 text-xs font-semibold cursor-pointer transition-colors"
            >
              <ArrowLeft className="size-3.5" />
              <span className="hidden sm:inline">Docs</span>
            </Link>

            <div className="flex items-center gap-2 min-w-0">
              <div className="size-8 bg-[#ea6c3b] flex items-center justify-center text-white font-extrabold text-sm shadow-xs shrink-0">
                BH
              </div>
              <div className="flex items-center gap-2 min-w-0">
                <AstryxHeading level={1} className="text-sm sm:text-base font-bold text-slate-900 truncate">
                  {stageMode === 'manual'
                    ? 'Hồ Sơ Dữ Liệu Thực Nghiệm & Kịch Bản — ĐH FPT 2027 (SE08)'
                    : 'Bàn Điều Khiển Thuyết Trình SE08'}
                </AstryxHeading>
                <span className="hidden 2xl:inline-flex px-2 py-0.5 text-[11px] font-mono tabular-nums font-semibold bg-orange-50 text-orange-800 border border-orange-200">
                  12 Bước · 20:00
                </span>
              </div>
            </div>

            {/* Công tắc Kép: Tài liệu & Copy mẫu (Không Selenium) <-> Tự động (Selenium) */}
            <div
              role="group"
              aria-label="Chế độ vận hành buổi bảo vệ"
              className="inline-flex items-center border border-slate-200 bg-slate-50"
            >
              <button
                type="button"
                onClick={() => setStageMode('manual')}
                title="Chế độ Thao tác tay: Ẩn toàn bộ kết nối tự động, hiển thị thẻ Copy 1 chạm & hướng dẫn từng bước sạch sẽ trên màn chiếu Duplicate"
                className={`min-h-7 inline-flex items-center gap-1.5 px-2.5 py-1 text-xs font-semibold cursor-pointer transition-colors ${
                  stageMode === 'manual'
                    ? 'bg-[#ea6c3b] text-white font-bold'
                    : 'bg-white text-slate-700 hover:bg-slate-50'
                }`}
              >
                <BookOpen className="size-3.5 shrink-0" />
                <span>Tài liệu &amp; Copy mẫu</span>
              </button>
              <button
                type="button"
                onClick={() => setStageMode('auto')}
                title="Chế độ Tự động: Kết nối cổng điều khiển trình duyệt 1 chạm khi Hội đồng cho phép"
                className={`min-h-7 inline-flex items-center gap-1.5 px-2.5 py-1 text-xs font-semibold border-l border-slate-200 cursor-pointer transition-colors ${
                  stageMode === 'auto'
                    ? 'bg-[#ea6c3b] text-white font-bold'
                    : 'bg-white text-slate-700 hover:bg-slate-50'
                }`}
              >
                <Play className="size-3.5 shrink-0" />
                <span>Tự động</span>
              </button>
            </div>
          </div>

          {/* Cụm Đồng hồ 20:00 + Công cụ tương ứng từng chế độ */}
          <div className="flex flex-wrap items-center gap-1.5">
            {/* Đồng hồ sân khấu 20 phút (font-mono tabular-nums) */}
            <div className="min-h-7 inline-flex items-center gap-1.5 px-2.5 py-1 bg-slate-50 border border-slate-200 text-xs font-mono tabular-nums">
              <Clock className="size-3.5 text-[#ea6c3b] shrink-0" />
              <span className="font-bold text-slate-900">{formatClock(elapsedSec)}</span>
              <span className="text-slate-500">/ 20:00</span>
              <button
                type="button"
                onClick={() => setTimerRunning((v) => !v)}
                className="min-h-7 px-2 py-0.5 bg-orange-50 hover:bg-orange-100 text-orange-900 border border-orange-200 font-sans text-[11px] font-bold cursor-pointer"
              >
                {timerRunning ? 'Tạm dừng' : 'Đếm giờ'}
              </button>
              {elapsedSec > 0 && (
                <button
                  type="button"
                  onClick={() => {
                    setTimerRunning(false);
                    setElapsedSec(0);
                  }}
                  title="Đặt lại đồng hồ về 00:00"
                  className="min-h-7 px-1.5 py-0.5 bg-white hover:bg-slate-100 text-slate-600 border border-slate-200 text-[11px] cursor-pointer"
                >
                  00:00
                </button>
              )}
            </div>

            {stageMode === 'manual' ? (
              /* Sub-tabs chuyên biệt khi ở Chế độ Tài liệu & Copy mẫu */
              <div className="inline-flex items-center border border-slate-200 bg-white">
                <button
                  type="button"
                  onClick={() => setManualSubView('step')}
                  className={`min-h-7 inline-flex items-center gap-1 px-2.5 py-1 text-xs font-semibold cursor-pointer transition-colors ${
                    manualSubView === 'step'
                      ? 'bg-orange-50 text-orange-950 font-bold'
                      : 'text-slate-700 hover:bg-slate-50'
                  }`}
                >
                  <ListOrdered className="size-3.5 text-[#ea6c3b]" />
                  <span>Theo bước (B1–B12)</span>
                </button>
                <button
                  type="button"
                  onClick={() => setManualSubView('sheet')}
                  className={`min-h-7 inline-flex items-center gap-1 px-2.5 py-1 text-xs font-semibold border-l border-slate-200 cursor-pointer transition-colors ${
                    manualSubView === 'sheet'
                      ? 'bg-orange-50 text-orange-950 font-bold'
                      : 'text-slate-700 hover:bg-slate-50'
                  }`}
                >
                  <LayoutGrid className="size-3.5 text-[#ea6c3b]" />
                  <span>Bảng phẳng 1 trang</span>
                </button>
                <button
                  type="button"
                  onClick={() => setManualSubView('create')}
                  className={`min-h-7 inline-flex items-center gap-1 px-2.5 py-1 text-xs font-semibold border-l border-slate-200 cursor-pointer transition-colors ${
                    manualSubView === 'create'
                      ? 'bg-orange-50 text-orange-950 font-bold'
                      : 'text-slate-700 hover:bg-slate-50'
                  }`}
                >
                  <PlusSquare className="size-3.5 text-[#ea6c3b]" />
                  <span>Tạo mới tại chỗ (4)</span>
                </button>
              </div>
            ) : (
              /* Công cụ điều khiển trình duyệt khi ở Chế độ Tự động */
              <>
                <div
                  className="min-h-7 inline-flex items-center gap-1.5 px-2.5 py-1 bg-white border border-slate-200 text-xs"
                  title={
                    wsConnected
                      ? `WebSocket :3999/ws đang đồng bộ (${wsClientsCount} kết nối)`
                      : 'Trạng thái kết nối tới dịch vụ điều khiển :3999'
                  }
                >
                  <AstryxStatusDot
                    variant={connected ? 'accent' : 'neutral'}
                    label={connected ? 'Đã kết nối' : 'Chưa bật'}
                    isPulsing={connected}
                  />
                  <span className="text-slate-700 font-mono tabular-nums font-medium">
                    {connected ? (wsConnected ? `Socket · ${wsClientsCount}` : 'Đã kết nối') : 'Chưa bật :3999'}
                  </span>
                </div>

                <div className="inline-flex items-center border border-slate-200 bg-white">
                  <button
                    type="button"
                    onClick={() => handleArrangeWindows('split')}
                    disabled={busyAction !== null}
                    className={`min-h-7 inline-flex items-center gap-1 px-2.5 py-1 text-xs font-semibold cursor-pointer transition-colors ${
                      status?.window_mode === 'split'
                        ? 'bg-orange-50 text-orange-950 font-bold'
                        : 'text-slate-700 hover:bg-slate-50'
                    }`}
                  >
                    <Columns2 className="size-3.5 text-slate-600" />
                    <span>70/30</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => handleArrangeWindows('maximize')}
                    disabled={busyAction !== null}
                    className={`min-h-7 inline-flex items-center gap-1 px-2.5 py-1 text-xs font-semibold cursor-pointer transition-colors border-l border-slate-200 ${
                      status?.window_mode === 'maximize'
                        ? 'bg-orange-50 text-orange-950 font-bold'
                        : 'text-slate-700 hover:bg-slate-50'
                    }`}
                  >
                    <Maximize2 className="size-3.5 text-slate-600" />
                    <span className="hidden xl:inline">Toàn màn hình</span>
                  </button>
                </div>

                <button
                  type="button"
                  disabled={busyAction !== null}
                  onClick={handleLoginAll}
                  className="min-h-7 inline-flex items-center gap-1.5 px-3 py-1 bg-[#ea6c3b] hover:bg-[#d95d2c] text-white text-xs font-semibold border border-[#ea6c3b] cursor-pointer shadow-xs transition-colors disabled:opacity-50"
                >
                  {busyAction === 'LOGIN_ALL' ? <RefreshCw className="size-3.5 animate-spin" /> : <Users className="size-3.5" />}
                  <span>Mở 6 Vai trò</span>
                </button>

                <button
                  type="button"
                  onClick={handleCyclePace}
                  title="Đổi tốc độ gõ & dừng trực quan của Selenium (Chậm / Vừa / Nhanh)"
                  className="min-h-7 inline-flex items-center gap-1 px-2.5 py-1 bg-white hover:bg-orange-50 border border-slate-200 text-xs font-semibold text-slate-700 cursor-pointer transition-colors"
                >
                  <span>Tốc độ: {paceLabel}</span>
                </button>

                {busyAction !== null && (
                  <button
                    type="button"
                    onClick={handleCancelBusy}
                    title="Bỏ qua ngay bước đang chờ (Esc)"
                    className="min-h-7 inline-flex items-center gap-1 px-2.5 py-1 bg-amber-50 hover:bg-amber-100 border border-amber-300 text-xs font-bold text-amber-900 cursor-pointer transition-colors"
                  >
                    <RotateCcw className="size-3.5" />
                    <span>Bỏ qua chờ</span>
                  </button>
                )}

                <button
                  type="button"
                  onClick={handleKillChrome}
                  title="Tắt toàn bộ Chrome để mở lại sạch sẽ nếu cửa sổ trình duyệt bị treo"
                  className="min-h-7 inline-flex items-center gap-1 px-2 py-1 bg-white hover:bg-slate-100 border border-slate-200 text-xs font-semibold text-slate-700 cursor-pointer transition-colors"
                >
                  <span className="hidden 2xl:inline">Tắt Chrome</span>
                  <span className="2xl:hidden">×Chrome</span>
                </button>

                <button
                  type="button"
                  disabled={busyAction !== null}
                  onClick={() => setShowResetConfirm(true)}
                  className="min-h-7 inline-flex items-center gap-1.5 px-2.5 py-1 bg-white hover:bg-slate-50 border border-slate-200 text-xs font-semibold text-slate-700 cursor-pointer transition-colors disabled:opacity-50"
                >
                  {busyAction === 'RESET_DB' ? <RefreshCw className="size-3.5 animate-spin" /> : <Database className="size-3.5 text-slate-600" />}
                  <span>Khôi phục DB</span>
                </button>

                <button
                  type="button"
                  disabled={busyAction !== null}
                  onClick={() => setShowCleanConfirm(true)}
                  className="min-h-7 inline-flex items-center gap-1.5 px-2.5 py-1 bg-white hover:bg-red-50 border border-slate-200 hover:border-red-300 text-xs font-semibold text-slate-700 hover:text-red-700 cursor-pointer transition-colors disabled:opacity-50"
                >
                  {busyAction === 'CLEAN_DB' ? <RefreshCw className="size-3.5 animate-spin" /> : <Trash2 className="size-3.5 text-slate-600" />}
                  <span className="hidden xl:inline">Xóa Demo</span>
                </button>
              </>
            )}

            {/* Nút 1-Click chuyển nhanh Cloud (brandhub.id.vn) <-> Local (localhost:3000) */}
            <div
              role="group"
              aria-label="Môi trường chạy hệ thống"
              className="inline-flex items-center border border-slate-200 bg-white font-mono text-[11px]"
            >
              <button
                type="button"
                onClick={() => {
                  setTargetAppUrl(PROD_APP_URL);
                  showToast('Đã trỏ toàn bộ liên kết sang Cloud chính thức: https://brandhub.id.vn');
                }}
                title="Môi trường chính thức trên Cloud (https://brandhub.id.vn)"
                className={`min-h-7 px-2 py-1 cursor-pointer transition-colors ${
                  configIds.app_url === PROD_APP_URL
                    ? 'bg-orange-50 text-orange-950 font-bold'
                    : 'text-slate-600 hover:bg-slate-50'
                }`}
              >
                brandhub.id.vn
              </button>
              <button
                type="button"
                onClick={() => {
                  setTargetAppUrl(LOCAL_APP_URL);
                  showToast('Đã chuyển nhanh toàn bộ liên kết sang dự phòng Local: http://localhost:3000');
                }}
                title="Dự phòng tức thì khi mạng hội trường gián đoạn (http://localhost:3000)"
                className={`min-h-7 px-2 py-1 border-l border-slate-200 cursor-pointer transition-colors ${
                  configIds.app_url === LOCAL_APP_URL
                    ? 'bg-orange-50 text-orange-950 font-bold'
                    : 'text-slate-600 hover:bg-slate-50'
                }`}
              >
                localhost:3000
              </button>
            </div>

            {/* Nút Đổi giao diện Sáng / Tối ngay tại chỗ */}
            <button
              type="button"
              onClick={() => setTheme(resolvedTheme === 'dark' ? 'light' : 'dark')}
              title={resolvedTheme === 'dark' ? 'Chuyển sang nền Trắng - Cam sáng rõ cho máy chiếu' : 'Chuyển sang giao diện Tối'}
              aria-label="Đổi chế độ Sáng hoặc Tối"
              className="min-h-7 inline-flex items-center gap-1 px-2.5 py-1 border border-slate-200 hover:border-orange-300 bg-white hover:bg-slate-50 text-slate-700 text-xs font-semibold cursor-pointer transition-colors"
            >
              {resolvedTheme === 'dark' ? <Sun className="size-3.5 text-[#ea6c3b]" /> : <Moon className="size-3.5 text-slate-600" />}
              <span className="hidden xl:inline">{resolvedTheme === 'dark' ? 'Sáng' : 'Tối'}</span>
            </button>

            <button
              type="button"
              title="Xem hướng dẫn vận hành cho cả 2 trường hợp"
              onClick={() => setShowGuideModal(true)}
              className="min-h-7 inline-flex items-center gap-1 px-2.5 py-1 border border-slate-200 hover:border-orange-300 bg-white hover:bg-slate-50 text-slate-700 text-xs font-semibold cursor-pointer transition-colors"
            >
              <HelpCircle className="size-3.5 text-slate-600" />
              <span className="hidden lg:inline">Hướng dẫn</span>
            </button>
          </div>
        </div>

        {/* Dải 6 Vai trò Canonical */}
        <div className="bg-slate-50 border-t border-slate-200">
          <div className="max-w-[1600px] mx-auto px-3 sm:px-4 py-1.5 flex items-center justify-between gap-2 overflow-x-auto no-scrollbar">
            <div className="flex items-center gap-1.5 min-w-0">
              <span className="text-[11px] font-bold text-slate-500 shrink-0 hidden sm:inline mr-1">
                {stageMode === 'manual' ? 'Tài khoản 6 Vai trò (Bấm để chép Email):' : 'Cửa sổ Chrome:'}
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
                    title={
                      stageMode === 'manual'
                        ? `${item.role} (${item.fullName}): ${item.email} — Bấm để sao chép nhanh`
                        : `${item.role}: ${item.fullName} (${item.email}) — Bấm để đưa cửa sổ lên trước`
                    }
                    className={`min-h-7 inline-flex items-center gap-1.5 px-2.5 py-1 border text-xs cursor-pointer transition-colors shrink-0 ${
                      isCurrentStepRole
                        ? 'bg-orange-50 text-orange-950 border-orange-400 font-bold shadow-xs'
                        : 'bg-white text-slate-700 border-slate-200 hover:border-orange-300 hover:bg-slate-50'
                    }`}
                  >
                    <span
                      className={`size-2 shrink-0 ${
                        stageMode === 'manual'
                          ? isCurrentStepRole
                            ? 'bg-[#ea6c3b]'
                            : 'bg-slate-300'
                          : roleStat?.alive
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
                    {stageMode === 'auto' && !roleStat?.alive && (
                      <span className="text-red-500 font-semibold text-[10px] ml-0.5">(Mở)</span>
                    )}
                  </button>
                );
              })}
              {stageMode === 'manual' && (
                <button
                  type="button"
                  onClick={() => handleCopy(getDemoPassword(), 'header_pwd', 'Mật khẩu demo')}
                  title="Sao chép mật khẩu chung"
                  className="min-h-7 inline-flex items-center gap-1 px-2.5 py-1 bg-white hover:bg-orange-50 text-slate-700 border border-slate-200 text-xs font-mono font-semibold cursor-pointer shrink-0"
                >
                  <KeyRound className="size-3 text-[#ea6c3b]" />
                  <span>{copiedKey === 'header_pwd' ? 'Đã chép MK!' : 'MK: ••••'}</span>
                </button>
              )}
            </div>

            <div className="hidden xl:flex items-center gap-1.5 text-[11px] text-slate-500 shrink-0 font-mono tabular-nums">
              <span className="font-sans">Phím nhanh:</span>
              {stageMode === 'manual' ? (
                <>
                  <kbd className="px-1.5 py-0.5 bg-white border border-slate-200 font-bold text-slate-800">C</kbd>
                  <span className="font-sans">chép ô tiếp</span>
                  <AstryxKbd keys="1" />
                  <span>-</span>
                  <AstryxKbd keys="5" />
                  <span className="font-sans">chép ô 1–5</span>
                  <AstryxKbd keys="left" />
                  <AstryxKbd keys="right" />
                  <span className="font-sans">đổi bước</span>
                </>
              ) : (
                <>
                  <AstryxKbd keys="space" />
                  <span className="font-sans">chạy tiếp</span>
                  <AstryxKbd keys="left" />
                  <AstryxKbd keys="right" />
                  <span className="font-sans">đổi bước</span>
                  <AstryxKbd keys="1" />
                  <span>-</span>
                  <AstryxKbd keys="5" />
                  <span className="font-sans">nút con</span>
                </>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* =====================================================================
       * CHẾ ĐỘ XEM 2: BẢNG PHẲNG 1 TRANG (ALL-IN-ONE ZERO-SCROLL SHEET)
       * ===================================================================== */}
      {stageMode === 'manual' && manualSubView === 'sheet' ? (
        <main className="max-w-[1600px] mx-auto px-4 py-4 space-y-4">
          {/* Hàng 1: 6 Tài khoản + Link vào thẳng từng vai trò */}
          <AstryxCard padding={4} className="bg-white border border-slate-200 shadow-xs space-y-3">
            <div className="flex flex-wrap items-center justify-between gap-2">
              <div className="flex items-center gap-2">
                <span className="px-2 py-0.5 text-[11px] font-mono font-bold bg-orange-50 text-orange-900 border border-orange-200">
                  6 CANONICAL ROLES
                </span>
                <AstryxHeading level={2} className="text-sm sm:text-base font-bold text-slate-900">
                  Tài khoản Đăng nhập &amp; Trang Khởi điểm Theo Vai trò
                </AstryxHeading>
              </div>
              <button
                type="button"
                onClick={() => handleCopy(getDemoPassword(), 'sheet_pwd', 'Mật khẩu demo')}
                className="min-h-7 px-3 py-1 bg-[#ea6c3b] hover:bg-[#d95d2c] text-white text-xs font-mono font-bold inline-flex items-center gap-1.5 cursor-pointer"
              >
                <Copy className="size-3.5" />
                <span>Copy mật khẩu chung</span>
              </button>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-2.5">
              {CANONICAL_ROLES.map((r) => {
                const roleUrl = `${configIds.app_url}${resolveRoute(r.defaultRoute)}`;
                const emailKey = `sheet_role_${r.role}`;
                return (
                  <div key={r.role} className="p-3 bg-slate-50 border border-slate-200 flex flex-col justify-between gap-2">
                    <div>
                      <div className="flex items-center justify-between gap-1">
                        <span className="px-2 py-0.5 text-[11px] font-mono font-bold bg-orange-50 text-orange-900 border border-orange-200">
                          {r.role}
                        </span>
                        <span className="text-[11px] font-semibold text-slate-600">{r.shortLabel}</span>
                      </div>
                      <div className="text-xs font-bold text-slate-900 mt-1.5">{r.fullName}</div>
                      <div className="text-[11px] font-mono text-slate-600 truncate mt-0.5">{r.email}</div>
                    </div>
                    <div className="flex items-center gap-1.5 pt-1">
                      {r.role !== 'Guest' && (
                        <button
                          type="button"
                          onClick={() => handleCopy(r.email, emailKey, `Email ${r.role}`)}
                          className="min-h-7 px-2 py-1 flex-1 bg-white hover:bg-orange-50 border border-slate-200 text-[11px] font-semibold text-slate-800 inline-flex items-center justify-center gap-1 cursor-pointer"
                        >
                          {copiedKey === emailKey ? <Check className="size-3 text-emerald-600" /> : <Copy className="size-3" />}
                          <span>{copiedKey === emailKey ? 'Đã chép' : 'Chép Email'}</span>
                        </button>
                      )}
                      <a
                        href={roleUrl}
                        target="_blank"
                        rel="noreferrer"
                        className="min-h-7 px-2 py-1 flex-1 bg-white hover:bg-slate-100 border border-slate-200 text-[11px] font-semibold text-slate-700 inline-flex items-center justify-center gap-1"
                      >
                        <span>Mở trang</span>
                        <ExternalLink className="size-3 text-[#ea6c3b]" />
                      </a>
                    </div>
                  </div>
                );
              })}
            </div>
          </AstryxCard>

          {/* Hàng 2: Lưới Toàn Bộ Các Trường Dữ Liệu Cần Copy Xuyên Suốt B1 -> B12 */}
          <AstryxCard padding={4} className="bg-white border border-slate-200 shadow-xs space-y-3">
            <div className="flex flex-wrap items-center justify-between gap-2">
              <div className="flex items-center gap-2">
                <span className="px-2 py-0.5 text-[11px] font-mono font-bold bg-orange-50 text-orange-900 border border-orange-200">
                  B1 → B12 COPY SHEET
                </span>
                <AstryxHeading level={2} className="text-sm sm:text-base font-bold text-slate-900">
                  Toàn bộ Dữ liệu Nhập liệu Kịch bản Chính (Bấm 1 chạm để Sao chép)
                </AstryxHeading>
              </div>
              <span className="text-xs text-slate-600">
                Mẹo: Chạy <code className="font-mono">preload_clipboard_win_v.bat</code> trước buổi bảo vệ để nạp sẵn toàn bộ 10 ô này vào <strong>Win + V</strong>.
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {allMainCopyItems.map((item, idx) => {
                const val = customTexts[item.copyKey] ?? '';
                const cKey = `sheet_item_${item.copyKey}`;
                const done = Boolean(copiedHistory[cKey]);
                const active = copiedKey === cKey;
                return (
                  <div
                    key={item.copyKey}
                    className={`p-3.5 border space-y-2 transition-colors ${
                      active || done ? 'bg-emerald-50/60 border-emerald-400' : 'bg-white border-slate-200 hover:border-orange-300'
                    }`}
                  >
                    <div className="flex items-center justify-between gap-2">
                      <div className="flex items-center gap-1.5 min-w-0">
                        <span className="px-1.5 py-0.5 text-[11px] font-mono tabular-nums font-bold bg-slate-100 text-slate-800 border border-slate-200 shrink-0">
                          {idx + 1}. {item.step}
                        </span>
                        <span className="px-1.5 py-0.5 text-[10px] font-mono font-bold bg-orange-50 text-orange-800 border border-orange-200 shrink-0">
                          {item.role}
                        </span>
                        <span className="text-xs font-bold text-slate-900 truncate">{item.label}</span>
                      </div>
                      <button
                        type="button"
                        onClick={() => handleCopy(val, cKey, item.label)}
                        className={`min-h-7 px-2.5 py-1 text-xs font-bold border inline-flex items-center gap-1 shrink-0 cursor-pointer ${
                          active || done
                            ? 'bg-emerald-50 text-emerald-900 border-emerald-400'
                            : 'bg-[#ea6c3b] hover:bg-[#d95d2c] text-white border-[#ea6c3b]'
                        }`}
                      >
                        {active || done ? <Check className="size-3.5" /> : <Copy className="size-3.5" />}
                        <span>{active ? 'Đã chép!' : done ? 'Chép lại' : 'Sao chép'}</span>
                      </button>
                    </div>
                    <div
                      onClick={() => handleCopy(val, cKey, item.label)}
                      className="p-2.5 bg-slate-50 border border-slate-200 text-xs font-mono text-slate-800 whitespace-pre-wrap max-h-28 overflow-y-auto cursor-pointer leading-relaxed"
                    >
                      {val}
                    </div>
                    <div className="text-[11px] text-slate-600">{item.note}</div>
                  </div>
                );
              })}
            </div>
          </AstryxCard>

          {/* Hàng 3: Tóm tắt Lưu ý B9 / B10 / B11 + 15 Màn hình Q&A */}
          <div className="p-3.5 bg-amber-50 border border-amber-300 text-amber-900 text-xs leading-relaxed flex items-start gap-2.5">
            <AlertTriangle className="size-4 shrink-0 mt-0.5" />
            <div>
              <strong>Ba điểm chốt trên sân khấu (Lộc bấm máy · Trung thuyết trình):</strong> (1) Tại <strong>B9</strong>: Sau khi <code className="font-mono">Client</code> bấm Duyệt v2, quay về cửa sổ <code className="font-mono">Creator</code> trên <code className="font-mono">/editor</code> bấm nút cam <strong>"Gửi phê duyệt"</strong> để chốt <code className="font-mono">Task FINISHED</code> &amp; <code className="font-mono">Post APPROVED</code>. (2) Tại <strong>B10</strong>: Bấm Đăng ngay trên kênh thật đã nối OAuth (Facebook Fanpage / Threads) rồi mở tab thật đối chiếu. (3) Tại <strong>B11</strong>: Giới thiệu <code className="font-mono">Agency Plus = 990.000đ/tháng</code> rồi qua <code className="font-mono">/credit</code> nạp lẻ tùy chỉnh <strong>10 Credits = 2.000đ</strong> để quét VietQR ngân hàng thật.
            </div>
          </div>

          {renderQaGridSection(true)}
        </main>
      ) : stageMode === 'manual' && manualSubView === 'create' ? (
        /* ===================================================================
         * CHẾ ĐỘ XEM 3: 4 GÓI DỮ LIỆU DỰ PHÒNG "TẠO MỚI TẠI CHỖ" KHI HỎI XOÁY
         * =================================================================== */
        <main className="max-w-[1400px] mx-auto px-4 py-4 space-y-4">
          <AstryxCard padding={4} className="bg-white border border-slate-200 shadow-xs space-y-1.5">
            <div className="flex flex-wrap items-center justify-between gap-2">
              <div className="flex items-center gap-2">
                <span className="px-2 py-0.5 text-[11px] font-mono font-bold bg-orange-50 text-orange-900 border border-orange-200">
                  LIVE Q&amp;A BACKUP DATA
                </span>
                <AstryxHeading level={2} className="text-base font-bold text-slate-900">
                  Bộ Dữ liệu Mẫu Dự phòng Khi Hội đồng Yêu cầu "Tạo Mới Ngay Tại Chỗ"
                </AstryxHeading>
              </div>
              <button
                type="button"
                onClick={() => setManualSubView('step')}
                className="min-h-7 px-3 py-1 bg-white hover:bg-slate-50 border border-slate-200 text-xs font-semibold text-slate-700 cursor-pointer"
              >
                ← Quay lại kịch bản B1–B12
              </button>
            </div>
            <p className="text-xs text-slate-600">
              Toàn bộ nhãn trường dưới đây khớp chính xác 1-1 với biểu mẫu giao diện thực tế của <code className="font-mono">brandhub-web</code> (Chiến dịch, Công việc &amp; Subtask, Khảo sát học sinh, Đối tác truyền thông).
            </p>
          </AstryxCard>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {CREATE_LIVE_PACKS.map((pack) => {
              const packUrl = `${configIds.app_url}${resolveRoute(pack.routeTemplate)}`;
              return (
                <AstryxCard key={pack.id} padding={4} className="bg-white border border-slate-200 shadow-xs space-y-3">
                  <div className="flex flex-wrap items-start justify-between gap-2 border-b border-slate-100 pb-2.5">
                    <div className="space-y-1">
                      <div className="flex items-center gap-1.5">
                        <span className="px-2 py-0.5 text-[11px] font-mono font-bold bg-orange-50 text-orange-900 border border-orange-200">
                          {pack.role}: {pack.actorName}
                        </span>
                      </div>
                      <AstryxHeading level={3} className="text-sm sm:text-base font-bold text-slate-900">
                        {pack.title}
                      </AstryxHeading>
                      <p className="text-xs text-slate-600">{pack.whenAsked}</p>
                    </div>
                    <a
                      href={packUrl}
                      target="_blank"
                      rel="noreferrer"
                      className="min-h-7 px-2.5 py-1 bg-slate-50 hover:bg-orange-50 border border-slate-200 text-xs font-semibold text-slate-800 inline-flex items-center gap-1 shrink-0"
                    >
                      <span>Mở màn hình</span>
                      <ExternalLink className="size-3 text-[#ea6c3b]" />
                    </a>
                  </div>

                  <div className="p-2.5 bg-slate-50 border border-slate-200 space-y-1">
                    <div className="text-[11px] font-bold text-slate-700 uppercase">Trình tự bấm trên giao diện:</div>
                    {pack.steps.map((st, idx) => (
                      <div key={idx} className="text-xs text-slate-700 leading-relaxed flex items-start gap-1.5">
                        <span className="font-mono tabular-nums font-bold text-[#ea6c3b]">{idx + 1}.</span>
                        <span>{st}</span>
                      </div>
                    ))}
                  </div>

                  <div className="space-y-2">
                    {pack.fields.map((fld) => {
                      const fKey = `pack_${pack.id}_${fld.id}`;
                      const isCopied = copiedKey === fKey;
                      const done = Boolean(copiedHistory[fKey]);
                      return (
                        <div
                          key={fld.id}
                          className={`p-3 border space-y-1.5 ${
                            isCopied || done ? 'bg-emerald-50/60 border-emerald-400' : 'bg-white border-slate-200'
                          }`}
                        >
                          <div className="flex items-center justify-between gap-2">
                            <span className="text-xs font-bold text-slate-900">{fld.label}</span>
                            <button
                              type="button"
                              onClick={() => handleCopy(fld.value, fKey, fld.label)}
                              className={`min-h-7 px-2.5 py-1 text-xs font-bold border inline-flex items-center gap-1 cursor-pointer ${
                                isCopied || done
                                  ? 'bg-emerald-50 text-emerald-900 border-emerald-400'
                                  : 'bg-[#ea6c3b] hover:bg-[#d95d2c] text-white border-[#ea6c3b]'
                              }`}
                            >
                              {isCopied || done ? <Check className="size-3" /> : <Copy className="size-3" />}
                              <span>{isCopied ? 'Đã chép!' : done ? 'Chép lại' : 'Sao chép'}</span>
                            </button>
                          </div>
                          <div
                            onClick={() => handleCopy(fld.value, fKey, fld.label)}
                            className="p-2 bg-slate-50 border border-slate-200 text-xs font-mono text-slate-800 whitespace-pre-wrap cursor-pointer leading-relaxed"
                          >
                            {fld.value}
                          </div>
                          {fld.note && <div className="text-[11px] text-slate-600">{fld.note}</div>}
                        </div>
                      );
                    })}
                  </div>
                </AstryxCard>
              );
            })}
          </div>
        </main>
      ) : (
        /* ===================================================================
         * CHẾ ĐỘ XEM 1 (MẶC ĐỊNH): SIDEBAR DỌC B0–B12 + BƯỚC HIỆN TẠI
         * =================================================================== */
        <div className="flex items-start">
          {/* Sidebar dọc B0 -> B12 (tuân thủ 1px border discipline, không dùng border-l-4) */}
          <nav
            aria-label={`Danh sách ${MAIN_STEPS_COUNT} bước demo`}
            className="hidden lg:block w-[280px] shrink-0 self-start sticky top-0 max-h-dvh overflow-y-auto border-r border-slate-200 bg-white"
          >
            <div className="divide-y divide-slate-100">
              {DEMO_STEPS.map((step, idx) => {
                const isSelected = idx === activeStepIndex;
                const isDone =
                  stageMode === 'manual'
                    ? step.manualChecklist.length > 0 &&
                      step.manualChecklist.every((_, cIdx) => Boolean(manualCheckDone[`${step.code}_chk_${cIdx}`]))
                    : step.actions.every((a) => Boolean(doneActions[a.id]));
                const hasSomeDone =
                  !isDone &&
                  (stageMode === 'manual'
                    ? step.manualChecklist.some((_, cIdx) => Boolean(manualCheckDone[`${step.code}_chk_${cIdx}`]))
                    : step.actions.some((a) => Boolean(doneActions[a.id])));
                return (
                  <button
                    key={step.code}
                    ref={isSelected ? activePillRef : null}
                    type="button"
                    onClick={() => selectStepWithSync(idx)}
                    title={`${step.code}: ${step.title} (${step.role})`}
                    className={`min-h-7 w-full flex items-start gap-2.5 px-3.5 py-2.5 text-left cursor-pointer transition-colors ${
                      isSelected
                        ? 'bg-orange-50'
                        : hasSomeDone
                        ? 'bg-slate-50 hover:bg-slate-100'
                        : 'bg-white hover:bg-slate-50'
                    }`}
                  >
                    <span
                      className={`px-1.5 py-0.5 font-mono tabular-nums text-[11px] font-bold shrink-0 mt-0.5 border ${
                        isSelected
                          ? 'bg-[#ea6c3b] text-white border-[#ea6c3b]'
                          : isDone
                          ? 'bg-emerald-50 text-emerald-800 border-emerald-300'
                          : 'bg-slate-100 text-slate-600 border-slate-200'
                      }`}
                    >
                      {isDone ? <Check className="size-3" aria-hidden="true" /> : step.code}
                    </span>
                    <span className="min-w-0 flex-1">
                      <span
                        className={`block text-xs leading-snug text-pretty ${
                          isSelected
                            ? 'font-bold text-orange-950'
                            : isDone
                            ? 'font-medium text-slate-600'
                            : 'font-medium text-slate-700'
                        }`}
                      >
                        {step.shortTitle}
                      </span>
                      <span className="block text-[11px] font-mono tabular-nums text-slate-500 mt-0.5">
                        {step.role} · {step.timeBudget}
                      </span>
                    </span>
                  </button>
                );
              })}
            </div>
          </nav>

          <main className="flex-1 min-w-0 max-w-[1060px] mx-auto px-4 py-4 space-y-4">
            {/* Thanh chọn bước rút gọn cho màn hình nhỏ (<lg) */}
            <div className="lg:hidden flex items-center gap-1.5 overflow-x-auto no-scrollbar pb-1">
              {DEMO_STEPS.map((step, idx) => (
                <button
                  key={step.code}
                  type="button"
                  onClick={() => selectStepWithSync(idx)}
                  className={`min-h-7 px-2.5 py-1 text-xs font-mono tabular-nums font-bold border shrink-0 cursor-pointer ${
                    idx === activeStepIndex
                      ? 'bg-[#ea6c3b] text-white border-[#ea6c3b]'
                      : 'bg-white text-slate-700 border-slate-200'
                  }`}
                >
                  {step.code}
                </button>
              ))}
            </div>

            {/* Thẻ chính của bước hiện tại */}
            <AstryxCard padding={4} className="bg-white border border-slate-200 shadow-xs space-y-4">
              {/* Hàng 1: Định danh Bước + Báo đổi vai + Nút Trước/Tiếp */}
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div className="space-y-1.5 min-w-0 flex-1">
                  <div className="flex flex-wrap items-center gap-1.5">
                    <span className="px-2 py-0.5 text-xs font-mono tabular-nums font-bold bg-slate-100 text-slate-800 border border-slate-200">
                      {currentStep.stepNumber === 0
                        ? `Chuẩn bị · ${currentStep.code}`
                        : `Bước ${currentStep.stepNumber}/${MAIN_STEPS_COUNT} · ${currentStep.code}`}
                    </span>
                    <span className="px-2 py-0.5 text-xs font-semibold bg-orange-50 text-orange-900 border border-orange-200">
                      {currentStep.role}: {currentStep.actorName}
                    </span>
                    <span className="px-2 py-0.5 text-xs font-mono tabular-nums font-medium bg-slate-50 text-slate-600 border border-slate-200">
                      Khung giờ: {currentStep.timeBudget}
                    </span>
                    <span className="px-2 py-0.5 text-xs font-mono tabular-nums font-medium bg-slate-50 text-slate-600 border border-slate-200">
                      {currentStep.frCode}
                    </span>
                    {roleChangedFromPrev && (
                      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 text-xs font-bold bg-amber-50 text-amber-900 border border-amber-300">
                        Chuyển cửa sổ sang {currentStep.role}
                      </span>
                    )}
                  </div>

                  <AstryxHeading level={2} className="text-lg sm:text-xl font-bold text-slate-900 text-balance">
                    {currentStep.title}
                  </AstryxHeading>

                  {/* Đường dẫn trang đích + Các link phụ trong bước */}
                  {currentStep.routeTemplate && (
                    <div className="flex flex-wrap items-center gap-1.5 text-xs text-slate-500 pt-0.5">
                      <span className="font-medium">Trang đích ({currentStep.role}):</span>
                      <a
                        href={`${configIds.app_url}${resolvedRoute}`}
                        target="_blank"
                        rel="noreferrer"
                        className="min-h-7 inline-flex items-center gap-1.5 px-2.5 py-1 bg-slate-50 hover:bg-slate-100 text-slate-700 border border-slate-200 font-mono"
                      >
                        <span>{resolvedRoute}</span>
                        <ExternalLink className="size-3 shrink-0 text-slate-500" />
                      </a>
                      <button
                        type="button"
                        onClick={handleSyncCurrentStepRoute}
                        disabled={busyAction !== null}
                        title={
                          stageMode === 'manual'
                            ? 'Sao chép đường dẫn đầy đủ để dán lên cửa sổ Chrome của vai trò tương ứng'
                            : 'Đưa ngay cửa sổ Chrome của vai trò này tới đúng trang đích'
                        }
                        className="min-h-7 inline-flex items-center gap-1 px-2.5 py-1 bg-white hover:bg-orange-50 text-slate-700 hover:text-orange-950 border border-slate-200 text-xs font-semibold cursor-pointer transition-colors"
                      >
                        {stageMode === 'manual' ? (
                          <>
                            <Copy className="size-3 text-[#ea6c3b]" />
                            <span>Copy URL</span>
                          </>
                        ) : (
                          <>
                            <Compass className="size-3 text-[#ea6c3b]" />
                            <span>Đồng bộ Chrome</span>
                          </>
                        )}
                      </button>

                      {currentStep.extraRoutes?.map((er, erIdx) => {
                        const erPath = resolveRoute(er.routeTemplate);
                        return (
                          <a
                            key={erIdx}
                            href={`${configIds.app_url}${erPath}`}
                            target="_blank"
                            rel="noreferrer"
                            title={`Mở ${er.label} (${er.role}): ${erPath}`}
                            className="min-h-7 inline-flex items-center gap-1 px-2.5 py-1 bg-orange-50/60 hover:bg-orange-100 text-orange-950 border border-orange-200 text-xs font-semibold"
                          >
                            <span>{er.label}</span>
                            <ExternalLink className="size-3 shrink-0 text-[#ea6c3b]" />
                          </a>
                        );
                      })}
                    </div>
                  )}
                </div>

                <div className="flex flex-wrap items-center gap-1.5 shrink-0">
                  <button
                    type="button"
                    onClick={handleResetCurrentStep}
                    title="Xóa dấu tích đã làm của bước hiện tại"
                    className="min-h-7 inline-flex items-center gap-1 px-2.5 py-1 bg-white hover:bg-slate-50 border border-slate-200 text-xs font-semibold text-slate-700 cursor-pointer transition-colors"
                  >
                    <RotateCcw className="size-3 text-slate-600" />
                    <span className="hidden sm:inline">Đặt lại bước</span>
                  </button>
                  <button
                    type="button"
                    onClick={handleCopyAllStepData}
                    title="Sao chép toàn bộ dữ liệu mẫu của bước này vào Clipboard"
                    className="min-h-7 inline-flex items-center gap-1 px-2.5 py-1 bg-white hover:bg-slate-50 border border-slate-200 text-xs font-semibold text-slate-700 cursor-pointer transition-colors"
                  >
                    <ClipboardCheck className="size-3 text-slate-600" />
                    <span className="hidden sm:inline">Chép cả bước</span>
                  </button>
                  <AstryxButton
                    label="← Trước"
                    variant="secondary"
                    size="sm"
                    isDisabled={activeStepIndex === 0}
                    onClick={() => selectStepWithSync((i) => Math.max(0, i - 1))}
                  />
                  <AstryxButton
                    label="Tiếp →"
                    variant="secondary"
                    size="sm"
                    isDisabled={activeStepIndex === DEMO_STEPS.length - 1}
                    onClick={() => selectStepWithSync((i) => Math.min(DEMO_STEPS.length - 1, i + 1))}
                  />
                </div>
              </div>

              {/* Cảnh báo bẫy thao tác tay (nếu bước này có điểm hiểm như B4, B9, B10) */}
              {currentStep.trapWarning && (
                <div className="p-3 bg-amber-50 border border-amber-300 text-amber-900 text-xs sm:text-sm leading-relaxed flex items-start gap-2.5">
                  <AlertTriangle className="size-4 shrink-0 mt-0.5" />
                  <div>
                    <strong className="font-bold">Lưu ý quan trọng trên sân khấu: </strong>
                    <span>{currentStep.trapWarning}</span>
                  </div>
                </div>
              )}

              {/* PHẦN NỘI DUNG KHÁC BIỆT THEO CHẾ ĐỘ: MANUAL COPY-KIT vs AUTO */}
              {stageMode === 'manual' ? (
                <div className="space-y-4">
                  {/* Thanh hành động nhanh Copy tiếp theo (Phím C) */}
                  <div className="p-3 bg-slate-50 border border-slate-200 flex flex-wrap items-center justify-between gap-3">
                    <div className="min-w-0 flex-1">
                      <div className="text-[11px] font-bold uppercase text-slate-600">
                         Sao chép nhanh dữ liệu chuẩn của {currentStep.code} (Phím C hoặc bấm trực tiếp vào thẻ)
                      </div>
                      <div className="text-xs sm:text-sm font-semibold text-slate-800 mt-0.5">
                        Mỗi lần nhấn phím <strong className="font-mono">C</strong> sẽ tự động chép ô tiếp theo chưa dùng trong bước này để bạn sang Chrome nhấn <strong className="font-mono">Ctrl + V</strong>.
                      </div>
                    </div>
                    <div className="flex items-center gap-2 shrink-0">
                      <button
                        type="button"
                        onClick={handleCopyNextStepField}
                        className="min-h-7 inline-flex items-center gap-2 px-4 py-2 bg-[#ea6c3b] hover:bg-[#d95d2c] text-white font-bold text-xs sm:text-sm border border-[#ea6c3b] cursor-pointer transition-colors"
                      >
                        <Copy className="size-4 shrink-0" />
                        <span>Chép ô tiếp theo</span>
                        <span className="bg-white/20 text-white px-1.5 py-0.5 text-[11px] font-mono">C</span>
                      </button>
                      {activeStepIndex < DEMO_STEPS.length - 1 && (
                        <button
                          type="button"
                          onClick={() => selectStepWithSync((i) => Math.min(DEMO_STEPS.length - 1, i + 1))}
                          className="min-h-7 inline-flex items-center gap-1.5 px-3.5 py-2 bg-white hover:bg-slate-100 text-slate-800 font-bold text-xs sm:text-sm border border-slate-200 cursor-pointer"
                        >
                          <span>Qua {DEMO_STEPS[activeStepIndex + 1].code}</span>
                          <ArrowRight className="size-4 text-[#ea6c3b]" />
                        </button>
                      )}
                    </div>
                  </div>

                  {/* Các thẻ Dữ liệu Copy 1 chạm được mở nổi bật ngay trước mắt */}
                  <div className="space-y-2">
                    <div className="text-xs font-bold uppercase text-slate-700">
                      Trường dữ liệu chuẩn bước {currentStep.code} ({currentStep.fields.length} mục)
                    </div>
                    {renderStepFieldsCards()}
                  </div>

                  {/* Checklist thao tác tay từng bước (bấm để gạch dấu đã xong) */}
                  <div className="space-y-2">
                    <div className="text-xs font-bold uppercase text-slate-700">
                      Trình tự thao tác trên trình duyệt ({currentStep.role})
                    </div>
                    <div className="divide-y divide-slate-100 border border-slate-200 bg-white">
                      {currentStep.manualChecklist.map((line, cIdx) => {
                        const chkKey = `${currentStep.code}_chk_${cIdx}`;
                        const checked = Boolean(manualCheckDone[chkKey]);
                        return (
                          <button
                            key={chkKey}
                            type="button"
                            onClick={() => setManualCheckDone((prev) => ({ ...prev, [chkKey]: !prev[chkKey] }))}
                            className={`min-h-7 w-full px-3.5 py-2.5 text-left flex items-start gap-2.5 cursor-pointer transition-colors ${
                              checked ? 'bg-slate-50 text-slate-500' : 'bg-white hover:bg-slate-50 text-slate-800'
                            }`}
                          >
                            <span
                              className={`size-5 font-mono tabular-nums text-xs font-bold border inline-flex items-center justify-center shrink-0 mt-0.5 ${
                                checked
                                  ? 'bg-emerald-50 text-emerald-800 border-emerald-300'
                                  : 'bg-orange-50 text-orange-900 border-orange-200'
                              }`}
                            >
                              {checked ? <Check className="size-3" aria-hidden="true" /> : cIdx + 1}
                            </span>
                            <span className={`text-xs sm:text-sm leading-relaxed ${checked ? 'line-through' : 'font-medium'}`}>
                              {line}
                            </span>
                          </button>
                        );
                      })}
                    </div>
                  </div>
                </div>
              ) : (
                /* GIAO DIỆN ĐIỀU KHIỂN TỰ ĐỘNG (AUTO MODE) */
                <>
                  <div className="p-3 bg-slate-50 border border-slate-200 flex flex-wrap items-center justify-between gap-3">
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
                          : `Đã hoàn thành trọn vẹn cả ${MAIN_STEPS_COUNT} bước thuyết trình!`}
                      </div>
                    </div>

                    <div className="flex items-center gap-2">
                      {busyAction !== null && (
                        <button
                          type="button"
                          onClick={handleCancelBusy}
                          className="min-h-7 px-3 py-2 bg-red-600 hover:bg-red-700 text-white font-bold text-xs shadow-xs cursor-pointer transition-colors"
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
                        className="min-h-7 inline-flex items-center gap-2.5 px-5 py-2.5 bg-[#ea6c3b] hover:bg-[#d95d2c] text-white font-bold text-xs sm:text-sm border border-[#ea6c3b] shadow-xs cursor-pointer transition-colors disabled:opacity-50"
                      >
                        {busyAction !== null ? (
                          <RefreshCw className="size-4 animate-spin" />
                        ) : nextPendingAction ? (
                          <Play className="size-4" />
                        ) : (
                          <ArrowRight className="size-4" />
                        )}
                        <span className="font-mono tabular-nums">
                          {nextPendingAction
                            ? `Thực thi ngay (${
                                currentStep.actions.findIndex((a) => a.id === nextPendingAction.id) + 1
                              }/${currentStep.actions.length})`
                            : activeStepIndex < DEMO_STEPS.length - 1
                            ? `Sang bước ${DEMO_STEPS[activeStepIndex + 1].code} →`
                            : `Đã hoàn tất ${MAIN_STEPS_COUNT}/${MAIN_STEPS_COUNT}`}
                        </span>
                        <span className="bg-white/20 text-white px-1.5 py-0.5 text-[11px] font-mono">Space</span>
                      </button>
                    </div>
                  </div>

                  {/* Các nút hành động đánh số [1]..[5] */}
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
                          className={`min-h-7 p-3.5 border text-left flex items-start gap-3 cursor-pointer transition-colors ${
                            isNextRecommended
                              ? 'bg-orange-50/60 text-slate-900 border-orange-400 hover:bg-orange-50 shadow-xs'
                              : isDone
                              ? 'bg-slate-50 text-slate-600 border-slate-200'
                              : 'bg-white text-slate-900 border-slate-200 hover:border-orange-300 hover:bg-slate-50'
                          }`}
                        >
                          <div
                            className={`size-8 shrink-0 flex items-center justify-center font-mono tabular-nums font-extrabold text-sm ${
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
                                className={`px-2 py-0.5 font-mono tabular-nums text-[10px] font-bold shrink-0 whitespace-nowrap ${
                                  isNextRecommended
                                    ? 'bg-orange-100 text-orange-900 border border-orange-200'
                                    : isDone
                                    ? 'bg-slate-200 text-slate-700'
                                    : 'bg-slate-100 text-slate-600'
                                }`}
                              >
                                {isNextRecommended ? `Phím ${numKey} · Tiếp` : isDone ? 'Đã chạy' : `Phím ${numKey}`}
                              </span>
                            </div>
                            <div className="text-xs mt-1 leading-relaxed text-slate-600">
                              {formatReadableDescription(act.description)}
                            </div>
                          </div>
                        </button>
                      );
                    })}
                  </div>

                  {/* CHROME CUE */}
                  <div className="px-3.5 py-2.5 bg-slate-50 border border-slate-200 flex items-start gap-2.5">
                    <span className="px-1.5 py-0.5 text-[10px] font-bold bg-orange-100 text-orange-900 border border-orange-200 shrink-0 mt-0.5 font-mono">
                      CHROME CUE
                    </span>
                    <div className="text-xs sm:text-sm text-slate-800 leading-relaxed text-pretty">
                      <strong className="text-slate-900 font-bold">Tóm tắt luồng: </strong>
                      <span className="text-slate-700">{currentStep.manualBrowserCue}</span>
                    </div>
                  </div>
                </>
              )}

              <AstryxDivider variant="subtle" />

              {/* Máy nhắc chữ sân khấu (Teleprompter) */}
              <div className="space-y-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="text-xs font-bold uppercase text-slate-700">
                    Ý chính trình bày trước Hội đồng ({currentStep.code})
                  </div>
                  {(Object.keys(doneActions).length > 0 ||
                    Object.keys(copiedHistory).length > 0 ||
                    Object.keys(manualCheckDone).length > 0) && (
                    <button
                      type="button"
                      onClick={() => {
                        setDoneActions({});
                        setCopiedHistory({});
                        setManualCheckDone({});
                      }}
                      className="min-h-7 px-2.5 py-1 inline-flex items-center bg-white hover:bg-slate-50 border border-slate-200 text-xs font-semibold text-slate-600 hover:text-orange-800 cursor-pointer"
                    >
                      Xóa dấu tích đã làm
                    </button>
                  )}
                </div>

                <div className="grid grid-cols-1 gap-2">
                  {currentStep.talkingPoints.map((pt, i) => (
                    <div
                      key={i}
                      className="px-3.5 py-2.5 bg-slate-50 border border-slate-200 text-sm leading-relaxed flex items-start gap-2.5"
                    >
                      <span className="size-5 bg-orange-100 text-orange-900 border border-orange-200 font-mono tabular-nums text-xs font-bold shrink-0 mt-0.5 flex items-center justify-center">
                        {i + 1}
                      </span>
                      <span className="text-pretty font-medium text-slate-800">{pt}</span>
                    </div>
                  ))}
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-3 pt-1">
                  <div className="md:col-span-2 p-3.5 bg-white border border-slate-200 space-y-1">
                    <div className="text-[11px] font-bold text-slate-500 uppercase">Lời dẫn gợi ý đầy đủ</div>
                    <p className="text-sm text-slate-700 leading-relaxed text-pretty">{currentStep.presenterScript}</p>
                  </div>
                  <div className="p-3.5 bg-slate-50 border border-slate-200 space-y-1">
                    <div className="text-[11px] font-bold text-slate-600 uppercase">Kết quả trên màn hình</div>
                    <p className="text-xs text-slate-600 leading-relaxed text-pretty">{currentStep.expectedOutcome}</p>
                  </div>
                </div>
              </div>
            </AstryxCard>

            {/* Trong chế độ Auto vẫn có ngăn mở nhanh các thẻ Copy dự phòng */}
            {stageMode === 'auto' && (
              <AstryxCard padding={4} className="bg-white border border-slate-200 shadow-xs">
                <AstryxCollapsible
                  defaultIsOpen={false}
                  trigger={
                    <div className="flex flex-wrap items-center justify-between gap-2 pr-2 min-h-7">
                      <span className="text-xs sm:text-sm font-bold text-slate-800">
                        Dữ liệu điền tự động &amp; Sao chép thủ công dự phòng ({currentStep.fields.length} mục)
                      </span>
                      <span className="px-2 py-0.5 text-[11px] font-medium bg-slate-100 text-slate-600 border border-slate-200">
                        Bấm để mở hoặc nhấn phím C để chép nhanh
                      </span>
                    </div>
                  }
                >
                  <div className="pt-3">{renderStepFieldsCards()}</div>
                </AstryxCollapsible>
              </AstryxCard>
            )}

            {/* Ngăn Truy cập nhanh Q&A Hội đồng: 15 Màn hình Chuyên sâu */}
            {renderQaGridSection(false)}

            {/* Chân trang sạch sẽ theo từng chế độ */}
            <div className="px-4 py-3 bg-slate-50 border border-slate-200 flex flex-wrap items-center justify-between gap-3 text-xs text-slate-600">
              {stageMode === 'manual' ? (
                <>
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-slate-700">SE08 Digital Agency × Trường Đại học FPT</span>
                    <span>•</span>
                    <span>Hồ sơ dữ liệu kịch bản thực nghiệm (6 Canonical Roles · 141 FRs)</span>
                  </div>
                  <a
                    href="/demo/brandhub_manual_demo_kit.html"
                    target="_blank"
                    rel="noreferrer"
                    className="min-h-7 px-2.5 py-1 bg-white border border-slate-200 font-semibold text-[#ea6c3b] hover:underline inline-flex items-center gap-1"
                  >
                    <span>Mở bản HTML độc lập (Offline)</span>
                    <ExternalLink className="size-3.5" />
                  </a>
                </>
              ) : (
                <>
                  <div className="flex items-center gap-2">
                    <span className="font-mono font-semibold text-slate-700">Control Bridge (:3999)</span>
                    <span>•</span>
                    <span>Bàn điều khiển thuyết trình BrandHub SE08</span>
                  </div>
                  <a
                    href="http://localhost:3999"
                    target="_blank"
                    rel="noreferrer"
                    className="min-h-7 px-2.5 py-1 bg-white border border-slate-200 font-semibold text-[#ea6c3b] hover:underline inline-flex items-center gap-1"
                  >
                    <span>Mở giao diện cổng :3999</span>
                    <ExternalLink className="size-3.5" />
                  </a>
                </>
              )}
            </div>
          </main>
        </div>
      )}
    </div>
  );
};

export default DemoMonitorPage;
