#!/usr/bin/env python3
"""
================================================================================
BRANDHUB LIVE DEMO MONITOR (SELENIUM 4 MULTI-ROLE CONTROLLER + QUICK FILL)
================================================================================
Công cụ điều khiển trình duyệt trực tiếp phục vụ buổi bảo vệ Đồ án Tốt nghiệp
của nhóm SE_08 triển khai Chiến dịch Tuyển sinh Đại học FPT 2027 (4 Tuần):
  - Quản lý 5 cửa sổ Chrome độc lập ứng với 5 Canonical Roles:
    Owner (Lê Trí Trung), Manager (Nguyễn Thành Lộc), Creator (Nguyễn Chơn Phước),
    Client (Ban Tuyển sinh Đại học FPT), Admin (Quản trị viên BrandHub).
  - Tự động đăng nhập cả 5 tài khoản chỉ với 1 nút bấm (tự động dự phòng mật khẩu).
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
import json
import os
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

try:
    from selenium import webdriver
    from selenium.common.exceptions import WebDriverException
    from selenium.webdriver.chrome.options import Options
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
}

ROLE_PROFILES: dict[str, dict[str, str]] = {
    "Owner": {
        "role": "Owner",
        "code": "OWNER",
        "full_name": "Lê Trí Trung",
        "email": "user177@demo.brandhub.test",
        "badge_color": "#EA580C",
        "default_route": "/agency/{agency_id}/media-packages",
    },
    "Manager": {
        "role": "Manager",
        "code": "MANAGER",
        "full_name": "Nguyễn Thành Lộc",
        "email": "user1@demo.brandhub.test",
        "badge_color": "#EA580C",
        "default_route": "/workspaces/{workspace_id}/campaigns",
    },
    "Creator": {
        "role": "Creator",
        "code": "CREATOR",
        "full_name": "Nguyễn Chơn Phước",
        "email": "user13@demo.brandhub.test",
        "badge_color": "#EA580C",
        "default_route": "/workspaces/{workspace_id}/tasks",
    },
    "Client": {
        "role": "Client",
        "code": "CLIENT",
        "full_name": "Ban Tuyển sinh Đại học FPT",
        "email": "user59@demo.brandhub.test",
        "badge_color": "#EA580C",
        "default_route": "/workspaces/{workspace_id}/task-approvals",
    },
    "Admin": {
        "role": "Admin",
        "code": "ADMIN",
        "full_name": "Quản trị viên BrandHub",
        "email": "admin@demo.brandhub.test",
        "badge_color": "#EA580C",
        "default_route": "/admin?view=revenue",
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
# 2. SELENIUM BROWSER CONTROLLER
# ==============================================================================
class DemoBrowserController:
    def __init__(self, app_url: str, password: str) -> None:
        self.app_url = app_url.rstrip("/")
        self.password = password
        self.ids = dict(DEFAULT_IDS)
        self.drivers: dict[str, webdriver.Chrome] = {}
        self.window_mode: str = "normal"
        self.lock = threading.Lock()
        self.profile_base_dir = Path.home() / ".brandhub_demo_chrome_profiles"
        self.profile_base_dir.mkdir(parents=True, exist_ok=True)
        self.repo_root = Path(__file__).resolve().parents[2]
        self.prep_script_path = Path(__file__).resolve().parent / "prepare_demo_data_template.py"

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
            return False

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

        driver = webdriver.Chrome(options=opts)
        self.drivers[role] = driver
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

    def bring_to_front(self, driver: webdriver.Chrome) -> None:
        try:
            driver.switch_to.window(driver.current_window_handle)
        except Exception:
            pass
        try:
            driver.execute_cdp_cmd("Page.bringToFront", {})
        except Exception:
            pass
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
            msg = f"Đã phóng to toàn màn hình {updated} cửa sổ Chrome."
        else:
            msg = f"Đã chuyển về kích thước tiêu chuẩn cho {updated} cửa sổ Chrome."
        return {"ok": True, "window_mode": self.window_mode, "updated": updated, "message": msg}

    def inject_role_Hud_badge(self, driver: webdriver.Chrome, role: str, step_label: str = "") -> None:
        self.bring_to_front(driver)
        info = ROLE_PROFILES[role]
        js = """
        (function(role, name, email, stepLabel) {
            const old = document.getElementById('bh-demo-hud-badge');
            if (old) old.remove();
            const el = document.createElement('div');
            el.id = 'bh-demo-hud-badge';
            el.style.cssText = [
                'position:fixed',
                'bottom:16px',
                'left:16px',
                'z-index:2147483647',
                'background:#FFFFFF',
                'color:#0F172A',
                'padding:8px 14px',
                'border-radius:10px',
                'font-family:Inter,system-ui,-apple-system,sans-serif',
                'font-size:12px',
                'box-shadow:0 10px 25px rgba(15,23,42,0.12)',
                'border:1px solid #FED7AA',
                'border-left:5px solid #EA580C',
                'pointer-events:none',
                'display:flex',
                'align-items:center',
                'gap:10px'
            ].join(';');
            el.innerHTML = `
                <span style="background:#EA580C;color:#fff;font-weight:800;padding:2px 8px;border-radius:6px;letter-spacing:0.4px;text-transform:uppercase;font-size:11px;">${role}</span>
                <span style="font-weight:700;color:#0F172A;">${name}</span>
                <span style="color:#64748B;">(${email})</span>
                ${stepLabel ? `<span style="background:#FFF7ED;color:#C2410C;border:1px solid #FDBA74;padding:2px 8px;border-radius:6px;font-weight:700;">${stepLabel}</span>` : ''}
            `;
            document.body.appendChild(el);
        })(arguments[0], arguments[1], arguments[2], arguments[3]);
        """
        try:
            driver.execute_script(js, info["role"], info["full_name"], info["email"], step_label)
        except Exception:
            pass

    def highlight_element(
        self,
        driver: webdriver.Chrome,
        element,
        label: str = "THAO TÁC TẠI ĐÂY",
        color: str = "#EA580C",
    ) -> None:
        """Cuộn tới phần tử và tạo viền cam nổi bật chuẩn tông Trắng - Cam."""
        js = """
        const el = arguments[0];
        const label = arguments[1];
        const color = '#EA580C';
        if (!el) return;
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        el.style.transition = 'all 0.25s ease';
        el.style.outline = `3px solid ${color}`;
        el.style.outlineOffset = '3px';
        el.style.boxShadow = '0 0 0 6px rgba(234,88,12,0.18), 0 8px 20px rgba(234,88,12,0.22)';

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
            'z-index:2147483647',
            `background:${color}`,
            'color:#fff',
            'font-family:Inter,system-ui,-apple-system,sans-serif',
            'font-size:11px',
            'font-weight:800',
            'padding:4px 10px',
            'border-radius:6px',
            'box-shadow:0 4px 12px rgba(234,88,12,0.35)',
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
            dest_route = self.format_route(target_route or info["default_route"])
            dest_url = f"{self.app_url}{dest_route}"

            driver.get(dest_url)
            time.sleep(1.0)

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

            self.bring_to_front(driver)
            self.inject_role_Hud_badge(driver, role, step_label)
            return {
                "ok": True,
                "role": role,
                "email": info["email"],
                "full_name": info["full_name"],
                "current_url": driver.current_url,
            }

    def login_all_roles(self) -> list[dict[str, Any]]:
        results = []
        for role in ["Owner", "Manager", "Creator", "Client", "Admin"]:
            res = self.login_role(role, step_label="Sẵn sàng bảo vệ đồ án")
            results.append(res)
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
            for drv in list(self.drivers.values()):
                if not self.is_driver_alive(drv):
                    continue
                try:
                    drv.execute_script(js_clean, mode)
                    drv.refresh()
                    refreshed += 1
                except Exception:
                    pass
        return refreshed

    def reset_demo_database_data(self) -> dict[str, Any]:
        if not self.prep_script_path.exists():
            return {"ok": False, "error": f"Không tìm thấy script: {self.prep_script_path}"}
        try:
            proc = subprocess.run(
                [sys.executable, "-X", "utf8", str(self.prep_script_path), "--apply"],
                cwd=str(self.prep_script_path.parent),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=60,
            )
            if proc.returncode == 0:
                refreshed = self._sync_open_browsers_storage("reset")
                extra = f" (đã làm mới {refreshed} cửa sổ Chrome)" if refreshed > 0 else ""
                return {
                    "ok": True,
                    "message": (
                        "Đã nạp lại dữ liệu chuẩn trên PostgreSQL, MongoDB và Redis: SE08 Digital Agency, "
                        f"7 Gói đa lĩnh vực, Chiến dịch ĐH FPT 2027 (4 tuần, 20 công việc){extra}."
                    ),
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
            proc = subprocess.run(
                [sys.executable, "-X", "utf8", str(self.prep_script_path), "--clean"],
                cwd=str(self.prep_script_path.parent),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=60,
            )
            if proc.returncode == 0:
                refreshed = self._sync_open_browsers_storage("clean")
                extra = f" và làm mới {refreshed} cửa sổ Chrome" if refreshed > 0 else ""
                return {
                    "ok": True,
                    "message": (
                        "Đã xóa sạch toàn bộ dữ liệu mẫu cùng các bản ghi phát sinh sau buổi demo "
                        f"trên PostgreSQL, MongoDB, Redis{extra}."
                    ),
                    "stdout": proc.stdout.strip(),
                }
            return {
                "ok": False,
                "error": f"Script trả về mã lỗi {proc.returncode}: {proc.stderr.strip() or proc.stdout.strip()}",
            }
        except Exception as exc:
            return {"ok": False, "error": f"Lỗi khi xóa dữ liệu demo (--clean): {exc}"}

    # ==========================================================================
    # 3. THỰC THI CÁC BƯỚC KỊCH BẢN (B1 -> B15) & SUB-ACTIONS CHI TIẾT
    # ==========================================================================
    def execute_step_action(self, action_id: str, custom_payload: dict[str, Any] | None = None) -> dict[str, Any]:
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
                f"/workspaces/{ws_id}/client-profile",
                "B2.2 - Hồ sơ Thương hiệu (Brand Profile) Trường Đại học FPT",
            )
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
                "Manager",
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
                "Manager",
                f"/workspaces/{ws_id}/tasks/{event_task_id}/event",
                "Q&A - Kế hoạch Sự kiện Ngày hội FPTU Open Day 2027",
                "Đã mở Trình điều phối Sự kiện Ngày hội FPTU Open Day 2027 (5 phân khu chuyên sâu).",
            ),
            "QA_WORKSHOP_EDITOR": (
                "Manager",
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
                "Manager",
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
                "Owner",
                "/packages/share/goi-tuyen-sinh-dh-fpt-2027",
                "Q&A - Đường dẫn Công khai Chia sẻ Gói Truyền thông cho Khách hàng",
                "Đã mở trang Chào giá Gói Truyền thông Công khai (/packages/share/goi-tuyen-sinh-dh-fpt-2027).",
            ),
            "QA_PUBLIC_SURVEY": (
                "Client",
                "/public/surveys/khao-sat-chon-nganh-fptu-2027",
                "Q&A - Biểu mẫu Khảo sát Công khai dành cho Học sinh Lớp 12",
                "Đã mở trang Khảo sát Công khai dành cho học sinh THPT (/public/surveys/khao-sat-chon-nganh-fptu-2027).",
            ),
            "QA_ADMIN_CREDIT_PRICES": (
                "Admin",
                "/admin/credit-prices",
                "Q&A - Cấu hình Bảng giá Tín dụng AI toàn hệ thống",
                "Đã mở trang Quản trị Bảng giá AI Credit (/admin/credit-prices) với đủ 7 nghiệp vụ AI.",
            ),
        }
        if action_id in qa_routes:
            qa_role, qa_path, qa_hud, qa_msg = qa_routes[action_id]
            res = self.login_role(qa_role, qa_path, qa_hud)
            return {**res, "message": qa_msg}

        return {"ok": False, "error": f"Mã hành động không xác định: {action_id}"}

    def get_status(self) -> dict[str, Any]:
        roles_status = {}
        for role, info in ROLE_PROFILES.items():
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
            "ids": self.ids,
            "texts": DEMO_TEXTS,
            "roles": roles_status,
        }


# ==============================================================================
# 3. HTTP SERVER PHỤC VỤ GIAO DIỆN ĐIỀU KHIỂN (PORT 3999)
# ==============================================================================
CONTROLLER: DemoBrowserController | None = None
_PRIMARY_HTML = Path(__file__).resolve().parents[2] / "public" / "demo" / "demo_flow_navigator.html"
_LOCAL_HTML = Path(__file__).resolve().parent / "demo_flow_navigator.html"
HTML_FILE_PATH = _PRIMARY_HTML if _PRIMARY_HTML.exists() else _LOCAL_HTML


class DemoMonitorRequestHandler(BaseHTTPRequestHandler):
    def _send_json(self, data: dict[str, Any], status: int = 200) -> None:
        raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path in ("/", "/index.html", "/demo"):
            if HTML_FILE_PATH.exists():
                raw = HTML_FILE_PATH.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
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
    parser = argparse.ArgumentParser(description="BrandHub Live Demo Monitor (Selenium 4)")
    parser.add_argument("--app-url", default=DEFAULT_APP_URL, help="URL của ứng dụng BrandHub Web (mặc định: http://localhost:3000)")
    parser.add_argument("--port", type=int, default=DEFAULT_MONITOR_PORT, help="Cổng của Bàn điều khiển Demo (mặc định: 3999)")
    parser.add_argument("--password", default=DEFAULT_PASSWORD, help="Mật khẩu chung của các tài khoản demo")
    args = parser.parse_args()

    CONTROLLER = DemoBrowserController(app_url=args.app_url, password=args.password)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), DemoMonitorRequestHandler)

    print("=" * 78)
    print("  BRANDHUB LIVE DEMO MONITOR - TUYỂN SINH ĐẠI HỌC FPT 2027 (SE08 DIGITAL)")
    print("=" * 78)
    print(f"  - BrandHub Web App URL : {args.app_url}")
    print(f"  - Bàn điều khiển HTML  : http://localhost:{args.port}")
    print(f"  - Cổng API điều khiển  : http://localhost:{args.port}/api/status")
    print("=" * 78)
    print(f"Running on http://127.0.0.1:{args.port} (Press CTRL+C to quit)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Đang đóng Bàn điều khiển Demo...")
        server.server_close()


if __name__ == "__main__":
    main()
