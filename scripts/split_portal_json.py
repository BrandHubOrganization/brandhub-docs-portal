#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Splits the monolithic src/data/portalData.json into small, clean, easy-to-edit JSON files
organized by Report (figures/) and by Functional Domain (frs/).
"""
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "src" / "data"
MONO_JSON = DATA_DIR / "portalData.json"


def save_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Created: {path.relative_to(BASE_DIR)} ({len(obj) if isinstance(obj, list) else 'dict'} items)")


def simplify_figure(fig: dict) -> dict:
    """Keep clean, easy-to-edit fields in each figure JSON."""
    out = {
        "id": fig["id"],
        "figNum": fig["figNum"],
        "reportId": fig["reportId"],
        "reportName": fig["reportName"],
        "section": fig["section"],
        "category": fig["category"],
        "title": fig["title"],
        "caption": fig["caption"],
        "imageUrl": fig["imageUrl"],
        "imageWidth": fig.get("imageWidth", 0),
        "imageHeight": fig.get("imageHeight", 0),
        "actors": fig.get("actors", []),
        "summary": fig.get("summary", ""),
        "viSummary": fig.get("viSummary", ""),
        "components": fig.get("components", []),
    }
    # Optional fields only when present so JSON stays clean and uncluttered
    for opt_key in [
        "domainCode",
        "domainTitle",
        "frCode",
        "ucId",
        "trigger",
        "interface",
        "dataProcessing",
        "dataSpecs",
        "businessRules",
        "linkedBrCodes",
        "linkedMsgCodes",
        "validations",
        "normalFlow",
        "abnormalCases",
        "postConditions",
        "lifelines",
        "sequenceMessages",
        "screenFigureId",
        "sequenceFigureId",
        "classDiagramFigureId",
        "subImages",
    ]:
        val = fig.get(opt_key)
        if val:
            out[opt_key] = val
    return out


def main():
    raw = json.loads(MONO_JSON.read_text(encoding="utf-8"))

    # 1. project.json (general info, reports, domains, actors)
    save_json(
        DATA_DIR / "project.json",
        {
            "projectInfo": raw["projectInfo"],
            "reports": raw["reports"],
            "domains": raw["domains"],
            "actors": raw["actors"],
        },
    )

    # 2. Split Figures into 6 clean files under src/data/figures/
    figures = [simplify_figure(f) for f in raw["figures"]]
    r1_figs = [f for f in figures if f["reportId"] == "report1"]
    r2_figs = [f for f in figures if f["reportId"] == "report2"]
    r3_overview_figs = [
        f for f in figures if f["reportId"] == "report3" and f["figNum"] <= 9
    ]
    r3_screen_figs = [
        f for f in figures if f["reportId"] == "report3" and f["figNum"] >= 10
    ]
    r4_class_figs = [
        f for f in figures if f["reportId"] == "report4" and f["id"].startswith("cd-")
    ]
    r4_seq_figs = [
        f for f in figures if f["reportId"] == "report4" and f["id"].startswith("seq-")
    ]

    save_json(DATA_DIR / "figures" / "report1.json", r1_figs)
    save_json(DATA_DIR / "figures" / "report2.json", r2_figs)
    save_json(DATA_DIR / "figures" / "report3-overview.json", r3_overview_figs)
    save_json(DATA_DIR / "figures" / "report3-screens.json", r3_screen_figs)
    save_json(DATA_DIR / "figures" / "report4-class.json", r4_class_figs)
    save_json(DATA_DIR / "figures" / "report4-sequence.json", r4_seq_figs)

    # 3. Split 141 FRs into 9 domain files under src/data/frs/domain-3.x.json
    frs = raw["frs"]
    for dom in raw["domains"]:
        d_code = dom["code"]
        dom_frs = [fr for fr in frs if fr["domainCode"] == d_code]
        save_json(DATA_DIR / "frs" / f"domain-{d_code}.json", dom_frs)

    # 4. useCases.json, rulesAndMessages.json, matrices.json
    save_json(DATA_DIR / "useCases.json", raw["useCases"])
    save_json(
        DATA_DIR / "rulesAndMessages.json",
        {
            "businessRules": raw["businessRules"],
            "messages": raw["messages"],
        },
    )
    save_json(
        DATA_DIR / "matrices.json",
        {
            "screenDescriptions": raw["screenDescriptions"],
            "screenAuthorization": raw["screenAuthorization"],
            "nonScreenFunctions": raw["nonScreenFunctions"],
            "entities": raw["entities"],
        },
    )

    # Remove monolithic portalData.json so there is only 1 source of truth
    if MONO_JSON.exists():
        MONO_JSON.unlink()
        print("Removed monolithic src/data/portalData.json")


if __name__ == "__main__":
    main()
