# -*- coding: utf-8 -*-
import os
import json
import glob

from humanize_data_dict import (
    REPORTS_VI,
    DOMAINS_VI,
    ACTORS_VI,
    REPORT1_FIGURES_VI,
    REPORT2_FIGURES_VI,
    REPORT3_OVERVIEW_VI,
    CLASS_DIAGRAMS_VI,
    BUSINESS_RULES_VI,
    MESSAGES_CONTEXT_VI,
    SCREENS_VI,
    NON_SCREEN_VI,
    ENTITIES_VI,
)
from humanize_frs_part1 import FRS_PART1
from humanize_frs_part2 import FRS_PART2
from humanize_frs_part3 import FRS_PART3

ALL_FRS_VI = {}
ALL_FRS_VI.update(FRS_PART1)
ALL_FRS_VI.update(FRS_PART2)
ALL_FRS_VI.update(FRS_PART3)

PORTAL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PORTAL_DIR, "src", "data")


def describe_sequence_lifeline(name: str, stereotype: str, fr_title: str, fr_code: str) -> tuple[str, str]:
    """Return a clean Vietnamese type label and practical explanation for a Sequence Diagram lifeline."""
    st = (stereotype or "").lower()
    nm = name.strip()

    if "actor" in st or nm in ("Guest", "Owner", "Manager", "Creator", "Client", "Admin") or "," in nm:
        return (
            "Người thực hiện (Actor)",
            f"Vai trò ({nm}) trực tiếp thao tác trên màn hình để thực hiện chức năng {fr_code} ({fr_title})."
        )
    if "boundary" in st or "page" in nm.lower() or "(ui)" in nm.lower() or "screen" in nm.lower() or "view" in nm.lower():
        return (
            "Giao diện màn hình (UI)",
            f"Màn hình giao diện ({nm}) tiếp nhận thao tác của người dùng, kiểm tra sơ bộ dữ liệu nhập và hiển thị kết quả phản hồi."
        )
    if "controller" in st or "controller" in nm.lower():
        return (
            "Tầng điều phối API (Controller)",
            f"Lớp {nm} tiếp nhận yêu cầu từ giao diện, kiểm tra quyền truy cập của người dùng và chuyển dữ liệu xuống tầng xử lý nghiệp vụ."
        )
    if "repository" in st or "repository" in nm.lower():
        return (
            "Tầng truy vấn dữ liệu (Repository)",
            f"Lớp {nm} thực hiện các câu lệnh đọc, thêm mới hoặc cập nhật bản ghi trong cơ sở dữ liệu."
        )
    if "database" in st or nm.lower() in ("database", "postgresql", "mongodb", "redis", "neo4j", "chromadb"):
        return (
            "Cơ sở dữ liệu (Database)",
            f"Hệ quản trị cơ sở dữ liệu ({nm}) lưu trữ bền vững và đảm bảo tính toàn vẹn của dữ liệu."
        )
    if "mail" in nm.lower() or "smtp" in nm.lower() or "notification" in nm.lower():
        return (
            "Dịch vụ Gửi thông báo / Email",
            f"Dịch vụ ({nm}) phụ trách gửi mã OTP, email thông báo hoặc đẩy thông báo thời gian thực tới người nhận."
        )
    if "sepay" in nm.lower() or "payos" in nm.lower() or "payment" in nm.lower():
        return (
            "Dịch vụ Thanh toán (SePay / VietQR)",
            f"Dịch vụ ({nm}) khởi tạo mã VietQR và xác nhận kết quả chuyển khoản ngân hàng tự động."
        )
    if any(k in nm.lower() for k in ("oauth", "google", "facebook", "instagram", "tiktok", "threads", "drive", "s3", "storage")):
        return (
            "Dịch vụ Tích hợp Bên ngoài",
            f"Dịch vụ kết nối ({nm}) hỗ trợ xác thực tài khoản, lưu trữ đám mây hoặc đăng bài sang nền tảng mạng xã hội."
        )
    return (
        "Tầng xử lý nghiệp vụ (Service)",
        f"Lớp nghiệp vụ ({nm}) kiểm tra các quy tắc ràng buộc (Business Rules) và điều phối luồng xử lý chính của chức năng {fr_code} ({fr_title})."
    )


def describe_class_item(name: str, raw_type: str, domain_code: str, domain_title: str, role_map: dict) -> tuple[str, str]:
    """Return a clean Vietnamese type label and practical explanation for a Class Diagram class."""
    if name in role_map:
        desc = role_map[name]
    else:
        t_low = raw_type.lower()
        if "controller" in t_low or name.endswith("Controller"):
            desc = f"Lớp tiếp nhận các yêu cầu API từ giao diện và kiểm tra phân quyền trong phân hệ {domain_code} ({domain_title})."
        elif "service" in t_low or name.endswith("Service"):
            desc = f"Lớp xử lý các quy tắc nghiệp vụ cốt lõi của phân hệ {domain_code} ({domain_title})."
        elif "repository" in t_low or name.endswith("Repository"):
            target = name.replace("Repository", "")
            desc = f"Lớp giao tiếp cơ sở dữ liệu để truy vấn, lưu và cập nhật bảng {target}."
        else:
            desc = f"Lớp mô hình dữ liệu (Entity) lưu trữ các thuộc tính và trạng thái của {name} trong phân hệ {domain_code}."

    t_low = raw_type.lower()
    if "controller" in t_low or name.endswith("Controller"):
        vi_type = "Tầng API (Controller)"
    elif "service" in t_low or name.endswith("Service"):
        vi_type = "Xử lý nghiệp vụ (Service)"
    elif "repository" in t_low or name.endswith("Repository"):
        vi_type = "Truy vấn CSDL (Repository)"
    else:
        vi_type = "Thực thể dữ liệu (Entity)"

    return vi_type, desc


def main():
    print(f"Loaded {len(ALL_FRS_VI)} FR Vietnamese specifications.")
    assert len(ALL_FRS_VI) == 141, f"Expected 141 FRs, got {len(ALL_FRS_VI)}"

    # 1. Update project.json
    proj_path = os.path.join(DATA_DIR, "project.json")
    proj = json.load(open(proj_path, "r", encoding="utf-8"))
    for rep in proj["reports"]:
        if rep["id"] in REPORTS_VI:
            rep["description"] = REPORTS_VI[rep["id"]]["description"]
    for dom in proj["domains"]:
        if dom["code"] in DOMAINS_VI:
            dom["summary"] = DOMAINS_VI[dom["code"]]
    for act in proj["actors"]:
        role = act["role"]
        if role in ACTORS_VI:
            act["description"] = ACTORS_VI[role]
    json.dump(proj, open(proj_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("Updated project.json")

    # 2. Update rulesAndMessages.json
    rm_path = os.path.join(DATA_DIR, "rulesAndMessages.json")
    rm = json.load(open(rm_path, "r", encoding="utf-8"))
    for br in rm["businessRules"]:
        if br["code"] in BUSINESS_RULES_VI:
            br["definition"] = BUSINESS_RULES_VI[br["code"]]
    msg_type_vi = {
        "In line": "Hiển thị trực tiếp trên màn hình (Inline)",
        "In red, under the text box": "Chữ đỏ báo lỗi ngay dưới ô nhập",
        "Toast message": "Thông báo nổi góc màn hình (Toast)",
        "Warning banner": "Băng cảnh báo nổi bật (Warning Banner)",
    }
    for msg in rm["messages"]:
        code = msg["code"]
        if code in MESSAGES_CONTEXT_VI:
            msg["context"] = MESSAGES_CONTEXT_VI[code]
        if msg["type"] in msg_type_vi:
            msg["type"] = msg_type_vi[msg["type"]]
    json.dump(rm, open(rm_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("Updated rulesAndMessages.json")

    # 3. Update matrices.json
    mat_path = os.path.join(DATA_DIR, "matrices.json")
    mat = json.load(open(mat_path, "r", encoding="utf-8"))
    for sc in mat["screenDescriptions"]:
        idx = str(sc["index"])
        if idx in SCREENS_VI:
            feat_vi, scr_vi, desc_vi = SCREENS_VI[idx]
            sc["feature"] = feat_vi
            sc["screen"] = scr_vi
            sc["description"] = desc_vi
    for nf in mat["nonScreenFunctions"]:
        idx = str(nf["index"])
        if idx in NON_SCREEN_VI:
            feat_vi, fn_vi, desc_vi = NON_SCREEN_VI[idx]
            nf["feature"] = feat_vi
            nf["systemFunction"] = fn_vi
            nf["description"] = desc_vi
    for ent in mat["entities"]:
        ename = ent["entity"]
        if ename in ENTITIES_VI:
            ent["description"] = ENTITIES_VI[ename]
    json.dump(mat, open(mat_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("Updated matrices.json")

    # 4. Update useCases.json
    uc_path = os.path.join(DATA_DIR, "useCases.json")
    ucs = json.load(open(uc_path, "r", encoding="utf-8"))
    for uc in ucs:
        fr_code = uc.get("frCode")
        if fr_code and fr_code in ALL_FRS_VI:
            uc["description"] = f"({fr_code}) {ALL_FRS_VI[fr_code]['summary']}"
    json.dump(ucs, open(uc_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("Updated useCases.json")

    # 5. Update all 9 FR domain files (src/data/frs/domain-3.2.json .. domain-3.10.json)
    for dom_file in sorted(glob.glob(os.path.join(DATA_DIR, "frs", "domain-*.json"))):
        fr_list = json.load(open(dom_file, "r", encoding="utf-8"))
        for fr in fr_list:
            code = fr["code"]
            spec = ALL_FRS_VI[code]
            fr["viSummary"] = spec["summary"]
            fr["purpose"] = spec["summary"]
            fr["ucDescription"] = f"({code}) {spec['summary']}"
            fr["trigger"] = spec["trigger"]
            fr["interface"] = spec["interface"]
            fr["dataProcessing"] = spec["processing"]
            fr["dataSpecs"] = {
                "inputRequired": spec["in_req"],
                "inputOptional": spec["in_opt"],
                "systemData": spec["sys_data"],
                "output": spec["output"],
            }
            fr["normalFlow"] = spec["flow"]
            fr["abnormalCases"] = spec["abnormal"]
            # Also update embedded businessRules text
            for b in fr.get("businessRules", []):
                if b["code"] in BUSINESS_RULES_VI:
                    b["text"] = BUSINESS_RULES_VI[b["code"]]
        json.dump(fr_list, open(dom_file, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"Updated {os.path.basename(dom_file)} ({len(fr_list)} FRs)")

    # 6. Update figures/report1.json
    r1_path = os.path.join(DATA_DIR, "figures", "report1.json")
    r1_figs = json.load(open(r1_path, "r", encoding="utf-8"))
    for fig in r1_figs:
        if fig["id"] in REPORT1_FIGURES_VI:
            info = REPORT1_FIGURES_VI[fig["id"]]
            fig["viSummary"] = info["viSummary"]
            fig["summary"] = info["viSummary"]
            fig["components"] = info["components"]
    json.dump(r1_figs, open(r1_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("Updated figures/report1.json")

    # 7. Update figures/report2.json
    r2_path = os.path.join(DATA_DIR, "figures", "report2.json")
    r2_figs = json.load(open(r2_path, "r", encoding="utf-8"))
    for fig in r2_figs:
        if fig["id"] in REPORT2_FIGURES_VI:
            info = REPORT2_FIGURES_VI[fig["id"]]
            fig["viSummary"] = info["viSummary"]
            fig["summary"] = info["viSummary"]
            fig["components"] = info["components"]
    json.dump(r2_figs, open(r2_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("Updated figures/report2.json")

    # 8. Update figures/report3-overview.json
    r3o_path = os.path.join(DATA_DIR, "figures", "report3-overview.json")
    r3o_figs = json.load(open(r3o_path, "r", encoding="utf-8"))
    for fig in r3o_figs:
        if fig["id"] in REPORT3_OVERVIEW_VI:
            info = REPORT3_OVERVIEW_VI[fig["id"]]
            fig["viSummary"] = info["viSummary"]
            fig["summary"] = info["viSummary"]
            fig["components"] = info["components"]
    json.dump(r3o_figs, open(r3o_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("Updated figures/report3-overview.json")

    # 9. Update figures/report3-screens.json (141 Screen Layout figures)
    r3s_path = os.path.join(DATA_DIR, "figures", "report3-screens.json")
    r3s_figs = json.load(open(r3s_path, "w+" if not os.path.exists(r3s_path) else "r", encoding="utf-8"))
    for fig in r3s_figs:
        code = fig.get("frCode")
        if code and code in ALL_FRS_VI:
            spec = ALL_FRS_VI[code]
            fig["viSummary"] = spec["summary"]
            fig["summary"] = spec["summary"]
            fig["trigger"] = spec["trigger"]
            fig["interface"] = spec["interface"]
            fig["dataProcessing"] = spec["processing"]
            fig["normalFlow"] = spec["flow"]
            fig["abnormalCases"] = spec["abnormal"]
            fig["components"] = [
                {
                    "name": "Bố cục giao diện màn hình",
                    "type": "Màn hình (UI)",
                    "description": spec["interface"],
                },
                {
                    "name": "Thông tin người dùng nhập / chọn",
                    "type": "Dữ liệu đầu vào",
                    "description": f"Bắt buộc: {spec['in_req']} | Tùy chọn: {spec['in_opt']}",
                },
                {
                    "name": "Kiểm tra & Xử lý của hệ thống",
                    "type": "Logic xử lý",
                    "description": spec["processing"],
                },
                {
                    "name": "Kết quả hiển thị & Phản hồi",
                    "type": "Kết quả đầu ra",
                    "description": spec["output"],
                },
            ]
    json.dump(r3s_figs, open(r3s_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("Updated figures/report3-screens.json")

    # 10. Update figures/report4-class.json (9 Class Diagram figures)
    r4c_path = os.path.join(DATA_DIR, "figures", "report4-class.json")
    r4c_figs = json.load(open(r4c_path, "r", encoding="utf-8"))
    for fig in r4c_figs:
        cid = fig["id"]
        if cid in CLASS_DIAGRAMS_VI:
            cinfo = CLASS_DIAGRAMS_VI[cid]
            fig["viSummary"] = cinfo["viSummary"]
            fig["summary"] = cinfo["viSummary"]
            rmap = cinfo["roleMap"]
            new_comps = []
            for comp in fig.get("components", []):
                cname = comp["name"]
                vi_type, vi_desc = describe_class_item(
                    cname,
                    comp.get("type", ""),
                    fig.get("domainCode", ""),
                    fig.get("domainTitle", ""),
                    rmap,
                )
                new_comps.append({
                    "name": cname,
                    "type": vi_type,
                    "description": vi_desc,
                })
            fig["components"] = new_comps
    json.dump(r4c_figs, open(r4c_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("Updated figures/report4-class.json")

    # 11. Update figures/report4-sequence.json (141 Sequence Diagram figures)
    r4s_path = os.path.join(DATA_DIR, "figures", "report4-sequence.json")
    r4s_figs = json.load(open(r4s_path, "r", encoding="utf-8"))
    for fig in r4s_figs:
        code = fig.get("frCode")
        if code and code in ALL_FRS_VI:
            spec = ALL_FRS_VI[code]
            fr_title = fig.get("title", "").replace(f"Sequence Diagram — {code} ", "").strip()
            fig["viSummary"] = (
                f"Sơ đồ tuần tự (Sequence Diagram) mô tả từng bước tương tác từ lúc người dùng thao tác trên màn hình đến khi hệ thống xử lý và trả kết quả cho chức năng {code} ({fr_title}): {spec['summary']}"
            )
            fig["summary"] = spec["summary"]
            fig["normalFlow"] = spec["flow"]
            fig["abnormalCases"] = spec["abnormal"]
            new_comps = []
            for comp in fig.get("components", []):
                vi_type, vi_desc = describe_sequence_lifeline(
                    comp["name"],
                    comp.get("type", ""),
                    fr_title,
                    code,
                )
                new_comps.append({
                    "name": comp["name"],
                    "type": vi_type,
                    "description": vi_desc,
                })
            fig["components"] = new_comps
    json.dump(r4s_figs, open(r4s_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("Updated figures/report4-sequence.json")
    print("ALL JSON DATA FILES UPDATED SUCCESSFULLY!")


if __name__ == "__main__":
    main()
