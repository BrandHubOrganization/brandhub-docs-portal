# -*- coding: utf-8 -*-
"""
Practical, simple, logical Vietnamese specifications for FRs in domains 3.8, 3.9, 3.10 (35 FRs).
"""

FRS_PART3 = {
    # ==================== 3.8 Publishing & Social ====================
    "3.8.1": {
        "summary": "Cho phép Client hoặc Manager kết nối các tài khoản mạng xã hội chính thức của nhãn hàng (gồm 4 nền tảng: Facebook Page, Instagram Business, TikTok và Threads) vào Workspace để phục vụ đăng bài tự động.",
        "trigger": "Khi Client hoặc Manager mở màn hình Kết nối Mạng xã hội (/social-accounts), chọn nền tảng cần liên kết và xác nhận cấp quyền trên cửa sổ đăng nhập của nền tảng đó.",
        "interface": "Màn hình Kết nối Mạng xã hội (/social-accounts) hiển thị 4 thẻ nền tảng (Facebook, Instagram, TikTok, Threads), trạng thái kết nối hiện tại, danh sách các trang/kênh đã liên kết và nút Kết nối thêm tài khoản.",
        "processing": "Sau khi người dùng đăng nhập và cấp quyền trên cửa sổ chính thức của mạng xã hội (chuẩn OAuth 2.0), hệ thống kiểm tra giới hạn số lượng kênh kết nối theo gói dịch vụ của Agency, lưu khóa kết nối đã mã hóa an toàn vào Workspace hiện tại và tự động duy trì làm mới phiên kết nối (BR-53).",
        "in_req": "Chọn 1 trong 4 nền tảng (Facebook, Instagram, TikTok hoặc Threads) và xác nhận cấp quyền đăng bài trên cửa sổ của nền tảng đó.",
        "in_opt": "Chọn trang Fanpage hoặc tài khoản doanh nghiệp cụ thể nếu người dùng quản lý nhiều trang.",
        "sys_data": "Lưu khóa kết nối OAuth2 đã mã hóa, tên trang/kênh, ảnh đại diện kênh và thời hạn hiệu lực token trong Workspace (BR-53).",
        "output": "Liên kết tài khoản mạng xã hội vào Workspace thành công và hiển thị thông báo MSG51.",
        "flow": [
            "Client hoặc Manager mở màn hình Kết nối Mạng xã hội (/social-accounts) trong Workspace.",
            "Người dùng bấm nút Kết nối bên cạnh nền tảng muốn thêm (Facebook, Instagram, TikTok hoặc Threads).",
            "Trên cửa sổ xác thực của mạng xã hội, người dùng đăng nhập, chọn trang của nhãn hàng và đồng ý cấp quyền đăng bài.",
            "Hệ thống lưu kết nối an toàn cho Workspace (BR-53) và hiển thị tài khoản vừa thêm kèm thông báo MSG51."
        ],
        "abnormal": [
            "Nếu người dùng hủy cấp quyền giữa chừng hoặc mạng xã hội báo lỗi: Hệ thống hiển thị thông báo MSG54 để người dùng thử lại.",
            "Nếu người thao tác không có quyền Manager hoặc Client trong dự án: Hệ thống chặn thao tác và báo MSG07."
        ]
    },
    "3.8.2": {
        "summary": "Cho phép Client hoặc Manager ngắt kết nối một tài khoản mạng xã hội khỏi Workspace. Khi ngắt kết nối, hệ thống sẽ hủy các lịch hẹn đăng đang chờ của kênh đó nhưng vẫn giữ nguyên lịch sử và số liệu của các bài đã đăng trước đây.",
        "trigger": "Khi Client hoặc Manager bấm nút Ngắt kết nối (Disconnect) bên cạnh một tài khoản mạng xã hội trên trang Kết nối Mạng xã hội (/social-accounts) và xác nhận.",
        "interface": "Nút Ngắt kết nối trên từng tài khoản đã liên kết tại màn hình Kết nối Mạng xã hội (/social-accounts) kèm hộp thoại xác nhận.",
        "processing": "Hệ thống kiểm tra quyền của Client hoặc Manager trong Workspace (BR-20), xóa khóa kết nối OAuth của tài khoản đó, tự động hủy các bài viết đang xếp lịch chờ đăng (PENDING) vào kênh đó và giữ nguyên toàn bộ dữ liệu thống kê của những bài đã xuất bản thành công (BR-53).",
        "in_req": "Chọn tài khoản mạng xã hội đang kết nối và xác nhận Ngắt kết nối.",
        "in_opt": "Không bắt buộc.",
        "sys_data": "Thu hồi khóa kết nối, hủy các lịch hẹn đăng đang chờ của kênh đó và bảo toàn lịch sử bài đã đăng (BR-53).",
        "output": "Ngắt kết nối tài khoản mạng xã hội thành công và hiển thị thông báo MSG51.",
        "flow": [
            "Client hoặc Manager mở màn hình Kết nối Mạng xã hội (/social-accounts) và bấm Ngắt kết nối cạnh kênh cần gỡ.",
            "Người dùng bấm Đồng ý trên hộp thoại xác nhận.",
            "Hệ thống xóa khóa ủy quyền đăng bài và hủy các lịch đăng tự động đang chờ của kênh đó (BR-53).",
            "Hệ thống giữ nguyên lịch sử các bài đã đăng trước đây và hiển thị thông báo MSG51."
        ],
        "abnormal": [
            "Nếu tài khoản mạng xã hội đó đã được ngắt kết nối từ trước: Hệ thống hiển thị thông báo MSG01."
        ]
    },
    "3.8.3": {
        "summary": "Hiển thị bảng điều khiển tổng hợp toàn bộ các bài viết đã đăng thành công lên 4 mạng xã hội của dự án, kèm biểu đồ phân bổ theo nền tảng và tổng số lượt tương tác thu được.",
        "trigger": "Khi thành viên trong dự án mở màn hình Thống kê Bài đã đăng (/publish/dashboard).",
        "interface": "Màn hình Thống kê Bài đã đăng (/publish/dashboard) hiển thị tổng số bài đã xuất bản, tổng lượt tương tác (thích, bình luận, chia sẻ, lượt xem), biểu đồ so sánh hiệu quả giữa Facebook, Instagram, TikTok, Threads và danh sách các bài viết gần đây.",
        "processing": "Hệ thống kiểm tra quyền thành viên trong Workspace (BR-20), tổng hợp dữ liệu các bài viết ở trạng thái Đã xuất bản (PUBLISHED) cùng các chỉ số tương tác mới nhất được đồng bộ từ 4 mạng xã hội (BR-57) để hiển thị.",
        "in_req": "Mở màn hình Thống kê Bài đã đăng của Workspace.",
        "in_opt": "Lọc theo nền tảng (Facebook, Instagram, TikTok, Threads) hoặc theo khoảng thời gian đăng.",
        "sys_data": "Danh sách bài đã đăng và tổng hợp số liệu tương tác định kỳ từ API mạng xã hội (BR-57).",
        "output": "Hiển thị bảng thống kê tổng quan và danh sách các bài đã xuất bản.",
        "flow": [
            "Thành viên (Owner, Manager, Creator hoặc Client) mở màn hình Thống kê Bài đã đăng (/publish/dashboard).",
            "Hệ thống kiểm tra quyền truy cập trong dự án (BR-20).",
            "Hệ thống tổng hợp danh sách các bài viết đã xuất bản và số liệu tương tác từ 4 nền tảng (BR-57).",
            "Màn hình hiển thị các thẻ chỉ số tổng hợp, biểu đồ và danh sách bài đăng để người dùng theo dõi hiệu quả."
        ],
        "abnormal": [
            "Nếu dự án chưa có bài đăng nào xuất bản trong khoảng thời gian đang lọc: Hệ thống hiển thị thông báo MSG01."
        ]
    },
    "3.8.4": {
        "summary": "Xem chi tiết nội dung, hình ảnh/video, đường dẫn bài viết thực tế trên mạng xã hội (permalink) và các chỉ số tương tác cụ thể (lượt thích, bình luận, chia sẻ, lượt xem) của một bài đăng đã xuất bản.",
        "trigger": "Khi thành viên bấm vào một bài viết trong danh sách đã xuất bản để mở trang Chi tiết Bài đã đăng (/publish/posts/:id).",
        "interface": "Màn hình Chi tiết Bài đã đăng (/publish/posts/:id) hiển thị khung nội dung và ảnh/video đã đăng, nền tảng xuất bản, thời gian đăng, nút Mở xem bài gốc trên mạng xã hội, cùng các thẻ số liệu: Lượt thích/thả tim (Reactions), Bình luận (Comments), Chia sẻ (Shares) và Lượt xem (Views).",
        "processing": "Hệ thống kiểm tra quyền thành viên trong Workspace (BR-20), lấy thông tin bài đăng và số liệu tương tác đã đồng bộ gần nhất từ mạng xã hội đích (BR-57) để hiển thị chi tiết.",
        "in_req": "Chọn một bài viết đã xuất bản để xem chi tiết.",
        "in_opt": "Bấm nút Làm mới số liệu để cập nhật chỉ số tương tác mới nhất.",
        "sys_data": "Đường dẫn bài đăng gốc (permalink), thời điểm xuất bản và các chỉ số tương tác chi tiết (BR-57).",
        "output": "Hiển thị đầy đủ nội dung và kết quả tương tác của bài đăng.",
        "flow": [
            "Từ màn hình Thống kê Bài đã đăng (/publish/dashboard), người dùng bấm vào một bài viết cụ thể.",
            "Hệ thống kiểm tra quyền thành viên trong Workspace (BR-20).",
            "Hệ thống tải nội dung bài đăng, đường dẫn gốc và các chỉ số lượt thích, bình luận, chia sẻ, lượt xem (BR-57).",
            "Màn hình hiển thị chi tiết hiệu quả của bài viết đó."
        ],
        "abnormal": [
            "Nếu không tìm thấy bài đăng hoặc người dùng không thuộc dự án: Hệ thống hiển thị thông báo MSG01 hoặc MSG07."
        ]
    },
    "3.8.5": {
        "summary": "Cho phép Creator, Manager và Client xem trước giao diện hiển thị của bài viết (trên cả màn hình điện thoại và máy tính) theo đúng bố cục thực tế của từng mạng xã hội (Facebook, Instagram, TikTok, Threads) trước khi duyệt hoặc đăng bài.",
        "trigger": "Khi người dùng mở chế độ Xem trước Bài đăng (Preview Post) trong màn hình Xuất bản (/publish) hoặc Chi tiết Task.",
        "interface": "Khung Xem trước Bài đăng (/publish) gồm các tab chuyển đổi giữa Facebook (Feed / Story / Reels), Instagram (Post / Reels / Story), TikTok Video và Threads Post, nút chuyển chế độ Điện thoại / Máy tính, cùng bảng kiểm tra quy chuẩn ảnh/video và giới hạn số ký tự.",
        "processing": "Hệ thống dựng khung giao diện mô phỏng giống hệt cách bài viết sẽ xuất hiện trên từng mạng xã hội, đồng thời tự động kiểm tra độ dài văn bản, tỷ lệ khung hình (1:1, 9:16, 16:9), định dạng và thời lượng video xem có đạt chuẩn của nền tảng đó hay không (BR-55).",
        "in_req": "Chọn bài viết / Task cần xem trước và chọn nền tảng mạng xã hội muốn mô phỏng.",
        "in_opt": "Chuyển đổi giữa khung nhìn Điện thoại (Mobile) và Máy tính (Desktop).",
        "sys_data": "Kiểm tra tự động giới hạn ký tự, tỷ lệ khung hình ảnh/video và thời lượng theo quy định của từng nền tảng (BR-55).",
        "output": "Hiển thị bản mô phỏng bài đăng trực quan (hoặc cảnh báo MSG52 nếu ảnh/video/caption chưa đúng chuẩn của nền tảng đó).",
        "flow": [
            "Creator, Manager hoặc Client mở bài viết trong màn hình Xuất bản (/publish) và bấm nút Xem trước (Preview).",
            "Người dùng chọn tab nền tảng muốn kiểm tra (Facebook, Instagram, TikTok hoặc Threads).",
            "Hệ thống kiểm tra định dạng ảnh/video, tỷ lệ khung hình và độ dài caption theo quy chuẩn của nền tảng đó (BR-55).",
            "Màn hình hiển thị khung mô phỏng bài đăng thực tế (và báo rõ nếu có thông số nào cần chỉnh lại theo MSG52)."
        ],
        "abnormal": [
            "Nếu văn bản vượt quá số ký tự cho phép (ví dụ quá 500 ký tự trên Threads) hoặc video sai tỷ lệ khung hình: Hệ thống hiển thị cảnh báo đỏ MSG52 ngay bên dưới để người dùng sửa lại trước khi đăng."
        ]
    },
    "3.8.6": {
        "summary": "Cho phép Creator hoặc Manager hẹn ngày giờ cụ thể để hệ thống tự động xuất bản bài viết đã được phê duyệt lên các tài khoản mạng xã hội đã chọn.",
        "trigger": "Khi Creator hoặc Manager chọn một bài viết đã duyệt trên màn hình Xuất bản (/publish), chọn kênh mạng xã hội cùng ngày giờ đăng và bấm Lên lịch đăng.",
        "interface": "Màn hình Hẹn giờ Đăng bài (/publish, /calendar) gồm ô chọn Task đã duyệt, tích chọn các tài khoản mạng xã hội đích (Facebook, Instagram, TikTok, Threads), ô chọn Ngày và Giờ hẹn đăng (hiển thị theo múi giờ chuẩn của Workspace) và nút Xác nhận lên lịch.",
        "processing": "Hệ thống kiểm tra bài viết bắt buộc phải hoàn tất quy trình duyệt 3 cấp (trạng thái APPROVED - BR-34, BR-54), đã đạt kiểm tra an toàn nội dung (BR-42), đúng quy chuẩn kỹ thuật của nền tảng đích (BR-55) và tài khoản người đăng không bị gắn cờ vi phạm (BR-63). Thời gian hẹn giờ được tính theo múi giờ của Workspace (BR-22, phải cách hiện tại ít nhất 5 phút - BR-56) và đưa vào hàng đợi chờ đăng tự động.",
        "in_req": "Chọn bài viết đã được phê duyệt (APPROVED), chọn ít nhất 1 tài khoản mạng xã hội đã kết nối và chọn Ngày giờ hẹn đăng trong tương lai.",
        "in_opt": "Tùy chọn cấu hình riêng cho từng nền tảng (như ảnh bìa Reels/TikTok).",
        "sys_data": "Kiểm tra điều kiện Đã duyệt (BR-54), quy đổi giờ hẹn theo múi giờ Workspace (BR-22) và tạo lịch chờ đăng ở trạng thái PENDING (BR-56).",
        "output": "Đặt lịch hẹn giờ đăng bài thành công và hiển thị thông báo MSG53.",
        "flow": [
            "Creator hoặc Manager mở màn hình Lên lịch Xuất bản (/publish) và chọn một bài viết đã hoàn tất phê duyệt.",
            "Người dùng tích chọn các trang mạng xã hội muốn đăng và chọn Ngày giờ xuất bản (theo múi giờ của Workspace - BR-22).",
            "Người dùng bấm nút Lên lịch đăng (Schedule Post).",
            "Hệ thống kiểm tra điều kiện phê duyệt (BR-54), định dạng tệp (BR-55), lưu vào hàng đợi hẹn giờ (BR-56) và hiển thị thông báo MSG53."
        ],
        "abnormal": [
            "Nếu bài viết chưa hoàn tất quy trình phê duyệt 3 cấp hoặc chưa qua kiểm tra an toàn nội dung: Hệ thống chặn lên lịch và báo MSG36 (BR-54).",
            "Nếu chọn thời gian hẹn giờ ở trong quá khứ hoặc định dạng ảnh/video không hợp lệ: Hệ thống báo lỗi MSG03 hoặc MSG52."
        ]
    },
    "3.8.7": {
        "summary": "Theo dõi trạng thái của các bài đăng trong hàng đợi xuất bản theo thời gian thực (Đang chờ đến giờ -> Đang đăng -> Đã đăng thành công -> Hoặc Gặp lỗi), hỗ trợ tự động thử lại khi lỗi mạng và cho phép bấm Thử đăng lại thủ công.",
        "trigger": "Khi thành viên mở màn hình Hàng đợi & Trạng thái Xuất bản (/publish) để kiểm tra tiến độ các bài hẹn giờ hoặc bấm nút Thử lại (Retry) trên bài bị lỗi.",
        "interface": "Bảng Theo dõi Trạng thái Xuất bản hiển thị Tiêu đề bài viết, Kênh mạng xã hội đích, Giờ hẹn đăng, nhãn Trạng thái (PENDING, IN_PROGRESS, PUBLISHED, FAILED), lý do lỗi (nếu có) và nút Thử đăng lại (Retry).",
        "processing": "Hệ thống hiển thị trạng thái thực tế của từng lệnh đăng bài (BR-56). Đối với các bài gặp sự cố kết nối tạm thời từ phía mạng xã hội, hệ thống tự động thử đăng lại tối đa 3 lần; nếu vẫn thất bại thì chuyển sang trạng thái Lỗi (FAILED) và cho phép Manager/Creator bấm Thử lại sau khi kiểm tra kết nối tài khoản.",
        "in_req": "Mở màn hình Theo dõi Trạng thái Xuất bản trong Workspace.",
        "in_opt": "Lọc theo trạng thái (Đang chờ / Đang đăng / Đã đăng / Bị lỗi) hoặc bấm nút Thử lại trên bài lỗi.",
        "sys_data": "Trạng thái tiến trình đăng bài, số lần đã tự động thử lại (tối đa 3 lần - BR-56) và thông báo phản hồi từ mạng xã hội.",
        "output": "Hiển thị trạng thái xuất bản cập nhật mới nhất của các bài đăng.",
        "flow": [
            "Thành viên mở màn hình Hàng đợi Xuất bản (/publish) trong Workspace.",
            "Hệ thống kiểm tra quyền truy cập (BR-20) và hiển thị danh sách các bài đang chờ đăng, đang xử lý, đã đăng hoặc bị lỗi (BR-56).",
            "Khi đến đúng giờ hẹn, hệ thống tự động chuyển bài sang Đang đăng và cập nhật thành Đã đăng (PUBLISHED) ngay khi hoàn tất.",
            "Nếu có bài báo trạng thái Lỗi (FAILED), người dùng có thể xem nguyên nhân và bấm nút Thử lại (Retry) để đăng lại."
        ],
        "abnormal": [
            "Nếu việc đăng bài bị lỗi do quyền kết nối mạng xã hội đã hết hạn: Hệ thống hiển thị thông báo MSG54 nhắc người dùng kết nối lại tài khoản mạng xã hội (3.8.1)."
        ]
    },
    "3.8.8": {
        "summary": "Xuất bản trực tiếp (hoặc theo lịch hẹn) một bài viết tiêu chuẩn (gồm văn bản, ảnh đơn, bộ nhiều ảnh hoặc video) lên trang Facebook Page đã kết nối của dự án.",
        "trigger": "Khi Creator hoặc Manager chọn đăng bài lên Facebook Page tại màn hình Xuất bản (/publish) hoặc khi đến giờ hẹn đăng tự động.",
        "interface": "Tùy chọn Xuất bản Facebook Post trên màn hình Xuất bản (/publish) hiển thị trang Facebook Page đích, nội dung văn bản, ảnh/video đính kèm và nút Đăng lên Facebook.",
        "processing": "Hệ thống kiểm tra bài viết đã được phê duyệt (BR-54), đạt kiểm tra an toàn nội dung (BR-42), kết nối Facebook Page còn hiệu lực (BR-53) và tệp ảnh/video đúng chuẩn của Facebook (BR-55). Sau đó, hệ thống đẩy bài viết lên Facebook Page, lưu lại mã bài đăng cùng đường dẫn bài viết (permalink) và chuyển trạng thái sang Đã xuất bản (BR-56).",
        "in_req": "Bài viết đã được phê duyệt (APPROVED) và trang Facebook Page đích đã kết nối trong Workspace.",
        "in_opt": "Chọn đăng ngay lập tức hoặc đăng theo giờ hẹn (3.8.6).",
        "sys_data": "Kiểm tra điều kiện duyệt bài (BR-54), gửi bài qua Facebook API và lưu đường dẫn bài đăng thực tế (BR-56).",
        "output": "Đăng bài lên Facebook Page thành công và hiển thị thông báo MSG53.",
        "flow": [
            "Creator hoặc Manager chọn bài viết đã duyệt trên màn hình Xuất bản (/publish) và chọn kênh Facebook Page.",
            "Người dùng bấm nút Đăng ngay (hoặc hệ thống tự kích hoạt khi đến đúng giờ hẹn).",
            "Hệ thống kiểm tra trạng thái phê duyệt (BR-54), quy chuẩn tệp đính kèm (BR-55) và gửi nội dung lên Facebook Page.",
            "Hệ thống lưu lại đường dẫn bài đăng từ Facebook, cập nhật trạng thái Đã xuất bản (PUBLISHED) và hiển thị thông báo MSG53."
        ],
        "abnormal": [
            "Nếu tệp ảnh/video không đúng định dạng hỗ trợ của Facebook: Hệ thống báo lỗi MSG52.",
            "Nếu kết nối Facebook Page bị hết hạn hoặc lỗi đường truyền: Hệ thống báo thông báo MSG54."
        ]
    },
    "3.8.9": {
        "summary": "Xuất bản tin ngắn 24 giờ (Facebook Story dạng ảnh dọc hoặc video ngắn tỷ lệ 9:16) lên trang Facebook Page đã kết nối của dự án.",
        "trigger": "Khi Creator hoặc Manager chọn xuất bản định dạng Facebook Story trên màn hình Xuất bản (/publish) hoặc khi đến lịch hẹn.",
        "interface": "Tùy chọn Xuất bản Facebook Story trên màn hình Xuất bản (/publish) hiển thị khung xem trước dọc 9:16, trang Facebook Page đích và nút Đăng Story.",
        "processing": "Hệ thống kiểm tra bài đăng đã được phê duyệt (BR-54) và kiểm tra tệp ảnh/video đáp ứng đúng tỷ lệ khung hình dọc 9:16 cùng thời lượng cho phép của Facebook Story (BR-55). Sau đó, hệ thống tải tệp lên Facebook Page Story và cập nhật trạng thái hoàn tất (BR-56).",
        "in_req": "Ấn phẩm ảnh hoặc video dọc (9:16) đã được phê duyệt và trang Facebook Page đích.",
        "in_opt": "Chọn đăng ngay hoặc hẹn giờ đăng.",
        "sys_data": "Kiểm tra tỷ lệ khung hình 9:16, thời lượng Story (BR-55) và ghi nhận mã Story đã đăng trên Facebook (BR-56).",
        "output": "Xuất bản Facebook Story thành công và hiển thị thông báo MSG53.",
        "flow": [
            "Creator hoặc Manager chọn đầu việc Facebook Story đã được phê duyệt trong màn hình Xuất bản (/publish).",
            "Người dùng chọn trang Facebook Page đích và bấm Đăng Story.",
            "Hệ thống kiểm tra điều kiện phê duyệt (BR-54) và quy chuẩn khung hình dọc 9:16 của tệp (BR-55).",
            "Hệ thống xuất bản lên Facebook Story, lưu trạng thái Đã đăng và hiển thị thông báo MSG53."
        ],
        "abnormal": [
            "Nếu tệp video dài quá giới hạn Story hoặc sai tỷ lệ khung hình: Hệ thống báo lỗi MSG52.",
            "Nếu kết nối Facebook gặp lỗi: Hệ thống báo thông báo MSG54."
        ]
    },
    "3.8.10": {
        "summary": "Xuất bản video ngắn định dạng dọc (Facebook Reels) kèm mô tả (caption) lên trang Facebook Page đã kết nối của dự án.",
        "trigger": "Khi Creator hoặc Manager chọn xuất bản định dạng Facebook Reels trên màn hình Xuất bản (/publish) hoặc khi đến giờ hẹn đăng.",
        "interface": "Tùy chọn Xuất bản Facebook Reels trên màn hình Xuất bản (/publish) hiển thị trình phát video dọc 9:16, ô mô tả Reels, trang Facebook Page đích và nút Đăng Reels.",
        "processing": "Hệ thống kiểm tra đầu việc đã được phê duyệt (BR-54), kiểm tra video đạt chuẩn Reels (định dạng MP4/MOV, tỷ lệ 9:16, thời lượng 3–90 giây - BR-55), sau đó tải video lên Facebook Reels và cập nhật trạng thái xuất bản cùng đường dẫn video (BR-56).",
        "in_req": "Video ngắn tỷ lệ 9:16 đã được phê duyệt, nội dung mô tả (caption) và trang Facebook Page đích.",
        "in_opt": "Chọn ảnh bìa (thumbnail) cho video Reels.",
        "sys_data": "Kiểm tra thời lượng video Reels (3–90 giây), tỷ lệ 9:16 (BR-55) và lưu đường dẫn Reels sau khi đăng (BR-56).",
        "output": "Xuất bản video Facebook Reels thành công và hiển thị thông báo MSG53.",
        "flow": [
            "Creator hoặc Manager chọn đầu việc Facebook Reels đã được phê duyệt tại màn hình Xuất bản (/publish).",
            "Người dùng kiểm tra video, lời bình (caption), chọn trang Facebook Page và bấm Đăng Reels.",
            "Hệ thống kiểm tra điều kiện phê duyệt (BR-54) và thông số kỹ thuật video Reels (BR-55).",
            "Hệ thống tải video lên Facebook Reels, cập nhật trạng thái Đã xuất bản (BR-56) và hiển thị thông báo MSG53."
        ],
        "abnormal": [
            "Nếu video không đúng tỷ lệ dọc hoặc vượt quá thời lượng Reels cho phép: Hệ thống báo lỗi MSG52.",
            "Nếu quá trình tải video lên Facebook bị gián đoạn: Hệ thống tự động thử lại và báo MSG54 nếu vẫn lỗi."
        ]
    },
    "3.8.11": {
        "summary": "Xuất bản bài đăng ảnh đơn hoặc bộ nhiều ảnh xoay vòng (Carousel) kèm lời bình (caption) và bộ hashtag lên tài khoản Instagram Business đã kết nối.",
        "trigger": "Khi Creator hoặc Manager chọn xuất bản bài đăng Instagram Post trên màn hình Xuất bản (/publish) hoặc khi đến lịch hẹn.",
        "interface": "Tùy chọn Xuất bản Instagram Post hiển thị ảnh đơn hoặc bộ ảnh Carousel, nội dung caption kèm hashtag, tài khoản Instagram Business đích và nút Đăng lên Instagram.",
        "processing": "Hệ thống kiểm tra bài đăng đã được phê duyệt (BR-54), kiểm tra định dạng và tỷ lệ khung hình ảnh theo chuẩn của Instagram (BR-55), sau đó khởi tạo gói hình ảnh và xuất bản chính thức lên tài khoản Instagram Business đã chọn (BR-56).",
        "in_req": "Ít nhất 1 hình ảnh đã được phê duyệt, nội dung caption và tài khoản Instagram Business đích.",
        "in_opt": "Sắp xếp thứ tự các ảnh trong bộ ảnh xoay vòng (Carousel).",
        "sys_data": "Kiểm tra quy chuẩn ảnh Instagram (BR-55), đăng bài qua Instagram API và lưu đường dẫn bài đăng (BR-56).",
        "output": "Xuất bản bài đăng Instagram Post thành công và hiển thị thông báo MSG53.",
        "flow": [
            "Creator hoặc Manager chọn bài viết Instagram đã được phê duyệt trên màn hình Xuất bản (/publish).",
            "Người dùng kiểm tra hình ảnh, nội dung caption và bấm Đăng lên Instagram.",
            "Hệ thống kiểm tra điều kiện phê duyệt (BR-54) và kích thước/định dạng ảnh hợp lệ (BR-55).",
            "Hệ thống đăng bài lên Instagram Business, lưu lại đường dẫn bài viết (BR-56) và hiển thị thông báo MSG53."
        ],
        "abnormal": [
            "Nếu bài đăng Instagram không có hình ảnh đính kèm hoặc ảnh sai tỷ lệ cho phép: Hệ thống báo lỗi MSG52.",
            "Nếu phiên kết nối Instagram hết hạn: Hệ thống báo thông báo MSG54."
        ]
    },
    "3.8.12": {
        "summary": "Xuất bản video ngắn lên mục Instagram Reels kèm ảnh bìa (cover) và nội dung caption thông qua tài khoản Instagram Business đã kết nối.",
        "trigger": "Khi Creator hoặc Manager chọn xuất bản Instagram Reels trên màn hình Xuất bản (/publish) hoặc khi đến giờ hẹn đăng.",
        "interface": "Tùy chọn Xuất bản Instagram Reels hiển thị video dọc 9:16, khung chọn ảnh bìa (Cover frame), nội dung caption/hashtag và nút Đăng Instagram Reels.",
        "processing": "Hệ thống kiểm tra đầu việc đã hoàn tất phê duyệt (BR-54), kiểm tra video đạt chuẩn Instagram Reels (định dạng MP4/MOV, tỷ lệ khung hình dọc 9:16, thời lượng hợp lệ - BR-55), sau đó tải video lên Instagram, chờ xử lý xong và kích hoạt xuất bản (BR-56).",
        "in_req": "Video ngắn tỷ lệ 9:16 đã được phê duyệt, nội dung caption và tài khoản Instagram Business đích.",
        "in_opt": "Chọn khung hình làm ảnh bìa (Cover) và tùy chọn chia sẻ đồng thời lên bảng tin chính (Feed).",
        "sys_data": "Kiểm tra chuẩn video Instagram Reels (BR-55), theo dõi tiến trình xử lý video và lưu đường dẫn bài đăng (BR-56).",
        "output": "Xuất bản video Instagram Reels thành công và hiển thị thông báo MSG53.",
        "flow": [
            "Creator hoặc Manager chọn đầu việc Instagram Reels đã được duyệt trên màn hình Xuất bản (/publish).",
            "Người dùng chọn tài khoản Instagram Business, kiểm tra ảnh bìa cùng caption và bấm Đăng Reels.",
            "Hệ thống kiểm tra trạng thái duyệt (BR-54) và thông số kỹ thuật của video (BR-55).",
            "Hệ thống xuất bản video lên Instagram Reels, cập nhật trạng thái Đã đăng (BR-56) và hiển thị thông báo MSG53."
        ],
        "abnormal": [
            "Nếu định dạng video hoặc tỷ lệ khung hình không đạt chuẩn Instagram Reels: Hệ thống báo lỗi MSG52.",
            "Nếu máy chủ Instagram phản hồi lỗi: Hệ thống báo thông báo MSG54."
        ]
    },
    "3.8.13": {
        "summary": "Xuất bản hình ảnh hoặc video ngắn 24 giờ lên mục Tin (Instagram Story) của tài khoản Instagram Business đã kết nối.",
        "trigger": "Khi Creator hoặc Manager chọn xuất bản Instagram Story trên màn hình Xuất bản (/publish) hoặc khi đến giờ hẹn đăng.",
        "interface": "Tùy chọn Xuất bản Instagram Story hiển thị khung xem trước toàn màn hình dọc 9:16, tài khoản Instagram Business đích và nút Đăng Story.",
        "processing": "Hệ thống kiểm tra ấn phẩm đã được phê duyệt (BR-54) và đạt đúng tỷ lệ hiển thị dọc 9:16 cùng giới hạn thời lượng của Instagram Story (BR-55), sau đó đẩy ấn phẩm lên Instagram Story và cập nhật trạng thái hoàn tất (BR-56).",
        "in_req": "Hình ảnh hoặc video dọc 9:16 đã được phê duyệt và tài khoản Instagram Business đích.",
        "in_opt": "Chọn đăng ngay hoặc hẹn giờ đăng.",
        "sys_data": "Kiểm tra quy chuẩn 9:16 của Instagram Story (BR-55) và lưu trạng thái xuất bản thành công (BR-56).",
        "output": "Xuất bản Instagram Story thành công và hiển thị thông báo MSG53.",
        "flow": [
            "Creator hoặc Manager chọn đầu việc Instagram Story đã duyệt tại màn hình Xuất bản (/publish).",
            "Người dùng chọn tài khoản Instagram Business đích và bấm Đăng Story.",
            "Hệ thống kiểm tra trạng thái phê duyệt (BR-54) và định dạng tệp 9:16 (BR-55).",
            "Hệ thống đăng ấn phẩm lên Instagram Story và hiển thị thông báo MSG53."
        ],
        "abnormal": [
            "Nếu tệp ảnh/video sai kích thước hoặc vượt quá thời lượng Story: Hệ thống báo lỗi MSG52.",
            "Nếu kết nối tài khoản Instagram bị gián đoạn: Hệ thống báo thông báo MSG54."
        ]
    },
    "3.8.14": {
        "summary": "Xuất bản video ngắn kèm mô tả (caption), thẻ hashtag và các tùy chọn tương tác (cho phép bình luận, Duet, Stitch) lên tài khoản TikTok đã kết nối của dự án.",
        "trigger": "Khi Creator hoặc Manager chọn xuất bản video lên TikTok tại màn hình Xuất bản (/publish) hoặc khi đến giờ hẹn đăng.",
        "interface": "Tùy chọn Xuất bản TikTok Video hiển thị trình phát video dọc 9:16, ô mô tả kèm hashtag, thiết lập quyền hiển thị (Công khai / Bạn bè / Riêng tư), nút bật/tắt Bình luận / Duet / Stitch và nút Đăng lên TikTok.",
        "processing": "Hệ thống kiểm tra đầu việc đã hoàn tất phê duyệt (BR-54) và kiểm tra video đáp ứng đúng quy chuẩn của TikTok (định dạng MP4/MOV/WebM, tỷ lệ khung hình dọc, thời lượng và dung lượng hợp lệ - BR-55). Sau đó, hệ thống tải video lên TikTok theo từng phân đoạn ổn định và lưu mã bài đăng (BR-56).",
        "in_req": "Tệp video đã được phê duyệt, nội dung mô tả (caption) và tài khoản TikTok đích.",
        "in_opt": "Cài đặt quyền riêng tư (Public/Friends/Private) và bật/tắt cho phép Comment, Duet, Stitch.",
        "sys_data": "Kiểm tra quy chuẩn video TikTok (BR-55), tải video lên TikTok API và lưu đường dẫn bài đăng (BR-56).",
        "output": "Xuất bản video lên TikTok thành công và hiển thị thông báo MSG53.",
        "flow": [
            "Creator hoặc Manager chọn đầu việc TikTok Video đã duyệt tại màn hình Xuất bản (/publish).",
            "Người dùng chọn tài khoản TikTok đích, cấu hình tùy chọn tương tác (Bình luận, Duet, Stitch) và bấm Đăng lên TikTok.",
            "Hệ thống kiểm tra điều kiện phê duyệt (BR-54) và định dạng/thời lượng video (BR-55).",
            "Hệ thống tải video lên TikTok, cập nhật trạng thái Đã xuất bản (BR-56) và hiển thị thông báo MSG53."
        ],
        "abnormal": [
            "Nếu tệp video sai định dạng hoặc caption vượt quá độ dài cho phép của TikTok: Hệ thống báo lỗi MSG52.",
            "Nếu phiên ủy quyền TikTok đã hết hạn hoặc lỗi kết nối: Hệ thống hiển thị thông báo MSG54."
        ]
    },
    "3.8.15": {
        "summary": "Xuất bản bài viết văn bản ngắn (tối đa 500 ký tự) kèm hình ảnh hoặc video lên tài khoản mạng xã hội Threads đã kết nối của dự án.",
        "trigger": "Khi Creator hoặc Manager chọn xuất bản bài viết lên Threads tại màn hình Xuất bản (/publish) hoặc khi đến giờ hẹn đăng.",
        "interface": "Tùy chọn Xuất bản Threads Post hiển thị khung văn bản (kèm bộ đếm tối đa 500 ký tự), hình ảnh/video đính kèm, tài khoản Threads đích và nút Đăng lên Threads.",
        "processing": "Hệ thống kiểm tra bài viết đã được phê duyệt (BR-54), kiểm tra độ dài văn bản không vượt quá 500 ký tự và tệp ảnh/video đính kèm đúng chuẩn của Threads (BR-55), sau đó xuất bản bài viết lên Threads và lưu lại đường dẫn bài đăng (BR-56).",
        "in_req": "Nội dung bài viết đã được phê duyệt (tối đa 500 ký tự) và tài khoản Threads đích.",
        "in_opt": "Đính kèm hình ảnh hoặc video minh họa cho bài đăng Threads.",
        "sys_data": "Kiểm tra giới hạn 500 ký tự của Threads (BR-55), xuất bản qua Threads API và lưu đường dẫn bài đăng (BR-56).",
        "output": "Xuất bản bài viết lên Threads thành công và hiển thị thông báo MSG53.",
        "flow": [
            "Creator hoặc Manager chọn bài viết Threads đã được duyệt trên màn hình Xuất bản (/publish).",
            "Người dùng chọn tài khoản Threads đích, kiểm tra độ dài văn bản dưới 500 ký tự và bấm Đăng lên Threads.",
            "Hệ thống kiểm tra điều kiện phê duyệt (BR-54) và quy chuẩn bài đăng Threads (BR-55).",
            "Hệ thống xuất bản bài viết lên Threads, lưu đường dẫn bài đăng (BR-56) và hiển thị thông báo MSG53."
        ],
        "abnormal": [
            "Nếu nội dung văn bản dài quá 500 ký tự hoặc tệp đính kèm không hợp lệ: Hệ thống báo lỗi MSG52 để người dùng rút gọn lại.",
            "Nếu kết nối tài khoản Threads gặp sự cố: Hệ thống báo thông báo MSG54."
        ]
    },

    # ==================== 3.9 Subscription & Billing ====================
    "3.9.1": {
        "summary": "Cho phép Owner nâng cấp gói dịch vụ của Agency từ gói Cơ bản (Basic) lên gói cao hơn (Pro hoặc Enterprise) để mở rộng số lượng Workspace, số thành viên, dung lượng lưu trữ và lượng điểm AI Credit được cấp hàng tháng. (Hệ thống chỉ hỗ trợ nâng cấp lên gói cao hơn, không có luồng hạ cấp gói).",
        "trigger": "Khi Owner mở màn hình Gói đăng ký dịch vụ (/subscription/plans), chọn một gói cao hơn gói hiện tại và bấm Nâng cấp gói.",
        "interface": "Màn hình Các Gói Dịch vụ (/subscription/plans) hiển thị bảng so sánh quyền lợi giữa gói Basic, Pro và Enterprise (số lượng Workspace tối đa, số nhân sự, số kênh mạng xã hội, dung lượng kho và điểm AI Credit tặng kèm mỗi tháng), nhãn Gói hiện tại và nút Nâng cấp ngay.",
        "processing": "Hệ thống kiểm tra người thực hiện là Owner của Agency (BR-15) và kiểm tra gói được chọn có cấp bậc cao hơn gói hiện hành (BR-58). Sau đó, hệ thống tạo đơn hàng nâng cấp gói ở trạng thái Chờ thanh toán (PENDING - BR-59) và chuyển Owner sang màn hình quét mã VietQR SePay (3.9.2).",
        "in_req": "Owner chọn gói dịch vụ mục tiêu cao hơn gói hiện tại (Pro hoặc Enterprise) và kỳ hạn thanh toán.",
        "in_opt": "Thông tin xuất hóa đơn công ty (tên đơn vị, mã số thuế).",
        "sys_data": "Kiểm tra điều kiện chỉ nâng cấp lên gói cao hơn (BR-58), tạo đơn hàng chờ thanh toán kèm mã tham chiếu SePay (BR-59).",
        "output": "Tạo đơn hàng nâng cấp gói thành công (hiển thị MSG55) và chuyển sang màn hình Thanh toán SePay (3.9.2).",
        "flow": [
            "Owner mở màn hình Gói đăng ký dịch vụ (/subscription/plans) để xem bảng so sánh các gói.",
            "Owner chọn gói cao hơn gói đang dùng (ví dụ nâng từ Basic lên Pro hoặc Enterprise) và bấm Nâng cấp.",
            "Hệ thống kiểm tra quyền Owner (BR-15) và xác nhận gói mới có cấp bậc cao hơn gói hiện tại (BR-58).",
            "Hệ thống khởi tạo đơn hàng chờ thanh toán (BR-59), hiển thị thông báo MSG55 và chuyển sang màn hình quét mã QR SePay (3.9.2)."
        ],
        "abnormal": [
            "Nếu chọn gói trùng với gói đang dùng hoặc gói thấp hơn: Hệ thống không cho phép chọn và báo MSG36 (BR-58).",
            "Nếu người thao tác không phải là Owner của Agency: Hệ thống chặn thao tác và báo MSG07."
        ]
    },
    "3.9.2": {
        "summary": "Thực hiện thanh toán đơn hàng nâng cấp gói dịch vụ (3.9.1) hoặc mua thêm điểm AI Credit (3.9.5) bằng cách quét mã chuyển khoản ngân hàng VietQR qua cổng SePay / PayOS. Ngay khi chuyển khoản xong, hệ thống tự động xác nhận và kích hoạt quyền lợi ngay lập tức.",
        "trigger": "Khi Owner mở màn hình Thanh toán đơn hàng (/subscription/checkout), quét mã QR bằng ứng dụng ngân hàng để chuyển khoản và hệ thống nhận thông báo xác nhận từ SePay.",
        "interface": "Màn hình Thanh toán SePay (/subscription/checkout) hiển thị hình ảnh mã VietQR tự động điền sẵn số tiền và nội dung chuyển khoản, thông tin tài khoản nhận, đồng hồ đếm ngược thời gian hiệu lực đơn hàng và trạng thái tự động cập nhật khi thanh toán xong.",
        "processing": "Hệ thống hiển thị mã VietQR gắn với mã đơn hàng duy nhất. Khi Owner chuyển khoản thành công, cổng thanh toán SePay gửi thông báo (Webhook) về hệ thống. Hệ thống kiểm tra chữ ký bảo mật và số tiền khớp với đơn hàng, chuyển trạng thái đơn từ Chờ thanh toán (PENDING) sang Đã thanh toán (PAID), nâng cấp gói hoặc cộng điểm AI Credit ngay lập tức (đảm bảo chỉ cộng đúng 1 lần - BR-58, BR-59, BR-60) và tạo hóa đơn điện tử (BR-61).",
        "in_req": "Đơn hàng đang ở trạng thái Chờ thanh toán (PENDING) và giao dịch chuyển khoản ngân hàng đúng số tiền/nội dung trên mã VietQR.",
        "in_opt": "Không bắt buộc.",
        "sys_data": "Xác thực thông báo thanh toán từ SePay, chuyển đơn sang PAID (BR-59), mở rộng hạn mức gói/cộng điểm AI Credit (BR-58, BR-60) và xuất hóa đơn (BR-61).",
        "output": "Xác nhận thanh toán thành công, kích hoạt ngay gói dịch vụ hoặc điểm AI Credit mới và hiển thị thông báo MSG56.",
        "flow": [
            "Trên màn hình Thanh toán (/subscription/checkout), hệ thống hiển thị mã VietQR kèm số tiền và nội dung chuyển khoản của đơn hàng.",
            "Owner mở ứng dụng ngân hàng trên điện thoại, quét mã VietQR và xác nhận chuyển khoản.",
            "Cổng SePay tự động gửi thông báo xác nhận giao dịch về hệ thống BrandHub.",
            "Hệ thống kiểm tra giao dịch hợp lệ, chuyển đơn hàng sang Đã thanh toán (PAID - BR-59), cập nhật ngay gói cước/số dư AI Credit (BR-58, BR-60), tạo hóa đơn (BR-61) và hiển thị thông báo MSG56."
        ],
        "abnormal": [
            "Nếu quá thời gian chờ mà người dùng chưa chuyển khoản: Hệ thống tự động chuyển đơn hàng sang trạng thái Hết hạn (EXPIRED - MSG36) để người dùng tạo lại đơn mới khi cần."
        ]
    },
    "3.9.3": {
        "summary": "Cho phép Owner xem lại toàn bộ lịch sử các giao dịch thanh toán của Agency (nâng cấp gói cước và mua thêm điểm AI Credit) và tải hóa đơn điện tử định dạng PDF về máy để lưu trữ kế toán.",
        "trigger": "Khi Owner mở màn hình Lịch sử Hóa đơn (/subscription/invoices) hoặc bấm nút Tải hóa đơn PDF trên một giao dịch.",
        "interface": "Màn hình Lịch sử Hóa đơn (/subscription/invoices) gồm bộ lọc theo trạng thái và thời gian, bảng danh sách giao dịch (Mã hóa đơn, Nội dung thanh toán, Số tiền, Phương thức SePay VietQR, Trạng thái PAID/PENDING/EXPIRED, Ngày giao dịch) và nút Tải PDF.",
        "processing": "Hệ thống kiểm tra quyền Owner của Agency (BR-15), lấy danh sách seluruh đơn hàng và hóa đơn thanh toán của công ty (BR-61) để hiển thị và cho phép xuất tải tệp biên lai PDF.",
        "in_req": "Owner mở màn hình Lịch sử Hóa đơn của Agency.",
        "in_opt": "Lọc theo loại giao dịch (Nâng cấp gói / Mua AI Credit), trạng thái đơn hoặc khoảng ngày.",
        "sys_data": "Danh sách hóa đơn thanh toán bất biến của Agency (BR-61).",
        "output": "Hiển thị bảng lịch sử giao dịch và tải tệp hóa đơn PDF về máy.",
        "flow": [
            "Owner mở màn hình Lịch sử Hóa đơn (/subscription/invoices).",
            "Hệ thống xác nhận quyền Owner (BR-15) và tải danh sách các giao dịch của Agency (BR-61).",
            "Owner có thể lọc xem các đơn đã thanh toán thành công (PAID) hoặc tìm theo mã đơn.",
            "Khi Owner bấm nút Tải PDF trên một giao dịch đã thanh toán, hệ thống xuất tệp hóa đơn điện tử về máy."
        ],
        "abnormal": [
            "Nếu chưa có giao dịch nào khớp với bộ lọc: Hệ thống hiển thị thông báo MSG01."
        ]
    },
    "3.9.4": {
        "summary": "Giúp Owner và Manager theo dõi chi tiết số dư điểm AI Credit còn lại, lượng điểm đã sử dụng theo từng tính năng AI (Tạo Caption, Ảnh, Video, Đại sứ ảo) và theo từng Workspace hoặc thành viên.",
        "trigger": "Khi Owner hoặc Manager mở màn hình Theo dõi Điểm AI Credit (/credit).",
        "interface": "Màn hình Theo dõi AI Credit (/credit) hiển thị Tổng số dư điểm hiện có (tách rõ Điểm định kỳ trong gói tháng và Điểm mua thêm), biểu đồ mức tiêu thụ theo tính năng AI, bảng thống kê điểm đã dùng của từng Workspace và lịch sử trừ/hoàn điểm chi tiết.",
        "processing": "Hệ thống tổng hợp dữ liệu từ sổ theo dõi điểm AI Credit (BR-60), hiển thị rõ quy tắc ưu tiên trừ điểm định kỳ hàng tháng trước khi trừ sang điểm mua thêm, cũng như ghi nhận đầy đủ các khoản hoàn điểm tự động khi dịch vụ AI bị lỗi (BR-48).",
        "in_req": "Owner hoặc Manager mở màn hình Theo dõi Điểm AI Credit.",
        "in_opt": "Lọc lịch sử sử dụng điểm theo Workspace, theo thành viên hoặc theo kỳ tháng.",
        "sys_data": "Số dư điểm khả dụng, lịch sử trừ điểm/hoàn điểm (BR-48, BR-60) và đơn giá áp dụng tại thời điểm sử dụng (BR-64).",
        "output": "Hiển thị bảng thống kê số dư và nhật ký chi tiêu điểm AI Credit.",
        "flow": [
            "Owner hoặc Manager mở màn hình Theo dõi AI Credit (/credit).",
            "Hệ thống kiểm tra quyền truy cập và tải số dư cùng lịch sử giao dịch điểm từ sổ cái AI Credit (BR-60).",
            "Người dùng xem biểu đồ phân bổ điểm đã dùng cho Tạo Caption, Ảnh, Video và Đại sứ ảo.",
            "Người dùng có thể lọc theo từng Workspace để biết dự án nào đang sử dụng nhiều điểm nhất."
        ],
        "abnormal": [
            "Nếu chưa có lượt sử dụng AI nào trong khoảng thời gian đang lọc: Hệ thống hiển thị thông báo MSG01."
        ]
    },
    "3.9.5": {
        "summary": "Cho phép Owner mua thêm các gói nạp điểm AI Credit (Top-up Packs) khi công ty cần sử dụng AI nhiều hơn số điểm tặng sẵn hàng tháng trong gói đăng ký.",
        "trigger": "Khi Owner mở màn hình Mua thêm AI Credit (/credit), chọn một gói điểm nạp thêm và bấm Thanh toán.",
        "interface": "Khu vực Mua thêm Điểm AI Credit (/credit) hiển thị các gói điểm nạp sẵn (ví dụ gói 500, 2.000, 5.000 AI Credits) kèm mức giá VNĐ, số dư hiện tại và nút Mua ngay qua SePay.",
        "processing": "Hệ thống kiểm tra quyền Owner (BR-15), khởi tạo đơn hàng mua thêm điểm AI Credit ở trạng thái Chờ thanh toán (PENDING - BR-59) và chuyển sang màn hình quét mã VietQR SePay (3.9.2). Ngay khi thanh toán xong, số điểm mua thêm được cộng ngay vào quỹ điểm của Agency (BR-60).",
        "in_req": "Owner chọn gói điểm AI Credit cần mua thêm.",
        "in_opt": "Số lượng gói muốn mua.",
        "sys_data": "Tạo đơn hàng mua thêm điểm chờ thanh toán qua SePay (BR-59) và cộng vào quỹ điểm nạp thêm khi hoàn tất (BR-60).",
        "output": "Khởi tạo đơn hàng mua điểm AI Credit thành công (hiển thị MSG55) và chuyển sang màn hình quét mã VietQR SePay (3.9.2).",
        "flow": [
            "Owner mở màn hình Quản lý AI Credit (/credit) và chọn mục Mua thêm điểm (Top-up).",
            "Owner chọn gói số lượng điểm AI Credit phù hợp với nhu cầu và bấm Mua ngay.",
            "Hệ thống kiểm tra quyền Owner (BR-15) và tạo đơn hàng thanh toán mới (BR-59).",
            "Hệ thống hiển thị thông báo MSG55 và mở màn hình quét mã VietQR SePay (3.9.2) để hoàn tất thanh toán."
        ],
        "abnormal": [
            "Nếu người thao tác không phải là Owner của Agency: Hệ thống chặn thao tác và báo MSG07."
        ]
    },
    "3.9.6": {
        "summary": "Cho phép Owner đặt và điều chỉnh hạn mức sử dụng điểm AI Credit tối đa hàng tháng cho từng Workspace hoặc từng thành viên, giúp kiểm soát chi phí AI hợp lý giữa các dự án khách hàng.",
        "trigger": "Khi Owner mở phần Cài đặt Hạn mức AI Credit (/credit), nhập số điểm tối đa cho phép của từng Workspace và bấm Lưu hạn mức.",
        "interface": "Bảng Phân bổ Hạn mức AI Credit (/credit) hiển thị tổng quỹ điểm của Agency, danh sách các Workspace trực thuộc, số điểm mỗi Workspace đã dùng trong tháng, ô nhập Hạn mức tối đa (Quota) và nút Lưu thiết lập.",
        "processing": "Hệ thống kiểm tra quyền Owner (BR-15) và kiểm tra hạn mức mới nhập vào phải là số không âm, không vượt quá tổng quỹ điểm của Agency và không thấp hơn số điểm mà Workspace đó đã dùng trong kỳ hiện tại (BR-60). Sau đó, hệ thống lưu hạn mức mới để áp dụng ngay khi các Creator trong dự án đó gọi tính năng AI (BR-48).",
        "in_req": "Chọn Workspace (hoặc thành viên) và nhập Hạn mức điểm AI Credit tối đa được phép sử dụng.",
        "in_opt": "Bật thông báo nhắc nhở khi dự án sử dụng đạt 80% hạn mức.",
        "sys_data": "Kiểm tra tổng hạn mức với quỹ điểm của Agency và mức đã tiêu thụ trong kỳ (BR-48, BR-60).",
        "output": "Cập nhật hạn mức sử dụng điểm AI Credit thành công và hiển thị thông báo MSG57.",
        "flow": [
            "Owner mở phần Phân bổ Hạn mức trên màn hình Quản lý AI Credit (/credit).",
            "Owner nhập số điểm tối đa cho phép sử dụng đối với từng Workspace dự án rồi bấm Lưu.",
            "Hệ thống kiểm tra quyền Owner (BR-15) và đảm bảo hạn mức mới hợp lệ so với số dư của Agency và số điểm dự án đã dùng (BR-60).",
            "Hệ thống lưu hạn mức mới và hiển thị thông báo thành công (MSG57)."
        ],
        "abnormal": [
            "Nếu đặt hạn mức thấp hơn số điểm mà Workspace đó đã tiêu thụ trong tháng hoặc vượt quá quỹ điểm của Agency: Hệ thống báo lỗi giá trị không hợp lệ (MSG03)."
        ]
    },

    # ==================== 3.10 Admin Functions ====================
    "3.10.1": {
        "summary": "Cho phép Admin tạo và gửi thông báo chung trên toàn hệ thống (đến tất cả người dùng, hoặc lọc riêng theo nhóm Owner, theo gói cước Basic/Pro/Enterprise) qua thông báo trên ứng dụng và email.",
        "trigger": "Khi Admin mở màn hình Phát Thông báo Hệ thống (/admin), soạn tiêu đề cùng nội dung, chọn nhóm người nhận và bấm Phát thông báo.",
        "interface": "Màn hình Phát Thông báo trên cổng Admin (/admin) gồm ô nhập Tiêu đề thông báo, Nội dung chi tiết, chọn Mức độ (Thông tin / Bảo trì / Khẩn cấp), chọn Nhóm người nhận (Tất cả / Theo vai trò / Theo gói đăng ký) và nút Gửi thông báo.",
        "processing": "Hệ thống kiểm tra quyền Admin (BR-62), kiểm tra tiêu đề và nội dung không bị để trống, lọc danh sách người dùng khớp với nhóm đối tượng đã chọn, đẩy thông báo trực tiếp lên ứng dụng/email của người nhận và lưu vết vào nhật ký quản trị (BR-65).",
        "in_req": "Tiêu đề thông báo, Nội dung thông báo và Nhóm đối tượng người nhận.",
        "in_opt": "Mức độ ưu tiên của thông báo và đường dẫn đính kèm (nếu có).",
        "sys_data": "Lưu bản ghi thông báo hệ thống, gửi đến các tài khoản mục tiêu và ghi nhật ký Admin (BR-62, BR-65).",
        "output": "Phát thông báo toàn hệ thống thành công và hiển thị thông báo MSG58.",
        "flow": [
            "Admin mở mục Phát Thông báo Hệ thống trên cổng quản trị (/admin).",
            "Admin nhập Tiêu đề, Nội dung thông báo (ví dụ: lịch bảo trì hoặc tính năng mới) và chọn nhóm người dùng nhận tin.",
            "Admin bấm nút Phát thông báo.",
            "Hệ thống kiểm tra quyền Admin (BR-62), gửi thông báo tới nhóm người nhận, lưu nhật ký quản trị (BR-65) và hiển thị thông báo MSG58."
        ],
        "abnormal": [
            "Nếu để trống Tiêu đề hoặc Nội dung thông báo: Hệ thống báo lỗi MSG02.",
            "Nếu không có tài khoản nào thuộc nhóm bộ lọc người nhận đã chọn: Hệ thống báo MSG01."
        ]
    },
    "3.10.2": {
        "summary": "Hiển thị cho Admin bảng điều khiển thống kê toàn cảnh hoạt động của nền tảng BrandHub: tổng số người dùng, tổng số Agency & Workspace đang hoạt động, tổng số bài đã đăng lên 4 mạng xã hội, lưu lượng sử dụng AI và tổng doanh thu.",
        "trigger": "Khi Admin mở màn hình Tổng quan Quản trị Hệ thống (/admin).",
        "interface": "Màn hình Tổng quan Admin (/admin) hiển thị các thẻ chỉ số lớn (Tổng người dùng, Tổng Agency/Workspace, Tổng bài xuất bản, Lượt gọi AI, Tổng doanh thu) cùng biểu đồ tăng trưởng theo thời gian.",
        "processing": "Hệ thống kiểm tra quyền Admin (BR-62), tổng hợp số liệu thống kê người dùng, dự án, bài đăng và doanh thu từ các hóa đơn đã thanh toán (BR-61) để vẽ biểu đồ tổng quan.",
        "in_req": "Admin mở màn hình Tổng quan Hệ thống (/admin).",
        "in_opt": "Chọn khoảng thời gian xem thống kê (7 ngày, 30 ngày, theo quý, theo năm).",
        "sys_data": "Số liệu tổng hợp toàn nền tảng về người dùng, Agency, bài đăng, lượt dùng AI và doanh thu (BR-61, BR-62).",
        "output": "Hiển thị bảng điều khiển thống kê toàn nền tảng cho Admin.",
        "flow": [
            "Admin đăng nhập và mở màn hình Tổng quan Hệ thống (/admin).",
            "Hệ thống xác nhận quyền Admin toàn hệ thống (BR-62).",
            "Hệ thống tổng hợp các chỉ số vận hành và doanh thu trên toàn nền tảng (BR-61).",
            "Màn hình hiển thị các thẻ số liệu và biểu đồ tăng trưởng trực quan."
        ],
        "abnormal": [
            "Nếu tài khoản không có quyền Admin cố truy cập đường dẫn `/admin`: Hệ thống chặn truy cập và báo MSG07."
        ]
    },
    "3.10.3": {
        "summary": "Giúp Admin theo dõi tình trạng hoạt động và mức tiêu thụ tài nguyên (CPU, RAM, ổ cứng, độ trễ phản hồi và kết nối cơ sở dữ liệu) của các máy chủ dịch vụ theo thời gian thực để phát hiện sớm nếu có dịch vụ bị quá tải.",
        "trigger": "Khi Admin mở màn hình Giám sát Sức khỏe Hệ thống (/admin/system-health).",
        "interface": "Màn hình Giám sát Hệ thống (/admin/system-health) hiển thị trạng thái từng dịch vụ (Đang hoạt động tốt UP / Cảnh báo chậm DEGRADED / Ngừng phản hồi DOWN), thanh đo % CPU, % RAM, tình trạng hàng đợi xử lý và kết nối Cơ sở dữ liệu.",
        "processing": "Hệ thống kiểm tra quyền Admin (BR-62), thu thập chỉ số hoạt động trực tiếp từ các dịch vụ (API Gateway, Dịch vụ Nghiệp vụ, Dịch vụ Xuất bản, Dịch vụ AI) cùng các cơ sở dữ liệu để hiển thị lên màn hình giám sát.",
        "in_req": "Admin mở màn hình Giám sát Sức khỏe Hệ thống (/admin/system-health).",
        "in_opt": "Lọc xem theo từng dịch vụ hoặc bấm Làm mới số liệu tức thì.",
        "sys_data": "Trạng thái sống (UP/DOWN), mức sử dụng CPU, RAM, ổ cứng và độ trễ kết nối của từng dịch vụ (BR-62).",
        "output": "Hiển thị bảng giám sát tình trạng kỹ thuật của toàn bộ hệ thống theo thời gian thực.",
        "flow": [
            "Admin mở màn hình Giám sát Sức khỏe Hệ thống (/admin/system-health).",
            "Hệ thống kiểm tra quyền Admin (BR-62) và đọc các chỉ số đo lường mới nhất từ các máy chủ dịch vụ.",
            "Màn hình hiển thị trạng thái hoạt động, mức CPU/RAM và tốc độ phản hồi của từng thành phần.",
            "Admin có thể theo dõi trực tiếp để kịp thời xử lý nếu có dịch vụ nào báo quá tải."
        ],
        "abnormal": [
            "Nếu người truy cập không phải là Admin: Hệ thống chặn truy cập và báo MSG07."
        ]
    },
    "3.10.4": {
        "summary": "Cho phép Admin xem và xử lý Hàng đợi kiểm duyệt các nội dung bị gắn cờ nghi ngờ vi phạm chính sách cộng đồng (hoặc bài đăng của tài khoản đang bị theo dõi mức Cam), để quyết định Cho phép đăng hay Xác nhận vi phạm và gỡ bỏ.",
        "trigger": "Khi Admin mở màn hình Hàng đợi Kiểm duyệt Nội dung (/admin?view=moderation), xem xét một bài viết bị gắn cờ và bấm Cho phép hoặc Xác nhận vi phạm.",
        "interface": "Màn hình Hàng đợi Kiểm duyệt (/admin?view=moderation) hiển thị danh sách các bài viết/ấn phẩm bị cảnh báo, lý do bị gắn cờ cùng các từ ngữ nghi vấn (BR-42), thông tin người tạo và 2 nút quyết định: Cho phép lưu hành (Approve/Dismiss) hoặc Xác nhận vi phạm (Confirm Violation).",
        "processing": "Hệ thống kiểm tra quyền Admin (BR-62). Khi Admin bấm Cho phép lưu hành, hệ thống gỡ cờ cảnh báo để bài viết được tiếp tục xuất bản. Khi Admin bấm Xác nhận vi phạm, hệ thống chặn bài viết đó, ghi nhận lỗi vi phạm cho tài khoản người tạo (theo cơ chế 3 mức Vàng/Cam/Đỏ - BR-63) và lưu vào nhật ký kiểm toán (BR-65).",
        "in_req": "Chọn mục nội dung trong hàng đợi kiểm duyệt và chọn Quyết định xử lý (Cho phép lưu hành hoặc Xác nhận vi phạm).",
        "in_opt": "Ghi chú lý do kiểm duyệt hoặc mức cảnh cáo áp dụng.",
        "sys_data": "Cập nhật trạng thái kiểm duyệt nội dung (BR-42), liên kết xử lý mức cảnh cáo tài khoản (BR-63) và ghi nhật ký Admin (BR-65).",
        "output": "Xử lý mục kiểm duyệt thành công và hiển thị thông báo MSG58.",
        "flow": [
            "Admin mở màn hình Hàng đợi Kiểm duyệt Nội dung (/admin?view=moderation).",
            "Admin chọn một bài viết bị gắn cờ để xem chi tiết nội dung văn bản, hình ảnh và đoạn từ ngữ bị cảnh báo (BR-42).",
            "Admin đưa ra quyết định: bấm Cho phép lưu hành (nếu nội dung an toàn) hoặc bấm Xác nhận vi phạm kèm lý do.",
            "Hệ thống cập nhật trạng thái bài viết, áp dụng quy tắc xử lý vi phạm (BR-63), ghi nhật ký quản trị (BR-65) và hiển thị thông báo MSG58."
        ],
        "abnormal": [
            "Nếu xác nhận vi phạm nhưng bỏ trống lý do ghi nhận: Hệ thống báo lỗi MSG02.",
            "Nếu mục nội dung đó đã được một Admin khác xử lý xong trước đó: Hệ thống báo MSG36."
        ]
    },
    "3.10.5": {
        "summary": "Cho phép Admin ghi nhận mức cảnh cáo vi phạm (Vàng, Cam, Đỏ) hoặc gỡ cảnh cáo cho tài khoản người dùng theo quy tắc 3 mức: 3 cảnh cáo Vàng tự gộp thành 1 mức Cam (tài khoản bị gắn cờ kiểm duyệt trước khi đăng); vi phạm mức Đỏ hoặc đủ 3 mức Cam sẽ chuyển sang khóa tài khoản 30 ngày.",
        "trigger": "Khi Admin mở hồ sơ vi phạm của người dùng trên cổng quản trị (/admin?view=users), chọn mức cảnh cáo (hoặc gỡ cảnh cáo) kèm lý do và bấm Cập nhật.",
        "interface": "Hộp thoại Quản lý Vi phạm & Trạng thái Người dùng trên cổng Admin hiển thị lịch sử các lần cảnh cáo (Vàng / Cam / Đỏ), trạng thái hiện tại của tài khoản (ACTIVE, FLAGGED, DEACTIVATED), ô chọn thao tác xử lý, ô nhập lý do bắt buộc và nút Xác nhận.",
        "processing": "Hệ thống kiểm tra quyền Admin và đảm bảo Admin không tự phạt chính mình hoặc phạt một Admin khác (BR-62). Khi ghi nhận cảnh cáo mới: nếu tích lũy đủ 3 mức Vàng (YELLOW) thì tự động chuyển thành 1 mức Cam (ORANGE) và gắn cờ tài khoản sang FLAGGED (mọi bài đăng phải qua Admin duyệt ở 3.10.4); nếu nhận mức Đỏ (RED) hoặc đủ 3 mức Cam thì kích hoạt xét duyệt tạm khóa 30 ngày (BR-63). Mọi cảnh cáo sẽ tự hết hạn sau 30 ngày liên tiếp không vi phạm thêm.",
        "in_req": "Chọn tài khoản người dùng, chọn Mức xử lý vi phạm (Cảnh cáo Vàng / Cam / Đỏ hoặc Gỡ cảnh cáo) và nhập Lý do xử lý.",
        "in_opt": "Đính kèm mã bài viết hoặc bằng chứng vi phạm.",
        "sys_data": "Tự động quy đổi cấp độ cảnh cáo (3 Vàng -> 1 Cam -> Gắn cờ FLAGGED -> Tạm khóa 30 ngày theo BR-63) và lưu nhật ký kiểm toán (BR-65).",
        "output": "Cập nhật trạng thái vi phạm của tài khoản thành công và hiển thị thông báo MSG59.",
        "flow": [
            "Trên màn hình Quản lý Người dùng (/admin?view=users), Admin chọn tài khoản cần xử lý vi phạm.",
            "Admin chọn mức cảnh cáo (Vàng, Cam, Đỏ hoặc Gỡ cảnh cáo) và nhập rõ lý do cùng bằng chứng vi phạm.",
            "Admin bấm nút Xác nhận cập nhật.",
            "Hệ thống tự động tính toán mức cảnh cáo tích lũy và cập nhật trạng thái tài khoản theo quy tắc BR-63, lưu nhật ký Admin (BR-65) và hiển thị thông báo MSG59."
        ],
        "abnormal": [
            "Nếu bỏ trống ô lý do xử lý vi phạm: Hệ thống báo lỗi bắt buộc nhập (MSG02).",
            "Nếu Admin cố áp dụng mức phạt lên tài khoản của chính mình hoặc một Admin khác: Hệ thống chặn thao tác và báo MSG07 / MSG36 (BR-62)."
        ]
    },
    "3.10.6": {
        "summary": "Cho phép Admin xem, tìm kiếm và lọc danh sách toàn bộ tài khoản người dùng trên hệ thống theo họ tên, email, vai trò hệ thống hoặc trạng thái hoạt động.",
        "trigger": "Khi Admin mở màn hình Quản lý Người dùng (/admin?view=users).",
        "interface": "Màn hình Quản lý Người dùng (/admin?view=users) gồm ô tìm kiếm theo Tên/Email, bộ lọc theo Vai trò hệ thống (USER / ADMIN), lọc theo Trạng thái tài khoản (Đang hoạt động, Chờ xác thực, Đang gắn cờ, Tạm khóa, Đã xóa), bảng danh sách người dùng và nút Tạo tài khoản mới.",
        "processing": "Hệ thống kiểm tra quyền Admin (BR-62), truy xuất danh sách người dùng trên toàn nền tảng theo điều kiện tìm kiếm/bộ lọc và hiển thị kèm thông tin số lượng Agency/Workspace mà mỗi người đang tham gia.",
        "in_req": "Admin mở màn hình Quản lý Người dùng (/admin?view=users).",
        "in_opt": "Từ khóa tìm kiếm (họ tên, email) và bộ lọc theo vai trò hoặc trạng thái tài khoản.",
        "sys_data": "Danh sách tài khoản toàn hệ thống, trạng thái bảo mật, số lần cảnh cáo và ngày tạo (BR-62).",
        "output": "Hiển thị bảng danh sách người dùng toàn hệ thống cho Admin.",
        "flow": [
            "Admin mở tab Quản lý Người dùng (/admin?view=users) trên cổng quản trị.",
            "Hệ thống xác nhận quyền Admin (BR-62) và tải danh sách tài khoản người dùng.",
            "Admin nhập từ khóa email/họ tên hoặc lọc theo trạng thái tài khoản (ví dụ: đang bị gắn cờ FLAGGED hoặc tạm khóa).",
            "Màn hình hiển thị danh sách tài khoản khớp điều kiện để Admin xem chi tiết hoặc thao tác."
        ],
        "abnormal": [
            "Nếu không tìm thấy người dùng nào khớp với bộ lọc: Hệ thống hiển thị thông báo MSG01."
        ]
    },
    "3.10.7": {
        "summary": "Cho phép Admin chủ động tạo mới một tài khoản người dùng trực tiếp từ cổng quản trị và tự động gửi thông tin kích hoạt tài khoản qua email cho người đó.",
        "trigger": "Khi Admin bấm nút Tạo người dùng mới trên màn hình Quản lý Người dùng (/admin?view=users), điền thông tin tài khoản và bấm Tạo.",
        "interface": "Hộp thoại Tạo Người dùng Mới trên cổng Admin gồm ô nhập Họ và tên, Địa chỉ Email, chọn Vai trò hệ thống (USER hoặc ADMIN), Số điện thoại (tùy chọn) và nút Tạo tài khoản.",
        "processing": "Hệ thống kiểm tra quyền Admin (BR-62), kiểm tra định dạng email hợp lệ và email chưa từng tồn tại trên hệ thống (BR-01). Sau đó, hệ thống tạo tài khoản ở trạng thái chờ kích hoạt, tự động gửi thông tin đăng nhập/kích hoạt tạm thời qua email cho người dùng và ghi lại vào nhật ký quản trị (BR-65).",
        "in_req": "Họ và tên, Địa chỉ Email chưa từng đăng ký và Vai trò hệ thống.",
        "in_opt": "Số điện thoại liên hệ và ghi chú quản trị.",
        "sys_data": "Kiểm tra email duy nhất (BR-01), tạo tài khoản, gửi email kích hoạt và lưu nhật ký Admin (BR-65).",
        "output": "Tạo tài khoản người dùng mới thành công, gửi email kích hoạt và hiển thị thông báo MSG59.",
        "flow": [
            "Trên màn hình Quản lý Người dùng (/admin?view=users), Admin bấm nút Tạo người dùng mới.",
            "Admin nhập Họ tên, Địa chỉ Email và chọn Vai trò hệ thống cho tài khoản.",
            "Admin bấm nút Xác nhận tạo.",
            "Hệ thống kiểm tra email chưa bị trùng (BR-01), tạo tài khoản mới, gửi email kích hoạt cho người dùng (BR-65) và hiển thị thông báo MSG59."
        ],
        "abnormal": [
            "Nếu để trống Họ tên/Email hoặc nhập sai định dạng email: Hệ thống báo lỗi MSG02 hoặc MSG04.",
            "Nếu địa chỉ email này đã có tài khoản trên hệ thống: Hệ thống báo lỗi email đã tồn tại (MSG08)."
        ]
    },
    "3.10.8": {
        "summary": "Cho phép Admin chỉnh sửa thông tin hồ sơ hành chính (họ tên, số điện thoại) và phân quyền cấp hệ thống của tài khoản người dùng, đồng thời giữ cố định email gốc và ngăn việc tự hạ quyền Admin của chính mình.",
        "trigger": "Khi Admin chọn Chỉnh sửa trên một tài khoản tại màn hình Quản lý Người dùng (/admin?view=users), thay đổi thông tin và bấm Lưu.",
        "interface": "Hộp thoại Chỉnh sửa Người dùng trên cổng Admin gồm ô sửa Họ và tên, Số điện thoại, chọn Vai trò hệ thống, ô Email (khóa chỉ đọc) và nút Lưu thay đổi.",
        "processing": "Hệ thống kiểm tra quyền Admin (BR-62), giữ nguyên địa chỉ email đăng nhập chính (BR-11), đồng thời chặn việc Admin tự gỡ quyền Admin của chính mình hoặc gỡ quyền của một Admin khác (BR-62). Sau khi lưu thông tin mới, hệ thống ghi nhận vào nhật ký quản trị (BR-65).",
        "in_req": "Chọn tài khoản cần sửa, nhập Họ và tên cùng Vai trò hệ thống hợp lệ.",
        "in_opt": "Cập nhật Số điện thoại và ghi chú quản trị.",
        "sys_data": "Bảo toàn email định danh (BR-11), bảo vệ quyền Admin (BR-62) và lưu nhật ký kiểm toán (BR-65).",
        "output": "Cập nhật thông tin tài khoản người dùng thành công và hiển thị thông báo MSG59.",
        "flow": [
            "Trên màn hình Quản lý Người dùng (/admin?view=users), Admin bấm nút Chỉnh sửa bên cạnh tài khoản cần cập nhật.",
            "Admin sửa lại Họ tên, Số điện thoại hoặc quyền hệ thống rồi bấm Lưu thay đổi.",
            "Hệ thống kiểm tra quy tắc bảo vệ tài khoản Admin (BR-62) và dữ liệu đầu vào hợp lệ.",
            "Hệ thống lưu thông tin cập nhật, ghi vào nhật ký quản trị (BR-65) và hiển thị thông báo MSG59."
        ],
        "abnormal": [
            "Nếu Admin cố tình tự hạ quyền Admin của chính mình hoặc sửa quyền của một Admin khác: Hệ thống chặn thao tác và báo MSG07 (BR-62).",
            "Nếu xóa trống ô Họ và tên: Hệ thống báo lỗi MSG02."
        ]
    },
    "3.10.9": {
        "summary": "Cho phép Admin tạm khóa (vô hiệu hóa 30 ngày) đối với tài khoản vi phạm nghiêm trọng. Khi bị tạm khóa, toàn bộ phiên đăng nhập của tài khoản đó bị đăng xuất ngay lập tức; sau khi hết hạn 30 ngày, hệ thống sẽ tự động mở khóa lại tài khoản.",
        "trigger": "Khi Admin bấm nút Tạm khóa tài khoản (Deactivate User) trên màn hình Quản lý Người dùng (/admin?view=users), nhập lý do khóa và xác nhận.",
        "interface": "Hộp thoại Tạm khóa Tài khoản trên cổng Admin gồm thông tin tài khoản vi phạm, thời hạn khóa (30 ngày), ô nhập Lý do khóa tài khoản bắt buộc và nút Xác nhận tạm khóa.",
        "processing": "Hệ thống kiểm tra quyền Admin và đảm bảo tài khoản bị khóa không phải là một Admin (BR-62). Khi xác nhận, hệ thống chuyển trạng thái tài khoản sang Tạm khóa (DEACTIVATED trong 30 ngày - BR-63), lập tức đăng xuất mọi thiết bị đang đăng nhập của người đó, chặn đăng nhập mới (BR-05) và lưu lý do vào nhật ký quản trị (BR-65). Khi hết 30 ngày, tiến trình tự động sẽ khôi phục tài khoản về trạng thái Hoạt động (ACTIVE).",
        "in_req": "Chọn tài khoản người dùng cần khóa và nhập Lý do tạm khóa tài khoản.",
        "in_opt": "Chọn mã biên bản vi phạm liên quan.",
        "sys_data": "Chuyển trạng thái tài khoản sang DEACTIVATED (kèm mốc tự mở lại sau 30 ngày - BR-63), thu hồi phiên đăng nhập (BR-05) và ghi nhật ký Admin (BR-65).",
        "output": "Tạm khóa tài khoản người dùng thành công và hiển thị thông báo MSG59.",
        "flow": [
            "Trên màn hình Quản lý Người dùng (/admin?view=users), Admin chọn tài khoản vi phạm và bấm Tạm khóa (Deactivate).",
            "Admin nhập lý do tạm khóa vào hộp thoại xác nhận và bấm Đồng ý.",
            "Hệ thống kiểm tra tài khoản đích không phải là Admin (BR-62), chuyển trạng thái sang Tạm khóa 30 ngày (BR-63) và thu hồi ngay mọi phiên đăng nhập của tài khoản đó (BR-05).",
            "Hệ thống lưu nhật ký quản trị (BR-65), gửi thông báo email cho người dùng và hiển thị thông báo MSG59."
        ],
        "abnormal": [
            "Nếu để trống ô lý do khóa tài khoản: Hệ thống báo lỗi MSG02.",
            "Nếu cố khóa tài khoản của chính mình hoặc một Admin khác, hoặc tài khoản đã bị khóa từ trước: Hệ thống chặn thao tác và báo MSG07 hoặc MSG36 (BR-62)."
        ]
    },
    "3.10.10": {
        "summary": "Cho phép Admin và Owner xem bảng đơn giá điểm AI Credit hiện hành của toàn hệ thống cho từng loại tính năng AI (Tạo Caption, Tạo Ảnh, Tạo Video, Tạo Đại sứ ảo, Gợi ý Hashtag).",
        "trigger": "Khi Admin hoặc Owner mở màn hình Bảng giá AI Credit (/credit/prices).",
        "interface": "Màn hình Bảng giá AI Credit (/credit/prices) hiển thị bảng danh mục các tính năng AI: Mã tính năng, Tên thao tác AI, Mô hình sử dụng, Đơn giá số điểm AI Credit trừ cho mỗi lượt gọi, Ngày cập nhật gần nhất và các nút Chỉnh sửa giá / Nhập CSV (chỉ hiển thị cho Admin).",
        "processing": "Hệ thống tải danh sách đơn giá điểm AI Credit đang áp dụng trên toàn nền tảng (BR-48, BR-64) và hiển thị công khai để Owner nắm rõ mức phí và Admin quản lý.",
        "in_req": "Admin hoặc Owner mở màn hình Bảng giá AI Credit (/credit/prices).",
        "in_opt": "Tìm kiếm theo tên tính năng AI.",
        "sys_data": "Danh mục tính năng AI và đơn giá điểm AI Credit hiện hành (BR-64).",
        "output": "Hiển thị bảng đơn giá tiêu hao điểm AI Credit của từng tính năng.",
        "flow": [
            "Admin hoặc Owner mở màn hình Bảng giá AI Credit (/credit/prices).",
            "Hệ thống kiểm tra quyền truy cập và tải bảng cấu hình đơn giá hiện tại từ cơ sở dữ liệu (BR-64).",
            "Màn hình hiển thị rõ mỗi lượt Tạo Caption, Tạo Ảnh, Tạo Video hay Tạo Đại sứ ảo sẽ tốn bao nhiêu điểm AI Credit.",
            "Nếu là Admin, màn hình hiển thị thêm công cụ sửa giá trực tiếp (3.10.11) hoặc nhập bảng giá từ file CSV (3.10.12)."
        ],
        "abnormal": [
            "Nếu từ khóa tìm kiếm không khớp với tính năng AI nào: Hệ thống hiển thị thông báo MSG01."
        ]
    },
    "3.10.11": {
        "summary": "Cho phép Admin chỉnh sửa trực tiếp số điểm AI Credit cần trừ cho từng tính năng AI trên bảng giá. Mức giá mới sẽ áp dụng cho các lượt sử dụng AI tiếp theo mà không làm thay đổi lịch sử các giao dịch đã trừ trước đó.",
        "trigger": "Khi Admin sửa số điểm đơn giá của một tính năng trên màn hình Bảng giá AI Credit (/credit/prices) và bấm Lưu cập nhật.",
        "interface": "Ô nhập chỉnh sửa Đơn giá điểm AI Credit (Unit Cost) ngay trên từng dòng tính năng tại màn hình Bảng giá AI Credit (/credit/prices) kèm nút Lưu thay đổi.",
        "processing": "Hệ thống kiểm tra quyền Admin (BR-62) và kiểm tra đơn giá mới phải là số nguyên dương hợp lệ. Sau khi lưu, đơn giá mới được áp dụng ngay cho các yêu cầu tạo AI mới (không làm thay đổi các giao dịch cũ hay các tiến trình đang chạy dở - BR-48, BR-64) và được ghi lại vào nhật ký quản trị (BR-65).",
        "in_req": "Chọn tính năng AI cần đổi giá và nhập Đơn giá điểm AI Credit mới (số nguyên lớn hơn 0).",
        "in_opt": "Ghi chú lý do điều chỉnh đơn giá.",
        "sys_data": "Cập nhật đơn giá mới cho các lượt gọi AI tiếp theo (BR-48, BR-64) và lưu nhật ký Admin (BR-65).",
        "output": "Cập nhật đơn giá AI Credit thành công và hiển thị thông báo MSG60.",
        "flow": [
            "Admin mở màn hình Bảng giá AI Credit (/credit/prices) và bấm Chỉnh sửa trên dòng tính năng cần đổi giá.",
            "Admin nhập số điểm AI Credit mới (ví dụ đổi từ 5 điểm sang 4 điểm) và bấm Lưu.",
            "Hệ thống kiểm tra quyền Admin (BR-62) và xác nhận đơn giá mới là số dương hợp lệ.",
            "Hệ thống lưu mức giá mới (BR-64), ghi nhật ký quản trị (BR-65) và hiển thị thông báo MSG60."
        ],
        "abnormal": [
            "Nếu nhập đơn giá bằng 0, số âm hoặc bỏ trống: Hệ thống báo lỗi giá trị không hợp lệ (MSG02, MSG03)."
        ]
    },
    "3.10.12": {
        "summary": "Cho phép Admin tải lên tệp bảng tính CSV để kiểm tra xem trước và cập nhật hàng loạt đơn giá điểm AI Credit cho nhiều tính năng cùng lúc một cách nhanh chóng và chính xác.",
        "trigger": "Khi Admin bấm nút Nhập bảng giá CSV trên màn hình Bảng giá AI Credit (/credit/prices), chọn tệp CSV, xem trước bảng đối chiếu và bấm Xác nhận áp dụng.",
        "interface": "Hộp thoại Nhập Bảng giá từ CSV gồm nút tải tệp mẫu chuẩn, khung chọn tệp `.csv` từ máy tính, bảng Xem trước các dòng dữ liệu đọc được từ tệp (hiển thị giá cũ -> giá mới hoặc báo đỏ dòng bị lỗi) và nút Xác nhận cập nhật.",
        "processing": "Hệ thống kiểm tra quyền Admin (BR-62), kiểm tra tệp tải lên đúng định dạng CSV và kiểm tra từng dòng dữ liệu (mã tính năng tồn tại, đơn giá là số nguyên dương). Nếu tất cả các dòng đều hợp lệ và Admin bấm xác nhận, hệ thống sẽ cập nhật đồng bộ toàn bộ bảng giá trong một lần (nếu có dòng lỗi thì giữ nguyên bảng giá cũ, không cập nhật nửa vời - BR-64) và lưu nhật ký quản trị (BR-65).",
        "in_req": "Tệp CSV đúng cấu trúc mẫu (chứa mã tính năng AI và đơn giá điểm mới) và bấm Xác nhận sau khi xem trước.",
        "in_opt": "Ghi chú đợt cập nhật bảng giá.",
        "sys_data": "Kiểm tra toàn bộ các dòng trong tệp CSV, áp dụng cập nhật đồng bộ toàn bộ bảng giá (BR-64) và lưu nhật ký Admin (BR-65).",
        "output": "Nhập và cập nhật bảng giá AI Credit từ CSV thành công, hiển thị thông báo MSG60.",
        "flow": [
            "Trên màn hình Bảng giá AI Credit (/credit/prices), Admin bấm nút Nhập từ CSV và chọn tệp `.csv` từ máy tính.",
            "Hệ thống đọc tệp, kiểm tra từng dòng và hiển thị bảng Xem trước (so sánh đơn giá hiện tại và đơn giá mới).",
            "Admin kiểm tra bảng xem trước và bấm nút Xác nhận áp dụng.",
            "Hệ thống cập nhật đồng bộ toàn bộ đơn giá mới (BR-64), ghi vào nhật ký quản trị (BR-65) và hiển thị thông báo MSG60."
        ],
        "abnormal": [
            "Nếu chọn tệp không phải định dạng `.csv` hoặc tệp quá dung lượng: Hệ thống báo lỗi MSG22.",
            "Nếu trong tệp CSV có dòng chứa mã tính năng không tồn tại hoặc đơn giá âm: Hệ thống chỉ rõ dòng bị lỗi và không áp dụng thay đổi cho đến khi Admin sửa lại tệp (MSG03)."
        ]
    },
    "3.10.13": {
        "summary": "Cung cấp cho Admin bảng điều khiển phân tích doanh thu toàn hệ thống, thống kê tổng tiền thực thu từ các giao dịch SePay đã thanh toán, biểu đồ doanh thu theo tháng/quý và tỷ trọng doanh thu giữa Gói đăng ký (Pro/Enterprise) với Gói mua thêm điểm AI Credit.",
        "trigger": "Khi Admin mở màn hình Thống kê Doanh thu (/admin?view=revenue).",
        "interface": "Màn hình Thống kê Doanh thu (/admin?view=revenue) hiển thị Tổng doanh thu thực thu, Số lượng đơn hàng thành công, biểu đồ cột/đường xu hướng doanh thu theo Ngày / Tuần / Tháng / Quý, biểu đồ tròn cơ cấu doanh thu (Gói đăng ký so với Nạp lẻ AI Credit) và danh sách các giao dịch gần nhất.",
        "processing": "Hệ thống kiểm tra quyền Admin (BR-62), tổng hợp toàn bộ các đơn hàng đã xác nhận thanh toán thành công qua cổng SePay (trạng thái PAID - BR-59, BR-61) để tính toán số liệu và vẽ biểu đồ theo kỳ thời gian Admin chọn.",
        "in_req": "Admin mở màn hình Thống kê Doanh thu (/admin?view=revenue).",
        "in_opt": "Bộ lọc khoảng thời gian (Tháng này, Quý này, Năm nay hoặc chọn từ ngày đến ngày) và lọc theo nguồn thu.",
        "sys_data": "Tổng hợp dữ liệu hóa đơn đã thanh toán (PAID) từ cổng SePay trên toàn hệ thống (BR-59, BR-61, BR-62).",
        "output": "Hiển thị bảng thống kê và biểu đồ phân tích doanh thu toàn nền tảng.",
        "flow": [
            "Admin mở tab Thống kê Doanh thu (/admin?view=revenue) trên cổng quản trị.",
            "Hệ thống xác nhận quyền Admin (BR-62) và truy xuất dữ liệu các giao dịch đã thanh toán (BR-59, BR-61).",
            "Admin chọn khoảng thời gian muốn xem (ví dụ theo tháng hoặc theo quý).",
            "Màn hình hiển thị tổng doanh thu, biểu đồ tăng trưởng và cơ cấu doanh thu chi tiết."
        ],
        "abnormal": [
            "Nếu trong khoảng thời gian đang chọn chưa phát sinh giao dịch thanh toán nào: Hệ thống hiển thị thông báo MSG01."
        ]
    },
    "3.10.14": {
        "summary": "Cho phép Admin xuất và tải xuống tệp báo cáo quản trị định dạng PDF (gồm Báo cáo Doanh thu & Giao dịch, Báo cáo Tăng trưởng Người dùng & Agency, hoặc Báo cáo Sử dụng AI Credit) theo khoảng thời gian chọn trước để lưu trữ hoặc trình bày.",
        "trigger": "Khi Admin chọn loại báo cáo cùng khoảng thời gian trên màn hình Báo cáo (/admin?view=revenue), rồi bấm nút Xuất Báo cáo PDF.",
        "interface": "Khu vực Xuất Báo cáo PDF trên cổng Admin gồm hộp chọn Loại báo cáo (Doanh thu / Người dùng & Agency / Tiêu thụ AI Credit), ô chọn Từ ngày – Đến ngày và nút Xuất tệp PDF.",
        "processing": "Hệ thống kiểm tra quyền Admin (BR-62), kiểm tra khoảng ngày hợp lệ, tổng hợp số liệu thống kê chính xác từ cơ sở dữ liệu (BR-61), dàn trang biểu đồ cùng bảng số liệu thành tệp tài liệu PDF chuyên nghiệp, ghi nhận vào nhật ký quản trị (BR-65) và tải tệp về máy cho Admin.",
        "in_req": "Chọn Loại báo cáo cần xuất và Khoảng thời gian (Từ ngày – Đến ngày).",
        "in_opt": "Nhập tiêu đề ghi chú hiển thị trên trang bìa báo cáo PDF.",
        "sys_data": "Tổng hợp số liệu báo cáo (BR-61, BR-62), tạo tệp PDF và ghi vết vào nhật ký quản trị (BR-65).",
        "output": "Kết xuất tệp báo cáo PDF thành công, tải về máy tính và hiển thị thông báo MSG60.",
        "flow": [
            "Trên cổng quản trị (/admin?view=revenue), Admin mở mục Xuất Báo cáo PDF.",
            "Admin chọn Loại báo cáo cần lấy (ví dụ Báo cáo Doanh thu) và chọn khoảng thời gian Từ ngày – Đến ngày.",
            "Admin bấm nút Xuất tệp PDF.",
            "Hệ thống kiểm tra quyền Admin (BR-62), tổng hợp dữ liệu thành tệp PDF chuẩn, lưu nhật ký hệ thống (BR-65), hiển thị thông báo MSG60 và tải tệp về máy."
        ],
        "abnormal": [
            "Nếu chọn ngày kết thúc sớm hơn ngày bắt đầu hoặc bỏ trống loại báo cáo: Hệ thống báo lỗi MSG02 hoặc MSG03."
        ]
    },
}
