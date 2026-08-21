# zoning_diagram.py — full replacement

import html
import math


def _layout_blocks(blocks):
    n = len(blocks)
    cols = min(4, n) if n > 0 else 1
    rows = math.ceil(n / cols) if cols else 1
    canvas_width = 700
    margin_x = 40
    gap_x = 20
    box_height = 140
    gap_y = 30
    top_offset = 50
    box_width = (canvas_width - 2 * margin_x - (cols - 1) * gap_x) / cols
    grid_bottom = top_offset + rows * box_height + (rows - 1) * gap_y
    return {
        "cols": cols, "rows": rows, "canvas_width": canvas_width,
        "margin_x": margin_x, "gap_x": gap_x, "box_height": box_height,
        "gap_y": gap_y, "top_offset": top_offset, "box_width": box_width,
        "grid_bottom": grid_bottom,
    }


def get_diagram_height(report: dict) -> int:
    """Call this from ui_flow.py to size the streamlit_html component correctly."""
    blocks = report.get("diagram") or report.get("space_allocation") or [{}, {}, {}]
    layout = _layout_blocks(blocks)
    return int(layout["grid_bottom"] + 40 + 30 + 20)


def generate_zoning_diagram_svg(report: dict) -> str:
    blocks = report.get("diagram", []) or []
    if not blocks:
        blocks = []
        for item in report.get("space_allocation", []) or []:
            blocks.append({
                "label": item.get("zone_name") or item.get("space") or "Zone",
                "area": item.get("area_sqft") or item.get("area") or 0,
            })

    if not blocks:
        blocks = [
            {"label": "Public / Guest Facing", "area": 1200},
            {"label": "Private / Living", "area": 900},
            {"label": "Service / Back of House", "area": 600},
        ]

    colors = ["#00e5b0", "#ff6b35", "#1a9cff", "#c77dff", "#ffd166", "#06d6a0", "#ef476f"]
    total_area = sum(max(1, int(b.get("area", 0) or 0)) for b in blocks)
    layout = _layout_blocks(blocks)
    cols, box_width = layout["cols"], layout["box_width"]
    box_height, gap_x, gap_y = layout["box_height"], layout["gap_x"], layout["gap_y"]
    margin_x, top_offset = layout["margin_x"], layout["top_offset"]
    canvas_width, grid_bottom = layout["canvas_width"], layout["grid_bottom"]

    items = []
    for index, block in enumerate(blocks):
        label = html.escape(str(block.get("label", f"Zone {index + 1}")))
        area = int(block.get("area", 0) or 0)
        pct = round((area / total_area) * 100, 1) if total_area else 0
        row, col = index // cols, index % cols
        x = margin_x + col * (box_width + gap_x)
        y = top_offset + row * (box_height + gap_y)
        color = colors[index % len(colors)]

        items.append(
            f'''<rect x="{x:.1f}" y="{y:.1f}" width="{box_width:.1f}" height="{box_height}" rx="18" fill="{color}" fill-opacity="0.22" stroke="{color}" stroke-width="2" />
            <text x="{x + box_width / 2:.1f}" y="{y + 40}" text-anchor="middle" fill="#ffffff" font-size="15" font-family="Syne" font-weight="700">{label}</text>
            <text x="{x + box_width / 2:.1f}" y="{y + 72}" text-anchor="middle" fill="#8fb4d9" font-size="13" font-family="JetBrains Mono">Approx. {area} sq ft</text>
            <text x="{x + box_width / 2:.1f}" y="{y + 98}" text-anchor="middle" fill="#00e5b0" font-size="12" font-family="JetBrains Mono">{pct}% of concept area</text>'''
        )

    footer_y = grid_bottom + 40
    canvas_height = footer_y + 30

    svg = f'''<svg width="100%" height="{canvas_height}" viewBox="0 0 {canvas_width} {canvas_height}" xmlns="http://www.w3.org/2000/svg" style="background:#08101d;border-radius:16px;">
        <defs>
            <pattern id="bg-grid" width="20" height="20" patternUnits="userSpaceOnUse">
                <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#10203a" stroke-width="1" />
            </pattern>
        </defs>
        <rect width="{canvas_width}" height="{canvas_height}" fill="url(#bg-grid)" />
        <text x="{canvas_width/2}" y="26" text-anchor="middle" fill="#00e5b0" font-size="18" font-family="Syne" font-weight="700">ZONING DIAGRAM</text>
        {''.join(items)}
        <line x1="{margin_x + box_width/2}" y1="{grid_bottom + 20}" x2="{canvas_width - margin_x - box_width/2}" y2="{grid_bottom + 20}" stroke="#00e5b0" stroke-width="2" stroke-dasharray="8 5" />
        <text x="{canvas_width/2}" y="{footer_y}" text-anchor="middle" fill="#8fb4d9" font-size="12" font-family="JetBrains Mono">Adjacency Spine / Public → Private → Service</text>
    </svg>'''
    return svg