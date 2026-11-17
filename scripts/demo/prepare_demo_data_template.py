#!/usr/bin/env python3
"""
================================================================================
BRANDHUB LIVE DEMO DATA PREPARATION - FPT UNIVERSITY ADMISSIONS 2027 (4 WEEKS)
================================================================================
Thiết lập đồng bộ 100% dữ liệu PostgreSQL & MongoDB cho buổi bảo vệ Đồ án Tốt nghiệp
của nhóm SE_08 (Lê Trí Trung, Nguyễn Thành Lộc, Nguyễn Chơn Phước, Nguyễn Minh Tuấn,
Hà Văn Ân) triển khai chiến dịch truyền thông 4 tuần cho Khách hàng:
Ban Tuyển sinh Trường Đại học FPT (Mùa tuyển sinh khóa K23 - Năm 2027).

Bao phủ liên kết dữ liệu xuyên suốt toàn bộ các trang trên hệ thống BrandHub:
  1. Agency & Thành viên SE_08 + Hồ sơ Khách hàng (Trường Đại học FPT)
  2. Danh mục 7 Gói truyền thông Đa lĩnh vực (Giáo dục ĐH FPT, Công nghệ SaaS,
     F&B, Bất động sản, Dược mỹ phẩm, Thương mại điện tử, Du lịch Nghỉ dưỡng)
     tuân thủ tuyệt đối PackageOfferingValidator (7 loại dịch vụ chuẩn, 0 Livestream)
  3. Chiến dịch Tuyển sinh Đại học FPT 2027 kéo dài 4 tuần (Tuần 1 Coming Soon ->
     Tuần 2 Ngành học & Tiện ích Campus -> Tuần 3 Chuỗi Workshop THPT & Open Day ->
     Tuần 4 Báo chí chính thống & Đa nền tảng chốt đợt hồ sơ) với 6 khối Brief,
     Master Brief, 6 Đối tác báo chí/KOL/truyền hình và 20 Công việc chi tiết
  4. Hệ thống Subtask theo vai trò (TaskCatalog) & Phê duyệt từng phần (SectionStore)
  5. Thư viện Tài nguyên (/library) tích hợp sẵn 7 bộ ảnh Key Visual Gemini Nano Banana
     kèm ảnh thực tế Unsplash hiển thị trực tiếp cho cả Agency và Client
  6. Đa nền tảng xuất bản (Facebook, Instagram, TikTok, Threads), Lịch đăng bài,
     Dashboard tương tác, Khảo sát học sinh THPT, Yêu cầu nội dung, Nhóm Hashtag,
     Mẫu Email, Trò chuyện nhóm, Kho tri thức AI (GraphRAG), Gói cước SePay (VietQR) & Admin.

Cách chạy:
  1. Tự động đọc cấu hình từ brandhub-business-service/.env và nạp vào DB:
     python prepare_demo_data_template.py --apply

  2. Chỉ xuất file SQL & JSON preview để kiểm tra:
     python prepare_demo_data_template.py
================================================================================
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import os
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus


# ==============================================================================
# 0. TIỆN ÍCH ĐỊNH DANH CHUẨN JAVA & TỰ ĐỘNG ĐỌC .ENV / ẢNH KEY VISUAL
# ==============================================================================
def java_name_uuid_from_bytes(name: str) -> str:
    """Tái tạo chính xác UUID.nameUUIDFromBytes(name.getBytes(UTF_8)) của Java."""
    md5_bytes = bytearray(hashlib.md5(name.encode("utf-8")).digest())
    md5_bytes[6] = (md5_bytes[6] & 0x0F) | 0x30  # version 3
    md5_bytes[8] = (md5_bytes[8] & 0x3F) | 0x80  # IETF variant
    return str(uuid.UUID(bytes=bytes(md5_bytes)))


def campaign_task_id(campaign_id: str, work_item_id: str) -> str:
    """Khớp CampaignTaskStore.taskId(campaignId, workItemId)."""
    return java_name_uuid_from_bytes(f"campaign:{campaign_id}:item:{work_item_id}")


def subtask_id(task_id: str, role: str) -> str:
    """Khớp CampaignTaskStore.catalogSubtasks."""
    return java_name_uuid_from_bytes(f"task:{task_id}:role:{role}")


def section_doc_id(task_id: str, section_key: str) -> str:
    """Khớp TaskSectionDocument.idOf(taskId, sectionKey) = taskId|sectionKey."""
    return f"{task_id}|{section_key}"


def section_ver_id(task_id: str, section_key: str, version_no: int) -> str:
    """Khớp TaskSectionVersionDocument.idOf(taskId, sectionKey, versionNo)."""
    return f"{task_id}|{section_key}|{version_no}"


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "brandhub-business-service").exists() and (parent / "brandhub-web").exists():
            return parent
    return here.parents[3]


def load_default_db_uris() -> tuple[str, str, str]:
    """Đọc kết nối PostgreSQL & MongoDB thực tế từ brandhub-business-service/.env."""
    repo_root = find_repo_root()
    env_file = repo_root / "brandhub-business-service" / ".env"
    env_vals: dict[str, str] = {}
    if env_file.exists():
        for raw_line in env_file.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env_vals[k.strip()] = v.strip().strip('"').strip("'")

    jdbc_url = os.environ.get("POSTGRES_URL") or env_vals.get("POSTGRES_URL", "jdbc:postgresql://localhost:5432/brandhub")
    pg_user = os.environ.get("POSTGRES_USERNAME") or env_vals.get("POSTGRES_USERNAME", "brandhub")
    pg_pass = os.environ.get("POSTGRES_PASSWORD") or env_vals.get("POSTGRES_PASSWORD", "password")
    clean_pg = jdbc_url.replace("jdbc:postgresql://", "")
    pg_uri = f"postgresql://{quote_plus(pg_user)}:{quote_plus(pg_pass)}@{clean_pg}"

    mongo_uri = os.environ.get("MONGODB_URI") or env_vals.get("MONGODB_URI", "mongodb://localhost:27017/brandhub")
    mongo_db = os.environ.get("MONGODB_DATABASE") or env_vals.get("MONGODB_DATABASE", "brandhub")
    return pg_uri, mongo_uri, mongo_db


def load_default_redis_url() -> str:
    """Đọc kết nối Redis thực tế từ brandhub-ai-service/.env."""
    repo_root = find_repo_root()
    env_file = repo_root / "brandhub-ai-service" / ".env"
    env_vals: dict[str, str] = {}
    if env_file.exists():
        for raw_line in env_file.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env_vals[k.strip()] = v.strip().strip('"').strip("'")
    return os.environ.get("REDIS_URL") or env_vals.get("REDIS_URL", "redis://:root@localhost:6379/0")


def load_default_sepay_merchant() -> str:
    """Đọc mã tài khoản đối soát SePay thực tế từ brandhub-business-service/.env."""
    repo_root = find_repo_root()
    env_file = repo_root / "brandhub-business-service" / ".env"
    env_vals: dict[str, str] = {}
    if env_file.exists():
        for raw_line in env_file.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env_vals[k.strip()] = v.strip().strip('"').strip("'")
    val = os.environ.get("SEPAY_MERCHANT_ACCOUNT") or env_vals.get("SEPAY_MERCHANT_ACCOUNT", "")
    return val.strip() or "BRANDHUB_SEPAY_VN"


def load_asset_data_uri(filename: str) -> tuple[str, int]:
    """
    Tạo Data URI JPEG gọn nhẹ từ file ảnh đã sinh sẵn trong public/demo-assets/fptu-2027/
    để MaterialResponseFactory hiển thị tức thì trong /library mà không phụ thuộc S3.
    """
    repo_root = find_repo_root()
    candidates = [
        repo_root / "brandhub-web" / "public" / "demo-assets" / "fptu-2027" / filename,
        repo_root / "brandhub-docs-portal" / "public" / "demo-assets" / "fptu-2027" / filename,
    ]
    img_path = next((p for p in candidates if p.exists()), None)
    if not img_path:
        # Fallback 1x1 cam FPT nếu chạy ở môi trường tách rời
        tiny = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
        return f"data:image/png;base64,{tiny}", 1024

    raw_bytes = img_path.read_bytes()
    orig_size = len(raw_bytes)
    try:
        from PIL import Image

        with Image.open(io.BytesIO(raw_bytes)) as im:
            im = im.convert("RGB")
            im.thumbnail((960, 540))
            buf = io.BytesIO()
            im.save(buf, format="JPEG", quality=80, optimize=True)
            compact = buf.getvalue()
            b64 = base64.b64encode(compact).decode("ascii")
            return f"data:image/jpeg;base64,{b64}", orig_size
    except Exception:
        b64 = base64.b64encode(raw_bytes).decode("ascii")
        return f"data:image/jpeg;base64,{b64}", orig_size


# ==============================================================================
# 1. ĐỊNH DANH CỐ ĐỊNH TRONG KỊCH BẢN (DETERMINISTIC DEMO IDENTIFIERS)
# ==============================================================================
AGENCY_ID = "359a1839-18c7-48e2-8a68-f5f68c3375b6"        # SE08 Digital Agency
WORKSPACE_ID = "b47477c4-13ad-44ff-8c49-f73f1837461b"     # Đại học FPT Tuyển sinh 2027 x SE08 Digital
CLIENT_PROFILE_ID = "d7e00000-0000-4000-8000-000000000001"  # Ban Tuyển sinh Đại học FPT

PACKAGE_ID = "d7e00000-0000-4000-8000-000000000200"       # Gói Tuyển sinh Đại học FPT 2027 (4 Tuần)
WS_PACKAGE_ID = "d7e00000-0000-4000-8000-000000000201"    # Hợp đồng gói gắn với Workspace ĐH FPT
CAMPAIGN_ID = "d7e00000-0000-4000-8000-000000000301"      # Chiến dịch Tuyển sinh Đại học FPT 2027 (4 Tuần)

# 6 gói truyền thông đa lĩnh vực trong danh mục của SE08 Digital Agency
CATALOG_PKG_TECH_ID = "d7e00000-0000-4000-8000-000000000211"
CATALOG_PKG_FNB_ID = "d7e00000-0000-4000-8000-000000000212"
CATALOG_PKG_REALESTATE_ID = "d7e00000-0000-4000-8000-000000000213"
CATALOG_PKG_BEAUTY_ID = "d7e00000-0000-4000-8000-000000000214"
CATALOG_PKG_ECOM_ID = "d7e00000-0000-4000-8000-000000000215"
CATALOG_PKG_TRAVEL_ID = "d7e00000-0000-4000-8000-000000000216"

# 7 Deliverable IDs của Gói Tuyển sinh Đại học FPT 2027 (mỗi loại dịch vụ chuẩn 1 dòng)
DELIV_POST_ID = "d7e00000-0000-4000-8000-000000000251"
DELIV_VIDEO_ID = "d7e00000-0000-4000-8000-000000000252"
DELIV_WORKSHOP_ID = "d7e00000-0000-4000-8000-000000000253"
DELIV_EVENT_ID = "d7e00000-0000-4000-8000-000000000254"
DELIV_KOL_ID = "d7e00000-0000-4000-8000-000000000255"
DELIV_EMAIL_ID = "d7e00000-0000-4000-8000-000000000256"
DELIV_PRESS_ID = "d7e00000-0000-4000-8000-000000000257"

# 6 Đối tác truyền thông bên thứ ba (Third-Party Collaborators)
COLLAB_VNEXPRESS_ID = "d7e00000-0000-4000-8000-000000000501"
COLLAB_THANHNIEN_ID = "d7e00000-0000-4000-8000-000000000502"
COLLAB_DANTRI_ID = "d7e00000-0000-4000-8000-000000000503"
COLLAB_VTV1_ID = "d7e00000-0000-4000-8000-000000000504"
COLLAB_SCHANNEL_ID = "d7e00000-0000-4000-8000-000000000505"
COLLAB_CAMPUS_LED_ID = "d7e00000-0000-4000-8000-000000000506"

# Công việc trọng tâm để trình diễn trực tiếp trên sân khấu (B4 -> B13)
# Giữ nguyên TASK_1_ID cố định để đồng bộ với Selenium Demo Monitor & DemoMonitorPage
LIVE_WORK_ITEM_ID = "d7e00000-0000-4000-8000-000000000706"
TASK_1_ID = "c6453698-cf56-38c1-96d2-90ccdd985228"
POST_1_ID = "d7e00000-0000-4000-8000-000000000401"
SURVEY_TASK_ID = "2a100fd3-db57-3355-bef4-45dfbb4cf2f3"
SURVEY_DOC_ID = "d7e00000-0000-4000-8000-000000000801"

# Danh sách đầy đủ thành viên nhóm đồ án SE_08 (Agency) + Khách hàng ĐH FPT + Admin
DEMO_ACCOUNTS = {
    "OWNER": {
        "id": "87e97722-97c1-47ff-9d5f-02894e30bed2",
        "email": "user177@demo.brandhub.test",
        "full_name": "Lê Trí Trung",
        "role": "Owner",
        "title": "Giám đốc Điều hành SE08 Digital (Owner)",
        "bio": "Phụ trách chiến lược tổng thể, xây dựng gói truyền thông đa ngành và quản lý đối tác báo chí tại SE08 Digital Agency.",
    },
    "MANAGER": {
        "id": "48a55552-71bd-468c-ba02-fa849eeb7682",
        "email": "user1@demo.brandhub.test",
        "full_name": "Nguyễn Thành Lộc",
        "role": "Manager",
        "title": "Quản lý Chiến dịch Truyền thông (Manager)",
        "bio": "Điều phối kế hoạch 4 tuần chiến dịch Tuyển sinh Đại học FPT 2027, quản lý tiến độ Subtask và kiểm duyệt nội dung nội bộ.",
    },
    "CREATOR": {
        "id": "56034372-e963-4717-8dfa-e68e34d34c7a",
        "email": "user13@demo.brandhub.test",
        "full_name": "Nguyễn Chơn Phước",
        "role": "Creator",
        "title": "Chuyên viên Nội dung Đa nền tảng (Creator)",
        "bio": "Biên soạn nội dung tuyển sinh trên Facebook, Instagram, TikTok và Threads cho chiến dịch Đại học FPT 2027.",
    },
    "CREATOR_2": {
        "id": "38fcc012-0aff-426f-8466-05de1109ee13",
        "email": "user14@demo.brandhub.test",
        "full_name": "Nguyễn Minh Tuấn",
        "role": "Creator",
        "title": "Chuyên viên Thiết kế Visual, Video & Sự kiện Workshop",
        "bio": "Sản xuất Key Visual, Reels/TikTok thực tế tại Campus và điều phối chuỗi Workshop phổ biến tiện ích cho học sinh THPT.",
    },
    "CREATOR_3": {
        "id": "12c1e6b1-f808-419c-ab84-b7fe3b64c148",
        "email": "user15@demo.brandhub.test",
        "full_name": "Hà Văn Ân",
        "role": "Creator",
        "title": "Chuyên viên Quan hệ Báo chí (PR) & Email Marketing",
        "bio": "Phụ trách thông cáo báo chí trên VnExpress, Thanh Niên, Dân Trí, khảo sát học sinh lớp 12 và bản tin Email tư vấn tuyển sinh.",
    },
    "CLIENT": {
        "id": "b663ffe6-6693-41d3-8df5-27805e4dc8b6",
        "email": "user59@demo.brandhub.test",
        "full_name": "Ban Tuyển sinh Đại học FPT",
        "role": "Client",
        "title": "Đại diện Truyền thông & Tuyển sinh Trường Đại học FPT",
        "bio": "Đơn vị khách hàng phối hợp thẩm định thông tin quy chế tuyển sinh khóa K23 (2027), Học bổng Nguyễn Văn Đạo và kỳ thực tập OJT.",
    },
    "ADMIN": {
        "id": "90d56307-940b-4bec-820d-0ba39850041c",
        "email": "admin@demo.brandhub.test",
        "full_name": "Quản trị viên BrandHub",
        "role": "Admin",
        "title": "Quản trị Vận hành Nền tảng BrandHub",
        "bio": "Giám sát doanh thu gói cước SePay (VietQR), vận hành hạ tầng và xử lý hàng đợi kiểm duyệt nội dung cộng đồng.",
    },
}

PG_USER_IDS = {k: v["id"] for k, v in DEMO_ACCOUNTS.items()}

# Đường dẫn ảnh Key Visual đã sinh sẵn bằng Gemini Nano Banana + ảnh Unsplash chọn lọc
ASSET_BASE_URL = "/demo-assets/fptu-2027"
FPTU_VISUALS = {
    "week1_coming_soon": {
        "id": "d7e00000-0000-4000-8000-000000000901",
        "file": "fptu-week1-coming-soon.jpg",
        "name": "KV_Tuan1_ComingSoon_TuyenSinh_FPTU_2027.jpg",
        "folder": "folder_w1",
        "url": f"{ASSET_BASE_URL}/fptu-week1-coming-soon.jpg",
    },
    "week2_semiconductor": {
        "id": "d7e00000-0000-4000-8000-000000000902",
        "file": "fptu-week2-semiconductor-ai.jpg",
        "name": "KV_Tuan2_PhongLab_ViMach_BanDan_AI_FPTU.jpg",
        "folder": "folder_w2",
        "url": f"{ASSET_BASE_URL}/fptu-week2-semiconductor-ai.jpg",
    },
    "week2_software_biz": {
        "id": "d7e00000-0000-4000-8000-000000000903",
        "file": "fptu-week2-software-digital-biz.jpg",
        "name": "KV_Tuan2_KyThuatPhanMem_QuanTriKinhDoanhSo.jpg",
        "folder": "folder_w2",
        "url": f"{ASSET_BASE_URL}/fptu-week2-software-digital-biz.jpg",
    },
    "week2_campus_utilities": {
        "id": "d7e00000-0000-4000-8000-000000000904",
        "file": "fptu-week2-campus-utilities.jpg",
        "name": "KV_Tuan2_TienIchCampus_ThuVienXanh_Vovinam_CLB.jpg",
        "folder": "folder_w2",
        "url": f"{ASSET_BASE_URL}/fptu-week2-campus-utilities.jpg",
    },
    "week3_thpt_workshop": {
        "id": "d7e00000-0000-4000-8000-000000000905",
        "file": "fptu-week3-thpt-workshop.jpg",
        "name": "KV_Tuan3_Workshop_THPT_TraiNghiem_VR_Robotics.jpg",
        "folder": "folder_w3",
        "url": f"{ASSET_BASE_URL}/fptu-week3-thpt-workshop.jpg",
    },
    "week3_openday_kol": {
        "id": "d7e00000-0000-4000-8000-000000000906",
        "file": "fptu-week3-openday-kol.jpg",
        "name": "KV_Tuan3_FPTU_OpenDay_2027_GiaoLuu_SanKhau.jpg",
        "folder": "folder_w3",
        "url": f"{ASSET_BASE_URL}/fptu-week3-openday-kol.jpg",
    },
    "week4_ojt_press": {
        "id": "d7e00000-0000-4000-8000-000000000907",
        "file": "fptu-week4-ojt-press.jpg",
        "name": "KV_Tuan4_BaoChi_KyThucTapDoanhNghiep_OJT_FPTSoftware.jpg",
        "folder": "folder_w4",
        "url": f"{ASSET_BASE_URL}/fptu-week4-ojt-press.jpg",
    },
}

UNSPLASH_CAMPUS_PHOTOS = [
    {
        "id": "d7e00000-0000-4000-8000-000000000908",
        "name": "Anh_HocBong_NguyenVanDao_SinhVienTieuBieu.jpg",
        "folder": "folder_w1",
        "url": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "id": "d7e00000-0000-4000-8000-000000000909",
        "name": "Anh_KhongGian_HocNhom_ThuVien_FPTU.jpg",
        "folder": "folder_w2",
        "url": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "id": "d7e00000-0000-4000-8000-000000000910",
        "name": "Anh_HoiThao_TuVanHuongNghiep_HocSinhLop12.jpg",
        "folder": "folder_w3",
        "url": "https://images.unsplash.com/photo-1540575467063-178a50c2df87?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "id": "d7e00000-0000-4000-8000-000000000911",
        "name": "Anh_KySuTre_LamViecDuAnQuocTe_OJT.jpg",
        "folder": "folder_w4",
        "url": "https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=1200&q=80",
    },
]


# ==============================================================================
# 2. DANH MỤC 7 GÓI TRUYỀN THÔNG ĐA LĨNH VỰC (CHUẨN PACKAGE OFFERING VALIDATOR)
# ==============================================================================
def deliverable(
    did: str,
    service_type: str,
    name: str,
    quantity: int,
    unit: str,
    description: str,
    criteria: str,
    rev_limit: int = 2,
) -> dict[str, Any]:
    return {
        "id": did,
        "serviceType": service_type,
        "name": name,
        "quantity": quantity,
        "unit": unit,
        "description": description,
        "acceptanceCriteria": criteria,
        "revisionLimit": rev_limit,
    }


def build_flagship_fptu_deliverables() -> list[dict[str, Any]]:
    """7 hạng mục phủ đủ 7 loại dịch vụ chuẩn của Gói Tuyển sinh Đại học FPT 2027 (4 Tuần)."""
    return [
        deliverable(
            DELIV_POST_ID,
            "SOCIAL_POST",
            "Chuỗi bài viết đa nền tảng theo 4 chặng tuyển sinh khóa K23",
            8,
            "bài",
            (
                "Triển khai 08 bài viết chuyên biệt xuyên suốt 4 tuần trên Facebook, Instagram, TikTok và Threads: "
                "(1) Coming Soon khởi động mùa tuyển sinh 2027, (2) Công bố Học bổng Nguyễn Văn Đạo, "
                "(3) Chuyên sâu ngành Vi mạch bán dẫn & AI, (4) Nhóm ngành Kỹ thuật phần mềm & Kinh tế số, "
                "(5) Khám phá hệ sinh thái tiện ích Campus 5 cơ sở, (6) Điểm nhấn chuỗi Workshop THPT & mở cổng xét học bổng, "
                "(7) Câu chuyện học sinh lớp 12 sau buổi Workshop, và (8) Nhắc hạn nộp hồ sơ xét tuyển đợt 1."
            ),
            (
                "Đầy đủ bộ ảnh đúng kích thước từng nền tảng, thông tin học bổng 50%-70%-100%, kỳ thực tập OJT học kỳ 6 "
                "và đường dẫn https://tuyensinh.fpt.edu.vn được Ban Tuyển sinh ĐH FPT phê duyệt."
            ),
            3,
        ),
        deliverable(
            DELIV_VIDEO_ID,
            "SHORT_VIDEO",
            "Chuỗi video dọc Reels & TikTok trải nghiệm thực tế Campus và Workshop",
            3,
            "video",
            (
                "Sản xuất 03 video ngắn định dạng 9:16 (60-90 giây): (1) Hé lộ kiến trúc xanh tại 5 cơ sở Hà Nội, Đà Nẵng, "
                "Quy Nhơn, TP.HCM, Cần Thơ; (2) Một ngày học tại phòng Lab bán dẫn, rèn luyện Vovinam và sinh hoạt CLB; "
                "(3) Recap không khí sôi nổi của học sinh THPT tại chuỗi Workshop trải nghiệm."
            ),
            "Độ phân giải Full HD 60fps, phụ đề chuẩn nhận diện màu cam FPT, thời lượng 60-90 giây và âm nhạc bản quyền.",
            2,
        ),
        deliverable(
            DELIV_WORKSHOP_ID,
            "WORKSHOP_SUPPORT",
            "Chuỗi Workshop phổ biến tiện ích học đường ĐH FPT cho học sinh THPT",
            2,
            "buổi",
            (
                "Phối hợp tổ chức 02 buổi Workshop trực tiếp dành cho học sinh lớp 12 nhằm giới thiệu hệ sinh thái tiện ích "
                "của Trường Đại học FPT (phòng Lab Vi mạch & AI, thư viện, ký túc xá, sân Vovinam, hơn 40 CLB sinh viên, "
                "học kỳ doanh nghiệp OJT) kèm khu vực trải nghiệm thực tế ảo VR và cánh tay robot."
            ),
            "Kịch bản chi tiết, danh sách diễn giả giảng viên, phương án đón tiếp học sinh THPT và báo cáo số lượng đăng ký sau buổi.",
            2,
        ),
        deliverable(
            DELIV_EVENT_ID,
            "EVENT_PLANNING",
            "Kế hoạch tổng thể Ngày hội FPTU Open Day 2027: Một ngày làm sinh viên",
            1,
            "sự kiện",
            (
                "Xây dựng kịch bản chương trình, sơ đồ phân luồng đón đoàn xe các trường THPT, khu gian hàng demo đồ án "
                "công nghệ, bàn tư vấn hồ sơ Học bổng Nguyễn Văn Đạo và phương án truyền thông tại khuôn viên trường."
            ),
            "Bàn giao đầy đủ Agenda, danh sách nhân sự điều phối tại chỗ, dự toán hậu cần và được duyệt trước ngày sự kiện 5 ngày.",
            2,
        ),
        deliverable(
            DELIV_KOL_ID,
            "KOL_BOOKING",
            "Mời KOL Công nghệ & Đại sứ Sinh viên FPTU đồng hành tại Workshop và Open Day",
            2,
            "KOL",
            (
                "Lựa chọn, đàm phán và xây dựng định hướng nội dung cho 02 gương mặt đồng hành: (1) Nhà sáng tạo nội dung "
                "công nghệ giao lưu cùng học sinh lớp 12 tại Workshop; (2) Đại sứ sinh viên khóa K19 vừa hoàn thành kỳ "
                "thực tập OJT tại FPT Software chia sẻ kinh nghiệm học tập thực tế."
            ),
            "Hồ sơ đề xuất KOL, biên bản thống nhất lịch trình xuất hiện, kịch bản phát biểu và bài đăng tổng kết trên kênh cá nhân.",
            2,
        ),
        deliverable(
            DELIV_EMAIL_ID,
            "EMAIL_NEWSLETTER",
            "Bản tin Email cẩm nang chọn ngành 2027 & vé mời tham dự Workshop THPT",
            1,
            "bản tin",
            (
                "Thiết kế mẫu bản tin HTML cá nhân hóa gửi tới danh sách học sinh lớp 12 đã đăng ký quan tâm, đính kèm "
                "cẩm nang tóm tắt 6 nhóm ngành đào tạo, mức học bổng và mã QR xác nhận tham dự buổi Workshop trải nghiệm."
            ),
            "Hiển thị chuẩn trên Gmail di động và máy tính, tỷ lệ gửi thành công đạt trên 98% trên tập người nhận đã đồng ý.",
            2,
        ),
        deliverable(
            DELIV_PRESS_ID,
            "PRESS_RECOMMENDATION",
            "Tuyến bài báo chí chính thống tổng kết chuỗi Workshop THPT & đào tạo OJT",
            2,
            "bài",
            (
                "Biên soạn 02 bài thông cáo và phân tích chuyên sâu gửi đăng trên VnExpress (Chuyên mục Giáo dục) và "
                "Báo Thanh Niên / Dân Trí ở tuần cuối chiến dịch: tổng kết hoạt động hướng nghiệp cho học sinh THPT "
                "và mô hình gắn kết đào tạo đại học với doanh nghiệp công nghệ năm 2027."
            ),
            "Chuẩn văn phong báo chí chính luận, trích dẫn chính xác phát ngôn đại diện nhà trường và kèm bộ ảnh thực tế chất lượng cao.",
            2,
        ),
    ]


def build_multi_industry_catalog() -> list[dict[str, Any]]:
    """6 gói truyền thông đa lĩnh vực khác nhau của SE08 Digital Agency, mỗi gói 5-6 hạng mục đặc thù."""
    def uid(tag: str) -> str:
        return java_name_uuid_from_bytes(f"se08-catalog-deliv:{tag}")

    return [
        {
            "id": CATALOG_PKG_TECH_ID,
            "name": "Gói Công nghệ & Giải pháp B2B SaaS: Ra mắt Nền tảng Quản trị Số (6 Tuần)",
            "duration_weeks": 6,
            "budget_amount": 240000000,
            "scope_description": (
                "Dành cho doanh nghiệp phần mềm, AI và Cloud khi ra mắt phiên bản sản phẩm mới tới nhóm giám đốc công nghệ (CTO), "
                "quản lý vận hành và cộng đồng kỹ sư tại Việt Nam."
            ),
            "deliverables": [
                deliverable(
                    uid("tech-post"), "SOCIAL_POST",
                    "Chuỗi bài phân tích bài toán vận hành & Case Study chuyển đổi số thực tế", 10, "bài",
                    "Gồm 03 bài phân tích chi phí vận hành cũ, 04 bài giới thiệu kiến trúc bảo mật sản phẩm và 03 bài trích dẫn số liệu triển khai thực tế tại doanh nghiệp.",
                    "Số liệu kỹ thuật được đội ngũ sản phẩm xác nhận, trình bày kèm sơ đồ trực quan dễ đọc.", 2,
                ),
                deliverable(
                    uid("tech-video"), "SHORT_VIDEO",
                    "Video hướng dẫn nhanh tính năng cốt lõi trong 60 giây (Product Walkthrough)", 4, "video",
                    "Quay màn hình giao diện thực tế kết hợp lời dẫn cô đọng giải quyết từng tác vụ cụ thể của người dùng doanh nghiệp.",
                    "Hình ảnh giao diện sắc nét 1080p, có phụ đề tiếng Việt và lời kêu gọi đăng ký dùng thử 14 ngày.", 2,
                ),
                deliverable(
                    uid("tech-workshop"), "WORKSHOP_SUPPORT",
                    "Hội thảo chuyên đề ứng dụng AI trong quản trị vận hành dành cho lãnh đạo doanh nghiệp", 2, "buổi",
                    "Tổ chức 01 buổi hội thảo trực tiếp tại TP.HCM và 01 buổi trực tuyến kết nối chuyên gia tư vấn giải pháp cùng khách mời.",
                    "Thu hút tối thiểu 80 đại diện doanh nghiệp đăng ký tham dự và bàn giao danh sách câu hỏi chuyên môn.", 2,
                ),
                deliverable(
                    uid("tech-press"), "PRESS_RECOMMENDATION",
                    "Tuyến bài chuyên môn công nghệ trên VnExpress Số hóa & Tạp chí Diễn đàn Doanh nghiệp", 3, "bài",
                    "Đề xuất góc tiếp cận thị trường, soạn thảo bài viết phỏng vấn nhà sáng lập và điều phối lịch đăng báo điện tử.",
                    "Bài viết tuân thủ quy định biên tập báo chí và xuất bản đúng tuần ra mắt sản phẩm.", 2,
                ),
                deliverable(
                    uid("tech-kol"), "KOL_BOOKING",
                    "Chuyên gia công nghệ & Quản trị doanh nghiệp đánh giá trải nghiệm thực tế", 2, "KOL",
                    "Mời 02 chuyên gia uy tín trong cộng đồng công nghệ dùng thử sản phẩm và viết bài chia sẻ góc nhìn độc lập.",
                    "Nội dung trung thực, nêu rõ ưu điểm kỹ thuật và gắn đường dẫn trang đăng ký chính thức.", 2,
                ),
                deliverable(
                    uid("tech-email"), "EMAIL_NEWSLETTER",
                    "Chuỗi bản tin Email hướng dẫn khai thác sản phẩm cho khách hàng đăng ký dùng thử", 2, "bản tin",
                    "Gồm 01 bản tin chào mừng kèm tài liệu hướng dẫn khởi tạo nhanh và 01 bản tin tổng hợp mẹo tự động hóa quy trình.",
                    "Cá nhân hóa theo tên công ty khách hàng và tích hợp nút đặt lịch tư vấn 1-1.", 2,
                ),
            ],
        },
        {
            "id": CATALOG_PKG_FNB_ID,
            "name": "Gói F&B & Chuỗi Cửa hàng Đồ uống: Khai trương Cụm Quán Mới & Menu Theo Mùa (4 Tuần)",
            "duration_weeks": 4,
            "budget_amount": 135000000,
            "scope_description": (
                "Thiết kế riêng cho thương hiệu cà phê, trà trái cây và nhà hàng khi mở mới điểm bán hoặc tung bộ sưu tập đồ uống "
                "theo mùa, tập trung kéo khách ghé quán trong 30 ngày đầu."
            ),
            "deliverables": [
                deliverable(
                    uid("fnb-post"), "SOCIAL_POST",
                    "Chuỗi bài kể chuyện nguyên liệu nông sản bản địa, không gian quán & ưu đãi khai trương", 12, "bài",
                    "Chia thành 3 nhóm bài rõ rệt: câu chuyện vùng nguyên liệu trà và cà phê, góc ngồi làm việc sáng thoáng tại cửa hàng mới, và chương trình mời bạn bè khung giờ chiều.",
                    "Ảnh chụp món uống dưới ánh sáng tự nhiên, nêu rõ địa chỉ cửa hàng và thời gian áp dụng ưu đãi.", 2,
                ),
                deliverable(
                    uid("fnb-video"), "SHORT_VIDEO",
                    "Reels & TikTok cận cảnh pha chế tại quầy bar và trải nghiệm khách hàng ngày đầu mở cửa", 6, "video",
                    "Ghi hình âm thanh pha chế chân thực (ASMR), thao tác của barista và cảm nhận tự nhiên của khách ghé quán.",
                    "Nhịp dựng nhanh trong 30-45 giây, bắt trọn màu sắc tươi mới của dòng đồ uống theo mùa.", 2,
                ),
                deliverable(
                    uid("fnb-event"), "EVENT_PLANNING",
                    "Sự kiện dùng thử Menu mới (Tasting Day) cuối tuần đầu khai trương", 1, "sự kiện",
                    "Lên kịch bản đón khách trải nghiệm 4 món mới, khu vực chụp ảnh lấy liền và phiếu quà tặng cho lần ghé tiếp theo.",
                    "Đảm bảo luồng phục vụ thông suốt tại quầy trong khung giờ cao điểm 09:00-11:30 và 19:00-21:00.", 2,
                ),
                deliverable(
                    uid("fnb-kol"), "KOL_BOOKING",
                    "Food Reviewer địa phương trải nghiệm thực tế và gợi ý món ngon tại quán", 5, "KOL",
                    "Kết nối 05 nhà sáng tạo nội dung ẩm thực có tệp người xem đúng khu vực quận/thành phố nơi cửa hàng vừa mở.",
                    "Mỗi bài đăng có video hoặc bộ ảnh chụp trực tiếp tại quán và gắn thẻ vị trí cửa hàng chính xác.", 2,
                ),
                deliverable(
                    uid("fnb-press"), "PRESS_RECOMMENDATION",
                    "Bài giới thiệu không gian thưởng thức & xu hướng đồ uống mùa mới trên chuyên trang giới trẻ", 1, "bài",
                    "Biên tập bài giới thiệu câu chuyện thương hiệu và thiết kế kiến trúc cửa hàng mới trên Kênh14 hoặc Znews.",
                    "Hình ảnh không gian quán đạt chuẩn biên tập và lên trang đúng dịp cuối tuần khai trương.", 2,
                ),
                deliverable(
                    uid("fnb-email"), "EMAIL_NEWSLETTER",
                    "Bản tin gửi khách hàng thân thiết tặng mã ưu đãi dùng thử bộ sưu tập mới", 1, "bản tin",
                    "Gửi thư mời riêng tới tệp hội viên hiện có để tri ân và mời ghé thăm chi nhánh mới.",
                    "Mã ưu đãi hiển thị rõ ràng, dễ quét tại quầy thu ngân.", 2,
                ),
            ],
        },
        {
            "id": CATALOG_PKG_REALESTATE_ID,
            "name": "Gói Bất động sản Đô thị & Nghỉ dưỡng: Giới thiệu Phân khu Xanh & Nhà mẫu (8 Tuần)",
            "duration_weeks": 8,
            "budget_amount": 320000000,
            "scope_description": (
                "Phục vụ chủ đầu tư và đơn vị phân phối dự án khu đô thị sinh thái hoặc căn hộ cao cấp, tập trung minh bạch hóa "
                "pháp lý, tiến độ hạ tầng thực tế và tổ chức tham quan nhà mẫu."
            ),
            "deliverables": [
                deliverable(
                    uid("re-post"), "SOCIAL_POST",
                    "Chuỗi bài phân tích quy hoạch hạ tầng vùng, thiết kế căn hộ thông thoáng & tiến độ thi công", 12, "bài",
                    "Cung cấp bản đồ kết nối giao thông, mặt bằng công năng chi tiết từng loại căn hộ, hệ thống công viên nội khu và ảnh cập nhật công trường hai tuần một lần.",
                    "Mọi thông số diện tích, pháp lý và chính sách thanh toán khớp tuyệt đối với hồ sơ công bố của chủ đầu tư.", 3,
                ),
                deliverable(
                    uid("re-video"), "SHORT_VIDEO",
                    "Video Flycam tiến độ thực tế dự án & chuyến tham quan chi tiết căn hộ mẫu", 4, "video",
                    "Kết hợp cảnh quay trên cao toàn khu đô thị lúc bình minh và góc máy dẫn người xem đi qua phòng khách, bếp, ban công nhà mẫu.",
                    "Chất lượng 4K sắc nét, đồ họa chú thích khoảng cách tới trường học, bệnh viện và trục đường chính.", 2,
                ),
                deliverable(
                    uid("re-event"), "EVENT_PLANNING",
                    "Lễ giới thiệu phân khu mới & Trải nghiệm thực tế khu nhà mẫu cuối tuần", 1, "sự kiện",
                    "Tổ chức đón tiếp khách hàng gia đình, khu vực sa bàn tư vấn chuyên sâu và bàn giải đáp chính sách vay ngân hàng.",
                    "Kịch bản trang trọng, chu đáo từ khâu đón xe đến khu vực tư vấn riêng từng gia đình.", 2,
                ),
                deliverable(
                    uid("re-workshop"), "WORKSHOP_SUPPORT",
                    "Tọa đàm quy hoạch đô thị xanh & bài toán tài chính mua nhà an cư cho gia đình trẻ", 1, "buổi",
                    "Mời kiến trúc sư cảnh quan và chuyên gia tài chính cá nhân giải đáp trực tiếp cách cân đối dòng tiền mua nhà.",
                    "Nội dung thiết thực, trung lập, hỗ trợ người mua hiểu rõ phương án tài chính dài hạn.", 2,
                ),
                deliverable(
                    uid("re-press"), "PRESS_RECOMMENDATION",
                    "Tuyến bài phân tích tiềm năng hạ tầng khu vực trên CafeF, VnEconomy & Báo Đầu Tư", 3, "bài",
                    "Biên soạn loạt bài góc nhìn quy hoạch đô thị vệ tinh, xu hướng sống xanh và cập nhật cột mốc thi công dự án.",
                    "Đảm bảo tính khách quan báo chí, số liệu quy hoạch dẫn nguồn cơ quan chức năng.", 2,
                ),
                deliverable(
                    uid("re-email"), "EMAIL_NEWSLETTER",
                    "Bản tin cập nhật ảnh tiến độ công trường & bảng chính sách thanh toán gửi khách quan tâm", 2, "bản tin",
                    "Định kỳ gửi ảnh thực tế hạng mục đang thi công kèm lịch mở cửa nhà mẫu để duy trì kết nối với khách hàng.",
                    "Bố cục sang trọng, tải nhanh trên điện thoại và có nút đặt lịch xe đưa đón tham quan.", 2,
                ),
            ],
        },
        {
            "id": CATALOG_PKG_BEAUTY_ID,
            "name": "Gói Dược mỹ phẩm & Chăm sóc Sức khỏe: Ra mắt Dòng Phục hồi Da Khoa học (4 Tuần)",
            "duration_weeks": 4,
            "budget_amount": 165000000,
            "scope_description": (
                "Dành cho thương hiệu dược mỹ phẩm và chăm sóc sức khỏe chính hãng, đặt trọng tâm vào kiến thức da liễu chuẩn xác, "
                "minh bạch bảng thành phần và tuân thủ nghiêm ngặt quy định quảng cáo mỹ phẩm."
            ),
            "deliverables": [
                deliverable(
                    uid("beauty-post"), "SOCIAL_POST",
                    "Chuỗi bài giải thích cơ chế hoạt chất, hướng dẫn kết hợp chu trình dưỡng da sáng tối", 10, "bài",
                    "Giải thích dễ hiểu vai trò của từng hoạt chất phục hồi hàng rào bảo vệ da, cách dùng cho da nhạy cảm và lưu ý chống nắng.",
                    "Tuyệt đối không dùng từ ngữ điều trị y khoa trái phép hoặc cam kết kết quả phi thực tế; kiểm duyệt nội dung trước khi đăng.", 3,
                ),
                deliverable(
                    uid("beauty-video"), "SHORT_VIDEO",
                    "Video cận cảnh kết cấu thẩm thấu (Texture Test) & nhật ký chăm sóc da thực tế", 5, "video",
                    "Quay cận cảnh chất kem/serum trên da dưới ánh sáng chuẩn màu, hướng dẫn lượng dùng vừa đủ cho từng loại da.",
                    "Ánh sáng trung thực không dùng bộ lọc làm mịn da quá đà, thể hiện đúng chất lượng sản phẩm.", 2,
                ),
                deliverable(
                    uid("beauty-workshop"), "WORKSHOP_SUPPORT",
                    "Buổi soi da miễn phí & trò chuyện chăm sóc da giao mùa cùng chuyên gia da liễu", 1, "buổi",
                    "Tổ chức buổi gặp gỡ quy mô 60 khách hàng để kiểm tra độ ẩm da bằng máy phân tích và tư vấn chu trình cá nhân hóa.",
                    "Quy trình vệ sinh thiết bị soi da sạch sẽ, không gian thân thiện và chuẩn bị bộ mẫu thử mang về.", 2,
                ),
                deliverable(
                    uid("beauty-kol"), "KOL_BOOKING",
                    "Beauty Creator uy tín chia sẻ cảm nhận sau 14 ngày trải nghiệm sản phẩm", 4, "KOL",
                    "Hợp tác với 04 nhà sáng tạo nội dung mảng chăm sóc da khoa học để ghi lại cảm nhận thực tế về độ dịu nhẹ và cấp ẩm.",
                    "Nội dung tuân thủ quy chuẩn truyền thông mỹ phẩm, nêu rõ tình trạng da của người trải nghiệm.", 2,
                ),
                deliverable(
                    uid("beauty-press"), "PRESS_RECOMMENDATION",
                    "Bài chuyên đề xu hướng chăm sóc da tối giản, an toàn trên Tạp chí Đẹp & Báo Phụ Nữ", 2, "bài",
                    "Giới thiệu nguồn gốc nghiên cứu dòng sản phẩm mới và lời khuyên bảo vệ làn da trước thời tiết nắng nóng.",
                    "Văn phong tinh tế, thông tin xuất xứ và số công bố mỹ phẩm rõ ràng.", 2,
                ),
                deliverable(
                    uid("beauty-email"), "EMAIL_NEWSLETTER",
                    "Bản tin cẩm nang phân biệt tình trạng da & ưu đãi bộ sản phẩm dùng thử 15ml", 1, "bản tin",
                    "Gửi tài liệu tóm tắt cách nhận diện da thiếu ẩm kèm mã quà tặng mẫu thử cho khách hàng đăng ký mới.",
                    "Thiết kế trang nhã, hình ảnh nhẹ và đường dẫn tới gian hàng chính hãng.", 2,
                ),
            ],
        },
        {
            "id": CATALOG_PKG_ECOM_ID,
            "name": "Gói Thương mại Điện tử & Bán lẻ: Chiến dịch Lễ hội Mua sắm Mega Sale (4 Tuần)",
            "duration_weeks": 4,
            "budget_amount": 150000000,
            "scope_description": (
                "Tối ưu chuyển đổi đơn hàng cho thương hiệu bán lẻ gia dụng, thời trang và điện tử tiêu dùng trong các kỳ "
                "mua sắm cao điểm hàng tháng trên mạng xã hội và sàn thương mại điện tử."
            ),
            "deliverables": [
                deliverable(
                    uid("ecom-post"), "SOCIAL_POST",
                    "Chuỗi bài gợi ý giỏ hàng thông minh, so sánh dòng sản phẩm & lịch săn mã ưu đãi", 14, "bài",
                    "Phân bổ từ giai đoạn giới thiệu sản phẩm chủ lực, hướng dẫn ghép mã tiết kiệm đến nhắc khung giờ ưu đãi 0h-9h-12h-20h.",
                    "Giá niêm yết và điều kiện áp dụng mã ưu đãi chính xác 100% theo chương trình trên gian hàng.", 2,
                ),
                deliverable(
                    uid("ecom-video"), "SHORT_VIDEO",
                    "Chuỗi video mở hộp thực tế, kiểm tra độ bền và hướng dẫn sử dụng nhanh tại nhà", 8, "video",
                    "Tập trung giải đáp các thắc mắc phổ biến nhất của người mua trước khi chốt đơn như kích thước thật, phụ kiện đi kèm và chế độ bảo hành.",
                    "Mở đầu trực diện vào công năng sản phẩm trong 3 giây đầu, gắn rõ mã sản phẩm trong phần mô tả.", 2,
                ),
                deliverable(
                    uid("ecom-kol"), "KOL_BOOKING",
                    "KOC gia đình trẻ & đánh giá đồ gia dụng trải nghiệm sản phẩm tại không gian sống thật", 4, "KOL",
                    "Lựa chọn 04 KOC có tỷ lệ tương tác tự nhiên cao để quay video sử dụng sản phẩm trong sinh hoạt hàng ngày.",
                    "Bàn giao file video gốc kèm quyền sử dụng lại trên kênh truyền thông chính thức của nhãn hàng trong 3 tháng.", 2,
                ),
                deliverable(
                    uid("ecom-email"), "EMAIL_NEWSLETTER",
                    "Chuỗi bản tin mở quyền đặt trước ưu đãi sớm cho tệp khách hàng cũ", 2, "bản tin",
                    "Gửi thông báo trước 24 giờ cho khách hàng đã từng mua sắm kèm mã giảm giá tri ân riêng.",
                    "Phân nhóm đúng danh mục sản phẩm khách hàng quan tâm và theo dõi tỷ lệ nhấp chuột.", 2,
                ),
                deliverable(
                    uid("ecom-press"), "PRESS_RECOMMENDATION",
                    "Bài tổng hợp xu hướng mua sắm tiêu dùng thông minh dịp cuối năm trên báo điện tử", 1, "bài",
                    "Giới thiệu các dòng sản phẩm tiết kiệm điện năng, tiện lợi và chính sách hậu mãi chính hãng của thương hiệu.",
                    "Xuất bản trước ngày cao điểm chiến dịch 3 ngày để củng cố độ tin cậy thương hiệu.", 2,
                ),
            ],
        },
        {
            "id": CATALOG_PKG_TRAVEL_ID,
            "name": "Gói Du lịch & Nghỉ dưỡng Biển: Quảng bá Mùa Hè Đà Nẵng - Hội An (6 Tuần)",
            "duration_weeks": 6,
            "budget_amount": 195000000,
            "scope_description": (
                "Đồng hành cùng khu nghỉ dưỡng biển, khách sạn và tổ hợp văn hóa giải trí miền Trung thu hút khách gia đình "
                "và khách đoàn doanh nghiệp trong mùa du lịch cao điểm."
            ),
            "deliverables": [
                deliverable(
                    uid("travel-post"), "SOCIAL_POST",
                    "Chuỗi bài gợi ý lịch trình 3 ngày 2 đêm, ẩm thực địa phương & tiện ích cho gia đình có trẻ nhỏ", 10, "bài",
                    "Kể câu chuyện trọn vẹn một kỳ nghỉ từ đón bình minh biển Mỹ Khê, thưởng thức hải sản bản địa, lớp học làm đèn lồng đến khu vui chơi trẻ em.",
                    "Hình ảnh nắng vàng biển xanh rực rỡ, thông tin hạng phòng và chính sách đặt sớm rõ ràng.", 2,
                ),
                deliverable(
                    uid("travel-video"), "SHORT_VIDEO",
                    "Thước phim ngắn cảm xúc bình minh trên biển, hồ bơi vô cực & trải nghiệm làng nghề", 5, "video",
                    "Ghi lại những khoảnh khắc thư giãn chân thực của gia đình và cặp đôi tại khu nghỉ dưỡng và phố cổ Hội An.",
                    "Màu phim trong trẻo, âm thanh sóng biển và nhạc nền nhẹ nhàng, truyền tải cảm giác nghỉ ngơi trọn vẹn.", 2,
                ),
                deliverable(
                    uid("travel-event"), "EVENT_PLANNING",
                    "Đêm nhạc Acoustic & Tiệc nướng hải sản bên bờ biển mở màn mùa hè", 1, "sự kiện",
                    "Thiết kế không gian sân khấu ngoài trời trên bãi cát, thực đơn ẩm thực miền Trung và hoạt động giao lưu cho du khách lưu trú.",
                    "Có phương án dự phòng thời tiết đầy đủ và đảm bảo an toàn khu vực bãi biển.", 2,
                ),
                deliverable(
                    uid("travel-kol"), "KOL_BOOKING",
                    "Gia đình Travel Blogger ghi hình kỳ nghỉ thực tế 3 ngày 2 đêm", 3, "KOL",
                    "Mời 03 gia đình/nhà sáng tạo nội dung du lịch lưu trú thực tế và chia sẻ kinh nghiệm di chuyển, ăn uống, nghỉ ngơi chi tiết.",
                    "Mỗi KOL đăng tải tối thiểu 01 video Reels/TikTok và 01 bộ ảnh kèm đánh giá thực tế.", 2,
                ),
                deliverable(
                    uid("travel-press"), "PRESS_RECOMMENDATION",
                    "Tuyến bài gợi ý điểm đến nghỉ dưỡng gia đình miền Trung trên VnExpress Du lịch & Tuổi Trẻ", 2, "bài",
                    "Biên soạn bài viết cẩm nang du lịch hè kết hợp giới thiệu các hoạt động văn hóa bản địa đặc sắc tại điểm đến.",
                    "Lên trang đầu tháng cao điểm hè với bộ ảnh chất lượng biên tập báo chí.", 2,
                ),
                deliverable(
                    uid("travel-email"), "EMAIL_NEWSLETTER",
                    "Bản tin giới thiệu gói hội nghị kết hợp nghỉ dưỡng (MICE) gửi bộ phận Nhân sự doanh nghiệp", 1, "bản tin",
                    "Giới thiệu sức chứa phòng hội nghị, tiệc tối gắn kết đội ngũ và ưu đãi đặt đoàn sớm cho doanh nghiệp.",
                    "Đính kèm hồ sơ năng lực sảnh tiệc và thông tin đầu mối phụ trách khách đoàn.", 2,
                ),
            ],
        },
    ]


# ==============================================================================
# 3. MASTER BRIEF 6 KHỐI & DANH SÁCH 20 CÔNG VIỆC CHIẾN DỊCH 4 TUẦN ĐH FPT 2027
# ==============================================================================
def build_campaign_brief_json(now_iso: str) -> dict[str, Any]:
    master_brief_html = (
        "<h3>1. Bối cảnh &amp; Hành trình chiến dịch 4 tuần</h3>"
        "<p>Chiến dịch Tuyển sinh khóa K23 (năm 2027) của Trường Đại học FPT do <strong>SE08 Digital Agency</strong> "
        "phối hợp cùng <strong>Ban Tuyển sinh Đại học FPT</strong> triển khai xuyên suốt 4 tuần liên tiếp: "
        "<strong>Tuần 1</strong> mở màn Coming Soon &amp; công bố Học bổng Nguyễn Văn Đạo; "
        "<strong>Tuần 2</strong> đi sâu vào các ngành học mũi nhọn (Thiết kế Vi mạch bán dẫn, AI, Kỹ thuật phần mềm, Kinh tế số) "
        "và hệ sinh thái tiện ích học đường tại 5 cơ sở; "
        "<strong>Tuần 3</strong> tổ chức chuỗi Workshop phổ biến tiện ích trực tiếp cho học sinh THPT cùng ngày hội FPTU Open Day 2027; "
        "<strong>Tuần 4</strong> lan tỏa trên báo chí chính thống (VnExpress, Thanh Niên, Dân Trí) và đa nền tảng để chốt hồ sơ xét tuyển đợt 1.</p>"
        "<h3>2. Công chúng mục tiêu &amp; Thông điệp cốt lõi</h3>"
        "<p>Hướng trực tiếp tới học sinh lớp 12 (khóa 2k9) yêu thích môi trường đại học công nghệ năng động, giàu trải nghiệm thực tế "
        "và quý phụ huynh cần thông tin rõ ràng về mức Học bổng Nguyễn Văn Đạo (50%, 70%, 100% học phí toàn khóa) cũng như "
        "học kỳ thực tập tại doanh nghiệp (On-the-Job Training - OJT) ngay từ học kỳ 6.</p>"
        "<h3>3. Hệ thống kênh triển khai đồng bộ</h3>"
        "<ul>"
        "<li><strong>4 nền tảng mạng xã hội:</strong> Facebook Fanpage Tuyển sinh Đại học FPT, Instagram, TikTok và Threads.</li>"
        "<li><strong>Hoạt động trực tiếp tại trường THPT &amp; Campus:</strong> 02 buổi Workshop trải nghiệm tiện ích, VR/Robotics và 01 ngày hội Open Day.</li>"
        "<li><strong>Báo chí, Email &amp; KOL:</strong> VnExpress, Báo Thanh Niên, Dân Trí, bản tin Email học sinh lớp 12 và Creator công nghệ Schannel / Duy Luân.</li>"
        "</ul>"
    )
    return {
        "campaignFormats": ["DIGITAL", "EVENT", "PR"],
        "conceptType": "COMBINED",
        "conceptIdea": (
            "Đưa phòng Lab Vi mạch bán dẫn, Trí tuệ nhân tạo và hệ sinh thái tiện ích thực tế của 5 cơ sở Đại học FPT "
            "đến tận tay học sinh lớp 12 thông qua chuỗi nội dung đa nền tảng kết hợp Workshop trải nghiệm trực tiếp."
        ),
        "objectives": ["LEAD_GENERATION", "BRAND_AWARENESS", "EVENT_ATTENDANCE"],
        "targetAudiences": ["GEN_Z", "PARENTS", "STUDENTS"],
        "audienceInsights": ["PRICE_SENSITIVE", "QUALITY_FIRST", "CAREER_FOCUSED"],
        "audienceNote": (
            "Học sinh lớp 12 muốn nhìn thấy tận mắt phòng thực hành, thư viện, sân tập Vovinam, đời sống hơn 40 CLB và lắng nghe anh chị sinh viên kể chuyện đi OJT. "
            "Phụ huynh đặc biệt quan tâm điều kiện xét Học bổng Nguyễn Văn Đạo và đầu ra nghề nghiệp tại FPT Software cùng doanh nghiệp đối tác."
        ),
        "channels": ["FACEBOOK", "INSTAGRAM", "TIKTOK", "THREADS", "PR_NEWS"],
        "contentPillars": ["EDUCATION", "PRODUCT_STORY", "EVENT_RECAP", "TESTIMONIAL"],
        "primaryCta": "SIGN_UP",
        "eventFormat": "HYBRID",
        "eventConcept": (
            "Chuỗi Workshop phổ biến tiện ích học đường Đại học FPT cho học sinh THPT kết hợp Ngày hội FPTU Open Day 2027 "
            "tại khuôn viên trường với gian hàng trải nghiệm VR, cánh tay robot và bàn tư vấn học bổng trực tiếp."
        ),
        "eventLocation": "Hệ thống 5 cơ sở Trường Đại học FPT (Hà Nội, Đà Nẵng, Quy Nhơn, TP.HCM, Cần Thơ) & Cụm trường THPT trọng điểm",
        "expectedScale": "2.500 học sinh lớp 12 và phụ huynh tham gia chuỗi Workshop & Ngày hội FPTU Open Day 2027",
        "eventHighlights": (
            "Trải nghiệm kính VR tham quan 5 cơ sở, thử nghiệm mô hình Robotics, giao lưu cùng Creator công nghệ và nhận cẩm nang Học bổng Nguyễn Văn Đạo 2027."
        ),
        "digitalFormats": ["SOCIAL_POST", "SHORT_VIDEO", "INFOGRAPHIC", "LANDING_PAGE"],
        "kpiFocus": ["REACH", "ENGAGEMENT", "LEADS", "CTR"],
        "prAngles": ["EXPERT_OPINION", "CSR_COMMUNITY", "MILESTONE_LAUNCH"],
        "keyMessage": (
            "Tuyển sinh Đại học FPT 2027: Học thực hành tại hệ sinh thái Campus hiện đại ở 5 cơ sở, thực tập doanh nghiệp OJT từ học kỳ 6, "
            "cơ hội chinh phục Học bổng Nguyễn Văn Đạo tới 100% học phí."
        ),
        "brandTones": ["PROFESSIONAL", "INSPIRING", "YOUTHFUL"],
        "notes": (
            "Mọi bài đăng phải ghi rõ năm tuyển sinh 2027 (khóa K23), 3 mức Học bổng Nguyễn Văn Đạo (50%, 70%, 100%) và cổng đăng ký chính thức "
            "https://tuyensinh.fpt.edu.vn. Tuyệt đối không dùng từ ngữ cam kết phóng đại thiếu căn cứ hoặc hạ thấp đơn vị giáo dục khác."
        ),
        "generatedBrief": master_brief_html,
        "generatedBriefUpdatedAt": now_iso,
    }


def build_4week_plan_specs(now: datetime) -> list[dict[str, Any]]:
    """
    20 hạng mục công việc (19 hạng mục thuộc gói + 1 khảo sát phát sinh ngoài gói)
    trải đều 4 tuần của Chiến dịch Tuyển sinh Đại học FPT 2027.
    """
    def wi_id(idx: int) -> str:
        if idx == 6:
            return LIVE_WORK_ITEM_ID
        return f"d7e00000-0000-4000-8000-{700 + idx:012d}"

    def dt(days_offset: int, hour: int = 9) -> datetime:
        base = (now + timedelta(days=days_offset)).replace(hour=hour, minute=0, second=0, microsecond=0)
        return base

    return [
        # ---------------- TUẦN 1: COMING SOON & CÔNG BỐ HỌC BỔNG (ĐÃ HOÀN THÀNH) ----------------
        {
            "idx": 1,
            "week": 1,
            "work_item_id": wi_id(1),
            "deliverable_id": DELIV_POST_ID,
            "type": "POST",
            "name": "[Tuần 1 - Coming Soon] Khởi động mùa Tuyển sinh Đại học FPT 2027 tại 5 cơ sở toàn quốc",
            "assignee_key": "CREATOR",
            "status": "FINISHED",
            "due": dt(-13, 9),
            "visual_key": "week1_coming_soon",
            "platforms": ["FACEBOOK", "INSTAGRAM", "TIKTOK", "THREADS"],
            "post_status": "PUBLISHED",
            "description": "Bài mở màn chính thức mùa Tuyển sinh khóa K23 (2027) trên cả 4 nền tảng, giới thiệu thông điệp chủ đạo và hình ảnh không gian xanh tại 5 cơ sở Hà Nội, Đà Nẵng, Quy Nhơn, TP.HCM và Cần Thơ.",
            "criteria": "Đồng bộ nhận diện màu cam FPTU 2027, hiển thị rõ tên 5 cơ sở đào tạo và đường dẫn cổng thông tin tuyển sinh.",
            "caption": (
                "COMING SOON: CHÍNH THỨC KHỞI ĐỘNG MÙA TUYỂN SINH ĐẠI HỌC FPT 2027 (KHÓA K23)\n\n"
                "Mùa tuyển sinh năm 2027 tại Trường Đại học FPT đã sẵn sàng chào đón thế hệ tân sinh viên khóa K23 (2k9) "
                "tại cả 5 cơ sở đào tạo: Hà Nội, Đà Nẵng, Quy Nhơn, TP.HCM và Cần Thơ.\n\n"
                "Trong 4 tuần sắp tới, Ban Tuyển sinh Đại học FPT sẽ lần lượt công bố:\n"
                "- Quy chế xét tuyển năm 2027 và chương trình Học bổng Nguyễn Văn Đạo mức 50%, 70%, 100% học phí.\n"
                "- Thông tin chi tiết các chuyên ngành mũi nhọn: Thiết kế Vi mạch bán dẫn, Trí tuệ nhân tạo (AI), Kỹ thuật phần mềm, An toàn thông tin và Kinh tế số.\n"
                "- Lịch trình chuỗi Workshop trải nghiệm tiện ích học đường dành riêng cho học sinh THPT và Ngày hội FPTU Open Day 2027.\n\n"
                "Theo dõi ngay kênh chính thức và đăng ký nhận cẩm nang tuyển sinh sớm tại: https://tuyensinh.fpt.edu.vn"
            ),
            "hashtags": ["#DaiHocFPT", "#FPTUniversity", "#TuyenSinhFPTU2027", "#KhoaK23", "#2k9ChonNganh"],
            "metrics": {"reactions": 1840, "comments": 215, "shares": 164, "impressions": 48200, "reach": 36900, "clicks": 2410, "saves": 390},
        },
        {
            "idx": 2,
            "week": 1,
            "work_item_id": wi_id(2),
            "deliverable_id": DELIV_VIDEO_ID,
            "type": "SHORT_VIDEO",
            "name": "[Tuần 1 - Reels/TikTok #1] Hé lộ kiến trúc xanh 5 cơ sở Đại học FPT đón tân sinh viên K23",
            "assignee_key": "CREATOR_2",
            "status": "FINISHED",
            "due": dt(-11, 19),
            "visual_key": "week1_coming_soon",
            "platforms": ["TIKTOK", "INSTAGRAM", "FACEBOOK"],
            "post_status": "PUBLISHED",
            "description": "Video ngắn 60 giây điểm qua kiến trúc bậc thang phủ cây xanh đặc trưng, hồ sen, giảng đường và khu thể thao tại 5 cơ sở của Trường Đại học FPT.",
            "criteria": "Tỉ lệ dọc 9:16 sắc nét, chuyển cảnh mượt giữa 5 cơ sở và kèm phụ đề giới thiệu mùa tuyển sinh 2027.",
            "caption": (
                "Một vòng 5 cơ sở xanh mát của Trường Đại học FPT từ Bắc vào Nam trước thềm mùa Tuyển sinh 2027. "
                "Bạn hẹn gặp FPTU tại Hà Nội, Đà Nẵng, Quy Nhơn, TP.HCM hay Cần Thơ?\n\n"
                "Khám phá ngay thông tin khóa K23 tại: https://tuyensinh.fpt.edu.vn"
            ),
            "hashtags": ["#FPTUniversity", "#CampusFPTU", "#TuyenSinh2027", "#ReelsGiaoDuc", "#2k9"],
            "metrics": {"reactions": 3420, "comments": 412, "shares": 528, "impressions": 94500, "reach": 76200, "clicks": 3180, "saves": 845},
        },
        {
            "idx": 3,
            "week": 1,
            "work_item_id": wi_id(3),
            "deliverable_id": DELIV_POST_ID,
            "type": "POST",
            "name": "[Tuần 1 - Học bổng] Công bố quy chế Học bổng Nguyễn Văn Đạo 2027 mức 50%, 70% và 100%",
            "assignee_key": "CREATOR",
            "status": "FINISHED",
            "due": dt(-9, 9),
            "visual_key": "unsplash_0",
            "platforms": ["FACEBOOK", "INSTAGRAM", "THREADS"],
            "post_status": "PUBLISHED",
            "description": "Bài viết thông tin chi tiết điều kiện, phương thức xét cấp và 3 mức hỗ trợ học phí toàn khóa của chương trình Học bổng Nguyễn Văn Đạo năm 2027.",
            "criteria": "Trình bày minh bạch điều kiện hồ sơ thành tích học tập, kỳ thi học bổng và mốc thời gian nộp hồ sơ đợt 1.",
            "caption": (
                "CHÍNH THỨC CÔNG BỐ CHƯƠNG TRÌNH HỌC BỔNG NGUYỄN VĂN ĐẠO NĂM 2027\n\n"
                "Nhằm đồng hành cùng học sinh THPT có năng lực học tập, công nghệ và hoạt động phong trào xuất sắc trên toàn quốc, "
                "Trường Đại học FPT công bố quỹ Học bổng Nguyễn Văn Đạo năm 2027 dành cho tân sinh viên khóa K23:\n\n"
                "- Các mức học bổng áp dụng trong suốt toàn khóa học: 50%, 70% và 100% học phí.\n"
                "- Phương thức xét cấp: Xét thẳng theo thành tích học tập, giải thưởng cấp Tỉnh/Quốc gia hoặc tham dự kỳ thi giành học bổng của trường.\n"
                "- Áp dụng cho toàn bộ các chuyên ngành đào tạo tại 5 cơ sở trên cả nước.\n\n"
                "Tra cứu chi tiết tiêu chí xét học bổng năm 2027 tại: https://tuyensinh.fpt.edu.vn"
            ),
            "hashtags": ["#HocBongNguyenVanDao", "#DaiHocFPT", "#TuyenSinhFPTU2027", "#HocBongDaiHoc"],
            "metrics": {"reactions": 2690, "comments": 530, "shares": 612, "impressions": 67400, "reach": 51800, "clicks": 4520, "saves": 1120},
        },

        # ---------------- TUẦN 2: NGÀNH HỌC MŨI NHỌN, TIỆN ÍCH CAMPUS & MỞ ĐĂNG KÝ WORKSHOP ----------------
        {
            "idx": 4,
            "week": 2,
            "work_item_id": wi_id(4),
            "deliverable_id": DELIV_POST_ID,
            "type": "POST",
            "name": "[Tuần 2 - Ngành học #1] Thiết kế Vi mạch bán dẫn & Trí tuệ nhân tạo: Lộ trình thực hành phòng Lab",
            "assignee_key": "CREATOR",
            "status": "FINISHED",
            "due": dt(-7, 9),
            "visual_key": "week2_semiconductor",
            "platforms": ["FACEBOOK", "INSTAGRAM", "THREADS"],
            "post_status": "PUBLISHED",
            "description": "Bài phân tích chương trình đào tạo chuyên ngành Thiết kế Vi mạch bán dẫn và Trí tuệ nhân tạo (AI), hệ thống trang thiết bị phòng Lab và nhu cầu nhân lực thực tế.",
            "criteria": "Sử dụng bộ ảnh thực tế tại phòng Lab bán dẫn & AI, nêu rõ học phần thực hành trên bo mạch FPGA và dự án AI.",
            "caption": (
                "HỌC THIẾT KẾ VI MẠCH BÁN DẪN & TRÍ TUỆ NHÂN TẠO TẠI ĐẠI HỌC FPT CÓ GÌ ĐẶC BIỆT?\n\n"
                "Đón đầu nhu cầu nhân lực kỹ thuật chất lượng cao trong lĩnh vực chip bán dẫn và AI ứng dụng, sinh viên Trường Đại học FPT "
                "được tiếp cận trực tiếp môi trường thực hành ngay từ những học kỳ chuyên ngành đầu tiên:\n\n"
                "- Thực hành đo kiểm, thiết kế mạch số trên bo mạch FPGA và mô phỏng hệ thống AI tại phòng Lab chuyên dụng.\n"
                "- Giáo trình nhập khẩu bản quyền quốc tế kết hợp tăng cường ngoại ngữ tiếng Anh và ngoại ngữ thứ hai (Nhật/Trung/Hàn).\n"
                "- Tham gia học kỳ thực tập doanh nghiệp (OJT) từ học kỳ 6 tại FPT Semiconductor, FPT Smart Cloud và các đối tác công nghệ.\n\n"
                "Tìm hiểu khung chương trình đào tạo năm 2027 tại: https://tuyensinh.fpt.edu.vn"
            ),
            "hashtags": ["#ViMachBanDan", "#TriTueNhanTao", "#DaiHocFPT", "#TuyenSinhFPTU2027"],
            "metrics": {"reactions": 1950, "comments": 284, "shares": 230, "impressions": 52100, "reach": 39400, "clicks": 2890, "saves": 640},
        },
        {
            "idx": 5,
            "week": 2,
            "work_item_id": wi_id(5),
            "deliverable_id": DELIV_POST_ID,
            "type": "POST",
            "name": "[Tuần 2 - Ngành học #2] Kỹ thuật phần mềm, An toàn thông tin & Quản trị kinh doanh số 2027",
            "assignee_key": "CREATOR",
            "status": "FINISHED",
            "due": dt(-6, 10),
            "visual_key": "week2_software_biz",
            "platforms": ["FACEBOOK", "INSTAGRAM", "TIKTOK", "THREADS"],
            "post_status": "PUBLISHED",
            "description": "Giới thiệu nhóm ngành công nghệ thông tin và kinh tế số gắn liền với mô hình làm dự án nhóm (Project-based Learning) tại Đại học FPT.",
            "criteria": "Nêu bật sự giao thoa giữa tư duy sản phẩm phần mềm, bảo mật hệ thống và phân tích dữ liệu kinh doanh số.",
            "caption": (
                "KỸ THUẬT PHẦN MỀM, AN TOÀN THÔNG TIN HAY QUẢN TRỊ KINH DOANH SỐ: ĐÂU LÀ LỰA CHỌN CHO 2K9?\n\n"
                "Tại Trường Đại học FPT, sinh viên các nhóm ngành Công nghệ thông tin và Kinh tế số thường xuyên phối hợp trong "
                "cùng một không gian làm việc dự án để hoàn thiện sản phẩm thực tế:\n\n"
                "- Kỹ thuật phần mềm & An toàn thông tin: Phát triển ứng dụng web/di động, kiến trúc đám mây và bảo vệ hệ thống dữ liệu.\n"
                "- Quản trị kinh doanh số & Truyền thông đa phương tiện: Nghiên cứu người dùng, thiết kế UI/UX, vận hành thương mại điện tử và chiến dịch truyền thông số.\n\n"
                "Đăng ký tư vấn chọn chuyên ngành phù hợp với sở trường tại: https://tuyensinh.fpt.edu.vn"
            ),
            "hashtags": ["#KyThuatPhanMem", "#QuanTriKinhDoanhSo", "#DaiHocFPT", "#TuyenSinh2027"],
            "metrics": {"reactions": 1620, "comments": 198, "shares": 145, "impressions": 43800, "reach": 33100, "clicks": 2140, "saves": 510},
        },
        {
            "idx": 6_0,
            "week": 2,
            "work_item_id": wi_id(51),
            "deliverable_id": DELIV_POST_ID,
            "type": "POST",
            "name": "[Tuần 2 - Tiện ích Campus] Khám phá thư viện xanh, sân Vovinam, ký túc xá & 40 CLB sinh viên FPTU",
            "assignee_key": "CREATOR_2",
            "status": "FINISHED",
            "due": dt(-4, 9),
            "visual_key": "week2_campus_utilities",
            "platforms": ["FACEBOOK", "INSTAGRAM", "THREADS"],
            "post_status": "PUBLISHED",
            "description": "Bài viết giới thiệu toàn diện hệ sinh thái tiện ích học tập và đời sống sinh viên tại Đại học FPT trước thềm chuỗi Workshop dành cho học sinh THPT.",
            "criteria": "Hình ảnh thực tế thư viện kính, đồng phục Vovinam xanh, sinh hoạt CLB ven hồ và thông báo mở cổng đăng ký tham dự Workshop THPT.",
            "caption": (
                "BÊN TRONG KHUÔN VIÊN ĐẠI HỌC FPT: HỆ SINH THÁI TIỆN ÍCH TOÀN DIỆN CHO TÂN SINH VIÊN\n\n"
                "Trước khi bước vào chuỗi Workshop phổ biến tiện ích học đường dành cho các bạn học sinh THPT vào tuần tới, "
                "hãy cùng điểm qua những không gian gắn bó mỗi ngày với sinh viên Đại học FPT:\n\n"
                "- Thư viện hiện đại nhiều tầng ngập tràn ánh sáng tự nhiên với hàng chục nghìn đầu sách chuyên ngành quốc tế.\n"
                "- Sân tập Vovinam ngoài trời, khu liên hợp thể thao, ký túc xá tiện nghi ngay trong khuôn viên trường.\n"
                "- Hơn 40 câu lạc bộ học thuật, lập trình, khởi nghiệp, âm nhạc dân tộc và nghệ thuật biểu diễn sôi nổi suốt bốn mùa.\n\n"
                "Các bạn học sinh lớp 12 muốn trực tiếp trải nghiệm những tiện ích này? Đăng ký ngay vé tham dự Chuỗi Workshop THPT 2027 tại: https://tuyensinh.fpt.edu.vn"
            ),
            "hashtags": ["#TienIchFPTU", "#VovinamFPTU", "#DoiSongSinhVien", "#WorkshopTHPT2027", "#DaiHocFPT"],
            "metrics": {"reactions": 2890, "comments": 376, "shares": 310, "impressions": 71200, "reach": 55600, "clicks": 3490, "saves": 780},
        },
        {
            "idx": 7,
            "week": 2,
            "work_item_id": wi_id(7),
            "deliverable_id": DELIV_VIDEO_ID,
            "type": "SHORT_VIDEO",
            "name": "[Tuần 2 - Reels/TikTok #2] Một ngày trải nghiệm phòng Lab bán dẫn, giờ Vovinam và CLB tại FPTU",
            "assignee_key": "CREATOR_2",
            "status": "FINISHED",
            "due": dt(-3, 19),
            "visual_key": "week2_campus_utilities",
            "platforms": ["TIKTOK", "INSTAGRAM"],
            "post_status": "PUBLISHED",
            "description": "Vlog ngắn theo chân một sinh viên năm hai từ ca thực hành sáng tại Lab Vi mạch đến giờ rèn luyện Vovinam chiều và buổi tập nhạc cùng CLB bên hồ.",
            "criteria": "Nhịp điệu trẻ trung, chân thực, lồng ghép lời mời học sinh THPT đến tham dự buổi Workshop tuần 3.",
            "caption": (
                "Theo chân sinh viên FPTU từ phòng Lab Vi mạch buổi sáng đến sân tập Vovinam và buổi acoustic bên hồ lúc hoàng hôn. "
                "Hẹn gặp các bạn học sinh lớp 12 tại chuỗi Workshop trải nghiệm tuần này nhé!"
            ),
            "hashtags": ["#MotNgayLamSinhVienFPTU", "#Vovinam", "#WorkshopTHPT2027", "#FPTUniversity"],
            "metrics": {"reactions": 4120, "comments": 489, "shares": 640, "impressions": 112000, "reach": 88400, "clicks": 3920, "saves": 970},
        },
        {
            "idx": 8,
            "week": 2,
            "work_item_id": wi_id(8),
            "deliverable_id": DELIV_EMAIL_ID,
            "type": "EMAIL_NEWSLETTER",
            "name": "[Tuần 2 - Bản tin Email] Cẩm nang ngành học 2027 & Vé mời học sinh lớp 12 dự chuỗi Workshop THPT",
            "assignee_key": "CREATOR_3",
            "status": "FINISHED",
            "due": dt(-2, 15),
            "visual_key": "week3_thpt_workshop",
            "description": "Thiết kế và gửi bản tin Email chứa cẩm nang chọn ngành năm 2027 cùng mã QR check-in chuỗi Workshop phổ biến tiện ích học đường tới danh sách học sinh THPT đã đăng ký.",
            "criteria": "Gửi tới tập người nhận đã xác nhận đồng ý (consent), tỷ lệ vào hộp thư chính cao và có liên kết xác nhận tham dự.",
        },
        {
            "idx": 9,
            "week": 2,
            "work_item_id": None,  # Công việc phát sinh ngoài gói (Out-of-Scope SURVEY)
            "task_id_override": SURVEY_TASK_ID,
            "deliverable_id": None,
            "type": "SURVEY",
            "name": "[Tuần 2 - Khảo sát THPT] Khảo sát nhu cầu tìm hiểu ngành học & tiện ích ĐH FPT của học sinh lớp 12",
            "assignee_key": "CREATOR_3",
            "status": "FINISHED",
            "due": dt(-2, 18),
            "visual_key": "unsplash_2",
            "description": "Bảng khảo sát trực tuyến thu thập nguyện vọng ngành học, mức độ quan tâm về học bổng, ký túc xá và câu hỏi học sinh lớp 12 muốn giải đáp tại buổi Workshop Tuần 3.",
            "criteria": "Biểu mẫu gồm 5 câu hỏi rõ ràng, tổng hợp thống kê để đội ngũ giảng viên chuẩn bị nội dung sát nhu cầu thực tế.",
        },

        # ---------------- TUẦN 3: CHUỖI WORKSHOP THPT & OPEN DAY (TUẦN ĐANG CHẠY & DEMO SÂN KHẤU!) ----------------
        {
            "idx": 10,
            "week": 3,
            "work_item_id": LIVE_WORK_ITEM_ID,
            "task_id_override": TASK_1_ID,  # TASK TRỌNG TÂM TRÌNH DIỄN TRỰC TIẾP B4 -> B13
            "deliverable_id": DELIV_POST_ID,
            "type": "POST",
            "name": "[Tuần 3 - Bài trọng điểm] Điểm nhấn Chuỗi Workshop THPT & Mở đăng ký Học bổng Vi mạch, AI đợt 1 năm 2027",
            "assignee_key": "CREATOR",
            "status": "IN_PROGRESS",
            "due": dt(2, 9),
            "visual_key": "week3_thpt_workshop",
            "platforms": ["FACEBOOK", "INSTAGRAM", "TIKTOK", "THREADS"],
            "post_status": "DRAFT",
            "description": (
                "Bài đăng đa nền tảng trọng điểm của Tuần 3: cập nhật hoạt động trải nghiệm tiện ích học đường tại chuỗi Workshop THPT "
                "và thông báo mở cổng đăng ký xét Học bổng Nguyễn Văn Đạo năm 2027 cho nhóm ngành Thiết kế Vi mạch bán dẫn & AI."
            ),
            "criteria": (
                "Nêu rõ trải nghiệm phòng Lab bán dẫn & tiện ích tại 5 cơ sở, 3 mức Học bổng Nguyễn Văn Đạo (50%, 70%, 100% học phí), "
                "học kỳ thực tập doanh nghiệp OJT từ học kỳ 6 và đường dẫn https://tuyensinh.fpt.edu.vn."
            ),
            "caption": "",  # Để trống phần Caption ở trạng thái DRAFT nhằm demo trực tiếp AI tạo Caption + Quick Fill + Duyệt v1/v2 trên sân khấu!
            "hashtags": ["#DaiHocFPT", "#FPTUniversity", "#TuyenSinhFPTU2027", "#WorkshopTHPT2027", "#HocBongNguyenVanDao", "#ViMachBanDan"],
        },
        {
            "idx": 11,
            "week": 3,
            "work_item_id": wi_id(11),
            "deliverable_id": DELIV_WORKSHOP_ID,
            "type": "WORKSHOP",
            "name": "[Tuần 3 - Workshop #1] Workshop phổ biến tiện ích học đường & trải nghiệm VR, Robotics cho THPT khu vực miền Trung",
            "assignee_key": "CREATOR_2",
            "status": "FINISHED",
            "due": dt(-1, 16),
            "visual_key": "week3_thpt_workshop",
            "description": "Buổi Workshop đầu tiên đón 420 học sinh lớp 12 các trường THPT tại Đà Nẵng và Quảng Nam trực tiếp trải nghiệm kính VR tham quan 5 cơ sở, điều khiển cánh tay robot và tìm hiểu đời sống nội trú.",
            "criteria": "Hoàn thành toàn bộ 5 hạng mục chương trình, diễn giả, hậu cần, danh sách check-in và báo cáo tổng kết sau buổi.",
        },
        {
            "idx": 12,
            "week": 3,
            "work_item_id": wi_id(12),
            "deliverable_id": DELIV_WORKSHOP_ID,
            "type": "WORKSHOP",
            "name": "[Tuần 3 - Workshop #2] Workshop định hướng ngành Bán dẫn, AI & phổ biến tiện ích OJT cho cụm THPT Hà Nội - TP.HCM",
            "assignee_key": "CREATOR_2",
            "status": "IN_PROGRESS",
            "due": dt(2, 15),
            "visual_key": "week3_thpt_workshop",
            "description": "Buổi Workshop thứ hai kết nối trực tiếp học sinh lớp 12 tại Hà Nội và TP.HCM với giảng viên bộ môn Vi mạch bán dẫn, giới thiệu chi tiết thư viện, phòng Lab, chế độ học bổng và kỳ thực tập OJT.",
            "criteria": "Chốt danh sách diễn giả, khu vực bàn trải nghiệm thiết bị và danh sách 650 học sinh THPT đã đăng ký tham dự.",
        },
        {
            "idx": 13,
            "week": 3,
            "work_item_id": wi_id(13),
            "deliverable_id": DELIV_KOL_ID,
            "type": "KOL_BOOKING",
            "name": "[Tuần 3 - KOL #1] Phối hợp Creator công nghệ Duy Luân & Schannel giao lưu cùng học sinh tại Workshop THPT",
            "assignee_key": "CREATOR_2",
            "status": "IN_REVIEW",
            "due": dt(1, 17),
            "visual_key": "week3_openday_kol",
            "description": "Điều phối lịch xuất hiện và duyệt kịch bản chia sẻ thực tế của khách mời công nghệ về xu hướng nghề nghiệp kỹ sư AI, bán dẫn dành cho thế hệ 2k9 tại buổi Workshop và Open Day.",
            "criteria": "Bản dự thảo nội dung chia sẻ của KOL bám sát định hướng giáo dục, không dùng thuật ngữ quá hàn lâm với học sinh lớp 12.",
        },
        {
            "idx": 14,
            "week": 3,
            "work_item_id": wi_id(14),
            "deliverable_id": DELIV_EVENT_ID,
            "type": "EVENT_PLAN",
            "name": "[Tuần 3 - Sự kiện lớn] Ngày hội FPTU Open Day 2027: Một ngày làm sinh viên Đại học FPT",
            "assignee_key": "CREATOR_2",
            "status": "IN_PROGRESS",
            "due": dt(3, 16),
            "visual_key": "week3_openday_kol",
            "description": "Sự kiện trọng điểm cuối Tuần 3 đón học sinh THPT và phụ huynh tham quan trực tiếp khuôn viên trường, dự lớp học thử, xem biểu diễn Vovinam và tư vấn hồ sơ Học bổng Nguyễn Văn Đạo 2027.",
            "criteria": "Hoàn tất kịch bản sân khấu chính, sơ đồ 12 gian hàng trải nghiệm ngành học và phương án xe đưa đón các trường THPT.",
        },
        {
            "idx": 15,
            "week": 3,
            "work_item_id": wi_id(15),
            "deliverable_id": DELIV_KOL_ID,
            "type": "KOL_BOOKING",
            "name": "[Tuần 3 - KOL #2] Đại sứ Sinh viên khóa K19 kể chuyện kỳ thực tập OJT tại FPT Software trong Open Day",
            "assignee_key": "CREATOR",
            "status": "IN_PROGRESS",
            "due": dt(3, 18),
            "visual_key": "week4_ojt_press",
            "description": "Phối hợp cùng sinh viên tiêu biểu vừa hoàn thành học kỳ doanh nghiệp OJT chia sẻ chân thực về môi trường làm việc dự án quốc tế và kỹ năng ngoại ngữ tích lũy tại trường.",
            "criteria": "Chuẩn bị bộ câu hỏi giao lưu trên sân khấu Open Day và bài chia sẻ ảnh hậu trường trên Threads, Instagram.",
        },
        {
            "idx": 16,
            "week": 3,
            "work_item_id": wi_id(16),
            "deliverable_id": DELIV_VIDEO_ID,
            "type": "SHORT_VIDEO",
            "name": "[Tuần 3 - Reels/TikTok #3] Video Recap không khí học sinh THPT hào hứng thử nghiệm VR & Robotics tại Workshop",
            "assignee_key": "CREATOR_2",
            "status": "IN_PROGRESS",
            "due": dt(4, 20),
            "visual_key": "week3_openday_kol",
            "description": "Dựng video ngắn tổng hợp những khoảnh khắc ấn tượng và phỏng vấn nhanh cảm nhận của các bạn học sinh lớp 12 khi lần đầu bước vào phòng Lab và thư viện Đại học FPT.",
            "criteria": "Thời lượng 60 giây, âm thanh phỏng vấn hiện trường rõ nét và gắn lời nhắc hạn nộp hồ sơ đợt 1.",
        },

        # ---------------- TUẦN 4: BÁO CHÍ CHÍNH THỐNG & ĐA NỀN TẢNG CHỐT ĐỢT HỒ SƠ ----------------
        {
            "idx": 17,
            "week": 4,
            "work_item_id": wi_id(17),
            "deliverable_id": DELIV_PRESS_ID,
            "type": "PRESS_RECOMMENDATION",
            "name": "[Tuần 4 - Báo chí #1] Tuyến bài VnExpress Giáo dục: Đại học FPT đưa phòng Lab bán dẫn và tiện ích số đến gần học sinh THPT",
            "assignee_key": "CREATOR_3",
            "status": "IN_REVIEW",
            "due": dt(6, 9),
            "visual_key": "week4_ojt_press",
            "description": "Thông cáo và bài viết chuyên sâu gửi VnExpress Giáo dục tổng kết chuỗi Workshop trải nghiệm tiện ích học đường cho hơn 2.000 học sinh lớp 12 cùng định hướng đào tạo nhân lực công nghệ 2027.",
            "criteria": "Văn phong báo chí chính luận, có số liệu học sinh tham dự thực tế và phát ngôn chính thức từ đại diện Ban Tuyển sinh ĐH FPT.",
        },
        {
            "idx": 18,
            "week": 4,
            "work_item_id": wi_id(18),
            "deliverable_id": DELIV_PRESS_ID,
            "type": "PRESS_RECOMMENDATION",
            "name": "[Tuần 4 - Báo chí #2] Bài phân tích trên Báo Thanh Niên & Dân Trí: Giá trị thực tiễn từ học kỳ doanh nghiệp OJT năm thứ ba",
            "assignee_key": "CREATOR_3",
            "status": "TODO",
            "due": dt(9, 9),
            "visual_key": "week4_ojt_press",
            "description": "Bài báo phân tích mô hình hợp tác giữa Trường Đại học FPT và mạng lưới doanh nghiệp công nghệ giúp sinh viên tích lũy kinh nghiệm thực chiến trước khi tốt nghiệp.",
            "criteria": "Đính kèm bộ ảnh sinh viên thực tập tại trung tâm phần mềm và thông tin xét tuyển khóa K23 năm 2027.",
        },
        {
            "idx": 19,
            "week": 4,
            "work_item_id": wi_id(19),
            "deliverable_id": DELIV_POST_ID,
            "type": "POST",
            "name": "[Tuần 4 - Đa nền tảng #1] Câu chuyện học sinh lớp 12 tìm thấy ngành học mơ ước sau buổi Workshop trải nghiệm FPTU",
            "assignee_key": "CREATOR",
            "status": "FINISHED",
            "due": dt(7, 9),
            "visual_key": "week3_openday_kol",
            "platforms": ["FACEBOOK", "INSTAGRAM", "TIKTOK", "THREADS"],
            "post_status": "SCHEDULED",
            "scheduled_offset_days": 6,
            "description": "Bài đăng đa nền tảng đã được duyệt sẵn và lên lịch xuất bản cho đầu Tuần 4: chia sẻ góc nhìn chân thực của học sinh THPT và phụ huynh sau khi tham quan phòng Lab, thư viện và ký túc xá.",
            "criteria": "Trích dẫn chia sẻ thực tế của học sinh tham dự Open Day kèm bộ ảnh sự kiện rõ nét trên cả 4 nền tảng.",
            "caption": (
                "TỪ BUỔI WORKSHOP TRẢI NGHIỆM ĐẾN QUYẾT ĐỊNH CHỌN NGÀNH CỦA CÁC BẠN HỌC SINH LỚP 12\n\n"
                "Sau chuỗi Workshop phổ biến tiện ích học đường và Ngày hội FPTU Open Day 2027, hơn 2.000 học sinh THPT cùng phụ huynh "
                "đã trực tiếp cầm trên tay bo mạch thực hành, bước qua không gian thư viện xanh và lắng nghe đàn anh khóa K19 kể chuyện đi thực tập OJT.\n\n"
                "Những trải nghiệm mắt thấy tai nghe giúp các bạn 2k9 tự tin xác định lộ trình đại học phù hợp nhất cho riêng mình.\n\n"
                "Cổng nhận hồ sơ xét tuyển và đăng ký Học bổng Nguyễn Văn Đạo đợt 1 năm 2027 vẫn đang mở tại: https://tuyensinh.fpt.edu.vn"
            ),
            "hashtags": ["#FPTUOpenDay2027", "#WorkshopTHPT2027", "#DaiHocFPT", "#TuyenSinhFPTU2027", "#KhoaK23"],
        },
        {
            "idx": 20,
            "week": 4,
            "work_item_id": wi_id(20),
            "deliverable_id": DELIV_POST_ID,
            "type": "POST",
            "name": "[Tuần 4 - Đa nền tảng #2] Nhắc hạn hoàn tất hồ sơ xét tuyển & Học bổng Nguyễn Văn Đạo đợt 1 năm 2027",
            "assignee_key": "CREATOR",
            "status": "FINISHED",
            "due": dt(12, 9),
            "visual_key": "week4_ojt_press",
            "platforms": ["FACEBOOK", "INSTAGRAM", "TIKTOK", "THREADS"],
            "post_status": "SCHEDULED",
            "scheduled_offset_days": 11,
            "description": "Bài tổng kết chặng cuối chiến dịch 4 tuần trên Facebook, Instagram, TikTok và Threads: tóm tắt checklist giấy tờ cần chuẩn bị và nhắc mốc đóng cổng nhận hồ sơ đợt 1 khóa K23.",
            "criteria": "Checklist 4 bước nộp hồ sơ trực tuyến ngắn gọn, dễ lưu lại trên điện thoại cho học sinh và phụ huynh.",
            "caption": (
                "NHẮC HẠN HOÀN TẤT HỒ SƠ XÉT TUYỂN & ĐĂNG KÝ HỌC BỔNG NGUYỄN VĂN ĐẠO ĐỢT 1 NĂM 2027\n\n"
                "Chỉ còn ít ngày nữa để các sĩ tử 2k9 hoàn tất hồ sơ xét tuyển sớm và đăng ký xét cấp Học bổng Nguyễn Văn Đạo "
                "(mức 50%, 70%, 100% học phí toàn khóa) vào Trường Đại học FPT.\n\n"
                "4 bước kiểm tra nhanh hồ sơ trực tuyến:\n"
                "1. Chọn chuyên ngành và cơ sở dự tuyển (Hà Nội, Đà Nẵng, Quy Nhơn, TP.HCM hoặc Cần Thơ).\n"
                "2. Tải ảnh chụp học bạ THPT và các giấy chứng nhận thành tích (nếu đăng ký xét học bổng).\n"
                "3. Kiểm tra email xác nhận mã hồ sơ từ Ban Tuyển sinh Đại học FPT.\n"
                "4. Liên hệ hotline hoặc hộp thư Fanpage chính thức nếu cần hỗ trợ bổ sung minh chứng.\n\n"
                "Hoàn tất hồ sơ ngay hôm nay tại: https://tuyensinh.fpt.edu.vn"
            ),
            "hashtags": ["#TuyenSinhFPTU2027", "#HocBongNguyenVanDao", "#DaiHocFPT", "#FPTUniversity", "#2k9"],
        },
    ]


# ==============================================================================
# 4. THỰC THI CẬP NHẬT POSTGRESQL (100% SCHEMA-EXACT & PARAMETERIZED)
# ==============================================================================
def build_postgres_bundle(now: datetime) -> dict[str, Any]:
    start_date = (now - timedelta(days=14)).strftime("%Y-%m-%d")
    end_date = (now + timedelta(days=14)).strftime("%Y-%m-%d")
    now_iso = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    flagship_deliverables = build_flagship_fptu_deliverables()
    flagship_offering = {"deliverables": flagship_deliverables}
    final_terms = {
        "sourcePackageId": PACKAGE_ID,
        "name": "Gói Tuyển sinh Đại học FPT 2027: Chiến dịch Đa kênh & Chuỗi Workshop 4 Tuần",
        "durationWeeks": 4,
        "budgetAmount": 185000000,
        "scopeDescription": (
            "Triển khai trọn gói chiến dịch truyền thông tuyển sinh khóa K23 (năm 2027) kéo dài 4 tuần cho Trường Đại học FPT: "
            "từ chuỗi bài Coming Soon, giới thiệu chuyên ngành mũi nhọn & tiện ích Campus, tổ chức chuỗi Workshop trải nghiệm "
            "tại các trường THPT, ngày hội Open Day đến tuyến bài báo chí chính thống và đa nền tảng."
        ),
        "quantityBasis": "TOTAL",
        "offeringDetails": flagship_offering,
    }
    allocations = [{"deliverableId": d["id"], "quantity": d["quantity"]} for d in flagship_deliverables]

    specs = build_4week_plan_specs(now)
    work_items = [
        {
            "id": s["work_item_id"],
            "deliverableId": s["deliverable_id"],
            "name": s["name"],
            "type": s["type"],
            "dueDate": s["due"].strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        for s in specs
        if s.get("work_item_id") is not None
    ]

    # Milestones tuân thủ tuyệt đối CampaignPlanValidator.timeline() (yêu cầu "name" <=255 ký tự & "date" YYYY-MM-DD trong khoảng startDate..endDate)
    timeline = {
        "startDate": start_date,
        "endDate": end_date,
        "milestones": [
            {
                "name": "Tuần 1: Khởi động Coming Soon & Công bố Học bổng Nguyễn Văn Đạo 2027",
                "date": (now - timedelta(days=9)).strftime("%Y-%m-%d"),
            },
            {
                "name": "Tuần 2: Giới thiệu Ngành học Vi mạch, AI, Kinh tế số & Tiện ích 5 Cơ sở",
                "date": (now - timedelta(days=3)).strftime("%Y-%m-%d"),
            },
            {
                "name": "Tuần 3: Tổ chức Chuỗi Workshop Phổ biến Tiện ích THPT & Ngày hội Open Day",
                "date": (now + timedelta(days=3)).strftime("%Y-%m-%d"),
            },
            {
                "name": "Tuần 4: Lan tỏa Báo chí Chính thống & Đa nền tảng Chốt Hồ sơ Đợt 1",
                "date": (now + timedelta(days=12)).strftime("%Y-%m-%d"),
            },
        ],
        "brief": build_campaign_brief_json(now_iso),
    }

    strategy_detail = (
        "Chiến dịch 4 tuần dẫn dắt hành trình nhận thức của học sinh lớp 12 và phụ huynh theo 4 chặng liên kết chặt chẽ: "
        "(1) Khởi động nhận diện mùa tuyển sinh 2027 và Học bổng Nguyễn Văn Đạo; "
        "(2) Giải mã chiều sâu đào tạo ngành Thiết kế Vi mạch bán dẫn, AI, Kỹ thuật phần mềm, Kinh tế số cùng tiện ích Campus; "
        "(3) Đưa trải nghiệm thực tế đến học sinh THPT qua chuỗi Workshop VR/Robotics và Ngày hội Open Day; "
        "(4) Củng cố uy tín học thuật và đầu ra thực tập doanh nghiệp OJT trên báo chí chính thống cùng đa nền tảng mạng xã hội."
    )
    brand_guideline = (
        "Sử dụng tông màu chủ đạo Cam FPT (#F05A28 / #EA580C) trên nền Trắng sáng hiện đại. "
        "Văn phong rõ ràng, tôn trọng người đọc, dùng số liệu xác thực về 5 cơ sở đào tạo, 3 mức học bổng (50%, 70%, 100%) "
        "và học kỳ thực tập OJT từ học kỳ 6. Không sử dụng ngôn từ giật gân hoặc so sánh thiếu chuẩn mực."
    )

    collaborators = [
        (
            COLLAB_VNEXPRESS_ID,
            "VnExpress - Chuyên mục Giáo dục & Số hóa",
            "NEWSPAPER",
            {"email": "giaoduc@vnexpress.net", "phone": "02473008899", "website": "https://vnexpress.net/giao-duc", "contactPerson": "Ban Biên tập Giáo dục"},
            "Đối tác đăng tải bài phân tích chuyên sâu về chuỗi Workshop trải nghiệm phòng Lab bán dẫn và AI cho học sinh THPT.",
            "LIVE",
        ),
        (
            COLLAB_THANHNIEN_ID,
            "Báo Thanh Niên - Ban Giáo dục Tuyển sinh",
            "NEWSPAPER",
            {"email": "bangiaoduc@thanhnien.vn", "phone": "02839309999", "website": "https://thanhnien.vn/giao-duc.htm", "contactPerson": "Tổ Tư vấn Mùa thi"},
            "Phối hợp tuyến bài cẩm nang chọn ngành công nghệ và giá trị thực tiễn của học kỳ doanh nghiệp OJT năm 2027.",
            "CONFIRMED",
        ),
        (
            COLLAB_DANTRI_ID,
            "Báo Điện tử Dân Trí - Chuyên mục Giáo dục",
            "NEWSPAPER",
            {"email": "giaoduc@dantri.com.vn", "phone": "02437366491", "website": "https://dantri.com.vn/giao-duc.htm", "contactPerson": "Phòng Nội dung Giáo dục"},
            "Đưa tin tổng kết Ngày hội FPTU Open Day 2027 và chính sách Học bổng Nguyễn Văn Đạo dành cho học sinh lớp 12.",
            "CONFIRMED",
        ),
        (
            COLLAB_VTV1_ID,
            "Đài Truyền hình VTV1 - Bản tin Công nghệ & Giáo dục",
            "TV",
            {"email": "bantincongnghe@vtv.vn", "phone": "02438355931", "website": "https://vtv.vn/cong-nghe.htm", "contactPerson": "Ê-kíp Phóng sự Khoa giáo"},
            "Ghi hình phóng sự ngắn về mô hình phòng Lab Thiết kế Vi mạch bán dẫn phục vụ đào tạo đại học.",
            "CONFIRMED",
        ),
        (
            COLLAB_SCHANNEL_ID,
            "Creator Công nghệ Duy Luân & Tổ hợp Schannel",
            "OTHER",
            {"email": "booking@schannel.vn", "phone": "0909123456", "website": "https://www.tiktok.com/@schannel.vn", "contactPerson": "Quản lý Lịch trình KOL"},
            "Khách mời giao lưu trực tiếp cùng học sinh THPT tại buổi Workshop Tuần 3 và Ngày hội FPTU Open Day 2027.",
            "LIVE",
        ),
        (
            COLLAB_CAMPUS_LED_ID,
            "Hệ thống Bảng tin & Màn hình LED Cụm Trường THPT Đối tác",
            "BANNER",
            {"email": "media.school@se08digital.vn", "phone": "02363888999", "website": "https://tuyensinh.fpt.edu.vn", "contactPerson": "Bộ phận Truyền thông Học đường"},
            "Hiển thị poster thông báo lịch tổ chức Workshop trải nghiệm tiện ích Đại học FPT tại 18 trường THPT trọng điểm.",
            "LIVE",
        ),
    ]

    hashtags = [
        ("#DaiHocFPT", "daihocfpt", "BRAND", True, None),
        ("#FPTUniversity", "fptuniversity", "BRAND", True, None),
        ("#TraiNghiemDeThanhCong", "trainghiemdethanhcong", "BRAND", False, None),
        ("#TuyenSinhFPTU2027", "tuyensinhfptu2027", "CAMPAIGN", True, CAMPAIGN_ID),
        ("#HocBongNguyenVanDao", "hocbongnguyenvandao", "CAMPAIGN", False, CAMPAIGN_ID),
        ("#ViMachBanDan", "vimachbandan", "CAMPAIGN", False, CAMPAIGN_ID),
        ("#HocKyDoanhNghiepOJT", "hockydoanhnghiepojt", "CAMPAIGN", False, CAMPAIGN_ID),
        ("#KhoaK23", "khoak23", "CAMPAIGN", False, CAMPAIGN_ID),
        ("#WorkshopTHPT2027", "workshopthpt2027", "EVENT_SPECIFIC", False, CAMPAIGN_ID),
        ("#FPTUOpenDay2027", "fptuopenday2027", "EVENT_SPECIFIC", False, CAMPAIGN_ID),
        ("#2k9ChonNganh", "2k9chonnganh", "TRENDING", False, None),
        ("#SinhVienCongNghe", "sinhviencongnghe", "TRENDING", False, None),
    ]

    return {
        "start_date": start_date,
        "end_date": end_date,
        "flagship_deliverables": flagship_deliverables,
        "flagship_offering": flagship_offering,
        "final_terms": final_terms,
        "allocations": allocations,
        "work_items": work_items,
        "timeline": timeline,
        "strategy_detail": strategy_detail,
        "brand_guideline": brand_guideline,
        "catalog_packages": build_multi_industry_catalog(),
        "collaborators": collaborators,
        "hashtags": hashtags,
    }


def build_sql_preview_text(bundle: dict[str, Any]) -> str:
    """Xuất bản SQL preview rõ ràng phục vụ lưu trữ tài liệu báo cáo."""
    return (
        "-- ============================================================================\n"
        "-- BRANDHUB LIVE DEMO POSTGRESQL PREVIEW (FPT UNIVERSITY ADMISSIONS 2027)\n"
        "-- Sử dụng `python prepare_demo_data_template.py --apply` để thực thi an toàn\n"
        "-- bằng truy vấn tham số hóa (parameterized queries) vào PostgreSQL & MongoDB.\n"
        "-- ============================================================================\n"
        f"-- Agency       : {AGENCY_ID} (SE08 Digital Agency)\n"
        f"-- Workspace    : {WORKSPACE_ID} (Đại học FPT Tuyển sinh 2027 x SE08 Digital)\n"
        f"-- MediaPackage : {PACKAGE_ID} (4 tuần - 7 hạng mục dịch vụ - 185.000.000 VND)\n"
        f"-- Campaign     : {CAMPAIGN_ID} ({bundle['start_date']} -> {bundle['end_date']}, {len(bundle['work_items'])} hạng mục gói)\n"
        f"-- Catalog Pkgs : {1 + len(bundle['catalog_packages'])} gói đa lĩnh vực\n"
    )


def apply_postgres(pg_uri: str, bundle: dict[str, Any]) -> dict[str, str]:
    try:
        import psycopg2
    except ImportError as exc:
        raise RuntimeError("Cần cài đặt psycopg2-binary: pip install psycopg2-binary") from exc

    resolved_ids = dict(PG_USER_IDS)
    conn = psycopg2.connect(pg_uri)
    try:
        with conn:
            with conn.cursor() as cur:
                # 1. Cập nhật thông tin chuẩn cho 7 tài khoản (5 thành viên SE_08 + Client ĐH FPT + Admin)
                for key, acc in DEMO_ACCOUNTS.items():
                    cur.execute(
                        """
                        UPDATE users
                        SET full_name = %s,
                            professional_title = %s,
                            bio = %s,
                            location = 'Đà Nẵng & Hà Nội, Việt Nam',
                            working_language = 'vi,en',
                            status = 'ACTIVE',
                            is_active = TRUE,
                            two_factor_enabled = FALSE,
                            require_password_reset = FALSE,
                            last_login_at = NOW() - INTERVAL '45 minutes',
                            updated_at = NOW()
                        WHERE email = %s
                        RETURNING id;
                        """,
                        (acc["full_name"], acc["title"], acc["bio"], acc["email"]),
                    )
                    row = cur.fetchone()
                    if row and row[0]:
                        resolved_ids[key] = str(row[0])

                owner_id = resolved_ids["OWNER"]
                manager_id = resolved_ids["MANAGER"]
                creator_id = resolved_ids["CREATOR"]
                creator2_id = resolved_ids["CREATOR_2"]
                creator3_id = resolved_ids["CREATOR_3"]
                client_id = resolved_ids["CLIENT"]
                admin_id = resolved_ids["ADMIN"]

                demo_user_ids_clean = [owner_id, manager_id, creator_id, creator2_id, creator3_id, client_id, admin_id]
                demo_ws_ids_clean = [
                    WORKSPACE_ID,
                    "d7e00000-0000-4000-8000-000000000091",
                    "d7e00000-0000-4000-8000-000000000092",
                ]
                # Dọn dẹp triệt để dữ liệu phát sinh sau lần chạy thử demo trước (strikes, AI nháp, canvas Yjs, đơn VietQR treo)
                cur.execute(
                    """
                    UPDATE users
                    SET status = 'ACTIVE', is_active = TRUE, clean_period_ends_at = NULL, reactivate_at = NULL
                    WHERE id = ANY(%s::uuid[]);
                    DELETE FROM sanction_reviews WHERE user_id = ANY(%s::uuid[]);
                    UPDATE user_strikes SET converted_to_id = NULL WHERE user_id = ANY(%s::uuid[]);
                    DELETE FROM user_strikes WHERE user_id = ANY(%s::uuid[]);
                    DELETE FROM admin_account_operations WHERE user_id = ANY(%s::uuid[]);
                    DELETE FROM ai_caption_generations WHERE workspace_id = ANY(%s::uuid[]);
                    DELETE FROM ai_video_jobs WHERE workspace_id = ANY(%s::uuid[]);
                    DELETE FROM task_content_operations WHERE task_id IN (SELECT id FROM tasks WHERE workspace_id = ANY(%s::uuid[]));
                    DELETE FROM task_content_snapshots WHERE task_id IN (SELECT id FROM tasks WHERE workspace_id = ANY(%s::uuid[]));
                    DELETE FROM tasks WHERE workspace_id = ANY(%s::uuid[]);
                    """,
                    (
                        demo_user_ids_clean,
                        demo_user_ids_clean,
                        demo_user_ids_clean,
                        demo_user_ids_clean,
                        demo_user_ids_clean,
                        demo_ws_ids_clean,
                        demo_ws_ids_clean,
                        demo_ws_ids_clean,
                        demo_ws_ids_clean,
                        demo_ws_ids_clean,
                    ),
                )
                cur.execute(
                    """
                    SELECT id::text FROM billing_orders
                    WHERE agency_id = %s::uuid
                      AND status IN ('PENDING_PAYMENT', 'EXPIRED', 'CANCELLED', 'REVIEW_REQUIRED')
                      AND id NOT IN (SELECT order_id FROM agency_subscription_periods WHERE order_id IS NOT NULL)
                      AND id NOT IN (SELECT order_id FROM credit_grants WHERE order_id IS NOT NULL)
                      AND id NOT IN (SELECT order_id FROM storage_addon_subscriptions WHERE order_id IS NOT NULL);
                    """,
                    (AGENCY_ID,),
                )
                rehearsal_ords = [r[0] for r in cur.fetchall()]
                if rehearsal_ords:
                    cur.execute(
                        """
                        DELETE FROM subscription_operational_issues WHERE order_id = ANY(%s::uuid[]);
                        DELETE FROM subscription_provider_checks WHERE order_id = ANY(%s::uuid[]);
                        DELETE FROM billing_payment_events WHERE order_id = ANY(%s::uuid[]);
                        DELETE FROM billing_payments WHERE attempt_id IN (SELECT id FROM billing_payment_attempts WHERE order_id = ANY(%s::uuid[]));
                        DELETE FROM billing_payment_attempts WHERE order_id = ANY(%s::uuid[]);
                        DELETE FROM billing_order_fulfillments WHERE order_id = ANY(%s::uuid[]);
                        DELETE FROM billing_orders WHERE id = ANY(%s::uuid[]);
                        """,
                        (
                            rehearsal_ords,
                            rehearsal_ords,
                            rehearsal_ords,
                            rehearsal_ords,
                            rehearsal_ords,
                            rehearsal_ords,
                            rehearsal_ords,
                        ),
                    )
                cur.execute(
                    """
                    DELETE FROM credit_reservation_allocations
                    WHERE agency_id = %s::uuid
                      AND reservation_id NOT IN (SELECT reservation_id FROM credit_operations WHERE reservation_id IS NOT NULL);
                    DELETE FROM ai_credit_reservations
                    WHERE agency_id = %s::uuid
                      AND id NOT IN (SELECT reservation_id FROM credit_operations WHERE reservation_id IS NOT NULL);
                    """,
                    (AGENCY_ID, AGENCY_ID),
                )

                # 2. Dọn sạch các Agency/Workspace ngẫu nhiên do Faker sinh trước đó gắn với Owner để không bị rác dữ liệu
                cur.execute(
                    """
                    SELECT id::text FROM users
                    WHERE email LIKE 'user%%@demo.brandhub.test'
                      AND email NOT IN ('user177@demo.brandhub.test', 'user1@demo.brandhub.test',
                                        'user13@demo.brandhub.test', 'user14@demo.brandhub.test',
                                        'user15@demo.brandhub.test', 'user59@demo.brandhub.test')
                    ORDER BY email LIMIT 1;
                    """
                )
                fallback_row = cur.fetchone()
                if fallback_row:
                    other_owner = fallback_row[0]
                    cur.execute(
                        """
                        UPDATE agencies
                        SET owner_id = %s::uuid
                        WHERE owner_id = %s::uuid AND id <> %s::uuid;
                        """,
                        (other_owner, owner_id, AGENCY_ID),
                    )
                    cur.execute(
                        """
                        DELETE FROM agency_members
                        WHERE user_id = %s::uuid AND agency_id <> %s::uuid;
                        """,
                        (owner_id, AGENCY_ID),
                    )
                    cur.execute(
                        """
                        UPDATE workspaces
                        SET status = 'SOFT_DELETED', deleted_at = NOW()
                        WHERE agency_id = %s::uuid
                          AND id NOT IN (
                              %s::uuid,
                              'd7e00000-0000-4000-8000-000000000091'::uuid,
                              'd7e00000-0000-4000-8000-000000000092'::uuid
                          )
                          AND deleted_at IS NULL;
                        """,
                        (AGENCY_ID, WORKSPACE_ID),
                    )

                # 3. Chuẩn hóa SE08 Digital Agency & danh sách 5 thành viên đồ án SE_08
                cur.execute(
                    """
                    INSERT INTO agencies (
                        id, name, owner_id, description, category, company_size,
                        website, phone, location, brand_color, tagline, founded_year,
                        facebook_url, linkedin_url, status, created_at, updated_at
                    ) VALUES (
                        %s::uuid, 'SE08 Digital Agency', %s::uuid,
                        'Đơn vị tư vấn chiến lược và triển khai chiến dịch truyền thông đa nền tảng chuyên sâu cho lĩnh vực Giáo dục đại học, Công nghệ và Thương hiệu Việt.',
                        'MARKETING', 'SIZE_11_50',
                        'https://se08digital.vn', '02363999888',
                        'Khu đô thị Công nghệ FPT, Phường Hòa Hải, Quận Ngũ Hành Sơn, Đà Nẵng',
                        '#EA580C', 'Chiến lược dữ liệu thật - Sáng tạo gắn kết thực tiễn', 2024,
                        'https://facebook.com/se08digital', 'https://linkedin.com/company/se08digital',
                        'ACTIVE', NOW() - INTERVAL '180 days', NOW()
                    )
                    ON CONFLICT (id) DO UPDATE SET
                        name = EXCLUDED.name,
                        owner_id = EXCLUDED.owner_id,
                        description = EXCLUDED.description,
                        category = EXCLUDED.category,
                        company_size = EXCLUDED.company_size,
                        website = EXCLUDED.website,
                        phone = EXCLUDED.phone,
                        location = EXCLUDED.location,
                        brand_color = EXCLUDED.brand_color,
                        tagline = EXCLUDED.tagline,
                        status = 'ACTIVE',
                        deleted_at = NULL,
                        updated_at = NOW();
                    """,
                    (AGENCY_ID, owner_id),
                )

                cur.execute("DELETE FROM agency_members WHERE agency_id = %s::uuid;", (AGENCY_ID,))
                for uid, a_role in [
                    (owner_id, "OWNER"),
                    (manager_id, "MEMBER"),
                    (creator_id, "MEMBER"),
                    (creator2_id, "MEMBER"),
                    (creator3_id, "MEMBER"),
                ]:
                    cur.execute(
                        """
                        INSERT INTO agency_members (id, agency_id, user_id, role, joined_at)
                        VALUES (%s::uuid, %s::uuid, %s::uuid, %s::agency_member_role, NOW() - INTERVAL '90 days')
                        ON CONFLICT (agency_id, user_id) DO UPDATE SET role = EXCLUDED.role;
                        """,
                        (java_name_uuid_from_bytes(f"agency-member:{AGENCY_ID}:{uid}"), AGENCY_ID, uid, a_role),
                    )

                # 4. Hồ sơ Khách hàng (ClientProfile): Ban Tuyển sinh Đại học FPT
                social_links = json.dumps(
                    {
                        "facebook": "https://www.facebook.com/university.fpt.edu.vn",
                        "instagram": "https://www.instagram.com/fpt_university",
                        "tiktok": "https://www.tiktok.com/@fptuniversity",
                        "website": "https://tuyensinh.fpt.edu.vn",
                    },
                    ensure_ascii=False,
                )
                cur.execute(
                    """
                    INSERT INTO client_profiles (
                        id, user_id, display_name, company, industry,
                        logo_url, banner_url, phone, website, location,
                        description, social_links, note, contact_name, contact_email,
                        company_size, address, tagline, founded_year, budget_range,
                        created_at, updated_at
                    ) VALUES (
                        %s::uuid, %s::uuid,
                        'Ban Tuyển sinh Đại học FPT',
                        'Trường Đại học FPT (FPT University)',
                        'EDUCATION',
                        %s, %s,
                        '02473005588', 'https://tuyensinh.fpt.edu.vn',
                        'Hà Nội, Đà Nẵng, Quy Nhơn, TP.HCM, Cần Thơ',
                        'Đơn vị phụ trách công tác tư vấn hướng nghiệp, xét tuyển đại học chính quy và chương trình Học bổng Nguyễn Văn Đạo tại 5 cơ sở của Trường Đại học FPT trên toàn quốc.',
                        %s::jsonb,
                        'Ưu tiên kiểm duyệt kỹ độ chính xác về 3 mức học bổng (50%%, 70%%, 100%%), lộ trình thực tập doanh nghiệp OJT từ học kỳ 6 và lịch tổ chức Workshop THPT.',
                        'Ban Tuyển sinh Đại học FPT', 'tuyensinh@fpt.edu.vn',
                        'SIZE_500_PLUS',
                        'Khu Giáo dục và Đào tạo, Khu Công nghệ cao Hòa Lạc, Km29 Đại lộ Thăng Long, Hà Nội',
                        'Trải nghiệm để thành công', 2006, '150.000.000 - 250.000.000 VND / chiến dịch',
                        NOW() - INTERVAL '120 days', NOW()
                    )
                    ON CONFLICT (id) DO UPDATE SET
                        user_id = EXCLUDED.user_id,
                        display_name = EXCLUDED.display_name,
                        company = EXCLUDED.company,
                        industry = EXCLUDED.industry,
                        logo_url = EXCLUDED.logo_url,
                        banner_url = EXCLUDED.banner_url,
                        phone = EXCLUDED.phone,
                        website = EXCLUDED.website,
                        location = EXCLUDED.location,
                        description = EXCLUDED.description,
                        social_links = EXCLUDED.social_links,
                        note = EXCLUDED.note,
                        contact_name = EXCLUDED.contact_name,
                        contact_email = EXCLUDED.contact_email,
                        tagline = EXCLUDED.tagline,
                        updated_at = NOW();
                    """,
                    (
                        CLIENT_PROFILE_ID,
                        client_id,
                        FPTU_VISUALS["week1_coming_soon"]["url"],
                        FPTU_VISUALS["week3_openday_kol"]["url"],
                        social_links,
                    ),
                )

                # 5. Chuẩn hóa Workspace chính: Đại học FPT Tuyển sinh 2027 x SE08 Digital
                ws_settings = json.dumps(
                    {
                        "approvalMode": "TWO_TIER",
                        "defaultTimezone": "Asia/Ho_Chi_Minh",
                        "brandBannedWords": [
                            "cam kết 100% việc làm lương ngàn đô",
                            "tuyển thẳng không cần điều kiện",
                            "bằng cấp vô giá trị",
                            "học bổng ảo",
                        ],
                    },
                    ensure_ascii=False,
                )
                cur.execute(
                    """
                    INSERT INTO workspaces (
                        id, agency_id, name, created_by, timezone_config, settings,
                        industry, company_size, website, phone, location, description,
                        brand_color, logo_url, banner_url, tagline, founded_year,
                        facebook_url, instagram_url, status, created_at, updated_at
                    ) VALUES (
                        %s::uuid, %s::uuid,
                        'Đại học FPT Tuyển sinh 2027 x SE08 Digital',
                        %s::uuid, 'Asia/Ho_Chi_Minh', %s::jsonb,
                        'EDUCATION', 'SIZE_500_PLUS',
                        'https://tuyensinh.fpt.edu.vn', '02473005588',
                        '5 cơ sở: Hà Nội, Đà Nẵng, Quy Nhơn, TP.HCM, Cần Thơ',
                        'Không gian phối hợp chiến dịch Tuyển sinh khóa K23 (năm 2027) kéo dài 4 tuần giữa SE08 Digital Agency và Ban Tuyển sinh Trường Đại học FPT.',
                        '#F05A28', %s, %s,
                        'Tuyển sinh Đại học FPT 2027 - Khai phóng Tiềm năng Công nghệ', 2006,
                        'https://www.facebook.com/university.fpt.edu.vn',
                        'https://www.instagram.com/fpt_university',
                        'ACTIVE', NOW() - INTERVAL '60 days', NOW()
                    )
                    ON CONFLICT (id) DO UPDATE SET
                        agency_id = EXCLUDED.agency_id,
                        name = EXCLUDED.name,
                        created_by = EXCLUDED.created_by,
                        timezone_config = 'Asia/Ho_Chi_Minh',
                        settings = EXCLUDED.settings,
                        industry = 'EDUCATION',
                        company_size = 'SIZE_500_PLUS',
                        website = EXCLUDED.website,
                        phone = EXCLUDED.phone,
                        location = EXCLUDED.location,
                        description = EXCLUDED.description,
                        brand_color = '#F05A28',
                        logo_url = EXCLUDED.logo_url,
                        banner_url = EXCLUDED.banner_url,
                        tagline = EXCLUDED.tagline,
                        status = 'ACTIVE',
                        deleted_at = NULL,
                        updated_at = NOW();
                    """,
                    (
                        WORKSPACE_ID,
                        AGENCY_ID,
                        owner_id,
                        ws_settings,
                        FPTU_VISUALS["week1_coming_soon"]["url"],
                        FPTU_VISUALS["week3_openday_kol"]["url"],
                    ),
                )

                # Gắn đầy đủ thành viên vào Workspace (Manager Lộc + 3 Creator Phước, Tuấn, Ân + Client Ban Tuyển sinh ĐH FPT)
                # Lưu ý: Owner Lê Trí Trung truy cập quyền OWNER thông qua agency.owner_id (theo quy chuẩn LinkedDemoSeeder).
                cur.execute("DELETE FROM workspace_members WHERE workspace_id = %s::uuid;", (WORKSPACE_ID,))
                ws_member_rows = [
                    (manager_id, None, "MANAGER"),
                    (creator_id, None, "CREATOR"),
                    (creator2_id, None, "CREATOR"),
                    (creator3_id, None, "CREATOR"),
                    (client_id, CLIENT_PROFILE_ID, "CLIENT"),
                ]
                for uid, cp_id, w_role in ws_member_rows:
                    wm_id = java_name_uuid_from_bytes(f"ws-member:{WORKSPACE_ID}:{uid}")
                    cur.execute(
                        """
                        INSERT INTO workspace_members (
                            id, workspace_id, user_id, client_profile_id, role,
                            added_by, joined_at, is_active, created_at, updated_at
                        ) VALUES (
                            %s::uuid, %s::uuid, %s::uuid, %s::uuid, %s::workspace_member_role,
                            %s::uuid, NOW() - INTERVAL '45 days', TRUE, NOW() - INTERVAL '45 days', NOW()
                        );
                        """,
                        (wm_id, WORKSPACE_ID, uid, cp_id, w_role, owner_id),
                    )

                # 6. Danh mục 7 Gói truyền thông Đa lĩnh vực (1 gói ĐH FPT 2027 + 6 gói chuyên ngành)
                keep_pkg_ids = [PACKAGE_ID] + [p["id"] for p in bundle["catalog_packages"]]
                cur.execute(
                    """
                    DELETE FROM media_packages
                    WHERE agency_id = %s::uuid
                      AND id <> ALL(%s::uuid[])
                      AND id NOT IN (SELECT package_id FROM workspace_media_packages WHERE package_id IS NOT NULL);
                    """,
                    (AGENCY_ID, keep_pkg_ids),
                )

                all_packages_to_upsert = [
                    {
                        "id": PACKAGE_ID,
                        "name": bundle["final_terms"]["name"],
                        "duration_weeks": 4,
                        "budget_amount": 185000000,
                        "scope_description": bundle["final_terms"]["scopeDescription"],
                        "offering": bundle["flagship_offering"],
                    }
                ] + [
                    {
                        "id": p["id"],
                        "name": p["name"],
                        "duration_weeks": p["duration_weeks"],
                        "budget_amount": p["budget_amount"],
                        "scope_description": p["scope_description"],
                        "offering": {"deliverables": p["deliverables"]},
                    }
                    for p in bundle["catalog_packages"]
                ]

                for idx, pkg in enumerate(all_packages_to_upsert):
                    s_token = (
                        "goi-tuyen-sinh-dh-fpt-2027"
                        if pkg["id"] == PACKAGE_ID
                        else f"goi-se08-da-nganh-{idx:02d}"
                    )
                    cur.execute(
                        """
                        INSERT INTO media_packages (
                            id, name, is_template, agency_id, is_available_to_workspaces,
                            duration_weeks, budget_amount, scope_description, offering_details,
                            share_enabled, share_token, created_by, created_at, updated_at
                        ) VALUES (
                            %s::uuid, %s, FALSE, %s::uuid, TRUE,
                            %s, %s, %s, %s::jsonb,
                            TRUE, %s, %s::uuid, NOW() - (%s || ' days')::interval, NOW()
                        )
                        ON CONFLICT (id) DO UPDATE SET
                            name = EXCLUDED.name,
                            agency_id = EXCLUDED.agency_id,
                            is_available_to_workspaces = TRUE,
                            duration_weeks = EXCLUDED.duration_weeks,
                            budget_amount = EXCLUDED.budget_amount,
                            scope_description = EXCLUDED.scope_description,
                            offering_details = EXCLUDED.offering_details,
                            share_enabled = TRUE,
                            share_token = EXCLUDED.share_token,
                            created_by = EXCLUDED.created_by,
                            updated_at = NOW();
                        """,
                        (
                            pkg["id"],
                            pkg["name"],
                            AGENCY_ID,
                            pkg["duration_weeks"],
                            pkg["budget_amount"],
                            pkg["scope_description"],
                            json.dumps(pkg["offering"], ensure_ascii=False),
                            s_token,
                            owner_id,
                            str(35 - idx * 3),
                        ),
                    )

                # 7. Gắn Gói Tuyển sinh Đại học FPT 2027 vào Workspace (APPROVED + DEPLOYED)
                final_terms_json = json.dumps(bundle["final_terms"], ensure_ascii=False)
                cur.execute(
                    """
                    INSERT INTO workspace_media_packages (
                        id, workspace_id, package_id, negotiation_status, final_terms,
                        terms_version, client_proposal_count,
                        approved_by_agency_at, approved_by_client_at,
                        share_enabled, manager_led, preparation_status,
                        created_at, updated_at
                    ) VALUES (
                        %s::uuid, %s::uuid, %s::uuid, 'APPROVED', %s::jsonb,
                        2, 1,
                        NOW() - INTERVAL '16 days', NOW() - INTERVAL '15 days',
                        FALSE, TRUE, 'DEPLOYED',
                        NOW() - INTERVAL '18 days', NOW()
                    )
                    ON CONFLICT (workspace_id) DO UPDATE SET
                        package_id = EXCLUDED.package_id,
                        negotiation_status = 'APPROVED',
                        final_terms = EXCLUDED.final_terms,
                        terms_version = 2,
                        approved_by_agency_at = NOW() - INTERVAL '16 days',
                        approved_by_client_at = NOW() - INTERVAL '15 days',
                        manager_led = TRUE,
                        preparation_status = 'DEPLOYED',
                        preparation_error = NULL,
                        updated_at = NOW()
                    RETURNING id;
                    """,
                    (WS_PACKAGE_ID, WORKSPACE_ID, PACKAGE_ID, final_terms_json),
                )
                wmp_row = cur.fetchone()
                actual_wmp_id = str(wmp_row[0]) if wmp_row else WS_PACKAGE_ID
                resolved_ids["WS_PACKAGE_ID"] = actual_wmp_id

                cur.execute(
                    "UPDATE workspaces SET workspace_media_package_id = %s::uuid WHERE id = %s::uuid;",
                    (actual_wmp_id, WORKSPACE_ID),
                )

                neg_events = [
                    (1, "BASELINE", None, None, "SE08 Digital Agency khởi tạo đề xuất Gói Tuyển sinh Đại học FPT 2027 (4 Tuần) trên 4 nền tảng.", 18),
                    (2, "COUNTER_OFFER", manager_id, "MANAGER", "Nguyễn Thành Lộc cập nhật gói 19 hạng mục theo đề xuất của Ban Tuyển sinh ĐH FPT (02 buổi Workshop THPT, 01 Ngày hội Open Day, 02 tuyến bài báo chí VnExpress & Thanh Niên) và hai bên thống nhất phê duyệt.", 16),
                ]
                for idx_ne, (t_ver, n_act, n_actor, n_role, n_note, days_ago) in enumerate(neg_events):
                    cur.execute(
                        """
                        INSERT INTO package_negotiation_events (
                            id, workspace_media_package_id, terms_version, action,
                            actor_id, actor_role, note, terms_snapshot, created_at
                        ) VALUES (
                            %s::uuid, %s::uuid, %s, %s,
                            %s::uuid, %s, %s, %s::jsonb, NOW() - (%s || ' days')::interval
                        )
                        ON CONFLICT DO NOTHING;
                        """,
                        (
                            java_name_uuid_from_bytes(f"pkg-neg-2027:{actual_wmp_id}:{idx_ne}"),
                            actual_wmp_id,
                            t_ver,
                            n_act,
                            n_actor,
                            n_role,
                            n_note,
                            final_terms_json,
                            str(days_ago),
                        ),
                    )

                # 8. Đối tác truyền thông bên thứ ba (Third-Party Collaborators)
                cur.execute(
                    """
                    DELETE FROM campaign_collaborators
                    WHERE media_campaign_id IN (
                        SELECT id FROM media_campaigns WHERE workspace_media_package_id = %s::uuid
                    );
                    """,
                    (actual_wmp_id,),
                )
                extra_agency_collabs = [
                    (
                        "d7e00000-0000-4000-8000-000000000511",
                        "Báo Tuổi Trẻ - Chuyên trang Nhịp sống Số & Giáo dục",
                        "NEWSPAPER",
                        {"contactPerson": "Nhà báo Minh Đức", "email": "giaoduc@tuoitre.com.vn", "phone": "02839973838"},
                        "Đối tác truyền thông báo chí kỳ cựu cho khối trường đại học và doanh nghiệp công nghệ phía Nam.",
                    ),
                    (
                        "d7e00000-0000-4000-8000-000000000512",
                        "Hệ thống Màn hình LED Quảng trường Cầu Rồng & Sân bay Đà Nẵng",
                        "BANNER",
                        {"contactPerson": "Lê Quốc Hưng", "email": "booking@doohdanang.vn", "phone": "02363888999"},
                        "Đối tác quảng cáo ngoài trời DOOH phục vụ chiến dịch cao điểm tuyển sinh và du lịch miền Trung.",
                    ),
                    (
                        "d7e00000-0000-4000-8000-000000000513",
                        "Đài Phát thanh - Truyền hình Đà Nẵng (DanangTV)",
                        "TV",
                        {"contactPerson": "BTV Thanh Huyền", "email": "banbientap@danangtv.vn", "phone": "02363896555"},
                        "Phối hợp ghi hình phóng sự chuỗi Workshop hướng nghiệp THPT và sự kiện công nghệ tại FPT City.",
                    ),
                    (
                        "d7e00000-0000-4000-8000-000000000514",
                        "Cộng đồng Sinh viên Công nghệ & Học bổng Việt Nam (EduTech Creators)",
                        "OTHER",
                        {"contactPerson": "Phạm Gia Bảo", "email": "collab@edutechvn.org", "phone": "0905666789"},
                        "Mạng lưới KOC sinh viên chuyên review môi trường học tập, ký túc xá và kỳ thực tập doanh nghiệp.",
                    ),
                ]
                keep_collab_ids = [c[0] for c in bundle["collaborators"]] + [c[0] for c in extra_agency_collabs]
                cur.execute(
                    """
                    DELETE FROM third_party_collaborators
                    WHERE agency_id = %s::uuid
                      AND id <> ALL(%s::uuid[])
                      AND id NOT IN (SELECT collaborator_id FROM campaign_collaborators);
                    """,
                    (AGENCY_ID, keep_collab_ids),
                )
                all_collabs_to_upsert = [
                    (c_id, p_name, p_type, c_info, notes)
                    for c_id, p_name, p_type, c_info, notes, _coop_status in bundle["collaborators"]
                ] + extra_agency_collabs
                for c_id, p_name, p_type, c_info, notes in all_collabs_to_upsert:
                    cur.execute(
                        """
                        INSERT INTO third_party_collaborators (
                            id, agency_id, partner_name, partner_type, contact_info, notes,
                            is_active, first_used_at, usage_history_verified, version,
                            created_by, created_at, updated_at
                        ) VALUES (
                            %s::uuid, %s::uuid, %s, %s::collaborator_type, %s::jsonb, %s,
                            TRUE, NOW() - INTERVAL '14 days', TRUE, 1,
                            %s::uuid, NOW() - INTERVAL '30 days', NOW()
                        )
                        ON CONFLICT (id) DO UPDATE SET
                            agency_id = EXCLUDED.agency_id,
                            partner_name = EXCLUDED.partner_name,
                            partner_type = EXCLUDED.partner_type,
                            contact_info = EXCLUDED.contact_info,
                            notes = EXCLUDED.notes,
                            is_active = TRUE,
                            usage_history_verified = TRUE,
                            updated_at = NOW();
                        """,
                        (c_id, AGENCY_ID, p_name, p_type, json.dumps(c_info, ensure_ascii=False), notes, owner_id),
                    )

                # 9. Chiến dịch Tuyển sinh Đại học FPT 2027 (4 Tuần - IN_PROGRESS)
                # Xóa chiến dịch cũ khác ID nếu gắn cùng workspace_media_package_id để giữ đúng CAMPAIGN_ID cố định
                cur.execute(
                    """
                    DELETE FROM campaign_deployments
                    WHERE campaign_id IN (
                        SELECT id FROM media_campaigns
                        WHERE workspace_media_package_id = %s::uuid AND id <> %s::uuid
                    );
                    DELETE FROM campaign_versions
                    WHERE campaign_id IN (
                        SELECT id FROM media_campaigns
                        WHERE workspace_media_package_id = %s::uuid AND id <> %s::uuid
                    );
                    DELETE FROM media_campaigns
                    WHERE workspace_media_package_id = %s::uuid AND id <> %s::uuid;
                    """,
                    (actual_wmp_id, CAMPAIGN_ID, actual_wmp_id, CAMPAIGN_ID, actual_wmp_id, CAMPAIGN_ID),
                )

                timeline_json = json.dumps(bundle["timeline"], ensure_ascii=False)
                deliverables_json = json.dumps(bundle["flagship_deliverables"], ensure_ascii=False)
                allocations_json = json.dumps(bundle["allocations"], ensure_ascii=False)
                work_items_json = json.dumps(bundle["work_items"], ensure_ascii=False)

                cur.execute(
                    """
                    INSERT INTO media_campaigns (
                        id, workspace_media_package_id, name, strategy_detail, brand_guideline,
                        timeline, package_terms_snapshot, package_terms_version,
                        allocations, deliverable_plan, work_items,
                        content_version, row_version, status,
                        approved_by_agency_at, approved_by_agency_id, approved_by_agency_version,
                        approved_by_client_at, approved_by_client_id, approved_by_client_version,
                        created_at, updated_at
                    ) VALUES (
                        %s::uuid, %s::uuid,
                        'Chiến dịch Tuyển sinh Đại học FPT 2027: Khai phóng Tiềm năng Công nghệ (4 Tuần)',
                        %s, %s,
                        %s::jsonb, %s::jsonb, 2,
                        %s::jsonb, %s::jsonb, %s::jsonb,
                        1, 1, 'IN_PROGRESS',
                        NOW() - INTERVAL '15 days', %s::uuid, 1,
                        NOW() - INTERVAL '14 days', %s::uuid, 1,
                        NOW() - INTERVAL '16 days', NOW()
                    )
                    ON CONFLICT (id) DO UPDATE SET
                        workspace_media_package_id = EXCLUDED.workspace_media_package_id,
                        name = EXCLUDED.name,
                        strategy_detail = EXCLUDED.strategy_detail,
                        brand_guideline = EXCLUDED.brand_guideline,
                        timeline = EXCLUDED.timeline,
                        package_terms_snapshot = EXCLUDED.package_terms_snapshot,
                        package_terms_version = 2,
                        allocations = EXCLUDED.allocations,
                        deliverable_plan = EXCLUDED.deliverable_plan,
                        work_items = EXCLUDED.work_items,
                        content_version = 1,
                        status = 'IN_PROGRESS',
                        approved_by_agency_at = NOW() - INTERVAL '15 days',
                        approved_by_agency_id = EXCLUDED.approved_by_agency_id,
                        approved_by_agency_version = 1,
                        approved_by_client_at = NOW() - INTERVAL '14 days',
                        approved_by_client_id = EXCLUDED.approved_by_client_id,
                        approved_by_client_version = 1,
                        completed_at = NULL,
                        completed_by = NULL,
                        completion_reason = NULL,
                        updated_at = NOW();
                    """,
                    (
                        CAMPAIGN_ID,
                        actual_wmp_id,
                        bundle["strategy_detail"],
                        bundle["brand_guideline"],
                        timeline_json,
                        final_terms_json,
                        allocations_json,
                        deliverables_json,
                        work_items_json,
                        manager_id,
                        client_id,
                    ),
                )

                snapshot_json = json.dumps(
                    {
                        "name": "Chiến dịch Tuyển sinh Đại học FPT 2027: Khai phóng Tiềm năng Công nghệ (4 Tuần)",
                        "strategyDetail": bundle["strategy_detail"],
                        "brandGuideline": bundle["brand_guideline"],
                        "timeline": bundle["timeline"],
                        "workItems": bundle["work_items"],
                        "deliverablePlan": bundle["flagship_deliverables"],
                    },
                    ensure_ascii=False,
                )
                cur.execute("DELETE FROM campaign_versions WHERE campaign_id = %s::uuid;", (CAMPAIGN_ID,))
                cur.execute(
                    """
                    INSERT INTO campaign_versions (id, campaign_id, content_version, snapshot, created_by, created_at)
                    VALUES (%s::uuid, %s::uuid, 1, %s::jsonb, %s::uuid, NOW() - INTERVAL '15 days');
                    """,
                    (java_name_uuid_from_bytes(f"camp-ver:{CAMPAIGN_ID}:1"), CAMPAIGN_ID, snapshot_json, manager_id),
                )

                cur.execute("DELETE FROM campaign_deployments WHERE campaign_id = %s::uuid;", (CAMPAIGN_ID,))
                cur.execute(
                    """
                    INSERT INTO campaign_deployments (
                        id, campaign_id, content_version, requested_by, status,
                        attempt_count, created_at, updated_at, completed_at
                    ) VALUES (
                        %s::uuid, %s::uuid, 1, %s::uuid, 'SUCCEEDED',
                        1, NOW() - INTERVAL '14 days', NOW() - INTERVAL '14 days', NOW() - INTERVAL '14 days'
                    );
                    """,
                    (java_name_uuid_from_bytes(f"camp-deploy:{CAMPAIGN_ID}:1"), CAMPAIGN_ID, manager_id),
                )

                rev_events = [
                    ("AGENCY", "APPROVE", manager_id, "Nguyễn Thành Lộc hoàn tất phân bổ lịch trình 4 tuần (19 hạng mục từ gói truyền thông) và trình duyệt kế hoạch tổng thể.", 15),
                    ("CLIENT", "FEEDBACK", client_id, "Ban Tuyển sinh ĐH FPT xác nhận lộ trình 4 tuần rất rõ ràng, lưu ý nhấn mạnh 3 mức Học bổng Nguyễn Văn Đạo (50%, 70%, 100%) và kỳ thực tập OJT học kỳ 6.", 15),
                    ("CLIENT", "APPROVE", client_id, "Ban Tuyển sinh Trường Đại học FPT chính thức phê duyệt kế hoạch Chiến dịch Tuyển sinh 2027 để triển khai công việc.", 14),
                ]
                for idx_re, (r_side, r_type, r_actor, r_comment, days_ago) in enumerate(rev_events):
                    cur.execute(
                        """
                        INSERT INTO campaign_review_events (
                            id, campaign_id, content_version, actor_id, actor_side, event_type, comment, created_at
                        ) VALUES (
                            %s::uuid, %s::uuid, 1, %s::uuid, %s, %s, %s, NOW() - (%s || ' days')::interval
                        )
                        ON CONFLICT (id) DO NOTHING;
                        """,
                        (
                            java_name_uuid_from_bytes(f"camp-rev-2027:{CAMPAIGN_ID}:{idx_re}"),
                            CAMPAIGN_ID,
                            r_actor,
                            r_side,
                            r_type,
                            r_comment,
                            str(days_ago),
                        ),
                    )

                # Gắn cả 6 đối tác vào chiến dịch
                for idx, (c_id, _p_name, _p_type, _c_info, _notes, coop_status) in enumerate(bundle["collaborators"]):
                    cc_id = f"d7e00000-0000-4000-8000-{601 + idx:012d}"
                    cur.execute(
                        """
                        INSERT INTO campaign_collaborators (
                            id, media_campaign_id, collaborator_id, cooperation_status, updated_by, updated_at
                        ) VALUES (
                            %s::uuid, %s::uuid, %s::uuid, %s::cooperation_status, %s::uuid, NOW() - INTERVAL '5 days'
                        );
                        """,
                        (cc_id, CAMPAIGN_ID, c_id, coop_status, manager_id),
                    )

                # 10. Bộ Hashtag chuẩn của Workspace Tuyển sinh Đại học FPT 2027
                cur.execute("DELETE FROM workspace_hashtags WHERE workspace_id = %s::uuid;", (WORKSPACE_ID,))
                for tag, norm_tag, purpose, is_req, c_ref in bundle["hashtags"]:
                    h_id = java_name_uuid_from_bytes(f"ws-hashtag:{WORKSPACE_ID}:{norm_tag}")
                    cur.execute(
                        """
                        INSERT INTO workspace_hashtags (
                            id, workspace_id, tag, normalized_tag, purpose,
                            added_by, added_by_name, is_required, campaign_id,
                            created_at, updated_at, version
                        ) VALUES (
                            %s::uuid, %s::uuid, %s, %s, %s,
                            %s::uuid, 'Nguyễn Thành Lộc', %s, %s::uuid,
                            NOW() - INTERVAL '14 days', NOW(), 0
                        );
                        """,
                        (h_id, WORKSPACE_ID, tag, norm_tag, purpose, manager_id, is_req, c_ref),
                    )

                # 11. Workspace Template mẫu ngành Giáo dục Đại học của SE08 Digital Agency
                tpl_id = "d7e00000-0000-4000-8000-000000000680"
                tpl_snapshot = json.dumps(
                    {
                        "industry": "EDUCATION",
                        "timezoneConfig": "Asia/Ho_Chi_Minh",
                        "brandColor": "#F05A28",
                        "defaultHashtags": ["#DaiHocFPT", "#TuyenSinhFPTU2027", "#HocBongNguyenVanDao"],
                        "approvalMode": "TWO_TIER",
                    },
                    ensure_ascii=False,
                )
                cur.execute(
                    """
                    INSERT INTO workspace_templates (id, agency_id, name, source_workspace_id, config_snapshot, created_by, created_at)
                    VALUES (
                        %s::uuid, %s::uuid,
                        'Mẫu Không gian Chiến dịch Tuyển sinh Đại học & Chuỗi Workshop THPT',
                        %s::uuid, %s::jsonb, %s::uuid, NOW() - INTERVAL '20 days'
                    )
                    ON CONFLICT (id) DO UPDATE SET
                        name = EXCLUDED.name,
                        config_snapshot = EXCLUDED.config_snapshot;
                    """,
                    (tpl_id, AGENCY_ID, WORKSPACE_ID, tpl_snapshot, owner_id),
                )

                # 12. Đảm bảo Gói cước Agency (PLUS/PRO đang hoạt động để B14 nâng cấp lên gói cao hơn) & Ví AI Credit dồi dào
                cur.execute(
                    """
                    UPDATE agency_subscriptions
                    SET status = 'ACTIVE',
                        current_period_start = NOW() - INTERVAL '10 days',
                        current_period_end = NOW() + INTERVAL '20 days',
                        updated_at = NOW()
                    WHERE agency_id = %s::uuid;
                    """,
                    (AGENCY_ID,),
                )
                cur.execute(
                    """
                    INSERT INTO agency_credit_wallets (agency_id, available_credits, reserved_credits, opening_balance_state, version, updated_at)
                    VALUES (%s::uuid, 8500, 0, 'VERIFIED', 1, NOW())
                    ON CONFLICT (agency_id) DO UPDATE SET
                        available_credits = GREATEST(agency_credit_wallets.available_credits, 8500),
                        opening_balance_state = 'VERIFIED',
                        updated_at = NOW();
                    """,
                    (AGENCY_ID,),
                )

                # 13. Hàng đợi kiểm duyệt nội dung cộng đồng (FR 3.10.4) & Thông báo hệ thống cho màn hình Admin (B15)
                cur.execute("DELETE FROM content_moderation_reviews WHERE workspace_id = %s::uuid;", (WORKSPACE_ID,))
                mod_samples = [
                    (
                        "d7e000000000000000000191",
                        "COMPLIANCE",
                        "Phát hiện cụm từ cam kết tuyển thẳng thiếu căn cứ quy chế Bộ GD&ĐT cần quản trị viên kiểm tra",
                        "PENDING",
                        None,
                        None,
                        None,
                        "Cam kết tuyển thẳng 100% không cần xét học bạ, đóng phí giữ chỗ nhận ngay học bổng toàn phần!",
                    ),
                    (
                        "d7e000000000000000000192",
                        "COMPLIANCE",
                        "Kiểm tra định kỳ bài thông báo Học bổng Nguyễn Văn Đạo 2027",
                        "APPROVED",
                        "Nội dung tuân thủ đúng quy chế tuyển sinh và chính sách cộng đồng.",
                        None,
                        None,
                        "Thông báo quy chế xét cấp Học bổng Nguyễn Văn Đạo năm 2027 mức 50%, 70%, 100% học phí tại 5 cơ sở.",
                    ),
                    (
                        "d7e000000000000000000193",
                        "FLAGGED_AUTHOR",
                        "Nội dung quảng cáo so sánh hạ thấp đơn vị đào tạo khác",
                        "BLOCKED",
                        "Vi phạm quy chuẩn truyền thông giáo dục: sử dụng ngôn từ công kích đơn vị khác.",
                        "YELLOW",
                        "HARASSMENT",
                        "Tất cả các trường khác đều dạy lý thuyết lỗi thời, bằng cấp vô giá trị!",
                    ),
                ]
                for p_id, src, reason, m_status, d_note, s_lvl, s_cat, c_text in mod_samples:
                    r_id = java_name_uuid_from_bytes(f"mod-review:{p_id}")
                    decided = m_status != "PENDING"
                    cur.execute(
                        """
                        INSERT INTO content_moderation_reviews (
                            id, post_id, content_version, content_hash, workspace_id, author_id,
                            source, reason, status, decision_note, strike_level, strike_category,
                            reviewed_by, reviewed_at, created_at, row_version
                        ) VALUES (
                            %s::uuid, %s, 1, %s, %s::uuid, %s::uuid,
                            %s, %s, %s, %s, %s, %s,
                            %s::uuid, CASE WHEN %s THEN NOW() - INTERVAL '1 day' ELSE NULL END,
                            NOW() - INTERVAL '2 days', 0
                        )
                        ON CONFLICT (id) DO UPDATE SET
                            reason = EXCLUDED.reason,
                            status = EXCLUDED.status,
                            decision_note = EXCLUDED.decision_note,
                            reviewed_by = EXCLUDED.reviewed_by,
                            reviewed_at = EXCLUDED.reviewed_at;
                        """,
                        (
                            r_id,
                            p_id,
                            sha256_hex(c_text),
                            WORKSPACE_ID,
                            creator_id,
                            src,
                            reason,
                            m_status,
                            d_note,
                            s_lvl,
                            s_cat,
                            admin_id if decided else None,
                            decided,
                        ),
                    )

                cur.execute(
                    """
                    INSERT INTO admin_notifications (
                        id, title, content, type, target_type, status,
                        sent_at, recipient_count, created_by, created_at, updated_at, row_version
                    ) VALUES
                        (
                            'd7e00000-0000-4000-8000-000000000101'::uuid,
                            'Cập nhật bộ lọc kiểm duyệt nội dung truyền thông Giáo dục & Y tế',
                            'Hệ thống AI kiểm duyệt tuân thủ đã bổ sung danh mục từ khóa nhạy cảm cho mùa tuyển sinh 2027.',
                            'UPDATE', 'ALL', 'SENT',
                            NOW() - INTERVAL '7 days', 32, %s::uuid, NOW() - INTERVAL '7 days', NOW() - INTERVAL '7 days', 0
                        ),
                        (
                            'd7e00000-0000-4000-8000-000000000102'::uuid,
                            'Đối soát thanh toán tự động qua cổng SePay (VietQR)',
                            'Hoàn tất nâng cấp luồng xác nhận giao dịch nâng cấp gói Agency và nạp AI Credit thời gian thực.',
                            'MAINTENANCE', 'ALL', 'SENT',
                            NOW() - INTERVAL '3 days', 32, %s::uuid, NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days', 0
                        )
                    ON CONFLICT (id) DO UPDATE SET
                        title = EXCLUDED.title,
                        content = EXCLUDED.content,
                        updated_at = NOW();
                    """,
                    (admin_id, admin_id),
                )

                # 14. Lịch sử gửi Email thực tế (mail_batches, mail_deliveries, mail_suppressions) - xóa sạch dữ liệu Faker cũ
                cur.execute(
                    """
                    DELETE FROM mail_deliveries
                    WHERE batch_id IN (
                        SELECT id FROM mail_batches WHERE workspace_id = %s::uuid OR agency_id = %s::uuid
                    );
                    DELETE FROM mail_batches WHERE workspace_id = %s::uuid OR agency_id = %s::uuid;
                    DELETE FROM mail_suppressions WHERE workspace_id = %s::uuid OR agency_id = %s::uuid;
                    """,
                    (WORKSPACE_ID, AGENCY_ID, WORKSPACE_ID, AGENCY_ID, WORKSPACE_ID, AGENCY_ID),
                )
                batch_1_id = "d7e00000-0000-4000-8000-000000000891"
                batch_2_id = "d7e00000-0000-4000-8000-000000000892"
                ws_display = "Đại học FPT Tuyển sinh 2027 x SE08 Digital"
                batch_1_html = (
                    "<div style='font-family:Inter,Arial,sans-serif;max-width:600px;margin:0 auto;padding:20px;'>"
                    "<h2 style='color:#ea580c;'>Vé mời Workshop Trải nghiệm Phòng Lab &amp; Tiện ích Đại học FPT 2027</h2>"
                    "<p>Ban Tuyển sinh Trường Đại học FPT xác nhận lịch tham dự buổi trải nghiệm kính thực tế ảo VR, "
                    "mô hình Robotics và tư vấn Học bổng Nguyễn Văn Đạo (50%, 70%, 100%) dành cho học sinh lớp 12.</p></div>"
                )
                batch_2_html = (
                    "<div style='font-family:Inter,Arial,sans-serif;max-width:600px;margin:0 auto;padding:20px;'>"
                    "<h2 style='color:#ea580c;'>Báo cáo Tiến độ Tuần 2 Chiến dịch Tuyển sinh Đại học FPT 2027</h2>"
                    "<p>Nhóm dự án SE08 Digital Agency cập nhật kết quả xuất bản 8 hạng mục truyền thông trên 4 nền tảng "
                    "(Facebook, Instagram, TikTok, Threads) và danh sách 18 trường THPT xác nhận tham dự chuỗi Workshop Tuần 3.</p></div>"
                )
                cur.execute(
                    """
                    INSERT INTO mail_batches (
                        id, workspace_id, workspace_name, template_id, template_name,
                        sent_by, sender_email, sender_name, kind, status,
                        subject, body_html, attachments, scheduled_at, timezone,
                        total, accepted, rejected_count, sent_count, failed_count, suppressed_count,
                        created_at, completed_at, scope, agency_id
                    ) VALUES
                        (
                            %s::uuid, %s::uuid, %s, 'd7e00000-0000-4000-8000-000000000881',
                            'Thư mời tham dự Workshop Trải nghiệm Tiện ích Đại học FPT 2027',
                            %s::uuid, 'user15@demo.brandhub.test', 'Hà Văn Ân', 'SEND', 'COMPLETED',
                            '[Đại học FPT 2027] Vé mời tham dự Workshop trải nghiệm Phòng Lab & Tiện ích Campus',
                            %s, '[]'::jsonb, NOW() - INTERVAL '3 days', 'Asia/Ho_Chi_Minh',
                            4, 4, 0, 4, 0, 0,
                            NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days' + INTERVAL '2 minutes',
                            'CAMPAIGN_BROADCAST', NULL
                        ),
                        (
                            %s::uuid, %s::uuid, %s, 'd7e00000-0000-4000-8000-000000000882',
                            'Báo cáo tiến độ tuần Chiến dịch Tuyển sinh gửi Ban Tuyển sinh ĐH FPT',
                            %s::uuid, 'user1@demo.brandhub.test', 'Nguyễn Thành Lộc', 'SEND', 'COMPLETED',
                            '[SE08 Digital x ĐH FPT] Báo cáo kết quả Tuần 2 Chiến dịch Tuyển sinh 2027',
                            %s, '[]'::jsonb, NOW() - INTERVAL '5 days', 'Asia/Ho_Chi_Minh',
                            2, 2, 0, 2, 0, 0,
                            NOW() - INTERVAL '5 days', NOW() - INTERVAL '5 days' + INTERVAL '1 minute',
                            'WORKSPACE_MANAGER', NULL
                        );
                    """,
                    (
                        batch_1_id,
                        WORKSPACE_ID,
                        ws_display,
                        creator3_id,
                        batch_1_html,
                        batch_2_id,
                        WORKSPACE_ID,
                        ws_display,
                        manager_id,
                        batch_2_html,
                    ),
                )
                student_deliveries = [
                    ("hoangnam.2k9@demo.brandhub.test", "Nguyễn Hoàng Nam - THPT Phan Châu Trinh"),
                    ("minhkhoi.2k9@demo.brandhub.test", "Trần Minh Khôi - THPT Chuyên Lê Quý Đôn"),
                    ("ngocanh.2k9@demo.brandhub.test", "Võ Ngọc Ánh - THPT Hoàng Hoa Thám"),
                    ("giahan.2k9@demo.brandhub.test", "Lê Gia Hân - THPT Trần Phú"),
                ]
                for idx_d, (r_email, r_name) in enumerate(student_deliveries):
                    cur.execute(
                        """
                        INSERT INTO mail_deliveries (
                            id, batch_id, recipient, recipient_name, variables,
                            rendered_subject, rendered_body_html, external_audience,
                            status, attempts, next_attempt_at, sent_at, event_key
                        ) VALUES (
                            %s::uuid, %s::uuid, %s, %s, %s::jsonb,
                            %s, %s, TRUE,
                            'SENT', 1, NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days', %s
                        );
                        """,
                        (
                            java_name_uuid_from_bytes(f"mail-deliv:{batch_1_id}:{idx_d}"),
                            batch_1_id,
                            r_email,
                            r_name,
                            json.dumps({"name": r_name}, ensure_ascii=False),
                            f"[Đại học FPT 2027] Vé mời {r_name} tham dự Workshop trải nghiệm Phòng Lab & Tiện ích Campus",
                            batch_1_html,
                            f"fptu2027-ws-invite-{idx_d}",
                        ),
                    )
                report_deliveries = [
                    ("user59@demo.brandhub.test", "Ban Tuyển sinh Đại học FPT"),
                    ("user177@demo.brandhub.test", "Lê Trí Trung"),
                ]
                for idx_r, (r_email, r_name) in enumerate(report_deliveries):
                    cur.execute(
                        """
                        INSERT INTO mail_deliveries (
                            id, batch_id, recipient, recipient_name, variables,
                            rendered_subject, rendered_body_html, external_audience,
                            status, attempts, next_attempt_at, sent_at, event_key
                        ) VALUES (
                            %s::uuid, %s::uuid, %s, %s, %s::jsonb,
                            '[SE08 Digital x ĐH FPT] Báo cáo kết quả Tuần 2 Chiến dịch Tuyển sinh 2027',
                            %s, FALSE,
                            'SENT', 1, NOW() - INTERVAL '5 days', NOW() - INTERVAL '5 days', %s
                        );
                        """,
                        (
                            java_name_uuid_from_bytes(f"mail-deliv:{batch_2_id}:{idx_r}"),
                            batch_2_id,
                            r_email,
                            r_name,
                            json.dumps({"name": r_name, "weekNumber": "2"}, ensure_ascii=False),
                            batch_2_html,
                            f"fptu2027-weekly-rep-{idx_r}",
                        ),
                    )
                cur.execute(
                    """
                    INSERT INTO mail_suppressions (id, workspace_id, email_lower, reason, created_at, agency_id, client_profile_id)
                    VALUES
                        (%s::uuid, %s::uuid, 'cuusinhvien.k21@demo.brandhub.test', 'UNSUBSCRIBED', NOW() - INTERVAL '4 days', NULL, %s::uuid),
                        (%s::uuid, NULL, 'homthu.cu.thpt@demo.brandhub.test', 'HARD_BOUNCE', NOW() - INTERVAL '6 days', %s::uuid, NULL);
                    """,
                    (
                        java_name_uuid_from_bytes(f"mail-supp:{WORKSPACE_ID}:1"),
                        WORKSPACE_ID,
                        CLIENT_PROFILE_ID,
                        java_name_uuid_from_bytes(f"mail-supp:{AGENCY_ID}:1"),
                        AGENCY_ID,
                    ),
                )

                # 15. Chuông thông báo trong ứng dụng (user_notifications) sạch 100% cho cả 7 tài khoản Demo
                demo_user_list = [owner_id, manager_id, creator_id, creator2_id, creator3_id, client_id, admin_id]
                cur.execute("DELETE FROM user_notifications WHERE user_id = ANY(%s::uuid[]);", (demo_user_list,))
                inbox_rows = [
                    (
                        owner_id,
                        "Ban Tuyển sinh ĐH FPT đã phê duyệt Gói Tuyển sinh 2027 (4 Tuần)",
                        "Gói truyền thông 19 hạng mục ngân sách 185.000.000 VND đã chuyển sang trạng thái triển khai.",
                        f"/workspaces/{WORKSPACE_ID}/media-package",
                        False,
                        6,
                    ),
                    (
                        owner_id,
                        "Ví AI Credit của SE08 Digital Agency đang có 8.500 điểm khả dụng",
                        "Sẵn sàng phân bổ hạn mức cho nhóm nội dung, hình ảnh và kiểm tra tuân thủ mùa tuyển sinh.",
                        f"/agency/{AGENCY_ID}/credit",
                        True,
                        24,
                    ),
                    (
                        manager_id,
                        "Yêu cầu nội dung mới từ Ban Tuyển sinh Đại học FPT",
                        "Đề nghị bổ sung bài thông báo 08 điểm đón xe buýt miễn phí dự Ngày hội FPTU Open Day 2027.",
                        f"/workspaces/{WORKSPACE_ID}/requests",
                        False,
                        3,
                    ),
                    (
                        manager_id,
                        "Hà Văn Ân đã gửi duyệt Thông cáo Báo chí VnExpress Giáo dục",
                        "Phần thông cáo tổng kết chuỗi Workshop trải nghiệm tiện ích THPT đang chờ Manager xem xét.",
                        f"/workspaces/{WORKSPACE_ID}/tasks",
                        False,
                        5,
                    ),
                    (
                        creator_id,
                        "Ban Tuyển sinh ĐH FPT đã duyệt ảnh & kênh đăng Bài trọng điểm Tuần 3",
                        "Phần hình ảnh Workshop THPT và lịch đăng 4 nền tảng đã đạt yêu cầu, sẵn sàng hoàn thiện caption.",
                        f"/workspaces/{WORKSPACE_ID}/editor?taskId={TASK_1_ID}",
                        False,
                        2,
                    ),
                    (
                        creator2_id,
                        "Nguyễn Thành Lộc nhắc lịch hậu cần Ngày hội FPTU Open Day 2027",
                        "Kiểm tra lần cuối phương án âm thanh sân khấu chính và 12 trạm trải nghiệm phòng Lab bán dẫn.",
                        f"/workspaces/{WORKSPACE_ID}/tasks",
                        False,
                        4,
                    ),
                    (
                        creator3_id,
                        "Đã hoàn tất gửi 4/4 vé mời Email Chuỗi Workshop THPT 2027",
                        "Lô gửi thư mời tham dự trải nghiệm tiện ích học đường ĐH FPT đã hoàn thành không có lỗi phát sinh.",
                        f"/workspaces/{WORKSPACE_ID}/mail-templates/batches",
                        False,
                        8,
                    ),
                    (
                        client_id,
                        "Có 2 phần nội dung Ngày hội FPTU Open Day 2027 chờ Khách hàng duyệt",
                        "Nguyễn Thành Lộc đã duyệt nội bộ kịch bản chương trình và kế hoạch truyền thông sự kiện Open Day.",
                        f"/workspaces/{WORKSPACE_ID}/portal",
                        False,
                        3,
                    ),
                    (
                        client_id,
                        "Báo cáo khảo sát học sinh lớp 12 trước thềm Workshop Tuần 3 đã cập nhật",
                        "Biểu mẫu khảo sát nguyện vọng ngành Vi mạch, AI và tiện ích nội trú đã ghi nhận phản hồi mới.",
                        f"/workspaces/{WORKSPACE_ID}/tasks/{SURVEY_TASK_ID}/survey",
                        True,
                        18,
                    ),
                    (
                        admin_id,
                        "Có 1 bài đăng vi phạm quy chuẩn tuyển sinh trong hàng đợi kiểm duyệt",
                        "Hệ thống phát hiện cụm từ cam kết tuyển thẳng thiếu căn cứ cần Admin xử lý tại hàng đợi tuân thủ.",
                        "/admin?view=moderation",
                        False,
                        2,
                    ),
                ]
                for idx_n, (u_id, n_title, n_body, n_url, is_read, hrs_ago) in enumerate(inbox_rows):
                    cur.execute(
                        """
                        INSERT INTO user_notifications (
                            id, user_id, type, title, content, action_url, created_at, read_at
                        ) VALUES (
                            %s::uuid, %s::uuid, 'UPDATE', %s, %s, %s,
                            NOW() - (%s || ' hours')::interval,
                            CASE WHEN %s THEN NOW() - INTERVAL '1 hour' ELSE NULL END
                        );
                        """,
                        (
                            java_name_uuid_from_bytes(f"fptu2027-notif:{idx_n}"),
                            u_id,
                            n_title,
                            n_body,
                            n_url,
                            str(hrs_ago),
                            is_read,
                        ),
                    )

                # 16. Lời mời thành viên Agency & Workspace (xóa sạch email Faker ngẫu nhiên)
                cur.execute(
                    """
                    DELETE FROM agency_invitations WHERE agency_id = %s::uuid OR invited_by = ANY(%s::uuid[]);
                    DELETE FROM workspace_invitations WHERE workspace_id = %s::uuid OR invited_by = ANY(%s::uuid[]);
                    """,
                    (AGENCY_ID, demo_user_list, WORKSPACE_ID, demo_user_list),
                )
                cur.execute(
                    """
                    INSERT INTO agency_invitations (
                        id, agency_id, invited_email, invited_by, token, note, workspace_id, role, status, expires_at, created_at
                    ) VALUES (
                        %s::uuid, %s::uuid, 'thietke.motion@se08digital.vn', %s::uuid,
                        'inv-agency-se08-motion-2027',
                        'Mời chuyên viên dựng đồ họa chuyển động hỗ trợ cao điểm Ngày hội FPTU Open Day 2027',
                        %s::uuid, 'CREATOR'::workspace_member_role, 'PENDING'::invitation_status,
                        NOW() + INTERVAL '7 days', NOW() - INTERVAL '1 day'
                    );
                    """,
                    (
                        java_name_uuid_from_bytes(f"agency-inv:{AGENCY_ID}:1"),
                        AGENCY_ID,
                        owner_id,
                        WORKSPACE_ID,
                    ),
                )
                cur.execute(
                    """
                    INSERT INTO workspace_invitations (
                        id, workspace_id, invited_email, invited_by, token, role, status, expires_at, created_at
                    ) VALUES (
                        %s::uuid, %s::uuid, 'tuvan.tuyensinh.danang@fpt.edu.vn', %s::uuid,
                        'inv-ws-fptu-danang-2027',
                        'CLIENT'::workspace_member_role, 'PENDING'::invitation_status,
                        NOW() + INTERVAL '7 days', NOW() - INTERVAL '12 hours'
                    );
                    """,
                    (
                        java_name_uuid_from_bytes(f"ws-inv:{WORKSPACE_ID}:1"),
                        WORKSPACE_ID,
                        manager_id,
                    ),
                )

                # 17. Bảng giá AI Credit (/admin/credit-prices), Hạn mức Credit Workspace & Dung lượng Kho Client Vault
                credit_ops = [
                    ("CONTENT_GENERATE", 5),
                    ("CAPTION_VARIANTS", 8),
                    ("HASHTAG_GENERATE", 2),
                    ("AMBASSADOR_GENERATE", 40),
                    ("CHARACTER_SHEET", 30),
                    ("COMMERCIAL_IMAGE", 20),
                    ("VIDEO_GENERATE", 60),
                ]
                for op_name, unit_cred in credit_ops:
                    cur.execute("SELECT COUNT(*) FROM ai_credit_operation_prices WHERE operation = %s;", (op_name,))
                    if (cur.fetchone() or [0])[0] == 0:
                        cur.execute(
                            """
                            INSERT INTO ai_credit_operation_prices (
                                id, operation, revision, unit_credits, enabled, created_by, created_at
                            ) VALUES (
                                %s::uuid, %s, 1, %s, TRUE, %s::uuid, NOW() - INTERVAL '30 days'
                            );
                            """,
                            (java_name_uuid_from_bytes(f"credit-price:{op_name}:1"), op_name, unit_cred, admin_id),
                        )

                cur.execute(
                    "DELETE FROM workspace_credit_limits WHERE agency_id = %s::uuid AND workspace_id = %s::uuid;",
                    (AGENCY_ID, WORKSPACE_ID),
                )
                cur.execute(
                    """
                    INSERT INTO workspace_credit_limits (agency_id, workspace_id, cap, version, updated_by, updated_at)
                    VALUES (%s::uuid, %s::uuid, 5000, 1, %s::uuid, NOW());
                    """,
                    (AGENCY_ID, WORKSPACE_ID, owner_id),
                )
                cur.execute("DELETE FROM client_vault_storage_usage WHERE user_id = %s::uuid;", (client_id,))
                cur.execute(
                    """
                    INSERT INTO client_vault_storage_usage (user_id, used_bytes, reserved_bytes, version, inventory_verified_at, updated_at)
                    VALUES (%s::uuid, 1845200, 0, 1, NOW(), NOW());
                    """,
                    (client_id,),
                )

                # 18. Hai Workspace khách hàng đa ngành sạch sẽ của SE08 Digital Agency (để trình chuyển đổi Workspace giàu dữ liệu, 0 Faker)
                companion_workspaces = [
                    (
                        "d7e00000-0000-4000-8000-000000000091",
                        "CloudWork SaaS Vietnam x SE08 Digital",
                        "TECHNOLOGY",
                        "SIZE_51_200",
                        "https://cloudwork.vn",
                        "02873008899",
                        "Quận 1, TP. Hồ Chí Minh",
                        "Không gian triển khai nội dung ra mắt nền tảng quản trị hiệu suất doanh nghiệp B2B CloudWork 3.0.",
                        "#2563EB",
                        "Tối ưu vận hành số cho doanh nghiệp Việt",
                        2021,
                    ),
                    (
                        "d7e00000-0000-4000-8000-000000000092",
                        "Tiệm Trà & Bánh Mùa Thu x SE08 Digital",
                        "FNB",
                        "SIZE_11_50",
                        "https://muathuteabakery.vn",
                        "02439996688",
                        "Quận Hoàn Kiếm, Hà Nội & Quận Hải Châu, Đà Nẵng",
                        "Không gian truyền thông chuỗi cửa hàng trà trái cây thủ công và bánh nướng theo mùa.",
                        "#D97706",
                        "Hương vị thủ công ấm áp mỗi ngày",
                        2020,
                    ),
                ]
                for cw_id, cw_name, cw_ind, cw_size, cw_web, cw_phone, cw_loc, cw_desc, cw_color, cw_tag, cw_year in companion_workspaces:
                    cur.execute(
                        """
                        INSERT INTO workspaces (
                            id, agency_id, name, created_by, timezone_config, settings,
                            industry, company_size, website, phone, location, description,
                            brand_color, logo_url, banner_url, tagline, founded_year,
                            status, created_at, updated_at
                        ) VALUES (
                            %s::uuid, %s::uuid, %s, %s::uuid, 'Asia/Ho_Chi_Minh', '{"approvalMode":"TWO_TIER"}'::jsonb,
                            %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s,
                            'ACTIVE', NOW() - INTERVAL '40 days', NOW() - INTERVAL '1 day'
                        )
                        ON CONFLICT (id) DO UPDATE SET
                            agency_id = EXCLUDED.agency_id,
                            name = EXCLUDED.name,
                            industry = EXCLUDED.industry,
                            company_size = EXCLUDED.company_size,
                            description = EXCLUDED.description,
                            brand_color = EXCLUDED.brand_color,
                            tagline = EXCLUDED.tagline,
                            status = 'ACTIVE',
                            deleted_at = NULL,
                            updated_at = NOW();
                        """,
                        (
                            cw_id,
                            AGENCY_ID,
                            cw_name,
                            owner_id,
                            cw_ind,
                            cw_size,
                            cw_web,
                            cw_phone,
                            cw_loc,
                            cw_desc,
                            cw_color,
                            UNSPLASH_CAMPUS_PHOTOS[1]["url"],
                            UNSPLASH_CAMPUS_PHOTOS[3]["url"],
                            cw_tag,
                            cw_year,
                        ),
                    )
                    cur.execute("DELETE FROM workspace_members WHERE workspace_id = %s::uuid;", (cw_id,))
                    for m_uid, m_role in [(manager_id, "MANAGER"), (creator_id, "CREATOR"), (creator2_id, "CREATOR")]:
                        cur.execute(
                            """
                            INSERT INTO workspace_members (
                                id, workspace_id, user_id, role, added_by, joined_at, is_active, created_at, updated_at
                            ) VALUES (
                                %s::uuid, %s::uuid, %s::uuid, %s::workspace_member_role, %s::uuid,
                                NOW() - INTERVAL '35 days', TRUE, NOW() - INTERVAL '35 days', NOW()
                            );
                            """,
                            (java_name_uuid_from_bytes(f"ws-member:{cw_id}:{m_uid}"), cw_id, m_uid, m_role, owner_id),
                        )

                # 19. Đồng bộ Gói cước PLUS, Doanh thu SePay (SEEPAY), Hóa đơn & Sổ cái AI Credit chuẩn xác 100%
                sepay_merchant = load_default_sepay_merchant()
                for p_code, p_disp, p_price, p_ws, p_mem, p_cli, p_store, p_cred, p_conc, p_ver_ret, p_trash_ret, p_act_ret in [
                    ("PLUS", "Plus Agency", 1990000, 10, 15, 50, 100000000000, 5000, 3, 90, 30, 180),
                    ("ENTERPRISE", "Enterprise Agency", 5990000, 50, 50, 200, 1000000000000, 25000, 10, 365, 90, 365),
                ]:
                    cur.execute(
                        "SELECT id FROM billing_plan_versions WHERE code = %s AND is_sellable = TRUE AND price_monthly IS NOT NULL AND price_monthly > 0 ORDER BY version DESC LIMIT 1;",
                        (p_code,),
                    )
                    if not cur.fetchone():
                        cur.execute(
                            """
                            INSERT INTO billing_plan_versions (
                                id, code, version, display_name, price_monthly, currency,
                                max_active_workspaces, max_internal_members, max_clients,
                                storage_limit_bytes, monthly_ai_credits, max_concurrent_ai_jobs,
                                version_retention_days, trash_retention_days, activity_retention_days, is_sellable
                            ) VALUES (
                                %s::uuid, %s,
                                COALESCE((SELECT MAX(version) FROM billing_plan_versions WHERE code = %s), 0) + 1,
                                %s, %s, 'VND',
                                %s, %s, %s,
                                %s, %s, %s,
                                %s, %s, %s, TRUE
                            );
                            """,
                            (
                                java_name_uuid_from_bytes(f"sellable-plan-ver:{p_code}"),
                                p_code,
                                p_code,
                                p_disp,
                                p_price,
                                p_ws,
                                p_mem,
                                p_cli,
                                p_store,
                                p_cred,
                                p_conc,
                                p_ver_ret,
                                p_trash_ret,
                                p_act_ret,
                            ),
                        )
                cur.execute(
                    "SELECT id, price_monthly, monthly_ai_credits FROM billing_plan_versions WHERE code = 'PLUS' AND is_sellable = TRUE ORDER BY version DESC LIMIT 1;"
                )
                plus_plan = cur.fetchone()
                cur.execute(
                    "SELECT id, price_monthly, monthly_ai_credits FROM billing_plan_versions WHERE code = 'ENTERPRISE' AND is_sellable = TRUE ORDER BY version DESC LIMIT 1;"
                )
                ent_plan = cur.fetchone()

                if plus_plan:
                    plus_ver_id, plus_price, plus_credits = str(plus_plan[0]), int(plus_plan[1] or 1990000), int(plus_plan[2] or 5000)
                    ent_ver_id = str(ent_plan[0]) if ent_plan else plus_ver_id
                    ent_price = int(ent_plan[1] or 5990000) if ent_plan else 5990000

                    # Huỷ các đơn treo cũ trên SE08 để nút Gia hạn/Mua thêm trên /subscription/plans tạo mã VietQR mới ngay lập tức
                    cur.execute(
                        """
                        UPDATE billing_orders
                        SET status = 'EXPIRED', updated_at = NOW()
                        WHERE agency_id = %s::uuid AND status IN ('PENDING_PAYMENT', 'PAID');
                        """,
                        (AGENCY_ID,),
                    )

                    se08_sub_id = java_name_uuid_from_bytes(f"agency-sub:{AGENCY_ID}")
                    cur.execute(
                        """
                        INSERT INTO agency_subscriptions (
                            id, agency_id, plan_version_id, status,
                            current_period_start, current_period_end,
                            migration_state, version, created_at, updated_at
                        ) VALUES (
                            %s::uuid, %s::uuid, %s::uuid, 'ACTIVE',
                            (date_trunc('day', NOW() AT TIME ZONE 'UTC') AT TIME ZONE 'UTC') - INTERVAL '10 days',
                            ((date_trunc('day', NOW() AT TIME ZONE 'UTC') AT TIME ZONE 'UTC') - INTERVAL '10 days') + INTERVAL '1 month',
                            'READY', 1, NOW() - INTERVAL '60 days', NOW()
                        )
                        ON CONFLICT (agency_id) DO UPDATE SET
                            plan_version_id = EXCLUDED.plan_version_id,
                            status = 'ACTIVE',
                            current_period_start = EXCLUDED.current_period_start,
                            current_period_end = EXCLUDED.current_period_end,
                            migration_state = 'READY',
                            updated_at = NOW()
                        RETURNING id, current_period_start, current_period_end;
                        """,
                        (se08_sub_id, AGENCY_ID, plus_ver_id),
                    )
                    sub_row = cur.fetchone()
                    actual_sub_id = str(sub_row[0])
                    p_start = sub_row[1]
                    p_end = sub_row[2]

                    def ensure_current_subscription_period(
                        ag_id: str,
                        sub_id: str,
                        plan_vid: str,
                        ord_id: str,
                        per_start: Any,
                        per_end: Any,
                        fallback_key: str,
                    ) -> str:
                        cur.execute(
                            """
                            SELECT id::text FROM agency_subscription_periods
                            WHERE agency_id = %s::uuid
                            ORDER BY CASE status WHEN 'CURRENT' THEN 0 WHEN 'FUTURE' THEN 1 ELSE 2 END, ends_at DESC;
                            """,
                            (ag_id,),
                        )
                        existing_pids = [r[0] for r in cur.fetchall()]
                        target_pid = existing_pids[0] if existing_pids else java_name_uuid_from_bytes(fallback_key)
                        for old_pid in existing_pids[1:]:
                            cur.execute(
                                """
                                UPDATE agency_subscription_periods
                                SET status = 'ENDED',
                                    starts_at = CASE
                                        WHEN starts_at < %s AND ends_at > %s
                                        THEN (SELECT MIN(starts_at) FROM agency_subscription_periods WHERE agency_id = %s::uuid) - INTERVAL '40 days'
                                        ELSE starts_at
                                    END,
                                    ends_at = CASE
                                        WHEN starts_at < %s AND ends_at > %s
                                        THEN (SELECT MIN(starts_at) FROM agency_subscription_periods WHERE agency_id = %s::uuid) - INTERVAL '10 days'
                                        ELSE ends_at
                                    END
                                WHERE id = %s::uuid;
                                """,
                                (per_end, per_start, ag_id, per_end, per_start, ag_id, old_pid),
                            )
                        cur.execute(
                            """
                            INSERT INTO agency_subscription_periods (
                                id, agency_id, subscription_id, plan_version_id, order_id, starts_at, ends_at, status, created_at
                            ) VALUES (
                                %s::uuid, %s::uuid, %s::uuid, %s::uuid, %s::uuid, %s, %s, 'CURRENT', NOW() - INTERVAL '10 days'
                            )
                            ON CONFLICT (id) DO UPDATE SET
                                subscription_id = EXCLUDED.subscription_id,
                                plan_version_id = EXCLUDED.plan_version_id,
                                order_id = EXCLUDED.order_id,
                                starts_at = EXCLUDED.starts_at,
                                ends_at = EXCLUDED.ends_at,
                                status = 'CURRENT';
                            """,
                            (target_pid, ag_id, sub_id, plan_vid, ord_id, per_start, per_end),
                        )
                        return target_pid

                    def upsert_verified_sepay_receipt(
                        ord_key: str,
                        ag_id: str,
                        payer_uid: str,
                        kind: str,
                        amt: int,
                        p_ver_id: str | None,
                        snap_dict: dict[str, Any],
                        days_ago: int,
                        hours_offset: int = 3,
                        per_start: Any = None,
                        per_end: Any = None,
                    ) -> str:
                        ord_id = java_name_uuid_from_bytes(f"bh-demo-order:{ord_key}")
                        att_id = java_name_uuid_from_bytes(f"bh-demo-attempt:{ord_key}")
                        pay_id = java_name_uuid_from_bytes(f"bh-demo-payment:{ord_key}")
                        ord_code = "BH" + sha256_hex(ord_key)[:20].upper()
                        prov_ref = "FT26320" + sha256_hex("ref:" + ord_key)[:9].upper()
                        cur.execute(
                            """
                            INSERT INTO billing_orders (
                                id, agency_id, payer_user_id, kind, status,
                                idempotency_key, payload_hash, amount, currency,
                                product_snapshot, plan_version_id, period_start, period_end,
                                expires_at, paid_at, fulfilled_at, created_at, updated_at
                            ) VALUES (
                                %s::uuid, %s::uuid, %s::uuid, %s, 'FULFILLED',
                                %s, %s, %s, 'VND',
                                %s::jsonb, %s::uuid, %s, %s,
                                NOW() - (%s || ' days')::interval + INTERVAL '15 minutes',
                                NOW() - (%s || ' days')::interval + (%s || ' hours')::interval,
                                NOW() - (%s || ' days')::interval + (%s || ' hours')::interval,
                                NOW() - (%s || ' days')::interval,
                                NOW() - (%s || ' days')::interval + (%s || ' hours')::interval
                            )
                            ON CONFLICT (id) DO UPDATE SET
                                status = 'FULFILLED',
                                amount = EXCLUDED.amount,
                                product_snapshot = EXCLUDED.product_snapshot,
                                period_start = EXCLUDED.period_start,
                                period_end = EXCLUDED.period_end,
                                paid_at = EXCLUDED.paid_at,
                                fulfilled_at = EXCLUDED.fulfilled_at,
                                updated_at = NOW();
                            """,
                            (
                                ord_id,
                                ag_id,
                                payer_uid,
                                kind,
                                f"idem-{ord_key}",
                                sha256_hex(f"payload:{ord_key}"),
                                amt,
                                json.dumps(snap_dict, ensure_ascii=False),
                                p_ver_id,
                                per_start,
                                per_end,
                                str(days_ago),
                                str(days_ago),
                                str(hours_offset),
                                str(days_ago),
                                str(hours_offset),
                                str(days_ago),
                                str(days_ago),
                                str(hours_offset),
                            ),
                        )
                        cur.execute(
                            """
                            INSERT INTO billing_payment_attempts (
                                id, agency_id, order_id, provider, merchant_account,
                                provider_order_code, payment_link_id, status, created_at, updated_at
                            ) VALUES (
                                %s::uuid, %s::uuid, %s::uuid, 'SEEPAY', %s,
                                %s, %s, 'SUCCEEDED',
                                NOW() - (%s || ' days')::interval,
                                NOW() - (%s || ' days')::interval + (%s || ' hours')::interval
                            )
                            ON CONFLICT (id) DO UPDATE SET
                                merchant_account = EXCLUDED.merchant_account,
                                status = 'SUCCEEDED',
                                updated_at = NOW();
                            """,
                            (
                                att_id,
                                ag_id,
                                ord_id,
                                sepay_merchant,
                                ord_code,
                                f"sepay-qr-{ord_code.lower()}",
                                str(days_ago),
                                str(days_ago),
                                str(hours_offset),
                            ),
                        )
                        cur.execute(
                            """
                            INSERT INTO billing_payments (
                                id, agency_id, attempt_id, provider, merchant_account,
                                provider_reference, amount, currency, paid_at, verification_state, created_at
                            ) VALUES (
                                %s::uuid, %s::uuid, %s::uuid, 'SEEPAY', %s,
                                %s, %s, 'VND',
                                NOW() - (%s || ' days')::interval + (%s || ' hours')::interval,
                                'VERIFIED',
                                NOW() - (%s || ' days')::interval + (%s || ' hours')::interval
                            )
                            ON CONFLICT (id) DO UPDATE SET
                                merchant_account = EXCLUDED.merchant_account,
                                amount = EXCLUDED.amount,
                                paid_at = EXCLUDED.paid_at,
                                verification_state = 'VERIFIED';
                            """,
                            (
                                pay_id,
                                ag_id,
                                att_id,
                                sepay_merchant,
                                prov_ref,
                                amt,
                                str(days_ago),
                                str(hours_offset),
                                str(days_ago),
                                str(hours_offset),
                            ),
                        )
                        return ord_id

                    # 3 hóa đơn thực tế của SE08 Digital Agency (1 Gói Plus + 2 đợt nạp AI Credit)
                    se08_sub_ord = upsert_verified_sepay_receipt(
                        "se08-plus-202611",
                        AGENCY_ID,
                        owner_id,
                        "SUBSCRIPTION",
                        plus_price,
                        plus_ver_id,
                        {"action": "UPGRADE", "planCode": "PLUS", "planVersionId": plus_ver_id, "periodMonths": 1, "monthlyCredits": plus_credits},
                        10,
                        2,
                        p_start,
                        p_end,
                    )
                    se08_topup1_ord = upsert_verified_sepay_receipt(
                        "se08-topup1-202611",
                        AGENCY_ID,
                        owner_id,
                        "CREDIT_TOPUP",
                        1000000,
                        None,
                        {"credits": 5000, "unitPriceVnd": 200},
                        7,
                        4,
                    )
                    se08_topup2_ord = upsert_verified_sepay_receipt(
                        "se08-topup2-202611",
                        AGENCY_ID,
                        owner_id,
                        "CREDIT_TOPUP",
                        300000,
                        None,
                        {"credits": 1500, "unitPriceVnd": 200},
                        2,
                        5,
                    )

                    for ord_f, b_type in [
                        (se08_sub_ord, "SUBSCRIPTION_PERIOD"),
                        (se08_sub_ord, "CREDIT_GRANT"),
                        (se08_topup1_ord, "CREDIT_GRANT"),
                        (se08_topup2_ord, "CREDIT_GRANT"),
                    ]:
                        cur.execute(
                            """
                            INSERT INTO billing_order_fulfillments (id, agency_id, order_id, benefit_type, created_at)
                            VALUES (%s::uuid, %s::uuid, %s::uuid, %s, NOW() - INTERVAL '2 days')
                            ON CONFLICT (order_id, benefit_type) DO NOTHING;
                            """,
                            (java_name_uuid_from_bytes(f"fulfill:{ord_f}:{b_type}"), AGENCY_ID, ord_f, b_type),
                        )

                    se08_sub_period_id = ensure_current_subscription_period(
                        AGENCY_ID,
                        actual_sub_id,
                        plus_ver_id,
                        se08_sub_ord,
                        p_start,
                        p_end,
                        f"sepay-period-nov:{AGENCY_ID}",
                    )

                    # Bổ sung 4 Agency Việt Nam trả phí trong tháng hiện tại để /admin?view=revenue có biểu đồ MRR/ARR & giao dịch đẹp mắt
                    peer_agencies = [
                        ("user2@demo.brandhub.test", "Trần Quốc Bảo", "d7e00000-0000-4000-8000-000000000081", "Sao Khuê Media Agency", "ENTERPRISE", ent_ver_id, ent_price, 12, 600000, 4),
                        ("user3@demo.brandhub.test", "Lê Minh Khuê", "d7e00000-0000-4000-8000-000000000082", "CloudWork Creative Studio", "PLUS", plus_ver_id, plus_price, 8, 400000, 3),
                        ("user4@demo.brandhub.test", "Phạm Hoàng Yến", "d7e00000-0000-4000-8000-000000000083", "Mùa Thu Brand Lab", "PLUS", plus_ver_id, plus_price, 5, 800000, 1),
                        ("user5@demo.brandhub.test", "Đỗ Gia Hưng", "d7e00000-0000-4000-8000-000000000084", "Đông Á Digital Hub", "ENTERPRISE", ent_ver_id, ent_price, 1, 500000, 0),
                    ]
                    for p_email, p_fullname, p_ag_id, p_ag_name, p_code, p_vid, p_amt, sub_days_ago, top_amt, top_days_ago in peer_agencies:
                        cur.execute(
                            """
                            UPDATE users
                            SET full_name = %s, status = 'ACTIVE', is_active = TRUE, last_login_at = NOW() - INTERVAL '3 hours'
                            WHERE email = %s RETURNING id;
                            """,
                            (p_fullname, p_email),
                        )
                        prow = cur.fetchone()
                        if not prow:
                            continue
                        p_uid = str(prow[0])
                        cur.execute(
                            """
                            INSERT INTO agencies (id, name, owner_id, description, category, company_size, status, created_at, updated_at)
                            VALUES (%s::uuid, %s, %s::uuid, 'Đối tác Agency sử dụng nền tảng quản trị truyền thông BrandHub.', 'MARKETING', 'SIZE_11_50', 'ACTIVE', NOW() - INTERVAL '45 days', NOW())
                            ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, owner_id = EXCLUDED.owner_id, status = 'ACTIVE', deleted_at = NULL;
                            """,
                            (p_ag_id, p_ag_name, p_uid),
                        )
                        p_sub_id = java_name_uuid_from_bytes(f"peer-sub:{p_ag_id}")
                        cur.execute(
                            """
                            INSERT INTO agency_subscriptions (
                                id, agency_id, plan_version_id, status, current_period_start, current_period_end, migration_state, version, created_at, updated_at
                            ) VALUES (
                                %s::uuid, %s::uuid, %s::uuid, 'ACTIVE',
                                NOW() - (%s || ' days')::interval,
                                NOW() - (%s || ' days')::interval + INTERVAL '30 days',
                                'READY', 1, NOW() - INTERVAL '30 days', NOW()
                            )
                            ON CONFLICT (agency_id) DO UPDATE SET
                                plan_version_id = EXCLUDED.plan_version_id,
                                status = 'ACTIVE',
                                current_period_start = EXCLUDED.current_period_start,
                                current_period_end = EXCLUDED.current_period_end,
                                migration_state = 'READY',
                                updated_at = NOW()
                            RETURNING id, current_period_start, current_period_end;
                            """,
                            (p_sub_id, p_ag_id, p_vid, str(sub_days_ago), str(sub_days_ago)),
                        )
                        ps_row = cur.fetchone()
                        ps_id, ps_start, ps_end = str(ps_row[0]), ps_row[1], ps_row[2]
                        p_ord = upsert_verified_sepay_receipt(
                            f"peer-sub-{p_ag_id}",
                            p_ag_id,
                            p_uid,
                            "SUBSCRIPTION",
                            p_amt,
                            p_vid,
                            {"action": "UPGRADE", "planCode": p_code, "planVersionId": p_vid, "periodMonths": 1},
                            sub_days_ago,
                            2,
                            ps_start,
                            ps_end,
                        )
                        ensure_current_subscription_period(
                            p_ag_id,
                            ps_id,
                            p_vid,
                            p_ord,
                            ps_start,
                            ps_end,
                            f"peer-period:{p_ag_id}",
                        )
                        upsert_verified_sepay_receipt(
                            f"peer-topup-{p_ag_id}",
                            p_ag_id,
                            p_uid,
                            "CREDIT_TOPUP",
                            top_amt,
                            None,
                            {"credits": top_amt // 200, "unitPriceVnd": 200},
                            top_days_ago,
                            1,
                        )

                    # Đồng bộ credit_grants (tổng khả dụng đúng 8.500 điểm), credit_usage_periods & ai_credit_reservations cho SE08
                    cur.execute(
                        "SELECT id::text FROM credit_grants WHERE period_id = %s::uuid AND source_type = 'PERIOD' LIMIT 1;",
                        (se08_sub_period_id,),
                    )
                    ex_pg = cur.fetchone()
                    grant_period_id = ex_pg[0] if ex_pg else java_name_uuid_from_bytes(f"grant-period:{se08_sub_period_id}")
                    grant_topup1_id = java_name_uuid_from_bytes(f"grant-topup:{se08_topup1_ord}")
                    grant_topup2_id = java_name_uuid_from_bytes(f"grant-topup:{se08_topup2_ord}")
                    keep_grants = [grant_period_id, grant_topup1_id, grant_topup2_id]
                    cur.execute(
                        """
                        UPDATE credit_grants
                        SET expired = expired + available, available = 0
                        WHERE agency_id = %s::uuid AND id <> ALL(%s::uuid[]) AND available > 0;
                        """,
                        (AGENCY_ID, keep_grants),
                    )
                    grant_rows = [
                        (grant_period_id, "PERIOD", f"period:{se08_sub_period_id}", None, se08_sub_period_id, 5000, 4380, 620, p_start, p_end),
                        (grant_topup1_id, "TOPUP", f"topup:{se08_topup1_ord}", se08_topup1_ord, None, 5000, 2620, 2380, p_start + timedelta(days=3), None),
                        (grant_topup2_id, "TOPUP", f"topup:{se08_topup2_ord}", se08_topup2_ord, None, 1500, 1500, 0, p_start + timedelta(days=8), None),
                    ]
                    for g_id, g_src, g_skey, g_oid, g_pid, g_amt, g_avail, g_cons, g_from, g_exp in grant_rows:
                        cur.execute(
                            """
                            INSERT INTO credit_grants (
                                id, agency_id, source_type, source_key, order_id, period_id,
                                amount, available, reserved, consumed, expired, revoked, valid_from, expires_at, created_at
                            ) VALUES (
                                %s::uuid, %s::uuid, %s, %s, %s::uuid, %s::uuid,
                                %s, %s, 0, %s, 0, 0, %s, %s, %s
                            )
                            ON CONFLICT (id) DO UPDATE SET
                                amount = EXCLUDED.amount,
                                available = EXCLUDED.available,
                                reserved = 0,
                                consumed = EXCLUDED.consumed,
                                expired = 0,
                                revoked = 0,
                                valid_from = EXCLUDED.valid_from,
                                expires_at = EXCLUDED.expires_at;
                            """,
                            (g_id, AGENCY_ID, g_src, g_skey, g_oid, g_pid, g_amt, g_avail, g_cons, g_from, g_exp, g_from),
                        )

                    cur.execute(
                        """
                        UPDATE agency_credit_wallets
                        SET available_credits = 8500,
                            reserved_credits = 0,
                            opening_balance_state = 'VERIFIED',
                            updated_at = NOW()
                        WHERE agency_id = %s::uuid;
                        """,
                        (AGENCY_ID,),
                    )

                    usage_period_id = java_name_uuid_from_bytes(f"credit-usage-period:{se08_sub_period_id}")
                    cur.execute(
                        """
                        INSERT INTO credit_usage_periods (id, agency_id, starts_at, ends_at, kind, subscription_period_id)
                        VALUES (%s::uuid, %s::uuid, %s, %s, 'PAID', %s::uuid)
                        ON CONFLICT (agency_id, starts_at, kind) DO UPDATE SET
                            ends_at = EXCLUDED.ends_at,
                            subscription_period_id = EXCLUDED.subscription_period_id
                        RETURNING id;
                        """,
                        (usage_period_id, AGENCY_ID, p_start, p_end, se08_sub_period_id),
                    )
                    actual_usage_period_id = str(cur.fetchone()[0])

                    cur.execute(
                        """
                        INSERT INTO workspace_credit_usage (agency_id, workspace_id, period_id, used, reserved)
                        VALUES (%s::uuid, %s::uuid, %s::uuid, 620, 0)
                        ON CONFLICT (agency_id, workspace_id, period_id) DO UPDATE SET
                            used = 620, reserved = 0;
                        """,
                        (AGENCY_ID, WORKSPACE_ID, actual_usage_period_id),
                    )

                    # Đọc bảng giá hiện hành để ghi nhận lịch sử tiêu dùng AI Credit thực tế của từng thành viên SE08
                    price_map: dict[str, tuple[str, int]] = {}
                    for op_n in ("CONTENT_GENERATE", "AMBASSADOR_GENERATE", "COMMERCIAL_IMAGE", "VIDEO_GENERATE"):
                        cur.execute(
                            "SELECT id, unit_credits FROM ai_credit_operation_prices WHERE operation = %s ORDER BY revision DESC LIMIT 1;",
                            (op_n,),
                        )
                        pr = cur.fetchone()
                        if pr:
                            price_map[op_n] = (str(pr[0]), int(pr[1]))

                    settled_ai_runs = [
                        ("fptu2027-ai-phuoc-cap-w1", creator_id, "CONTENT_GENERATE", 8, 7),
                        ("fptu2027-ai-phuoc-var-w2", creator_id, "CAPTION_VARIANTS", 1, 5),
                        ("fptu2027-ai-phuoc-tag-w2", creator_id, "HASHTAG_GENERATE", 1, 4),
                        ("fptu2027-ai-tuan-img-kv", creator2_id, "COMMERCIAL_IMAGE", 7, 6),
                        ("fptu2027-ai-tuan-vid-reel", creator2_id, "VIDEO_GENERATE", 5, 3),
                        ("fptu2027-ai-an-pr-draft", creator3_id, "CONTENT_GENERATE", 6, 2),
                        ("fptu2027-ai-loc-brief", manager_id, "CONTENT_GENERATE", 6, 8),
                        ("fptu2027-ai-trung-amb", owner_id, "AMBASSADOR_GENERATE", 2, 4),
                    ]
                    total_seeded_used = 0
                    for r_key, r_actor, r_op, r_units, r_days_ago in settled_ai_runs:
                        res_id = java_name_uuid_from_bytes(f"ai-res:{r_key}")
                        if r_op in price_map:
                            pr_id, u_cred = price_map[r_op]
                            r_ver = pr_id
                        else:
                            pr_id, u_cred, r_ver = None, 0, "FREE_V1"
                        amt_cred = u_cred * r_units
                        total_seeded_used += amt_cred
                        cur.execute(
                            """
                            INSERT INTO ai_credit_reservations (
                                id, job_id, agency_id, workspace_id, actor_id, period_id,
                                action, model, rate_version, status,
                                reserved_amount, charged_amount, deadline,
                                created_at, settled_at, request_key, payload_hash,
                                price_id, unit_credits, units, successful_units,
                                execution_state, execution_updated_at
                            ) VALUES (
                                %s::uuid, %s::uuid, %s::uuid, %s::uuid, %s::uuid, %s::uuid,
                                %s, 'gemini-2.5-flash', %s, 'SETTLED',
                                %s, %s, NOW() - (%s || ' days')::interval + INTERVAL '1 day',
                                NOW() - (%s || ' days')::interval,
                                NOW() - (%s || ' days')::interval + INTERVAL '1 minute',
                                %s, %s,
                                %s::uuid, %s, %s, %s,
                                'SUCCEEDED', NOW() - (%s || ' days')::interval + INTERVAL '1 minute'
                            )
                            ON CONFLICT (id) DO UPDATE SET
                                period_id = EXCLUDED.period_id,
                                reserved_amount = EXCLUDED.reserved_amount,
                                charged_amount = EXCLUDED.charged_amount,
                                unit_credits = EXCLUDED.unit_credits,
                                units = EXCLUDED.units,
                                successful_units = EXCLUDED.successful_units,
                                status = 'SETTLED';
                            """,
                            (
                                res_id,
                                res_id,
                                AGENCY_ID,
                                WORKSPACE_ID,
                                r_actor,
                                actual_usage_period_id,
                                r_op,
                                r_ver,
                                amt_cred,
                                amt_cred,
                                str(r_days_ago),
                                str(r_days_ago),
                                str(r_days_ago),
                                r_key,
                                sha256_hex(r_key),
                                pr_id,
                                u_cred,
                                r_units,
                                r_units,
                                str(r_days_ago),
                            ),
                        )
                    cur.execute(
                        "UPDATE workspace_credit_usage SET used = %s WHERE agency_id = %s::uuid AND workspace_id = %s::uuid AND period_id = %s::uuid;",
                        (total_seeded_used, AGENCY_ID, WORKSPACE_ID, actual_usage_period_id),
                    )

        print("[OK] Đã đồng bộ PostgreSQL thành công (SE08 Digital Agency, 7 Gói đa ngành, Chiến dịch ĐH FPT 2027 4 tuần).")
    finally:
        conn.close()
    return resolved_ids


# ==============================================================================
# 5. XÂY DỰNG & ĐỒNG BỘ TOÀN DIỆN DỮ LIỆU MONGODB
# ==============================================================================
ROLE_SUBTASK_DEFS: dict[str, list[tuple[str, str]]] = {
    "POST": [
        ("POST_RESEARCH", "Nghiên cứu / Phỏng vấn"),
        ("POST_CONTENT", "Viết content"),
        ("POST_MEDIA", "Media (quay/chụp/thiết kế)"),
        ("POST_EDITING", "Biên tập"),
        ("POST_PUBLISHING", "Đăng bài"),
    ],
    "SHORT_VIDEO": [
        ("VIDEO_SCRIPT", "Ý tưởng & Kịch bản"),
        ("VIDEO_SHOOT", "Quay"),
        ("VIDEO_EDIT", "Dựng / hậu kỳ"),
        ("VIDEO_PUBLISH", "Caption & Đăng"),
    ],
    "WORKSHOP": [
        ("WORKSHOP_PROGRAM", "Nội dung chương trình"),
        ("WORKSHOP_SPEAKER", "Diễn giả"),
        ("WORKSHOP_LOGISTICS", "Hậu cần"),
        ("WORKSHOP_REGISTRATION", "Đăng ký & truyền thông"),
        ("WORKSHOP_REPORT", "Tổng kết"),
    ],
    "EVENT_PLAN": [
        ("EVENT_AGENDA", "Concept & Agenda"),
        ("EVENT_LOGISTICS", "Hậu cần & Địa điểm"),
        ("EVENT_PROMOTION", "Truyền thông sự kiện"),
        ("EVENT_ONSITE", "Điều phối tại chỗ"),
        ("EVENT_REPORT", "Báo cáo sau sự kiện"),
    ],
    "KOL_BOOKING": [
        ("KOL_SOURCING", "Tìm & đề xuất KOL"),
        ("KOL_NEGOTIATION", "Đàm phán"),
        ("KOL_BRIEF", "Brief cho KOL"),
        ("KOL_CONTENT_REVIEW", "Duyệt nội dung KOL"),
        ("KOL_TRACKING", "Theo dõi & báo cáo"),
    ],
    "EMAIL_NEWSLETTER": [
        ("EMAIL_CONTENT", "Viết nội dung"),
        ("EMAIL_DESIGN", "Thiết kế template"),
        ("EMAIL_SEND", "Danh sách & lịch gửi"),
        ("EMAIL_REPORT", "Báo cáo"),
    ],
    "PRESS_RECOMMENDATION": [
        ("PRESS_MEDIA_LIST", "Lập danh sách báo"),
        ("PRESS_RELEASE", "Viết thông cáo"),
        ("PRESS_PITCHING", "Liên hệ & pitching"),
        ("PRESS_TRACKING", "Theo dõi đưa tin"),
    ],
    "SURVEY": [
        ("SURVEY_DESIGN", "Thiết kế bảng hỏi"),
        ("SURVEY_DISTRIBUTE", "Phân phối & thu thập"),
        ("SURVEY_ANALYSIS", "Phân tích & báo cáo"),
    ],
}


def resolve_visual_url(visual_key: str) -> str:
    if visual_key in FPTU_VISUALS:
        return FPTU_VISUALS[visual_key]["url"]
    if visual_key.startswith("unsplash_"):
        idx = int(visual_key.split("_")[1])
        return UNSPLASH_CAMPUS_PHOTOS[idx]["url"]
    return FPTU_VISUALS["week1_coming_soon"]["url"]


def build_mongo_bundle(resolved_ids: dict[str, str], now: datetime) -> dict[str, Any]:
    owner_id = resolved_ids["OWNER"]
    manager_id = resolved_ids["MANAGER"]
    creator_id = resolved_ids["CREATOR"]
    creator2_id = resolved_ids["CREATOR_2"]
    creator3_id = resolved_ids["CREATOR_3"]
    client_id = resolved_ids["CLIENT"]
    ws_pkg_id = resolved_ids.get("WS_PACKAGE_ID", WS_PACKAGE_ID)

    # 1. Thư mục & Thư viện Tài nguyên (/library): 4 thư mục theo 4 tuần + 11 file ảnh có sẵn preview base64
    folder_defs = [
        ("folder_w1", "d7e00000-0000-4000-8000-000000000851", "01. Tuần 1 - Coming Soon & Học bổng Nguyễn Văn Đạo 2027", "0001"),
        ("folder_w2", "d7e00000-0000-4000-8000-000000000852", "02. Tuần 2 - Phòng Lab Vi mạch, AI & Tiện ích 5 Cơ sở", "0002"),
        ("folder_w3", "d7e00000-0000-4000-8000-000000000853", "03. Tuần 3 - Chuỗi Workshop THPT & FPTU Open Day 2027", "0003"),
        ("folder_w4", "d7e00000-0000-4000-8000-000000000854", "04. Tuần 4 - Tư liệu Báo chí & Thực tập Doanh nghiệp OJT", "0004"),
    ]
    folder_map = {key: fid for key, fid, _, _ in folder_defs}
    material_folders = [
        {
            "_id": fid,
            "scope_type": "WORKSPACE",
            "workspace_id": WORKSPACE_ID,
            "owner_user_id": None,
            "name": fname,
            "normalized_name": fname.lower(),
            "sort_key": skey,
            "parent_folder_id": None,
            "ancestor_ids": [],
            "created_by": creator2_id,
            "created_at": now - timedelta(days=15),
            "updated_at": now - timedelta(days=1),
            "version": 1,
        }
        for _key, fid, fname, skey in folder_defs
    ]

    materials: list[dict[str, Any]] = []
    for idx, (_vkey, vinfo) in enumerate(FPTU_VISUALS.items()):
        data_uri, file_bytes = load_asset_data_uri(vinfo["file"])
        fid = folder_map[vinfo["folder"]]
        materials.append(
            {
                "_id": vinfo["id"],
                "workspace_id": WORKSPACE_ID,
                "name": vinfo["name"],
                "original_name": vinfo["file"],
                "normalized_name": vinfo["name"].lower(),
                "scope_type": "WORKSPACE",
                "folder_id": fid,
                "ancestor_folder_ids": [fid],
                "sort_key": f"{idx + 1:04d}",
                "content_hash": sha256_hex(vinfo["id"]),
                "current_version_number": 1,
                "type": "RETOUCHED",
                "mime_type": "image/jpeg",
                "file_size": file_bytes,
                "url": data_uri,
                "s3_key": f"demo/fptu-2027/{vinfo['file']}",
                "storage_provider": "SYSTEM_S3",
                "status": "READY",
                "media_kind": "IMAGE",
                "purpose": "MATERIAL",
                "visibility": "CLIENT",
                "client_profile_id": CLIENT_PROFILE_ID,
                "access_state": "READY",
                "access_revision": 1,
                "version": 1,
                "draft": False,
                "ai_source": "GEMINI_NANO_BANANA",
                "created_by": creator2_id,
                "updated_by": creator2_id,
                "created_at": now - timedelta(days=14 - idx),
                "updated_at": now - timedelta(hours=12),
            }
        )

    for u_idx, uphoto in enumerate(UNSPLASH_CAMPUS_PHOTOS):
        fid = folder_map[uphoto["folder"]]
        materials.append(
            {
                "_id": uphoto["id"],
                "workspace_id": WORKSPACE_ID,
                "name": uphoto["name"],
                "original_name": uphoto["name"],
                "normalized_name": uphoto["name"].lower(),
                "scope_type": "WORKSPACE",
                "folder_id": fid,
                "ancestor_folder_ids": [fid],
                "sort_key": f"{20 + u_idx:04d}",
                "content_hash": sha256_hex(uphoto["id"]),
                "current_version_number": 1,
                "type": "RAW",
                "mime_type": "image/jpeg",
                "file_size": 248000,
                "url": uphoto["url"],
                "s3_key": f"demo/fptu-2027-ref/{uphoto['name']}",
                "storage_provider": "SYSTEM_S3",
                "status": "READY",
                "media_kind": "IMAGE",
                "purpose": "BRAND_REFERENCE",
                "visibility": "CLIENT",
                "client_profile_id": CLIENT_PROFILE_ID,
                "access_state": "READY",
                "access_revision": 1,
                "version": 1,
                "draft": False,
                "created_by": client_id,
                "updated_by": client_id,
                "created_at": now - timedelta(days=15 - u_idx),
                "updated_at": now - timedelta(days=2),
            }
        )

    # 2. Tài khoản mạng xã hội đã kết nối (4 nền tảng chuẩn: Facebook, Instagram, TikTok, Threads)
    social_accounts = [
        {
            "_id": f"d7e00000-0000-4000-8000-{861 + i:012d}",
            "workspace_id": WORKSPACE_ID,
            "client_id": CLIENT_PROFILE_ID,
            "platform": plat,
            "account_id": acc_code,
            "account_name": acc_name,
            "avatar_url": FPTU_VISUALS["week1_coming_soon"]["url"],
            "encrypted_token": f"demo-token-{plat.lower()}",
            "encrypted_iv": "0123456789abcdef",
            "token_expires_at": now + timedelta(days=55),
            "token_status": "ACTIVE",
            "is_active": True,
            "created_at": now - timedelta(days=30),
            "updated_at": now - timedelta(days=1),
        }
        for i, (plat, acc_code, acc_name) in enumerate(
            [
                ("FACEBOOK", "fptu.admissions.official", "Tuyển sinh Trường Đại học FPT"),
                ("INSTAGRAM", "fpt_university_admissions", "@fptuniversity.tuyensinh"),
                ("TIKTOK", "fptuniversity.official", "@fptu.official (Đại học FPT)"),
                ("THREADS", "fptuniversity.threads", "@fptuniversity.tuyensinh"),
            ]
        )
    ]

    # 3. 20 Công việc (Tasks) + Task Sections + Section Versions + Posts + Publish Logs
    specs = build_4week_plan_specs(now)
    tasks: list[dict[str, Any]] = []
    task_sections: list[dict[str, Any]] = []
    task_section_versions: list[dict[str, Any]] = []
    posts: list[dict[str, Any]] = []
    publish_logs: list[dict[str, Any]] = []

    sample_student_comments = [
        ("Nguyễn Hoàng Nam (THPT Phan Châu Trinh)", "Cho em hỏi điểm học bạ lớp 12 bao nhiêu thì đủ điều kiện nộp hồ sơ xét Học bổng Nguyễn Văn Đạo năm 2027 ạ?"),
        ("Phụ huynh Lê Thu Hà", "Nhà trường cho cô hỏi buổi Workshop Chủ nhật này tại Đà Nẵng phụ huynh đi cùng con vào tham quan phòng Lab và ký túc xá được không?"),
        ("Trần Minh Khôi (2k9 - THPT Chuyên Lê Quý Đôn)", "Mình vừa tham gia buổi trải nghiệm kính VR và cánh tay robot hôm qua, phòng Lab Vi mạch nhìn thực tế rất hiện đại."),
        ("Võ Ngọc Ánh (2k9 - THPT Hoàng Hoa Thám)", "Ngành Quản trị kinh doanh số học kỳ 6 cũng được đi thực tập doanh nghiệp OJT như khối Công nghệ thông tin đúng không ạ?"),
        ("Phạm Gia Huy (THPT Chu Văn An - Hà Nội)", "Khuôn viên Hòa Lạc mùa này xanh quá, hẹn gặp các bạn 2k9 tại Ngày hội FPTU Open Day cuối tuần nhé!"),
        ("Phụ huynh Đặng Quốc Tuấn", "Gia đình rất quan tâm chương trình thực tập 4 đến 8 tháng tại FPT Software từ năm ba, nhờ ban tư vấn gửi thêm lộ trình môn học."),
        ("Lê Gia Hân (THPT Trần Phú)", "Đã nhận được email vé mời QR tham dự Workshop sáng thứ Bảy rồi ạ, nhóm lớp em đăng ký 6 bạn cùng đi."),
        ("Đỗ Minh Nhật (2k9 - THPT Nguyễn Thượng Hiền)", "Cho mình hỏi chuyên ngành Trí tuệ nhân tạo ở cơ sở TP.HCM và Quy Nhơn có học chung khung giáo trình quốc tế không ạ?"),
    ]

    for s in specs:
        w_item_id = s.get("work_item_id")
        t_id = s.get("task_id_override") or campaign_task_id(CAMPAIGN_ID, w_item_id)
        assignee = resolved_ids[s["assignee_key"]]
        due_dt: datetime = s["due"]
        planned_start = due_dt - timedelta(days=3)
        created_dt = now - timedelta(days=15)
        t_status = s["status"]
        is_out_of_scope = w_item_id is None

        sub_status_default = "FINISHED" if t_status == "FINISHED" else ("IN_PROGRESS" if t_status in ("IN_PROGRESS", "IN_REVIEW") else "TODO")
        subtasks = []
        for r_idx, (role_code, role_label) in enumerate(ROLE_SUBTASK_DEFS[s["type"]]):
            # Phân bổ hợp lý giữa Phước (Content), Tuấn (Media/Video/Workshop) và Ân (PR/Email/Survey)
            if role_code in ("POST_MEDIA", "VIDEO_SHOOT", "VIDEO_EDIT", "WORKSHOP_LOGISTICS", "EVENT_LOGISTICS"):
                sub_assignee = creator2_id
            elif role_code.startswith("PRESS_") or role_code.startswith("EMAIL_") or role_code.startswith("SURVEY_"):
                sub_assignee = creator3_id
            else:
                sub_assignee = assignee

            if t_id == TASK_1_ID:
                # Task trình diễn sân khấu: Nghiên cứu, Media, Đăng bài đã chuẩn bị xong; Viết content & Biên tập đang thực hiện
                this_sub_status = "FINISHED" if role_code in ("POST_RESEARCH", "POST_MEDIA", "POST_PUBLISHING") else "IN_PROGRESS"
            else:
                this_sub_status = "FINISHED" if (t_status == "IN_REVIEW" and r_idx < len(ROLE_SUBTASK_DEFS[s["type"]]) - 1) else sub_status_default

            subtasks.append(
                {
                    "id": subtask_id(t_id, role_code),
                    "parentTaskId": t_id,
                    "name": role_label,
                    "assigneeId": sub_assignee,
                    "supervisorOverrideId": None,
                    "dueDate": due_dt,
                    "status": this_sub_status,
                    "plannedStartDate": planned_start,
                    "subtaskRole": role_code,
                }
            )

        started = t_status != "TODO"
        first_started_at = (planned_start + timedelta(hours=2)) if started else None
        first_started_by = assignee if started else None

        type_meta: dict[str, Any] = {
            "acceptanceCriteria": s["criteria"],
            "sortOrder": s["idx"],
            "weekNumber": s["week"],
        }
        if is_out_of_scope:
            type_meta["outOfScope"] = True

        task_doc: dict[str, Any] = {
            "_id": t_id,
            "workspaceId": WORKSPACE_ID,
            "campaignId": CAMPAIGN_ID,
            "campaignWorkItemId": w_item_id,
            "name": s["name"],
            "description": s["description"],
            "type": s["type"],
            "status": t_status,
            "assigneeId": assignee,
            "assignedAt": created_dt + timedelta(hours=1),
            "assignedBy": manager_id,
            "supervisorId": manager_id,
            "initialManager": manager_id,
            "requiresClientApproval": not is_out_of_scope,
            "approvalRound": 1,
            "plannedStartDate": planned_start,
            "dueDate": due_dt,
            "publishDate": due_dt,
            "sourceType": "CAMPAIGN_OUT_OF_SCOPE" if is_out_of_scope else "CAMPAIGN",
            "sourceRefId": None if is_out_of_scope else w_item_id,
            "createdBy": manager_id,
            "createdAt": created_dt,
            "updatedAt": due_dt if t_status == "FINISHED" else now - timedelta(minutes=30),
            "workflowRevision": 0 if t_status == "TODO" else (3 if t_status == "IN_REVIEW" else 2),
            "firstStartedAt": first_started_at,
            "firstStartedBy": first_started_by,
            "inputReferences": [
                {"label": "Cổng thông tin Tuyển sinh Đại học FPT 2027", "url": "https://tuyensinh.fpt.edu.vn"},
            ],
            "subtasks": subtasks,
            "typeMetadata": type_meta,
        }
        if t_status == "IN_REVIEW":
            task_doc["reviewStep"] = "MANAGER"
            task_doc["lastSubmission"] = {
                "round": 1,
                "submittedBy": assignee,
                "submittedAt": now - timedelta(hours=4),
                "closedBy": None,
                "closedAt": None,
                "outcome": None,
            }
        elif t_status == "FINISHED":
            task_doc["lastSubmission"] = {
                "round": 1,
                "submittedBy": assignee,
                "submittedAt": due_dt - timedelta(hours=8),
                "closedBy": manager_id if is_out_of_scope else client_id,
                "closedAt": due_dt - timedelta(hours=2),
                "outcome": "APPROVED",
            }
        tasks.append(task_doc)

        # Khởi tạo dữ liệu Section chi tiết theo đúng chuẩn SectionStore (taskId|sectionKey)
        vis_url = resolve_visual_url(s["visual_key"])
        if t_id == TASK_1_ID:
            # TASK_1_ID: Bố trí sẵn trạng thái lý tưởng cho buổi thuyết trình trực tiếp (B5 -> B11)
            brief_content = {
                "notes": (
                    "1. Nêu bật không khí thực tế từ chuỗi Workshop phổ biến tiện ích học đường ĐH FPT tại các trường THPT.\n"
                    "2. Thông tin chính xác 3 mức Học bổng Nguyễn Văn Đạo năm 2027: 50%, 70% và 100% học phí toàn khóa.\n"
                    "3. Nhấn mạnh lộ trình thực tập doanh nghiệp (On-the-Job Training - OJT) từ học kỳ 6 tại FPT Software và FPT Smart Cloud.\n"
                    "4. Kêu gọi học sinh lớp 12 đăng ký xét tuyển đợt 1 tại https://tuyensinh.fpt.edu.vn."
                ),
                "sources": ["https://tuyensinh.fpt.edu.vn"],
                "materials": [FPTU_VISUALS["week3_thpt_workshop"]["id"]],
            }
            sec_specs = [
                ("POST.BRIEF", "INTERNAL", "INTERNAL_APPROVED", 1, brief_content),
                ("POST.MEDIA", "OUTPUT", "CLIENT_APPROVED", 1, {}),
                ("POST.CHANNELS", "OUTPUT", "CLIENT_APPROVED", 1, {}),
                ("POST.CAPTION", "OUTPUT", "DRAFT", 0, {}),
            ]
            for s_key, vis, s_stat, v_cnt, s_content in sec_specs:
                task_sections.append(
                    {
                        "_id": section_doc_id(t_id, s_key),
                        "workspaceId": WORKSPACE_ID,
                        "taskId": t_id,
                        "sectionKey": s_key,
                        "visibility": vis,
                        "status": s_stat,
                        "revision": 2 if v_cnt > 0 else 1,
                        "versionCount": v_cnt,
                        "content": s_content,
                        "updatedBy": assignee,
                        "updatedAt": now - timedelta(hours=1),
                    }
                )
                if v_cnt > 0:
                    snap_content = (
                        brief_content
                        if s_key == "POST.BRIEF"
                        else (
                            {"media": [{"external_url": vis_url, "media_type": "IMAGE"}]}
                            if s_key == "POST.MEDIA"
                            else {"targetPlatforms": s["platforms"], "scheduledAt": due_dt.strftime("%Y-%m-%dT%H:%M:%SZ")}
                        )
                    )
                    task_section_versions.append(
                        {
                            "_id": section_ver_id(t_id, s_key, 1),
                            "workspaceId": WORKSPACE_ID,
                            "taskId": t_id,
                            "sectionKey": s_key,
                            "versionNo": 1,
                            "content": snap_content,
                            "submittedBy": assignee,
                            "submittedAt": now - timedelta(hours=3),
                        }
                    )
        elif s["type"] == "POST":
            p_sec_stat = (
                "CLIENT_APPROVED"
                if t_status == "FINISHED"
                else ("INTERNAL_APPROVED" if t_status in ("IN_PROGRESS", "IN_REVIEW") else "DRAFT")
            )
            post_sections = [
                (
                    "POST.BRIEF",
                    "INTERNAL",
                    "INTERNAL_APPROVED" if t_status != "TODO" else "DRAFT",
                    {
                        "notes": f"<p>{s['description']}</p><p>Tiêu chí nghiệm thu: {s['criteria']}</p>",
                        "sources": [
                            "https://tuyensinh.fpt.edu.vn",
                            "Quy chế Học bổng Nguyễn Văn Đạo 2027",
                        ],
                        "materials": ["Logo & Bộ nhận diện", "Ảnh thực tế 5 cơ sở ĐH FPT"],
                    },
                ),
                ("POST.CAPTION", "OUTPUT", p_sec_stat, {}),
                ("POST.MEDIA", "OUTPUT", p_sec_stat, {}),
                ("POST.CHANNELS", "OUTPUT", p_sec_stat, {}),
            ]
            for s_key, vis, s_stat, s_content in post_sections:
                task_sections.append(
                    {
                        "_id": section_doc_id(t_id, s_key),
                        "workspaceId": WORKSPACE_ID,
                        "taskId": t_id,
                        "sectionKey": s_key,
                        "visibility": vis,
                        "status": s_stat,
                        "revision": 2 if s_stat != "DRAFT" else 1,
                        "versionCount": 1 if s_stat != "DRAFT" else 0,
                        "content": s_content,
                        "updatedBy": assignee,
                        "updatedAt": now - timedelta(hours=8),
                    }
                )
        elif s["type"] == "SHORT_VIDEO":
            v_sec_stat = (
                "CLIENT_APPROVED"
                if t_status == "FINISHED"
                else ("INTERNAL_APPROVED" if t_status in ("IN_PROGRESS", "IN_REVIEW") else "DRAFT")
            )
            vid_sections = [
                (
                    "VIDEO.SCRIPT",
                    "OUTPUT",
                    v_sec_stat if t_status != "TODO" else "INTERNAL_APPROVED",
                    {
                        "idea": f"<p>{s['description']}</p><p>Nhịp dựng nhanh 45 giây dọc 9:16 bắt mắt học sinh THPT khóa 2k9.</p>",
                        "scenes": [
                            "Cảnh 1 (0-4s): Góc máy flycam cổng Trường Đại học FPT buổi sáng nắng vàng",
                            "Cảnh 2 (4-15s): Sinh viên thực hành trực tiếp tại phòng Lab Vi mạch bán dẫn & AI",
                            "Cảnh 3 (15-28s): Nhịp sống thư viện xanh, sân tập Vovinam và hơn 40 CLB sinh viên",
                            "Cảnh 4 (28-38s): Chia sẻ ngắn về học kỳ thực tập doanh nghiệp OJT từ học kỳ 6",
                            "Cảnh 5 (38-45s): Thông tin Học bổng Nguyễn Văn Đạo 2027 & lời mời đăng ký tại bio",
                        ],
                    },
                ),
                ("VIDEO.SHOOT", "INTERNAL", "INTERNAL_APPROVED", {"rawFootageNote": "Đã quay 4K 60fps tại Campus Đà Nẵng & Hòa Lạc"}),
                ("VIDEO.EDIT", "OUTPUT", v_sec_stat, {}),
                ("VIDEO.CAPTION", "OUTPUT", v_sec_stat, {}),
                ("VIDEO.CHANNELS", "OUTPUT", v_sec_stat, {}),
            ]
            for s_key, vis, s_stat, s_content in vid_sections:
                task_sections.append(
                    {
                        "_id": section_doc_id(t_id, s_key),
                        "workspaceId": WORKSPACE_ID,
                        "taskId": t_id,
                        "sectionKey": s_key,
                        "visibility": vis,
                        "status": s_stat,
                        "revision": 2,
                        "versionCount": 1,
                        "content": s_content,
                        "updatedBy": assignee,
                        "updatedAt": now - timedelta(hours=7),
                    }
                )
        elif s["type"] == "WORKSHOP":
            sec_stat = "CLIENT_APPROVED" if t_status == "FINISHED" else "INTERNAL_APPROVED"
            ws_sections = [
                (
                    "WORKSHOP.PROGRAM",
                    "OUTPUT",
                    {
                        "topic": f"<p><strong>{s['name']}</strong>: Đưa học sinh lớp 12 trực tiếp trải nghiệm hệ sinh thái tiện ích học đường, phòng Lab bán dẫn, AI và tư vấn quy chế Học bổng Nguyễn Văn Đạo 2027.</p>",
                        "agenda": [
                            "08:00 - 08:30: Đón đoàn học sinh lớp 12, phát thẻ đeo cam FPTU và cẩm nang ngành học 2027",
                            "08:30 - 09:15: Phổ biến hệ sinh thái tiện ích 5 cơ sở ĐH FPT (Thư viện, Ký túc xá, Vovinam, 40+ CLB, Học kỳ OJT)",
                            "09:15 - 10:15: Trải nghiệm thực tế kính VR tham quan phòng Lab bán dẫn và điều khiển cánh tay Robotics",
                            "10:15 - 11:00: Hỏi đáp trực tiếp quy chế xét Học bổng Nguyễn Văn Đạo 2027 cùng giảng viên & Đại sứ sinh viên",
                        ],
                        "materials": [
                            "Slide thuyết trình tiện ích 5 cơ sở ĐH FPT",
                            "Cẩm nang Học bổng Nguyễn Văn Đạo 50% - 70% - 100%",
                            "Bộ kính thực tế ảo VR & mô hình cánh tay Robotics",
                        ],
                    },
                ),
                (
                    "WORKSHOP.SPEAKERS",
                    "OUTPUT",
                    {
                        "speakers": [
                            {
                                "name": "TS. Trần Quang Minh",
                                "title": "Trưởng Bộ môn Thiết kế Vi mạch & AI - ĐH FPT",
                                "topic": "Xu hướng nhân lực Bán dẫn, AI và chương trình đào tạo thực chiến",
                                "inviteStatus": "Đã xác nhận",
                            },
                            {
                                "name": "ThS. Lê Thu Phương",
                                "title": "Đại diện Ban Tuyển sinh Đại học FPT",
                                "topic": "Quy chế xét tuyển K23 & Học bổng Nguyễn Văn Đạo năm 2027",
                                "inviteStatus": "Đã xác nhận",
                            },
                            {
                                "name": "Nguyễn Minh Anh (K19)",
                                "title": "Đại sứ Sinh viên vừa hoàn thành kỳ OJT tại FPT Software",
                                "topic": "Trải nghiệm thực tập doanh nghiệp OJT học kỳ 6 và đời sống CLB",
                                "inviteStatus": "Đã xác nhận",
                            },
                        ]
                    },
                ),
                (
                    "WORKSHOP.LOGISTICS",
                    "INTERNAL",
                    {
                        "format": "Offline (Tại địa điểm)",
                        "venue": "Hội trường lớn & Khu vực sảnh trưng bày Robotics Trường Đại học FPT",
                        "venueOrMeetingUrl": "Hội trường lớn & Khu vực sảnh trưng bày Robotics Trường Đại học FPT (5 cơ sở)",
                        "meetingUrl": "https://tuyensinh.fpt.edu.vn/workshop-thpt-2027",
                        "cost": 18500000,
                    },
                ),
                (
                    "WORKSHOP.REGISTRATION",
                    "OUTPUT",
                    {
                        "promotionPlan": "Phối hợp Bí thư Đoàn 18 trường THPT, gửi bản tin Email kèm mã QR check-in và thông báo trên Fanpage Tuyển sinh ĐH FPT."
                    },
                ),
                (
                    "WORKSHOP.REPORT",
                    "OUTPUT",
                    {
                        "registrations": 465 if t_status == "FINISHED" else 390,
                        "registeredCount": 465 if t_status == "FINISHED" else 390,
                        "attendees": 420 if t_status == "FINISHED" else 0,
                        "attendedCount": 420 if t_status == "FINISHED" else 0,
                        "feedback": (
                            "<p>94% học sinh lớp 12 đánh giá phần trải nghiệm thiết bị Lab bán dẫn và tư vấn lộ trình thực tập OJT rất dễ hiểu, thực tế.</p>"
                            if t_status == "FINISHED"
                            else "<p>Đã chốt danh sách 390 học sinh lớp 12 đăng ký trước qua mã QR của Đoàn trường THPT.</p>"
                        ),
                        "photos": [vis_url],
                        "lessons": "<p>Bổ sung thêm 2 bàn tư vấn riêng cho nhóm học sinh hỏi sâu về hồ sơ xét Học bổng Nguyễn Văn Đạo.</p>",
                    },
                ),
            ]
            for s_key, vis, s_content in ws_sections:
                this_stat = (
                    "INTERNAL_APPROVED"
                    if vis == "INTERNAL"
                    else ("DRAFT" if (s_key == "WORKSHOP.REPORT" and t_status != "FINISHED") else sec_stat)
                )
                task_sections.append(
                    {
                        "_id": section_doc_id(t_id, s_key),
                        "workspaceId": WORKSPACE_ID,
                        "taskId": t_id,
                        "sectionKey": s_key,
                        "visibility": vis,
                        "status": this_stat,
                        "revision": 2,
                        "versionCount": 1,
                        "content": s_content,
                        "updatedBy": assignee,
                        "updatedAt": now - timedelta(hours=6),
                    }
                )
        elif s["type"] == "EVENT_PLAN":
            ev_sections = [
                (
                    "EVENT.AGENDA",
                    "OUTPUT",
                    "INTERNAL_APPROVED",
                    True,
                    {
                        "concept": "<p><strong>FPTU Open Day 2027: Một ngày làm sinh viên công nghệ toàn cầu.</strong> Học sinh THPT và phụ huynh trực tiếp tham quan 12 trạm tiện ích thực tế tại khuôn viên trường.</p>",
                        "goal": "<p>Đón 1.500 học sinh THPT và phụ huynh tham quan trực tiếp khuôn viên trường, phòng Lab bán dẫn và tư vấn tại chỗ 400 bộ hồ sơ xét tuyển sớm khóa K23.</p>",
                        "goals": "Đón 1.500 học sinh THPT và phụ huynh tham quan trực tiếp khuôn viên trường, phòng Lab bán dẫn và tư vấn tại chỗ 400 bộ hồ sơ xét tuyển sớm khóa K23.",
                        "datetimeVenue": f"07:30 - 16:30 ngày {due_dt.strftime('%d/%m/%Y')} tại Quảng trường trung tâm, Thư viện xanh & Khu Lab Công nghệ Trường Đại học FPT",
                        "plannedTime": due_dt.strftime("%Y-%m-%d 07:30 - 16:30"),
                        "plannedVenue": "Quảng trường trung tâm, Thư viện xanh & Khu Lab Công nghệ Trường Đại học FPT",
                        "agenda": [
                            {"time": "07:30 - 08:15", "item": "Đón đoàn xe học sinh THPT & đồng diễn Vovinam chào mừng tại sân trường", "owner": "Nguyễn Minh Tuấn & Đội Tình nguyện"},
                            {"time": "08:15 - 09:30", "item": "Phiên chia sẻ tại sân khấu chính cùng Ban Tuyển sinh, giảng viên AI & khách mời công nghệ", "owner": "Nguyễn Thành Lộc & Ban Tuyển sinh"},
                            {"time": "09:30 - 11:30", "item": "Tham quan theo lộ trình 12 trạm tiện ích (Lab Vi mạch, Thư viện xanh, Ký túc xá, Phố 40+ CLB)", "owner": "Đại sứ Sinh viên K19"},
                            {"time": "13:30 - 16:00", "item": "Tư vấn chuyên sâu 1-1 cùng phụ huynh về học phí, Học bổng Nguyễn Văn Đạo & học kỳ OJT", "owner": "Ban Tuyển sinh Đại học FPT"},
                        ],
                    },
                ),
                (
                    "EVENT.LOGISTICS",
                    "INTERNAL",
                    "INTERNAL_APPROVED",
                    False,
                    {
                        "venue": "Sân khấu ngoài trời & 12 phòng chức năng khuôn viên Trường Đại học FPT",
                        "vendors": [
                            {"name": "Công ty Sự kiện Ánh Sáng Việt", "category": "Âm thanh, ánh sáng & màn LED P3 ngoài trời", "costVnd": 22000000, "contact": "0905 312 688"},
                            {"name": "Đội xe Hợp đồng Đất Quảng", "category": "08 tuyến xe 45 chỗ đưa đón học sinh THPT", "costVnd": 15000000, "contact": "0903 558 119"},
                            {"name": "Xưởng In Nhanh Hòa Hải", "category": "In 1.800 thẻ đeo cam, standee & sổ tay ngành học", "costVnd": 8000000, "contact": "0914 220 445"},
                        ],
                        "totalBudget": 45000000,
                        "checklist": [
                            "Backdrop & Standee",
                            "Âm thanh & Ánh sáng",
                            "Bàn Check-in & QR",
                            "Quà tặng / Goodie bag",
                            "Đội ngũ quay chụp sự kiện",
                            "Teabreak / Catering",
                        ],
                    },
                ),
                (
                    "EVENT.PROMOTION",
                    "OUTPUT",
                    "INTERNAL_APPROVED",
                    True,
                    {
                        "plan": "<p>Phủ sóng truyền thông 3 giai đoạn: (1) Chuỗi bài đếm ngược kèm bản đồ 08 tuyến xe đón trên Facebook, Instagram, TikTok, Threads; (2) Cập nhật hình ảnh & Reels trực tiếp tại 12 trạm trải nghiệm; (3) Tuyến bài tổng kết trên báo điện tử.</p>",
                        "guests": [
                            {"name": "Reviewer Duy Luân (Schannel)", "org": "Khách mời giao lưu công nghệ & AI", "inviteStatus": "Đã xác nhận"},
                            {"name": "Ban Giám hiệu & Bí thư Đoàn 18 trường THPT", "org": "Các trường THPT đối tác", "inviteStatus": "Đã xác nhận"},
                            {"name": "Phóng viên Ban Giáo dục VnExpress & Thanh Niên", "org": "Cơ quan báo chí", "inviteStatus": "Đã mời"},
                        ],
                    },
                ),
                (
                    "EVENT.RUNSHEET",
                    "INTERNAL",
                    "INTERNAL_APPROVED",
                    False,
                    {
                        "runsheet": [
                            {"time": "06:30", "task": "Tổng duyệt âm thanh sân khấu, kiểm tra đường truyền Wifi khu vực quét QR check-in", "owner": "Nguyễn Minh Tuấn"},
                            {"time": "07:30", "task": "Đón 08 đoàn xe THPT tại cổng chính, phân luồng theo màu dây đeo", "owner": "Đội Tình nguyện viên K19"},
                            {"time": "09:30", "task": "Điều phối luân chuyển các nhóm học sinh qua Lab Vi mạch, Thư viện và Ký túc xá", "owner": "Nguyễn Thành Lộc"},
                            {"time": "14:00", "task": "Hỗ trợ phụ huynh tra cứu quy chế Học bổng Nguyễn Văn Đạo tại 10 bàn tư vấn", "owner": "Hà Văn Ân & Ban Tuyển sinh"},
                        ],
                        "staffing": "<p>Tổng nhân sự vận hành: 04 thành viên SE08 Digital điều phối truyền thông tại chỗ, 15 cán bộ tư vấn tuyển sinh ĐH FPT và 35 sinh viên tình nguyện dẫn đoàn.</p>",
                    },
                ),
                (
                    "EVENT.REPORT",
                    "OUTPUT",
                    "DRAFT",
                    False,
                    {
                        "result": "<p>Khung báo cáo nghiệm thu sẵn sàng cập nhật ngay sau khi kết thúc Ngày hội FPTU Open Day 2027 (chỉ tiêu 1.500 người tham dự và 400 hồ sơ tư vấn sâu).</p>",
                        "attendeeCount": 1500,
                        "lessons": "<p>Ưu tiên phân luồng giờ tham quan phòng Lab bán dẫn theo từng ca 25 phút để học sinh có nhiều thời gian tương tác thiết bị.</p>",
                    },
                ),
            ]
            for s_key, vis, s_stat, wait_client, s_content in ev_sections:
                sec_doc: dict[str, Any] = {
                    "_id": section_doc_id(t_id, s_key),
                    "workspaceId": WORKSPACE_ID,
                    "taskId": t_id,
                    "sectionKey": s_key,
                    "visibility": vis,
                    "status": s_stat,
                    "revision": 2,
                    "versionCount": 1 if s_stat != "DRAFT" else 0,
                    "content": s_content,
                    "updatedBy": assignee,
                    "updatedAt": now - timedelta(hours=5),
                }
                if wait_client:
                    sec_doc["clientPendingSince"] = now - timedelta(hours=5)
                task_sections.append(sec_doc)
        elif s["type"] == "KOL_BOOKING":
            kol_stat = "CLIENT_APPROVED" if t_status == "FINISHED" else "INTERNAL_APPROVED"
            is_student_koc = "Đại sứ Sinh viên" in s["name"]
            kol_sections = [
                (
                    "KOL.SHORTLIST",
                    "OUTPUT",
                    kol_stat,
                    {
                        "shortlist": [
                            {
                                "name": "Duy Luân Dễ Thương (Schannel / Tech Creator)",
                                "channel": "TikTok",
                                "link": "https://www.tiktok.com/@duyluandethuong",
                                "followers": 680000,
                                "engagementRate": "6.8%",
                                "reason": "Giọng kể chuyện công nghệ gần gũi, rất uy tín với học sinh THPT yêu thích ngành AI & Kỹ thuật phần mềm.",
                            },
                            {
                                "name": "Nguyễn Minh Anh - Đại sứ Sinh viên FPTU K19",
                                "channel": "TikTok",
                                "link": "https://www.tiktok.com/@fptu.official",
                                "followers": 95000,
                                "engagementRate": "9.4%",
                                "reason": "Sinh viên thực tế vừa hoàn thành học kỳ thực tập OJT tại FPT Software, chia sẻ chân thực về đời sống Campus.",
                            },
                            {
                                "name": "Meichan (Education & Study Vlog)",
                                "channel": "Instagram",
                                "link": "https://www.instagram.com/umm.meichan",
                                "followers": 520000,
                                "engagementRate": "5.9%",
                                "reason": "Truyền cảm hứng học ngoại ngữ và trải nghiệm môi trường đại học quốc tế năng động.",
                            },
                        ]
                    },
                ),
                (
                    "KOL.DEAL",
                    "INTERNAL",
                    "INTERNAL_APPROVED",
                    {
                        "kol": (
                            "Nguyễn Minh Anh - Đại sứ Sinh viên FPTU K19 (TikTok)"
                            if is_student_koc
                            else "Duy Luân Dễ Thương (Schannel / Tech Creator) (TikTok)"
                        ),
                        "priceVnd": 8000000 if is_student_koc else 28000000,
                        "deliverables": [
                            "1 Video TikTok 60 giây quay thực tế tại Campus ĐH FPT",
                            "1 Bài đăng Facebook kèm bộ 4 ảnh trải nghiệm phòng Lab",
                            "1 Instagram Reel & chia sẻ đồng thời trên Threads",
                            "Gắn đường dẫn đăng ký FPTU Open Day 2027 trên phần mô tả 14 ngày",
                        ],
                        "terms": "<p>Thanh toán 50% khi chốt kịch bản, 50% sau 5 ngày nghiệm thu chỉ số. Cho phép Ban Tuyển sinh ĐH FPT sử dụng video làm tư liệu truyền thông tuyển sinh khóa K23 trong 6 tháng.</p>",
                    },
                ),
                (
                    "KOL.BRIEF",
                    "OUTPUT",
                    kol_stat,
                    {
                        "keyMessage": "<p>Trải nghiệm mắt thấy tai nghe môi trường học tập công nghệ tại Trường Đại học FPT: từ phòng Lab Vi mạch bán dẫn, thư viện xanh, võ thuật Vovinam đến học kỳ thực tập doanh nghiệp OJT từ học kỳ 6.</p>",
                        "dos": [
                            "Quay trực tiếp tại phòng Lab Vi mạch, thư viện xanh và sảnh sự kiện Open Day",
                            "Nhắc chính xác 3 mức Học bổng Nguyễn Văn Đạo 50%, 70%, 100%",
                            "Gắn đầy đủ bộ hashtag chiến dịch và gắn thẻ trang Tuyển sinh Trường Đại học FPT",
                        ],
                        "donts": [
                            "Không dùng cụm từ cam kết tuyển thẳng trái quy chế tuyển sinh",
                            "Không so sánh hạ thấp các trường đại học khác",
                            "Không sử dụng nhạc nền vướng bản quyền thương mại",
                        ],
                        "requiredHashtags": ["#DaiHocFPT", "#TuyenSinhFPTU2027", "#FPTUOpenDay", "#HocKyOJT"],
                        "postDeadline": due_dt.strftime("%Y-%m-%d"),
                    },
                ),
                (
                    "KOL.DRAFT",
                    "OUTPUT",
                    kol_stat if t_status == "FINISHED" else "SUBMITTED",
                    {
                        "draftCaption": "<p>Một ngày đột nhập phòng Lab Thiết kế Vi mạch bán dẫn & AI tại Trường Đại học FPT cùng các bạn học sinh 2k9! Ấn tượng nhất là sinh viên năm ba đã bước vào học kỳ thực tập OJT làm dự án thật tại FPT Software.</p>",
                        "draftMedia": [vis_url],
                        "reviewNote": "<p>Góc quay sáng rõ, lời thoại tự nhiên, nêu chính xác thông tin học kỳ OJT và Học bổng Nguyễn Văn Đạo 2027.</p>",
                    },
                ),
                (
                    "KOL.REPORT",
                    "OUTPUT",
                    "CLIENT_APPROVED" if t_status == "FINISHED" else "DRAFT",
                    {
                        "postLink": "https://www.tiktok.com/@fptu.official/video/202700309",
                        "postedAt": due_dt.strftime("%Y-%m-%dT19:30"),
                        "views": 186400 if t_status == "FINISHED" else 64200,
                        "likes": 14800 if t_status == "FINISHED" else 5300,
                        "comments": 620 if t_status == "FINISHED" else 215,
                        "shares": 1240 if t_status == "FINISHED" else 410,
                    },
                ),
            ]
            for s_key, vis, s_stat, s_content in kol_sections:
                task_sections.append(
                    {
                        "_id": section_doc_id(t_id, s_key),
                        "workspaceId": WORKSPACE_ID,
                        "taskId": t_id,
                        "sectionKey": s_key,
                        "visibility": vis,
                        "status": s_stat,
                        "revision": 2,
                        "versionCount": 1 if s_stat != "DRAFT" else 0,
                        "content": s_content,
                        "updatedBy": assignee,
                        "updatedAt": now - timedelta(hours=4),
                    }
                )
        elif s["type"] == "EMAIL_NEWSLETTER":
            mail_blocks = [
                {"id": "eb1", "type": "header", "props": {}},
                {"id": "eb2", "type": "heading", "props": {"text": "Vé mời tham dự Chuỗi Workshop Trải nghiệm Tiện ích Đại học FPT 2027", "align": "left"}},
                {"id": "eb3", "type": "paragraph", "props": {"text": "Chào bạn, Ban Tuyển sinh Trường Đại học FPT trân trọng gửi lịch trình trải nghiệm thực tế phòng Lab bán dẫn, kính VR, Robotics và tư vấn Học bổng Nguyễn Văn Đạo (50%, 70%, 100%) dành cho học sinh lớp 12."}},
                {"id": "eb4", "type": "cta_button", "props": {"label": "Nhận Mã QR Check-in Sự kiện", "urlType": "campaign", "customUrl": ""}},
                {"id": "eb5", "type": "footer", "props": {}},
            ]
            em_sections = [
                (
                    "EMAIL.CONTENT",
                    "OUTPUT",
                    "CLIENT_APPROVED",
                    {
                        "subject": "[Đại học FPT 2027] Vé mời tham dự Workshop trải nghiệm Phòng Lab & Tiện ích Campus",
                        "preheader": "Xác nhận chỗ ngồi, mã QR check-in và cẩm nang Học bổng Nguyễn Văn Đạo 2027",
                        "blocks": mail_blocks,
                    },
                ),
                (
                    "EMAIL.DESIGN",
                    "OUTPUT",
                    "CLIENT_APPROVED",
                    {
                        "subject": "[Đại học FPT 2027] Vé mời tham dự Workshop trải nghiệm Phòng Lab & Tiện ích Campus",
                        "preheader": "Thiết kế chuẩn nhận diện cam #EA580C của Trường Đại học FPT",
                        "blocks": mail_blocks,
                    },
                ),
                (
                    "EMAIL.AUDIENCE",
                    "OUTPUT",
                    "CLIENT_APPROVED",
                    {
                        "recipientGroupIds": ["d7e00000-0000-4000-8000-000000000871"],
                        "scheduledAt": (now - timedelta(days=3)).strftime("%Y-%m-%dT08:30"),
                        "batchId": "d7e00000-0000-4000-8000-000000000891",
                    },
                ),
                (
                    "EMAIL.REPORT",
                    "OUTPUT",
                    "CLIENT_APPROVED",
                    {
                        "note": "<p>100% thư mời kèm mã QR check-in đã gửi thành công tới danh sách học sinh lớp 12 đăng ký đợt 1, không phát sinh lỗi trả thư.</p>",
                        "comment": "100% thư mời kèm mã QR check-in đã gửi thành công tới danh sách học sinh lớp 12 đăng ký đợt 1.",
                    },
                ),
            ]
            for s_key, vis, s_stat, s_content in em_sections:
                task_sections.append(
                    {
                        "_id": section_doc_id(t_id, s_key),
                        "workspaceId": WORKSPACE_ID,
                        "taskId": t_id,
                        "sectionKey": s_key,
                        "visibility": vis,
                        "status": s_stat,
                        "revision": 2,
                        "versionCount": 1,
                        "content": s_content,
                        "updatedBy": assignee,
                        "updatedAt": now - timedelta(days=2),
                    }
                )
        elif s["type"] == "SURVEY":
            sv_sections = [
                ("SURVEY.FORM", "OUTPUT", "CLIENT_APPROVED", {}),
                (
                    "SURVEY.DISTRIBUTION",
                    "OUTPUT",
                    "CLIENT_APPROVED",
                    {
                        "publicLink": "http://localhost:5173/public/surveys/khao-sat-chon-nganh-fptu-2027",
                        "channels": "Facebook, Instagram, TikTok, Threads, Email, QR tại sự kiện",
                        "closeAt": (now + timedelta(days=7)).strftime("%Y-%m-%dT23:59"),
                        "targetResponses": 500,
                    },
                ),
                (
                    "SURVEY.REPORT",
                    "OUTPUT",
                    "CLIENT_APPROVED",
                    {
                        "insight": "<p>Nhóm ngành Thiết kế Vi mạch bán dẫn & Trí tuệ nhân tạo (AI) cùng Kỹ thuật phần mềm chiếm tỷ trọng quan tâm cao nhất trong nhóm học sinh lớp 12 tham gia khảo sát.</p>",
                        "conclusion": "<p>Học sinh và phụ huynh đặc biệt muốn trải nghiệm trực tiếp phòng Lab công nghệ và nghe giải đáp cụ thể về điều kiện xét Học bổng Nguyễn Văn Đạo cũng như học kỳ thực tập OJT.</p>",
                        "recommendations": "<p>Tăng thời lượng thực hành tại trạm Lab Bán dẫn và bố trí thêm bàn tư vấn học bổng chuyên sâu tại Ngày hội FPTU Open Day 2027.</p>",
                    },
                ),
            ]
            for s_key, vis, s_stat, s_content in sv_sections:
                task_sections.append(
                    {
                        "_id": section_doc_id(t_id, s_key),
                        "workspaceId": WORKSPACE_ID,
                        "taskId": t_id,
                        "sectionKey": s_key,
                        "visibility": vis,
                        "status": s_stat,
                        "revision": 2,
                        "versionCount": 1,
                        "content": s_content,
                        "updatedBy": assignee,
                        "updatedAt": now - timedelta(days=1),
                    }
                )
        elif s["type"] == "PRESS_RECOMMENDATION":
            pr_stat = "SUBMITTED" if t_status == "IN_REVIEW" else "INTERNAL_APPROVED"
            pr_body_html = (
                "<p>Trong khuôn khổ chiến dịch tư vấn tuyển sinh khóa K23 năm 2027, Trường Đại học FPT đã tổ chức chuỗi Workshop trải nghiệm tiện ích học đường "
                "và Ngày hội Open Day dành cho học sinh THPT tại nhiều tỉnh thành. Học sinh lớp 12 được trực tiếp quan sát quy trình kiểm thử mạch bán dẫn, "
                "tương tác với mô hình Robotics, tham quan thư viện xanh, sân rèn luyện Vovinam và trao đổi cùng các sinh viên khóa trên vừa hoàn thành học kỳ thực tập "
                "doanh nghiệp (On-the-Job Training - OJT) tại FPT Software.</p>"
                "<p>Bên cạnh trải nghiệm không gian học tập tại 5 cơ sở Hà Nội, Đà Nẵng, Quy Nhơn, TP.HCM và Cần Thơ, Ban Tuyển sinh nhà trường cũng công bố chi tiết "
                "chương trình Học bổng Nguyễn Văn Đạo năm 2027 với các mức hỗ trợ 50%, 70% và 100% học phí toàn khóa học.</p>"
            )
            pr_sections = [
                (
                    "PRESS.MEDIA_LIST",
                    "INTERNAL",
                    "INTERNAL_APPROVED",
                    {
                        "outlets": [
                            {
                                "outlet": "VnExpress",
                                "section": "Chuyên mục Giáo dục - Tuyển sinh",
                                "journalist": "Nhà báo Thu Tâm",
                                "contact": "giaoduc@vnexpress.net | 024 7300 8899",
                                "note": "Ưu tiên bài ảnh thực tế học sinh THPT trải nghiệm Lab bán dẫn",
                            },
                            {
                                "outlet": "Báo Thanh Niên",
                                "section": "Ban Giáo dục & Hướng nghiệp",
                                "journalist": "Nhà báo Đăng Nguyên",
                                "contact": "bangiaoduc@thanhnien.vn | 028 3930 9988",
                                "note": "Khai thác sâu góc nhìn học kỳ thực tập doanh nghiệp OJT học kỳ 6",
                            },
                            {
                                "outlet": "Báo Điện tử Dân Trí",
                                "section": "Giáo dục - Khuyến học",
                                "journalist": "Nhà báo Hoàng Hạnh",
                                "contact": "giaoduc@dantri.com.vn | 024 3736 6491",
                                "note": "Đưa tin tổng hợp Học bổng Nguyễn Văn Đạo năm 2027",
                            },
                        ]
                    },
                ),
                (
                    "PRESS.RELEASE",
                    "OUTPUT",
                    pr_stat,
                    {
                        "title": "Đại học FPT đưa trải nghiệm phòng Lab bán dẫn, AI và hệ sinh thái tiện ích học đường đến hơn 2.000 học sinh THPT",
                        "sapo": "<p>Thông qua chuỗi Workshop hướng nghiệp thực tế mùa tuyển sinh 2027, học sinh lớp 12 trực tiếp thực hành trên thiết bị công nghệ và tìm hiểu lộ trình thực tập doanh nghiệp OJT từ năm thứ ba.</p>",
                        "content": pr_body_html,
                        "body": pr_body_html,
                        "attachments": [FPTU_VISUALS["week4_ojt_press"]["id"]],
                    },
                ),
                (
                    "PRESS.CONTACT_LOG",
                    "INTERNAL",
                    "INTERNAL_APPROVED",
                    {
                        "log": [
                            {
                                "date": (now - timedelta(days=3)).strftime("%Y-%m-%d"),
                                "outlet": "VnExpress Giáo dục",
                                "contact": "Nhà báo Thu Tâm",
                                "channel": "Email",
                                "result": "Đồng ý đăng",
                            },
                            {
                                "date": (now - timedelta(days=2)).strftime("%Y-%m-%d"),
                                "outlet": "Báo Thanh Niên",
                                "contact": "Nhà báo Đăng Nguyên",
                                "channel": "Điện thoại",
                                "result": "Đang trao đổi",
                            },
                            {
                                "date": (now - timedelta(days=1)).strftime("%Y-%m-%d"),
                                "outlet": "Báo Điện tử Dân Trí",
                                "contact": "Nhà báo Hoàng Hạnh",
                                "channel": "Email",
                                "result": "Đã gửi",
                            },
                        ]
                    },
                ),
                (
                    "PRESS.COVERAGE",
                    "OUTPUT",
                    "DRAFT",
                    {
                        "coverage": [
                            {
                                "outlet": "VnExpress Giáo dục (dự kiến lên bài đầu Tuần 4)",
                                "link": "https://vnexpress.net/giao-duc",
                                "publishedAt": due_dt.strftime("%Y-%m-%d"),
                            }
                        ]
                    },
                ),
            ]
            for s_key, vis, s_stat, s_content in pr_sections:
                task_sections.append(
                    {
                        "_id": section_doc_id(t_id, s_key),
                        "workspaceId": WORKSPACE_ID,
                        "taskId": t_id,
                        "sectionKey": s_key,
                        "visibility": vis,
                        "status": s_stat,
                        "revision": 2,
                        "versionCount": 1 if s_stat != "DRAFT" else 0,
                        "content": s_content,
                        "updatedBy": assignee,
                        "updatedAt": now - timedelta(hours=3),
                    }
                )

        # Tạo bản ghi PostDocument cho tất cả các công việc POST và SHORT_VIDEO
        if s["type"] in ("POST", "SHORT_VIDEO") and "post_status" in s:
            p_id = POST_1_ID if t_id == TASK_1_ID else f"d7e00000-0000-4000-8000-{400 + s['idx']:012d}"
            p_status = s["post_status"]
            platforms = s["platforms"]
            media_type = "VIDEO" if s["type"] == "SHORT_VIDEO" else "IMAGE"
            media_items = [
                {
                    "material_id": None,
                    "s3_key": None,
                    "external_url": vis_url,
                    "media_type": media_type,
                }
            ]
            if s["type"] == "POST" and s["idx"] in (1, 60):
                media_items.append(
                    {
                        "material_id": None,
                        "s3_key": None,
                        "external_url": UNSPLASH_CAMPUS_PHOTOS[1]["url"],
                        "media_type": "IMAGE",
                    }
                )

            post_doc: dict[str, Any] = {
                "_id": p_id,
                "workspace_id": WORKSPACE_ID,
                "task_id": t_id,
                "created_by": assignee,
                "content_text": s.get("caption", ""),
                "hashtags": s.get("hashtags", []),
                "media": media_items,
                "target_platforms": platforms,
                "platform": platforms[0],
                "ai_generated": s["idx"] in (1, 4, 19),
                "status": p_status,
                "content_version": 1,
                "created_at": created_dt,
                "updated_at": due_dt if p_status == "PUBLISHED" else now - timedelta(minutes=20),
            }

            if p_status == "PUBLISHED":
                m = s["metrics"]
                pub_at = due_dt + timedelta(minutes=5)
                post_doc["published_at"] = pub_at
                post_doc["platform_post_id"] = f"fptu2027_{s['idx']}"
                post_doc["platform_post_url"] = f"https://www.facebook.com/university.fpt.edu.vn/posts/202700{s['idx']}"
                post_doc["reaction_count"] = m["reactions"]
                post_doc["comment_count"] = m["comments"]
                post_doc["share_count"] = m["shares"]
                post_doc["impression_count"] = m["impressions"]
                post_doc["reach_count"] = m["reach"]
                post_doc["click_count"] = m["clicks"]
                post_doc["saved_count"] = m["saves"]
                post_doc["reaction_breakdown"] = {
                    "LIKE": int(m["reactions"] * 0.62),
                    "LOVE": int(m["reactions"] * 0.28),
                    "WOW": int(m["reactions"] * 0.10),
                }
                post_doc["engagement_updated_at"] = now - timedelta(hours=2)
                cmt_offset = s["idx"] % len(sample_student_comments)
                rotated_cmts = (sample_student_comments[cmt_offset:] + sample_student_comments[:cmt_offset])[:3]
                built_cmts = [
                    {
                        "id": f"cmt_{s['idx']}_{ci}",
                        "authorName": author,
                        "authorAvatar": UNSPLASH_CAMPUS_PHOTOS[0]["url"],
                        "content": ctext,
                        "commentedAt": pub_at + timedelta(hours=ci + 1),
                    }
                    for ci, (author, ctext) in enumerate(rotated_cmts)
                ]
                post_doc["cached_comments"] = built_cmts
                platform_data = {}
                share_weights = [0.45, 0.25, 0.20, 0.10]
                for pi, plat in enumerate(platforms):
                    w = share_weights[pi] if pi < len(share_weights) else 0.15
                    platform_data[plat] = {
                        "platform": plat,
                        "platformPostId": f"{plat.lower()}_2027_{s['idx']}",
                        "platformPostUrl": f"https://tuyensinh.fpt.edu.vn/social/{plat.lower()}/{s['idx']}",
                        "status": "PUBLISHED",
                        "publishedAt": pub_at,
                        "reactionCount": max(25, int(m["reactions"] * w)),
                        "commentCount": max(5, int(m["comments"] * w)),
                        "shareCount": max(3, int(m["shares"] * w)),
                        "impressionCount": max(500, int(m["impressions"] * w)),
                        "reachCount": max(350, int(m["reach"] * w)),
                        "clickCount": max(20, int(m["clicks"] * w)),
                        "savedCount": max(5, int(m["saves"] * w)),
                        "engagementUpdatedAt": now - timedelta(hours=2),
                        "cachedComments": built_cmts,
                    }
                    publish_logs.append(
                        {
                            "_id": f"d7e00000-0000-4000-8000-{9200 + s['idx'] * 10 + pi:012d}",
                            "workspace_id": WORKSPACE_ID,
                            "post_id": p_id,
                            "platform": plat,
                            "result": "SUCCESS",
                            "retry_count": 0,
                            "created_at": pub_at,
                        }
                    )
                post_doc["platform_data"] = platform_data
            elif p_status == "SCHEDULED":
                sched_dt = (now + timedelta(days=s.get("scheduled_offset_days", 6))).replace(hour=9, minute=0, second=0, microsecond=0)
                post_doc["scheduled_at"] = sched_dt
            else:
                post_doc["scheduled_at"] = due_dt

            posts.append(post_doc)

    # 3a-extra. Năm bản tin cập nhật nhanh trải đều các ngày gần nhất (-8, -5, -2, -1, 0) để biểu đồ 7 ngày trên /dashboard & /posts/dashboard
    # luôn liên tục không có ngày trống, có đủ 4 định dạng (Ảnh, Nhiều ảnh, Thước phim, Văn bản) và đủ đóng góp của cả 3 Creator SE08.
    daily_pulse_specs = [
        (
            81,
            creator3_id,
            now - timedelta(days=8),
            15,
            ["THREADS", "FACEBOOK"],
            [],
            (
                "GÓC GIẢI ĐÁP HỌC BỔNG NGUYỄN VĂN ĐẠO 2027 CHO 2K9\n\n"
                "Tổng hợp 5 câu hỏi được học sinh lớp 12 gửi về nhiều nhất trong tuần đầu mở cổng thông tin khóa K23: "
                "cách chuẩn bị minh chứng giải thưởng học sinh giỏi, lịch thi đánh giá năng lực học bổng và quyền lợi duy trì các mức 50%, 70%, 100% suốt khóa học.\n\n"
                "Xem hướng dẫn chi tiết tại: https://tuyensinh.fpt.edu.vn"
            ),
            ["#HocBongNguyenVanDao", "#GiaiDapTuyenSinh", "#DaiHocFPT", "#2k9"],
            {"reactions": 1180, "comments": 246, "shares": 132, "impressions": 31400, "reach": 24800, "clicks": 1790, "saves": 420},
        ),
        (
            82,
            creator3_id,
            now - timedelta(days=5),
            11,
            ["FACEBOOK", "INSTAGRAM", "THREADS"],
            [
                {"material_id": None, "s3_key": None, "external_url": FPTU_VISUALS["week2_semiconductor"]["url"], "media_type": "IMAGE"},
                {"material_id": None, "s3_key": None, "external_url": FPTU_VISUALS["week2_software_biz"]["url"], "media_type": "IMAGE"},
            ],
            (
                "SO SÁNH NHANH LỘ TRÌNH HỌC TẬP KHỐI VI MẠCH BÁN DẪN, AI & KỸ THUẬT PHẦN MỀM TẠI ĐH FPT\n\n"
                "Bộ infographic tóm tắt các học phần nền tảng, trang thiết bị phòng Lab thực hành và vị trí thực tập doanh nghiệp OJT từ học kỳ 6 "
                "để các bạn học sinh lớp 12 dễ dàng đối chiếu với sở trường Toán, Lý, Tin của bản thân."
            ),
            ["#ViMachBanDan", "#KyThuatPhanMem", "#ChonNganh2027", "#FPTUniversity"],
            {"reactions": 2340, "comments": 318, "shares": 295, "impressions": 62800, "reach": 49200, "clicks": 3120, "saves": 890},
        ),
        (
            83,
            creator2_id,
            now - timedelta(days=2),
            14,
            ["FACEBOOK", "INSTAGRAM", "TIKTOK", "THREADS"],
            [
                {"material_id": None, "s3_key": None, "external_url": FPTU_VISUALS["week3_thpt_workshop"]["url"], "media_type": "IMAGE"},
            ],
            (
                "HẬU TRƯỜNG CHUẨN BỊ 12 TRẠM TRẢI NGHIỆM VR & ROBOTICS ĐÓN HỌC SINH THPT TUẦN 3\n\n"
                "Đội ngũ giảng viên và sinh viên các câu lạc bộ công nghệ Trường Đại học FPT đã hoàn tất lắp đặt khu vực thử nghiệm bo mạch FPGA, "
                "kính thực tế ảo tham quan 5 cơ sở và bàn tư vấn hồ sơ Học bổng Nguyễn Văn Đạo năm 2027."
            ),
            ["#WorkshopTHPT2027", "#PhongLabFPTU", "#TraiNghiemCongNghe", "#DaiHocFPT"],
            {"reactions": 3150, "comments": 392, "shares": 348, "impressions": 79400, "reach": 63500, "clicks": 3860, "saves": 940},
        ),
        (
            84,
            creator_id,
            now - timedelta(days=1),
            20,
            ["FACEBOOK", "INSTAGRAM", "TIKTOK", "THREADS"],
            [
                {"material_id": None, "s3_key": None, "external_url": FPTU_VISUALS["week3_thpt_workshop"]["url"], "media_type": "IMAGE"},
                {"material_id": None, "s3_key": None, "external_url": FPTU_VISUALS["week3_openday_kol"]["url"], "media_type": "IMAGE"},
            ],
            (
                "HƠN 420 HỌC SINH LỚP 12 KHU VỰC MIỀN TRUNG HÀO HỨNG TRẢI NGHIỆM WORKSHOP TIỆN ÍCH HỌC ĐƯỜNG ĐH FPT\n\n"
                "Những khoảnh khắc rạng rỡ tại buổi Workshop đợt 1 hôm nay: từ trạm điều khiển cánh tay Robotics, tham quan thư viện xanh, "
                "sân tập Vovinam đến phần giải đáp trực tiếp về kỳ thực tập OJT tại FPT Software.\n\n"
                "Đăng ký tham dự đợt tiếp theo & Ngày hội FPTU Open Day 2027 tại: https://tuyensinh.fpt.edu.vn"
            ),
            ["#WorkshopTHPT2027", "#FPTUOpenDay", "#DaiHocFPT", "#TuyenSinhFPTU2027"],
            {"reactions": 3860, "comments": 465, "shares": 512, "impressions": 98600, "reach": 79200, "clicks": 4680, "saves": 1150},
        ),
        (
            85,
            creator3_id,
            now,
            8,
            ["FACEBOOK", "THREADS", "INSTAGRAM"],
            [
                {"material_id": None, "s3_key": None, "external_url": FPTU_VISUALS["week3_openday_kol"]["url"], "media_type": "IMAGE"},
            ],
            (
                "CẬP NHẬT SÁNG NAY: MỞ BỔ SUNG ĐĂNG KÝ XE BUÝT ĐƯA ĐÓN HỌC SINH THPT DỰ NGÀY HỘI FPTU OPEN DAY 2027\n\n"
                "Để thuận tiện cho học sinh lớp 12 và quý phụ huynh đến tham quan trực tiếp khuôn viên trường, phòng Lab bán dẫn và ký túc xá nội trú, "
                "Ban Tuyển sinh Đại học FPT bố trí các tuyến xe đón miễn phí tại điểm hẹn trung tâm.\n\n"
                "Xác nhận điểm đón ngay tại: https://tuyensinh.fpt.edu.vn"
            ),
            ["#FPTUOpenDay2027", "#DaiHocFPT", "#TuyenSinh2027", "#2k9ChonNganh"],
            {"reactions": 2480, "comments": 312, "shares": 284, "impressions": 64200, "reach": 51400, "clicks": 3540, "saves": 760},
        ),
    ]
    for dp_idx, dp_author, dp_day, dp_hour, dp_plats, dp_media, dp_text, dp_tags, dp_m in daily_pulse_specs:
        dp_id = f"d7e00000-0000-4000-8000-{400 + dp_idx:012d}"
        dp_pub = dp_day.replace(hour=min(dp_hour, max(0, now.hour - 1)) if dp_day.date() == now.date() else dp_hour, minute=15, second=0, microsecond=0)
        if dp_pub > now:
            dp_pub = now - timedelta(minutes=35)
        c_off = dp_idx % len(sample_student_comments)
        dp_cmts = (sample_student_comments[c_off:] + sample_student_comments[:c_off])[:3]
        dp_built_cmts = [
            {
                "id": f"cmt_{dp_idx}_{ci}",
                "authorName": author,
                "authorAvatar": UNSPLASH_CAMPUS_PHOTOS[0]["url"],
                "content": ctext,
                "commentedAt": dp_pub + timedelta(minutes=20 * (ci + 1)),
            }
            for ci, (author, ctext) in enumerate(dp_cmts)
        ]
        dp_plat_data = {}
        for pi, plat in enumerate(dp_plats):
            w = [0.5, 0.3, 0.12, 0.08][pi] if pi < 4 else 0.15
            dp_plat_data[plat] = {
                "platform": plat,
                "platformPostId": f"{plat.lower()}_2027_{dp_idx}",
                "platformPostUrl": f"https://tuyensinh.fpt.edu.vn/social/{plat.lower()}/{dp_idx}",
                "status": "PUBLISHED",
                "publishedAt": dp_pub,
                "reactionCount": max(30, int(dp_m["reactions"] * w)),
                "commentCount": max(8, int(dp_m["comments"] * w)),
                "shareCount": max(5, int(dp_m["shares"] * w)),
                "impressionCount": max(800, int(dp_m["impressions"] * w)),
                "reachCount": max(500, int(dp_m["reach"] * w)),
                "clickCount": max(25, int(dp_m["clicks"] * w)),
                "savedCount": max(10, int(dp_m["saves"] * w)),
                "engagementUpdatedAt": now - timedelta(minutes=25),
                "cachedComments": dp_built_cmts,
            }
            publish_logs.append(
                {
                    "_id": f"d7e00000-0000-4000-8000-{9200 + dp_idx * 10 + pi:012d}",
                    "workspace_id": WORKSPACE_ID,
                    "post_id": dp_id,
                    "platform": plat,
                    "result": "SUCCESS",
                    "retry_count": 0,
                    "created_at": dp_pub,
                }
            )
        posts.append(
            {
                "_id": dp_id,
                "workspace_id": WORKSPACE_ID,
                "task_id": None,
                "created_by": dp_author,
                "content_text": dp_text,
                "hashtags": dp_tags,
                "media": dp_media,
                "target_platforms": dp_plats,
                "platform": dp_plats[0],
                "ai_generated": dp_idx in (82, 84),
                "status": "PUBLISHED",
                "content_version": 1,
                "created_at": dp_pub - timedelta(hours=3),
                "updated_at": dp_pub,
                "published_at": dp_pub,
                "platform_post_id": f"fptu2027_{dp_idx}",
                "platform_post_url": f"https://www.facebook.com/university.fpt.edu.vn/posts/202700{dp_idx}",
                "reaction_count": dp_m["reactions"],
                "comment_count": dp_m["comments"],
                "share_count": dp_m["shares"],
                "impression_count": dp_m["impressions"],
                "reach_count": dp_m["reach"],
                "click_count": dp_m["clicks"],
                "saved_count": dp_m["saves"],
                "reaction_breakdown": {
                    "LIKE": int(dp_m["reactions"] * 0.60),
                    "LOVE": int(dp_m["reactions"] * 0.30),
                    "WOW": int(dp_m["reactions"] * 0.10),
                },
                "engagement_updated_at": now - timedelta(minutes=25),
                "cached_comments": dp_built_cmts,
                "platform_data": dp_plat_data,
            }
        )

    # 3b. Ba bài đăng đang chờ trong Hàng đợi Kiểm duyệt Admin (FR 3.10.4) khớp với content_moderation_reviews
    admin_mod_posts = [
        (
            "d7e000000000000000000191",
            "PENDING_APPROVAL",
            "Cam kết tuyển thẳng 100% không cần xét học bạ, đóng phí giữ chỗ nhận ngay học bổng toàn phần!",
        ),
        (
            "d7e000000000000000000192",
            "APPROVED",
            "Thông báo quy chế xét cấp Học bổng Nguyễn Văn Đạo năm 2027 mức 50%, 70%, 100% học phí tại 5 cơ sở.",
        ),
        (
            "d7e000000000000000000193",
            "REJECTED",
            "Tất cả các trường khác đều dạy lý thuyết lỗi thời, bằng cấp vô giá trị!",
        ),
    ]
    post_versions: list[dict[str, Any]] = []
    for mp_id, mp_status, mp_text in admin_mod_posts:
        posts.append(
            {
                "_id": mp_id,
                "workspace_id": WORKSPACE_ID,
                "created_by": creator_id,
                "content_text": mp_text,
                "hashtags": ["#TuyenSinhFPTU2027"],
                "media": [],
                "target_platforms": ["FACEBOOK"],
                "platform": "FACEBOOK",
                "ai_generated": False,
                "status": mp_status,
                "content_version": 1,
                "seed_tag": "fptu-2027-mod",
                "created_at": now - timedelta(days=2),
                "updated_at": now - timedelta(days=1),
            }
        )
        post_versions.append(
            {
                "_id": f"{mp_id}:1",
                "post_id": mp_id,
                "version": 1,
                "workspace_id": WORKSPACE_ID,
                "created_by": creator_id,
                "content_hash": sha256_hex(mp_text),
                "captured_at": now - timedelta(days=2),
                "content_text": mp_text,
                "hashtags": ["#TuyenSinhFPTU2027"],
                "media": [],
                "target_platforms": ["FACEBOOK"],
                "seed_tag": "fptu-2027-mod",
            }
        )

    # 4. Biểu mẫu Khảo sát Học sinh THPT & 12 phản hồi thực tế (surveys & survey_responses)
    survey_doc = {
        "_id": SURVEY_DOC_ID,
        "workspaceId": WORKSPACE_ID,
        "taskId": SURVEY_TASK_ID,
        "publicToken": "khao-sat-chon-nganh-fptu-2027",
        "formName": "Khảo sát nguyện vọng ngành học & trải nghiệm tiện ích Đại học FPT 2027",
        "title": "Khảo sát Nhu cầu Tìm hiểu Ngành học & Chuỗi Workshop Trải nghiệm Đại học FPT 2027",
        "description": "Khảo sát nhanh 2 phút giúp Ban Tuyển sinh Đại học FPT chuẩn bị nội dung tư vấn học bổng và trải nghiệm phòng Lab sát nhất với mối quan tâm của các bạn học sinh lớp 12.",
        "bannerUrl": FPTU_VISUALS["week3_thpt_workshop"]["url"],
        "status": "PUBLISHED",
        "questions": [
            {
                "id": "q1_major",
                "type": "MULTIPLE_CHOICE",
                "label": "Nhóm chuyên ngành nào tại Trường Đại học FPT bạn đang quan tâm nhất cho kỳ tuyển sinh năm 2027?",
                "options": [
                    "Thiết kế Vi mạch bán dẫn & Trí tuệ nhân tạo (AI)",
                    "Kỹ thuật phần mềm & An toàn thông tin",
                    "Quản trị kinh doanh số & Thương mại điện tử",
                    "Truyền thông đa phương tiện & Thiết kế Mỹ thuật số",
                    "Ngôn ngữ Anh - Nhật - Hàn - Trung thương mại",
                ],
                "required": True,
            },
            {
                "id": "q2_campus",
                "type": "MULTIPLE_CHOICE",
                "label": "Bạn dự định đăng ký học tập tại cơ sở nào trong 5 cơ sở của Trường Đại học FPT?",
                "options": ["Hà Nội (Hòa Lạc)", "Đà Nẵng (FPT City)", "Quy Nhơn (An Phú Thịnh)", "TP.HCM (Khu Công nghệ cao)", "Cần Thơ (Ninh Kiều)"],
                "required": True,
            },
            {
                "id": "q3_utilities",
                "type": "CHECKBOX",
                "label": "Bạn muốn trực tiếp trải nghiệm tiện ích nào nhất khi tham dự buổi Workshop & Open Day của trường?",
                "options": [
                    "Phòng Lab Thiết kế Vi mạch bán dẫn, VR & Robotics",
                    "Thư viện xanh và không gian tự học nhóm",
                    "Ký túc xá nội trú và tuyến xe buýt học đường",
                    "Sân tập Vovinam và hơn 40 CLB sinh viên",
                    "Bàn tư vấn hồ sơ Học bổng Nguyễn Văn Đạo & học kỳ OJT",
                ],
                "required": True,
            },
            {
                "id": "q4_question",
                "type": "LONG_TEXT",
                "label": "Câu hỏi cụ thể bạn hoặc gia đình muốn giảng viên Đại học FPT giải đáp tại buổi Workshop là gì?",
                "required": False,
            },
        ],
        "createdAt": now - timedelta(days=6),
        "updatedAt": now - timedelta(days=2),
    }

    sample_survey_entries = [
        ("Thiết kế Vi mạch bán dẫn & Trí tuệ nhân tạo (AI)", "Đà Nẵng (FPT City)", ["Phòng Lab Thiết kế Vi mạch bán dẫn, VR & Robotics", "Bàn tư vấn hồ sơ Học bổng Nguyễn Văn Đạo & học kỳ OJT"], "Em muốn hỏi điều kiện điểm Toán - Lý lớp 12 để thi Học bổng Nguyễn Văn Đạo mức 70% ạ."),
        ("Kỹ thuật phần mềm & An toàn thông tin", "Hà Nội (Hòa Lạc)", ["Phòng Lab Thiết kế Vi mạch bán dẫn, VR & Robotics", "Ký túc xá nội trú và tuyến xe buýt học đường"], "Cho em hỏi sinh viên năm nhất ở Hòa Lạc đăng ký phòng ký túc xá 4 người như thế nào?"),
        ("Quản trị kinh doanh số & Thương mại điện tử", "TP.HCM (Khu Công nghệ cao)", ["Thư viện xanh và không gian tự học nhóm", "Sân tập Vovinam và hơn 40 CLB sinh viên"], "Ngành Kinh doanh số kỳ thực tập OJT có được làm tại các công ty truyền thông đối tác không ạ?"),
        ("Thiết kế Vi mạch bán dẫn & Trí tuệ nhân tạo (AI)", "Hà Nội (Hòa Lạc)", ["Phòng Lab Thiết kế Vi mạch bán dẫn, VR & Robotics", "Bàn tư vấn hồ sơ Học bổng Nguyễn Văn Đạo & học kỳ OJT"], "Em đạt giải Nhì Tin học cấp Tỉnh lớp 12 thì nộp hồ sơ xét học bổng thẳng cần giấy tờ gì?"),
        ("Truyền thông đa phương tiện & Thiết kế Mỹ thuật số", "Đà Nẵng (FPT City)", ["Thư viện xanh và không gian tự học nhóm", "Sân tập Vovinam và hơn 40 CLB sinh viên"], "Em rất muốn xem studio dựng phim và CLB truyền thông của anh chị sinh viên FPTU Đà Nẵng."),
        ("Kỹ thuật phần mềm & An toàn thông tin", "Cần Thơ (Ninh Kiều)", ["Phòng Lab Thiết kế Vi mạch bán dẫn, VR & Robotics", "Ký túc xá nội trú và tuyến xe buýt học đường"], "Phụ huynh muốn tìm hiểu chi tiết lộ trình học tiếng Anh dự bị cho tân sinh viên K23."),
        ("Thiết kế Vi mạch bán dẫn & Trí tuệ nhân tạo (AI)", "Quy Nhơn (An Phú Thịnh)", ["Phòng Lab Thiết kế Vi mạch bán dẫn, VR & Robotics", "Thư viện xanh và không gian tự học nhóm"], "Cơ sở Quy Nhơn chuyên sâu về AI có những dự án thực tập nào từ năm ba ạ?"),
        ("Ngôn ngữ Anh - Nhật - Hàn - Trung thương mại", "TP.HCM (Khu Công nghệ cao)", ["Sân tập Vovinam và hơn 40 CLB sinh viên", "Bàn tư vấn hồ sơ Học bổng Nguyễn Văn Đạo & học kỳ OJT"], "Cho em hỏi chương trình trao đổi học kỳ nước ngoài tại Nhật Bản đối với ngành Ngôn ngữ Nhật."),
        ("Thiết kế Vi mạch bán dẫn & Trí tuệ nhân tạo (AI)", "TP.HCM (Khu Công nghệ cao)", ["Phòng Lab Thiết kế Vi mạch bán dẫn, VR & Robotics", "Bàn tư vấn hồ sơ Học bổng Nguyễn Văn Đạo & học kỳ OJT"], "Em học chuyên Lý tại TP.HCM muốn đăng ký tham quan phòng thực hành mạch số vào sáng Chủ nhật."),
        ("Kỹ thuật phần mềm & An toàn thông tin", "Đà Nẵng (FPT City)", ["Phòng Lab Thiết kế Vi mạch bán dẫn, VR & Robotics", "Sân tập Vovinam và hơn 40 CLB sinh viên"], "Em muốn hỏi lịch sinh hoạt CLB lập trình thi đấu và đội tuyển An toàn thông tin của trường ạ."),
        ("Quản trị kinh doanh số & Thương mại điện tử", "Hà Nội (Hòa Lạc)", ["Thư viện xanh và không gian tự học nhóm", "Ký túc xá nội trú và tuyến xe buýt học đường"], "Nhà ở nội thành Hà Nội thì bắt tuyến xe buýt nào lên cơ sở Hòa Lạc vào dịp Open Day ạ?"),
        ("Truyền thông đa phương tiện & Thiết kế Mỹ thuật số", "TP.HCM (Khu Công nghệ cao)", ["Thư viện xanh và không gian tự học nhóm", "Sân tập Vovinam và hơn 40 CLB sinh viên"], "Ngành Thiết kế Mỹ thuật số có xét học bổng năng khiếu cho học sinh có dự án sáng tạo cá nhân không ạ?"),
        ("Thiết kế Vi mạch bán dẫn & Trí tuệ nhân tạo (AI)", "Đà Nẵng (FPT City)", ["Phòng Lab Thiết kế Vi mạch bán dẫn, VR & Robotics", "Ký túc xá nội trú và tuyến xe buýt học đường"], "Gia đình ở Quảng Ngãi muốn đăng ký nội trú trọn năm đầu tiên cho cháu tại FPT City Đà Nẵng."),
        ("Kỹ thuật phần mềm & An toàn thông tin", "Quy Nhơn (An Phú Thịnh)", ["Phòng Lab Thiết kế Vi mạch bán dẫn, VR & Robotics", "Bàn tư vấn hồ sơ Học bổng Nguyễn Văn Đạo & học kỳ OJT"], "Cho em hỏi hạn chót nộp hồ sơ xét Học bổng Nguyễn Văn Đạo đợt 1 năm 2027 tại cơ sở Quy Nhơn."),
        ("Ngôn ngữ Anh - Nhật - Hàn - Trung thương mại", "Hà Nội (Hòa Lạc)", ["Thư viện xanh và không gian tự học nhóm", "Bàn tư vấn hồ sơ Học bổng Nguyễn Văn Đạo & học kỳ OJT"], "Em có chứng chỉ IELTS 7.0 thì được miễn những học phần tiếng Anh nào trong năm đầu tiên ạ?"),
        ("Kỹ thuật phần mềm & An toàn thông tin", "Cần Thơ (Ninh Kiều)", ["Sân tập Vovinam và hơn 40 CLB sinh viên", "Ký túc xá nội trú và tuyến xe buýt học đường"], "Các anh chị khóa trên cho em hỏi kinh nghiệm chuẩn bị phỏng vấn thực tập OJT học kỳ 6 với ạ."),
    ]
    survey_responses = [
        {
            "_id": f"d7e00000-0000-4000-8000-{811 + idx:012d}",
            "surveyId": SURVEY_DOC_ID,
            "taskId": SURVEY_TASK_ID,
            "submittedAt": now - timedelta(days=5 - (idx % 4), hours=idx * 2),
            "answers": [
                {"questionId": "q1_major", "value": maj, "selectedOptions": [maj]},
                {"questionId": "q2_campus", "value": camp, "selectedOptions": [camp]},
                {"questionId": "q3_utilities", "value": ", ".join(utils), "selectedOptions": utils},
                {"questionId": "q4_question", "value": qtxt, "selectedOptions": []},
            ],
        }
        for idx, (maj, camp, utils, qtxt) in enumerate(sample_survey_entries)
    ]

    # 5. Yêu cầu nội dung từ Ban Tuyển sinh Đại học FPT gửi SE08 Digital Agency (/requests)
    content_requests = [
        {
            "_id": "d7e00000-0000-4000-8000-000000000831",
            "workspaceId": WORKSPACE_ID,
            "requestedBy": client_id,
            "title": "Bổ sung khảo sát nguyện vọng ngành học của học sinh lớp 12 trước buổi Workshop Tuần 3",
            "description": "Đề nghị nhóm SE08 thiết kế biểu mẫu khảo sát ngắn để thu thập câu hỏi của học sinh THPT về ngành Vi mạch, AI và tiện ích nội trú trước ngày diễn ra Workshop.",
            "type": "SURVEY",
            "dueDate": now - timedelta(days=2),
            "status": "ACCEPTED",
            "version": 1,
            "generatedTaskId": SURVEY_TASK_ID,
            "reviewedBy": manager_id,
            "reviewedAt": now - timedelta(days=6),
            "decisionNote": "Đã tiếp nhận và phân công Hà Văn Ân triển khai biểu mẫu khảo sát gắn trực tiếp vào chiến dịch.",
            "decidedBy": manager_id,
            "decidedAt": now - timedelta(days=6),
            "createdAt": now - timedelta(days=7),
            "updatedAt": now - timedelta(days=6),
            "targetPlatforms": [],
            "history": [],
        },
        {
            "_id": "d7e00000-0000-4000-8000-000000000832",
            "workspaceId": WORKSPACE_ID,
            "requestedBy": client_id,
            "title": "Cập nhật thông tin tuyến xe buýt đón học sinh THPT dự Ngày hội FPTU Open Day 2027",
            "description": "Nhờ nhóm SE08 bổ sung bài thông báo lộ trình 08 điểm đón xe miễn phí dành cho học sinh lớp 12 và phụ huynh tham dự Ngày hội Open Day cuối tuần này.",
            "type": "POST",
            "dueDate": now + timedelta(days=2),
            "status": "PENDING",
            "version": 1,
            "createdAt": now - timedelta(hours=5),
            "updatedAt": now - timedelta(hours=5),
            "targetPlatforms": ["FACEBOOK", "INSTAGRAM", "THREADS"],
            "history": [],
        },
    ]

    # 6. Hồ sơ Thương hiệu & Kho tri thức AI (brand_profiles & knowledge_documents cho GraphRAG + Compliance)
    brand_profile = {
        "_id": "d7e00000-0000-4000-8000-000000000840",
        "workspace_id": WORKSPACE_ID,
        "brand_name": "Trường Đại học FPT (FPT University) - Tuyển sinh 2027",
        "industry": "Giáo dục Đại học & Đào tạo Công nghệ (Thiết kế Vi mạch bán dẫn, AI, Kỹ thuật phần mềm, Kinh tế số)",
        "tone_of_voice": "Rõ ràng, hiện đại, truyền cảm hứng cho học sinh THPT và minh bạch số liệu học bổng, thực tập doanh nghiệp OJT cho phụ huynh.",
        "target_audience": "Học sinh lớp 12 (khóa 2k9) và phụ huynh trên toàn quốc tìm hiểu kỳ tuyển sinh đại học năm 2027.",
        "key_messages": [
            "Đào tạo tại 5 cơ sở hiện đại: Hà Nội, Đà Nẵng, Quy Nhơn, TP.HCM và Cần Thơ.",
            "Chương trình Học bổng Nguyễn Văn Đạo năm 2027 hỗ trợ 50%, 70% và 100% học phí toàn khóa.",
            "100% sinh viên tham gia học kỳ thực tập tại doanh nghiệp (On-the-Job Training - OJT) từ học kỳ 6.",
            "Hệ sinh thái tiện ích học đường toàn diện: phòng Lab bán dẫn & AI, thư viện xanh, ký túc xá, Vovinam và hơn 40 CLB sinh viên.",
        ],
        "updated_at": now,
    }

    knowledge_documents = [
        {
            "_id": "d7e00000-0000-4000-8000-000000000841",
            "workspace_id": WORKSPACE_ID,
            "client_id": CLIENT_PROFILE_ID,
            "title": "Quy chế Tuyển sinh Khóa K23 & Học bổng Nguyễn Văn Đạo Năm 2027",
            "content": (
                "Năm 2027, Trường Đại học FPT tuyển sinh khóa K23 tại 5 cơ sở: Hà Nội (Khu Công nghệ cao Hòa Lạc), Đà Nẵng (Khu đô thị FPT City), "
                "Quy Nhơn (Khu đô thị mới An Phú Thịnh), TP.HCM (Khu Công nghệ cao TP. Thủ Đức) và Cần Thơ (Quận Ninh Kiều). "
                "Chương trình Học bổng Nguyễn Văn Đạo năm 2027 gồm các mức 50%, 70% và 100% học phí toàn khóa học dành cho học sinh THPT có thành tích "
                "học tập xuất sắc, đạt giải kỳ thi học sinh giỏi hoặc đạt điểm cao tại kỳ thi học bổng của trường. Cổng đăng ký chính thức: https://tuyensinh.fpt.edu.vn."
            ),
            "created_at": now - timedelta(days=15),
            "updated_at": now - timedelta(days=2),
        },
        {
            "_id": "d7e00000-0000-4000-8000-000000000842",
            "workspace_id": WORKSPACE_ID,
            "client_id": CLIENT_PROFILE_ID,
            "title": "Đào tạo Ngành Thiết kế Vi mạch Bán dẫn, Trí tuệ Nhân tạo & Học kỳ Doanh nghiệp OJT",
            "content": (
                "Sinh viên các chuyên ngành Thiết kế Vi mạch bán dẫn, Trí tuệ nhân tạo (AI), Kỹ thuật phần mềm, An toàn thông tin và Quản trị kinh doanh số "
                "học tập theo giáo trình chuẩn quốc tế, chú trọng tiếng Anh và ngoại ngữ thứ hai. Từ học kỳ 6, sinh viên bước vào học kỳ thực tập thực tế "
                "tại doanh nghiệp (On-the-Job Training - OJT) kéo dài 4 đến 8 tháng tại FPT Software, FPT Semiconductor, FPT Smart Cloud và mạng lưới doanh nghiệp đối tác."
            ),
            "created_at": now - timedelta(days=14),
            "updated_at": now - timedelta(days=2),
        },
        {
            "_id": "d7e00000-0000-4000-8000-000000000843",
            "workspace_id": WORKSPACE_ID,
            "client_id": CLIENT_PROFILE_ID,
            "title": "Hệ sinh thái Tiện ích Campus & Chuỗi Workshop Hướng nghiệp THPT 2027",
            "content": (
                "Khuôn viên Trường Đại học FPT tích hợp thư viện xanh nhiều tầng, phòng Lab thực hành chuyên sâu, ký túc xá nội trú, sân rèn luyện võ thuật "
                "Vovinam và hơn 40 câu lạc bộ sinh viên. Trong Tuần 3 của chiến dịch tuyển sinh 2027, nhà trường tổ chức chuỗi Workshop phổ biến tiện ích học đường "
                "cho học sinh lớp 12 kèm gian hàng trải nghiệm kính thực tế ảo VR, cánh tay Robotics và Ngày hội FPTU Open Day 2027."
            ),
            "created_at": now - timedelta(days=12),
            "updated_at": now - timedelta(days=1),
        },
    ]

    # 7. Mẫu Email Block-Builder & Nhóm người nhận cho Workspace Tuyển sinh ĐH FPT (/mail-templates)
    recipient_group_id = "d7e00000-0000-4000-8000-000000000871"
    mail_recipient_groups = [
        {
            "_id": recipient_group_id,
            "workspaceId": WORKSPACE_ID,
            "name": "Danh sách Học sinh Lớp 12 Đăng ký Chuỗi Workshop THPT 2027",
            "recipients": [
                {"email": "hoangnam.2k9@demo.brandhub.test", "name": "Nguyễn Hoàng Nam - THPT Phan Châu Trinh", "consent": True, "consentSource": "CSV_IMPORT", "importedAt": now - timedelta(days=4)},
                {"email": "minhkhoi.2k9@demo.brandhub.test", "name": "Trần Minh Khôi - THPT Chuyên Lê Quý Đôn", "consent": True, "consentSource": "CSV_IMPORT", "importedAt": now - timedelta(days=4)},
                {"email": "ngocanh.2k9@demo.brandhub.test", "name": "Võ Ngọc Ánh - THPT Hoàng Hoa Thám", "consent": True, "consentSource": "MANUAL", "importedAt": now - timedelta(days=3)},
                {"email": "giahan.2k9@demo.brandhub.test", "name": "Lê Gia Hân - THPT Trần Phú", "consent": True, "consentSource": "CSV_IMPORT", "importedAt": now - timedelta(days=3)},
            ],
            "createdBy": creator3_id,
            "createdAt": now - timedelta(days=5),
        }
    ]

    fptu_mail_templates = [
        {
            "_id": "d7e00000-0000-4000-8000-000000000881",
            "workspaceId": WORKSPACE_ID,
            "agencyId": None,
            "name": "Thư mời tham dự Workshop Trải nghiệm Tiện ích Đại học FPT 2027",
            "subject": "[Đại học FPT 2027] Vé mời {{name}} tham dự Workshop trải nghiệm Phòng Lab & Tiện ích Campus",
            "type": "CUSTOM",
            "scope": "CAMPAIGN_BROADCAST",
            "bodyHtml": (
                "<div style='font-family:Inter,Arial,sans-serif;max-width:600px;margin:0 auto;padding:24px;border:1px solid #fed7aa;border-radius:12px;'>"
                "<h2 style='color:#ea580c;margin-top:0;'>Chào mừng bạn đến với Chuỗi Workshop THPT 2027</h2>"
                "<p>Xin chào <strong>{{name}}</strong>,</p>"
                "<p>Ban Tuyển sinh Trường Đại học FPT xác nhận đăng ký tham dự buổi Workshop phổ biến tiện ích học đường "
                "và định hướng ngành Thiết kế Vi mạch bán dẫn, Trí tuệ nhân tạo năm 2027 của bạn.</p>"
                "<p>Tại chương trình, bạn sẽ trực tiếp trải nghiệm kính VR tham quan 5 cơ sở, thử nghiệm Robotics và nhận cẩm nang Học bổng Nguyễn Văn Đạo (50%, 70%, 100%).</p>"
                "<p><a href='https://tuyensinh.fpt.edu.vn' style='display:inline-block;background:#ea580c;color:#ffffff;padding:10px 18px;border-radius:8px;text-decoration:none;font-weight:600;'>Xem lịch trình &amp; Mã check-in</a></p>"
                "</div>"
            ),
            "layoutJson": json.dumps(
                {
                    "version": 1,
                    "locale": "vi",
                    "blocks": [
                        {"id": "b1", "type": "header", "props": {}},
                        {"id": "b2", "type": "heading", "props": {"text": "Vé mời Workshop Trải nghiệm Tiện ích Đại học FPT 2027", "align": "left"}},
                        {"id": "b3", "type": "paragraph", "props": {"text": "Xin chào {{name}}, cảm ơn bạn đã đăng ký tham gia trải nghiệm phòng Lab bán dẫn, thư viện xanh và tư vấn Học bổng Nguyễn Văn Đạo 2027."}},
                        {"id": "b4", "type": "cta_button", "props": {"label": "Xem thông tin buổi Workshop", "urlType": "campaign"}},
                        {"id": "b5", "type": "footer", "props": {}},
                    ],
                },
                ensure_ascii=False,
            ),
            "attachments": [],
            "createdBy": creator3_id,
            "createdAt": now - timedelta(days=6),
            "updatedAt": now - timedelta(days=2),
        },
        {
            "_id": "d7e00000-0000-4000-8000-000000000882",
            "workspaceId": None,
            "agencyId": AGENCY_ID,
            "name": "Báo cáo tiến độ tuần Chiến dịch Tuyển sinh gửi Ban Tuyển sinh ĐH FPT",
            "subject": "[SE08 Digital x ĐH FPT] Báo cáo kết quả Tuần {{weekNumber}} Chiến dịch Tuyển sinh 2027",
            "type": "CUSTOM",
            "scope": "AGENCY_CLIENT",
            "bodyHtml": (
                "<div style='font-family:Inter,Arial,sans-serif;max-width:600px;margin:0 auto;padding:24px;border:1px solid #e2e8f0;border-radius:12px;'>"
                "<h2 style='color:#ea580c;margin-top:0;'>Báo cáo Tiến độ Chiến dịch Tuyển sinh 2027</h2>"
                "<p>Kính gửi <strong>Ban Tuyển sinh Trường Đại học FPT</strong>,</p>"
                "<p>Nhóm dự án SE08 Digital Agency kính gửi bảng tổng hợp tiến độ xuất bản đa nền tảng, chỉ số tiếp cận học sinh THPT và công tác chuẩn bị chuỗi Workshop tuần này.</p>"
                "</div>"
            ),
            "layoutJson": json.dumps(
                {
                    "version": 1,
                    "locale": "vi",
                    "blocks": [
                        {"id": "b1", "type": "header", "props": {}},
                        {"id": "b2", "type": "heading", "props": {"text": "Báo cáo tiến độ tuần Chiến dịch Tuyển sinh 2027", "align": "left"}},
                        {"id": "b3", "type": "paragraph", "props": {"text": "Kính gửi {{name}}, nhóm SE08 Digital cập nhật số liệu bài đăng đa nền tảng và lượt đăng ký Workshop THPT trong tuần."}},
                        {"id": "b4", "type": "cta_button", "props": {"label": "Mở Dashboard Chiến dịch", "urlType": "client"}},
                        {"id": "b5", "type": "footer", "props": {}},
                    ],
                },
                ensure_ascii=False,
            ),
            "attachments": [],
            "createdBy": manager_id,
            "createdAt": now - timedelta(days=10),
            "updatedAt": now - timedelta(days=1),
        },
    ]

    # 8. Kênh chat chuyên đề & Tin nhắn trao đổi thực tế trong Workspace Chat
    wm_lookup = {
        "MANAGER": (java_name_uuid_from_bytes(f"ws-member:{WORKSPACE_ID}:{manager_id}"), manager_id, "MANAGER", "Nguyễn Thành Lộc"),
        "CREATOR": (java_name_uuid_from_bytes(f"ws-member:{WORKSPACE_ID}:{creator_id}"), creator_id, "CREATOR", "Nguyễn Chơn Phước"),
        "CREATOR_2": (java_name_uuid_from_bytes(f"ws-member:{WORKSPACE_ID}:{creator2_id}"), creator2_id, "CREATOR", "Nguyễn Minh Tuấn"),
        "CREATOR_3": (java_name_uuid_from_bytes(f"ws-member:{WORKSPACE_ID}:{creator3_id}"), creator3_id, "CREATOR", "Hà Văn Ân"),
        "CLIENT": (java_name_uuid_from_bytes(f"ws-member:{WORKSPACE_ID}:{client_id}"), client_id, "CLIENT", "Ban Tuyển sinh Đại học FPT"),
    }

    ch_workshop_id = java_name_uuid_from_bytes(f"{WORKSPACE_ID}:ch-workshop-openday-2027")
    ch_internal_id = java_name_uuid_from_bytes(f"{WORKSPACE_ID}:ch-se08-internal-2027")
    all_chat_members = sorted([owner_id, manager_id, creator_id, creator2_id, creator3_id, client_id])
    agency_chat_members = sorted([owner_id, manager_id, creator_id, creator2_id, creator3_id])

    chat_channels = [
        {
            "_id": ch_workshop_id,
            "workspaceId": WORKSPACE_ID,
            "name": "workshop-thpt-openday-2027",
            "nameKey": "workshop-thpt-openday-2027",
            "description": "Phối hợp hậu cần chuỗi Workshop phổ biến tiện ích tại trường THPT và Ngày hội FPTU Open Day 2027",
            "type": "PUBLIC",
            "createdBy": manager_id,
            "creationKey": f"PUBLIC:workshop-thpt-openday-2027::{':'.join(all_chat_members)}",
            "memberUserIds": all_chat_members,
            "archived": False,
            "managersOnly": False,
            "createdAt": now - timedelta(days=12),
        },
        {
            "_id": ch_internal_id,
            "workspaceId": WORKSPACE_ID,
            "name": "noi-bo-se08-content-pr",
            "nameKey": "noi-bo-se08-content-pr",
            "description": "Trao đổi nội bộ nhóm SE08 Digital Agency về tiến độ sản xuất Key Visual, Video Reels và bài báo chí",
            "type": "PRIVATE",
            "createdBy": manager_id,
            "creationKey": f"PRIVATE:noi-bo-se08-content-pr::{':'.join(agency_chat_members)}",
            "memberUserIds": agency_chat_members,
            "archived": False,
            "managersOnly": False,
            "createdAt": now - timedelta(days=14),
        },
    ]

    chat_rows = [
        (None, "MANAGER", "GENERAL", None, "Chào cả nhóm SE08 và Ban Tuyển sinh ĐH FPT, chúng ta chính thức bước sang Tuần 3 (Chuỗi Workshop THPT & Open Day 2027). Mọi hạng mục Tuần 1 và Tuần 2 đã hoàn tất xuất bản trên cả 4 kênh."),
        (None, "CREATOR_2", "GENERAL", None, "Em cập nhật nhanh buổi Workshop #1 hôm qua tại Đà Nẵng: có 420 bạn học sinh lớp 12 tham dự, khu vực đeo kính VR xem phòng Lab bán dẫn và điều khiển cánh tay robot đông kín từ đầu giờ sáng ạ."),
        (None, "CLIENT", "GENERAL", None, "Cảm ơn Tuấn và cả nhóm SE08. Ban Tuyển sinh đánh giá rất cao bộ ảnh thực tế tại buổi Workshop. Đối với bài đăng trọng điểm Tuần 3 sắp lên, nhờ Phước lưu ý nêu rõ cả 3 mức Học bổng Nguyễn Văn Đạo 50%, 70%, 100% và học kỳ doanh nghiệp OJT từ học kỳ 6 nhé."),
        (None, "CREATOR", "GENERAL", None, "Dạ vâng ạ! Phần thông tin nền, hình ảnh Workshop và lịch đăng 4 nền tảng (Facebook, Instagram, TikTok, Threads) của bài trọng điểm Tuần 3 đã được duyệt xong, chiều nay em hoàn thiện phần nội dung bài viết và gửi duyệt ngay."),
        (None, "CREATOR_3", "GENERAL", None, "Báo cáo anh Lộc và Ban Tuyển sinh: khảo sát học sinh lớp 12 đã thu về đầy đủ câu hỏi thực tế, em cũng đã gửi bản thảo thông cáo báo chí VnExpress Giáo dục lên hàng đợi duyệt cho đầu Tuần 4 rồi ạ."),
        (None, "MANAGER", "MEDIA_PACKAGE", ws_pkg_id, "Gói Tuyển sinh Đại học FPT 2027 (4 tuần) hiện đã hoàn thành 8/19 hạng mục đúng hạn, 7 hạng mục đang triển khai trong Tuần 3 và 4 hạng mục cuối đã sẵn sàng lịch cho Tuần 4."),
        (None, "CLIENT", "MEDIA_PACKAGE", ws_pkg_id, "Tiến độ bám rất sát kế hoạch tuyển sinh đợt 1 của nhà trường. Phần khảo sát học sinh THPT phát sinh thêm cũng đã hỗ trợ rất tốt cho đội ngũ giảng viên chuẩn bị nội dung diễn giả."),
        (None, "MANAGER", "MEDIA_CAMPAIGN", CAMPAIGN_ID, "Nhắc lịch cả nhóm: cuối tuần này diễn ra Ngày hội FPTU Open Day 2027, Tuấn phối hợp sát cùng ê-kíp Schannel / Duy Luân và bạn Đại sứ sinh viên K19 tại sân khấu chính nhé."),
        (None, "CREATOR_2", "MEDIA_CAMPAIGN", CAMPAIGN_ID, "Dạ anh Lộc, kịch bản sân khấu và bộ dây đeo cam FPTU Open Day 2027 đã sẵn sàng 100%."),
        (ch_workshop_id, "CREATOR_2", "GENERAL", None, "Danh sách 18 trường THPT xác nhận tham gia đợt trải nghiệm tiện ích Campus tuần này đã chốt xong phương án xe đưa đón."),
        (ch_workshop_id, "CLIENT", "GENERAL", None, "Ban Tuyển sinh đã bố trí thêm 06 giảng viên ngành Thiết kế Vi mạch và AI trực tiếp đứng trạm hướng dẫn thực hành cho các em học sinh lớp 12."),
        (ch_internal_id, "MANAGER", "GENERAL", None, "Anh em SE08 lưu ý: bộ 7 ảnh Key Visual mùa tuyển sinh 2027 Tuấn vừa xuất đã có sẵn trong Thư viện (/library), Phước và Ân lấy trực tiếp từ thư mục từng tuần nhé."),
        (ch_internal_id, "CREATOR", "GENERAL", None, "Đã nhận anh Lộc! Em đang mở task bài trọng điểm Tuần 3 để hoàn thiện caption chuẩn giọng thương hiệu ĐH FPT."),
    ]

    chat_messages = [
        {
            "_id": f"d7e1{idx + 1:020x}",
            "workspaceId": WORKSPACE_ID,
            "channelId": ch_id,
            "senderMemberId": wm_lookup[s_key][0],
            "senderUserId": wm_lookup[s_key][1],
            "senderRole": wm_lookup[s_key][2],
            "senderDisplayName": wm_lookup[s_key][3],
            "content": text,
            "contextType": ctx_type,
            "contextId": ctx_id,
            "clientMessageId": java_name_uuid_from_bytes(f"fptu2027-chat:{idx}"),
            "threadRootId": None,
            "mentionUserIds": [],
            "attachmentIds": [],
            "reactions": {},
            "pinned": idx == 0,
            "createdAt": now - timedelta(hours=(len(chat_rows) - idx) * 2),
        }
        for idx, (ch_id, s_key, ctx_type, ctx_id, text) in enumerate(chat_rows)
    ]

    # 8b. Trao đổi trực tiếp trên Task trọng điểm (task_comments & task_approvals)
    task_comments = [
        {
            "_id": java_name_uuid_from_bytes(f"task-cmt:{TASK_1_ID}:1"),
            "workspaceId": WORKSPACE_ID,
            "taskId": TASK_1_ID,
            "authorId": creator2_id,
            "authorRole": "CREATOR",
            "authorDisplayName": "Nguyễn Minh Tuấn",
            "content": "Mình đã tải bộ ảnh thực tế buổi Workshop THPT (trải nghiệm kính VR phòng Lab bán dẫn & Robotics) lên Thư viện thư mục Tuần 3 rồi nhé Phước ơi.",
            "mentions": [creator_id],
            "attachmentIds": [],
            "clientRequestId": java_name_uuid_from_bytes(f"task-cmt-req:{TASK_1_ID}:1"),
            "createdAt": now - timedelta(hours=5),
        },
        {
            "_id": java_name_uuid_from_bytes(f"task-cmt:{TASK_1_ID}:2"),
            "workspaceId": WORKSPACE_ID,
            "taskId": TASK_1_ID,
            "authorId": client_id,
            "authorRole": "CLIENT",
            "authorDisplayName": "Ban Tuyển sinh Đại học FPT",
            "content": "Hình ảnh buổi Workshop và lựa chọn 4 kênh xuất bản (Facebook, Instagram, TikTok, Threads) đã đạt yêu cầu. Nhờ Phước hoàn thiện phần nội dung bài viết nêu rõ 3 mức Học bổng Nguyễn Văn Đạo 50%, 70%, 100% và kỳ thực tập OJT học kỳ 6.",
            "mentions": [creator_id],
            "attachmentIds": [],
            "clientRequestId": java_name_uuid_from_bytes(f"task-cmt-req:{TASK_1_ID}:2"),
            "createdAt": now - timedelta(hours=3),
        },
    ]

    finished_task_ids = [t["_id"] for t in tasks if t["status"] == "FINISHED" and t["requiresClientApproval"]]
    task_approvals = []
    for f_idx, ft_id in enumerate(finished_task_ids[:4]):
        task_approvals.append(
            {
                "_id": java_name_uuid_from_bytes(f"task-appr:{ft_id}:mgr"),
                "taskId": ft_id,
                "approvalRound": 1,
                "step": "MANAGER",
                "action": "APPROVE",
                "actorId": manager_id,
                "comment": "Nội dung và hình ảnh bám sát định hướng chiến dịch Tuyển sinh ĐH FPT 2027, chuyển Ban Tuyển sinh duyệt xuất bản.",
                "createdAt": now - timedelta(days=10 - f_idx, hours=4),
            }
        )
        task_approvals.append(
            {
                "_id": java_name_uuid_from_bytes(f"task-appr:{ft_id}:cli"),
                "taskId": ft_id,
                "approvalRound": 1,
                "step": "CLIENT",
                "action": "APPROVE",
                "actorId": client_id,
                "comment": "Thông tin ngành học, tiện ích 5 cơ sở và quy chế học bổng chính xác. Đồng ý đăng tải.",
                "createdAt": now - timedelta(days=10 - f_idx, hours=2),
            }
        )

    # 9. Nhật ký sử dụng AI & Báo cáo tổng hợp (ai_usage_logs & report_jobs)
    ai_usage_logs = [
        {
            "_id": f"d7e00000-0000-4000-8000-{950 + i:012d}",
            "workspace_id": WORKSPACE_ID,
            "feature": feat,
            "model": model,
            "success": True,
            "created_at": now - timedelta(days=12 - i),
        }
        for i, (feat, model) in enumerate(
            [
                ("caption_generation", "gemini-2.5-flash"),
                ("hashtag_suggestion", "gemini-2.5-flash"),
                ("compliance_check", "gemini-2.5-flash"),
                ("caption_generation", "gpt-4o-mini"),
                ("compliance_check", "gemini-2.5-flash"),
                ("hashtag_suggestion", "gemini-2.5-flash"),
            ]
        )
    ]

    report_jobs = [
        {
            "_id": "d7e00000-0000-4000-8000-000000000970",
            "workspace_id": WORKSPACE_ID,
            "requested_by": manager_id,
            "status": "DONE",
            "date_from": now - timedelta(days=14),
            "date_to": now,
            "created_at": now - timedelta(hours=6),
            "updated_at": now - timedelta(hours=6),
        }
    ]

    # 10. Kho lưu trữ riêng của Khách hàng (CLIENT_VAULT) & chia sẻ sang Workspace ĐH FPT 2027 (/library khi đăng nhập Client)
    vault_folder_defs = [
        ("vf_1", "d7e00000-0000-4000-8000-000000000981", "01. Bộ Nhận diện & Cẩm nang Học bổng Nguyễn Văn Đạo 2027", "0001"),
        ("vf_2", "d7e00000-0000-4000-8000-000000000982", "02. Tư liệu Ảnh gốc Phòng Lab & 5 Cơ sở Đại học FPT", "0002"),
    ]
    client_vault_shares: list[dict[str, Any]] = []
    for _vk, vfid, vfname, vskey in vault_folder_defs:
        material_folders.append(
            {
                "_id": vfid,
                "scope_type": "CLIENT_VAULT",
                "workspace_id": WORKSPACE_ID,
                "owner_user_id": client_id,
                "name": vfname,
                "normalized_name": vfname.lower(),
                "sort_key": vskey,
                "parent_folder_id": None,
                "ancestor_ids": [],
                "created_by": client_id,
                "created_at": now - timedelta(days=20),
                "updated_at": now - timedelta(days=2),
                "version": 1,
            }
        )
        client_vault_shares.append(
            {
                "_id": java_name_uuid_from_bytes(f"vault-share:{WORKSPACE_ID}:FOLDER:{vfid}"),
                "owner_user_id": client_id,
                "workspace_id": WORKSPACE_ID,
                "client_profile_id": CLIENT_PROFILE_ID,
                "resource_type": "FOLDER",
                "resource_id": vfid,
                "shared_at": now - timedelta(days=16),
                "shared_by": client_id,
            }
        )

    vault_visual_specs = [
        ("d7e00000-0000-4000-8000-000000000985", "d7e00000-0000-4000-8000-000000000981", "Poster_Goc_Hoc_Bong_Nguyen_Van_Dao_2027.jpg", "fptu-week1-coming-soon.jpg"),
        ("d7e00000-0000-4000-8000-000000000986", "d7e00000-0000-4000-8000-000000000981", "So_Tay_Quy_Che_Tuyen_Sinh_Khoa_K23_FPTU.jpg", "fptu-week4-ojt-press.jpg"),
        ("d7e00000-0000-4000-8000-000000000987", "d7e00000-0000-4000-8000-000000000982", "Anh_Goc_Phong_Lab_Vi_Mach_Ban_Dan_AI.jpg", "fptu-week2-semiconductor-ai.jpg"),
        ("d7e00000-0000-4000-8000-000000000988", "d7e00000-0000-4000-8000-000000000982", "Anh_Goc_Thu_Vien_Xanh_Va_San_Vovinam_FPTU.jpg", "fptu-week2-campus-utilities.jpg"),
    ]
    for v_idx, (vm_id, vf_id, vm_name, vm_file) in enumerate(vault_visual_specs):
        v_uri, v_bytes = load_asset_data_uri(vm_file)
        materials.append(
            {
                "_id": vm_id,
                "workspace_id": WORKSPACE_ID,
                "owner_user_id": client_id,
                "name": vm_name,
                "original_name": vm_file,
                "normalized_name": vm_name.lower(),
                "scope_type": "CLIENT_VAULT",
                "folder_id": vf_id,
                "ancestor_folder_ids": [vf_id],
                "sort_key": f"{v_idx + 1:04d}",
                "content_hash": sha256_hex(vm_id),
                "current_version_number": 1,
                "type": "RAW",
                "mime_type": "image/jpeg",
                "file_size": v_bytes,
                "url": v_uri,
                "s3_key": f"demo/client-vault-fptu/{vm_file}",
                "storage_provider": "SYSTEM_S3",
                "status": "READY",
                "media_kind": "IMAGE",
                "purpose": "BRAND_REFERENCE",
                "visibility": "CLIENT",
                "client_profile_id": CLIENT_PROFILE_ID,
                "access_state": "READY",
                "access_revision": 1,
                "version": 1,
                "draft": False,
                "created_by": client_id,
                "updated_by": client_id,
                "created_at": now - timedelta(days=19 - v_idx),
                "updated_at": now - timedelta(days=2),
            }
        )
        client_vault_shares.append(
            {
                "_id": java_name_uuid_from_bytes(f"vault-share:{WORKSPACE_ID}:MATERIAL:{vm_id}"),
                "owner_user_id": client_id,
                "workspace_id": WORKSPACE_ID,
                "client_profile_id": CLIENT_PROFILE_ID,
                "resource_type": "MATERIAL",
                "resource_id": vm_id,
                "shared_at": now - timedelta(days=16),
                "shared_by": client_id,
            }
        )

    # Biểu mẫu đăng ký đi kèm 2 công việc WORKSHOP để WorkshopEditorPage hiển thị sẵn câu hỏi đăng ký
    workshop_surveys = []
    for ws_idx, t in enumerate([tk for tk in tasks if tk["type"] == "WORKSHOP"]):
        workshop_surveys.append(
            {
                "_id": f"d7e00000-0000-4000-8000-{805 + ws_idx:012d}",
                "workspaceId": WORKSPACE_ID,
                "taskId": t["_id"],
                "publicToken": f"dang-ky-workshop-thpt-fptu-2027-dot-{ws_idx + 1}",
                "formName": f"Phiếu đăng ký tham dự {t['name']}",
                "title": f"Đăng ký tham dự Trải nghiệm Phòng Lab & Tiện ích Đại học FPT 2027 (Đợt {ws_idx + 1})",
                "description": "Dành cho học sinh lớp 12 và giáo viên phụ trách Đoàn trường đăng ký nhận thẻ đeo check-in tại buổi Workshop.",
                "bannerUrl": FPTU_VISUALS["week3_thpt_workshop"]["url"],
                "status": "PUBLISHED",
                "questions": [
                    {"id": "wq1_name", "type": "SHORT_TEXT", "label": "Họ và tên học sinh lớp 12", "required": True},
                    {"id": "wq2_school", "type": "SHORT_TEXT", "label": "Trường THPT đang theo học", "required": True},
                    {
                        "id": "wq3_station",
                        "type": "MULTIPLE_CHOICE",
                        "label": "Trạm trải nghiệm công nghệ bạn muốn tham gia đầu tiên?",
                        "options": [
                            "Trạm Kính thực tế ảo VR & Phòng Lab Thiết kế Vi mạch bán dẫn",
                            "Trạm Điều khiển cánh tay Robotics & Trí tuệ nhân tạo",
                            "Bàn tư vấn Học bổng Nguyễn Văn Đạo & Học kỳ doanh nghiệp OJT",
                        ],
                        "required": True,
                    },
                ],
                "createdAt": now - timedelta(days=7),
                "updatedAt": now - timedelta(days=1),
            }
        )

    return {
        "material_folders": material_folders,
        "materials": materials,
        "client_vault_shares": client_vault_shares,
        "social_accounts": social_accounts,
        "tasks": tasks,
        "task_sections": task_sections,
        "task_section_versions": task_section_versions,
        "task_comments": task_comments,
        "task_approvals": task_approvals,
        "posts": posts,
        "post_versions": post_versions,
        "publish_logs": publish_logs,
        "survey": survey_doc,
        "workshop_surveys": workshop_surveys,
        "survey_responses": survey_responses,
        "content_requests": content_requests,
        "brand_profile": brand_profile,
        "knowledge_documents": knowledge_documents,
        "mail_recipient_groups": mail_recipient_groups,
        "mail_templates": fptu_mail_templates,
        "chat_channels": chat_channels,
        "chat_messages": chat_messages,
        "ai_usage_logs": ai_usage_logs,
        "report_jobs": report_jobs,
    }


def apply_mongo(mongo_uri: str, mongo_db_name: str, bundle: dict[str, Any], client_user_id: str) -> None:
    try:
        from pymongo import MongoClient
    except ImportError as exc:
        raise RuntimeError("Cần cài đặt pymongo: pip install pymongo") from exc

    client = MongoClient(mongo_uri)
    try:
        try:
            default_db = client.get_default_database()
            db = default_db if default_db is not None else client[mongo_db_name]
        except Exception:
            db = client[mongo_db_name]

        # 1. Dọn dẹp sạch toàn bộ dữ liệu cũ/rời rạc trong Workspace ĐH FPT trước khi nạp mới
        old_task_ids = [doc["_id"] for doc in db.tasks.find({"workspaceId": WORKSPACE_ID}, {"_id": 1})]
        new_task_ids = [t["_id"] for t in bundle["tasks"]]
        all_clean_task_ids = list(set(old_task_ids + new_task_ids))

        if all_clean_task_ids:
            db.task_sections.delete_many({"taskId": {"$in": all_clean_task_ids}})
            db.task_section_versions.delete_many({"taskId": {"$in": all_clean_task_ids}})
            db.task_section_events.delete_many({"taskId": {"$in": all_clean_task_ids}})
            db.task_approvals.delete_many({"taskId": {"$in": all_clean_task_ids}})

        db.tasks.delete_many({"workspaceId": WORKSPACE_ID})
        db.task_comments.delete_many({"workspaceId": WORKSPACE_ID})
        db.posts.delete_many({"workspace_id": WORKSPACE_ID})
        db.post_versions.delete_many({"workspace_id": WORKSPACE_ID})
        db.publish_logs.delete_many({"workspace_id": WORKSPACE_ID})
        db.material_references.delete_many({"workspace_id": WORKSPACE_ID})
        db.materials.delete_many({"$or": [{"workspace_id": WORKSPACE_ID}, {"scope_type": "CLIENT_VAULT", "owner_user_id": client_user_id}]})
        db.material_folders.delete_many({"$or": [{"workspace_id": WORKSPACE_ID}, {"scope_type": "CLIENT_VAULT", "owner_user_id": client_user_id}]})
        db.client_vault_shares.delete_many({"$or": [{"workspace_id": WORKSPACE_ID}, {"owner_user_id": client_user_id}]})
        db.social_accounts.delete_many({"workspace_id": WORKSPACE_ID})
        db.surveys.delete_many({"workspaceId": WORKSPACE_ID})
        db.survey_responses.delete_many({"surveyId": SURVEY_DOC_ID})
        db.content_requests.delete_many({"workspaceId": WORKSPACE_ID})
        db.brand_profiles.delete_many({"workspace_id": WORKSPACE_ID})
        db.knowledge_documents.delete_many({"workspace_id": WORKSPACE_ID})
        db.mail_recipient_groups.delete_many({"workspaceId": WORKSPACE_ID})
        db.mail_templates.delete_many(
            {
                "$or": [
                    {"workspaceId": WORKSPACE_ID},
                    {"agencyId": AGENCY_ID},
                    {"name": {"$in": ["gg", "test", "Test", "demo", "abc"]}},
                ]
            }
        )
        db.chat_channel_reads.delete_many({"workspaceId": WORKSPACE_ID})
        db.chat_channels.delete_many({"workspaceId": WORKSPACE_ID})
        db.chat_messages.delete_many({"workspaceId": WORKSPACE_ID})
        db.ai_usage_logs.delete_many({"workspace_id": WORKSPACE_ID})
        db.report_jobs.delete_many({"workspace_id": WORKSPACE_ID})

        # 2. Insert / Upsert dữ liệu chuẩn xuyên suốt 4 tuần
        def upsert_many(col_name: str, docs: list[dict[str, Any]]) -> None:
            col = db[col_name]
            for d in docs:
                col.replace_one({"_id": d["_id"]}, d, upsert=True)

        upsert_many("material_folders", bundle["material_folders"])
        upsert_many("materials", bundle["materials"])
        upsert_many("client_vault_shares", bundle["client_vault_shares"])
        upsert_many("social_accounts", bundle["social_accounts"])
        upsert_many("tasks", bundle["tasks"])
        upsert_many("task_sections", bundle["task_sections"])
        upsert_many("task_section_versions", bundle["task_section_versions"])
        upsert_many("task_comments", bundle["task_comments"])
        upsert_many("task_approvals", bundle["task_approvals"])
        upsert_many("posts", bundle["posts"])
        upsert_many("post_versions", bundle["post_versions"])
        upsert_many("publish_logs", bundle["publish_logs"])
        db.surveys.replace_one({"_id": bundle["survey"]["_id"]}, bundle["survey"], upsert=True)
        upsert_many("surveys", bundle["workshop_surveys"])
        upsert_many("survey_responses", bundle["survey_responses"])
        upsert_many("content_requests", bundle["content_requests"])
        db.brand_profiles.replace_one({"_id": bundle["brand_profile"]["_id"]}, bundle["brand_profile"], upsert=True)
        upsert_many("knowledge_documents", bundle["knowledge_documents"])
        upsert_many("mail_recipient_groups", bundle["mail_recipient_groups"])
        upsert_many("mail_templates", bundle["mail_templates"])
        upsert_many("chat_channels", bundle["chat_channels"])
        upsert_many("chat_messages", bundle["chat_messages"])
        upsert_many("ai_usage_logs", bundle["ai_usage_logs"])
        upsert_many("report_jobs", bundle["report_jobs"])

        print(
            f"[OK] Đã đồng bộ MongoDB ({db.name}) thành công:\n"
            f"     - {len(bundle['tasks'])} tasks (4 tuần), {len(bundle['task_sections'])} task_sections\n"
            f"     - {len(bundle['posts'])} posts (Facebook, Instagram, TikTok, Threads), {len(bundle['publish_logs'])} publish_logs\n"
            f"     - {len(bundle['material_folders'])} thư mục & {len(bundle['materials'])} tài nguyên Thư viện + Client Vault\n"
            f"     - {1 + len(bundle['workshop_surveys'])} khảo sát/đăng ký ({len(bundle['survey_responses'])} phản hồi), {len(bundle['content_requests'])} yêu cầu nội dung, "
            f"{len(bundle['knowledge_documents'])} tài liệu AI, {len(bundle['chat_messages'])} tin nhắn nhóm."
        )
    finally:
        client.close()


def apply_redis_trends(redis_url: str, now: datetime) -> None:
    """Nạp sẵn dữ liệu Xu hướng (Trends v2) vào Redis để /ai-studio/trends, /workspaces/:id/trends & /admin?view=trends hiển thị tức thì."""
    try:
        import redis as sync_redis
    except ImportError:
        print("[WARN] Bỏ qua đồng bộ Redis Trends do chưa cài gói redis.")
        return

    try:
        r = sync_redis.from_url(redis_url, decode_responses=True)
        r.ping()
    except Exception as exc:
        print(f"[WARN] Không kết nối được Redis ({exc}); bỏ qua bước nạp Trends.")
        return

    ttl = 7 * 86400
    base_trends = [
        {
            "slug": "hoc-bong-nguyen-van-dao-2027",
            "keyword": "Học bổng Nguyễn Văn Đạo & Tuyển sinh Đại học 2027",
            "score": 94.6,
            "virality": 91.2,
            "engagement": 89.5,
            "topic": "giáo_dục",
            "status": "peaking",
            "mood": "positive",
            "emotion": "hào hứng",
            "brand_risk": "low",
            "cross_topic": True,
            "keywords": ["học bổng nguyễn văn đạo", "tuyển sinh 2027", "xét tuyển sớm k23", "đại học fpt"],
            "hashtags": ["#TuyenSinhFPTU2027", "#HocBongNguyenVanDao", "#DaiHocFPT", "#2k9ChonNganh"],
            "sources": {"facebook": 148, "tiktok": 195, "threads": 84},
            "samples": [
                "Tổng hợp điều kiện nộp hồ sơ xét Học bổng Nguyễn Văn Đạo mức 50%, 70%, 100% học phí cho teen 2k9.",
                "Kinh nghiệm chuẩn bị hồ sơ thành tích học tập lớp 12 săn học bổng công nghệ đợt 1.",
            ],
        },
        {
            "slug": "thiet-ke-vi-mach-ban-dan-ai",
            "keyword": "Ngành Thiết kế Vi mạch Bán dẫn & Trí tuệ Nhân tạo (AI)",
            "score": 91.8,
            "virality": 88.4,
            "engagement": 86.0,
            "topic": "công_nghệ",
            "status": "rising",
            "mood": "positive",
            "emotion": "tò mò",
            "brand_risk": "low",
            "cross_topic": True,
            "keywords": ["vi mạch bán dẫn", "kỹ sư ai", "phòng lab bán dẫn", "nhân lực công nghệ cao"],
            "hashtags": ["#ViMachBanDan", "#TriTueNhanTao", "#FPTUniversity", "#CongNghe2027"],
            "sources": {"facebook": 112, "tiktok": 164, "threads": 92},
            "samples": [
                "Bên trong phòng Lab Thiết kế Vi mạch bán dẫn và AI nơi sinh viên thực hành từ năm hai.",
                "Vì sao khối ngành Vi mạch bán dẫn và Trí tuệ nhân tạo thu hút mạnh học sinh giỏi Toán - Lý - Tin 2k9?",
            ],
        },
        {
            "slug": "hoc-ky-thuc-tap-doanh-nghiep-ojt",
            "keyword": "Học kỳ thực tập doanh nghiệp OJT từ năm thứ ba",
            "score": 87.4,
            "virality": 83.5,
            "engagement": 84.2,
            "topic": "giáo_dục",
            "status": "rising",
            "mood": "positive",
            "emotion": "tin tưởng",
            "brand_risk": "low",
            "cross_topic": False,
            "keywords": ["học kỳ ojt", "thực tập fpt software", "kinh nghiệm thực tế", "việc làm sau tốt nghiệp"],
            "hashtags": ["#HocKyOJT", "#ThucTapDoanhNghiep", "#FPTSoftware", "#SinhVienCongNghe"],
            "sources": {"facebook": 96, "tiktok": 142, "threads": 68},
            "samples": [
                "Nhật ký 4 tháng đi thực tập OJT học kỳ 6 tại FPT Software của sinh viên K19 ngành Kỹ thuật phần mềm.",
                "Phụ huynh đánh giá cao mô hình đào tạo gắn liền kỳ thực tập dự án thật tại doanh nghiệp.",
            ],
        },
        {
            "slug": "ngay-hoi-open-day-workshop-thpt",
            "keyword": "Ngày hội Open Day & Workshop trải nghiệm phòng Lab THPT",
            "score": 84.9,
            "virality": 85.0,
            "engagement": 81.6,
            "topic": "đời_sống_giới_trẻ",
            "status": "new",
            "mood": "positive",
            "emotion": "vui vẻ",
            "brand_risk": "low",
            "cross_topic": False,
            "keywords": ["open day 2027", "workshop thpt", "kính thực tế ảo vr", "cánh tay robotics"],
            "hashtags": ["#FPTUOpenDay", "#WorkshopTHPT", "#TraiNghiemCampus", "#2k9"],
            "sources": {"facebook": 105, "tiktok": 178, "threads": 54},
            "samples": [
                "Hơn 400 bạn học sinh lớp 12 hào hứng thử kính VR và điều khiển robot tại buổi Workshop hướng nghiệp.",
                "Lịch trình 08 tuyến xe buýt đón học sinh THPT tham gia Ngày hội FPTU Open Day cuối tuần này.",
            ],
        },
        {
            "slug": "doi-song-noi-tru-clb-vovinam",
            "keyword": "Review đời sống Ký túc xá xanh, Vovinam & 40+ CLB Đại học",
            "score": 81.2,
            "virality": 80.1,
            "engagement": 79.4,
            "topic": "đời_sống_giới_trẻ",
            "status": "rising",
            "mood": "positive",
            "emotion": "yêu thích",
            "brand_risk": "low",
            "cross_topic": False,
            "keywords": ["ký túc xá đh fpt", "đồng diễn vovinam", "thư viện xanh", "clb sinh viên"],
            "hashtags": ["#CampusLife", "#VovinamFPTU", "#ThuVienXanh", "#KyTucXa"],
            "sources": {"facebook": 78, "tiktok": 156, "threads": 61},
            "samples": [
                "Một ngày từ sáng tập Vovinam, trưa học nhóm ở thư viện xanh đến tối sinh hoạt CLB âm nhạc tại FPTU.",
            ],
        },
        {
            "slug": "ngoai-ngu-anh-nhat-nganh-it",
            "keyword": "Lợi thế song ngữ Anh - Nhật cho kỹ sư Công nghệ thông tin",
            "score": 77.5,
            "virality": 74.8,
            "engagement": 75.0,
            "topic": "giáo_dục",
            "status": "rising",
            "mood": "positive",
            "emotion": "quan tâm",
            "brand_risk": "low",
            "cross_topic": False,
            "keywords": ["tiếng nhật cntt", "học kỳ nước ngoài", "kỹ sư cầu nối brse", "song ngữ đại học"],
            "hashtags": ["#SongNguCNTT", "#KySuCauNoi", "#HocKyNuocNgoai"],
            "sources": {"facebook": 64, "tiktok": 88, "threads": 49},
            "samples": [
                "Lộ trình rèn tiếng Anh và ngoại ngữ thứ hai giúp sinh viên CNTT tự tin tham gia dự án quốc tế.",
            ],
        },
    ]

    run_id = now.strftime("%Y%m%d%H%M%S")
    pipe = r.pipeline(transaction=True)
    for day_offset in range(7):
        day_dt = now - timedelta(days=day_offset)
        date_str = day_dt.strftime("%Y-%m-%d")
        daily_key = f"trends:v2:{date_str}:all"
        pipe.delete(daily_key, daily_key + ":data")
        pipe.set(daily_key + ":published", "1", ex=ttl)

        zmap: dict[str, float] = {}
        hmap: dict[str, str] = {}
        for rank_idx, item in enumerate(base_trends, 1):
            decay = max(0.76, 1.0 - day_offset * 0.035)
            score = round(item["score"] * decay, 2)
            tid = f"trend:{date_str}:all:{item['slug']}"
            daily_counts = [
                max(18, int(sum(item["sources"].values()) * (0.55 + 0.07 * d)))
                for d in range(7)
            ]
            cand = {
                "trend_id": tid,
                "rank": rank_idx,
                "keyword": item["keyword"],
                "anomaly_score": round(score * 0.96, 2),
                "virality_score": item["virality"],
                "engagement_score": item["engagement"],
                "final_score": score,
                "sample_posts": item["samples"],
                "source_distribution": item["sources"],
                "metadata": {"daily_counts": daily_counts, "workspace_fit": True},
                "keywords": item["keywords"],
                "hashtags": item["hashtags"],
                "topic": item["topic"],
                "mood": item["mood"],
                "emotion": item["emotion"],
                "emotion_dist": {"hào hứng": 0.52, "tin tưởng": 0.33, "tò mò": 0.15},
                "brand_risk": item["brand_risk"],
                "status": item["status"],
                "momentum": {
                    "velocity": 1.38,
                    "acceleration": 0.22,
                    "active_days": 7,
                    "daily_counts": daily_counts,
                },
                "cross_topic": item["cross_topic"],
                "is_campaign": False,
                "post_items": [
                    {
                        "url": "https://www.facebook.com/university.fpt.edu.vn",
                        "author": "Cộng đồng Học sinh THPT 2k9",
                        "source": "facebook",
                        "likes": 2450,
                        "shares": 380,
                        "comments": 290,
                        "postedAt": day_dt.strftime("%Y-%m-%dT09:00:00Z"),
                        "text": item["samples"][0],
                    },
                    {
                        "url": "https://www.tiktok.com/@fptu.official",
                        "author": "Góc Hướng nghiệp Công nghệ",
                        "source": "tiktok",
                        "likes": 6800,
                        "shares": 910,
                        "comments": 430,
                        "postedAt": day_dt.strftime("%Y-%m-%dT14:30:00Z"),
                        "text": item["samples"][-1],
                    },
                ],
            }
            zmap[tid] = score
            hmap[tid] = json.dumps(cand, ensure_ascii=False)

        pipe.zadd(daily_key, zmap)
        pipe.hset(daily_key + ":data", mapping=hmap)
        pipe.expire(daily_key, ttl)
        pipe.expire(daily_key + ":data", ttl)
        status_doc = json.dumps(
            {
                "run_id": run_id,
                "status": "completed",
                "date": date_str,
                "published_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "count": len(base_trends),
            }
        )
        pipe.set(daily_key + ":status", status_doc, ex=ttl)

        if day_offset == 0:
            live_key = "trends:v2:live:all"
            pipe.delete(live_key, live_key + ":data")
            pipe.set(live_key + ":published", "1", ex=ttl)
            pipe.zadd(live_key, zmap)
            pipe.hset(live_key + ":data", mapping=hmap)
            pipe.expire(live_key, ttl)
            pipe.expire(live_key + ":data", ttl)
            pipe.set("trends:v2:status:all", status_doc, ex=ttl)

    for plat in ("FACEBOOK", "INSTAGRAM", "TIKTOK", "THREADS"):
        plat_payload = {
            "trends": [
                {"keyword": t["keyword"], "score": t["score"], "hashtags": t["hashtags"]}
                for t in base_trends
            ],
            "cachedAt": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "ttlSeconds": ttl,
        }
        pipe.set(f"trends:{plat}:VN", json.dumps(plat_payload, ensure_ascii=False), ex=ttl)

    pipe.execute()
    print(f"[OK] Đã đồng bộ Redis Trends thành công ({len(base_trends)} xu hướng chủ đạo suốt 7 ngày cho AI Studio & Workspace).")


def clean_postgres(pg_uri: str) -> dict[str, str]:
    """Xóa sạch toàn bộ dữ liệu mẫu và dữ liệu phát sinh sau khi demo trong PostgreSQL (giữ lại tài khoản đăng nhập & khung Agency/Workspace rỗng)."""
    try:
        import psycopg2
    except ImportError as exc:
        raise RuntimeError("Cần cài đặt psycopg2-binary: pip install psycopg2-binary") from exc

    resolved_ids = dict(PG_USER_IDS)
    conn = psycopg2.connect(pg_uri)
    try:
        with conn:
            with conn.cursor() as cur:
                for key, acc in DEMO_ACCOUNTS.items():
                    cur.execute("SELECT id::text FROM users WHERE email = %s LIMIT 1;", (acc["email"],))
                    row = cur.fetchone()
                    if row and row[0]:
                        resolved_ids[key] = str(row[0])

                owner_id = resolved_ids["OWNER"]
                manager_id = resolved_ids["MANAGER"]
                creator_id = resolved_ids["CREATOR"]
                creator2_id = resolved_ids["CREATOR_2"]
                creator3_id = resolved_ids["CREATOR_3"]
                client_id = resolved_ids["CLIENT"]
                admin_id = resolved_ids["ADMIN"]

                demo_users = [owner_id, manager_id, creator_id, creator2_id, creator3_id, client_id, admin_id]
                companion_ws_ids = [
                    "d7e00000-0000-4000-8000-000000000091",
                    "d7e00000-0000-4000-8000-000000000092",
                ]
                demo_ws_ids = [WORKSPACE_ID] + companion_ws_ids

                # 1. Đặt lại trạng thái sạch cho 7 tài khoản Demo & xóa cảnh cáo phát sinh (B15)
                cur.execute(
                    """
                    UPDATE users
                    SET status = 'ACTIVE', is_active = TRUE, clean_period_ends_at = NULL, reactivate_at = NULL
                    WHERE id = ANY(%s::uuid[]);
                    DELETE FROM sanction_reviews WHERE user_id = ANY(%s::uuid[]);
                    UPDATE user_strikes SET converted_to_id = NULL WHERE user_id = ANY(%s::uuid[]);
                    DELETE FROM user_strikes WHERE user_id = ANY(%s::uuid[]);
                    DELETE FROM admin_account_operations WHERE user_id = ANY(%s::uuid[]);
                    DELETE FROM content_moderation_reviews WHERE workspace_id = ANY(%s::uuid[]);
                    """,
                    (demo_users, demo_users, demo_users, demo_users, demo_users, demo_ws_ids),
                )

                # 2. Xóa các bản nháp AI, Video Jobs & Yjs Canvas Tasks trong PostgreSQL
                cur.execute(
                    """
                    DELETE FROM ai_caption_generations WHERE workspace_id = ANY(%s::uuid[]);
                    DELETE FROM ai_video_jobs WHERE workspace_id = ANY(%s::uuid[]);
                    DELETE FROM task_content_operations WHERE task_id IN (SELECT id FROM tasks WHERE workspace_id = ANY(%s::uuid[]));
                    DELETE FROM task_content_snapshots WHERE task_id IN (SELECT id FROM tasks WHERE workspace_id = ANY(%s::uuid[]));
                    DELETE FROM tasks WHERE workspace_id = ANY(%s::uuid[]);
                    """,
                    (demo_ws_ids, demo_ws_ids, demo_ws_ids, demo_ws_ids, demo_ws_ids),
                )

                # 3. Xóa Hashtag trước khi xóa Chiến dịch (do workspace_hashtags.campaign_id tham chiếu media_campaigns)
                cur.execute("DELETE FROM workspace_hashtags WHERE workspace_id = ANY(%s::uuid[]);", (demo_ws_ids,))

                # 4. Xóa Chiến dịch, Lịch sử duyệt chiến dịch, Đối tác & Gói truyền thông
                cur.execute("DELETE FROM content_request_completion_jobs WHERE workspace_id = ANY(%s::uuid[]);", (demo_ws_ids,))
                cur.execute(
                    """
                    DELETE FROM campaign_collaborators
                    WHERE media_campaign_id IN (
                        SELECT id FROM media_campaigns
                        WHERE workspace_media_package_id IN (
                            SELECT id FROM workspace_media_packages WHERE workspace_id = ANY(%s::uuid[])
                        )
                    );
                    DELETE FROM campaign_deployments
                    WHERE campaign_id IN (
                        SELECT id FROM media_campaigns
                        WHERE workspace_media_package_id IN (
                            SELECT id FROM workspace_media_packages WHERE workspace_id = ANY(%s::uuid[])
                        )
                    );
                    DELETE FROM campaign_review_events
                    WHERE campaign_id IN (
                        SELECT id FROM media_campaigns
                        WHERE workspace_media_package_id IN (
                            SELECT id FROM workspace_media_packages WHERE workspace_id = ANY(%s::uuid[])
                        )
                    );
                    DELETE FROM campaign_versions
                    WHERE campaign_id IN (
                        SELECT id FROM media_campaigns
                        WHERE workspace_media_package_id IN (
                            SELECT id FROM workspace_media_packages WHERE workspace_id = ANY(%s::uuid[])
                        )
                    );
                    DELETE FROM media_campaigns
                    WHERE workspace_media_package_id IN (
                        SELECT id FROM workspace_media_packages WHERE workspace_id = ANY(%s::uuid[])
                    );
                    UPDATE workspaces SET workspace_media_package_id = NULL WHERE id = ANY(%s::uuid[]);
                    """,
                    (demo_ws_ids, demo_ws_ids, demo_ws_ids, demo_ws_ids, demo_ws_ids, demo_ws_ids),
                )

                cur.execute("SAVEPOINT sp_wmp_clean;")
                try:
                    cur.execute("DELETE FROM workspace_media_packages WHERE workspace_id = ANY(%s::uuid[]);", (demo_ws_ids,))
                    cur.execute("RELEASE SAVEPOINT sp_wmp_clean;")
                except Exception:
                    cur.execute("ROLLBACK TO SAVEPOINT sp_wmp_clean;")

                cur.execute(
                    """
                    DELETE FROM media_packages
                    WHERE agency_id = %s::uuid
                      AND id NOT IN (SELECT package_id FROM workspace_media_packages WHERE package_id IS NOT NULL);
                    DELETE FROM third_party_collaborators
                    WHERE agency_id = %s::uuid
                      AND id NOT IN (SELECT collaborator_id FROM campaign_collaborators);
                    DELETE FROM workspace_templates
                    WHERE agency_id = %s::uuid OR source_workspace_id = ANY(%s::uuid[]);
                    """,
                    (AGENCY_ID, AGENCY_ID, AGENCY_ID, demo_ws_ids),
                )

                # 5. Xóa Lô gửi Email, Danh sách từ chối nhận thư, Lời mời & Chuông thông báo
                admin_notif_ids = [
                    "d7e00000-0000-4000-8000-000000000101",
                    "d7e00000-0000-4000-8000-000000000102",
                ]
                cur.execute(
                    """
                    DELETE FROM mail_deliveries
                    WHERE batch_id IN (
                        SELECT id FROM mail_batches WHERE workspace_id = ANY(%s::uuid[]) OR agency_id = %s::uuid
                    );
                    DELETE FROM mail_batches WHERE workspace_id = ANY(%s::uuid[]) OR agency_id = %s::uuid;
                    DELETE FROM mail_attachments WHERE workspace_id = ANY(%s::uuid[]);
                    DELETE FROM mail_suppressions WHERE workspace_id = ANY(%s::uuid[]) OR agency_id = %s::uuid;
                    DELETE FROM mail_send_quota WHERE scope_id = ANY(%s);
                    DELETE FROM user_notifications WHERE user_id = ANY(%s::uuid[]) OR notification_id = ANY(%s::uuid[]);
                    DELETE FROM admin_email_outbox WHERE notification_id = ANY(%s::uuid[]);
                    DELETE FROM admin_notifications WHERE id = ANY(%s::uuid[]);
                    DELETE FROM agency_invitations WHERE agency_id = %s::uuid OR workspace_id = ANY(%s::uuid[]);
                    DELETE FROM workspace_invitations WHERE workspace_id = ANY(%s::uuid[]);
                    """,
                    (
                        demo_ws_ids,
                        AGENCY_ID,
                        demo_ws_ids,
                        AGENCY_ID,
                        demo_ws_ids,
                        demo_ws_ids,
                        AGENCY_ID,
                        demo_ws_ids + [AGENCY_ID],
                        demo_users,
                        admin_notif_ids,
                        admin_notif_ids,
                        admin_notif_ids,
                        AGENCY_ID,
                        demo_ws_ids,
                        demo_ws_ids,
                    ),
                )

                # 6. Xóa dữ liệu AI Credit Reservations, Hạn mức Workspace, Dung lượng Client Vault & Đơn VietQR phát sinh (B14)
                cur.execute(
                    """
                    DELETE FROM credit_reservation_allocations
                    WHERE agency_id = %s::uuid
                      AND reservation_id NOT IN (SELECT reservation_id FROM credit_operations WHERE reservation_id IS NOT NULL);
                    DELETE FROM ai_credit_reservations
                    WHERE agency_id = %s::uuid
                      AND id NOT IN (SELECT reservation_id FROM credit_operations WHERE reservation_id IS NOT NULL);
                    DELETE FROM workspace_credit_usage WHERE agency_id = %s::uuid AND workspace_id = ANY(%s::uuid[]);
                    DELETE FROM workspace_credit_limits WHERE agency_id = %s::uuid AND workspace_id = ANY(%s::uuid[]);
                    DELETE FROM client_vault_storage_usage WHERE user_id = %s::uuid;
                    """,
                    (AGENCY_ID, AGENCY_ID, AGENCY_ID, demo_ws_ids, AGENCY_ID, demo_ws_ids, client_id),
                )

                # Xóa các credit_grants mẫu chưa ghi vào sổ cái bất biến credit_entries; phần còn lại chuyển về hết hạn (0 khả dụng)
                cur.execute(
                    """
                    DELETE FROM credit_grants
                    WHERE agency_id = %s::uuid
                      AND id NOT IN (SELECT grant_id FROM credit_entries)
                      AND id NOT IN (SELECT grant_id FROM credit_reservation_allocations);
                    UPDATE credit_grants
                    SET expired = expired + available + reserved, available = 0, reserved = 0
                    WHERE agency_id = %s::uuid AND (available > 0 OR reserved > 0);
                    UPDATE agency_credit_wallets
                    SET available_credits = 0, reserved_credits = 0, updated_at = NOW()
                    WHERE agency_id = %s::uuid;
                    """,
                    (AGENCY_ID, AGENCY_ID, AGENCY_ID),
                )

                # Xóa các đơn thanh toán VietQR treo/phát sinh trên SE08 chưa gắn chu kỳ hoặc grant
                cur.execute(
                    """
                    SELECT id::text FROM billing_orders
                    WHERE agency_id = %s::uuid
                      AND id NOT IN (SELECT order_id FROM agency_subscription_periods WHERE order_id IS NOT NULL)
                      AND id NOT IN (SELECT order_id FROM credit_grants WHERE order_id IS NOT NULL)
                      AND id NOT IN (SELECT order_id FROM storage_addon_subscriptions WHERE order_id IS NOT NULL);
                    """,
                    (AGENCY_ID,),
                )
                removable_orders = [r[0] for r in cur.fetchall()]
                if removable_orders:
                    cur.execute(
                        """
                        DELETE FROM subscription_operational_issues WHERE order_id = ANY(%s::uuid[]);
                        DELETE FROM subscription_provider_checks WHERE order_id = ANY(%s::uuid[]);
                        DELETE FROM billing_payment_events WHERE order_id = ANY(%s::uuid[]);
                        DELETE FROM billing_payments WHERE attempt_id IN (SELECT id FROM billing_payment_attempts WHERE order_id = ANY(%s::uuid[]));
                        DELETE FROM billing_payment_attempts WHERE order_id = ANY(%s::uuid[]);
                        DELETE FROM billing_order_fulfillments WHERE order_id = ANY(%s::uuid[]);
                        DELETE FROM billing_orders WHERE id = ANY(%s::uuid[]);
                        """,
                        (
                            removable_orders,
                            removable_orders,
                            removable_orders,
                            removable_orders,
                            removable_orders,
                            removable_orders,
                            removable_orders,
                        ),
                    )

                # 7. Gỡ 2 Workspace phụ mẫu (CloudWork & Tiệm Trà Mùa Thu) để danh sách gọn gàng sau khi xóa Demo
                cur.execute("SAVEPOINT sp_comp_ws;")
                try:
                    cur.execute("DELETE FROM workspace_members WHERE workspace_id = ANY(%s::uuid[]);", (companion_ws_ids,))
                    cur.execute("DELETE FROM workspaces WHERE id = ANY(%s::uuid[]);", (companion_ws_ids,))
                    cur.execute("RELEASE SAVEPOINT sp_comp_ws;")
                except Exception:
                    cur.execute("ROLLBACK TO SAVEPOINT sp_comp_ws;")
                    cur.execute(
                        "UPDATE workspaces SET status = 'SOFT_DELETED', deleted_at = NOW() WHERE id = ANY(%s::uuid[]);",
                        (companion_ws_ids,),
                    )

        print("[OK] Đã xóa sạch toàn bộ dữ liệu mẫu và dữ liệu phát sinh trong PostgreSQL.")
    finally:
        conn.close()
    return resolved_ids


def clean_mongo(mongo_uri: str, mongo_db_name: str, client_user_id: str) -> None:
    """Xóa sạch toàn bộ dữ liệu mẫu và dữ liệu phát sinh trong MongoDB cho các Workspace Demo."""
    try:
        from pymongo import MongoClient
    except ImportError as exc:
        raise RuntimeError("Cần cài đặt pymongo: pip install pymongo") from exc

    demo_ws_ids = [
        WORKSPACE_ID,
        "d7e00000-0000-4000-8000-000000000091",
        "d7e00000-0000-4000-8000-000000000092",
    ]
    client = MongoClient(mongo_uri)
    try:
        try:
            default_db = client.get_default_database()
            db = default_db if default_db is not None else client[mongo_db_name]
        except Exception:
            db = client[mongo_db_name]

        task_ids = [doc["_id"] for doc in db.tasks.find({"workspaceId": {"$in": demo_ws_ids}}, {"_id": 1})]
        deterministic_task_ids = [
            campaign_task_id(CAMPAIGN_ID, f"d7e00000-0000-4000-8000-{701 + i:012d}")
            for i in range(25)
        ] + [TASK_1_ID, SURVEY_TASK_ID]
        task_ids = list(set(task_ids + deterministic_task_ids))
        survey_ids = [doc["_id"] for doc in db.surveys.find({"workspaceId": {"$in": demo_ws_ids}}, {"_id": 1})]
        survey_ids = list(set(survey_ids + [SURVEY_DOC_ID, "d7e00000-0000-4000-8000-000000000805", "d7e00000-0000-4000-8000-000000000806"]))

        db.task_sections.delete_many({"$or": [{"taskId": {"$in": task_ids}}, {"workspaceId": {"$in": demo_ws_ids}}]})
        db.task_section_versions.delete_many({"$or": [{"taskId": {"$in": task_ids}}, {"workspaceId": {"$in": demo_ws_ids}}]})
        db.task_section_events.delete_many({"$or": [{"taskId": {"$in": task_ids}}, {"workspaceId": {"$in": demo_ws_ids}}]})
        db.task_approvals.delete_many({"$or": [{"taskId": {"$in": task_ids}}, {"workspaceId": {"$in": demo_ws_ids}}]})
        db.tasks.delete_many({"workspaceId": {"$in": demo_ws_ids}})
        db.task_comments.delete_many({"workspaceId": {"$in": demo_ws_ids}})
        db.posts.delete_many({"workspace_id": {"$in": demo_ws_ids}})
        db.post_versions.delete_many({"workspace_id": {"$in": demo_ws_ids}})
        db.publish_logs.delete_many({"workspace_id": {"$in": demo_ws_ids}})
        db.material_references.delete_many({"workspace_id": {"$in": demo_ws_ids}})
        db.material_versions.delete_many({"workspace_id": {"$in": demo_ws_ids}})
        db.materials.delete_many(
            {"$or": [{"workspace_id": {"$in": demo_ws_ids}}, {"scope_type": "CLIENT_VAULT", "owner_user_id": client_user_id}]}
        )
        db.material_folders.delete_many(
            {"$or": [{"workspace_id": {"$in": demo_ws_ids}}, {"scope_type": "CLIENT_VAULT", "owner_user_id": client_user_id}]}
        )
        db.client_vault_shares.delete_many(
            {"$or": [{"workspace_id": {"$in": demo_ws_ids}}, {"owner_user_id": client_user_id}]}
        )
        db.social_accounts.delete_many({"workspace_id": {"$in": demo_ws_ids}})
        db.survey_responses.delete_many(
            {"$or": [{"surveyId": {"$in": survey_ids}}, {"workspaceId": {"$in": demo_ws_ids}}]}
        )
        db.surveys.delete_many({"workspaceId": {"$in": demo_ws_ids}})
        db.content_requests.delete_many({"workspaceId": {"$in": demo_ws_ids}})
        db.brand_profiles.delete_many({"workspace_id": {"$in": demo_ws_ids}})
        db.knowledge_documents.delete_many({"workspace_id": {"$in": demo_ws_ids}})
        db.mail_recipient_groups.delete_many({"workspaceId": {"$in": demo_ws_ids}})
        db.mail_templates.delete_many(
            {
                "$or": [
                    {"workspaceId": {"$in": demo_ws_ids}},
                    {"agencyId": AGENCY_ID},
                    {"name": {"$in": ["gg", "test", "Test", "demo", "abc"]}},
                ]
            }
        )
        db.chat_channel_reads.delete_many({"workspaceId": {"$in": demo_ws_ids}})
        db.chat_schedules.delete_many({"workspaceId": {"$in": demo_ws_ids}})
        db.chat_attachments.delete_many({"workspaceId": {"$in": demo_ws_ids}})
        db.chat_channels.delete_many({"workspaceId": {"$in": demo_ws_ids}})
        db.chat_messages.delete_many({"workspaceId": {"$in": demo_ws_ids}})
        db.ai_usage_logs.delete_many({"workspace_id": {"$in": demo_ws_ids}})
        db.report_jobs.delete_many({"workspace_id": {"$in": demo_ws_ids}})
        db.video_projects.delete_many({"workspaceId": {"$in": demo_ws_ids}})

        print(f"[OK] Đã xóa sạch toàn bộ dữ liệu mẫu và dữ liệu phát sinh trong MongoDB ({db.name}).")
    finally:
        client.close()


def clean_redis_trends(redis_url: str) -> None:
    """Xóa bộ nhớ đệm Xu hướng mẫu trong Redis."""
    try:
        import redis as sync_redis
    except ImportError:
        return
    try:
        r = sync_redis.from_url(redis_url, decode_responses=True)
        r.ping()
    except Exception:
        return

    keys_to_delete: list[str] = [
        "trends:FACEBOOK:VN",
        "trends:INSTAGRAM:VN",
        "trends:TIKTOK:VN",
        "trends:THREADS:VN",
    ]
    for k in r.scan_iter("trends:v2:*"):
        keys_to_delete.append(str(k))
    if keys_to_delete:
        r.delete(*keys_to_delete)
    print(f"[OK] Đã xóa sạch {len(keys_to_delete)} khóa xu hướng mẫu trong Redis.")


def json_default(obj: Any) -> Any:
    if isinstance(obj, datetime):
        return obj.strftime("%Y-%m-%dT%H:%M:%SZ")
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def main() -> None:
    default_pg_uri, default_mongo_uri, default_mongo_db = load_default_db_uris()
    default_redis_url = load_default_redis_url()
    parser = argparse.ArgumentParser(description="Prepare BrandHub FPT University 2027 4-Week Live Demo Data")
    parser.add_argument("--apply", action="store_true", help="Thực thi trực tiếp vào PostgreSQL, MongoDB và Redis")
    parser.add_argument("--clean", action="store_true", help="Xóa sạch toàn bộ dữ liệu mẫu và dữ liệu phát sinh sau khi demo")
    parser.add_argument("--pg-uri", default=default_pg_uri, help="PostgreSQL connection URI")
    parser.add_argument("--mongo-uri", default=default_mongo_uri, help="MongoDB connection URI")
    parser.add_argument("--mongo-db", default=default_mongo_db, help="MongoDB database name")
    parser.add_argument("--redis-url", default=default_redis_url, help="Redis connection URI")
    args = parser.parse_args()

    if args.clean:
        resolved_ids = clean_postgres(args.pg_uri)
        clean_mongo(args.mongo_uri, args.mongo_db, resolved_ids["CLIENT"])
        clean_redis_trends(args.redis_url)
        return

    now = datetime.now(timezone.utc)
    pg_bundle = build_postgres_bundle(now)
    preview_mongo = build_mongo_bundle(PG_USER_IDS, now)

    # Trong file JSON preview, rút gọn chuỗi base64 ảnh để file nhẹ, dễ đọc
    preview_copy = json.loads(json.dumps(preview_mongo, default=json_default, ensure_ascii=False))
    for mat in preview_copy.get("materials", []):
        if isinstance(mat.get("url"), str) and mat["url"].startswith("data:"):
            mat["url"] = mat["url"][:64] + "...[base64-jpeg-preview]..."

    out_dir = Path(__file__).resolve().parent
    sql_path = out_dir / "prepare_demo_postgres_preview.sql"
    mongo_path = out_dir / "prepare_demo_mongo_preview.json"

    sql_path.write_text(build_sql_preview_text(pg_bundle), encoding="utf-8")
    mongo_path.write_text(json.dumps(preview_copy, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[PREVIEW] Đã xuất tóm tắt SQL tại  : {sql_path}")
    print(f"[PREVIEW] Đã xuất dữ liệu Mongo tại: {mongo_path}")

    if args.apply:
        resolved_ids = apply_postgres(args.pg_uri, pg_bundle)
        live_mongo_bundle = build_mongo_bundle(resolved_ids, now)
        apply_mongo(args.mongo_uri, args.mongo_db, live_mongo_bundle, resolved_ids["CLIENT"])
        apply_redis_trends(args.redis_url, now)
    else:
        print("\n[INFO] Thêm cờ `--apply` để nạp trực tiếp dữ liệu hoặc `--clean` để xóa sạch dữ liệu sau khi demo.")


if __name__ == "__main__":
    main()
