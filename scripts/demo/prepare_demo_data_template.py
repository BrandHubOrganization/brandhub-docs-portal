#!/usr/bin/env python3
"""
SCRIPT CHI TIẾT CHUẨN BỊ DỮ LIỆU LIVE DEMO BRANDHUB (POSTGRESQL + MONGODB ATLAS)
================================================================================
Kịch bản thực tế hệ sinh thái FPT & 5 Thành viên nhóm đồ án:
  - Đơn vị Agency       : FPT Smart Ads Agency (`359a1839-18c7-48e2-8a68-f5f68c3375b6`)
  - Thương hiệu Client  : Đại học FPT (Tập đoàn FPT)
  - Workspace chung     : FPT University x FPT Smart Ads (`b47477c4-13ad-44ff-8c49-f73f1837461b`)
  - 5 Thành viên Đồ án  :
      1. `Owner`   : Lê Trí Trung       (`user177@demo.brandhub.test`)
      2. `Manager` : Nguyễn Thành Lộc   (`user1@demo.brandhub.test`)
      3. `Creator` : Nguyễn Chơn Phước  (`user13@demo.brandhub.test`)
      4. `Client`  : Nguyễn Minh Tuấn   (`user59@demo.brandhub.test`)
      5. `Admin`   : Hà Văn Ân          (`admin@demo.brandhub.test`)

Đã đối chiếu chính xác 100% với Schema & Logic kiểm tra trong code:
  - `MediaPackage.java` (`media_packages`), `WorkspaceMediaPackage.java` (`workspace_media_packages`),
    `PackageNegotiationEvent.java` (`package_negotiation_events`)
  - `MediaCampaign.java` (`media_campaigns`), `CampaignVersion.java` (`campaign_versions`),
    `CampaignReviewEvent.java` (`campaign_review_events`)
  - `CampaignPlanValidator.java`: Mã UUID của từng `CampaignWorkItem` bắt buộc tính theo công thức
    `UUID.nameUUIDFromBytes("package-deliverable:" + deliverableId + ":" + index)`
  - `CampaignTaskStore.java`: Mã `_id` của từng `TaskDocument` trong MongoDB `tasks` bắt buộc tính theo
    `UUID.nameUUIDFromBytes("campaign:" + campaignId + ":item:" + workItemId)`

Trạng thái: Mặc định xuất file xem trước, truyền `--apply` để đẩy trực tiếp lên PostgreSQL và MongoDB Atlas.
"""

import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
import subprocess
import sys
import uuid

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def java_name_uuid_from_bytes(raw: str) -> str:
    """Tái tạo chính xác hàm `UUID.nameUUIDFromBytes(byte[])` của Java (MD5 UUID v3)."""
    md5_bytes = hashlib.md5(raw.encode("utf-8")).digest()
    return str(uuid.UUID(bytes=md5_bytes, version=3))


# ==============================================================================
# 1. CẤU HÌNH CHI TIẾT DỮ LIỆU DEMO HỆ SINH THÁI FPT CHO 15 BƯỚC (B1 -> B15)
# ==============================================================================

AGENCY_ID = "359a1839-18c7-48e2-8a68-f5f68c3375b6"           # FPT Smart Ads Agency
WORKSPACE_ID = "b47477c4-13ad-44ff-8c49-f73f1837461b"        # FPT University x FPT Smart Ads
CLIENT_PROFILE_ID = "d7e00000-0000-4000-8000-000000000001"   # Đại học FPT (Tập đoàn FPT)

PACKAGE_ID = "d7e00000-0000-4000-8000-000000000200"
WS_PACKAGE_ID = "d7e00000-0000-4000-8000-000000000201"
CAMPAIGN_ID = "d7e00000-0000-4000-8000-000000000301"

# UUID của 5 tài khoản trong PostgreSQL
PG_USER_IDS = {
    "OWNER": "87e97722-97c1-47ff-9d5f-02894e30bed2",     # user177@demo.brandhub.test -> Lê Trí Trung
    "MANAGER": "48a55552-71bd-468c-ba02-fa849eeb7682",   # user1@demo.brandhub.test   -> Nguyễn Thành Lộc
    "CREATOR": "56034372-e963-4717-8dfa-e68e34d34c7a",   # user13@demo.brandhub.test  -> Nguyễn Chơn Phước
    "CLIENT": "b663ffe6-6693-41d3-8df5-27805e4dc8b6",    # user59@demo.brandhub.test  -> Nguyễn Minh Tuấn
    "ADMIN": "90d56307-940b-4bec-820d-0ba39850041c",     # admin@demo.brandhub.test   -> Hà Văn Ân
}

MONGODB_URI = "mongodb+srv://brandhub-mongo:3TfyH74Nz.gxmZH@brandhub.dupoa3v.mongodb.net/?appName=brandhub"
MONGODB_DB = "brandhub"

# 1.1 Năm tài khoản chuẩn tương ứng 5 Thành viên nhóm đồ án trên 5 Cửa sổ Chrome
DEMO_ACCOUNTS = {
    "user177@demo.brandhub.test": {
        "window": "Cửa sổ 1 (Owner)",
        "role": "Owner",
        "full_name": "Lê Trí Trung",
        "scope": "Giám đốc FPT Smart Ads Agency",
    },
    "user1@demo.brandhub.test": {
        "window": "Cửa sổ 2 (Manager)",
        "role": "Manager",
        "full_name": "Nguyễn Thành Lộc",
        "scope": "Quản lý Chiến dịch & Workspace FPT University x FPT Smart Ads",
    },
    "user13@demo.brandhub.test": {
        "window": "Cửa sổ 3 (Creator)",
        "role": "Creator",
        "full_name": "Nguyễn Chơn Phước",
        "scope": "Chuyên viên Sáng tạo Nội dung FPT Smart Ads Agency",
    },
    "user59@demo.brandhub.test": {
        "window": "Cửa sổ 4 (Client)",
        "role": "Client",
        "full_name": "Nguyễn Minh Tuấn",
        "scope": "Đại diện Thương hiệu Đại học FPT (Tập đoàn FPT)",
    },
    "admin@demo.brandhub.test": {
        "window": "Cửa sổ 5 (Admin)",
        "role": "Admin",
        "full_name": "Hà Văn Ân",
        "scope": "Quản trị viên Hệ thống BrandHub Platform",
    },
}

# 1.2 Cấu trúc 3 hạng mục bàn giao (Deliverables) trong Gói truyền thông Đại học FPT
DELIVERABLES = [
    {
        "id": "d7e00000-0000-4000-8000-000000000211",
        "serviceType": "SOCIAL_POST",
        "name": "Bài đăng truyền thông học bổng ngành Vi mạch & Sự kiện AI4VN",
        "quantity": 2,
        "unit": "bài đăng",
        "description": (
            "Viết bài giới thiệu chương trình đào tạo ngành Thiết kế Vi mạch và Trí tuệ nhân tạo tại Đại học FPT, "
            "hưởng ứng mục tiêu 50.000 kỹ sư bán dẫn của Việt Nam đến năm 2030."
        ),
        "acceptanceCriteria": (
            "Nội dung ngắn gọn, nêu rõ mức học bổng Nguyễn Văn Đạo (50% đến 100%) và kỳ thực tập tại FPT Software "
            "từ năm thứ 3, đạt trạng thái PASSED khi kiểm tra an toàn nội dung."
        ),
        "revisionLimit": 3,
    },
    {
        "id": "d7e00000-0000-4000-8000-000000000212",
        "serviceType": "PRESS_RECOMMENDATION",
        "name": "Đề xuất báo chí về chương trình đào tạo nhân lực bán dẫn hưởng ứng mục tiêu quốc gia 2030",
        "quantity": 1,
        "unit": "bản đề xuất",
        "description": "Chuẩn bị thông tin gửi các báo giáo dục và công nghệ trong dịp Ngày hội Trí tuệ Nhân tạo Việt Nam (AI4VN).",
        "acceptanceCriteria": "Có số liệu chỉ tiêu tuyển sinh, thông tin phòng lab bán dẫn tại Hòa Lạc và danh sách báo dự kiến.",
        "revisionLimit": 2,
    },
    {
        "id": "d7e00000-0000-4000-8000-000000000213",
        "serviceType": "WORKSHOP_SUPPORT",
        "name": "Khảo sát nhu cầu học sinh THPT về ngành Vi mạch bán dẫn và Chuyển đổi số tại Việt Nam",
        "quantity": 1,
        "unit": "bảng khảo sát",
        "description": "Khảo sát học sinh lớp 12 tham gia Tuần lễ trải nghiệm công nghệ tại Khu Công nghệ cao Hòa Lạc.",
        "acceptanceCriteria": "Gồm 5 câu hỏi trắc nghiệm ngắn gọn và 1 câu hỏi mở về nguyện vọng nghề nghiệp.",
        "revisionLimit": 2,
    },
]

TASK_TYPE_MAP = {
    "SOCIAL_POST": "POST",
    "WORKSHOP_SUPPORT": "SURVEY",
    "EVENT_PLANNING": "EVENT_PLAN",
    "PRESS_RECOMMENDATION": "PRESS_RECOMMENDATION",
}

FPT_SAMPLE_CAPTIONS = [
    "Đại học FPT mở đăng ký xét tuyển ngành Thiết kế Vi mạch và Trí tuệ nhân tạo năm 2026 tại 5 cơ sở Hà Nội, Đà Nẵng, Quy Nhơn, TP.HCM và Cần Thơ.",
    "Học bổng Nguyễn Văn Đạo tài trợ từ 50% đến 100% học phí toàn khóa cho học sinh THPT đạt thành tích tốt môn Toán, Lý, Tin học.",
    "Sinh viên ngành Vi mạch bán dẫn và AI tại Đại học FPT tham gia học kỳ thực tập doanh nghiệp (OJT) tại FPT Software và FPT Smart Cloud từ năm thứ 3.",
    "Trải nghiệm phòng thực hành chip bán dẫn và khu trình diễn giải pháp AI tại Đại học FPT cơ sở Hòa Lạc trong khuôn khổ sự kiện AI4VN 2026.",
    "Đồng hành cùng mục tiêu phát triển 50.000 kỹ sư công nghệ bán dẫn và trí tuệ nhân tạo cho Việt Nam đến năm 2030.",
]

FPT_CHAT_SCRIPT = [
    ("MANAGER", "GENERAL", "Chào mọi người, tuần này nhóm mình tập trung triển khai chiến dịch tuyển sinh ngành Thiết kế Vi mạch và AI cho Đại học FPT nhé."),
    ("CREATOR", "GENERAL", "Dạ anh Lộc, em đã nhận 2 bài đăng mạng xã hội và đang viết bản nháp thông tin học bổng Nguyễn Văn Đạo."),
    ("CLIENT", "GENERAL", "Cảm ơn team FPT Smart Ads. Bên trường muốn nêu rõ thông tin học kỳ thực tập OJT tại FPT Software từ năm thứ 3 để phụ huynh nắm được."),
    ("MANAGER", "GENERAL", "Dạ anh Tuấn, em đã cập nhật yêu cầu này vào hướng dẫn thương hiệu của chiến dịch."),
    ("CREATOR", "GENERAL", "Hình ảnh phòng lab bán dẫn tại cơ sở Hòa Lạc em lấy trong thư viện tài nguyên của Workspace được không ạ?"),
    ("CLIENT", "GENERAL", "Được nhé Phước, bộ ảnh thực hành tại Khu Công nghệ cao Hòa Lạc mới chụp tháng trước đã tải lên sẵn rồi."),
    ("MANAGER", "GENERAL", "Lịch đăng bài mình vẫn giữ vào sáng thứ Ba và thứ Năm hàng tuần trên cả 4 kênh Facebook, Instagram, TikTok và Threads."),
    ("CREATOR", "GENERAL", "Em vừa hoàn thiện bản nháp bài đăng mở đăng ký học bổng để gửi anh Lộc duyệt nội bộ."),
    ("MANAGER", "GENERAL", "Anh đã xem qua, phần thông tin 5 cơ sở đào tạo viết rất gọn và dễ đọc."),
    ("CREATOR", "GENERAL", "Dạ em đã chạy kiểm tra an toàn nội dung (PASSED) trước khi bấm gửi duyệt."),
    ("MANAGER", "MEDIA_PACKAGE", "Gói truyền thông tuyển sinh hiện bao gồm 2 bài đăng đa nền tảng, 1 đề xuất báo chí dịp AI4VN và 1 khảo sát học sinh THPT."),
    ("CLIENT", "MEDIA_PACKAGE", "Ngân sách gói dịch vụ 18.000.000 VNĐ cho 6 tuần đã được ban tuyển sinh Đại học FPT phê duyệt."),
    ("MANAGER", "MEDIA_PACKAGE", "Cảm ơn anh Tuấn, biên bản thống nhất điều khoản v3 đã lưu trên hệ thống."),
    ("MANAGER", "MEDIA_CAMPAIGN", "Chiến dịch đợt 1 ưu tiên tiếp cận học sinh lớp 12 quan tâm ngành Vi mạch bán dẫn và sự kiện AI4VN."),
    ("CREATOR", "MEDIA_CAMPAIGN", "Em sẽ chuẩn bị thêm định dạng ảnh dọc cho kênh TikTok và Instagram của trường."),
    ("CLIENT", "MEDIA_CAMPAIGN", "Nhờ team gửi báo cáo số lượt tiếp cận và tương tác vào cuối tuần để trường tổng hợp nhé."),
]


def build_package_terms_snapshot(budget_amount: int, note_suffix: str = "") -> dict:
    """Sinh cấu trúc JSON `final_terms` khớp 100% với `MediaPackageServiceImpl.createTermsSnapshot`."""
    return {
        "sourcePackageId": PACKAGE_ID,
        "name": "Gói Truyền thông Tuyển sinh Vi mạch & AI Đại học FPT 2026",
        "durationWeeks": 6,
        "budgetAmount": budget_amount,
        "scopeDescription": (
            "Triển khai truyền thông trong 6 tuần cho đợt tuyển sinh ngành Thiết kế Vi mạch và AI tại Đại học FPT, "
            "gắn với mục tiêu phát triển 50.000 kỹ sư bán dẫn của Việt Nam đến năm 2030"
            + note_suffix
        ),
        "quantityBasis": "TOTAL",
        "offeringDetails": {
            "deliverables": DELIVERABLES,
        },
    }


def build_deterministic_work_items_and_tasks() -> tuple[list[dict], list[dict]]:
    """
    Sinh danh sách `work_items` (cho bảng Postgres `media_campaigns`) và `tasks` (cho MongoDB `tasks`)
    với mã UUID tính theo đúng thuật toán `CampaignPlanValidator.generateWorkItems` và `CampaignTaskStore.taskId`.
    """
    custom_titles = [
        "[Bài #1] Mở đăng ký học bổng ngành Thiết kế Vi mạch & AI tại Đại học FPT",
        "[Bài #2] Tổng kết Ngày hội Trí tuệ Nhân tạo Việt Nam (AI4VN) tại cơ sở Hòa Lạc",
        "[Báo chí #1] Thông cáo chương trình đào tạo nhân lực bán dẫn hưởng ứng mục tiêu quốc gia 2030",
        "[Khảo sát #1] Khảo sát nhu cầu học sinh THPT về ngành Vi mạch bán dẫn và Chuyển đổi số",
    ]
    due_offsets_days = [5, 10, 14, 18]

    work_items = []
    mongo_tasks = []
    idx_counter = 0

    for d in DELIVERABLES:
        for i in range(1, d["quantity"] + 1):
            work_item_id = java_name_uuid_from_bytes(f"package-deliverable:{d['id']}:{i}")
            task_id = java_name_uuid_from_bytes(f"campaign:{CAMPAIGN_ID}:item:{work_item_id}")
            task_type = TASK_TYPE_MAP[d["serviceType"]]
            title = custom_titles[idx_counter]
            due_iso = f"2026-11-{10 + due_offsets_days[idx_counter]:02d}T10:00:00Z"

            work_items.append({
                "id": work_item_id,
                "deliverableId": d["id"],
                "name": title,
                "type": task_type,
                "dueDate": due_iso,
            })

            mongo_tasks.append({
                "_id": task_id,
                "workspaceId": WORKSPACE_ID,
                "campaignId": CAMPAIGN_ID,
                "campaignWorkItemId": work_item_id,
                "type": task_type,
                "name": title,
                "description": d["description"],
                "status": "TODO",
                "assigneeId": PG_USER_IDS["CREATOR"],
                "supervisorId": PG_USER_IDS["MANAGER"],
                "createdBy": PG_USER_IDS["MANAGER"],
                "assignedBy": PG_USER_IDS["MANAGER"],
                "requiresClientApproval": True,
                "approvalRound": 1,
                "workflowRevision": 0,
                "inputReferences": [],
                "subtasks": [],
                "typeMetadata": {
                    "acceptanceCriteria": d["acceptanceCriteria"],
                },
                "sourceType": "CAMPAIGN",
                "sourceRefId": work_item_id,
                "dueDate": due_iso,
                "_class": "com.brandhub.business.document.TaskDocument",
                "seed_tag": "demo-prepared-fpt",
            })
            idx_counter += 1

    return work_items, mongo_tasks


def build_sql_preview() -> str:
    """Sinh toàn bộ kịch bản SQL chuẩn bị dữ liệu Hệ sinh thái FPT & 5 Thành viên Đồ án trên PostgreSQL."""
    terms_v1 = json.dumps(build_package_terms_snapshot(20000000), ensure_ascii=False)
    terms_v2 = json.dumps(
        build_package_terms_snapshot(17500000, " (Đại học FPT đề xuất tối ưu ngân sách 17,5M)"),
        ensure_ascii=False,
    )
    terms_v3 = json.dumps(
        build_package_terms_snapshot(18000000, " (Chốt ngân sách 18M kèm 3 vòng chỉnh sửa bài đăng)"),
        ensure_ascii=False,
    )
    offering_json = json.dumps({"deliverables": DELIVERABLES}, ensure_ascii=False)
    deliverables_json = json.dumps(DELIVERABLES, ensure_ascii=False)
    allocations_json = json.dumps(
        [{"deliverableId": d["id"], "quantity": d["quantity"]} for d in DELIVERABLES],
        ensure_ascii=False,
    )
    work_items, _ = build_deterministic_work_items_and_tasks()
    work_items_json = json.dumps(work_items, ensure_ascii=False)
    timeline_json = json.dumps(
        {
            "startDate": "2026-11-06",
            "endDate": "2026-12-18",
            "milestones": [
                {"name": "Mở đăng ký học bổng ngành Vi mạch & AI tại Đại học FPT", "date": "2026-11-12"},
                {"name": "Sự kiện Ngày hội Trí tuệ Nhân tạo Việt Nam (AI4VN) tại Hòa Lạc", "date": "2026-12-15"},
            ],
        },
        ensure_ascii=False,
    )
    campaign_snapshot_json = json.dumps(
        {
            "name": "Chiến dịch Tuyển sinh Ngành Vi mạch Bán dẫn & Sự kiện AI4VN 2026",
            "strategyDetail": (
                "Giới thiệu chương trình đào tạo ngành Thiết kế Vi mạch và Trí tuệ nhân tạo tại Đại học FPT, "
                "hưởng ứng mục tiêu 50.000 kỹ sư bán dẫn của Việt Nam đến năm 2030 và sự kiện AI4VN tại Hòa Lạc."
            ),
            "brandGuideline": (
                "Ngôn từ rõ ràng, gần gũi với học sinh THPT và phụ huynh. "
                "Nêu cụ thể thông tin học bổng Nguyễn Văn Đạo và kỳ thực tập tại FPT Software, tuân thủ quy định an toàn thông tin."
            ),
            "timeline": json.loads(timeline_json),
            "workItems": work_items,
            "deliverablePlan": DELIVERABLES,
        },
        ensure_ascii=False,
    )

    return f"""-- =============================================================================
-- KỊCH BẢN SQL CHUẨN BỊ DỮ LIỆU DEMO FPT & 5 THÀNH VIÊN ĐỒ ÁN TRÊN POSTGRESQL
-- =============================================================================
ALTER TABLE workspace_media_packages ADD COLUMN IF NOT EXISTS share_token varchar(64);
ALTER TABLE workspace_media_packages ADD COLUMN IF NOT EXISTS share_enabled boolean NOT NULL DEFAULT false;
ALTER TABLE workspace_media_packages ADD COLUMN IF NOT EXISTS manager_led boolean NOT NULL DEFAULT false;
ALTER TABLE workspace_media_packages ADD COLUMN IF NOT EXISTS preparation_status varchar(255) NOT NULL DEFAULT 'READY';
ALTER TABLE workspace_media_packages ADD COLUMN IF NOT EXISTS preparation_actor_id uuid;
ALTER TABLE workspace_media_packages ADD COLUMN IF NOT EXISTS preparation_lease uuid;
ALTER TABLE workspace_media_packages ADD COLUMN IF NOT EXISTS preparation_lease_until timestamptz;
ALTER TABLE workspace_media_packages ADD COLUMN IF NOT EXISTS preparation_error varchar(64);
ALTER TABLE workspace_media_packages ADD COLUMN IF NOT EXISTS last_request_id uuid;
ALTER TABLE workspace_media_packages ADD COLUMN IF NOT EXISTS last_request_hash varchar(64);

DO $$
DECLARE
  v_owner   uuid := (SELECT id FROM users WHERE email = 'user177@demo.brandhub.test');
  v_manager uuid := (SELECT id FROM users WHERE email = 'user1@demo.brandhub.test');
  v_creator uuid := (SELECT id FROM users WHERE email = 'user13@demo.brandhub.test');
  v_client  uuid := (SELECT id FROM users WHERE email = 'user59@demo.brandhub.test');
  v_admin   uuid := (SELECT id FROM users WHERE email = 'admin@demo.brandhub.test');
  v_basic   uuid := (SELECT id FROM billing_plan_versions WHERE code = 'BASIC' ORDER BY version DESC LIMIT 1);
BEGIN
  -- 1. Cập nhật tên 5 Thành viên nhóm đồ án cho 5 tài khoản tương ứng 5 Cửa sổ Chrome
  UPDATE users SET full_name = 'Lê Trí Trung', updated_at = NOW()      WHERE id = v_owner;
  UPDATE users SET full_name = 'Nguyễn Thành Lộc', updated_at = NOW()  WHERE id = v_manager;
  UPDATE users SET full_name = 'Nguyễn Chơn Phước', updated_at = NOW() WHERE id = v_creator;
  UPDATE users SET full_name = 'Nguyễn Minh Tuấn', updated_at = NOW()  WHERE id = v_client;
  UPDATE users SET full_name = 'Hà Văn Ân', updated_at = NOW()         WHERE id = v_admin;

  -- 2. Cập nhật tên Doanh nghiệp hệ sinh thái FPT (FPT Smart Ads Agency & Đại học FPT)
  UPDATE agencies
     SET name = 'FPT Smart Ads Agency',
         description = 'Đơn vị truyền thông số và giải pháp quảng cáo thông minh trực thuộc hệ sinh thái FPT',
         updated_at = NOW()
   WHERE id = '{AGENCY_ID}'::uuid;

  UPDATE workspaces
     SET name = 'FPT University x FPT Smart Ads',
         description = 'Không gian làm việc chung phục vụ Chiến dịch Tuyển sinh Vi mạch Bán dẫn & AI Đại học FPT 2026',
         website = 'https://daihoc.fpt.edu.vn',
         location = 'Khu Công nghệ cao Hòa Lạc, Hà Nội',
         updated_at = NOW()
   WHERE id = '{WORKSPACE_ID}'::uuid;

  INSERT INTO client_profiles (id, user_id, display_name, company, industry, website, location, contact_name, contact_email)
  VALUES (
    '{CLIENT_PROFILE_ID}'::uuid,
    v_client,
    'Đại học FPT',
    'Đại học FPT (Tập đoàn FPT)',
    'Giáo dục Đại học & Đào tạo Công nghệ (Vi mạch Bán dẫn, AI, Kỹ thuật Phần mềm)',
    'https://daihoc.fpt.edu.vn',
    'Khu Công nghệ cao Hòa Lạc, Hà Nội',
    'Nguyễn Minh Tuấn',
    'user59@demo.brandhub.test'
  )
  ON CONFLICT (id) DO UPDATE SET
    user_id = EXCLUDED.user_id,
    display_name = EXCLUDED.display_name,
    company = EXCLUDED.company,
    industry = EXCLUDED.industry,
    website = EXCLUDED.website,
    location = EXCLUDED.location,
    contact_name = EXCLUDED.contact_name,
    contact_email = EXCLUDED.contact_email,
    updated_at = NOW();

  UPDATE workspace_members
     SET client_profile_id = '{CLIENT_PROFILE_ID}'::uuid
   WHERE workspace_id = '{WORKSPACE_ID}'::uuid AND role = 'CLIENT';

  -- 3. Làm sạch các bản ghi ngoài phạm vi đề tài (ẩn gói Livestream/Zalo, giữ nguyên cờ is_template để thỏa mãn chk_media_packages_template_agency_scope)
  UPDATE media_packages
     SET is_available_to_workspaces = FALSE,
         name = CASE WHEN LOWER(name) LIKE '%livestream%' THEN 'Gói Truyền thông Sự kiện & Hội thảo Công nghệ' ELSE name END,
         scope_description = CASE WHEN LOWER(COALESCE(scope_description, '')) LIKE '%livestream%' THEN 'Lên kế hoạch truyền thông sự kiện và hội thảo chuyên đề.' ELSE scope_description END,
         updated_at = NOW()
   WHERE LOWER(name) LIKE '%livestream%'
      OR LOWER(COALESCE(scope_description, '')) LIKE '%livestream%'
      OR LOWER(offering_details::text) LIKE '%livestream%'
      OR LOWER(name) LIKE '%zalo%';

  -- 4. Tạo Gói dịch vụ mẫu của FPT Smart Ads Agency (Bước B1: /agency/.../media-packages)
  INSERT INTO media_packages (
    id, name, is_template, agency_id, custom_workspace_id, source_template_id,
    is_available_to_workspaces, duration_weeks, budget_amount, scope_description,
    offering_details, created_by, created_at, updated_at
  ) VALUES (
    '{PACKAGE_ID}'::uuid,
    'Gói Truyền thông Tuyển sinh Vi mạch & AI Đại học FPT 2026',
    FALSE,
    '{AGENCY_ID}'::uuid,
    NULL,
    NULL,
    TRUE,
    6,
    18000000.00,
    'Triển khai truyền thông trong 6 tuần cho đợt tuyển sinh ngành Thiết kế Vi mạch và AI tại Đại học FPT, gắn với mục tiêu phát triển 50.000 kỹ sư bán dẫn của Việt Nam đến năm 2030.',
    '{offering_json}'::jsonb,
    v_owner,
    NOW() - INTERVAL '5 days',
    NOW() - INTERVAL '2 days'
  ) ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    is_available_to_workspaces = TRUE,
    duration_weeks = EXCLUDED.duration_weeks,
    budget_amount = EXCLUDED.budget_amount,
    scope_description = EXCLUDED.scope_description,
    offering_details = EXCLUDED.offering_details,
    updated_at = NOW();

  -- 5. Gỡ các gói livestream/campaign cũ trên Workspace này (nếu có) và gắn WS_PACKAGE_ID chuẩn
  UPDATE workspaces SET workspace_media_package_id = NULL WHERE id = '{WORKSPACE_ID}'::uuid;

  DELETE FROM media_campaigns
   WHERE workspace_media_package_id IN (
     SELECT id FROM workspace_media_packages WHERE workspace_id = '{WORKSPACE_ID}'::uuid
   ) AND id <> '{CAMPAIGN_ID}'::uuid;

  DELETE FROM workspace_media_packages
   WHERE workspace_id = '{WORKSPACE_ID}'::uuid
     AND id <> '{WS_PACKAGE_ID}'::uuid
     AND NOT EXISTS (
       SELECT 1 FROM package_negotiation_events pne WHERE pne.workspace_media_package_id = workspace_media_packages.id
     );

  INSERT INTO workspace_media_packages (
    id, workspace_id, package_id, negotiation_status, final_terms, previous_terms,
    terms_version, client_proposal_count, approved_by_agency_at, approved_by_client_at,
    preparation_status, created_at, updated_at
  ) VALUES (
    '{WS_PACKAGE_ID}'::uuid,
    '{WORKSPACE_ID}'::uuid,
    '{PACKAGE_ID}'::uuid,
    'APPROVED',
    '{terms_v3}'::jsonb,
    '{terms_v2}'::jsonb,
    3,
    1,
    NOW() - INTERVAL '2 days',
    NOW() - INTERVAL '2 days',
    'READY',
    NOW() - INTERVAL '4 days',
    NOW() - INTERVAL '2 days'
  ) ON CONFLICT (workspace_id) DO UPDATE SET
    package_id = EXCLUDED.package_id,
    negotiation_status = 'APPROVED',
    final_terms = EXCLUDED.final_terms,
    previous_terms = EXCLUDED.previous_terms,
    terms_version = 3,
    client_proposal_count = 1,
    approved_by_agency_at = EXCLUDED.approved_by_agency_at,
    approved_by_client_at = EXCLUDED.approved_by_client_at,
    preparation_status = 'READY',
    updated_at = NOW();

  UPDATE workspaces
     SET workspace_media_package_id = (SELECT id FROM workspace_media_packages WHERE workspace_id = '{WORKSPACE_ID}'::uuid)
   WHERE id = '{WORKSPACE_ID}'::uuid;

  INSERT INTO package_negotiation_events (id, workspace_media_package_id, terms_version, action, actor_id, actor_role, note, terms_snapshot, created_at)
  VALUES
    (gen_random_uuid(), (SELECT id FROM workspace_media_packages WHERE workspace_id = '{WORKSPACE_ID}'::uuid), 1, 'BASELINE', NULL, NULL, 'Khởi tạo gói truyền thông tuyển sinh từ danh mục của FPT Smart Ads Agency.', '{terms_v1}'::jsonb, NOW() - INTERVAL '4 days'),
    (gen_random_uuid(), (SELECT id FROM workspace_media_packages WHERE workspace_id = '{WORKSPACE_ID}'::uuid), 2, 'REQUEST_CHANGE', v_client, 'CLIENT', 'Đại học FPT đề xuất điều chỉnh ngân sách xuống 17.500.000 VNĐ và giữ nguyên tiến độ 6 tuần.', '{terms_v2}'::jsonb, NOW() - INTERVAL '3 days'),
    (gen_random_uuid(), (SELECT id FROM workspace_media_packages WHERE workspace_id = '{WORKSPACE_ID}'::uuid), 3, 'COUNTER_OFFER', v_manager, 'MANAGER', 'FPT Smart Ads chốt mức ngân sách ưu đãi nội bộ FPT 18.000.000 VNĐ, hỗ trợ tối đa 3 vòng chỉnh sửa cho mỗi bài đăng.', '{terms_v3}'::jsonb, NOW() - INTERVAL '2 days')
  ON CONFLICT (workspace_media_package_id, terms_version) DO NOTHING;

  -- 6. Tạo Chiến dịch Tuyển sinh Đại học FPT ở trạng thái APPROVED (Sẵn sàng cho cả luồng duyệt/triển khai và luồng Task)
  DELETE FROM campaign_deployments WHERE campaign_id = '{CAMPAIGN_ID}'::uuid;
  DELETE FROM campaign_review_events WHERE campaign_id = '{CAMPAIGN_ID}'::uuid;
  DELETE FROM campaign_versions WHERE campaign_id = '{CAMPAIGN_ID}'::uuid;

  INSERT INTO media_campaigns (
    id, workspace_media_package_id, name, strategy_detail, brand_guideline,
    timeline, package_terms_snapshot, package_terms_version, allocations,
    deliverable_plan, work_items, content_version, row_version, status,
    approved_by_agency_at, approved_by_agency_id, approved_by_agency_version,
    approved_by_client_at, approved_by_client_id, approved_by_client_version,
    created_at, updated_at
  ) VALUES (
    '{CAMPAIGN_ID}'::uuid,
    (SELECT id FROM workspace_media_packages WHERE workspace_id = '{WORKSPACE_ID}'::uuid),
    'Chiến dịch Tuyển sinh Ngành Vi mạch Bán dẫn & Sự kiện AI4VN 2026',
    'Giới thiệu chương trình đào tạo ngành Thiết kế Vi mạch và Trí tuệ nhân tạo tại Đại học FPT, hưởng ứng mục tiêu 50.000 kỹ sư bán dẫn của Việt Nam đến năm 2030 và sự kiện AI4VN tại Hòa Lạc.',
    'Ngôn từ rõ ràng, gần gũi với học sinh THPT và phụ huynh. Nêu cụ thể thông tin học bổng Nguyễn Văn Đạo và kỳ thực tập tại FPT Software, tuân thủ quy định an toàn thông tin.',
    '{timeline_json}'::jsonb,
    '{terms_v3}'::jsonb,
    3,
    '{allocations_json}'::jsonb,
    '{deliverables_json}'::jsonb,
    '{work_items_json}'::jsonb,
    1,
    0,
    'APPROVED',
    NOW() - INTERVAL '1 day', v_manager, 1,
    NOW() - INTERVAL '1 day', v_client, 1,
    NOW() - INTERVAL '2 days', NOW() - INTERVAL '1 day'
  ) ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    strategy_detail = EXCLUDED.strategy_detail,
    brand_guideline = EXCLUDED.brand_guideline,
    timeline = EXCLUDED.timeline,
    package_terms_snapshot = EXCLUDED.package_terms_snapshot,
    package_terms_version = 3,
    allocations = EXCLUDED.allocations,
    deliverable_plan = EXCLUDED.deliverable_plan,
    work_items = EXCLUDED.work_items,
    content_version = 1,
    status = 'APPROVED',
    approved_by_agency_at = EXCLUDED.approved_by_agency_at,
    approved_by_agency_id = v_manager,
    approved_by_agency_version = 1,
    approved_by_client_at = EXCLUDED.approved_by_client_at,
    approved_by_client_id = v_client,
    approved_by_client_version = 1,
    completed_at = NULL,
    completed_by = NULL,
    completion_reason = NULL,
    completion_task_summary = NULL,
    updated_at = NOW();

  INSERT INTO campaign_versions (id, campaign_id, content_version, snapshot, created_by, created_at)
  VALUES (gen_random_uuid(), '{CAMPAIGN_ID}'::uuid, 1, '{campaign_snapshot_json}'::jsonb, v_manager, NOW() - INTERVAL '2 days')
  ON CONFLICT ON CONSTRAINT uq_campaign_versions_campaign_version DO NOTHING;

  INSERT INTO campaign_review_events (id, campaign_id, content_version, actor_id, actor_side, event_type, comment, created_at)
  VALUES
    (gen_random_uuid(), '{CAMPAIGN_ID}'::uuid, 1, v_client, 'CLIENT', 'FEEDBACK', 'Kế hoạch truyền thông ngành Thiết kế Vi mạch & Học bổng Nguyễn Văn Đạo trên 4 nền tảng rất sát thực tế, đồng ý triển khai.', NOW() - INTERVAL '30 hours'),
    (gen_random_uuid(), '{CAMPAIGN_ID}'::uuid, 1, v_manager, 'AGENCY', 'APPROVE', NULL, NOW() - INTERVAL '25 hours'),
    (gen_random_uuid(), '{CAMPAIGN_ID}'::uuid, 1, v_client, 'CLIENT', 'APPROVE', NULL, NOW() - INTERVAL '24 hours');

  -- 7. Tạo phiên bản gói PLUS (version = 2) với giá 2.000 VNĐ (tuân thủ trigger bất biến billing_plan_version_immutable)
  --    và đưa FPT Smart Ads Agency về gói BASIC để sẵn sàng quét VietQR SePay ở Bước B14
  UPDATE billing_plan_versions SET is_sellable = FALSE WHERE code = 'PLUS' AND version = 1;

  INSERT INTO billing_plan_versions (
    code, version, display_name, price_monthly, currency,
    max_active_workspaces, max_internal_members, max_clients,
    storage_limit_bytes, monthly_ai_credits, max_concurrent_ai_jobs,
    version_retention_days, trash_retention_days, activity_retention_days,
    features, is_sellable
  )
  SELECT
    'PLUS', 2, 'Plus', 2000, 'VND',
    max_active_workspaces, max_internal_members, max_clients,
    storage_limit_bytes, monthly_ai_credits, max_concurrent_ai_jobs,
    version_retention_days, trash_retention_days, activity_retention_days,
    features, TRUE
  FROM billing_plan_versions
  WHERE code = 'PLUS' AND version = 1
  ON CONFLICT (code, version) DO UPDATE SET is_sellable = TRUE;

  UPDATE agency_subscriptions
     SET plan_version_id = v_basic,
         status = 'ACTIVE',
         updated_at = NOW()
   WHERE agency_id = '{AGENCY_ID}'::uuid;
END $$;
"""


def apply_postgres(sql_text: str) -> None:
    """Thực thi kịch bản SQL trực tiếp vào container `brandhub-postgres`."""
    print("\n[POSTGRES] Đang đẩy dữ liệu vào container `brandhub-postgres` (DB: brandhub)...")
    proc = subprocess.run(
        ["docker", "exec", "-i", "brandhub-postgres", "psql", "-v", "ON_ERROR_STOP=1", "-U", "brandhub", "-d", "brandhub"],
        input=sql_text.encode("utf-8"),
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"Lỗi thực thi PostgreSQL:\n{proc.stderr.decode('utf-8', errors='replace')}")
    print("[POSTGRES] Đã cập nhật thành công PostgreSQL!")


def apply_mongo(mongo_tasks: list[dict]) -> None:
    """Thực thi đồng bộ toàn bộ dữ liệu demo FPT & 5 Thành viên lên MongoDB Atlas."""
    from pymongo import MongoClient

    print(f"\n[MONGODB] Đang kết nối tới MongoDB Atlas (DB: {MONGODB_DB})...")
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=10000)
    db = client[MONGODB_DB]
    now = datetime.now(timezone.utc)

    # 1. Cập nhật tên 5 thành viên trong collection `users` của MongoDB
    for email, info in DEMO_ACCOUNTS.items():
        db.users.update_many(
            {"email": email},
            {"$set": {"full_name": info["full_name"], "updated_at": now}},
        )
    print("  [1/6] Đã cập nhật họ tên 5 thành viên nhóm đồ án trong `db.users`.")

    # 2. Xóa các task nháp "Untitled post" và cập nhật 24 task biểu đồ sang thương hiệu Đại học FPT
    del_untitled = db.tasks.delete_many({"workspaceId": WORKSPACE_ID, "name": "Untitled post"})
    for doc in db.tasks.find({"workspaceId": WORKSPACE_ID, "name": {"$regex": "TH True Milk"}}):
        new_name = doc["name"].replace("TH True Milk", "Đại học FPT")
        db.tasks.update_one(
            {"_id": doc["_id"]},
            {
                "$set": {
                    "name": new_name,
                    "description": "Công việc truyền thông định kỳ của Workspace FPT University x FPT Smart Ads.",
                }
            },
        )
    # Upsert 4 công việc chiến dịch theo mã UUID cố định (UUID v3)
    for t in mongo_tasks:
        due_dt = datetime.fromisoformat(t["dueDate"].replace("Z", "+00:00"))
        doc_to_save = dict(t)
        doc_to_save["dueDate"] = due_dt
        doc_to_save["plannedStartDate"] = now
        doc_to_save["createdAt"] = now - timedelta(days=1)
        doc_to_save["updatedAt"] = now
        doc_to_save["assignedAt"] = now - timedelta(hours=12)
        db.tasks.replace_one({"_id": doc_to_save["_id"]}, doc_to_save, upsert=True)
    print(f"  [2/6] Đã đồng bộ 4 Task chiến dịch FPT (xóa {del_untitled.deleted_count} task nháp thừa) trong `db.tasks`.")

    # 3. Cập nhật 4 tài khoản mạng xã hội (`FACEBOOK`, `INSTAGRAM`, `TIKTOK`, `THREADS`) sang Đại học FPT
    social_mapping = {
        "FACEBOOK": ("fb-fptuniversity-page", "FPT University Official"),
        "INSTAGRAM": ("ig-fptuniversity-biz", "fptuniversity.official"),
        "TIKTOK": ("tt-fptuniversity-vn", "fptuniversity.vn"),
        "THREADS": ("th-fptuniversity-official", "fptuniversity.official"),
    }
    for platform, (acc_id, acc_name) in social_mapping.items():
        db.social_accounts.update_many(
            {"workspace_id": WORKSPACE_ID, "platform": platform},
            {
                "$set": {
                    "account_id": acc_id,
                    "account_name": acc_name,
                    "client_id": "demo-client-fpt-university",
                    "is_active": True,
                    "token_status": "ACTIVE",
                    "updated_at": now,
                }
            },
        )
    print("  [3/6] Đã cập nhật 4 tài khoản mạng xã hội (Facebook, Instagram, TikTok, Threads) sang `FPT University Official`.")

    # 4. Cập nhật 16 tin nhắn trao đổi trong `db.chat_messages` với tên thật 5 thành viên & nội dung tuyển sinh FPT
    role_display = {
        "MANAGER": "Nguyễn Thành Lộc",
        "CREATOR": "Nguyễn Chơn Phước",
        "CLIENT": "Nguyễn Minh Tuấn",
        "OWNER": "Lê Trí Trung",
    }
    chat_docs = list(db.chat_messages.find({"workspaceId": WORKSPACE_ID}).sort("createdAt", 1))
    for idx, cdoc in enumerate(chat_docs):
        script_role, script_ctx, script_text = FPT_CHAT_SCRIPT[idx % len(FPT_CHAT_SCRIPT)]
        current_role = cdoc.get("senderRole", script_role)
        upd_fields = {
            "senderDisplayName": role_display.get(current_role, "Nguyễn Thành Lộc"),
            "content": script_text,
        }
        if cdoc.get("contextType") == "MEDIA_PACKAGE":
            upd_fields["contextId"] = WS_PACKAGE_ID
        elif cdoc.get("contextType") == "MEDIA_CAMPAIGN":
            upd_fields["contextId"] = CAMPAIGN_ID
        db.chat_messages.update_one({"_id": cdoc["_id"]}, {"$set": upd_fields})
    print(f"  [4/6] Đã cập nhật {len(chat_docs)} tin nhắn trong `db.chat_messages` sang tên thành viên và kịch bản Đại học FPT.")

    # 5. Cập nhật các bài đăng mẫu trong `db.posts` và `db.post_versions` sang nội dung tuyển sinh Vi mạch & AI4VN
    posts_in_ws = list(db.posts.find({"workspace_id": WORKSPACE_ID}))
    for idx, pdoc in enumerate(posts_in_ws):
        caption = FPT_SAMPLE_CAPTIONS[idx % len(FPT_SAMPLE_CAPTIONS)]
        hashtags = ["#DaiHocFPT", "#ViMachBanDan", "#AI4VN", "#HocBongNguyenVanDao"]
        db.posts.update_one(
            {"_id": pdoc["_id"]},
            {"$set": {"content_text": caption, "hashtags": hashtags, "updated_at": now}},
        )
        content_hash = hashlib.sha256(caption.encode("utf-8")).hexdigest()
        db.post_versions.update_many(
            {"post_id": str(pdoc["_id"])},
            {"$set": {"content_text": caption, "hashtags": hashtags, "content_hash": content_hash}},
        )
    print(f"  [5/6] Đã cập nhật {len(posts_in_ws)} bài đăng mẫu trong `db.posts` & `db.post_versions` sang nội dung Đại học FPT.")

    # 6. Đồng bộ hồ sơ thương hiệu RAG trong `db.brand_profiles`
    db.brand_profiles.replace_one(
        {"workspace_id": WORKSPACE_ID},
        {
            "workspace_id": WORKSPACE_ID,
            "brand_name": "Đại học FPT (Tập đoàn FPT)",
            "industry": "Giáo dục Đại học & Đào tạo Công nghệ (Vi mạch Bán dẫn, AI, Kỹ thuật Phần mềm)",
            "tone_of_voice": "Rõ ràng, gần gũi với học sinh THPT và phụ huynh, thông tin chính xác về học bổng và thực tập.",
            "target_audience": "Học sinh THPT lớp 12 trên toàn quốc và phụ huynh quan tâm ngành Thiết kế Vi mạch, Trí tuệ nhân tạo.",
            "key_messages": [
                "Chương trình đào tạo ngành Thiết kế Vi mạch và Trí tuệ nhân tạo tại 5 cơ sở Hà Nội, Đà Nẵng, Quy Nhơn, TP.HCM và Cần Thơ.",
                "Quỹ học bổng Nguyễn Văn Đạo hỗ trợ từ 50% đến 100% học phí toàn khóa.",
                "100% sinh viên tham gia kỳ thực tập tại doanh nghiệp (OJT) từ học kỳ 6 tại FPT Software và FPT Smart Cloud.",
                "Hưởng ứng mục tiêu quốc gia đào tạo 50.000 kỹ sư bán dẫn và AI đến năm 2030.",
            ],
            "updated_at": now,
        },
        upsert=True,
    )
    print("  [6/6] Đã đồng bộ hồ sơ thương hiệu `Đại học FPT (Tập đoàn FPT)` trong `db.brand_profiles`.")


def main():
    parser = argparse.ArgumentParser(description="Chi tiết hóa và đồng bộ dữ liệu Live Demo BrandHub (FPT Ecosystem & 5 Team Members)")
    parser.add_argument(
        "--export-sql",
        default="prepare_demo_postgres_preview.sql",
        help="Xuất file SQL xem trước để kiểm tra (mặc định: prepare_demo_postgres_preview.sql)",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Thực thi đẩy trực tiếp dữ liệu lên PostgreSQL và MongoDB Atlas",
    )
    args = parser.parse_args()

    work_items, mongo_tasks = build_deterministic_work_items_and_tasks()
    sql_text = build_sql_preview()

    out_sql_path = args.export_sql
    with open(out_sql_path, "w", encoding="utf-8") as f:
        f.write(sql_text)

    out_mongo_path = out_sql_path.replace("postgres_preview.sql", "mongo_preview.json")
    mongo_preview_doc = {
        "database": "brandhub (MongoDB Atlas)",
        "workspaceId": WORKSPACE_ID,
        "workspaceName": "FPT University x FPT Smart Ads",
        "agencyName": "FPT Smart Ads Agency",
        "clientBrandName": "Đại học FPT (Tập đoàn FPT)",
        "campaignId": CAMPAIGN_ID,
        "team_members": DEMO_ACCOUNTS,
        "tasks_to_upsert": mongo_tasks,
        "chat_messages_sender_display_name_updates": {
            "OWNER": "Lê Trí Trung",
            "MANAGER": "Nguyễn Thành Lộc",
            "CREATOR": "Nguyễn Chơn Phước",
            "CLIENT": "Nguyễn Minh Tuấn",
            "ADMIN": "Hà Văn Ân",
        },
    }
    with open(out_mongo_path, "w", encoding="utf-8") as f:
        json.dump(mongo_preview_doc, f, ensure_ascii=False, indent=2)

    print("=" * 84)
    print("BẢN CHI TIẾT DỮ LIỆU DEMO HỆ SINH THÁI FPT & 5 THÀNH VIÊN ĐỒ ÁN")
    print("=" * 84)
    print(f"1. Đã xuất kịch bản SQL Postgres đầy đủ ra file : {out_sql_path}")
    print(f"2. Đã xuất tài liệu JSON MongoDB đầy đủ ra file : {out_mongo_path}")
    print("\n3. Danh sách 5 Thành viên Nhóm Đồ án theo 5 Vai trò chuẩn:")
    for email, info in DEMO_ACCOUNTS.items():
        print(f"   - {info['window']:18s} | {info['role']:8s} | {info['full_name']:18s} | {email} ({info['scope']})")
    print("\n4. Bảng đối chiếu mã UUID cố định (UUID v3) cho 4 Hạng mục -> Công việc:")
    for i, (wi, mt) in enumerate(zip(work_items, mongo_tasks), start=1):
        print(f"   [{i}] {wi['name']}")
        print(f"       - Deliverable ID (Postgres) : {wi['deliverableId']}")
        print(f"       - WorkItem ID    (Postgres) : {wi['id']}")
        print(f"       - Task _id       (MongoDB)  : {mt['_id']}  (type={mt['type']}, due={wi['dueDate']})")

    if args.apply:
        apply_postgres(sql_text)
        apply_mongo(mongo_tasks)
        print("\n" + "=" * 84)
        print("HOÀN TẤT ĐỒNG BỘ DỮ LIỆU DEMO LÊN CẢ POSTGRESQL VÀ MONGODB ATLAS!")
        print("=" * 84)


if __name__ == "__main__":
    main()
