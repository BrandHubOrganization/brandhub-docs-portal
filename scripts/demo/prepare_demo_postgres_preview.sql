-- =============================================================================
-- BẢN XEM TRƯỚC SQL CHUẨN BỊ DỮ LIỆU DEMO FPT & 5 THÀNH VIÊN ĐỒ ÁN (CHƯA CHẠY LÊN DB)
-- =============================================================================
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

  -- 2. Cập nhật tên Doanh nghiệp hệ sinh thái FPT (FPT Smart Ads Agency & FPT University – Đại học FPT)
  UPDATE agencies
     SET name = 'FPT Smart Ads Agency',
         description = 'Đơn vị truyền thông số & giải pháp quảng cáo thông minh trực thuộc hệ sinh thái FPT',
         updated_at = NOW()
   WHERE id = '359a1839-18c7-48e2-8a68-f5f68c3375b6'::uuid;

  UPDATE workspaces
     SET name = 'FPT University x FPT Smart Ads',
         description = 'Không gian làm việc chung phục vụ Chiến dịch Tuyển sinh & Công nghệ AI Đại học FPT 2026',
         updated_at = NOW()
   WHERE id = 'b47477c4-13ad-44ff-8c49-f73f1837461b'::uuid;

  UPDATE client_profiles
     SET company_name = 'FPT University – Đại học FPT (Tập đoàn FPT)',
         industry = 'Giáo dục Đại học & Đào tạo Công nghệ (AI, Bán dẫn, Kỹ thuật Phần mềm)',
         updated_at = NOW()
   WHERE workspace_id = 'b47477c4-13ad-44ff-8c49-f73f1837461b'::uuid;

  -- 3. Làm sạch các bản ghi ngoài phạm vi đề tài (ẩn gói Livestream/Zalo)
  UPDATE media_packages
     SET is_available_to_workspaces = FALSE,
         is_template = FALSE,
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
    'd7e00000-0000-4000-8000-000000000200'::uuid,
    'Gói Truyền thông Tuyển sinh Vi mạch & AI Đại học FPT 2026',
    FALSE,
    '359a1839-18c7-48e2-8a68-f5f68c3375b6'::uuid,
    NULL,
    NULL,
    TRUE,
    6,
    18000000.00,
    'Triển khai truyền thông trong 6 tuần cho đợt tuyển sinh ngành Thiết kế Vi mạch và AI tại Đại học FPT, gắn với mục tiêu phát triển 50.000 kỹ sư bán dẫn của Việt Nam đến năm 2030.',
    '{"deliverables": [{"id": "d7e00000-0000-4000-8000-000000000211", "serviceType": "SOCIAL_POST", "name": "Bài đăng truyền thông học bổng ngành Vi mạch & Sự kiện AI4VN", "quantity": 2, "unit": "bài đăng", "description": "Viết bài giới thiệu chương trình đào tạo ngành Thiết kế Vi mạch và Trí tuệ nhân tạo tại Đại học FPT, hưởng ứng mục tiêu 50.000 kỹ sư bán dẫn của Việt Nam đến năm 2030.", "acceptanceCriteria": "Nội dung ngắn gọn, nêu rõ mức học bổng Nguyễn Văn Đạo (50% đến 100%) và kỳ thực tập tại FPT Software từ năm thứ 3, đạt trạng thái PASSED khi kiểm tra an toàn nội dung.", "revisionLimit": 3}, {"id": "d7e00000-0000-4000-8000-000000000212", "serviceType": "PRESS_RECOMMENDATION", "name": "Đề xuất báo chí về chương trình đào tạo nhân lực bán dẫn hưởng ứng mục tiêu quốc gia 2030", "quantity": 1, "unit": "bản đề xuất", "description": "Chuẩn bị thông tin gửi các báo giáo dục và công nghệ trong dịp Ngày hội Trí tuệ Nhân tạo Việt Nam (AI4VN).", "acceptanceCriteria": "Có số liệu chỉ tiêu tuyển sinh, thông tin phòng lab bán dẫn tại Hòa Lạc và danh sách báo dự kiến.", "revisionLimit": 2}, {"id": "d7e00000-0000-4000-8000-000000000213", "serviceType": "WORKSHOP_SUPPORT", "name": "Khảo sát nhu cầu học sinh THPT về ngành Vi mạch bán dẫn và Chuyển đổi số tại Việt Nam", "quantity": 1, "unit": "bảng khảo sát", "description": "Khảo sát học sinh lớp 12 tham gia Tuần lễ trải nghiệm công nghệ tại Khu Công nghệ cao Hòa Lạc.", "acceptanceCriteria": "Gồm 5 câu hỏi trắc nghiệm ngắn gọn và 1 câu hỏi mở về nguyện vọng nghề nghiệp.", "revisionLimit": 2}]}'::jsonb,
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

  -- 5. Gắn Gói dịch vụ vào Workspace FPT University x FPT Smart Ads ở trạng thái APPROVED (Bước B2)
  INSERT INTO workspace_media_packages (
    id, workspace_id, package_id, negotiation_status, final_terms, previous_terms,
    terms_version, client_proposal_count, approved_by_agency_at, approved_by_client_at,
    created_at, updated_at
  ) VALUES (
    'd7e00000-0000-4000-8000-000000000201'::uuid,
    'b47477c4-13ad-44ff-8c49-f73f1837461b'::uuid,
    'd7e00000-0000-4000-8000-000000000200'::uuid,
    'APPROVED',
    '{"sourcePackageId": "d7e00000-0000-4000-8000-000000000200", "name": "Gói Truyền thông Tuyển sinh Vi mạch & AI Đại học FPT 2026", "durationWeeks": 6, "budgetAmount": 18000000, "scopeDescription": "Triển khai truyền thông trong 6 tuần cho đợt tuyển sinh ngành Thiết kế Vi mạch và AI tại Đại học FPT, gắn với mục tiêu phát triển 50.000 kỹ sư bán dẫn của Việt Nam đến năm 2030 (Chốt ngân sách 18M kèm 3 vòng chỉnh sửa bài đăng)", "quantityBasis": "TOTAL", "offeringDetails": {"deliverables": [{"id": "d7e00000-0000-4000-8000-000000000211", "serviceType": "SOCIAL_POST", "name": "Bài đăng truyền thông học bổng ngành Vi mạch & Sự kiện AI4VN", "quantity": 2, "unit": "bài đăng", "description": "Viết bài giới thiệu chương trình đào tạo ngành Thiết kế Vi mạch và Trí tuệ nhân tạo tại Đại học FPT, hưởng ứng mục tiêu 50.000 kỹ sư bán dẫn của Việt Nam đến năm 2030.", "acceptanceCriteria": "Nội dung ngắn gọn, nêu rõ mức học bổng Nguyễn Văn Đạo (50% đến 100%) và kỳ thực tập tại FPT Software từ năm thứ 3, đạt trạng thái PASSED khi kiểm tra an toàn nội dung.", "revisionLimit": 3}, {"id": "d7e00000-0000-4000-8000-000000000212", "serviceType": "PRESS_RECOMMENDATION", "name": "Đề xuất báo chí về chương trình đào tạo nhân lực bán dẫn hưởng ứng mục tiêu quốc gia 2030", "quantity": 1, "unit": "bản đề xuất", "description": "Chuẩn bị thông tin gửi các báo giáo dục và công nghệ trong dịp Ngày hội Trí tuệ Nhân tạo Việt Nam (AI4VN).", "acceptanceCriteria": "Có số liệu chỉ tiêu tuyển sinh, thông tin phòng lab bán dẫn tại Hòa Lạc và danh sách báo dự kiến.", "revisionLimit": 2}, {"id": "d7e00000-0000-4000-8000-000000000213", "serviceType": "WORKSHOP_SUPPORT", "name": "Khảo sát nhu cầu học sinh THPT về ngành Vi mạch bán dẫn và Chuyển đổi số tại Việt Nam", "quantity": 1, "unit": "bảng khảo sát", "description": "Khảo sát học sinh lớp 12 tham gia Tuần lễ trải nghiệm công nghệ tại Khu Công nghệ cao Hòa Lạc.", "acceptanceCriteria": "Gồm 5 câu hỏi trắc nghiệm ngắn gọn và 1 câu hỏi mở về nguyện vọng nghề nghiệp.", "revisionLimit": 2}]}}'::jsonb,
    '{"sourcePackageId": "d7e00000-0000-4000-8000-000000000200", "name": "Gói Truyền thông Tuyển sinh Vi mạch & AI Đại học FPT 2026", "durationWeeks": 6, "budgetAmount": 17500000, "scopeDescription": "Triển khai truyền thông trong 6 tuần cho đợt tuyển sinh ngành Thiết kế Vi mạch và AI tại Đại học FPT, gắn với mục tiêu phát triển 50.000 kỹ sư bán dẫn của Việt Nam đến năm 2030 (Đại học FPT đề xuất tối ưu ngân sách 17,5M)", "quantityBasis": "TOTAL", "offeringDetails": {"deliverables": [{"id": "d7e00000-0000-4000-8000-000000000211", "serviceType": "SOCIAL_POST", "name": "Bài đăng truyền thông học bổng ngành Vi mạch & Sự kiện AI4VN", "quantity": 2, "unit": "bài đăng", "description": "Viết bài giới thiệu chương trình đào tạo ngành Thiết kế Vi mạch và Trí tuệ nhân tạo tại Đại học FPT, hưởng ứng mục tiêu 50.000 kỹ sư bán dẫn của Việt Nam đến năm 2030.", "acceptanceCriteria": "Nội dung ngắn gọn, nêu rõ mức học bổng Nguyễn Văn Đạo (50% đến 100%) và kỳ thực tập tại FPT Software từ năm thứ 3, đạt trạng thái PASSED khi kiểm tra an toàn nội dung.", "revisionLimit": 3}, {"id": "d7e00000-0000-4000-8000-000000000212", "serviceType": "PRESS_RECOMMENDATION", "name": "Đề xuất báo chí về chương trình đào tạo nhân lực bán dẫn hưởng ứng mục tiêu quốc gia 2030", "quantity": 1, "unit": "bản đề xuất", "description": "Chuẩn bị thông tin gửi các báo giáo dục và công nghệ trong dịp Ngày hội Trí tuệ Nhân tạo Việt Nam (AI4VN).", "acceptanceCriteria": "Có số liệu chỉ tiêu tuyển sinh, thông tin phòng lab bán dẫn tại Hòa Lạc và danh sách báo dự kiến.", "revisionLimit": 2}, {"id": "d7e00000-0000-4000-8000-000000000213", "serviceType": "WORKSHOP_SUPPORT", "name": "Khảo sát nhu cầu học sinh THPT về ngành Vi mạch bán dẫn và Chuyển đổi số tại Việt Nam", "quantity": 1, "unit": "bảng khảo sát", "description": "Khảo sát học sinh lớp 12 tham gia Tuần lễ trải nghiệm công nghệ tại Khu Công nghệ cao Hòa Lạc.", "acceptanceCriteria": "Gồm 5 câu hỏi trắc nghiệm ngắn gọn và 1 câu hỏi mở về nguyện vọng nghề nghiệp.", "revisionLimit": 2}]}}'::jsonb,
    3,
    1,
    NOW() - INTERVAL '2 days',
    NOW() - INTERVAL '2 days',
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
    updated_at = NOW();

  UPDATE workspaces
     SET workspace_media_package_id = (SELECT id FROM workspace_media_packages WHERE workspace_id = 'b47477c4-13ad-44ff-8c49-f73f1837461b'::uuid)
   WHERE id = 'b47477c4-13ad-44ff-8c49-f73f1837461b'::uuid;

  DELETE FROM package_negotiation_events
   WHERE workspace_media_package_id = (SELECT id FROM workspace_media_packages WHERE workspace_id = 'b47477c4-13ad-44ff-8c49-f73f1837461b'::uuid);

  INSERT INTO package_negotiation_events (id, workspace_media_package_id, terms_version, action, actor_id, actor_role, note, terms_snapshot, created_at)
  VALUES
    (gen_random_uuid(), (SELECT id FROM workspace_media_packages WHERE workspace_id = 'b47477c4-13ad-44ff-8c49-f73f1837461b'::uuid), 1, 'BASELINE', v_client, 'CLIENT', 'Khởi tạo gói truyền thông tuyển sinh từ danh mục của FPT Smart Ads Agency.', '{"sourcePackageId": "d7e00000-0000-4000-8000-000000000200", "name": "Gói Truyền thông Tuyển sinh Vi mạch & AI Đại học FPT 2026", "durationWeeks": 6, "budgetAmount": 20000000, "scopeDescription": "Triển khai truyền thông trong 6 tuần cho đợt tuyển sinh ngành Thiết kế Vi mạch và AI tại Đại học FPT, gắn với mục tiêu phát triển 50.000 kỹ sư bán dẫn của Việt Nam đến năm 2030", "quantityBasis": "TOTAL", "offeringDetails": {"deliverables": [{"id": "d7e00000-0000-4000-8000-000000000211", "serviceType": "SOCIAL_POST", "name": "Bài đăng truyền thông học bổng ngành Vi mạch & Sự kiện AI4VN", "quantity": 2, "unit": "bài đăng", "description": "Viết bài giới thiệu chương trình đào tạo ngành Thiết kế Vi mạch và Trí tuệ nhân tạo tại Đại học FPT, hưởng ứng mục tiêu 50.000 kỹ sư bán dẫn của Việt Nam đến năm 2030.", "acceptanceCriteria": "Nội dung ngắn gọn, nêu rõ mức học bổng Nguyễn Văn Đạo (50% đến 100%) và kỳ thực tập tại FPT Software từ năm thứ 3, đạt trạng thái PASSED khi kiểm tra an toàn nội dung.", "revisionLimit": 3}, {"id": "d7e00000-0000-4000-8000-000000000212", "serviceType": "PRESS_RECOMMENDATION", "name": "Đề xuất báo chí về chương trình đào tạo nhân lực bán dẫn hưởng ứng mục tiêu quốc gia 2030", "quantity": 1, "unit": "bản đề xuất", "description": "Chuẩn bị thông tin gửi các báo giáo dục và công nghệ trong dịp Ngày hội Trí tuệ Nhân tạo Việt Nam (AI4VN).", "acceptanceCriteria": "Có số liệu chỉ tiêu tuyển sinh, thông tin phòng lab bán dẫn tại Hòa Lạc và danh sách báo dự kiến.", "revisionLimit": 2}, {"id": "d7e00000-0000-4000-8000-000000000213", "serviceType": "WORKSHOP_SUPPORT", "name": "Khảo sát nhu cầu học sinh THPT về ngành Vi mạch bán dẫn và Chuyển đổi số tại Việt Nam", "quantity": 1, "unit": "bảng khảo sát", "description": "Khảo sát học sinh lớp 12 tham gia Tuần lễ trải nghiệm công nghệ tại Khu Công nghệ cao Hòa Lạc.", "acceptanceCriteria": "Gồm 5 câu hỏi trắc nghiệm ngắn gọn và 1 câu hỏi mở về nguyện vọng nghề nghiệp.", "revisionLimit": 2}]}}'::jsonb, NOW() - INTERVAL '4 days'),
    (gen_random_uuid(), (SELECT id FROM workspace_media_packages WHERE workspace_id = 'b47477c4-13ad-44ff-8c49-f73f1837461b'::uuid), 2, 'REQUEST_CHANGE', v_client, 'CLIENT', 'Đại học FPT đề xuất điều chỉnh ngân sách xuống 17.500.000 VNĐ và giữ nguyên tiến độ 6 tuần.', '{"sourcePackageId": "d7e00000-0000-4000-8000-000000000200", "name": "Gói Truyền thông Tuyển sinh Vi mạch & AI Đại học FPT 2026", "durationWeeks": 6, "budgetAmount": 17500000, "scopeDescription": "Triển khai truyền thông trong 6 tuần cho đợt tuyển sinh ngành Thiết kế Vi mạch và AI tại Đại học FPT, gắn với mục tiêu phát triển 50.000 kỹ sư bán dẫn của Việt Nam đến năm 2030 (Đại học FPT đề xuất tối ưu ngân sách 17,5M)", "quantityBasis": "TOTAL", "offeringDetails": {"deliverables": [{"id": "d7e00000-0000-4000-8000-000000000211", "serviceType": "SOCIAL_POST", "name": "Bài đăng truyền thông học bổng ngành Vi mạch & Sự kiện AI4VN", "quantity": 2, "unit": "bài đăng", "description": "Viết bài giới thiệu chương trình đào tạo ngành Thiết kế Vi mạch và Trí tuệ nhân tạo tại Đại học FPT, hưởng ứng mục tiêu 50.000 kỹ sư bán dẫn của Việt Nam đến năm 2030.", "acceptanceCriteria": "Nội dung ngắn gọn, nêu rõ mức học bổng Nguyễn Văn Đạo (50% đến 100%) và kỳ thực tập tại FPT Software từ năm thứ 3, đạt trạng thái PASSED khi kiểm tra an toàn nội dung.", "revisionLimit": 3}, {"id": "d7e00000-0000-4000-8000-000000000212", "serviceType": "PRESS_RECOMMENDATION", "name": "Đề xuất báo chí về chương trình đào tạo nhân lực bán dẫn hưởng ứng mục tiêu quốc gia 2030", "quantity": 1, "unit": "bản đề xuất", "description": "Chuẩn bị thông tin gửi các báo giáo dục và công nghệ trong dịp Ngày hội Trí tuệ Nhân tạo Việt Nam (AI4VN).", "acceptanceCriteria": "Có số liệu chỉ tiêu tuyển sinh, thông tin phòng lab bán dẫn tại Hòa Lạc và danh sách báo dự kiến.", "revisionLimit": 2}, {"id": "d7e00000-0000-4000-8000-000000000213", "serviceType": "WORKSHOP_SUPPORT", "name": "Khảo sát nhu cầu học sinh THPT về ngành Vi mạch bán dẫn và Chuyển đổi số tại Việt Nam", "quantity": 1, "unit": "bảng khảo sát", "description": "Khảo sát học sinh lớp 12 tham gia Tuần lễ trải nghiệm công nghệ tại Khu Công nghệ cao Hòa Lạc.", "acceptanceCriteria": "Gồm 5 câu hỏi trắc nghiệm ngắn gọn và 1 câu hỏi mở về nguyện vọng nghề nghiệp.", "revisionLimit": 2}]}}'::jsonb, NOW() - INTERVAL '3 days'),
    (gen_random_uuid(), (SELECT id FROM workspace_media_packages WHERE workspace_id = 'b47477c4-13ad-44ff-8c49-f73f1837461b'::uuid), 3, 'COUNTER_OFFER', v_manager, 'MANAGER', 'FPT Smart Ads chốt mức ngân sách ưu đãi nội bộ FPT 18.000.000 VNĐ, hỗ trợ tối đa 3 vòng chỉnh sửa cho mỗi bài đăng.', '{"sourcePackageId": "d7e00000-0000-4000-8000-000000000200", "name": "Gói Truyền thông Tuyển sinh Vi mạch & AI Đại học FPT 2026", "durationWeeks": 6, "budgetAmount": 18000000, "scopeDescription": "Triển khai truyền thông trong 6 tuần cho đợt tuyển sinh ngành Thiết kế Vi mạch và AI tại Đại học FPT, gắn với mục tiêu phát triển 50.000 kỹ sư bán dẫn của Việt Nam đến năm 2030 (Chốt ngân sách 18M kèm 3 vòng chỉnh sửa bài đăng)", "quantityBasis": "TOTAL", "offeringDetails": {"deliverables": [{"id": "d7e00000-0000-4000-8000-000000000211", "serviceType": "SOCIAL_POST", "name": "Bài đăng truyền thông học bổng ngành Vi mạch & Sự kiện AI4VN", "quantity": 2, "unit": "bài đăng", "description": "Viết bài giới thiệu chương trình đào tạo ngành Thiết kế Vi mạch và Trí tuệ nhân tạo tại Đại học FPT, hưởng ứng mục tiêu 50.000 kỹ sư bán dẫn của Việt Nam đến năm 2030.", "acceptanceCriteria": "Nội dung ngắn gọn, nêu rõ mức học bổng Nguyễn Văn Đạo (50% đến 100%) và kỳ thực tập tại FPT Software từ năm thứ 3, đạt trạng thái PASSED khi kiểm tra an toàn nội dung.", "revisionLimit": 3}, {"id": "d7e00000-0000-4000-8000-000000000212", "serviceType": "PRESS_RECOMMENDATION", "name": "Đề xuất báo chí về chương trình đào tạo nhân lực bán dẫn hưởng ứng mục tiêu quốc gia 2030", "quantity": 1, "unit": "bản đề xuất", "description": "Chuẩn bị thông tin gửi các báo giáo dục và công nghệ trong dịp Ngày hội Trí tuệ Nhân tạo Việt Nam (AI4VN).", "acceptanceCriteria": "Có số liệu chỉ tiêu tuyển sinh, thông tin phòng lab bán dẫn tại Hòa Lạc và danh sách báo dự kiến.", "revisionLimit": 2}, {"id": "d7e00000-0000-4000-8000-000000000213", "serviceType": "WORKSHOP_SUPPORT", "name": "Khảo sát nhu cầu học sinh THPT về ngành Vi mạch bán dẫn và Chuyển đổi số tại Việt Nam", "quantity": 1, "unit": "bảng khảo sát", "description": "Khảo sát học sinh lớp 12 tham gia Tuần lễ trải nghiệm công nghệ tại Khu Công nghệ cao Hòa Lạc.", "acceptanceCriteria": "Gồm 5 câu hỏi trắc nghiệm ngắn gọn và 1 câu hỏi mở về nguyện vọng nghề nghiệp.", "revisionLimit": 2}]}}'::jsonb, NOW() - INTERVAL '2 days');

  -- 6. Tạo Chiến dịch Tuyển sinh Đại học FPT ở trạng thái APPROVED (Chờ bấm nút "Triển khai" ở Bước B3)
  DELETE FROM campaign_deployments WHERE campaign_id = 'd7e00000-0000-4000-8000-000000000301'::uuid;
  DELETE FROM campaign_review_events WHERE campaign_id = 'd7e00000-0000-4000-8000-000000000301'::uuid;
  DELETE FROM campaign_versions WHERE campaign_id = 'd7e00000-0000-4000-8000-000000000301'::uuid;

  INSERT INTO media_campaigns (
    id, workspace_media_package_id, name, strategy_detail, brand_guideline,
    timeline, package_terms_snapshot, package_terms_version, allocations,
    deliverable_plan, work_items, content_version, row_version, status,
    approved_by_agency_at, approved_by_agency_id, approved_by_agency_version,
    approved_by_client_at, approved_by_client_id, approved_by_client_version,
    created_at, updated_at
  ) VALUES (
    'd7e00000-0000-4000-8000-000000000301'::uuid,
    (SELECT id FROM workspace_media_packages WHERE workspace_id = 'b47477c4-13ad-44ff-8c49-f73f1837461b'::uuid),
    'Chiến dịch Tuyển sinh Ngành Vi mạch Bán dẫn & Sự kiện AI4VN 2026',
    'Giới thiệu chương trình đào tạo ngành Thiết kế Vi mạch và Trí tuệ nhân tạo tại Đại học FPT, hưởng ứng mục tiêu 50.000 kỹ sư bán dẫn của Việt Nam đến năm 2030 và sự kiện AI4VN tại Hòa Lạc.',
    'Ngôn từ rõ ràng, gần gũi với học sinh THPT và phụ huynh. Nêu cụ thể thông tin học bổng Nguyễn Văn Đạo và kỳ thực tập tại FPT Software, tuân thủ quy định an toàn thông tin.',
    '{"startDate": "2026-11-06", "endDate": "2026-12-18", "milestones": [{"name": "Mở đăng ký học bổng ngành Vi mạch & AI tại Đại học FPT", "date": "2026-11-12"}, {"name": "Sự kiện Ngày hội Trí tuệ Nhân tạo Việt Nam (AI4VN) tại Hòa Lạc", "date": "2026-12-15"}]}'::jsonb,
    '{"sourcePackageId": "d7e00000-0000-4000-8000-000000000200", "name": "Gói Truyền thông Tuyển sinh Vi mạch & AI Đại học FPT 2026", "durationWeeks": 6, "budgetAmount": 18000000, "scopeDescription": "Triển khai truyền thông trong 6 tuần cho đợt tuyển sinh ngành Thiết kế Vi mạch và AI tại Đại học FPT, gắn với mục tiêu phát triển 50.000 kỹ sư bán dẫn của Việt Nam đến năm 2030 (Chốt ngân sách 18M kèm 3 vòng chỉnh sửa bài đăng)", "quantityBasis": "TOTAL", "offeringDetails": {"deliverables": [{"id": "d7e00000-0000-4000-8000-000000000211", "serviceType": "SOCIAL_POST", "name": "Bài đăng truyền thông học bổng ngành Vi mạch & Sự kiện AI4VN", "quantity": 2, "unit": "bài đăng", "description": "Viết bài giới thiệu chương trình đào tạo ngành Thiết kế Vi mạch và Trí tuệ nhân tạo tại Đại học FPT, hưởng ứng mục tiêu 50.000 kỹ sư bán dẫn của Việt Nam đến năm 2030.", "acceptanceCriteria": "Nội dung ngắn gọn, nêu rõ mức học bổng Nguyễn Văn Đạo (50% đến 100%) và kỳ thực tập tại FPT Software từ năm thứ 3, đạt trạng thái PASSED khi kiểm tra an toàn nội dung.", "revisionLimit": 3}, {"id": "d7e00000-0000-4000-8000-000000000212", "serviceType": "PRESS_RECOMMENDATION", "name": "Đề xuất báo chí về chương trình đào tạo nhân lực bán dẫn hưởng ứng mục tiêu quốc gia 2030", "quantity": 1, "unit": "bản đề xuất", "description": "Chuẩn bị thông tin gửi các báo giáo dục và công nghệ trong dịp Ngày hội Trí tuệ Nhân tạo Việt Nam (AI4VN).", "acceptanceCriteria": "Có số liệu chỉ tiêu tuyển sinh, thông tin phòng lab bán dẫn tại Hòa Lạc và danh sách báo dự kiến.", "revisionLimit": 2}, {"id": "d7e00000-0000-4000-8000-000000000213", "serviceType": "WORKSHOP_SUPPORT", "name": "Khảo sát nhu cầu học sinh THPT về ngành Vi mạch bán dẫn và Chuyển đổi số tại Việt Nam", "quantity": 1, "unit": "bảng khảo sát", "description": "Khảo sát học sinh lớp 12 tham gia Tuần lễ trải nghiệm công nghệ tại Khu Công nghệ cao Hòa Lạc.", "acceptanceCriteria": "Gồm 5 câu hỏi trắc nghiệm ngắn gọn và 1 câu hỏi mở về nguyện vọng nghề nghiệp.", "revisionLimit": 2}]}}'::jsonb,
    3,
    '[{"deliverableId": "d7e00000-0000-4000-8000-000000000211", "quantity": 2}, {"deliverableId": "d7e00000-0000-4000-8000-000000000212", "quantity": 1}, {"deliverableId": "d7e00000-0000-4000-8000-000000000213", "quantity": 1}]'::jsonb,
    '[{"id": "d7e00000-0000-4000-8000-000000000211", "serviceType": "SOCIAL_POST", "name": "Bài đăng truyền thông học bổng ngành Vi mạch & Sự kiện AI4VN", "quantity": 2, "unit": "bài đăng", "description": "Viết bài giới thiệu chương trình đào tạo ngành Thiết kế Vi mạch và Trí tuệ nhân tạo tại Đại học FPT, hưởng ứng mục tiêu 50.000 kỹ sư bán dẫn của Việt Nam đến năm 2030.", "acceptanceCriteria": "Nội dung ngắn gọn, nêu rõ mức học bổng Nguyễn Văn Đạo (50% đến 100%) và kỳ thực tập tại FPT Software từ năm thứ 3, đạt trạng thái PASSED khi kiểm tra an toàn nội dung.", "revisionLimit": 3}, {"id": "d7e00000-0000-4000-8000-000000000212", "serviceType": "PRESS_RECOMMENDATION", "name": "Đề xuất báo chí về chương trình đào tạo nhân lực bán dẫn hưởng ứng mục tiêu quốc gia 2030", "quantity": 1, "unit": "bản đề xuất", "description": "Chuẩn bị thông tin gửi các báo giáo dục và công nghệ trong dịp Ngày hội Trí tuệ Nhân tạo Việt Nam (AI4VN).", "acceptanceCriteria": "Có số liệu chỉ tiêu tuyển sinh, thông tin phòng lab bán dẫn tại Hòa Lạc và danh sách báo dự kiến.", "revisionLimit": 2}, {"id": "d7e00000-0000-4000-8000-000000000213", "serviceType": "WORKSHOP_SUPPORT", "name": "Khảo sát nhu cầu học sinh THPT về ngành Vi mạch bán dẫn và Chuyển đổi số tại Việt Nam", "quantity": 1, "unit": "bảng khảo sát", "description": "Khảo sát học sinh lớp 12 tham gia Tuần lễ trải nghiệm công nghệ tại Khu Công nghệ cao Hòa Lạc.", "acceptanceCriteria": "Gồm 5 câu hỏi trắc nghiệm ngắn gọn và 1 câu hỏi mở về nguyện vọng nghề nghiệp.", "revisionLimit": 2}]'::jsonb,
    '[{"id": "eef8cfde-2ec0-34d1-8ff6-a53f097ff4bb", "deliverableId": "d7e00000-0000-4000-8000-000000000211", "name": "[Bài #1] Mở đăng ký học bổng ngành Thiết kế Vi mạch & AI tại Đại học FPT", "type": "POST", "dueDate": "2026-11-15T10:00:00Z"}, {"id": "b4a8ad8b-43f5-3d31-91b6-b0c3960dac5d", "deliverableId": "d7e00000-0000-4000-8000-000000000211", "name": "[Bài #2] Tổng kết Ngày hội Trí tuệ Nhân tạo Việt Nam (AI4VN) tại cơ sở Hòa Lạc", "type": "POST", "dueDate": "2026-11-20T10:00:00Z"}, {"id": "48bdf50b-2b6b-3177-8a98-cfaa93caaf1d", "deliverableId": "d7e00000-0000-4000-8000-000000000212", "name": "[Báo chí #1] Thông cáo chương trình đào tạo nhân lực bán dẫn hưởng ứng mục tiêu quốc gia 2030", "type": "PRESS_RECOMMENDATION", "dueDate": "2026-11-24T10:00:00Z"}, {"id": "8f2c291b-9a9c-39fe-aae0-fa09d4e75c02", "deliverableId": "d7e00000-0000-4000-8000-000000000213", "name": "[Khảo sát #1] Khảo sát nhu cầu học sinh THPT về ngành Vi mạch bán dẫn và Chuyển đổi số", "type": "SURVEY", "dueDate": "2026-11-28T10:00:00Z"}]'::jsonb,
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
  VALUES (gen_random_uuid(), 'd7e00000-0000-4000-8000-000000000301'::uuid, 1, '{"name": "Chiến dịch Tuyển sinh Ngành Vi mạch Bán dẫn & Sự kiện AI4VN 2026", "strategyDetail": "Giới thiệu chương trình đào tạo ngành Thiết kế Vi mạch và Trí tuệ nhân tạo tại Đại học FPT, hưởng ứng mục tiêu 50.000 kỹ sư bán dẫn của Việt Nam đến năm 2030 và sự kiện AI4VN tại Hòa Lạc.", "brandGuideline": "Ngôn từ rõ ràng, gần gũi với học sinh THPT và phụ huynh. Nêu cụ thể thông tin học bổng Nguyễn Văn Đạo và kỳ thực tập tại FPT Software, tuân thủ quy định an toàn thông tin.", "timeline": {"startDate": "2026-11-06", "endDate": "2026-12-18", "milestones": [{"name": "Mở đăng ký học bổng ngành Vi mạch & AI tại Đại học FPT", "date": "2026-11-12"}, {"name": "Sự kiện Ngày hội Trí tuệ Nhân tạo Việt Nam (AI4VN) tại Hòa Lạc", "date": "2026-12-15"}]}, "workItems": [{"id": "eef8cfde-2ec0-34d1-8ff6-a53f097ff4bb", "deliverableId": "d7e00000-0000-4000-8000-000000000211", "name": "[Bài #1] Mở đăng ký học bổng ngành Thiết kế Vi mạch & AI tại Đại học FPT", "type": "POST", "dueDate": "2026-11-15T10:00:00Z"}, {"id": "b4a8ad8b-43f5-3d31-91b6-b0c3960dac5d", "deliverableId": "d7e00000-0000-4000-8000-000000000211", "name": "[Bài #2] Tổng kết Ngày hội Trí tuệ Nhân tạo Việt Nam (AI4VN) tại cơ sở Hòa Lạc", "type": "POST", "dueDate": "2026-11-20T10:00:00Z"}, {"id": "48bdf50b-2b6b-3177-8a98-cfaa93caaf1d", "deliverableId": "d7e00000-0000-4000-8000-000000000212", "name": "[Báo chí #1] Thông cáo chương trình đào tạo nhân lực bán dẫn hưởng ứng mục tiêu quốc gia 2030", "type": "PRESS_RECOMMENDATION", "dueDate": "2026-11-24T10:00:00Z"}, {"id": "8f2c291b-9a9c-39fe-aae0-fa09d4e75c02", "deliverableId": "d7e00000-0000-4000-8000-000000000213", "name": "[Khảo sát #1] Khảo sát nhu cầu học sinh THPT về ngành Vi mạch bán dẫn và Chuyển đổi số", "type": "SURVEY", "dueDate": "2026-11-28T10:00:00Z"}], "deliverablePlan": [{"id": "d7e00000-0000-4000-8000-000000000211", "serviceType": "SOCIAL_POST", "name": "Bài đăng truyền thông học bổng ngành Vi mạch & Sự kiện AI4VN", "quantity": 2, "unit": "bài đăng", "description": "Viết bài giới thiệu chương trình đào tạo ngành Thiết kế Vi mạch và Trí tuệ nhân tạo tại Đại học FPT, hưởng ứng mục tiêu 50.000 kỹ sư bán dẫn của Việt Nam đến năm 2030.", "acceptanceCriteria": "Nội dung ngắn gọn, nêu rõ mức học bổng Nguyễn Văn Đạo (50% đến 100%) và kỳ thực tập tại FPT Software từ năm thứ 3, đạt trạng thái PASSED khi kiểm tra an toàn nội dung.", "revisionLimit": 3}, {"id": "d7e00000-0000-4000-8000-000000000212", "serviceType": "PRESS_RECOMMENDATION", "name": "Đề xuất báo chí về chương trình đào tạo nhân lực bán dẫn hưởng ứng mục tiêu quốc gia 2030", "quantity": 1, "unit": "bản đề xuất", "description": "Chuẩn bị thông tin gửi các báo giáo dục và công nghệ trong dịp Ngày hội Trí tuệ Nhân tạo Việt Nam (AI4VN).", "acceptanceCriteria": "Có số liệu chỉ tiêu tuyển sinh, thông tin phòng lab bán dẫn tại Hòa Lạc và danh sách báo dự kiến.", "revisionLimit": 2}, {"id": "d7e00000-0000-4000-8000-000000000213", "serviceType": "WORKSHOP_SUPPORT", "name": "Khảo sát nhu cầu học sinh THPT về ngành Vi mạch bán dẫn và Chuyển đổi số tại Việt Nam", "quantity": 1, "unit": "bảng khảo sát", "description": "Khảo sát học sinh lớp 12 tham gia Tuần lễ trải nghiệm công nghệ tại Khu Công nghệ cao Hòa Lạc.", "acceptanceCriteria": "Gồm 5 câu hỏi trắc nghiệm ngắn gọn và 1 câu hỏi mở về nguyện vọng nghề nghiệp.", "revisionLimit": 2}]}'::jsonb, v_manager, NOW() - INTERVAL '2 days');

  INSERT INTO campaign_review_events (id, campaign_id, content_version, actor_id, actor_side, event_type, comment, created_at)
  VALUES
    (gen_random_uuid(), 'd7e00000-0000-4000-8000-000000000301'::uuid, 1, v_client, 'CLIENT', 'FEEDBACK', 'Kế hoạch truyền thông ngành AI & Học bổng Nguyễn Văn Đạo trên 4 nền tảng rất sát thực tế, đồng ý triển khai.', NOW() - INTERVAL '30 hours'),
    (gen_random_uuid(), 'd7e00000-0000-4000-8000-000000000301'::uuid, 1, v_manager, 'AGENCY', 'APPROVE', NULL, NOW() - INTERVAL '25 hours'),
    (gen_random_uuid(), 'd7e00000-0000-4000-8000-000000000301'::uuid, 1, v_client, 'CLIENT', 'APPROVE', NULL, NOW() - INTERVAL '24 hours');

  -- 7. Cấu hình giá gói PLUS = 2.000 VNĐ và đưa FPT Smart Ads Agency về gói BASIC để quét VietQR SePay (Bước B14)
  UPDATE billing_plan_versions
     SET price_monthly = 2000,
         is_sellable = TRUE
   WHERE code = 'PLUS';

  UPDATE agency_subscriptions
     SET plan_version_id = v_basic,
         status = 'ACTIVE',
         updated_at = NOW()
   WHERE agency_id = '359a1839-18c7-48e2-8a68-f5f68c3375b6'::uuid;
END $$;
