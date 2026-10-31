import os
import re
import csv
import json
import time
import glob
import hashlib
import sqlite3
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import docx
from docx.oxml.ns import qn
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = r"d:\ProjectCode\BrandHub"
PORTAL_DIR = os.path.join(ROOT_DIR, "brandhub-docs-portal")
STAGING_DIR = os.path.join(PORTAL_DIR, "assets_staging")
DATA_DIR = os.path.join(PORTAL_DIR, "src", "data")
CACHE_PATH = os.path.join(PORTAL_DIR, "scripts", "cloudinary_cache.json")

os.makedirs(STAGING_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)

CANONICAL_ROLES = ["Guest", "Owner", "Manager", "Creator", "Client", "Admin"]

ROLE_REPLACEMENTS = [
    (r"\bUnauthenticated Users?\b", "Guest"),
    (r"\bAnonymous Users?\b", "Guest"),
    (r"\bVisitors?\b", "Guest"),
    (r"\bAgency Owners?\b", "Owner"),
    (r"\bWorkspace [Mm]anagers?\b", "Manager"),
    (r"\bAccount Managers?\b", "Manager"),
    (r"\bContent Creators?\b", "Creator"),
    (r"\bBrand Clients?\b", "Client"),
    (r"\bSystem Administrators?\b", "Admin"),
    (r"\bSystem Admins?\b", "Admin"),
    (r"\bAdministrators?\b", "Admin"),
]

def sanitize_roles(text: str) -> str:
    if not text:
        return ""
    res = text
    for pat, repl in ROLE_REPLACEMENTS:
        res = re.sub(pat, repl, res)
    return res

def extract_canonical_actors(actor_str: str) -> list:
    s = sanitize_roles(actor_str)
    found = []
    for r in CANONICAL_ROLES:
        if re.search(rf"\b{r}\b", s, re.IGNORECASE):
            found.append(r)
    if not found:
        # fallback check
        if "Authenticated" in s or "Member" in s or "Invited" in s:
            found = ["Owner", "Manager", "Creator"]
        else:
            found = ["Owner", "Manager"]
    return found

def get_font(size: int, bold: bool = False):
    candidates = [
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                pass
    return ImageFont.load_default()

def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [""]

def render_screen_mockup(out_path: str, fig_num: int, fr_code: str, title: str, domain_title: str, actors: list, purpose: str, interface_desc: str, data_specs: dict, br_codes: list):
    """Render a crisp 1920x1080 BrandHub UI Screen Layout Mockup for FRs without embedded docx screenshots."""
    W, H = 1920, 1080
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)

    f_logo = get_font(24, True)
    f_h1 = get_font(30, True)
    f_h2 = get_font(20, True)
    f_body = get_font(17, False)
    f_small = get_font(15, False)
    f_badge = get_font(14, True)

    # Sidebar (Dark Slate)
    draw.rectangle([0, 0, 280, H], fill=(15, 23, 42))
    draw.rounded_rectangle([24, 24, 64, 64], radius=10, fill=(79, 70, 229))
    draw.text((36, 30), "B", fill=(255, 255, 255), font=f_logo)
    draw.text((78, 30), "BrandHub", fill=(255, 255, 255), font=f_logo)
    draw.text((24, 78), "AI Content & Campaign OS", fill=(148, 163, 184), font=f_small)

    nav_items = [
        ("3.2", "Authentication & Security"),
        ("3.3", "User & Client Profile"),
        ("3.4", "Agency & Workspace"),
        ("3.5", "Media Package & Campaign"),
        ("3.6", "Content & Task Workflow"),
        ("3.7", "AI Studio & Knowledge"),
        ("3.8", "Social Publishing"),
        ("3.9", "Subscription & Billing"),
        ("3.10", "Admin Console"),
    ]
    y_nav = 130
    dom_prefix = ".".join(fr_code.split(".")[:2])
    for code_p, nav_label in nav_items:
        active = (code_p == dom_prefix)
        if active:
            draw.rounded_rectangle([16, y_nav, 264, y_nav + 44], radius=8, fill=(79, 70, 229))
            draw.text((32, y_nav + 11), f"{nav_label}", fill=(255, 255, 255), font=f_badge)
        else:
            draw.text((32, y_nav + 11), f"{nav_label}", fill=(148, 163, 184), font=f_small)
        y_nav += 54

    # Role indicator at bottom of sidebar
    draw.rounded_rectangle([16, H - 110, 264, H - 24], radius=10, fill=(30, 41, 59))
    draw.text((30, H - 96), "Active Role Context", fill=(148, 163, 184), font=f_small)
    draw.text((30, H - 68), " / ".join(actors[:3]), fill=(56, 189, 248), font=f_badge)

    # Top Header Bar
    draw.rectangle([280, 0, W, 76], fill=(255, 255, 255))
    draw.line([280, 76, W, 76], fill=(226, 232, 240), width=2)
    route_match = re.search(r"(/[a-zA-Z0-9_/:?=&-]+)", interface_desc or "")
    route_str = route_match.group(1) if route_match else f"/app/{fr_code.replace('.', '-')}"
    draw.rounded_rectangle([310, 18, 980, 58], radius=8, fill=(241, 245, 249), outline=(203, 213, 225))
    draw.text((328, 28), f"https://app.brandhub.vn{route_str}", fill=(71, 85, 105), font=f_small)

    # Right header badges
    draw.rounded_rectangle([W - 420, 20, W - 230, 56], radius=8, fill=(238, 242, 255), outline=(199, 210, 254))
    draw.text((W - 404, 29), f"FR {fr_code}  •  Figure {fig_num}", fill=(67, 56, 202), font=f_badge)
    draw.rounded_rectangle([W - 210, 20, W - 36, 56], radius=8, fill=(240, 253, 244), outline=(187, 247, 208))
    draw.text((W - 192, 29), f"Role: {actors[0] if actors else 'Owner'}", fill=(21, 128, 61), font=f_badge)

    # Page Title & Breadcrumb
    draw.text((320, 100), f"{domain_title}  /  FR {fr_code}", fill=(100, 116, 139), font=f_small)
    draw.text((320, 128), f"{title}", fill=(15, 23, 42), font=f_h1)

    # Primary Action Button in top-right of content
    draw.rounded_rectangle([W - 290, 116, W - 48, 168], radius=10, fill=(79, 70, 229))
    draw.text((W - 262, 132), f"Execute {title[:18]}", fill=(255, 255, 255), font=f_badge)

    # Left Main Interactive Card (Workspace / Form / View)
    draw.rounded_rectangle([320, 192, 1240, 1036], radius=14, fill=(255, 255, 255), outline=(226, 232, 240), width=2)
    draw.rectangle([320, 192, 1240, 252], fill=(248, 250, 252))
    draw.line([320, 252, 1240, 252], fill=(226, 232, 240), width=2)
    draw.text((348, 210), f"Screen Interface & Interactive Controls — {title}", fill=(15, 23, 42), font=f_h2)

    # Interface overview box
    draw.rounded_rectangle([348, 274, 1212, 410], radius=10, fill=(248, 250, 252), outline=(203, 213, 225))
    draw.text((368, 288), "UI Layout & Components Specification:", fill=(51, 65, 85), font=f_badge)
    ui_lines = wrap_text(draw, interface_desc or purpose, f_body, 820)
    y_txt = 316
    for ln in ui_lines[:3]:
        draw.text((368, y_txt), ln, fill=(71, 85, 105), font=f_body)
        y_txt += 26

    # Parse required/optional inputs into visual form fields or data table columns
    req_in = data_specs.get("inputRequired", "None")
    opt_in = data_specs.get("inputOptional", "None")
    fields = []
    for src, is_req in [(req_in, True), (opt_in, False)]:
        if src and src.lower() != "none.":
            parts = [p.strip() for p in re.split(r",\s*(?=[a-zA-Z0-9_]+\s*\()", src) if p.strip()]
            if not parts:
                parts = [p.strip() for p in src.split(",") if p.strip()]
            for p in parts[:6]:
                fields.append((p, is_req))

    draw.text((348, 432), "Interactive Form Fields / View Parameters", fill=(15, 23, 42), font=f_h2)
    y_field = 472
    if fields:
        for idx_f, (f_desc, is_req) in enumerate(fields[:6]):
            col = idx_f % 2
            row = idx_f // 2
            fx = 348 + col * 440
            fy = 472 + row * 112
            draw.text((fx, fy), f_desc[:46] + (" *" if is_req else " (Optional)"), fill=(51, 65, 85), font=f_badge)
            draw.rounded_rectangle([fx, fy + 28, fx + 412, fy + 82], radius=8, fill=(255, 255, 255), outline=(148, 163, 184), width=2)
            draw.text((fx + 16, fy + 44), f"Enter / Select {f_desc.split('(')[0].strip()}...", fill=(148, 163, 184), font=f_small)
        y_field = 472 + ((min(len(fields), 6) + 1) // 2) * 112 + 16
    else:
        # Render a crisp data table preview for View/List screens
        headers = ["ID / Reference", "Primary Item / Resource", "Status / State", "Updated Timestamp", "Actions"]
        draw.rounded_rectangle([348, 472, 1212, 760], radius=10, fill=(255, 255, 255), outline=(203, 213, 225))
        draw.rectangle([348, 472, 1212, 520], fill=(241, 245, 249))
        col_x = [368, 510, 790, 950, 1110]
        for cx, h_text in zip(col_x, headers):
            draw.text((cx, 486), h_text, fill=(51, 65, 85), font=f_badge)
        for r_i in range(4):
            ry = 520 + r_i * 58
            draw.line([348, ry, 1212, ry], fill=(226, 232, 240), width=1)
            draw.text((col_x[0], ry + 18), f"#BH-{1042 + r_i}", fill=(79, 70, 229), font=f_badge)
            draw.text((col_x[1], ry + 18), f"{title} Record #{r_i + 1}", fill=(30, 41, 59), font=f_small)
            draw.rounded_rectangle([col_x[2], ry + 14, col_x[2] + 105, ry + 42], radius=12, fill=(220, 252, 231))
            draw.text((col_x[2] + 16, ry + 19), "ACTIVE", fill=(21, 128, 61), font=f_badge)
            draw.text((col_x[3], ry + 18), "2026-10-30 14:20", fill=(100, 116, 139), font=f_small)
            draw.rounded_rectangle([col_x[4], ry + 12, col_x[4] + 84, ry + 44], radius=6, fill=(241, 245, 249), outline=(203, 213, 225))
            draw.text((col_x[4] + 18, ry + 19), "Inspect", fill=(51, 65, 85), font=f_small)
        y_field = 784

    # Bottom Output & Confirmation Bar inside Left Card
    draw.rounded_rectangle([348, max(y_field, 820), 1212, 1008], radius=10, fill=(238, 242, 255), outline=(199, 210, 254))
    draw.text((368, max(y_field, 820) + 16), "Expected System Output & State Transition:", fill=(67, 56, 202), font=f_badge)
    out_lines = wrap_text(draw, data_specs.get("output", purpose), f_body, 820)
    yo = max(y_field, 820) + 46
    for ln in out_lines[:3]:
        draw.text((368, yo), ln, fill=(49, 46, 129), font=f_body)
        yo += 26

    # Right Side Panel: Purpose, Data Processing & Enforced Business Rules
    draw.rounded_rectangle([1268, 192, W - 36, 610], radius=14, fill=(255, 255, 255), outline=(226, 232, 240), width=2)
    draw.rectangle([1268, 192, W - 36, 252], fill=(248, 250, 252))
    draw.line([1268, 252, W - 36, 252], fill=(226, 232, 240), width=2)
    draw.text((1294, 210), "Functional Purpose & Processing", fill=(15, 23, 42), font=f_h2)

    draw.text((1294, 272), "Purpose:", fill=(79, 70, 229), font=f_badge)
    p_lines = wrap_text(draw, purpose, f_small, 560)
    yp = 298
    for ln in p_lines[:4]:
        draw.text((1294, yp), ln, fill=(51, 65, 85), font=f_small)
        yp += 24

    draw.text((1294, yp + 12), "System Data Tracked:", fill=(79, 70, 229), font=f_badge)
    s_lines = wrap_text(draw, data_specs.get("systemData", "userId, workspaceId, status, updatedAt"), f_small, 560)
    ys = yp + 38
    for ln in s_lines[:4]:
        draw.text((1294, ys), ln, fill=(71, 85, 105), font=f_small)
        ys += 24

    # Right Bottom Card: Business Rules & Actors
    draw.rounded_rectangle([1268, 634, W - 36, 1036], radius=14, fill=(255, 255, 255), outline=(226, 232, 240), width=2)
    draw.rectangle([1268, 634, W - 36, 694], fill=(248, 250, 252))
    draw.line([1268, 694, W - 36, 694], fill=(226, 232, 240), width=2)
    draw.text((1294, 652), "Authorized Actors & Business Rules", fill=(15, 23, 42), font=f_h2)

    draw.text((1294, 714), "Canonical Roles Permitted:", fill=(51, 65, 85), font=f_badge)
    rx = 1294
    for act in actors:
        draw.rounded_rectangle([rx, 744, rx + 92, 778], radius=8, fill=(224, 231, 255), outline=(165, 180, 252))
        draw.text((rx + 14, 752), act, fill=(55, 48, 163), font=f_badge)
        rx += 102

    draw.text((1294, 804), "Enforced Business Rules (SRS):", fill=(51, 65, 85), font=f_badge)
    yb = 836
    for b_item in (br_codes[:4] if br_codes else [{"code": "BR-20", "text": "Strict RBAC & Workspace multi-tenant isolation enforced."}]):
        b_txt = f"{b_item['code']}: {b_item['text']}"
        b_lines = wrap_text(draw, b_txt, f_small, 560)
        for ln in b_lines[:2]:
            draw.text((1294, yb), ln, fill=(71, 85, 105), font=f_small)
            yb += 22
        yb += 6

    img.save(out_path, "PNG", optimize=True)

def render_sequence_diagram_png(out_path: str, fr_code: str, title: str, actors: list, lifelines: list, messages: list):
    """Render a crisp Visual Paradigm style UML Sequence Diagram PNG for FRs without a pre-rendered VP PNG."""
    W = max(1800, 320 * max(len(lifelines), 5))
    H = max(1050, 240 + len(messages) * 64 + 120)
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    f_title = get_font(22, True)
    f_box = get_font(15, True)
    f_stereo = get_font(13, False)
    f_msg = get_font(14, False)

    # Outer frame
    draw.rectangle([16, 16, W - 16, H - 16], outline=(100, 116, 139), width=2)
    # sd pentagon header
    draw.polygon([(16, 16), (460, 16), (460, 42), (444, 56), (16, 56)], fill=(241, 245, 249), outline=(100, 116, 139))
    draw.text((30, 25), f"sd Sequence Diagram — {fr_code} - {title}", fill=(15, 23, 42), font=f_title)

    n = len(lifelines)
    margin_x = 150
    spacing = (W - 2 * margin_x) // max(n - 1, 1)
    xs = [margin_x + i * spacing for i in range(n)]

    top_y = 95
    bottom_y = H - 70

    # Draw lifelines
    for idx, lf in enumerate(lifelines):
        cx = xs[idx]
        # Header box
        draw.rounded_rectangle([cx - 110, top_y, cx + 110, top_y + 58], radius=4, fill=(224, 242, 254), outline=(2, 132, 199), width=2)
        draw.text((cx - 95, top_y + 8), f"<<{lf['stereotype']}>>", fill=(3, 105, 161), font=f_stereo)
        draw.text((cx - 95, top_y + 28), lf["name"][:24], fill=(15, 23, 42), font=f_box)

        # Dashed line
        y_cur = top_y + 58
        while y_cur < bottom_y:
            draw.line([cx, y_cur, cx, min(y_cur + 10, bottom_y)], fill=(100, 116, 139), width=2)
            y_cur += 18

        # Activation bar
        msg_start_y = top_y + 85
        msg_end_y = top_y + 85 + len(messages) * 60
        draw.rectangle([cx - 7, msg_start_y, cx + 7, msg_end_y], fill=(186, 230, 253), outline=(2, 132, 199), width=1)

    # Draw messages
    for m_idx, msg in enumerate(messages):
        my = top_y + 100 + m_idx * 60
        s_i = min(msg.get("fromIdx", 0), n - 1)
        t_i = min(msg.get("toIdx", min(1, n - 1)), n - 1)
        x1, x2 = xs[s_i], xs[t_i]
        is_ret = msg.get("isReturn", False)
        color = (71, 85, 105) if is_ret else (15, 23, 42)
        if x1 == x2:
            # Self call
            draw.line([x1 + 7, my, x1 + 48, my], fill=color, width=2)
            draw.line([x1 + 48, my, x1 + 48, my + 24], fill=color, width=2)
            draw.line([x1 + 48, my + 24, x1 + 7, my + 24], fill=color, width=2)
            draw.text((x1 + 56, my + 2), f"{m_idx + 1}: {msg['label'][:52]}", fill=color, font=f_msg)
        else:
            if is_ret:
                # Dashed return arrow
                cur_x = min(x1, x2)
                while cur_x < max(x1, x2):
                    draw.line([cur_x, my, min(cur_x + 10, max(x1, x2)), my], fill=color, width=2)
                    cur_x += 16
            else:
                draw.line([x1, my, x2, my], fill=color, width=2)
            # Arrowhead at x2
            direction = 1 if x2 > x1 else -1
            draw.polygon([(x2, my), (x2 - direction * 10, my - 5), (x2 - direction * 10, my + 5)], fill=color)
            tx = min(x1, x2) + 18
            draw.text((tx, my - 22), f"{m_idx + 1}: {msg['label'][:65]}", fill=color, font=f_msg)

    img.save(out_path, "PNG", optimize=True)

def render_class_diagram_36_png(out_path: str):
    """Render a crisp 2400x1400 Class Diagram PNG for 3.6 Content & Workflow."""
    W, H = 2400, 1400
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    f_title = get_font(24, True)
    f_cls = get_font(16, True)
    f_stereo = get_font(13, False)
    f_mem = get_font(13, False)

    draw.rectangle([16, 16, W - 16, H - 16], outline=(100, 116, 139), width=2)
    draw.text((36, 30), "cd 3.6 - Content & Workflow Class Diagram", fill=(15, 23, 42), font=f_title)

    classes = [
        ("TaskController", "Controller", ["+ getTaskDetail(taskId)", "+ assignTask(taskId, req)", "+ updateTaskStatus(taskId)", "+ filterTasks(criteria)"]),
        ("TaskService", "Service", ["+ identifyTaskDetail(id, dto)", "+ assignCreatorAndQc(id, dto)", "+ submitApprovalStep(id, dto)", "+ listByViewMode(workspaceId, view)"]),
        ("Task", "Entity", ["- id: UUID", "- workspaceId: UUID", "- campaignId: UUID", "- title: String", "- taskType: TaskType", "- status: TaskStatus", "- assigneeId: UUID", "- scheduledAt: Instant"]),
        ("TaskApproval", "Entity", ["- id: UUID", "- taskId: UUID", "- stepOrder: Integer", "- approverRole: WorkspaceRole", "- decision: ApprovalStatus", "- feedbackComment: String"]),
        ("TaskComment", "Entity", ["- id: UUID", "- taskId: UUID", "- authorId: UUID", "- parentCommentId: UUID", "- content: String", "- attachments: List<String>"]),
        ("ContentVersion", "Entity", ["- id: UUID", "- taskId: UUID", "- versionNumber: Integer", "- bodyUnicode: String", "- editorId: UUID", "- createdAt: Instant"]),
        ("MaterialRepositoryController", "Controller", ["+ listMaterials(workspaceId)", "+ uploadMaterial(req)", "+ updateMetadata(id, req)", "+ applyWatermark(id, cfg)"]),
        ("MaterialService", "Service", ["+ uploadAndClassify(file, type)", "+ connectGoogleDrive(code)", "+ syncDriveFolder(folderId)", "+ renderWatermarkedCopy(id, cfg)"]),
        ("MaterialAsset", "Entity", ["- id: UUID", "- workspaceId: UUID", "- category: MaterialCategory", "- s3Key: String", "- isRawRestricted: Boolean", "- watermarkApplied: Boolean"]),
        ("HashtagCollection", "Entity", ["- id: UUID", "- workspaceId: UUID", "- name: String", "- purposeType: HashtagPurpose", "- tags: List<String>", "- isDeleted: Boolean"]),
        ("SurveyService", "Service", ["+ createSurveyForm(workspaceId, dto)", "+ getSurveyAnalytics(surveyId)", "+ generateMeetingLink(workspaceId)"]),
        ("MailTemplateService", "Service", ["+ listTemplates(workspaceId)", "+ createTemplate(dto)", "+ sendTemplatedEmail(id, recipients)", "+ checkContentCompliance(text)"]),
    ]

    cols = 4
    box_w, box_h = 510, 340
    start_x, start_y = 60, 100
    gap_x, gap_y = 560, 410

    centers = []
    for i, (cname, stereo, members) in enumerate(classes):
        r = i // cols
        c = i % cols
        x = start_x + c * gap_x
        y = start_y + r * gap_y
        centers.append((x + box_w // 2, y + box_h // 2))
        draw.rounded_rectangle([x, y, x + box_w, y + box_h], radius=6, fill=(254, 249, 195), outline=(161, 98, 7), width=2)
        draw.rectangle([x, y, x + box_w, y + 64], fill=(253, 224, 71), outline=(161, 98, 7), width=2)
        draw.text((x + 18, y + 10), f"<<{stereo}>>", fill=(113, 63, 18), font=f_stereo)
        draw.text((x + 18, y + 32), cname, fill=(15, 23, 42), font=f_cls)
        my = y + 80
        for m in members:
            draw.text((x + 18, my), m, fill=(30, 41, 59), font=f_mem)
            my += 32

    # Draw relationship lines between rows
    edges = [(0, 1), (1, 2), (2, 3), (2, 4), (2, 5), (6, 7), (7, 8), (1, 9), (1, 10), (1, 11)]
    for a, b in edges:
        x1, y1 = centers[a]
        x2, y2 = centers[b]
        draw.line([x1, y1, x2, y2], fill=(100, 116, 139), width=2)

    img.save(out_path, "PNG", optimize=True)

print("Helper functions loaded successfully.")

