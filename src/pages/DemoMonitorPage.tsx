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
  violation_sample:
    '\n\n[Đoạn văn kiểm thử bộ lọc an toàn]: Cam kết 100% việc làm lương ngàn đô ngay khi nhập học, tuyển thẳng không cần điều kiện, các nơi khác đều là bằng cấp vô giá trị!',
  caption_v1_clean:
    'TỪ SÂN TRƯỜNG THPT ĐẾN PHÒNG LAB CÔNG NGHỆ CAO: MỞ ĐĂNG KÝ XÉT HỌC BỔNG ĐẠI HỌC FPT 2027\n\nSau chuỗi Workshop phổ biến tiện ích học đường sôi nổi tại các trường THPT, hàng trăm bạn học sinh lớp 12 đã trực tiếp đeo kính VR khám phá khuôn viên 5 cơ sở, điều khiển cánh tay Robotics và trò chuyện cùng giảng viên ngành Thiết kế Vi mạch bán dẫn, Trí tuệ nhân tạo (AI).\n\nHệ sinh thái học tập thực tiễn đang chờ đón tân sinh viên khóa K23 tại Trường Đại học FPT:\n- Môi trường học tập hiện đại tại Hà Nội, Đà Nẵng, Quy Nhơn, TP.HCM và Cần Thơ với thư viện xanh, ký túc xá tiện nghi, sân Vovinam và hơn 40 CLB sinh viên.\n- Giáo trình chuẩn quốc tế, chú trọng tiếng Anh và kỹ năng làm việc trong dự án công nghệ thực tế.\n- Cổng nhận hồ sơ đăng ký xét Học bổng Nguyễn Văn Đạo đợt 1 năm 2027 đã chính thức mở.\n\nĐăng ký tư vấn và nộp hồ sơ trực tuyến tại: https://tuyensinh.fpt.edu.vn\n#DaiHocFPT #TuyenSinhFPTU2027 #WorkshopTHPT #HocBongNguyenVanDao #ViMachBanDan #FPTUniversity',
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
    code: 'B1',
    stage: 'Giai đoạn 1: Gói truyền thông Đa lĩnh vực & Chiến dịch 4 tuần',
    stageShort: 'GĐ 1: Gói & Chiến dịch',
    timeBudget: '00:00 - 01:15',
    title: 'Danh mục 7 Gói truyền thông Đa lĩnh vực & Gói Tuyển sinh ĐH FPT 2027',
    shortTitle: '7 Gói đa ngành & Gói ĐH FPT',
    frCode: 'FR 3.5.1 - 3.5.4',
    role: 'Owner',
    actorName: 'Lê Trí Trung',
    actorEmail: 'user177@demo.brandhub.test',
    routeTemplate: '/agency/{agency_id}/media-packages',
    manualBrowserCue:
      'Bấm [1] lướt qua 7 thẻ gói đa lĩnh vực của SE08 -> Bấm [2] mở gói Tuyển sinh ĐH FPT 2027 (185 triệu VNĐ, 19 hạng mục) đã chốt trong Workspace.',
    talkingPoints: [
      'SE08 Digital Agency chuẩn hóa sẵn 7 gói truyền thông chuyên biệt cho Giáo dục, SaaS, F&B, BĐS, Mỹ phẩm, TMĐT và Du lịch.',
      'Mỗi lĩnh vực định nghĩa cơ cấu loại bài đặc thù riêng, tuân thủ 7 loại dịch vụ chuẩn của hệ thống.',
      'Gói trọng tâm cho Đại học FPT mùa tuyển sinh 2027 kéo dài 4 tuần (185 triệu VNĐ) gồm 19 hạng mục từ bài Social, Reels, Workshop THPT đến PR báo chí.',
    ],
    presenterScript:
      'Đầu tiên, trong vai trò Owner Lê Trí Trung của SE08 Digital Agency, chúng em xây dựng bộ danh mục 7 gói truyền thông chuẩn hóa trên nhiều lĩnh vực từ Giáo dục, Công nghệ SaaS, F&B, Bất động sản đến Dược mỹ phẩm, Thương mại điện tử và Du lịch. Riêng với khách hàng Trường Đại học FPT mùa tuyển sinh 2027, chúng em thiết kế gói chiến dịch 4 tuần gồm 19 hạng mục: 08 bài đa nền tảng, 03 video ngắn Reels/TikTok, 02 bài PR báo chí chính thống, 02 buổi Workshop phổ biến tiện ích học đường tại trường THPT, 01 kế hoạch Ngày hội FPTU Open Day, 02 hạng mục KOL công nghệ và 01 bản tin Email.',
    expectedOutcome:
      'Hiển thị đầy đủ 7 thẻ Gói truyền thông đa lĩnh vực ở trạng thái ACTIVE cùng lịch sử thương thảo và phê duyệt gói 185 triệu VNĐ với Ban Tuyển sinh ĐH FPT.',
    fields: [
      {
        field: 'Gói trọng tâm gắn cho Đại học FPT (185.000.000 VNĐ / 4 tuần)',
        actionType: 'Tự động điền sẵn',
        value:
          'Gói Tuyển sinh Đại học FPT 2027: Chiến dịch Đa kênh & Chuỗi Workshop 4 Tuần (19 hạng mục thuộc đủ 7 loại dịch vụ chuẩn)',
        note: 'Bao phủ trọn vẹn từ bài Coming Soon, giới thiệu ngành học, chuỗi Workshop THPT đến PR báo chí',
      },
      {
        field: '6 Gói truyền thông đa lĩnh vực khác trong danh mục của SE08',
        actionType: 'Tự động điền sẵn',
        value:
          '1. Công nghệ & Giải pháp B2B SaaS | 2. F&B & Chuỗi cửa hàng đồ uống | 3. Bất động sản Đô thị & Nghỉ dưỡng | 4. Dược mỹ phẩm & Chăm sóc sức khỏe | 5. Thương mại điện tử Mega Sale | 6. Du lịch & Nghỉ dưỡng Biển Đà Nẵng - Hội An',
        note: 'Mỗi gói có 5-6 hạng mục mang đặc trưng riêng của từng ngành',
      },
    ],
    actions: [
      {
        id: 'B1_NAV',
        label: 'Mở Danh mục 7 Gói truyền thông đa lĩnh vực',
        description: 'Mở /agency/{agency_id}/media-packages trên cửa sổ Owner (Lê Trí Trung)',
        variant: 'primary',
        icon: <Play className="size-4" />,
      },
      {
        id: 'B1_NAV_WS_PACKAGE',
        label: 'Mở Gói ĐH FPT 2027 đã thương thảo trong Workspace',
        description: 'Xem gói 185 triệu VNĐ (19 hạng mục) đã được Ban Tuyển sinh ĐH FPT phê duyệt',
        variant: 'outline',
        icon: <Layers className="size-4" />,
      },
    ],
  },
  {
    stepNumber: 2,
    code: 'B2',
    stage: 'Giai đoạn 1: Gói truyền thông Đa lĩnh vực & Chiến dịch 4 tuần',
    stageShort: 'GĐ 1: Gói & Chiến dịch',
    timeBudget: '01:15 - 02:30',
    title: 'Workspace ĐH FPT 2027, Thư viện 7 Key Visual Gemini & Chat nhóm',
    shortTitle: 'Workspace, Thư viện KV & Chat',
    frCode: 'FR 3.4.9, 3.4.21, 3.5.5, 3.6.25',
    role: 'Owner',
    actorName: 'Lê Trí Trung',
    actorEmail: 'user177@demo.brandhub.test',
    routeTemplate: '/workspaces/{workspace_id}/members',
    manualBrowserCue:
      'Bấm lần lượt [1] -> [2] -> [3] -> [4] (hoặc phím Space) để lướt qua đội ngũ 5 thành viên SE08, Brand Profile ĐH FPT, 4 thư mục ảnh Gemini trong /library và trao đổi nhóm /chat.',
    talkingPoints: [
      'Workspace quy tụ đủ 5 thành viên nhóm SE08 (Trung, Lộc, Phước, Tuấn, Ân) làm việc trực tiếp cùng Ban Tuyển sinh Đại học FPT.',
      'Brand Profile lưu sẵn thông tin 5 cơ sở, kỳ thực tập OJT, tài liệu RAG và danh sách từ ngữ hạn chế.',
      'Thư viện /library đã chia sẵn 4 thư mục tuần chứa 7 bộ Key Visual tạo bằng Gemini Nano Banana, 4 ảnh thực tế khuôn viên trường và 5 mẫu bài viết.',
    ],
    presenterScript:
      'Khi Ban Tuyển sinh Đại học FPT đồng thuận thỏa thuận gói dịch vụ, toàn bộ đội ngũ 5 thành viên SE08 Digital Agency gồm Lê Trí Trung, Nguyễn Thành Lộc, Nguyễn Chơn Phước, Nguyễn Minh Tuấn và Hà Văn Ân cùng làm việc trực tiếp với khách hàng trong một Workspace thống nhất. Tại đây, Hồ sơ thương hiệu lưu sẵn quy chuẩn tuyển sinh, còn Thư viện tài nguyên chia sẵn 4 thư mục theo từng tuần cùng 7 ấn phẩm Key Visual thiết kế bằng Gemini Nano Banana để sẵn sàng gắn vào bài viết.',
    expectedOutcome:
      'Hiển thị thành viên nhóm SE08 trong Workspace, Hồ sơ thương hiệu Đại học FPT, 11 ấn phẩm hình ảnh hiển thị trực tiếp trong /library và lịch sử trao đổi công việc trong /chat.',
    fields: [
      {
        field: 'Đội ngũ SE08 Digital Agency & Khách hàng trong Workspace',
        actionType: 'Tự động điền sẵn',
        value:
          'Owner: Lê Trí Trung | Manager: Nguyễn Thành Lộc | 3 Creator: Nguyễn Chơn Phước, Nguyễn Minh Tuấn, Hà Văn Ân | Client: Ban Tuyển sinh Đại học FPT',
      },
      {
        field: 'Thư viện hình ảnh chiến dịch (/library)',
        actionType: 'Tự động điền sẵn',
        value:
          '4 Thư mục Tuần 1 -> Tuần 4 chứa 7 ảnh Key Visual Gemini Nano Banana (Coming Soon, Vi mạch & AI, KTPM & Kinh doanh số, Tiện ích Campus, Workshop THPT, FPTU Open Day, OJT & Báo chí) + 4 ảnh thực tế Unsplash + Kho riêng Client Vault',
      },
      {
        field: 'Từ khóa hạn chế trong Brand Profile Đại học FPT',
        actionType: 'Tự động điền sẵn',
        value:
          'cam kết 100% việc làm lương ngàn đô, học bổng ảo, tuyển thẳng không cần điều kiện, bằng cấp vô giá trị',
        note: 'Dùng cho AI sinh nội dung và kiểm duyệt tự động ở Bước B7',
      },
    ],
    actions: [
      {
        id: 'B2_NAV',
        label: 'Mở Đội ngũ 5 Thành viên SE08 & Khách hàng (/members)',
        description: 'Xem Lê Trí Trung, Nguyễn Thành Lộc, Phước, Tuấn, Ân & Ban Tuyển sinh ĐH FPT',
        variant: 'primary',
        icon: <Users className="size-4" />,
      },
      {
        id: 'B2_NAV_CLIENT_PROFILE',
        label: 'Mở Hồ sơ Thương hiệu Đại học FPT (/client-profile)',
        description: 'Xem thông tin 5 cơ sở, học kỳ OJT và danh mục từ khóa hạn chế',
        variant: 'outline',
        icon: <FileText className="size-4" />,
      },
      {
        id: 'B2_NAV_LIBRARY',
        label: 'Mở Thư viện 7 ảnh Key Visual Gemini (/library)',
        description: 'Xem 4 thư mục tuần, bộ ảnh Gemini Nano Banana + Unsplash và Mẫu bài đăng',
        variant: 'outline',
        icon: <FolderOpen className="size-4" />,
      },
      {
        id: 'B2_NAV_CHAT',
        label: 'Mở Kênh Trò chuyện nhóm SE08 & ĐH FPT (/chat)',
        description: 'Xem trao đổi thực tế giữa team SE08 và Ban Tuyển sinh ĐH FPT',
        variant: 'subtle',
        icon: <MessageSquare className="size-4" />,
      },
    ],
  },
  {
    stepNumber: 3,
    code: 'B3',
    stage: 'Giai đoạn 1: Gói truyền thông Đa lĩnh vực & Chiến dịch 4 tuần',
    stageShort: 'GĐ 1: Gói & Chiến dịch',
    timeBudget: '02:30 - 04:15',
    title: 'Điều phối Chiến dịch Tuyển sinh 4 Tuần (Brief, 20 Công việc, 6 Đối tác)',
    shortTitle: 'Chiến dịch 4 Tuần (3 bước)',
    frCode: 'FR 3.5.6 - 3.5.13',
    role: 'Manager',
    actorName: 'Nguyễn Thành Lộc',
    actorEmail: 'user1@demo.brandhub.test',
    routeTemplate: '/workspaces/{workspace_id}/campaigns',
    manualBrowserCue:
      'Bấm [1] -> [2] -> [3] (hệ thống tự gõ việc phát sinh lịch xe Open Day, sau đó có thể bấm Hủy/Tạo trên Chrome) -> Bấm [4] xem 6 đối tác báo chí/KOL.',
    talkingPoints: [
      'Bước 1 (Master Brief 6 khối): Vạch rõ lộ trình 4 tuần từ Coming Soon K23, giới thiệu ngành học & tiện ích, chuỗi Workshop THPT đến báo chí.',
      'Bước 2 (Timeline): Quản lý 19 hạng mục chuẩn của gói và cho phép thêm linh hoạt công việc phát sinh ngoài gói.',
      'Bước 3 (Đối tác): Quản lý đồng bộ 6 đơn vị VnExpress, Thanh Niên, Dân Trí, VTV1, Schannel và Màn hình LED THPT.',
    ],
    presenterScript:
      'Chuyển sang màn hình của Manager Nguyễn Thành Lộc, toàn bộ chiến dịch tuyển sinh năm 2027 kéo dài 4 tuần được hoạch định xuyên suốt: Tuần 1 tung chuỗi bài Coming Soon mở màn mùa tuyển sinh khóa K23 và công bố Học bổng Nguyễn Văn Đạo; Tuần 2 đi sâu giới thiệu các ngành mũi nhọn Thiết kế Vi mạch, AI, Kỹ thuật phần mềm, Kinh doanh số cùng hệ thống tiện ích học đường để chuẩn bị cho chuỗi sự kiện tại trường cấp 3; Tuần 3 triển khai chuỗi Workshop trực tiếp tại các trường THPT, tổ chức Ngày hội FPTU Open Day và lên bài cùng KOL công nghệ; Tuần 4 đẩy mạnh tuyến bài báo chí chính thống trên VnExpress, Thanh Niên, Dân Trí và nhắc hạn chốt hồ sơ đợt 1 trên cả 4 nền tảng.',
    expectedOutcome:
      'Trình diễn mượt cả 3 bước của Chiến dịch 4 tuần, điền tự động hộp thoại Công việc phát sinh ngoài gói và kiểm tra 6 đối tác báo chí/KOL.',
    fields: [
      {
        field: 'Lộ trình 4 Tuần trong Master Brief (6/6 khối hoàn chỉnh)',
        actionType: 'Tự động điền sẵn',
        value:
          'Tuần 1: Coming Soon K23 & Học bổng | Tuần 2: Ngành học mũi nhọn & Phổ biến tiện ích Campus | Tuần 3: Chuỗi Workshop THPT & Ngày hội Open Day | Tuần 4: Báo chí chính thống & Đa nền tảng chốt đợt 1',
      },
      {
        field: 'Bước 2 - Tên công việc phát sinh ngoài gói (Quick-Fill)',
        actionType: 'Nhập text',
        value: DEFAULT_DEMO_TEXTS.out_of_scope_title,
        copyKey: 'out_of_scope_title',
      },
      {
        field: 'Bước 2 - Mô tả công việc phát sinh',
        actionType: 'Nhập text',
        value: DEFAULT_DEMO_TEXTS.out_of_scope_desc,
        copyKey: 'out_of_scope_desc',
      },
      {
        field: 'Bước 3 - 6 Đối tác Báo chí, Truyền hình, KOL & OOH',
        actionType: 'Tự động điền sẵn',
        value:
          'VnExpress, Báo Thanh Niên, Báo Dân Trí, Đài Truyền hình VTV1, Schannel Network, Hệ thống Màn hình LED Học đường THPT',
      },
    ],
    actions: [
      {
        id: 'B3_STEP_INFO',
        label: 'Mở Bước 1: Lộ trình 4 Tuần & Master Brief',
        description: 'Hiển thị 6/6 khối Brief và bản Master Brief tổng hợp 4 tuần',
        variant: 'primary',
        icon: <FileText className="size-4" />,
      },
      {
        id: 'B3_STEP_TASKS',
        label: 'Mở Bước 2: Timeline 19 Hạng mục trong gói',
        description: 'Hiển thị lịch trình 4 tuần và làm nổi bật nút Thêm công việc phát sinh',
        variant: 'outline',
        icon: <Layers className="size-4" />,
      },
      {
        id: 'B3_FILL_OUT_OF_SCOPE',
        label: 'Điền thử Công việc phát sinh (Lịch xe Open Day)',
        description: 'Tự động mở hộp thoại và gõ Tên, Hạn xuất bản, Mô tả & Tiêu chí nghiệm thu',
        variant: 'subtle',
        icon: <Sparkles className="size-4" />,
      },
      {
        id: 'B3_STEP_PARTNERS',
        label: 'Mở Bước 3: 6 Đối tác Báo chí / KOL & Triển khai',
        description: 'Hiển thị VnExpress, Thanh Niên, Dân Trí, VTV1, Schannel & LED THPT',
        variant: 'primary',
        icon: <Handshake className="size-4" />,
      },
    ],
  },
  {
    stepNumber: 4,
    code: 'B4',
    stage: 'Giai đoạn 2: Điều phối 20 Công việc, Subtask, Khảo sát & Yêu cầu',
    stageShort: 'GĐ 2: Công việc & Subtask',
    timeBudget: '04:15 - 05:45',
    title: 'Phân bổ 20 Công việc cho 3 Creator SE08, Khảo sát THPT & Yêu cầu Client',
    shortTitle: '20 Công việc, Khảo sát & Yêu cầu',
    frCode: 'FR 3.6.1 - 3.6.10, 3.6.28 - 3.6.32',
    role: 'Manager',
    actorName: 'Nguyễn Thành Lộc',
    actorEmail: 'user1@demo.brandhub.test',
    routeTemplate: '/workspaces/{workspace_id}/tasks',
    manualBrowserCue:
      'Bấm [1] xem bảng 20 công việc & 5 Subtask bài Tuần 3; bấm [3] xem 16 phiếu Khảo sát lớp 12 và bấm [4] xem Yêu cầu từ Ban Tuyển sinh.',
    talkingPoints: [
      '20 công việc phân công chuyên môn hóa cho 3 Creator nhóm SE08: Phước (Social), Tuấn (Key Visual, Reels & Workshop), Ân (Báo chí, Email & Khảo sát).',
      'Bài trọng điểm Tuần 3 có 5 Role Subtasks phối hợp chéo giữa Ân (Nghiên cứu), Tuấn (Key Visual) và Phước (Soạn bài).',
      'Liên kết trực tiếp với trang Khảo sát nguyện vọng học sinh lớp 12 (16 phản hồi) và trang Yêu cầu nội dung từ nhà trường.',
    ],
    presenterScript:
      'Khi chiến dịch đi vào vận hành, toàn bộ 20 đầu việc trong 4 tuần được phân công rõ cho 3 Creator của nhóm SE08: Nguyễn Chơn Phước phụ trách nội dung đa nền tảng, Nguyễn Minh Tuấn đảm nhận thiết kế Key Visual, dựng Reels và kịch bản chuỗi Workshop THPT, còn Hà Văn Ân phụ trách thông cáo báo chí VnExpress/Thanh Niên, bản tin Email và khảo sát học sinh lớp 12. Đặc biệt ở bài trọng điểm Tuần 3 đang thực hiện, 5 Subtask con cũng được phối hợp chéo giữa Tuấn, Ân và Phước rất chặt chẽ.',
    expectedOutcome:
      'Hiển thị đầy đủ 20 công việc theo tiến độ thực tế của tuần thứ 3, chi tiết 5 Subtask không thiếu trường nào, cùng bảng kết quả 16 phiếu khảo sát học sinh THPT và 2 yêu cầu từ khách hàng.',
    fields: [
      {
        field: 'Bài trọng điểm đang thực hiện tại Tuần 3 (Task #1)',
        actionType: 'Tự động điền sẵn',
        value:
          '[Tuần 3 - Bài trọng điểm] Điểm nhấn Chuỗi Workshop THPT & Mở cổng đăng ký Học bổng ĐH FPT 2027',
      },
      {
        field: '5 Subtask phối hợp giữa các thành viên SE08',
        actionType: 'Tự động điền sẵn',
        value:
          '1. Nghiên cứu thông tin (Hà Văn Ân - FINISHED) | 2. Soạn nội dung (Nguyễn Chơn Phước - IN_PROGRESS) | 3. Thiết kế Key Visual (Nguyễn Minh Tuấn - FINISHED) | 4. Biên tập & Rà soát | 5. Lên lịch đăng 4 kênh (FINISHED)',
      },
      {
        field: 'Mô tả Subtask mẫu (Quick-Fill nếu muốn chỉnh sửa trực tiếp)',
        actionType: 'Nhập text',
        value: DEFAULT_DEMO_TEXTS.subtask_desc,
        copyKey: 'subtask_desc',
      },
    ],
    actions: [
      {
        id: 'B4_NAV',
        label: 'Mở 20 Công việc 4 tuần & Xem 5 Subtask Tuần 3',
        description: 'Mở trang Công việc và bật ngăn chi tiết [Tuần 3 - Bài trọng điểm]',
        variant: 'primary',
        icon: <Play className="size-4" />,
      },
      {
        id: 'B4_FILL_SUBTASK',
        label: 'Điền mẫu Mô tả & Tiêu chí nghiệm thu Subtask',
        description: 'Gõ tuần tự mô tả và tiêu chí nghiệm thu vào form Subtask đang mở',
        variant: 'outline',
        icon: <Sparkles className="size-4" />,
      },
      {
        id: 'B4_NAV_SURVEYS',
        label: 'Mở Khảo sát Nguyện vọng Học sinh THPT (/survey)',
        description: 'Xem khảo sát 4 câu hỏi và 16 phản hồi thực tế của học sinh lớp 12',
        variant: 'outline',
        icon: <ClipboardList className="size-4" />,
      },
      {
        id: 'B4_NAV_EVENT',
        label: 'Mở Kế hoạch Sự kiện FPTU Open Day 2027 (/event)',
        description: 'Creator Phước điều phối 5 phân khu: concept, runsheet, hậu cần, nhân sự & báo cáo',
        variant: 'outline',
        icon: <Calendar className="size-4" />,
      },
      {
        id: 'B4_NAV_WORKSHOP',
        label: 'Mở Chuỗi Workshop THPT (/workshop)',
        description: 'Diễn giả, chương trình, hậu cần & phiếu đăng ký học sinh',
        variant: 'outline',
        icon: <Presentation className="size-4" />,
      },
      {
        id: 'B4_NAV_REQUESTS',
        label: 'Mở Yêu cầu Nội dung từ Ban Tuyển sinh (/requests)',
        description: 'Xem 2 yêu cầu bổ sung bài truyền thông từ phía Đại học FPT',
        variant: 'subtle',
        icon: <FileText className="size-4" />,
      },
    ],
  },
  {
    stepNumber: 5,
    code: 'B5',
    stage: 'Giai đoạn 2: Điều phối 20 Công việc, Subtask, Khảo sát & Yêu cầu',
    stageShort: 'GĐ 2: Công việc & Subtask',
    timeBudget: '05:45 - 06:30',
    title: 'Creator Nguyễn Chơn Phước nhận việc Tuần 3 & Kiểm tra tiến độ Subtask',
    shortTitle: 'Creator nhận bài Tuần 3',
    frCode: 'FR 3.6.3, 3.6.4',
    role: 'Creator',
    actorName: 'Nguyễn Chơn Phước',
    actorEmail: 'user13@demo.brandhub.test',
    routeTemplate: '/workspaces/{workspace_id}/tasks',
    manualBrowserCue:
      'Chỉ vào các Subtask Nghiên cứu (Ân) và Hình ảnh (Tuấn) đã báo Hoàn thành, sẵn sàng bấm sang bước B6 mở /editor.',
    talkingPoints: [
      'Cửa sổ chuyển sang Creator Nguyễn Chơn Phước với danh sách đầu việc cá nhân xuyên suốt 4 tuần.',
      'Các bài Tuần 1-2 đã xuất bản; hiện tập trung vào [Tuần 3 - Bài trọng điểm] tổng hợp chuỗi Workshop THPT.',
      'Nhờ tách phần độc lập, tư liệu của Hà Văn Ân và Key Visual của Nguyễn Minh Tuấn đã duyệt sẵn.',
    ],
    presenterScript:
      'Trên màn hình của Creator Nguyễn Chơn Phước, bạn thấy rõ các bài đăng Tuần 1, Tuần 2 đã hoàn thành và xuất bản, hiện tập trung vào bài trọng điểm của Tuần 3 tổng hợp chuỗi Workshop tại trường THPT. Nhờ cơ chế tách phần độc lập, tư liệu nghiên cứu của Hà Văn Ân và bộ Key Visual của Nguyễn Minh Tuấn đều đã được nghiệm thu sẵn.',
    expectedOutcome:
      'Creator xem chi tiết công việc [Tuần 3 - Bài trọng điểm] và làm nổi bật nút chuyển sang Trình soạn thảo hợp nhất (/editor).',
    fields: [
      {
        field: 'Người phụ trách chính (Coordinator / Assignee)',
        actionType: 'Tự động điền sẵn',
        value: 'Nguyễn Chơn Phước (Creator - Phụ trách Social đa nền tảng)',
      },
      {
        field: 'Người giám sát duyệt nội bộ (Supervisor)',
        actionType: 'Tự động điền sẵn',
        value: 'Nguyễn Thành Lộc (Manager)',
      },
    ],
    actions: [
      {
        id: 'B5_NAV',
        label: 'Mở việc của Creator & Chọn [Tuần 3 - Bài trọng điểm]',
        description: 'Điều hướng trình duyệt Creator tới /workspaces/{workspace_id}/tasks',
        variant: 'primary',
        icon: <Play className="size-4" />,
      },
      {
        id: 'B5_NAV_VIDEO',
        label: 'Mở Video ngắn Reels/TikTok #3 Tuần 3 (/editor)',
        description: 'Kịch bản, quay, dựng, caption & kênh đăng của video recap',
        variant: 'outline',
        icon: <Video className="size-4" />,
      },
      {
        id: 'B5_NAV_KOL',
        label: 'Mở Booking KOL Duy Luân & Schannel (/kol)',
        description: 'Shortlist, thỏa thuận chi phí, brief, bản nháp & nghiệm thu số liệu',
        variant: 'outline',
        icon: <Megaphone className="size-4" />,
      },
    ],
  },
  {
    stepNumber: 6,
    code: 'B6',
    stage: 'Giai đoạn 3: Trình soạn thảo (/editor), Bắn ảnh Gemini & Gọi AI',
    stageShort: 'GĐ 3: /editor, Ảnh Gemini & AI',
    timeBudget: '06:30 - 08:30',
    title: 'Bắn trực tiếp ảnh Key Visual Gemini lên bài viết & Gọi AI tạo Caption',
    shortTitle: 'Bắn ảnh Gemini & Gọi AI',
    frCode: 'FR 3.6.11, 3.6.25, 3.7.1, 3.7.2',
    role: 'Creator',
    actorName: 'Nguyễn Chơn Phước',
    actorEmail: 'user13@demo.brandhub.test',
    routeTemplate: '/workspaces/{workspace_id}/editor?taskId={task_id}',
    manualBrowserCue:
      'Bấm [1] mở /editor -> Bấm [2] bắn ngay ảnh Key Visual Gemini lên bài viết -> Bấm [3] đổi Quick/Docs -> Bấm [4] tự điền 5 ô AI (có thể bấm "Tạo gợi ý" trên Chrome).',
    talkingPoints: [
      'Trình soạn thảo /editor chia bài viết thành 4 khung độc lập (BRIEF, MEDIA, CHANNELS, CAPTION) khớp với từng Subtask.',
      'Chỉ 1 cú nhấp [2], ảnh Key Visual tạo sẵn bằng Gemini Nano Banana trong Kho tài nguyên được bắn thẳng lên bài và khung xem trước 4 nền tảng.',
      'Hộp thoại AI tự động nhận ngữ cảnh Brand Profile Đại học FPT để gợi ý nội dung sát thực tế mùa tuyển sinh 2027.',
    ],
    presenterScript:
      'Tại Trình soạn thảo hợp nhất (/editor), bài viết được tách thành 4 phần độc lập gắn với từng Subtask. Khi cần đính kèm thêm hình ảnh sự kiện, chúng em chỉ cần mở tab Kho tài nguyên ngay trong khung Hình ảnh và bắn thẳng tấm Key Visual Tuần 3 đã tạo bằng Gemini Nano Banana lên bài viết; lập tức khung xem trước bên phải cập nhật giao diện hiển thị trên cả Facebook, Instagram, TikTok và Threads. Tiếp theo, Creator mở hộp thoại Tạo bằng AI để sinh bản thảo dựa trên ngữ cảnh thương hiệu Đại học FPT.',
    expectedOutcome:
      'Ảnh Key Visual Gemini hiển thị ngay trên bài viết và khung điện thoại xem trước 4 nền tảng; hộp thoại AI được điền tuần tự 5 trường và làm nổi bật nút "Tạo gợi ý".',
    fields: [
      {
        field: 'Ấn phẩm Key Visual Gemini bắn trực tiếp lên bài (POST.MEDIA)',
        actionType: 'Bấm nút',
        value:
          'KV_Tuan3_Workshop_THPT_TienIch.jpg + KV_Tuan3_FPTU_OpenDay_2027.jpg (tạo sẵn bằng Gemini Nano Banana trong Kho tài nguyên)',
        note: 'Hiển thị tức thì không phụ thuộc đường truyền tải file bên ngoài',
      },
      {
        field: '1. Chủ đề bài viết (AI Topic)',
        actionType: 'Nhập text',
        value: DEFAULT_DEMO_TEXTS.ai_topic,
        copyKey: 'ai_topic',
      },
      {
        field: '2. Tham số AI (Tone, Nền tảng, Ngôn ngữ, Số hashtag)',
        actionType: 'Chọn dropdown',
        value: 'Giọng điệu: Chuyên nghiệp | Nền tảng: Facebook | Ngôn ngữ: Tiếng Việt | Số hashtag: 6',
      },
    ],
    actions: [
      {
        id: 'B6_NAV_EDITOR',
        label: 'Mở Trình soạn thảo hợp nhất (/editor)',
        description: 'Điều hướng Creator tới /workspaces/{workspace_id}/editor?taskId={task_id}',
        variant: 'primary',
        icon: <Play className="size-4" />,
      },
      {
        id: 'B6_PUSH_KEY_VISUAL',
        label: 'Bắn ảnh Key Visual Gemini lên bài viết',
        description: 'Mở tab Kho tài nguyên và gắn ngay ảnh KV_Tuan3_FPTU_OpenDay_2027 lên bài',
        variant: 'primary',
        icon: <Image className="size-4" />,
      },
      {
        id: 'B6_TOGGLE_DOCS_MODE',
        label: 'Chuyển đổi Chế độ Nhanh / Tài liệu',
        description: 'Chuyển đổi linh hoạt giữa Quick Mode và Docs Mode trên thanh công cụ',
        variant: 'outline',
        icon: <FileText className="size-4" />,
      },
      {
        id: 'B6_SEQ_FILL_AI',
        label: 'Điền tuần tự 5 trường AI Tạo Caption',
        description: 'Tự động mở modal AI và điền Topic, Tone, Platform, Ngôn ngữ, Số hashtag',
        variant: 'primary',
        icon: <Sparkles className="size-4" />,
      },
    ],
  },
  {
    stepNumber: 7,
    code: 'B7',
    stage: 'Giai đoạn 3: Trình soạn thảo (/editor), Bắn ảnh Gemini & Gọi AI',
    stageShort: 'GĐ 3: /editor, Ảnh Gemini & AI',
    timeBudget: '08:30 - 10:00',
    title: 'Kiểm duyệt an toàn nội dung (3.6.33) & Gửi duyệt phần POST.CAPTION (v1)',
    shortTitle: 'Kiểm tra vi phạm & Gửi v1',
    frCode: 'FR 3.6.33, 3.6.18',
    role: 'Creator',
    actorName: 'Nguyễn Chơn Phước',
    actorEmail: 'user13@demo.brandhub.test',
    routeTemplate: '/workspaces/{workspace_id}/editor?taskId={task_id}',
    manualBrowserCue:
      'Bấm [1] rồi nhấn nút "Kiểm tra vi phạm" trên Chrome để hiện cảnh báo -> Bấm [2] điền bản sạch v1 rồi nhấn "Lưu thay đổi" và "Gửi duyệt" trên khung POST.CAPTION.',
    talkingPoints: [
      'Chèn thử câu vi phạm quy chuẩn thương hiệu ("cam kết 100% việc làm lương ngàn đô...") để test chốt chặn FR 3.6.33.',
      'Hệ thống lập tức phát hiện cụm từ nằm trong danh sách cấm của Đại học FPT.',
      'Khôi phục bản thảo sạch v1 (chủ đích chưa ghi 3 mức học bổng & OJT để khách hàng góp ý ở B9), bấm Lưu và Gửi duyệt riêng phần POST.CAPTION.',
    ],
    presenterScript:
      'Trước khi gửi bài cho quản lý, chúng em kiểm thử chốt chặn an toàn nội dung bằng cách thêm một câu quảng cáo quá mức vào cuối bài và bấm "Kiểm tra vi phạm". Hệ thống đối chiếu ngay với từ điển hạn chế của Đại học FPT và báo cảnh báo rõ ràng. Sau khi xóa câu vi phạm và khôi phục bản thảo sạch v1, Creator lưu lại và bấm "Gửi duyệt" riêng phần Nội dung bài đăng.',
    expectedOutcome:
      'Hệ thống phát hiện chính xác cụm từ vi phạm quy chuẩn tuyển sinh; sau khi làm sạch, phần POST.CAPTION chuyển sang SUBMITTED (v1).',
    fields: [
      {
        field: 'Câu mẫu thử nghiệm bộ lọc vi phạm (FR 3.6.33)',
        actionType: 'Nhập text',
        value: DEFAULT_DEMO_TEXTS.violation_sample.trim(),
        copyKey: 'violation_sample',
      },
      {
        field: 'Nội dung bản thảo sạch v1 (chưa nêu 3 mức học bổng 2027 & OJT)',
        actionType: 'Nhập text',
        value: DEFAULT_DEMO_TEXTS.caption_v1_clean,
        copyKey: 'caption_v1_clean',
        note: 'Chủ đích chừa chi tiết 3 mức học bổng 50%-70%-100% và kỳ OJT để Ban Tuyển sinh ĐH FPT góp ý ở Bước B9',
      },
    ],
    actions: [
      {
        id: 'B7_FILL_VIOLATION',
        label: 'Chèn câu vi phạm để test Kiểm duyệt (3.6.33)',
        description: 'Gõ thêm câu chứa từ cấm vào cuối bài và làm nổi bật nút Kiểm tra vi phạm',
        variant: 'outline',
        icon: <ShieldAlert className="size-4" />,
      },
      {
        id: 'B7_CLEAN_AND_RESTORE',
        label: 'Khôi phục bản thảo sạch v1 & Chỉ nút Gửi duyệt',
        description: 'Điền lại bản v1 chuẩn mùa tuyển sinh 2027 và chỉ vào nút Lưu / Gửi duyệt',
        variant: 'primary',
        icon: <Send className="size-4" />,
      },
    ],
  },
  {
    stepNumber: 8,
    code: 'B8',
    stage: 'Giai đoạn 4: Duyệt từng phần 2 tầng & Đối chiếu phiên bản v1/v2',
    stageShort: 'GĐ 4: Duyệt 2 tầng & Diff v1/v2',
    timeBudget: '10:00 - 11:00',
    title: 'Manager Nguyễn Thành Lộc duyệt nội bộ phần Nội dung bài đăng (v1)',
    shortTitle: 'Manager duyệt nội bộ v1',
    frCode: 'FR 3.6.19',
    role: 'Manager',
    actorName: 'Nguyễn Thành Lộc',
    actorEmail: 'user1@demo.brandhub.test',
    routeTemplate: '/workspaces/{workspace_id}/task-approvals?task={task_id}',
    manualBrowserCue:
      'Sau khi bấm [1], trên cửa sổ Chrome của Manager hãy bấm nút "Duyệt" trên thẻ Nội dung bài đăng (POST.CAPTION) để chuyển sang Client.',
    talkingPoints: [
      'Cửa sổ tự động chuyển sang Manager Nguyễn Thành Lộc tại hàng đợi phê duyệt.',
      'Các phần Nghiên cứu, Hình ảnh Key Visual và Kênh đăng đã hoàn tất, Manager chỉ cần rà soát riêng phần POST.CAPTION.',
      'Bấm "Duyệt" để chuyển tiếp bản v1 sang hàng đợi nghiệm thu của Ban Tuyển sinh Đại học FPT.',
    ],
    presenterScript:
      'Ở tầng kiểm soát nội bộ của SE08 Digital Agency, Manager Nguyễn Thành Lộc mở màn hình Phê duyệt. Các phần Nghiên cứu, Hình ảnh Key Visual và Kênh đăng đã hoàn tất từ trước, nên Manager chỉ cần tập trung duyệt phần Nội dung bài đăng v1 để chuyển tiếp sang cho khách hàng.',
    expectedOutcome:
      'Phần POST.CAPTION chuyển sang trạng thái INTERNAL_APPROVED và xuất hiện ngay bên phía Client.',
    fields: [
      {
        field: 'Phần công việc cần duyệt nội bộ',
        actionType: 'Bấm nút',
        value: 'Nội dung bài đăng (POST.CAPTION) - Phiên bản v1',
      },
    ],
    actions: [
      {
        id: 'B8_NAV_MANAGER_APPROVAL',
        label: 'Mở màn hình Duyệt của Manager & Chỉ nút Duyệt',
        description: 'Điều hướng Manager tới /task-approvals?task={task_id}',
        variant: 'primary',
        icon: <CheckCircle2 className="size-4" />,
      },
    ],
  },
  {
    stepNumber: 9,
    code: 'B9',
    stage: 'Giai đoạn 4: Duyệt từng phần 2 tầng & Đối chiếu phiên bản v1/v2',
    stageShort: 'GĐ 4: Duyệt 2 tầng & Diff v1/v2',
    timeBudget: '11:00 - 12:15',
    title: 'Ban Tuyển sinh ĐH FPT nghiệm thu v1 & Yêu cầu bổ sung Học bổng + OJT',
    shortTitle: 'Client yêu cầu bổ sung v1',
    frCode: 'FR 3.6.20, 3.6.21',
    role: 'Client',
    actorName: 'Ban Tuyển sinh Đại học FPT',
    actorEmail: 'user59@demo.brandhub.test',
    routeTemplate: '/workspaces/{workspace_id}/task-approvals?task={task_id}',
    manualBrowserCue:
      'Bấm [1] mở màn hình Client -> Bấm [2] tự động gõ góp ý vào hộp thoại -> Trên Chrome của Client bấm nút "Yêu cầu chỉnh sửa / Xác nhận" để trả về.',
    talkingPoints: [
      'Khách hàng Ban Tuyển sinh ĐH FPT chỉ nhìn thấy các phần đầu ra (OUTPUT), hoàn toàn không thấy ghi chú nội bộ POST.BRIEF của Agency.',
      'Nhà trường yêu cầu chỉnh sửa riêng phần POST.CAPTION để bổ sung rõ 3 mức học bổng 50%, 70%, 100% và kỳ thực tập OJT từ học kỳ 6.',
      'Chỉ riêng phần Nội dung quay về RETURNED; phần Hình ảnh Key Visual và Kênh đăng vẫn giữ nguyên trạng thái đã duyệt.',
    ],
    presenterScript:
      'Chuyển sang cửa sổ của khách hàng là Ban Tuyển sinh Đại học FPT, hệ thống chỉ hiển thị những phần đầu ra đã qua duyệt nội bộ và ẩn hoàn toàn ghi chú nháp nội bộ của Agency. Sau khi đọc bài tổng hợp Workshop, đại diện nhà trường đánh giá tốt không khí bài viết nhưng bấm "Yêu cầu chỉnh sửa" để đề nghị nêu rõ 3 mức học bổng 50%, 70%, 100% học phí cùng chương trình thực tập OJT từ học kỳ 6 tại FPT Software và FPT Smart Cloud.',
    expectedOutcome:
      'Chỉ riêng phần POST.CAPTION quay về trạng thái RETURNED kèm ghi chú chi tiết của nhà trường; phần Hình ảnh Key Visual và Kênh đăng vẫn giữ nguyên trạng thái đã duyệt.',
    fields: [
      {
        field: 'Ghi chú yêu cầu chỉnh sửa của Ban Tuyển sinh Đại học FPT (v1)',
        actionType: 'Nhập text',
        value: DEFAULT_DEMO_TEXTS.client_reject_note,
        copyKey: 'client_reject_note',
      },
    ],
    actions: [
      {
        id: 'B9_NAV_CLIENT_APPROVAL',
        label: 'Mở màn hình Nghiệm thu của Ban Tuyển sinh ĐH FPT',
        description: 'Điều hướng Client tới /task-approvals?task={task_id}',
        variant: 'primary',
        icon: <Play className="size-4" />,
      },
      {
        id: 'B9_SEQ_FILL_REJECT_REASON',
        label: 'Điền nhận xét yêu cầu bổ sung Học bổng 2027 + OJT',
        description: 'Tự động bấm Yêu cầu chỉnh sửa và gõ góp ý chi tiết của nhà trường',
        variant: 'primary',
        icon: <Sparkles className="size-4" />,
      },
    ],
  },
  {
    stepNumber: 10,
    code: 'B10',
    stage: 'Giai đoạn 4: Duyệt từng phần 2 tầng & Đối chiếu phiên bản v1/v2',
    stageShort: 'GĐ 4: Duyệt 2 tầng & Diff v1/v2',
    timeBudget: '12:15 - 13:45',
    title: 'Creator cập nhật bản v2, Gửi duyệt lại & Mở đối chiếu Diff v1 vs v2',
    shortTitle: 'Creator sửa v2 & Xem Diff',
    frCode: 'FR 3.6.11, 3.6.18',
    role: 'Creator',
    actorName: 'Nguyễn Chơn Phước',
    actorEmail: 'user13@demo.brandhub.test',
    routeTemplate: '/workspaces/{workspace_id}/editor?taskId={task_id}',
    manualBrowserCue:
      'Bấm [1] mở lại /editor -> Bấm [2] tự gõ nối tiếp đoạn v2, sau đó bấm "Lưu thay đổi" và "Gửi duyệt" trên Chrome -> Bấm [3] mở bảng đối chiếu Diff v1 vs v2.',
    talkingPoints: [
      'Góp ý của Ban Tuyển sinh hiển thị ngay trên khung POST.CAPTION và Subtask tương ứng tự động mở lại.',
      'Creator bấm [2] bổ sung đầy đủ 3 mức Học bổng Nguyễn Văn Đạo 2027 (50%, 70%, 100%) và kỳ thực tập OJT học kỳ 6, lưu và gửi duyệt bản v2.',
      'Mở ngăn Lịch sử phiên bản (SectionVersionDrawer) để hội đồng thấy trực quan từng dòng nội dung vừa thêm mới giữa v1 và v2.',
    ],
    presenterScript:
      'Quay lại màn hình của Creator Nguyễn Chơn Phước, góp ý của Ban Tuyển sinh hiển thị trực tiếp ngay trên khung Nội dung bài đăng và Subtask tương ứng cũng tự động mở lại. Phước bổ sung đầy đủ quyền lợi học bổng 50%, 70%, 100% cùng kỳ thực tập OJT từ học kỳ 6, lưu và gửi duyệt bản v2. Khi mở ngăn "Lịch sử phiên bản", cả quản lý và khách hàng đều đối chiếu trực quan được từng dòng nội dung vừa cập nhật giữa v1 và v2.',
    expectedOutcome:
      'Bản thảo v2 được gửi duyệt thành công và ngăn Lịch sử phiên bản (SectionVersionDrawer) tô sáng rõ đoạn văn bản mới bổ sung so với bản v1.',
    fields: [
      {
        field: 'Đoạn nội dung bổ sung vào bản v2 (Học bổng 50%-100% & OJT)',
        actionType: 'Nhập text',
        value: DEFAULT_DEMO_TEXTS.caption_v2_addition.trim(),
        copyKey: 'caption_v2_addition',
      },
      {
        field: 'Đối chiếu lịch sử phiên bản (v1 vs v2)',
        actionType: 'Mở ngăn đối chiếu',
        value: 'Bấm biểu tượng Lịch sử phiên bản trên khung POST.CAPTION để xem bảng so sánh dòng xanh/đỏ',
      },
    ],
    actions: [
      {
        id: 'B10_NAV_CREATOR_FIX',
        label: 'Mở lại Trình soạn thảo (/editor) của Creator',
        description: 'Làm nổi bật phần POST.CAPTION kèm góp ý của Ban Tuyển sinh ĐH FPT',
        variant: 'outline',
        icon: <Play className="size-4" />,
      },
      {
        id: 'B10_SEQ_FILL_V2',
        label: 'Bổ sung đoạn Học bổng 50%-100% & OJT vào bản v2',
        description: 'Gõ nối tiếp đoạn thông tin mới vào cuối bài viết và chỉ nút Lưu / Gửi duyệt',
        variant: 'primary',
        icon: <Sparkles className="size-4" />,
      },
      {
        id: 'B10_OPEN_VERSION_DIFF',
        label: 'Mở Lịch sử phiên bản (So sánh Diff v1 vs v2)',
        description: 'Bấm nút Lịch sử phiên bản trên khung POST.CAPTION để mở ngăn đối chiếu',
        variant: 'primary',
        icon: <GitCompare className="size-4" />,
      },
    ],
  },
  {
    stepNumber: 11,
    code: 'B11',
    stage: 'Giai đoạn 4: Duyệt từng phần 2 tầng & Đối chiếu phiên bản v1/v2',
    stageShort: 'GĐ 4: Duyệt 2 tầng & Diff v1/v2',
    timeBudget: '13:45 - 15:00',
    title: 'Manager & Ban Tuyển sinh ĐH FPT phê duyệt hoàn tất bản v2',
    shortTitle: 'Duyệt hoàn tất v2 -> FINISHED',
    frCode: 'FR 3.6.19, 3.6.20',
    role: 'Client',
    actorName: 'Nguyễn Thành Lộc -> Ban Tuyển sinh ĐH FPT',
    actorEmail: 'user1@demo.brandhub.test / user59@demo.brandhub.test',
    routeTemplate: '/workspaces/{workspace_id}/task-approvals?task={task_id}',
    manualBrowserCue:
      'Bấm [1] rồi nhấn "Duyệt" trên Chrome Manager -> Bấm [2] rồi nhấn "Duyệt" trên Chrome Client để chốt hoàn tất toàn bộ Task & Post.',
    talkingPoints: [
      'Manager Nguyễn Thành Lộc duyệt nội bộ bản v2, sau đó Ban Tuyển sinh ĐH FPT bấm Duyệt nghiệm thu chính thức.',
      'Khi toàn bộ phần đầu ra (MEDIA, CHANNELS, CAPTION) đạt CLIENT_APPROVED, hệ thống tự động đóng Task sang FINISHED.',
      'Tất cả 5 Subtask tự động đồng bộ sang Hoàn thành và bài đăng mở khóa sang trạng thái APPROVED.',
    ],
    presenterScript:
      'Sau khi bản v2 được gửi lên, Manager Nguyễn Thành Lộc duyệt nội bộ và đại diện Ban Tuyển sinh Đại học FPT bấm "Duyệt" nghiệm thu cuối cùng. Ngay khoảnh khắc phần đầu ra cuối cùng đạt trạng thái khách hàng chấp thuận, hệ thống tự động đồng bộ toàn bộ 5 Subtask sang Hoàn thành, đóng công việc ở trạng thái FINISHED và mở khóa bài viết sang trạng thái APPROVED để sẵn sàng xuất bản đa nền tảng.',
    expectedOutcome:
      '[Tuần 3 - Bài trọng điểm] tự động chuyển sang FINISHED, cả 5 Subtask chuyển sang FINISHED và bài đăng chuyển sang APPROVED.',
    fields: [
      {
        field: 'Bước 11.1 - Manager duyệt nội bộ v2',
        actionType: 'Bấm nút',
        value: 'Bấm nút "Duyệt" trên màn hình Manager (Nguyễn Thành Lộc)',
      },
      {
        field: 'Bước 11.2 - Ban Tuyển sinh ĐH FPT nghiệm thu hoàn tất v2',
        actionType: 'Bấm nút',
        value: 'Bấm nút "Duyệt" trên màn hình Client -> Tự động hoàn tất Task, Subtask & mở khóa Post',
      },
    ],
    actions: [
      {
        id: 'B11_NAV_MANAGER_V2',
        label: 'Mở màn hình Manager duyệt bản v2',
        description: 'Điều hướng Manager tới /task-approvals?task={task_id}',
        variant: 'outline',
        icon: <CheckCircle2 className="size-4" />,
      },
      {
        id: 'B11_NAV_CLIENT_V2',
        label: 'Mở màn hình Ban Tuyển sinh ĐH FPT duyệt hoàn tất v2',
        description: 'Điều hướng Client tới /task-approvals?task={task_id}',
        variant: 'primary',
        icon: <Award className="size-4" />,
      },
    ],
  },
  {
    stepNumber: 12,
    code: 'B12',
    stage: 'Giai đoạn 5: Đa nền tảng, Lịch đăng, Analytics, SePay & Admin',
    stageShort: 'GĐ 5: Xuất bản, SePay & Admin',
    timeBudget: '15:00 - 16:15',
    title: 'Kết nối 4 Nền tảng MXH, Bộ Hashtag Tuyển sinh & Mẫu Email Workshop',
    shortTitle: '4 Kênh MXH, Hashtag & Email',
    frCode: 'FR 3.4.23, 3.6.34, 3.8.1 - 3.8.5',
    role: 'Manager',
    actorName: 'Nguyễn Thành Lộc',
    actorEmail: 'user1@demo.brandhub.test',
    routeTemplate: '/workspaces/{workspace_id}/social-accounts',
    manualBrowserCue:
      'Bấm [1] -> [2] -> [3] -> [4] để lướt nhanh 4 kết nối OAuth (Facebook, Instagram, TikTok, Threads), 12 Hashtag tuyển sinh, Mẫu Email và Lịch sử gửi lô Email.',
    talkingPoints: [
      'Cả 4 nền tảng chính thức của hệ thống gồm Facebook, Instagram, TikTok và Threads đều đã kết nối OAuth hoạt động tốt.',
      'Bộ 12 Hashtag chuẩn mùa tuyển sinh 2027 được phân loại sẵn để tái sử dụng nhất quán.',
      'Mẫu Email và lịch sử gửi vé mời tham dự chuỗi Workshop THPT cho học sinh lớp 12 sẵn sàng trong cùng Workspace.',
    ],
    presenterScript:
      'Trước khi xuất bản đồng loạt, Manager kiểm tra hạ tầng kênh truyền thông của Workspace: cả 4 tài khoản chính thức của Tuyển sinh Đại học FPT trên Facebook, Instagram, TikTok và Threads đều đang kết nối hoạt động qua OAuth. Bên cạnh đó, bộ Hashtag bắt buộc của chiến dịch cùng mẫu Email và lịch sử gửi vé mời tham dự Workshop cho học sinh THPT cũng được chuẩn hóa đồng bộ.',
    expectedOutcome:
      'Hiển thị 4 kết nối OAuth hoạt động tốt (Facebook, Instagram, TikTok, Threads), 12 Hashtag chiến dịch, 2 mẫu Email và 2 lô gửi Email hoàn tất.',
    fields: [
      {
        field: '4 tài khoản Mạng xã hội chính thức của chiến dịch',
        actionType: 'Tự động điền sẵn',
        value:
          'Facebook: Đại học FPT - FPT University Tuyển sinh | Instagram: @fptuniversity.official | TikTok: @fptuniversity_official | Threads: @fptuniversity.official',
      },
      {
        field: 'Bộ Hashtag & Mẫu Email đi kèm chiến dịch',
        actionType: 'Tự động điền sẵn',
        value:
          '12 Hashtag chuẩn (#DaiHocFPT, #TuyenSinhFPTU2027, #WorkshopTHPT...), 2 Mẫu Email & 2 Lô gửi Email (6 lượt gửi thành công)',
      },
    ],
    actions: [
      {
        id: 'B12_NAV_SOCIAL',
        label: 'Mở Kết nối 4 Nền tảng Mạng xã hội (/social-accounts)',
        description: 'Xem kết nối OAuth Facebook, Instagram, TikTok và Threads',
        variant: 'primary',
        icon: <Globe className="size-4" />,
      },
      {
        id: 'B12_NAV_HASHTAGS',
        label: 'Mở Bộ Hashtag Chiến dịch Tuyển sinh',
        description: 'Xem 12 hashtag phân loại thương hiệu, ngành học và học bổng',
        variant: 'outline',
        icon: <Hash className="size-4" />,
      },
      {
        id: 'B12_NAV_MAIL_TEMPLATES',
        label: 'Mở Mẫu Email mời dự Workshop THPT (/mail-templates)',
        description: 'Xem mẫu Email Block-Builder gửi cho danh sách học sinh lớp 12',
        variant: 'subtle',
        icon: <Mail className="size-4" />,
      },
      {
        id: 'B12_NAV_MAIL_BATCHES',
        label: 'Mở Lịch sử Lô gửi Email (/mail-templates/batches)',
        description: 'Xem 2 đợt gửi vé mời Workshop THPT & báo cáo tiến độ tuần',
        variant: 'outline',
        icon: <Send className="size-4" />,
      },
      {
        id: 'B12_NAV_NEWSLETTER',
        label: 'Mở Bản tin Email Cẩm nang ngành học 2027 (/newsletter)',
        description: 'Trình thiết kế email kéo-thả: nội dung, thiết kế, danh sách nhận & lịch gửi',
        variant: 'outline',
        icon: <Mail className="size-4" />,
      },
    ],
  },
  {
    stepNumber: 13,
    code: 'B13',
    stage: 'Giai đoạn 5: Đa nền tảng, Lịch đăng, Analytics, SePay & Admin',
    stageShort: 'GĐ 5: Xuất bản, SePay & Admin',
    timeBudget: '16:15 - 17:45',
    title: 'Xuất bản Đa nền tảng, Lịch đăng bài 4 tuần (/calendar) & Dashboard',
    shortTitle: 'Xuất bản, Lịch 4 tuần & Analytics',
    frCode: 'FR 3.8.8 - 3.8.15',
    role: 'Creator',
    actorName: 'Nguyễn Chơn Phước',
    actorEmail: 'user13@demo.brandhub.test',
    routeTemplate: '/workspaces/{workspace_id}/posts/dashboard',
    manualBrowserCue:
      'Bấm [1] mở Bảng điều phối Bài đăng 4 tuần (/posts/dashboard), sau đó bấm [2] mở Lịch 4 tuần (/calendar) và [3] mở Dashboard tương tác.',
    talkingPoints: [
      'Danh sách bài đăng phản ánh trọn vẹn 4 tuần: các bài Tuần 1-2 đã lên sóng, bài Tuần 3 sẵn sàng xuất bản và bài Tuần 4 đã hẹn giờ.',
      'Trang Lịch xuất bản /calendar hiển thị trực quan mật độ phủ sóng trên 4 nền tảng.',
      'Toàn bộ chỉ số Reach, Impressions, Reactions từ 38 lượt phát hành đổ trực tiếp về Dashboard phân tích.',
    ],
    presenterScript:
      'Khi bài viết Tuần 3 đã ở trạng thái APPROVED, Creator theo dõi tiến độ phát hành trên Bảng điều phối bài đăng đa nền tảng. Mở sang trang Lịch xuất bản (/calendar), hội đồng có thể nhìn thấy bức tranh toàn cảnh 4 tuần tuyển sinh từ các bài đã lên sóng tới lịch hẹn chốt hồ sơ ở Tuần 4, đồng thời toàn bộ chỉ số Reach, Impressions và Reactions từ 4 nền tảng đều đổ về Dashboard phân tích theo thời gian thực.',
    expectedOutcome:
      'Danh sách 17 bài viết hiển thị rõ trên /posts/dashboard, lịch đăng 4 tuần hiển thị trực quan trên /calendar và biểu đồ tương tác đa nền tảng cập nhật đầy đủ trên /dashboard.',
    fields: [
      {
        field: 'Chuỗi bài đăng đa nền tảng trong 4 tuần chiến dịch',
        actionType: 'Tự động điền sẵn',
        value:
          'Các bài PUBLISHED (Tuần 1-2 & đầu Tuần 3, tổng 38 lượt phát hành trên FB/IG/TikTok/Threads) + bài APPROVED vừa duyệt + 2 bài SCHEDULED hẹn giờ Tuần 4',
      },
    ],
    actions: [
      {
        id: 'B13_NAV_PUBLISH',
        label: 'Mở Bảng điều phối Bài đăng 4 tuần (/posts/dashboard)',
        description: 'Điều hướng Creator tới /workspaces/{workspace_id}/posts/dashboard',
        variant: 'primary',
        icon: <Send className="size-4" />,
      },
      {
        id: 'B13_NAV_CALENDAR',
        label: 'Mở Lịch xuất bản Chiến dịch 4 tuần (/calendar)',
        description: 'Xem lịch phân bổ bài viết từ Tuần 1 đến Tuần 4 trên các nền tảng',
        variant: 'outline',
        icon: <Calendar className="size-4" />,
      },
      {
        id: 'B13_NAV_DASHBOARD',
        label: 'Mở Dashboard Phân tích Tương tác (/dashboard)',
        description: 'Xem thống kê Reach, Impressions, Reactions & tiến độ chiến dịch',
        variant: 'outline',
        icon: <Play className="size-4" />,
      },
      {
        id: 'B13_NAV_PRESS',
        label: 'Mở Tuyến bài Báo chí VnExpress Giáo dục Tuần 4 (/press)',
        description: 'Thông cáo báo chí, danh sách phóng viên, nhật ký liên hệ & link tin bài đã lên',
        variant: 'outline',
        icon: <Newspaper className="size-4" />,
      },
    ],
  },
  {
    stepNumber: 14,
    code: 'B14',
    stage: 'Giai đoạn 5: Đa nền tảng, Lịch đăng, Analytics, SePay & Admin',
    stageShort: 'GĐ 5: Xuất bản, SePay & Admin',
    timeBudget: '17:45 - 18:45',
    title: 'Owner nâng cấp gói cước SE08 Digital qua SePay (VietQR) & Ví AI Credit',
    shortTitle: 'Nâng cấp gói VietQR & Ví AI',
    frCode: 'FR 3.9.1 - 3.9.6',
    role: 'Owner',
    actorName: 'Lê Trí Trung',
    actorEmail: 'user177@demo.brandhub.test',
    routeTemplate: '/subscription/plans',
    manualBrowserCue:
      'Bấm [1] mở bảng gói cước (bấm "Nâng cấp" để tạo mã VietQR SePay) -> Bấm [2] xem Ví AI Credit 8.500 điểm của SE08 Digital.',
    talkingPoints: [
      'Owner Lê Trí Trung kiểm tra hạn mức gói dịch vụ và ví tín dụng AI (hiện có 8.500 credits, cấp hạn mức 5.000 credits cho Workspace ĐH FPT).',
      'Thực hiện nâng cấp gói cước SaaS cho SE08 Digital Agency để mở rộng số lượng Workspace khách hàng.',
      'Tích hợp cổng SePay sinh mã VietQR động và tự động đối soát kích hoạt qua webhook.',
    ],
    presenterScript:
      'Để phục vụ đồng thời nhiều chiến dịch lớn cho khách hàng, Owner Lê Trí Trung truy cập trang Quản lý gói dịch vụ để nâng cấp gói cước qua cổng SePay bằng mã VietQR động, đồng thời kiểm soát trực tiếp Ví tín dụng AI 8.500 điểm phân bổ cho từng Workspace.',
    expectedOutcome:
      'Hiển thị bảng so sánh các gói dịch vụ SaaS qua SePay (VietQR) và trang quản lý Ví AI Credit của SE08 Digital Agency.',
    fields: [
      {
        field: 'Cổng thanh toán & Ví tín dụng AI của SE08 Digital Agency',
        actionType: 'Tự động điền sẵn',
        value: 'Thanh toán quét mã VietQR qua SePay | Số dư ví AI hiện tại: 8.500 credits (hạn mức Workspace ĐH FPT: 5.000 credits)',
      },
    ],
    actions: [
      {
        id: 'B14_NAV_PLANS',
        label: 'Mở trang Nâng cấp gói dịch vụ (/subscription/plans)',
        description: 'Điều hướng Owner tới /subscription/plans (SePay VietQR)',
        variant: 'primary',
        icon: <Play className="size-4" />,
      },
      {
        id: 'B14_NAV_CREDITS',
        label: 'Mở Ví AI Credit SE08 Digital (/credit)',
        description: 'Xem số dư 8.500 điểm và hạn mức phân bổ cho Workspace ĐH FPT 2027',
        variant: 'outline',
        icon: <Sparkles className="size-4" />,
      },
    ],
  },
  {
    stepNumber: 15,
    code: 'B15',
    stage: 'Giai đoạn 5: Đa nền tảng, Lịch đăng, Analytics, SePay & Admin',
    stageShort: 'GĐ 5: Xuất bản, SePay & Admin',
    timeBudget: '18:45 - 20:00',
    title: 'Admin giám sát doanh thu nền tảng & Hàng đợi kiểm duyệt (3.10.4)',
    shortTitle: 'Admin Doanh thu & Kiểm duyệt',
    frCode: 'FR 3.10.1 - 3.10.14',
    role: 'Admin',
    actorName: 'Quản trị viên BrandHub',
    actorEmail: 'admin@demo.brandhub.test',
    routeTemplate: '/admin?view=revenue',
    manualBrowserCue:
      'Bấm [1] xem biểu đồ doanh thu toàn nền tảng -> Bấm [2] mở Hàng đợi kiểm duyệt nội dung cộng đồng (FR 3.10.4) khép lại phần trình diễn.',
    talkingPoints: [
      'Góc nhìn Quản trị viên BrandHub (Admin) giám sát doanh thu gói đăng ký SaaS từ các Agency trên toàn nền tảng.',
      'Theo dõi trạng thái đối soát các giao dịch thanh toán SePay (VietQR) và cấu hình gói cước.',
      'Kiểm soát Hàng đợi kiểm duyệt nội dung cộng đồng (FR 3.10.4) gồm 3 bản ghi cảnh báo thực tế để giữ môi trường xuất bản an toàn.',
    ],
    presenterScript:
      'Khép lại luồng trình diễn, ở góc nhìn Quản trị viên BrandHub (Admin), hệ thống cung cấp bức tranh tổng thể về doanh thu gói đăng ký từ các Agency như SE08 Digital, đồng thời duy trì Hàng đợi kiểm duyệt an toàn nội dung cộng đồng để rà soát các cảnh báo vi phạm phát sinh trên toàn nền tảng.',
    expectedOutcome:
      'Hiển thị biểu đồ doanh thu SaaS toàn hệ thống và danh sách 3 bản ghi thực tế trong Hàng đợi kiểm duyệt nội dung của Admin.',
    fields: [
      {
        field: 'Phạm vi giám sát của Admin toàn nền tảng',
        actionType: 'Tự động điền sẵn',
        value:
          'Thống kê doanh thu gói đăng ký SePay (VietQR), quản lý gói cước, cấu hình bảng giá AI Credit & Hàng đợi kiểm duyệt nội dung (FR 3.10.4)',
      },
    ],
    actions: [
      {
        id: 'B15_NAV_ADMIN_REVENUE',
        label: 'Mở Dashboard Doanh thu toàn hệ thống (Admin)',
        description: 'Điều hướng Admin tới /admin?view=revenue',
        variant: 'primary',
        icon: <Play className="size-4" />,
      },
      {
        id: 'B15_NAV_ADMIN_MODERATION',
        label: 'Mở Hàng đợi Kiểm duyệt Nội dung (FR 3.10.4)',
        description: 'Điều hướng Admin tới /admin?view=moderation',
        variant: 'outline',
        icon: <ShieldAlert className="size-4" />,
      },
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
        {/* Sidebar dọc B1 -> B15: liệt kê đủ cả quy trình cho Hội đồng theo dõi tổng quan */}
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
