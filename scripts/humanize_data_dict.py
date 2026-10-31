# -*- coding: utf-8 -*-
"""
Practical, clear, non-academic Vietnamese explanations for:
- Project Overview (Reports, Domains, Actors)
- Report 1, Report 2, Report 3 Overview Figures
- Report 4 Class Diagrams (9 domains)
- 65 Business Rules (BR-01 .. BR-65)
- 60 System Messages (MSG01 .. MSG60)
- 38 Screens, 12 Background Tasks, 28 Database Entities
"""

REPORTS_VI = {
    "report1": {
        "description": "Giới thiệu bối cảnh thực tế của các Agency truyền thông, so sánh ưu/nhược điểm của các công cụ hiện có (Hootsuite, Buffer, Jira, Notion) và xác định phạm vi 9 phân hệ của nền tảng BrandHub."
    },
    "report2": {
        "description": "Kế hoạch triển khai dự án: cấu trúc phân rã công việc (WBS), quy trình làm việc Agile-Scrum theo từng Sprint 2 tuần, 5 bước kiểm thử chất lượng phần mềm và cách quản lý mã nguồn trên GitHub."
    },
    "report3": {
        "description": "Tài liệu đặc tả yêu cầu phần mềm (SRS): quy định 6 vai trò người dùng chuẩn, 141 chức năng chi tiết (UC-001 đến UC-141), 150 sơ đồ và giao diện màn hình, 65 quy tắc nghiệp vụ và 60 mã thông báo."
    },
    "report4": {
        "description": "Tài liệu thiết kế phần mềm (SDD): gồm 9 sơ đồ lớp (Class Diagram) theo từng phân hệ và 141 sơ đồ tuần tự (Sequence Diagram) mô tả luồng xử lý chi tiết của từng chức năng."
    },
}

DOMAINS_VI = {
    "3.2": "Đăng ký, đăng nhập bằng Email hoặc Google, quên/đổi mật khẩu, xác thực mã OTP qua email, bảo mật 2 lớp (2FA), đăng xuất và xóa tài khoản.",
    "3.3": "Xem và cập nhật thông tin cá nhân của người dùng; quản lý hồ sơ thương hiệu của Client để dùng chung cho nhiều dự án mà không cần nhập lại.",
    "3.4": "Tạo và quản lý công ty (Agency), mời thành viên qua email, tạo không gian làm việc (Workspace) cho từng nhãn hàng, gán Manager phụ trách, cài đặt múi giờ và lưu mẫu Workspace.",
    "3.5": "Thiết lập gói dịch vụ truyền thông (Media Package), trao đổi và chốt gói với Client, lập kế hoạch chiến dịch (Media Campaign), tự động tạo danh sách đầu việc và xử lý yêu cầu phát sinh.",
    "3.6": "Quản lý công việc theo 4 chế độ (Danh sách, Lịch, Gantt, Kanban), duyệt bài 3 cấp (Creator -> Manager -> Client), soạn thảo văn bản, kho tư liệu kết nối Google Drive, đóng dấu ảnh, bộ Hashtag, khảo sát, mẫu email và kiểm tra từ ngữ vi phạm.",
    "3.7": "Gợi ý chủ đề và hashtag đang thịnh hành, lưu tài liệu hướng dẫn thương hiệu (Brand Guideline) để AI viết bài đúng giọng điệu, tạo hình ảnh/video và người mẫu đại diện ảo bằng AI, quản lý và gợi ý đối tác truyền thông (KOL/KOC, báo chí).",
    "3.8": "Kết nối tài khoản mạng xã hội, xem trước giao diện bài đăng, hẹn giờ đăng tự động và theo dõi chỉ số tương tác trên 4 nền tảng: Facebook, Instagram, TikTok và Threads.",
    "3.9": "Nâng cấp gói dịch vụ của Agency, thanh toán tự động bằng mã VietQR (qua cổng SePay / PayOS), xem lịch sử hóa đơn, mua thêm và phân bổ hạn mức điểm AI Credit cho từng dự án.",
    "3.10": "Cổng quản trị dành cho Admin: gửi thông báo toàn hệ thống, xem thống kê hoạt động, theo dõi tình trạng máy chủ, kiểm duyệt bài viết bị báo cáo, quản lý tài khoản người dùng, cài đặt bảng giá AI Credit và xuất báo cáo doanh thu PDF.",
}

ACTORS_VI = {
    "Guest": "Người dùng chưa đăng nhập: có thể xem trang giới thiệu, đăng ký tài khoản mới, đăng nhập bằng Email hoặc Google, nhập mã xác nhận OTP và khôi phục mật khẩu khi quên.",
    "Owner": "Chủ sở hữu Agency: người tạo và quản lý công ty, mời nhân sự vào Agency, tạo các Workspace cho từng dự án khách hàng, thiết lập gói dịch vụ mẫu, nâng cấp gói cước, mua điểm AI Credit qua SePay và cấp hạn mức sử dụng cho từng Workspace.",
    "Manager": "Quản lý dự án trong Workspace: người trực tiếp làm việc với Client để thỏa thuận gói truyền thông và kế hoạch chiến dịch, giao việc cho Creator, kiểm duyệt chất lượng bài viết ở bước trung gian, tải tài liệu thương hiệu cho AI và lên lịch đăng bài.",
    "Creator": "Nhân sự sáng tạo nội dung trong Workspace: người nhận đầu việc, viết bài, sử dụng công cụ AI để tạo caption/hình ảnh/video/người mẫu ảo, tải tư liệu, gắn logo đóng dấu bản quyền, kiểm tra từ ngữ vi phạm và gửi bài chờ duyệt.",
    "Client": "Khách hàng (đại diện nhãn hàng) được mời vào Workspace: cập nhật hồ sơ thương hiệu của mình, trao đổi và phê duyệt gói dịch vụ cùng kế hoạch chiến dịch, gửi yêu cầu nội dung phát sinh, kết nối Google Drive / mạng xã hội, duyệt bài bước cuối và xem kết quả tương tác.",
    "Admin": "Quản trị viên toàn hệ thống: theo dõi số liệu vận hành và tình trạng máy chủ, gửi thông báo chung, xử lý các nội dung bị cảnh báo vi phạm, quản lý trạng thái tài khoản người dùng, điều chỉnh bảng giá AI Credit và xuất báo cáo doanh thu.",
}

REPORT1_FIGURES_VI = {
    "r1-fig-1": {
        "viSummary": "Giao diện quản lý đăng bài nhiều cột của Hootsuite. Công cụ này mạnh về hẹn giờ đăng bài nhưng thiếu quy trình thỏa thuận gói dịch vụ và duyệt bài nhiều bước giữa Agency với Client.",
        "components": [
            {
                "name": "Bảng điều khiển đa cột (Streams)",
                "type": "Giao diện tham khảo",
                "description": "Hiển thị danh sách bài đăng và bình luận từ nhiều mạng xã hội trên cùng một màn hình."
            },
            {
                "name": "Hạn chế đối với mô hình Agency",
                "type": "Điểm rút kinh nghiệm",
                "description": "Chưa hỗ trợ tách biệt không gian làm việc theo từng khách hàng (Workspace) và chưa có bước Client phê duyệt chiến dịch."
            }
        ]
    },
    "r1-fig-2": {
        "viSummary": "Giao diện lịch đăng bài của Buffer. Thiết kế gọn nhẹ, dễ dùng cho cá nhân nhưng không đủ tính năng phân quyền đội nhóm (Owner, Manager, Creator, Client) và quản lý tiến độ sản xuất nội dung.",
        "components": [
            {
                "name": "Lịch xếp hàng bài đăng (Publishing Queue)",
                "type": "Giao diện tham khảo",
                "description": "Cho phép lên lịch đăng bài đơn giản theo khung giờ cố định trong tuần."
            },
            {
                "name": "Hạn chế đối với mô hình Agency",
                "type": "Điểm rút kinh nghiệm",
                "description": "Thiếu công cụ quản lý đầu việc, kho tư liệu chung và công cụ AI viết bài theo tài liệu thương hiệu riêng."
            }
        ]
    },
    "r1-fig-3": {
        "viSummary": "Giao diện bảng công việc Kanban của Jira. BrandHub học hỏi cách quản lý danh sách đầu việc (Backlog) và bộ lọc rõ ràng của Jira, đồng thời tích hợp thêm trình soạn thảo nội dung, AI và đăng bài trực tiếp.",
        "components": [
            {
                "name": "Bảng kéo thả trạng thái (Kanban & Backlog)",
                "type": "Điểm học hỏi",
                "description": "Giúp theo dõi trực quan công việc nào đang chờ làm, đang thực hiện hay đang chờ duyệt."
            },
            {
                "name": "Điểm cải tiến trên BrandHub",
                "type": "Tích hợp chuyên biệt",
                "description": "Bổ sung luồng duyệt bài 3 cấp (Creator -> Manager -> Client) và xuất bản thẳng lên 4 mạng xã hội ngay khi duyệt xong."
            }
        ]
    },
    "r1-fig-4": {
        "viSummary": "Giao diện tài liệu của Notion thường được các Agency dùng để ghi chú kịch bản thủ công. BrandHub khắc phục việc dữ liệu rời rạc bằng cách chuyển thẳng kế hoạch chiến dịch đã duyệt thành các đầu việc (Task) có thể theo dõi tiến độ.",
        "components": [
            {
                "name": "Trang soạn thảo kế hoạch và ghi chú",
                "type": "Giao diện tham khảo",
                "description": "Linh hoạt khi viết tài liệu nhưng phải tạo lại công việc và copy bài sang công cụ khác bằng tay."
            },
            {
                "name": "Điểm cải tiến trên BrandHub",
                "type": "Tự động hóa luồng việc",
                "description": "Khi Client bấm duyệt Kế hoạch Chiến dịch, hệ thống tự động tạo luôn danh sách Task tương ứng trong Workspace."
            }
        ]
    },
    "r1-fig-5": {
        "viSummary": "Sơ đồ tổng quan phạm vi của hệ thống BrandHub: kết nối xuyên suốt từ quản lý Agency & Workspace, lập chiến dịch, sản xuất nội dung có AI hỗ trợ, duyệt bài 3 cấp đến đăng tự động lên 4 mạng xã hội (Facebook, Instagram, TikTok, Threads).",
        "components": [
            {
                "name": "Khối Quản trị Tổ chức & Chiến dịch",
                "type": "Phân hệ 3.2 – 3.5",
                "description": "Quản lý tài khoản, hồ sơ Client, mô hình Agency – Workspace, đàm phán gói dịch vụ và lập kế hoạch chiến dịch."
            },
            {
                "name": "Khối Sản xuất Nội dung & Công cụ AI",
                "type": "Phân hệ 3.6 – 3.7",
                "description": "Quản lý đầu việc, duyệt bài 3 cấp, kho tư liệu, bắt nhịp xu hướng và tạo văn bản/hình ảnh/video bằng AI."
            },
            {
                "name": "Khối Xuất bản Đa kênh, Thanh toán & Quản trị",
                "type": "Phân hệ 3.8 – 3.10",
                "description": "Hẹn giờ đăng bài lên Facebook, Instagram, TikTok, Threads; thanh toán gói cước qua SePay (VietQR) và quản trị hệ thống."
            }
        ]
    }
}

REPORT2_FIGURES_VI = {
    "r2-fig-1": {
        "viSummary": "Sơ đồ phân rã công việc (WBS) chia nhỏ toàn bộ dự án thành các giai đoạn (Khởi động, Phân tích yêu cầu, Thiết kế, Lập trình, Kiểm thử) và 9 phân hệ chức năng gồm 141 FR.",
        "components": [
            {
                "name": "Phân chia theo giai đoạn và phân hệ",
                "type": "Cấu trúc WBS",
                "description": "Giúp nhóm 5 thành viên phân bổ rõ trách nhiệm làm tài liệu, thiết kế giao diện, viết code và kiểm thử cho từng phần."
            }
        ]
    },
    "r2-fig-2": {
        "viSummary": "Quy trình phát triển phần mềm theo mô hình Agile-Scrum lặp lại qua từng Sprint ngắn (2 tuần/Sprint), giúp nhóm liên tục hoàn thiện tính năng và nhận góp ý sớm từ giảng viên hướng dẫn.",
        "components": [
            {
                "name": "Chu kỳ Sprint 2 tuần",
                "type": "Quy trình làm việc",
                "description": "Gồm lập kế hoạch đầu Sprint, họp ngắn hàng ngày, lập trình – kiểm thử và nghiệm thu kết quả cuối Sprint."
            }
        ]
    },
    "r2-fig-3": {
        "viSummary": "Mô hình phối hợp song song giữa nhóm phát triển hệ thống chính (Web/Backend quản lý công việc, đăng bài) và nhóm phát triển dịch vụ AI (gợi ý xu hướng, tạo nội dung và hình ảnh).",
        "components": [
            {
                "name": "Nhánh phát triển Nền tảng cốt lõi (Core Platform)",
                "type": "Backend & Frontend",
                "description": "Xây dựng giao diện người dùng, quản lý phân quyền, chiến dịch, luồng duyệt bài và kết nối mạng xã hội."
            },
            {
                "name": "Nhánh phát triển Dịch vụ AI (AI Track)",
                "type": "AI & Dữ liệu",
                "description": "Xây dựng bộ thu thập xu hướng, kho tài liệu thương hiệu và kết nối các mô hình tạo văn bản, ảnh, video."
            }
        ]
    },
    "r2-fig-4": {
        "viSummary": "Quy trình kiểm tra chéo trong nhóm: mỗi tính năng sau khi code xong đều phải qua bước đồng đội đọc duyệt code (Peer Review) và kiểm tra chạy thử trước khi ghép vào nhánh chính.",
        "components": [
            {
                "name": "Duyệt code chéo & Họp rà soát tiến độ",
                "type": "Phối hợp nhóm",
                "description": "Đảm bảo code thống nhất quy chuẩn, phát hiện lỗi sớm và bám sát đúng đặc tả trong báo cáo SRS."
            }
        ]
    },
    "r2-fig-5": {
        "viSummary": "Quy trình kiểm soát chất lượng 5 bước: Kiểm tra quy chuẩn code -> Kiểm thử đơn vị (Unit Test) -> Kiểm thử tích hợp API -> Kiểm thử toàn hệ thống (System Test) -> Nghiệm thu thực tế (UAT).",
        "components": [
            {
                "name": "5 chốt chặn kiểm thử chất lượng",
                "type": "Đảm bảo chất lượng (QA)",
                "description": "Mỗi chức năng đều được kiểm tra cả trường hợp nhập đúng và các trường hợp nhập sai/thiếu dữ liệu trước khi bàn giao."
            }
        ]
    },
    "r2-fig-6": {
        "viSummary": "Cấu trúc tổ chức các kho mã nguồn (Repositories) trên GitHub và thư mục tài liệu báo cáo của dự án, tách biệt rõ từng dịch vụ để dễ bảo trì và triển khai.",
        "components": [
            {
                "name": "Hệ thống kho mã nguồn (GitHub Repositories)",
                "type": "Quản lý cấu hình",
                "description": "Gồm cổng điều phối API Gateway, dịch vụ nghiệp vụ chính, dịch vụ AI, dịch vụ đăng bài, giao diện Web/Mobile và bộ báo cáo."
            }
        ]
    },
    "r2-fig-7": {
        "viSummary": "Quy tắc phân nhánh làm việc trên Git (`main`, `develop`, `feature/*`, `release/*`, `hotfix/*`) giúp các thành viên code độc lập từng tính năng mà không làm lỗi code của nhau.",
        "components": [
            {
                "name": "Mô hình phân nhánh Git (Git Flow)",
                "type": "Quản lý mã nguồn",
                "description": "Mỗi tính năng mới được làm trên nhánh `feature/*` riêng, sau khi kiểm tra đạt yêu cầu mới gộp vào `develop` và `main`."
            }
        ]
    }
}

REPORT3_OVERVIEW_VI = {
    "r3-fig-1": {
        "viSummary": "Sơ đồ ngữ cảnh tổng thể (System Context Diagram) cho thấy 6 nhóm người dùng (Guest, Owner, Manager, Creator, Client, Admin) tương tác với BrandHub như thế nào, và cách hệ thống kết nối với các dịch vụ bên ngoài (AI, 4 mạng xã hội, Google Drive, cổng thanh toán SePay).",
        "components": [
            {
                "name": "Hệ thống trung tâm BrandHub",
                "type": "Nền tảng chính",
                "description": "Xử lý toàn bộ nghiệp vụ quản lý Agency, Workspace, chiến dịch, duyệt bài, gọi AI và tự động đăng bài."
            },
            {
                "name": "6 Vai trò người dùng (Actors)",
                "type": "Người sử dụng",
                "description": "Guest, Owner, Manager, Creator, Client và Admin truy cập hệ thống trên trình duyệt web hoặc ứng dụng di động."
            },
            {
                "name": "Các dịch vụ AI bên ngoài",
                "type": "Tích hợp AI",
                "description": "Hỗ trợ tạo văn bản bài viết, sinh hình ảnh quảng cáo, người mẫu đại diện ảo và video ngắn."
            },
            {
                "name": "4 Nền tảng Mạng xã hội",
                "type": "Tích hợp Xuất bản",
                "description": "Kết nối chính thức với Facebook, Instagram, TikTok và Threads để đăng bài và lấy số liệu tương tác."
            },
            {
                "name": "Google Drive & Cổng thanh toán SePay (VietQR)",
                "type": "Lưu trữ & Thanh toán",
                "description": "Google Drive giúp đồng bộ kho ảnh/video của khách hàng; SePay giúp tạo mã QR và xác nhận chuyển khoản tự động."
            }
        ]
    },
    "r3-fig-2": {
        "viSummary": "Sơ đồ tổng hợp toàn bộ 141 Use Cases (UC-001 đến UC-141) chia theo 9 phân hệ chức năng và phân quyền rõ cho từng vai trò người dùng. Bạn có thể bấm vào các nút bên dưới ảnh để xem cận cảnh từng phân hệ.",
        "components": [
            {
                "name": "Xác thực & Hồ sơ (UC-001 – UC-013)",
                "type": "Phân hệ 3.2 & 3.3",
                "description": "Đăng ký, đăng nhập, xác thực OTP/2FA, quản lý hồ sơ cá nhân và hồ sơ thương hiệu của Client."
            },
            {
                "name": "Quản lý Agency & Workspace (UC-014 – UC-039)",
                "type": "Phân hệ 3.4",
                "description": "Tạo công ty, mời nhân sự, lập không gian làm việc cho từng nhãn hàng, gán Manager và cài đặt múi giờ."
            },
            {
                "name": "Gói dịch vụ & Chiến dịch truyền thông (UC-040 – UC-052)",
                "type": "Phân hệ 3.5",
                "description": "Thỏa thuận gói dịch vụ, lập kế hoạch chiến dịch, tự động tạo danh sách đầu việc và nhận yêu cầu phát sinh."
            },
            {
                "name": "Sản xuất nội dung, AI, Đăng bài & Quản trị (UC-053 – UC-141)",
                "type": "Phân hệ 3.6 – 3.10",
                "description": "Giao việc, duyệt bài 3 cấp, kho tư liệu, công cụ sáng tạo AI, đăng bài 4 mạng xã hội, thanh toán SePay và cổng Admin."
            }
        ]
    },
    "r3-fig-3": {
        "viSummary": "Sơ đồ luồng di chuyển màn hình dành cho Guest (người dùng chưa đăng nhập): từ Trang chủ -> Đăng ký / Đăng nhập -> Nhập mã xác nhận OTP -> Khôi phục mật khẩu.",
        "components": [
            {
                "name": "Trang giới thiệu (Landing Page)",
                "type": "Màn hình mở đầu",
                "description": "Giới thiệu tính năng, bảng giá các gói dịch vụ và nút chuyển sang Đăng ký hoặc Đăng nhập."
            },
            {
                "name": "Màn hình Đăng ký & Đăng nhập (/register, /login)",
                "type": "Xác thực tài khoản",
                "description": "Cho phép tạo tài khoản mới hoặc đăng nhập bằng mật khẩu / tài khoản Google."
            },
            {
                "name": "Màn hình Xác nhận OTP & Quên mật khẩu",
                "type": "Xác minh bảo mật",
                "description": "Nhập mã 6 số gửi qua email để kích hoạt tài khoản hoặc đặt lại mật khẩu mới."
            }
        ]
    },
    "r3-fig-4": {
        "viSummary": "Sơ đồ luồng màn hình dành cho Client (Khách hàng): xem và cập nhật hồ sơ thương hiệu, đàm phán & phê duyệt gói dịch vụ/chiến dịch, gửi yêu cầu phát sinh, kết nối tài khoản mạng xã hội và duyệt bài trước khi đăng.",
        "components": [
            {
                "name": "Hồ sơ thương hiệu (Client Profile)",
                "type": "Thông tin nhãn hàng",
                "description": "Quản lý tên thương hiệu, logo, ngành hàng và thông tin liên hệ dùng chung cho mọi dự án."
            },
            {
                "name": "Đàm phán & Duyệt Gói dịch vụ / Chiến dịch",
                "type": "Thỏa thuận kế hoạch",
                "description": "Xem đề xuất từ Agency, gửi phản hồi chỉnh sửa và bấm phê duyệt phương án thống nhất."
            },
            {
                "name": "Duyệt bài bước cuối & Xem hiệu quả bài đăng",
                "type": "Nghiệm thu kết quả",
                "description": "Xem trước bài viết hoàn chỉnh để duyệt đăng hoặc yêu cầu sửa lại, đồng thời theo dõi lượt tương tác sau khi đăng."
            }
        ]
    },
    "r3-fig-5": {
        "viSummary": "Sơ đồ luồng màn hình dành cho Admin: theo dõi số liệu toàn hệ thống, giám sát sức khỏe máy chủ, kiểm duyệt nội dung bị báo cáo, quản lý tài khoản người dùng, chỉnh bảng giá AI Credit và xuất báo cáo doanh thu.",
        "components": [
            {
                "name": "Bảng thống kê & Giám sát hệ thống",
                "type": "Giám sát vận hành",
                "description": "Xem tổng số người dùng, số bài đăng, doanh thu và tình trạng hoạt động (CPU, RAM, kết nối) của các máy chủ."
            },
            {
                "name": "Kiểm duyệt nội dung & Quản lý người dùng",
                "type": "An toàn nền tảng",
                "description": "Xem xét các bài viết bị cảnh báo vi phạm, gửi thông báo toàn hệ thống và quản lý trạng thái/mức phạt tài khoản."
            },
            {
                "name": "Cấu hình bảng giá AI Credit & Báo cáo doanh thu",
                "type": "Cấu hình & Tài chính",
                "description": "Cập nhật số điểm trừ cho từng tính năng AI, nhập bảng giá qua file CSV và xuất báo cáo doanh thu ra PDF."
            }
        ]
    },
    "r3-fig-6": {
        "viSummary": "Sơ đồ luồng màn hình dành cho Owner (Chủ sở hữu Agency): tạo công ty, mời nhân sự, mở các Workspace theo dự án và gán Manager, quản lý gói cước, thanh toán qua SePay và phân bổ hạn mức AI Credit.",
        "components": [
            {
                "name": "Quản lý Agency & Nhân sự công ty",
                "type": "Cấp công ty (Agency)",
                "description": "Tạo Agency mới, xem bảng thống kê toàn công ty, gửi lời mời nhân viên qua email và quản lý danh sách thành viên."
            },
            {
                "name": "Khởi tạo Workspace & Thư viện mẫu (Template)",
                "type": "Cấp dự án (Workspace)",
                "description": "Tạo không gian làm việc cho khách hàng, chỉ định Manager phụ trách và lưu cấu hình mẫu để dùng lại."
            },
            {
                "name": "Gói đăng ký, Thanh toán SePay & Hạn mức AI Credit",
                "type": "Quản lý chi phí",
                "description": "Nâng cấp gói Pro/Enterprise, quét mã VietQR thanh toán, mua thêm AI Credit và chia hạn mức cho từng Workspace."
            }
        ]
    },
    "r3-fig-7": {
        "viSummary": "Sơ đồ luồng màn hình dành cho Manager (Quản lý dự án): điều hành công việc trong Workspace, lập kế hoạch chiến dịch, chi tiết hóa đầu việc và giao cho Creator, duyệt chất lượng nội dung và lên lịch đăng bài.",
        "components": [
            {
                "name": "Lập kế hoạch Chiến dịch & Xử lý yêu cầu khách hàng",
                "type": "Lập kế hoạch",
                "description": "Chốt gói dịch vụ, lên danh sách bài viết cho chiến dịch và tiếp nhận các yêu cầu phát sinh từ Client."
            },
            {
                "name": "Phân công công việc & Quản lý tiến độ",
                "type": "Điều phối sản xuất",
                "description": "Điền yêu cầu chi tiết cho từng Task, giao việc cho Creator và theo dõi trên bảng Danh sách / Lịch / Gantt / Kanban."
            },
            {
                "name": "Kiểm duyệt bài viết & Lên lịch xuất bản",
                "type": "Duyệt & Đăng bài",
                "description": "Duyệt nội dung do Creator gửi lên, chuyển tiếp cho Client duyệt và hẹn giờ đăng lên 4 mạng xã hội."
            }
        ]
    },
    "r3-fig-8": {
        "viSummary": "Sơ đồ luồng màn hình dành cho Creator (Người sáng tạo nội dung): xem các đầu việc được giao, viết bài kết hợp bộ đổi kiểu chữ Unicode, dùng AI tạo caption/ảnh/video/người mẫu ảo, quản lý kho tư liệu và gửi bài duyệt.",
        "components": [
            {
                "name": "Bảng công việc & Trình soạn thảo nội dung",
                "type": "Soạn thảo bài đăng",
                "description": "Nhận Task được giao, viết bài có hỗ trợ định dạng chữ nổi bật và tự động lưu lịch sử các lần chỉnh sửa."
            },
            {
                "name": "Bộ công cụ sáng tạo AI (AI Studio)",
                "type": "Hỗ trợ sáng tạo",
                "description": "Xem xu hướng đang hot, tạo nhanh lời bình (caption), hình ảnh sản phẩm, video ngắn và đại sứ ảo bằng AI."
            },
            {
                "name": "Kho tư liệu, Đóng dấu ảnh & Gửi duyệt",
                "type": "Hoàn thiện ấn phẩm",
                "description": "Tải ảnh/video lên kho, gắn logo đóng dấu bản quyền, chèn bộ hashtag, kiểm tra từ ngữ vi phạm và bấm gửi duyệt."
            }
        ]
    },
    "r3-fig-9": {
        "viSummary": "Sơ đồ quan hệ thực thể cơ sở dữ liệu (ERD) gồm 28 bảng chính, thể hiện cách lưu trữ và liên kết dữ liệu giữa Người dùng, Agency, Workspace, Chiến dịch, Công việc (Task), Kho tư liệu, Bài đăng và Hóa đơn thanh toán.",
        "components": [
            {
                "name": "Nhóm bảng Người dùng, Agency & Workspace",
                "type": "Tổ chức & Phân quyền",
                "description": "Gồm User, ClientProfile, Agency, AgencyMember, AgencyInvitation, Workspace, WorkspaceMember, WorkspaceTemplate."
            },
            {
                "name": "Nhóm bảng Chiến dịch & Quy trình công việc",
                "type": "Kế hoạch & Sản xuất",
                "description": "Gồm MediaPackage, MediaCampaign, ContentRequest, Task, TaskApproval, TaskComment, ContentVersion."
            },
            {
                "name": "Nhóm bảng Tư liệu, AI, Mạng xã hội & Thanh toán",
                "type": "Tư liệu, Xuất bản & Chi phí",
                "description": "Gồm MaterialRepository, CustomerDriveConnection, HashtagCollection, Survey, MailTemplate, BrandKnowledgeDocument, ThirdPartyCollaborator, SocialAccount, Post, SubscriptionOrder, AICreditLedger, SystemNotification."
            }
        ]
    }
}

CLASS_DIAGRAMS_VI = {
    "cd-3.2": {
        "viSummary": "Sơ đồ lớp (Class Diagram) của phân hệ 3.2 (Xác thực & Phân quyền): mô tả cấu trúc dữ liệu người dùng, phiên đăng nhập, liên kết Google OAuth và các lớp xử lý đăng ký, đăng nhập, mã xác nhận OTP và bảo mật 2 lớp.",
        "roleMap": {
            "User": "Bảng lưu thông tin tài khoản người dùng (họ tên, email, mật khẩu mã hóa, trạng thái tài khoản, cài đặt 2FA).",
            "AuthenticatedUser": "Đối tượng lưu thông tin người dùng đang đăng nhập trong phiên làm việc hiện tại.",
            "UserSystemRole": "Bảng lưu vai trò cấp hệ thống của người dùng (USER hoặc ADMIN).",
            "UserRefreshToken": "Bảng quản lý danh sách phiên đăng nhập (Refresh Token) để duy trì đăng nhập và thu hồi khi đăng xuất/đổi mật khẩu.",
            "UserOAuthProvider": "Bảng lưu thông tin liên kết tài khoản Google OAuth 2.0 với tài khoản BrandHub.",
            "AuditLog": "Bảng ghi nhận nhật ký các thao tác bảo mật quan trọng (đăng nhập, đổi mật khẩu, khóa/xóa tài khoản).",
            "AuthController": "Tiếp nhận các yêu cầu API về đăng ký, đăng nhập, xác thực OTP, quên/đổi mật khẩu và đăng xuất.",
            "GoogleOAuthController": "Tiếp nhận yêu cầu đăng nhập nhanh bằng tài khoản Google.",
            "AuthService": "Xử lý logic kiểm tra thông tin đăng ký/đăng nhập, tạo mã OTP, kiểm tra bảo mật 2 lớp và cấp phiên làm việc.",
            "GoogleOAuthService": "Xử lý việc kiểm tra thông tin tài khoản Google và tự động liên kết hoặc tạo mới tài khoản.",
            "OAuthService": "Dịch vụ dùng chung hỗ trợ kết nối và xác thực theo chuẩn OAuth 2.0.",
            "UserRepository": "Truy vấn và cập nhật dữ liệu bảng người dùng (User) trong cơ sở dữ liệu.",
            "UserSystemRoleRepository": "Truy vấn thông tin quyền hạn hệ thống của tài khoản.",
            "UserRefreshTokenRepository": "Lưu và xóa các phiên đăng nhập (Refresh Token) trong cơ sở dữ liệu.",
            "UserOAuthProviderRepository": "Truy vấn thông tin liên kết tài khoản Google của người dùng.",
            "AuditLogRepository": "Lưu nhật ký hoạt động bảo mật vào cơ sở dữ liệu."
        }
    },
    "cd-3.3": {
        "viSummary": "Sơ đồ lớp (Class Diagram) của phân hệ 3.3 (Hồ sơ Người dùng & Khách hàng): mô tả cấu trúc lưu trữ hồ sơ cá nhân và hồ sơ thương hiệu của Client có thể tái sử dụng cho nhiều dự án.",
        "roleMap": {
            "User": "Lưu thông tin cá nhân của người dùng (ảnh đại diện, họ tên, số điện thoại, ngôn ngữ, kỹ năng).",
            "ClientProfile": "Lưu thông tin thương hiệu của Client (tên nhãn hàng, logo, ngành nghề, website, mã số thuế, thông tin liên hệ).",
            "ProfileController": "Tiếp nhận yêu cầu xem và cập nhật hồ sơ cá nhân của người dùng.",
            "ClientProfileController": "Tiếp nhận yêu cầu xem và cập nhật hồ sơ thương hiệu của Client.",
            "ProfileService": "Kiểm tra dữ liệu cập nhật hồ sơ cá nhân, tải ảnh đại diện và giữ cố định email đăng nhập.",
            "ClientProfileService": "Quản lý thông tin thương hiệu của Client và đồng bộ hiển thị tới các Workspace liên quan.",
            "UserRepository": "Truy vấn và lưu thông tin hồ sơ cá nhân vào cơ sở dữ liệu.",
            "ClientProfileRepository": "Truy vấn và lưu hồ sơ thương hiệu của Client vào cơ sở dữ liệu."
        }
    },
    "cd-3.4": {
        "viSummary": "Sơ đồ lớp (Class Diagram) của phân hệ 3.4 (Agency & Workspace): mô tả mối quan hệ giữa Công ty (Agency), Thành viên, Lời mời gia nhập, Không gian làm việc (Workspace) và Mẫu cấu hình (Workspace Template).",
        "roleMap": {
            "Agency": "Lưu thông tin công ty truyền thông do Owner sở hữu (tên, logo, gói dịch vụ đang dùng, số dư AI Credit).",
            "AgencyMember": "Lưu danh sách nhân sự thuộc Agency và hạn mức sử dụng AI Credit của từng người.",
            "AgencyInvitation": "Lưu thông tin lời mời tham gia Agency qua email kèm thời hạn hiệu lực 3 ngày.",
            "Workspace": "Lưu thông tin không gian làm việc của từng dự án/khách hàng, múi giờ chuẩn và hạn mức AI Credit riêng.",
            "WorkspaceMember": "Lưu danh sách thành viên trong Workspace cùng vai trò cụ thể (Manager, Creator, Client).",
            "WorkspaceTemplate": "Lưu các mẫu cấu hình Workspace để Owner áp dụng nhanh khi mở dự án mới.",
            "AgencyController": "Tiếp nhận các yêu cầu tạo, xem, sửa, xóa mềm Agency và quản lý lời mời thành viên.",
            "WorkspaceController": "Tiếp nhận các yêu cầu tạo, xem, cập nhật Workspace, quản lý thành viên và mẫu Template.",
            "AgencyService": "Xử lý nghiệp vụ quản lý công ty, gửi/chấp nhận/từ chối lời mời và bảo toàn dữ liệu khi xóa thành viên.",
            "WorkspaceService": "Xử lý nghiệp vụ tạo Workspace (bắt buộc có Manager), cài đặt múi giờ và phân quyền thành viên.",
            "WorkspaceTemplateService": "Xử lý việc lưu, xem, áp dụng và xóa các mẫu cấu hình Workspace."
        }
    },
    "cd-3.5": {
        "viSummary": "Sơ đồ lớp (Class Diagram) của phân hệ 3.5 (Gói Truyền thông & Chiến dịch): mô tả cấu trúc của Gói dịch vụ (Media Package), Kế hoạch Chiến dịch (Media Campaign), các hạng mục công việc dự kiến và Yêu cầu phát sinh (Content Request).",
        "roleMap": {
            "MediaPackage": "Lưu thông tin gói dịch vụ truyền thông (thời hạn, chi phí, số lượng bài đăng cam kết và trạng thái đàm phán).",
            "MediaCampaign": "Lưu kế hoạch triển khai chiến dịch chi tiết dựa trên gói dịch vụ đã chốt, kèm lịch sử các phiên bản chỉnh sửa.",
            "ContentRequest": "Lưu các yêu cầu làm nội dung bổ sung/phát sinh do Client hoặc Manager gửi lên.",
            "MediaPackageController": "Tiếp nhận yêu cầu tạo gói dịch vụ, xem gói mẫu, gửi đề xuất chỉnh sửa và phê duyệt gói.",
            "MediaCampaignController": "Tiếp nhận yêu cầu lập chiến dịch, cập nhật kế hoạch, phê duyệt kích hoạt và đóng chiến dịch.",
            "ContentRequestController": "Tiếp nhận yêu cầu tạo mới, theo dõi trạng thái, chỉnh sửa hoặc hủy yêu cầu nội dung phát sinh.",
            "MediaPackageService": "Xử lý luồng đàm phán qua lại và xác nhận đồng thuận gói dịch vụ giữa Agency với Client.",
            "MediaCampaignService": "Quản lý kế hoạch chiến dịch và tự động chuyển các hạng mục đã duyệt sang danh sách Task Backlog.",
            "ContentRequestService": "Quản lý vòng đời yêu cầu phát sinh và tự động tạo Task mới khi yêu cầu được chấp nhận."
        }
    },
    "cd-3.6": {
        "viSummary": "Sơ đồ lớp (Class Diagram) của phân hệ 3.6 (Nội dung & Quy trình làm việc): mô tả cấu trúc Đầu việc (Task), Chuỗi duyệt 3 cấp, Lịch sử phiên bản bài viết, Kho tư liệu, Kết nối Google Drive, Bộ Hashtag, Khảo sát, Mẫu Email và Nhắn tin trực tuyến.",
        "roleMap": {
            "Task": "Lưu thông tin chi tiết của từng đầu việc sản xuất nội dung (tiêu đề, mô tả, nền tảng, hạn chót, người làm, trạng thái).",
            "TaskApproval": "Lưu lịch sử từng bước phê duyệt hoặc trả lại bài viết theo chuỗi Creator -> Manager -> Client.",
            "TaskComment": "Lưu các bình luận trao đổi, tệp đính kèm và gắn thẻ thành viên ngay trên đầu việc.",
            "ContentVersion": "Lưu lịch sử các phiên bản nội dung bài viết để xem lại hoặc khôi phục khi cần.",
            "MaterialRepository": "Lưu thông tin ảnh, video và tài liệu trong kho tư liệu của Workspace (phân loại Ảnh gốc RAW, Đã chỉnh sửa, Tài liệu mẫu).",
            "CustomerDriveConnection": "Lưu thông tin kết nối tài khoản Google Drive của khách hàng để đồng bộ tư liệu.",
            "HashtagCollection": "Lưu các bộ sưu tập thẻ Hashtag phân loại theo chiến dịch hoặc sự kiện.",
            "Survey": "Lưu biểu mẫu khảo sát ý kiến và kết quả thống kê phản hồi của người tham gia.",
            "MailTemplate": "Lưu các mẫu email thông báo có gắn biến tự động và lịch sử gửi email.",
            "TaskController": "Điều phối các thao tác cập nhật đầu việc, giao việc, lọc công việc theo 4 chế độ xem và duyệt bài.",
            "MaterialController": "Điều phối việc tải lên, cập nhật, đóng dấu bản quyền (watermark), tải xuống tư liệu và đồng bộ Google Drive.",
            "WorkflowService": "Kiểm soát chặt chẽ quy trình chuyển trạng thái công việc và chuỗi phê duyệt 3 cấp."
        }
    },
    "cd-3.7": {
        "viSummary": "Sơ đồ lớp (Class Diagram) của phân hệ 3.7 (Tính năng AI): mô tả cấu trúc Chủ đề xu hướng, Tài liệu kiến thức thương hiệu (Brand Guideline), Tiến trình tạo Caption/Ảnh/Video/Đại sứ ảo bằng AI và Danh bạ đối tác truyền thông.",
        "roleMap": {
            "BrandKnowledgeDocument": "Lưu thông tin các tệp tài liệu hướng dẫn thương hiệu đã tải lên để AI đọc hiểu và viết đúng phong cách nhãn hàng.",
            "ThirdPartyCollaborator": "Lưu hồ sơ các đối tác truyền thông bên thứ ba (KOL/KOC, báo điện tử, kênh quảng cáo) và tiến độ hợp tác.",
            "AIStudioController": "Tiếp nhận các yêu cầu xem xu hướng, quản lý tài liệu thương hiệu và tạo nội dung/hình ảnh/video bằng AI.",
            "CollaboratorController": "Tiếp nhận các yêu cầu quản lý danh bạ đối tác truyền thông và gợi ý đối tác phù hợp bằng AI.",
            "AITrendService": "Thu thập và phân tích các chủ đề, từ khóa và thẻ hashtag đang thịnh hành phù hợp với ngành hàng.",
            "AIGenerationService": "Xử lý việc tạo caption, hình ảnh, video và đại sứ ảo bằng AI, đồng thời kiểm tra và trừ điểm AI Credit tương ứng.",
            "BrandKnowledgeService": "Xử lý việc tải lên, trích xuất nội dung và xóa tài liệu hướng dẫn thương hiệu của từng Workspace."
        }
    },
    "cd-3.8": {
        "viSummary": "Sơ đồ lớp (Class Diagram) của phân hệ 3.8 (Xuất bản & Mạng xã hội): mô tả cấu trúc Tài khoản mạng xã hội đã kết nối, Bài đăng hẹn giờ/xuất bản trên 4 nền tảng (Facebook, Instagram, TikTok, Threads) và Số liệu tương tác.",
        "roleMap": {
            "SocialAccount": "Lưu thông tin kết nối và quyền đăng bài của các trang Facebook, Instagram, TikTok và Threads trong Workspace.",
            "Post": "Lưu thông tin bài đăng mạng xã hội, thời gian hẹn giờ đăng, trạng thái xuất bản, đường dẫn bài viết và các chỉ số tương tác.",
            "SocialAccountController": "Tiếp nhận yêu cầu kết nối mới hoặc ngắt kết nối tài khoản mạng xã hội.",
            "PublishingController": "Tiếp nhận yêu cầu xem trước bài đăng, hẹn giờ đăng, đăng ngay và xem thống kê tương tác.",
            "PublishingService": "Kiểm tra bài viết đã duyệt và đúng quy chuẩn kích thước/ký tự, đẩy bài lên 4 mạng xã hội và tự động thử lại nếu lỗi mạng.",
            "SocialMetricsService": "Định kỳ cập nhật số lượt thích, bình luận, chia sẻ và lượt xem từ mạng xã hội về bảng thống kê."
        }
    },
    "cd-3.9": {
        "viSummary": "Sơ đồ lớp (Class Diagram) của phân hệ 3.9 (Gói đăng ký & Thanh toán): mô tả cấu trúc Đơn hàng nâng cấp gói / mua thêm điểm, Xử lý thanh toán tự động qua SePay (VietQR), Hóa đơn điện tử và Sổ theo dõi điểm AI Credit.",
        "roleMap": {
            "SubscriptionOrder": "Lưu thông tin đơn hàng nâng cấp gói dịch vụ (Pro, Enterprise) hoặc mua thêm gói điểm AI Credit kèm mã thanh toán SePay.",
            "AICreditLedger": "Lưu lịch sử cộng điểm, trừ điểm sử dụng AI, hoàn điểm khi lỗi và hạn mức điểm của từng Workspace.",
            "BillingController": "Tiếp nhận yêu cầu nâng cấp gói, tạo mã QR thanh toán, nhận thông báo từ SePay và tải hóa đơn PDF.",
            "AICreditController": "Tiếp nhận yêu cầu xem thống kê sử dụng AI Credit, mua thêm điểm và cài đặt hạn mức cho Workspace.",
            "SePayPaymentService": "Tạo mã VietQR cho đơn hàng và tự động kích hoạt gói cước / cộng điểm ngay khi nhận xác nhận chuyển khoản từ SePay.",
            "AICreditService": "Quản lý số dư điểm AI Credit của Agency và kiểm soát hạn mức chi tiêu của từng Workspace."
        }
    },
    "cd-3.10": {
        "viSummary": "Sơ đồ lớp (Class Diagram) của phân hệ 3.10 (Chức năng Quản trị Admin): mô tả cấu trúc Thông báo hệ thống, Lịch sử cảnh cáo vi phạm, Hàng đợi kiểm duyệt nội dung, Bảng giá AI Credit và Báo cáo thống kê toàn nền tảng.",
        "roleMap": {
            "SystemNotification": "Lưu nội dung thông báo toàn hệ thống, nhóm người nhận mục tiêu và trạng thái đã đọc.",
            "UserViolationStrike": "Lưu lịch sử các lần cảnh cáo vi phạm (Vàng, Cam, Đỏ) và thời hạn khóa tài khoản tạm thời.",
            "AdminDashboardController": "Tiếp nhận yêu cầu xem thống kê toàn nền tảng, giám sát tình trạng máy chủ và xuất báo cáo doanh thu PDF.",
            "AdminModerationController": "Tiếp nhận yêu cầu xử lý hàng đợi kiểm duyệt nội dung bị báo cáo và cập nhật mức phạt vi phạm.",
            "AdminUserController": "Tiếp nhận yêu cầu xem danh sách, tạo mới, sửa thông tin và khóa/mở khóa tài khoản người dùng.",
            "AdminPricingController": "Tiếp nhận yêu cầu xem, sửa trực tiếp hoặc nhập file CSV bảng giá tiêu hao AI Credit."
        }
    }
}

BUSINESS_RULES_VI = {
    "BR-01": "Mỗi địa chỉ email chỉ được đăng ký cho một tài khoản duy nhất (không phân biệt chữ hoa hay chữ thường, ví dụ User@gmail.com và user@gmail.com được tính là một). Nếu đăng ký email đã tồn tại, hệ thống sẽ báo lỗi MSG08.",
    "BR-02": "Mật khẩu phải có ít nhất 8 ký tự và chứa ít nhất 1 chữ số; mật khẩu luôn được mã hóa an toàn trước khi lưu vào cơ sở dữ liệu.",
    "BR-03": "Mã xác nhận OTP gửi qua email (khi đăng ký hoặc quên mật khẩu) gồm 6 chữ số, có hiệu lực trong 10 phút và chỉ dùng được 1 lần. Khi tạo mã mới thì mã cũ sẽ hết hiệu lực ngay.",
    "BR-04": "Mỗi lần bấm gửi lại mã OTP phải cách nhau ít nhất 60 giây. Nếu nhập sai mã OTP liên tiếp 5 lần thì mã đó sẽ bị khóa, người dùng phải yêu cầu gửi mã mới.",
    "BR-05": "Chỉ những tài khoản đã xác thực email và đang hoạt động mới được đăng nhập vào hệ thống. Tài khoản chưa xác thực sẽ được chuyển sang màn hình nhập OTP (3.2.6); tài khoản đang bị khóa hoặc đã xóa sẽ bị từ chối đăng nhập.",
    "BR-06": "Nếu nhập sai mật khẩu đăng nhập 5 lần liên tiếp trong vòng 15 phút, tài khoản sẽ tạm khóa chức năng đăng nhập bằng mật khẩu trong 15 phút để chống dò mật khẩu.",
    "BR-07": "Khi đăng nhập bằng Google, nếu email Google trùng với tài khoản đã có trên BrandHub thì hệ thống tự động liên kết và đăng nhập luôn; nếu chưa có thì hệ thống tự tạo tài khoản mới đã xác thực.",
    "BR-08": "Khi đặt lại mật khẩu do quên (3.2.4), hệ thống sẽ đăng xuất toàn bộ các thiết bị đang đăng nhập cũ. Khi chủ động đổi mật khẩu (3.2.5), người dùng phải nhập đúng mật khẩu hiện tại và mật khẩu mới phải khác mật khẩu cũ.",
    "BR-09": "Nếu tài khoản có bật bảo mật 2 lớp (2FA), sau khi nhập đúng mật khẩu, người dùng cần nhập thêm mã 6 số từ ứng dụng Authenticator trên điện thoại (thay đổi mỗi 30 giây) mới hoàn tất đăng nhập.",
    "BR-10": "Khi người dùng tự xóa tài khoản (3.2.9), hệ thống sẽ tạm khóa và cho phép khôi phục trong 30 ngày trước khi xóa hẳn. Lưu ý: Không thể xóa tài khoản nếu người đó đang là Owner duy nhất của một Agency còn thành viên hoặc chiến dịch đang chạy.",
    "BR-11": "Mỗi người dùng có một Hồ sơ cá nhân duy nhất trên hệ thống; địa chỉ email đăng nhập chính được cố định, không thể tự đổi trên màn hình sửa hồ sơ.",
    "BR-12": "Ảnh đại diện (Avatar) và ảnh bìa tải lên ở Hồ sơ cá nhân, Hồ sơ Client, Agency hoặc Workspace phải có định dạng PNG, JPG hoặc WEBP và dung lượng tối đa 5 MB.",
    "BR-13": "Mỗi tài khoản Client có một Hồ sơ thương hiệu riêng (gồm tên nhãn hàng, ngành nghề, logo, website, thông tin liên hệ) có thể dùng chung cho nhiều Workspace khác nhau mà không cần phải nhập lại.",
    "BR-14": "Chỉ chính tài khoản Client đó hoặc Manager trong Workspace liên kết mới được xem và cập nhật Hồ sơ thương hiệu của Client, và không được phép thay đổi email gốc của tài khoản Client.",
    "BR-15": "Người tạo ra một Agency sẽ giữ vai trò Owner duy nhất của Agency đó và có toàn quyền quản lý các Workspace, nhân sự cũng như thanh toán gói cước của công ty.",
    "BR-16": "Chỉ Owner mới có quyền xóa Agency (3.4.6) hoặc xóa Workspace (3.4.17). Khi xóa, dữ liệu sẽ được chuyển sang trạng thái tạm ẩn trong 30 ngày để Owner có thể khôi phục lại nếu xóa nhầm, đồng thời tạm ngưng quyền truy cập của các thành viên.",
    "BR-17": "Lời mời tham gia Agency được gửi qua email và thông báo trên ứng dụng. Khi chấp nhận, người dùng trở thành thành viên chung của Agency (chưa tự động vào các Workspace riêng). Lời mời sẽ tự hết hạn sau 3 ngày nếu không phản hồi.",
    "BR-18": "Chỉ đúng tài khoản có email nhận được lời mời (và lời mời đó vẫn đang chờ phản hồi, chưa hết hạn 3 ngày) mới có thể bấm Chấp nhận (3.4.9) hoặc Từ chối (3.4.10).",
    "BR-19": "Khi xóa một thành viên khỏi Agency (3.4.11) hoặc Workspace (3.4.26), người đó sẽ mất quyền truy cập ngay lập tức, nhưng toàn bộ bài viết, công việc và tư liệu mà họ đã làm trước đó vẫn được giữ nguyên cho dự án.",
    "BR-20": "Phân quyền xem Workspace: Owner nhìn thấy toàn bộ tất cả các Workspace trong Agency của mình; còn Manager, Creator và Client chỉ nhìn thấy và truy cập được những Workspace mà mình được thêm vào làm thành viên.",
    "BR-21": "Khi tạo mới một Workspace (3.4.14), Owner bắt buộc phải chọn ít nhất 1 thành viên làm Manager phụ trách. Trong suốt quá trình hoạt động, mỗi Workspace luôn phải có ít nhất 1 Manager.",
    "BR-22": "Mỗi Workspace đều có cài đặt Múi giờ chuẩn riêng (ví dụ UTC+7). Mọi mốc thời gian chiến dịch, hạn chót công việc và giờ hẹn đăng bài trong Workspace đều được tính theo múi giờ này.",
    "BR-23": "Thành viên có thể chủ động rời khỏi một Workspace (3.4.18) mà vẫn giữ tư cách thành viên của Agency. Tuy nhiên, nếu người đó đang là Manager duy nhất của Workspace thì phải chuyển quyền Manager cho người khác trước khi rời đi.",
    "BR-24": "Mẫu cấu hình Workspace (Workspace Template) giúp lưu lại các thiết lập sẵn (ngành hàng, múi giờ, khung vai trò, gói dịch vụ mẫu). Khi xóa một Template (3.4.22), các Workspace đã tạo từ mẫu đó trước đây vẫn hoạt động bình thường.",
    "BR-25": "Gói dịch vụ truyền thông (Media Package) gồm các gói mẫu có sẵn hoặc gói do Owner tự thiết lập (quy định rõ thời gian, số lượng bài đăng, KPI và chi phí). Chỉ Owner mới có quyền tạo mới hoặc bật/tắt các gói mẫu của Agency.",
    "BR-26": "Trong mỗi dự án, Client và đại diện Agency (Owner/Manager) có thể trao đổi, đề xuất chỉnh sửa các điều khoản của gói truyền thông (3.5.3) cho đến khi cả hai bên cùng bấm phê duyệt chốt gói (3.5.4).",
    "BR-27": "Kế hoạch Chiến dịch Truyền thông (Media Campaign - 3.5.5) phải được lập dựa trên một Gói dịch vụ đã được duyệt, liệt kê cụ thể các bài viết dự kiến, kênh đăng và lịch trình thực hiện cho nhãn hàng.",
    "BR-28": "Mỗi lần chỉnh sửa hoặc góp ý trên Kế hoạch Chiến dịch (3.5.7) đều được hệ thống lưu lại thành một phiên bản lịch sử để hai bên dễ dàng đối chiếu trước khi duyệt chính thức.",
    "BR-29": "Kế hoạch Chiến dịch chỉ chính thức bắt đầu khi cả Manager và Client cùng xác nhận phê duyệt (3.5.8). Ngay khi duyệt xong, hệ thống tự động tạo các đầu việc (Task) tương ứng vào danh sách chờ (Backlog) của Workspace.",
    "BR-30": "Chỉ Manager mới có quyền xác nhận hoàn tất và đóng Chiến dịch Truyền thông đang chạy (3.5.9). Khi chiến dịch kết thúc, các yêu cầu nội dung phát sinh còn đang chờ xử lý của chiến dịch đó cũng sẽ tự động đóng lại.",
    "BR-31": "Yêu cầu nội dung phát sinh (Content Request) đi qua các trạng thái: Chờ xử lý (PENDING) -> Đang xem xét (IN_PROGRESS) -> Chấp nhận (ACCEPTED) hoặc Từ chối (DENIED) do Owner/Manager quyết định. Khi được Chấp nhận, hệ thống tự động tạo thành một Task mới trong Workspace.",
    "BR-32": "Người gửi Yêu cầu nội dung phát sinh (Client hoặc Manager) chỉ có thể sửa nội dung (3.5.12) hoặc hủy yêu cầu (3.5.13) khi yêu cầu đó vẫn đang ở trạng thái Chờ xử lý (PENDING).",
    "BR-33": "Mỗi công việc (Task) trong Workspace đi qua 5 trạng thái: Chờ phân rã (BACKLOG) -> Cần làm (TODO) -> Đang làm (IN_PROGRESS) -> Đang chờ duyệt (IN_REVIEW) -> Hoàn thành (DONE). Chỉ Manager mới có quyền điền đặc tả chi tiết (3.6.1) và giao việc cho Creator (3.6.2).",
    "BR-34": "Quy trình duyệt bài 3 cấp (3.6.9): Creator gửi bài nháp -> Người kiểm tra nội bộ (nếu có) duyệt -> Manager duyệt -> Client duyệt bước cuối. Nếu bất kỳ cấp nào bấm Trả lại (kèm lý do bắt buộc), bài viết sẽ quay về cho Creator sửa lại từ đầu nhưng vẫn giữ nguyên lịch sử nhận xét trước đó.",
    "BR-35": "Màn hình soạn thảo bài viết (3.6.10) tự động lưu lại các phiên bản mỗi khi người dùng lưu nháp hoặc gửi duyệt, giúp Creator và Manager dễ dàng xem lại lịch sử chỉnh sửa và khôi phục bản cũ (3.6.34) mà không tốn thêm điểm AI Credit.",
    "BR-36": "Tư liệu trong kho của Workspace được phân thành 3 loại: Ảnh/video gốc chưa chỉnh sửa (RAW), Ấn phẩm đã hoàn thiện (RETOUCHED) và Tài liệu tham khảo thương hiệu (BRAND_REFERENCE). Nếu chọn nhầm tệp RAW để đăng bài, hệ thống sẽ hiện cảnh báo nhắc nhở; tư liệu đã xóa có thể khôi phục trong 30 ngày.",
    "BR-37": "Khi kết nối Google Drive của khách hàng (3.6.15), hệ thống chỉ xin quyền đọc dữ liệu để đồng bộ các tệp ảnh/video được chọn vào kho tư liệu của Workspace (3.6.16). Khi ngắt kết nối (3.6.17), các tệp đã đồng bộ vào kho trước đó vẫn được giữ nguyên.",
    "BR-38": "Khi đóng dấu bản quyền (Watermark - 3.6.18), hệ thống ghép logo thương hiệu lên ảnh theo vị trí, kích thước và độ mờ đã chọn, sau đó lưu thành một tệp ảnh mới trong kho tư liệu để giữ nguyên ảnh gốc.",
    "BR-39": "Các bộ sưu tập Hashtag được quản lý riêng theo từng Workspace và phân loại theo mục đích chiến dịch/sự kiện. Khi xóa một bộ Hashtag (3.6.24), hệ thống chỉ ẩn khỏi danh sách chọn mới chứ không làm mất các hashtag đã chèn vào bài viết cũ.",
    "BR-40": "Biểu mẫu Khảo sát (3.6.25) giúp thu thập ý kiến phản hồi của người tham gia sự kiện và thống kê kết quả trực tiếp (3.6.26); tính năng Tạo link họp (3.6.27) giúp tạo nhanh đường dẫn phòng họp trực tuyến gắn với lịch của Workspace.",
    "BR-41": "Mẫu Email (Mail Template) cho phép chèn các thông tin tự động (như tên người nhận, tên chiến dịch). Khi gửi email hàng loạt (3.6.32), hệ thống tự động bỏ qua những địa chỉ đã hủy đăng ký nhận tin.",
    "BR-42": "Tính năng Kiểm tra tuân thủ nội dung (3.6.33) giúp rà soát văn bản bài viết để phát hiện các từ ngữ nhạy cảm, bạo lực, phản cảm hoặc vi phạm chính sách cộng đồng, tô sáng đoạn vi phạm để Creator sửa lại trước khi duyệt và đăng bài.",
    "BR-43": "Phòng trò chuyện trực tuyến (Realtime Chat - 3.6.35) chỉ dành riêng cho các thành viên và Client trong cùng một Workspace, hỗ trợ gửi tin nhắn tức thì, trả lời theo luồng, thả biểu tượng cảm xúc và nhắc tên (@mention).",
    "BR-44": "Cả 4 chế độ xem công việc (Danh sách 3.6.4, Lịch 3.6.5, Biểu đồ Gantt 3.6.6, Bảng Kanban 3.6.7) và Bộ lọc (3.6.8) đều hiển thị chung một nguồn dữ liệu Task của Workspace, đồng bộ theo đúng múi giờ và quyền hạn của từng người.",
    "BR-45": "Danh sách Chủ đề xu hướng (3.7.1) và Đồ thị xu hướng AI (3.7.2) được tổng hợp tự động theo lịch thu thập do Admin cấu hình (3.7.13), giúp gợi ý các chủ đề và thẻ hashtag đang thịnh hành sát với ngành hàng.",
    "BR-46": "Tài liệu hướng dẫn thương hiệu (Brand Guideline) tải lên kho tri thức AI (3.7.4) hỗ trợ định dạng PDF, DOCX, TXT hoặc đường dẫn web (tối đa 10 MB), được kiểm tra an toàn và lưu tách biệt hoàn toàn theo từng Workspace.",
    "BR-47": "Khi xóa một Tài liệu hướng dẫn thương hiệu (3.7.5), hệ thống xóa cả tệp gốc lẫn toàn bộ dữ liệu trích xuất của tài liệu đó để AI không còn sử dụng thông tin cũ khi viết bài.",
    "BR-48": "Mọi thao tác tạo nội dung có tính phí bằng AI (Tạo Caption 3.7.6, Tạo Đại sứ ảo 3.7.7, Tạo Ảnh 3.7.9, Tạo Video 3.7.11) đều kiểm tra số dư điểm AI Credit trước khi chạy, trừ điểm theo bảng giá hiện hành (BR-64) và tự động hoàn lại điểm nếu dịch vụ AI gặp sự cố.",
    "BR-49": "Khi tạo Caption (3.7.6), Ảnh (3.7.9) hoặc Video (3.7.11), hệ thống kết hợp thông tin từ Tài liệu thương hiệu của Workspace, Mẫu phong cách đã chọn (3.7.8, 3.7.10) và Đại sứ thương hiệu ảo (3.7.7) để sản phẩm đầu ra giữ đúng nhận diện nhãn hàng.",
    "BR-50": "Các hình ảnh và video do AI tạo ra có thể xuất tải về máy (3.7.12) theo các định dạng thông dụng (MP4, WebM cho video; PNG, JPG, WebP cho ảnh) hoặc lưu thẳng vào Kho tư liệu của Workspace.",
    "BR-51": "Mỗi Agency có một Danh bạ đối tác truyền thông bên thứ ba (3.7.15–3.7.18) gồm KOL, KOC, báo điện tử, kênh quảng cáo và truyền hình, giúp theo dõi trạng thái hợp tác từ lúc Liên hệ -> Đàm phán -> Chốt hợp tác -> Đang lên sóng.",
    "BR-52": "Tính năng Gợi ý đối tác bằng AI (3.7.19) tự động chấm điểm và đề xuất các đối tác phù hợp nhất trong danh bạ dựa trên ngành hàng của chiến dịch, tệp khách hàng mục tiêu và mức ngân sách dự kiến.",
    "BR-53": "Các tài khoản mạng xã hội (Facebook, Instagram, TikTok, Threads) được kết nối riêng cho từng Workspace (3.8.1). Khi ngắt kết nối một tài khoản (3.8.2), hệ thống hủy quyền đăng bài và tự động hủy các lịch hẹn đăng đang chờ của kênh đó.",
    "BR-54": "Chỉ những bài viết đã hoàn tất quy trình phê duyệt (BR-34) và vượt qua bước kiểm tra nội dung an toàn (BR-42) mới được phép hẹn giờ đăng (3.8.6) hoặc đăng ngay lên mạng xã hội (3.8.8–3.8.15).",
    "BR-55": "Trước khi đăng hoặc khi Xem trước bài đăng (3.8.5), hệ thống tự động kiểm tra định dạng tệp, tỷ lệ khung hình, thời lượng video và giới hạn số ký tự theo đúng quy định của từng nền tảng (Facebook, Instagram, TikTok, Threads).",
    "BR-56": "Các bài hẹn giờ đăng (3.8.6) được chạy theo đúng múi giờ của Workspace, cập nhật trạng thái từ Chờ đăng -> Đang đăng -> Đã đăng (hoặc Lỗi - 3.8.7). Nếu gặp lỗi kết nối mạng tạm thời, hệ thống sẽ tự động thử đăng lại tối đa 3 lần.",
    "BR-57": "Sau khi bài viết được đăng thành công, hệ thống định kỳ cập nhật các chỉ số tương tác (lượt thích, bình luận, chia sẻ, lượt xem) từ mạng xã hội về Bảng thống kê bài đăng (3.8.3) và Chi tiết bài đăng (3.8.4).",
    "BR-58": "Mỗi Agency mới tạo sẽ bắt đầu ở gói Cơ bản (Basic). Khi Owner nâng cấp lên gói cao hơn (Pro hoặc Enterprise qua 3.9.1) và thanh toán thành công, hệ thống sẽ mở rộng ngay giới hạn số lượng Workspace, thành viên, dung lượng lưu trữ và điểm AI Credit hàng tháng.",
    "BR-59": "Mọi giao dịch nâng cấp gói cước (3.9.1) và mua thêm điểm AI Credit (3.9.5) đều thanh toán qua mã VietQR của cổng SePay (3.9.2). Đơn hàng chỉ chuyển sang Đã thanh toán và cộng quyền lợi khi hệ thống nhận được thông báo xác nhận hợp lệ từ SePay.",
    "BR-60": "Mọi biến động điểm AI Credit đều được ghi lại rõ ràng trong lịch sử (3.9.4); hệ thống ưu tiên trừ điểm định kỳ hàng tháng trước khi trừ đến điểm mua thêm, đồng thời cho phép Owner đặt giới hạn sử dụng điểm cho từng Workspace và thành viên (3.9.6).",
    "BR-61": "Mỗi giao dịch thanh toán thành công đều tự động tạo hóa đơn điện tử để Owner tra cứu và tải về trong mục Lịch sử hóa đơn (3.9.3), đồng thời tổng hợp vào Bảng thống kê doanh thu của Admin (3.10.13).",
    "BR-62": "Chỉ những tài khoản có quyền Admin toàn hệ thống mới truy cập được các chức năng quản trị (3.10.1–3.10.14). Để đảm bảo an toàn, Admin không thể tự khóa tài khoản của chính mình hoặc khóa tài khoản của một Admin khác.",
    "BR-63": "Cơ chế xử lý vi phạm 3 mức (3.10.5, 3.10.9): 3 lần cảnh cáo mức Vàng (YELLOW) sẽ tự động gộp thành 1 mức Cam (ORANGE); tài khoản bị mức Cam sẽ bị gắn cờ theo dõi (mọi bài đăng cần Admin duyệt qua hàng đợi 3.10.4); nếu vi phạm mức Đỏ (RED) hoặc tích lũy 3 mức Cam thì tài khoản sẽ bị tạm khóa 30 ngày. Sau 30 ngày không có vi phạm mới, cảnh cáo sẽ tự hết hạn và tài khoản hết hạn khóa 30 ngày sẽ tự mở lại.",
    "BR-64": "Admin có thể chỉnh sửa đơn giá điểm AI Credit cho từng tính năng riêng lẻ (3.10.11) hoặc nhập hàng loạt từ file CSV (3.10.12). Giá mới sẽ áp dụng cho các lượt gọi AI tiếp theo và không làm thay đổi lịch sử các giao dịch đã trừ trước đó.",
    "BR-65": "Khi Admin tạo tài khoản mới trên cổng quản trị (3.10.7), hệ thống sẽ gửi thông tin kích hoạt qua email cho người dùng. Mọi thao tác quản trị của Admin (duyệt vi phạm, khóa tài khoản, gửi thông báo, đổi giá AI Credit, xuất báo cáo PDF) đều được ghi lại đầy đủ vào nhật ký hệ thống."
}

MESSAGES_CONTEXT_VI = {
    "MSG01": "Không tìm thấy dữ liệu nào khớp với từ khóa tìm kiếm hoặc bộ lọc hiện tại",
    "MSG02": "Người dùng bỏ trống các ô thông tin bắt buộc phải nhập (có dấu *)",
    "MSG03": "Nội dung nhập vào vượt quá độ dài tối đa hoặc nằm ngoài phạm vi cho phép",
    "MSG04": "Địa chỉ email nhập vào không đúng định dạng chuẩn (ví dụ thiếu @ hoặc tên miền)",
    "MSG05": "Mật khẩu chưa đủ điều kiện an toàn (cần tối thiểu 8 ký tự và có ít nhất 1 chữ số)",
    "MSG06": "Mật khẩu nhập lại ở ô xác nhận không trùng khớp với mật khẩu vừa đặt",
    "MSG07": "Người dùng không có quyền thực hiện thao tác này theo phân quyền vai trò",
    "MSG08": "Địa chỉ email này đã được đăng ký cho một tài khoản khác trên hệ thống",
    "MSG09": "Nhập sai địa chỉ email hoặc mật khẩu khi đăng nhập",
    "MSG10": "Đăng ký tài khoản mới thành công và hệ thống đã gửi mã xác nhận OTP qua email",
    "MSG11": "Tài khoản bị tạm khóa đăng nhập 15 phút do nhập sai mật khẩu quá 5 lần liên tiếp",
    "MSG12": "Tài khoản hiện đang bị khóa hoặc đang trong thời gian chờ xóa nên không thể đăng nhập",
    "MSG13": "Đăng nhập hoặc liên kết qua tài khoản Google bị hủy giữa chừng hoặc gặp lỗi kết nối",
    "MSG14": "Đã gửi yêu cầu khôi phục mật khẩu (hiển thị thông báo gửi mã đặt lại mật khẩu qua email)",
    "MSG15": "Mã xác nhận OTP hoặc mã bảo mật 2 lớp (2FA) không đúng hoặc đã hết thời hạn",
    "MSG16": "Yêu cầu gửi lại mã OTP khi chưa hết 60 giây chờ hoặc đã nhập sai quá số lần quy định",
    "MSG17": "Đặt lại mật khẩu mới hoặc đổi mật khẩu thành công",
    "MSG18": "Mật khẩu hiện tại nhập không đúng, hoặc mật khẩu mới trùng với mật khẩu đang dùng",
    "MSG19": "Bật/tắt hoặc xác nhận mã bảo mật 2 lớp (2FA) thành công",
    "MSG20": "Đăng xuất khỏi phiên làm việc hoặc xác nhận xóa mềm tài khoản thành công",
    "MSG21": "Cập nhật thông tin hồ sơ cá nhân, hồ sơ Client, Agency hoặc Workspace thành công",
    "MSG22": "Tệp hình ảnh hoặc tài liệu tải lên không đúng định dạng hỗ trợ hoặc vượt quá dung lượng cho phép",
    "MSG23": "Tạo mới Agency hoặc tạo mới Workspace thành công",
    "MSG24": "Xóa mềm Agency hoặc Workspace thành công (có thể khôi phục lại trong vòng 30 ngày)",
    "MSG25": "Gửi lời mời thành viên tham gia Agency qua email thành công (có hiệu lực trong 3 ngày)",
    "MSG26": "Người dùng được mời đã là thành viên chính thức hoặc đang có một lời mời chờ phản hồi",
    "MSG27": "Chấp nhận hoặc từ chối lời mời tham gia Agency thành công",
    "MSG28": "Lời mời tham gia Agency đã quá hạn 3 ngày hoặc không còn hiệu lực",
    "MSG29": "Thêm thành viên, đổi vai trò hoặc xóa/rời khỏi Workspace thành công",
    "MSG30": "Lưu mới, áp dụng hoặc xóa mẫu cấu hình Workspace (Template) thành công",
    "MSG31": "Tạo gói dịch vụ truyền thông, gửi đề xuất điều chỉnh hoặc phê duyệt chốt gói thành công",
    "MSG32": "Tạo mới hoặc lưu cập nhật bản Kế hoạch Chiến dịch Truyền thông thành công",
    "MSG33": "Phê duyệt Kế hoạch Chiến dịch thành công và tự động chuyển các hạng mục sang danh sách công việc (Backlog)",
    "MSG34": "Nghiệm thu hoàn tất Chiến dịch Truyền thông và đóng các yêu cầu phát sinh còn tồn đọng",
    "MSG35": "Tạo mới, cập nhật, đổi trạng thái hoặc hủy Yêu cầu nội dung phát sinh thành công",
    "MSG36": "Không thể chỉnh sửa, xóa hoặc hủy mục này do trạng thái hiện tại không còn cho phép thay đổi",
    "MSG37": "Cập nhật chi tiết công việc (Task), phân công người làm, đổi trạng thái hoặc bình luận thành công",
    "MSG38": "Gửi bài duyệt, phê duyệt hoặc trả lại bài viết kèm nhận xét trong quy trình duyệt 3 cấp thành công",
    "MSG39": "Lưu bản nháp bài viết hoặc khôi phục lại phiên bản nội dung trước đó thành công",
    "MSG40": "Tải lên, cập nhật thông tin, đóng dấu bản quyền hoặc xóa mềm tư liệu trong kho thành công",
    "MSG41": "Cảnh báo nhắc người dùng khi chọn tệp ảnh/video gốc chưa qua chỉnh sửa (RAW) để đưa vào bài đăng",
    "MSG42": "Kết nối, đồng bộ tệp hoặc ngắt kết nối kho lưu trữ Google Drive thành công",
    "MSG43": "Chèn thẻ hashtag vào bài viết hoặc thêm/sửa/xóa bộ sưu tập Hashtag thành công",
    "MSG44": "Tạo biểu mẫu khảo sát, tạo đường dẫn phòng họp trực tuyến hoặc lưu/gửi mẫu Email thành công",
    "MSG45": "Phát hiện từ ngữ vi phạm tiêu chuẩn cộng đồng khi kiểm tra nội dung bài viết",
    "MSG46": "Tải lên hoặc xóa tài liệu hướng dẫn thương hiệu (Brand Guideline) trong kho AI thành công",
    "MSG47": "Tạo nội dung Caption, Đại sứ ảo, Hình ảnh, Video hoặc Gợi ý Hashtag bằng AI thành công",
    "MSG48": "Số dư điểm AI Credit không đủ hoặc đã chạm trần hạn mức điểm được cấp cho Workspace/thành viên",
    "MSG49": "Quá trình tạo nội dung bằng AI bị gián đoạn hoặc quá thời gian chờ (số điểm AI Credit tạm giữ đã được hoàn lại)",
    "MSG50": "Thêm mới, cập nhật, xóa hoặc nhận gợi ý danh sách đối tác truyền thông (Collaborator) thành công",
    "MSG51": "Kết nối hoặc ngắt kết nối tài khoản mạng xã hội (Facebook, Instagram, TikTok, Threads) thành công",
    "MSG52": "Định dạng ảnh/video, tỷ lệ khung hình, thời lượng hoặc độ dài văn bản không đúng quy chuẩn của mạng xã hội đích",
    "MSG53": "Hẹn giờ đăng hoặc xuất bản bài viết trực tiếp lên mạng xã hội đã chọn thành công",
    "MSG54": "Đăng bài lên mạng xã hội thất bại do lỗi kết nối hoặc phiên ủy quyền tài khoản đã hết hạn (cần kết nối lại hoặc thử lại)",
    "MSG55": "Khởi tạo đơn hàng nâng cấp gói dịch vụ hoặc mua thêm điểm AI Credit thành công (hiển thị mã VietQR SePay)",
    "MSG56": "Xác nhận thanh toán chuyển khoản SePay thành công, đã nâng cấp gói cước hoặc cộng thêm điểm AI Credit",
    "MSG57": "Cập nhật hạn mức sử dụng điểm AI Credit tối đa cho Workspace hoặc thành viên thành công",
    "MSG58": "Phát thông báo toàn hệ thống hoặc lưu quyết định kiểm duyệt nội dung vi phạm thành công",
    "MSG59": "Tạo tài khoản mới, cập nhật thông tin, ghi nhận mức phạt vi phạm hoặc khóa/mở khóa người dùng thành công",
    "MSG60": "Cập nhật bảng giá AI Credit (trực tiếp hoặc qua file CSV), lưu lịch thu thập xu hướng hoặc xuất báo cáo PDF thành công"
}

SCREENS_VI = {
    "1": ("Xác thực & Tài khoản", "Màn hình Đăng ký (/register)", "Cho phép người dùng mới (Guest) tạo tài khoản BrandHub bằng họ tên, email và mật khẩu."),
    "2": ("Xác thực & Tài khoản", "Màn hình Đăng nhập (/login)", "Đăng nhập vào hệ thống bằng email/mật khẩu hoặc đăng nhập nhanh qua tài khoản Google."),
    "3": ("Xác thực & Tài khoản", "Màn hình Xác thực OTP (/verify-otp)", "Nhập mã OTP 6 chữ số gửi qua email để kích hoạt tài khoản mới hoặc xác nhận đặt lại mật khẩu."),
    "4": ("Xác thực & Tài khoản", "Màn hình Quên & Đặt lại mật khẩu (/forgot-password, /reset-password)", "Yêu cầu gửi mã khôi phục qua email và thiết lập lại mật khẩu mới khi quên."),
    "5": ("Xác thực & Tài khoản", "Màn hình Bảo mật 2 lớp 2FA (/verify-2fa, /settings/security)", "Quét mã QR cài đặt ứng dụng Authenticator và nhập mã xác nhận 6 số khi đăng nhập."),
    "6": ("Xác thực & Tài khoản", "Màn hình Cài đặt Bảo mật & Tài khoản (/settings/security)", "Cho phép người dùng đổi mật khẩu hiện tại, đăng xuất hoặc yêu cầu xóa mềm tài khoản."),
    "7": ("Hồ sơ cá nhân & Nhãn hàng", "Màn hình Hồ sơ cá nhân (/profile)", "Xem và cập nhật thông tin cá nhân, ảnh đại diện, ảnh bìa, số điện thoại, kỹ năng và ngôn ngữ."),
    "8": ("Hồ sơ cá nhân & Nhãn hàng", "Màn hình Hồ sơ thương hiệu Client (/client-profiles)", "Xem và cập nhật thông tin thương hiệu, ngành hàng, logo và liên hệ của Client để dùng chung cho các dự án."),
    "9": ("Agency & Workspace", "Màn hình Danh sách & Tạo mới Agency (/agency, /agency/create)", "Xem các công ty (Agency) đang sở hữu hoặc tham gia và tạo mới một Agency."),
    "10": ("Agency & Workspace", "Màn hình Tổng quan & Hồ sơ Agency (/agency/:id, /agency/:id/stats)", "Xem biểu đồ thống kê hoạt động của toàn Agency, chỉnh sửa thông tin giới thiệu công ty hoặc xóa mềm Agency."),
    "11": ("Agency & Workspace", "Màn hình Thành viên & Lời mời Agency (/agency/:id/members, /agency/invitations)", "Gửi lời mời nhân sự qua email, theo dõi thời hạn 3 ngày của lời mời, chấp nhận/từ chối lời mời và quản lý thành viên."),
    "12": ("Agency & Workspace", "Màn hình Danh sách & Tạo mới Workspace (/workspace, /workspace/create)", "Xem danh sách các không gian làm việc (Workspace) được phân quyền và tạo Workspace mới kèm gán Manager."),
    "13": ("Agency & Workspace", "Màn hình Tổng quan & Cài đặt Workspace (/workspace/:id/dashboard, /workspace/:id/detail)", "Xem tiến độ công việc trong dự án, dung lượng lưu trữ, chỉnh sửa thông tin, cài đặt múi giờ chuẩn, rời hoặc xóa Workspace."),
    "14": ("Agency & Workspace", "Màn hình Thư viện Mẫu Workspace (/templates, /workspace/:id/templates)", "Lưu cấu hình Workspace hiện tại thành mẫu, xem danh sách mẫu, áp dụng mẫu cho dự án mới hoặc xóa mẫu."),
    "15": ("Agency & Workspace", "Màn hình Thành viên & Phân quyền Workspace (/workspace/:id/members)", "Xem danh sách thành viên trong dự án, thêm nhân sự hoặc Client vào Workspace, đổi vai trò hoặc xóa khỏi dự án."),
    "16": ("Gói dịch vụ & Chiến dịch", "Màn hình Danh mục & Đàm phán Gói truyền thông (/media-package)", "Tạo gói dịch vụ tùy chỉnh, xem các gói mẫu, trao đổi điều khoản với Client và xác nhận chốt gói truyền thông."),
    "17": ("Gói dịch vụ & Chiến dịch", "Màn hình Lập Kế hoạch Chiến dịch Truyền thông (/workspace/:id/campaign)", "Xây dựng kế hoạch bài viết chi tiết cho chiến dịch, cập nhật theo góp ý, phê duyệt kích hoạt tạo Task và nghiệm thu chiến dịch."),
    "18": ("Gói dịch vụ & Chiến dịch", "Màn hình Yêu cầu Nội dung phát sinh (/workspace/:id/requests)", "Gửi yêu cầu làm thêm bài viết/sự kiện phát sinh, theo dõi trạng thái xét duyệt, chỉnh sửa hoặc hủy yêu cầu khi đang chờ."),
    "19": ("Nội dung & Quy trình", "Màn hình Quản lý Công việc Đa chế độ (/workspace/:id/tasks)", "Xem, lọc và sắp xếp công việc theo 4 chế độ trực quan: Bảng danh sách (List), Lịch (Calendar), Tiến độ (Gantt) và Cột kéo thả (Kanban)."),
    "20": ("Nội dung & Quy trình", "Màn hình Chi tiết Công việc, Bình luận & Duyệt bài (/workspace/:id/tasks/:taskId)", "Điền yêu cầu chi tiết cho đầu việc, giao việc cho Creator, trao đổi bình luận và thực hiện duyệt bài 3 cấp (Creator -> Manager -> Client)."),
    "21": ("Nội dung & Quy trình", "Màn hình Soạn thảo Nội dung & Lịch sử Phiên bản (/workspace/:id/content-writing)", "Soạn thảo văn bản bài đăng tích hợp đổi kiểu chữ Unicode nổi bật, kiểm tra từ ngữ vi phạm và khôi phục các phiên bản cũ."),
    "22": ("Nội dung & Quy trình", "Màn hình Kho Tư liệu & Đóng dấu Bản quyền (/workspace/:id/library)", "Quản lý ảnh/video gốc (RAW), ấn phẩm hoàn thiện và tài liệu mẫu; đồng bộ Google Drive và gắn logo đóng dấu (Watermark)."),
    "23": ("Nội dung & Quy trình", "Màn hình Bộ sưu tập Hashtag (/workspace/:id/hashtag-groups)", "Xem, thêm mới, chỉnh sửa, xóa các nhóm thẻ Hashtag theo chiến dịch và chèn nhanh vào bài viết."),
    "24": ("Nội dung & Quy trình", "Màn hình Khảo sát & Tạo Phòng họp (/workspace/:id/surveys, /workspace/:id/meetings)", "Tạo biểu mẫu khảo sát ý kiến khách hàng, xem biểu đồ thống kê kết quả và tạo nhanh link họp trực tuyến Google Meet."),
    "25": ("Nội dung & Quy trình", "Màn hình Mẫu Email & Gửi Email (/workspace/:id/mail-templates)", "Xem, tạo, sửa, xóa các mẫu email thông báo có gắn biến tự động và gửi email cho khách hàng/đội dự án."),
    "26": ("Nội dung & Quy trình", "Màn hình Nhắn tin Trực tuyến Workspace (/workspace/:id/chat)", "Nhắn tin, gửi tệp đính kèm và trao đổi trực tiếp theo thời gian thực giữa các thành viên và Client trong cùng dự án."),
    "27": ("Tính năng AI", "Màn hình Gợi ý Xu hướng & Đồ thị Xu hướng AI (/ai-studio/trends)", "Xem các chủ đề, từ khóa đang thịnh hành theo ngành hàng, khám phá mạng lưới liên kết xu hướng và cấu hình lịch thu thập."),
    "28": ("Tính năng AI", "Màn hình Kho Tài liệu Thương hiệu AI (/ai-studio/knowledge-base)", "Tải lên, tra cứu và quản lý các tài liệu Brand Guideline (PDF, DOCX, TXT) để AI đọc hiểu và viết bài đúng phong cách nhãn hàng."),
    "29": ("Tính năng AI", "Màn hình Sáng tạo AI Studio (/editor, /ai-studio/ambassadors, /ai-studio/video)", "Sử dụng AI để viết caption, tạo người mẫu đại sứ ảo, chọn mẫu phong cách, sinh hình ảnh quảng cáo, tạo video ngắn và xuất tệp."),
    "30": ("Tính năng AI", "Màn hình Danh bạ Đối tác & Gợi ý bằng AI (/collaborators, /campaign-partners)", "Quản lý danh sách KOL/KOC, báo điện tử, kênh quảng cáo của Agency và dùng AI gợi ý đối tác phù hợp với ngân sách chiến dịch."),
    "31": ("Xuất bản & Mạng xã hội", "Màn hình Kết nối Tài khoản Mạng xã hội (/social-accounts)", "Liên kết và quản lý quyền đăng bài tự động cho 4 nền tảng: Facebook, Instagram, TikTok và Threads."),
    "32": ("Xuất bản & Mạng xã hội", "Màn hình Xem trước, Hẹn giờ & Xuất bản Bài đăng (/publish, /calendar)", "Xem trước giao diện bài viết trên từng mạng xã hội, hẹn giờ đăng tự động hoặc xuất bản ngay và theo dõi trạng thái đăng."),
    "33": ("Xuất bản & Mạng xã hội", "Màn hình Thống kê & Chi tiết Bài đã đăng (/publish/dashboard, /publish/posts/:id)", "Theo dõi tổng quan các bài đã xuất bản và xem chi tiết số lượt thích, bình luận, chia sẻ, lượt xem của từng bài."),
    "34": ("Gói cước & Thanh toán", "Màn hình Nâng cấp Gói, Thanh toán SePay & Hóa đơn (/subscription/plans)", "Chọn nâng cấp gói Pro/Enterprise, quét mã QR chuyển khoản qua SePay và xem/tải hóa đơn thanh toán PDF."),
    "35": ("Gói cước & Thanh toán", "Màn hình Theo dõi, Mua thêm & Phân bổ AI Credit (/credit)", "Xem lịch sử tiêu dùng điểm AI Credit, mua thêm gói điểm bổ sung và đặt hạn mức sử dụng điểm cho từng Workspace."),
    "36": ("Quản trị Hệ thống (Admin)", "Màn hình Tổng quan Hệ thống, Máy chủ & Thông báo (/admin, /admin/system-health)", "Xem số liệu thống kê toàn nền tảng, theo dõi sức khỏe máy chủ (CPU, RAM, Database) và gửi thông báo chung."),
    "37": ("Quản trị Hệ thống (Admin)", "Màn hình Kiểm duyệt Nội dung & Quản lý Người dùng (/admin?view=moderation)", "Xử lý các nội dung bị gắn cờ vi phạm và quản lý danh sách người dùng, tạo/sửa tài khoản, ghi nhận cảnh cáo hoặc khóa tài khoản."),
    "38": ("Quản trị Hệ thống (Admin)", "Màn hình Bảng giá AI Credit & Báo cáo Doanh thu (/credit/prices, /admin?view=revenue)", "Xem, cập nhật trực tiếp hoặc nhập file CSV bảng giá AI Credit; xem biểu đồ doanh thu toàn hệ thống và xuất báo cáo PDF.")
}

NON_SCREEN_VI = {
    "1": ("Xác thực & Bảo mật", "Tiến trình Gửi Email Xác thực & Mã OTP", "Tự động gửi email chứa mã OTP 6 số khi đăng ký/quên mật khẩu, email kích hoạt tài khoản mới và thông báo bảo mật."),
    "2": ("Xác thực & Bảo mật", "Dịch vụ Quản lý & Làm mới Phiên Kết nối OAuth2", "Xử lý liên kết tài khoản, mã hóa bảo mật và tự động gia hạn quyền kết nối cho Google, Google Drive, Facebook, Instagram, TikTok và Threads."),
    "3": ("Agency & Workspace", "Tiến trình Kiểm tra Lời mời Hết hạn & Dọn dữ liệu Xóa mềm", "Tự động chuyển các lời mời tham gia Agency sang trạng thái Hết hạn sau 3 ngày và dọn dẹp các tài khoản/Agency/Workspace đã quá 30 ngày chờ khôi phục."),
    "4": ("Chiến dịch Truyền thông", "Tiến trình Tự động Tạo Đầu việc (Task) từ Chiến dịch", "Ngay khi Kế hoạch Chiến dịch được cả Manager và Client phê duyệt, hệ thống tự động tạo các Task tương ứng vào bảng công việc của Workspace."),
    "5": ("Nội dung & Quy trình", "Tiến trình Đồng bộ Tư liệu từ Google Drive", "Tải các tệp hình ảnh và video được chọn từ thư mục Google Drive của khách hàng về Kho tư liệu của Workspace."),
    "6": ("Nội dung & Quy trình", "Tiến trình Gửi Email theo Mẫu & Lọc danh sách từ chối", "Thực hiện gửi email tự động theo mẫu của Workspace và tự động bỏ qua những địa chỉ email đã hủy đăng ký nhận tin."),
    "7": ("Tính năng AI", "Tiến trình Xử lý & Trích xuất Tài liệu Thương hiệu (RAG)", "Kiểm tra an toàn, đọc nội dung từ các tệp PDF/DOCX/TXT hướng dẫn thương hiệu và lưu vào kho dữ liệu AI riêng của từng Workspace."),
    "8": ("Tính năng AI", "Tiến trình Thu thập & Phân tích Xu hướng Thịnh hành", "Định kỳ thu thập các chủ đề, từ khóa và hashtag đang được quan tâm trên thị trường để cập nhật vào bảng gợi ý xu hướng."),
    "9": ("Xuất bản & Mạng xã hội", "Tiến trình Đăng bài Hẹn giờ & Cập nhật Số liệu Tương tác", "Tự động đăng các bài viết đã hẹn giờ lên Facebook, Instagram, TikTok, Threads khi đến lịch (tự thử lại tối đa 3 lần nếu lỗi mạng) và lấy số liệu tương tác về hệ thống."),
    "10": ("Gói cước & Thanh toán", "Tiến trình Xác nhận Thanh toán SePay & Hoàn điểm AI Credit", "Nhận thông báo chuyển khoản từ ngân hàng qua SePay để kích hoạt gói cước/cộng điểm ngay lập tức, đồng thời tự động hoàn lại điểm AI Credit nếu việc tạo ảnh/video gặp lỗi."),
    "11": ("Quản trị Hệ thống (Admin)", "Tiến trình Xóa Cảnh cáo Hết hạn & Mở khóa Tài khoản", "Kiểm tra hàng ngày để tự động xóa các mức cảnh cáo vi phạm sau 30 ngày không tái phạm và mở khóa lại các tài khoản đã hết thời hạn phạt 30 ngày."),
    "12": ("Quản trị Hệ thống (Admin)", "Tiến trình Thu thập Chỉ số Sức khỏe Máy chủ", "Định kỳ đo mức sử dụng CPU, RAM, ổ cứng và trạng thái kết nối của các dịch vụ để hiển thị trên màn hình Giám sát hệ thống của Admin.")
}

ENTITIES_VI = {
    "User": "Lưu thông tin tài khoản người dùng (họ tên, email, mật khẩu mã hóa, cài đặt 2FA, vai trò hệ thống USER/ADMIN, trạng thái hoạt động và số lần cảnh cáo vi phạm).",
    "UserViolationStrike": "Lưu lịch sử các lần cảnh cáo vi phạm (mức Vàng, Cam, Đỏ) do Admin ghi nhận kèm bằng chứng, lý do và thời hạn áp dụng.",
    "ClientProfile": "Lưu hồ sơ thương hiệu của Client (tên nhãn hàng, ngành nghề, logo, website, mã số thuế, thông tin liên hệ) dùng chung xuyên suốt nhiều Workspace.",
    "Agency": "Lưu thông tin công ty truyền thông do Owner tạo và sở hữu (tên công ty, logo, gói đăng ký hiện tại, tổng số dư điểm AI Credit và trạng thái xóa mềm 30 ngày).",
    "AgencyMember": "Lưu danh sách các thành viên thuộc một Agency, ngày gia nhập, trạng thái hoạt động và hạn mức điểm AI Credit cá nhân.",
    "AgencyInvitation": "Lưu các lời mời gia nhập Agency do Owner gửi qua email, kèm mã xác nhận, trạng thái (Chờ phản hồi, Đã nhận, Từ chối, Hết hạn) và mốc hết hạn 3 ngày.",
    "Workspace": "Lưu thông tin không gian làm việc riêng của từng dự án/khách hàng trong Agency, bao gồm múi giờ chuẩn, hạn mức điểm AI Credit và trạng thái hoạt động.",
    "WorkspaceMember": "Lưu danh sách thành viên tham gia vào một Workspace cụ thể cùng vai trò trong dự án đó (Manager, Creator hoặc Client).",
    "WorkspaceTemplate": "Lưu các mẫu cấu hình Workspace (múi giờ mặc định, cấu trúc vai trò, gói dịch vụ mẫu) để Owner tái sử dụng nhanh cho các dự án mới.",
    "MediaPackage": "Lưu thông tin các gói dịch vụ truyền thông mẫu hoặc gói tùy chỉnh (thời gian triển khai, số lượng bài đăng cam kết, KPI, chi phí và lịch sử đàm phán).",
    "MediaCampaign": "Lưu kế hoạch triển khai chiến dịch truyền thông chi tiết dựa trên gói dịch vụ đã duyệt, gồm danh sách hạng mục bài viết, các phiên bản chỉnh sửa và trạng thái phê duyệt.",
    "ContentRequest": "Lưu các yêu cầu làm thêm nội dung phát sinh do Client hoặc Manager gửi lên, theo dõi trạng thái xử lý (Chờ duyệt, Đang xem, Chấp nhận, Từ chối, Đã hủy) và mã Task liên kết.",
    "Task": "Lưu thông tin đầu việc sản xuất nội dung trong Workspace (tiêu đề, yêu cầu chi tiết, kênh đăng dự kiến, hạn hoàn thành, trạng thái công việc, Creator thực hiện và người duyệt).",
    "TaskApproval": "Lưu lịch sử từng bước duyệt hoặc trả lại bài viết trong quy trình 3 cấp (Creator -> Manager -> Client), ghi rõ người duyệt, thời gian và nhận xét.",
    "TaskComment": "Lưu các bình luận trao đổi, hình ảnh đính kèm và lượt nhắc tên (@mention) giữa các thành viên trên từng đầu việc.",
    "ContentVersion": "Lưu lịch sử các phiên bản nội dung bài viết đã soạn thảo, giúp đối chiếu sự thay đổi và khôi phục lại phiên bản cũ bất kỳ lúc nào.",
    "MaterialRepository": "Lưu danh mục các tệp hình ảnh, video và tài liệu trong kho của Workspace, phân loại rõ (Ảnh gốc RAW, Đã chỉnh sửa, Tài liệu mẫu) và trạng thái đóng dấu logo.",
    "CustomerDriveConnection": "Lưu thông tin kết nối an toàn với thư mục Google Drive của khách hàng để đồng bộ ảnh/video vào kho tư liệu của Workspace.",
    "HashtagCollection": "Lưu các nhóm thẻ Hashtag của Workspace được phân loại theo chiến dịch, sự kiện hoặc thẻ bắt buộc của nhãn hàng.",
    "Survey": "Lưu thông tin biểu mẫu khảo sát ý kiến khách hàng/sự kiện, danh sách câu hỏi và kết quả thống kê phản hồi.",
    "MailTemplate": "Lưu các mẫu email thông báo có gắn biến tự động (như tên khách hàng, tên chiến dịch) và lịch sử các đợt gửi email.",
    "BrandKnowledgeDocument": "Lưu thông tin các tài liệu hướng dẫn thương hiệu (PDF, DOCX, TXT) được tải lên để cung cấp kiến thức chuẩn cho công cụ AI của từng Workspace.",
    "ThirdPartyCollaborator": "Lưu danh bạ đối tác truyền thông bên thứ ba của Agency (KOL, KOC, báo điện tử, kênh quảng cáo) và tiến độ hợp tác trong các chiến dịch.",
    "SocialAccount": "Lưu thông tin kết nối tài khoản mạng xã hội (Facebook, Instagram, TikTok, Threads) của từng Workspace để phục vụ đăng bài tự động.",
    "Post": "Lưu thông tin bài đăng mạng xã hội gắn với Task đã duyệt, gồm nền tảng đăng, giờ hẹn đăng, trạng thái xuất bản, đường dẫn bài viết và các chỉ số tương tác.",
    "SubscriptionOrder": "Lưu thông tin đơn hàng nâng cấp gói dịch vụ hoặc mua thêm điểm AI Credit của Agency, mã thanh toán VietQR SePay, trạng thái đơn hàng và tệp hóa đơn PDF.",
    "AICreditLedger": "Lưu sổ theo dõi chi tiết mọi giao dịch cộng điểm, tạm giữ, trừ điểm khi dùng AI, hoàn điểm khi lỗi và bảng đơn giá của từng thao tác AI.",
    "SystemNotification": "Lưu các thông báo toàn hệ thống do Admin gửi đi, bộ lọc nhóm người nhận và trạng thái đã đọc của từng người dùng."
}
