# -*- coding: utf-8 -*-
"""
Practical, simple, logical Vietnamese specifications for FRs in domains 3.2, 3.3, 3.4, 3.5 (52 FRs).
Each entry is a dict with:
- summary: Short, natural explanation of what the feature does in practice
- trigger: When the user uses this feature
- interface: What appears on the screen
- processing: How the system checks and processes the action
- in_req: Required user inputs
- in_opt: Optional inputs / filters
- sys_data: What the system automatically records or verifies
- output: What the user gets as the result
- flow: List of 4 clear, logical steps
- abnormal: List of 2-3 practical error handling cases
"""

FRS_PART1 = {
    # ==================== 3.2 Authentication & Authorization ====================
    "3.2.1": {
        "summary": "Cho phép người dùng mới (Guest) tạo tài khoản BrandHub bằng Họ tên, Email và Mật khẩu trên trang Đăng ký (/register), sau đó nhận mã OTP 6 số qua email để kích hoạt tài khoản.",
        "trigger": "Khi Guest mở trang Đăng ký (/register), điền thông tin cá nhân và bấm nút Tạo tài khoản.",
        "interface": "Màn hình Đăng ký (/register) gồm các ô nhập: Họ và tên, Địa chỉ Email, Mật khẩu, Nhập lại mật khẩu, nút Tạo tài khoản và nút chuyển sang Đăng nhập bằng Google.",
        "processing": "Hệ thống kiểm tra các ô bắt buộc không bị bỏ trống, định dạng email hợp lệ và email chưa từng được đăng ký trước đó (BR-01). Tiếp theo, hệ thống kiểm tra mật khẩu đủ độ an toàn (ít nhất 8 ký tự, có chữ số - BR-02), lưu tài khoản ở trạng thái chờ xác thực, tạo mã OTP 6 số có hiệu lực 10 phút (BR-03) gửi về email và chuyển người dùng sang màn hình nhập OTP.",
        "in_req": "Họ và tên, Địa chỉ Email, Mật khẩu (tối thiểu 8 ký tự và có ít nhất 1 chữ số), Nhập lại mật khẩu xác nhận.",
        "in_opt": "Không bắt buộc.",
        "sys_data": "Mã tài khoản mới, mật khẩu đã mã hóa bảo mật, trạng thái tài khoản Chờ xác thực (PENDING_VERIFICATION) và mã OTP 6 số (hiệu lực 10 phút).",
        "output": "Tạo tài khoản thành công, gửi mã OTP qua email (hiển thị thông báo MSG10) và chuyển sang màn hình Xác thực OTP (3.2.6).",
        "flow": [
            "Guest mở trang Đăng ký (/register) và điền đầy đủ Họ tên, Email, Mật khẩu và Nhập lại mật khẩu.",
            "Guest bấm nút Tạo tài khoản.",
            "Hệ thống kiểm tra email chưa bị trùng (BR-01) và mật khẩu đáp ứng đúng điều kiện bảo mật (BR-02).",
            "Hệ thống lưu tài khoản ở trạng thái chờ kích hoạt, gửi mã OTP 6 số (hiệu lực 10 phút - BR-03) vào email và chuyển sang màn hình nhập OTP (3.2.6)."
        ],
        "abnormal": [
            "Nếu bỏ trống thông tin, nhập sai định dạng email hoặc mật khẩu chưa đủ 8 ký tự/thiếu số: Hệ thống báo lỗi ngay dưới ô nhập (MSG02, MSG04, MSG05, MSG06) để người dùng sửa lại.",
            "Nếu địa chỉ email này đã được đăng ký trước đó: Hệ thống thông báo email đã tồn tại (MSG08) và gợi ý chuyển sang trang Đăng nhập."
        ]
    },
    "3.2.2": {
        "summary": "Cho phép người dùng đăng nhập vào hệ thống bằng Email và Mật khẩu trên trang Đăng nhập (/login). Nếu tài khoản có bật bảo mật 2 lớp (2FA) thì hệ thống sẽ yêu cầu nhập thêm mã xác nhận từ điện thoại.",
        "trigger": "Khi người dùng mở trang Đăng nhập (/login), nhập Email cùng Mật khẩu và bấm nút Đăng nhập.",
        "interface": "Màn hình Đăng nhập (/login) gồm ô nhập Email, ô nhập Mật khẩu (có nút ẩn/hiện mật khẩu), nút Đăng nhập, đường dẫn Quên mật khẩu và nút Đăng nhập bằng Google.",
        "processing": "Hệ thống đối chiếu email và mật khẩu với dữ liệu đã lưu (BR-01, BR-02), đồng thời kiểm tra tài khoản đã xác thực email và không bị khóa (BR-05). Nếu tài khoản có bật 2FA thì chuyển sang bước nhập mã 6 số (BR-09); nếu không bật 2FA thì khởi tạo ngay phiên đăng nhập và đưa người dùng vào màn hình làm việc.",
        "in_req": "Địa chỉ Email và Mật khẩu đăng nhập.",
        "in_opt": "Tùy chọn Ghi nhớ tài khoản cho lần đăng nhập sau.",
        "sys_data": "Trạng thái hoạt động của tài khoản, số lần nhập sai mật khẩu liên tiếp (khóa tạm 15 phút nếu sai 5 lần - BR-06) và mã phiên làm việc.",
        "output": "Đăng nhập thành công vào màn hình chính (hoặc chuyển sang màn hình nhập mã bảo mật 2 lớp 3.2.7 nếu tài khoản có bật 2FA).",
        "flow": [
            "Người dùng mở trang Đăng nhập (/login), nhập Email và Mật khẩu rồi bấm Đăng nhập.",
            "Hệ thống kiểm tra thông tin đăng nhập và trạng thái tài khoản đang hoạt động (BR-05).",
            "Nếu tài khoản có bật bảo mật 2 lớp (2FA), hệ thống chuyển sang màn hình nhập mã xác nhận 6 số từ ứng dụng Authenticator (3.2.7).",
            "Nếu thông tin hợp lệ, hệ thống tạo phiên đăng nhập và chuyển người dùng vào trang làm việc chính theo đúng vai trò."
        ],
        "abnormal": [
            "Nếu nhập sai email hoặc mật khẩu: Hệ thống báo thông tin đăng nhập không chính xác (MSG09). Nếu nhập sai liên tiếp 5 lần trong 15 phút, tài khoản sẽ tạm khóa đăng nhập trong 15 phút (BR-06, MSG11).",
            "Nếu tài khoản chưa xác thực email: Hệ thống gửi mã OTP mới và chuyển sang màn hình Xác thực OTP (3.2.6).",
            "Nếu tài khoản đang bị khóa hoặc đã xóa: Hệ thống từ chối đăng nhập và hiển thị thông báo MSG12."
        ]
    },
    "3.2.3": {
        "summary": "Cho phép người dùng đăng ký hoặc đăng nhập nhanh chỉ với 1 cú nhấp chuột bằng tài khoản Google mà không cần phải nhớ mật khẩu riêng trên BrandHub.",
        "trigger": "Khi người dùng bấm vào nút Tiếp tục với Google (Continue with Google) trên trang Đăng nhập (/login) hoặc Đăng ký (/register).",
        "interface": "Nút Tiếp tục với Google trên màn hình Đăng nhập/Đăng ký và cửa sổ chọn tài khoản chính thức của Google.",
        "processing": "Sau khi người dùng chọn tài khoản Google, hệ thống nhận thông tin email đã xác thực từ Google. Nếu email này đã có tài khoản trên BrandHub thì hệ thống tự động liên kết và đăng nhập luôn; nếu chưa có thì hệ thống tự tạo tài khoản mới (lấy sẵn họ tên và ảnh đại diện từ Google - BR-07) và đăng nhập ngay vào hệ thống.",
        "in_req": "Tài khoản Google hợp lệ do người dùng chọn xác nhận trên cửa sổ Google.",
        "in_opt": "Không bắt buộc.",
        "sys_data": "Email, họ tên, ảnh đại diện từ Google, trạng thái tài khoản (BR-05) và mã phiên đăng nhập.",
        "output": "Đăng nhập thành công và chuyển thẳng vào màn hình làm việc chính.",
        "flow": [
            "Người dùng bấm nút Tiếp tục với Google trên trang Đăng nhập (/login) hoặc Đăng ký (/register).",
            "Người dùng chọn tài khoản Google của mình trên cửa sổ xác nhận của Google.",
            "Hệ thống kiểm tra email Google: nếu đã có trên hệ thống thì liên kết vào tài khoản hiện tại, nếu chưa có thì tự động tạo tài khoản mới (BR-07).",
            "Hệ thống kiểm tra tài khoản không bị khóa (BR-05), tạo phiên làm việc và đưa người dùng vào trang chính."
        ],
        "abnormal": [
            "Nếu người dùng đóng cửa sổ Google giữa chừng hoặc hủy cấp quyền: Hệ thống quay lại trang đăng nhập và báo thao tác Google chưa hoàn tất (MSG13).",
            "Nếu tài khoản gắn với email đó đang bị khóa hoặc đã xóa: Hệ thống chặn đăng nhập và báo MSG12."
        ]
    },
    "3.2.4": {
        "summary": "Giúp người dùng lấy lại mật khẩu khi bị quên bằng cách nhận mã xác nhận OTP 6 số qua email và đặt lại mật khẩu mới.",
        "trigger": "Khi người dùng bấm vào đường dẫn Quên mật khẩu trên trang Đăng nhập (/forgot-password) và nhập địa chỉ email của mình.",
        "interface": "Màn hình Quên & Đặt lại mật khẩu (/forgot-password, /reset-password) gồm ô nhập Email nhận mã, ô nhập mã OTP 6 số, ô Mật khẩu mới, ô Nhập lại mật khẩu mới và nút Cập nhật mật khẩu.",
        "processing": "Hệ thống kiểm tra email và gửi mã OTP 6 số (hiệu lực 10 phút - BR-03) về hộp thư của người dùng. Khi người dùng nhập đúng mã OTP và mật khẩu mới đạt chuẩn (BR-02), hệ thống lưu mật khẩu mới và tự động đăng xuất toàn bộ các thiết bị cũ để đảm bảo an toàn (BR-08).",
        "in_req": "Địa chỉ Email đã đăng ký, Mã OTP 6 số nhận qua email, Mật khẩu mới và Nhập lại mật khẩu mới.",
        "in_opt": "Không bắt buộc.",
        "sys_data": "Mã OTP khôi phục (hiệu lực 10 phút, tối đa 5 lần thử - BR-03, BR-04), mật khẩu mới đã mã hóa và lệnh thu hồi các phiên đăng nhập cũ (BR-08).",
        "output": "Cập nhật mật khẩu mới thành công (hiển thị MSG17) và chuyển về trang Đăng nhập để đăng nhập lại.",
        "flow": [
            "Người dùng mở màn hình Quên mật khẩu (/forgot-password), nhập Email của mình và bấm Gửi mã xác nhận.",
            "Hệ thống tạo mã OTP 6 số có hiệu lực 10 phút (BR-03), gửi vào email và hiển thị thông báo MSG14.",
            "Người dùng nhập mã OTP 6 số kèm Mật khẩu mới và Nhập lại mật khẩu mới rồi bấm Xác nhận.",
            "Hệ thống kiểm tra mã OTP hợp lệ, lưu mật khẩu mới, đăng xuất mọi phiên đăng nhập cũ (BR-08), báo thành công (MSG17) và chuyển về trang Đăng nhập."
        ],
        "abnormal": [
            "Nếu mã OTP nhập sai hoặc đã quá 10 phút: Hệ thống báo mã không hợp lệ hoặc đã hết hạn (MSG15). Nếu nhập sai quá 5 lần thì khóa mã đó và yêu cầu gửi lại mã mới (BR-04).",
            "Nếu mật khẩu mới ngắn hơn 8 ký tự, thiếu chữ số hoặc nhập lại không khớp: Hệ thống báo lỗi dưới ô nhập (MSG05, MSG06)."
        ]
    },
    "3.2.5": {
        "summary": "Cho phép người dùng đang đăng nhập chủ động thay đổi mật khẩu của mình trong phần Cài đặt bảo mật bằng cách xác nhận mật khẩu hiện tại và nhập mật khẩu mới.",
        "trigger": "Khi người dùng mở trang Cài đặt bảo mật (/settings/security), điền mật khẩu cũ cùng mật khẩu mới và bấm Lưu thay đổi.",
        "interface": "Khu vực Đổi mật khẩu trên màn hình Cài đặt bảo mật (/settings/security) gồm 3 ô nhập: Mật khẩu hiện tại, Mật khẩu mới, Nhập lại mật khẩu mới và nút Cập nhật mật khẩu.",
        "processing": "Hệ thống kiểm tra Mật khẩu hiện tại người dùng nhập vào có đúng không, đồng thời kiểm tra Mật khẩu mới phải khác mật khẩu cũ (BR-08) và đủ độ mạnh (tối thiểu 8 ký tự, có số - BR-02). Sau khi cập nhật thành công, hệ thống giữ nguyên phiên làm việc hiện tại của người dùng.",
        "in_req": "Mật khẩu hiện tại, Mật khẩu mới (khác mật khẩu cũ, tối thiểu 8 ký tự và có số), Nhập lại mật khẩu mới.",
        "in_opt": "Không bắt buộc.",
        "sys_data": "Mật khẩu mới đã mã hóa và thời gian cập nhật mật khẩu.",
        "output": "Đổi mật khẩu thành công, hiển thị thông báo MSG17 và tiếp tục làm việc bình thường.",
        "flow": [
            "Người dùng mở phần Cài đặt bảo mật (/settings/security) và chọn mục Đổi mật khẩu.",
            "Người dùng nhập Mật khẩu hiện tại, Mật khẩu mới và Nhập lại mật khẩu mới rồi bấm Cập nhật.",
            "Hệ thống kiểm tra mật khẩu hiện tại chính xác, mật khẩu mới đạt chuẩn (BR-02) và không trùng mật khẩu cũ (BR-08).",
            "Hệ thống lưu mật khẩu mới và hiển thị thông báo đổi mật khẩu thành công (MSG17)."
        ],
        "abnormal": [
            "Nếu nhập sai mật khẩu hiện tại hoặc đặt mật khẩu mới giống hệt mật khẩu cũ: Hệ thống báo lỗi MSG18 để người dùng nhập lại.",
            "Nếu mật khẩu mới không đủ 8 ký tự/thiếu số hoặc 2 ô mật khẩu mới không khớp nhau: Hệ thống báo lỗi MSG05 hoặc MSG06."
        ]
    },
    "3.2.6": {
        "summary": "Xác nhận mã OTP 6 chữ số được gửi tới email của người dùng để hoàn tất kích hoạt tài khoản mới đăng ký (3.2.1) hoặc xác minh yêu cầu đặt lại mật khẩu (3.2.4).",
        "trigger": "Khi người dùng được chuyển tới màn hình Xác thực OTP (/verify-otp), nhập 6 chữ số nhận được trong email và bấm Xác nhận.",
        "interface": "Màn hình Xác thực OTP (/verify-otp) gồm 6 ô nhập số OTP, đồng hồ đếm ngược thời gian hiệu lực, nút Xác nhận và nút Gửi lại mã (Resend OTP - mở sau 60 giây).",
        "processing": "Hệ thống kiểm tra mã OTP 6 số có khớp với mã đã gửi không, còn trong thời hạn 10 phút không và chưa vượt quá 5 lần nhập sai (BR-03, BR-04). Nếu hợp lệ, hệ thống đánh dấu mã đã sử dụng và kích hoạt tài khoản sang trạng thái Đang hoạt động (ACTIVE - BR-05).",
        "in_req": "Mã xác nhận OTP gồm 6 chữ số gửi qua email.",
        "in_opt": "Bấm nút Gửi lại mã mới (sau khi hết 60 giây chờ).",
        "sys_data": "Trạng thái mã OTP, bộ đếm số lần nhập sai (tối đa 5 lần - BR-04), thời gian chờ gửi lại (60 giây) và trạng thái kích hoạt tài khoản.",
        "output": "Xác thực thành công, tài khoản được kích hoạt (ACTIVE) và chuyển người dùng sang bước tiếp theo.",
        "flow": [
            "Trên màn hình Xác thực OTP (/verify-otp), người dùng nhập mã 6 chữ số vừa nhận được trong hộp thư email.",
            "Người dùng bấm nút Xác nhận.",
            "Hệ thống kiểm tra mã OTP chính xác và còn trong thời hạn 10 phút (BR-03).",
            "Hệ thống chuyển trạng thái tài khoản sang Đang hoạt động (ACTIVE - BR-05) và đưa người dùng vào hệ thống (hoặc sang bước đặt mật khẩu mới nếu đang khôi phục mật khẩu)."
        ],
        "abnormal": [
            "Nếu nhập sai mã OTP hoặc mã đã quá hạn 10 phút: Hệ thống báo lỗi MSG15.",
            "Nếu nhập sai quá 5 lần liên tiếp hoặc bấm gửi lại khi chưa đủ 60 giây chờ: Hệ thống khóa mã cũ và báo người dùng đợi đủ 60 giây để lấy mã mới (BR-04, MSG16)."
        ]
    },
    "3.2.7": {
        "summary": "Bật bảo mật 2 lớp (2FA) bằng cách quét mã QR qua ứng dụng Authenticator (Google/Microsoft Authenticator) trên điện thoại, và kiểm tra mã 6 số này mỗi khi đăng nhập.",
        "trigger": "Khi người dùng bật/tắt 2FA trong trang Cài đặt bảo mật (/settings/security) hoặc khi đăng nhập vào tài khoản đã bật 2FA (/verify-2fa).",
        "interface": "Khung hiển thị ảnh mã QR (để quét bằng điện thoại), ô nhập mã xác thực 6 số từ ứng dụng Authenticator và nút Xác nhận. (Giao diện lược bỏ phần hiện chuỗi mã khóa văn bản và mã dự phòng để gọn gàng và an toàn hơn).",
        "processing": "Khi thiết lập, hệ thống tạo mã QR để người dùng quét vào ứng dụng Authenticator. Khi người dùng nhập mã 6 số hiển thị trên điện thoại (thay đổi mỗi 30 giây - BR-09), hệ thống kiểm tra tính hợp lệ để kích hoạt 2FA hoặc cho phép hoàn tất đăng nhập.",
        "in_req": "Mã xác thực 6 chữ số hiển thị trên ứng dụng Authenticator của điện thoại.",
        "in_opt": "Không bắt buộc.",
        "sys_data": "Trạng thái bật/tắt 2FA của tài khoản và khóa đồng bộ thời gian 30 giây với ứng dụng Authenticator (BR-09).",
        "output": "Cập nhật trạng thái bảo mật 2 lớp thành công (MSG19) hoặc hoàn tất đăng nhập vào hệ thống.",
        "flow": [
            "Người dùng mở mục Bảo mật 2 lớp trong Cài đặt (/settings/security) hoặc được chuyển tới màn hình nhập mã 2FA (/verify-2fa) lúc đăng nhập.",
            "Nếu là lần đầu bật 2FA, người dùng mở ứng dụng Authenticator trên điện thoại để quét mã QR trên màn hình.",
            "Người dùng nhập mã 6 chữ số đang hiển thị trên ứng dụng Authenticator vào ô xác nhận và bấm Xác nhận.",
            "Hệ thống kiểm tra mã 6 số hợp lệ (BR-09), lưu cài đặt (hiển thị MSG19) hoặc mở phiên đăng nhập cho người dùng."
        ],
        "abnormal": [
            "Nếu mã 6 số nhập sai hoặc đã qua chu kỳ 30 giây trên điện thoại: Hệ thống báo mã không hợp lệ (MSG15) để người dùng nhập mã mới đang hiển thị."
        ]
    },
    "3.2.8": {
        "summary": "Cho phép người dùng đăng xuất an toàn khỏi phiên làm việc hiện tại, đồng thời ghi nhớ phương thức đăng nhập gần nhất để lần sau đăng nhập lại nhanh hơn.",
        "trigger": "Khi người dùng bấm vào ảnh đại diện trên thanh menu và chọn nút Đăng xuất (Logout).",
        "interface": "Nút Đăng xuất trong menu tài khoản trên thanh điều hướng hoặc trong trang Cài đặt bảo mật.",
        "processing": "Hệ thống hủy ngay phiên đăng nhập hiện tại trên máy chủ để không ai có thể dùng lại phiên cũ, xóa thông tin phiên trên trình duyệt nhưng giữ lại gợi ý email/phương thức đăng nhập vừa dùng để tiện cho lần vào sau.",
        "in_req": "Người dùng đang đăng nhập bấm chọn Đăng xuất.",
        "in_opt": "Không bắt buộc.",
        "sys_data": "Thu hồi mã phiên làm việc hiện tại và cập nhật nhật ký đăng xuất.",
        "output": "Kết thúc phiên làm việc, hiển thị thông báo MSG20 và quay về màn hình Đăng nhập (/login).",
        "flow": [
            "Người dùng mở menu tài khoản ở góc trên màn hình và bấm chọn Đăng xuất.",
            "Hệ thống hủy hiệu lực phiên làm việc hiện tại trên máy chủ.",
            "Trình duyệt xóa dữ liệu phiên đăng nhập tạm thời và hiển thị thông báo đã đăng xuất (MSG20).",
            "Hệ thống chuyển người dùng về lại màn hình Đăng nhập (/login)."
        ],
        "abnormal": [
            "Nếu phiên đăng nhập đã hết hạn từ trước do để máy quá lâu: Hệ thống vẫn tự động dọn sạch dữ liệu trên trình duyệt và đưa người dùng về màn hình Đăng nhập."
        ]
    },
    "3.2.9": {
        "summary": "Cho phép người dùng tự xóa tài khoản cá nhân của mình. Tài khoản sẽ được tạm ẩn và giữ lại dữ liệu trong 30 ngày để có thể khôi phục nếu đổi ý trước khi xóa hẳn.",
        "trigger": "Khi người dùng mở phần Cài đặt bảo mật (/settings/security), bấm nút Xóa tài khoản, nhập mật khẩu xác nhận và đồng ý.",
        "interface": "Khu vực Xóa tài khoản trong trang Cài đặt bảo mật (/settings/security) kèm hộp thoại cảnh báo, ô nhập mật khẩu xác nhận và nút Xác nhận xóa tài khoản.",
        "processing": "Hệ thống kiểm tra mật khẩu xác nhận có đúng không, và kiểm tra người dùng có đang là Owner duy nhất của một Agency còn nhân sự hoặc chiến dịch đang chạy hay không (BR-10). Nếu đủ điều kiện, hệ thống chuyển tài khoản sang trạng thái Đã xóa mềm (lưu thời hạn 30 ngày chờ khôi phục - BR-16) và đăng xuất ngay lập tức.",
        "in_req": "Mật khẩu hiện tại để xác nhận và tích chọn đồng ý xóa tài khoản.",
        "in_opt": "Lý do xóa tài khoản (ghi chú tùy chọn).",
        "sys_data": "Trạng thái tài khoản chuyển sang Đã xóa mềm (DELETED), mốc thời gian 30 ngày khôi phục (BR-10, BR-16) và thu hồi toàn bộ phiên đăng nhập.",
        "output": "Tài khoản chuyển sang trạng thái chờ xóa 30 ngày, hiển thị thông báo MSG20 và chuyển về trang chủ.",
        "flow": [
            "Người dùng vào trang Cài đặt bảo mật (/settings/security) và bấm nút Xóa tài khoản.",
            "Trên hộp thoại xác nhận, người dùng nhập mật khẩu hiện tại và bấm Xác nhận xóa.",
            "Hệ thống kiểm tra mật khẩu đúng và đảm bảo người dùng không vướng quyền Owner duy nhất của một Agency đang hoạt động (BR-10).",
            "Hệ thống chuyển tài khoản sang trạng thái xóa mềm (có thể khôi phục trong 30 ngày), đăng xuất tài khoản và hiển thị thông báo MSG20."
        ],
        "abnormal": [
            "Nếu nhập sai mật khẩu xác nhận: Hệ thống báo mật khẩu không đúng (MSG18) và giữ nguyên tài khoản.",
            "Nếu người dùng đang là Owner duy nhất của một Agency vẫn còn thành viên hoặc chiến dịch đang chạy: Hệ thống chặn thao tác xóa và báo cần đóng hoặc bàn giao Agency trước (BR-10, MSG36)."
        ]
    },

    # ==================== 3.3 User & Client Profile ====================
    "3.3.1": {
        "summary": "Xem thông tin hồ sơ cá nhân của bản thân gồm ảnh đại diện, họ tên, email, số điện thoại, kỹ năng, ngôn ngữ và trạng thái bảo mật tài khoản.",
        "trigger": "Khi người dùng bấm vào mục Hồ sơ cá nhân (/profile) từ menu tài khoản.",
        "interface": "Màn hình Hồ sơ cá nhân (/profile) hiển thị ảnh đại diện, ảnh bìa, họ và tên, địa chỉ email (chỉ xem), số điện thoại, giới thiệu bản thân, kỹ năng, ngôn ngữ và nút Chỉnh sửa hồ sơ.",
        "processing": "Hệ thống kiểm tra phiên đăng nhập hợp lệ (BR-05) và lấy thông tin hồ sơ cá nhân của người dùng đang đăng nhập (BR-11) để hiển thị lên màn hình.",
        "in_req": "Người dùng đang đăng nhập mở trang Hồ sơ cá nhân.",
        "in_opt": "Không bắt buộc.",
        "sys_data": "Thông tin tài khoản, ảnh đại diện, số điện thoại, ngôn ngữ, múi giờ và trạng thái bảo mật 2FA.",
        "output": "Hiển thị đầy đủ thông tin hồ sơ cá nhân hiện tại của người dùng.",
        "flow": [
            "Người dùng bấm vào mục Hồ sơ cá nhân (/profile) trên thanh điều hướng.",
            "Hệ thống kiểm tra phiên đăng nhập hợp lệ của người dùng (BR-05).",
            "Hệ thống tải dữ liệu hồ sơ cá nhân từ cơ sở dữ liệu (BR-11).",
            "Màn hình hiển thị đầy đủ ảnh đại diện, thông tin liên hệ và các thiết lập cá nhân."
        ],
        "abnormal": [
            "Nếu phiên đăng nhập đã hết hạn: Hệ thống báo lỗi phân quyền (MSG07) và yêu cầu đăng nhập lại."
        ]
    },
    "3.3.2": {
        "summary": "Cập nhật thông tin hồ sơ cá nhân (họ tên, số điện thoại, giới thiệu, kỹ năng, ngôn ngữ) và tải lên ảnh đại diện mới. Địa chỉ email đăng nhập được giữ cố định để bảo vệ định danh tài khoản.",
        "trigger": "Khi người dùng chỉnh sửa thông tin hoặc chọn ảnh đại diện mới trên trang Hồ sơ cá nhân (/profile) rồi bấm Lưu thay đổi.",
        "interface": "Biểu mẫu chỉnh sửa trên màn hình Hồ sơ cá nhân (/profile) gồm nút tải ảnh đại diện/ảnh bìa, ô sửa Họ tên, Số điện thoại, Giới thiệu, Kỹ năng, Ngôn ngữ, ô Email (khóa cố định không cho sửa) và nút Lưu thay đổi.",
        "processing": "Hệ thống kiểm tra Họ tên không bị để trống, tệp ảnh tải lên đúng định dạng (PNG, JPG, WEBP) và không quá 5 MB (BR-12), đồng thời giữ nguyên địa chỉ email gốc (BR-11) trước khi lưu thông tin mới.",
        "in_req": "Họ và tên (không được để trống).",
        "in_opt": "Ảnh đại diện / ảnh bìa mới (PNG, JPG, WEBP tối đa 5 MB), Số điện thoại, Giới thiệu ngắn, Kỹ năng, Ngôn ngữ hiển thị.",
        "sys_data": "Đường dẫn lưu trữ ảnh mới và thời gian cập nhật hồ sơ.",
        "output": "Lưu thông tin hồ sơ cá nhân mới thành công và hiển thị thông báo MSG21.",
        "flow": [
            "Người dùng mở trang Hồ sơ cá nhân (/profile) và thay đổi Họ tên, Số điện thoại, Giới thiệu hoặc chọn tải ảnh đại diện mới.",
            "Người dùng bấm nút Lưu thay đổi.",
            "Hệ thống kiểm tra thông tin hợp lệ và kiểm tra ảnh tải lên có dung lượng dưới 5 MB, đúng định dạng ảnh (BR-12).",
            "Hệ thống lưu cập nhật hồ sơ (giữ cố định email gốc theo BR-11) và hiển thị thông báo thành công (MSG21)."
        ],
        "abnormal": [
            "Nếu để trống ô Họ tên hoặc nhập quá độ dài quy định: Hệ thống báo lỗi dưới ô nhập (MSG02, MSG03).",
            "Nếu chọn tệp ảnh sai định dạng hoặc nặng quá 5 MB: Hệ thống từ chối tải ảnh và báo lỗi MSG22."
        ]
    },
    "3.3.3": {
        "summary": "Xem hồ sơ thương hiệu của Khách hàng (Client Profile) gồm tên nhãn hàng, logo, ngành nghề, website và thông tin liên hệ. Hồ sơ này có thể dùng chung cho nhiều dự án (Workspace) khác nhau mà không cần nhập lại.",
        "trigger": "Khi Client hoặc Manager phụ trách mở màn hình Hồ sơ thương hiệu Client (/client-profiles hoặc trong Workspace).",
        "interface": "Màn hình Hồ sơ thương hiệu Client hiển thị Tên nhãn hàng, Logo thương hiệu, Lĩnh vực ngành nghề, Website, Mã số thuế, Địa chỉ, Thông tin liên hệ và danh sách các Workspace đang liên kết.",
        "processing": "Hệ thống kiểm tra người xem có phải là chính chủ tài khoản Client đó hoặc là Manager/Owner trong Workspace liên kết hay không (BR-14), sau đó tải thông tin hồ sơ thương hiệu lên màn hình (BR-13).",
        "in_req": "Tài khoản Client hoặc Manager có quyền truy cập mở trang Hồ sơ thương hiệu.",
        "in_opt": "Không bắt buộc.",
        "sys_data": "Mã hồ sơ Client, tên thương hiệu, logo, ngành hàng, thông tin liên hệ và các Workspace đang gắn kết.",
        "output": "Hiển thị chi tiết Hồ sơ thương hiệu của Client.",
        "flow": [
            "Client hoặc Manager mở màn hình Hồ sơ thương hiệu Client (/client-profiles).",
            "Hệ thống kiểm tra quyền xem hồ sơ của người dùng (BR-14).",
            "Hệ thống truy xuất dữ liệu thương hiệu dùng chung của Client (BR-13).",
            "Màn hình hiển thị đầy đủ thông tin nhận diện thương hiệu và thông tin liên hệ của nhãn hàng."
        ],
        "abnormal": [
            "Nếu người dùng không phải chủ hồ sơ Client và không phải Manager của dự án liên kết: Hệ thống chặn truy cập và báo MSG07."
        ]
    },
    "3.3.4": {
        "summary": "Cập nhật thông tin Hồ sơ thương hiệu của Client (tên thương hiệu, logo, ngành hàng, website, địa chỉ, số điện thoại). Khi cập nhật, thông tin mới sẽ tự động đồng bộ sang tất cả các Workspace mà Client đang tham gia.",
        "trigger": "Khi Client hoặc Manager chỉnh sửa thông tin trên màn hình Hồ sơ thương hiệu Client và bấm Lưu cập nhật.",
        "interface": "Biểu mẫu chỉnh sửa Hồ sơ thương hiệu Client gồm ô nhập Tên thương hiệu, chọn Ngành nghề, tải Logo mới, nhập Website, Mã số thuế, Địa chỉ, Số điện thoại liên hệ và nút Lưu.",
        "processing": "Hệ thống kiểm tra quyền chỉnh sửa (BR-14), kiểm tra Tên thương hiệu và Ngành nghề không bị trống, kiểm tra tệp Logo tải lên dưới 5 MB (BR-12), sau đó lưu và đồng bộ thông tin thương hiệu mới tới các Workspace liên quan (BR-13).",
        "in_req": "Tên thương hiệu và Lĩnh vực ngành nghề.",
        "in_opt": "Tệp ảnh Logo thương hiệu (PNG, JPG, WEBP tối đa 5 MB), Website, Mã số thuế, Địa chỉ, Số điện thoại liên hệ.",
        "sys_data": "Giữ cố định email gốc của tài khoản Client (BR-14) và tự động đồng bộ hồ sơ tới các Workspace liên kết (BR-13).",
        "output": "Cập nhật hồ sơ thương hiệu thành công và hiển thị thông báo MSG21.",
        "flow": [
            "Client hoặc Manager mở biểu mẫu chỉnh sửa trên màn hình Hồ sơ thương hiệu Client.",
            "Người dùng sửa Tên thương hiệu, Ngành nghề, Thông tin liên hệ hoặc tải lên Logo mới rồi bấm Lưu.",
            "Hệ thống kiểm tra quyền hạn (BR-14), dữ liệu bắt buộc và định dạng ảnh Logo (BR-12).",
            "Hệ thống lưu cập nhật, tự động đồng bộ sang các Workspace mà Client tham gia (BR-13) và báo thành công (MSG21)."
        ],
        "abnormal": [
            "Nếu bỏ trống Tên thương hiệu hoặc Ngành nghề: Hệ thống báo lỗi MSG02 dưới ô nhập.",
            "Nếu tệp Logo tải lên sai định dạng hoặc vượt quá 5 MB: Hệ thống báo lỗi MSG22."
        ]
    },

    # ==================== 3.4 Agency & Workspace ====================
    "3.4.1": {
        "summary": "Hiển thị danh sách tất cả các công ty (Agency) mà người dùng đang làm chủ sở hữu (Owner) hoặc đang tham gia làm thành viên, giúp chuyển đổi nhanh giữa các công ty hoặc tạo Agency mới.",
        "trigger": "Khi người dùng mở màn hình Danh sách Agency (/agency).",
        "interface": "Màn hình Danh sách Agency (/agency) gồm ô tìm kiếm theo tên, bộ lọc (Tất cả / Đang sở hữu / Đang tham gia), danh sách thẻ Agency (hiển thị Logo, Tên công ty, Vai trò, Số thành viên, Số Workspace, Gói dịch vụ) và nút Tạo Agency mới.",
        "processing": "Hệ thống tìm tất cả các Agency mà người dùng đang là Owner (BR-15) hoặc là thành viên chính thức, ẩn các Agency đã xóa mềm (trừ khi Owner mở xem để khôi phục trong 30 ngày - BR-16) và hiển thị ra danh sách.",
        "in_req": "Người dùng đã đăng nhập mở trang Danh sách Agency.",
        "in_opt": "Từ khóa tìm kiếm tên Agency và bộ lọc theo vai trò (Sở hữu / Tham gia).",
        "sys_data": "Danh sách Agency, vai trò của người dùng, tổng số thành viên, số Workspace và gói cước của từng Agency.",
        "output": "Hiển thị danh sách các thẻ Agency mà người dùng có quyền truy cập.",
        "flow": [
            "Người dùng mở màn hình Danh sách Agency (/agency).",
            "Hệ thống kiểm tra phiên đăng nhập và truy xuất các Agency mà người dùng sở hữu hoặc tham gia (BR-15).",
            "Người dùng có thể nhập từ khóa tìm kiếm hoặc lọc theo nhóm Agency.",
            "Màn hình hiển thị các thẻ Agency kèm nút bấm vào xem Tổng quan (3.4.2) hoặc Hồ sơ công ty (3.4.4)."
        ],
        "abnormal": [
            "Nếu không có Agency nào khớp với từ khóa tìm kiếm: Hệ thống hiển thị thông báo không tìm thấy kết quả (MSG01) kèm nút Tạo Agency mới (3.4.3)."
        ]
    },
    "3.4.2": {
        "summary": "Cung cấp cho chủ sở hữu (Owner) bảng điều khiển tổng quan của toàn công ty (Agency Dashboard), thống kê số lượng Workspace, nhân sự, tiến độ các chiến dịch và mức sử dụng điểm AI Credit.",
        "trigger": "Khi Owner chọn một Agency và mở màn hình Tổng quan Agency (/agency/:id/stats).",
        "interface": "Màn hình Tổng quan Agency hiển thị các thẻ số liệu chính (Tổng số Workspace, Tổng nhân sự, Chiến dịch đang chạy, Số dư AI Credit), biểu đồ hiệu suất công việc theo tuần/tháng và đường dẫn nhanh tới các dự án.",
        "processing": "Hệ thống kiểm tra người xem có đúng là Owner của Agency đó không (BR-15), sau đó tổng hợp số liệu thống kê từ tất cả các Workspace và nhân sự trực thuộc công ty để vẽ biểu đồ.",
        "in_req": "Owner chọn Agency cần xem bảng điều khiển tổng quan.",
        "in_opt": "Bộ lọc khoảng thời gian thống kê (7 ngày, 30 ngày, theo quý).",
        "sys_data": "Tổng số Workspace, số thành viên đang hoạt động, số lượng chiến dịch, tiến độ Task và số dư điểm AI Credit của Agency.",
        "output": "Hiển thị bảng thống kê KPI và biểu đồ hoạt động của toàn Agency.",
        "flow": [
            "Owner truy cập vào màn hình Tổng quan của Agency (/agency/:id/stats).",
            "Hệ thống xác nhận quyền Owner đối với Agency đó (BR-15).",
            "Hệ thống tổng hợp số liệu thành viên, các Workspace đang hoạt động, tiến độ chiến dịch và quỹ điểm AI Credit.",
            "Màn hình hiển thị trực quan các thẻ chỉ số và biểu đồ theo dõi."
        ],
        "abnormal": [
            "Nếu người truy cập không phải là Owner của Agency hoặc Agency đang bị tạm khóa: Hệ thống từ chối truy cập và hiển thị MSG07 hoặc MSG36."
        ]
    },
    "3.4.3": {
        "summary": "Cho phép người dùng khởi tạo một công ty truyền thông (Agency) mới. Người tạo sẽ tự động trở thành chủ sở hữu (Owner) duy nhất của Agency đó và bắt đầu với gói dịch vụ Cơ bản (Basic).",
        "trigger": "Khi người dùng bấm nút Tạo Agency mới (/agency/create), điền thông tin công ty và bấm Hoàn tất.",
        "interface": "Màn hình Tạo Agency (/agency/create) gồm ô nhập Tên công ty/Agency, chọn Lĩnh vực hoạt động, Mô tả giới thiệu, Website/Liên hệ, nút tải lên Logo/Ảnh bìa (kèm khung xem trước trực tiếp) và nút Tạo Agency.",
        "processing": "Hệ thống kiểm tra Tên công ty không bị để trống, tệp Logo tải lên hợp lệ (dưới 5 MB - BR-12), kiểm tra giới hạn tạo Agency theo gói tài khoản (BR-58), sau đó tạo bản ghi Agency mới và gán người tạo làm Owner duy nhất (BR-15).",
        "in_req": "Tên công ty (Agency Name) và Lĩnh vực hoạt động.",
        "in_opt": "Logo công ty, Ảnh bìa (PNG, JPG, WEBP tối đa 5 MB), Mô tả giới thiệu, Website, Số điện thoại và Địa chỉ liên hệ.",
        "sys_data": "Mã Agency mới, gán cố định vai trò OWNER cho người tạo (BR-15) và kích hoạt gói dịch vụ Basic mặc định (BR-58).",
        "output": "Tạo Agency mới thành công (hiển thị MSG23) và chuyển vào trang quản lý của Agency vừa tạo.",
        "flow": [
            "Người dùng mở màn hình Tạo Agency (/agency/create) và nhập Tên công ty, Lĩnh vực hoạt động, Mô tả cùng Logo.",
            "Người dùng bấm nút Tạo Agency.",
            "Hệ thống kiểm tra dữ liệu bắt buộc, định dạng ảnh Logo (BR-12) và điều kiện khởi tạo (BR-58).",
            "Hệ thống lưu Agency mới, gán người tạo làm Owner duy nhất (BR-15), hiển thị thông báo MSG23 và mở trang quản lý Agency."
        ],
        "abnormal": [
            "Nếu bỏ trống Tên công ty: Hệ thống báo lỗi MSG02 dưới ô nhập.",
            "Nếu ảnh Logo/Banner tải lên sai định dạng hoặc vượt quá 5 MB: Hệ thống báo lỗi MSG22."
        ]
    },
    "3.4.4": {
        "summary": "Xem trang hồ sơ giới thiệu chính thức của công ty (Agency Profile) gồm tên công ty, logo, năng lực chuyên môn, thông tin liên hệ và các gói dịch vụ mẫu để Client và thành viên nắm rõ thông tin.",
        "trigger": "Khi Owner, Manager, Creator hoặc Client mở trang Hồ sơ công ty (/agency/:id).",
        "interface": "Màn hình Hồ sơ Agency (/agency/:id) hiển thị Ảnh bìa, Logo, Tên công ty, Giới thiệu năng lực, Lĩnh vực hoạt động, Website, Email/Số điện thoại liên hệ và nút Chỉnh sửa (chỉ hiện với Owner).",
        "processing": "Hệ thống kiểm tra người dùng có quyền xem thông tin Agency không, sau đó tải và hiển thị toàn bộ thông tin giới thiệu của công ty.",
        "in_req": "Chọn Agency cần xem hồ sơ giới thiệu.",
        "in_opt": "Không bắt buộc.",
        "sys_data": "Thông tin giới thiệu, bộ nhận diện thương hiệu và thông tin liên hệ của Agency.",
        "output": "Hiển thị trang Hồ sơ giới thiệu của Agency.",
        "flow": [
            "Người dùng (Owner, Manager, Creator hoặc Client) mở trang Hồ sơ Agency (/agency/:id).",
            "Hệ thống kiểm tra quyền truy cập và trạng thái hoạt động của Agency (BR-15).",
            "Hệ thống tải thông tin hồ sơ công ty từ cơ sở dữ liệu.",
            "Màn hình hiển thị đầy đủ thông tin giới thiệu, logo và liên hệ của Agency."
        ],
        "abnormal": [
            "Nếu người dùng không thuộc Agency hoặc không có quyền xem: Hệ thống chặn truy cập và báo MSG07."
        ]
    },
    "3.4.5": {
        "summary": "Cho phép chủ sở hữu (Owner) chỉnh sửa thông tin giới thiệu, thông tin liên hệ và thay đổi Logo/Ảnh bìa của công ty (Agency).",
        "trigger": "Khi Owner mở phần cài đặt Hồ sơ Agency (/agency/:id), sửa thông tin và bấm Lưu thay đổi.",
        "interface": "Biểu mẫu cập nhật Hồ sơ Agency gồm ô sửa Tên công ty, Lĩnh vực, Mô tả giới thiệu, Website, Email/Số điện thoại liên hệ, nút đổi Logo/Ảnh bìa và nút Lưu.",
        "processing": "Hệ thống kiểm tra người thực hiện đúng là Owner của Agency (BR-15), kiểm tra Tên công ty không bị để trống và ảnh tải lên không quá 5 MB (BR-12), sau đó lưu thông tin mới.",
        "in_req": "Tên công ty (Agency Name).",
        "in_opt": "Logo mới, Ảnh bìa mới (PNG, JPG, WEBP tối đa 5 MB), Lĩnh vực hoạt động, Mô tả, Website, Địa chỉ và Số điện thoại.",
        "sys_data": "Thời gian cập nhật và đường dẫn ảnh mới của Agency.",
        "output": "Cập nhật thông tin công ty thành công và hiển thị thông báo MSG21.",
        "flow": [
            "Owner mở phần chỉnh sửa Hồ sơ công ty trên trang quản lý Agency (/agency/:id).",
            "Owner thay đổi Tên công ty, Mô tả, Liên hệ hoặc tải lên Logo mới rồi bấm Lưu thay đổi.",
            "Hệ thống xác nhận quyền Owner (BR-15) và kiểm tra tính hợp lệ của thông tin/hình ảnh (BR-12).",
            "Hệ thống lưu hồ sơ công ty mới và hiển thị thông báo cập nhật thành công (MSG21)."
        ],
        "abnormal": [
            "Nếu người thao tác không phải là Owner của Agency: Hệ thống từ chối và báo MSG07.",
            "Nếu để trống Tên công ty hoặc tải ảnh nặng quá 5 MB: Hệ thống báo lỗi MSG02 hoặc MSG22."
        ]
    },
    "3.4.6": {
        "summary": "Cho phép Owner xóa mềm công ty (Remove Agency). Khi xóa, Agency và các dự án bên trong sẽ tạm ngưng hoạt động nhưng toàn bộ dữ liệu vẫn được giữ lại trong 30 ngày để Owner khôi phục nếu cần.",
        "trigger": "Khi Owner bấm nút Xóa Agency trong phần Cài đặt công ty, nhập lại tên Agency để xác nhận và đồng ý.",
        "interface": "Khu vực Xóa công ty trên màn hình Cài đặt Agency (/agency/:id) kèm hộp thoại xác nhận yêu cầu nhập đúng tên Agency và nút Xác nhận xóa.",
        "processing": "Hệ thống kiểm tra quyền Owner duy nhất (BR-15) và kiểm tra chuỗi tên xác nhận. Sau đó, hệ thống chuyển trạng thái Agency sang Tạm ẩn chờ xóa (lưu giữ 30 ngày - BR-16) và tạm dừng quyền truy cập của các thành viên vào các Workspace trực thuộc.",
        "in_req": "Nhập đúng tên Agency vào ô xác nhận xóa.",
        "in_opt": "Lý do xóa (tùy chọn).",
        "sys_data": "Trạng thái Agency chuyển sang Đã xóa mềm (DELETED_PENDING), mốc hạn 30 ngày khôi phục (BR-16).",
        "output": "Xóa mềm Agency thành công, hiển thị thông báo MSG24 (nhắc có thể khôi phục trong 30 ngày) và quay về danh sách Agency.",
        "flow": [
            "Owner mở phần Cài đặt của Agency (/agency/:id) và bấm chọn Xóa Agency.",
            "Trên hộp thoại cảnh báo, Owner nhập lại chính xác tên Agency để xác nhận và bấm Đồng ý.",
            "Hệ thống kiểm tra quyền Owner (BR-15) và chuyển trạng thái Agency cùng các Workspace bên trong sang chế độ tạm khóa chờ xóa 30 ngày (BR-16).",
            "Hệ thống hiển thị thông báo MSG24 và điều hướng về màn hình Danh sách Agency."
        ],
        "abnormal": [
            "Nếu nhập tên xác nhận không khớp với tên Agency: Hệ thống báo lỗi MSG02/MSG03 và không thực hiện xóa.",
            "Nếu người thao tác không phải là Owner: Hệ thống chặn thao tác và báo MSG07."
        ]
    },
    "3.4.7": {
        "summary": "Cho phép Owner gửi lời mời nhân sự mới tham gia vào công ty (Agency) thông qua địa chỉ Email. Lời mời có hiệu lực trong vòng 3 ngày (72 giờ).",
        "trigger": "Khi Owner mở trang Thành viên Agency (/agency/:id/members), nhập địa chỉ email của người cần mời và bấm Gửi lời mời.",
        "interface": "Hộp thoại Mời thành viên trên màn hình Thành viên Agency (/agency/:id/members) gồm ô nhập Địa chỉ Email, ô lời nhắn (tùy chọn) và nút Gửi lời mời.",
        "processing": "Hệ thống kiểm tra quyền Owner (BR-15), kiểm tra định dạng email hợp lệ (BR-01) và kiểm tra người đó chưa phải là thành viên hoặc chưa có lời mời nào đang chờ. Tiếp theo, hệ thống tạo lời mời ở trạng thái Chờ phản hồi (PENDING) có hạn 3 ngày (BR-17) và gửi thông báo kèm email cho người nhận.",
        "in_req": "Địa chỉ Email của người muốn mời vào Agency.",
        "in_opt": "Lời nhắn giới thiệu kèm theo lời mời.",
        "sys_data": "Mã lời mời, trạng thái Chờ phản hồi (PENDING) và thời gian hết hạn sau 3 ngày (72 giờ - BR-17).",
        "output": "Gửi lời mời thành công, hiển thị thông báo MSG25 và thêm vào danh sách lời mời đang chờ.",
        "flow": [
            "Owner mở màn hình Thành viên Agency (/agency/:id/members) và bấm nút Mời thành viên.",
            "Owner nhập địa chỉ Email của nhân sự cần mời và bấm Gửi lời mời.",
            "Hệ thống kiểm tra email hợp lệ và chưa tồn tại trong danh sách thành viên hoặc danh sách đang chờ của Agency.",
            "Hệ thống lưu lời mời (hiệu lực 3 ngày - BR-17), gửi email/thông báo cho người nhận và hiển thị thông báo MSG25."
        ],
        "abnormal": [
            "Nếu nhập trống hoặc sai định dạng email: Hệ thống báo lỗi MSG02 hoặc MSG04.",
            "Nếu email đó đã là thành viên của Agency hoặc đang có lời mời chờ phản hồi: Hệ thống báo thông báo MSG26."
        ]
    },
    "3.4.8": {
        "summary": "Theo dõi danh sách và trạng thái của các lời mời tham gia Agency (Đang chờ, Đã chấp nhận, Đã từ chối, Đã hết hạn sau 3 ngày).",
        "trigger": "Khi Owner mở tab Lời mời trên trang Thành viên Agency (/agency/:id/members) hoặc khi người dùng mở trang Lời mời nhận được (/agency/invitations).",
        "interface": "Bảng danh sách lời mời hiển thị Email người nhận, Tên Agency mời, Ngày gửi, Thời gian còn lại (đếm ngược 3 ngày), nhãn Trạng thái (PENDING, ACCEPTED, DECLINED, EXPIRED) và các nút thao tác.",
        "processing": "Hệ thống tự động kiểm tra các lời mời đã quá 3 ngày để chuyển sang trạng thái Hết hạn (EXPIRED - BR-17), sau đó hiển thị danh sách lời mời theo quyền của người xem (BR-18).",
        "in_req": "Người dùng mở trang danh sách lời mời.",
        "in_opt": "Lọc theo trạng thái lời mời (Đang chờ / Đã chấp nhận / Đã từ chối / Hết hạn) hoặc tìm theo email.",
        "sys_data": "Trạng thái hiện tại của lời mời và thời gian hết hạn 3 ngày (BR-17).",
        "output": "Hiển thị danh sách lời mời kèm trạng thái cập nhật mới nhất.",
        "flow": [
            "Owner hoặc người dùng được mời mở màn hình Quản lý lời mời (/agency/invitations).",
            "Hệ thống kiểm tra quyền truy cập và cập nhật trạng thái các lời mời đã quá hạn 3 ngày (BR-17).",
            "Hệ thống truy xuất danh sách các lời mời liên quan đến tài khoản.",
            "Màn hình hiển thị bảng lời mời kèm trạng thái và thời hạn còn lại."
        ],
        "abnormal": [
            "Nếu không có lời mời nào khớp với bộ lọc: Hệ thống hiển thị thông báo trống MSG01."
        ]
    },
    "3.4.9": {
        "summary": "Cho phép người dùng được mời bấm Chấp nhận lời mời để chính thức trở thành thành viên của công ty (Agency).",
        "trigger": "Khi người dùng nhận được lời mời (còn trong thời hạn 3 ngày) và bấm nút Chấp nhận (Accept) trên trang Lời mời (/agency/invitations).",
        "interface": "Thẻ lời mời tham gia Agency hiển thị Tên công ty, Người mời, Thời hạn còn lại cùng 2 nút: Chấp nhận (Accept) và Từ chối (Decline).",
        "processing": "Hệ thống kiểm tra tài khoản đang đăng nhập có đúng email được mời không (BR-18) và lời mời vẫn đang ở trạng thái Chờ phản hồi, chưa quá hạn 3 ngày (BR-17). Nếu hợp lệ, hệ thống chuyển lời mời sang Đã chấp nhận (ACCEPTED) và thêm người dùng vào danh sách thành viên chính thức của Agency.",
        "in_req": "Chọn lời mời đang chờ và bấm nút Chấp nhận.",
        "in_opt": "Không bắt buộc.",
        "sys_data": "Cập nhật trạng thái lời mời sang ACCEPTED, tạo bản ghi thành viên mới trong Agency và gửi thông báo cho Owner.",
        "output": "Gia nhập Agency thành công, hiển thị thông báo MSG27 và Agency mới xuất hiện trong danh sách của người dùng.",
        "flow": [
            "Người dùng mở danh sách Lời mời nhận được (/agency/invitations) hoặc nhấp vào link mời trong email.",
            "Người dùng bấm nút Chấp nhận trên lời mời của Agency.",
            "Hệ thống kiểm tra đúng tài khoản được mời (BR-18) và lời mời chưa quá hạn 3 ngày (BR-17).",
            "Hệ thống thêm người dùng làm thành viên chính thức của Agency, cập nhật trạng thái lời mời sang Đã chấp nhận và hiển thị thông báo MSG27."
        ],
        "abnormal": [
            "Nếu lời mời đã quá hạn 3 ngày hoặc đã bị thu hồi trước đó: Hệ thống từ chối và hiển thị thông báo lời mời đã hết hạn (MSG28)."
        ]
    },
    "3.4.10": {
        "summary": "Cho phép người dùng được mời bấm Từ chối lời mời tham gia Agency nếu không có nhu cầu gia nhập công ty đó.",
        "trigger": "Khi người dùng bấm nút Từ chối (Decline) trên lời mời tham gia Agency đang chờ phản hồi.",
        "interface": "Nút Từ chối (Decline) trên thẻ lời mời tại màn hình Lời mời (/agency/invitations).",
        "processing": "Hệ thống kiểm tra đúng người nhận lời mời (BR-18) và lời mời vẫn đang ở trạng thái Chờ phản hồi (BR-17), sau đó chuyển trạng thái lời mời sang Đã từ chối (DECLINED) và báo lại cho Owner.",
        "in_req": "Chọn lời mời đang chờ và bấm nút Từ chối.",
        "in_opt": "Không bắt buộc.",
        "sys_data": "Cập nhật trạng thái lời mời sang DECLINED và lưu thời gian phản hồi.",
        "output": "Ghi nhận từ chối lời mời thành công và hiển thị thông báo MSG27.",
        "flow": [
            "Người dùng mở trang Lời mời (/agency/invitations) và xem lời mời đang chờ.",
            "Người dùng bấm nút Từ chối.",
            "Hệ thống kiểm tra tính hợp lệ của lời mời (BR-17, BR-18) và cập nhật trạng thái sang Đã từ chối (DECLINED).",
            "Hệ thống gửi thông báo phản hồi cho Owner của Agency và hiển thị thông báo MSG27."
        ],
        "abnormal": [
            "Nếu lời mời đã hết hạn 3 ngày hoặc đã được xử lý trước đó: Hệ thống hiển thị thông báo MSG28."
        ]
    },
    "3.4.11": {
        "summary": "Cho phép Owner xóa một thành viên ra khỏi công ty (Agency). Người bị xóa sẽ mất quyền truy cập ngay lập tức, nhưng toàn bộ bài viết, công việc và tư liệu họ đã làm trước đó vẫn được giữ nguyên cho công ty.",
        "trigger": "Khi Owner chọn một thành viên trong danh sách Thành viên Agency (/agency/:id/members), bấm Xóa khỏi Agency và xác nhận.",
        "interface": "Bảng danh sách thành viên Agency (/agency/:id/members) kèm nút Xóa thành viên và hộp thoại xác nhận trước khi xóa.",
        "processing": "Hệ thống kiểm tra quyền Owner (BR-15), kiểm tra thành viên đó không phải là Manager duy nhất đang phụ trách một Workspace nào đó (BR-21). Nếu hợp lệ, hệ thống thu hồi quyền truy cập của người đó khỏi Agency và các Workspace trực thuộc, đồng thời giữ nguyên toàn bộ tài liệu/bài viết họ từng tạo (BR-19).",
        "in_req": "Chọn thành viên cần xóa khỏi Agency và xác nhận.",
        "in_opt": "Lý do xóa thành viên (ghi chú nội bộ).",
        "sys_data": "Thu hồi quyền thành viên trong Agency và các Workspace, bảo toàn lịch sử bài viết/tư liệu (BR-19).",
        "output": "Xóa thành viên khỏi Agency thành công và hiển thị thông báo MSG29.",
        "flow": [
            "Owner mở danh sách Thành viên của Agency (/agency/:id/members) và bấm nút Xóa bên cạnh thành viên cần gỡ.",
            "Owner bấm Đồng ý trên hộp thoại xác nhận.",
            "Hệ thống kiểm tra thành viên đó không phải là Manager duy nhất của bất kỳ Workspace nào đang chạy (BR-21).",
            "Hệ thống gỡ quyền truy cập của thành viên khỏi Agency và các Workspace, giữ nguyên toàn bộ sản phẩm công việc cũ (BR-19) và báo thành công (MSG29)."
        ],
        "abnormal": [
            "Nếu thành viên đó đang là Manager duy nhất của một Workspace: Hệ thống chặn thao tác xóa và nhắc Owner cần gán một Manager khác thay thế cho Workspace đó trước (BR-21, MSG36).",
            "Nếu Owner cố tình tự xóa chính tài khoản Owner của mình: Hệ thống chặn và báo lỗi MSG36."
        ]
    },
    "3.4.12": {
        "summary": "Xem danh sách các không gian làm việc (Workspace) trong công ty. Owner nhìn thấy toàn bộ tất cả các Workspace của Agency, còn Manager, Creator và Client chỉ nhìn thấy những Workspace mà mình tham gia.",
        "trigger": "Khi người dùng mở màn hình Danh sách Workspace (/workspace).",
        "interface": "Màn hình Danh sách Workspace (/workspace) gồm ô tìm kiếm tên dự án, danh sách thẻ Workspace (hiển thị Tên dự án/nhãn hàng, Tên Manager phụ trách, Múi giờ, Số lượng thành viên, Tiến độ công việc) và nút Tạo Workspace mới (dành cho Owner).",
        "processing": "Hệ thống kiểm tra vai trò của người dùng: nếu là Owner thì lấy toàn bộ các Workspace của Agency (BR-15); nếu là Manager, Creator hoặc Client thì chỉ lấy những Workspace mà người đó đang là thành viên (BR-20).",
        "in_req": "Người dùng đã đăng nhập mở màn hình Danh sách Workspace.",
        "in_opt": "Từ khóa tìm kiếm theo tên Workspace hoặc lọc theo trạng thái hoạt động.",
        "sys_data": "Danh sách Workspace theo đúng phân quyền (BR-20), thông tin Manager phụ trách và múi giờ của từng Workspace.",
        "output": "Hiển thị danh sách các Workspace mà người dùng được phép truy cập.",
        "flow": [
            "Người dùng mở màn hình Danh sách Workspace (/workspace).",
            "Hệ thống kiểm tra vai trò của người dùng trong Agency (BR-15, BR-20).",
            "Hệ thống lấy danh sách toàn bộ Workspace (nếu là Owner) hoặc các Workspace được phân công (nếu là Manager, Creator, Client).",
            "Màn hình hiển thị các thẻ Workspace để người dùng bấm vào làm việc."
        ],
        "abnormal": [
            "Nếu không tìm thấy Workspace nào khớp với từ khóa: Hệ thống hiển thị thông báo trống MSG01."
        ]
    },
    "3.4.13": {
        "summary": "Hiển thị bảng điều khiển tổng quan của một dự án (Workspace Dashboard), giúp các thành viên nắm nhanh số lượng công việc theo từng trạng thái, lịch đăng bài sắp tới và lượng điểm AI Credit đã dùng.",
        "trigger": "Khi Owner, Manager, Creator hoặc Client bấm vào một Workspace để mở màn hình Tổng quan dự án (/workspace/:id/dashboard).",
        "interface": "Màn hình Tổng quan Workspace hiển thị thống kê số lượng Task (Đang chờ, Đang làm, Chờ duyệt, Đã duyệt, Đã đăng), lịch bài đăng sắp tới (theo múi giờ của Workspace), tiến độ chiến dịch và mức tiêu thụ AI Credit của dự án.",
        "processing": "Hệ thống kiểm tra người dùng có quyền truy cập vào Workspace này không (BR-20), sau đó tổng hợp số liệu công việc, lịch xuất bản (quy đổi theo múi giờ chuẩn của Workspace - BR-22) và hạn mức điểm AI Credit để hiển thị.",
        "in_req": "Chọn một Workspace mà người dùng có quyền truy cập.",
        "in_opt": "Bộ lọc khoảng thời gian xem thống kê.",
        "sys_data": "Số liệu thống kê Task theo trạng thái, lịch bài đăng sắp tới và số điểm AI Credit đã sử dụng trong Workspace.",
        "output": "Hiển thị màn hình tổng quan tiến độ và hoạt động của Workspace.",
        "flow": [
            "Người dùng chọn một Workspace từ danh sách để mở trang Tổng quan (/workspace/:id/dashboard).",
            "Hệ thống kiểm tra quyền truy cập của người dùng đối với Workspace đó (BR-20).",
            "Hệ thống tổng hợp số liệu Task, tiến độ chiến dịch, lịch đăng bài (theo múi giờ BR-22) và điểm AI Credit.",
            "Màn hình hiển thị các biểu đồ và bảng tóm tắt trực quan của dự án."
        ],
        "abnormal": [
            "Nếu người dùng không phải là thành viên của Workspace này (và không phải Owner): Hệ thống chặn truy cập và báo MSG07."
        ]
    },
    "3.4.14": {
        "summary": "Cho phép Owner tạo mới một không gian làm việc (Workspace) cho dự án hoặc nhãn hàng mới. Khi tạo, Owner bắt buộc phải chọn ít nhất 1 thành viên làm Manager phụ trách và thiết lập múi giờ chuẩn cho dự án.",
        "trigger": "Khi Owner mở màn hình Tạo Workspace (/workspace/create), điền thông tin dự án, chọn Manager phụ trách và bấm Tạo mới.",
        "interface": "Màn hình Tạo Workspace (/workspace/create) gồm ô nhập Tên Workspace, Mô tả dự án, ô chọn Thành viên làm Manager (bắt buộc), ô chọn Múi giờ chuẩn (UTC Timezone), tùy chọn Gói dịch vụ / Mẫu cấu hình có sẵn và nút Tạo Workspace.",
        "processing": "Hệ thống kiểm tra quyền Owner (BR-15), kiểm tra giới hạn số lượng Workspace theo gói đăng ký hiện tại của Agency (BR-58), đảm bảo đã chọn ít nhất 1 thành viên của Agency làm Manager (BR-21) và có chọn Múi giờ hợp lệ (BR-22), sau đó khởi tạo Workspace mới.",
        "in_req": "Tên Workspace, chọn ít nhất 01 thành viên làm Manager phụ trách (BR-21) và chọn Múi giờ chuẩn của dự án (BR-22).",
        "in_opt": "Mô tả dự án, Ảnh đại diện Workspace (PNG, JPG, WEBP tối đa 5 MB), chọn Client liên kết hoặc chọn Mẫu cấu hình Workspace.",
        "sys_data": "Mã Workspace mới, gán quyền MANAGER cho người được chọn, lưu cài đặt múi giờ và kiểm tra hạn mức gói cước (BR-58).",
        "output": "Tạo Workspace mới thành công (hiển thị MSG23) và chuyển vào trang quản lý của Workspace đó.",
        "flow": [
            "Owner bấm nút Tạo Workspace mới (/workspace/create) trong Agency của mình.",
            "Owner nhập Tên Workspace, Mô tả, chọn ít nhất 1 nhân sự làm Manager phụ trách (BR-21) và chọn Múi giờ chuẩn cho dự án (BR-22).",
            "Owner bấm nút Tạo Workspace.",
            "Hệ thống kiểm tra hạn mức gói cước (BR-58), lưu Workspace mới kèm phân quyền Manager, hiển thị thông báo MSG23 và mở giao diện Workspace."
        ],
        "abnormal": [
            "Nếu bỏ trống Tên Workspace hoặc chưa chọn Manager phụ trách: Hệ thống báo lỗi bắt buộc nhập (MSG02).",
            "Nếu Agency đã đạt giới hạn số lượng Workspace tối đa của gói cước hiện tại: Hệ thống báo cần nâng cấp gói dịch vụ (MSG48)."
        ]
    },
    "3.4.15": {
        "summary": "Xem thông tin cài đặt chi tiết của dự án (Workspace Profile), bao gồm tên dự án, mô tả, thông tin khách hàng (Client) liên kết, người quản lý (Manager) và cài đặt múi giờ chuẩn.",
        "trigger": "Khi thành viên trong dự án mở trang Thông tin & Cài đặt Workspace (/workspace/:id/detail).",
        "interface": "Màn hình Hồ sơ Workspace (/workspace/:id/detail) hiển thị Tên Workspace, Ảnh đại diện, Mô tả dự án, Thông tin Client liên kết, Danh sách Manager phụ trách và thông số Múi giờ chuẩn (IANA UTC Timezone).",
        "processing": "Hệ thống kiểm tra người dùng là thành viên của Workspace hoặc là Owner của Agency (BR-20), sau đó tải thông tin cấu hình và múi giờ của Workspace (BR-22) lên màn hình.",
        "in_req": "Thành viên có quyền truy cập mở trang Hồ sơ Workspace.",
        "in_opt": "Không bắt buộc.",
        "sys_data": "Thông tin định danh Workspace, cài đặt múi giờ (BR-22), thông tin Client và trạng thái hoạt động.",
        "output": "Hiển thị đầy đủ thông tin cấu hình của Workspace.",
        "flow": [
            "Người dùng mở mục Thông tin & Cài đặt của Workspace (/workspace/:id/detail).",
            "Hệ thống kiểm tra quyền truy cập của người dùng trong Workspace đó (BR-20).",
            "Hệ thống truy xuất dữ liệu cấu hình và thiết lập múi giờ của Workspace (BR-22).",
            "Màn hình hiển thị chi tiết hồ sơ dự án."
        ],
        "abnormal": [
            "Nếu người dùng không thuộc Workspace này: Hệ thống từ chối truy cập và hiển thị MSG07."
        ]
    },
    "3.4.16": {
        "summary": "Cho phép Owner hoặc Manager cập nhật thông tin của Workspace (tên dự án, mô tả, ảnh đại diện) và điều chỉnh cài đặt Múi giờ chuẩn để đồng bộ lịch đăng bài và hạn chót công việc.",
        "trigger": "Khi Owner hoặc Manager sửa thông tin trên trang Cài đặt Workspace (/workspace/:id/detail) và bấm Lưu thay đổi.",
        "interface": "Biểu mẫu chỉnh sửa Hồ sơ Workspace gồm ô sửa Tên Workspace, Mô tả dự án, nút đổi Ảnh đại diện, hộp chọn Múi giờ chuẩn (UTC Timezone) và nút Lưu.",
        "processing": "Hệ thống kiểm tra người thực hiện có quyền Owner hoặc Manager của Workspace không (BR-15, BR-21), kiểm tra ảnh đại diện dưới 5 MB (BR-12) và cập nhật múi giờ mới để áp dụng cho các lịch hẹn đăng bài và hạn công việc trong dự án (BR-22).",
        "in_req": "Tên Workspace và Múi giờ chuẩn (UTC Timezone).",
        "in_opt": "Mô tả dự án, Ảnh đại diện mới của Workspace (PNG, JPG, WEBP tối đa 5 MB).",
        "sys_data": "Cập nhật thông tin Workspace và quy đổi hiển thị thời gian theo múi giờ mới (BR-22).",
        "output": "Lưu cập nhật hồ sơ Workspace thành công và hiển thị thông báo MSG21.",
        "flow": [
            "Owner hoặc Manager mở màn hình Cài đặt Workspace (/workspace/:id/detail).",
            "Người dùng chỉnh sửa Tên dự án, Mô tả, Ảnh đại diện hoặc đổi lại Múi giờ chuẩn (BR-22) rồi bấm Lưu.",
            "Hệ thống kiểm tra quyền hạn (BR-15, BR-21) và định dạng tệp ảnh tải lên (BR-12).",
            "Hệ thống lưu cấu hình mới và hiển thị thông báo thành công (MSG21)."
        ],
        "abnormal": [
            "Nếu Creator hoặc Client (không có quyền quản lý) cố gắng sửa cấu hình Workspace: Hệ thống chặn thao tác và báo MSG07.",
            "Nếu bỏ trống Tên Workspace hoặc tải ảnh quá 5 MB: Hệ thống báo lỗi MSG02 hoặc MSG22."
        ]
    },
    "3.4.17": {
        "summary": "Cho phép Owner xóa mềm một Workspace khi dự án kết thúc hoặc không còn sử dụng. Dữ liệu của Workspace được giữ lại trong 30 ngày để Owner có thể khôi phục trước khi xóa vĩnh viễn.",
        "trigger": "Khi Owner bấm nút Xóa Workspace trong phần Cài đặt dự án (/workspace/:id/detail), xác nhận tên dự án và đồng ý.",
        "interface": "Khu vực Xóa Workspace trên trang Cài đặt (/workspace/:id/detail) kèm hộp thoại xác nhận tên Workspace và nút Xác nhận xóa.",
        "processing": "Hệ thống kiểm tra chỉ duy nhất Owner mới có quyền xóa Workspace (BR-15, BR-16). Khi xác nhận hợp lệ, hệ thống chuyển trạng thái Workspace sang Tạm ẩn chờ xóa (lưu giữ 30 ngày - BR-16) và ngưng quyền truy cập của các thành viên trong dự án đó.",
        "in_req": "Owner nhập đúng tên Workspace để xác nhận xóa.",
        "in_opt": "Lý do đóng/xóa dự án.",
        "sys_data": "Trạng thái Workspace chuyển sang Đã xóa mềm (INACTIVE/DELETED_PENDING) kèm hạn 30 ngày khôi phục (BR-16).",
        "output": "Xóa mềm Workspace thành công, hiển thị thông báo MSG24 và quay về danh sách Workspace.",
        "flow": [
            "Owner mở trang Cài đặt của Workspace (/workspace/:id/detail) và bấm nút Xóa Workspace.",
            "Owner nhập lại tên Workspace vào hộp thoại xác nhận và bấm Đồng ý.",
            "Hệ thống kiểm tra quyền Owner (BR-15) và chuyển Workspace sang trạng thái xóa mềm có hạn khôi phục 30 ngày (BR-16).",
            "Hệ thống hiển thị thông báo MSG24 và đưa người dùng về trang Danh sách Workspace."
        ],
        "abnormal": [
            "Nếu người thao tác không phải là Owner (ví dụ Manager hoặc Creator): Hệ thống chặn thao tác và báo MSG07.",
            "Nếu nhập tên xác nhận không khớp: Hệ thống báo lỗi MSG02."
        ]
    },
    "3.4.18": {
        "summary": "Cho phép thành viên tự rời khỏi một Workspace cụ thể khi không còn tham gia dự án đó nữa, nhưng vẫn giữ nguyên tư cách là thành viên của công ty (Agency).",
        "trigger": "Khi thành viên bấm nút Rời khỏi Workspace trong phần Cài đặt dự án (/workspace/:id/detail) và xác nhận.",
        "interface": "Nút Rời khỏi Workspace (Leave Workspace) kèm hộp thoại xác nhận trên màn hình Cài đặt Workspace (/workspace/:id/detail).",
        "processing": "Hệ thống kiểm tra nếu người muốn rời đi đang là Manager duy nhất của Workspace đó thì yêu cầu phải chuyển quyền Manager cho một thành viên khác trước (BR-21, BR-23). Nếu hợp lệ, hệ thống gỡ người đó khỏi danh sách thành viên của Workspace nhưng vẫn giữ nguyên tài khoản trong Agency (BR-23).",
        "in_req": "Xác nhận đồng ý rời khỏi Workspace.",
        "in_opt": "Không bắt buộc.",
        "sys_data": "Gỡ quyền truy cập khỏi Workspace hiện tại, giữ nguyên tư cách thành viên Agency (BR-23) và bảo toàn các công việc đã làm trước đó.",
        "output": "Rời khỏi Workspace thành công, hiển thị thông báo MSG29 và chuyển về trang Danh sách Workspace.",
        "flow": [
            "Thành viên mở trang Cài đặt Workspace (/workspace/:id/detail) và bấm nút Rời khỏi Workspace.",
            "Người dùng bấm Đồng ý trên hộp thoại xác nhận.",
            "Hệ thống kiểm tra đảm bảo Workspace vẫn còn ít nhất 1 Manager khác đang hoạt động (BR-21, BR-23).",
            "Hệ thống gỡ người dùng khỏi Workspace đó, hiển thị thông báo MSG29 và chuyển về danh sách Workspace."
        ],
        "abnormal": [
            "Nếu người dùng đang là Manager duy nhất của Workspace: Hệ thống chặn thao tác rời dự án và báo cần bổ nhiệm một Manager khác thay thế trước (BR-21, BR-23, MSG36)."
        ]
    },
    "3.4.19": {
        "summary": "Cho phép Owner lưu lại cấu hình của một Workspace đang dùng (gồm múi giờ, khung vai trò, bộ hashtag, mẫu email và gói dịch vụ mẫu) thành Mẫu chuẩn (Workspace Template) để tái sử dụng nhanh cho các dự án sau.",
        "trigger": "Khi Owner bấm nút Lưu thành Mẫu (Save as Template) trong trang Cài đặt Workspace hoặc Thư viện mẫu (/templates), đặt tên mẫu và bấm Lưu.",
        "interface": "Hộp thoại Lưu mẫu Workspace gồm ô nhập Tên mẫu (Template Name), Ngành hàng áp dụng, Mô tả ngắn, các tùy chọn cấu hình muốn lưu lại và nút Lưu mẫu.",
        "processing": "Hệ thống kiểm tra quyền Owner (BR-15), trích xuất các thiết lập cấu trúc của Workspace hiện tại (không sao chép dữ liệu tin nhắn hay bài viết riêng tư) và lưu thành một bản mẫu mới trong thư viện của Agency (BR-24).",
        "in_req": "Tên mẫu cấu hình (Template Name) và Workspace nguồn cần lưu.",
        "in_opt": "Mô tả mẫu và phân loại ngành hàng.",
        "sys_data": "Bản ghi cấu hình mẫu gồm múi giờ mặc định, khung phân quyền, bộ hashtag mẫu, mẫu email và gói dịch vụ liên kết (BR-24).",
        "output": "Lưu mẫu Workspace mới thành công và hiển thị thông báo MSG30.",
        "flow": [
            "Owner mở trang Cài đặt của một Workspace chuẩn hoặc trang Thư viện mẫu (/templates) và chọn Lưu thành mẫu.",
            "Owner nhập Tên mẫu, Mô tả và chọn các mục cấu hình muốn lưu lại rồi bấm Lưu.",
            "Hệ thống kiểm tra quyền Owner (BR-15) và kiểm tra tên mẫu hợp lệ.",
            "Hệ thống đóng gói cấu hình thành Workspace Template mới (BR-24) và hiển thị thông báo MSG30."
        ],
        "abnormal": [
            "Nếu bỏ trống Tên mẫu hoặc nhập quá độ dài cho phép: Hệ thống báo lỗi MSG02 hoặc MSG03."
        ]
    },
    "3.4.20": {
        "summary": "Cho phép Owner xem danh sách và chi tiết các Mẫu cấu hình Workspace (gồm cả mẫu gợi ý của hệ thống và mẫu riêng do Agency đã lưu) để chọn dùng khi mở dự án mới.",
        "trigger": "Khi Owner mở màn hình Thư viện Mẫu Workspace (/templates).",
        "interface": "Màn hình Thư viện Mẫu Workspace (/templates) hiển thị danh sách các thẻ mẫu, bộ lọc theo ngành hàng, nút Xem chi tiết cấu trúc bên trong mẫu, nút Áp dụng mẫu và nút Xóa mẫu.",
        "processing": "Hệ thống kiểm tra quyền Owner (BR-15) và tải danh sách các mẫu cấu hình có sẵn cùng các mẫu do Agency tự tạo (BR-24) để hiển thị.",
        "in_req": "Owner mở màn hình Thư viện Mẫu Workspace.",
        "in_opt": "Từ khóa tìm kiếm tên mẫu hoặc lọc theo ngành hàng.",
        "sys_data": "Danh sách mẫu Workspace kèm thông tin múi giờ mặc định, gói dịch vụ mẫu và ngày tạo.",
        "output": "Hiển thị danh sách và thông tin chi tiết của các Workspace Template.",
        "flow": [
            "Owner mở màn hình Thư viện Mẫu Workspace (/templates).",
            "Hệ thống xác nhận quyền Owner (BR-15) và lấy danh sách các mẫu cấu hình hiện có (BR-24).",
            "Owner có thể lọc theo ngành hàng hoặc bấm vào từng mẫu để xem trước các thiết lập bên trong.",
            "Màn hình hiển thị chi tiết cấu trúc của mẫu đã chọn."
        ],
        "abnormal": [
            "Nếu chưa có mẫu nào khớp với từ khóa tìm kiếm: Hệ thống hiển thị thông báo MSG01."
        ]
    },
    "3.4.21": {
        "summary": "Cho phép Owner áp dụng một Mẫu cấu hình (Workspace Template) đã lưu vào một Workspace để tự động thiết lập sẵn múi giờ, bộ hashtag, mẫu email và gói dịch vụ mẫu chỉ trong vài giây.",
        "trigger": "Khi Owner chọn một mẫu trong Thư viện mẫu (/templates), chọn Workspace đích cần áp dụng và bấm Áp dụng mẫu.",
        "interface": "Hộp thoại Áp dụng mẫu trên màn hình Thư viện Mẫu Workspace (/templates) gồm danh sách chọn mẫu, chọn Workspace đích và nút Xác nhận áp dụng.",
        "processing": "Hệ thống kiểm tra quyền Owner (BR-15), đọc dữ liệu cấu hình từ mẫu đã chọn và tự động tạo các thiết lập tương ứng (múi giờ BR-22, bộ hashtag mẫu, mẫu email, gói truyền thông mẫu) vào Workspace đích mà không làm mất dữ liệu đang có của dự án đó (BR-24).",
        "in_req": "Chọn Mẫu cấu hình (Template) và chọn Workspace đích cần áp dụng.",
        "in_opt": "Tùy chọn các hạng mục muốn chép sang Workspace đích.",
        "sys_data": "Sao chép thiết lập múi giờ, bộ hashtag mẫu và mẫu email từ Template sang Workspace đích (BR-24).",
        "output": "Áp dụng mẫu cấu hình vào Workspace thành công và hiển thị thông báo MSG30.",
        "flow": [
            "Trên màn hình Thư viện Mẫu Workspace (/templates), Owner chọn một mẫu muốn sử dụng và bấm Áp dụng.",
            "Owner chọn Workspace đích cần áp dụng cấu hình và bấm Xác nhận.",
            "Hệ thống kiểm tra quyền Owner (BR-15) và trạng thái hoạt động của Workspace đích.",
            "Hệ thống tự động thiết lập múi giờ (BR-22) cùng các danh mục mẫu vào Workspace đích (BR-24) và hiển thị thông báo MSG30."
        ],
        "abnormal": [
            "Nếu Workspace đích đang bị khóa hoặc đã xóa mềm: Hệ thống từ chối áp dụng và hiển thị thông báo MSG36."
        ]
    },
    "3.4.22": {
        "summary": "Cho phép Owner xóa các Mẫu cấu hình Workspace do Agency tự tạo khi không còn nhu cầu sử dụng. Việc xóa mẫu không làm ảnh hưởng tới các Workspace đã từng áp dụng mẫu đó trước đây.",
        "trigger": "Khi Owner bấm nút Xóa trên một mẫu tùy chỉnh trong Thư viện Mẫu Workspace (/templates) và xác nhận.",
        "interface": "Nút Xóa mẫu trên thẻ Template tại màn hình Thư viện Mẫu Workspace (/templates) kèm hộp thoại xác nhận.",
        "processing": "Hệ thống kiểm tra quyền Owner (BR-15) và kiểm tra mẫu đó là mẫu riêng của Agency (không phải mẫu mặc định cố định của hệ thống), sau đó xóa mẫu khỏi thư viện mà vẫn giữ nguyên các dự án đã tạo từ mẫu này trước đó (BR-24).",
        "in_req": "Chọn mẫu tùy chỉnh cần xóa và xác nhận đồng ý.",
        "in_opt": "Không bắt buộc.",
        "sys_data": "Xóa bản ghi mẫu khỏi thư viện Agency, giữ nguyên các Workspace đã áp dụng trước đây (BR-24).",
        "output": "Xóa mẫu cấu hình thành công và hiển thị thông báo MSG30.",
        "flow": [
            "Owner mở màn hình Thư viện Mẫu Workspace (/templates) và bấm nút Xóa trên mẫu muốn gỡ bỏ.",
            "Owner bấm Đồng ý trên hộp thoại xác nhận xóa.",
            "Hệ thống kiểm tra quyền Owner (BR-15) và xác nhận đây là mẫu do Agency tự tạo.",
            "Hệ thống xóa mẫu khỏi danh sách lựa chọn (BR-24) và hiển thị thông báo MSG30."
        ],
        "abnormal": [
            "Nếu người dùng cố xóa mẫu mặc định dùng chung của toàn hệ thống: Hệ thống chặn thao tác và báo MSG36."
        ]
    },
    "3.4.23": {
        "summary": "Xem danh sách toàn bộ các thành viên đang tham gia trong một dự án (Workspace), kèm theo vai trò cụ thể của từng người (Owner, Manager, Creator, Client).",
        "trigger": "Khi thành viên trong dự án mở màn hình Thành viên Workspace (/workspace/:id/members).",
        "interface": "Màn hình Thành viên Workspace (/workspace/:id/members) gồm ô tìm kiếm, bộ lọc theo vai trò, bảng danh sách thành viên (hiển thị Ảnh đại diện, Họ tên, Email, nhãn Vai trò trong Workspace, Ngày tham gia) và các nút Thêm / Đổi vai trò / Xóa (hiển thị cho Owner và Manager).",
        "processing": "Hệ thống kiểm tra người xem thuộc Workspace đó (BR-20), sau đó truy xuất danh sách toàn bộ thành viên cùng vai trò hiện tại của họ trong dự án (BR-21).",
        "in_req": "Thành viên có quyền truy cập mở trang Thành viên Workspace.",
        "in_opt": "Tìm kiếm theo tên/email hoặc lọc theo vai trò (Manager, Creator, Client).",
        "sys_data": "Danh sách thành viên dự án, vai trò tương ứng và trạng thái hoạt động.",
        "output": "Hiển thị bảng danh sách thành viên của Workspace.",
        "flow": [
            "Người dùng mở mục Thành viên (/workspace/:id/members) trong Workspace đang làm việc.",
            "Hệ thống kiểm tra quyền truy cập của người dùng đối với Workspace đó (BR-20).",
            "Hệ thống lấy danh sách thành viên và vai trò tương ứng từ cơ sở dữ liệu.",
            "Màn hình hiển thị danh sách thành viên kèm các công cụ tìm kiếm, lọc theo vai trò."
        ],
        "abnormal": [
            "Nếu lọc hoặc tìm kiếm không có thành viên nào khớp: Hệ thống hiển thị thông báo MSG01."
        ]
    },
    "3.4.24": {
        "summary": "Cho phép Owner hoặc Manager thêm nhân sự thuộc Agency hoặc thêm tài khoản Khách hàng (Client) vào làm việc trong Workspace và gán vai trò cụ thể (Manager, Creator hoặc Client).",
        "trigger": "Khi Owner hoặc Manager bấm nút Thêm thành viên trên trang Thành viên Workspace (/workspace/:id/members), chọn người dùng cùng vai trò và bấm Xác nhận.",
        "interface": "Hộp thoại Thêm thành viên vào Workspace gồm ô chọn nhân sự từ danh sách Agency (hoặc nhập email Client đối tác), ô chọn Vai trò trong dự án (Manager, Creator, Client) và nút Thêm vào dự án.",
        "processing": "Hệ thống kiểm tra quyền của Owner hoặc Manager (BR-15, BR-21), kiểm tra người được chọn chưa có mặt trong Workspace đó (BR-20), sau đó thêm vào dự án với vai trò được gán và tự động liên kết Hồ sơ thương hiệu nếu người được thêm là Client (BR-13).",
        "in_req": "Chọn người dùng cần thêm và chọn Vai trò trong Workspace (Manager, Creator hoặc Client).",
        "in_opt": "Ghi chú phân công nhiệm vụ ban đầu.",
        "sys_data": "Bản ghi thành viên mới trong Workspace, quyền truy cập dự án (BR-20) và thông báo gửi cho người vừa được thêm.",
        "output": "Thêm thành viên vào Workspace thành công và hiển thị thông báo MSG29.",
        "flow": [
            "Owner hoặc Manager mở trang Thành viên Workspace (/workspace/:id/members) và bấm nút Thêm thành viên.",
            "Người quản lý chọn nhân sự từ danh sách của Agency (hoặc chọn tài khoản Client) và chọn vai trò (Manager, Creator hoặc Client).",
            "Người quản lý bấm nút Thêm vào dự án.",
            "Hệ thống kiểm tra người đó chưa bị trùng trong dự án, lưu phân quyền mới và hiển thị thông báo MSG29."
        ],
        "abnormal": [
            "Nếu người được chọn đã là thành viên trong Workspace này rồi: Hệ thống báo lỗi trùng thành viên (MSG26).",
            "Nếu người thực hiện không phải là Owner hoặc Manager của dự án: Hệ thống chặn thao tác và báo MSG07."
        ]
    },
    "3.4.25": {
        "summary": "Cho phép Owner hoặc Manager thay đổi vai trò của một thành viên trong Workspace (ví dụ nâng cấp từ Creator lên làm Manager phụ trách hoặc ngược lại), đồng thời đảm bảo dự án luôn có ít nhất 1 Manager.",
        "trigger": "Khi Owner hoặc Manager chọn đổi vai trò mới cho một thành viên trên bảng Thành viên Workspace (/workspace/:id/members) và bấm Lưu.",
        "interface": "Hộp chọn đổi vai trò (Role dropdown: Manager, Creator, Client) ngay trên từng dòng thành viên tại màn hình Thành viên Workspace (/workspace/:id/members).",
        "processing": "Hệ thống kiểm tra quyền của Owner/Manager (BR-15, BR-21) và kiểm tra quy tắc bắt buộc: mỗi Workspace phải luôn có ít nhất 1 Manager đang hoạt động (không cho phép chuyển Manager duy nhất còn lại xuống làm Creator - BR-21). Nếu hợp lệ, hệ thống cập nhật ngay quyền hạn mới.",
        "in_req": "Chọn thành viên trong Workspace và chọn Vai trò mới cần đổi.",
        "in_opt": "Không bắt buộc.",
        "sys_data": "Cập nhật vai trò của thành viên trong Workspace và kiểm tra số lượng Manager tối thiểu >= 1 (BR-21).",
        "output": "Cập nhật vai trò thành viên thành công và hiển thị thông báo MSG29.",
        "flow": [
            "Trên màn hình Thành viên Workspace (/workspace/:id/members), Owner hoặc Manager bấm vào ô Vai trò của thành viên cần thay đổi.",
            "Người quản lý chọn vai trò mới (ví dụ từ Creator sang Manager) và xác nhận.",
            "Hệ thống kiểm tra đảm bảo sau khi đổi, dự án vẫn còn ít nhất 1 Manager đang hoạt động (BR-21).",
            "Hệ thống lưu vai trò mới cho thành viên và hiển thị thông báo MSG29."
        ],
        "abnormal": [
            "Nếu cố tình hạ quyền của người đang là Manager duy nhất trong dự án: Hệ thống chặn thao tác và báo dự án bắt buộc phải có ít nhất 1 Manager (BR-21, MSG36)."
        ]
    },
    "3.4.26": {
        "summary": "Cho phép Owner hoặc Manager xóa một thành viên ra khỏi dự án (Workspace). Người bị xóa không còn vào được dự án đó nữa, nhưng các công việc họ đã đóng góp vẫn được giữ lại và họ vẫn là thành viên của Agency.",
        "trigger": "Khi Owner hoặc Manager bấm nút Xóa khỏi Workspace bên cạnh một thành viên tại trang Thành viên Workspace (/workspace/:id/members) và xác nhận.",
        "interface": "Nút Xóa khỏi dự án trên bảng Thành viên Workspace (/workspace/:id/members) kèm hộp thoại xác nhận.",
        "processing": "Hệ thống kiểm tra quyền của Owner/Manager (BR-21), kiểm tra người bị xóa không phải là Manager duy nhất của dự án (BR-21), sau đó thu hồi quyền truy cập của người đó khỏi Workspace trong khi vẫn bảo toàn toàn bộ bài viết, bình luận và tư liệu họ đã tạo (BR-19).",
        "in_req": "Chọn thành viên cần gỡ khỏi Workspace và xác nhận đồng ý.",
        "in_opt": "Không bắt buộc.",
        "sys_data": "Gỡ bản ghi thành viên khỏi Workspace, giữ nguyên tư cách thành viên trong Agency và bảo toàn dữ liệu công việc cũ (BR-19).",
        "output": "Gỡ thành viên khỏi Workspace thành công và hiển thị thông báo MSG29.",
        "flow": [
            "Owner hoặc Manager mở trang Thành viên Workspace (/workspace/:id/members) và bấm nút Xóa bên cạnh thành viên cần gỡ khỏi dự án.",
            "Người quản lý bấm Đồng ý trên hộp thoại xác nhận.",
            "Hệ thống kiểm tra đảm bảo người đó không phải là Manager duy nhất của Workspace (BR-21).",
            "Hệ thống thu hồi quyền truy cập dự án của thành viên đó, giữ nguyên các bài viết/tư liệu họ đã đóng góp (BR-19) và hiển thị thông báo MSG29."
        ],
        "abnormal": [
            "Nếu thành viên đó là Manager duy nhất còn lại của dự án: Hệ thống chặn thao tác xóa và yêu cầu chỉ định Manager khác trước (BR-21, MSG36)."
        ]
    },

    # ==================== 3.5 Media Package & Media Campaign ====================
    "3.5.1": {
        "summary": "Cho phép Owner thiết lập các gói dịch vụ truyền thông mẫu hoặc gói tùy chỉnh (quy định rõ thời gian triển khai, mức ngân sách, số lượng bài đăng cam kết và chỉ tiêu KPI) để làm cơ sở chào dịch vụ và làm việc với Client.",
        "trigger": "Khi Owner mở màn hình Quản lý Gói truyền thông (/media-package/agency), bấm Tạo gói mới, điền thông số gói và bấm Lưu.",
        "interface": "Màn hình Quản lý Gói truyền thông gồm biểu mẫu tạo gói: Tên gói dịch vụ, Loại gói (Theo thời gian / Theo ngân sách / Trọn gói theo KPI), Thời lượng (ví dụ 2 tuần, 1 tháng), Chi phí dự kiến, Danh sách số lượng bài đăng theo từng nền tảng, Chỉ tiêu KPI cam kết và nút Lưu gói.",
        "processing": "Hệ thống kiểm tra quyền Owner (BR-15), kiểm tra các thông tin bắt buộc (tên gói, thời lượng, hạng mục bàn giao và mức giá >= 0), sau đó lưu gói dịch vụ vào danh mục của Agency để sẵn sàng gắn vào các dự án khách hàng (BR-25).",
        "in_req": "Tên gói truyền thông, Phân loại gói, Thời lượng triển khai, Danh sách số lượng bài đăng cam kết và Mức giá dự kiến.",
        "in_opt": "Mô tả chi tiết quyền lợi, chỉ tiêu KPI cam kết (lượt tiếp cận, tương tác) và trạng thái hiển thị mẫu.",
        "sys_data": "Mã gói dịch vụ truyền thông, người tạo (Owner) và trạng thái kích hoạt trong danh mục Agency (BR-25).",
        "output": "Tạo gói dịch vụ truyền thông thành công và hiển thị thông báo MSG31.",
        "flow": [
            "Owner mở màn hình Danh mục Gói truyền thông (/media-package/agency) và bấm Tạo gói dịch vụ mới.",
            "Owner nhập Tên gói, chọn Loại gói, Thời lượng triển khai, Số lượng bài đăng cam kết trên từng kênh, KPI và Đơn giá.",
            "Owner bấm nút Lưu gói dịch vụ.",
            "Hệ thống kiểm tra quyền Owner (BR-15) cùng dữ liệu đầu vào, lưu gói dịch vụ mới (BR-25) và hiển thị thông báo MSG31."
        ],
        "abnormal": [
            "Nếu bỏ trống Tên gói, hạng mục bàn giao hoặc nhập mức giá âm: Hệ thống báo lỗi dưới ô nhập (MSG02, MSG03)."
        ]
    },
    "3.5.2": {
        "summary": "Cho phép Owner, Manager và Client xem danh sách và chi tiết các gói dịch vụ truyền thông mẫu (chia theo thời lượng, theo ngân sách hoặc trọn gói theo KPI) để dễ dàng chọn gói phù hợp cho dự án.",
        "trigger": "Khi Owner, Manager hoặc Client mở màn hình Danh mục Gói truyền thông mẫu (/media-package).",
        "interface": "Màn hình Danh mục Gói truyền thông (/media-package) hiển thị các thẻ gói dịch vụ phân theo 3 nhóm (Theo thời gian, Theo ngân sách, Trọn gói KPI), bảng so sánh số lượng bài đăng, thời lượng, chi phí và nút Chọn gói này để đàm phán.",
        "processing": "Hệ thống kiểm tra quyền truy cập của người dùng trong Workspace/Agency (BR-20), sau đó tải danh sách các gói mẫu của hệ thống và các gói riêng của Agency (BR-25) để hiển thị.",
        "in_req": "Mở màn hình Danh mục Gói truyền thông mẫu.",
        "in_opt": "Bộ lọc theo loại gói (Thời gian / Ngân sách / KPI) hoặc tìm theo từ khóa.",
        "sys_data": "Danh sách gói truyền thông mẫu, cơ cấu hạng mục bàn giao và bảng giá tham khảo (BR-25).",
        "output": "Hiển thị danh sách các gói truyền thông mẫu và chi tiết quyền lợi của từng gói.",
        "flow": [
            "Owner, Manager hoặc Client mở màn hình Gói truyền thông (/media-package) trong dự án.",
            "Hệ thống tải danh sách các gói dịch vụ mẫu đang mở của hệ thống và của Agency (BR-25).",
            "Người dùng lọc theo nhu cầu (thời gian, ngân sách hoặc KPI) và bấm vào từng gói để xem chi tiết số lượng bài viết cam kết.",
            "Người dùng có thể chọn một gói mẫu để bắt đầu bước trao đổi và điều chỉnh cho dự án (3.5.3)."
        ],
        "abnormal": [
            "Nếu không có gói mẫu nào khớp với bộ lọc tìm kiếm: Hệ thống hiển thị thông báo MSG01."
        ]
    },
    "3.5.3": {
        "summary": "Cho phép Client và đại diện Agency (Manager/Owner) trao đổi, đề xuất điều chỉnh các điều khoản của gói truyền thông (như số lượng bài viết, thời gian chạy, chi phí) qua từng vòng đàm phán cho đến khi hai bên thống nhất.",
        "trigger": "Khi Client hoặc Manager chọn một gói truyền thông trong dự án (/media-package), chỉnh sửa đề xuất hoặc gửi phản hồi đàm phán và bấm Gửi đề xuất.",
        "interface": "Màn hình Đàm phán Gói truyền thông gồm bảng chỉnh sửa số lượng ấn phẩm/bài đăng, thời lượng, ngân sách đề xuất, khung ghi chú phản hồi giữa Client và Agency, lịch sử các lần đề xuất và nút Gửi đề xuất chỉnh sửa.",
        "processing": "Hệ thống kiểm tra gói dịch vụ của dự án chưa bị khóa phê duyệt cuối cùng (BR-26), lưu lại bản đề xuất điều chỉnh mới kèm nội dung trao đổi của Client/Manager và gửi thông báo cho bên còn lại xem xét.",
        "in_req": "Nội dung đề xuất điều chỉnh (số lượng bài đăng, thời lượng, mức ngân sách hoặc ghi chú điều khoản).",
        "in_opt": "Tệp tài liệu báo giá hoặc yêu cầu đính kèm.",
        "sys_data": "Lưu lịch sử vòng đàm phán, chuyển trạng thái gói sang Đang đàm phán (NEGOTIATING - BR-26) và thông báo cho đối tác.",
        "output": "Ghi nhận đề xuất điều chỉnh gói truyền thông thành công và hiển thị thông báo MSG31.",
        "flow": [
            "Trên màn hình Gói truyền thông của Workspace (/media-package), Client hoặc Manager chọn gói dịch vụ và nhập các đề xuất thay đổi (về số lượng bài, thời hạn hoặc chi phí).",
            "Người dùng nhập ghi chú trao đổi và bấm nút Gửi đề xuất.",
            "Hệ thống kiểm tra gói chưa bị khóa duyệt (BR-26) và các thông số nhập vào hợp lệ.",
            "Hệ thống lưu phiên bản đề xuất mới vào lịch sử đàm phán, gửi thông báo cho phía bên kia và hiển thị thông báo MSG31."
        ],
        "abnormal": [
            "Nếu gói truyền thông này đã được hai bên chốt duyệt (APPROVED) trước đó: Hệ thống chặn chỉnh sửa và báo gói đã khóa (MSG36)."
        ]
    },
    "3.5.4": {
        "summary": "Xác nhận phê duyệt chốt Gói dịch vụ truyền thông (Approve Media Package) khi cả hai bên (Agency và Client) đã thống nhất hoàn toàn về chi phí, thời gian và số lượng bài đăng cam kết.",
        "trigger": "Khi Manager và Client bấm nút Phê duyệt chốt gói (Approve Package) trên màn hình Gói truyền thông của dự án (/media-package).",
        "interface": "Bảng tổng kết điều khoản cuối cùng của Gói truyền thông kèm trạng thái xác nhận của 2 bên (Phía Agency & Phía Client) và nút Phê duyệt chốt gói.",
        "processing": "Hệ thống ghi nhận xác nhận đồng ý của từng bên (Manager/Owner và Client). Khi cả hai bên đều đã bấm xác nhận đồng thuận, hệ thống chuyển trạng thái gói sang Đã phê duyệt (APPROVED - BR-26) và khóa nội dung gói để dùng làm căn cứ lập Kế hoạch Chiến dịch (3.5.5).",
        "in_req": "Xác nhận phê duyệt từ phía Agency (Manager/Owner) và phía Khách hàng (Client).",
        "in_opt": "Ghi chú xác nhận chốt gói.",
        "sys_data": "Trạng thái xác nhận của 2 bên, thời điểm phê duyệt và khóa gói ở trạng thái APPROVED (BR-26, BR-27).",
        "output": "Phê duyệt chốt gói truyền thông thành công (MSG31), mở khóa bước lập Kế hoạch Chiến dịch chi tiết.",
        "flow": [
            "Client và Manager xem lại bản điều khoản cuối cùng của Gói truyền thông trong dự án (/media-package).",
            "Người dùng bấm nút Phê duyệt chốt gói và xác nhận đồng ý.",
            "Hệ thống kiểm tra và ghi nhận chữ ký xác nhận của bên vừa bấm (BR-26).",
            "Khi cả hai bên (Agency và Client) đều đã xác nhận, hệ thống chuyển gói sang trạng thái Đã phê duyệt (APPROVED) và hiển thị thông báo MSG31."
        ],
        "abnormal": [
            "Nếu gói đã được duyệt khóa từ trước hoặc không ở trạng thái chờ duyệt: Hệ thống hiển thị thông báo MSG36."
        ]
    },
    "3.5.5": {
        "summary": "Cho phép Manager lập Kế hoạch Chiến dịch Truyền thông chi tiết (Media Campaign) dựa trên gói dịch vụ đã chốt, liệt kê cụ thể mục tiêu, thời gian chạy và danh sách từng bài viết dự kiến cho nhãn hàng.",
        "trigger": "Khi Manager mở màn hình Chiến dịch Truyền thông (/workspace/:id/campaign), bấm Tạo chiến dịch mới, điền kế hoạch bài viết và bấm Lưu.",
        "interface": "Màn hình Tạo Chiến dịch Truyền thông (/workspace/:id/campaign) gồm ô chọn Gói truyền thông đã duyệt, nhập Tên chiến dịch, Mục tiêu, Ngày bắt đầu – Ngày kết thúc, cùng bảng thêm danh sách các hạng mục bài viết dự kiến (Tiêu đề, Kênh đăng, Định dạng, Ngày dự kiến) và nút Lưu kế hoạch.",
        "processing": "Hệ thống kiểm tra dự án đã có Gói truyền thông được duyệt làm cơ sở (BR-27), kiểm tra mốc thời gian bắt đầu/kết thúc hợp lệ theo múi giờ của Workspace (BR-22), tạo bản ghi Chiến dịch kèm phiên bản đầu tiên (BR-28) và gửi thông báo để Client vào xem xét.",
        "in_req": "Gói truyền thông gốc đã duyệt, Tên chiến dịch, Mục tiêu, Ngày bắt đầu – Ngày kết thúc và ít nhất 1 hạng mục bài viết dự kiến.",
        "in_opt": "Ghi chú định hướng nội dung và tài liệu đính kèm.",
        "sys_data": "Mã chiến dịch, phiên bản kế hoạch v1 (BR-28), quy đổi thời gian theo múi giờ Workspace (BR-22) và trạng thái Chờ duyệt (PENDING_APPROVAL).",
        "output": "Tạo bản Kế hoạch Chiến dịch Truyền thông thành công và hiển thị thông báo MSG32.",
        "flow": [
            "Manager mở màn hình Chiến dịch Truyền thông (/workspace/:id/campaign) và chọn Tạo chiến dịch từ gói dịch vụ đã duyệt.",
            "Manager nhập Tên chiến dịch, Mục tiêu, Khung thời gian chạy và lên danh sách các bài viết dự kiến (tiêu đề, nền tảng đăng, lịch dự kiến).",
            "Manager bấm nút Lưu và gửi duyệt.",
            "Hệ thống kiểm tra điều kiện gói dịch vụ (BR-27), lưu bản kế hoạch phiên bản đầu tiên (BR-28) và hiển thị thông báo MSG32."
        ],
        "abnormal": [
            "Nếu dự án chưa có Gói truyền thông nào ở trạng thái Đã phê duyệt (APPROVED): Hệ thống chặn tạo chiến dịch và nhắc cần chốt gói dịch vụ trước (BR-27, MSG36).",
            "Nếu bỏ trống Tên chiến dịch hoặc đặt ngày kết thúc sớm hơn ngày bắt đầu: Hệ thống báo lỗi MSG02 hoặc MSG03."
        ]
    },
    "3.5.6": {
        "summary": "Cho phép Manager, Creator và Client xem chi tiết bản Kế hoạch Chiến dịch Truyền thông, bao gồm mục tiêu, tiến độ tổng thể, danh sách toàn bộ các bài viết dự kiến và lịch sử các lần chỉnh sửa.",
        "trigger": "Khi thành viên trong dự án mở màn hình Chi tiết Chiến dịch Truyền thông (/workspace/:id/campaign).",
        "interface": "Màn hình Chi tiết Chiến dịch hiển thị thông tin tổng quan, trạng thái hiện tại, danh sách các hạng mục bài viết dự kiến (kèm kênh đăng và lịch trình), lịch sử các phiên bản cập nhật và khu vực nhận xét giữa Agency với Client.",
        "processing": "Hệ thống kiểm tra người xem là thành viên của Workspace (BR-20), sau đó tải thông tin chiến dịch, danh sách các hạng mục công việc và lịch sử phiên bản (BR-27, BR-28) lên màn hình.",
        "in_req": "Chọn Chiến dịch truyền thông cần xem trong Workspace.",
        "in_opt": "Chọn xem lại các phiên bản trước đó trong lịch sử chỉnh sửa.",
        "sys_data": "Thông tin chiến dịch, gói truyền thông gốc, danh sách hạng mục và lịch sử phiên bản (BR-28).",
        "output": "Hiển thị đầy đủ nội dung Kế hoạch Chiến dịch Truyền thông.",
        "flow": [
            "Manager, Creator hoặc Client mở mục Chiến dịch Truyền thông (/workspace/:id/campaign) trong Workspace.",
            "Hệ thống kiểm tra quyền truy cập của người dùng trong dự án (BR-20).",
            "Hệ thống tải chi tiết kế hoạch chiến dịch, danh sách đầu mục bài viết và lịch sử trao đổi (BR-27, BR-28).",
            "Màn hình hiển thị toàn bộ thông tin chiến dịch để người dùng theo dõi hoặc đóng góp ý kiến."
        ],
        "abnormal": [
            "Nếu dự án chưa có chiến dịch nào hoặc không khớp bộ lọc: Hệ thống hiển thị thông báo MSG01."
        ]
    },
    "3.5.7": {
        "summary": "Cho phép Manager và Client chỉnh sửa hoặc gửi góp ý điều chỉnh bản Kế hoạch Chiến dịch Truyền thông trước khi phê duyệt chính thức. Mỗi lần cập nhật đều được lưu lại thành một phiên bản mới để dễ đối chiếu.",
        "trigger": "Khi Manager chỉnh sửa các hạng mục bài viết/lịch trình hoặc khi Client gửi nhận xét yêu cầu điều chỉnh trên màn hình Chiến dịch (/workspace/:id/campaign) và bấm Lưu cập nhật.",
        "interface": "Biểu mẫu cập nhật Chiến dịch gồm danh sách các hạng mục bài viết (cho phép thêm, sửa, xóa dòng hạng mục), ô điều chỉnh thời gian, khung nhập góp ý của Client và nút Lưu phiên bản mới.",
        "processing": "Hệ thống kiểm tra chiến dịch vẫn đang ở trạng thái Bản nháp (DRAFT) hoặc Chờ duyệt (PENDING_APPROVAL - BR-27, BR-30), lưu lại các thay đổi thành một phiên bản lịch sử mới (BR-28) và gửi thông báo cập nhật cho các bên liên quan.",
        "in_req": "Các nội dung chỉnh sửa trên kế hoạch chiến dịch hoặc nội dung góp ý điều chỉnh.",
        "in_opt": "Ghi chú tóm tắt những điểm vừa thay đổi trong phiên bản mới.",
        "sys_data": "Tạo bản chụp phiên bản mới (Version snapshot - BR-28), người cập nhật và thời gian sửa.",
        "output": "Lưu cập nhật kế hoạch chiến dịch thành công và hiển thị thông báo MSG32.",
        "flow": [
            "Manager hoặc Client mở bản Kế hoạch Chiến dịch đang chờ duyệt (/workspace/:id/campaign).",
            "Người dùng chỉnh sửa danh sách bài viết dự kiến, đổi lịch đăng hoặc nhập nhận xét góp ý rồi bấm Lưu cập nhật.",
            "Hệ thống kiểm tra chiến dịch chưa bị đóng (BR-30) và dữ liệu sửa đổi hợp lệ.",
            "Hệ thống lưu thành một phiên bản lịch sử mới (BR-28) và hiển thị thông báo MSG32."
        ],
        "abnormal": [
            "Nếu chiến dịch đã hoàn tất và đóng lại (COMPLETED): Hệ thống không cho phép chỉnh sửa thêm và báo MSG36."
        ]
    },
    "3.5.8": {
        "summary": "Phê duyệt và kích hoạt Chiến dịch Truyền thông. Ngay khi cả Manager và Client cùng bấm duyệt, hệ thống sẽ chuyển chiến dịch sang Đang triển khai và tự động tạo toàn bộ các hạng mục bài viết thành các đầu việc (Task) trong bảng công việc của Workspace.",
        "trigger": "Khi Manager và Client bấm nút Phê duyệt Chiến dịch (Approve Campaign) trên màn hình Chiến dịch Truyền thông (/workspace/:id/campaign).",
        "interface": "Khu vực Phê duyệt Chiến dịch hiển thị bản kế hoạch chốt, trạng thái đồng thuận của Manager và Client, cùng nút Phê duyệt & Triển khai công việc.",
        "processing": "Hệ thống kiểm tra xác nhận đồng ý của cả Manager và Client (BR-29). Ngay khi đủ sự đồng thuận của 2 bên, hệ thống chuyển trạng thái chiến dịch sang Đang chạy (IN_PROGRESS) và tự động tạo hàng loạt các Task tương ứng vào cột Chờ xử lý (BACKLOG) của Workspace để đội ngũ bắt đầu làm việc.",
        "in_req": "Xác nhận phê duyệt từ cả Manager và Client đối với bản kế hoạch chiến dịch hiện tại.",
        "in_opt": "Ghi chú khi phê duyệt.",
        "sys_data": "Chuyển trạng thái chiến dịch sang IN_PROGRESS và tự động khởi tạo danh sách Task trong Backlog của Workspace (BR-29).",
        "output": "Chiến dịch chính thức kích hoạt, toàn bộ đầu việc được đẩy vào bảng Task của Workspace và hiển thị thông báo MSG33.",
        "flow": [
            "Manager và Client kiểm tra lại danh sách các bài viết dự kiến trên màn hình Chiến dịch (/workspace/:id/campaign).",
            "Cả hai bên bấm nút Phê duyệt Chiến dịch.",
            "Hệ thống ghi nhận sự đồng thuận của 2 bên và chuyển trạng thái chiến dịch sang Đang triển khai (IN_PROGRESS - BR-29).",
            "Hệ thống tự động tạo các đầu việc (Task) tương ứng vào danh sách Backlog của Workspace và hiển thị thông báo MSG33."
        ],
        "abnormal": [
            "Nếu chiến dịch đã được duyệt kích hoạt từ trước hoặc đã kết thúc: Hệ thống chặn thao tác lặp lại và báo MSG36."
        ]
    },
    "3.5.9": {
        "summary": "Cho phép Manager nghiệm thu và đánh dấu hoàn tất Chiến dịch Truyền thông sau khi đã bàn giao xong các hạng mục. Khi đóng chiến dịch, các yêu cầu phát sinh còn đang chờ xử lý của chiến dịch đó cũng sẽ tự động đóng lại.",
        "trigger": "Khi Manager bấm nút Hoàn tất Chiến dịch (Complete Campaign) trên màn hình Chiến dịch Truyền thông (/workspace/:id/campaign) và xác nhận.",
        "interface": "Nút Hoàn tất & Đóng Chiến dịch kèm hộp thoại tóm tắt kết quả thực hiện trên màn hình Chiến dịch (/workspace/:id/campaign).",
        "processing": "Hệ thống kiểm tra người thực hiện là Manager (BR-30) và chiến dịch đang ở trạng thái Đang triển khai (IN_PROGRESS). Khi xác nhận, hệ thống chuyển trạng thái chiến dịch sang Đã hoàn thành (COMPLETED), đồng thời tự động chuyển các yêu cầu phát sinh (Content Request) còn đang chờ (PENDING) của chiến dịch đó sang Đã hủy (CANCELLED - BR-30, BR-32).",
        "in_req": "Manager chọn chiến dịch đang chạy và xác nhận Hoàn tất chiến dịch.",
        "in_opt": "Ghi chú tổng kết nghiệm thu chiến dịch.",
        "sys_data": "Chuyển trạng thái chiến dịch sang COMPLETED, ghi nhận thời gian hoàn tất và đóng các yêu cầu phát sinh còn treo (BR-30).",
        "output": "Đóng chiến dịch thành công và hiển thị thông báo MSG34.",
        "flow": [
            "Manager mở màn hình Chiến dịch Truyền thông đang chạy (/workspace/:id/campaign) và bấm nút Hoàn tất Chiến dịch.",
            "Manager xem tóm tắt tiến độ trên hộp thoại xác nhận và bấm Đồng ý.",
            "Hệ thống kiểm tra quyền Manager (BR-30) và cập nhật trạng thái chiến dịch sang Đã hoàn thành (COMPLETED).",
            "Hệ thống tự động đóng các yêu cầu phát sinh còn đang chờ của chiến dịch đó và hiển thị thông báo MSG34."
        ],
        "abnormal": [
            "Nếu người thao tác không phải là Manager hoặc chiến dịch chưa được kích hoạt chạy: Hệ thống từ chối và báo MSG07 hoặc MSG36."
        ]
    },
    "3.5.10": {
        "summary": "Cho phép Client hoặc Manager gửi yêu cầu làm thêm nội dung phát sinh ngoài kế hoạch ban đầu (ví dụ: bài đăng sự kiện đột xuất, thông cáo mới) để đội dự án xem xét và bổ sung vào công việc.",
        "trigger": "Khi Client hoặc Manager mở màn hình Yêu cầu Nội dung (/workspace/:id/requests), bấm Tạo yêu cầu mới, điền nội dung mong muốn và bấm Gửi.",
        "interface": "Màn hình Tạo Yêu cầu Nội dung (/workspace/:id/requests) gồm ô nhập Tiêu đề yêu cầu, Mô tả chi tiết nội dung mong muốn, chọn Nền tảng đăng dự kiến, Hạn hoàn thành mong muốn, nút đính kèm tệp tham khảo và nút Gửi yêu cầu.",
        "processing": "Hệ thống kiểm tra quyền thành viên trong Workspace (BR-20), kiểm tra tiêu đề và mô tả không bị bỏ trống, sau đó lưu yêu cầu mới ở trạng thái Chờ xử lý (PENDING - BR-31) và gửi thông báo cho Manager của dự án.",
        "in_req": "Tiêu đề yêu cầu nội dung phát sinh và Mô tả chi tiết yêu cầu.",
        "in_opt": "Nền tảng mạng xã hội mong muốn, Hạn chót đề xuất và Tệp tài liệu/hình ảnh tham khảo.",
        "sys_data": "Mã yêu cầu phát sinh, người gửi, thời gian tạo và trạng thái khởi tạo Chờ xử lý (PENDING - BR-31).",
        "output": "Tạo yêu cầu nội dung phát sinh thành công và hiển thị thông báo MSG35.",
        "flow": [
            "Client hoặc Manager mở màn hình Yêu cầu Nội dung (/workspace/:id/requests) và bấm nút Tạo yêu cầu mới.",
            "Người dùng nhập Tiêu đề, Mô tả chi tiết bài viết cần làm thêm, chọn kênh đăng và hạn mong muốn rồi bấm Gửi yêu cầu.",
            "Hệ thống kiểm tra thông tin bắt buộc và lưu yêu cầu ở trạng thái Chờ xử lý (PENDING - BR-31).",
            "Hệ thống thông báo cho Manager phụ trách dự án và hiển thị thông báo thành công (MSG35)."
        ],
        "abnormal": [
            "Nếu bỏ trống Tiêu đề hoặc Mô tả yêu cầu: Hệ thống báo lỗi MSG02 dưới ô nhập."
        ]
    },
    "3.5.11": {
        "summary": "Theo dõi và xử lý trạng thái của các Yêu cầu nội dung phát sinh (Chờ xử lý -> Đang xem xét -> Chấp nhận hoặc Từ chối). Khi Manager bấm Chấp nhận một yêu cầu, hệ thống sẽ tự động tạo ngay một đầu việc (Task) mới trong Workspace.",
        "trigger": "Khi Manager hoặc Client mở danh sách Yêu cầu Nội dung (/workspace/:id/requests) để xem tiến độ hoặc khi Manager đổi trạng thái xét duyệt yêu cầu.",
        "interface": "Bảng danh sách Yêu cầu Nội dung hiển thị Tiêu đề, Người gửi, Ngày tạo, Hạn mong muốn, nhãn Trạng thái (PENDING, IN_PROGRESS, ACCEPTED, DENIED) và các nút tiếp nhận/chấp nhận/từ chối dành cho Manager.",
        "processing": "Hệ thống cho phép cả Client và Manager theo dõi trạng thái, nhưng chỉ Manager/Owner mới có quyền đổi trạng thái xét duyệt (BR-31). Đặc biệt, khi Manager chuyển trạng thái sang Đã chấp nhận (ACCEPTED), hệ thống tự động tạo một Task mới trong danh sách công việc (Backlog) của Workspace để giao cho Creator thực hiện (BR-31, BR-33).",
        "in_req": "Chọn yêu cầu nội dung và chọn trạng thái xử lý mới (Đang xem xét / Chấp nhận / Từ chối - dành cho Manager).",
        "in_opt": "Ghi chú phản hồi hoặc lý do từ chối yêu cầu.",
        "sys_data": "Cập nhật trạng thái yêu cầu và tự động tạo Task mới trong Workspace khi yêu cầu được Chấp nhận (BR-31).",
        "output": "Cập nhật trạng thái yêu cầu thành công (hiển thị MSG35) và sinh Task mới nếu được chấp nhận.",
        "flow": [
            "Manager hoặc Client mở màn hình Yêu cầu Nội dung (/workspace/:id/requests) để xem danh sách các yêu cầu phát sinh.",
            "Manager mở một yêu cầu đang chờ và chọn chuyển trạng thái sang Đang xem xét (IN_PROGRESS), Chấp nhận (ACCEPTED) hoặc Từ chối (DENIED).",
            "Nếu chọn Chấp nhận, hệ thống tự động tạo một Task tương ứng vào bảng công việc của Workspace (BR-31, BR-33).",
            "Hệ thống lưu trạng thái mới, thông báo cho Client và hiển thị thông báo MSG35."
        ],
        "abnormal": [
            "Nếu Client cố tự bấm Chấp nhận yêu cầu: Hệ thống chặn thao tác vì chỉ Manager/Owner mới có quyền xét duyệt (BR-31, MSG07).",
            "Nếu yêu cầu đã được xử lý xong hoặc đã hủy trước đó: Hệ thống báo không thể đổi trạng thái lại (MSG36)."
        ]
    },
    "3.5.12": {
        "summary": "Cho phép người tạo (Client hoặc Manager) chỉnh sửa lại nội dung, mô tả hoặc hạn mong muốn của Yêu cầu phát sinh khi yêu cầu đó vẫn đang ở trạng thái Chờ xử lý (PENDING).",
        "trigger": "Khi Client hoặc Manager mở một yêu cầu đang ở trạng thái Chờ xử lý (/workspace/:id/requests), sửa lại thông tin và bấm Lưu.",
        "interface": "Biểu mẫu chỉnh sửa Yêu cầu Nội dung gồm ô sửa Tiêu đề, Mô tả chi tiết, Nền tảng mong muốn, Hạn đề xuất và nút Lưu cập nhật.",
        "processing": "Hệ thống kiểm tra yêu cầu đó có đúng là đang ở trạng thái Chờ xử lý (PENDING) hay không (BR-32). Nếu phía Agency đã bắt đầu xử lý hoặc đã duyệt/từ chối thì hệ thống khóa không cho sửa nữa; nếu vẫn đang PENDING thì lưu nội dung mới.",
        "in_req": "Tiêu đề và Mô tả yêu cầu sau khi chỉnh sửa.",
        "in_opt": "Cập nhật hạn mong muốn hoặc tệp đính kèm.",
        "sys_data": "Kiểm tra điều kiện trạng thái PENDING (BR-32) và lưu thời gian cập nhật.",
        "output": "Cập nhật nội dung yêu cầu phát sinh thành công và hiển thị thông báo MSG35.",
        "flow": [
            "Người tạo mở một Yêu cầu nội dung đang ở trạng thái Chờ xử lý (PENDING) trên trang Yêu cầu (/workspace/:id/requests).",
            "Người dùng sửa lại Tiêu đề, Mô tả hoặc Hạn mong muốn rồi bấm Lưu cập nhật.",
            "Hệ thống kiểm tra yêu cầu vẫn đang ở trạng thái PENDING (BR-32) và dữ liệu nhập hợp lệ.",
            "Hệ thống lưu thông tin mới và hiển thị thông báo MSG35."
        ],
        "abnormal": [
            "Nếu yêu cầu đã được Manager chuyển sang Đang xem xét, Đã chấp nhận hoặc Đã từ chối: Hệ thống chặn chỉnh sửa và hiển thị thông báo MSG36 (BR-32)."
        ]
    },
    "3.5.13": {
        "summary": "Cho phép Client hoặc Manager hủy bỏ một Yêu cầu nội dung phát sinh nếu không còn cần thiết nữa, với điều kiện yêu cầu đó vẫn đang ở trạng thái Chờ xử lý (PENDING).",
        "trigger": "Khi người tạo bấm nút Hủy yêu cầu (Cancel Request) trên một yêu cầu đang chờ tại màn hình Yêu cầu Nội dung (/workspace/:id/requests) và xác nhận.",
        "interface": "Nút Hủy yêu cầu kèm hộp thoại xác nhận trên màn hình Yêu cầu Nội dung (/workspace/:id/requests).",
        "processing": "Hệ thống kiểm tra yêu cầu đang ở trạng thái Chờ xử lý (PENDING - BR-32). Nếu hợp lệ, hệ thống chuyển trạng thái yêu cầu sang Đã hủy (CANCELLED); nếu yêu cầu đã chuyển sang bước xử lý hoặc đã tạo thành Task thì không cho phép hủy.",
        "in_req": "Chọn yêu cầu đang ở trạng thái PENDING và xác nhận Hủy.",
        "in_opt": "Lý do hủy yêu cầu.",
        "sys_data": "Chuyển trạng thái yêu cầu từ PENDING sang CANCELLED (BR-32).",
        "output": "Hủy yêu cầu nội dung phát sinh thành công và hiển thị thông báo MSG35.",
        "flow": [
            "Trên màn hình Yêu cầu Nội dung (/workspace/:id/requests), người tạo chọn một yêu cầu đang ở trạng thái Chờ xử lý (PENDING) và bấm Hủy yêu cầu.",
            "Người dùng bấm Đồng ý trên hộp thoại xác nhận.",
            "Hệ thống kiểm tra yêu cầu vẫn đang ở trạng thái PENDING (BR-32).",
            "Hệ thống chuyển trạng thái yêu cầu sang Đã hủy (CANCELLED) và hiển thị thông báo MSG35."
        ],
        "abnormal": [
            "Nếu yêu cầu đã chuyển sang trạng thái Đang xem xét, Đã chấp nhận hoặc Đã từ chối: Hệ thống từ chối hủy và hiển thị thông báo MSG36 (BR-32)."
        ]
    },
}
