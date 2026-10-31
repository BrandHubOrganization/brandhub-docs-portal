# -*- coding: utf-8 -*-
"""
Practical, simple, logical Vietnamese specifications for FRs in domains 3.6 and 3.7 (54 FRs).
"""

FRS_PART2 = {
    # ==================== 3.6 Content & Workflow ====================
    "3.6.1": {
        "summary": "Cho phép Manager bổ sung thông tin chi tiết cho một đầu việc (Task) vừa được tạo từ Chiến dịch hoặc Yêu cầu phát sinh, bao gồm yêu cầu bài viết (Brief), loại ấn phẩm, nền tảng đăng, hạn hoàn thành và tài liệu tham khảo.",
        "trigger": "Khi Manager mở một đầu việc trong danh sách Backlog của Workspace (/workspace/:id/tasks/:taskId), điền đầy đủ yêu cầu thực hiện và bấm Lưu.",
        "interface": "Bảng Chi tiết Công việc (/workspace/:id/tasks/:taskId) gồm ô sửa Tiêu đề Task, Mô tả yêu cầu chi tiết (Brief), chọn Loại nội dung (Bài đăng, Story, Reels, Video, Khảo sát), chọn Nền tảng đăng, đặt Hạn hoàn thành (Due Date), Mức độ ưu tiên, đính kèm Tư liệu tham khảo và nút Lưu.",
        "processing": "Hệ thống kiểm tra quyền Manager (BR-33), kiểm tra các thông tin bắt buộc và hạn hoàn thành hợp lệ theo múi giờ chuẩn của Workspace (BR-22), sau đó lưu thông tin và chuyển trạng thái công việc từ Chờ phân rã (BACKLOG) sang Cần làm (TODO).",
        "in_req": "Tiêu đề công việc, Yêu cầu chi tiết (Brief), Loại nội dung, ít nhất 1 Nền tảng đăng dự kiến và Hạn hoàn thành.",
        "in_opt": "Mức độ ưu tiên (Thấp / Trung bình / Cao / Khẩn cấp), Tư liệu tham khảo đính kèm và tùy chọn Yêu cầu Client duyệt bước cuối.",
        "sys_data": "Quy đổi thời gian theo múi giờ của Workspace (BR-22) và chuyển trạng thái Task từ BACKLOG sang TODO (BR-33).",
        "output": "Cập nhật đặc tả công việc thành công (hiển thị MSG37), sẵn sàng để giao cho Creator thực hiện.",
        "flow": [
            "Manager mở bảng công việc của Workspace (/workspace/:id/tasks) và chọn một Task đang ở cột Chờ phân rã (BACKLOG).",
            "Manager điền Yêu cầu chi tiết (Brief), chọn Loại ấn phẩm, Nền tảng mạng xã hội sẽ đăng và Hạn hoàn thành theo múi giờ dự án (BR-22).",
            "Manager bấm nút Lưu thông tin công việc.",
            "Hệ thống kiểm tra quyền Manager (BR-33), lưu đặc tả chi tiết, chuyển trạng thái Task sang Cần làm (TODO) và hiển thị thông báo MSG37."
        ],
        "abnormal": [
            "Nếu bỏ trống Yêu cầu chi tiết, chưa chọn kênh đăng hoặc đặt hạn hoàn thành không hợp lệ: Hệ thống báo lỗi MSG02 hoặc MSG03.",
            "Nếu người thao tác không phải là Manager của dự án: Hệ thống chặn chỉnh sửa và báo MSG07."
        ]
    },
    "3.6.2": {
        "summary": "Cho phép Manager phân công một đầu việc (Task) cho Creator phụ trách viết bài/thiết kế chính, đồng thời có thể gán thêm một người kiểm tra chất lượng nội bộ trong cùng Workspace.",
        "trigger": "Khi Manager mở chi tiết công việc (/workspace/:id/tasks/:taskId), chọn Creator thực hiện và bấm Giao việc.",
        "interface": "Khu vực Phân công trên màn hình Chi tiết Công việc (/workspace/:id/tasks/:taskId) gồm hộp chọn Người thực hiện chính (Creator), hộp chọn Người kiểm tra nội bộ (Reviewer - tùy chọn) và nút Lưu phân công.",
        "processing": "Hệ thống kiểm tra quyền Manager (BR-33) và kiểm tra Creator được chọn đang là thành viên hoạt động trong Workspace đó (BR-20). Sau khi lưu phân công, hệ thống gửi thông báo ngay cho Creator nhận việc để bắt đầu làm (BR-34).",
        "in_req": "Chọn đầu việc (Task) và chọn 01 thành viên Creator trong Workspace làm người thực hiện chính.",
        "in_opt": "Chọn thêm người kiểm tra chất lượng nội bộ (Reviewer) và lời nhắn giao việc.",
        "sys_data": "Lưu thông tin người nhận việc trên Task và gửi thông báo thời gian thực cho Creator.",
        "output": "Giao việc cho Creator thành công và hiển thị thông báo MSG37.",
        "flow": [
            "Manager mở màn hình Chi tiết Công việc (/workspace/:id/tasks/:taskId) cần phân công.",
            "Manager chọn tên Creator phụ trách từ danh sách thành viên của Workspace (và chọn thêm người kiểm tra nội bộ nếu cần).",
            "Manager bấm nút Lưu phân công.",
            "Hệ thống kiểm tra quyền hạn (BR-20, BR-33), cập nhật người phụ trách cho Task, gửi thông báo cho Creator và hiển thị MSG37."
        ],
        "abnormal": [
            "Nếu chưa chọn Creator hoặc chọn người không thuộc Workspace này: Hệ thống báo lỗi MSG02 hoặc MSG07."
        ]
    },
    "3.6.3": {
        "summary": "Cho phép các thành viên trong dự án (Owner, Manager, Creator, Client) viết bình luận, đính kèm ảnh minh họa và nhắc tên (@mention) nhau ngay trên từng đầu việc để trao đổi và góp ý tập trung.",
        "trigger": "Khi thành viên mở chi tiết một công việc (/workspace/:id/tasks/:taskId), nhập nội dung nhận xét vào khung bình luận và bấm Gửi.",
        "interface": "Khung Thảo luận & Bình luận ở cuối màn hình Chi tiết Công việc (/workspace/:id/tasks/:taskId) gồm danh sách bình luận theo luồng trả lời, ô nhập văn bản có hỗ trợ gõ @mention nhắc tên, nút đính kèm ảnh và nút Gửi bình luận.",
        "processing": "Hệ thống kiểm tra người dùng là thành viên của Workspace (BR-20), kiểm tra nội dung bình luận không trống và ảnh đính kèm (nếu có) dưới 5 MB (BR-12), sau đó lưu bình luận và gửi thông báo cho những người được nhắc tên (@mention).",
        "in_req": "Nội dung bình luận trao đổi trên đầu việc.",
        "in_opt": "Hình ảnh minh họa đính kèm (PNG, JPG, WEBP tối đa 5 MB) và gắn thẻ @mention thành viên.",
        "sys_data": "Mã bình luận, người gửi, thời gian gửi và danh sách thành viên nhận thông báo.",
        "output": "Hiển thị ngay bình luận mới trên luồng trao đổi của Task và báo MSG37.",
        "flow": [
            "Thành viên (Owner, Manager, Creator hoặc Client) mở màn hình Chi tiết Công việc (/workspace/:id/tasks/:taskId).",
            "Người dùng nhập nội dung góp ý vào ô bình luận, có thể gõ @ để nhắc tên đồng đội hoặc đính kèm ảnh minh họa.",
            "Người dùng bấm nút Gửi bình luận.",
            "Hệ thống kiểm tra quyền thành viên (BR-20) và tệp ảnh đính kèm (BR-12), lưu bình luận lên màn hình và thông báo cho các thành viên liên quan."
        ],
        "abnormal": [
            "Nếu bấm gửi khi ô bình luận đang trống: Hệ thống báo lỗi MSG02.",
            "Nếu ảnh đính kèm vượt quá 5 MB hoặc sai định dạng: Hệ thống báo lỗi MSG22."
        ]
    },
    "3.6.4": {
        "summary": "Hiển thị toàn bộ công việc của dự án dưới dạng bảng danh sách chi tiết (List View), giúp theo dõi nhanh mã công việc, tiêu đề, người làm, kênh đăng, mức độ ưu tiên, hạn chót và sắp xếp thứ tự ưu tiên.",
        "trigger": "Khi thành viên mở màn hình Công việc của Workspace và chọn tab Dạng danh sách (/workspace/:id/tasks?view=list).",
        "interface": "Màn hình Danh sách Công việc dạng bảng gồm các cột: Mã Task, Tiêu đề, Trạng thái, Người thực hiện (Creator), Nền tảng đăng, Độ ưu tiên, Hạn chót (Due Date), cùng chức năng bấm tiêu đề cột để sắp xếp hoặc kéo thả đổi thứ tự.",
        "processing": "Hệ thống kiểm tra quyền thành viên trong Workspace (BR-20), lấy danh sách Task chung của dự án (BR-44), quy đổi hạn chót theo múi giờ của Workspace (BR-22) và hiển thị thành bảng phân trang.",
        "in_req": "Mở chế độ xem Danh sách (List View) trong Workspace.",
        "in_opt": "Chọn cột cần sắp xếp (theo hạn chót, độ ưu tiên, trạng thái) hoặc kéo thả thứ tự dòng.",
        "sys_data": "Danh sách Task của Workspace đã đồng bộ theo múi giờ dự án (BR-22, BR-33, BR-44).",
        "output": "Hiển thị bảng danh sách công việc rõ ràng, đầy đủ thông tin.",
        "flow": [
            "Thành viên trong dự án mở mục Công việc và chọn chế độ xem Danh sách (/workspace/:id/tasks?view=list).",
            "Hệ thống kiểm tra quyền truy cập dự án (BR-20) và tải danh sách Task (BR-44).",
            "Hệ thống hiển thị hạn hoàn thành theo đúng múi giờ của Workspace (BR-22).",
            "Người dùng có thể bấm sắp xếp theo cột hoặc nhấp vào từng dòng để mở xem chi tiết công việc."
        ],
        "abnormal": [
            "Nếu dự án chưa có công việc nào hoặc không khớp bộ lọc: Hệ thống hiển thị thông báo MSG01."
        ]
    },
    "3.6.5": {
        "summary": "Hiển thị các đầu việc và lịch đăng bài trực quan trên tờ lịch theo Ngày, Tuần hoặc Tháng (giống Google Calendar), đồng thời hỗ trợ kéo thả thẻ công việc sang ngày khác để đổi lịch nhanh.",
        "trigger": "Khi thành viên chuyển sang tab Xem dạng Lịch (/workspace/:id/tasks?view=calendar) hoặc kéo thả một thẻ công việc sang ô ngày mới trên lịch.",
        "interface": "Màn hình Lịch Công việc hiển thị lưới lịch theo Ngày / Tuần / Tháng, các thẻ công việc gắn màu theo trạng thái hoặc nền tảng mạng xã hội, nút chuyển tháng và thao tác kéo thả thẻ giữa các ngày.",
        "processing": "Hệ thống hiển thị vị trí các Task trên lịch dựa theo hạn hoàn thành hoặc giờ hẹn đăng đã quy đổi theo múi giờ chuẩn của Workspace (BR-22, BR-44). Khi Manager kéo thả thẻ sang ngày mới, hệ thống kiểm tra ngày hợp lệ và cập nhật lại hạn công việc (BR-33).",
        "in_req": "Chọn chế độ xem Lịch (Calendar View) và chọn khung thời gian (Ngày / Tuần / Tháng).",
        "in_opt": "Kéo thả thẻ Task sang ô ngày khác để dời lịch (dành cho Manager).",
        "sys_data": "Mốc thời gian hạn chót và giờ đăng bài tính theo múi giờ Workspace (BR-22, BR-44).",
        "output": "Hiển thị lịch công việc trực quan và cập nhật ngày mới khi kéo thả (MSG37).",
        "flow": [
            "Thành viên mở bảng Công việc của Workspace và chọn tab Lịch (/workspace/:id/tasks?view=calendar).",
            "Hệ thống tải danh sách Task và sắp xếp vào đúng các ô ngày/giờ theo múi giờ của dự án (BR-22, BR-44).",
            "Người dùng chuyển đổi qua lại giữa chế độ xem Tháng, Tuần hoặc Ngày để theo dõi lịch đăng bài.",
            "Nếu Manager kéo một thẻ Task thả sang ngày mới, hệ thống cập nhật lại hạn chót của Task đó và báo MSG37."
        ],
        "abnormal": [
            "Nếu kéo thả một Task đã xuất bản xong hoặc người kéo không có quyền sửa lịch: Hệ thống trả thẻ về vị trí cũ và báo MSG07 hoặc MSG36."
        ]
    },
    "3.6.6": {
        "summary": "Hiển thị tiến độ các công việc trong chiến dịch dưới dạng biểu đồ đường thời gian (Gantt Timeline), giúp nhìn rõ công việc nào bắt đầu khi nào, kéo dài bao lâu và có bị chậm tiến độ hay không.",
        "trigger": "Khi thành viên mở bảng Công việc của Workspace và chọn tab Biểu đồ Gantt (/workspace/:id/tasks?view=gantt).",
        "interface": "Màn hình Biểu đồ Gantt gồm danh sách đầu việc ở cột bên trái và các thanh ngang biểu diễn thời gian bắt đầu – kết thúc dọc theo trục ngày/tuần ở bên phải, kèm vạch kẻ đánh dấu ngày hôm nay.",
        "processing": "Hệ thống kiểm tra quyền truy cập dự án (BR-20), lấy dữ liệu thời gian bắt đầu, hạn kết thúc và trạng thái hoàn thành của từng Task (BR-44) quy đổi theo múi giờ Workspace (BR-22) để vẽ các thanh tiến độ.",
        "in_req": "Mở chế độ xem Biểu đồ tiến độ Gantt (/workspace/:id/tasks?view=gantt).",
        "in_opt": "Chọn độ thu phóng trục thời gian (theo Ngày, Tuần hoặc Tháng).",
        "sys_data": "Khoảng thời gian thực hiện, tỷ lệ hoàn thành và sự liên kết giữa các Task trong chiến dịch (BR-22, BR-44).",
        "output": "Hiển thị biểu đồ tiến độ Gantt trực quan theo dòng thời gian của dự án.",
        "flow": [
            "Thành viên mở mục Công việc của Workspace và chuyển sang tab Gantt (/workspace/:id/tasks?view=gantt).",
            "Hệ thống kiểm tra quyền truy cập (BR-20) và tải dữ liệu lịch trình của các Task (BR-44).",
            "Hệ thống căn chỉnh các mốc bắt đầu và hạn chót theo múi giờ chuẩn của Workspace (BR-22).",
            "Màn hình hiển thị các thanh thời gian giúp người dùng theo dõi tổng thể tiến độ chiến dịch."
        ],
        "abnormal": [
            "Nếu không có công việc nào trong khoảng thời gian đang chọn: Hệ thống hiển thị thông báo MSG01."
        ]
    },
    "3.6.7": {
        "summary": "Hiển thị và quản lý công việc trên bảng phân cột Kanban (kiểu Jira), cho phép nhóm cột theo Trạng thái, theo Người thực hiện hoặc theo Nền tảng mạng xã hội và kéo thả thẻ để chuyển trạng thái.",
        "trigger": "Khi thành viên mở tab Bảng Kanban (/workspace/:id/tasks?view=kanban) hoặc kéo thả thẻ Task từ cột này sang cột khác.",
        "interface": "Màn hình Bảng Kanban gồm các cột dọc (Chờ phân rã / Cần làm / Đang làm / Chờ duyệt / Hoàn thành), nút chọn cách nhóm cột (Theo trạng thái, Theo người làm, Theo nền tảng) và các thẻ Task có thể kéo thả.",
        "processing": "Hệ thống hiển thị các thẻ Task vào từng cột tương ứng (BR-44). Khi người dùng kéo thả thẻ sang cột trạng thái mới, hệ thống kiểm tra quyền hạn và quy tắc luồng duyệt bài (BR-33, BR-34): chỉ cho phép chuyển sang Hoàn thành/Đã duyệt khi đã đi qua quy trình phê duyệt.",
        "in_req": "Mở chế độ xem Kanban hoặc kéo thả thẻ Task sang cột mới.",
        "in_opt": "Chọn chế độ nhóm cột (Group by Status / Assignee / Platform).",
        "sys_data": "Trạng thái hiện tại của Task và kiểm tra điều kiện chuyển bước hợp lệ (BR-33, BR-34).",
        "output": "Hiển thị bảng Kanban và cập nhật trạng thái Task ngay khi kéo thả hợp lệ (MSG37).",
        "flow": [
            "Thành viên mở mục Công việc và chọn tab Bảng Kanban (/workspace/:id/tasks?view=kanban).",
            "Hệ thống phân bổ các thẻ Task vào các cột trạng thái (hoặc theo người làm / nền tảng đăng - BR-44).",
            "Creator hoặc Manager kéo một thẻ Task đang làm thả sang cột trạng thái kế tiếp.",
            "Hệ thống kiểm tra việc chuyển trạng thái tuân thủ đúng quy trình (BR-33, BR-34), lưu trạng thái mới và hiển thị thông báo MSG37."
        ],
        "abnormal": [
            "Nếu người dùng kéo nhảy cóc một Task chưa duyệt sang thẳng cột Hoàn thành (bỏ qua quy trình duyệt 3 cấp BR-34): Hệ thống trả thẻ về cột cũ và báo lỗi MSG36."
        ]
    },
    "3.6.8": {
        "summary": "Cung cấp thanh tìm kiếm và bộ lọc đa tiêu chí (theo từ khóa, trạng thái, người phụ trách, chiến dịch, nền tảng đăng, độ ưu tiên và khoảng thời gian) áp dụng đồng bộ cho cả 4 chế độ xem Danh sách, Lịch, Gantt và Kanban.",
        "trigger": "Khi người dùng nhập từ khóa tìm kiếm hoặc chọn các điều kiện lọc trên thanh công cụ của màn hình Công việc (/workspace/:id/tasks).",
        "interface": "Thanh bộ lọc công việc gồm ô nhập Từ khóa tìm kiếm, các hộp chọn lọc theo Trạng thái, Người thực hiện (Assignee), Chiến dịch, Nền tảng (Facebook, Instagram, TikTok, Threads), Mức ưu tiên, Khoảng ngày và nút Xóa lọc.",
        "processing": "Hệ thống kiểm tra quyền thành viên (BR-20), kết hợp tất cả các tiêu chí lọc mà người dùng đã chọn để truy xuất danh sách Task tương ứng (quy đổi ngày lọc theo múi giờ Workspace - BR-22) và cập nhật ngay lên chế độ xem hiện tại (BR-44).",
        "in_req": "Ít nhất một từ khóa tìm kiếm hoặc tiêu chí lọc do người dùng chọn.",
        "in_opt": "Kết hợp nhiều bộ lọc cùng lúc (Trạng thái + Người làm + Nền tảng + Khoảng ngày).",
        "sys_data": "Tập kết quả Task thỏa mãn điều kiện lọc trên cả 4 chế độ hiển thị (BR-44).",
        "output": "Cập nhật danh sách công việc trên màn hình theo đúng điều kiện lọc.",
        "flow": [
            "Trên màn hình Công việc (/workspace/:id/tasks), người dùng nhập từ khóa hoặc chọn các bộ lọc (ví dụ: chỉ xem việc của tôi, nền tảng TikTok, trạng thái Đang làm).",
            "Hệ thống kiểm tra các tham số lọc và quy đổi khoảng thời gian theo múi giờ của dự án (BR-22).",
            "Hệ thống lọc danh sách Task khớp với tất cả điều kiện đã chọn (BR-44).",
            "Màn hình hiện tại (Danh sách, Lịch, Gantt hoặc Kanban) hiển thị ngay các công việc tìm được."
        ],
        "abnormal": [
            "Nếu không có công việc nào khớp với các điều kiện lọc: Hệ thống hiển thị thông báo không tìm thấy kết quả (MSG01) và nút Xóa bộ lọc."
        ]
    },
    "3.6.9": {
        "summary": "Thực hiện quy trình duyệt bài 3 cấp chặt chẽ: Creator gửi bài -> Manager kiểm duyệt nội bộ -> Client phê duyệt cuối cùng. Nếu bất kỳ cấp nào bấm Trả lại (Reject kèm lý do), bài viết sẽ quay về cho Creator sửa lại nhưng vẫn giữ nguyên toàn bộ lịch sử nhận xét.",
        "trigger": "Khi Creator bấm Gửi duyệt bài viết, hoặc khi Manager / Client bấm Phê duyệt (Approve) hay Trả lại yêu cầu sửa (Reject) trên màn hình Chi tiết Công việc (/workspace/:id/tasks/:taskId).",
        "interface": "Thanh tiến trình Duyệt bài 3 cấp trên màn hình Task (/workspace/:id/tasks/:taskId) hiển thị bước hiện tại (Creator -> Manager -> Client), lịch sử các lần duyệt/trả lại kèm nhận xét, ô nhập lý do và 2 nút: Phê duyệt (Approve) / Trả lại sửa (Reject).",
        "processing": "Hệ thống kiểm tra đúng người có quyền ở bước duyệt hiện tại (BR-34) và bài viết đã qua kiểm tra an toàn nội dung (BR-42). Nếu bấm Phê duyệt, Task sẽ chuyển lên cấp tiếp theo (và sang trạng thái Đã duyệt sẵn sàng đăng bài khi hoàn tất cấp cuối - BR-54). Nếu bấm Trả lại, hệ thống bắt buộc nhập lý do nhận xét, lưu vào lịch sử duyệt và đưa Task quay về bước đầu để Creator chỉnh sửa (BR-34).",
        "in_req": "Quyết định xét duyệt (Gửi duyệt / Phê duyệt / Trả lại) và Lý do nhận xét (bắt buộc phải nhập khi chọn Trả lại bài).",
        "in_opt": "Ghi chú khen ngợi hoặc dặn dò thêm khi bấm Phê duyệt.",
        "sys_data": "Bản ghi lịch sử duyệt (người duyệt, cấp duyệt, quyết định, thời gian, nhận xét) và trạng thái mới của Task (BR-34, BR-54).",
        "output": "Chuyển bước phê duyệt thành công (hoặc trả bài về cho Creator sửa lại) và hiển thị thông báo MSG38.",
        "flow": [
            "Sau khi soạn xong nội dung và ấn phẩm, Creator bấm Gửi duyệt trên đầu việc (/workspace/:id/tasks/:taskId).",
            "Manager (và người kiểm tra nội bộ nếu có) mở xem bài viết: nếu đạt yêu cầu thì bấm Phê duyệt để chuyển lên cho Client; nếu cần sửa thì nhập lý do và bấm Trả lại.",
            "Ở bước cuối, Client xem trước bài đăng và bấm Phê duyệt hoàn tất (hoặc Trả lại kèm góp ý nếu muốn chỉnh sửa).",
            "Khi hoàn tất đủ các cấp duyệt, hệ thống chuyển Task sang trạng thái Đã duyệt (APPROVED - sẵn sàng xuất bản theo BR-54) và hiển thị thông báo MSG38."
        ],
        "abnormal": [
            "Nếu bấm Trả lại (Reject) nhưng để trống ô lý do nhận xét: Hệ thống báo bắt buộc phải nhập lý do để Creator biết cần sửa gì (MSG02).",
            "Nếu người dùng không đúng vai trò của bước duyệt hiện tại cố bấm duyệt: Hệ thống chặn thao tác và báo MSG07."
        ]
    },
    "3.6.10": {
        "summary": "Cung cấp trình soạn thảo nội dung bài đăng tích hợp sẵn bộ chuyển đổi kiểu chữ Unicode (in đậm, in nghiêng, chữ kiểu nổi bật để đăng lên mạng xã hội không bị mất định dạng) và tự động lưu lịch sử các phiên bản chỉnh sửa.",
        "trigger": "Khi Creator hoặc Manager mở màn hình Soạn thảo nội dung của đầu việc (/workspace/:id/content-writing), viết bài, định dạng chữ và bấm Lưu.",
        "interface": "Màn hình Soạn thảo Nội dung (/workspace/:id/content-writing) gồm khung viết bài, thanh công cụ đổi phông chữ Unicode (Đậm, Nghiêng, Chữ nghệ thuật), bộ đếm số ký tự theo từng mạng xã hội, nút gọi AI gợi ý, nút chèn Hashtag và danh sách Lịch sử phiên bản bên cạnh.",
        "processing": "Hệ thống chuyển đổi các đoạn chữ được bôi đen sang ký tự chuẩn Unicode tương thích với cả 4 mạng xã hội. Mỗi khi người dùng bấm lưu hoặc gửi duyệt, hệ thống tự động tạo một bản chụp phiên bản mới (Content Version) ghi rõ người sửa và thời gian sửa để có thể xem lại hoặc khôi phục bất kỳ lúc nào (BR-35).",
        "in_req": "Nội dung văn bản bài viết đang soạn thảo cho đầu việc.",
        "in_opt": "Chọn kiểu chữ Unicode muốn áp dụng, gắn tư liệu ảnh/video và ghi chú phiên bản.",
        "sys_data": "Mã phiên bản nội dung mới (Version snapshot), người lưu, thời gian lưu và số lượng ký tự (BR-35).",
        "output": "Lưu bản nháp bài viết kèm phiên bản lịch sử mới thành công và hiển thị thông báo MSG39.",
        "flow": [
            "Creator hoặc Manager mở trình Soạn thảo nội dung (/workspace/:id/content-writing) từ đầu việc được giao.",
            "Người dùng gõ nội dung bài đăng, bôi đen các câu tiêu đề để chuyển sang kiểu chữ Unicode in đậm/in nghiêng bắt mắt.",
            "Người dùng bấm nút Lưu nội dung.",
            "Hệ thống lưu nội dung hiện tại, tự động ghi nhận thêm một phiên bản mới vào lịch sử chỉnh sửa (BR-35) và hiển thị thông báo MSG39."
        ],
        "abnormal": [
            "Nếu để trống hoàn toàn nội dung khi bấm lưu phiên bản hoặc vượt quá giới hạn độ dài tối đa: Hệ thống báo lỗi MSG02 hoặc MSG03."
        ]
    },
    "3.6.11": {
        "summary": "Xem và tra cứu kho lưu trữ tư liệu sáng tạo của dự án (Material Repository), được phân loại rõ thành 3 nhóm: (1) Ảnh/video gốc chưa chỉnh sửa (RAW - có nhãn cảnh báo không đăng trực tiếp), (2) Ấn phẩm đã chỉnh sửa hoàn thiện (Retouched), và (3) Tài liệu mẫu thương hiệu do Client cung cấp.",
        "trigger": "Khi thành viên trong dự án mở màn hình Kho Tư liệu (/workspace/:id/library).",
        "interface": "Màn hình Kho Tư liệu (/workspace/:id/library) gồm các tab phân loại (Tất cả / Ảnh gốc RAW / Đã chỉnh sửa Retouched / Tài liệu thương hiệu), ô tìm kiếm, lưới hiển thị ảnh/video kèm nhãn trạng thái và cảnh báo nếu là tệp RAW.",
        "processing": "Hệ thống kiểm tra quyền thành viên trong Workspace (BR-20), lấy danh sách các tư liệu chưa bị xóa và hiển thị kèm nhãn phân loại rõ ràng. Nếu người dùng bấm chọn một tệp gốc (RAW) để gắn vào bài đăng, hệ thống sẽ hiện băng cảnh báo nhắc nhở (BR-36, MSG41).",
        "in_req": "Mở màn hình Kho Tư liệu của Workspace.",
        "in_opt": "Lọc theo phân loại (RAW / Retouched / Brand Reference), định dạng tệp hoặc tìm theo tên.",
        "sys_data": "Danh sách tư liệu, nhãn phân loại giai đoạn xử lý (BR-36), dung lượng và người tải lên.",
        "output": "Hiển thị danh sách tư liệu của dự án kèm nhãn phân loại trực quan.",
        "flow": [
            "Thành viên mở mục Kho Tư liệu (/workspace/:id/library) trong Workspace.",
            "Hệ thống kiểm tra quyền truy cập dự án (BR-20) và tải danh mục tư liệu hiện có (BR-36).",
            "Người dùng lọc xem theo nhóm Ảnh gốc (RAW), Đã hoàn thiện (Retouched) hoặc Tài liệu mẫu của Client.",
            "Nếu người dùng chọn một tệp RAW cho bài chuẩn bị đăng, hệ thống hiển thị cảnh báo nhắc sử dụng bản đã chỉnh sửa (MSG41)."
        ],
        "abnormal": [
            "Nếu kho tư liệu chưa có tệp nào khớp với bộ lọc: Hệ thống hiển thị thông báo MSG01."
        ]
    },
    "3.6.12": {
        "summary": "Cho phép Creator, Manager hoặc Client tải các tệp hình ảnh, video hoặc tài liệu nhận diện thương hiệu mới từ máy tính lên Kho tư liệu chung của Workspace.",
        "trigger": "Khi thành viên bấm nút Tải tư liệu lên (Upload Material) trên màn hình Kho Tư liệu (/workspace/:id/library), chọn tệp cùng phân loại và bấm Tải lên.",
        "interface": "Hộp thoại Tải tư liệu lên gồm khung kéo thả chọn tệp từ máy tính, ô nhập Tên tư liệu, hộp chọn Phân loại bắt buộc (Ảnh/video gốc RAW, Đã chỉnh sửa Retouched, hoặc Tài liệu mẫu thương hiệu), ô gắn nhãn (tags) và nút Tải lên.",
        "processing": "Hệ thống kiểm tra quyền thành viên (BR-20), kiểm tra định dạng tệp được hỗ trợ và dung lượng không vượt quá hạn mức gói lưu trữ của Agency (BR-58), lưu tệp lên đám mây và ghi nhận vào Kho tư liệu theo đúng nhóm phân loại đã chọn (BR-36).",
        "in_req": "Tệp hình ảnh/video/tài liệu cần tải lên, Tên tư liệu và Phân loại tư liệu (RAW, Retouched hoặc Brand Reference).",
        "in_opt": "Mô tả ghi chú sử dụng và các thẻ từ khóa (tags) để dễ tìm kiếm.",
        "sys_data": "Đường dẫn lưu trữ tệp, dung lượng tệp, người tải lên và phân loại tư liệu (BR-36).",
        "output": "Tải tư liệu mới vào kho thành công và hiển thị thông báo MSG40.",
        "flow": [
            "Creator, Manager hoặc Client mở Kho Tư liệu (/workspace/:id/library) và bấm nút Tải tư liệu lên.",
            "Người dùng chọn tệp từ máy tính, đặt tên và chọn rõ phân loại (Ảnh gốc RAW, Đã hoàn thiện Retouched hoặc Tài liệu thương hiệu).",
            "Người dùng bấm nút Xác nhận tải lên.",
            "Hệ thống kiểm tra định dạng/dung lượng tệp hợp lệ, lưu tư liệu vào kho của Workspace (BR-36) và hiển thị thông báo MSG40."
        ],
        "abnormal": [
            "Nếu tệp tải lên sai định dạng hoặc vượt quá giới hạn dung lượng cho phép: Hệ thống từ chối và báo lỗi MSG22.",
            "Nếu kho lưu trữ của Agency đã đầy theo giới hạn gói cước: Hệ thống báo lỗi hết hạn mức dung lượng (MSG48)."
        ]
    },
    "3.6.13": {
        "summary": "Cho phép Creator hoặc Manager cập nhật lại tên, mô tả, thẻ tìm kiếm hoặc chuyển trạng thái phân loại của tư liệu trong kho (ví dụ chuyển từ Ảnh gốc RAW sang Đã chỉnh sửa hoàn thiện Retouched sau khi hậu kỳ xong).",
        "trigger": "Khi Creator hoặc Manager chọn một tư liệu trong kho (/workspace/:id/library), sửa thông tin hoặc tải bản đã chỉnh sửa lên và bấm Lưu.",
        "interface": "Hộp thoại Cập nhật Tư liệu gồm ô sửa Tên tư liệu, đổi Phân loại (từ RAW sang Retouched), sửa Mô tả / Nhãn tìm kiếm, tùy chọn tải tệp mới thay thế và nút Lưu cập nhật.",
        "processing": "Hệ thống kiểm tra quyền của Creator hoặc Manager trong Workspace (BR-20), cập nhật thông tin và trạng thái phân loại mới cho tư liệu. Khi chuyển từ RAW sang Retouched, hệ thống tự động gỡ bỏ cảnh báo hạn chế đăng bài trên tư liệu đó (BR-36).",
        "in_req": "Chọn tư liệu cần sửa, nhập Tên tư liệu và Phân loại mới.",
        "in_opt": "Cập nhật mô tả, thẻ từ khóa (tags) hoặc tệp phiên bản đã qua chỉnh sửa.",
        "sys_data": "Cập nhật trạng thái phân loại tư liệu (BR-36) và thời gian chỉnh sửa mới nhất.",
        "output": "Cập nhật thông tin tư liệu thành công và hiển thị thông báo MSG40.",
        "flow": [
            "Creator hoặc Manager mở Kho Tư liệu (/workspace/:id/library) và bấm chọn Chỉnh sửa trên tư liệu cần cập nhật.",
            "Người dùng sửa lại Tên, Nhãn tìm kiếm hoặc đổi phân loại từ Ảnh gốc (RAW) sang Đã chỉnh sửa (Retouched).",
            "Người dùng bấm nút Lưu cập nhật.",
            "Hệ thống kiểm tra dữ liệu hợp lệ, lưu thông tin mới cho tư liệu (BR-36) và hiển thị thông báo MSG40."
        ],
        "abnormal": [
            "Nếu để trống Tên tư liệu khi lưu: Hệ thống báo lỗi MSG02."
        ]
    },
    "3.6.14": {
        "summary": "Cho phép Creator hoặc Manager xóa mềm những tư liệu không còn dùng khỏi Kho tư liệu của Workspace. Tư liệu đã xóa sẽ ẩn khỏi danh sách chọn mới nhưng không làm mất ảnh trong các bài viết cũ và có thể khôi phục trong 30 ngày.",
        "trigger": "Khi Creator hoặc Manager bấm nút Xóa trên một tư liệu tại màn hình Kho Tư liệu (/workspace/:id/library) và xác nhận.",
        "interface": "Nút Xóa tư liệu trên từng thẻ tệp trong Kho Tư liệu (/workspace/:id/library) kèm hộp thoại xác nhận xóa.",
        "processing": "Hệ thống kiểm tra quyền thành viên (BR-20), chuyển trạng thái tư liệu sang Đã xóa mềm (ẩn khỏi kho hiện tại nhưng giữ lại tệp trong 30 ngày và bảo toàn hình ảnh cho các Task/bài đăng cũ đã gắn tư liệu đó - BR-36).",
        "in_req": "Chọn tư liệu cần xóa trong kho và xác nhận đồng ý.",
        "in_opt": "Không bắt buộc.",
        "sys_data": "Đánh dấu xóa mềm tư liệu kèm thời hạn 30 ngày khôi phục (BR-36).",
        "output": "Xóa mềm tư liệu khỏi kho thành công và hiển thị thông báo MSG40.",
        "flow": [
            "Trên màn hình Kho Tư liệu (/workspace/:id/library), Creator hoặc Manager bấm nút Xóa trên tư liệu muốn gỡ bỏ.",
            "Người dùng bấm Đồng ý trên hộp thoại xác nhận.",
            "Hệ thống kiểm tra quyền thực hiện (BR-20) và chuyển tư liệu sang trạng thái xóa mềm (BR-36).",
            "Tư liệu được ẩn khỏi danh sách kho hiện tại và hệ thống hiển thị thông báo MSG40."
        ],
        "abnormal": [
            "Nếu tư liệu đó đã bị xóa từ trước: Hệ thống báo không thể thực hiện lặp lại (MSG36)."
        ]
    },
    "3.6.15": {
        "summary": "Cho phép Client hoặc Manager liên kết thư mục Google Drive của khách hàng vào Workspace (qua đăng nhập Google an toàn) để lấy ảnh chụp và video dung lượng lớn vào dự án mà không cần tải thủ công từng tệp.",
        "trigger": "Khi Client hoặc Manager bấm nút Kết nối Google Drive trong màn hình Kho Tư liệu (/workspace/:id/library) và cấp quyền đọc thư mục trên cửa sổ Google.",
        "interface": "Khu vực Kết nối Google Drive trong Kho Tư liệu (/workspace/:id/library) gồm nút Liên kết tài khoản Google Drive, cửa sổ cấp quyền của Google và khung chọn thư mục nguồn.",
        "processing": "Sau khi người dùng xác nhận trên cửa sổ Google, hệ thống nhận khóa kết nối chỉ đọc (Read-only OAuth2), mã hóa bảo mật và gắn kết nối thư mục Google Drive đó vào Workspace hiện tại (BR-37).",
        "in_req": "Xác nhận cấp quyền đọc Google Drive trên cửa sổ Google và chọn thư mục dùng chung cho dự án.",
        "in_opt": "Không bắt buộc.",
        "sys_data": "Lưu khóa kết nối Google Drive đã mã hóa và thông tin thư mục liên kết của Workspace (BR-37).",
        "output": "Kết nối Google Drive với Workspace thành công và hiển thị thông báo MSG42.",
        "flow": [
            "Client hoặc Manager mở Kho Tư liệu (/workspace/:id/library) và bấm nút Kết nối Google Drive.",
            "Trên cửa sổ xác nhận của Google, người dùng chọn tài khoản và đồng ý cấp quyền đọc dữ liệu.",
            "Người dùng chọn thư mục Google Drive chứa tư liệu của nhãn hàng.",
            "Hệ thống lưu kết nối an toàn cho Workspace (BR-37) và hiển thị thông báo thành công (MSG42)."
        ],
        "abnormal": [
            "Nếu người dùng hủy cấp quyền trên cửa sổ Google hoặc mất kết nối: Hệ thống giữ nguyên trạng thái chưa liên kết và báo MSG13."
        ]
    },
    "3.6.16": {
        "summary": "Đồng bộ và nhập các tệp hình ảnh, video được chọn từ thư mục Google Drive đã kết nối về thẳng Kho tư liệu của Workspace.",
        "trigger": "Khi Client hoặc Manager chọn các tệp trong thư mục Google Drive liên kết (/workspace/:id/library) và bấm nút Đồng bộ về kho.",
        "interface": "Danh sách các tệp trong thư mục Google Drive đã kết nối, ô tích chọn tệp muốn lấy về, hộp chọn phân loại tư liệu (RAW / Retouched / Brand Reference) và nút Đồng bộ ngay.",
        "processing": "Hệ thống kiểm tra kết nối Google Drive của Workspace đang hoạt động (BR-37), kiểm tra các tệp được chọn đúng định dạng hỗ trợ và không bị trùng lặp với tệp đã lấy về trước đó, sau đó tải tệp vào Kho tư liệu của dự án (BR-36).",
        "in_req": "Chọn ít nhất 1 tệp ảnh/video từ Google Drive và chọn nhóm phân loại tư liệu tương ứng.",
        "in_opt": "Gắn thêm nhãn tìm kiếm (tags) cho đợt đồng bộ.",
        "sys_data": "Đối chiếu mã tệp Google Drive để chống trùng lặp, kiểm tra dung lượng kho (BR-58) và lưu vào Kho tư liệu (BR-36, BR-37).",
        "output": "Đồng bộ các tệp từ Google Drive vào Kho tư liệu thành công và hiển thị thông báo MSG42.",
        "flow": [
            "Trên màn hình Kho Tư liệu (/workspace/:id/library), Client hoặc Manager mở tab Google Drive đã kết nối.",
            "Người dùng tích chọn các tệp hình ảnh/video cần đưa vào dự án, chọn phân loại (ví dụ Ảnh gốc RAW hoặc Tài liệu thương hiệu) và bấm Đồng bộ.",
            "Hệ thống kiểm tra định dạng tệp và dung lượng lưu trữ khả dụng của Agency (BR-58).",
            "Hệ thống nhập các tệp về Kho tư liệu của Workspace (BR-36, BR-37) và hiển thị thông báo MSG42."
        ],
        "abnormal": [
            "Nếu có tệp không đúng định dạng hỗ trợ hoặc quá dung lượng: Hệ thống báo lỗi MSG22 hoặc MSG48.",
            "Nếu phiên kết nối Google Drive đã hết hạn: Hệ thống báo cần kết nối lại Google Drive (MSG36)."
        ]
    },
    "3.6.17": {
        "summary": "Cho phép Client hoặc Manager ngắt kết nối tài khoản Google Drive khỏi Workspace. Sau khi ngắt kết nối, toàn bộ các tư liệu đã từng đồng bộ vào kho trước đó vẫn được giữ nguyên cho dự án.",
        "trigger": "Khi Client hoặc Manager bấm nút Ngắt kết nối Google Drive trong màn hình Kho Tư liệu (/workspace/:id/library) và xác nhận.",
        "interface": "Nút Ngắt kết nối Google Drive kèm hộp thoại xác nhận trong phần quản lý kho của Workspace (/workspace/:id/library).",
        "processing": "Hệ thống kiểm tra quyền của Client hoặc Manager trong Workspace (BR-20), xóa khóa liên kết Google Drive và dừng việc đồng bộ mới, đồng thời giữ nguyên toàn bộ các tệp ảnh/video đã nhập vào Kho tư liệu trước đó (BR-37).",
        "in_req": "Xác nhận đồng ý ngắt kết nối Google Drive của Workspace.",
        "in_opt": "Không bắt buộc.",
        "sys_data": "Thu hồi khóa kết nối Google Drive và giữ nguyên các tư liệu đã nhập vào kho (BR-37).",
        "output": "Ngắt kết nối Google Drive thành công và hiển thị thông báo MSG42.",
        "flow": [
            "Client hoặc Manager mở phần cài đặt Google Drive trong Kho Tư liệu (/workspace/:id/library) và bấm Ngắt kết nối.",
            "Người dùng bấm Đồng ý trên hộp thoại xác nhận.",
            "Hệ thống hủy liên kết Google Drive của Workspace đó.",
            "Hệ thống bảo toàn nguyên vẹn các tệp đã đồng bộ trước đây (BR-37) và hiển thị thông báo MSG42."
        ],
        "abnormal": [
            "Nếu người thao tác không có quyền trong Workspace: Hệ thống chặn thao tác và báo MSG07."
        ]
    },
    "3.6.18": {
        "summary": "Cho phép Creator đóng dấu logo bản quyền thương hiệu (Watermark) lên hình ảnh đã chỉnh sửa với tùy chọn góc đặt, kích thước và độ mờ linh hoạt. Ảnh sau khi đóng dấu được lưu thành tệp mới để giữ nguyên ảnh gốc.",
        "trigger": "Khi Creator chọn một bức ảnh trong Kho Tư liệu (/workspace/:id/library), mở công cụ Đóng dấu bản quyền, chỉnh vị trí logo và bấm Áp dụng.",
        "interface": "Màn hình Đóng dấu ảnh (Watermark Studio) gồm khung xem trước ảnh trực tiếp, ô chọn Logo của Client (hoặc tải logo lên), chọn Vị trí đặt logo (4 góc hoặc chính giữa), thanh trượt chỉnh Kích thước (Scale) và Độ mờ (Opacity 10%–100%), cùng nút Lưu ảnh đã đóng dấu.",
        "processing": "Hệ thống kiểm tra bức ảnh được chọn (nếu là ảnh gốc RAW chưa chỉnh sửa thì hiện cảnh báo nhắc nhở MSG41 - BR-36). Sau đó, hệ thống ghép lớp logo lên ảnh theo đúng vị trí, tỷ lệ và độ mờ đã chọn, rồi xuất thành một tệp ảnh mới trong Kho tư liệu mà không ghi đè lên tệp ảnh gốc (BR-38).",
        "in_req": "Chọn ảnh cần đóng dấu trong kho, chọn Logo thương hiệu và chọn Vị trí / Kích thước / Độ mờ.",
        "in_opt": "Đặt tên riêng cho tệp ảnh mới sau khi đóng dấu.",
        "sys_data": "Tạo tệp ảnh mới đã gắn watermark trong Kho tư liệu và giữ nguyên tệp ảnh gốc ban đầu (BR-38).",
        "output": "Tạo bản ảnh đóng dấu thương hiệu thành công và hiển thị thông báo MSG40.",
        "flow": [
            "Creator chọn một bức ảnh hoàn thiện trong Kho Tư liệu (/workspace/:id/library) và bấm Công cụ đóng dấu (Apply Watermark).",
            "Creator chọn logo của nhãn hàng, điều chỉnh vị trí góc đặt, kích thước và độ mờ trên khung xem trước.",
            "Creator bấm nút Lưu ảnh đóng dấu.",
            "Hệ thống xử lý ghép logo, lưu thành một bản ảnh mới trong kho tư liệu (giữ nguyên bản gốc - BR-38) và hiển thị thông báo MSG40."
        ],
        "abnormal": [
            "Nếu Creator chọn một bức ảnh đang gắn nhãn RAW (chưa chỉnh sửa hậu kỳ): Hệ thống hiển thị băng cảnh báo MSG41 nhắc người dùng nên dùng ảnh đã chỉnh sửa (BR-36).",
            "Nếu tệp logo tải lên bị lỗi định dạng: Hệ thống báo lỗi MSG22."
        ]
    },
    "3.6.19": {
        "summary": "Cho phép các thành viên trong dự án (Owner, Manager, Creator, Client) tải tệp hình ảnh, video hoặc tài liệu từ Kho tư liệu của Workspace về máy tính cá nhân.",
        "trigger": "Khi thành viên bấm nút Tải xuống (Download) trên một tư liệu trong Kho Tư liệu (/workspace/:id/library).",
        "interface": "Nút Tải xuống (Download) trên thẻ tư liệu hoặc trong cửa sổ xem chi tiết tư liệu tại màn hình Kho Tư liệu (/workspace/:id/library).",
        "processing": "Hệ thống kiểm tra người dùng là thành viên có quyền truy cập Workspace đó (BR-20) và tư liệu đang tồn tại hợp lệ (BR-36), sau đó cấp đường dẫn tải tệp trực tiếp về máy tính của người dùng.",
        "in_req": "Chọn tư liệu cần tải về trong Kho Tư liệu của Workspace.",
        "in_opt": "Chọn tải bản gốc hoặc bản đã đóng dấu watermark (nếu có).",
        "sys_data": "Kiểm tra quyền thành viên dự án (BR-20) và tạo liên kết tải tệp an toàn.",
        "output": "Trình duyệt bắt đầu tải tệp tư liệu về máy tính của người dùng.",
        "flow": [
            "Thành viên mở Kho Tư liệu của dự án (/workspace/:id/library) và tìm đến tệp cần lấy.",
            "Người dùng bấm vào nút Tải xuống trên tư liệu đó.",
            "Hệ thống kiểm tra quyền truy cập của người dùng trong Workspace (BR-20).",
            "Hệ thống trả về tệp gốc độ phân giải cao để trình duyệt tải về máy."
        ],
        "abnormal": [
            "Nếu người dùng không thuộc Workspace hoặc tệp đã bị xóa: Hệ thống chặn tải xuống và báo MSG07 hoặc MSG01."
        ]
    },
    "3.6.20": {
        "summary": "Cho phép Creator chọn nhanh một bộ sưu tập Hashtag của dự án để chèn thẳng vào nội dung bài viết đang soạn thảo, tự động thêm dấu '#' và loại bỏ các thẻ bị trùng lặp.",
        "trigger": "Khi Creator đang viết bài trong trình Soạn thảo (/workspace/:id/content-writing), bấm nút Chèn Hashtag, chọn bộ sưu tập muốn dùng và bấm Áp dụng.",
        "interface": "Bảng chọn nhanh Bộ sưu tập Hashtag ngay trong màn hình Soạn thảo bài viết (/workspace/:id/content-writing), hiển thị các nhóm hashtag của dự án, danh sách các thẻ bên trong và nút Chèn vào bài viết.",
        "processing": "Hệ thống lấy các thẻ hashtag mà Creator đã chọn từ bộ sưu tập của Workspace (BR-39), tự động chuẩn hóa dấu '#' ở đầu mỗi từ, lọc bỏ các thẻ đã có sẵn trong bài viết để không bị lặp và chèn vào cuối nội dung bài đăng (BR-35).",
        "in_req": "Chọn ít nhất 1 bộ sưu tập Hashtag hoặc các thẻ hashtag lẻ cần chèn vào bài viết đang mở.",
        "in_opt": "Bỏ tích những thẻ hashtag không muốn chèn trong nhóm.",
        "sys_data": "Tự động chuẩn hóa tiền tố '#', khử trùng lặp hashtag và cập nhật vào nội dung bài viết (BR-35, BR-39).",
        "output": "Chèn bộ thẻ hashtag vào bài viết thành công và hiển thị thông báo MSG43.",
        "flow": [
            "Trong lúc soạn bài viết (/workspace/:id/content-writing), Creator bấm nút Chèn Hashtag trên thanh công cụ.",
            "Creator chọn một bộ sưu tập Hashtag của chiến dịch (hoặc tích chọn các thẻ lẻ) rồi bấm Chèn vào bài.",
            "Hệ thống tự động kiểm tra định dạng dấu '#' và loại bỏ các thẻ bị trùng lặp (BR-39).",
            "Các thẻ hashtag được thêm ngay vào bài viết và hệ thống hiển thị thông báo MSG43."
        ],
        "abnormal": [
            "Nếu dự án chưa có bộ hashtag nào khớp từ khóa tìm kiếm: Hệ thống hiển thị thông báo MSG01."
        ]
    },
    "3.6.21": {
        "summary": "Xem danh sách các Bộ sưu tập Hashtag được thiết lập riêng cho từng Workspace (gồm nhóm hashtag thương hiệu cố định của Client, nhóm hashtag theo sự kiện/chiến dịch và hashtag xu hướng).",
        "trigger": "Khi thành viên mở màn hình Bộ sưu tập Hashtag của dự án (/workspace/:id/hashtag-groups).",
        "interface": "Màn hình Bộ sưu tập Hashtag (/workspace/:id/hashtag-groups) gồm ô tìm kiếm, bộ lọc theo mục đích (Thương hiệu / Chiến dịch / Sự kiện / Xu hướng), danh sách các thẻ nhóm Hashtag kèm số lượng thẻ bên trong và nút Tạo bộ mới.",
        "processing": "Hệ thống kiểm tra quyền thành viên trong Workspace (BR-20), lấy toàn bộ các nhóm Hashtag đang hoạt động của dự án (BR-39) và hiển thị lên màn hình.",
        "in_req": "Mở màn hình Bộ sưu tập Hashtag của Workspace.",
        "in_opt": "Từ khóa tìm kiếm tên bộ sưu tập hoặc lọc theo phân loại mục đích.",
        "sys_data": "Danh sách các nhóm Hashtag và các thẻ hashtag bên trong của Workspace (BR-39).",
        "output": "Hiển thị danh sách đầy đủ các Bộ sưu tập Hashtag của dự án.",
        "flow": [
            "Thành viên trong dự án mở mục Bộ sưu tập Hashtag (/workspace/:id/hashtag-groups).",
            "Hệ thống kiểm tra quyền truy cập dự án (BR-20) và tải danh sách các nhóm Hashtag (BR-39).",
            "Người dùng có thể lọc theo loại chiến dịch hoặc tìm theo từ khóa.",
            "Màn hình hiển thị các bộ sưu tập cùng danh sách thẻ hashtag bên trong để sao chép hoặc quản lý."
        ],
        "abnormal": [
            "Nếu chưa có bộ sưu tập Hashtag nào khớp với tìm kiếm: Hệ thống hiển thị thông báo MSG01."
        ]
    },
    "3.6.22": {
        "summary": "Cho phép Creator, Manager hoặc Client tạo mới một Bộ sưu tập Hashtag trong Workspace và phân loại theo mục đích (Hashtag cốt lõi của nhãn hàng, Chiến dịch, Sự kiện) để cả đội dùng thống nhất.",
        "trigger": "Khi thành viên bấm nút Tạo bộ Hashtag mới trên màn hình Bộ sưu tập Hashtag (/workspace/:id/hashtag-groups), nhập tên nhóm cùng các thẻ hashtag và bấm Lưu.",
        "interface": "Hộp thoại Tạo Bộ sưu tập Hashtag gồm ô nhập Tên bộ sưu tập, hộp chọn Mục đích sử dụng (Thương hiệu / Chiến dịch / Sự kiện / Bắt buộc từ Client), ô nhập danh sách các thẻ hashtag và nút Lưu bộ sưu tập.",
        "processing": "Hệ thống kiểm tra quyền thành viên trong Workspace (BR-20), kiểm tra tên bộ sưu tập không bị trùng trong cùng dự án, tự động gắn dấu '#' và loại bỏ khoảng trắng thừa cho từng thẻ hashtag trước khi lưu vào kho của Workspace (BR-39).",
        "in_req": "Tên bộ sưu tập Hashtag, Phân loại mục đích sử dụng và ít nhất 1 thẻ hashtag.",
        "in_opt": "Mô tả hướng dẫn khi nào nên dùng bộ hashtag này.",
        "sys_data": "Chuẩn hóa định dạng các thẻ hashtag và lưu vào Workspace hiện tại (BR-39).",
        "output": "Tạo bộ sưu tập Hashtag mới thành công và hiển thị thông báo MSG43.",
        "flow": [
            "Creator, Manager hoặc Client mở màn hình Bộ sưu tập Hashtag (/workspace/:id/hashtag-groups) và bấm Tạo bộ mới.",
            "Người dùng nhập Tên bộ sưu tập, chọn Mục đích sử dụng và nhập danh sách các thẻ hashtag.",
            "Người dùng bấm nút Lưu bộ sưu tập.",
            "Hệ thống tự động chuẩn hóa định dạng '#' cho các thẻ, lưu bộ sưu tập vào Workspace (BR-39) và hiển thị thông báo MSG43."
        ],
        "abnormal": [
            "Nếu để trống Tên bộ sưu tập hoặc chưa nhập thẻ hashtag nào: Hệ thống báo lỗi MSG02."
        ]
    },
    "3.6.23": {
        "summary": "Cho phép Creator hoặc Manager chỉnh sửa lại tên nhóm, mục đích phân loại hoặc thêm/bớt các thẻ hashtag bên trong một Bộ sưu tập Hashtag của Workspace.",
        "trigger": "Khi Creator hoặc Manager chọn một bộ sưu tập trên trang Hashtag (/workspace/:id/hashtag-groups), sửa danh sách thẻ và bấm Lưu cập nhật.",
        "interface": "Hộp thoại Chỉnh sửa Bộ sưu tập Hashtag gồm ô sửa Tên nhóm, đổi Mục đích phân loại, danh sách các thẻ hashtag hiện có (cho phép xóa bớt hoặc gõ thêm thẻ mới) và nút Lưu thay đổi.",
        "processing": "Hệ thống kiểm tra quyền chỉnh sửa trong Workspace (BR-20), tự động chuẩn hóa các thẻ hashtag mới thêm vào và cập nhật lại bộ sưu tập (BR-39).",
        "in_req": "Chọn bộ sưu tập cần sửa, Tên bộ sưu tập và danh sách thẻ hashtag sau khi chỉnh sửa.",
        "in_opt": "Cập nhật mô tả ghi chú của bộ sưu tập.",
        "sys_data": "Chuẩn hóa danh sách thẻ mới và lưu thời gian cập nhật (BR-39).",
        "output": "Cập nhật Bộ sưu tập Hashtag thành công và hiển thị thông báo MSG43.",
        "flow": [
            "Creator hoặc Manager mở màn hình Bộ sưu tập Hashtag (/workspace/:id/hashtag-groups) và bấm Sửa trên nhóm cần điều chỉnh.",
            "Người dùng đổi tên nhóm, thêm các thẻ hashtag mới hoặc xóa bớt các thẻ cũ rồi bấm Lưu.",
            "Hệ thống kiểm tra dữ liệu hợp lệ và chuẩn hóa lại danh sách thẻ (BR-39).",
            "Hệ thống lưu thay đổi và hiển thị thông báo MSG43."
        ],
        "abnormal": [
            "Nếu xóa hết toàn bộ thẻ hoặc để trống tên bộ sưu tập: Hệ thống báo lỗi MSG02."
        ]
    },
    "3.6.24": {
        "summary": "Cho phép Creator hoặc Manager xóa mềm một Bộ sưu tập Hashtag không còn sử dụng khỏi danh sách của Workspace, trong khi vẫn giữ nguyên các thẻ hashtag đã từng được chèn vào các bài viết trước đó.",
        "trigger": "Khi Creator hoặc Manager bấm nút Xóa trên một Bộ sưu tập Hashtag (/workspace/:id/hashtag-groups) và xác nhận.",
        "interface": "Nút Xóa bộ sưu tập kèm hộp thoại xác nhận trên màn hình Bộ sưu tập Hashtag (/workspace/:id/hashtag-groups).",
        "processing": "Hệ thống kiểm tra quyền trong Workspace (BR-20), chuyển trạng thái bộ sưu tập sang Đã xóa mềm để ẩn khỏi danh sách chọn mới, đồng thời giữ nguyên toàn bộ nội dung các bài viết cũ đã dùng các hashtag đó (BR-39).",
        "in_req": "Chọn bộ sưu tập Hashtag cần xóa và xác nhận đồng ý.",
        "in_opt": "Không bắt buộc.",
        "sys_data": "Đánh dấu xóa mềm bộ sưu tập Hashtag trong Workspace (BR-39).",
        "output": "Xóa bộ sưu tập Hashtag thành công và hiển thị thông báo MSG43.",
        "flow": [
            "Creator hoặc Manager mở trang Bộ sưu tập Hashtag (/workspace/:id/hashtag-groups) và bấm nút Xóa trên nhóm muốn gỡ bỏ.",
            "Người dùng bấm Đồng ý trên hộp thoại xác nhận.",
            "Hệ thống kiểm tra quyền thực hiện (BR-20) và ẩn bộ sưu tập đó khỏi danh sách hoạt động (BR-39).",
            "Hệ thống hiển thị thông báo xóa thành công (MSG43)."
        ],
        "abnormal": [
            "Nếu bộ sưu tập đó đã bị xóa trước đó: Hệ thống báo lỗi MSG36."
        ]
    },
    "3.6.25": {
        "summary": "Cho phép Manager hoặc Creator tạo biểu mẫu khảo sát ý kiến (Survey) với nhiều dạng câu hỏi (trắc nghiệm, chọn nhiều đáp án, chấm điểm, tự luận) và lấy đường dẫn chia sẻ để thu thập phản hồi từ khách hàng hoặc người tham dự sự kiện.",
        "trigger": "Khi Manager hoặc Creator mở màn hình Khảo sát (/workspace/:id/surveys), bấm Tạo khảo sát mới, thiết kế danh sách câu hỏi và bấm Xuất bản.",
        "interface": "Màn hình Tạo Khảo sát (/workspace/:id/surveys) gồm ô nhập Tiêu đề khảo sát, Mô tả mục đích, Thời hạn đóng biểu mẫu, công cụ thêm câu hỏi (Trắc nghiệm 1 lựa chọn, Nhiều lựa chọn, Thang điểm 1–5, Văn bản tự do) và nút Lưu & Lấy link chia sẻ.",
        "processing": "Hệ thống kiểm tra quyền thành viên trong Workspace (BR-20), kiểm tra biểu mẫu có tiêu đề và ít nhất 1 câu hỏi hợp lệ, sau đó lưu cấu trúc khảo sát và tạo đường dẫn công khai để người tham gia điền câu trả lời (BR-40).",
        "in_req": "Tiêu đề biểu mẫu khảo sát và ít nhất 1 câu hỏi khảo sát.",
        "in_opt": "Mô tả giới thiệu, thời hạn đóng khảo sát và cài đặt câu hỏi bắt buộc trả lời.",
        "sys_data": "Mã khảo sát, cấu trúc danh sách câu hỏi và đường dẫn chia sẻ biểu mẫu (BR-40).",
        "output": "Tạo biểu mẫu khảo sát thành công, cấp link chia sẻ và hiển thị thông báo MSG44.",
        "flow": [
            "Manager hoặc Creator mở màn hình Khảo sát (/workspace/:id/surveys) trong Workspace và bấm Tạo khảo sát mới.",
            "Người dùng nhập Tiêu đề, Mô tả và lần lượt thêm các câu hỏi trắc nghiệm, thang điểm hoặc câu hỏi mở.",
            "Người dùng bấm nút Lưu khảo sát.",
            "Hệ thống lưu biểu mẫu, tạo đường dẫn chia sẻ công khai (BR-40) và hiển thị thông báo MSG44."
        ],
        "abnormal": [
            "Nếu bỏ trống Tiêu đề khảo sát hoặc chưa thêm câu hỏi nào: Hệ thống báo lỗi MSG02."
        ]
    },
    "3.6.26": {
        "summary": "Hiển thị báo cáo thống kê và biểu đồ phân tích kết quả trả lời của biểu mẫu khảo sát (tổng số người phản hồi, tỷ lệ chọn từng đáp án trắc nghiệm và danh sách câu trả lời tự luận) để đánh giá hiệu quả sự kiện/chiến dịch.",
        "trigger": "Khi Manager hoặc Client bấm vào xem Kết quả phân tích của một biểu mẫu khảo sát (/workspace/:id/surveys).",
        "interface": "Màn hình Phân tích Khảo sát hiển thị Tổng số lượt phản hồi, Tỷ lệ hoàn thành, biểu đồ cột/tròn thống kê tỷ lệ từng câu hỏi trắc nghiệm và bảng danh sách các ý kiến đóng góp chi tiết.",
        "processing": "Hệ thống kiểm tra quyền truy cập dự án của Manager hoặc Client (BR-20), tổng hợp toàn bộ dữ liệu câu trả lời đã thu thập được theo thời gian thực (BR-40) và tính toán tỷ lệ phần trăm cho từng câu hỏi.",
        "in_req": "Chọn biểu mẫu khảo sát cần xem thống kê kết quả.",
        "in_opt": "Lọc phản hồi theo khoảng thời gian gửi.",
        "sys_data": "Số lượng phản hồi, tỷ lệ phân bổ đáp án và danh sách câu trả lời chi tiết (BR-40).",
        "output": "Hiển thị bảng thống kê và biểu đồ phân tích kết quả khảo sát.",
        "flow": [
            "Manager hoặc Client mở danh sách Khảo sát (/workspace/:id/surveys) và chọn Xem phân tích trên biểu mẫu cần kiểm tra.",
            "Hệ thống kiểm tra quyền truy cập trong Workspace (BR-20).",
            "Hệ thống tổng hợp toàn bộ lượt trả lời và vẽ biểu đồ thống kê theo từng câu hỏi (BR-40).",
            "Màn hình hiển thị trực quan số liệu và các ý kiến đóng góp của người tham gia."
        ],
        "abnormal": [
            "Nếu biểu mẫu khảo sát chưa có người nào gửi câu trả lời: Hệ thống hiển thị thông báo chưa có dữ liệu phản hồi (MSG01)."
        ]
    },
    "3.6.27": {
        "summary": "Cho phép Owner, Manager hoặc Creator tạo nhanh đường dẫn phòng họp trực tuyến (Google Meet) gắn với lịch của Workspace để đội ngũ Agency và Client vào họp bàn kịch bản hoặc duyệt ấn phẩm ngay.",
        "trigger": "Khi thành viên mở mục Cuộc họp (/workspace/:id/meetings), nhập tiêu đề cùng thời gian họp và bấm Tạo link phòng họp.",
        "interface": "Màn hình Tạo Phòng họp (/workspace/:id/meetings) gồm ô nhập Chủ đề cuộc họp, chọn Thời gian bắt đầu – kết thúc, chọn các thành viên / Client tham dự và nút Tạo link Google Meet.",
        "processing": "Hệ thống kiểm tra quyền thành viên trong Workspace (BR-20), quy đổi thời gian họp theo múi giờ chuẩn của dự án (BR-22), tự động khởi tạo đường dẫn phòng họp trực tuyến duy nhất (BR-40) và gửi thông báo kèm link họp cho các thành viên được mời.",
        "in_req": "Chủ đề cuộc họp và Thời gian diễn ra cuộc họp.",
        "in_opt": "Danh sách thành viên tham dự cụ thể và nội dung chương trình họp (Agenda).",
        "sys_data": "Đường dẫn phòng họp trực tuyến (Google Meet URL), thời gian theo múi giờ Workspace (BR-22, BR-40) và thông báo lịch họp.",
        "output": "Khởi tạo link phòng họp thành công, cho phép copy link ngay và hiển thị thông báo MSG44.",
        "flow": [
            "Owner, Manager hoặc Creator mở màn hình Cuộc họp (/workspace/:id/meetings) và bấm Tạo cuộc họp mới.",
            "Người dùng nhập Chủ đề cuộc họp, chọn Ngày giờ họp (theo múi giờ dự án BR-22) và chọn người tham gia.",
            "Người dùng bấm nút Tạo link phòng họp.",
            "Hệ thống sinh đường dẫn phòng họp trực tuyến (BR-40), gửi thông báo cho các thành viên và hiển thị thông báo MSG44."
        ],
        "abnormal": [
            "Nếu bỏ trống Chủ đề cuộc họp hoặc chọn thời gian không hợp lệ: Hệ thống báo lỗi MSG02 hoặc MSG03."
        ]
    },
    "3.6.28": {
        "summary": "Xem danh sách và nội dung chi tiết của các mẫu Email thông báo trong Workspace (gồm mẫu mời họp, gửi báo cáo chiến dịch, thông báo duyệt bài) có hỗ trợ các biến điền tự động như tên khách hàng, tên chiến dịch.",
        "trigger": "Khi Manager hoặc Creator mở màn hình Thư viện Mẫu Email (/workspace/:id/mail-templates).",
        "interface": "Màn hình Mẫu Email (/workspace/:id/mail-templates) hiển thị danh sách các mẫu email của hệ thống và của dự án, khung xem trước bố cục email, danh sách các biến tự động (như `{{client_name}}`, `{{campaign_name}}`) và nút Tạo mẫu mới / Gửi email.",
        "processing": "Hệ thống kiểm tra quyền thành viên trong Workspace (BR-20), tải danh sách các mẫu email mặc định và mẫu tùy chỉnh của dự án (BR-41) để người dùng xem trước.",
        "in_req": "Mở màn hình Mẫu Email của Workspace.",
        "in_opt": "Tìm kiếm theo tên mẫu email hoặc lọc theo mục đích sử dụng.",
        "sys_data": "Danh sách mẫu email, tiêu đề, nội dung HTML và danh sách các biến tự động đi kèm (BR-41).",
        "output": "Hiển thị danh sách và bản xem trước của các mẫu Email trong dự án.",
        "flow": [
            "Manager hoặc Creator mở màn hình Mẫu Email (/workspace/:id/mail-templates) trong Workspace.",
            "Hệ thống kiểm tra quyền truy cập (BR-20) và lấy danh sách các mẫu email hiện có (BR-41).",
            "Người dùng bấm vào từng mẫu để xem trước giao diện hiển thị và các thẻ biến tự động.",
            "Từ đây, người dùng có thể chọn tạo mẫu mới (3.6.29), chỉnh sửa (3.6.30) hoặc gửi email (3.6.32)."
        ],
        "abnormal": [
            "Nếu không tìm thấy mẫu email nào khớp với từ khóa: Hệ thống hiển thị thông báo MSG01."
        ]
    },
    "3.6.29": {
        "summary": "Cho phép Manager hoặc Creator tạo mới một mẫu Email thông báo cho dự án, hỗ trợ chèn các thẻ biến tự động (như tên người nhận, tên chiến dịch, tên công việc) để dùng lại nhiều lần mà không cần gõ lại từ đầu.",
        "trigger": "Khi Manager hoặc Creator bấm nút Tạo mẫu Email mới trên trang Mẫu Email (/workspace/:id/mail-templates), soạn tiêu đề cùng nội dung và bấm Lưu.",
        "interface": "Trình soạn thảo Mẫu Email gồm ô nhập Tên mẫu, Tiêu đề bức thư (Subject), khung soạn thảo nội dung văn bản/HTML, thanh chọn chèn nhanh các thẻ biến (`{{recipient_name}}`, `{{campaign_name}}`, `{{task_title}}`) và nút Lưu mẫu.",
        "processing": "Hệ thống kiểm tra quyền trong Workspace (BR-20), kiểm tra Tên mẫu, Tiêu đề và Nội dung email không bị để trống, đồng thời kiểm tra các thẻ biến `{{...}}` đúng cú pháp trước khi lưu vào thư viện của dự án (BR-41).",
        "in_req": "Tên mẫu email, Tiêu đề email (Subject) và Nội dung bức thư.",
        "in_opt": "Chèn các thẻ biến tự động (`{{recipient_name}}`, `{{campaign_name}}`...) vào tiêu đề và nội dung.",
        "sys_data": "Mã mẫu email mới, danh sách các biến sử dụng trong mẫu và người tạo (BR-41).",
        "output": "Tạo mẫu Email mới thành công và hiển thị thông báo MSG44.",
        "flow": [
            "Manager hoặc Creator mở màn hình Mẫu Email (/workspace/:id/mail-templates) và bấm Tạo mẫu mới.",
            "Người dùng nhập Tên mẫu, Tiêu đề email và soạn thảo nội dung kèm chèn các thẻ biến tự động.",
            "Người dùng bấm nút Lưu mẫu Email.",
            "Hệ thống kiểm tra cú pháp các thẻ biến hợp lệ (BR-41), lưu mẫu mới vào dự án và hiển thị thông báo MSG44."
        ],
        "abnormal": [
            "Nếu bỏ trống Tên mẫu, Tiêu đề hoặc Nội dung email, hoặc viết sai cú pháp thẻ biến: Hệ thống báo lỗi MSG02 hoặc MSG03."
        ]
    },
    "3.6.30": {
        "summary": "Cho phép Manager hoặc Creator chỉnh sửa lại tiêu đề, bố cục nội dung và các thẻ biến tự động của một mẫu Email đã tạo trong Workspace.",
        "trigger": "Khi Manager hoặc Creator chọn một mẫu email trong thư viện (/workspace/:id/mail-templates), sửa nội dung và bấm Lưu cập nhật.",
        "interface": "Màn hình Chỉnh sửa Mẫu Email gồm ô sửa Tên mẫu, Tiêu đề email, khung chỉnh sửa nội dung HTML/văn bản, khung xem trước trực tiếp và nút Lưu thay đổi.",
        "processing": "Hệ thống kiểm tra quyền thành viên (BR-20), kiểm tra cú pháp các thẻ biến `{{...}}` hợp lệ và lưu bản cập nhật mới cho mẫu email đó (BR-41).",
        "in_req": "Chọn mẫu email cần sửa, nhập Tiêu đề và Nội dung sau khi chỉnh sửa.",
        "in_opt": "Thêm hoặc bớt các thẻ biến tự động trong nội dung thư.",
        "sys_data": "Kiểm tra cú pháp biến tự động (BR-41) và cập nhật thời gian sửa mẫu.",
        "output": "Lưu cập nhật mẫu Email thành công và hiển thị thông báo MSG44.",
        "flow": [
            "Manager hoặc Creator mở màn hình Mẫu Email (/workspace/:id/mail-templates) và chọn Chỉnh sửa trên mẫu cần sửa.",
            "Người dùng thay đổi Tiêu đề, Nội dung bức thư hoặc các thẻ biến tự động rồi bấm Lưu.",
            "Hệ thống kiểm tra thông tin bắt buộc và tính hợp lệ của các thẻ biến (BR-41).",
            "Hệ thống lưu phiên bản mới của mẫu email và hiển thị thông báo MSG44."
        ],
        "abnormal": [
            "Nếu để trống Tiêu đề hoặc Nội dung email khi lưu: Hệ thống báo lỗi MSG02."
        ]
    },
    "3.6.31": {
        "summary": "Cho phép Manager hoặc Creator xóa các mẫu Email tùy chỉnh không còn dùng khỏi thư viện của Workspace (các mẫu email mặc định bắt buộc của hệ thống sẽ được bảo vệ không cho xóa).",
        "trigger": "Khi Manager hoặc Creator bấm nút Xóa trên một mẫu email tùy chỉnh (/workspace/:id/mail-templates) và xác nhận.",
        "interface": "Nút Xóa mẫu email kèm hộp thoại xác nhận trên màn hình Mẫu Email (/workspace/:id/mail-templates).",
        "processing": "Hệ thống kiểm tra quyền thành viên (BR-20) và kiểm tra mẫu đó là mẫu tùy chỉnh của dự án (không phải mẫu hệ thống cố định - BR-41), sau đó xóa mẫu khỏi thư viện mà không làm mất lịch sử các email đã gửi trước đó.",
        "in_req": "Chọn mẫu email tùy chỉnh cần xóa và xác nhận đồng ý.",
        "in_opt": "Không bắt buộc.",
        "sys_data": "Xóa mẫu email khỏi danh sách chọn của Workspace và giữ nguyên nhật ký gửi mail cũ (BR-41).",
        "output": "Xóa mẫu Email thành công và hiển thị thông báo MSG44.",
        "flow": [
            "Manager hoặc Creator mở trang Mẫu Email (/workspace/:id/mail-templates) và bấm nút Xóa trên mẫu tùy chỉnh cần gỡ.",
            "Người dùng bấm Đồng ý trên hộp thoại xác nhận.",
            "Hệ thống kiểm tra đây không phải là mẫu mặc định bắt buộc của hệ thống (BR-41).",
            "Hệ thống xóa mẫu khỏi thư viện của dự án và hiển thị thông báo MSG44."
        ],
        "abnormal": [
            "Nếu cố xóa mẫu email mặc định của hệ thống: Hệ thống chặn thao tác và báo MSG36."
        ]
    },
    "3.6.32": {
        "summary": "Cho phép Manager hoặc Creator gửi email thông báo cho Client hoặc danh sách người nhận bằng mẫu Email đã chọn. Hệ thống sẽ tự động điền tên người nhận, tên chiến dịch vào đúng vị trí các thẻ biến và tự động lọc bỏ những địa chỉ đã hủy đăng ký nhận tin.",
        "trigger": "Khi Manager hoặc Creator chọn một mẫu Email (/workspace/:id/mail-templates), nhập danh sách người nhận cùng thông tin biến và bấm Gửi email.",
        "interface": "Màn hình Gửi Email theo mẫu gồm ô chọn Mẫu Email, ô chọn hoặc nhập danh sách Địa chỉ Email người nhận, các ô điền giá trị cho biến tự động (nếu cần), khung xem trước bức thư hoàn chỉnh và nút Gửi ngay.",
        "processing": "Hệ thống kiểm tra định dạng email người nhận (BR-04), tự động loại bỏ các địa chỉ nằm trong danh sách từ chối nhận thư (Suppression list - BR-41), điền giá trị thực tế vào các thẻ biến `{{...}}` và đẩy vào hàng đợi gửi thư.",
        "in_req": "Chọn Mẫu Email cần gửi và nhập ít nhất 1 địa chỉ Email người nhận hợp lệ.",
        "in_opt": "Điền thông tin bổ sung cho các biến tùy chỉnh trong thư hoặc chọn giờ gửi theo múi giờ dự án (BR-22).",
        "sys_data": "Tự động ghép nội dung biến, lọc bỏ email đã hủy nhận tin (BR-41) và ghi lại nhật ký gửi thư.",
        "output": "Đưa lệnh gửi email vào hàng đợi xử lý thành công và hiển thị thông báo MSG44.",
        "flow": [
            "Trên màn hình Mẫu Email (/workspace/:id/mail-templates), Manager hoặc Creator chọn một mẫu thư và bấm Gửi Email.",
            "Người dùng chọn danh sách người nhận (Client hoặc thành viên), kiểm tra bản xem trước đã điền sẵn tên chiến dịch/khách hàng và bấm Xác nhận gửi.",
            "Hệ thống kiểm tra định dạng email, lọc bỏ những địa chỉ đã từ chối nhận tin và kiểm tra hạn mức gửi trong ngày (BR-41).",
            "Hệ thống thực hiện gửi email, lưu vào lịch sử gửi của dự án và hiển thị thông báo MSG44."
        ],
        "abnormal": [
            "Nếu danh sách người nhận bị trống hoặc chứa địa chỉ email sai định dạng: Hệ thống báo lỗi MSG02 hoặc MSG04.",
            "Nếu đã vượt quá hạn mức gửi email trong ngày của dự án: Hệ thống báo chạm trần hạn mức (MSG48)."
        ]
    },
    "3.6.33": {
        "summary": "Kiểm tra độ an toàn và tuân thủ tiêu chuẩn cộng đồng của nội dung bài viết trước khi duyệt hoặc đăng bài. Hệ thống tự động rà soát và tô sáng các từ ngữ nhạy cảm, bạo lực, thô tục hoặc từ khóa bị cấm trên mạng xã hội kèm gợi ý sửa lại.",
        "trigger": "Khi Creator hoặc Manager bấm nút Kiểm tra Tuân thủ Nội dung (Check Compliance) trong lúc soạn thảo hoặc duyệt bài viết (/workspace/:id/tasks/:taskId).",
        "interface": "Bảng Kết quả Kiểm tra Tuân thủ ngay cạnh trình soạn thảo bài viết: hiển thị trạng thái Đạt chuẩn (An toàn) hoặc Cảnh báo vi phạm, tô màu đỏ/vàng trực tiếp các từ ngữ vi phạm trong bài viết kèm giải thích lý do và gợi ý từ thay thế.",
        "processing": "Hệ thống gửi văn bản bài viết qua bộ kiểm duyệt an toàn nội dung để đối chiếu với các quy tắc cộng đồng (chống bạo lực, ngôn từ thù ghét, phản cảm, từ khóa cấm quảng cáo - BR-42). Kết quả kiểm tra được lưu lại trên Task làm điều kiện bắt buộc trước khi bài viết được phê duyệt và xuất bản (BR-34, BR-54).",
        "in_req": "Nội dung văn bản bài viết (caption/kịch bản) của Task cần kiểm tra.",
        "in_opt": "Chọn nền tảng mạng xã hội mục tiêu để đối chiếu bộ từ khóa hạn chế tương ứng.",
        "sys_data": "Điểm đánh giá mức độ an toàn, danh sách các cụm từ vi phạm (nếu có) và trạng thái Đạt kiểm duyệt trên Task (BR-42).",
        "output": "Hiển thị kết quả rà soát an toàn nội dung (thông báo MSG37 nếu đạt chuẩn, hoặc cảnh báo MSG45 nếu phát hiện từ vi phạm).",
        "flow": [
            "Sau khi viết xong nội dung bài đăng, Creator hoặc Manager bấm nút Kiểm tra Tuân thủ (Check Compliance).",
            "Hệ thống quét toàn bộ văn bản để tìm các từ ngữ nhạy cảm, bạo lực, thô tục hoặc vi phạm chính sách mạng xã hội (BR-42).",
            "Nếu không có vi phạm, hệ thống đánh dấu bài viết Đạt chuẩn an toàn và hiển thị thông báo MSG37.",
            "Nếu phát hiện từ ngữ vi phạm, hệ thống hiển thị cảnh báo MSG45 và tô sáng các cụm từ đó để Creator sửa lại ngay trước khi gửi duyệt."
        ],
        "abnormal": [
            "Nếu bấm kiểm tra khi bài viết đang để trống hoàn toàn: Hệ thống báo cần nhập nội dung bài viết trước (MSG02)."
        ]
    },
    "3.6.34": {
        "summary": "Cho phép Creator và Manager xem lại toàn bộ lịch sử các phiên bản bài viết đã lưu cũng như các nội dung/hình ảnh đã tạo bằng AI trước đó để đối chiếu sự thay đổi hoặc khôi phục lại bản cũ hoàn toàn miễn phí (không tốn lại điểm AI Credit).",
        "trigger": "Khi Creator hoặc Manager mở bảng Lịch sử Nội dung (Content History) trên màn hình Soạn thảo hoặc Chi tiết Task (/workspace/:id/content-writing).",
        "interface": "Bảng Lịch sử Phiên bản hiển thị danh sách các mốc lưu bài theo thời gian, tên người chỉnh sửa, khung so sánh sự khác biệt giữa bản cũ với bản hiện tại và nút Khôi phục phiên bản này (Restore).",
        "processing": "Hệ thống lấy danh sách các bản chụp phiên bản nội dung (Content Versions) của Task (BR-35). Khi người dùng chọn Khôi phục một phiên bản cũ, hệ thống đưa nội dung đó trở lại làm bản hiện hành và tạo một mốc lịch sử mới mà không trừ bất kỳ điểm AI Credit nào (BR-35, BR-60).",
        "in_req": "Mở mục Lịch sử Nội dung của Task (và chọn phiên bản muốn khôi phục nếu cần).",
        "in_opt": "Chọn 2 phiên bản bất kỳ để xem so sánh chi tiết những câu chữ đã thay đổi.",
        "sys_data": "Danh sách các phiên bản đã lưu (BR-35) và đảm bảo chi phí khôi phục bằng 0 AI Credit (BR-60).",
        "output": "Hiển thị lịch sử phiên bản bài viết hoặc khôi phục bản cũ thành công (hiển thị MSG39).",
        "flow": [
            "Trên màn hình Soạn thảo nội dung (/workspace/:id/content-writing), Creator hoặc Manager bấm mở bảng Lịch sử phiên bản.",
            "Hệ thống hiển thị danh sách các lần lưu bài trước đó kèm thời gian và người thực hiện (BR-35).",
            "Người dùng bấm vào một phiên bản cũ để xem lại câu chữ hoặc tài nguyên AI đã tạo.",
            "Nếu bấm nút Khôi phục phiên bản này, hệ thống áp dụng lại nội dung đó mà không trừ điểm AI Credit (BR-35, BR-60) và báo MSG39."
        ],
        "abnormal": [
            "Nếu đầu việc mới tạo chưa có phiên bản lịch sử nào được lưu: Hệ thống hiển thị thông báo MSG01."
        ]
    },
    "3.6.35": {
        "summary": "Cung cấp phòng nhắn tin trực tuyến theo thời gian thực (Realtime Chat) dành riêng cho các thành viên và Client trong cùng một Workspace, hỗ trợ gửi tin nhắn, trả lời theo luồng, thả biểu tượng cảm xúc và nhắc tên (@mention).",
        "trigger": "Khi thành viên trong dự án mở màn hình Trò chuyện Workspace (/workspace/:id/chat) và gửi tin nhắn trao đổi.",
        "interface": "Màn hình Nhắn tin Workspace (/workspace/:id/chat) gồm danh sách kênh trao đổi trong dự án, khung hiển thị tin nhắn trực tiếp, tính năng trả lời tin nhắn, thả cảm xúc (reactions), gõ @mention nhắc tên và ô nhập tin nhắn.",
        "processing": "Hệ thống kiểm tra người dùng là thành viên hoặc Client đang tham gia trong Workspace đó (cô lập bảo mật tuyệt đối giữa các dự án khác nhau - BR-20, BR-43), truyền tin nhắn tức thì qua kết nối thời gian thực (WebSocket) tới các thành viên đang mở dự án và lưu lịch sử trò chuyện.",
        "in_req": "Nội dung tin nhắn văn bản hoặc biểu tượng cảm xúc gửi trong phòng chat của Workspace.",
        "in_opt": "Trả lời vào một tin nhắn cụ thể (Thread reply) hoặc nhắc tên @mention đồng đội.",
        "sys_data": "Mã tin nhắn, người gửi, thời gian gửi và kiểm soát phạm vi hiển thị chỉ trong nội bộ Workspace (BR-20, BR-43).",
        "output": "Tin nhắn hiển thị ngay lập tức trên màn hình của tất cả thành viên trong kênh dự án.",
        "flow": [
            "Thành viên (Owner, Manager, Creator hoặc Client) mở mục Trò chuyện (/workspace/:id/chat) của Workspace.",
            "Hệ thống kiểm tra quyền thành viên trong dự án (BR-20, BR-43) và tải lịch sử tin nhắn gần nhất.",
            "Người dùng nhập nội dung trao đổi (có thể gõ @ nhắc tên thành viên) và bấm Gửi.",
            "Hệ thống chuyển tin nhắn ngay lập tức tới các thành viên trong kênh dự án."
        ],
        "abnormal": [
            "Nếu người dùng không thuộc Workspace này cố truy cập phòng chat: Hệ thống chặn truy cập và báo MSG07."
        ]
    },

    # ==================== 3.7 AI Features ====================
    "3.7.1": {
        "summary": "Hiển thị bảng gợi ý các chủ đề và từ khóa đang thịnh hành (Trending Topics) trên mạng xã hội phù hợp với ngành hàng của dự án, giúp Creator và Manager nhanh chóng bắt kịp xu hướng để viết bài thu hút tương tác.",
        "trigger": "Khi Creator hoặc Manager mở màn hình Gợi ý Xu hướng AI (/ai-studio/trends).",
        "interface": "Màn hình Gợi ý Xu hướng (/ai-studio/trends) gồm các nút lọc theo lĩnh vực ngành hàng, ô tìm kiếm từ khóa, danh sách các thẻ Chủ đề đang hot (hiển thị Tên chủ đề, Độ tăng trưởng xu hướng, Nền tảng bắt nguồn, Các hashtag liên quan) và nút Dùng chủ đề này để viết Caption.",
        "processing": "Hệ thống lấy danh sách các chủ đề và từ khóa xu hướng mới nhất đã được bộ thu thập tự động tổng hợp và chấm điểm mức độ lan truyền (BR-45), lọc theo ngành hàng mà người dùng chọn và hiển thị lên màn hình.",
        "in_req": "Creator hoặc Manager mở màn hình Gợi ý Xu hướng AI.",
        "in_opt": "Lọc theo nhóm ngành hàng, từ khóa tìm kiếm hoặc khung thời gian (24 giờ qua, 7 ngày qua).",
        "sys_data": "Danh sách chủ đề xu hướng, điểm mức độ thịnh hành, các thẻ hashtag đi kèm và thời gian cập nhật (BR-45).",
        "output": "Hiển thị danh sách các chủ đề đang thịnh hành để đội sáng tạo chọn làm nội dung.",
        "flow": [
            "Creator hoặc Manager mở màn hình Gợi ý Xu hướng AI (/ai-studio/trends).",
            "Hệ thống tải danh sách các chủ đề và từ khóa đang thịnh hành mới nhất (BR-45).",
            "Người dùng lọc theo ngành hàng của nhãn hàng để xem các chủ đề phù hợp nhất.",
            "Người dùng có thể bấm trực tiếp vào một chủ đề xu hướng để chuyển sang màn hình Tạo Caption bằng AI (3.7.6) với chủ đề đó."
        ],
        "abnormal": [
            "Nếu không có chủ đề xu hướng nào khớp với bộ lọc hiện tại: Hệ thống hiển thị thông báo MSG01."
        ]
    },
    "3.7.2": {
        "summary": "Hiển thị trực quan mạng lưới liên kết giữa các chủ đề, từ khóa và thẻ hashtag đang thịnh hành dưới dạng Sơ đồ mạng lưới (Knowledge Graph), giúp người làm nội dung hiểu rõ các từ khóa nào thường đi kèm với nhau trong một trào lưu.",
        "trigger": "Khi Admin hoặc Manager mở màn hình Đồ thị Xu hướng AI (/ai-studio/trends hoặc trên cổng Admin).",
        "interface": "Màn hình Đồ thị Xu hướng hiển thị sơ đồ các nút tròn (biểu diễn Chủ đề, Từ khóa, Nhãn hàng, Hashtag) nối với nhau bằng các đường liên kết, kèm bộ lọc ngành hàng và bảng thông tin chi tiết khi bấm vào từng nút.",
        "processing": "Hệ thống truy xuất mối quan hệ giữa các từ khóa và chủ đề xu hướng đã được phân tích trong cơ sở dữ liệu đồ thị (BR-45), sau đó vẽ sơ đồ mạng lưới tương tác để người dùng phóng to, thu nhỏ và bấm xem từng cụm chủ đề.",
        "in_req": "Admin hoặc Manager mở chế độ xem Đồ thị Xu hướng AI.",
        "in_opt": "Nhập từ khóa trung tâm hoặc lọc theo lĩnh vực để xem nhánh đồ thị liên quan.",
        "sys_data": "Các nút thực thể (Chủ đề, Từ khóa, Hashtag) và mức độ liên kết xuất hiện cùng nhau (BR-45).",
        "output": "Hiển thị sơ đồ mạng lưới liên kết xu hướng trực quan.",
        "flow": [
            "Admin hoặc Manager mở màn hình Đồ thị Xu hướng AI (/ai-studio/trends).",
            "Hệ thống tải dữ liệu các nút từ khóa và đường liên kết xu hướng (BR-45).",
            "Người dùng bấm vào một nút chủ đề bất kỳ trên sơ đồ để xem các từ khóa và hashtag vệ tinh xung quanh chủ đề đó.",
            "Màn hình hiển thị chi tiết ngữ cảnh của xu hướng ở bảng thông tin bên cạnh."
        ],
        "abnormal": [
            "Nếu từ khóa tìm kiếm chưa có trong dữ liệu xu hướng hiện tại: Hệ thống hiển thị thông báo MSG01."
        ]
    },
    "3.7.3": {
        "summary": "Xem danh sách và tra cứu nội dung các tệp Tài liệu hướng dẫn thương hiệu (Brand Guideline) đã tải lên kho kiến thức AI của Workspace, giúp kiểm tra những thông tin mà AI sẽ dựa vào khi viết bài cho nhãn hàng.",
        "trigger": "Khi Manager, Creator hoặc Client mở màn hình Kho Tài liệu Thương hiệu AI (/ai-studio/knowledge-base).",
        "interface": "Màn hình Kho Tài liệu Thương hiệu (/ai-studio/knowledge-base) hiển thị danh sách các tệp tài liệu đã tải lên (Tên tệp, Định dạng PDF/DOCX/TXT, Dung lượng, Trạng thái xử lý Đã sẵn sàng / Đang xử lý), ô tìm kiếm thử nội dung trong tài liệu và nút Tải tài liệu mới.",
        "processing": "Hệ thống kiểm tra quyền thành viên trong Workspace (BR-20), lấy danh sách các tài liệu thương hiệu thuộc riêng Workspace đó (không lẫn với dự án khác - BR-46) và cho phép người dùng gõ câu hỏi/từ khóa để xem thử các đoạn trích dẫn thương hiệu liên quan.",
        "in_req": "Mở màn hình Kho Tài liệu Thương hiệu AI của Workspace.",
        "in_opt": "Nhập từ khóa hoặc câu hỏi để tra cứu thử các đoạn nội dung trong tài liệu thương hiệu.",
        "sys_data": "Danh sách tài liệu thương hiệu của Workspace, trạng thái trích xuất dữ liệu và số đoạn văn bản đã lưu (BR-46).",
        "output": "Hiển thị danh sách tài liệu hướng dẫn thương hiệu và kết quả tra cứu nội dung.",
        "flow": [
            "Manager, Creator hoặc Client mở mục Kho Tài liệu Thương hiệu AI (/ai-studio/knowledge-base) của dự án.",
            "Hệ thống kiểm tra quyền truy cập (BR-20) và hiển thị các tài liệu Brand Guideline đang có của Workspace (BR-46).",
            "Người dùng có thể xem trạng thái xử lý của từng tệp hoặc gõ từ khóa vào ô tra cứu để kiểm tra thông tin thương hiệu.",
            "Màn hình hiển thị danh sách tài liệu và các đoạn trích dẫn khớp với nội dung tìm kiếm."
        ],
        "abnormal": [
            "Nếu dự án chưa tải lên tài liệu thương hiệu nào: Hệ thống hiển thị thông báo trống MSG01 kèm nút Tải tài liệu lên."
        ]
    },
    "3.7.4": {
        "summary": "Cho phép Manager hoặc Client tải tài liệu hướng dẫn thương hiệu (Brand Guideline dạng PDF, DOCX, TXT) lên kho kiến thức của Workspace để AI đọc hiểu thông tin sản phẩm, quy tắc từ ngữ và viết bài đúng giọng điệu của nhãn hàng.",
        "trigger": "Khi Manager hoặc Client bấm nút Tải tài liệu thương hiệu lên trên trang Kho Tài liệu AI (/ai-studio/knowledge-base), chọn tệp và bấm Xác nhận.",
        "interface": "Hộp thoại Tải Tài liệu Thương hiệu gồm khung chọn tệp (PDF, DOCX, TXT tối đa 10 MB) hoặc nhập đường dẫn trang web giới thiệu thương hiệu, ô đặt Tên tài liệu, Mô tả tóm tắt và nút Tải lên.",
        "processing": "Hệ thống kiểm tra quyền của Manager hoặc Client trong dự án (BR-20), kiểm tra tệp đúng định dạng (PDF, DOCX, TXT) và dung lượng hợp lệ, quét an toàn tệp, sau đó tự động trích xuất nội dung văn bản và lưu vào kho dữ liệu AI riêng biệt của Workspace đó (BR-46).",
        "in_req": "Tệp tài liệu thương hiệu (PDF, DOCX hoặc TXT) hoặc đường dẫn thông tin thương hiệu hợp lệ.",
        "in_opt": "Tên hiển thị của tài liệu và ghi chú phân loại (ví dụ: Quy chuẩn giọng văn, Thông tin sản phẩm mới).",
        "sys_data": "Kiểm tra an toàn tệp, lưu trữ tệp gốc và tách các đoạn nội dung vào kho kiến thức AI riêng của Workspace (BR-46).",
        "output": "Tải lên và trích xuất tài liệu thương hiệu thành công, hiển thị thông báo MSG46.",
        "flow": [
            "Manager hoặc Client mở màn hình Kho Tài liệu Thương hiệu AI (/ai-studio/knowledge-base) và bấm Tải tài liệu lên.",
            "Người dùng chọn tệp Brand Guideline (PDF, DOCX hoặc TXT) từ máy tính và bấm Xác nhận.",
            "Hệ thống kiểm tra định dạng, dung lượng tệp và tính an toàn của tài liệu (BR-46).",
            "Hệ thống lưu tệp, trích xuất nội dung vào kho kiến thức AI của Workspace và hiển thị thông báo MSG46."
        ],
        "abnormal": [
            "Nếu chọn tệp sai định dạng (không phải PDF/DOCX/TXT) hoặc vượt quá dung lượng cho phép: Hệ thống từ chối và báo lỗi MSG22."
        ]
    },
    "3.7.5": {
        "summary": "Cho phép Manager hoặc Client xóa bỏ những tài liệu hướng dẫn thương hiệu đã cũ hoặc không còn chính xác khỏi kho kiến thức AI của Workspace để AI không còn dùng thông tin cũ khi viết bài.",
        "trigger": "Khi Manager hoặc Client bấm nút Xóa bên cạnh một tài liệu trên trang Kho Tài liệu Thương hiệu AI (/ai-studio/knowledge-base) và xác nhận.",
        "interface": "Nút Xóa tài liệu kèm hộp thoại xác nhận trên màn hình Kho Tài liệu Thương hiệu AI (/ai-studio/knowledge-base).",
        "processing": "Hệ thống kiểm tra quyền của Manager hoặc Client trong Workspace (BR-20), sau đó xóa hoàn toàn cả tệp tài liệu gốc lẫn toàn bộ các đoạn dữ liệu đã trích xuất của tài liệu đó khỏi kho kiến thức AI của dự án (BR-47).",
        "in_req": "Chọn tài liệu thương hiệu cần xóa và xác nhận đồng ý.",
        "in_opt": "Không bắt buộc.",
        "sys_data": "Xóa tệp lưu trữ gốc và xóa toàn bộ dữ liệu trích xuất tương ứng trong kho AI của Workspace (BR-47).",
        "output": "Xóa tài liệu thương hiệu thành công và hiển thị thông báo MSG46.",
        "flow": [
            "Manager hoặc Client mở màn hình Kho Tài liệu Thương hiệu AI (/ai-studio/knowledge-base) và bấm nút Xóa cạnh tài liệu cũ.",
            "Người dùng bấm Đồng ý trên hộp thoại xác nhận xóa.",
            "Hệ thống kiểm tra quyền hạn trong dự án (BR-20).",
            "Hệ thống xóa tệp gốc cùng toàn bộ dữ liệu trích xuất của tài liệu đó (BR-47) và hiển thị thông báo MSG46."
        ],
        "abnormal": [
            "Nếu tài liệu không tồn tại hoặc người dùng không có quyền xóa: Hệ thống báo MSG01 hoặc MSG07."
        ]
    },
    "3.7.6": {
        "summary": "Giúp Creator tự động viết nội dung bài đăng (Caption) bằng AI dựa trên yêu cầu chủ đề kết hợp với Tài liệu thương hiệu của dự án và các xu hướng đang thịnh hành, đảm bảo bài viết cuốn hút và đúng phong cách nhãn hàng.",
        "trigger": "Khi Creator mở công cụ Tạo Caption bằng AI (/editor), nhập chủ đề bài viết, chọn giọng văn cùng nền tảng mạng xã hội và bấm Tạo Caption.",
        "interface": "Khung Tạo Caption bằng AI trong trình soạn thảo (/editor) gồm ô nhập Chủ đề / Ý tưởng chính, chọn Nền tảng đích (Facebook, Instagram, TikTok, Threads), chọn Giọng điệu (Chuyên nghiệp, Trẻ trung, Hài hước...), tích chọn Áp dụng Tài liệu thương hiệu / Chủ đề xu hướng, hiển thị số điểm AI Credit sẽ dùng và nút Tạo Caption.",
        "processing": "Hệ thống kiểm tra số dư điểm AI Credit của Agency và hạn mức của Workspace còn đủ theo bảng giá hiện hành không (BR-48, BR-60, BR-64). Nếu đủ, hệ thống tạm giữ điểm, lấy thông tin từ Tài liệu thương hiệu của dự án (BR-46, BR-49) để AI viết nội dung. Khi tạo xong thì trừ điểm chính thức; nếu dịch vụ AI gặp lỗi giữa chừng thì hệ thống tự động hoàn lại điểm ngay cho người dùng (BR-48).",
        "in_req": "Chủ đề hoặc ý chính của bài viết cần tạo và Nền tảng mạng xã hội mục tiêu.",
        "in_opt": "Giọng điệu bài viết (Tone of voice), độ dài mong muốn, chọn Chủ đề xu hướng (3.7.1) và bật dùng Tài liệu thương hiệu (3.7.3).",
        "sys_data": "Kiểm tra và trừ điểm AI Credit theo bảng giá (tự động hoàn điểm nếu lỗi - BR-48) và lưu lịch sử nội dung đã tạo (BR-35).",
        "output": "Hiển thị các phương án bài viết (Caption) do AI tạo ra để Creator chọn chèn vào trình soạn thảo (MSG47).",
        "flow": [
            "Trong màn hình Soạn thảo (/editor), Creator mở công cụ Tạo Caption bằng AI, nhập ý tưởng bài viết và chọn nền tảng đăng.",
            "Creator tích chọn kết hợp với Tài liệu thương hiệu của dự án rồi bấm nút Tạo Caption.",
            "Hệ thống kiểm tra số dư điểm AI Credit khả dụng (BR-48), kết hợp thông tin thương hiệu (BR-49) và gọi mô hình AI sinh nội dung.",
            "Hệ thống trừ điểm AI Credit tương ứng, hiển thị bài viết hoàn chỉnh kèm thông báo MSG47 để Creator đưa vào bài đăng."
        ],
        "abnormal": [
            "Nếu quỹ điểm AI Credit của Agency đã hết hoặc vượt quá hạn mức được cấp cho Workspace: Hệ thống dừng thao tác và báo cần nạp thêm hoặc nâng hạn mức điểm (MSG48).",
            "Nếu dịch vụ AI phản hồi quá lâu hoặc gặp sự cố kết nối: Hệ thống tự động hoàn trả lại toàn bộ số điểm AI Credit vừa tạm giữ và báo thông báo MSG49."
        ]
    },
    "3.7.7": {
        "summary": "Cho phép Creator tạo và lưu lại hình mẫu Đại sứ Thương hiệu Ảo (Virtual Brand Ambassador) bằng AI với khuôn mặt và phong cách nhất quán, giúp nhãn hàng có người mẫu đại diện xuyên suốt khi tạo ảnh quảng cáo (3.7.9) và video (3.7.11) mà không cần thuê mẫu chụp lại từ đầu.",
        "trigger": "Khi Creator mở màn hình Đại sứ Thương hiệu Ảo (/ai-studio/ambassadors), mô tả ngoại hình hoặc tải ảnh khuôn mặt mẫu tham chiếu và bấm Tạo Đại sứ ảo.",
        "interface": "Màn hình Tạo Đại sứ Thương hiệu Ảo (/ai-studio/ambassadors) gồm ô nhập Tên nhân vật đại diện, Giới tính, Độ tuổi, Mô tả ngoại hình và trang phục đặc trưng, khung tải ảnh chân dung tham chiếu (tùy chọn), hiển thị chi phí AI Credit và nút Tạo nhân vật.",
        "processing": "Hệ thống kiểm tra số dư và hạn mức điểm AI Credit (BR-48, BR-60), kết hợp mô tả ngoại hình và thông tin nhận diện thương hiệu của dự án (BR-49) để sinh bộ ảnh chân dung chuẩn của nhân vật đại sứ ảo. Nhân vật sau khi lưu có thể được chọn dùng lại nhiều lần khi tạo ảnh và video sản phẩm.",
        "in_req": "Tên nhân vật Đại sứ ảo và Mô tả đặc điểm ngoại hình / phong cách của nhân vật.",
        "in_opt": "Ảnh chân dung tham chiếu định hướng khuôn mặt và trang phục thương hiệu.",
        "sys_data": "Kiểm tra/trừ điểm AI Credit (tự hoàn điểm nếu lỗi - BR-48) và lưu hồ sơ nhân vật Đại sứ ảo vào Workspace (BR-49).",
        "output": "Khởi tạo thành công hình mẫu Đại sứ Thương hiệu Ảo, lưu vào danh sách của dự án và hiển thị thông báo MSG47.",
        "flow": [
            "Creator mở màn hình Đại sứ Thương hiệu Ảo (/ai-studio/ambassadors) và bấm Tạo đại sứ mới.",
            "Creator nhập Tên nhân vật, mô tả độ tuổi, nét mặt, trang phục đại diện cho nhãn hàng và bấm Tạo nhân vật.",
            "Hệ thống kiểm tra số dư điểm AI Credit (BR-48) và gọi dịch vụ AI tạo hình ảnh nhân vật nhất quán (BR-49).",
            "Hệ thống trừ điểm AI Credit, lưu hồ sơ Đại sứ ảo vào dự án để dùng cho các lần tạo ảnh/video sau và báo MSG47."
        ],
        "abnormal": [
            "Nếu không đủ điểm AI Credit: Hệ thống báo lỗi MSG48.",
            "Nếu quá trình tạo hình ảnh gặp sự cố: Hệ thống tự động hoàn lại điểm AI Credit đã giữ và báo MSG49."
        ]
    },
    "3.7.8": {
        "summary": "Hiển thị thư viện các Mẫu phong cách hình ảnh có sẵn (Image Style Templates như Chụp sản phẩm Studio, Tối giản, Cổ điển Vintage, Mùa lễ hội...) kèm ảnh minh họa trực quan, giúp Creator chỉ cần bấm chọn phong cách mà không phải tự viết câu lệnh kỹ thuật dài dòng.",
        "trigger": "Khi Creator mở thư viện Mẫu phong cách ảnh trong màn hình Sáng tạo AI (/editor hoặc /ai-studio).",
        "interface": "Thư viện Mẫu phong cách ảnh hiển thị lưới các thẻ phong cách kèm ảnh mẫu minh họa, tên phong cách (Studio Product, Minimalist, Vintage, Cinematic...), mô tả ánh sáng/bố cục và nút Chọn phong cách này.",
        "processing": "Hệ thống tải danh sách các mẫu phong cách hình ảnh đang hoạt động (BR-49) để Creator xem trước và chọn gắn vào bước tạo hình ảnh AI (3.7.9).",
        "in_req": "Mở danh mục Mẫu phong cách hình ảnh AI.",
        "in_opt": "Lọc theo chủ đề phong cách (Chụp sản phẩm / Thời trang / Lễ hội / Nghệ thuật).",
        "sys_data": "Danh sách mẫu phong cách ảnh kèm cấu hình ánh sáng, góc máy và tông màu thiết lập sẵn (BR-49).",
        "output": "Hiển thị danh sách các Mẫu phong cách hình ảnh để Creator lựa chọn.",
        "flow": [
            "Creator mở công cụ Tạo ảnh trong AI Studio và bấm xem Thư viện Mẫu phong cách ảnh.",
            "Hệ thống hiển thị các thẻ phong cách kèm hình ảnh minh họa mẫu (BR-49).",
            "Creator lọc theo nhóm chủ đề và bấm xem chi tiết hiệu ứng màu sắc/ánh sáng của từng mẫu.",
            "Creator bấm Chọn phong cách ưng ý để áp dụng ngay vào màn hình Tạo hình ảnh bằng AI (3.7.9)."
        ],
        "abnormal": [
            "Nếu tìm kiếm không có mẫu phong cách nào khớp từ khóa: Hệ thống hiển thị thông báo MSG01."
        ]
    },
    "3.7.9": {
        "summary": "Giúp Creator tạo hình ảnh bài đăng hoặc ảnh quảng cáo sản phẩm bằng AI bằng cách kết hợp mô tả ý tưởng với Mẫu phong cách đã chọn (3.7.8), Đại sứ thương hiệu ảo (3.7.7) và ảnh sản phẩm trong kho.",
        "trigger": "Khi Creator mở công cụ Tạo Ảnh bằng AI (/editor), nhập mô tả bức ảnh, chọn phong cách/đại sứ ảo và bấm Tạo hình ảnh.",
        "interface": "Màn hình Tạo Ảnh bằng AI gồm ô nhập Mô tả hình ảnh mong muốn, ô chọn Mẫu phong cách ảnh (3.7.8), ô chọn Đại sứ thương hiệu ảo (3.7.7 - tùy chọn), chọn Tỷ lệ khung hình (1:1, 9:16, 16:9), hiển thị số điểm AI Credit cần dùng và nút Tạo hình ảnh.",
        "processing": "Hệ thống kiểm tra số dư điểm AI Credit của Agency/Workspace (BR-48, BR-60), ghép nối mô tả của người dùng với thông số của Mẫu phong cách, khuôn mặt Đại sứ ảo và màu sắc thương hiệu (BR-49) để sinh ra hình ảnh độ phân giải cao. Ảnh tạo xong có thể lưu thẳng vào Kho tư liệu của dự án (BR-50).",
        "in_req": "Mô tả nội dung bức ảnh cần tạo và Tỷ lệ khung hình mong muốn.",
        "in_opt": "Chọn Mẫu phong cách ảnh (3.7.8), chọn Đại sứ thương hiệu ảo (3.7.7) và chọn ảnh sản phẩm tham chiếu từ kho.",
        "sys_data": "Kiểm tra và trừ điểm AI Credit theo bảng giá (tự hoàn điểm nếu lỗi - BR-48, BR-64) và lưu ảnh kết quả (BR-50).",
        "output": "Hiển thị hình ảnh quảng cáo do AI tạo ra, cho phép lưu vào Kho tư liệu hoặc chèn ngay vào bài viết (MSG47).",
        "flow": [
            "Creator mở công cụ Tạo Ảnh bằng AI, nhập mô tả bối cảnh bức ảnh muốn tạo.",
            "Creator chọn thêm Mẫu phong cách ảnh (3.7.8), chọn Đại sứ thương hiệu ảo (3.7.7) nếu muốn có người mẫu và chọn tỷ lệ khung hình.",
            "Creator bấm nút Tạo hình ảnh.",
            "Hệ thống kiểm tra và trừ điểm AI Credit (BR-48), sinh hình ảnh theo đúng thiết lập (BR-49), hiển thị kết quả và báo MSG47."
        ],
        "abnormal": [
            "Nếu số dư điểm AI Credit không đủ: Hệ thống chặn thao tác và báo MSG48.",
            "Nếu quá trình sinh ảnh gặp lỗi kết nối với máy chủ AI: Hệ thống tự động hoàn trả lại số điểm AI Credit đã giữ và báo MSG49."
        ]
    },
    "3.7.10": {
        "summary": "Hiển thị thư viện các Mẫu phong cách và chuyển động máy quay dành riêng cho Video AI (như Quay cận cảnh sản phẩm, Chuyển động xoay vòng, Slow-motion điện ảnh...), giúp Creator dễ dàng chọn nhịp điệu cho video ngắn Reels/TikTok.",
        "trigger": "Khi Creator mở danh mục Mẫu phong cách Video trong màn hình Tạo Video AI (/ai-studio/video).",
        "interface": "Thư viện Mẫu phong cách Video (/ai-studio/video) hiển thị các thẻ mẫu kèm hình động minh họa góc máy (Pan, Zoom, Orbit, Cinematic), nhịp điệu chuyển cảnh và nút Chọn mẫu này.",
        "processing": "Hệ thống tải danh sách các mẫu chuyển động và phong cách ánh sáng video được thiết lập sẵn (BR-49) để Creator chọn áp dụng khi tạo video ngắn bằng AI (3.7.11).",
        "in_req": "Mở danh mục Mẫu phong cách Video AI.",
        "in_opt": "Lọc theo kiểu chuyển động máy quay hoặc thể loại video (Reels / TikTok / Giới thiệu sản phẩm).",
        "sys_data": "Danh sách mẫu phong cách video và các thông số góc quay thiết lập sẵn (BR-49).",
        "output": "Hiển thị danh sách Mẫu phong cách Video để Creator lựa chọn.",
        "flow": [
            "Creator mở màn hình Tạo Video AI (/ai-studio/video) và bấm xem Thư viện Mẫu phong cách Video.",
            "Hệ thống hiển thị danh sách các mẫu chuyển động camera và hiệu ứng ánh sáng mẫu (BR-49).",
            "Creator xem trước hiệu ứng chuyển động của từng mẫu.",
            "Creator bấm Chọn mẫu phù hợp để áp dụng vào bước Tạo Video bằng AI (3.7.11)."
        ],
        "abnormal": [
            "Nếu không có mẫu video nào khớp với từ khóa tìm kiếm: Hệ thống hiển thị thông báo MSG01."
        ]
    },
    "3.7.11": {
        "summary": "Giúp Creator tạo các đoạn video ngắn bằng AI (phục vụ đăng Reels, TikTok, Story) từ kịch bản mô tả cảnh quay kết hợp với hình ảnh sản phẩm/Đại sứ ảo (3.7.7) và Mẫu phong cách chuyển động video (3.7.10).",
        "trigger": "Khi Creator mở màn hình Tạo Video bằng AI (/ai-studio/video), nhập mô tả cảnh quay, chọn mẫu chuyển động cùng tỷ lệ khung hình và bấm Tạo Video.",
        "interface": "Màn hình Tạo Video bằng AI (/ai-studio/video) gồm ô nhập Mô tả cảnh quay chuyển động, ô chọn Ảnh gốc / Đại sứ thương hiệu ảo (3.7.7), chọn Mẫu phong cách chuyển động (3.7.10), chọn Tỷ lệ khung hình (9:16 dọc hoặc 16:9 ngang), Thời lượng video, chi phí điểm AI Credit và nút Tạo Video.",
        "processing": "Hệ thống kiểm tra số dư và hạn mức điểm AI Credit (BR-48, BR-60, BR-64), tạm giữ số điểm tương ứng và gửi yêu cầu dựng video dựa trên hình ảnh tham chiếu cùng mẫu chuyển động đã chọn (BR-49). Khi video dựng xong, hệ thống trừ điểm chính thức và cho phép lưu vào Kho tư liệu (BR-50); nếu lỗi thì tự động hoàn trả lại toàn bộ điểm AI Credit (BR-48).",
        "in_req": "Mô tả cảnh quay video cần tạo, Tỷ lệ khung hình và Thời lượng video.",
        "in_opt": "Chọn Ảnh bắt đầu / Đại sứ thương hiệu ảo (3.7.7) và chọn Mẫu phong cách chuyển động camera (3.7.10).",
        "sys_data": "Kiểm tra/trừ điểm AI Credit (tự động hoàn điểm nếu lỗi - BR-48), xử lý hàng đợi dựng video và lưu tệp video kết quả (BR-50).",
        "output": "Tạo video ngắn bằng AI thành công, hiển thị trình phát xem trước và thông báo MSG47.",
        "flow": [
            "Creator mở màn hình Tạo Video bằng AI (/ai-studio/video) và nhập mô tả cảnh quay mong muốn.",
            "Creator chọn hình ảnh sản phẩm hoặc Đại sứ ảo làm khung hình gốc, chọn Mẫu phong cách video (3.7.10) và tỷ lệ 9:16 cho Reels/TikTok.",
            "Creator bấm nút Tạo Video.",
            "Hệ thống kiểm tra và trừ điểm AI Credit (BR-48), tiến hành dựng video (BR-49), hiển thị video hoàn chỉnh và báo MSG47."
        ],
        "abnormal": [
            "Nếu không đủ điểm AI Credit hoặc vượt hạn mức của Workspace: Hệ thống báo lỗi MSG48.",
            "Nếu tiến trình dựng video bị gián đoạn: Hệ thống tự động hoàn trả đủ điểm AI Credit đã giữ và báo MSG49."
        ]
    },
    "3.7.12": {
        "summary": "Cho phép Creator hoặc Manager xuất và tải các hình ảnh, video do AI tạo ra về máy tính theo đúng định dạng chuẩn (MP4, WebM cho video; PNG, JPG, WEBP cho ảnh) và tỷ lệ khung hình tối ưu cho từng mạng xã hội mà không tốn thêm điểm AI Credit.",
        "trigger": "Khi Creator hoặc Manager chọn một ấn phẩm AI đã tạo, chọn định dạng tệp cần xuất và bấm Xuất tệp (Export File).",
        "interface": "Hộp thoại Xuất tệp Đa phương tiện gồm ô chọn Định dạng xuất (Ảnh: PNG, JPG, WEBP; Video: MP4, WebM), chọn Chất lượng / Tỷ lệ khung hình (9:16, 1:1, 16:9), tùy chọn Lưu đồng thời vào Kho tư liệu và nút Xuất & Tải về.",
        "processing": "Hệ thống kiểm tra quyền thành viên trong Workspace (BR-20), chuyển đổi ấn phẩm AI sang đúng định dạng tệp mà người dùng yêu cầu (BR-50) và cho phép tải về máy hoàn toàn miễn phí (không trừ thêm AI Credit).",
        "in_req": "Chọn ấn phẩm AI cần xuất và chọn Định dạng tệp đầu ra (PNG/JPG/WEBP hoặc MP4/WebM).",
        "in_opt": "Tùy chọn lưu thêm một bản vào Kho tư liệu của Workspace.",
        "sys_data": "Chuyển đổi định dạng tệp theo chuẩn mạng xã hội với chi phí 0 AI Credit (BR-50).",
        "output": "Xuất tệp theo đúng định dạng đã chọn và tải về máy tính của người dùng.",
        "flow": [
            "Sau khi tạo xong hình ảnh hoặc video trong AI Studio, Creator hoặc Manager bấm nút Xuất tệp (Export File).",
            "Người dùng chọn định dạng tệp mong muốn (ví dụ MP4 cho video hoặc WEBP/PNG cho ảnh) và bấm Xác nhận xuất.",
            "Hệ thống kiểm tra quyền truy cập (BR-20) và xử lý đóng gói tệp theo định dạng đã chọn (BR-50).",
            "Hệ thống tải tệp về máy người dùng (và lưu vào Kho tư liệu nếu được chọn)."
        ],
        "abnormal": [
            "Nếu chọn định dạng không tương thích với loại tệp (ví dụ chọn xuất ảnh sang định dạng video): Hệ thống báo lỗi MSG22."
        ]
    },
    "3.7.13": {
        "summary": "Cho phép Admin cài đặt lịch chạy tự động (theo giờ/ngày) và các nguồn thu thập dữ liệu cho bộ cập nhật xu hướng thịnh hành của hệ thống.",
        "trigger": "Khi Admin mở màn hình Cấu hình Thu thập Xu hướng (/admin), điều chỉnh lịch chạy hoặc nguồn dữ liệu và bấm Lưu cấu hình.",
        "interface": "Bảng Cấu hình Thu thập Xu hướng trên cổng Admin gồm ô chọn Chu kỳ chạy tự động (mỗi 6 giờ, 12 giờ, hàng ngày), danh sách nguồn thu thập, bộ lọc ngành hàng, giới hạn số lượng chủ đề mỗi đợt và nút Lưu cấu hình.",
        "processing": "Hệ thống kiểm tra quyền Admin toàn hệ thống (BR-62), kiểm tra thông số chu kỳ thời gian hợp lệ, lưu cấu hình mới cho tiến trình thu thập xu hướng tự động (BR-45) và ghi lại vào nhật ký quản trị (BR-65).",
        "in_req": "Chu kỳ thời gian chạy thu thập tự động và danh sách nguồn/lĩnh vực thu thập.",
        "in_opt": "Giới hạn số lượng từ khóa tối đa thu thập trong mỗi phiên.",
        "sys_data": "Cập nhật lịch chạy tiến trình ngầm (BR-45) và lưu nhật ký thao tác của Admin (BR-65).",
        "output": "Lưu cấu hình lịch thu thập xu hướng thành công và hiển thị thông báo MSG60.",
        "flow": [
            "Admin mở phần Cấu hình Thu thập Xu hướng trên cổng quản trị (/admin).",
            "Admin chọn chu kỳ quét tự động, bật các nguồn chủ đề và đặt giới hạn số lượng bản ghi mỗi đợt.",
            "Admin bấm nút Lưu cấu hình.",
            "Hệ thống kiểm tra quyền Admin (BR-62), áp dụng lịch chạy mới (BR-45), ghi nhật ký hệ thống (BR-65) và hiển thị thông báo MSG60."
        ],
        "abnormal": [
            "Nếu người thao tác không có quyền Admin hoặc nhập chu kỳ thời gian sai định dạng: Hệ thống báo lỗi MSG07 hoặc MSG03."
        ]
    },
    "3.7.14": {
        "summary": "Tự động gợi ý các thẻ Hashtag đang thịnh hành và sát nhất với nội dung bài viết mà Creator đang soạn thảo (hoặc khi tạo bộ sưu tập Hashtag), giúp tăng khả năng tiếp cận người xem trên mạng xã hội.",
        "trigger": "Khi Creator bấm nút Gợi ý Hashtag bằng AI ngay trong màn hình Soạn thảo bài viết (/editor) hoặc trong màn hình Bộ sưu tập Hashtag (/workspace/:id/hashtag-groups).",
        "interface": "Bảng Gợi ý Hashtag Xu hướng hiển thị danh sách các thẻ hashtag do AI đề xuất dựa trên nội dung bài viết, kèm mức độ phổ biến của từng thẻ, ô tích chọn và nút Chèn vào bài viết / Lưu vào bộ sưu tập.",
        "processing": "Hệ thống đọc nội dung bài viết hoặc chủ đề ngành hàng hiện tại, đối chiếu với dữ liệu xu hướng đang thịnh hành (BR-45) để lọc ra bộ thẻ hashtag phù hợp nhất, chuẩn hóa dấu '#' và cho phép Creator chèn nhanh vào bài hoặc lưu vào bộ sưu tập của Workspace (BR-39).",
        "in_req": "Nội dung bài viết đang soạn hoặc chủ đề ngành hàng cần gợi ý hashtag.",
        "in_opt": "Chọn nền tảng mạng xã hội mục tiêu và số lượng hashtag muốn gợi ý.",
        "sys_data": "Danh sách thẻ hashtag gợi ý kèm điểm mức độ thịnh hành (BR-39, BR-45).",
        "output": "Hiển thị danh sách Hashtag xu hướng do AI đề xuất (MSG47) để người dùng chọn áp dụng.",
        "flow": [
            "Trong lúc viết bài (/editor) hoặc tạo nhóm Hashtag (/workspace/:id/hashtag-groups), Creator bấm nút Gợi ý Hashtag bằng AI.",
            "Hệ thống phân tích nội dung bài viết và đối chiếu với các từ khóa xu hướng mới nhất (BR-45).",
            "Màn hình hiển thị danh sách các thẻ hashtag phù hợp kèm thông báo MSG47.",
            "Creator tích chọn các thẻ ưng ý để chèn thẳng vào bài viết hoặc lưu vào bộ sưu tập của dự án (BR-39)."
        ],
        "abnormal": [
            "Nếu ô nội dung bài viết và chủ đề đều đang để trống: Hệ thống nhắc người dùng nhập chủ đề hoặc nội dung trước khi gợi ý (MSG02)."
        ]
    },
    "3.7.15": {
        "summary": "Cho phép Owner và Manager xem, tìm kiếm và lọc danh bạ các đối tác truyền thông bên thứ ba của Agency (gồm KOL, KOC, Báo điện tử, Trang đặt Banner quảng cáo và Kênh truyền hình) kèm bảng giá tham khảo và tiến độ hợp tác.",
        "trigger": "Khi Owner hoặc Manager mở màn hình Danh bạ Đối tác Truyền thông (/collaborators).",
        "interface": "Màn hình Danh bạ Đối tác (/collaborators) gồm ô tìm kiếm tên đối tác, bộ lọc theo loại hình (KOL/KOC, Báo điện tử, Banner, Kênh TV), lọc theo lĩnh vực ngành hàng, bảng danh sách đối tác (Tên, Lĩnh vực, Lượng người theo dõi/độc giả, Đơn giá tham khảo, Trạng thái hợp tác) và nút Thêm đối tác mới.",
        "processing": "Hệ thống kiểm tra quyền truy cập của Owner hoặc Manager (BR-20), lấy danh sách các đối tác truyền thông trong danh bạ của Agency (BR-51) và hiển thị theo bộ lọc người dùng chọn.",
        "in_req": "Owner hoặc Manager mở màn hình Danh bạ Đối tác Truyền thông.",
        "in_opt": "Tìm kiếm theo tên hoặc lọc theo phân loại kênh, ngành hàng, khoảng giá.",
        "sys_data": "Danh sách hồ sơ đối tác truyền thông, chỉ số tiếp cận và trạng thái hợp tác hiện tại (BR-51).",
        "output": "Hiển thị bảng danh bạ các đối tác truyền thông bên thứ ba của Agency.",
        "flow": [
            "Owner hoặc Manager mở màn hình Danh bạ Đối tác Truyền thông (/collaborators).",
            "Hệ thống kiểm tra quyền truy cập (BR-20) và tải danh sách đối tác của Agency (BR-51).",
            "Người dùng có thể lọc theo nhóm KOL/KOC, Báo chí hoặc Kênh quảng cáo và so sánh mức giá tham khảo.",
            "Người dùng bấm vào từng đối tác để xem chi tiết thông tin liên hệ và lịch sử hợp tác."
        ],
        "abnormal": [
            "Nếu không có đối tác nào khớp với điều kiện lọc: Hệ thống hiển thị thông báo MSG01."
        ]
    },
    "3.7.16": {
        "summary": "Cho phép Owner hoặc Manager thêm mới hồ sơ một đối tác truyền thông bên thứ ba (KOL/KOC, Báo điện tử, Kênh quảng cáo) vào danh bạ của Agency để tiện liên hệ và lập kế hoạch booking cho các chiến dịch.",
        "trigger": "Khi Owner hoặc Manager bấm nút Thêm đối tác mới trên màn hình Danh bạ Đối tác (/collaborators), điền thông tin và bấm Lưu.",
        "interface": "Biểu mẫu Thêm Đối tác Truyền thông gồm ô nhập Tên đối tác / Kênh, chọn Loại hình (KOL, KOC, Báo điện tử, Banner, TV), chọn Lĩnh vực chuyên môn, nhập Quy mô người theo dõi / lượt xem trung bình, Đơn giá tham khảo, Email / Số điện thoại liên hệ và nút Lưu hồ sơ.",
        "processing": "Hệ thống kiểm tra quyền của Owner hoặc Manager (BR-15, BR-51), kiểm tra tên đối tác, phân loại kênh và email liên hệ hợp lệ (BR-04), sau đó lưu hồ sơ đối tác mới vào danh bạ chung của Agency (BR-51).",
        "in_req": "Tên đối tác truyền thông, Phân loại kênh (KOL/KOC/Báo chí/Banner/TV), Lĩnh vực hoạt động và Thông tin liên hệ.",
        "in_opt": "Số lượng người theo dõi/độc giả, Đơn giá booking tham khảo, đường dẫn trang cá nhân/website và ghi chú.",
        "sys_data": "Mã hồ sơ đối tác mới và trạng thái hoạt động trong danh bạ của Agency (BR-51).",
        "output": "Thêm hồ sơ đối tác truyền thông mới thành công và hiển thị thông báo MSG50.",
        "flow": [
            "Owner hoặc Manager mở màn hình Danh bạ Đối tác (/collaborators) và bấm nút Thêm đối tác mới.",
            "Người dùng nhập Tên đối tác, chọn Loại hình kênh, Ngành hàng thế mạnh, Đơn giá tham khảo và Email/Số điện thoại liên hệ.",
            "Người dùng bấm nút Lưu hồ sơ.",
            "Hệ thống kiểm tra thông tin hợp lệ, lưu đối tác mới vào danh bạ Agency (BR-51) và hiển thị thông báo MSG50."
        ],
        "abnormal": [
            "Nếu bỏ trống Tên đối tác, Loại hình kênh hoặc nhập sai định dạng email liên hệ: Hệ thống báo lỗi MSG02 hoặc MSG04."
        ]
    },
    "3.7.17": {
        "summary": "Cho phép Owner hoặc Manager cập nhật thông tin hồ sơ, bảng giá của đối tác truyền thông và theo dõi tiến độ hợp tác thực tế trong chiến dịch (Đã liên hệ -> Đang đàm phán -> Đã chốt -> Đang lên sóng).",
        "trigger": "Khi Owner hoặc Manager mở hồ sơ một đối tác trên trang Danh bạ Đối tác (/collaborators), sửa thông tin hoặc cập nhật trạng thái hợp tác và bấm Lưu.",
        "interface": "Biểu mẫu Cập nhật Đối tác gồm các ô sửa thông tin liên hệ, đơn giá, chỉ số tiếp cận, hộp chọn Trạng thái hợp tác trong chiến dịch (CONTACTED, NEGOTIATING, CONFIRMED, LIVE_ON_AIR) kèm ô dán đường dẫn bài đăng nghiệm thu và nút Lưu cập nhật.",
        "processing": "Hệ thống kiểm tra quyền của Owner/Manager, lưu lại thông tin mới của đối tác và cập nhật trạng thái tiến độ hợp tác trong chiến dịch liên kết (BR-51).",
        "in_req": "Chọn hồ sơ đối tác cần sửa và nhập các thông tin / trạng thái hợp tác mới.",
        "in_opt": "Chi phí thỏa thuận thực tế và đường dẫn bài viết/quảng cáo đã lên sóng (link nghiệm thu).",
        "sys_data": "Cập nhật trạng thái hợp tác chiến dịch (BR-51) và thời gian chỉnh sửa hồ sơ.",
        "output": "Cập nhật hồ sơ và trạng thái đối tác thành công, hiển thị thông báo MSG50.",
        "flow": [
            "Owner hoặc Manager mở hồ sơ của một đối tác trong Danh bạ Đối tác (/collaborators) và chọn Chỉnh sửa.",
            "Người dùng cập nhật lại bảng giá, thông tin liên hệ hoặc chuyển trạng thái hợp tác (ví dụ từ Đang đàm phán sang Đã chốt / Đang lên sóng).",
            "Người dùng bấm nút Lưu cập nhật.",
            "Hệ thống lưu thông tin mới vào cơ sở dữ liệu (BR-51) và hiển thị thông báo MSG50."
        ],
        "abnormal": [
            "Nếu xóa trống Tên đối tác hoặc nhập mức giá âm: Hệ thống báo lỗi MSG02 hoặc MSG03."
        ]
    },
    "3.7.18": {
        "summary": "Cho phép Owner hoặc Manager xóa mềm (ngừng kích hoạt) hồ sơ một đối tác truyền thông khỏi danh bạ đang hoạt động của Agency, trong khi vẫn giữ nguyên dữ liệu lịch sử của đối tác đó trong các chiến dịch cũ.",
        "trigger": "Khi Owner hoặc Manager bấm nút Xóa bên cạnh một đối tác trong Danh bạ Đối tác (/collaborators) và xác nhận.",
        "interface": "Nút Xóa đối tác kèm hộp thoại xác nhận trên màn hình Danh bạ Đối tác Truyền thông (/collaborators).",
        "processing": "Hệ thống kiểm tra quyền của Owner hoặc Manager (BR-15, BR-51), chuyển trạng thái đối tác sang Ngừng hoạt động (ẩn khỏi danh sách chọn mới và gợi ý mới) nhưng bảo toàn nguyên vẹn lịch sử chi phí và bài nghiệm thu ở các chiến dịch trước (BR-51).",
        "in_req": "Chọn hồ sơ đối tác cần gỡ khỏi danh bạ và xác nhận đồng ý.",
        "in_opt": "Không bắt buộc.",
        "sys_data": "Đánh dấu xóa mềm hồ sơ đối tác và bảo toàn lịch sử hợp tác chiến dịch cũ (BR-51).",
        "output": "Gỡ đối tác khỏi danh bạ hoạt động thành công và hiển thị thông báo MSG50.",
        "flow": [
            "Trên màn hình Danh bạ Đối tác (/collaborators), Owner hoặc Manager bấm nút Xóa cạnh đối tác không còn hợp tác.",
            "Người dùng bấm Đồng ý trên hộp thoại xác nhận.",
            "Hệ thống kiểm tra quyền hạn (BR-15) và chuyển hồ sơ đối tác sang trạng thái ngừng hoạt động (BR-51).",
            "Hệ thống ẩn đối tác khỏi danh bạ hiện hành và hiển thị thông báo MSG50."
        ],
        "abnormal": [
            "Nếu hồ sơ đối tác đó đã bị xóa từ trước: Hệ thống hiển thị thông báo MSG36."
        ]
    },
    "3.7.19": {
        "summary": "Sử dụng AI để tự động phân tích và đề xuất danh sách các đối tác truyền thông bên thứ ba (KOL/KOC, báo chí, kênh quảng cáo) trong danh bạ phù hợp nhất với ngành hàng, tệp khách hàng mục tiêu và ngân sách của chiến dịch.",
        "trigger": "Khi Manager hoặc Client mở tính năng Gợi ý Đối tác bằng AI (/campaign-partners), chọn ngành hàng cùng mức ngân sách dự kiến và bấm Gợi ý đối tác.",
        "interface": "Màn hình Gợi ý Đối tác bằng AI (/campaign-partners) gồm ô chọn Chiến dịch / Ngành hàng thương hiệu, nhập Ngân sách dự kiến, chọn Mục tiêu (Tăng nhận diện / Tăng tương tác / Ra mắt sản phẩm), cùng danh sách các đối tác được AI xếp hạng theo độ phù hợp.",
        "processing": "Hệ thống đối chiếu ngành hàng, đối tượng khán giả và mức ngân sách của chiến dịch với dữ liệu các đối tác đang hoạt động trong danh bạ của Agency (BR-51), sau đó chấm điểm mức độ phù hợp và xếp hạng các phương án tối ưu nhất để Manager và Client lựa chọn (BR-52).",
        "in_req": "Ngành hàng của chiến dịch, Mục tiêu truyền thông và Mức ngân sách dự kiến.",
        "in_opt": "Lọc riêng theo nhóm kênh mong muốn (chỉ tìm KOL/KOC hoặc chỉ tìm Báo điện tử).",
        "sys_data": "Điểm đánh giá mức độ phù hợp của từng đối tác với ngân sách và ngành hàng của chiến dịch (BR-52).",
        "output": "Hiển thị danh sách các đối tác truyền thông được AI xếp hạng đề xuất kèm thông báo MSG50.",
        "flow": [
            "Manager hoặc Client mở màn hình Gợi ý Đối tác bằng AI (/campaign-partners) trong dự án.",
            "Người dùng chọn ngành hàng của nhãn hàng, nhập mức ngân sách dự kiến cho việc thuê đối tác và bấm Gợi ý.",
            "Hệ thống phân tích và chấm điểm độ tương thích của các đối tác trong danh bạ Agency (BR-51, BR-52).",
            "Màn hình hiển thị danh sách đối tác phù hợp nhất theo thứ tự ưu tiên để dự án liên hệ hợp tác (MSG50)."
        ],
        "abnormal": [
            "Nếu trong danh bạ chưa có đối tác nào thuộc ngành hàng hoặc tầm ngân sách đã chọn: Hệ thống hiển thị thông báo MSG01."
        ]
    },
}
