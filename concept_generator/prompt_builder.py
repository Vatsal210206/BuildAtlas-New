from typing import Dict, Any


PROJECT_CONTEXTS = {
    "house": "Prioritize privacy, daylight, family circulation, and a calm balance between shared family living and service efficiency.",
    "villa": "Prioritize amenity clustering, guest privacy, outdoor leisure, and a strong luxury-facing public spine with a quiet private family wing.",
    "duplex": "Balance independent circulation with shared utility logic and a clear floor-wise ownership split.",
    "apartment": "Optimize repeatable unit layouts, service efficiency, and common-area circulation for scale.",
    "resort": "Prioritize guest privacy, distinct service circulation, and a central hospitality spine around amenities.",
    "commercial": "Prioritize frontage visibility, loading clarity, and efficient visitor movement.",
    "office": "Prioritize collaboration, executive privacy, and a clean people-to-service adjacency hierarchy.",
    "warehouse": "Prioritize logistics flow, dock access, clear-span storage, and safety-driven circulation.",
}


def _format_requirements_block(structured_requirements: Dict[str, Any]) -> str:
    if not structured_requirements:
        return "- None provided"
    return "\n".join(f"- {key}: {value}" for key, value in structured_requirements.items())


def build_prompt(project_type: str, structured_requirements: Dict[str, Any], lifestyle_context: str, plot_info: Dict[str, Any], variant_hint: str = "") -> str:
    project_context = PROJECT_CONTEXTS.get(project_type, "Prioritize clear zoning logic, adjacency logic, and a concise conceptual story.")
    structured_block = _format_requirements_block(structured_requirements)
    plot_width = plot_info.get("plot_width", 0)
    plot_length = plot_info.get("plot_length", 0)
    orientation = plot_info.get("orientation", "North")
    site_note = plot_info.get("site_note", "None provided")
    lifestyle_context = lifestyle_context.strip() or "No lifestyle notes supplied."
    variant_hint = variant_hint.strip()

    prompt = f"""You are an experienced conceptual architect assistant generating a non-binding early-stage concept report.

System role:
- Act as a conceptual architect assistant.
- Never claim structural validity, code compliance, engineering feasibility, or permit readiness.
- Reason from zoning, adjacency, privacy, circulation, and lifestyle fit.
- Keep the output factual, concise, and visualizable.

Project type context paragraph:
{project_context}

Structured requirements block (Step 3 answers):
{structured_block}

Plot and site information:
- Plot width: {plot_width} ft
- Plot length: {plot_length} ft
- Orientation: {orientation}
- Site note: {site_note}

Lifestyle context (Step 4, client's own words):
{lifestyle_context}

Optional variant note:
{variant_hint if variant_hint else 'None'}

Output contract:
Return a single JSON object with exactly these top-level keys in this order:
1. concept_summary
2. zoning_logic
3. space_allocation
4. adjacency_rationale
5. future_expansion
6. disclaimer
7. diagram

Rules for the response:
- concept_summary: one short paragraph explaining the concept story.
- zoning_logic: an array of concise bullet-like strings describing the zoning logic.
- space_allocation: an array of objects, each shaped as {{"zone_name": "...", "area_sqft": <number>, "percent": <number>}}.
- adjacency_rationale: an array of concise strings explaining the adjacency rationale.
- future_expansion: an array of concise strings describing future expansion options.
- disclaimer: a short, standard conceptual-only disclaimer.
- diagram: a list of objects using the same zone names and areas as the space_allocation list, each shaped as {{"label": "...", "area": <number>, "adjacency": ["..."]}}.

Important: The final response must be distinct for different Step 3 and Step 4 inputs. Use the project type context, structured requirements, plot, and lifestyle notes to create a differentiated concept rather than a fixed template.
"""
    return prompt
