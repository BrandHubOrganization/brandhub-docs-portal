#!/usr/bin/env python3
"""
================================================================================
BRANDHUB LIVE DEMO MONITOR (SELENIUM 4 MULTI-ROLE CONTROLLER + QUICK FILL)
================================================================================
Công cụ điều khiển trình duyệt trực tiếp phục vụ buổi bảo vệ Đồ án Tốt nghiệp
của nhóm SE_08 triển khai Chiến dịch Tuyển sinh Đại học FPT 2027 (4 Tuần):
  - Quản lý 6 cửa sổ Chrome độc lập ứng với 6 Canonical Roles:
    Guest (Khách truy cập công khai), Owner (Lê Trí Trung), Manager (Nguyễn Thành Lộc),
    Creator (Nguyễn Chơn Phước), Client (Ban Tuyển sinh Đại học FPT), Admin (Quản trị viên BrandHub).
  - Tự động mở & đăng nhập đủ 6 cửa sổ Chrome chỉ với 1 nút bấm (tự động dự phòng mật khẩu).
  - Gắn sẵn thanh HUD nổi góc trái bên dưới (Shadow DOM + WebSocket thời gian thực :3999/ws)
    đồng bộ bước demo tức thì trên toàn bộ 6 cửa sổ Chrome khi trình chiếu song song Laptop <-> TV.
  - Điều hướng tức thì qua toàn bộ các trang của hệ thống theo lộ trình B1 -> B15:
    + 7 Gói truyền thông đa lĩnh vực (Giáo dục ĐH FPT, SaaS, F&B, BĐS, Mỹ phẩm, TMĐT, Du lịch)
    + Workspace ĐH FPT Tuyển sinh 2027 x SE08 Digital, Thư viện Key Visual Gemini & Chat nhóm
    + Chiến dịch 4 tuần (20 công việc từ Coming Soon, Ngành học, Tiện ích, Workshop THPT,
      FPTU Open Day đến Báo chí chính thống VnExpress / Thanh Niên / Dân Trí)
    + Bắn trực tiếp ảnh Key Visual Gemini Nano Banana lên bài viết trên /editor chỉ với 1 cú nhấp
    + Gọi AI sinh Caption, Kiểm duyệt vi phạm (FR 3.6.33), Duyệt 2 tầng v1/v2 & Diff phiên bản
    + Đa nền tảng (Facebook, Instagram, TikTok, Threads), Lịch đăng, Khảo sát THPT, SePay (VietQR) & Admin.
================================================================================
"""

from __future__ import annotations

import argparse
import base64
import contextlib
import ctypes
import hashlib
import io
import json
import os
import runpy
import socket
import struct
import subprocess
import sys
import threading
import time
import traceback
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

try:
    from selenium import webdriver
    from selenium.common.exceptions import WebDriverException
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
except ImportError:
    print("[ERROR] Chưa cài đặt thư viện `selenium`. Chạy: pip install selenium")
    sys.exit(1)


# ==============================================================================
# 1. CẤU HÌNH HỆ THỐNG & DỮ LIỆU KỊCH BẢN TUYỂN SINH ĐẠI HỌC FPT 2027 (4 TUẦN)
# ==============================================================================
DEFAULT_APP_URL = os.environ.get("BRANDHUB_APP_URL", "http://localhost:3000")
DEFAULT_MONITOR_PORT = int(os.environ.get("BRANDHUB_DEMO_PORT", "3999"))
DEFAULT_PASSWORD = os.environ.get("BRANDHUB_DEMO_PASSWORD", "Password123")

DEFAULT_IDS = {
    "agency_id": "359a1839-18c7-48e2-8a68-f5f68c3375b6",
    "workspace_id": "b47477c4-13ad-44ff-8c49-f73f1837461b",
    "package_id": "d7e00000-0000-4000-8000-000000000200",
    "ws_package_id": "d7e00000-0000-4000-8000-000000000201",
    "campaign_id": "d7e00000-0000-4000-8000-000000000301",
    "task_id": "c6453698-cf56-38c1-96d2-90ccdd985228",
    "survey_task_id": "2a100fd3-db57-3355-bef4-45dfbb4cf2f3",
    "event_task_id": "85a66c1c-b49b-3788-8bc3-a21336649041",
    "workshop_task_id": "c1176d26-249c-3d32-bbad-f720b3a518a4",
    "press_task_id": "b8585f25-6a26-3a5e-9199-19c2e9fb3f06",
    "kol_task_id": "3f1ae3a9-6518-35df-a596-1013c055e279",
    "newsletter_task_id": "b6a13469-05c4-3af0-88b1-ba2ca510d18f",
    "video_task_id": "31a69211-9cec-30f0-b3f0-4e01ac3315a1",
}

CANONICAL_ROLE_ORDER: tuple[str, ...] = ("Guest", "Owner", "Manager", "Creator", "Client", "Admin")

ROLE_PROFILES: dict[str, dict[str, Any]] = {
    "Guest": {
        "role": "Guest",
        "code": "GUEST",
        "full_name": "Khách truy cập công khai",
        "email": "Chưa đăng nhập",
        "badge_color": "#ea6c3b",
        "default_route": "/",
        "requires_auth": False,
    },
    "Owner": {
        "role": "Owner",
        "code": "OWNER",
        "full_name": "Lê Trí Trung",
        "email": "user177@demo.brandhub.test",
        "badge_color": "#ea6c3b",
        "default_route": "/agency/{agency_id}/media-packages",
        "requires_auth": True,
    },
    "Manager": {
        "role": "Manager",
        "code": "MANAGER",
        "full_name": "Nguyễn Thành Lộc",
        "email": "user1@demo.brandhub.test",
        "badge_color": "#ea6c3b",
        "default_route": "/workspaces/{workspace_id}/campaigns",
        "requires_auth": True,
    },
    "Creator": {
        "role": "Creator",
        "code": "CREATOR",
        "full_name": "Nguyễn Chơn Phước",
        "email": "user13@demo.brandhub.test",
        "badge_color": "#ea6c3b",
        "default_route": "/workspaces/{workspace_id}/tasks",
        "requires_auth": True,
    },
    "Client": {
        "role": "Client",
        "code": "CLIENT",
        "full_name": "Ban Tuyển sinh Đại học FPT",
        "email": "user59@demo.brandhub.test",
        "badge_color": "#ea6c3b",
        "default_route": "/workspaces/{workspace_id}/task-approvals",
        "requires_auth": True,
    },
    "Admin": {
        "role": "Admin",
        "code": "ADMIN",
        "full_name": "Quản trị viên BrandHub",
        "email": "admin@demo.brandhub.test",
        "badge_color": "#ea6c3b",
        "default_route": "/admin?view=revenue",
        "requires_auth": True,
    },
}

# Văn bản chuẩn phục vụ Quick-Fill trong buổi bảo vệ (kiểm duyệt theo chuẩn Humanizer:
# câu chữ tự nhiên, rõ số liệu thực tế mùa tuyển sinh 2027, không dùng gạch ngang dài hay từ sáo rỗng).
DEMO_TEXTS = {
    "out_of_scope_title": "[Tuần 3 - Phát sinh] Tổng hợp lịch xe đưa đón học sinh THPT dự Ngày hội FPTU Open Day 2027",
    "out_of_scope_desc": (
        "Bài thông báo chi tiết 08 điểm đón xe buýt miễn phí dành cho học sinh lớp 12 và phụ huynh tham gia "
        "trải nghiệm phòng Lab Thiết kế Vi mạch bán dẫn, thư viện xanh và tư vấn Học bổng Nguyễn Văn Đạo năm 2027."
    ),
    "out_of_scope_criteria": (
        "Ghi rõ khung giờ đón tại từng trường THPT, đầu mối sinh viên tình nguyện phụ trách mỗi tuyến xe "
        "và đính kèm đường dẫn đăng ký https://tuyensinh.fpt.edu.vn."
    ),
    "subtask_desc": (
        "Biên soạn nội dung bài đăng tổng hợp điểm nhấn chuỗi Workshop phổ biến tiện ích học đường ĐH FPT tại các trường THPT "
        "và thông báo mở cổng xét Học bổng Nguyễn Văn Đạo năm 2027 cho khóa K23."
    ),
    "subtask_criteria": (
        "Nêu rõ trải nghiệm kính VR và Robotics tại buổi Workshop, 3 mức học bổng 50%, 70%, 100% học phí, "
        "lộ trình thực tập doanh nghiệp OJT từ học kỳ 6 và đường dẫn https://tuyensinh.fpt.edu.vn."
    ),
    "brief_notes": (
        "1. Phản ánh không khí hào hứng của học sinh lớp 12 tại chuỗi Workshop trải nghiệm tiện ích học đường Đại học FPT.\n"
        "2. Cung cấp chính xác 3 mức Học bổng Nguyễn Văn Đạo năm 2027: 50%, 70% và 100% học phí toàn khóa.\n"
        "3. Nhấn mạnh kỳ thực tập doanh nghiệp (On-the-Job Training - OJT) từ học kỳ 6 tại FPT Software và FPT Smart Cloud.\n"
        "4. Hướng dẫn nộp hồ sơ xét tuyển đợt 1 trực tuyến tại https://tuyensinh.fpt.edu.vn."
    ),
    "brief_source_url": "https://tuyensinh.fpt.edu.vn",
    "ai_topic": (
        "Tổng hợp điểm nhấn chuỗi Workshop trải nghiệm tiện ích học đường Đại học FPT dành cho học sinh THPT "
        "(đeo kính VR tham quan phòng Lab bán dẫn, điều khiển Robotics, tìm hiểu thư viện xanh, sân Vovinam và 40 CLB) "
        "kết hợp thông báo mở đăng ký xét Học bổng Nguyễn Văn Đạo năm 2027 tại 5 cơ sở Hà Nội, Đà Nẵng, Quy Nhơn, TP.HCM, Cần Thơ."
    ),
    "ai_tone_label": "Chuyên nghiệp",
    "ai_platform_label": "Facebook",
    "ai_language_label": "Tiếng Việt",
    "ai_hashtag_count": "6",
    "violation_sample": (
        "\n\n[Đoạn văn kiểm thử bộ lọc an toàn]: Cam kết 100% việc làm lương ngàn đô ngay khi nhập học, "
        "tuyển thẳng không cần điều kiện, các nơi khác đều là bằng cấp vô giá trị!"
    ),
    "caption_v1_clean": (
        "TỪ SÂN TRƯỜNG THPT ĐẾN PHÒNG LAB CÔNG NGHỆ CAO: MỞ ĐĂNG KÝ XÉT HỌC BỔNG ĐẠI HỌC FPT 2027\n\n"
        "Sau chuỗi Workshop phổ biến tiện ích học đường sôi nổi tại các trường THPT, hàng trăm bạn học sinh lớp 12 "
        "đã trực tiếp đeo kính VR khám phá khuôn viên 5 cơ sở, điều khiển cánh tay Robotics và trò chuyện cùng giảng viên "
        "ngành Thiết kế Vi mạch bán dẫn, Trí tuệ nhân tạo (AI).\n\n"
        "Hệ sinh thái học tập thực tiễn đang chờ đón tân sinh viên khóa K23 tại Trường Đại học FPT:\n"
        "- Môi trường học tập hiện đại tại Hà Nội, Đà Nẵng, Quy Nhơn, TP.HCM và Cần Thơ với thư viện xanh, ký túc xá tiện nghi, sân Vovinam và hơn 40 CLB sinh viên.\n"
        "- Giáo trình chuẩn quốc tế, chú trọng tiếng Anh và kỹ năng làm việc trong dự án công nghệ thực tế.\n"
        "- Cổng nhận hồ sơ đăng ký xét Học bổng Nguyễn Văn Đạo đợt 1 năm 2027 đã chính thức mở.\n\n"
        "Đăng ký tư vấn và nộp hồ sơ trực tuyến tại: https://tuyensinh.fpt.edu.vn\n"
        "#DaiHocFPT #TuyenSinhFPTU2027 #WorkshopTHPT #HocBongNguyenVanDao #ViMachBanDan #FPTUniversity"
    ),
    "client_reject_note": (
        "Nội dung bản thảo v1 đã truyền tải rất tốt không khí thực tế của chuỗi Workshop tại các trường THPT. "
        "Tuy nhiên, Ban Tuyển sinh đề nghị bổ sung rõ 3 mức Học bổng Nguyễn Văn Đạo năm 2027 cụ thể (50%, 70% và 100% học phí toàn khóa) "
        "cùng thông tin học kỳ thực tập doanh nghiệp (On-the-Job Training - OJT) từ học kỳ 6 tại FPT Software và FPT Smart Cloud "
        "để phụ huynh và học sinh lớp 12 nắm đầy đủ quyền lợi trước khi duyệt xuất bản."
    ),
    "caption_v2_addition": (
        "\n\nQuyền lợi học bổng và lộ trình thực tập doanh nghiệp dành cho khóa K23 (2027):\n"
        "- Chương trình Học bổng Nguyễn Văn Đạo năm 2027: Trao tặng các mức 50%, 70% và 100% học phí toàn khóa học cho học sinh THPT có thành tích học tập và năng lực nổi trội.\n"
        "- Học kỳ doanh nghiệp (On-the-Job Training - OJT): 100% sinh viên tham gia làm việc thực tế từ học kỳ 6 tại FPT Software, FPT Smart Cloud và mạng lưới doanh nghiệp đối tác trong và ngoài nước."
    ),
}


# ==============================================================================
# 1.5. LỘ TRÌNH THUYẾT TRÌNH ĐỒNG BỘ (B0 -> B15 + Q&A) & WEBSOCKET HUB
# ==============================================================================
DEMO_TIMELINE: list[dict[str, Any]] = [
    {"step_code": "B0", "sub_code": "B0", "action_id": "B0_GUEST_LANDING", "role": "Guest", "title": "Trang chủ BrandHub (Khách truy cập công khai)", "stage": "Mở đầu", "fr_code": "FR 3.2", "kind": "nav", "hint": "Bấm Tiếp để bắt đầu Bước B1 với vai trò Owner."},
    {"step_code": "B1", "sub_code": "B1.1", "action_id": "B1_NAV", "role": "Owner", "title": "Danh mục 7 Gói truyền thông đa lĩnh vực", "stage": "GĐ 1: Gói & Chiến dịch", "fr_code": "FR 3.5.1 - 3.5.4", "kind": "nav", "hint": "Lướt qua 7 thẻ gói đa ngành của SE08 Digital Agency."},
    {"step_code": "B1", "sub_code": "B1.2", "action_id": "B1_NAV_WS_PACKAGE", "role": "Owner", "title": "Gói Tuyển sinh ĐH FPT 2027 (185tr, 19 hạng mục)", "stage": "GĐ 1: Gói & Chiến dịch", "fr_code": "FR 3.5.1 - 3.5.4", "kind": "nav", "hint": "Xem gói 185 triệu VNĐ đã thương thảo & chốt trong Workspace."},
    {"step_code": "B2", "sub_code": "B2.1", "action_id": "B2_NAV", "role": "Owner", "title": "Đội ngũ 5 Thành viên SE08 & Ban Tuyển sinh ĐH FPT", "stage": "GĐ 1: Gói & Chiến dịch", "fr_code": "FR 3.4.9", "kind": "nav", "hint": "Xem phân quyền nhóm SE08 & Ban Tuyển sinh trong Workspace."},
    {"step_code": "B2", "sub_code": "B2.2", "action_id": "B2_NAV_CLIENT_PROFILE", "role": "Owner", "title": "Hồ sơ Thương hiệu (Brand Profile) Trường Đại học FPT", "stage": "GĐ 1: Gói & Chiến dịch", "fr_code": "FR 3.4.21", "kind": "nav", "hint": "Xem thông tin 5 cơ sở, OJT và danh sách từ khóa hạn chế."},
    {"step_code": "B2", "sub_code": "B2.3", "action_id": "B2_NAV_LIBRARY", "role": "Creator", "title": "Thư viện 4 Thư mục Tuần & Key Visual Gemini", "stage": "GĐ 1: Gói & Chiến dịch", "fr_code": "FR 3.6.25", "kind": "nav", "hint": "Xem 4 thư mục tuần, 7 ảnh Key Visual Gemini & Mẫu bài viết."},
    {"step_code": "B2", "sub_code": "B2.4", "action_id": "B2_NAV_CHAT", "role": "Manager", "title": "Kênh Trò chuyện nhóm SE08 Digital & ĐH FPT", "stage": "GĐ 1: Gói & Chiến dịch", "fr_code": "FR 3.5.5", "kind": "nav", "hint": "Xem trao đổi trực tiếp giữa team SE08 và Ban Tuyển sinh ĐH FPT."},
    {"step_code": "B3", "sub_code": "B3.1", "action_id": "B3_STEP_INFO", "role": "Manager", "title": "Chiến dịch 4 Tuần: Lộ trình & Master Brief", "stage": "GĐ 1: Gói & Chiến dịch", "fr_code": "FR 3.5.6 - 3.5.13", "kind": "nav", "hint": "Xem 6/6 khối Master Brief cho 4 tuần chiến dịch tuyển sinh."},
    {"step_code": "B3", "sub_code": "B3.2", "action_id": "B3_STEP_TASKS", "role": "Manager", "title": "Chiến dịch 4 Tuần: Timeline 19 Hạng mục gói", "stage": "GĐ 1: Gói & Chiến dịch", "fr_code": "FR 3.5.6 - 3.5.13", "kind": "nav", "hint": "Xem timeline 4 tuần & nút Thêm công việc phát sinh."},
    {"step_code": "B3", "sub_code": "B3.3", "action_id": "B3_FILL_OUT_OF_SCOPE", "role": "Manager", "title": "Điền thử Công việc phát sinh (Lịch xe Open Day)", "stage": "GĐ 1: Gói & Chiến dịch", "fr_code": "FR 3.5.10", "kind": "fill", "hint": "Tự điền hộp thoại phát sinh; có thể bấm Tạo hoặc Đóng trên Chrome."},
    {"step_code": "B3", "sub_code": "B3.4", "action_id": "B3_STEP_PARTNERS", "role": "Manager", "title": "Chiến dịch 4 Tuần: 6 Đối tác Báo chí, KOL & OOH", "stage": "GĐ 1: Gói & Chiến dịch", "fr_code": "FR 3.5.12", "kind": "nav", "hint": "Xem VnExpress, Thanh Niên, Dân Trí, VTV1, Schannel & LED THPT."},
    {"step_code": "B4", "sub_code": "B4.1", "action_id": "B4_NAV", "role": "Manager", "title": "20 Công việc 4 tuần & 5 Subtask bài Tuần 3", "stage": "GĐ 2: Công việc & Subtask", "fr_code": "FR 3.6.1 - 3.6.10", "kind": "nav", "hint": "Xem phân công 3 Creator SE08 & 5 Subtask bài trọng điểm Tuần 3."},
    {"step_code": "B4", "sub_code": "B4.2", "action_id": "B4_FILL_SUBTASK", "role": "Manager", "title": "Điền mẫu Mô tả & Tiêu chí nghiệm thu Subtask", "stage": "GĐ 2: Công việc & Subtask", "fr_code": "FR 3.6.5", "kind": "fill", "hint": "Tự điền mô tả & tiêu chí nghiệm thu vào form Subtask đang mở."},
    {"step_code": "B4", "sub_code": "B4.3", "action_id": "B4_NAV_SURVEYS", "role": "Creator", "title": "Khảo sát Nguyện vọng Học sinh THPT (/survey)", "stage": "GĐ 2: Công việc & Subtask", "fr_code": "FR 3.6.28", "kind": "nav", "hint": "Xem khảo sát 4 câu hỏi và phản hồi thực tế của học sinh lớp 12."},
    {"step_code": "B4", "sub_code": "B4.4", "action_id": "B4_NAV_EVENT", "role": "Creator", "title": "Kế hoạch Sự kiện FPTU Open Day 2027 (/event)", "stage": "GĐ 2: Công việc & Subtask", "fr_code": "FR 3.6.29", "kind": "nav", "hint": "Xem 5 phân khu sự kiện lớn + runsheet Ngày hội FPTU Open Day."},
    {"step_code": "B4", "sub_code": "B4.5", "action_id": "B4_NAV_WORKSHOP", "role": "Creator", "title": "Chuỗi Workshop Trải nghiệm THPT (/workshop)", "stage": "GĐ 2: Công việc & Subtask", "fr_code": "FR 3.6.30", "kind": "nav", "hint": "Xem diễn giả, lịch trình, hậu cần & phiếu đăng ký học sinh."},
    {"step_code": "B4", "sub_code": "B4.6", "action_id": "B4_NAV_REQUESTS", "role": "Manager", "title": "Yêu cầu Nội dung từ Ban Tuyển sinh (/requests)", "stage": "GĐ 2: Công việc & Subtask", "fr_code": "FR 3.6.32", "kind": "nav", "hint": "Xem yêu cầu bổ sung bài truyền thông từ phía Đại học FPT."},
    {"step_code": "B5", "sub_code": "B5.1", "action_id": "B5_NAV", "role": "Creator", "title": "Creator nhận việc [Tuần 3 - Bài trọng điểm]", "stage": "GĐ 2: Công việc & Subtask", "fr_code": "FR 3.6.3 - 3.6.4", "kind": "nav", "hint": "Xem tiến độ Subtask Nghiên cứu & Key Visual đã hoàn tất sẵn."},
    {"step_code": "B5", "sub_code": "B5.2", "action_id": "B5_NAV_VIDEO", "role": "Creator", "title": "Video ngắn Reels/TikTok #3 Tuần 3 (/editor)", "stage": "GĐ 2: Công việc & Subtask", "fr_code": "FR 3.6.11", "kind": "nav", "hint": "Xem kịch bản, quay, dựng, caption & kênh đăng video recap."},
    {"step_code": "B5", "sub_code": "B5.3", "action_id": "B5_NAV_KOL", "role": "Creator", "title": "Booking KOL Duy Luân & Schannel (/kol)", "stage": "GĐ 2: Công việc & Subtask", "fr_code": "FR 3.6.31", "kind": "nav", "hint": "Xem shortlist, chi phí, brief & nghiệm thu số liệu KOL."},
    {"step_code": "B6", "sub_code": "B6.1", "action_id": "B6_NAV_EDITOR", "role": "Creator", "title": "Trình soạn thảo hợp nhất (/editor) — 4 khối độc lập", "stage": "GĐ 3: /editor, Ảnh & AI", "fr_code": "FR 3.6.11", "kind": "nav", "hint": "Giới thiệu 4 phần độc lập: BRIEF, MEDIA, CHANNELS, CAPTION."},
    {"step_code": "B6", "sub_code": "B6.2", "action_id": "B6_PUSH_KEY_VISUAL", "role": "Creator", "title": "Bắn ảnh Key Visual Gemini lên bài viết & Preview", "stage": "GĐ 3: /editor, Ảnh & AI", "fr_code": "FR 3.6.25", "kind": "fill", "hint": "Gắn trực tiếp ảnh Key Visual Gemini vào bài & xem preview 4 kênh."},
    {"step_code": "B6", "sub_code": "B6.3", "action_id": "B6_TOGGLE_DOCS_MODE", "role": "Creator", "title": "Chuyển đổi Chế độ Nhanh / Chế độ Tài liệu", "stage": "GĐ 3: /editor, Ảnh & AI", "fr_code": "FR 3.6.11", "kind": "toggle", "hint": "Chuyển qua lại giữa Quick Mode và Docs Mode trên thanh công cụ."},
    {"step_code": "B6", "sub_code": "B6.4", "action_id": "B6_SEQ_FILL_AI", "role": "Creator", "title": "Điền tuần tự 5 trường AI Tạo Caption (Gemini)", "stage": "GĐ 3: /editor, Ảnh & AI", "fr_code": "FR 3.7.1 - 3.7.2", "kind": "fill", "hint": "Bấm 'Tạo gợi ý' trên hộp thoại AI để gọi Gemini sinh nội dung."},
    {"step_code": "B7", "sub_code": "B7.1", "action_id": "B7_FILL_VIOLATION", "role": "Creator", "title": "Kiểm thử Bộ lọc Kiểm tra vi phạm (FR 3.6.33)", "stage": "GĐ 3: /editor, Ảnh & AI", "fr_code": "FR 3.6.33", "kind": "fill", "hint": "Nhấn nút 'Kiểm tra vi phạm' trên Chrome để thấy cảnh báo từ cấm."},
    {"step_code": "B7", "sub_code": "B7.2", "action_id": "B7_CLEAN_AND_RESTORE", "role": "Creator", "title": "Khôi phục bản thảo sạch v1 & Gửi duyệt CAPTION", "stage": "GĐ 3: /editor, Ảnh & AI", "fr_code": "FR 3.6.18", "kind": "fill", "hint": "Nhấn 'Lưu thay đổi' rồi 'Gửi duyệt' trên khung POST.CAPTION."},
    {"step_code": "B8", "sub_code": "B8", "action_id": "B8_NAV_MANAGER_APPROVAL", "role": "Manager", "title": "Manager duyệt nội bộ phần Nội dung bài đăng (v1)", "stage": "GĐ 4: Duyệt 2 tầng & Diff", "fr_code": "FR 3.6.19", "kind": "nav", "hint": "Trên Chrome Manager, bấm 'Duyệt' ở thẻ POST.CAPTION để đẩy sang Client."},
    {"step_code": "B9", "sub_code": "B9.1", "action_id": "B9_NAV_CLIENT_APPROVAL", "role": "Client", "title": "Ban Tuyển sinh ĐH FPT nghiệm thu bản thảo v1", "stage": "GĐ 4: Duyệt 2 tầng & Diff", "fr_code": "FR 3.6.20", "kind": "nav", "hint": "Client chỉ thấy phần đầu ra OUTPUT, ẩn ghi chú nội bộ BRIEF."},
    {"step_code": "B9", "sub_code": "B9.2", "action_id": "B9_SEQ_FILL_REJECT_REASON", "role": "Client", "title": "Client yêu cầu bổ sung Học bổng 2027 & OJT", "stage": "GĐ 4: Duyệt 2 tầng & Diff", "fr_code": "FR 3.6.21", "kind": "fill", "hint": "Bấm xác nhận 'Yêu cầu chỉnh sửa' để trả riêng phần CAPTION về Creator."},
    {"step_code": "B10", "sub_code": "B10.1", "action_id": "B10_NAV_CREATOR_FIX", "role": "Creator", "title": "Creator xem góp ý & mở lại /editor sửa bản v2", "stage": "GĐ 4: Duyệt 2 tầng & Diff", "fr_code": "FR 3.6.11", "kind": "nav", "hint": "Xem góp ý của nhà trường hiển thị trực tiếp trên khung CAPTION."},
    {"step_code": "B10", "sub_code": "B10.2", "action_id": "B10_SEQ_FILL_V2", "role": "Creator", "title": "Bổ sung Học bổng 50%-100% & OJT (Bản thảo v2)", "stage": "GĐ 4: Duyệt 2 tầng & Diff", "fr_code": "FR 3.6.18", "kind": "fill", "hint": "Nhấn 'Lưu thay đổi' rồi 'Gửi duyệt' bản thảo v2 trên Chrome."},
    {"step_code": "B10", "sub_code": "B10.3", "action_id": "B10_OPEN_VERSION_DIFF", "role": "Creator", "title": "Mở Lịch sử phiên bản (Đối chiếu Diff v1 vs v2)", "stage": "GĐ 4: Duyệt 2 tầng & Diff", "fr_code": "FR 3.6.11", "kind": "toggle", "hint": "Đối chiếu từng dòng nội dung vừa thêm mới giữa bản v1 và v2."},
    {"step_code": "B11", "sub_code": "B11.1", "action_id": "B11_NAV_MANAGER_V2", "role": "Manager", "title": "Manager duyệt nội bộ bản cập nhật v2", "stage": "GĐ 4: Duyệt 2 tầng & Diff", "fr_code": "FR 3.6.19", "kind": "nav", "hint": "Trên Chrome Manager, bấm 'Duyệt' bản cập nhật v2."},
    {"step_code": "B11", "sub_code": "B11.2", "action_id": "B11_NAV_CLIENT_V2", "role": "Client", "title": "Ban Tuyển sinh ĐH FPT duyệt xuất bản chính thức (v2)", "stage": "GĐ 4: Duyệt 2 tầng & Diff", "fr_code": "FR 3.6.20", "kind": "nav", "hint": "Bấm 'Duyệt' trên Chrome Client -> Task tự đóng FINISHED, Post mở APPROVED."},
    {"step_code": "B12", "sub_code": "B12.1", "action_id": "B12_NAV_SOCIAL", "role": "Manager", "title": "Kết nối 4 Nền tảng: Facebook, Instagram, TikTok, Threads", "stage": "GĐ 5: Xuất bản, SePay & Admin", "fr_code": "FR 3.8.1 - 3.8.5", "kind": "nav", "hint": "Xem 4 kết nối OAuth chính thức của chiến dịch Đại học FPT 2027."},
    {"step_code": "B12", "sub_code": "B12.2", "action_id": "B12_NAV_HASHTAGS", "role": "Manager", "title": "Bộ 12 Hashtag Chiến dịch Tuyển sinh 2027", "stage": "GĐ 5: Xuất bản, SePay & Admin", "fr_code": "FR 3.6.34", "kind": "nav", "hint": "Xem bộ Hashtag chuẩn tái sử dụng nhất quán trên 4 nền tảng."},
    {"step_code": "B12", "sub_code": "B12.3", "action_id": "B12_NAV_MAIL_TEMPLATES", "role": "Manager", "title": "Mẫu Email mời học sinh lớp 12 dự Workshop THPT", "stage": "GĐ 5: Xuất bản, SePay & Admin", "fr_code": "FR 3.4.23", "kind": "nav", "hint": "Xem mẫu Email Block-Builder gửi vé mời Workshop THPT."},
    {"step_code": "B12", "sub_code": "B12.4", "action_id": "B12_NAV_MAIL_BATCHES", "role": "Manager", "title": "Lịch sử Lô gửi Email Workshop & Báo cáo Tuần", "stage": "GĐ 5: Xuất bản, SePay & Admin", "fr_code": "FR 3.4.23", "kind": "nav", "hint": "Xem 2 đợt gửi email hoàn tất trong chiến dịch."},
    {"step_code": "B12", "sub_code": "B12.5", "action_id": "B12_NAV_NEWSLETTER", "role": "Creator", "title": "Bản tin Email Cẩm nang ngành học 2027 (/newsletter)", "stage": "GĐ 5: Xuất bản, SePay & Admin", "fr_code": "FR 3.6.35", "kind": "nav", "hint": "Xem trình thiết kế bản tin email kéo-thả & lịch gửi."},
    {"step_code": "B13", "sub_code": "B13.1", "action_id": "B13_NAV_PUBLISH", "role": "Creator", "title": "Bảng điều phối Xuất bản Đa nền tảng (4 Tuần)", "stage": "GĐ 5: Xuất bản, SePay & Admin", "fr_code": "FR 3.8.8 - 3.8.12", "kind": "nav", "hint": "Xem danh sách bài đã đăng, vừa duyệt và bài hẹn giờ Tuần 4."},
    {"step_code": "B13", "sub_code": "B13.2", "action_id": "B13_NAV_CALENDAR", "role": "Creator", "title": "Lịch xuất bản Chiến dịch 4 Tuần (/calendar)", "stage": "GĐ 5: Xuất bản, SePay & Admin", "fr_code": "FR 3.8.13", "kind": "nav", "hint": "Xem mật độ phủ sóng 4 tuần trên Facebook, Instagram, TikTok, Threads."},
    {"step_code": "B13", "sub_code": "B13.3", "action_id": "B13_NAV_DASHBOARD", "role": "Creator", "title": "Dashboard Phân tích Tương tác (/dashboard)", "stage": "GĐ 5: Xuất bản, SePay & Admin", "fr_code": "FR 3.8.14 - 3.8.15", "kind": "nav", "hint": "Xem biểu đồ Reach, Impressions và Reactions đổ về thời gian thực."},
    {"step_code": "B13", "sub_code": "B13.4", "action_id": "B13_NAV_PRESS", "role": "Creator", "title": "Tuyến bài Báo chí VnExpress Giáo dục (/press)", "stage": "GĐ 5: Xuất bản, SePay & Admin", "fr_code": "FR 3.6.31", "kind": "nav", "hint": "Xem thông cáo báo chí, danh sách phóng viên & link tin bài."},
    {"step_code": "B14", "sub_code": "B14.1", "action_id": "B14_NAV_PLANS", "role": "Owner", "title": "Nâng cấp gói cước Agency qua SePay (VietQR)", "stage": "GĐ 5: Xuất bản, SePay & Admin", "fr_code": "FR 3.9.1 - 3.9.4", "kind": "nav", "hint": "Bấm 'Nâng cấp' trên Chrome Owner để sinh mã VietQR động qua SePay."},
    {"step_code": "B14", "sub_code": "B14.2", "action_id": "B14_NAV_CREDITS", "role": "Owner", "title": "Ví AI Credit SE08 Digital Agency (8.500 điểm)", "stage": "GĐ 5: Xuất bản, SePay & Admin", "fr_code": "FR 3.9.5 - 3.9.6", "kind": "nav", "hint": "Xem số dư 8.500 credits và hạn mức cấp cho Workspace ĐH FPT."},
    {"step_code": "B15", "sub_code": "B15.1", "action_id": "B15_NAV_ADMIN_REVENUE", "role": "Admin", "title": "Admin giám sát Doanh thu & Gói cước toàn nền tảng", "stage": "GĐ 5: Xuất bản, SePay & Admin", "fr_code": "FR 3.10.1 - 3.10.3", "kind": "nav", "hint": "Xem biểu đồ doanh thu gói SaaS & giao dịch đối soát SePay."},
    {"step_code": "B15", "sub_code": "B15.2", "action_id": "B15_NAV_ADMIN_MODERATION", "role": "Admin", "title": "Admin Hàng đợi kiểm duyệt nội dung (FR 3.10.4)", "stage": "GĐ 5: Xuất bản, SePay & Admin", "fr_code": "FR 3.10.4", "kind": "nav", "hint": "Xem 3 bản ghi cảnh báo kiểm duyệt cộng đồng — khép lại demo."},
]

QA_TIMELINE: list[dict[str, str]] = [
    {"action_id": "QA_PUBLIC_PACKAGE", "role": "Guest", "title": "Link Chào giá Gói công khai (Guest)", "route": "/packages/share/goi-tuyen-sinh-dh-fpt-2027"},
    {"action_id": "QA_PUBLIC_SURVEY", "role": "Guest", "title": "Biểu mẫu Khảo sát THPT công khai (Guest)", "route": "/public/surveys/khao-sat-chon-nganh-fptu-2027"},
    {"action_id": "QA_AI_TRENDS", "role": "Manager", "title": "AI Studio: Xu hướng MXH (Redis Live)", "route": "/ai-studio/trends"},
    {"action_id": "QA_AI_RAG", "role": "Manager", "title": "AI Studio: Kho Tri thức RAG ĐH FPT", "route": "/ai-studio/knowledge-base"},
    {"action_id": "QA_AI_AMBASSADORS", "role": "Creator", "title": "AI Studio: Đại sứ ảo Khóa K23", "route": "/ai-studio/ambassadors"},
    {"action_id": "QA_CLIENT_PORTAL", "role": "Client", "title": "Cổng Nghiệm thu Khách hàng (/portal)", "route": "/workspaces/{ws}/portal"},
    {"action_id": "QA_CLIENT_VAULT", "role": "Client", "title": "Kho Lưu trữ Riêng Client Vault", "route": "/workspaces/{ws}/library"},
    {"action_id": "QA_COLLABORATORS", "role": "Owner", "title": "Danh bạ 10 Đối tác Báo chí & KOL", "route": "/agency/{ag}/collaborators"},
    {"action_id": "QA_EVENT_EDITOR", "role": "Creator", "title": "Kế hoạch Sự kiện FPTU Open Day", "route": "/event"},
    {"action_id": "QA_WORKSHOP_EDITOR", "role": "Creator", "title": "Điều phối Chuỗi Workshop THPT", "route": "/workshop"},
    {"action_id": "QA_PRESS_EDITOR", "role": "Creator", "title": "Thông cáo Báo chí VnExpress", "route": "/press"},
    {"action_id": "QA_KOL_EDITOR", "role": "Creator", "title": "Booking KOL Duy Luân & Schannel", "route": "/kol"},
    {"action_id": "QA_NEWSLETTER_EDITOR", "role": "Creator", "title": "Thiết kế Bản tin Email Khối", "route": "/newsletter"},
    {"action_id": "QA_VIDEO_EDITOR", "role": "Creator", "title": "Video ngắn Reels/TikTok Recap", "route": "/editor"},
    {"action_id": "QA_ADMIN_CREDIT_PRICES", "role": "Admin", "title": "Bảng giá Tín dụng AI toàn hệ thống", "route": "/admin/credit-prices"},
]

TIMELINE_INDEX_BY_ACTION: dict[str, int] = {
    item["action_id"]: idx for idx, item in enumerate(DEMO_TIMELINE)
}
TIMELINE_INDEX_BY_ACTION["B3_NAV"] = TIMELINE_INDEX_BY_ACTION["B3_STEP_INFO"]
QA_ITEM_BY_ACTION: dict[str, dict[str, str]] = {
    item["action_id"]: item for item in QA_TIMELINE
}


# ==============================================================================
# 1.6. PURE-STDLIB RFC 6455 WEBSOCKET HUB (ĐỒNG BỘ TỨC THÌ 6 CỬA SỔ CHROME)
# ==============================================================================
_WS_GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"


def _ws_encode_frame(payload: bytes, opcode: int = 0x1) -> bytes:
    header = bytearray()
    header.append(0x80 | (opcode & 0x0F))
    length = len(payload)
    if length < 126:
        header.append(length)
    elif length < 65536:
        header.append(126)
        header.extend(struct.pack("!H", length))
    else:
        header.append(127)
        header.extend(struct.pack("!Q", length))
    return bytes(header) + payload


def _ws_recv_exact(sock: socket.socket, n: int) -> bytes | None:
    buf = bytearray()
    while len(buf) < n:
        try:
            chunk = sock.recv(n - len(buf))
        except (OSError, TimeoutError):
            return None
        if not chunk:
            return None
        buf.extend(chunk)
    return bytes(buf)


def _ws_read_frame(sock: socket.socket) -> tuple[int, bytes] | None:
    """Đọc trọn vẹn 1 thông điệp WebSocket (hỗ trợ ghép fragment theo RFC 6455)."""
    fragments = bytearray()
    msg_opcode: int | None = None
    while True:
        hdr = _ws_recv_exact(sock, 2)
        if hdr is None:
            return None
        b0, b1 = hdr[0], hdr[1]
        fin = (b0 & 0x80) != 0
        opcode = b0 & 0x0F
        masked = (b1 & 0x80) != 0
        length = b1 & 0x7F

        if length == 126:
            ext = _ws_recv_exact(sock, 2)
            if ext is None:
                return None
            length = struct.unpack("!H", ext)[0]
        elif length == 127:
            ext = _ws_recv_exact(sock, 8)
            if ext is None:
                return None
            length = struct.unpack("!Q", ext)[0]

        if length > 4 * 1024 * 1024:
            return None

        mask_key = _ws_recv_exact(sock, 4) if masked else b""
        if masked and mask_key is None:
            return None

        data = _ws_recv_exact(sock, length) if length > 0 else b""
        if data is None:
            return None

        if masked and data:
            data = bytes(b ^ mask_key[i & 3] for i, b in enumerate(data))

        # Control frames (Close / Ping / Pong) không bị phân mảnh
        if opcode >= 0x8:
            return (opcode, data)

        if msg_opcode is None:
            msg_opcode = opcode
        fragments.extend(data)
        if fin:
            return (msg_opcode, bytes(fragments))


class WSClient:
    def __init__(self, sock: socket.socket, client_id: str) -> None:
        self.sock = sock
        self.client_id = client_id
        self.window_role: str = ""
        self.send_lock = threading.Lock()
        self.closed = False

    def send_raw(self, frame: bytes) -> bool:
        if self.closed:
            return False
        with self.send_lock:
            if self.closed:
                return False
            try:
                self.sock.sendall(frame)
                return True
            except OSError:
                self.closed = True
                return False

    def send_json(self, data: dict[str, Any]) -> bool:
        raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
        return self.send_raw(_ws_encode_frame(raw, opcode=0x1))


class WebSocketHub:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._clients: dict[str, WSClient] = {}

    def register(self, sock: socket.socket) -> WSClient:
        cid = uuid.uuid4().hex[:10]
        client = WSClient(sock, cid)
        with self._lock:
            self._clients[cid] = client
        return client

    def unregister(self, client: WSClient) -> None:
        client.closed = True
        with self._lock:
            self._clients.pop(client.client_id, None)

    def set_role(self, client: WSClient, role: str) -> None:
        with self._lock:
            client.window_role = role

    def client_count(self) -> int:
        with self._lock:
            return len(self._clients)

    def connected_roles(self) -> list[str]:
        with self._lock:
            return sorted({c.window_role for c in self._clients.values() if c.window_role})

    def broadcast(self, data: dict[str, Any]) -> int:
        raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
        frame = _ws_encode_frame(raw, opcode=0x1)
        with self._lock:
            clients = list(self._clients.values())
        sent = 0
        dead: list[WSClient] = []
        for client in clients:
            if client.send_raw(frame):
                sent += 1
            else:
                dead.append(client)
        if dead:
            with self._lock:
                for c in dead:
                    self._clients.pop(c.client_id, None)
        return sent


# ==============================================================================
# 1.7. WIN32 WINDOW RAISER (ĐƯA ĐÚNG CỬA SỔ CHROME LÊN TRÊN CÙNG KHI CHIẾU TV)
# ==============================================================================
def _win32_list_chrome_hwnds() -> set[int]:
    if sys.platform != "win32":
        return set()
    hwnds: set[int] = set()
    try:
        user32 = ctypes.windll.user32
        WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)

        def callback(hwnd, _lparam):
            if user32.IsWindowVisible(hwnd):
                cls = ctypes.create_unicode_buffer(128)
                user32.GetClassNameW(hwnd, cls, 128)
                if cls.value == "Chrome_WidgetWin_1":
                    hwnds.add(int(hwnd))
            return True

        user32.EnumWindows(WNDENUMPROC(callback), 0)
    except Exception:
        pass
    return hwnds


def _win32_find_hwnd_by_title_marker(marker: str) -> int | None:
    if sys.platform != "win32" or not marker:
        return None
    found: list[int] = []
    try:
        user32 = ctypes.windll.user32
        WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)

        def callback(hwnd, _lparam):
            if user32.IsWindowVisible(hwnd):
                length = user32.GetWindowTextLengthW(hwnd)
                if length > 0:
                    buf = ctypes.create_unicode_buffer(length + 2)
                    user32.GetWindowTextW(hwnd, buf, length + 2)
                    if marker in buf.value:
                        found.append(int(hwnd))
                        return False
            return True

        user32.EnumWindows(WNDENUMPROC(callback), 0)
    except Exception:
        pass
    return found[0] if found else None


def _win32_raise_hwnd(hwnd: int | None) -> bool:
    if sys.platform != "win32" or not hwnd:
        return False
    try:
        user32 = ctypes.windll.user32
        if not user32.IsWindow(hwnd):
            return False
        SW_RESTORE = 9
        SW_SHOW = 5
        HWND_TOPMOST = -1
        HWND_NOTOPMOST = -2
        SWP_NOMOVE = 0x0002
        SWP_NOSIZE = 0x0001
        SWP_SHOWWINDOW = 0x0040

        if user32.IsIconic(hwnd):
            user32.ShowWindow(hwnd, SW_RESTORE)
        else:
            user32.ShowWindow(hwnd, SW_SHOW)

        fg_hwnd = user32.GetForegroundWindow()
        fg_tid = user32.GetWindowThreadProcessId(fg_hwnd, None) if fg_hwnd else 0
        target_tid = user32.GetWindowThreadProcessId(hwnd, None)
        attached = False
        if fg_tid and target_tid and fg_tid != target_tid:
            attached = bool(user32.AttachThreadInput(fg_tid, target_tid, True))
        try:
            user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW)
            user32.SetWindowPos(hwnd, HWND_NOTOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW)
            user32.BringWindowToTop(hwnd)
            user32.SetForegroundWindow(hwnd)
        finally:
            if attached:
                user32.AttachThreadInput(fg_tid, target_tid, False)
        return True
    except Exception:
        return False


# ==============================================================================
# 1.8. FLOATING BOTTOM-LEFT HUD COMPONENT (SHADOW DOM + WEBSOCKET SYNC)
# ==============================================================================
_HUD_JS_TEMPLATE = r"""
(function() {
  try {
    var WINDOW_ROLE = __WINDOW_ROLE__;
    var WINDOW_NAME = __WINDOW_NAME__;
    var WINDOW_EMAIL = __WINDOW_EMAIL__;
    var MONITOR_PORT = __MONITOR_PORT__;
    var WS_URL = 'ws://127.0.0.1:' + MONITOR_PORT + '/ws';
    var HTTP_BASE = 'http://127.0.0.1:' + MONITOR_PORT;

    if (!/^(https?|file):$/i.test(window.location.protocol)) return;

    if (window.__BH_DEMO_HUD_V2__) {
      window.__BH_DEMO_HUD_V2__.updateIdentity(WINDOW_ROLE, WINDOW_NAME, WINDOW_EMAIL);
      window.__BH_DEMO_HUD_V2__.ensureMounted();
      return;
    }

    var safeGet = function(k, fallback) {
      try { var v = window.localStorage.getItem(k); return v === null ? fallback : v; } catch (e) { return fallback; }
    };
    var safeSet = function(k, v) {
      try { window.localStorage.setItem(k, v); } catch (e) {}
    };

    var ROLE_ORDER = ['Guest', 'Owner', 'Manager', 'Creator', 'Client', 'Admin'];

    var state = {
      connected: false,
      collapsed: safeGet('bh-demo-hud-collapsed', '0') === '1',
      drawerOpen: false,
      drawerTab: 'steps',
      windowRole: WINDOW_ROLE,
      windowName: WINDOW_NAME,
      windowEmail: WINDOW_EMAIL,
      sync: null,
      pos: null,
      localBusy: false
    };

    try {
      var savedPos = safeGet('bh-demo-hud-pos', '');
      if (savedPos) {
        var parsedPos = JSON.parse(savedPos);
        if (parsedPos && typeof parsedPos.left === 'number' && typeof parsedPos.bottom === 'number') {
          state.pos = parsedPos;
        }
      }
    } catch (e) {}

    var host = null;
    var shadow = null;
    var ws = null;
    var reconnectTimer = null;
    var pingTimer = null;
    var reconnectDelay = 600;
    var dragging = null;

    var esc = function(s) {
      return String(s == null ? '' : s)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
    };

    var isDarkPage = function() {
      try {
        return document.documentElement.classList.contains('dark') ||
          document.documentElement.getAttribute('data-theme') === 'dark';
      } catch (e) { return false; }
    };

    var STYLE_CSS = [
      ':host { all: initial; position: fixed !important; left: 14px; bottom: 14px; z-index: 2147483647 !important; pointer-events: auto !important; font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important; }',
      '*, *::before, *::after { box-sizing: border-box; border-radius: 0 !important; }',
      '.hud-wrap { position: relative; display: flex; flex-direction: column; align-items: flex-start; gap: 6px; color: #0F172A; font-size: 12px; line-height: 1.3; user-select: none; }',
      '.hud-wrap.dark { color: #F8FAFC; }',
      '.hud-bar { position: relative; display: flex; align-items: center; gap: 8px; background: rgba(255,255,255,0.97); border: 1px solid #CBD5E1; box-shadow: 0 10px 28px rgba(15,23,42,0.16); padding: 6px 8px; max-width: min(760px, calc(100vw - 28px)); backdrop-filter: blur(10px); }',
      '.hud-wrap.dark .hud-bar { background: rgba(18,18,21,0.97); border-color: #3F3F46; box-shadow: 0 10px 30px rgba(0,0,0,0.45); }',
      '.hud-progress { position: absolute; top: 0; left: 0; right: 0; height: 2px; background: #F1F5F9; overflow: hidden; }',
      '.hud-wrap.dark .hud-progress { background: #27272A; }',
      '.hud-progress-fill { height: 100%; background: #ea6c3b; transition: width 180ms ease; }',
      '.hud-drag { display: inline-flex; align-items: center; gap: 6px; cursor: grab; padding: 2px 2px 2px 0; }',
      '.hud-drag:active { cursor: grabbing; }',
      '.hud-dot { width: 8px; height: 8px; flex-shrink: 0; background: #F59E0B; }',
      '.hud-dot.ok { background: #10B981; }',
      '.hud-role-badge { background: #ea6c3b; color: #FFFFFF; font-weight: 800; font-size: 10px; letter-spacing: 0.05em; text-transform: uppercase; padding: 3px 7px; flex-shrink: 0; }',
      '.hud-role-name { font-weight: 700; font-size: 12px; color: #0F172A; white-space: nowrap; max-width: 145px; overflow: hidden; text-overflow: ellipsis; }',
      '.hud-wrap.dark .hud-role-name { color: #F8FAFC; }',
      '.hud-sep { width: 1px; height: 20px; background: #E2E8F0; flex-shrink: 0; }',
      '.hud-wrap.dark .hud-sep { background: #27272A; }',
      '.hud-case { display: flex; align-items: center; gap: 6px; min-width: 0; flex: 1; }',
      '.hud-code { font-family: "Geist Mono", ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 11px; font-weight: 800; background: #FFFAF5; color: #C2410C; border: 1px solid #FDBA74; padding: 2px 6px; flex-shrink: 0; }',
      '.hud-wrap.dark .hud-code { background: rgba(234,108,59,0.16); color: #FDBA74; border-color: rgba(234,108,59,0.45); }',
      '.hud-title { font-weight: 600; font-size: 12px; color: #1E293B; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 270px; }',
      '.hud-wrap.dark .hud-title { color: #E2E8F0; }',
      '.hud-counter { font-family: "Geist Mono", ui-monospace, monospace; font-variant-numeric: tabular-nums; font-size: 11px; font-weight: 700; color: #475569; flex-shrink: 0; }',
      '.hud-wrap.dark .hud-counter { color: #94A3B8; }',
      '.hud-jump-role { display: inline-flex; align-items: center; gap: 4px; background: #FFF7ED; color: #9A3412; border: 1px solid #FDBA74; padding: 2px 7px; font-size: 11px; font-weight: 700; cursor: pointer; flex-shrink: 0; min-height: 26px; }',
      '.hud-jump-role:hover { background: #FFEDD5; }',
      '.hud-wrap.dark .hud-jump-role { background: rgba(234,108,59,0.2); color: #FED7AA; border-color: rgba(234,108,59,0.5); }',
      '.hud-actions { display: inline-flex; align-items: center; gap: 4px; flex-shrink: 0; }',
      '.hud-btn { display: inline-flex; align-items: center; justify-content: center; gap: 4px; min-width: 28px; min-height: 28px; padding: 0 8px; border: 1px solid #CBD5E1; background: #FFFFFF; color: #0F172A; font-family: inherit; font-size: 11px; font-weight: 700; cursor: pointer; transition: background 120ms ease, border-color 120ms ease, color 120ms ease; }',
      '.hud-btn:hover:not(:disabled) { background: #F8FAFC; border-color: #94A3B8; }',
      '.hud-btn:disabled { opacity: 0.42; cursor: not-allowed; }',
      '.hud-btn:focus-visible { outline: none; box-shadow: 0 0 0 2px #FFFFFF, 0 0 0 4px #ea6c3b; }',
      '.hud-wrap.dark .hud-btn { background: #18181B; border-color: #3F3F46; color: #F8FAFC; }',
      '.hud-wrap.dark .hud-btn:hover:not(:disabled) { background: #27272A; border-color: #71717A; }',
      '.hud-wrap.dark .hud-btn:focus-visible { box-shadow: 0 0 0 2px #09090B, 0 0 0 4px #ea6c3b; }',
      '.hud-btn-primary { background: #ea6c3b; border-color: #ea6c3b; color: #FFFFFF; padding: 0 10px; }',
      '.hud-btn-primary:hover:not(:disabled) { background: #d95d2c; border-color: #d95d2c; }',
      '.hud-wrap.dark .hud-btn-primary { background: #ea6c3b; border-color: #ea6c3b; color: #FFFFFF; }',
      '.hud-wrap.dark .hud-btn-primary:hover:not(:disabled) { background: #d95d2c; border-color: #d95d2c; }',
      '.hud-btn-icon { padding: 0; width: 28px; }',
      '.hud-btn-active { background: #FFFAF5; border-color: #ea6c3b; color: #C2410C; }',
      '.hud-wrap.dark .hud-btn-active { background: rgba(234,108,59,0.2); border-color: #ea6c3b; color: #FDBA74; }',
      '.hud-drawer { width: min(520px, calc(100vw - 28px)); max-height: 62vh; display: flex; flex-direction: column; background: rgba(255,255,255,0.99); border: 1px solid #CBD5E1; box-shadow: 0 16px 40px rgba(15,23,42,0.2); overflow: hidden; }',
      '.hud-wrap.dark .hud-drawer { background: rgba(18,18,21,0.99); border-color: #3F3F46; box-shadow: 0 16px 42px rgba(0,0,0,0.55); }',
      '.hud-drawer-head { padding: 10px 12px; border-bottom: 1px solid #E2E8F0; background: #F8FAFC; display: flex; flex-direction: column; gap: 8px; }',
      '.hud-wrap.dark .hud-drawer-head { background: #18181B; border-color: #27272A; }',
      '.hud-drawer-top { display: flex; align-items: center; justify-content: space-between; gap: 8px; }',
      '.hud-drawer-title { font-size: 12px; font-weight: 800; color: #0F172A; }',
      '.hud-wrap.dark .hud-drawer-title { color: #F8FAFC; }',
      '.hud-socket-pill { font-size: 11px; font-weight: 600; color: #047857; background: #ECFDF5; border: 1px solid #A7F3D0; padding: 2px 7px; }',
      '.hud-socket-pill.off { color: #B45309; background: #FFFBEB; border-color: #FDE68A; }',
      '.hud-roles-grid { display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 4px; }',
      '.hud-role-btn { display: inline-flex; align-items: center; justify-content: center; gap: 4px; min-height: 28px; padding: 0 4px; border: 1px solid #CBD5E1; background: #FFFFFF; color: #0F172A; font-size: 11px; font-weight: 700; cursor: pointer; }',
      '.hud-role-btn:hover { border-color: #ea6c3b; background: #FFFAF5; }',
      '.hud-role-btn.current { background: #ea6c3b; border-color: #ea6c3b; color: #FFFFFF; }',
      '.hud-wrap.dark .hud-role-btn { background: #121215; border-color: #3F3F46; color: #E2E8F0; }',
      '.hud-wrap.dark .hud-role-btn.current { background: #ea6c3b; border-color: #ea6c3b; color: #FFFFFF; }',
      '.hud-role-dot { width: 6px; height: 6px; background: #CBD5E1; flex-shrink: 0; }',
      '.hud-role-dot.alive { background: #10B981; }',
      '.hud-role-btn.current .hud-role-dot.alive { background: #FFFFFF; }',
      '.hud-drawer-controls { display: flex; align-items: center; justify-content: space-between; gap: 6px; flex-wrap: wrap; }',
      '.hud-tabs { display: inline-flex; border: 1px solid #CBD5E1; }',
      '.hud-wrap.dark .hud-tabs { border-color: #3F3F46; }',
      '.hud-tab { min-height: 26px; padding: 0 10px; border: none; background: #FFFFFF; color: #475569; font-size: 11px; font-weight: 700; cursor: pointer; }',
      '.hud-tab.active { background: #0F172A; color: #FFFFFF; }',
      '.hud-wrap.dark .hud-tab { background: #121215; color: #94A3B8; }',
      '.hud-wrap.dark .hud-tab.active { background: #ea6c3b; color: #FFFFFF; }',
      '.hud-drawer-list { overflow-y: auto; flex: 1; padding: 4px; display: flex; flex-direction: column; gap: 2px; }',
      '.hud-item { display: flex; align-items: center; gap: 8px; width: 100%; text-align: left; padding: 7px 8px; border: 1px solid transparent; background: transparent; color: inherit; cursor: pointer; font-family: inherit; }',
      '.hud-item:hover { background: #F8FAFC; border-color: #E2E8F0; }',
      '.hud-item.active { background: #FFFAF5; border-color: #FDBA74; }',
      '.hud-wrap.dark .hud-item:hover { background: #1F1F23; border-color: #3F3F46; }',
      '.hud-wrap.dark .hud-item.active { background: rgba(234,108,59,0.16); border-color: rgba(234,108,59,0.5); }',
      '.hud-item-code { font-family: "Geist Mono", ui-monospace, monospace; font-size: 11px; font-weight: 800; color: #C2410C; min-width: 44px; flex-shrink: 0; }',
      '.hud-wrap.dark .hud-item-code { color: #FDBA74; }',
      '.hud-item-role { font-size: 10px; font-weight: 800; text-transform: uppercase; padding: 1px 5px; background: #F1F5F9; color: #334155; border: 1px solid #CBD5E1; min-width: 56px; text-align: center; flex-shrink: 0; }',
      '.hud-wrap.dark .hud-item-role { background: #27272A; color: #E2E8F0; border-color: #3F3F46; }',
      '.hud-item-title { font-size: 12px; font-weight: 600; flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }',
      '.hud-item-done { font-size: 11px; font-weight: 800; color: #10B981; flex-shrink: 0; }',
      '.hud-drawer-foot { padding: 6px 12px; border-top: 1px solid #E2E8F0; background: #F8FAFC; font-size: 11px; color: #475569; display: flex; justify-content: space-between; gap: 8px; }',
      '.hud-wrap.dark .hud-drawer-foot { background: #18181B; border-color: #27272A; color: #94A3B8; }',
      '.hud-hint-bar { padding: 4px 10px; background: #FFFAF5; border: 1px solid #FDBA74; color: #9A3412; font-size: 11px; font-weight: 600; max-width: min(760px, calc(100vw - 28px)); }',
      '.hud-wrap.dark .hud-hint-bar { background: rgba(234,108,59,0.16); border-color: rgba(234,108,59,0.45); color: #FED7AA; }',
      '@media (prefers-reduced-motion: reduce) { *, *::before, *::after { transition: none !important; animation: none !important; } }'
    ].join('\n');

    var applyHostPosition = function() {
      if (!host) return;
      if (state.pos) {
        var maxLeft = Math.max(8, window.innerWidth - 180);
        var maxBottom = Math.max(8, window.innerHeight - 48);
        var l = Math.min(Math.max(8, state.pos.left), maxLeft);
        var b = Math.min(Math.max(8, state.pos.bottom), maxBottom);
        host.style.left = l + 'px';
        host.style.bottom = b + 'px';
      } else {
        host.style.left = '14px';
        host.style.bottom = '14px';
      }
    };

    var sendCommand = function(payload) {
      if (ws && ws.readyState === WebSocket.OPEN) {
        try {
          ws.send(JSON.stringify(payload));
          return;
        } catch (e) {}
      }
      // REST fallback nếu WebSocket đang tự kết nối lại
      try {
        fetch(HTTP_BASE + '/api/hud/command', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        }).then(function(r) { return r.json(); }).then(function(data) {
          if (data && data.state) {
            state.sync = data.state;
            render();
          }
        }).catch(function() {});
      } catch (e) {}
    };

    var fetchInitialState = function() {
      try {
        fetch(HTTP_BASE + '/api/hud/state')
          .then(function(r) { return r.json(); })
          .then(function(data) {
            if (data && data.type === 'state') {
              state.sync = data;
              render();
            }
          })
          .catch(function() {});
      } catch (e) {}
    };

    var connectSocket = function() {
      if (ws && (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING)) return;
      try {
        ws = new WebSocket(WS_URL);
      } catch (e) {
        scheduleReconnect();
        return;
      }
      ws.onopen = function() {
        state.connected = true;
        reconnectDelay = 600;
        try {
          ws.send(JSON.stringify({ type: 'hello', window_role: state.windowRole }));
        } catch (e) {}
        if (pingTimer) clearInterval(pingTimer);
        pingTimer = setInterval(function() {
          if (ws && ws.readyState === WebSocket.OPEN) {
            try { ws.send(JSON.stringify({ type: 'ping' })); } catch (e) {}
          }
        }, 15000);
        render();
      };
      ws.onmessage = function(ev) {
        try {
          var msg = JSON.parse(ev.data);
          if (msg && msg.type === 'state') {
            state.sync = msg;
            state.localBusy = false;
            render();
          }
        } catch (e) {}
      };
      ws.onclose = function() {
        state.connected = false;
        if (pingTimer) { clearInterval(pingTimer); pingTimer = null; }
        render();
        scheduleReconnect();
      };
      ws.onerror = function() {
        try { ws.close(); } catch (e) {}
      };
    };

    var scheduleReconnect = function() {
      if (reconnectTimer) return;
      reconnectTimer = setTimeout(function() {
        reconnectTimer = null;
        reconnectDelay = Math.min(2500, Math.round(reconnectDelay * 1.4));
        connectSocket();
      }, reconnectDelay);
    };

    var render = function() {
      if (!shadow) return;
      var sync = state.sync;
      var cur = sync && sync.current ? sync.current : {
        index: 0,
        step_code: 'B0',
        sub_code: 'B0',
        role: state.windowRole,
        title: 'Sẵn sàng thuyết trình BrandHub',
        hint: ''
      };
      var total = sync && sync.total ? sync.total : 1;
      var idx = typeof cur.index === 'number' ? cur.index : 0;
      var autoExec = sync ? Boolean(sync.auto_execute) : true;
      var connectedCount = sync && typeof sync.connected_clients === 'number' ? sync.connected_clients : (state.connected ? 1 : 0);
      var pct = total > 1 ? Math.round((idx / (total - 1)) * 100) : 0;
      var roleMismatch = cur.role && cur.role !== state.windowRole;
      var darkCls = isDarkPage() ? ' dark' : '';
      var doneMap = {};
      if (sync && Array.isArray(sync.done_actions)) {
        for (var d = 0; d < sync.done_actions.length; d++) doneMap[sync.done_actions[d]] = true;
      }

      var drawerHtml = '';
      if (state.drawerOpen && !state.collapsed) {
        var rolesHtml = '';
        for (var ri = 0; ri < ROLE_ORDER.length; ri++) {
          var rName = ROLE_ORDER[ri];
          var rAlive = sync && sync.roles && sync.roles[rName] && sync.roles[rName].alive;
          var rCur = rName === state.windowRole ? ' current' : '';
          rolesHtml += '<button type="button" class="hud-role-btn' + rCur + '" data-cmd="focus_role" data-role="' + esc(rName) + '" title="Chuyển sang cửa sổ ' + esc(rName) + ' (Alt+' + (ri + 1) + ')">'
            + '<span class="hud-role-dot' + (rAlive ? ' alive' : '') + '"></span>'
            + '<span>' + esc(rName) + '</span>'
            + '</button>';
        }

        var listHtml = '';
        if (state.drawerTab === 'steps') {
          var timeline = (sync && Array.isArray(sync.timeline)) ? sync.timeline : [];
          for (var ti = 0; ti < timeline.length; ti++) {
            var item = timeline[ti];
            var isAct = !sync.active_qa && ti === idx;
            var isDone = Boolean(doneMap[item.action_id]);
            listHtml += '<button type="button" class="hud-item' + (isAct ? ' active' : '') + '" data-cmd="goto" data-idx="' + ti + '">'
              + '<span class="hud-item-code">' + esc(item.sub_code) + '</span>'
              + '<span class="hud-item-role">' + esc(item.role) + '</span>'
              + '<span class="hud-item-title">' + esc(item.title) + '</span>'
              + (isDone ? '<span class="hud-item-done">&#10003;</span>' : '')
              + '</button>';
          }
        } else {
          var qaItems = (sync && Array.isArray(sync.qa_items)) ? sync.qa_items : [];
          for (var qi = 0; qi < qaItems.length; qi++) {
            var qa = qaItems[qi];
            var qaAct = sync && sync.active_qa && sync.active_qa.action_id === qa.action_id;
            listHtml += '<button type="button" class="hud-item' + (qaAct ? ' active' : '') + '" data-cmd="qa_action" data-action="' + esc(qa.action_id) + '">'
              + '<span class="hud-item-code">Q&amp;A</span>'
              + '<span class="hud-item-role">' + esc(qa.role) + '</span>'
              + '<span class="hud-item-title">' + esc(qa.title) + '</span>'
              + '</button>';
          }
        }

        drawerHtml = '<div class="hud-drawer">'
          + '<div class="hud-drawer-head">'
          + '<div class="hud-drawer-top">'
          + '<span class="hud-drawer-title">Điều khiển nhanh 6 cửa sổ Chrome</span>'
          + '<span class="hud-socket-pill' + (state.connected ? '' : ' off') + '">'
          + (state.connected ? ('Socket đồng bộ · ' + connectedCount + ' kết nối') : 'Đang nối lại Socket...')
          + '</span>'
          + '</div>'
          + '<div class="hud-roles-grid">' + rolesHtml + '</div>'
          + '<div class="hud-drawer-controls">'
          + '<div class="hud-tabs">'
          + '<button type="button" class="hud-tab' + (state.drawerTab === 'steps' ? ' active' : '') + '" data-tab="steps">Kịch bản (B0–B15)</button>'
          + '<button type="button" class="hud-tab' + (state.drawerTab === 'qa' ? ' active' : '') + '" data-tab="qa">Q&amp;A Hội đồng</button>'
          + '</div>'
          + '<div class="hud-actions">'
          + '<button type="button" class="hud-btn' + (autoExec ? ' hud-btn-active' : '') + '" data-cmd="toggle_auto" title="BẬT: Bấm Tiếp/Trước tự chuyển trang & đưa đúng cửa sổ Chrome lên trên. TẮT: Chỉ đổi chữ trên Banner đồng bộ 6 cửa sổ.">'
          + (autoExec ? 'Tự lái Chrome: BẬT' : 'Chỉ đổi Banner')
          + '</button>'
          + '<button type="button" class="hud-btn" data-cmd="maximize_all" title="Phóng to toàn màn hình cả 6 cửa sổ Chrome khi chiếu TV">Toàn màn hình</button>'
          + '</div>'
          + '</div>'
          + '</div>'
          + '<div class="hud-drawer-list" id="hud-drawer-list">' + listHtml + '</div>'
          + '<div class="hud-drawer-foot">'
          + '<span>Phím tắt: Alt+&#8592;/&#8594; đổi bước · Alt+R chạy lại · Alt+1..6 đổi vai trò</span>'
          + '<span>Kéo nhãn vai trò để di chuyển · Nhấp đúp để đặt lại góc trái</span>'
          + '</div>'
          + '</div>';
      }

      var barInner = '';
      if (state.collapsed) {
        barInner = '<div class="hud-drag" id="hud-drag-handle" title="Kéo để di chuyển · Nhấp đúp để đặt lại góc trái dưới">'
          + '<span class="hud-dot' + (state.connected ? ' ok' : '') + '" title="' + (state.connected ? 'WebSocket đã đồng bộ' : 'Đang kết nối lại WebSocket') + '"></span>'
          + '<span class="hud-role-badge">' + esc(state.windowRole) + '</span>'
          + '</div>'
          + '<span class="hud-code" title="' + esc(cur.title) + '">' + esc(cur.sub_code) + '</span>'
          + '<div class="hud-actions">'
          + '<button type="button" class="hud-btn hud-btn-icon" data-cmd="prev" ' + (idx <= 0 ? 'disabled' : '') + ' title="Quay lại bước trước (Alt+←)">&#9664;</button>'
          + '<button type="button" class="hud-btn hud-btn-primary hud-btn-icon" data-cmd="next" ' + (idx >= total - 1 ? 'disabled' : '') + ' title="Bước tiếp theo (Alt+→)">&#9654;</button>'
          + '<button type="button" class="hud-btn hud-btn-icon" data-cmd="toggle_collapse" title="Mở rộng thanh điều khiển demo">&#43;</button>'
          + '</div>';
      } else {
        var prevTitle = (sync && sync.prev_preview) ? ('Quay lại: ' + sync.prev_preview.sub_code + ' (' + sync.prev_preview.role + ') - ' + sync.prev_preview.title + ' [Alt+←]') : 'Quay lại bước trước (Alt+←)';
        var nextTitle = (sync && sync.next_preview) ? ('Tiếp theo: ' + sync.next_preview.sub_code + ' (' + sync.next_preview.role + ') - ' + sync.next_preview.title + ' [Alt+→]') : 'Bước tiếp theo (Alt+→)';
        var nextLabel = 'Tiếp &#9654;';

        barInner = '<div class="hud-progress"><div class="hud-progress-fill" style="width:' + pct + '%"></div></div>'
          + '<div class="hud-drag" id="hud-drag-handle" title="Cửa sổ ' + esc(state.windowRole) + ' (' + esc(state.windowEmail) + ') · Kéo để di chuyển · Nhấp đúp đặt lại vị trí">'
          + '<span class="hud-dot' + (state.connected ? ' ok' : '') + '" title="' + (state.connected ? ('WebSocket đồng bộ (' + connectedCount + ' kết nối)') : 'Đang kết nối lại WebSocket :3999') + '"></span>'
          + '<span class="hud-role-badge">' + esc(state.windowRole) + '</span>'
          + '<span class="hud-role-name">' + esc(state.windowName) + '</span>'
          + '</div>'
          + '<span class="hud-sep"></span>'
          + '<div class="hud-case" title="' + esc(cur.sub_code + ' · ' + cur.title + (cur.hint ? '\nGợi ý: ' + cur.hint : '')) + '">'
          + '<span class="hud-code">' + esc(cur.sub_code) + '</span>'
          + '<span class="hud-title">' + esc(cur.title) + '</span>'
          + '<span class="hud-counter">' + (idx + 1) + '/' + total + '</span>'
          + (roleMismatch
              ? '<button type="button" class="hud-jump-role" data-cmd="focus_role" data-role="' + esc(cur.role) + '" title="Bước hiện tại đang ở vai trò ' + esc(cur.role) + ' — Bấm để nhảy sang cửa sổ ' + esc(cur.role) + '">&#8599; ' + esc(cur.role) + '</button>'
              : '')
          + '</div>'
          + '<div class="hud-actions">'
          + '<button type="button" class="hud-btn" data-cmd="prev" ' + (idx <= 0 ? 'disabled' : '') + ' title="' + esc(prevTitle) + '">&#9664; Trước</button>'
          + '<button type="button" class="hud-btn hud-btn-primary" data-cmd="next" ' + (idx >= total - 1 ? 'disabled' : '') + ' title="' + esc(nextTitle) + '">' + nextLabel + '</button>'
          + '<button type="button" class="hud-btn hud-btn-icon" data-cmd="rerun" title="Chạy lại bước hiện tại trên Chrome (Alt+R)">&#8635;</button>'
          + '<button type="button" class="hud-btn hud-btn-icon' + (state.drawerOpen ? ' hud-btn-active' : '') + '" data-cmd="toggle_drawer" title="Mở danh sách 6 vai trò & các bước B0–B15 (Alt+M)">&#9776;</button>'
          + '<button type="button" class="hud-btn hud-btn-icon" data-cmd="toggle_collapse" title="Thu gọn thanh banner">&#8211;</button>'
          + '</div>';
      }

      var errHtml = '';
      if (!state.collapsed && sync && sync.last_error && state.dismissedErrVer !== sync.version) {
        errHtml = '<div class="hud-hint-bar" style="display:flex;align-items:center;justify-content:space-between;gap:8px;">'
          + '<span>' + esc(sync.last_error) + '</span>'
          + '<button type="button" class="hud-btn hud-btn-icon" data-cmd="dismiss_err" title="Đóng thông báo">&#10005;</button>'
          + '</div>';
      }

      shadow.innerHTML = '<style>' + STYLE_CSS + '</style>'
        + '<div class="hud-wrap' + darkCls + '">'
        + drawerHtml
        + errHtml
        + '<div class="hud-bar">' + barInner + '</div>'
        + '</div>';

      // Giữ cuộn vào mục đang active khi mở danh sách
      if (state.drawerOpen) {
        var activeEl = shadow.querySelector('.hud-item.active');
        if (activeEl && activeEl.scrollIntoView) {
          try { activeEl.scrollIntoView({ block: 'nearest' }); } catch (e) {}
        }
      }

      bindEvents();
    };

    var handleButtonAction = function(btn) {
      var tab = btn.getAttribute('data-tab');
      if (tab) {
        state.drawerTab = tab;
        render();
        return;
      }
      var cmd = btn.getAttribute('data-cmd');
      if (!cmd) return;
      if (cmd === 'dismiss_err') {
        if (state.sync) state.dismissedErrVer = state.sync.version;
        render();
        return;
      }
      if (cmd === 'toggle_collapse') {
        state.collapsed = !state.collapsed;
        if (state.collapsed) state.drawerOpen = false;
        safeSet('bh-demo-hud-collapsed', state.collapsed ? '1' : '0');
        render();
        return;
      }
      if (cmd === 'toggle_drawer') {
        state.drawerOpen = !state.drawerOpen;
        render();
        return;
      }
      if (cmd === 'next') {
        state.localBusy = true;
        render();
        sendCommand({ type: 'next' });
        return;
      }
      if (cmd === 'prev') {
        state.localBusy = true;
        render();
        sendCommand({ type: 'prev' });
        return;
      }
      if (cmd === 'rerun') {
        state.localBusy = true;
        render();
        sendCommand({ type: 'rerun' });
        return;
      }
      if (cmd === 'cancel_busy') {
        state.localBusy = false;
        sendCommand({ type: 'cancel_busy' });
        render();
        return;
      }
      if (cmd === 'goto') {
        var idxNum = parseInt(btn.getAttribute('data-idx') || '0', 10);
        state.drawerOpen = false;
        state.localBusy = true;
        render();
        sendCommand({ type: 'goto', index: idxNum });
        return;
      }
      if (cmd === 'qa_action') {
        var aid = btn.getAttribute('data-action') || '';
        state.drawerOpen = false;
        state.localBusy = true;
        render();
        sendCommand({ type: 'qa_action', action_id: aid });
        return;
      }
      if (cmd === 'focus_role') {
        var roleName = btn.getAttribute('data-role') || '';
        state.drawerOpen = false;
        render();
        sendCommand({ type: 'focus_role', role: roleName });
        return;
      }
      if (cmd === 'toggle_auto') {
        var curAuto = state.sync ? Boolean(state.sync.auto_execute) : true;
        sendCommand({ type: 'set_auto_execute', value: !curAuto });
        return;
      }
      if (cmd === 'maximize_all') {
        state.drawerOpen = false;
        render();
        sendCommand({ type: 'arrange_windows', mode: 'maximize' });
      }
    };

    var bindEvents = function() {
      if (!shadow) return;
      var btns = shadow.querySelectorAll('button');
      for (var i = 0; i < btns.length; i++) {
        (function(b) {
          // Chặn mousedown lấy focus ra khỏi modal/input Radix phía sau
          b.addEventListener('mousedown', function(ev) {
            ev.preventDefault();
            ev.stopPropagation();
          });
          b.addEventListener('pointerdown', function(ev) {
            ev.stopPropagation();
          });
          b.addEventListener('click', function(ev) {
            ev.preventDefault();
            ev.stopPropagation();
            if (!b.disabled) handleButtonAction(b);
          });
        })(btns[i]);
      }

      var dragHandle = shadow.getElementById('hud-drag-handle');
      if (dragHandle) {
        dragHandle.addEventListener('dblclick', function(ev) {
          ev.stopPropagation();
          state.pos = null;
          safeSet('bh-demo-hud-pos', '');
          applyHostPosition();
        });
        dragHandle.addEventListener('mousedown', function(ev) {
          if (ev.button !== 0) return;
          ev.preventDefault();
          ev.stopPropagation();
          var rect = host.getBoundingClientRect();
          dragging = {
            startX: ev.clientX,
            startY: ev.clientY,
            origLeft: rect.left,
            origBottom: window.innerHeight - rect.bottom
          };
        });
      }
    };

    window.addEventListener('mousemove', function(ev) {
      if (!dragging || !host) return;
      var dx = ev.clientX - dragging.startX;
      var dy = ev.clientY - dragging.startY;
      state.pos = {
        left: Math.round(dragging.origLeft + dx),
        bottom: Math.round(dragging.origBottom - dy)
      };
      applyHostPosition();
    });

    window.addEventListener('mouseup', function() {
      if (!dragging) return;
      dragging = null;
      if (state.pos) {
        safeSet('bh-demo-hud-pos', JSON.stringify(state.pos));
      }
    });

    window.addEventListener('resize', applyHostPosition);

    // Phím tắt không xung đột với form BrandHub: Alt + mũi tên trái/phải, Alt + R, Alt + M, Alt + 1..6
    window.addEventListener('keydown', function(ev) {
      if (ev.key === 'Escape') {
        if (state.drawerOpen) {
          state.drawerOpen = false;
          render();
          return;
        }
        if ((state.sync && state.sync.busy) || state.localBusy) {
          state.localBusy = false;
          sendCommand({ type: 'cancel_busy' });
          render();
          return;
        }
      }
      if (!ev.altKey || ev.ctrlKey || ev.metaKey) return;
      if (ev.key === 'ArrowRight' || ev.key === 'PageDown') {
        ev.preventDefault();
        state.localBusy = true;
        render();
        sendCommand({ type: 'next' });
      } else if (ev.key === 'ArrowLeft' || ev.key === 'PageUp') {
        ev.preventDefault();
        state.localBusy = true;
        render();
        sendCommand({ type: 'prev' });
      } else if (ev.key === 'r' || ev.key === 'R') {
        ev.preventDefault();
        state.localBusy = true;
        render();
        sendCommand({ type: 'rerun' });
      } else if (ev.key === 'm' || ev.key === 'M') {
        ev.preventDefault();
        state.drawerOpen = !state.drawerOpen;
        render();
      } else if (ev.key >= '1' && ev.key <= '6') {
        var rTarget = ROLE_ORDER[parseInt(ev.key, 10) - 1];
        if (rTarget) {
          ev.preventDefault();
          sendCommand({ type: 'focus_role', role: rTarget });
        }
      }
    }, true);

    var ensureMounted = function() {
      var rootEl = document.documentElement;
      if (!rootEl) return;
      var legacy = document.getElementById('bh-demo-hud-badge');
      if (legacy && legacy.parentNode) legacy.parentNode.removeChild(legacy);

      if (!host) {
        host = document.createElement('div');
        host.id = 'bh-demo-hud-root';
        host.setAttribute('data-bh-demo-role', state.windowRole);
        host.addEventListener('pointerdown', function(ev) { ev.stopPropagation(); });
        host.addEventListener('mousedown', function(ev) { ev.stopPropagation(); });
        shadow = host.attachShadow({ mode: 'open' });
      }
      if (!rootEl.contains(host)) {
        rootEl.appendChild(host);
      }
      applyHostPosition();
      render();
    };

    var boot = function() {
      ensureMounted();
      fetchInitialState();
      connectSocket();

      // Theo dõi DOM và class dark mode để tự phục hồi tức thì nếu trang thay đổi cấu trúc
      try {
        var obs = new MutationObserver(function(mutations) {
          var needRemount = !document.documentElement.contains(host);
          var themeChanged = false;
          for (var m = 0; m < mutations.length; m++) {
            if (mutations[m].type === 'attributes') themeChanged = true;
          }
          if (needRemount) {
            ensureMounted();
          } else if (themeChanged) {
            render();
          }
        });
        obs.observe(document.documentElement, { childList: true, attributes: true, attributeFilter: ['class', 'data-theme'] });
      } catch (e) {}

      // Watchdog phòng hờ tuyệt đối mỗi 2 giây
      setInterval(function() {
        if (document.documentElement && (!host || !document.documentElement.contains(host))) {
          ensureMounted();
        }
      }, 2000);
    };

    window.__BH_DEMO_HUD_V2__ = {
      ensureMounted: ensureMounted,
      updateIdentity: function(r, n, e) {
        state.windowRole = r;
        state.windowName = n;
        state.windowEmail = e;
        if (ws && ws.readyState === WebSocket.OPEN) {
          try { ws.send(JSON.stringify({ type: 'hello', window_role: r })); } catch (err) {}
        }
        render();
      }
    };

    if (document.documentElement) {
      boot();
    } else {
      document.addEventListener('DOMContentLoaded', boot);
    }
  } catch (err) {}
})();
"""


def build_hud_script(role: str, monitor_port: int) -> str:
    info = ROLE_PROFILES.get(role, ROLE_PROFILES["Owner"])
    return (
        _HUD_JS_TEMPLATE
        .replace("__WINDOW_ROLE__", json.dumps(info["role"], ensure_ascii=False))
        .replace("__WINDOW_NAME__", json.dumps(info["full_name"], ensure_ascii=False))
        .replace("__WINDOW_EMAIL__", json.dumps(info["email"], ensure_ascii=False))
        .replace("__MONITOR_PORT__", str(int(monitor_port)))
    )


# ==============================================================================
# 2. SELENIUM BROWSER CONTROLLER + STATE SYNC ENGINE
# ==============================================================================
class DemoBrowserController:
    def __init__(self, app_url: str, password: str, monitor_port: int = DEFAULT_MONITOR_PORT) -> None:
        self.app_url = app_url.rstrip("/")
        self.password = password
        self.monitor_port = monitor_port
        self.ids = dict(DEFAULT_IDS)
        self.drivers: dict[str, webdriver.Chrome] = {}
        self.hwnds: dict[str, int] = {}
        self.window_mode: str = "normal"
        self.lock = threading.Lock()
        self.profile_base_dir = Path.home() / ".brandhub_demo_chrome_profiles"
        self.profile_base_dir.mkdir(parents=True, exist_ok=True)
        self.repo_root = Path(__file__).resolve().parents[2]
        self.prep_script_path = Path(__file__).resolve().parent / "prepare_demo_data_template.py"
        self._prep_lock = threading.Lock()
        self._hud_script_ids: dict[int, str] = {}

        # Trạng thái đồng bộ thời gian thực qua WebSocket trên toàn bộ 6 cửa sổ Chrome
        self.ws_hub = WebSocketHub()
        self.state_lock = threading.Lock()
        self.state_version: int = 1
        self.timeline_index: int = 0
        self.active_qa: dict[str, str] | None = None
        self.auto_execute: bool = True
        self.busy: bool = False
        self.busy_label: str = ""
        self.done_actions: set[str] = set()
        self.last_message: str = "Sẵn sàng thuyết trình 6 vai trò BrandHub."
        self.last_error: str = ""

    def format_route(self, route_template: str) -> str:
        return route_template.format(**self.ids)

    def _is_alive(self, role: str) -> bool:
        drv = self.drivers.get(role)
        if not drv:
            return False
        try:
            _ = drv.current_url
            return True
        except WebDriverException:
            self.drivers.pop(role, None)
            self.hwnds.pop(role, None)
            return False

    def _register_hud_cdp(self, driver: webdriver.Chrome, role: str) -> None:
        """Đăng ký script HUD vào CDP để tự động gắn trên mọi tài liệu mới, reload và chuyển trang."""
        script = build_hud_script(role, self.monitor_port)
        try:
            old_id = self._hud_script_ids.get(id(driver))
            if old_id:
                try:
                    driver.execute_cdp_cmd("Page.removeScriptToEvaluateOnNewDocument", {"identifier": old_id})
                except Exception:
                    pass
            res = driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})
            if isinstance(res, dict) and res.get("identifier"):
                self._hud_script_ids[id(driver)] = str(res["identifier"])
        except Exception:
            pass

    def _ensure_hud_mounted(self, driver: webdriver.Chrome, role: str) -> None:
        """Bảo đảm thanh HUD nổi luôn hiển thị ngay lập tức trên tài liệu hiện tại."""
        script = build_hud_script(role, self.monitor_port)
        try:
            driver.execute_script(script)
        except Exception:
            pass

    def _capture_hwnd_for_driver(self, role: str, driver: webdriver.Chrome, before_hwnds: set[int]) -> None:
        if sys.platform != "win32":
            return
        try:
            after_hwnds = _win32_list_chrome_hwnds()
            created = list(after_hwnds - before_hwnds)
            if len(created) == 1:
                self.hwnds[role] = created[0]
                return
            # Dự phòng bằng marker tạm trong title
            marker = f"[BH-WIN-{role}]"
            old_title = driver.execute_script("return document.title || '';") or ""
            driver.execute_script("document.title = arguments[0];", f"{marker} {old_title}")
            time.sleep(0.08)
            hwnd = _win32_find_hwnd_by_title_marker(marker)
            driver.execute_script("document.title = arguments[0];", old_title)
            if hwnd:
                self.hwnds[role] = hwnd
        except Exception:
            pass

    def ensure_driver(self, role: str) -> webdriver.Chrome:
        if role not in ROLE_PROFILES:
            raise ValueError(f"Role không hợp lệ: {role}")
        if self._is_alive(role):
            return self.drivers[role]

        profile_dir = self.profile_base_dir / role.lower()
        profile_dir.mkdir(parents=True, exist_ok=True)

        opts = Options()
        opts.add_argument(f"--user-data-dir={profile_dir}")
        opts.add_argument("--window-size=1440,920")
        opts.add_argument("--disable-notifications")
        opts.add_argument("--no-first-run")
        opts.add_argument("--no-default-browser-check")
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option("useAutomationExtension", False)

        before_hwnds = _win32_list_chrome_hwnds()
        # chromedriver mặc định dùng chung console của Python; nếu cmd của Runner đã chết thì nó crash 0xC0000142.
        # CREATE_NO_WINDOW cấp cho chromedriver một console ẩn riêng.
        service = ChromeService(popen_kw={"creation_flags": getattr(subprocess, "CREATE_NO_WINDOW", 0)})
        driver = webdriver.Chrome(options=opts, service=service)
        # Mặc định Selenium chờ tải trang tới 300s và giữ self.lock suốt thời gian đó -> mọi bước sau kẹt "Đang chạy..."
        driver.set_page_load_timeout(30)
        self.drivers[role] = driver
        self._capture_hwnd_for_driver(role, driver, before_hwnds)
        # Đăng ký CDP HUD ngay khi Chrome vừa khởi tạo — TRƯỚC khi tải trang đầu tiên!
        self._register_hud_cdp(driver, role)
        self._apply_window_mode_to_driver(driver)
        return driver

    def _apply_window_mode_to_driver(self, driver: webdriver.Chrome) -> None:
        try:
            if self.window_mode == "split":
                dims = driver.execute_script(
                    "return {w: window.screen.availWidth || 1920, h: window.screen.availHeight || 1040};"
                )
                avail_w = int((dims or {}).get("w") or 1920)
                avail_h = int((dims or {}).get("h") or 1040)
                driver.set_window_rect(x=0, y=0, width=max(960, int(avail_w * 0.71)), height=avail_h)
            elif self.window_mode == "maximize":
                driver.maximize_window()
        except Exception:
            pass

    def bring_to_front(self, driver: webdriver.Chrome, role: str | None = None) -> None:
        target_role = role
        if target_role is None:
            for r_name, drv in list(self.drivers.items()):
                if drv is driver:
                    target_role = r_name
                    break
        try:
            driver.switch_to.window(driver.current_window_handle)
        except Exception:
            pass
        try:
            driver.execute_cdp_cmd("Page.bringToFront", {})
        except Exception:
            pass
        if target_role:
            hwnd = self.hwnds.get(target_role)
            if not _win32_raise_hwnd(hwnd):
                # Tìm lại HWND bằng marker title nếu cửa sổ đã thay đổi handle
                self._capture_hwnd_for_driver(target_role, driver, set())
                _win32_raise_hwnd(self.hwnds.get(target_role))
        self._apply_window_mode_to_driver(driver)

    def arrange_windows(self, mode: str) -> dict[str, Any]:
        if mode not in ("split", "maximize", "normal"):
            return {"ok": False, "error": f"Chế độ cửa sổ không hợp lệ: {mode}"}
        self.window_mode = mode
        updated = 0
        for role in list(self.drivers.keys()):
            if self._is_alive(role):
                drv = self.drivers[role]
                self._apply_window_mode_to_driver(drv)
                updated += 1
        if mode == "split":
            msg = f"Đã xếp gọn {updated} cửa sổ Chrome sang 71% bên trái màn hình (dành 29% bên phải cho Bàn điều khiển)."
        elif mode == "maximize":
            msg = f"Đã phóng to toàn màn hình {updated} cửa sổ Chrome (sẵn sàng chiếu song song TV)."
        else:
            msg = f"Đã chuyển về kích thước tiêu chuẩn cho {updated} cửa sổ Chrome."
        self.broadcast_state(last_message=msg)
        return {"ok": True, "window_mode": self.window_mode, "updated": updated, "message": msg}

    def inject_role_Hud_badge(self, driver: webdriver.Chrome, role: str, step_label: str = "") -> None:
        """Giữ tương thích ngược: bảo đảm thanh HUD WebSocket gắn trên Chrome và đưa cửa sổ lên trước."""
        self.bring_to_front(driver, role=role)
        self._register_hud_cdp(driver, role)
        self._ensure_hud_mounted(driver, role)
        if step_label:
            self.broadcast_state(last_message=step_label)

    def get_sync_state(self) -> dict[str, Any]:
        with self.state_lock:
            idx = max(0, min(self.timeline_index, len(DEMO_TIMELINE) - 1))
            item = DEMO_TIMELINE[idx]
            if self.active_qa:
                cur_obj = {
                    "index": idx,
                    "step_code": "Q&A",
                    "sub_code": "Q&A",
                    "action_id": self.active_qa["action_id"],
                    "role": self.active_qa["role"],
                    "actor_name": ROLE_PROFILES[self.active_qa["role"]]["full_name"],
                    "title": self.active_qa["title"],
                    "stage": "Q&A Hội đồng",
                    "fr_code": "Q&A",
                    "kind": "nav",
                    "hint": "Đang trình bày màn hình chuyên sâu Q&A Hội đồng.",
                }
            else:
                cur_obj = {
                    "index": idx,
                    "step_code": item["step_code"],
                    "sub_code": item["sub_code"],
                    "action_id": item["action_id"],
                    "role": item["role"],
                    "actor_name": ROLE_PROFILES[item["role"]]["full_name"],
                    "title": item["title"],
                    "stage": item["stage"],
                    "fr_code": item["fr_code"],
                    "kind": item["kind"],
                    "hint": item.get("hint", ""),
                }
            prev_item = DEMO_TIMELINE[idx - 1] if idx > 0 else None
            next_item = DEMO_TIMELINE[idx + 1] if idx < len(DEMO_TIMELINE) - 1 else None
            state_payload = {
                "type": "state",
                "version": self.state_version,
                "timeline_index": idx,
                "total": len(DEMO_TIMELINE),
                "current": cur_obj,
                "active_qa": self.active_qa,
                "prev_preview": (
                    {"sub_code": prev_item["sub_code"], "role": prev_item["role"], "title": prev_item["title"]}
                    if prev_item else None
                ),
                "next_preview": (
                    {"sub_code": next_item["sub_code"], "role": next_item["role"], "title": next_item["title"]}
                    if next_item else None
                ),
                "auto_execute": self.auto_execute,
                "busy": self.busy,
                "busy_label": self.busy_label,
                "done_actions": sorted(self.done_actions),
                "last_message": self.last_message,
                "last_error": self.last_error,
                "connected_clients": self.ws_hub.client_count(),
                "connected_roles": self.ws_hub.connected_roles(),
                "window_mode": self.window_mode,
                "roles": {
                    r: {
                        "alive": r in self.drivers,
                        "ws_connected": r in self.ws_hub.connected_roles(),
                        "full_name": ROLE_PROFILES[r]["full_name"],
                        "email": ROLE_PROFILES[r]["email"],
                    }
                    for r in CANONICAL_ROLE_ORDER
                },
                "timeline": [
                    {
                        "index": i,
                        "step_code": t["step_code"],
                        "sub_code": t["sub_code"],
                        "action_id": t["action_id"],
                        "role": t["role"],
                        "title": t["title"],
                        "kind": t["kind"],
                    }
                    for i, t in enumerate(DEMO_TIMELINE)
                ],
                "qa_items": QA_TIMELINE,
            }
        return state_payload

    def broadcast_state(
        self,
        *,
        last_message: str | None = None,
        last_error: str | None = None,
        busy: bool | None = None,
        busy_label: str | None = None,
    ) -> dict[str, Any]:
        with self.state_lock:
            self.state_version += 1
            if last_message is not None:
                self.last_message = last_message
            if last_error is not None:
                self.last_error = last_error
            if busy is not None:
                self.busy = busy
            if busy_label is not None:
                self.busy_label = busy_label
        snap = self.get_sync_state()
        self.ws_hub.broadcast(snap)
        return snap

    def _run_timeline_item_async(self, item: dict[str, Any], direction: str) -> None:
        def worker() -> None:
            action_id = item["action_id"]
            role = item["role"]
            kind = item.get("kind", "nav")
            try:
                if direction == "prev" and kind in ("fill", "toggle"):
                    # Khi bấm Quay lại vào bước gõ form/toggle: đưa cửa sổ vai trò lên trước,
                    # tránh vô tình gõ lặp dữ liệu 2 lần (có nút Chạy lại ↻ nếu muốn chạy lại).
                    with self.lock:
                        drv = self.ensure_driver(role)
                        self.bring_to_front(drv, role=role)
                        self._ensure_hud_mounted(drv, role)
                    self.broadcast_state(
                        busy=False,
                        busy_label="",
                        last_message=f"Đã quay lại {item['sub_code']} ({role}). Bấm ↻ nếu muốn tự gõ lại dữ liệu.",
                        last_error="",
                    )
                    return

                res = self.execute_step_action(action_id, custom_payload=None, _from_timeline=True)
                ok = bool(res.get("ok"))
                if ok:
                    with self.state_lock:
                        self.done_actions.add(action_id)
                self.broadcast_state(
                    busy=False,
                    busy_label="",
                    last_message=str(res.get("message", "")) if ok else "",
                    last_error="" if ok else str(res.get("error", "Lỗi thực thi thao tác.")),
                )
            except Exception as exc:
                self.broadcast_state(busy=False, busy_label="", last_error=str(exc))

        threading.Thread(target=worker, daemon=True).start()

    def handle_hud_command(self, cmd: dict[str, Any]) -> dict[str, Any]:
        ctype = str(cmd.get("type", "")).strip()

        if ctype == "cancel_busy":
            snap = self.broadcast_state(busy=False, busy_label="", last_message="Đã hủy trạng thái chờ khẩn cấp.")
            return {"ok": True, "state": snap}

        if ctype == "set_auto_execute":
            val = bool(cmd.get("value", True))
            with self.state_lock:
                self.auto_execute = val
            snap = self.broadcast_state(
                last_message="Đã BẬT chế độ tự động điều khiển Chrome theo bước." if val else "Đã chuyển sang chế độ chỉ đồng bộ Banner trên 6 cửa sổ."
            )
            return {"ok": True, "state": snap}

        if ctype == "arrange_windows":
            mode = str(cmd.get("mode", "maximize"))
            def _arr():
                self.arrange_windows(mode)
            threading.Thread(target=_arr, daemon=True).start()
            return {"ok": True, "state": self.get_sync_state()}

        if ctype == "focus_role":
            role = str(cmd.get("role", "Owner"))
            if role not in ROLE_PROFILES:
                return {"ok": False, "error": f"Role không hợp lệ: {role}", "state": self.get_sync_state()}

            def _focus():
                self.broadcast_state(busy=True, busy_label=f"Đang mở {role}...")
                try:
                    if self._is_alive(role):
                        with self.lock:
                            drv = self.drivers[role]
                            self.bring_to_front(drv, role=role)
                            self._ensure_hud_mounted(drv, role)
                        self.broadcast_state(busy=False, busy_label="", last_message=f"Đã chuyển lên cửa sổ {role}.", last_error="")
                    else:
                        res = self.login_role(role)
                        self.broadcast_state(
                            busy=False,
                            busy_label="",
                            last_message=f"Đã mở cửa sổ {role}." if res.get("ok") else "",
                            last_error="" if res.get("ok") else str(res.get("error", "")),
                        )
                except Exception as exc:
                    self.broadcast_state(busy=False, busy_label="", last_error=str(exc))

            threading.Thread(target=_focus, daemon=True).start()
            return {"ok": True, "state": self.get_sync_state()}

        if ctype == "qa_action":
            action_id = str(cmd.get("action_id", ""))
            qa_meta = QA_ITEM_BY_ACTION.get(action_id)
            if not qa_meta:
                return {"ok": False, "error": f"Không tìm thấy Q&A: {action_id}", "state": self.get_sync_state()}
            with self.state_lock:
                self.active_qa = qa_meta
                should_exec = self.auto_execute
            snap = self.broadcast_state(
                busy=should_exec,
                busy_label=f"Đang mở {qa_meta['title']}..." if should_exec else "",
                last_error="",
            )
            if should_exec:
                def _run_qa():
                    res = self.execute_step_action(action_id, _from_timeline=True)
                    self.broadcast_state(
                        busy=False,
                        busy_label="",
                        last_message=str(res.get("message", "")) if res.get("ok") else "",
                        last_error="" if res.get("ok") else str(res.get("error", "")),
                    )
                threading.Thread(target=_run_qa, daemon=True).start()
            return {"ok": True, "state": snap}

        if ctype == "goto_step_code":
            code = str(cmd.get("step_code", "")).strip()
            target_idx = next((i for i, t in enumerate(DEMO_TIMELINE) if t["step_code"] == code), None)
            if target_idx is None:
                return {"ok": False, "error": f"Không tìm thấy bước: {code}", "state": self.get_sync_state()}
            with self.state_lock:
                self.timeline_index = target_idx
                self.active_qa = None
                item = DEMO_TIMELINE[target_idx]
                explicit_exec = cmd.get("execute")
                should_exec = False if explicit_exec is None else bool(explicit_exec)
            snap = self.broadcast_state(
                busy=should_exec,
                busy_label=f"Đang chuyển sang {item['sub_code']} ({item['role']})..." if should_exec else "",
                last_error="",
            )
            if should_exec:
                self._run_timeline_item_async(item, direction="goto")
            return {"ok": True, "state": snap}

        if ctype in ("next", "prev", "goto", "rerun"):
            with self.state_lock:
                old_idx = self.timeline_index
                if ctype == "next":
                    new_idx = min(len(DEMO_TIMELINE) - 1, old_idx + 1)
                elif ctype == "prev":
                    new_idx = max(0, old_idx - 1)
                elif ctype == "goto":
                    raw_idx = int(cmd.get("index", old_idx))
                    new_idx = max(0, min(len(DEMO_TIMELINE) - 1, raw_idx))
                else:
                    new_idx = old_idx
                self.timeline_index = new_idx
                self.active_qa = None
                item = DEMO_TIMELINE[new_idx]
                # Trước/Tiếp chỉ đổi bước; chỉ ↻ (rerun) mới tự chạy Selenium. Không khóa banner ("Đang chạy...").
                should_exec = ctype == "rerun"

            snap = self.broadcast_state(
                busy=False,
                busy_label="",
                last_error="",
            )
            if should_exec:
                self._run_timeline_item_async(item, direction=ctype)
            return {"ok": True, "state": snap}

        return {"ok": False, "error": f"Lệnh HUD không hợp lệ: {ctype}", "state": self.get_sync_state()}

    def highlight_element(
        self,
        driver: webdriver.Chrome,
        element,
        label: str = "THAO TÁC TẠI ĐÂY",
        color: str = "#ea6c3b",
    ) -> None:
        """Cuộn tới phần tử và tạo viền cam ấm dịu chuẩn BrandHub (0px góc vuông)."""
        js = """
        const el = arguments[0];
        const label = arguments[1];
        const color = '#ea6c3b';
        if (!el) return;
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        el.style.transition = 'all 0.25s ease';
        el.style.outline = `3px solid ${color}`;
        el.style.outlineOffset = '3px';
        el.style.boxShadow = '0 0 0 6px rgba(234,108,59,0.18), 0 8px 20px rgba(234,108,59,0.22)';

        const oldTag = document.getElementById('bh-demo-target-tag');
        if (oldTag) oldTag.remove();

        const rect = el.getBoundingClientRect();
        const tag = document.createElement('div');
        tag.id = 'bh-demo-target-tag';
        tag.textContent = label;
        tag.style.cssText = [
            'position:fixed',
            `top:${Math.max(8, rect.top - 36)}px`,
            `left:${Math.max(8, rect.left)}px`,
            'z-index:2147483646',
            `background:${color}`,
            'color:#fff',
            'font-family:Inter,system-ui,-apple-system,sans-serif',
            'font-size:11px',
            'font-weight:800',
            'padding:4px 10px',
            'border-radius:0px',
            'box-shadow:0 4px 12px rgba(234,108,59,0.32)',
            'pointer-events:none'
        ].join(';');
        document.body.appendChild(tag);
        setTimeout(() => { if (tag && tag.parentNode) tag.remove(); }, 7000);
        """
        try:
            driver.execute_script(js, element, label, color)
        except Exception:
            pass

    def react_set_value(
        self,
        driver: webdriver.Chrome,
        element,
        value: str,
        append: bool = False,
        human_typing: bool = True,
    ) -> None:
        """Gán giá trị cho input/textarea trong React (kèm hiệu ứng gõ chữ trực quan khi thuyết trình)."""
        try:
            driver.execute_script("arguments[0].scrollIntoView({behavior:'smooth', block:'center'});", element)
            element.click()
        except Exception:
            pass

        if not append:
            try:
                element.send_keys(Keys.CONTROL, "a")
                element.send_keys(Keys.BACKSPACE)
            except Exception:
                pass

        if human_typing and len(value) <= 980:
            chunk_size = 5 if len(value) > 160 else 2
            current_js = """
            const el = arguments[0];
            const val = arguments[1];
            const proto = el.tagName === 'TEXTAREA'
                ? window.HTMLTextAreaElement.prototype
                : window.HTMLInputElement.prototype;
            const setter = Object.getOwnPropertyDescriptor(proto, 'value')?.set;
            const nextVal = (el.value || '') + val;
            if (setter) {
                setter.call(el, nextVal);
            } else {
                el.value = nextVal;
            }
            el.dispatchEvent(new Event('input', { bubbles: true }));
            """
            for i in range(0, len(value), chunk_size):
                piece = value[i : i + chunk_size]
                driver.execute_script(current_js, element, piece)
                time.sleep(0.015)
            driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", element)
            return

        js = """
        const el = arguments[0];
        const text = arguments[1];
        const append = arguments[2];
        const proto = el.tagName === 'TEXTAREA'
            ? window.HTMLTextAreaElement.prototype
            : window.HTMLInputElement.prototype;
        const setter = Object.getOwnPropertyDescriptor(proto, 'value')?.set;
        const finalValue = append ? ((el.value || '') + text) : text;
        if (setter) {
            setter.call(el, finalValue);
        } else {
            el.value = finalValue;
        }
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
        """
        driver.execute_script(js, element, value, append)

    def select_radix_combobox_by_label(self, driver: webdriver.Chrome, combobox_el, option_text: str) -> bool:
        try:
            self.highlight_element(driver, combobox_el, f"Chọn: {option_text}")
            driver.execute_script("arguments[0].click();", combobox_el)
            time.sleep(0.28)
            opt_xpath = (
                f"//*[@role='option' and (contains(normalize-space(.), '{option_text}') "
                f"or .//*[contains(normalize-space(.), '{option_text}')])]"
            )
            options = driver.find_elements(By.XPATH, opt_xpath)
            if options:
                driver.execute_script("arguments[0].click();", options[0])
                time.sleep(0.22)
                return True
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        except Exception:
            pass
        return False

    def login_role(self, role: str, target_route: str | None = None, step_label: str = "") -> dict[str, Any]:
        with self.lock:
            driver = self.ensure_driver(role)
            info = ROLE_PROFILES[role]
            requires_auth = bool(info.get("requires_auth", True))
            dest_route = self.format_route(target_route or info["default_route"])
            dest_url = f"{self.app_url}{dest_route}"

            try:
                driver.get(dest_url)
                time.sleep(0.9)

                if not requires_auth:
                    # Vai trò Guest: giữ trạng thái chưa đăng nhập, xóa token cũ nếu có
                    try:
                        had_auth = driver.execute_script(
                            "try { var had = !!(localStorage.getItem('accessToken') || localStorage.getItem('refreshToken') || localStorage.getItem('auth-storage')); "
                            "if (had) { localStorage.removeItem('accessToken'); localStorage.removeItem('refreshToken'); localStorage.removeItem('auth-storage'); } return had; } catch(e) { return false; }"
                        )
                        if had_auth:
                            driver.get(dest_url)
                            time.sleep(0.6)
                    except Exception:
                        pass
                else:
                    current = driver.current_url
                    if "/login" in current or "/guest" in current:
                        if "/login" not in current:
                            driver.get(f"{self.app_url}/login")
                        try:
                            wait = WebDriverWait(driver, 10)
                            candidate_passwords = [self.password]
                            for alt_pwd in ("Password123", "Password123!"):
                                if alt_pwd not in candidate_passwords:
                                    candidate_passwords.append(alt_pwd)

                            logged_in = False
                            last_err: Exception | None = None
                            for pwd_try in candidate_passwords:
                                try:
                                    email_input = wait.until(
                                        EC.presence_of_element_located(
                                            (By.CSS_SELECTOR, "#email, input[type='email'], input[placeholder*='company.com']")
                                        )
                                    )
                                    pwd_input = driver.find_element(
                                        By.CSS_SELECTOR, "#password, input[type='password']"
                                    )
                                    self.react_set_value(driver, email_input, info["email"], append=False, human_typing=False)
                                    self.react_set_value(driver, pwd_input, pwd_try, append=False, human_typing=False)

                                    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                                    submit_btn.click()

                                    WebDriverWait(driver, 8).until(lambda d: "/login" not in d.current_url)
                                    logged_in = True
                                    break
                                except Exception as inner_exc:
                                    last_err = inner_exc

                            if not logged_in and last_err is not None:
                                raise last_err

                            time.sleep(0.6)
                            driver.get(dest_url)
                            time.sleep(0.8)
                        except Exception as exc:
                            return {
                                "ok": False,
                                "role": role,
                                "error": f"Không thể tự động đăng nhập {role} ({info['email']}): {exc}",
                            }
            finally:
                # Luôn bảo đảm thanh HUD góc trái dưới được gắn trên cửa sổ Chrome này kể cả khi lỗi đăng nhập
                self.bring_to_front(driver, role=role)
                self._register_hud_cdp(driver, role)
                self._ensure_hud_mounted(driver, role)

            self.broadcast_state(last_message=step_label or f"Đã sẵn sàng cửa sổ {role}.")
            return {
                "ok": True,
                "role": role,
                "email": info["email"],
                "full_name": info["full_name"],
                "current_url": driver.current_url,
            }

    def login_all_roles(self) -> list[dict[str, Any]]:
        results = []
        # Mở đủ 6 cửa sổ Chrome cho 6 Canonical Roles; mở Owner sau cùng để sẵn sàng vào B1 trên TV
        open_order = ["Guest", "Admin", "Client", "Creator", "Manager", "Owner"]
        for role in open_order:
            res = self.login_role(role, step_label=f"Đã mở cửa sổ {role} (đồng bộ 6 vai trò)")
            results.append(res)
        with self.state_lock:
            self.timeline_index = TIMELINE_INDEX_BY_ACTION.get("B1_NAV", 1)
            self.active_qa = None
        self.broadcast_state(
            busy=False,
            busy_label="",
            last_message="Đã mở và đồng bộ WebSocket đủ 6 cửa sổ Chrome (Guest, Owner, Manager, Creator, Client, Admin).",
            last_error="",
        )
        return results

    def _sync_open_browsers_storage(self, mode: str) -> int:
        refreshed = 0
        js_clean = """
        try {
            const emptyKeys = [
                'brandhub.portal.fptu2027.v1',
                'brandhub.library.templates.fptu2027.v2',
                'brandhub.ambassadors.v2',
                'brandhub.ambassador.jobs.v2'
            ];
            for (let i = window.localStorage.length - 1; i >= 0; i--) {
                const k = window.localStorage.key(i);
                if (!k) continue;
                if (
                    k.startsWith('brandhub.portal.fptu2027') ||
                    k.startsWith('brandhub.library.templates.fptu2027') ||
                    k.startsWith('brandhub.ambassadors.v2') ||
                    k.startsWith('brandhub.ambassador.jobs.v2')
                ) {
                    if (arguments[0] === 'clean') {
                        window.localStorage.setItem(k, '[]');
                    } else {
                        window.localStorage.removeItem(k);
                    }
                }
            }
            if (arguments[0] === 'clean') {
                emptyKeys.forEach((k) => window.localStorage.setItem(k, '[]'));
                const wsId = window.localStorage.getItem('brandhub.currentWorkspaceId');
                if (wsId) {
                    window.localStorage.setItem('brandhub.ambassadors.v2.' + wsId, '[]');
                    window.localStorage.setItem('brandhub.ambassador.jobs.v2.' + wsId, '[]');
                }
            }
        } catch (e) {}
        """
        with self.lock:
            for role in list(self.drivers.keys()):
                if not self._is_alive(role):
                    continue
                drv = self.drivers[role]
                try:
                    drv.execute_script(js_clean, mode)
                    drv.refresh()
                    self._ensure_hud_mounted(drv, role)
                    refreshed += 1
                except Exception:
                    pass
        return refreshed

    def _run_prep_script(self, flag: str) -> subprocess.CompletedProcess:
        """Chạy prepare_demo_data_template.py ngay trong tiến trình monitor.

        Không spawn python con: khi monitor được Repo Runner chạy nền, tiến trình con
        (Python bản Microsoft Store) chết lúc khởi tạo với 0xC0000142 (3221225794).
        """
        buf = io.StringIO()
        old_argv = sys.argv
        code = 0
        with self._prep_lock:
            sys.argv = [str(self.prep_script_path), flag]
            try:
                with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                    runpy.run_path(str(self.prep_script_path), run_name="__main__")
            except SystemExit as exc:
                code = exc.code if isinstance(exc.code, int) else (0 if exc.code is None else 1)
            except Exception:
                code = 1
                buf.write(traceback.format_exc())
            finally:
                sys.argv = old_argv
        out = buf.getvalue()
        return subprocess.CompletedProcess([flag], code, stdout=out, stderr=out if code else "")

    def reset_demo_database_data(self) -> dict[str, Any]:
        if not self.prep_script_path.exists():
            return {"ok": False, "error": f"Không tìm thấy script: {self.prep_script_path}"}
        try:
            proc = self._run_prep_script("--apply")
            if proc.returncode == 0:
                refreshed = self._sync_open_browsers_storage("reset")
                extra = f" (đã làm mới {refreshed} cửa sổ Chrome)" if refreshed > 0 else ""
                with self.state_lock:
                    self.timeline_index = TIMELINE_INDEX_BY_ACTION.get("B1_NAV", 1)
                    self.active_qa = None
                    self.done_actions.clear()
                msg = (
                    "Đã nạp lại dữ liệu chuẩn trên PostgreSQL, MongoDB và Redis: SE08 Digital Agency, "
                    f"7 Gói đa lĩnh vực, Chiến dịch ĐH FPT 2027 (4 tuần, 20 công việc){extra}."
                )
                self.broadcast_state(busy=False, busy_label="", last_message=msg, last_error="")
                return {
                    "ok": True,
                    "message": msg,
                    "stdout": proc.stdout.strip(),
                }
            return {
                "ok": False,
                "error": f"Script trả về mã lỗi {proc.returncode}: {proc.stderr.strip() or proc.stdout.strip()}",
            }
        except Exception as exc:
            return {"ok": False, "error": f"Lỗi khi chạy prepare_demo_data_template.py --apply: {exc}"}

    def clean_demo_database_data(self) -> dict[str, Any]:
        if not self.prep_script_path.exists():
            return {"ok": False, "error": f"Không tìm thấy script: {self.prep_script_path}"}
        try:
            proc = self._run_prep_script("--clean")
            if proc.returncode == 0:
                refreshed = self._sync_open_browsers_storage("clean")
                extra = f" và làm mới {refreshed} cửa sổ Chrome" if refreshed > 0 else ""
                with self.state_lock:
                    self.timeline_index = 0
                    self.active_qa = None
                    self.done_actions.clear()
                msg = (
                    "Đã xóa sạch toàn bộ dữ liệu mẫu cùng các bản ghi phát sinh sau buổi demo "
                    f"trên PostgreSQL, MongoDB, Redis{extra}."
                )
                self.broadcast_state(busy=False, busy_label="", last_message=msg, last_error="")
                return {
                    "ok": True,
                    "message": msg,
                    "stdout": proc.stdout.strip(),
                }
            return {
                "ok": False,
                "error": f"Script trả về mã lỗi {proc.returncode}: {proc.stderr.strip() or proc.stdout.strip()}",
            }
        except Exception as exc:
            return {"ok": False, "error": f"Lỗi khi xóa dữ liệu demo (--clean): {exc}"}

    # ==========================================================================
    # 3. THỰC THI CÁC BƯỚC KỊCH BẢN (B0 -> B15) & SUB-ACTIONS CHI TIẾT
    # ==========================================================================
    def execute_step_action(
        self,
        action_id: str,
        custom_payload: dict[str, Any] | None = None,
        _from_timeline: bool = False,
    ) -> dict[str, Any]:
        if not _from_timeline:
            with self.state_lock:
                if action_id in TIMELINE_INDEX_BY_ACTION:
                    self.timeline_index = TIMELINE_INDEX_BY_ACTION[action_id]
                    self.active_qa = None
                elif action_id in QA_ITEM_BY_ACTION:
                    self.active_qa = QA_ITEM_BY_ACTION[action_id]
            self.broadcast_state(busy=True, busy_label=f"Đang chạy {action_id}...", last_error="")

        try:
            res = self._execute_step_action_impl(action_id, custom_payload)
        except Exception as exc:
            # Lỗi bất ngờ không được để banner kẹt ở "Đang chạy..."
            res = {"ok": False, "error": f"Lỗi khi chạy {action_id}: {exc}"}

        if res.get("ok"):
            with self.state_lock:
                self.done_actions.add(action_id)
        if not _from_timeline:
            self.broadcast_state(
                busy=False,
                busy_label="",
                last_message=str(res.get("message", "")) if res.get("ok") else "",
                last_error="" if res.get("ok") else str(res.get("error", "")),
            )
        return res

    def _execute_step_action_impl(self, action_id: str, custom_payload: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = custom_payload or {}
        agency_id = self.ids["agency_id"]
        ws_id = self.ids["workspace_id"]
        task_id = self.ids["task_id"]
        survey_task_id = self.ids.get("survey_task_id", "2a100fd3-db57-3355-bef4-45dfbb4cf2f3")
        event_task_id = self.ids.get("event_task_id", "85a66c1c-b49b-3788-8bc3-a21336649041")
        workshop_task_id = self.ids.get("workshop_task_id", "c1176d26-249c-3d32-bbad-f720b3a518a4")
        press_task_id = self.ids.get("press_task_id", "b8585f25-6a26-3a5e-9199-19c2e9fb3f06")
        kol_task_id = self.ids.get("kol_task_id", "3f1ae3a9-6518-35df-a596-1013c055e279")
        newsletter_task_id = self.ids.get("newsletter_task_id", "b6a13469-05c4-3af0-88b1-ba2ca510d18f")
        video_task_id = self.ids.get("video_task_id", "31a69211-9cec-30f0-b3f0-4e01ac3315a1")

        # ----------------------------------------------------------------------
        # B0: Guest trình bày Trang chủ BrandHub công khai
        # ----------------------------------------------------------------------
        if action_id == "B0_GUEST_LANDING":
            res = self.login_role(
                "Guest",
                "/",
                "B0 - Trang chủ BrandHub (Khách truy cập công khai)",
            )
            return {
                **res,
                "message": "Đã mở Trang chủ BrandHub ở vai trò Guest (Khách truy cập công khai).",
            }

        # ----------------------------------------------------------------------
        # B1: Owner trình bày Danh mục 7 Gói truyền thông đa lĩnh vực của SE08 Digital Agency
        # ----------------------------------------------------------------------
        if action_id == "B1_NAV":
            res = self.login_role(
                "Owner",
                f"/agency/{agency_id}/media-packages",
                "B1.1 - Danh mục 7 Gói truyền thông Đa lĩnh vực",
            )
            return {
                **res,
                "message": "Đã mở Danh mục 7 Gói truyền thông đa ngành của SE08 Digital Agency (Owner: Lê Trí Trung).",
            }

        if action_id == "B1_NAV_WS_PACKAGE":
            res = self.login_role(
                "Owner",
                f"/workspaces/{ws_id}/media-package",
                "B1.2 - Gói Tuyển sinh ĐH FPT 2027 đã thương thảo & chốt trong Workspace",
            )
            return {
                **res,
                "message": "Đã mở Gói Tuyển sinh Đại học FPT 2027 (185 triệu VNĐ, 19 hạng mục) gắn trực tiếp với Workspace.",
            }

        # ----------------------------------------------------------------------
        # B2: Owner kiểm tra Workspace ĐH FPT Tuyển sinh 2027, Thư viện Key Visual & Chat nhóm
        # ----------------------------------------------------------------------
        if action_id == "B2_NAV":
            res = self.login_role(
                "Owner",
                f"/workspaces/{ws_id}/members",
                "B2.1 - Đội ngũ 5 Thành viên SE08 & Ban Tuyển sinh Đại học FPT",
            )
            return {
                **res,
                "message": "Đã mở danh sách thành viên Workspace Đại học FPT Tuyển sinh 2027 (đủ 5 thành viên SE08 & Ban Tuyển sinh).",
            }

        if action_id == "B2_NAV_CLIENT_PROFILE":
            res = self.login_role(
                "Owner",
                f"/workspaces/{ws_id}/clients",
                "B2.2 - Hồ sơ Thương hiệu (Brand Profile) Trường Đại học FPT",
            )
            try:
                driver = self.ensure_driver("Owner")
                wait = WebDriverWait(driver, 10)
                row = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//tr[.//text()[contains(., 'Ban Tuyển sinh Đại học FPT')]]")
                    )
                )
                row.click()
            except Exception:
                pass
            return {
                **res,
                "message": "Đã mở Hồ sơ Thương hiệu Đại học FPT (5 cơ sở đào tạo, học kỳ OJT và từ khóa hạn chế kiểm duyệt).",
            }

        if action_id == "B2_NAV_LIBRARY":
            res = self.login_role(
                "Creator",
                f"/workspaces/{ws_id}/library",
                "B2.3 - Thư viện 4 Thư mục Tuần, Mẫu bài & Bộ ảnh Key Visual Gemini",
            )
            return {
                **res,
                "message": "Đã mở Thư viện Tài nguyên (/library) với 4 thư mục tuần, 11 ảnh Key Visual Gemini Nano Banana + Unsplash và Mẫu bài viết.",
            }

        if action_id == "B2_NAV_CHAT":
            res = self.login_role(
                "Manager",
                f"/workspaces/{ws_id}/chat",
                "B2.4 - Trò chuyện phối hợp SE08 Digital & Ban Tuyển sinh ĐH FPT",
            )
            return {
                **res,
                "message": "Đã mở Kênh Trò chuyện nhóm (/chat) giữa SE08 Digital Agency và Ban Tuyển sinh Đại học FPT.",
            }

        # ----------------------------------------------------------------------
        # B3: Manager điều phối Chiến dịch 4 tuần (1. Thông tin, 2. 19 Công việc gói + Phát sinh, 3. 6 Đối tác)
        # ----------------------------------------------------------------------
        if action_id in ("B3_NAV", "B3_STEP_INFO"):
            res = self.login_role(
                "Manager",
                f"/workspaces/{ws_id}/campaigns",
                "B3.1 - Kế hoạch tổng thể 4 Tuần Tuyển sinh ĐH FPT 2027",
            )
            drv = self.drivers.get("Manager")
            if drv:
                time.sleep(0.8)
                try:
                    step1_btns = drv.find_elements(
                        By.XPATH,
                        "//button[contains(., 'Thông tin') or contains(., '1.')]",
                    )
                    if step1_btns:
                        drv.execute_script("arguments[0].click();", step1_btns[0])
                        time.sleep(0.4)
                    brief_cards = drv.find_elements(
                        By.XPATH,
                        "//*[contains(text(), 'Chiến lược') or contains(text(), 'Tuần 1') or contains(text(), 'Master Brief')]",
                    )
                    if brief_cards:
                        self.highlight_element(drv, brief_cards[0], "CHIẾN LƯỢC 4 TUẦN TUYỂN SINH ĐH FPT 2027")
                except Exception:
                    pass
            return {
                **res,
                "message": "Đã mở Bước 1 (Thông tin chiến dịch): lộ trình 4 tuần từ Coming Soon, Ngành học & Tiện ích, Workshop THPT đến Báo chí.",
            }

        if action_id == "B3_STEP_TASKS":
            res = self.login_role(
                "Manager",
                f"/workspaces/{ws_id}/campaigns",
                "B3.2 - Timeline 19 Hạng mục trong gói & Công việc phát sinh",
            )
            drv = self.drivers.get("Manager")
            if drv:
                time.sleep(0.8)
                try:
                    step2_btns = drv.find_elements(
                        By.XPATH,
                        "//button[contains(., 'Công việc') or contains(., '2.')]",
                    )
                    if step2_btns:
                        drv.execute_script("arguments[0].click();", step2_btns[0])
                        time.sleep(0.5)
                    oos_btns = drv.find_elements(
                        By.XPATH,
                        "//button[contains(., 'phát sinh') or contains(., 'Thêm công việc')]",
                    )
                    if oos_btns:
                        self.highlight_element(drv, oos_btns[0], "TIMELINE 4 TUẦN & THÊM CÔNG VIỆC PHÁT SINH")
                except Exception:
                    pass
            return {
                **res,
                "message": "Đã chuyển sang Bước 2 (Công việc): hiển thị đủ 19 hạng mục chuẩn của gói 4 tuần và nút Thêm công việc phát sinh.",
            }

        if action_id == "B3_FILL_OUT_OF_SCOPE":
            drv = self.ensure_driver("Manager")
            self.inject_role_Hud_badge(drv, "Manager", "B3.2 - Điền mẫu Công việc phát sinh ngoài gói")
            filled = []
            try:
                dialogs = drv.find_elements(By.CSS_SELECTOR, "[role='dialog']")
                if not dialogs:
                    oos_btns = drv.find_elements(
                        By.XPATH,
                        "//button[contains(., 'phát sinh') or contains(., 'Thêm công việc')]",
                    )
                    if oos_btns:
                        drv.execute_script("arguments[0].click();", oos_btns[0])
                        time.sleep(0.6)
                        dialogs = drv.find_elements(By.CSS_SELECTOR, "[role='dialog']")

                if dialogs:
                    dlg = dialogs[-1]
                    text_inputs = dlg.find_elements(By.CSS_SELECTOR, "input:not([type='datetime-local']):not([type='checkbox'])")
                    if text_inputs:
                        title_val = payload.get("out_of_scope_title", DEMO_TEXTS["out_of_scope_title"])
                        self.highlight_element(drv, text_inputs[0], "1. Tên công việc phát sinh")
                        self.react_set_value(drv, text_inputs[0], title_val, append=False, human_typing=True)
                        filled.append("Tên công việc phát sinh")
                        time.sleep(0.25)

                    dt_inputs = dlg.find_elements(By.CSS_SELECTOR, "input[type='datetime-local']")
                    if dt_inputs:
                        self.highlight_element(drv, dt_inputs[0], "2. Hạn xuất bản dự kiến")
                        self.react_set_value(drv, dt_inputs[0], "2027-05-12T10:00", append=False, human_typing=False)
                        filled.append("Hạn xuất bản")
                        time.sleep(0.2)

                    areas = dlg.find_elements(By.TAG_NAME, "textarea")
                    if len(areas) >= 1:
                        desc_val = payload.get("out_of_scope_desc", DEMO_TEXTS["out_of_scope_desc"])
                        self.highlight_element(drv, areas[0], "3. Mô tả công việc")
                        self.react_set_value(drv, areas[0], desc_val, append=False, human_typing=True)
                        filled.append("Mô tả công việc")
                        time.sleep(0.25)
                    if len(areas) >= 2:
                        crit_val = payload.get("out_of_scope_criteria", DEMO_TEXTS["out_of_scope_criteria"])
                        self.highlight_element(drv, areas[1], "4. Tiêu chí nghiệm thu")
                        self.react_set_value(drv, areas[1], crit_val, append=False, human_typing=True)
                        filled.append("Tiêu chí nghiệm thu")

                    submit_btns = dlg.find_elements(
                        By.XPATH,
                        ".//button[contains(., 'Tạo') or contains(., 'Lưu') or contains(., 'Thêm')]",
                    )
                    if submit_btns:
                        self.highlight_element(drv, submit_btns[-1], "5. BẤM ĐỂ TẠO (HOẶC ĐÓNG HỘP THOẠI)")
                return {
                    "ok": True,
                    "role": "Manager",
                    "filled_fields": filled,
                    "message": f"Đã điền tuần tự {len(filled)} trường trong hộp thoại Công việc phát sinh ngoài gói.",
                }
            except Exception as exc:
                return {"ok": False, "role": "Manager", "error": f"Lỗi khi điền Công việc phát sinh: {exc}"}

        if action_id == "B3_STEP_PARTNERS":
            res = self.login_role(
                "Manager",
                f"/workspaces/{ws_id}/campaigns",
                "B3.3 - 6 Đối tác Báo chí, Truyền hình, KOL & OOH",
            )
            drv = self.drivers.get("Manager")
            if drv:
                time.sleep(0.8)
                try:
                    step3_btns = drv.find_elements(
                        By.XPATH,
                        "//button[contains(., 'Đối tác') or contains(., '3.')]",
                    )
                    if step3_btns:
                        drv.execute_script("arguments[0].click();", step3_btns[0])
                        time.sleep(0.5)
                    deploy_btns = drv.find_elements(
                        By.XPATH,
                        "//button[contains(., 'Triển khai') or contains(., 'Deploy')]",
                    )
                    if deploy_btns:
                        self.highlight_element(drv, deploy_btns[0], "TRẠNG THÁI TRIỂN KHAI ĐỒNG BỘ CÔNG VIỆC")
                except Exception:
                    pass
            return {
                **res,
                "message": "Đã mở Bước 3 (Đối tác): hiển thị 6 đối tác VnExpress, Thanh Niên, Dân Trí, VTV1, Schannel và Hệ thống Màn hình LED THPT.",
            }

        # ----------------------------------------------------------------------
        # B4: Manager rà soát 20 Công việc 4 tuần, Khảo sát THPT & Yêu cầu từ Client
        # ----------------------------------------------------------------------
        if action_id == "B4_NAV":
            res = self.login_role(
                "Manager",
                f"/workspaces/{ws_id}/tasks",
                "B4.1 - 20 Công việc Chiến dịch 4 Tuần & 5 Subtask theo vai trò",
            )
            drv = self.drivers.get("Manager")
            if drv:
                time.sleep(1.0)
                try:
                    rows = drv.find_elements(
                        By.XPATH,
                        "//*[contains(text(), '[Tuần 3 - Bài trọng điểm]') or contains(text(), '[Tuần 3 - Bài trọng điểm]') or contains(text(), 'Điểm nhấn Chuỗi Workshop THPT')]",
                    )
                    if rows:
                        self.highlight_element(drv, rows[0], "BẤM ĐỂ MỞ BÀI TRỌNG ĐIỂM TUẦN 3 & SUBTASKS")
                        drv.execute_script("arguments[0].click();", rows[0])
                        time.sleep(0.7)
                        subtask_headings = drv.find_elements(
                            By.XPATH,
                            "//*[contains(text(), 'Công việc con') or contains(text(), 'Nghiên cứu') or contains(text(), 'Viết content')]",
                        )
                        if subtask_headings:
                            self.highlight_element(drv, subtask_headings[0], "5 SUBTASK PHỐI HỢP NHÓM SE_08")
                except Exception:
                    pass
            return {
                **res,
                "message": "Đã mở bảng 20 Công việc 4 tuần (Manager: Nguyễn Thành Lộc) và chọn bài trọng điểm Tuần 3.",
            }

        if action_id == "B4_FILL_SUBTASK":
            drv = self.ensure_driver("Manager")
            self.inject_role_Hud_badge(drv, "Manager", "B4.2 - Cập nhật mô tả & tiêu chí Subtask")
            filled = []
            try:
                edit_btns = drv.find_elements(
                    By.XPATH,
                    "//button[contains(@aria-label, 'Chỉnh sửa') or contains(., 'Chi tiết') or contains(., 'Sửa')]",
                )
                areas = drv.find_elements(By.TAG_NAME, "textarea")
                if not areas and edit_btns:
                    drv.execute_script("arguments[0].click();", edit_btns[0])
                    time.sleep(0.5)
                    areas = drv.find_elements(By.TAG_NAME, "textarea")

                if len(areas) >= 1:
                    self.highlight_element(drv, areas[0], "1. Mô tả công việc con (Subtask)")
                    self.react_set_value(
                        drv,
                        areas[0],
                        payload.get("subtask_desc", DEMO_TEXTS["subtask_desc"]),
                        append=False,
                        human_typing=True,
                    )
                    filled.append("Mô tả công việc con")
                    time.sleep(0.25)
                if len(areas) >= 2:
                    self.highlight_element(drv, areas[1], "2. Tiêu chí nghiệm thu Subtask")
                    self.react_set_value(
                        drv,
                        areas[1],
                        payload.get("subtask_criteria", DEMO_TEXTS["subtask_criteria"]),
                        append=False,
                        human_typing=True,
                    )
                    filled.append("Tiêu chí nghiệm thu Subtask")
                return {
                    "ok": True,
                    "role": "Manager",
                    "filled_fields": filled,
                    "message": f"Đã điền chi tiết Subtask ({len(filled)} trường) rõ ràng.",
                }
            except Exception as exc:
                return {"ok": False, "role": "Manager", "error": f"Không thể điền form Subtask: {exc}"}

        if action_id == "B4_NAV_SURVEYS":
            res = self.login_role(
                "Creator",
                f"/workspaces/{ws_id}/tasks/{survey_task_id}/survey",
                "B4.3 - Khảo sát Nguyện vọng Học sinh Lớp 12 (8 phản hồi thực tế)",
            )
            return {
                **res,
                "message": "Đã mở trình quản lý Khảo sát học sinh THPT (/tasks/.../survey) do Hà Văn Ân phụ trách với 8 câu trả lời thực tế.",
            }

        if action_id == "B4_NAV_REQUESTS":
            res = self.login_role(
                "Manager",
                f"/workspaces/{ws_id}/requests",
                "B4.4 - Yêu cầu Nội dung từ Ban Tuyển sinh Đại học FPT",
            )
            return {
                **res,
                "message": "Đã mở danh sách Yêu cầu nội dung (/requests) từ Ban Tuyển sinh ĐH FPT gửi nhóm SE08.",
            }

        # ----------------------------------------------------------------------
        # B5: Creator nhận việc & kiểm tra tiến độ Subtask
        # ----------------------------------------------------------------------
        if action_id == "B5_NAV":
            res = self.login_role(
                "Creator",
                f"/workspaces/{ws_id}/tasks",
                "B5 - Creator Nguyễn Chơn Phước nhận việc Tuần 3",
            )
            drv = self.drivers.get("Creator")
            if drv:
                time.sleep(1.0)
                try:
                    cards = drv.find_elements(
                        By.XPATH,
                        "//*[contains(text(), '[Tuần 3 - Bài trọng điểm]') or contains(text(), '[Tuần 3 - Bài trọng điểm]') or contains(text(), 'Điểm nhấn Chuỗi Workshop THPT')]",
                    )
                    if cards:
                        drv.execute_script("arguments[0].click();", cards[0])
                        time.sleep(0.7)
                    action_btns = drv.find_elements(
                        By.XPATH,
                        "//button[contains(., 'Bắt đầu làm') or contains(., 'Soạn bài viết') or contains(., 'Mở trình soạn thảo')]",
                    )
                    if action_btns:
                        self.highlight_element(drv, action_btns[0], "BẤM ĐỂ MỞ TRÌNH SOẠN THẢO HỢP NHẤT")
                except Exception:
                    pass
            return {
                **res,
                "message": "Đã mở trang Công việc của Creator (Nguyễn Chơn Phước) và chọn [Tuần 3 - Bài trọng điểm].",
            }

        # ----------------------------------------------------------------------
        # B6: Creator mở /editor, BẮN ẢNH KEY VISUAL GEMINI LÊN BÀI VIẾT & Gọi AI
        # ----------------------------------------------------------------------
        if action_id == "B6_NAV_EDITOR":
            res = self.login_role(
                "Creator",
                f"/workspaces/{ws_id}/editor?taskId={task_id}",
                "B6.1 - Trình soạn thảo hợp nhất (/editor)",
            )
            drv = self.drivers.get("Creator")
            if drv:
                time.sleep(1.1)
                try:
                    caption_sec = drv.find_elements(
                        By.CSS_SELECTOR,
                        "section[aria-labelledby='section-POST.CAPTION']",
                    )
                    if caption_sec:
                        self.highlight_element(drv, caption_sec[0], "PHẦN SOẠN NỘI DUNG BÀI ĐĂNG (POST.CAPTION)")
                except Exception:
                    pass
            return {
                **res,
                "message": "Đã mở Trình soạn thảo hợp nhất (/editor) của [Tuần 3 - Bài trọng điểm] (4 phần độc lập: BRIEF, MEDIA, CHANNELS, CAPTION).",
            }

        if action_id == "B6_PUSH_KEY_VISUAL":
            res = self.login_role(
                "Creator",
                f"/workspaces/{ws_id}/editor?taskId={task_id}",
                "B6.2 - Bắn trực tiếp ảnh Key Visual Gemini Nano Banana lên bài viết",
            )
            drv = self.drivers.get("Creator")
            if not drv:
                return {"ok": False, "role": "Creator", "error": "Chưa khởi tạo được trình duyệt Creator."}

            time.sleep(1.0)
            try:
                media_secs = drv.find_elements(By.CSS_SELECTOR, "section[aria-labelledby='section-POST.MEDIA']")
                media_scope = media_secs[0] if media_secs else drv

                repo_tabs = media_scope.find_elements(
                    By.XPATH,
                    ".//*[@role='tab' and (contains(., 'Kho tài nguyên') or contains(., 'Repository') or contains(., 'Thư viện'))]",
                )
                if not repo_tabs:
                    repo_tabs = drv.find_elements(
                        By.XPATH,
                        "//*[@role='tab' and (contains(., 'Kho tài nguyên') or contains(., 'Repository') or contains(., 'Thư viện'))]",
                    )

                if repo_tabs:
                    self.highlight_element(drv, repo_tabs[0], "1/2: MỞ KHO TÀI NGUYÊN KEY VISUAL GEMINI")
                    drv.execute_script("arguments[0].click();", repo_tabs[0])
                    time.sleep(0.9)

                # Chọn ảnh Key Visual Gemini Tuần 3 (Open Day hoặc Workshop THPT) trong Kho tài nguyên
                kv_cards = media_scope.find_elements(
                    By.XPATH,
                    ".//*[contains(text(), 'KV_Tuan3_FPTU_OpenDay_2027') or contains(text(), 'KV_Tuan3_Workshop_THPT')]/ancestor::button[1]"
                    " | .//button[.//*[contains(text(), 'KV_Tuan3_FPTU_OpenDay_2027') or contains(text(), 'KV_Tuan3_Workshop_THPT')]]"
                    " | .//*[contains(@title, 'KV_Tuan3_FPTU_OpenDay_2027') or contains(@title, 'KV_Tuan3_Workshop_THPT')]",
                )
                if not kv_cards:
                    # Fallback: chọn thẻ hình ảnh đầu tiên trong lưới Kho tài nguyên chưa được chọn
                    kv_cards = media_scope.find_elements(
                        By.XPATH,
                        ".//div[@role='tabpanel']//img/ancestor::*[self::button or self::div[@role='button']][1]",
                    )

                if kv_cards:
                    target_card = kv_cards[0]
                    self.highlight_element(drv, target_card, "2/2: ĐÃ BẮN ẢNH KEY VISUAL GEMINI LÊN KHUNG BÀI ĐĂNG!")
                    drv.execute_script("arguments[0].click();", target_card)
                    time.sleep(0.6)

                    # Nếu phần POST.MEDIA có nút Lưu thay đổi, làm nổi bật để người thuyết trình thấy rõ
                    save_media_btns = media_scope.find_elements(
                        By.XPATH,
                        ".//button[contains(., 'Lưu') or contains(., 'Save')]",
                    )
                    if save_media_btns:
                        self.highlight_element(drv, save_media_btns[0], "ẢNH ĐÃ LÊN BÀI! (TÙY CHỌN BẤM LƯU NẾU MUỐN CẬP NHẬT MEDIA)")

                    return {
                        "ok": True,
                        "role": "Creator",
                        "message": "Đã bắn trực tiếp ảnh Key Visual Gemini (KV_Tuan3_FPTU_OpenDay_2027) từ Kho tài nguyên lên bài viết và khung xem trước 4 nền tảng!",
                    }

                # Dự phòng nếu đang ở chế độ input[type='file']
                file_inputs = media_scope.find_elements(By.CSS_SELECTOR, "input[type='file']")
                local_kv = (
                    self.repo_root.parent
                    / "brandhub-web"
                    / "public"
                    / "demo-assets"
                    / "fptu-2027"
                    / "fptu-week3-openday-kol.jpg"
                )
                if file_inputs and local_kv.exists():
                    drv.execute_script("arguments[0].classList.remove('hidden'); arguments[0].style.display='block';", file_inputs[0])
                    file_inputs[0].send_keys(str(local_kv))
                    return {
                        "ok": True,
                        "role": "Creator",
                        "message": f"Đã đẩy trực tiếp file ảnh {local_kv.name} vào khung tải ảnh bài viết.",
                    }

                return {
                    "ok": True,
                    "role": "Creator",
                    "message": "Đã mở khu vực Hình ảnh (POST.MEDIA) trên Trình soạn thảo với bộ Key Visual Gemini sẵn sàng.",
                }
            except Exception as exc:
                return {"ok": False, "role": "Creator", "error": f"Lỗi khi bắn ảnh Key Visual lên bài viết: {exc}"}

        if action_id == "B6_TOGGLE_DOCS_MODE":
            drv = self.ensure_driver("Creator")
            self.inject_role_Hud_badge(drv, "Creator", "B6.3 - Chuyển đổi Chế độ Nhanh / Chế độ Tài liệu")
            try:
                mode_btns = drv.find_elements(
                    By.XPATH,
                    "//button[contains(., 'Tài liệu') or contains(., 'Docs') or contains(., 'Nhanh') or contains(., 'Quick')]",
                )
                if mode_btns:
                    target_btn = mode_btns[-1]
                    self.highlight_element(drv, target_btn, "CHUYỂN ĐỔI CHẾ ĐỘ SOẠN THẢO (QUICK / DOCS MODE)")
                    drv.execute_script("arguments[0].click();", target_btn)
                    return {
                        "ok": True,
                        "role": "Creator",
                        "message": "Đã chuyển đổi chế độ hiển thị trong Trình soạn thảo (/editor).",
                    }
                return {
                    "ok": True,
                    "role": "Creator",
                    "message": "Đang ở màn hình Trình soạn thảo (/editor).",
                }
            except Exception as exc:
                return {"ok": False, "role": "Creator", "error": f"Không thể chuyển chế độ soạn thảo: {exc}"}

        if action_id == "B6_FILL_BRIEF_SECTION":
            drv = self.ensure_driver("Creator")
            self.inject_role_Hud_badge(drv, "Creator", "B6 - Điền phần Nghiên cứu & Nguồn dẫn (POST.BRIEF)")
            filled = []
            try:
                brief_sec = drv.find_elements(By.CSS_SELECTOR, "section[aria-labelledby='section-POST.BRIEF']")
                container = brief_sec[0] if brief_sec else drv
                areas = container.find_elements(By.TAG_NAME, "textarea")
                if areas:
                    notes_val = payload.get("brief_notes", DEMO_TEXTS["brief_notes"])
                    self.highlight_element(drv, areas[0], "1. Ghi chú nghiên cứu (POST.BRIEF)")
                    self.react_set_value(drv, areas[0], notes_val, append=False, human_typing=True)
                    filled.append("Ghi chú nghiên cứu (POST.BRIEF)")
                    time.sleep(0.25)

                url_inputs = container.find_elements(By.CSS_SELECTOR, "input[type='url']")
                if url_inputs:
                    url_val = payload.get("brief_source_url", DEMO_TEXTS["brief_source_url"])
                    self.highlight_element(drv, url_inputs[0], "2. Đường dẫn nguồn tham khảo")
                    self.react_set_value(drv, url_inputs[0], url_val, append=False, human_typing=True)
                    filled.append("Nguồn dẫn tham khảo")

                return {
                    "ok": True,
                    "role": "Creator",
                    "filled_fields": filled,
                    "message": f"Đã điền phần Nghiên cứu thông tin (POST.BRIEF): {', '.join(filled) or 'đã duyệt sẵn'}.",
                }
            except Exception as exc:
                return {"ok": False, "role": "Creator", "error": f"Lỗi khi điền phần POST.BRIEF: {exc}"}

        if action_id == "B6_SEQ_FILL_AI":
            drv = self.ensure_driver("Creator")
            self.inject_role_Hud_badge(drv, "Creator", "B6.4 - Điền tuần tự 5 trường AI Tạo Caption")
            topic_text = payload.get("ai_topic", DEMO_TEXTS["ai_topic"])
            tone_label = payload.get("ai_tone_label", DEMO_TEXTS["ai_tone_label"])
            platform_label = payload.get("ai_platform_label", DEMO_TEXTS["ai_platform_label"])
            language_label = payload.get("ai_language_label", DEMO_TEXTS["ai_language_label"])
            hashtag_count = str(payload.get("ai_hashtag_count", DEMO_TEXTS["ai_hashtag_count"]))

            filled_steps: list[str] = []
            try:
                dialogs = drv.find_elements(By.CSS_SELECTOR, "[role='dialog']")
                if not dialogs:
                    ai_btns = drv.find_elements(
                        By.XPATH,
                        "//button[contains(., 'Tạo bằng AI') or contains(., 'AI') or contains(., 'Gợi ý')]",
                    )
                    if ai_btns:
                        drv.execute_script("arguments[0].click();", ai_btns[0])
                        time.sleep(0.6)
                        dialogs = drv.find_elements(By.CSS_SELECTOR, "[role='dialog']")

                container = dialogs[-1] if dialogs else drv

                topic_areas = container.find_elements(By.TAG_NAME, "textarea")
                if topic_areas:
                    self.highlight_element(drv, topic_areas[0], "1/5: Nhập Chủ đề bài viết (Topic)")
                    self.react_set_value(drv, topic_areas[0], topic_text, append=False, human_typing=True)
                    filled_steps.append("Chủ đề (Topic)")
                    time.sleep(0.3)

                combos = container.find_elements(By.CSS_SELECTOR, "button[role='combobox']")
                if len(combos) >= 1:
                    self.select_radix_combobox_by_label(drv, combos[0], tone_label)
                    filled_steps.append(f"Giọng điệu ({tone_label})")
                    time.sleep(0.22)
                if len(combos) >= 2:
                    self.select_radix_combobox_by_label(drv, combos[1], platform_label)
                    filled_steps.append(f"Nền tảng ({platform_label})")
                    time.sleep(0.22)
                if len(combos) >= 3:
                    self.select_radix_combobox_by_label(drv, combos[2], language_label)
                    filled_steps.append(f"Ngôn ngữ ({language_label})")
                    time.sleep(0.22)

                num_inputs = container.find_elements(By.CSS_SELECTOR, "input[type='number']")
                if num_inputs:
                    self.highlight_element(drv, num_inputs[0], f"5/5: Số lượng Hashtag ({hashtag_count})")
                    self.react_set_value(drv, num_inputs[0], hashtag_count, append=False, human_typing=False)
                    filled_steps.append(f"Số lượng Hashtag ({hashtag_count})")
                    time.sleep(0.25)

                gen_btns = container.find_elements(
                    By.XPATH,
                    ".//button[contains(., 'Tạo gợi ý') or contains(., 'Tạo nội dung') or contains(., 'Generate')]",
                )
                if gen_btns:
                    self.highlight_element(drv, gen_btns[0], "BẤM 'TẠO GỢI Ý' ĐỂ GỌI GEMINI AI")

                return {
                    "ok": True,
                    "role": "Creator",
                    "filled_fields": filled_steps,
                    "message": f"Đã điền tuần tự {len(filled_steps)} trường trong hộp thoại AI: {', '.join(filled_steps)}.",
                }
            except Exception as exc:
                return {"ok": False, "role": "Creator", "error": f"Lỗi khi điền hộp thoại AI: {exc}"}

        # ----------------------------------------------------------------------
        # B7: Kiểm tra vi phạm nội dung (3.6.33) & Gửi duyệt phần POST.CAPTION (v1)
        # ----------------------------------------------------------------------
        if action_id == "B7_FILL_VIOLATION":
            drv = self.ensure_driver("Creator")
            self.inject_role_Hud_badge(drv, "Creator", "B7.1 - Chèn câu vi phạm để test Bộ lọc An toàn")
            bad_text = payload.get("violation_sample", DEMO_TEXTS["violation_sample"])
            try:
                caption_sec = drv.find_elements(By.CSS_SELECTOR, "section[aria-labelledby='section-POST.CAPTION']")
                scope = caption_sec[0] if caption_sec else drv
                areas = scope.find_elements(By.TAG_NAME, "textarea") or drv.find_elements(By.TAG_NAME, "textarea")
                if not areas:
                    return {"ok": False, "role": "Creator", "error": "Không tìm thấy ô nội dung bài viết (textarea)."}
                self.highlight_element(drv, areas[0], "CHÈN CÂU VI PHẠM ĐỂ KIỂM THỬ")
                self.react_set_value(drv, areas[0], bad_text, append=True, human_typing=True)

                check_btns = drv.find_elements(
                    By.XPATH,
                    "//button[contains(., 'Kiểm tra vi phạm') or contains(., 'Kiểm duyệt') or contains(., 'Compliance')]",
                )
                if check_btns:
                    self.highlight_element(drv, check_btns[0], "BẤM 'KIỂM TRA VI PHẠM' (FR 3.6.33)")
                return {
                    "ok": True,
                    "role": "Creator",
                    "message": "Đã chèn đoạn văn chứa từ cấm vào bài viết. Hãy bấm 'Kiểm tra vi phạm' trên màn hình.",
                }
            except Exception as exc:
                return {"ok": False, "role": "Creator", "error": str(exc)}

        if action_id == "B7_CLEAN_AND_RESTORE":
            drv = self.ensure_driver("Creator")
            self.inject_role_Hud_badge(drv, "Creator", "B7.2 - Khôi phục bản thảo sạch v1 & Gửi duyệt phần POST.CAPTION")
            clean_v1 = payload.get("caption_v1_clean", DEMO_TEXTS["caption_v1_clean"])
            try:
                caption_sec = drv.find_elements(By.CSS_SELECTOR, "section[aria-labelledby='section-POST.CAPTION']")
                scope = caption_sec[0] if caption_sec else drv
                areas = scope.find_elements(By.TAG_NAME, "textarea") or drv.find_elements(By.TAG_NAME, "textarea")
                if not areas:
                    return {"ok": False, "role": "Creator", "error": "Không tìm thấy ô nội dung bài viết."}
                self.highlight_element(drv, areas[0], "KHÔI PHỤC NỘI DUNG CHUẨN V1 (TUYỂN SINH 2027)")
                self.react_set_value(drv, areas[0], clean_v1, append=False, human_typing=True)

                sec_submit_btns = scope.find_elements(
                    By.XPATH,
                    ".//button[contains(., 'Gửi duyệt') or contains(., 'Lưu')]",
                )
                if sec_submit_btns:
                    self.highlight_element(drv, sec_submit_btns[0], "BẤM 'LƯU' & 'GỬI DUYỆT' PHẦN NỘI DUNG (V1)")
                else:
                    submit_btns = drv.find_elements(
                        By.XPATH,
                        "//button[contains(., 'Gửi duyệt') or contains(., 'Lưu bản nháp')]",
                    )
                    if submit_btns:
                        self.highlight_element(drv, submit_btns[0], "BẤM 'LƯU' & 'GỬI DUYỆT' (V1)")
                return {
                    "ok": True,
                    "role": "Creator",
                    "message": "Đã điền bản thảo v1 sạch. Hãy bấm 'Lưu thay đổi' rồi bấm 'Gửi duyệt' trên phần Nội dung bài đăng.",
                }
            except Exception as exc:
                return {"ok": False, "role": "Creator", "error": str(exc)}

        # ----------------------------------------------------------------------
        # B8: Manager duyệt nội bộ (v1) trên /task-approvals
        # ----------------------------------------------------------------------
        if action_id == "B8_NAV_MANAGER_APPROVAL":
            res = self.login_role(
                "Manager",
                f"/workspaces/{ws_id}/task-approvals?task={task_id}",
                "B8 - Manager Nguyễn Thành Lộc duyệt nội bộ (v1)",
            )
            drv = self.drivers.get("Manager")
            if drv:
                time.sleep(1.0)
                try:
                    sec_cards = drv.find_elements(By.CSS_SELECTOR, "section[data-section-key='POST.CAPTION']")
                    scope = sec_cards[0] if sec_cards else drv
                    approve_btns = scope.find_elements(
                        By.XPATH,
                        ".//button[normalize-space(.)='Duyệt' or contains(., 'Duyệt nội bộ') or contains(., 'Phê duyệt')]",
                    )
                    if not approve_btns:
                        approve_btns = drv.find_elements(
                            By.XPATH,
                            "//button[normalize-space(.)='Duyệt' or contains(., 'Duyệt nội bộ') or contains(., 'Phê duyệt')]",
                        )
                    if approve_btns:
                        self.highlight_element(drv, approve_btns[0], "MANAGER: BẤM 'DUYỆT' PHẦN NỘI DUNG (V1)")
                except Exception:
                    pass
            return {
                **res,
                "message": "Đã mở Hàng đợi phê duyệt của Manager (Nguyễn Thành Lộc) tại [Tuần 3 - Bài trọng điểm].",
            }

        # ----------------------------------------------------------------------
        # B9: Client (Ban Tuyển sinh Đại học FPT) xem xét & Yêu cầu chỉnh sửa (v1)
        # ----------------------------------------------------------------------
        if action_id == "B9_NAV_CLIENT_APPROVAL":
            res = self.login_role(
                "Client",
                f"/workspaces/{ws_id}/task-approvals?task={task_id}",
                "B9 - Ban Tuyển sinh ĐH FPT nghiệm thu & Yêu cầu chỉnh sửa v1",
            )
            drv = self.drivers.get("Client")
            if drv:
                time.sleep(1.0)
                try:
                    sec_cards = drv.find_elements(By.CSS_SELECTOR, "section[data-section-key='POST.CAPTION']")
                    scope = sec_cards[0] if sec_cards else drv
                    ret_btns = scope.find_elements(
                        By.XPATH,
                        ".//button[contains(., 'Yêu cầu chỉnh sửa') or contains(., 'Trả về')]",
                    )
                    if not ret_btns:
                        ret_btns = drv.find_elements(
                            By.XPATH,
                            "//button[contains(., 'Yêu cầu chỉnh sửa') or contains(., 'Trả về')]",
                        )
                    if ret_btns:
                        self.highlight_element(drv, ret_btns[0], "CLIENT: BẤM 'YÊU CẦU CHỈNH SỬA'")
                except Exception:
                    pass
            return {
                **res,
                "message": "Đã mở màn hình Nghiệm thu của Client (Ban Tuyển sinh Đại học FPT).",
            }

        if action_id == "B9_SEQ_FILL_REJECT_REASON":
            drv = self.ensure_driver("Client")
            self.inject_role_Hud_badge(drv, "Client", "B9 - Điền lý do yêu cầu bổ sung Học bổng 2027 & OJT")
            reject_note = payload.get("client_reject_note", DEMO_TEXTS["client_reject_note"])
            try:
                note_inputs = drv.find_elements(By.CSS_SELECTOR, "[role='dialog'] textarea, #task-review-note")
                if not note_inputs:
                    sec_cards = drv.find_elements(By.CSS_SELECTOR, "section[data-section-key='POST.CAPTION']")
                    scope = sec_cards[0] if sec_cards else drv
                    ret_btns = scope.find_elements(
                        By.XPATH,
                        ".//button[contains(., 'Yêu cầu chỉnh sửa') or contains(., 'Trả về')]",
                    )
                    if not ret_btns:
                        ret_btns = drv.find_elements(
                            By.XPATH,
                            "//button[contains(., 'Yêu cầu chỉnh sửa') or contains(., 'Trả về')]",
                        )
                    if ret_btns:
                        drv.execute_script("arguments[0].click();", ret_btns[0])
                        time.sleep(0.5)
                        note_inputs = drv.find_elements(By.CSS_SELECTOR, "[role='dialog'] textarea, #task-review-note")

                if not note_inputs:
                    return {
                        "ok": False,
                        "role": "Client",
                        "error": "Không tìm thấy ô nhập Lý do yêu cầu chỉnh sửa. Hãy bấm nút 'Yêu cầu chỉnh sửa' trước.",
                    }

                target_area = note_inputs[-1]
                self.highlight_element(drv, target_area, "1/2: Nhập nhận xét của Ban Tuyển sinh Đại học FPT")
                self.react_set_value(drv, target_area, reject_note, append=False, human_typing=True)
                time.sleep(0.25)

                confirm_btns = drv.find_elements(
                    By.XPATH,
                    "//div[@role='dialog']//button[contains(., 'Yêu cầu chỉnh sửa') or contains(., 'Gửi') or contains(., 'Xác nhận')]",
                )
                if confirm_btns:
                    self.highlight_element(drv, confirm_btns[-1], "2/2: BẤM ĐỂ XÁC NHẬN TRẢ VỀ CHO CREATOR")

                return {
                    "ok": True,
                    "role": "Client",
                    "message": "Đã điền nhận xét của Ban Tuyển sinh ĐH FPT (bổ sung 3 mức học bổng 50%-70%-100% và kỳ thực tập OJT). Hãy bấm xác nhận.",
                }
            except Exception as exc:
                return {"ok": False, "role": "Client", "error": str(exc)}

        # ----------------------------------------------------------------------
        # B10: Creator cập nhật bản v2, gửi duyệt lại & mở Lịch sử phiên bản (Diff v1 vs v2)
        # ----------------------------------------------------------------------
        if action_id == "B10_NAV_CREATOR_FIX":
            res = self.login_role(
                "Creator",
                f"/workspaces/{ws_id}/editor?taskId={task_id}",
                "B10 - Creator xem phản hồi & cập nhật bản v2",
            )
            drv = self.drivers.get("Creator")
            if drv:
                time.sleep(1.0)
                try:
                    caption_sec = drv.find_elements(By.CSS_SELECTOR, "section[aria-labelledby='section-POST.CAPTION']")
                    if caption_sec:
                        self.highlight_element(drv, caption_sec[0], "PHẦN POST.CAPTION KÈM GÓP Ý CỦA BAN TUYỂN SINH ĐH FPT")
                except Exception:
                    pass
            return {
                **res,
                "message": "Đã mở lại Trình soạn thảo (/editor) của Creator để bổ sung thông tin Học bổng 2027 & OJT (v2).",
            }

        if action_id == "B10_SEQ_FILL_V2":
            drv = self.ensure_driver("Creator")
            self.inject_role_Hud_badge(drv, "Creator", "B10 - Bổ sung Học bổng 50%-100% & OJT học kỳ 6 (v2)")
            v2_addition = payload.get("caption_v2_addition", DEMO_TEXTS["caption_v2_addition"])
            try:
                caption_sec = drv.find_elements(By.CSS_SELECTOR, "section[aria-labelledby='section-POST.CAPTION']")
                scope = caption_sec[0] if caption_sec else drv
                areas = scope.find_elements(By.TAG_NAME, "textarea") or drv.find_elements(By.TAG_NAME, "textarea")
                if not areas:
                    return {"ok": False, "role": "Creator", "error": "Không tìm thấy ô soạn thảo bài viết."}

                self.highlight_element(drv, areas[0], "1/2: Bổ sung 3 mức Học bổng 2027 & kỳ OJT vào bản v2")
                self.react_set_value(drv, areas[0], v2_addition, append=True, human_typing=True)
                time.sleep(0.3)

                submit_btns = scope.find_elements(
                    By.XPATH,
                    ".//button[contains(., 'Gửi duyệt') or contains(., 'Lưu')]",
                )
                if submit_btns:
                    self.highlight_element(drv, submit_btns[0], "2/2: BẤM 'LƯU' & 'GỬI DUYỆT' BẢN V2")
                return {
                    "ok": True,
                    "role": "Creator",
                    "message": "Đã bổ sung chi tiết Học bổng Nguyễn Văn Đạo 2027 (50%, 70%, 100%) và kỳ thực tập OJT vào bài viết (v2).",
                }
            except Exception as exc:
                return {"ok": False, "role": "Creator", "error": str(exc)}

        if action_id == "B10_OPEN_VERSION_DIFF":
            drv = self.ensure_driver("Creator")
            self.inject_role_Hud_badge(drv, "Creator", "B10 - Mở Lịch sử phiên bản (So sánh Diff v1 vs v2)")
            try:
                caption_sec = drv.find_elements(By.CSS_SELECTOR, "section[aria-labelledby='section-POST.CAPTION']")
                scope = caption_sec[0] if caption_sec else drv
                hist_btns = scope.find_elements(
                    By.CSS_SELECTOR,
                    "button[aria-label='Lịch sử phiên bản'], button[title='Lịch sử phiên bản']",
                )
                if not hist_btns:
                    hist_btns = drv.find_elements(
                        By.CSS_SELECTOR,
                        "button[aria-label='Lịch sử phiên bản'], button[title='Lịch sử phiên bản']",
                    )
                if hist_btns:
                    self.highlight_element(drv, hist_btns[-1], "MỞ NGĂN ĐỐI CHIẾU PHIÊN BẢN V1 & V2")
                    drv.execute_script("arguments[0].click();", hist_btns[-1])
                    return {
                        "ok": True,
                        "role": "Creator",
                        "message": "Đã mở ngăn Lịch sử phiên bản (SectionVersionDrawer) để đối chiếu từng dòng thay đổi giữa v1 và v2.",
                    }
                return {
                    "ok": False,
                    "role": "Creator",
                    "error": "Chưa tìm thấy nút 'Lịch sử phiên bản' (cần gửi duyệt ít nhất 1 phiên bản trước).",
                }
            except Exception as exc:
                return {"ok": False, "role": "Creator", "error": str(exc)}

        # ----------------------------------------------------------------------
        # B11: Manager & Client phê duyệt hoàn tất bản v2
        # ----------------------------------------------------------------------
        if action_id == "B11_NAV_MANAGER_V2":
            res = self.login_role(
                "Manager",
                f"/workspaces/{ws_id}/task-approvals?task={task_id}",
                "B11.1 - Manager Nguyễn Thành Lộc duyệt nội bộ bản v2",
            )
            drv = self.drivers.get("Manager")
            if drv:
                time.sleep(0.9)
                try:
                    approve_btns = drv.find_elements(
                        By.XPATH,
                        "//button[normalize-space(.)='Duyệt' or contains(., 'Duyệt nội bộ') or contains(., 'Phê duyệt')]",
                    )
                    if approve_btns:
                        self.highlight_element(drv, approve_btns[0], "MANAGER: BẤM 'DUYỆT' BẢN V2")
                except Exception:
                    pass
            return {**res, "message": "Đã mở màn hình Manager để duyệt bản cập nhật v2."}

        if action_id == "B11_NAV_CLIENT_V2":
            res = self.login_role(
                "Client",
                f"/workspaces/{ws_id}/task-approvals?task={task_id}",
                "B11.2 - Ban Tuyển sinh ĐH FPT duyệt xuất bản chính thức (v2)",
            )
            drv = self.drivers.get("Client")
            if drv:
                time.sleep(0.9)
                try:
                    approve_btns = drv.find_elements(
                        By.XPATH,
                        "//button[normalize-space(.)='Duyệt' or contains(., 'Phê duyệt') or contains(., 'Đồng ý')]",
                    )
                    if approve_btns:
                        self.highlight_element(drv, approve_btns[0], "CLIENT: BẤM 'DUYỆT' HOÀN TẤT BÀI VIẾT")
                except Exception:
                    pass
            return {**res, "message": "Đã mở màn hình Client để phê duyệt chính thức bản v2 (Task chuyển sang FINISHED)."}

        # ----------------------------------------------------------------------
        # B12: Manager kiểm tra 4 Nền tảng MXH, Bộ Hashtag & Mẫu Email Workshop THPT
        # ----------------------------------------------------------------------
        if action_id == "B12_NAV_SOCIAL":
            res = self.login_role(
                "Manager",
                f"/workspaces/{ws_id}/social-accounts",
                "B12.1 - Kết nối 4 nền tảng: Facebook, Instagram, TikTok, Threads",
            )
            return {**res, "message": "Đã mở trang Quản lý Kết nối 4 Nền tảng Mạng xã hội (/social-accounts) của chiến dịch Đại học FPT 2027."}

        if action_id == "B12_NAV_HASHTAGS":
            res = self.login_role(
                "Manager",
                f"/workspaces/{ws_id}/library?tab=hashtags",
                "B12.2 - Bộ Hashtag bắt buộc Chiến dịch Tuyển sinh 2027",
            )
            return {**res, "message": "Đã mở trang Quản lý Bộ Hashtag chiến dịch (#DaiHocFPT, #TuyenSinhFPTU2027...)."}

        if action_id == "B12_NAV_MAIL_TEMPLATES":
            res = self.login_role(
                "Manager",
                f"/workspaces/{ws_id}/mail-templates",
                "B12.3 - Mẫu Email mời học sinh lớp 12 tham dự Workshop THPT",
            )
            return {**res, "message": "Đã mở trang Mẫu Email Block-Builder gửi vé mời dự chuỗi Workshop THPT 2027."}

        if action_id == "B12_NAV_MAIL_BATCHES":
            res = self.login_role(
                "Manager",
                f"/workspaces/{ws_id}/mail-templates/batches",
                "B12.4 - Lịch sử Lô gửi Email Vé mời Workshop THPT & Báo cáo Tuần",
            )
            return {**res, "message": "Đã mở trang Lịch sử Lô gửi Email (/mail-templates/batches) với 2 đợt gửi hoàn tất."}

        # ----------------------------------------------------------------------
        # B13: Creator xuất bản đa nền tảng, Xem Lịch đăng 4 tuần & Dashboard tương tác
        # ----------------------------------------------------------------------
        if action_id == "B13_NAV_PUBLISH":
            res = self.login_role(
                "Creator",
                f"/workspaces/{ws_id}/posts/dashboard",
                "B13.1 - Bảng điều phối Xuất bản Đa nền tảng (4 Tuần)",
            )
            drv = self.drivers.get("Creator")
            if drv:
                time.sleep(0.9)
                try:
                    pub_btns = drv.find_elements(
                        By.XPATH,
                        "//button[contains(., 'Đăng ngay') or contains(., 'Xuất bản') or contains(., 'Tạo bài viết')]",
                    )
                    if pub_btns:
                        self.highlight_element(drv, pub_btns[0], "HIỆU SUẤT & DANH SÁCH BÀI ĐĂNG 4 NỀN TẢNG")
                except Exception:
                    pass
            return {**res, "message": "Đã mở Bảng điều phối Bài đăng 4 tuần (/posts/dashboard) trên Facebook, Instagram, TikTok, Threads."}

        if action_id == "B13_NAV_CALENDAR":
            res = self.login_role(
                "Creator",
                f"/workspaces/{ws_id}/calendar",
                "B13.2 - Lịch xuất bản Chiến dịch Tuyển sinh 4 Tuần (/calendar)",
            )
            return {**res, "message": "Đã mở Lịch xuất bản trực quan (/calendar) hiển thị các bài đã đăng và lịch hẹn Tuần 4."}

        if action_id == "B13_NAV_DASHBOARD":
            res = self.login_role(
                "Creator",
                f"/workspaces/{ws_id}/dashboard",
                "B13.3 - Bảng điều khiển phân tích tương tác (Analytics)",
            )
            return {**res, "message": "Đã mở Dashboard phân tích số liệu Reach, Impressions và Reactions của chiến dịch."}

        # ----------------------------------------------------------------------
        # B14: Owner nâng cấp gói dịch vụ qua SePay (VietQR) & Ví AI Credit
        # ----------------------------------------------------------------------
        if action_id == "B14_NAV_PLANS":
            res = self.login_role(
                "Owner",
                "/subscription/plans",
                "B14.1 - Nâng cấp gói cước Agency qua SePay (VietQR)",
            )
            drv = self.drivers.get("Owner")
            if drv:
                time.sleep(0.9)
                try:
                    upg_btns = drv.find_elements(
                        By.XPATH,
                        "//button[contains(., 'Nâng cấp') or contains(., 'Chọn gói') or contains(., 'Enterprise')]",
                    )
                    if upg_btns:
                        self.highlight_element(drv, upg_btns[-1], "OWNER: BẤM 'NÂNG CẤP' ĐỂ TẠO MÃ VIETQR (SEPAY)")
                except Exception:
                    pass
            return {**res, "message": "Đã mở trang Nâng cấp gói dịch vụ (/subscription/plans) của SE08 Digital Agency."}

        if action_id == "B14_NAV_CREDITS":
            res = self.login_role(
                "Owner",
                f"/agency/{agency_id}/credit",
                "B14.2 - Ví AI Credit SE08 Digital Agency (8.500 điểm khả dụng)",
            )
            return {**res, "message": "Đã mở trang Quản lý Ví AI Credit và hạn mức phân bổ cho Workspace Đại học FPT 2027."}

        # ----------------------------------------------------------------------
        # B15: Admin giám sát doanh thu toàn nền tảng & Hàng đợi kiểm duyệt (3.10.4)
        # ----------------------------------------------------------------------
        if action_id == "B15_NAV_ADMIN_REVENUE":
            res = self.login_role(
                "Admin",
                "/admin?view=revenue",
                "B15.1 - Admin giám sát doanh thu & gói cước toàn hệ thống",
            )
            return {**res, "message": "Đã mở Dashboard Doanh thu toàn nền tảng (/admin?view=revenue) của Quản trị viên BrandHub."}

        if action_id == "B15_NAV_ADMIN_MODERATION":
            res = self.login_role(
                "Admin",
                "/admin?view=moderation",
                "B15.2 - Hàng đợi kiểm duyệt nội dung cộng đồng (FR 3.10.4)",
            )
            return {**res, "message": "Đã mở Hàng đợi Kiểm duyệt Nội dung Cộng đồng (/admin?view=moderation - FR 3.10.4)."}

        # ----------------------------------------------------------------------
        # Q&A HỘI ĐỒNG: TRUY CẬP NHANH CÁC TÍNH NĂNG CHUYÊN SÂU TRÊN TOÀN HỆ THỐNG
        # ----------------------------------------------------------------------
        qa_routes: dict[str, tuple[str, str, str, str]] = {
            "QA_EVENT_EDITOR": (
                "Creator",
                f"/workspaces/{ws_id}/tasks/{event_task_id}/event",
                "Q&A - Kế hoạch Sự kiện Ngày hội FPTU Open Day 2027",
                "Đã mở Trình điều phối Sự kiện Ngày hội FPTU Open Day 2027 (5 phân khu chuyên sâu).",
            ),
            "QA_WORKSHOP_EDITOR": (
                "Creator",
                f"/workspaces/{ws_id}/tasks/{workshop_task_id}/workshop",
                "Q&A - Điều phối Chuỗi Workshop Trải nghiệm THPT",
                "Đã mở Trình điều phối Workshop THPT (Diễn giả, Chương trình, Hậu cần & Biểu mẫu đăng ký).",
            ),
            "QA_PRESS_EDITOR": (
                "Creator",
                f"/workspaces/{ws_id}/tasks/{press_task_id}/press",
                "Q&A - Thông cáo Báo chí VnExpress Giáo dục",
                "Đã mở Trình biên tập Thông cáo Báo chí VnExpress, Danh sách phóng viên & Links tin bài.",
            ),
            "QA_KOL_EDITOR": (
                "Creator",
                f"/workspaces/{ws_id}/tasks/{kol_task_id}/kol",
                "Q&A - Booking KOL Duy Luân & Schannel Network",
                "Đã mở Trình quản lý Hợp tác KOL (Shortlist, Thỏa thuận chi phí, Bản nháp & Nghiệm thu số liệu).",
            ),
            "QA_NEWSLETTER_EDITOR": (
                "Creator",
                f"/workspaces/{ws_id}/tasks/{newsletter_task_id}/newsletter",
                "Q&A - Thiết kế Bản tin Email Khối Kéo-Thả",
                "Đã mở Trình thiết kế Bản tin Email Cẩm nang ngành học 2027 & Vé mời Workshop.",
            ),
            "QA_VIDEO_EDITOR": (
                "Creator",
                f"/workspaces/{ws_id}/editor?taskId={video_task_id}",
                "Q&A - Video ngắn Reels/TikTok Recap học sinh",
                "Đã mở Trình soạn Video ngắn (Kịch bản, Quay, Dựng, Caption & Kênh đăng).",
            ),
            "QA_AI_TRENDS": (
                "Manager",
                "/ai-studio/trends",
                "Q&A - Trạm Phân tích Xu hướng Mạng xã hội (Redis Live)",
                "Đã mở AI Studio Xu hướng (/ai-studio/trends) với 6 chủ đề mùa tuyển sinh 2027 nạp trực tiếp từ Redis.",
            ),
            "QA_AI_RAG": (
                "Manager",
                "/ai-studio/knowledge-base",
                "Q&A - Kho Tri thức Thương hiệu RAG Đại học FPT 2027",
                "Đã mở Kho Tri thức AI RAG (/ai-studio/knowledge-base) của Trường Đại học FPT.",
            ),
            "QA_AI_AMBASSADORS": (
                "Creator",
                "/ai-studio/ambassadors",
                "Q&A - Đại sứ Thương hiệu AI Khóa K23 (Minh Anh & Hoàng Khôi)",
                "Đã mở AI Studio Đại sứ ảo (/ai-studio/ambassadors) với 2 nhân vật đại diện mùa tuyển sinh 2027.",
            ),
            "QA_CLIENT_PORTAL": (
                "Client",
                f"/workspaces/{ws_id}/portal",
                "Q&A - Cổng Nghiệm thu Dành riêng cho Khách hàng (/portal)",
                "Đã mở Cổng Khách hàng (/portal) của Ban Tuyển sinh ĐH FPT với 2 hạng mục Open Day đang chờ duyệt.",
            ),
            "QA_CLIENT_VAULT": (
                "Client",
                f"/workspaces/{ws_id}/library",
                "Q&A - Kho Lưu trữ Riêng của Khách hàng (Client Vault)",
                "Đã mở Thư viện dưới góc nhìn Client với Kho Lưu trữ Riêng của ĐH FPT chia sẻ sang SE08.",
            ),
            "QA_COLLABORATORS": (
                "Owner",
                f"/agency/{agency_id}/collaborators",
                "Q&A - Danh bạ 10 Đối tác Báo chí, Truyền hình & KOL",
                "Đã mở Danh bạ Đối tác của SE08 Digital Agency (10 đơn vị báo chí, KOL và sản xuất đã chuẩn hóa).",
            ),
            "QA_PUBLIC_PACKAGE": (
                "Guest",
                "/packages/share/goi-tuyen-sinh-dh-fpt-2027",
                "Q&A - Đường dẫn Công khai Chia sẻ Gói Truyền thông (Guest)",
                "Đã mở trang Chào giá Gói Truyền thông Công khai trên cửa sổ Guest (/packages/share/goi-tuyen-sinh-dh-fpt-2027).",
            ),
            "QA_PUBLIC_SURVEY": (
                "Guest",
                "/public/surveys/khao-sat-chon-nganh-fptu-2027",
                "Q&A - Biểu mẫu Khảo sát Công khai dành cho Học sinh Lớp 12 (Guest)",
                "Đã mở trang Khảo sát Công khai trên cửa sổ Guest (/public/surveys/khao-sat-chon-nganh-fptu-2027).",
            ),
            "QA_ADMIN_CREDIT_PRICES": (
                "Admin",
                "/admin/credit-prices",
                "Q&A - Cấu hình Bảng giá Tín dụng AI toàn hệ thống",
                "Đã mở trang Quản trị Bảng giá AI Credit (/admin/credit-prices) với đủ 7 nghiệp vụ AI.",
            ),
        }
        step_editor_aliases = {
            "B4_NAV_EVENT": "QA_EVENT_EDITOR",
            "B4_NAV_WORKSHOP": "QA_WORKSHOP_EDITOR",
            "B5_NAV_VIDEO": "QA_VIDEO_EDITOR",
            "B5_NAV_KOL": "QA_KOL_EDITOR",
            "B12_NAV_NEWSLETTER": "QA_NEWSLETTER_EDITOR",
            "B13_NAV_PRESS": "QA_PRESS_EDITOR",
        }
        action_id = step_editor_aliases.get(action_id, action_id)
        if action_id in qa_routes:
            qa_role, qa_path, qa_hud, qa_msg = qa_routes[action_id]
            res = self.login_role(qa_role, qa_path, qa_hud)
            return {**res, "message": qa_msg}

        return {"ok": False, "error": f"Mã hành động không xác định: {action_id}"}

    def get_status(self) -> dict[str, Any]:
        roles_status = {}
        for role in CANONICAL_ROLE_ORDER:
            info = ROLE_PROFILES[role]
            alive = self._is_alive(role)
            url = ""
            if alive:
                try:
                    url = self.drivers[role].current_url
                except Exception:
                    alive = False
            roles_status[role] = {
                "alive": alive,
                "email": info["email"],
                "full_name": info["full_name"],
                "badge_color": info["badge_color"],
                "current_url": url,
            }
        return {
            "ok": True,
            "app_url": self.app_url,
            "window_mode": self.window_mode,
            "ws_clients": self.ws_hub.client_count(),
            "ws_roles": self.ws_hub.connected_roles(),
            "ids": self.ids,
            "texts": DEMO_TEXTS,
            "roles": roles_status,
            "sync": self.get_sync_state(),
        }


# ==============================================================================
# 3. HTTP + WEBSOCKET SERVER PHỤC VỤ GIAO DIỆN ĐIỀU KHIỂN & 6 CỬA SỔ CHROME (:3999)
# ==============================================================================
CONTROLLER: DemoBrowserController | None = None
_PRIMARY_HTML = Path(__file__).resolve().parents[2] / "public" / "demo" / "demo_flow_navigator.html"
_LOCAL_HTML = Path(__file__).resolve().parent / "demo_flow_navigator.html"
HTML_FILE_PATH = _PRIMARY_HTML if _PRIMARY_HTML.exists() else _LOCAL_HTML


class DemoMonitorHTTPServer(ThreadingHTTPServer):
    allow_reuse_address = True
    daemon_threads = True


class DemoMonitorRequestHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _send_json(self, data: dict[str, Any], status: int = 200) -> None:
        raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _handle_websocket(self) -> None:
        assert CONTROLLER is not None
        ws_key = (self.headers.get("Sec-WebSocket-Key") or "").strip()
        if not ws_key:
            self.send_error(400, "Missing Sec-WebSocket-Key")
            return

        accept = base64.b64encode(
            hashlib.sha1((ws_key + _WS_GUID).encode("ascii")).digest()
        ).decode("ascii")
        handshake = (
            "HTTP/1.1 101 Switching Protocols\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Accept: {accept}\r\n"
            "\r\n"
        ).encode("ascii")

        self.close_connection = True
        try:
            self.connection.sendall(handshake)
        except OSError:
            return

        self.connection.settimeout(None)
        client = CONTROLLER.ws_hub.register(self.connection)
        try:
            # Gửi trạng thái đồng bộ hiện tại ngay khi kết nối thành công
            client.send_json(CONTROLLER.get_sync_state())

            while True:
                frame = _ws_read_frame(self.connection)
                if frame is None:
                    break
                opcode, data = frame
                if opcode == 0x8:  # Close
                    client.send_raw(_ws_encode_frame(b"", opcode=0x8))
                    break
                if opcode == 0x9:  # Ping
                    client.send_raw(_ws_encode_frame(data, opcode=0xA))
                    continue
                if opcode == 0xA:  # Pong
                    continue
                if opcode == 0x1:  # Text JSON
                    try:
                        msg = json.loads(data.decode("utf-8"))
                    except Exception:
                        continue
                    if not isinstance(msg, dict):
                        continue
                    mtype = msg.get("type", "")
                    if mtype == "ping":
                        client.send_json({"type": "pong"})
                    elif mtype == "hello":
                        wrole = str(msg.get("window_role", "")).strip()
                        if wrole:
                            CONTROLLER.ws_hub.set_role(client, wrole)
                        CONTROLLER.ws_hub.broadcast(CONTROLLER.get_sync_state())
                    else:
                        CONTROLLER.handle_hud_command(msg)
        finally:
            CONTROLLER.ws_hub.unregister(client)
            try:
                CONTROLLER.ws_hub.broadcast(CONTROLLER.get_sync_state())
            except Exception:
                pass

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/ws" and "websocket" in (self.headers.get("Upgrade") or "").lower():
            self._handle_websocket()
            return

        if parsed.path in ("/", "/index.html", "/demo"):
            if HTML_FILE_PATH.exists():
                raw = HTML_FILE_PATH.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Cache-Control", "no-store")
                self.send_header("Content-Length", str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)
                return
            self._send_json({"ok": False, "error": f"Không tìm thấy file giao diện: {HTML_FILE_PATH}"}, 404)
            return

        if parsed.path == "/api/status":
            assert CONTROLLER is not None
            self._send_json(CONTROLLER.get_status())
            return

        if parsed.path == "/api/hud/state":
            assert CONTROLLER is not None
            self._send_json(CONTROLLER.get_sync_state())
            return

        if parsed.path == "/api/hud.js":
            assert CONTROLLER is not None
            role_q = "Guest"
            if parsed.query:
                for pair in parsed.query.split("&"):
                    if pair.startswith("role="):
                        cand = pair.split("=", 1)[1]
                        if cand in ROLE_PROFILES:
                            role_q = cand
            raw = build_hud_script(role_q, CONTROLLER.monitor_port).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/javascript; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
            return

        self._send_json({"ok": False, "error": "Not found"}, 404)

    def do_POST(self) -> None:
        assert CONTROLLER is not None
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", "0"))
        body_raw = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        try:
            body = json.loads(body_raw) if body_raw else {}
        except json.JSONDecodeError:
            body = {}

        try:
            self._handle_post(parsed, body)
        except Exception as exc:
            # Không để handler chết im lặng (trình duyệt chỉ thấy "Không kết nối được tới máy chủ Selenium")
            first_line = (str(exc).strip().splitlines() or [type(exc).__name__])[0]
            hint = " — Web localhost:3000 chưa chạy?" if "ERR_CONNECTION_REFUSED" in first_line else ""
            self._send_json({"ok": False, "error": f"Lỗi máy chủ demo: {first_line}{hint}"}, 500)

    def _handle_post(self, parsed: Any, body: dict[str, Any]) -> None:
        if parsed.path == "/api/hud/command":
            res = CONTROLLER.handle_hud_command(body)
            self._send_json(res)
            return

        if parsed.path == "/api/config":
            for k in ("agency_id", "workspace_id", "package_id", "ws_package_id", "campaign_id", "task_id"):
                if body.get(k):
                    CONTROLLER.ids[k] = str(body[k]).strip()
            if body.get("app_url"):
                CONTROLLER.app_url = str(body["app_url"]).rstrip("/")
            self._send_json({"ok": True, "ids": CONTROLLER.ids, "app_url": CONTROLLER.app_url})
            return

        if parsed.path == "/api/login-role":
            role = body.get("role", "Owner")
            route = body.get("route")
            step_label = body.get("step_label", "")
            res = CONTROLLER.login_role(role, route, step_label)
            self._send_json(res)
            return

        if parsed.path == "/api/login-all":
            results = CONTROLLER.login_all_roles()
            self._send_json({"ok": True, "results": results})
            return

        if parsed.path == "/api/reset-data":
            res = CONTROLLER.reset_demo_database_data()
            self._send_json(res)
            return

        if parsed.path == "/api/clean-data":
            res = CONTROLLER.clean_demo_database_data()
            self._send_json(res)
            return

        if parsed.path == "/api/arrange-windows":
            mode = str(body.get("mode", "split")).strip()
            res = CONTROLLER.arrange_windows(mode)
            self._send_json(res)
            return

        if parsed.path == "/api/step-action":
            action_id = body.get("action_id", "")
            custom_payload = body.get("payload", {})
            res = CONTROLLER.execute_step_action(action_id, custom_payload)
            self._send_json(res)
            return

        self._send_json({"ok": False, "error": f"Unknown endpoint: {parsed.path}"}, 404)

    def log_message(self, fmt: str, *args: Any) -> None:
        return


def main() -> None:
    global CONTROLLER
    parser = argparse.ArgumentParser(description="BrandHub Live Demo Monitor (Selenium 4 + WebSocket Sync)")
    parser.add_argument("--app-url", default=DEFAULT_APP_URL, help="URL của ứng dụng BrandHub Web (mặc định: http://localhost:3000)")
    parser.add_argument("--port", type=int, default=DEFAULT_MONITOR_PORT, help="Cổng của Bàn điều khiển Demo (mặc định: 3999)")
    parser.add_argument("--password", default=DEFAULT_PASSWORD, help="Mật khẩu chung của các tài khoản demo")
    args = parser.parse_args()

    CONTROLLER = DemoBrowserController(app_url=args.app_url, password=args.password, monitor_port=args.port)
    server = DemoMonitorHTTPServer(("127.0.0.1", args.port), DemoMonitorRequestHandler)

    print("=" * 78)
    print("  BRANDHUB LIVE DEMO MONITOR - 6 CANONICAL ROLES + WEBSOCKET HUD SYNC")
    print("=" * 78)
    print(f"  - BrandHub Web App URL : {args.app_url}")
    print(f"  - Bàn điều khiển HTML  : http://localhost:{args.port}")
    print(f"  - Cổng API điều khiển  : http://localhost:{args.port}/api/status")
    print(f"  - WebSocket đồng bộ HUD: ws://127.0.0.1:{args.port}/ws")
    print("=" * 78)
    print(f"Running on http://127.0.0.1:{args.port} (Press CTRL+C to quit)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Đang đóng Bàn điều khiển Demo...")
        server.server_close()


if __name__ == "__main__":
    main()
