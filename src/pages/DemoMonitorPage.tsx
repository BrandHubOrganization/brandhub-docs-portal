import React, { useEffect, useState } from 'react';
import {
  Play,
  Globe,
  Monitor,
  Sliders,
  Sparkles,
  ChevronRight,
  ChevronLeft,
  RotateCcw,
  ExternalLink,
  Copy,
  Check,
  Info,
  Layers,
  Database,
  Terminal,
  X,
  Building2,
  UserCheck,
  Cpu,
  MousePointerClick,
  Keyboard,
} from 'lucide-react';

interface MonitorState {
  base_url: string;
  agency_id: string;
  workspace_id: string;
  active_task_id: string;
  chunk_speed: 'fast' | 'normal' | 'slow';
  status_message: string;
  last_step: string | null;
}

interface RoleConfig {
  key: 'owner' | 'manager' | 'creator' | 'client' | 'admin';
  canonicalRole: 'Owner' | 'Manager' | 'Creator' | 'Client' | 'Admin';
  windowLabel: string;
  fullName: string;
  organization: string;
  email: string;
  password: string;
  defaultRoute: string;
  responsibility: string;
}

interface SequentialMicroStep {
  order: string;
  fieldLabel: string;
  behaviorBadge: string;
  sampleValue: string;
  domTarget: string;
  isManualStop?: boolean;
}

interface FieldSpec {
  fieldName: string;
  meaningForJury: string;
  selector: string;
  sampleValue: string;
  inputMode: string;
}

interface StepAction {
  actionId: string;
  label: string;
  variant: 'primary' | 'typing' | 'secondary' | 'warning';
  defaultTextKey?: string;
}

interface DemoStep {
  id: string;
  number: number;
  stageId: number;
  stageTitle: string;
  title: string;
  subtitle: string;
  roleKey: RoleConfig['key'];
  canonicalRole: RoleConfig['canonicalRole'];
  windowNumber: number;
  fptBusinessContext: string;
  routeTemplate: string;
  apiEndpoint: string;
  algorithmTier: string;
  stateBefore: string;
  stateAfter: string;
  manualSubmitButton: string;
  presenterNotes: string;
  sequentialPipeline: SequentialMicroStep[];
  fields: FieldSpec[];
  actions: StepAction[];
}

const ROLES: RoleConfig[] = [
  {
    key: 'owner',
    canonicalRole: 'Owner',
    windowLabel: 'Cửa sổ 1',
    fullName: 'Lê Trí Trung',
    organization: 'FPT Smart Ads Agency',
    email: 'user177@demo.brandhub.test',
    password: 'Password123',
    defaultRoute: '/agency/{agency_id}/media-packages',
    responsibility: 'Quản lý gói dịch vụ mẫu của FPT Smart Ads và nâng cấp thuê bao Plus qua VietQR SePay',
  },
  {
    key: 'manager',
    canonicalRole: 'Manager',
    windowLabel: 'Cửa sổ 2',
    fullName: 'Nguyễn Thành Lộc',
    organization: 'Workspace: FPT University x FPT Smart Ads',
    email: 'user1@demo.brandhub.test',
    password: 'Password123',
    defaultRoute: '/workspaces/{workspace_id}/campaigns',
    responsibility: 'Triển khai chiến dịch tuyển sinh Đại học FPT, giao việc cho Creator, duyệt bài tầng 1 và đăng bài',
  },
  {
    key: 'creator',
    canonicalRole: 'Creator',
    windowLabel: 'Cửa sổ 3',
    fullName: 'Nguyễn Chơn Phước',
    organization: 'FPT Smart Ads Agency',
    email: 'user13@demo.brandhub.test',
    password: 'Password123',
    defaultRoute: '/workspaces/{workspace_id}/tasks',
    responsibility: 'Soạn bài viết bằng AI, kiểm tra an toàn nội dung và bổ sung thông tin học bổng ở bản v2',
  },
  {
    key: 'client',
    canonicalRole: 'Client',
    windowLabel: 'Cửa sổ 4',
    fullName: 'Nguyễn Minh Tuấn',
    organization: 'Đại học FPT (Tập đoàn FPT)',
    email: 'user59@demo.brandhub.test',
    password: 'Password123',
    defaultRoute: '/workspaces/{workspace_id}/media-package',
    responsibility: 'Chốt gói dịch vụ, góp ý bổ sung học bổng Nguyễn Văn Đạo và duyệt chốt bài viết tầng 2',
  },
  {
    key: 'admin',
    canonicalRole: 'Admin',
    windowLabel: 'Cửa sổ 5',
    fullName: 'Hà Văn Ân',
    organization: 'Hệ thống BrandHub',
    email: 'admin@demo.brandhub.test',
    password: 'Password123',
    defaultRoute: '/admin?view=revenue',
    responsibility: 'Theo dõi doanh thu thuê bao toàn hệ thống (MRR/ARR) và kiểm duyệt nội dung vi phạm',
  },
];

const STAGES = [
  { id: 1, title: 'Chặng 1: Gói dịch vụ & Chiến dịch', range: 'B1 - B4' },
  { id: 2, title: 'Chặng 2: Soạn thảo AI & Kiểm duyệt', range: 'B5 - B7' },
  { id: 3, title: 'Chặng 3: Duyệt 2 cấp & Bản v2', range: 'B8 - B11' },
  { id: 4, title: 'Chặng 4: Xuất bản mạng xã hội', range: 'B12 - B13' },
  { id: 5, title: 'Chặng 5: Thanh toán VietQR & Admin', range: 'B14 - B15' },
];

const DEMO_STEPS: DemoStep[] = [
  {
    id: 'B1',
    number: 1,
    stageId: 1,
    stageTitle: 'Chặng 1: Gói dịch vụ & Chiến dịch',
    title: 'Xem gói truyền thông mẫu của FPT Smart Ads',
    subtitle: 'Lê Trí Trung (Owner) mở danh sách gói dịch vụ mẫu dành cho khối giáo dục và công nghệ tại Việt Nam',
    roleKey: 'owner',
    canonicalRole: 'Owner',
    windowNumber: 1,
    fptBusinessContext:
      'FPT Smart Ads thiết kế gói truyền thông phục vụ tuyển sinh ngành Thiết kế Vi mạch và AI tại Đại học FPT, hưởng ứng mục tiêu đào tạo 50.000 kỹ sư bán dẫn của Việt Nam đến năm 2030.',
    routeTemplate: '/agency/{agency_id}/media-packages',
    apiEndpoint: 'GET /api/v1/agencies/:agencyId/media-packages',
    algorithmTier: 'Đưa Cửa sổ 1 (Owner) lên trên cùng và mở trang Gói dịch vụ mẫu',
    stateBefore: 'ACTIVE (Gói dịch vụ mẫu)',
    stateAfter: 'Sẵn sàng áp dụng vào Workspace của Đại học FPT',
    manualSubmitButton: 'Click vào thẻ gói dịch vụ để chỉ cho Hội đồng xem số lượng hạng mục bàn giao',
    presenterNotes:
      'Giới thiệu ngắn gọn với Hội đồng: Gói dịch vụ quy định rõ 4 hạng mục công việc (2 bài đăng mạng xã hội, 1 thông cáo báo chí sự kiện AI4VN và 1 khảo sát học sinh THPT) với ngân sách 18.000.000đ trong 6 tuần.',
    sequentialPipeline: [
      {
        order: 'Bước 1',
        fieldLabel: 'Chuyển sang Cửa sổ 1 của Lê Trí Trung (Owner)',
        behaviorBadge: 'Đưa cửa sổ lên trước',
        sampleValue: 'Cửa sổ 1: Lê Trí Trung (Giám đốc FPT Smart Ads Agency)',
        domTarget: 'window.focus()',
      },
      {
        order: 'Bước 2',
        fieldLabel: 'Mở danh sách gói dịch vụ mẫu của Agency',
        behaviorBadge: 'Chuyển trang tự động',
        sampleValue: 'Gói Truyền thông Tuyển sinh Vi mạch & AI Đại học FPT 2026 (18.000.000đ)',
        domTarget: '/agency/{agency_id}/media-packages',
      },
      {
        order: 'Tự thao tác',
        fieldLabel: 'Người thuyết trình chỉ vào 3 nhóm hạng mục bàn giao trên màn hình',
        behaviorBadge: 'Thao tác trên sân khấu',
        sampleValue: '2 Bài đăng mạng xã hội, 1 Đề xuất báo chí AI4VN, 1 Khảo sát học sinh THPT',
        domTarget: 'MediaPackageCard',
        isManualStop: true,
      },
    ],
    fields: [
      {
        fieldName: 'Tên gói dịch vụ',
        meaningForJury: 'Gói truyền thông phục vụ sự kiện tuyển sinh và đào tạo nhân lực số tại Việt Nam',
        selector: 'MediaPackageCard > h3',
        sampleValue: 'Gói Truyền thông Tuyển sinh Vi mạch & AI Đại học FPT 2026',
        inputMode: 'Dữ liệu chuẩn bị sẵn',
      },
      {
        fieldName: 'Ngân sách và thời hạn',
        meaningForJury: 'Chi phí trọn gói và thời gian thực hiện chiến dịch',
        selector: 'MediaPackageCard > .price-badge',
        sampleValue: '18.000.000 VNĐ (Thời hạn 6 tuần)',
        inputMode: 'Dữ liệu chuẩn bị sẵn',
      },
      {
        fieldName: 'Các hạng mục bàn giao (Deliverables)',
        meaningForJury: 'Cơ sở để hệ thống tự động sinh ra các đầu việc cụ thể ở Bước B3',
        selector: 'MediaPackageCard > ul',
        sampleValue: '2 bài đăng mạng xã hội, 1 thông cáo báo chí và 1 khảo sát định hướng nghề nghiệp',
        inputMode: 'Dữ liệu chuẩn bị sẵn',
      },
    ],
    actions: [
      { actionId: 'B1_NAV', label: '1. Mở trang Gói dịch vụ mẫu (Lê Trí Trung - Owner)', variant: 'primary' },
    ],
  },
  {
    id: 'B2',
    number: 2,
    stageId: 1,
    stageTitle: 'Chặng 1: Gói dịch vụ & Chiến dịch',
    title: 'Đại học FPT xác nhận chốt gói truyền thông',
    subtitle: 'Nguyễn Minh Tuấn (Client - Đại học FPT) xem lại các điều khoản gói dịch vụ đã thống nhất giữa hai bên',
    roleKey: 'client',
    canonicalRole: 'Client',
    windowNumber: 4,
    fptBusinessContext:
      'Đại diện Đại học FPT (Nguyễn Minh Tuấn) và FPT Smart Ads đã thống nhất ngân sách 18.000.000đ cùng lịch sử 3 vòng trao đổi điều khoản.',
    routeTemplate: '/workspaces/{workspace_id}/media-package',
    apiEndpoint: 'GET /api/v1/workspaces/:workspaceId/media-package',
    algorithmTier: 'Đưa Cửa sổ 4 (Client) lên trên cùng và mở trang Gói dịch vụ của Workspace',
    stateBefore: 'NEGOTIATING (Đang đàm phán)',
    stateAfter: 'APPROVED / AGREED (Hai bên đã đồng thuận)',
    manualSubmitButton: 'Chỉ vào trạng thái Đã đồng thuận và bảng lịch sử 3 lần thương lượng giá',
    presenterNotes:
      'Giải thích ngắn gọn: Cả FPT Smart Ads và Đại học FPT đều phải xác nhận đồng ý thì gói dịch vụ mới khóa điều khoản và cho phép triển khai chiến dịch.',
    sequentialPipeline: [
      {
        order: 'Bước 1',
        fieldLabel: 'Chuyển sang Cửa sổ 4 của Nguyễn Minh Tuấn (Client)',
        behaviorBadge: 'Đưa cửa sổ lên trước',
        sampleValue: 'Cửa sổ 4: Nguyễn Minh Tuấn (Đại diện Đại học FPT)',
        domTarget: 'window.focus()',
      },
      {
        order: 'Bước 2',
        fieldLabel: 'Hiển thị thông tin gói dịch vụ đã chốt trong Workspace',
        behaviorBadge: 'Chuyển trang tự động',
        sampleValue: 'Trạng thái: Đã đồng thuận (Ngân sách chốt: 18.000.000 VNĐ)',
        domTarget: '/workspaces/{workspace_id}/media-package',
      },
    ],
    fields: [
      {
        fieldName: 'Đơn vị khách hàng',
        meaningForJury: 'Thương hiệu sử dụng dịch vụ truyền thông trong Workspace',
        selector: '[data-testid="workspace-package-header"]',
        sampleValue: 'Đại học FPT (Tập đoàn FPT)',
        inputMode: 'Hiển thị trực quan',
      },
      {
        fieldName: 'Lịch sử đàm phán 3 vòng',
        meaningForJury: 'Lưu vết quá trình đề xuất ngân sách từ 20 triệu xuống 17,5 triệu và chốt ở 18 triệu đồng',
        selector: 'NegotiationHistoryList',
        sampleValue: 'Vòng 1: 20M (Đề xuất gốc) -> Vòng 2: 17,5M (Client đề xuất) -> Vòng 3: 18M (Chốt hợp đồng)',
        inputMode: 'Hiển thị trực quan',
      },
    ],
    actions: [
      { actionId: 'B2_NAV', label: '1. Mở trang Gói dịch vụ phía Đại học FPT (Nguyễn Minh Tuấn - Client)', variant: 'primary' },
    ],
  },
  {
    id: 'B3',
    number: 3,
    stageId: 1,
    stageTitle: 'Chặng 1: Gói dịch vụ & Chiến dịch',
    title: 'Triển khai chiến dịch để tự động sinh 4 công việc',
    subtitle: 'Nguyễn Thành Lộc (Manager) mở chiến dịch truyền thông và bấm nút Triển khai',
    roleKey: 'manager',
    canonicalRole: 'Manager',
    windowNumber: 2,
    fptBusinessContext:
      'Chiến dịch tập trung vào hai sự kiện thực tế tại Việt Nam: đợt xét tuyển học bổng ngành Vi mạch bán dẫn năm 2026 và Ngày hội Trí tuệ Nhân tạo Việt Nam (AI4VN) tại Khu Công nghệ cao Hòa Lạc.',
    routeTemplate: '/workspaces/{workspace_id}/campaigns',
    apiEndpoint: 'POST /api/v1/workspaces/:workspaceId/campaigns/:campaignId/deploy',
    algorithmTier: 'Mở trang Chiến dịch + Khoanh sáng viền xanh lá quanh nút "Triển khai"',
    stateBefore: 'APPROVED (Kế hoạch chiến dịch đã duyệt)',
    stateAfter: 'DEPLOYED / IN_PROGRESS (Tự động tạo 4 Task trong bảng công việc)',
    manualSubmitButton: 'Tự tay bấm nút "Triển khai" đang được khoanh sáng màu xanh lá trên màn hình',
    presenterNotes:
      'Khi bấm nút "Triển khai", hệ thống tự động đối chiếu 4 hạng mục trong kế hoạch chiến dịch để tạo ra 4 công việc (Tasks) tương ứng bên bảng quản lý công việc.',
    sequentialPipeline: [
      {
        order: 'Bước 1',
        fieldLabel: 'Chuyển sang Cửa sổ 2 của Nguyễn Thành Lộc (Manager)',
        behaviorBadge: 'Đưa cửa sổ lên trước',
        sampleValue: 'Cửa sổ 2: Nguyễn Thành Lộc (Quản lý Chiến dịch)',
        domTarget: 'window.focus()',
      },
      {
        order: 'Bước 2',
        fieldLabel: 'Mở trang Chiến dịch của Workspace Đại học FPT',
        behaviorBadge: 'Chuyển trang tự động',
        sampleValue: 'Chiến dịch Tuyển sinh Ngành Vi mạch Bán dẫn & Sự kiện AI4VN 2026',
        domTarget: '/workspaces/{workspace_id}/campaigns',
      },
      {
        order: 'Tự bấm chốt',
        fieldLabel: 'Khoanh sáng nút "Triển khai" và dừng lại chờ bạn bấm',
        behaviorBadge: 'Viền xanh lá #059669',
        sampleValue: 'Bạn tự bấm nút "Triển khai" để hệ thống sinh 4 công việc tự động',
        domTarget: "//button[contains(., 'Triển khai') or contains(., 'Deploy')]",
        isManualStop: true,
      },
    ],
    fields: [
      {
        fieldName: 'Tên chiến dịch',
        meaningForJury: 'Gắn liền với mục tiêu phát triển nhân lực bán dẫn và sự kiện AI4VN tại Việt Nam',
        selector: 'CampaignCard > h3',
        sampleValue: 'Chiến dịch Tuyển sinh Ngành Vi mạch Bán dẫn & Sự kiện AI4VN 2026',
        inputMode: 'Hiển thị trực quan',
      },
      {
        fieldName: 'Nút Triển khai (Deploy)',
        meaningForJury: 'Chuyển hóa kế hoạch chiến dịch thành các đầu việc cụ thể cho đội ngũ thực hiện',
        selector: "//button[contains(., 'Triển khai') or contains(., 'Deploy')]",
        sampleValue: 'Được khoanh sáng viền xanh lá, chờ người thuyết trình bấm',
        inputMode: 'Tự bấm thủ công',
      },
    ],
    actions: [
      { actionId: 'B3_NAV', label: '1. Mở Chiến dịch & Khoanh sáng nút Triển khai (Nguyễn Thành Lộc)', variant: 'primary' },
    ],
  },
  {
    id: 'B4',
    number: 4,
    stageId: 1,
    stageTitle: 'Chặng 1: Gói dịch vụ & Chiến dịch',
    title: 'Giao Bài #1 cho Nguyễn Chơn Phước (Creator)',
    subtitle: 'Nguyễn Thành Lộc (Manager) kiểm tra 4 công việc vừa sinh tự động và giao Bài #1 cho Creator',
    roleKey: 'manager',
    canonicalRole: 'Manager',
    windowNumber: 2,
    fptBusinessContext:
      'Hệ thống đã tạo 4 công việc thực tế: Bài #1 về học bổng ngành Vi mạch & AI, Bài #2 về sự kiện AI4VN tại Hòa Lạc, Báo chí #1 về chương trình 50.000 kỹ sư bán dẫn Việt Nam, và Khảo sát #1 cho học sinh THPT.',
    routeTemplate: '/workspaces/{workspace_id}/tasks',
    apiEndpoint: 'PATCH /api/v1/workspaces/:workspaceId/tasks/:taskId/assign',
    algorithmTier: 'Điều hướng trực tiếp tới Bảng quản lý công việc',
    stateBefore: 'TODO (Vừa khởi tạo từ chiến dịch)',
    stateAfter: 'TODO (Đã giao cho Nguyễn Chơn Phước)',
    manualSubmitButton: 'Click vào "[Bài #1]" và chọn người thực hiện là Nguyễn Chơn Phước',
    presenterNotes:
      'Chỉ cho Hội đồng thấy 4 đầu việc tương ứng đúng với 3 nhóm hạng mục trong gói dịch vụ, sau đó giao Bài #1 cho Nguyễn Chơn Phước.',
    sequentialPipeline: [
      {
        order: 'Bước 1',
        fieldLabel: 'Mở Bảng công việc trên Cửa sổ 2 (Nguyễn Thành Lộc)',
        behaviorBadge: 'Chuyển trang tự động',
        sampleValue: '/workspaces/{workspace_id}/tasks',
        domTarget: 'TaskListPage',
      },
      {
        order: 'Tự bấm chốt',
        fieldLabel: 'Chọn "[Bài #1] Mở đăng ký học bổng ngành Thiết kế Vi mạch & AI tại Đại học FPT"',
        behaviorBadge: 'Thao tác trên sân khấu',
        sampleValue: 'Giao cho: Nguyễn Chơn Phước (Creator)',
        domTarget: 'Task Row #c6453698-cf56-38c1-96d2-90ccdd985228',
        isManualStop: true,
      },
    ],
    fields: [
      {
        fieldName: 'Tên công việc Bài #1',
        meaningForJury: 'Đầu việc bài đăng mạng xã hội đầu tiên của chiến dịch',
        selector: 'TaskRow[data-task-id="c6453698-cf56-38c1-96d2-90ccdd985228"]',
        sampleValue: '[Bài #1] Mở đăng ký học bổng ngành Thiết kế Vi mạch & AI tại Đại học FPT',
        inputMode: 'Hiển thị trực quan',
      },
      {
        fieldName: 'Người phụ trách (Assignee)',
        meaningForJury: 'Thành viên nhóm đồ án đảm nhận vai trò Creator',
        selector: 'AssigneeSelect',
        sampleValue: 'Nguyễn Chơn Phước (user13@demo.brandhub.test)',
        inputMode: 'Chọn trên giao diện',
      },
    ],
    actions: [
      { actionId: 'B4_NAV', label: '1. Mở Bảng công việc để giao Bài #1 (Nguyễn Thành Lộc)', variant: 'primary' },
    ],
  },
  {
    id: 'B5',
    number: 5,
    stageId: 2,
    stageTitle: 'Chặng 2: Soạn thảo AI & Kiểm duyệt',
    title: 'Nguyễn Chơn Phước (Creator) nhận việc và bắt đầu làm',
    subtitle: 'Chuyển sang Cửa sổ 3 (Creator) để nhận Bài #1 và đổi trạng thái sang Đang thực hiện (IN_PROGRESS)',
    roleKey: 'creator',
    canonicalRole: 'Creator',
    windowNumber: 3,
    fptBusinessContext:
      'Nguyễn Chơn Phước mở danh sách công việc được giao trong Workspace Đại học FPT và bắt đầu thực hiện Bài #1.',
    routeTemplate: '/workspaces/{workspace_id}/tasks',
    apiEndpoint: 'PATCH /api/v1/workspaces/:workspaceId/tasks/:taskId/status',
    algorithmTier: 'Đưa Cửa sổ 3 (Creator) lên trên cùng và mở danh sách công việc',
    stateBefore: 'TODO (Mới được giao)',
    stateAfter: 'IN_PROGRESS (Đang soạn thảo)',
    manualSubmitButton: 'Đổi trạng thái Bài #1 sang "Đang làm" (IN_PROGRESS) hoặc mở trình soạn thảo',
    presenterNotes:
      'Cho Hội đồng thấy giao diện của Creator chỉ tập trung vào công việc chuyên môn được giao, phân quyền rõ ràng với Manager và Client.',
    sequentialPipeline: [
      {
        order: 'Bước 1',
        fieldLabel: 'Đưa Cửa sổ 3 của Nguyễn Chơn Phước (Creator) lên trên cùng',
        behaviorBadge: 'Đưa cửa sổ lên trước',
        sampleValue: 'Cửa sổ 3: Nguyễn Chơn Phước (Chuyên viên Nội dung)',
        domTarget: 'window.focus()',
      },
      {
        order: 'Tự bấm chốt',
        fieldLabel: 'Chuyển trạng thái Bài #1 sang IN_PROGRESS',
        behaviorBadge: 'Thao tác trên sân khấu',
        sampleValue: 'Trạng thái: TODO -> IN_PROGRESS',
        domTarget: 'Task Status Select',
        isManualStop: true,
      },
    ],
    fields: [
      {
        fieldName: 'Trạng thái công việc',
        meaningForJury: 'Giúp Quản lý chiến dịch và Đại học FPT biết bài viết đang được thực hiện',
        selector: 'TaskStatusSelect',
        sampleValue: 'IN_PROGRESS (Đang thực hiện)',
        inputMode: 'Người thuyết trình chọn',
      },
    ],
    actions: [
      { actionId: 'B5_NAV', label: '1. Mở Danh sách việc của Nguyễn Chơn Phước (Creator)', variant: 'primary' },
    ],
  },
  {
    id: 'B6',
    number: 6,
    stageId: 2,
    stageTitle: 'Chặng 2: Soạn thảo AI & Kiểm duyệt',
    title: 'Dùng AI tạo nội dung bài đăng theo mục tiêu 50.000 kỹ sư bán dẫn Việt Nam',
    subtitle: 'Điền tuần tự 4 bước: Mở hộp thoại AI -> Gõ từng cụm chủ đề -> Chọn Mục tiêu -> Chọn Độ dài',
    roleKey: 'creator',
    canonicalRole: 'Creator',
    windowNumber: 3,
    fptBusinessContext:
      'Nguyễn Chơn Phước dùng công cụ AI để viết bài giới thiệu ngành Thiết kế Vi mạch và AI tại Đại học FPT, bám sát chương trình phát triển 50.000 kỹ sư bán dẫn của Việt Nam đến năm 2030.',
    routeTemplate: '/workspaces/{workspace_id}/content-writing?taskId={task_id}',
    apiEndpoint: 'POST /api/v1/workspaces/:workspaceId/ai/captions/generate',
    algorithmTier: 'Tầng 3 (React 19 Textarea) + Điền tuần tự từng trường có nghỉ nhịp 0.55s',
    stateBefore: 'Khung soạn thảo đang trống',
    stateAfter: 'AI trả về 3 phương án bài viết và trừ tín chỉ AI của Workspace',
    manualSubmitButton: 'Tự bấm nút "Tạo caption" (được khoanh sáng xanh lá) -> Chọn 1 phương án để đưa vào bài viết',
    presenterNotes:
      'Khi bấm nút số 2 bên dưới, hệ thống sẽ tự mở hộp thoại AI, gõ từng cụm từ tiếng Việt vào ô Chủ đề, nghỉ nửa giây rồi chọn nút Mục tiêu (Tương tác), chọn Độ dài (Vừa) và dừng lại trước nút "Tạo caption" để bạn bấm.',
    sequentialPipeline: [
      {
        order: 'Bước 1/4',
        fieldLabel: 'Mở hộp thoại Tạo Caption bằng AI',
        behaviorBadge: 'Click tự động + Nghỉ 0.65s',
        sampleValue: 'Mở hộp thoại AI Caption Dialog',
        domTarget: "//button[contains(., 'AI') or contains(., 'caption')]",
      },
      {
        order: 'Bước 2/4',
        fieldLabel: 'Gõ từng cụm từ vào ô Chủ đề bài viết',
        behaviorBadge: 'Nhả chữ 42-88ms/cụm',
        sampleValue:
          'Giới thiệu chương trình đào tạo ngành Thiết kế Vi mạch và Trí tuệ nhân tạo tại Đại học FPT, hưởng ứng mục tiêu 50.000 kỹ sư bán dẫn của Việt Nam đến năm 2030',
        domTarget: "[role='dialog'] textarea",
      },
      {
        order: 'Bước 3/4',
        fieldLabel: 'Chọn Mục tiêu bài đăng sau khi nghỉ 0.55s',
        behaviorBadge: 'Khoanh xanh + Click chọn',
        sampleValue: 'Tương tác (Engagement)',
        domTarget: "[role='dialog'] [role='group']:first-of-type button",
      },
      {
        order: 'Bước 4/4',
        fieldLabel: 'Chọn Độ dài bài viết sau khi nghỉ 0.45s',
        behaviorBadge: 'Khoanh xanh + Click chọn',
        sampleValue: 'Vừa (Medium)',
        domTarget: "[role='dialog'] [role='group']:last-of-type button",
      },
      {
        order: 'Tự bấm chốt',
        fieldLabel: 'Khoanh sáng nút "Tạo caption" và dừng chờ bạn bấm',
        behaviorBadge: 'Viền xanh lá #059669',
        sampleValue: 'Bạn tự bấm "Tạo caption", sau đó chọn 1 phương án để chèn vào khung soạn thảo',
        domTarget: "[role='dialog'] button[type='submit']",
        isManualStop: true,
      },
    ],
    fields: [
      {
        fieldName: 'Chủ đề yêu cầu AI viết (Topic)',
        meaningForJury: 'Nội dung ngắn gọn, gắn trực tiếp với mục tiêu đào tạo 50.000 kỹ sư bán dẫn tại Việt Nam',
        selector: "[role='dialog'] textarea",
        sampleValue:
          'Giới thiệu chương trình đào tạo ngành Thiết kế Vi mạch và Trí tuệ nhân tạo tại Đại học FPT, hưởng ứng mục tiêu 50.000 kỹ sư bán dẫn của Việt Nam đến năm 2030',
        inputMode: 'Gõ nhả chữ từng cụm (Có thể sửa bên dưới)',
      },
      {
        fieldName: 'Mục tiêu và Độ dài',
        meaningForJury: 'Giúp AI điều chỉnh độ dài câu chữ phù hợp với bài đăng Facebook của trường',
        selector: "[role='dialog'] [role='group'] button",
        sampleValue: 'Mục tiêu: Tương tác | Độ dài: Vừa | Kênh: Facebook',
        inputMode: 'Click tuần tự tự động',
      },
    ],
    actions: [
      { actionId: 'B6_NAV_EDITOR', label: '1. Mở trang Soạn thảo Yjs Canvas (Nguyễn Chơn Phước)', variant: 'secondary' },
      {
        actionId: 'B6_SEQ_FILL_AI',
        label: '2. Điền tuần tự Chủ đề & Tham số AI (Nhả chữ từng phần)',
        variant: 'typing',
        defaultTextKey: 'B6_AI_TOPIC',
      },
    ],
  },
  {
    id: 'B7',
    number: 7,
    stageId: 2,
    stageTitle: 'Chặng 2: Soạn thảo AI & Kiểm duyệt',
    title: 'Kiểm tra an toàn nội dung (Chặn câu vi phạm BLOCKED -> Sửa lại PASSED)',
    subtitle: 'Thử nghiệm chèn câu vi phạm để hệ thống chặn lại, sau đó khôi phục bản thảo v1 hợp lệ và gửi duyệt',
    roleKey: 'creator',
    canonicalRole: 'Creator',
    windowNumber: 3,
    fptBusinessContext:
      'Trước khi bài viết được gửi cho Quản lý duyệt, hệ thống tự động quét từ ngữ để ngăn chặn các nội dung vi phạm quy định an toàn thông tin tại Việt Nam.',
    routeTemplate: '/workspaces/{workspace_id}/content-writing?taskId={task_id}',
    apiEndpoint: 'POST /api/v1/workspaces/:workspaceId/moderation/check-caption',
    algorithmTier: 'Tầng 1 (Yjs Canvas InputEvent) đảm bảo không mất dấu cách tiếng Việt trên thẻ <canvas>',
    stateBefore: 'NOT_CHECKED -> BLOCKED (Khi có câu vi phạm)',
    stateAfter: 'PASSED (An toàn) -> Nộp duyệt bản v1 (IN_REVIEW)',
    manualSubmitButton: 'Bấm "Kiểm tra tuân thủ" (báo ĐỎ BLOCKED) -> Chạy nút 2 -> Bấm "Kiểm tra lại" (XANH PASSED) và "Nộp duyệt"',
    presenterNotes:
      'Bước này chứng minh tính năng bảo vệ thương hiệu: (1) Bấm nút 1 để gõ câu vi phạm rồi tự bấm "Kiểm tra tuân thủ" cho Hội đồng thấy cảnh báo đỏ BLOCKED. (2) Bấm nút 2 để hệ thống xóa câu lỗi và gõ lại bản v1 chuẩn của Đại học FPT, sau đó bấm "Kiểm tra lại" để lên trạng thái PASSED.',
    sequentialPipeline: [
      {
        order: 'Thử nghiệm 7.1',
        fieldLabel: 'Đưa con trỏ xuống cuối bài và gõ câu thử nghiệm vi phạm',
        behaviorBadge: 'Tầng 1: Yjs Canvas InputEvent',
        sampleValue: 'Bài viết chứa nội dung kích động bạo lực và ngôn từ thù ghét vi phạm quy định an toàn thông tin.',
        domTarget: "[aria-label='Content editor input']",
      },
      {
        order: 'Kiểm chứng chặn',
        fieldLabel: 'Khoanh sáng đỏ nút "Kiểm tra tuân thủ" chờ bạn bấm',
        behaviorBadge: 'Viền đỏ #DC2626',
        sampleValue: 'Hệ thống báo BLOCKED và khóa chức năng gửi duyệt bài viết',
        domTarget: "[data-testid='caption-moderation'] button",
        isManualStop: true,
      },
      {
        order: 'Khôi phục 7.2',
        fieldLabel: 'Xóa sạch câu vi phạm và gõ bản thảo v1 ngắn gọn, chuẩn mực',
        behaviorBadge: 'Ctrl+A + Backspace + Nhả chữ',
        sampleValue:
          'Đại học FPT mở cổng đăng ký ngành Thiết kế Vi mạch và Trí tuệ nhân tạo kỳ thu 2026. Chương trình đào tạo gắn với mục tiêu phát triển 50.000 kỹ sư bán dẫn tại Việt Nam đến năm 2030.',
        domTarget: "[aria-label='Content editor input']",
      },
      {
        order: 'Tự bấm chốt',
        fieldLabel: 'Khoanh sáng xanh nút "Kiểm tra lại" để bạn bấm và nộp duyệt',
        behaviorBadge: 'Viền xanh lá #059669',
        sampleValue: 'Hệ thống báo PASSED -> Bấm Lưu / Nộp duyệt bản v1',
        domTarget: "[data-testid='caption-moderation'] button",
        isManualStop: true,
      },
    ],
    fields: [
      {
        fieldName: 'Câu thử nghiệm vi phạm (B7.1)',
        meaningForJury: 'Dùng để kiểm chứng bộ lọc an toàn nội dung chặn các từ ngữ bạo lực, thù ghét',
        selector: "[aria-label='Content editor input']",
        sampleValue: 'Bài viết chứa nội dung kích động bạo lực và ngôn từ thù ghét vi phạm quy định an toàn thông tin.',
        inputMode: 'Gõ nối tiếp vào cuối bài',
      },
      {
        fieldName: 'Nội dung bản thảo v1 của Đại học FPT (B7.2)',
        meaningForJury: 'Văn bản ngắn gọn, rõ ý chính về ngành Vi mạch và mục tiêu 50.000 kỹ sư bán dẫn Việt Nam',
        selector: "[aria-label='Content editor input']",
        sampleValue:
          'Đại học FPT mở cổng đăng ký ngành Thiết kế Vi mạch và Trí tuệ nhân tạo kỳ thu 2026.\nChương trình đào tạo gắn với mục tiêu phát triển 50.000 kỹ sư bán dẫn tại Việt Nam đến năm 2030.\n#DaiHocFPT #ViMachBanDan #ChuyenDoiSoVietNam',
        inputMode: 'Xóa câu lỗi & Gõ lại bản v1',
      },
    ],
    actions: [
      {
        actionId: 'B7_FILL_VIOLATION',
        label: '1. (B7.1) Gõ câu thử vi phạm để test chặn BLOCKED',
        variant: 'warning',
        defaultTextKey: 'B7_VIOLATION',
      },
      {
        actionId: 'B7_CLEAN_AND_RESTORE',
        label: '2. (B7.2) Xóa câu lỗi & Điền bản v1 chuẩn Đại học FPT (PASSED)',
        variant: 'typing',
        defaultTextKey: 'B7_CLEAN_V1',
      },
    ],
  },
  {
    id: 'B8',
    number: 8,
    stageId: 3,
    stageTitle: 'Chặng 3: Duyệt 2 cấp & Bản v2',
    title: 'Nguyễn Thành Lộc (Manager) duyệt nội bộ tầng 1',
    subtitle: 'Quản lý chiến dịch kiểm tra bài viết v1 của Creator và bấm Phê duyệt để chuyển sang phía Đại học FPT',
    roleKey: 'manager',
    canonicalRole: 'Manager',
    windowNumber: 2,
    fptBusinessContext:
      'Nguyễn Thành Lộc rà soát nội dung bài viết ở cấp Agency trước khi gửi sang cho đại diện Đại học FPT nghiệm thu.',
    routeTemplate: '/workspaces/{workspace_id}/task-approvals?task={task_id}',
    apiEndpoint: 'POST /api/v1/workspaces/:workspaceId/tasks/:taskId/review/approve',
    algorithmTier: 'Đưa Cửa sổ 2 (Manager) lên trên cùng + Khoanh sáng xanh lá nút "Phê duyệt"',
    stateBefore: 'IN_REVIEW (Bước chờ: MANAGER_REVIEW)',
    stateAfter: 'IN_REVIEW (Bước chờ: CLIENT_REVIEW)',
    manualSubmitButton: 'Tự tay bấm nút "Phê duyệt" màu xanh lá và xác nhận',
    presenterNotes:
      'Chỉ cho Hội đồng thấy quy trình duyệt 2 cấp: Sau khi Nguyễn Thành Lộc duyệt xong tầng 1, bài viết mới chuyển sang trạng thái chờ khách hàng Đại học FPT duyệt ở tầng 2.',
    sequentialPipeline: [
      {
        order: 'Bước 1',
        fieldLabel: 'Chuyển sang Cửa sổ 2 của Nguyễn Thành Lộc (Manager)',
        behaviorBadge: 'Đưa cửa sổ lên trước',
        sampleValue: '/workspaces/{workspace_id}/task-approvals?task={task_id}',
        domTarget: 'TaskApprovalsPage',
      },
      {
        order: 'Tự bấm chốt',
        fieldLabel: 'Khoanh sáng nút "Phê duyệt" chờ bạn bấm',
        behaviorBadge: 'Viền xanh lá #059669',
        sampleValue: 'Nguyễn Thành Lộc bấm "Phê duyệt" (MANAGER_REVIEW -> CLIENT_REVIEW)',
        domTarget: 'button.bg-emerald-600',
        isManualStop: true,
      },
    ],
    fields: [
      {
        fieldName: 'Bước duyệt hiện tại',
        meaningForJury: 'Kiểm soát chất lượng nội bộ của FPT Smart Ads trước khi gửi khách hàng',
        selector: 'TaskReviewStatus',
        sampleValue: 'MANAGER_REVIEW (Quản lý chiến dịch duyệt tầng 1)',
        inputMode: 'Hiển thị trực quan',
      },
    ],
    actions: [
      { actionId: 'B8_NAV_MANAGER_APPROVAL', label: '1. Mở màn hình Duyệt tầng 1 (Nguyễn Thành Lộc - Manager)', variant: 'primary' },
    ],
  },
  {
    id: 'B9',
    number: 9,
    stageId: 3,
    stageTitle: 'Chặng 3: Duyệt 2 cấp & Bản v2',
    title: 'Đại học FPT góp ý yêu cầu bổ sung học bổng Nguyễn Văn Đạo và kỳ thực tập OJT',
    subtitle: 'Nguyễn Minh Tuấn (Client) mở hộp thoại Từ chối và gõ tuần tự nội dung góp ý cho bản v1',
    roleKey: 'client',
    canonicalRole: 'Client',
    windowNumber: 4,
    fptBusinessContext:
      'Đại diện Đại học FPT (Nguyễn Minh Tuấn) xem bản v1 và đề nghị bổ sung thêm 2 thông tin thực tế mà phụ huynh, học sinh rất quan tâm: mức học bổng Nguyễn Văn Đạo (50% đến 100%) và kỳ thực tập tại FPT Software từ năm thứ 3.',
    routeTemplate: '/workspaces/{workspace_id}/task-approvals?task={task_id}',
    apiEndpoint: 'POST /api/v1/workspaces/:workspaceId/tasks/:taskId/review/reject',
    algorithmTier: 'Tầng 3 (React 19 Textarea #task-review-note) + Tự mở hộp thoại và nhả chữ từng cụm',
    stateBefore: 'IN_REVIEW (Bước chờ: CLIENT_REVIEW)',
    stateAfter: 'REJECTED (Trả bài về cho Creator kèm ghi chú chỉnh sửa)',
    manualSubmitButton: 'Tự tay bấm nút xác nhận "Từ chối" màu đỏ trong hộp thoại sau khi hệ thống gõ xong lý do',
    presenterNotes:
      'Khi bấm nút số 2, hệ thống tự mở hộp thoại Từ chối và gõ câu góp ý ngắn gọn, tự nhiên như trao đổi công việc thực tế giữa khách hàng và Agency, sau đó dừng lại để bạn bấm xác nhận.',
    sequentialPipeline: [
      {
        order: 'Bước 1/2',
        fieldLabel: 'Mở hộp thoại Từ chối bài viết',
        behaviorBadge: 'Click tự động + Nghỉ 0.55s',
        sampleValue: 'Mở ô nhập ghi chú phản hồi (#task-review-note)',
        domTarget: 'button.bg-rose-600',
      },
      {
        order: 'Bước 2/2',
        fieldLabel: 'Gõ từng cụm từ góp ý của Nguyễn Minh Tuấn vào ô ghi chú',
        behaviorBadge: 'Nhả chữ 42-88ms/cụm',
        sampleValue:
          'Bài viết đã rõ ý chính. Nhờ bạn bổ sung thêm thông tin học bổng Nguyễn Văn Đạo từ 50% đến 100% và kỳ thực tập thực tế tại FPT Software từ năm thứ 3.',
        domTarget: '#task-review-note',
      },
      {
        order: 'Tự bấm chốt',
        fieldLabel: 'Khoanh sáng nút xác nhận "Từ chối" và dừng chờ bạn bấm',
        behaviorBadge: 'Viền đỏ #DC2626',
        sampleValue: 'Nguyễn Minh Tuấn bấm xác nhận Từ chối -> Bài viết chuyển sang REJECTED',
        domTarget: "[role='dialog'] button.bg-rose-600",
        isManualStop: true,
      },
    ],
    fields: [
      {
        fieldName: 'Ghi chú phản hồi của khách hàng (#task-review-note)',
        meaningForJury: 'Lưu lại yêu cầu cụ thể của Đại học FPT để Creator chỉnh sửa đúng ý',
        selector: '#task-review-note',
        sampleValue:
          'Bài viết đã rõ ý chính. Nhờ bạn bổ sung thêm thông tin học bổng Nguyễn Văn Đạo từ 50% đến 100% và kỳ thực tập thực tế tại FPT Software từ năm thứ 3.',
        inputMode: 'Gõ nhả chữ từng cụm (Có thể sửa bên dưới)',
      },
    ],
    actions: [
      { actionId: 'B9_NAV_CLIENT_APPROVAL', label: '1. Mở màn hình Duyệt phía Đại học FPT (Nguyễn Minh Tuấn)', variant: 'secondary' },
      {
        actionId: 'B9_SEQ_FILL_REJECT_REASON',
        label: '2. Mở hộp thoại & Gõ tuần tự góp ý bổ sung Học bổng Nguyễn Văn Đạo',
        variant: 'typing',
        defaultTextKey: 'B9_REJECT_REASON',
      },
    ],
  },
  {
    id: 'B10',
    number: 10,
    stageId: 3,
    stageTitle: 'Chặng 3: Duyệt 2 cấp & Bản v2',
    title: 'Creator bổ sung thông tin học bổng (Bản v2) và xem so sánh phiên bản v1 - v2',
    subtitle: 'Nguyễn Chơn Phước (Creator) thêm câu thông tin học bổng Nguyễn Văn Đạo, lưu bản v2 và mở xem lịch sử thay đổi',
    roleKey: 'creator',
    canonicalRole: 'Creator',
    windowNumber: 3,
    fptBusinessContext:
      'Nguyễn Chơn Phước đọc ghi chú của Nguyễn Minh Tuấn, bổ sung câu thông tin học bổng Nguyễn Văn Đạo 50% - 100% và kỳ thực tập hưởng lương tại FPT Software vào cuối bài để tạo bản v2.',
    routeTemplate: '/workspaces/{workspace_id}/editor?taskId={task_id}',
    apiEndpoint: 'GET /api/v1/workspaces/:workspaceId/tasks/:taskId/versions',
    algorithmTier: 'Tầng 1 & Tầng 2 (Tự động nhận diện Tiptap hoặc Yjs Canvas) + Xuống dòng cuối bài và nhả chữ',
    stateBefore: 'REJECTED (Bản v1)',
    stateAfter: 'IN_REVIEW (Bản v2 kèm lịch sử so sánh v1 và v2)',
    manualSubmitButton: 'Tự bấm "Lưu" -> Mở xem "Lịch sử phiên bản" (Diff v1 - v2) -> Bấm "Gửi duyệt"',
    presenterNotes:
      'Sau khi hệ thống gõ xong câu bổ sung ở cuối bài, bạn bấm Lưu và mở Lịch sử phiên bản để Hội đồng thấy rõ dòng chữ mới vừa thêm được đánh dấu khác biệt so với bản v1.',
    sequentialPipeline: [
      {
        order: 'Bước 1',
        fieldLabel: 'Chuyển về Cửa sổ 3 của Nguyễn Chơn Phước (Creator)',
        behaviorBadge: 'Đưa cửa sổ lên trước',
        sampleValue: '/workspaces/{workspace_id}/editor?taskId={task_id}',
        domTarget: 'EditorPage',
      },
      {
        order: 'Bước 2',
        fieldLabel: 'Đưa con trỏ xuống cuối bài và gõ câu bổ sung học bổng + thực tập FPT Software',
        behaviorBadge: 'Nhả chữ nối tiếp cuối bài',
        sampleValue:
          'Sinh viên có cơ hội nhận học bổng Nguyễn Văn Đạo từ 50% đến 100% học phí và tham gia thực tập hưởng lương tại FPT Software ngay từ năm thứ 3.',
        domTarget: ".ProseMirror[contenteditable='true'], [aria-label='Content editor input']",
      },
      {
        order: 'Tự bấm chốt',
        fieldLabel: 'Bấm "Lưu", mở xem so sánh phiên bản v1 - v2 và bấm "Gửi duyệt"',
        behaviorBadge: 'Thao tác trên sân khấu',
        sampleValue: 'Tạo bản v2 và gửi duyệt lại (REJECTED -> IN_REVIEW)',
        domTarget: 'TaskEditorActions > Button',
        isManualStop: true,
      },
    ],
    fields: [
      {
        fieldName: 'Nội dung bổ sung ở bản v2',
        meaningForJury: 'Trả lời đúng 2 ý mà đại diện Đại học FPT đã yêu cầu ở Bước B9',
        selector: ".ProseMirror[contenteditable='true'], [aria-label='Content editor input']",
        sampleValue:
          'Sinh viên có cơ hội nhận học bổng Nguyễn Văn Đạo từ 50% đến 100% học phí và tham gia thực tập hưởng lương tại FPT Software ngay từ năm thứ 3.',
        inputMode: 'Gõ nối tiếp vào cuối bài (append_newline=True)',
      },
    ],
    actions: [
      { actionId: 'B10_NAV_CREATOR_FIX', label: '1. Mở trình soạn thảo để sửa bài (Nguyễn Chơn Phước)', variant: 'secondary' },
      {
        actionId: 'B10_SEQ_FILL_V2',
        label: '2. Gõ bổ sung thông tin Học bổng Nguyễn Văn Đạo & Thực tập (Bản v2)',
        variant: 'typing',
        defaultTextKey: 'B10_V2_ADDITION',
      },
    ],
  },
  {
    id: 'B11',
    number: 11,
    stageId: 3,
    stageTitle: 'Chặng 3: Duyệt 2 cấp & Bản v2',
    title: 'Phê duyệt hoàn tất bản v2 (Manager Nguyễn Thành Lộc -> Client Nguyễn Minh Tuấn)',
    subtitle: 'Duyệt qua 2 cấp cho bản v2 để chuyển trạng thái bài viết sang APPROVED (Sẵn sàng đăng)',
    roleKey: 'client',
    canonicalRole: 'Client',
    windowNumber: 4,
    fptBusinessContext:
      'Bản v2 đã đầy đủ thông tin học bổng và thực tập. Nguyễn Thành Lộc duyệt tầng 1 và Nguyễn Minh Tuấn duyệt chốt tầng 2.',
    routeTemplate: '/workspaces/{workspace_id}/task-approvals?task={task_id}',
    apiEndpoint: 'POST /api/v1/workspaces/:workspaceId/tasks/:taskId/review/approve',
    algorithmTier: 'Chuyển nhanh từ Cửa sổ 2 (Manager) sang Cửa sổ 4 (Client) + Khoanh sáng nút Phê duyệt',
    stateBefore: 'IN_REVIEW (Bản v2)',
    stateAfter: 'APPROVED (Đã duyệt hoàn tất 2 cấp)',
    manualSubmitButton: 'Bấm "Phê duyệt" ở Cửa sổ 2 (Manager) -> Bấm nút 2 -> Bấm "Phê duyệt" ở Cửa sổ 4 (Client)',
    presenterNotes:
      'Khi cả Nguyễn Thành Lộc và Nguyễn Minh Tuấn cùng duyệt xong, bài viết chính thức đạt trạng thái APPROVED và sẵn sàng để xuất bản lên mạng xã hội.',
    sequentialPipeline: [
      {
        order: 'Bước 11a',
        fieldLabel: 'Mở Cửa sổ 2 (Nguyễn Thành Lộc) và khoanh sáng nút Phê duyệt tầng 1',
        behaviorBadge: 'Cửa sổ 2: Manager',
        sampleValue: 'Nguyễn Thành Lộc bấm "Phê duyệt" (MANAGER_REVIEW -> CLIENT_REVIEW)',
        domTarget: 'button.bg-emerald-600',
        isManualStop: true,
      },
      {
        order: 'Bước 11b',
        fieldLabel: 'Mở Cửa sổ 4 (Nguyễn Minh Tuấn) và khoanh sáng nút Phê duyệt tầng 2',
        behaviorBadge: 'Cửa sổ 4: Client',
        sampleValue: 'Nguyễn Minh Tuấn bấm "Phê duyệt" (CLIENT_REVIEW -> APPROVED)',
        domTarget: 'button.bg-emerald-600',
        isManualStop: true,
      },
    ],
    fields: [
      {
        fieldName: 'Trạng thái sau khi duyệt đủ 2 cấp',
        meaningForJury: 'Điều kiện bắt buộc để bài viết được phép đăng lên các kênh truyền thông chính thức',
        selector: 'TaskReviewStatus',
        sampleValue: 'APPROVED (Đã được Đại học FPT nghiệm thu)',
        inputMode: 'Hiển thị trực quan',
      },
    ],
    actions: [
      { actionId: 'B11_NAV_MANAGER_V2', label: '1. (B11a) Mở Cửa sổ 2: Nguyễn Thành Lộc duyệt vòng 2', variant: 'secondary' },
      { actionId: 'B11_NAV_CLIENT_V2', label: '2. (B11b) Mở Cửa sổ 4: Nguyễn Minh Tuấn duyệt chốt APPROVED', variant: 'primary' },
    ],
  },
  {
    id: 'B12',
    number: 12,
    stageId: 4,
    stageTitle: 'Chặng 4: Xuất bản mạng xã hội',
    title: 'Kiểm tra 4 tài khoản mạng xã hội của Đại học FPT',
    subtitle: 'Nguyễn Thành Lộc (Manager) mở trang quản lý 4 kênh đã kết nối: Facebook, Instagram, TikTok, Threads',
    roleKey: 'manager',
    canonicalRole: 'Manager',
    windowNumber: 2,
    fptBusinessContext:
      'Workspace đã kết nối sẵn 4 kênh truyền thông của Đại học FPT để đăng bài trực tiếp từ hệ thống BrandHub.',
    routeTemplate: '/workspaces/{workspace_id}/social-accounts',
    apiEndpoint: 'GET /api/v1/workspaces/:workspaceId/social-accounts',
    algorithmTier: 'Đưa Cửa sổ 2 (Manager) lên trên cùng và mở trang Tài khoản mạng xã hội',
    stateBefore: '4 tài khoản ở trạng thái CONNECTED',
    stateAfter: 'Sẵn sàng nhận lệnh xuất bản bài viết',
    manualSubmitButton: 'Chỉ cho Hội đồng xem 4 nền tảng Facebook, Instagram, TikTok và Threads đang kết nối',
    presenterNotes:
      'Giới thiệu 4 nền tảng mạng xã hội được hỗ trợ chính thức trong hệ thống: Facebook, Instagram, TikTok và Threads.',
    sequentialPipeline: [
      {
        order: 'Bước 1',
        fieldLabel: 'Mở trang Tài khoản mạng xã hội trên Cửa sổ 2 (Nguyễn Thành Lộc)',
        behaviorBadge: 'Chuyển trang tự động',
        sampleValue: 'Hiển thị 4 kênh: Facebook, Instagram, TikTok, Threads',
        domTarget: '/workspaces/{workspace_id}/social-accounts',
      },
    ],
    fields: [
      {
        fieldName: 'Danh sách 4 kênh mạng xã hội',
        meaningForJury: 'Các kênh truyền thông đã xác thực OAuth trong Workspace của Đại học FPT',
        selector: 'SocialAccountCard',
        sampleValue: 'Facebook (FPT University), Instagram, TikTok và Threads',
        inputMode: 'Hiển thị trực quan',
      },
    ],
    actions: [
      { actionId: 'B12_NAV_SOCIAL', label: '1. Mở 4 Kênh mạng xã hội của Đại học FPT (Nguyễn Thành Lộc)', variant: 'primary' },
    ],
  },
  {
    id: 'B13',
    number: 13,
    stageId: 4,
    stageTitle: 'Chặng 4: Xuất bản mạng xã hội',
    title: 'Đăng bài lên Fanpage Đại học FPT và xem kết quả xuất bản',
    subtitle: 'Nguyễn Thành Lộc (Manager) chọn Bài #1 đã duyệt, tích chọn kênh Facebook và bấm Đăng ngay',
    roleKey: 'manager',
    canonicalRole: 'Manager',
    windowNumber: 2,
    fptBusinessContext:
      'Bài viết tuyển sinh ngành Vi mạch và AI (bản v2) được đẩy qua Publisher Service để đăng lên Fanpage và cập nhật tiến độ chiến dịch.',
    routeTemplate: '/workspaces/{workspace_id}/publish',
    apiEndpoint: 'POST /api/v1/workspaces/:workspaceId/publish',
    algorithmTier: 'Điều hướng tới trang Xuất bản (B13a) và trang Theo dõi kết quả đăng bài (B13b)',
    stateBefore: 'APPROVED (Chờ đăng)',
    stateAfter: 'PUBLISHED (Đã đăng thành công lên Fanpage)',
    manualSubmitButton: 'Chỉ tích chọn 1 kênh (Facebook) rồi tự tay bấm nút "Đăng ngay"',
    presenterNotes:
      'Lưu ý: Chỉ tích chọn 1 kênh (Facebook) khi bấm "Đăng ngay", sau đó bấm nút số 2 (B13b) để mở bảng theo dõi trạng thái bài đăng.',
    sequentialPipeline: [
      {
        order: 'Bước 13a',
        fieldLabel: 'Mở trang Xuất bản bài viết trên Cửa sổ 2 (Nguyễn Thành Lộc)',
        behaviorBadge: 'Chuyển trang tự động',
        sampleValue: 'Chọn Bài #1 -> Tích chọn kênh Facebook -> Bấm Đăng ngay',
        domTarget: '/workspaces/{workspace_id}/publish',
        isManualStop: true,
      },
      {
        order: 'Bước 13b',
        fieldLabel: 'Mở trang Theo dõi kết quả xuất bản (Publish Dashboard)',
        behaviorBadge: 'Kiểm tra trạng thái PUBLISHED',
        sampleValue: 'Hiển thị lịch sử đăng bài và liên kết tới bài viết thực tế',
        domTarget: '/workspaces/{workspace_id}/publish/dashboard',
      },
    ],
    fields: [
      {
        fieldName: 'Kênh nhận bài đăng',
        meaningForJury: 'Thực hiện xuất bản bất đồng bộ qua hàng đợi RabbitMQ sang Publisher Service',
        selector: 'PlatformCheckbox[value="facebook"]',
        sampleValue: 'Facebook Fanpage (Chỉ tích chọn 1 kênh khi demo)',
        inputMode: 'Tự tích chọn & bấm Đăng ngay',
      },
    ],
    actions: [
      { actionId: 'B13_NAV_PUBLISH', label: '1. (B13a) Mở trang Xuất bản bài viết (Nguyễn Thành Lộc)', variant: 'primary' },
      { actionId: 'B13_NAV_DASHBOARD', label: '2. (B13b) Mở trang Kết quả xuất bản', variant: 'secondary' },
    ],
  },
  {
    id: 'B14',
    number: 14,
    stageId: 5,
    stageTitle: 'Chặng 5: Thanh toán VietQR & Admin',
    title: 'Nâng cấp gói thuê bao Plus cho FPT Smart Ads qua VietQR SePay',
    subtitle: 'Lê Trí Trung (Owner) mở trang Gói thuê bao và bấm nâng cấp lên gói Plus bằng mã QR ngân hàng',
    roleKey: 'owner',
    canonicalRole: 'Owner',
    windowNumber: 1,
    fptBusinessContext:
      'Để phục vụ thêm nhiều dự án truyền thông mới, Giám đốc FPT Smart Ads (Lê Trí Trung) nâng cấp tài khoản Agency lên gói Plus qua cổng VietQR SePay.',
    routeTemplate: '/subscription/plans',
    apiEndpoint: 'POST /api/v1/subscriptions/upgrade',
    algorithmTier: 'Đưa Cửa sổ 1 (Owner: Lê Trí Trung) lên trên cùng và mở trang Gói thuê bao',
    stateBefore: 'Gói hiện tại: Basic',
    stateAfter: 'Hiển thị mã QR VietQR (SePay) và tự động kích hoạt gói Plus sau khi thanh toán',
    manualSubmitButton: 'Tự tay bấm nút "Nâng cấp" ở thẻ gói Plus để mở mã QR VietQR trên màn hình',
    presenterNotes:
      'Trình bày luồng thanh toán tự động qua SePay/PayOS (VietQR): Hệ thống sinh mã QR kèm nội dung chuyển khoản định danh và tự động nâng cấp gói ngay khi nhận webhook.',
    sequentialPipeline: [
      {
        order: 'Bước 1',
        fieldLabel: 'Chuyển sang Cửa sổ 1 của Lê Trí Trung (Owner)',
        behaviorBadge: 'Đưa cửa sổ lên trước',
        sampleValue: '/subscription/plans',
        domTarget: 'SubscriptionPlansPage',
      },
      {
        order: 'Tự bấm chốt',
        fieldLabel: 'Bấm nút "Nâng cấp" ở gói Plus để hiển thị mã VietQR',
        behaviorBadge: 'Thao tác trên sân khấu',
        sampleValue: 'Mở hộp thoại quét mã VietQR SePay (2.000đ để test giao dịch thực tế)',
        domTarget: 'Upgrade Plan Button',
        isManualStop: true,
      },
    ],
    fields: [
      {
        fieldName: 'Gói thuê bao nâng cấp',
        meaningForJury: 'Mô hình thu phí định kỳ (SaaS Subscription) của nền tảng BrandHub',
        selector: 'PlanCard[data-plan="PLUS"]',
        sampleValue: 'Gói Plus (Tăng giới hạn Workspace, Thành viên và Tín chỉ AI)',
        inputMode: 'Người thuyết trình bấm Nâng cấp',
      },
    ],
    actions: [
      { actionId: 'B14_NAV_PLANS', label: '1. Mở trang Nâng cấp gói thuê bao VietQR (Lê Trí Trung - Owner)', variant: 'primary' },
    ],
  },
  {
    id: 'B15',
    number: 15,
    stageId: 5,
    stageTitle: 'Chặng 5: Thanh toán VietQR & Admin',
    title: 'Hà Văn Ân (Admin) xem báo cáo doanh thu MRR/ARR và hàng đợi kiểm duyệt',
    subtitle: 'Chuyển sang Cửa sổ 5 (Admin) để xem thống kê doanh thu thuê bao và danh sách nội dung vi phạm',
    roleKey: 'admin',
    canonicalRole: 'Admin',
    windowNumber: 5,
    fptBusinessContext:
      'Hà Văn Ân (Quản trị viên hệ thống BrandHub) kiểm tra doanh thu từ các gói thuê bao Agency và rà soát các cảnh báo an toàn nội dung trên toàn hệ thống.',
    routeTemplate: '/admin?view=revenue',
    apiEndpoint: 'GET /api/v1/admin/revenue/overview & GET /api/v1/admin/moderation/queue',
    algorithmTier: 'Đưa Cửa sổ 5 (Admin: Hà Văn Ân) lên trên cùng và chuyển nhanh giữa 2 màn hình quản trị',
    stateBefore: 'Dữ liệu giao dịch nâng cấp gói và lịch sử quét nội dung',
    stateAfter: 'Hiển thị biểu đồ doanh thu MRR/ARR và bảng hậu kiểm nội dung vi phạm',
    manualSubmitButton: 'Trình bày số liệu doanh thu ở B15a, sau đó bấm B15b để mở Hàng đợi kiểm duyệt',
    presenterNotes:
      'Kết thúc phần demo bằng góc nhìn quản trị hệ thống của Hà Văn Ân: vừa quản lý được dòng tiền thuê bao từ các Agency, vừa giám sát an toàn nội dung tập trung.',
    sequentialPipeline: [
      {
        order: 'Bước 15a',
        fieldLabel: 'Mở bảng thống kê Doanh thu thuê bao (MRR / ARR)',
        behaviorBadge: 'Cửa sổ 5: Admin Hà Văn Ân',
        sampleValue: '/admin?view=revenue',
        domTarget: 'AdminRevenueDashboard',
      },
      {
        order: 'Bước 15b',
        fieldLabel: 'Mở Hàng đợi kiểm duyệt nội dung vi phạm',
        behaviorBadge: 'Cửa sổ 5: Admin Hà Văn Ân',
        sampleValue: '/admin?view=moderation',
        domTarget: 'AdminModerationQueue',
      },
    ],
    fields: [
      {
        fieldName: 'Thống kê doanh thu (MRR / ARR)',
        meaningForJury: 'Tổng hợp doanh thu định kỳ tháng/năm và tỷ lệ chuyển đổi gói thuê bao',
        selector: 'AdminRevenueMetrics',
        sampleValue: 'Biểu đồ doanh thu và danh sách giao dịch nâng cấp gói qua SePay',
        inputMode: 'Hiển thị trực quan',
      },
      {
        fieldName: 'Hàng đợi kiểm duyệt (Moderation Queue)',
        meaningForJury: 'Ghi nhận các nội dung bị chặn hoặc cảnh báo từ các Workspace để Admin hậu kiểm',
        selector: 'ModerationQueueTable',
        sampleValue: 'Danh sách các bản ghi bị đánh dấu BLOCKED / WARNING',
        inputMode: 'Hiển thị trực quan',
      },
    ],
    actions: [
      { actionId: 'B15_NAV_ADMIN_REVENUE', label: '1. (B15a) Mở Dashboard Doanh thu MRR/ARR (Hà Văn Ân - Admin)', variant: 'primary' },
      { actionId: 'B15_NAV_ADMIN_MODERATION', label: '2. (B15b) Mở Hàng đợi Kiểm duyệt nội dung (Hà Văn Ân - Admin)', variant: 'secondary' },
    ],
  },
];

const DEFAULT_EDITABLE_TEXTS: Record<string, string> = {
  B6_AI_TOPIC:
    'Giới thiệu chương trình đào tạo ngành Thiết kế Vi mạch và Trí tuệ nhân tạo tại Đại học FPT, hưởng ứng mục tiêu 50.000 kỹ sư bán dẫn của Việt Nam đến năm 2030',
  B7_VIOLATION:
    'Bài viết chứa nội dung kích động bạo lực và ngôn từ thù ghét vi phạm quy định an toàn thông tin.',
  B7_CLEAN_V1:
    'Đại học FPT mở cổng đăng ký ngành Thiết kế Vi mạch và Trí tuệ nhân tạo kỳ thu 2026.\nChương trình đào tạo gắn với mục tiêu phát triển 50.000 kỹ sư bán dẫn tại Việt Nam đến năm 2030.\n#DaiHocFPT #ViMachBanDan #ChuyenDoiSoVietNam',
  B9_REJECT_REASON:
    'Bài viết đã rõ ý chính. Nhờ bạn bổ sung thêm thông tin học bổng Nguyễn Văn Đạo từ 50% đến 100% và kỳ thực tập thực tế tại FPT Software từ năm thứ 3.',
  B10_V2_ADDITION:
    'Sinh viên có cơ hội nhận học bổng Nguyễn Văn Đạo từ 50% đến 100% học phí và tham gia thực tập hưởng lương tại FPT Software ngay từ năm thứ 3.',
};

const MONITOR_API = 'http://localhost:3999';

export const DemoMonitorPage: React.FC = () => {
  const [serverOnline, setServerOnline] = useState<boolean>(false);
  const [activeRoles, setActiveRoles] = useState<string[]>([]);
  const [roleUrls, setRoleUrls] = useState<Record<string, string>>({});
  const [busyAction, setBusyAction] = useState<string | null>(null);
  const [selectedStepId, setSelectedStepId] = useState<string>('B1');
  const [completedSteps, setCompletedSteps] = useState<Record<string, boolean>>({});
  const [editableTexts, setEditableTexts] = useState<Record<string, string>>(DEFAULT_EDITABLE_TEXTS);
  const [copiedKey, setCopiedKey] = useState<string | null>(null);
  const [drawerTab, setDrawerTab] = useState<'none' | 'fpt-overview' | 'algorithm' | 'config'>('none');

  const [config, setConfig] = useState<MonitorState>({
    base_url: 'http://localhost:5173',
    agency_id: '359a1839-18c7-48e2-8a68-f5f68c3375b6',
    workspace_id: 'b47477c4-13ad-44ff-8c49-f73f1837461b',
    active_task_id: 'c6453698-cf56-38c1-96d2-90ccdd985228',
    chunk_speed: 'normal',
    status_message: 'Đang kết nối tới Selenium Monitor Server (:3999)...',
    last_step: null,
  });

  const currentStepIndex = DEMO_STEPS.findIndex((s) => s.id === selectedStepId);
  const currentStep = DEMO_STEPS[currentStepIndex] || DEMO_STEPS[0];
  const currentRoleConfig = ROLES.find((r) => r.key === currentStep.roleKey) || ROLES[0];

  const fetchState = async () => {
    try {
      const res = await fetch(`${MONITOR_API}/api/state`);
      const data = await res.json();
      if (data.ok) {
        setServerOnline(true);
        setActiveRoles(data.active_roles || []);
        setRoleUrls(data.role_urls || {});
        setConfig((prev) => ({
          ...prev,
          ...data.state,
        }));
      }
    } catch {
      setServerOnline(false);
    }
  };

  useEffect(() => {
    fetchState();
    const timer = setInterval(fetchState, 2500);
    return () => clearInterval(timer);
  }, []);

  const updateConfig = async (partial: Partial<MonitorState>) => {
    const next = { ...config, ...partial };
    setConfig(next);
    try {
      const res = await fetch(`${MONITOR_API}/api/config`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(next),
      });
      const data = await res.json();
      if (data.ok && data.state) {
        setConfig(data.state);
      }
    } catch {
      // ignore offline
    }
  };

  const runAction = async (actionId: string, stepId?: string, textKey?: string) => {
    setBusyAction(actionId);
    const payload: Record<string, string> = { action_id: actionId };
    if (textKey && editableTexts[textKey]) {
      payload.text = editableTexts[textKey];
    }
    try {
      const res = await fetch(`${MONITOR_API}/api/action`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (data.state) {
        setConfig(data.state);
      }
      if (stepId) {
        setCompletedSteps((prev) => ({ ...prev, [stepId]: true }));
      }
      await fetchState();
    } catch {
      setConfig((prev) => ({
        ...prev,
        status_message:
          'Chưa kết nối được cổng :3999. Hãy bấm "Start presentation" trên ứng dụng Run BrandHub hoặc chạy: npm run demo-monitor',
      }));
    } finally {
      setBusyAction(null);
    }
  };

  const resolveFullUrl = (template: string) => {
    const path = template
      .replace('{agency_id}', config.agency_id)
      .replace('{workspace_id}', config.workspace_id)
      .replace('{task_id}', config.active_task_id);
    return `${config.base_url.replace(/\/$/, '')}${path}`;
  };

  const copyToClipboard = (text: string, key: string) => {
    navigator.clipboard.writeText(text);
    setCopiedKey(key);
    setTimeout(() => setCopiedKey(null), 1500);
  };

  const goPrevStep = () => {
    if (currentStepIndex > 0) {
      setSelectedStepId(DEMO_STEPS[currentStepIndex - 1].id);
    }
  };

  const goNextStep = () => {
    if (currentStepIndex < DEMO_STEPS.length - 1) {
      setSelectedStepId(DEMO_STEPS[currentStepIndex + 1].id);
    }
  };

  return (
    <div className="min-h-[calc(100vh-3.5rem)] bg-slate-50 text-slate-900 flex flex-col font-sans">
      {/* ── THANH ĐIỀU KHIỂN TRÊN CÙNG (BLUE & WHITE COMMAND HEADER) ── */}
      <header className="bg-white border-b border-slate-200 px-5 py-2.5 sticky top-0 z-20 shadow-2xs">
        <div className="max-w-[1600px] mx-auto flex flex-wrap items-center justify-between gap-3">
          {/* Trạng thái & Thương hiệu */}
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-blue-600 text-white flex items-center justify-center shadow-xs">
              <Monitor className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-sm font-bold tracking-tight text-slate-900">
                  Bảng Điều Khiển Thuyết Trình (FPT Smart Ads & Đại học FPT)
                </h1>
                <span
                  className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[11px] font-semibold border ${
                    serverOnline
                      ? 'bg-blue-50 text-blue-700 border-blue-200'
                      : 'bg-amber-50 text-amber-800 border-amber-200'
                  }`}
                >
                  <span
                    className={`w-1.5 h-1.5 rounded-full ${
                      serverOnline ? 'bg-blue-600 animate-pulse' : 'bg-amber-500'
                    }`}
                  />
                  {serverOnline ? 'Selenium :3999 Sẵn sàng' : 'Chưa bật :3999'}
                </span>
              </div>
              <p className="text-xs text-slate-500">
                5 Thành viên Đồ án | Mục tiêu 50.000 kỹ sư bán dẫn Việt Nam 2030 & Sự kiện AI4VN | Tự bấm các nút chốt
              </p>
            </div>
          </div>

          {/* Cụm công cụ điều khiển nhanh */}
          <div className="flex flex-wrap items-center gap-2">
            {/* Chuyển môi trường Localhost / Production */}
            <div className="inline-flex rounded-lg border border-slate-200 bg-slate-100 p-0.5">
              <button
                type="button"
                onClick={() => updateConfig({ base_url: 'http://localhost:5173' })}
                className={`px-2.5 py-1 rounded-md text-xs font-semibold transition-all ${
                  config.base_url.includes('localhost')
                    ? 'bg-blue-600 text-white shadow-2xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                Localhost (:5173)
              </button>
              <button
                type="button"
                onClick={() => updateConfig({ base_url: 'https://brandhub.id.vn' })}
                className={`px-2.5 py-1 rounded-md text-xs font-semibold transition-all flex items-center gap-1 ${
                  config.base_url.includes('brandhub.id.vn')
                    ? 'bg-blue-600 text-white shadow-2xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                <Globe className="w-3 h-3" />
                brandhub.id.vn
              </button>
            </div>

            {/* Tốc độ nhả chữ */}
            <div className="inline-flex items-center rounded-lg border border-slate-200 bg-white px-2.5 py-1 gap-1.5">
              <Keyboard className="w-3.5 h-3.5 text-blue-600" />
              <span className="text-[11px] font-medium text-slate-500">Nhịp gõ:</span>
              <select
                value={config.chunk_speed}
                onChange={(e) =>
                  updateConfig({ chunk_speed: e.target.value as MonitorState['chunk_speed'] })
                }
                className="text-xs font-semibold text-blue-700 bg-transparent focus:outline-none cursor-pointer"
              >
                <option value="fast">Nhanh (22-48ms)</option>
                <option value="normal">Tự nhiên (42-88ms)</option>
                <option value="slow">Chậm rõ (80-145ms)</option>
              </select>
            </div>

            {/* Nút mở Bảng tổng quan Dữ liệu FPT & 5 Thành viên */}
            <button
              type="button"
              onClick={() => setDrawerTab(drawerTab === 'fpt-overview' ? 'none' : 'fpt-overview')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all flex items-center gap-1.5 ${
                drawerTab === 'fpt-overview'
                  ? 'bg-blue-50 border-blue-300 text-blue-700'
                  : 'bg-white border-slate-200 text-slate-700 hover:bg-slate-50'
              }`}
            >
              <Building2 className="w-3.5 h-3.5 text-blue-600" />
              Kịch bản Việt Nam & 5 Thành viên
            </button>

            {/* Nút mở Kiểm tra Thuật toán Selenium 3 Tầng */}
            <button
              type="button"
              onClick={() => setDrawerTab(drawerTab === 'algorithm' ? 'none' : 'algorithm')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all flex items-center gap-1.5 ${
                drawerTab === 'algorithm'
                  ? 'bg-blue-50 border-blue-300 text-blue-700'
                  : 'bg-white border-slate-200 text-slate-700 hover:bg-slate-50'
              }`}
            >
              <Cpu className="w-3.5 h-3.5 text-blue-600" />
              Thuật toán Gõ 3 Tầng
            </button>

            {/* Nút Cấu hình UUID */}
            <button
              type="button"
              onClick={() => setDrawerTab(drawerTab === 'config' ? 'none' : 'config')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all flex items-center gap-1.5 ${
                drawerTab === 'config'
                  ? 'bg-blue-50 border-blue-300 text-blue-700'
                  : 'bg-white border-slate-200 text-slate-700 hover:bg-slate-50'
              }`}
            >
              <Sliders className="w-3.5 h-3.5 text-blue-600" />
              UUID Hệ thống
            </button>

            {/* Nút Khởi tạo cả 5 cửa sổ */}
            <button
              type="button"
              disabled={busyAction !== null}
              onClick={() => runAction('INIT_ALL_5_ROLES')}
              className="px-3.5 py-1.5 rounded-lg text-xs font-semibold bg-blue-600 hover:bg-blue-700 text-white shadow-xs transition-all flex items-center gap-1.5 disabled:opacity-50 cursor-pointer"
            >
              <Play className="w-3.5 h-3.5 fill-current" />
              Khởi tạo 5 Cửa sổ
            </button>
          </div>
        </div>

        {/* ── DRAWER 1: BẢNG TỔNG QUAN SỰ KIỆN VIỆT NAM, DOANH NGHIỆP FPT & 5 THÀNH VIÊN ĐỒ ÁN ── */}
        {drawerTab === 'fpt-overview' && (
          <div className="max-w-[1600px] mx-auto mt-3 pt-3 border-t border-slate-200 bg-slate-50/90 rounded-xl p-4 space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Building2 className="w-4 h-4 text-blue-600" />
                <span className="text-xs font-bold uppercase tracking-wider text-blue-800">
                  Tóm tắt Kịch bản Thực tế tại Việt Nam & Phân vai 5 Thành viên Nhóm Đồ án
                </span>
              </div>
              <button
                type="button"
                onClick={() => setDrawerTab('none')}
                className="text-xs text-slate-500 hover:text-slate-800 flex items-center gap-1"
              >
                <X className="w-3.5 h-3.5" /> Đóng
              </button>
            </div>

            {/* 4 Thực thể cốt lõi */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
              <div className="bg-white rounded-lg border border-blue-200 p-3">
                <div className="text-[11px] font-bold text-blue-700 uppercase">1. Đơn vị thực hiện (Agency)</div>
                <div className="text-sm font-bold text-slate-900 mt-0.5">FPT Smart Ads Agency</div>
                <div className="text-xs text-slate-600 mt-1">
                  Đơn vị phụ trách lên kế hoạch truyền thông, viết bài bằng AI và quản lý lịch đăng bài.
                </div>
              </div>
              <div className="bg-white rounded-lg border border-blue-200 p-3">
                <div className="text-[11px] font-bold text-blue-700 uppercase">2. Khách hàng (Brand Client)</div>
                <div className="text-sm font-bold text-slate-900 mt-0.5">Đại học FPT (Tập đoàn FPT)</div>
                <div className="text-xs text-slate-600 mt-1">
                  Triển khai tuyển sinh ngành Thiết kế Vi mạch và Trí tuệ nhân tạo kỳ thu năm 2026.
                </div>
              </div>
              <div className="bg-white rounded-lg border border-blue-200 p-3">
                <div className="text-[11px] font-bold text-blue-700 uppercase">3. Sự kiện & Mục tiêu Quốc gia</div>
                <div className="text-sm font-bold text-slate-900 mt-0.5">50.000 Kỹ sư Bán dẫn & AI4VN</div>
                <div className="text-xs text-slate-600 mt-1">
                  Hưởng ứng mục tiêu 50.000 kỹ sư bán dẫn Việt Nam đến 2030 và Ngày hội Trí tuệ Nhân tạo Việt Nam (AI4VN).
                </div>
              </div>
              <div className="bg-white rounded-lg border border-blue-200 p-3">
                <div className="text-[11px] font-bold text-blue-700 uppercase">4. 4 Đầu việc trong Chiến dịch</div>
                <div className="text-sm font-bold text-slate-900 mt-0.5">2 Bài đăng, 1 Báo chí, 1 Khảo sát</div>
                <div className="text-xs text-slate-600 mt-1">
                  Ngân sách trọn gói 18.000.000 VNĐ trong 6 tuần trên Facebook, Instagram, TikTok và Threads.
                </div>
              </div>
            </div>

            {/* Bảng 5 thành viên nhóm đồ án */}
            <div className="bg-white rounded-lg border border-slate-200 overflow-hidden">
              <table className="w-full text-left border-collapse text-xs">
                <thead>
                  <tr className="bg-slate-50 border-b border-slate-200 text-[11px] font-bold uppercase text-slate-500">
                    <th className="py-2 px-3">Cửa sổ Chrome</th>
                    <th className="py-2 px-3">Vai trò (Role)</th>
                    <th className="py-2 px-3">Thành viên Nhóm Đồ án</th>
                    <th className="py-2 px-3">Đơn vị trong Kịch bản</th>
                    <th className="py-2 px-3">Tài khoản Đăng nhập</th>
                    <th className="py-2 px-3">Công việc thực hiện trong buổi bảo vệ</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {ROLES.map((r) => (
                    <tr key={r.key} className="hover:bg-blue-50/30">
                      <td className="py-2 px-3 font-bold text-slate-800">{r.windowLabel}</td>
                      <td className="py-2 px-3">
                        <span className="px-2 py-0.5 rounded bg-blue-600 text-white font-bold text-[11px]">
                          {r.canonicalRole}
                        </span>
                      </td>
                      <td className="py-2 px-3 font-bold text-blue-900">{r.fullName}</td>
                      <td className="py-2 px-3 font-medium text-slate-700">{r.organization}</td>
                      <td className="py-2 px-3 font-mono text-[11px] text-slate-600">{r.email}</td>
                      <td className="py-2 px-3 text-slate-600">{r.responsibility}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* ── DRAWER 2: KIỂM CHỨNG THUẬT TOÁN SELENIUM 3 TẦNG ── */}
        {drawerTab === 'algorithm' && (
          <div className="max-w-[1600px] mx-auto mt-3 pt-3 border-t border-slate-200 bg-slate-50/90 rounded-xl p-4 space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Cpu className="w-4 h-4 text-blue-600" />
                <span className="text-xs font-bold uppercase tracking-wider text-blue-800">
                  Cơ chế Thuật toán Gõ Chữ Tuần tự 3 Tầng (Tương thích với cả 3 loại ô nhập liệu của BrandHub Web)
                </span>
              </div>
              <button
                type="button"
                onClick={() => setDrawerTab('none')}
                className="text-xs text-slate-500 hover:text-slate-800 flex items-center gap-1"
              >
                <X className="w-3.5 h-3.5" /> Đóng
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
              <div className="bg-white rounded-lg border border-blue-200 p-3.5 space-y-1.5">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-blue-700 uppercase text-[11px]">
                    Tầng 1: Yjs Canvas Text Editor
                  </span>
                  <span className="px-2 py-0.5 rounded bg-blue-50 text-blue-700 font-mono text-[10px]">
                    Bước B7.1, B7.2
                  </span>
                </div>
                <p className="font-semibold text-slate-900">
                  Áp dụng cho: <code>[aria-label="Content editor input"]</code>
                </p>
                <p className="text-slate-600 leading-relaxed">
                  Trình soạn thảo <code>CanvasTextEditor</code> lưu dữ liệu trong <code>Y.Text</code> (Yjs) và vẽ lên thẻ{' '}
                  <code>&lt;canvas&gt;</code>. Thuật toán phát sự kiện{' '}
                  <code>new InputEvent(&apos;beforeinput&apos;, &#123; inputType: &apos;insertText&apos;, data: chunk &#125;)</code>{' '}
                  theo từng cụm âm tiết tiếng Việt để không bị mất dấu cách.
                </p>
              </div>

              <div className="bg-white rounded-lg border border-blue-200 p-3.5 space-y-1.5">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-blue-700 uppercase text-[11px]">
                    Tầng 2: Tiptap RichTextEditor (.ProseMirror)
                  </span>
                  <span className="px-2 py-0.5 rounded bg-blue-50 text-blue-700 font-mono text-[10px]">
                    Bước B10.2
                  </span>
                </div>
                <p className="font-semibold text-slate-900">
                  Áp dụng cho: <code>.ProseMirror[contenteditable="true"]</code>
                </p>
                <p className="text-slate-600 leading-relaxed">
                  Sử dụng <code>ActionChains(driver).key_down(Keys.CONTROL).send_keys(&apos;a&apos;).key_up(Keys.CONTROL)</code>{' '}
                  để giải phóng phím <code>Ctrl</code> đúng chuẩn, sau đó đưa con trỏ xuống cuối bài và nhả từng cụm từ với độ trễ 42-88ms.
                </p>
              </div>

              <div className="bg-white rounded-lg border border-blue-200 p-3.5 space-y-1.5">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-blue-700 uppercase text-[11px]">
                    Tầng 3: React 19 Controlled Input & Textarea
                  </span>
                  <span className="px-2 py-0.5 rounded bg-blue-50 text-blue-700 font-mono text-[10px]">
                    Đăng nhập, B6.2, B9.2
                  </span>
                </div>
                <p className="font-semibold text-slate-900">
                  Áp dụng cho: <code>AiCaptionDialog</code>, <code>#task-review-note</code>, <code>LoginPage</code>
                </p>
                <p className="text-slate-600 leading-relaxed">
                  Đồng bộ giá trị của React 19 qua <code>HTMLTextAreaElement.prototype.value</code> setter và sự kiện{' '}
                  <code>input</code> trước khi gõ từng cụm ký tự, nghỉ <code>0.55s</code> giữa các trường và khoanh sáng nút chốt cuối cùng.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* ── DRAWER 3: CẤU HÌNH ĐỊNH DANH UUID ── */}
        {drawerTab === 'config' && (
          <div className="max-w-[1600px] mx-auto mt-3 pt-3 border-t border-slate-200 grid grid-cols-1 md:grid-cols-4 gap-3 bg-slate-50/80 p-3.5 rounded-xl">
            <div>
              <label className="block text-[11px] font-bold uppercase text-slate-500 mb-1">
                Base URL (Localhost / Production)
              </label>
              <input
                type="text"
                value={config.base_url}
                onChange={(e) => setConfig({ ...config, base_url: e.target.value })}
                onBlur={() => updateConfig({ base_url: config.base_url })}
                className="w-full px-2.5 py-1.5 text-xs font-mono bg-white border border-slate-300 rounded-md focus:border-blue-600 focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-[11px] font-bold uppercase text-slate-500 mb-1">
                Agency ID (FPT Smart Ads Agency)
              </label>
              <input
                type="text"
                value={config.agency_id}
                onChange={(e) => setConfig({ ...config, agency_id: e.target.value })}
                onBlur={() => updateConfig({ agency_id: config.agency_id })}
                className="w-full px-2.5 py-1.5 text-xs font-mono bg-white border border-slate-300 rounded-md focus:border-blue-600 focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-[11px] font-bold uppercase text-slate-500 mb-1">
                Workspace ID (FPT University x FPT Smart Ads)
              </label>
              <input
                type="text"
                value={config.workspace_id}
                onChange={(e) => setConfig({ ...config, workspace_id: e.target.value })}
                onBlur={() => updateConfig({ workspace_id: config.workspace_id })}
                className="w-full px-2.5 py-1.5 text-xs font-mono bg-white border border-slate-300 rounded-md focus:border-blue-600 focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-[11px] font-bold uppercase text-slate-500 mb-1">
                Active Task ID ([Bài #1] Học bổng Vi mạch & AI)
              </label>
              <input
                type="text"
                value={config.active_task_id}
                onChange={(e) => setConfig({ ...config, active_task_id: e.target.value })}
                onBlur={() => updateConfig({ active_task_id: config.active_task_id })}
                className="w-full px-2.5 py-1.5 text-xs font-mono bg-white border border-slate-300 rounded-md focus:border-blue-600 focus:outline-none"
              />
            </div>
          </div>
        )}
      </header>

      {/* ── DẢI 5 CỬA SỐ VAI TRÒ TƯƠNG ỨNG 5 THÀNH VIÊN NHÓM ĐỒ ÁN ── */}
      <section className="bg-white border-b border-slate-200 px-5 py-2.5">
        <div className="max-w-[1600px] mx-auto grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-2.5">
          {ROLES.map((r) => {
            const isActive = activeRoles.includes(r.key);
            const isCurrentStepRole = currentStep.roleKey === r.key;
            const liveUrl = roleUrls[r.key] || '';

            return (
              <div
                key={r.key}
                className={`rounded-xl border p-2.5 transition-all flex flex-col justify-between ${
                  isCurrentStepRole
                    ? 'border-blue-600 bg-blue-50/50 ring-2 ring-blue-600/15'
                    : 'border-slate-200 bg-white hover:border-blue-300'
                }`}
              >
                <div>
                  <div className="flex items-center justify-between gap-1.5 mb-1">
                    <div className="flex items-center gap-1.5">
                      <span
                        className={`text-[11px] font-bold px-2 py-0.5 rounded-md ${
                          isCurrentStepRole
                            ? 'bg-blue-600 text-white'
                            : 'bg-slate-100 text-slate-700'
                        }`}
                      >
                        {r.windowLabel}: {r.canonicalRole}
                      </span>
                      {isCurrentStepRole && (
                        <span className="text-[10px] font-bold text-blue-700 bg-blue-100 px-1.5 py-0.5 rounded">
                          Đang diễn
                        </span>
                      )}
                    </div>
                    <span
                      className={`inline-flex items-center gap-1 text-[10px] font-semibold ${
                        isActive ? 'text-blue-700' : 'text-slate-400'
                      }`}
                    >
                      <span
                        className={`w-1.5 h-1.5 rounded-full ${
                          isActive ? 'bg-blue-600' : 'bg-slate-300'
                        }`}
                      />
                      {isActive ? 'Đã bật' : 'Chưa mở'}
                    </span>
                  </div>

                  {/* Tên thành viên nhóm đồ án nổi bật */}
                  <div className="text-xs font-bold text-slate-900 flex items-center gap-1">
                    <UserCheck className="w-3.5 h-3.5 text-blue-600 shrink-0" />
                    <span className="truncate">{r.fullName}</span>
                  </div>
                  <div className="text-[11px] font-medium text-blue-700 truncate mt-0.5">
                    {r.organization}
                  </div>
                  <div className="flex items-center justify-between text-[11px] text-slate-500 font-mono mt-0.5">
                    <span className="truncate" title={r.email}>
                      {r.email}
                    </span>
                    <button
                      type="button"
                      onClick={() => copyToClipboard(r.email, `email-${r.key}`)}
                      className="text-slate-400 hover:text-blue-600 p-0.5 shrink-0"
                      title="Sao chép Email"
                    >
                      {copiedKey === `email-${r.key}` ? (
                        <Check className="w-3 h-3 text-blue-600" />
                      ) : (
                        <Copy className="w-3 h-3" />
                      )}
                    </button>
                  </div>
                  {liveUrl && (
                    <div
                      className="mt-1 text-[10px] font-mono text-blue-700 bg-blue-50 px-1.5 py-0.5 rounded truncate border border-blue-100"
                      title={liveUrl}
                    >
                      Đang ở: {liveUrl.replace(config.base_url, '') || '/'}
                    </div>
                  )}
                </div>

                <div className="mt-2 pt-1.5 border-t border-slate-100 flex items-center gap-1.5">
                  <button
                    type="button"
                    disabled={busyAction !== null}
                    onClick={() => runAction(`FOCUS_ROLE:${r.key}`)}
                    className={`flex-1 py-1 px-2 rounded-md text-[11px] font-semibold transition-colors cursor-pointer ${
                      isCurrentStepRole
                        ? 'bg-blue-600 text-white hover:bg-blue-700'
                        : 'bg-slate-100 text-slate-700 hover:bg-blue-50 hover:text-blue-700'
                    }`}
                  >
                    Đưa lên trước
                  </button>
                  <button
                    type="button"
                    disabled={busyAction !== null}
                    onClick={() => runAction(`INIT_ROLE:${r.key}`)}
                    className="py-1 px-2 rounded-md text-[11px] font-semibold border border-slate-200 text-slate-600 hover:border-blue-300 hover:text-blue-700 transition-colors cursor-pointer"
                    title="Đăng nhập lại tuần tự"
                  >
                    Đăng nhập
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* ── BỐ CỤC CHÍNH 2 CỘT: DANH SÁCH 15 BƯỚC (TRÁI) & BẢNG ĐIỀU KHIỂN TRỰC QUAN (PHẢI) ── */}
      <div className="max-w-[1600px] w-full mx-auto flex-1 grid grid-cols-1 lg:grid-cols-12 gap-5 p-5">
        {/* CỘT TRÁI: TIMELINE 15 BƯỚC */}
        <aside className="lg:col-span-4 xl:col-span-3 flex flex-col gap-3">
          <div className="bg-white rounded-xl border border-slate-200 p-3.5 shadow-2xs">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
                Tiến độ Kịch bản (15 Bước)
              </span>
              <span className="text-xs font-bold text-blue-700 bg-blue-50 px-2 py-0.5 rounded-full">
                {Object.keys(completedSteps).length} / 15 hoàn thành
              </span>
            </div>
            <div className="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
              <div
                className="h-full bg-blue-600 transition-all duration-300"
                style={{ width: `${(Object.keys(completedSteps).length / 15) * 100}%` }}
              />
            </div>
          </div>

          <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-2xs flex-1 divide-y divide-slate-100">
            {STAGES.map((stage) => {
              const stageSteps = DEMO_STEPS.filter((s) => s.stageId === stage.id);
              return (
                <div key={stage.id} className="p-2.5">
                  <div className="flex items-center justify-between px-2 py-1 mb-1">
                    <span className="text-[11px] font-bold uppercase tracking-wider text-blue-700">
                      {stage.title}
                    </span>
                    <span className="text-[10px] font-mono font-semibold text-slate-400">
                      {stage.range}
                    </span>
                  </div>
                  <div className="space-y-1">
                    {stageSteps.map((step) => {
                      const isSelected = step.id === selectedStepId;
                      const isDone = !!completedSteps[step.id];
                      const stepRole = ROLES.find((r) => r.key === step.roleKey);
                      return (
                        <button
                          key={step.id}
                          type="button"
                          onClick={() => setSelectedStepId(step.id)}
                          className={`w-full text-left px-2.5 py-2 rounded-lg transition-all flex items-start gap-2.5 cursor-pointer ${
                            isSelected
                              ? 'bg-blue-600 text-white shadow-xs'
                              : isDone
                              ? 'bg-blue-50/50 text-slate-800 hover:bg-blue-50'
                              : 'text-slate-700 hover:bg-slate-50'
                          }`}
                        >
                          <span
                            className={`mt-0.5 w-6 h-6 rounded-md text-[11px] font-bold flex items-center justify-center shrink-0 ${
                              isSelected
                                ? 'bg-white text-blue-700'
                                : isDone
                                ? 'bg-blue-600 text-white'
                                : 'bg-slate-100 text-slate-600'
                            }`}
                          >
                            {isDone && !isSelected ? <Check className="w-3.5 h-3.5" /> : step.id}
                          </span>
                          <div className="min-w-0 flex-1">
                            <div className="text-xs font-semibold leading-snug line-clamp-1">
                              {step.title}
                            </div>
                            <div
                              className={`text-[11px] mt-0.5 flex items-center gap-1.5 ${
                                isSelected ? 'text-blue-100' : 'text-slate-500'
                              }`}
                            >
                              <span className="font-semibold">{step.canonicalRole}:</span>
                              <span className="truncate">{stepRole?.fullName}</span>
                            </div>
                          </div>
                        </button>
                      );
                    })}
                  </div>
                </div>
              );
            })}
          </div>
        </aside>

        {/* CỘT PHẢI: BẢNG ĐIỀU KHIỂN CHI TIẾT & TRỰC QUAN HÓA CHO BAN GIÁM KHẢO */}
        <main className="lg:col-span-8 xl:col-span-9 flex flex-col gap-4">
          {/* Thẻ trạng thái phản hồi thời gian thực */}
          <div className="bg-blue-600 text-white rounded-xl px-4 py-3 shadow-xs flex flex-wrap items-center justify-between gap-3">
            <div className="flex items-center gap-2.5 min-w-0">
              <Terminal className="w-4 h-4 shrink-0 text-blue-200" />
              <span className="text-xs font-medium truncate" title={config.status_message}>
                {busyAction ? `Đang thực thi lệnh: ${busyAction}...` : config.status_message}
              </span>
            </div>
            <div className="flex items-center gap-2 shrink-0">
              <button
                type="button"
                onClick={goPrevStep}
                disabled={currentStepIndex === 0}
                className="px-2.5 py-1 rounded-md bg-blue-700 hover:bg-blue-800 disabled:opacity-40 text-xs font-semibold flex items-center gap-1 cursor-pointer"
              >
                <ChevronLeft className="w-3.5 h-3.5" /> Bước trước
              </button>
              <span className="text-xs font-bold px-2">
                Bước {currentStep.number} / 15
              </span>
              <button
                type="button"
                onClick={goNextStep}
                disabled={currentStepIndex === DEMO_STEPS.length - 1}
                className="px-2.5 py-1 rounded-md bg-white text-blue-700 hover:bg-blue-50 disabled:opacity-40 text-xs font-bold flex items-center gap-1 cursor-pointer"
              >
                Bước tiếp <ChevronRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          {/* KHỐI CHÍNH CỦA BƯỚC HIỆN TẠI */}
          <div className="bg-white rounded-xl border border-slate-200 shadow-2xs overflow-hidden">
            {/* Header của Bước */}
            <div className="p-5 border-b border-slate-200 bg-gradient-to-r from-blue-50/70 via-white to-white">
              <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="px-2.5 py-1 rounded-md bg-blue-600 text-white text-xs font-bold">
                    Bước {currentStep.id}
                  </span>
                  <span className="px-2.5 py-1 rounded-md bg-blue-50 text-blue-700 border border-blue-200 text-xs font-semibold">
                    {currentStep.stageTitle}
                  </span>
                  <span className="px-2.5 py-1 rounded-md bg-slate-100 text-slate-800 text-xs font-semibold flex items-center gap-1.5">
                    Cửa sổ {currentStep.windowNumber} | Vai trò: <strong>{currentStep.canonicalRole}</strong>
                  </span>
                </div>

                <label className="inline-flex items-center gap-1.5 text-xs font-semibold text-blue-700 cursor-pointer select-none">
                  <input
                    type="checkbox"
                    checked={!!completedSteps[currentStep.id]}
                    onChange={(e) =>
                      setCompletedSteps((prev) => ({
                        ...prev,
                        [currentStep.id]: e.target.checked,
                      }))
                    }
                    className="rounded border-slate-300 text-blue-600 focus:ring-blue-500 w-4 h-4"
                  />
                  Đánh dấu đã xong bước này
                </label>
              </div>

              <h2 className="text-lg font-bold text-slate-900">{currentStep.title}</h2>
              <p className="text-sm text-slate-600 mt-0.5">{currentStep.subtitle}</p>

              {/* THẺ BỐI CẢNH DOANH NGHIỆP FPT & THÀNH VIÊN THỰC HIỆN */}
              <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-3">
                <div className="rounded-xl bg-blue-50/70 border border-blue-200 p-3.5 flex items-start gap-3">
                  <div className="w-8 h-8 rounded-lg bg-blue-600 text-white flex items-center justify-center shrink-0 mt-0.5">
                    <UserCheck className="w-4 h-4" />
                  </div>
                  <div className="min-w-0">
                    <div className="text-[11px] font-bold uppercase tracking-wider text-blue-700">
                      Thành viên Đồ án Đang Thực hiện ({currentStep.canonicalRole})
                    </div>
                    <div className="text-sm font-bold text-slate-900 mt-0.5">
                      {currentRoleConfig.fullName} ({currentRoleConfig.organization})
                    </div>
                    <div className="text-xs text-slate-600 mt-0.5 font-mono">
                      Tài khoản: {currentRoleConfig.email} | {currentRoleConfig.windowLabel}
                    </div>
                  </div>
                </div>

                <div className="rounded-xl bg-slate-50 border border-slate-200 p-3.5 flex items-start gap-3">
                  <div className="w-8 h-8 rounded-lg bg-blue-100 text-blue-700 flex items-center justify-center shrink-0 mt-0.5">
                    <Building2 className="w-4 h-4" />
                  </div>
                  <div className="min-w-0">
                    <div className="text-[11px] font-bold uppercase tracking-wider text-slate-500">
                      Ý chính trong Kịch bản (FPT Smart Ads & Đại học FPT)
                    </div>
                    <p className="text-xs text-slate-700 mt-0.5 leading-relaxed">
                      {currentStep.fptBusinessContext}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* SƠ ĐỒ CHUYỂN TRẠNG THÁI TRỰC QUAN (STATE TRANSITION BANNER) */}
            <div className="px-5 py-3 bg-slate-50/70 border-b border-slate-200 grid grid-cols-1 md:grid-cols-3 gap-3 items-center">
              <div className="bg-white rounded-lg border border-slate-200 p-2.5">
                <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                  1. Trạng thái Đầu vào
                </div>
                <div className="text-xs font-bold text-slate-800 mt-0.5">{currentStep.stateBefore}</div>
              </div>

              <div className="bg-blue-50/80 rounded-lg border border-blue-200 p-2.5 flex items-center gap-2">
                <MousePointerClick className="w-4 h-4 text-blue-600 shrink-0" />
                <div className="min-w-0">
                  <div className="text-[10px] font-bold uppercase tracking-wider text-blue-700">
                    2. Nút Chốt Người thuyết trình Tự bấm
                  </div>
                  <div className="text-xs font-bold text-blue-950 truncate" title={currentStep.manualSubmitButton}>
                    {currentStep.manualSubmitButton}
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg border border-blue-200 p-2.5">
                <div className="text-[10px] font-bold uppercase tracking-wider text-blue-700">
                  3. Trạng thái Đích sau khi Bấm
                </div>
                <div className="text-xs font-bold text-blue-900 mt-0.5">{currentStep.stateAfter}</div>
              </div>
            </div>

            <div className="p-5 space-y-5">
              {/* 1. CỤM NÚT ĐIỀU KHIỂN SELENIUM (ACTION TRIGGERS) */}
              <div>
                <div className="flex flex-wrap items-center justify-between gap-2 mb-2.5">
                  <span className="text-xs font-bold uppercase tracking-wider text-blue-700 flex items-center gap-1.5">
                    <Sparkles className="w-3.5 h-3.5" />
                    Nút Điều Khiển Trình Duyệt (Selenium Live Actions)
                  </span>
                  <span className="text-[11px] font-medium text-slate-500">
                    Cơ chế: <strong>{currentStep.algorithmTier}</strong>
                  </span>
                </div>

                <div className="flex flex-wrap gap-2.5">
                  {currentStep.actions.map((act) => {
                    const isRunning = busyAction === act.actionId;
                    let btnStyle =
                      'bg-blue-600 hover:bg-blue-700 text-white border-transparent shadow-xs';
                    if (act.variant === 'typing') {
                      btnStyle =
                        'bg-blue-700 hover:bg-blue-800 text-white border-transparent shadow-xs ring-2 ring-blue-600/20';
                    } else if (act.variant === 'secondary') {
                      btnStyle =
                        'bg-white hover:bg-blue-50 text-blue-700 border-blue-300';
                    } else if (act.variant === 'warning') {
                      btnStyle =
                        'bg-amber-50 hover:bg-amber-100 text-amber-900 border-amber-300';
                    }

                    return (
                      <button
                        key={act.actionId}
                        type="button"
                        disabled={busyAction !== null}
                        onClick={() => runAction(act.actionId, currentStep.id, act.defaultTextKey)}
                        className={`px-4 py-2.5 rounded-lg text-xs font-bold border transition-all flex items-center gap-2 cursor-pointer disabled:opacity-50 ${btnStyle}`}
                      >
                        <Play className="w-3.5 h-3.5 fill-current" />
                        {isRunning ? 'Đang điều khiển & nhả chữ...' : act.label}
                      </button>
                    );
                  })}

                  <a
                    href={resolveFullUrl(currentStep.routeTemplate)}
                    target="_blank"
                    rel="noreferrer"
                    className="px-3 py-2.5 rounded-lg text-xs font-semibold border border-slate-200 text-slate-600 hover:text-blue-700 hover:border-blue-300 flex items-center gap-1.5 ml-auto"
                  >
                    <ExternalLink className="w-3.5 h-3.5" />
                    Mở URL trực tiếp
                  </a>
                </div>
              </div>

              {/* 2. TRỰC QUAN HÓA LUỒNG ĐIỀN DỮ LIỆU TUẦN TỰ (SEQUENTIAL PIPELINE CARDS) */}
              <div className="rounded-xl border border-blue-200 bg-blue-50/30 p-4">
                <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
                  <div className="flex items-center gap-2">
                    <Layers className="w-4 h-4 text-blue-600" />
                    <h3 className="text-xs font-bold uppercase tracking-wider text-blue-900">
                      Thứ tự Thao tác Tuần tự trên Màn hình Chiếu ({currentStep.sequentialPipeline.length} bước nhỏ)
                    </h3>
                  </div>
                  <span className="text-[11px] text-blue-700 font-medium">
                    Mỗi ô được khoanh viền sáng trên trình duyệt khi điền để Hội đồng nhìn rõ
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
                  {currentStep.sequentialPipeline.map((item, idx) => (
                    <div
                      key={idx}
                      className={`rounded-lg border p-3 flex flex-col justify-between ${
                        item.isManualStop
                          ? 'bg-emerald-50/70 border-emerald-300'
                          : 'bg-white border-slate-200'
                      }`}
                    >
                      <div>
                        <div className="flex items-center justify-between gap-2 mb-1.5">
                          <span
                            className={`px-2 py-0.5 rounded text-[11px] font-bold ${
                              item.isManualStop
                                ? 'bg-emerald-600 text-white'
                                : 'bg-blue-600 text-white'
                            }`}
                          >
                            {item.order}
                          </span>
                          <span
                            className={`text-[10px] font-semibold px-2 py-0.5 rounded border ${
                              item.isManualStop
                                ? 'bg-white text-emerald-800 border-emerald-200'
                                : 'bg-blue-50 text-blue-700 border-blue-200'
                            }`}
                          >
                            {item.behaviorBadge}
                          </span>
                        </div>
                        <div className="text-xs font-bold text-slate-900">{item.fieldLabel}</div>
                        <div className="mt-1.5 text-xs text-slate-700 bg-slate-50 rounded p-2 border border-slate-100 leading-relaxed">
                          {item.sampleValue}
                        </div>
                      </div>
                      <div className="mt-2 pt-1.5 border-t border-slate-100 flex items-center justify-between text-[10px] font-mono text-slate-400">
                        <span className="truncate" title={item.domTarget}>
                          Phần tử: {item.domTarget}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* 3. Ô CHỈNH SỬA NỘI DUNG GÕ TỰ ĐỘNG (NẾU BƯỚC NÀY CÓ NHẢ CHỮ TỪNG PHẦN) */}
              {currentStep.actions.some((a) => a.defaultTextKey) && (
                <div className="rounded-xl border border-blue-200 bg-white p-4 space-y-3 shadow-2xs">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold uppercase tracking-wider text-blue-800 flex items-center gap-1.5">
                      <Keyboard className="w-4 h-4 text-blue-600" />
                      Dữ liệu Mẫu Ngắn gọn Sẽ Nhả Từng Cụm Từ (Có thể sửa trực tiếp tại đây)
                    </span>
                    <button
                      type="button"
                      onClick={() => setEditableTexts(DEFAULT_EDITABLE_TEXTS)}
                      className="text-[11px] font-semibold text-blue-700 hover:underline flex items-center gap-1 cursor-pointer"
                    >
                      <RotateCcw className="w-3 h-3" /> Khôi phục mặc định
                    </button>
                  </div>

                  {currentStep.actions
                    .filter((a) => a.defaultTextKey)
                    .map((act) => {
                      const key = act.defaultTextKey!;
                      return (
                        <div key={key} className="space-y-1">
                          <div className="flex items-center justify-between">
                            <label className="text-xs font-bold text-slate-800">
                              Nội dung cho nút: <span className="text-blue-700">{act.label}</span>
                            </label>
                            <button
                              type="button"
                              onClick={() => copyToClipboard(editableTexts[key] || '', key)}
                              className="text-[11px] font-semibold text-blue-600 hover:text-blue-800 flex items-center gap-1 cursor-pointer"
                            >
                              {copiedKey === key ? (
                                <>
                                  <Check className="w-3 h-3" /> Đã chép
                                </>
                              ) : (
                                <>
                                  <Copy className="w-3 h-3" /> Sao chép văn bản
                                </>
                              )}
                            </button>
                          </div>
                          <textarea
                            rows={3}
                            value={editableTexts[key] || ''}
                            onChange={(e) =>
                              setEditableTexts((prev) => ({
                                ...prev,
                                [key]: e.target.value,
                              }))
                            }
                            className="w-full rounded-lg border border-slate-300 bg-slate-50/50 p-2.5 text-xs text-slate-900 focus:bg-white focus:border-blue-600 focus:outline-none leading-relaxed"
                          />
                        </div>
                      );
                    })}
                </div>
              )}

              {/* 4. BẢNG GIẢI THÍCH TRỰC QUAN CÁC TRƯỜNG DỮ LIỆU CHO BAN GIÁM KHẢO */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
                    <Database className="w-3.5 h-3.5 text-blue-600" />
                    Bảng Giải thích Các Trường Dữ liệu tại Bước {currentStep.id}
                  </span>
                  <span className="text-[11px] font-mono text-slate-500">
                    API: {currentStep.apiEndpoint}
                  </span>
                </div>

                <div className="overflow-x-auto rounded-xl border border-slate-200">
                  <table className="w-full text-left border-collapse">
                    <thead>
                      <tr className="bg-slate-50 border-b border-slate-200 text-[11px] font-bold uppercase text-slate-500">
                        <th className="py-2.5 px-3">Trường dữ liệu</th>
                        <th className="py-2.5 px-3">Ý nghĩa thực tế (Giải thích cho Hội đồng)</th>
                        <th className="py-2.5 px-3">Giá trị dữ liệu mẫu</th>
                        <th className="py-2.5 px-3">Cách điền dữ liệu</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-200 text-xs">
                      {currentStep.fields.map((f, idx) => (
                        <tr key={idx} className="hover:bg-slate-50/80">
                          <td className="py-2.5 px-3 font-bold text-slate-900 whitespace-nowrap">
                            <div>{f.fieldName}</div>
                            <code className="text-[10px] font-mono font-normal text-slate-400">
                              {f.selector}
                            </code>
                          </td>
                          <td className="py-2.5 px-3 text-slate-600 leading-relaxed">
                            {f.meaningForJury}
                          </td>
                          <td className="py-2.5 px-3 text-slate-900 font-medium bg-blue-50/20">
                            <div className="flex items-start justify-between gap-2">
                              <span className="leading-relaxed">{f.sampleValue}</span>
                              <button
                                type="button"
                                onClick={() =>
                                  copyToClipboard(f.sampleValue, `${currentStep.id}-f-${idx}`)
                                }
                                className="text-slate-400 hover:text-blue-600 shrink-0 mt-0.5 cursor-pointer"
                                title="Sao chép giá trị"
                              >
                                {copiedKey === `${currentStep.id}-f-${idx}` ? (
                                  <Check className="w-3.5 h-3.5 text-blue-600" />
                                ) : (
                                  <Copy className="w-3.5 h-3.5" />
                                )}
                              </button>
                            </div>
                          </td>
                          <td className="py-2.5 px-3 whitespace-nowrap">
                            <span className="inline-flex items-center px-2 py-0.5 rounded-md text-[11px] font-semibold bg-blue-50 text-blue-700 border border-blue-200">
                              {f.inputMode}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* 5. LỜI DẪN THUYẾT TRÌNH GỢI Ý TRÊN SÂN KHẤU */}
              <div className="rounded-xl bg-slate-50 border border-slate-200 p-4 flex items-start gap-3">
                <Info className="w-4 h-4 text-blue-600 shrink-0 mt-0.5" />
                <div className="text-xs space-y-1">
                  <div className="font-bold text-slate-800 uppercase tracking-wider text-[11px]">
                    Gợi ý trình bày ngắn gọn với Hội đồng
                  </div>
                  <p className="text-slate-600 leading-relaxed">{currentStep.presenterNotes}</p>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};
export default DemoMonitorPage;
