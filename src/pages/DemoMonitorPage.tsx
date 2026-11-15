import React, { useState, useEffect, useCallback, useRef } from 'react';
import {
  Play,
  Pause,
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
  ChevronRight,
  Sliders,
  Eye,
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
  Clock,
  MousePointerClick,
  ArrowRight,
  CheckCheck,
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
  AstryxSegmentedControl,
  AstryxSegmentedControlItem,
  AstryxCollapsible,
  AstryxDialog,
  AstryxKbd,
  AstryxSwitch,
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
  role: 'Owner' | 'Manager' | 'Creator' | 'Client' | 'Admin';
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
  role: 'Owner' | 'Manager' | 'Creator' | 'Client' | 'Admin';
  shortLabel: string;
  fullName: string;
  email: string;
  desc: string;
}> = [
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
      'Bấm [1] xem bảng 20 công việc & 5 Subtask bài Tuần 3; bấm [3] xem 8 phiếu Khảo sát lớp 12 và bấm [4] xem Yêu cầu từ Ban Tuyển sinh.',
    talkingPoints: [
      '20 công việc phân công chuyên môn hóa cho 3 Creator nhóm SE08: Phước (Social), Tuấn (Key Visual, Reels & Workshop), Ân (Báo chí, Email & Khảo sát).',
      'Bài trọng điểm Tuần 3 có 5 Role Subtasks phối hợp chéo giữa Ân (Nghiên cứu), Tuấn (Key Visual) và Phước (Soạn bài).',
      'Liên kết trực tiếp với trang Khảo sát nguyện vọng học sinh lớp 12 (8 phản hồi) và trang Yêu cầu nội dung từ nhà trường.',
    ],
    presenterScript:
      'Khi chiến dịch đi vào vận hành, toàn bộ 20 đầu việc trong 4 tuần được phân công rõ cho 3 Creator của nhóm SE08: Nguyễn Chơn Phước phụ trách nội dung đa nền tảng, Nguyễn Minh Tuấn đảm nhận thiết kế Key Visual, dựng Reels và kịch bản chuỗi Workshop THPT, còn Hà Văn Ân phụ trách thông cáo báo chí VnExpress/Thanh Niên, bản tin Email và khảo sát học sinh lớp 12. Đặc biệt ở bài trọng điểm Tuần 3 đang thực hiện, 5 Subtask con cũng được phối hợp chéo giữa Tuấn, Ân và Phước rất chặt chẽ.',
    expectedOutcome:
      'Hiển thị đầy đủ 20 công việc theo tiến độ thực tế của tuần thứ 3, chi tiết 5 Subtask không thiếu trường nào, cùng bảng kết quả 8 phiếu khảo sát học sinh THPT và 2 yêu cầu từ khách hàng.',
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
        description: 'Xem khảo sát 4 câu hỏi và 8 phản hồi thực tế của học sinh lớp 12',
        variant: 'outline',
        icon: <ClipboardList className="size-4" />,
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
      'Bấm [1] -> [2] -> [3] -> [4] để lướt nhanh 4 kết nối OAuth (Facebook, Instagram, TikTok, Threads), 8 Hashtag tuyển sinh, Mẫu Email và Lịch sử gửi lô Email.',
    talkingPoints: [
      'Cả 4 nền tảng chính thức của hệ thống gồm Facebook, Instagram, TikTok và Threads đều đã kết nối OAuth hoạt động tốt.',
      'Bộ 8 Hashtag chuẩn mùa tuyển sinh 2027 được phân loại sẵn để tái sử dụng nhất quán.',
      'Mẫu Email và lịch sử gửi vé mời tham dự chuỗi Workshop THPT cho học sinh lớp 12 sẵn sàng trong cùng Workspace.',
    ],
    presenterScript:
      'Trước khi xuất bản đồng loạt, Manager kiểm tra hạ tầng kênh truyền thông của Workspace: cả 4 tài khoản chính thức của Tuyển sinh Đại học FPT trên Facebook, Instagram, TikTok và Threads đều đang kết nối hoạt động qua OAuth. Bên cạnh đó, bộ Hashtag bắt buộc của chiến dịch cùng mẫu Email và lịch sử gửi vé mời tham dự Workshop cho học sinh THPT cũng được chuẩn hóa đồng bộ.',
    expectedOutcome:
      'Hiển thị 4 kết nối OAuth hoạt động tốt (Facebook, Instagram, TikTok, Threads), 8 Hashtag chiến dịch, 2 mẫu Email và 2 lô gửi Email hoàn tất.',
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
          '8 Hashtag chuẩn (#DaiHocFPT, #TuyenSinhFPTU2027, #WorkshopTHPT...), 2 Mẫu Email & 2 Lô gửi Email (6 lượt gửi thành công)',
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
        description: 'Xem 8 hashtag phân loại thương hiệu, ngành học và học bổng',
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
      'Toàn bộ chỉ số Reach, Impressions, Reactions từ 22 lượt phát hành đổ trực tiếp về Dashboard phân tích.',
    ],
    presenterScript:
      'Khi bài viết Tuần 3 đã ở trạng thái APPROVED, Creator theo dõi tiến độ phát hành trên Bảng điều phối bài đăng đa nền tảng. Mở sang trang Lịch xuất bản (/calendar), hội đồng có thể nhìn thấy bức tranh toàn cảnh 4 tuần tuyển sinh từ các bài đã lên sóng tới lịch hẹn chốt hồ sơ ở Tuần 4, đồng thời toàn bộ chỉ số Reach, Impressions và Reactions từ 4 nền tảng đều đổ về Dashboard phân tích theo thời gian thực.',
    expectedOutcome:
      'Danh sách 13 bài viết hiển thị rõ trên /posts/dashboard, lịch đăng 4 tuần hiển thị trực quan trên /calendar và biểu đồ tương tác đa nền tảng cập nhật đầy đủ trên /dashboard.',
    fields: [
      {
        field: 'Chuỗi bài đăng đa nền tảng trong 4 tuần chiến dịch',
        actionType: 'Tự động điền sẵn',
        value:
          'Các bài PUBLISHED (Tuần 1-2 & đầu Tuần 3, tổng 22 lượt phát hành trên FB/IG/TikTok/Threads) + bài APPROVED vừa duyệt + 2 bài SCHEDULED hẹn giờ Tuần 4',
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
    ],
  },
  {
    stepNumber: 14,
    code: 'B14',
    stage: 'Giai đoạn 5: Đa nền tảng, Lịch đăng, Analytics, SePay & Admin',
    stageShort: 'GĐ 5: Xuất bản, SePay & Admin',
    timeBudget: '17:45 - 18:45',
    title: 'Owner nâng cấp gói cước SE08 Digital qua SePay / PayOS (VietQR) & Ví AI Credit',
    shortTitle: 'Nâng cấp gói VietQR & Ví AI',
    frCode: 'FR 3.9.1 - 3.9.6',
    role: 'Owner',
    actorName: 'Lê Trí Trung',
    actorEmail: 'user177@demo.brandhub.test',
    routeTemplate: '/subscription/plans',
    manualBrowserCue:
      'Bấm [1] mở bảng gói cước (bấm "Nâng cấp" để tạo mã VietQR SePay/PayOS) -> Bấm [2] xem Ví AI Credit 8.500 điểm của SE08 Digital.',
    talkingPoints: [
      'Owner Lê Trí Trung kiểm tra hạn mức gói dịch vụ và ví tín dụng AI (hiện có 8.500 credits, cấp hạn mức 5.000 credits cho Workspace ĐH FPT).',
      'Thực hiện nâng cấp gói cước SaaS cho SE08 Digital Agency để mở rộng số lượng Workspace khách hàng.',
      'Tích hợp cổng SePay / PayOS sinh mã VietQR động và tự động đối soát kích hoạt qua webhook.',
    ],
    presenterScript:
      'Để phục vụ đồng thời nhiều chiến dịch lớn cho khách hàng, Owner Lê Trí Trung truy cập trang Quản lý gói dịch vụ để nâng cấp gói cước qua cổng SePay / PayOS bằng mã VietQR động, đồng thời kiểm soát trực tiếp Ví tín dụng AI 8.500 điểm phân bổ cho từng Workspace.',
    expectedOutcome:
      'Hiển thị bảng so sánh các gói dịch vụ SaaS qua SePay / PayOS và trang quản lý Ví AI Credit của SE08 Digital Agency.',
    fields: [
      {
        field: 'Cổng thanh toán & Ví tín dụng AI của SE08 Digital Agency',
        actionType: 'Tự động điền sẵn',
        value: 'Thanh toán quét mã VietQR qua SePay / PayOS | Số dư ví AI hiện tại: 8.500 credits (hạn mức Workspace ĐH FPT: 5.000 credits)',
      },
    ],
    actions: [
      {
        id: 'B14_NAV_PLANS',
        label: 'Mở trang Nâng cấp gói dịch vụ (/subscription/plans)',
        description: 'Điều hướng Owner tới /subscription/plans (SePay / PayOS VietQR)',
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
      'Theo dõi trạng thái đối soát các giao dịch thanh toán SePay / PayOS và cấu hình gói cước.',
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
          'Thống kê doanh thu gói đăng ký SePay/PayOS, quản lý gói cước, cấu hình bảng giá AI Credit & Hàng đợi kiểm duyệt nội dung (FR 3.10.4)',
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
  { id: 'QA_EVENT_EDITOR', label: 'Sự kiện FPTU Open Day (/event)', role: 'Manager', desc: '5 phân khu sự kiện lớn + Runsheet' },
  { id: 'QA_WORKSHOP_EDITOR', label: 'Chuỗi Workshop THPT (/workshop)', role: 'Manager', desc: 'Diễn giả, Lịch trình & Phiếu đăng ký' },
  { id: 'QA_PRESS_EDITOR', label: 'PR Báo chí VnExpress (/press)', role: 'Creator', desc: 'Thông cáo báo chí & Liên hệ phóng viên' },
  { id: 'QA_KOL_EDITOR', label: 'Booking KOL Schannel (/kol)', role: 'Manager', desc: 'Shortlist, Chi phí & Báo cáo nghiệm thu' },
  { id: 'QA_NEWSLETTER_EDITOR', label: 'Bản tin Email (/newsletter)', role: 'Creator', desc: 'Thiết kế khối Email Cẩm nang 2027' },
  { id: 'QA_AI_TRENDS', label: 'AI Xu hướng MXH (/ai-studio/trends)', role: 'Manager', desc: '6 xu hướng tuyển sinh trực tiếp từ Redis' },
  { id: 'QA_AI_RAG', label: 'AI Tri thức RAG (/ai-studio/knowledge-base)', role: 'Manager', desc: 'Tài liệu quy chế & học bổng ĐH FPT' },
  { id: 'QA_AI_AMBASSADORS', label: 'AI Đại sứ ảo (/ai-studio/ambassadors)', role: 'Creator', desc: 'Nhân vật Minh Anh & Hoàng Khôi K23' },
  { id: 'QA_CLIENT_PORTAL', label: 'Cổng Khách hàng (/portal)', role: 'Client', desc: '2 hạng mục Open Day chờ ĐH FPT duyệt' },
  { id: 'QA_CLIENT_VAULT', label: 'Kho riêng Client Vault (/library)', role: 'Client', desc: 'Tư liệu gốc ĐH FPT chia sẻ sang SE08' },
  { id: 'QA_COLLABORATORS', label: 'Danh bạ 10 Đối tác (/collaborators)', role: 'Owner', desc: '6 đối tác ĐH FPT + 4 đối tác đa ngành' },
  { id: 'QA_PUBLIC_PACKAGE', label: 'Link Chào giá Gói (Guest)', role: 'Owner', desc: '/packages/share/goi-tuyen-sinh-dh-fpt-2027' },
  { id: 'QA_PUBLIC_SURVEY', label: 'Link Khảo sát THPT (Guest)', role: 'Client', desc: '/public/surveys/khao-sat-chon-nganh-fptu-2027' },
  { id: 'QA_ADMIN_CREDIT_PRICES', label: 'Bảng giá AI Credit (/admin/credit-prices)', role: 'Admin', desc: 'Cấu hình đơn giá 7 nghiệp vụ AI' },
];

function formatStopwatch(totalSeconds: number): string {
  const mins = Math.floor(totalSeconds / 60);
  const secs = totalSeconds % 60;
  return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

export const DemoMonitorPage: React.FC = () => {
  const [monitorUrl, setMonitorUrl] = useState<string>('http://localhost:3999');
  const [status, setStatus] = useState<MonitorStatus | null>(null);
  const [connected, setConnected] = useState<boolean>(false);
  const [activeStepIndex, setActiveStepIndex] = useState<number>(0);
  const [busyAction, setBusyAction] = useState<string | null>(null);
  const [toastMessage, setToastMessage] = useState<{ text: string; isError?: boolean } | null>(null);
  const [copiedKey, setCopiedKey] = useState<string | null>(null);
  const [showConfigModal, setShowConfigModal] = useState<boolean>(false);
  const [showResetConfirm, setShowResetConfirm] = useState<boolean>(false);

  // Chế độ hiển thị tối ưu cho thuyết trình sân khấu
  const [viewMode, setViewMode] = useState<string>('stage'); // 'stage' | 'detail'
  const [stageFilter, setStageFilter] = useState<string>('all');
  const [largeScript, setLargeScript] = useState<boolean>(true);
  const [doneActions, setDoneActions] = useState<Record<string, boolean>>({});

  // Đồng hồ bấm giờ 20 phút bảo vệ đồ án
  const [elapsedSeconds, setElapsedSeconds] = useState<number>(0);
  const [timerRunning, setTimerRunning] = useState<boolean>(false);

  const [customTexts, setCustomTexts] = useState<Record<string, string>>(DEFAULT_DEMO_TEXTS);
  const [configIds, setConfigIds] = useState({
    app_url: 'http://localhost:3000',
    agency_id: '359a1839-18c7-48e2-8a68-f5f68c3375b6',
    workspace_id: 'b47477c4-13ad-44ff-8c49-f73f1837461b',
    campaign_id: 'd7e00000-0000-4000-8000-000000000301',
    task_id: 'c6453698-cf56-38c1-96d2-90ccdd985228',
  });

  const activePillRef = useRef<HTMLButtonElement | null>(null);

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

  useEffect(() => {
    if (!timerRunning) return;
    const id = setInterval(() => {
      setElapsedSeconds((s) => s + 1);
    }, 1000);
    return () => clearInterval(id);
  }, [timerRunning]);

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
      if (!timerRunning && elapsedSeconds === 0) {
        setTimerRunning(true);
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
    [busyAction, customTexts, elapsedSeconds, fetchMonitorStatus, monitorUrl, showToast, timerRunning]
  );

  // Nút dẫn dắt thông minh 1 chạm (Phím Space): Chạy thao tác kế tiếp trong bước, nếu xong hết thì qua bước mới
  const handleSmartAdvance = useCallback(() => {
    if (busyAction !== null) return;
    if (nextPendingAction) {
      triggerStepAction(nextPendingAction.id);
    } else if (activeStepIndex < DEMO_STEPS.length - 1) {
      setActiveStepIndex((i) => Math.min(DEMO_STEPS.length - 1, i + 1));
    }
  }, [activeStepIndex, busyAction, nextPendingAction, triggerStepAction]);

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
      if (showResetConfirm || showConfigModal) return;

      if (e.code === 'Space') {
        e.preventDefault();
        handleSmartAdvance();
        return;
      }
      if (e.key === 'ArrowRight' || e.key === 'PageDown') {
        e.preventDefault();
        setActiveStepIndex((i) => Math.min(DEMO_STEPS.length - 1, i + 1));
        return;
      }
      if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        e.preventDefault();
        setActiveStepIndex((i) => Math.max(0, i - 1));
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
    currentStep,
    handleLoginSingleRole,
    handleSmartAdvance,
    showConfigModal,
    showResetConfirm,
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
        showToast('Đã mở và đăng nhập tự động cả 5 cửa sổ Chrome cho 5 vai trò!');
      } else {
        showToast(data.error || 'Có lỗi khi đăng nhập 5 vai trò.', true);
      }
      await fetchMonitorStatus();
    } catch {
      showToast('Không kết nối được tới máy chủ Selenium (cổng 3999).', true);
    } finally {
      setBusyAction(null);
    }
  };

  const handleArrangeWindows = async (mode: 'split' | 'maximize') => {
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
        setDoneActions({});
        setActiveStepIndex(0);
        setElapsedSeconds(0);
        setTimerRunning(false);
        showToast(data.message || 'Đã khôi phục dữ liệu PostgreSQL & MongoDB về trạng thái chuẩn.');
      } else {
        showToast(data.error || 'Lỗi khi nạp lại dữ liệu mẫu.', true);
      }
    } catch {
      showToast('Không kết nối được tới máy chủ Selenium (cổng 3999).', true);
    } finally {
      setBusyAction(null);
    }
  };

  const handleSaveConfig = async () => {
    try {
      const res = await fetch(`${monitorUrl}/api/config`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(configIds),
      });
      const data = await res.json();
      if (data.ok) {
        showToast('Đã cập nhật cấu hình ID chiến dịch và công việc.');
        setShowConfigModal(false);
        fetchMonitorStatus();
      }
    } catch {
      showToast('Không thể lưu cấu hình vào cổng 3999.', true);
    }
  };

  const resolvedRoute = currentStep.routeTemplate
    .replace('{agency_id}', configIds.agency_id)
    .replace('{workspace_id}', configIds.workspace_id)
    .replace('{campaign_id}', configIds.campaign_id)
    .replace('{task_id}', configIds.task_id);

  const visibleSteps = DEMO_STEPS.filter((step) => {
    if (stageFilter === 'all') return true;
    return step.stage.startsWith(`Giai đoạn ${stageFilter}`);
  });

  const renderFieldsTable = () => (
    <div className="divide-y divide-slate-100 border border-slate-200 rounded-xl overflow-hidden">
      {currentStep.fields.map((f, i) => {
        const liveValue = f.copyKey ? customTexts[f.copyKey] ?? f.value : f.value;
        const isCopied = copiedKey === `${currentStep.code}_${i}`;
        return (
          <div key={i} className="p-3.5 bg-white hover:bg-orange-50/20 space-y-2">
            <div className="flex flex-wrap items-center justify-between gap-2">
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold text-slate-900">{f.field}</span>
                <AstryxBadge label={f.actionType} variant="orange" />
              </div>

              <AstryxButton
                label={isCopied ? 'Đã chép' : 'Sao chép'}
                variant="secondary"
                size="sm"
                icon={
                  isCopied ? (
                    <Check className="size-3 text-orange-600" />
                  ) : (
                    <Copy className="size-3 text-orange-600" />
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
                className="w-full p-2.5 text-xs text-slate-800 bg-orange-50/30 border border-orange-200 rounded-lg focus:bg-white focus:border-orange-500 focus:outline-none leading-relaxed"
              />
            ) : (
              <div className="p-2.5 text-xs text-slate-700 bg-slate-50 rounded-lg border border-slate-200/80 whitespace-pre-wrap leading-relaxed">
                {liveValue}
              </div>
            )}

            {f.note && <div className="text-[11px] text-orange-700 font-medium">Lưu ý: {f.note}</div>}
          </div>
        );
      })}
    </div>
  );

  return (
    <div className="min-h-dvh bg-white text-slate-900 font-sans">
      {/* Hộp thoại xác nhận trước khi khôi phục DB để tránh bấm nhầm trên sân khấu */}
      <AstryxDialog
        isOpen={showResetConfirm}
        onOpenChange={setShowResetConfirm}
        width={440}
        padding={5}
        aria-label="Xác nhận khôi phục dữ liệu gốc"
      >
        <div className="space-y-4">
          <div className="flex items-start gap-3">
            <div className="size-10 rounded-xl bg-orange-100 text-orange-700 flex items-center justify-center shrink-0">
              <Database className="size-5" />
            </div>
            <div className="space-y-1">
              <AstryxHeading level={3} className="text-base font-bold text-slate-900 text-balance">
                Khôi phục toàn bộ dữ liệu gốc PostgreSQL &amp; MongoDB?
              </AstryxHeading>
              <p className="text-xs text-slate-600 leading-relaxed text-pretty">
                Thao tác này sẽ chạy lại kịch bản chuẩn bị dữ liệu ban đầu (đặt lại trạng thái bài trọng điểm Tuần 3 về bản nháp trước khi gửi duyệt v1 và xóa dấu tích tiến độ hiện tại).
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

      {/* Thanh thông báo nổi (Toast) bằng Meta Astryx Banner */}
      {toastMessage && (
        <div className="fixed bottom-4 right-4 z-50 max-w-md shadow-lg rounded-xl overflow-hidden border border-orange-200 bg-white">
          <AstryxBanner
            status={toastMessage.isError ? 'warning' : 'info'}
            title={toastMessage.isError ? 'Thông báo điều khiển' : 'Đã thực thi'}
            description={toastMessage.text}
            isDismissable
            onDismiss={() => setToastMessage(null)}
          />
        </div>
      )}

      {/* Thanh Header gọn gàng chuẩn Trắng - Cam tối ưu cho sân khấu */}
      <header className="sticky top-0 z-30 bg-white border-b border-orange-200 shadow-xs">
        <div className="max-w-[1600px] mx-auto px-4 py-2.5 flex flex-wrap items-center justify-between gap-3">
          {/* Cụm thương hiệu + Chuyển chế độ Sân khấu / Chi tiết */}
          <div className="flex flex-wrap items-center gap-3">
            <div className="flex items-center gap-2.5">
              <div className="size-9 rounded-xl bg-orange-600 flex items-center justify-center text-white font-bold text-sm shadow-xs">
                BH
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <AstryxHeading level={1} className="text-sm sm:text-base font-bold text-slate-900 text-balance">
                    Điều Khiển Thuyết Trình SE08
                  </AstryxHeading>
                  <span className="hidden xl:inline-flex">
                    <AstryxBadge label="ĐH FPT 2027 • 4 Tuần" variant="orange" />
                  </span>
                </div>
              </div>
            </div>

            <AstryxSegmentedControl
              label="Chế độ giao diện"
              size="sm"
              value={viewMode}
              onChange={setViewMode}
            >
              <AstryxSegmentedControlItem value="stage" label="Sân khấu (Gọn)" />
              <AstryxSegmentedControlItem value="detail" label="Chi tiết (2 cột)" />
            </AstryxSegmentedControl>
          </div>

          {/* Cụm Đồng hồ 20 phút + Chia đôi màn hình + Đăng nhập 5 vai trò */}
          <div className="flex flex-wrap items-center gap-2">
            {/* Đồng hồ bấm giờ 20 phút */}
            <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-orange-50/80 border border-orange-200 text-xs">
              <Clock className="size-3.5 text-orange-600 shrink-0" />
              <span className="font-bold text-slate-900 tabular-nums">
                {formatStopwatch(elapsedSeconds)}
              </span>
              <span className="text-slate-400 tabular-nums">/ 20:00</span>
              <button
                type="button"
                aria-label={timerRunning ? 'Tạm dừng đồng hồ' : 'Bắt đầu bấm giờ'}
                onClick={() => setTimerRunning((v) => !v)}
                className="p-1 rounded hover:bg-orange-100 text-orange-700 cursor-pointer"
              >
                {timerRunning ? <Pause className="size-3" /> : <Play className="size-3" />}
              </button>
              <button
                type="button"
                aria-label="Đặt lại đồng hồ về 00:00"
                onClick={() => {
                  setTimerRunning(false);
                  setElapsedSeconds(0);
                }}
                className="p-1 rounded hover:bg-orange-100 text-slate-500 hover:text-orange-700 cursor-pointer"
              >
                <RotateCcw className="size-3" />
              </button>
            </div>

            {/* Trạng thái Selenium */}
            <div className="inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-white border border-slate-200 text-xs font-medium text-slate-700">
              <AstryxStatusDot
                variant={connected ? 'accent' : 'neutral'}
                label={connected ? 'Selenium đã kết nối' : 'Selenium chưa bật'}
                isPulsing={connected}
              />
              <span className="hidden sm:inline">{connected ? 'Đã kết nối' : 'Chưa bật :3999'}</span>
            </div>

            {/* Chia màn hình để Chrome không đè lên Bàn điều khiển */}
            <div className="hidden md:inline-flex items-center rounded-lg border border-orange-200 bg-orange-50/50 p-0.5 gap-0.5">
              <button
                type="button"
                onClick={() => handleArrangeWindows('split')}
                disabled={busyAction !== null}
                title="Xếp 5 cửa sổ Chrome gọn bên trái 71%, chừa 29% bên phải cho Bàn điều khiển"
                className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-xs font-semibold cursor-pointer disabled:opacity-50 ${
                  status?.window_mode === 'split'
                    ? 'bg-orange-600 text-white'
                    : 'text-slate-700 hover:bg-orange-100/70'
                }`}
              >
                <Columns2 className="size-3.5" />
                <span>Chia màn hình</span>
              </button>
              <button
                type="button"
                onClick={() => handleArrangeWindows('maximize')}
                disabled={busyAction !== null}
                title="Phóng to toàn màn hình các cửa sổ Chrome (dùng khi có 2 màn hình)"
                className={`inline-flex items-center gap-1 px-2 py-1 rounded-md text-xs font-semibold cursor-pointer disabled:opacity-50 ${
                  status?.window_mode === 'maximize'
                    ? 'bg-orange-600 text-white'
                    : 'text-slate-700 hover:bg-orange-100/70'
                }`}
              >
                <Maximize2 className="size-3.5" />
                <span className="hidden xl:inline">Phóng to</span>
              </button>
            </div>

            <AstryxButton
              label="Đăng nhập 5 Vai trò"
              variant="primary"
              size="sm"
              icon={<Users className="size-3.5" />}
              isDisabled={busyAction !== null}
              isLoading={busyAction === 'LOGIN_ALL'}
              onClick={handleLoginAll}
            />

            <AstryxButton
              label="Khôi phục DB"
              variant="secondary"
              size="sm"
              icon={<Database className="size-3.5 text-orange-600" />}
              isDisabled={busyAction !== null}
              isLoading={busyAction === 'RESET_DB'}
              onClick={() => setShowResetConfirm(true)}
            />

            <button
              type="button"
              aria-label="Mở cấu hình định danh Demo"
              onClick={() => setShowConfigModal((v) => !v)}
              className="p-2 rounded-lg border border-slate-200 hover:border-orange-300 text-slate-600 hover:text-orange-700 cursor-pointer"
            >
              <Sliders className="size-3.5" />
            </button>
          </div>
        </div>

        {/* Dải 5 Vai trò siêu gọn: Bấm 1 chạm để bật ngay cửa sổ Chrome của vai trò đó lên trên cùng */}
        <div className="bg-orange-50/40 border-t border-orange-100">
          <div className="max-w-[1600px] mx-auto px-4 py-1.5 flex items-center gap-2 overflow-x-auto">
            <span className="text-[11px] font-bold text-slate-500 shrink-0 hidden sm:inline">
              Cửa sổ Chrome:
            </span>
            <div className="flex items-center gap-1.5 flex-1 min-w-0">
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
                    className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg border text-xs font-semibold shrink-0 cursor-pointer disabled:opacity-50 ${
                      isCurrentStepRole
                        ? 'bg-orange-600 text-white border-orange-600 shadow-xs'
                        : 'bg-white text-slate-700 border-slate-200 hover:border-orange-300 hover:bg-orange-50/50'
                    }`}
                  >
                    <span
                      className={`size-2 rounded-full shrink-0 ${
                        roleStat?.alive
                          ? isCurrentStepRole
                            ? 'bg-white'
                            : 'bg-orange-500'
                          : 'bg-slate-300'
                      }`}
                    />
                    <span className="font-bold">{item.role}</span>
                    <span className={isCurrentStepRole ? 'text-orange-100' : 'text-slate-500'}>
                      · {item.shortLabel}
                    </span>
                  </button>
                );
              })}
            </div>
            <div className="hidden lg:flex items-center gap-1.5 text-[11px] text-slate-500 shrink-0">
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

        {/* Thanh nhảy nhanh 15 bước B1 -> B15 (luôn hiện ở Chế độ Sân khấu để không tốn diện tích cột trái) */}
        {viewMode === 'stage' && (
          <div className="bg-white border-t border-slate-100">
            <div className="max-w-[1600px] mx-auto px-4 py-2 flex items-center gap-1.5 overflow-x-auto">
              {DEMO_STEPS.map((step, idx) => {
                const isSelected = idx === activeStepIndex;
                const isStepDone = step.actions.every((a) => Boolean(doneActions[a.id]));
                const hasSomeDone = !isStepDone && step.actions.some((a) => Boolean(doneActions[a.id]));
                return (
                  <button
                    key={step.code}
                    ref={isSelected ? activePillRef : null}
                    type="button"
                    onClick={() => setActiveStepIndex(idx)}
                    title={`${step.code}: ${step.title} (${step.role})`}
                    className={`inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg border text-xs font-semibold shrink-0 cursor-pointer tabular-nums ${
                      isSelected
                        ? 'bg-orange-600 text-white border-orange-600 shadow-xs'
                        : isStepDone
                        ? 'bg-orange-50 text-orange-800 border-orange-300 hover:bg-orange-100/70'
                        : hasSomeDone
                        ? 'bg-orange-50/40 text-slate-800 border-orange-200'
                        : 'bg-white text-slate-600 border-slate-200 hover:border-orange-300'
                    }`}
                  >
                    {isStepDone && !isSelected && (
                      <Check className="size-3 text-orange-600 shrink-0" />
                    )}
                    <span className="font-extrabold">{step.code}</span>
                    <span
                      className={`hidden md:inline max-w-[130px] truncate ${
                        isSelected ? 'text-orange-50' : 'text-slate-600'
                      }`}
                    >
                      {step.shortTitle}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>
        )}
      </header>

      {/* Hộp thoại Cấu hình nhanh (nếu bật) */}
      {showConfigModal && (
        <div className="max-w-[1600px] mx-auto px-4 pt-4">
          <AstryxCard variant="orange" padding={4} className="rounded-2xl border border-orange-200 space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <Terminal className="size-4 text-orange-600" />
                <span>Cấu hình định danh Demo &amp; Cổng điều khiển Selenium</span>
              </h2>
              <AstryxButton
                label="Đóng"
                variant="ghost"
                size="sm"
                onClick={() => setShowConfigModal(false)}
              />
            </div>
            <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
              <div>
                <label className="block text-[11px] font-semibold text-slate-600 mb-1">Monitor API (:3999)</label>
                <input
                  value={monitorUrl}
                  onChange={(e) => setMonitorUrl(e.target.value)}
                  className="w-full px-3 py-1.5 text-xs rounded-lg bg-white border border-slate-200 focus:border-orange-500 focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-[11px] font-semibold text-slate-600 mb-1">Web App URL (:3000)</label>
                <input
                  value={configIds.app_url}
                  onChange={(e) => setConfigIds({ ...configIds, app_url: e.target.value })}
                  className="w-full px-3 py-1.5 text-xs rounded-lg bg-white border border-slate-200 focus:border-orange-500 focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-[11px] font-semibold text-slate-600 mb-1">Workspace ID</label>
                <input
                  value={configIds.workspace_id}
                  onChange={(e) => setConfigIds({ ...configIds, workspace_id: e.target.value })}
                  className="w-full px-3 py-1.5 text-xs font-mono rounded-lg bg-white border border-slate-200 focus:border-orange-500 focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-[11px] font-semibold text-slate-600 mb-1">Campaign ID</label>
                <input
                  value={configIds.campaign_id}
                  onChange={(e) => setConfigIds({ ...configIds, campaign_id: e.target.value })}
                  className="w-full px-3 py-1.5 text-xs font-mono rounded-lg bg-white border border-slate-200 focus:border-orange-500 focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-[11px] font-semibold text-slate-600 mb-1">Task Tuần 3 ID</label>
                <input
                  value={configIds.task_id}
                  onChange={(e) => setConfigIds({ ...configIds, task_id: e.target.value })}
                  className="w-full px-3 py-1.5 text-xs font-mono rounded-lg bg-white border border-slate-200 focus:border-orange-500 focus:outline-none"
                />
              </div>
            </div>
            <div className="flex justify-end">
              <AstryxButton
                label="Lưu cấu hình"
                variant="primary"
                size="sm"
                onClick={handleSaveConfig}
              />
            </div>
          </AstryxCard>
        </div>
      )}

      {/* Bố cục chính: Tối giản 1 cột lớn ở Chế độ Sân khấu | 2 cột ở Chế độ Chi tiết */}
      <main
        className={`mx-auto px-4 py-4 ${
          viewMode === 'stage'
            ? 'max-w-[1040px] space-y-4'
            : 'max-w-[1600px] grid grid-cols-1 lg:grid-cols-12 gap-6'
        }`}
      >
        {/* Cột trái (Chỉ hiện ở Chế độ Chi tiết 2 cột) */}
        {viewMode === 'detail' && (
          <aside className="lg:col-span-4 space-y-3">
            <AstryxCard padding={3} className="rounded-xl border border-orange-200 bg-white space-y-2.5">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold uppercase text-slate-600">
                  Tiến độ ({completedStepsCount}/15 bước đã chạy)
                </span>
                <AstryxBadge label={`Bước ${currentStep.stepNumber}/15`} variant="orange" />
              </div>
              <AstryxProgressBar
                label="Tiến độ các bước demo"
                isLabelHidden
                value={currentStep.stepNumber}
                max={15}
                variant="accent"
              />
              <div className="pt-1 overflow-x-auto">
                <AstryxSegmentedControl
                  label="Lọc theo giai đoạn"
                  size="sm"
                  value={stageFilter}
                  onChange={setStageFilter}
                >
                  <AstryxSegmentedControlItem value="all" label="Tất cả (15)" />
                  <AstryxSegmentedControlItem value="1" label="GĐ 1" />
                  <AstryxSegmentedControlItem value="2" label="GĐ 2" />
                  <AstryxSegmentedControlItem value="3" label="GĐ 3" />
                  <AstryxSegmentedControlItem value="4" label="GĐ 4" />
                  <AstryxSegmentedControlItem value="5" label="GĐ 5" />
                </AstryxSegmentedControl>
              </div>
            </AstryxCard>

            <div className="space-y-1.5 max-h-[calc(100dvh-260px)] overflow-y-auto pr-1">
              {visibleSteps.map((step) => {
                const idx = DEMO_STEPS.findIndex((s) => s.code === step.code);
                const isSelected = idx === activeStepIndex;
                const prev = idx > 0 ? DEMO_STEPS[idx - 1] : null;
                const showStageHeader = stageFilter === 'all' && (!prev || step.stage !== prev.stage);
                const isDone = step.actions.every((a) => Boolean(doneActions[a.id]));

                return (
                  <React.Fragment key={step.code}>
                    {showStageHeader && (
                      <div className="pt-2.5 pb-1 px-2 text-[11px] font-bold uppercase text-orange-700">
                        {step.stage}
                      </div>
                    )}
                    <button
                      type="button"
                      onClick={() => setActiveStepIndex(idx)}
                      className={`w-full text-left p-3 rounded-xl border flex items-start gap-3 cursor-pointer ${
                        isSelected
                          ? 'bg-orange-600 text-white border-orange-600 shadow-xs'
                          : 'bg-white text-slate-800 border-slate-200 hover:border-orange-300 hover:bg-orange-50/40'
                      }`}
                    >
                      <span
                        className={`px-2 py-0.5 rounded-md text-xs font-extrabold shrink-0 mt-0.5 tabular-nums ${
                          isSelected
                            ? 'bg-white text-orange-700'
                            : isDone
                            ? 'bg-orange-100 text-orange-800 border border-orange-300'
                            : 'bg-orange-50 text-orange-700 border border-orange-200'
                        }`}
                      >
                        {isDone && !isSelected ? `✓ ${step.code}` : step.code}
                      </span>
                      <div className="min-w-0 flex-1">
                        <div className="font-semibold text-xs leading-snug">{step.title}</div>
                        <div
                          className={`flex items-center gap-2 mt-1 text-[11px] tabular-nums ${
                            isSelected ? 'text-orange-100' : 'text-slate-500'
                          }`}
                        >
                          <span className="font-semibold">{step.role}</span>
                          <span>•</span>
                          <span className="truncate">{step.actorName}</span>
                          <span>•</span>
                          <span>{step.timeBudget}</span>
                        </div>
                      </div>
                      <ChevronRight
                        className={`size-4 shrink-0 mt-1 ${
                          isSelected ? 'text-white' : 'text-slate-300'
                        }`}
                      />
                    </button>
                  </React.Fragment>
                );
              })}
            </div>
          </aside>
        )}

        {/* Khu vực Điều khiển Chính của Bước Hiện Tại */}
        <section className={viewMode === 'detail' ? 'lg:col-span-8 space-y-4' : 'space-y-4'}>
          <AstryxCard padding={4} className="rounded-2xl bg-white border border-orange-200 shadow-xs space-y-4">
            {/* Hàng 1: Định danh Bước + Báo đổi vai + Nút Trước/Tiếp */}
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div className="space-y-1.5 min-w-0 flex-1">
                <div className="flex flex-wrap items-center gap-1.5">
                  <AstryxBadge label={`Bước ${currentStep.stepNumber}/15 · ${currentStep.code}`} variant="orange" />
                  <AstryxBadge
                    label={`${currentStep.role}: ${currentStep.actorName}`}
                    variant="orange"
                  />
                  <AstryxBadge label={`Khung giờ: ${currentStep.timeBudget}`} variant="neutral" />
                  <AstryxBadge label={currentStep.frCode} variant="neutral" />
                  {roleChangedFromPrev && (
                    <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-bold bg-orange-600 text-white">
                      Chuyển cửa sổ sang {currentStep.role}
                    </span>
                  )}
                </div>

                <AstryxHeading level={2} className="text-lg sm:text-xl font-bold text-slate-900 text-balance">
                  {currentStep.title}
                </AstryxHeading>

                <div className="flex flex-wrap items-center gap-2 text-xs text-slate-500 font-mono">
                  <span>Trang đích:</span>
                  <a
                    href={`${configIds.app_url}${resolvedRoute}`}
                    target="_blank"
                    rel="noreferrer"
                    className="text-orange-600 hover:underline inline-flex items-center gap-1 font-semibold break-all"
                  >
                    <AstryxCode>{resolvedRoute}</AstryxCode>
                    <ExternalLink className="size-3 shrink-0" />
                  </a>
                </div>
              </div>

              <div className="flex items-center gap-2 shrink-0">
                <AstryxButton
                  label="← Trước"
                  variant="secondary"
                  size="sm"
                  isDisabled={activeStepIndex === 0}
                  onClick={() => setActiveStepIndex((i) => Math.max(0, i - 1))}
                />
                <AstryxButton
                  label="Tiếp →"
                  variant="secondary"
                  size="sm"
                  isDisabled={activeStepIndex === DEMO_STEPS.length - 1}
                  onClick={() => setActiveStepIndex((i) => Math.min(DEMO_STEPS.length - 1, i + 1))}
                />
              </div>
            </div>

            {/* Hàng 2: NÚT DẪN THUYẾT TRÌNH 1 CHẠM (SPACE) - Chỉ cần bấm liên tục nút này suốt buổi bảo vệ */}
            <div className="p-3 rounded-xl bg-orange-50/70 border border-orange-200 flex flex-wrap items-center justify-between gap-3">
              <div className="min-w-0 flex-1">
                <div className="text-[11px] font-bold uppercase text-orange-800 flex items-center gap-1.5">
                  <Sparkles className="size-3.5 text-orange-600 shrink-0" />
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

              <button
                type="button"
                disabled={
                  busyAction !== null ||
                  (!nextPendingAction && activeStepIndex === DEMO_STEPS.length - 1)
                }
                onClick={handleSmartAdvance}
                className="inline-flex items-center gap-2.5 px-5 py-2.5 rounded-xl bg-orange-600 hover:bg-orange-700 text-white font-bold text-sm shadow-xs cursor-pointer disabled:opacity-50 shrink-0"
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
                <span className="bg-white/20 text-white px-1.5 py-0.5 rounded text-[11px] font-mono">
                  Space
                </span>
              </button>
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
                    className={`p-3.5 rounded-xl border text-left flex items-start gap-3 cursor-pointer disabled:opacity-50 ${
                      isNextRecommended
                        ? 'bg-orange-600 text-white border-orange-600 hover:bg-orange-700 shadow-xs ring-2 ring-orange-500/25'
                        : isDone
                        ? 'bg-orange-50/50 text-slate-900 border-orange-300 hover:bg-orange-100/60'
                        : 'bg-white text-slate-900 border-slate-200 hover:border-orange-300 hover:bg-orange-50/30'
                    }`}
                  >
                    <div
                      className={`size-8 rounded-lg shrink-0 flex items-center justify-center font-extrabold text-xs tabular-nums ${
                        isNextRecommended
                          ? 'bg-white text-orange-700'
                          : isDone
                          ? 'bg-orange-600 text-white'
                          : 'bg-orange-100 text-orange-700'
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
                      <div className="flex items-center justify-between gap-2">
                        <span className="text-xs sm:text-sm font-bold leading-snug">
                          {idx + 1}. {act.label}
                        </span>
                        <span
                          className={`px-1.5 py-0.5 rounded text-[10px] font-bold shrink-0 ${
                            isNextRecommended
                              ? 'bg-white/20 text-white'
                              : isDone
                              ? 'bg-orange-100 text-orange-800'
                              : 'bg-slate-100 text-slate-600'
                          }`}
                        >
                          {isNextRecommended ? `Phím ${numKey} · Tiếp theo` : isDone ? 'Đã chạy' : `Phím ${numKey}`}
                        </span>
                      </div>
                      <div
                        className={`text-xs mt-0.5 leading-normal ${
                          isNextRecommended ? 'text-orange-100' : 'text-slate-600'
                        }`}
                      >
                        {act.description}
                      </div>
                    </div>
                  </button>
                );
              })}
            </div>

            {/* Hàng 4: Chỉ dẫn thao tác tay trên Chrome (giúp người đứng sân khấu biết rõ có cần bấm thêm nút nào không) */}
            <div className="px-3.5 py-2.5 rounded-xl bg-amber-50/70 border border-orange-200 flex items-start gap-2.5">
              <MousePointerClick className="size-4 text-orange-600 shrink-0 mt-0.5" />
              <div className="text-xs sm:text-sm text-slate-800 leading-relaxed text-pretty">
                <strong className="text-orange-800">Thao tác kết hợp trên Chrome: </strong>
                {currentStep.manualBrowserCue}
              </div>
            </div>

            <AstryxDivider variant="subtle" />

            {/* Hàng 5: Máy nhắc chữ sân khấu (Teleprompter) dễ đọc từ xa */}
            <div className="space-y-3">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div className="text-xs font-bold uppercase text-orange-800 flex items-center gap-1.5">
                  <Eye className="size-4 text-orange-600" />
                  <span>Ý chính trình bày trước Hội đồng ({currentStep.code})</span>
                </div>
                <div className="flex items-center gap-3">
                  {Object.keys(doneActions).length > 0 && (
                    <button
                      type="button"
                      onClick={() => setDoneActions({})}
                      className="text-xs text-slate-500 hover:text-orange-700 underline cursor-pointer"
                    >
                      Xóa dấu tích đã chạy
                    </button>
                  )}
                  <AstryxSwitch
                    label="Chữ lớn dễ đọc"
                    value={largeScript}
                    onChange={setLargeScript}
                  />
                </div>
              </div>

              {/* 3 gạch đầu dòng ngắn gọn để liếc mắt 1 giây nắm ý */}
              <div className="grid grid-cols-1 gap-2">
                {currentStep.talkingPoints.map((pt, i) => (
                  <div
                    key={i}
                    className={`px-3.5 py-2.5 rounded-xl bg-orange-50/40 border border-orange-100 text-slate-900 flex items-start gap-2.5 ${
                      largeScript ? 'text-sm sm:text-base leading-relaxed' : 'text-xs sm:text-sm leading-relaxed'
                    }`}
                  >
                    <span className="size-5 rounded-full bg-orange-600 text-white text-xs font-bold flex items-center justify-center shrink-0 mt-0.5 tabular-nums">
                      {i + 1}
                    </span>
                    <span className="text-pretty font-medium">{pt}</span>
                  </div>
                ))}
              </div>

              {/* Lời dẫn nguyên văn đầy đủ & Kết quả màn hình */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3 pt-1">
                <div className="md:col-span-2 p-3.5 rounded-xl bg-white border border-slate-200 space-y-1">
                  <div className="text-[11px] font-bold text-slate-500 uppercase">
                    Lời dẫn gợi ý đầy đủ
                  </div>
                  <p
                    className={`text-slate-700 leading-relaxed text-pretty ${
                      largeScript ? 'text-sm' : 'text-xs'
                    }`}
                  >
                    {currentStep.presenterScript}
                  </p>
                </div>
                <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
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

          {/* Bảng Dữ liệu Quick-Fill & Copy dự phòng: Thu gọn sẵn ở Chế độ Sân khấu để màn hình luôn thoáng */}
          {viewMode === 'stage' ? (
            <AstryxCard padding={4} className="rounded-2xl bg-white border border-slate-200 shadow-xs">
              <AstryxCollapsible
                defaultIsOpen={false}
                trigger={
                  <div className="flex flex-wrap items-center justify-between gap-2 pr-2">
                    <span className="text-xs sm:text-sm font-bold text-slate-800">
                      Dữ liệu điền tự động &amp; Sao chép thủ công dự phòng ({currentStep.fields.length} mục)
                    </span>
                    <AstryxBadge label="Bấm để mở khi cần sửa tay" variant="neutral" />
                  </div>
                }
              >
                <div className="pt-3">{renderFieldsTable()}</div>
              </AstryxCollapsible>
            </AstryxCard>
          ) : (
            <AstryxCard padding={5} className="rounded-2xl bg-white border border-slate-200 shadow-xs space-y-4">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <AstryxHeading level={3} className="text-sm font-bold text-slate-900">
                  Bảng Dữ liệu Chuẩn &amp; Nội dung Điền Nhanh tại Bước {currentStep.code}
                </AstryxHeading>
                <AstryxBadge
                  label="Văn phong tự nhiên (Humanized Vietnamese)"
                  variant="orange"
                />
              </div>
              {renderFieldsTable()}
            </AstryxCard>
          )}

          {/* Ngăn Truy cập nhanh Q&A Hội đồng: Phủ kín 14 màn hình tính năng chuyên sâu đã nạp sẵn dữ liệu ĐH FPT 2027 */}
          <AstryxCard padding={4} className="rounded-2xl bg-white border border-orange-200 shadow-xs">
            <AstryxCollapsible
              defaultIsOpen={false}
              trigger={
                <div className="flex flex-wrap items-center justify-between gap-2 pr-2">
                  <span className="text-xs sm:text-sm font-bold text-slate-900 flex items-center gap-2">
                    <Sparkles className="size-4 text-orange-600 shrink-0" />
                    <span>Truy cập nhanh Q&amp;A Hội đồng: 14 Màn hình Chuyên sâu (Event, Workshop, PR, KOL, AI Studio, Client Vault)</span>
                  </span>
                  <AstryxBadge label="1 chạm mở đúng vai trò" variant="orange" />
                </div>
              }
            >
              <div className="pt-3 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
                {QA_QUICK_LINKS.map((item) => (
                  <button
                    key={item.id}
                    type="button"
                    disabled={busyAction !== null}
                    onClick={() => triggerStepAction(item.id)}
                    className="p-2.5 rounded-xl border border-slate-200 bg-white hover:border-orange-400 hover:bg-orange-50/40 text-left flex items-start justify-between gap-2 cursor-pointer disabled:opacity-50"
                  >
                    <div className="min-w-0">
                      <div className="text-xs font-bold text-slate-900 truncate">{item.label}</div>
                      <div className="text-[11px] text-slate-600 truncate mt-0.5">{item.desc}</div>
                    </div>
                    <span className="px-1.5 py-0.5 rounded bg-orange-50 text-orange-700 border border-orange-200 text-[10px] font-bold shrink-0">
                      {item.role}
                    </span>
                  </button>
                ))}
              </div>
            </AstryxCollapsible>
          </AstryxCard>

          {/* Chân trang lệnh chạy nhanh */}
          <div className="px-4 py-3 rounded-xl bg-orange-50/40 border border-orange-200 flex flex-wrap items-center justify-between gap-3 text-xs text-slate-700">
            <div className="flex items-center gap-2">
              <Terminal className="size-4 text-orange-600 shrink-0" />
              <span>
                Khởi động Selenium Bridge:{' '}
                <AstryxCode>python brandhub-docs-portal/scripts/demo/selenium_demo_monitor.py</AstryxCode>
              </span>
            </div>
            <a
              href="http://localhost:3999"
              target="_blank"
              rel="noreferrer"
              className="font-semibold text-orange-700 hover:underline inline-flex items-center gap-1"
            >
              <span>Mở bản HTML độc lập (:3999)</span>
              <ExternalLink className="size-3.5" />
            </a>
          </div>
        </section>
      </main>
    </div>
  );
};

export default DemoMonitorPage;
