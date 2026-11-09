#!/usr/bin/env python3
"""
BRANDHUB SELENIUM LIVE DEMO MONITOR SERVER (DIRECTOR CONSOLE v2.0)
==================================================================
Máy chủ điều khiển trình duyệt bằng Selenium 4 phục vụ buổi bảo vệ đồ án tốt nghiệp.
- Kịch bản thực tế hệ sinh thái FPT:
    * Đơn vị truyền thông (Agency) : FPT Smart Ads Agency
    * Thương hiệu khách hàng       : Đại học FPT (Tập đoàn FPT)
    * Không gian làm việc chung    : FPT University x FPT Smart Ads
- 5 cửa sổ Chrome độc lập gắn với 5 thành viên nhóm đồ án theo 5 vai trò chuẩn:
    1. `Owner`   : Lê Trí Trung       (user177@demo.brandhub.test)
    2. `Manager` : Nguyễn Thành Lộc   (user1@demo.brandhub.test)
    3. `Creator` : Nguyễn Chơn Phước  (user13@demo.brandhub.test)
    4. `Client`  : Nguyễn Minh Tuấn   (user59@demo.brandhub.test)
    5. `Admin`   : Hà Văn Ân          (admin@demo.brandhub.test)
- Thuật toán 3 tầng tương thích với kiến trúc BrandHub Web (React 19 + Yjs Canvas + Tiptap):
    * Tầng 1 (`CanvasTextEditor` + `Y.Text`): Phát sự kiện `InputEvent('beforeinput')`
      theo từng cụm âm tiết tiếng Việt, giữ nguyên dấu cách và tránh kẹt phím tắt.
    * Tầng 2 (`RichTextEditor` / Tiptap `.ProseMirror`): Điều khiển `ActionChains` + `send_keys`
      gõ chữ từng cụm.
    * Tầng 3 (`React 19 Controlled Input/Textarea`): Đồng bộ `_valueTracker` nội bộ của React 19
      trước khi gõ từng cụm ký tự và nghỉ nhịp giữa các trường (`pause_between_fields`).
- Không tự động bấm các nút Submit/Approve/Reject/Deploy/Publish chốt cuối
  mà khoanh sáng viền xanh/đỏ để người thuyết trình tự bấm trên sân khấu.
"""

import ctypes
import json
import os
import random
import re
import socket
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent
PROFILES_DIR = BASE_DIR / ".selenium_profiles"
PROFILES_DIR.mkdir(exist_ok=True)

# ==============================================================================
# CẤU HÌNH MẶC ĐỊNH HỆ SINH THÁI FPT & 5 THÀNH VIÊN NHÓM ĐỒ ÁN
# ==============================================================================

STATE = {
    "base_url": "http://localhost:5173",  # Đổi sang https://brandhub.id.vn trên UI với 1 nút bấm
    "agency_id": "359a1839-18c7-48e2-8a68-f5f68c3375b6",
    "workspace_id": "b47477c4-13ad-44ff-8c49-f73f1837461b",
    "active_task_id": "c6453698-cf56-38c1-96d2-90ccdd985228",
    "chunk_speed": "normal",  # "fast" | "normal" | "slow"
    "status_message": "Sẵn sàng. Hãy bấm 'Khởi tạo 5 Cửa sổ' hoặc chọn từng thành viên để mở trình duyệt.",
    "last_step": None,
}

ACCOUNTS = {
    "owner": {
        "role": "Owner",
        "window_label": "Cửa sổ 1 (Owner)",
        "email": "user177@demo.brandhub.test",
        "password": "Password123",
        "full_name": "Lê Trí Trung",
        "org_title": "Giám đốc FPT Smart Ads Agency",
        "start_path": "/agency/{agency_id}/media-packages",
    },
    "manager": {
        "role": "Manager",
        "window_label": "Cửa sổ 2 (Manager)",
        "email": "user1@demo.brandhub.test",
        "password": "Password123",
        "full_name": "Nguyễn Thành Lộc",
        "org_title": "Quản lý Chiến dịch (FPT University x FPT Smart Ads)",
        "start_path": "/workspaces/{workspace_id}/campaigns",
    },
    "creator": {
        "role": "Creator",
        "window_label": "Cửa sổ 3 (Creator)",
        "email": "user13@demo.brandhub.test",
        "password": "Password123",
        "full_name": "Nguyễn Chơn Phước",
        "org_title": "Chuyên viên Nội dung (FPT Smart Ads)",
        "start_path": "/workspaces/{workspace_id}/tasks",
    },
    "client": {
        "role": "Client",
        "window_label": "Cửa sổ 4 (Client)",
        "email": "user59@demo.brandhub.test",
        "password": "Password123",
        "full_name": "Nguyễn Minh Tuấn",
        "org_title": "Đại diện Đại học FPT (Tập đoàn FPT)",
        "start_path": "/workspaces/{workspace_id}/media-package",
    },
    "admin": {
        "role": "Admin",
        "window_label": "Cửa sổ 5 (Admin)",
        "email": "admin@demo.brandhub.test",
        "password": "Password123",
        "full_name": "Hà Văn Ân",
        "org_title": "Quản trị viên Hệ thống BrandHub",
        "start_path": "/admin?view=revenue",
    },
}

DEFAULT_TEXTS = {
    "B6_AI_TOPIC": (
        "Giới thiệu chương trình đào tạo ngành Thiết kế Vi mạch và Trí tuệ nhân tạo tại Đại học FPT, "
        "hưởng ứng mục tiêu 50.000 kỹ sư bán dẫn của Việt Nam đến năm 2030"
    ),
    "B7_VIOLATION": (
        "Bài viết chứa nội dung kích động bạo lực và ngôn từ thù ghét vi phạm quy định an toàn thông tin."
    ),
    "B7_CLEAN_V1": (
        "Đại học FPT mở cổng đăng ký ngành Thiết kế Vi mạch và Trí tuệ nhân tạo kỳ thu 2026.\n"
        "Chương trình đào tạo gắn với mục tiêu phát triển 50.000 kỹ sư bán dẫn tại Việt Nam đến năm 2030.\n"
        "#DaiHocFPT #ViMachBanDan #ChuyenDoiSoVietNam"
    ),
    "B9_REJECT_REASON": (
        "Bài viết đã rõ ý chính. Nhờ bạn bổ sung thêm thông tin học bổng Nguyễn Văn Đạo từ 50% đến 100% "
        "và kỳ thực tập thực tế tại FPT Software từ năm thứ 3."
    ),
    "B10_V2_ADDITION": (
        "Sinh viên có cơ hội nhận học bổng Nguyễn Văn Đạo từ 50% đến 100% học phí "
        "và tham gia thực tập hưởng lương tại FPT Software ngay từ năm thứ 3."
    ),
}

DRIVERS: dict[str, webdriver.Chrome] = {}
DRIVER_LOCK = threading.Lock()


# ==============================================================================
# CÁC HÀM TIỆN ÍCH SELENIUM: ĐƯA CỬA SỔ LÊN TRƯỚC & HIGHLIGHT TRỰC QUAN
# ==============================================================================

def _is_port_open(port: int) -> bool:
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=0.25):
            return True
    except OSError:
        return False


def get_effective_base_url() -> str:
    base = STATE["base_url"].rstrip("/")
    if "localhost:5173" in base and not _is_port_open(5173) and _is_port_open(3000):
        STATE["base_url"] = "http://localhost:3000"
        return STATE["base_url"]
    if "localhost:3000" in base and not _is_port_open(3000) and _is_port_open(5173):
        STATE["base_url"] = "http://localhost:5173"
        return STATE["base_url"]
    return base


def resolve_path(path_template: str) -> str:
    path = (
        path_template.replace("{agency_id}", STATE["agency_id"])
        .replace("{workspace_id}", STATE["workspace_id"])
        .replace("{task_id}", STATE["active_task_id"])
    )
    return get_effective_base_url() + path


def get_or_create_driver(role_key: str) -> webdriver.Chrome:
    """Khởi tạo hoặc lấy lại phiên Chrome của Role tương ứng (giữ nguyên session trong .selenium_profiles)."""
    with DRIVER_LOCK:
        existing = DRIVERS.get(role_key)
        if existing is not None:
            try:
                _ = existing.current_url
                return existing
            except WebDriverException:
                DRIVERS.pop(role_key, None)

        profile_path = PROFILES_DIR / role_key
        profile_path.mkdir(parents=True, exist_ok=True)

        opts = Options()
        opts.add_argument(f"--user-data-dir={profile_path}")
        opts.add_argument("--start-maximized")
        opts.add_argument("--disable-notifications")
        opts.add_argument("--disable-infobars")
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option("useAutomationExtension", False)
        opts.add_experimental_option(
            "prefs",
            {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
            },
        )

        driver = webdriver.Chrome(options=opts)
        DRIVERS[role_key] = driver
        return driver


def bring_browser_to_front(driver: webdriver.Chrome, role_key: str = ""):
    """Đưa cửa sổ Chrome của Role đó lên trên cùng màn hình máy chiếu."""
    try:
        driver.switch_to.window(driver.current_window_handle)
        driver.execute_script("window.focus();")
        if os.name == "nt":
            user32 = ctypes.windll.user32
            hwnd = user32.GetForegroundWindow()
            if hwnd:
                user32.ShowWindow(hwnd, 9)  # SW_RESTORE
    except Exception:
        pass


def highlight_element(
    driver: webdriver.Chrome,
    element,
    color: str = "#2563EB",
    duration_ms: int = 1100,
    badge_text: str = "",
):
    """
    Tạo hiệu ứng viền sáng trực quan quanh ô input hoặc nút bấm trên màn hình chiếu
    để Ban giám khảo dễ dàng nhìn thấy trường dữ liệu đang được thao tác.
    """
    try:
        driver.execute_script(
            """
            const el = arguments[0];
            const color = arguments[1];
            const dur = arguments[2];
            const badgeText = arguments[3];
            if (!el) return;
            el.scrollIntoView({ behavior: 'smooth', block: 'center' });
            const prevOutline = el.style.outline;
            const prevTransition = el.style.transition;
            const prevBoxShadow = el.style.boxShadow;
            el.style.transition = 'outline 0.2s ease, box-shadow 0.2s ease';
            el.style.outline = '2.5px solid ' + color;
            el.style.boxShadow = '0 0 0 6px ' + color + '28';

            let badgeEl = null;
            if (badgeText) {
                const rect = el.getBoundingClientRect();
                badgeEl = document.createElement('div');
                badgeEl.textContent = badgeText;
                badgeEl.style.position = 'fixed';
                badgeEl.style.top = Math.max(8, rect.top - 30) + 'px';
                badgeEl.style.left = Math.max(8, rect.left) + 'px';
                badgeEl.style.zIndex = '999999';
                badgeEl.style.background = color;
                badgeEl.style.color = '#ffffff';
                badgeEl.style.fontSize = '11px';
                badgeEl.style.fontWeight = '700';
                badgeEl.style.padding = '3px 9px';
                badgeEl.style.borderRadius = '999px';
                badgeEl.style.boxShadow = '0 4px 12px rgba(15, 23, 42, 0.22)';
                badgeEl.style.pointerEvents = 'none';
                document.body.appendChild(badgeEl);
            }

            setTimeout(() => {
                el.style.outline = prevOutline;
                el.style.boxShadow = prevBoxShadow;
                el.style.transition = prevTransition;
                if (badgeEl && badgeEl.parentNode) {
                    badgeEl.parentNode.removeChild(badgeEl);
                }
            }, dur);
            """,
            element,
            color,
            duration_ms,
            badge_text,
        )
    except Exception:
        pass


# ==============================================================================
# THUẬT TOÁN GÕ CHỮ NHẢ TỪNG PHẦN ĐA TẦNG (CHUẨN HÓA CHO REACT 19 + YJS CANVAS)
# ==============================================================================

def split_into_natural_chunks(text: str) -> list[str]:
    """
    Chia câu tiếng Việt thành từng cụm nhỏ (1 đến 4 ký tự hoặc theo âm tiết)
    để khi gõ vào ô input chữ hiện ra từng cụm tự nhiên như người đang gõ thật.
    """
    tokens = re.findall(r"\S+\s*|\s+", text)
    chunks: list[str] = []
    for token in tokens:
        if len(token) <= 4:
            chunks.append(token)
        else:
            mid = max(2, len(token) // 2)
            chunks.append(token[:mid])
            chunks.append(token[mid:])
    return chunks


def get_chunk_delays() -> tuple[float, float]:
    speed = STATE.get("chunk_speed", "normal")
    if speed == "fast":
        return (0.022, 0.048)
    if speed == "slow":
        return (0.080, 0.145)
    return (0.042, 0.088)


def _sleep_chunk_rhythm(chunk: str, min_d: float, max_d: float):
    delay = random.uniform(min_d, max_d)
    if any(p in chunk for p in (",", ".", ":", "!", "-", "\n")):
        delay += 0.13
    time.sleep(delay)


def _type_canvas_editor_chunks(
    driver: webdriver.Chrome,
    hidden_input,
    text: str,
    clear_first: bool,
    append_newline: bool,
):
    """
    TẦNG 1: Dành cho `CanvasTextEditor` (`aria-label='Content editor input'`).
    `CanvasTextEditor` của BrandHub quản lý văn bản bằng Yjs (`Y.Text`) và lắng nghe:
      - `onKeyDown` cho Ctrl+A, Backspace, ArrowDown, End
      - `onBeforeInput` (`InputEvent`) cho thao tác chèn văn bản (`insertText`) & xuống dòng (`insertLineBreak`).
    Phát trực tiếp `KeyboardEvent` & `InputEvent` theo từng cụm từ giúp hiển thị trên `<canvas>`
    ổn định, không bị mất dấu cách hay lỗi bộ gõ tiếng Việt.
    """
    # Khoanh sáng vùng khung Canvas cha để Hội đồng nhìn rõ
    try:
        wrapper = driver.execute_script(
            "return arguments[0].closest('.rounded-xl') || arguments[0].parentElement;",
            hidden_input,
        )
        highlight_element(driver, wrapper or hidden_input, "#2563EB", 1400, "Đang soạn thảo trên Yjs Canvas")
    except Exception:
        pass

    driver.execute_script("arguments[0].focus();", hidden_input)
    time.sleep(0.15)

    if clear_first:
        # Gửi Ctrl+A rồi Backspace trực tiếp vào handleKeyDown của CanvasTextEditor
        driver.execute_script(
            """
            const el = arguments[0];
            el.focus();
            el.dispatchEvent(new KeyboardEvent('keydown', { key: 'a', code: 'KeyA', ctrlKey: true, bubbles: true, cancelable: true }));
            el.dispatchEvent(new KeyboardEvent('keydown', { key: 'Backspace', code: 'Backspace', bubbles: true, cancelable: true }));
            """,
            hidden_input,
        )
        time.sleep(0.18)
    elif append_newline:
        # Đưa con trỏ xuống cuối toàn bộ văn bản (Ctrl+A -> ArrowRight) rồi chèn dòng mới
        driver.execute_script(
            """
            const el = arguments[0];
            el.focus();
            el.dispatchEvent(new KeyboardEvent('keydown', { key: 'a', code: 'KeyA', ctrlKey: true, bubbles: true, cancelable: true }));
            el.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowRight', code: 'ArrowRight', bubbles: true, cancelable: true }));
            el.dispatchEvent(new InputEvent('beforeinput', { inputType: 'insertLineBreak', data: '\\n', bubbles: true, cancelable: true }));
            """,
            hidden_input,
        )
        time.sleep(0.15)

    min_d, max_d = get_chunk_delays()
    for line_idx, line in enumerate(text.split("\n")):
        if line_idx > 0:
            driver.execute_script(
                """
                const el = arguments[0];
                el.focus();
                el.dispatchEvent(new InputEvent('beforeinput', { inputType: 'insertLineBreak', data: '\\n', bubbles: true, cancelable: true }));
                """,
                hidden_input,
            )
            time.sleep(0.12)

        chunks = split_into_natural_chunks(line)
        for chunk in chunks:
            driver.execute_script(
                """
                const el = arguments[0];
                const data = arguments[1];
                el.focus();
                el.dispatchEvent(new InputEvent('beforeinput', { inputType: 'insertText', data: data, bubbles: true, cancelable: true }));
                """,
                hidden_input,
                chunk,
            )
            _sleep_chunk_rhythm(chunk, min_d, max_d)


def _type_prosemirror_chunks(
    driver: webdriver.Chrome,
    element,
    text: str,
    clear_first: bool,
    append_newline: bool,
):
    """
    TẦNG 2: Chuyên biệt cho Tiptap `RichTextEditor` (`.ProseMirror[contenteditable='true']`).
    Sử dụng `ActionChains` chuẩn cho tổ hợp phím `Ctrl+A` để không bao giờ bị kẹt phím `Ctrl`.
    """
    highlight_element(driver, element, "#2563EB", 1300, "Đang gõ vào trình soạn thảo")
    time.sleep(0.2)
    try:
        element.click()
    except Exception:
        driver.execute_script("arguments[0].focus();", element)
    time.sleep(0.12)

    if clear_first:
        ActionChains(driver).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).pause(0.06).send_keys(
            Keys.BACKSPACE
        ).perform()
        time.sleep(0.15)
    elif append_newline:
        ActionChains(driver).key_down(Keys.CONTROL).send_keys(Keys.END).key_up(Keys.CONTROL).pause(0.06).send_keys(
            Keys.ENTER
        ).perform()
        time.sleep(0.12)

    min_d, max_d = get_chunk_delays()
    for line_idx, line in enumerate(text.split("\n")):
        if line_idx > 0:
            element.send_keys(Keys.ENTER)
            time.sleep(0.10)
        for chunk in split_into_natural_chunks(line):
            element.send_keys(chunk)
            _sleep_chunk_rhythm(chunk, min_d, max_d)


def _type_react_input_chunks(
    driver: webdriver.Chrome,
    element,
    text: str,
    clear_first: bool,
    append_newline: bool,
    field_label: str = "Đang nhập dữ liệu",
):
    """
    TẦNG 3: Chuyên biệt cho React 19 Controlled `<input>` và `<textarea>`
    (`LoginPage`, `AiCaptionDialog`, `TaskReviewDialog #task-review-note`).
    Đảm bảo xóa sạch state cũ trong React 19 thông qua native value setter + sự kiện `input`
    trước khi nhả từng cụm ký tự bằng `send_keys`.
    """
    highlight_element(driver, element, "#2563EB", 1200, field_label)
    time.sleep(0.2)
    try:
        element.click()
    except Exception:
        driver.execute_script("arguments[0].focus();", element)
    time.sleep(0.12)

    if clear_first:
        try:
            ActionChains(driver).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).pause(0.05).send_keys(
                Keys.BACKSPACE
            ).perform()
            # Đồng bộ thêm React 19 native value setter nếu còn sót ký tự
            driver.execute_script(
                """
                const el = arguments[0];
                const proto = el.tagName === 'TEXTAREA'
                    ? window.HTMLTextAreaElement.prototype
                    : window.HTMLInputElement.prototype;
                const setter = Object.getOwnPropertyDescriptor(proto, 'value')?.set;
                if (setter && el.value) {
                    setter.call(el, '');
                    el.dispatchEvent(new Event('input', { bubbles: true }));
                }
                """,
                element,
            )
        except Exception:
            pass
        time.sleep(0.12)
    elif append_newline:
        element.send_keys(Keys.END)
        time.sleep(0.06)
        element.send_keys("\n")
        time.sleep(0.10)

    min_d, max_d = get_chunk_delays()
    chunks = split_into_natural_chunks(text)
    for chunk in chunks:
        element.send_keys(chunk)
        _sleep_chunk_rhythm(chunk, min_d, max_d)


def type_in_chunks(
    driver: webdriver.Chrome,
    element,
    text: str,
    clear_first: bool = True,
    append_newline: bool = False,
    field_label: str = "Đang gõ tuần tự",
):
    """
    Bộ điều phối thuật toán gõ chữ từng cụm (tự động nhận diện đúng phần tử DOM).
    """
    aria_lbl = element.get_attribute("aria-label") or ""
    is_contenteditable = element.get_attribute("contenteditable") == "true"

    if "Content editor input" in aria_lbl:
        _type_canvas_editor_chunks(driver, element, text, clear_first, append_newline)
    elif is_contenteditable:
        _type_prosemirror_chunks(driver, element, text, clear_first, append_newline)
    else:
        _type_react_input_chunks(driver, element, text, clear_first, append_newline, field_label)


def pause_between_fields(seconds: float = 0.55):
    """Nhịp nghỉ tự nhiên giữa 2 ô input liên tiếp trên cùng một màn hình."""
    time.sleep(seconds)


# ==============================================================================
# CÁC KỊCH BẢN ĐIỀU KHIỂN TUẦN TỰ TỪNG BƯỚC (B1 -> B15)
# ==============================================================================

def login_single_role(role_key: str, auto_submit: bool = True) -> str:
    """Đăng nhập tuần tự cho 1 thành viên nhóm đồ án (Email từng cụm -> nghỉ -> Password từng cụm)."""
    acc = ACCOUNTS[role_key]
    driver = get_or_create_driver(role_key)
    bring_browser_to_front(driver, role_key)

    target_url = resolve_path(acc["start_path"])
    driver.get(target_url)
    time.sleep(1.0)

    if "/login" in driver.current_url:
        wait = WebDriverWait(driver, 10)
        email_inp = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text'], input[type='email']"))
        )
        type_in_chunks(
            driver,
            email_inp,
            acc["email"],
            clear_first=True,
            field_label=f"Bước 1/2: Nhập Email ({acc['full_name']})",
        )
        pause_between_fields(0.45)

        pwd_inp = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        type_in_chunks(
            driver,
            pwd_inp,
            acc["password"],
            clear_first=True,
            field_label="Bước 2/2: Nhập Mật khẩu",
        )
        pause_between_fields(0.35)

        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        highlight_element(driver, submit_btn, "#059669", 1200, "Đăng nhập")
        if auto_submit:
            submit_btn.click()
            time.sleep(1.8)
            driver.get(target_url)

    return f"Đã mở {acc['window_label']}: {acc['full_name']} ({acc['org_title']}) tại {driver.current_url}"


def execute_demo_action(action_id: str, payload: dict) -> str:
    """
    Thực thi từng thao tác điều khiển màn hình hoặc điền tuần tự từng ô input.
    LƯU Ý: Không bao giờ tự bấm nút Submit cuối cùng của các bước nghiệp vụ B1..B15.
    """
    ws_id = STATE["workspace_id"]
    ag_id = STATE["agency_id"]

    # ── KHỞI TẠO & ĐĂNG NHẬP SẴN ──
    if action_id.startswith("INIT_ROLE:"):
        role_key = action_id.split(":", 1)[1]
        return login_single_role(role_key, auto_submit=True)

    if action_id.startswith("FOCUS_ROLE:"):
        role_key = action_id.split(":", 1)[1]
        acc = ACCOUNTS[role_key]
        if role_key in DRIVERS:
            try:
                drv = DRIVERS[role_key]
                _ = drv.current_url
                bring_browser_to_front(drv, role_key)
                return f"Đã đưa {acc['window_label']} ({acc['full_name']}) lên trên cùng màn hình."
            except Exception:
                pass
        return login_single_role(role_key, auto_submit=True)

    if action_id.startswith("OPEN_ROUTE:"):
        role_key = action_id.split(":", 1)[1]
        custom_route = payload.get("route", ACCOUNTS[role_key]["start_path"])
        drv = get_or_create_driver(role_key)
        bring_browser_to_front(drv, role_key)
        drv.get(resolve_path(custom_route))
        return f"Đã chuyển {ACCOUNTS[role_key]['window_label']} ({ACCOUNTS[role_key]['full_name']}) tới {drv.current_url}"

    if action_id == "INIT_ALL_5_ROLES":
        for r in ("owner", "manager", "creator", "client", "admin"):
            login_single_role(r, auto_submit=True)
        bring_browser_to_front(get_or_create_driver("owner"), "owner")
        return "Đã khởi tạo và đăng nhập xong cả 5 cửa sổ của 5 thành viên nhóm đồ án!"

    # ── CHẶNG 1: THIẾT LẬP & CHIẾN DỊCH (B1 - B4) ──
    if action_id == "B1_NAV":
        d = get_or_create_driver("owner")
        bring_browser_to_front(d, "owner")
        d.get(resolve_path(f"/agency/{ag_id}/media-packages"))
        return "B1: Đã mở Cửa sổ 1 (Owner: Lê Trí Trung), Danh mục Gói truyền thông mẫu của FPT Smart Ads Agency."

    if action_id == "B2_NAV":
        d = get_or_create_driver("client")
        bring_browser_to_front(d, "client")
        d.get(resolve_path(f"/workspaces/{ws_id}/media-package"))
        return "B2: Đã mở Cửa sổ 4 (Client: Nguyễn Minh Tuấn), Gói truyền thông Tuyển sinh Đại học FPT 2026 đã chốt."

    if action_id == "B3_NAV":
        d = get_or_create_driver("manager")
        bring_browser_to_front(d, "manager")
        d.get(resolve_path(f"/workspaces/{ws_id}/campaigns"))
        time.sleep(0.85)
        try:
            btns = d.find_elements(By.XPATH, "//button[contains(., 'Triển khai') or contains(., 'Deploy')]")
            if btns:
                highlight_element(d, btns[0], "#059669", 2600, "Mời bạn bấm: Triển khai chiến dịch")
        except Exception:
            pass
        return "B3: Đã mở Chiến dịch (Manager: Nguyễn Thành Lộc). Nút 'Triển khai' đã được khoanh sáng, mời bạn tự bấm."

    if action_id == "B4_NAV":
        d = get_or_create_driver("manager")
        bring_browser_to_front(d, "manager")
        d.get(resolve_path(f"/workspaces/{ws_id}/tasks"))
        return "B4: Đã mở Bảng công việc (Manager: Nguyễn Thành Lộc). Chọn Bài #1 để giao cho Creator Nguyễn Chơn Phước."

    # ── CHẶNG 2: SÁNG TẠO AI & KIỂM TRA AN TOÀN (B5 - B7) ──
    if action_id == "B5_NAV":
        d = get_or_create_driver("creator")
        bring_browser_to_front(d, "creator")
        d.get(resolve_path(f"/workspaces/{ws_id}/tasks"))
        return "B5: Đã mở Cửa sổ 3 (Creator: Nguyễn Chơn Phước), nhận task Bài #1 và bắt đầu thực hiện."

    if action_id == "B6_NAV_EDITOR":
        d = get_or_create_driver("creator")
        bring_browser_to_front(d, "creator")
        d.get(resolve_path(f"/workspaces/{ws_id}/content-writing?taskId={STATE['active_task_id']}"))
        return "B6.1: Đã mở màn hình Soạn thảo Nội dung Yjs Canvas (Creator: Nguyễn Chơn Phước)."

    if action_id == "B6_SEQ_FILL_AI":
        """
        Điền tuần tự 4 bước trên hộp thoại AI tạo Caption đúng như người dùng thật:
          Bước 1: Mở hộp thoại AI (nếu chưa mở) -> nghỉ 0.6s.
          Bước 2: Focus ô Chủ đề (Textarea), gõ từng cụm từ chủ đề tuyển sinh AI Đại học FPT -> nghỉ 0.55s.
          Bước 3: Chọn Mục tiêu (Tương tác / Thông báo) trong nhóm nút Goal -> nghỉ 0.45s.
          Bước 4: Chọn Độ dài (Vừa / Medium) -> Khoanh sáng nút 'Tạo caption' và dừng lại chờ người thuyết trình bấm.
        """
        d = get_or_create_driver("creator")
        bring_browser_to_front(d, "creator")
        wait = WebDriverWait(d, 8)

        # Bước 1: Mở hộp thoại AI nếu chưa mở
        dialogs = d.find_elements(By.CSS_SELECTOR, "[role='dialog']")
        if not dialogs:
            ai_btns = d.find_elements(
                By.XPATH,
                "//button[contains(., 'AI') or contains(., 'caption') or contains(., 'Caption') or contains(., 'Tạo')]",
            )
            if ai_btns:
                highlight_element(d, ai_btns[0], "#2563EB", 700, "Bước 1/4: Mở hộp thoại AI")
                time.sleep(0.35)
                ai_btns[0].click()
                time.sleep(0.65)

        # Bước 2: Gõ tuần tự từng cụm từ vào ô Chủ đề
        topic_text = payload.get("text") or DEFAULT_TEXTS["B6_AI_TOPIC"]
        textarea = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "[role='dialog'] textarea, textarea"))
        )
        type_in_chunks(
            d,
            textarea,
            topic_text,
            clear_first=True,
            field_label="Bước 2/4: Nhập chủ đề Tuyển sinh Đại học FPT",
        )
        pause_between_fields(0.55)

        # Bước 3: Chọn Mục tiêu (Goal) & Bước 4: Chọn Độ dài (Length)
        try:
            groups = d.find_elements(By.CSS_SELECTOR, "[role='dialog'] [role='group']")
            if len(groups) >= 1:
                goal_btns = groups[0].find_elements(By.TAG_NAME, "button")
                if goal_btns:
                    target_goal = goal_btns[0]
                    highlight_element(d, target_goal, "#2563EB", 650, "Bước 3/4: Chọn Mục tiêu bài đăng")
                    target_goal.click()
                    pause_between_fields(0.45)
            if len(groups) >= 2:
                len_btns = groups[1].find_elements(By.TAG_NAME, "button")
                if len(len_btns) >= 2:
                    target_len = len_btns[1]  # Vừa (Medium)
                    highlight_element(d, target_len, "#2563EB", 650, "Bước 4/4: Chọn Độ dài Vừa")
                    target_len.click()
                    pause_between_fields(0.40)
        except Exception:
            pass

        # Khoanh sáng nút Submit "Tạo caption" nhưng KHÔNG tự ấn
        try:
            submit_btns = d.find_elements(
                By.CSS_SELECTOR,
                "[role='dialog'] button[type='submit'], [data-testid='generate-text']",
            )
            if submit_btns:
                highlight_element(
                    d,
                    submit_btns[0],
                    "#059669",
                    2800,
                    "Mời bạn tự bấm: Tạo 3 phương án Caption AI",
                )
        except Exception:
            pass

        return "B6.2: Đã điền tuần tự Chủ đề Đại học FPT + Mục tiêu + Độ dài. Mời bạn tự bấm nút 'Tạo caption'!"

    if action_id == "B7_FILL_VIOLATION":
        """
        Gõ tuần tự câu vi phạm vào trình soạn thảo để test chặn BLOCKED,
        sau đó khoanh sáng nút 'Kiểm tra tuân thủ' ([data-testid='caption-moderation'] button).
        """
        d = get_or_create_driver("creator")
        bring_browser_to_front(d, "creator")
        violation_text = payload.get("text") or DEFAULT_TEXTS["B7_VIOLATION"]

        editor_el = _find_editor_input(d)
        if editor_el is None:
            return "Không tìm thấy khung soạn thảo trên màn hình hiện tại. Hãy bấm B6.1 để mở trang Soạn thảo trước."

        type_in_chunks(
            d,
            editor_el,
            violation_text,
            clear_first=False,
            append_newline=True,
            field_label="B7.1: Chèn câu thử vi phạm tiêu chuẩn cộng đồng",
        )
        time.sleep(0.35)
        try:
            mod_btns = d.find_elements(By.CSS_SELECTOR, "[data-testid='caption-moderation'] button")
            if mod_btns:
                highlight_element(d, mod_btns[0], "#DC2626", 2600, "Mời bạn tự bấm: Kiểm tra tuân thủ (Sẽ báo BLOCKED)")
        except Exception:
            pass
        return "B7.1: Đã gõ từng cụm câu thử vi phạm. Mời bạn tự bấm nút 'Kiểm tra tuân thủ'."

    if action_id == "B7_CLEAN_AND_RESTORE":
        """Xóa câu vi phạm và điền lại nội dung chuẩn v1 của Đại học FPT để kiểm tra PASSED."""
        d = get_or_create_driver("creator")
        bring_browser_to_front(d, "creator")
        clean_v1 = payload.get("text") or DEFAULT_TEXTS["B7_CLEAN_V1"]

        editor_el = _find_editor_input(d)
        if editor_el is None:
            return "Không tìm thấy khung soạn thảo."

        type_in_chunks(
            d,
            editor_el,
            clean_v1,
            clear_first=True,
            append_newline=False,
            field_label="B7.2: Chuẩn hóa nội dung bản v1 (Sạch & Chuẩn Brand Voice FPT)",
        )
        time.sleep(0.35)
        try:
            mod_btns = d.find_elements(By.CSS_SELECTOR, "[data-testid='caption-moderation'] button")
            if mod_btns:
                highlight_element(d, mod_btns[0], "#059669", 2600, "Mời bạn bấm: Kiểm tra lại (PASSED) & Nộp duyệt")
        except Exception:
            pass
        return "B7.2: Đã xóa câu vi phạm và điền bản v1 chuẩn Đại học FPT. Mời bạn tự bấm 'Kiểm tra lại' và 'Nộp duyệt'."

    # ── CHẶNG 3: DUYỆT 2 CẤP & VERSION DIFF (B8 - B11) ──
    if action_id == "B8_NAV_MANAGER_APPROVAL":
        d = get_or_create_driver("manager")
        bring_browser_to_front(d, "manager")
        d.get(resolve_path(f"/workspaces/{ws_id}/task-approvals?task={STATE['active_task_id']}"))
        time.sleep(0.9)
        try:
            approve_btns = d.find_elements(By.CSS_SELECTOR, "button.bg-emerald-600")
            if approve_btns:
                highlight_element(d, approve_btns[0], "#059669", 2600, "Mời Manager tự bấm: Phê duyệt Tầng 1")
        except Exception:
            pass
        return "B8: Đã mở Cửa sổ 2 (Manager: Nguyễn Thành Lộc), Duyệt bài Tầng 1. Mời bạn tự bấm 'Phê duyệt'."

    if action_id == "B9_NAV_CLIENT_APPROVAL":
        d = get_or_create_driver("client")
        bring_browser_to_front(d, "client")
        d.get(resolve_path(f"/workspaces/{ws_id}/task-approvals?task={STATE['active_task_id']}"))
        return "B9.1: Đã mở Cửa sổ 4 (Client: Nguyễn Minh Tuấn), Xem trước bài viết chờ duyệt từ phía Đại học FPT."

    if action_id == "B9_SEQ_FILL_REJECT_REASON":
        """
        Tuần tự thao tác từ chối của Client Nguyễn Minh Tuấn:
          1. Nếu hộp thoại Từ chối (#task-review-note) chưa mở, tự bấm nút 'Từ chối' màu đỏ để mở hộp thoại -> nghỉ 0.55s.
          2. Focus vào ô #task-review-note, gõ từng cụm lý do yêu cầu bổ sung Học bổng Nguyễn Văn Đạo & OJT FPT Software.
          3. Khoanh sáng nút xác nhận Từ chối và dừng lại để người thuyết trình tự bấm.
        """
        d = get_or_create_driver("client")
        bring_browser_to_front(d, "client")
        reason_text = payload.get("text") or DEFAULT_TEXTS["B9_REJECT_REASON"]

        note_boxes = d.find_elements(By.CSS_SELECTOR, "#task-review-note, [role='dialog'] textarea")
        if not note_boxes:
            reject_btns = d.find_elements(
                By.XPATH,
                "//button[contains(., 'Từ chối') or contains(., 'Reject') or contains(@class, 'bg-rose-600')]",
            )
            if reject_btns:
                highlight_element(d, reject_btns[0], "#DC2626", 650, "Bước 1/2: Mở hộp thoại Từ chối")
                time.sleep(0.3)
                reject_btns[0].click()
                time.sleep(0.55)

        wait = WebDriverWait(d, 8)
        note_el = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#task-review-note, [role='dialog'] textarea"))
        )
        type_in_chunks(
            d,
            note_el,
            reason_text,
            clear_first=True,
            field_label="Bước 2/2: Gõ góp ý bổ sung Học bổng Nguyễn Văn Đạo & OJT FPT Software",
        )
        time.sleep(0.3)
        try:
            confirm_btns = d.find_elements(By.CSS_SELECTOR, "[role='dialog'] button.bg-rose-600, [role='dialog'] button[type='submit']")
            if confirm_btns:
                highlight_element(d, confirm_btns[-1], "#DC2626", 2600, "Mời Client tự bấm: Xác nhận Từ chối")
        except Exception:
            pass
        return "B9.2: Đã gõ từng cụm góp ý của Đại học FPT vào ô '#task-review-note'. Mời bạn tự bấm xác nhận 'Từ chối'."

    if action_id == "B10_NAV_CREATOR_FIX":
        d = get_or_create_driver("creator")
        bring_browser_to_front(d, "creator")
        d.get(resolve_path(f"/workspaces/{ws_id}/editor?taskId={STATE['active_task_id']}"))
        return "B10.1: Đã chuyển về Cửa sổ 3 (Creator: Nguyễn Chơn Phước) để sửa bài theo góp ý của Đại học FPT."

    if action_id == "B10_SEQ_FILL_V2":
        """Gõ từng cụm câu bổ sung Học bổng Nguyễn Văn Đạo & thực tập OJT FPT Software để tạo bản v2."""
        d = get_or_create_driver("creator")
        bring_browser_to_front(d, "creator")
        v2_addition = payload.get("text") or DEFAULT_TEXTS["B10_V2_ADDITION"]
        editor_el = _find_editor_input(d)
        if editor_el is None:
            return "Không tìm thấy khung soạn thảo bài viết."

        type_in_chunks(
            d,
            editor_el,
            v2_addition,
            clear_first=False,
            append_newline=True,
            field_label="B10.2: Bổ sung Học bổng Nguyễn Văn Đạo & OJT FPT Software (Bản v2)",
        )
        return "B10.2: Đã gõ bổ sung Học bổng Nguyễn Văn Đạo & OJT FPT Software (bản v2). Mời bạn tự bấm Lưu, mở Version History và Nộp duyệt lại."

    if action_id == "B11_NAV_MANAGER_V2":
        d = get_or_create_driver("manager")
        bring_browser_to_front(d, "manager")
        d.get(resolve_path(f"/workspaces/{ws_id}/task-approvals?task={STATE['active_task_id']}"))
        time.sleep(0.85)
        try:
            approve_btns = d.find_elements(By.CSS_SELECTOR, "button.bg-emerald-600")
            if approve_btns:
                highlight_element(d, approve_btns[0], "#059669", 2600, "Mời Manager bấm: Phê duyệt vòng 2")
        except Exception:
            pass
        return "B11a: Đã mở Cửa sổ 2 (Manager: Nguyễn Thành Lộc) để duyệt vòng 2. Mời bạn tự bấm 'Phê duyệt'."

    if action_id == "B11_NAV_CLIENT_V2":
        d = get_or_create_driver("client")
        bring_browser_to_front(d, "client")
        d.get(resolve_path(f"/workspaces/{ws_id}/task-approvals?task={STATE['active_task_id']}"))
        time.sleep(0.85)
        try:
            approve_btns = d.find_elements(By.CSS_SELECTOR, "button.bg-emerald-600")
            if approve_btns:
                highlight_element(d, approve_btns[0], "#059669", 2600, "Mời Client bấm: Phê duyệt chính thức (APPROVED)")
        except Exception:
            pass
        return "B11b: Đã mở Cửa sổ 4 (Client: Nguyễn Minh Tuấn) để phê duyệt chính thức bản v2. Mời bạn tự bấm 'Phê duyệt'."

    # ── CHẶNG 4: XUẤT BẢN MẠNG XÃ HỘI (B12 - B13) ──
    if action_id == "B12_NAV_SOCIAL":
        d = get_or_create_driver("manager")
        bring_browser_to_front(d, "manager")
        d.get(resolve_path(f"/workspaces/{ws_id}/social-accounts"))
        return "B12: Đã mở màn hình 4 Tài khoản Mạng xã hội chính thức của Đại học FPT (Manager: Nguyễn Thành Lộc)."

    if action_id == "B13_NAV_PUBLISH":
        d = get_or_create_driver("manager")
        bring_browser_to_front(d, "manager")
        d.get(resolve_path(f"/workspaces/{ws_id}/publish"))
        return "B13a: Đã mở màn hình Xuất bản (Manager: Nguyễn Thành Lộc). Lưu ý chỉ tích chọn 1 kênh (Facebook FPT University) và tự bấm 'Đăng ngay'."

    if action_id == "B13_NAV_DASHBOARD":
        d = get_or_create_driver("manager")
        bring_browser_to_front(d, "manager")
        d.get(resolve_path(f"/workspaces/{ws_id}/publish/dashboard"))
        return "B13b: Đã mở Bảng điều khiển kết quả xuất bản (Manager: Nguyễn Thành Lộc)."

    # ── CHẶNG 5: VIETQR SEPAY & ADMIN (B14 - B15) ──
    if action_id == "B14_NAV_PLANS":
        d = get_or_create_driver("owner")
        bring_browser_to_front(d, "owner")
        d.get(resolve_path("/subscription/plans"))
        return "B14: Đã mở Cửa sổ 1 (Owner: Lê Trí Trung), Nâng cấp gói thuê bao Plus cho FPT Smart Ads qua VietQR SePay."

    if action_id == "B15_NAV_ADMIN_REVENUE":
        d = get_or_create_driver("admin")
        bring_browser_to_front(d, "admin")
        d.get(resolve_path("/admin?view=revenue"))
        return "B15a: Đã mở Cửa sổ 5 (Admin: Hà Văn Ân), Bảng điều khiển Doanh thu MRR/ARR toàn nền tảng."

    if action_id == "B15_NAV_ADMIN_MODERATION":
        d = get_or_create_driver("admin")
        bring_browser_to_front(d, "admin")
        d.get(resolve_path("/admin?view=moderation"))
        return "B15b: Đã mở Cửa sổ 5 (Admin: Hà Văn Ân), Hàng đợi Kiểm duyệt Nội dung vi phạm toàn hệ thống."

    return f"Không nhận diện được mã hành động: {action_id}"


def _find_editor_input(driver: webdriver.Chrome):
    """Tìm vùng nhập văn bản của trình soạn thảo (CanvasTextEditor, Tiptap RichTextEditor, hoặc Textarea)."""
    selectors = [
        "[aria-label='Content editor input']",
        ".ProseMirror[contenteditable='true']",
        "[role='textbox'][contenteditable='true']",
        "textarea",
    ]
    for sel in selectors:
        els = driver.find_elements(By.CSS_SELECTOR, sel)
        for el in els:
            if el.is_displayed() or "Content editor input" in (el.get_attribute("aria-label") or ""):
                return el
    return None


# ==============================================================================
# HTTP SERVER PHỤC VỤ GIAO DIỆN MONITOR & API ĐIỀU KHIỂN SELENIUM
# ==============================================================================

class MonitorRequestHandler(BaseHTTPRequestHandler):
    def _send_json(self, data: dict, status: int = 200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._send_json({"ok": True})

    def do_GET(self):
        parsed = urlparse(self.path)
        portal_public_demo = BASE_DIR.parent.parent / "public" / "demo"
        if parsed.path in ("/", "/index.html", "/demo_flow_navigator.html"):
            html_file = portal_public_demo / "demo_flow_navigator.html"
            if html_file.exists():
                content = html_file.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return

        if parsed.path.startswith("/diagrams/") or parsed.path.startswith("/demo/"):
            img_name = os.path.basename(parsed.path)
            img_path = portal_public_demo / img_name
            if img_path.exists():
                content = img_path.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "image/png")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return

        if parsed.path == "/api/state":
            active_roles = []
            role_urls = {}
            for k, drv in list(DRIVERS.items()):
                try:
                    url = drv.current_url
                    active_roles.append(k)
                    role_urls[k] = url
                except Exception:
                    pass
            self._send_json(
                {
                    "ok": True,
                    "state": STATE,
                    "active_roles": active_roles,
                    "role_urls": role_urls,
                    "accounts": ACCOUNTS,
                }
            )
            return

        self._send_json({"ok": False, "error": "Not found"}, 404)

    def do_POST(self):
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        body = json.loads(raw) if raw else {}

        if parsed.path == "/api/config":
            for key in ("base_url", "agency_id", "workspace_id", "active_task_id", "chunk_speed"):
                if key in body and body[key]:
                    STATE[key] = str(body[key]).strip()
            STATE["status_message"] = (
                f"Đã cập nhật cấu hình: Base URL = {STATE['base_url']} (Tốc độ gõ: {STATE['chunk_speed']})"
            )
            self._send_json({"ok": True, "state": STATE})
            return

        if parsed.path == "/api/action":
            action_id = body.get("action_id", "")
            try:
                msg = execute_demo_action(action_id, body)
                STATE["last_step"] = action_id
                STATE["status_message"] = msg
                self._send_json({"ok": True, "message": msg, "state": STATE})
            except Exception as exc:
                err_msg = f"Lỗi khi chạy {action_id}: {exc}"
                STATE["status_message"] = err_msg
                self._send_json({"ok": False, "error": err_msg, "state": STATE}, 500)
            return

        self._send_json({"ok": False, "error": "Unknown endpoint"}, 404)

    def log_message(self, format, *args):
        pass


def main():
    port = int(os.environ.get("MONITOR_PORT", "3999"))
    server = ThreadingHTTPServer(("127.0.0.1", port), MonitorRequestHandler)
    print("=" * 80, flush=True)
    print(f"BRANDHUB SELENIUM MONITOR SERVER ĐANG CHẠY TẠI: http://localhost:{port}", flush=True)
    print(f"- Môi trường mặc định : {STATE['base_url']} (Đổi sang https://brandhub.id.vn trên UI)", flush=True)
    print("- Kịch bản doanh nghiệp: FPT Smart Ads Agency x FPT University (Đại học FPT)", flush=True)
    print("- 5 Thành viên đồ án  : Lê Trí Trung (Owner), Nguyễn Thành Lộc (Manager),", flush=True)
    print("                        Nguyễn Chơn Phước (Creator), Nguyễn Minh Tuấn (Client), Hà Văn Ân (Admin)", flush=True)
    print("- Thuật toán gõ 3 tầng: Yjs Canvas BeforeInput + Tiptap ActionChains + React 19 ValueSetter", flush=True)
    print("Application startup complete. Waiting on http://localhost:" + str(port), flush=True)
    print("=" * 80, flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nĐang đóng Monitor Server...")
        server.server_close()


if __name__ == "__main__":
    main()
