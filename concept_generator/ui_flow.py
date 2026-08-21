import html as html_escape
import time

import streamlit as st
from streamlit.components.v1 import html as streamlit_html
from floorplan_engine import LayoutSolver, calculate_vastu_score, calculate_cost, render_professional_floorplan
from .project_types import PROJECT_TYPES, get_project_type_config, get_plot_dimension_bounds
from .requirement_schemas import get_requirement_schema
from .prompt_builder import build_prompt
from .ai_client import ConceptGeneratorClient
from .report_parser import normalize_report
from .zoning_diagram import generate_zoning_diagram_svg, get_diagram_height

SECONDARY_TEXT_COLOR = "#b0c9e3"


def _render_secondary_caption(text: str, *, margin_top: str = "0.25rem", margin_bottom: str = "0.75rem"):
    st.markdown(
        f"<div style='font-size:0.82rem; color:{SECONDARY_TEXT_COLOR}; margin-top:{margin_top}; margin-bottom:{margin_bottom};'>{html_escape.escape(text)}</div>",
        unsafe_allow_html=True,
    )


def _mark_touched(field_key: str):
    st.session_state[f"touched_{field_key}"] = True


def render_project_type_selector():
    st.markdown("<div class='ba-card-title'>Select Project Type</div>", unsafe_allow_html=True)
    columns = st.columns(4)
    project_items = list(PROJECT_TYPES.items())
    selected_key = st.session_state.get("concept_project_type")

    for idx, (key, config) in enumerate(project_items):
        with columns[idx % 4]:
            card = st.container(border=True)
            card.markdown(f"<div style='text-align:center; padding:8px;'><div style='font-size:28px'>{config['icon']}</div><div style='font-weight:700;'>{config['name']}</div><div style='font-size:12px; color:#8fb4d9;'>{config['description']}</div></div>", unsafe_allow_html=True)
            if card.button(f"Select {config['name']}", key=f"select_{key}", use_container_width=True):
                st.session_state["concept_project_type"] = key
                st.session_state["touched_concept_project_type"] = True
                st.rerun()

    if selected_key:
        st.success(f"Selected: {PROJECT_TYPES[selected_key]['name']}")


def render_plot_step():
    project_key = st.session_state.get("concept_project_type", "house")
    project_type_name = PROJECT_TYPES[project_key]["name"]
    bounds = get_plot_dimension_bounds(project_key)
    min_value = bounds["min"]
    max_value = bounds["max"]

    st.session_state.setdefault("concept_plot_width", None)
    st.session_state.setdefault("concept_plot_length", None)
    st.session_state.setdefault("concept_orientation", None)
    st.session_state.setdefault("concept_site_note", "")

    st.markdown("<div class='ba-card-title'>Plot & Site Information</div>", unsafe_allow_html=True)
    _render_secondary_caption(f"Plot size limits are tuned for {project_type_name}: {min_value} ft to {max_value} ft.")

    col1, col2 = st.columns(2)
    with col1:
        plot_width = st.number_input(
            "Plot Width (ft)",
            min_value=min_value,
            max_value=max_value,
            step=5,
            value=st.session_state.get("concept_plot_width"),
            key="concept_plot_width",
            placeholder="Enter plot width in ft",
            help=f"Valid plot width range for {project_type_name}: {min_value} to {max_value} ft.",
        )
        orientation_options = ["— Select orientation —", "North", "South", "East", "West"]
        orientation_value = st.session_state.get("concept_orientation")
        orientation_index = orientation_options.index(orientation_value) if orientation_value in orientation_options else 0
        orientation_value = st.selectbox(
            "Orientation",
            orientation_options,
            index=orientation_index,
            key="concept_orientation",
        )
    with col2:
        plot_length = st.number_input(
            "Plot Length (ft)",
            min_value=min_value,
            max_value=max_value,
            step=5,
            value=st.session_state.get("concept_plot_length"),
            key="concept_plot_length",
            placeholder="Enter plot length in ft",
            help=f"Valid plot length range for {project_type_name}: {min_value} to {max_value} ft.",
        )
        site_note = st.text_input(
            "Site note / city hint",
            value=st.session_state.get("concept_site_note", ""),
            placeholder="Enter a short site note or city hint",
            key="concept_site_note",
        )

    # Keep the canonical plot state in session_state via Streamlit's widget state.
    _ = (plot_width, plot_length, orientation_value, site_note)


def render_requirements_step():
    project_key = st.session_state.get("concept_project_type", "house")
    schema = get_requirement_schema(project_key)
    st.markdown(f"<div class='ba-card-title'>Functional Requirements - {PROJECT_TYPES[project_key]['name']}</div>", unsafe_allow_html=True)
    for section in schema.get("sections", []):
        st.markdown(f"<div class='ba-card-title'> {section['title']} </div>", unsafe_allow_html=True)
        for field in section["fields"]:
            render_field(field)

    if schema.get("advanced"):
        with st.expander("Advanced", expanded=False):
            for field in schema["advanced"]:
                render_field(field)


def render_field(field: dict):
    # Do not assign to st.session_state[key] after this widget renders — use the widget's
    # return value instead. This caused two production bugs already (Bedrooms, Orientation).
    key = field['key']
    field_key = f"concept_{key}"
    field_type = field.get('type', 'text')

    if field_key not in st.session_state:
        if field_type == 'number':
            default_value = field.get('default')
            if default_value is None:
                default_value = field.get('min', 0)
            st.session_state[field_key] = default_value
        elif field_type == 'slider':
            default_value = field.get('default')
            if default_value is None:
                default_value = field.get('min', 0)
            st.session_state[field_key] = default_value
        elif field_type == 'select':
            options = field.get('options', [])
            neutral_option = field.get('neutral_option', '— Select —')
            if not options or options[0] != neutral_option:
                options = [neutral_option] + options
            default_value = field.get('default')
            if default_value is None:
                default_value = neutral_option if neutral_option in options else (options[0] if options else "")
            elif default_value not in options:
                default_value = neutral_option if neutral_option in options else (options[0] if options else "")
            st.session_state[field_key] = default_value
        else:
            default_value = field.get('default')
            st.session_state[field_key] = '' if default_value is None else str(default_value)

    value = st.session_state.get(field_key)
    if field_type == 'number':
        min_value = field.get('min', 0)
        max_value = field.get('max', 999)
        step = field.get('step', 1)
        numeric_type = float if any(isinstance(v, float) for v in [min_value, max_value, value]) else int

        if numeric_type is float:
            if not isinstance(value, (int, float)):
                value = field.get('default', field.get('min', 0))
            min_value = float(min_value)
            max_value = float(max_value)
            step = float(step)
        else:
            if not isinstance(value, (int, float)):
                value = field.get('default', field.get('min', 0))
            min_value = int(min_value)
            max_value = int(max_value)
            step = int(step)

        st.number_input(
            field['label'],
            min_value=min_value,
            max_value=max_value,
            step=step,
            placeholder=field.get('placeholder', f"Enter {field['label'].lower()}"),
            key=field_key,
            on_change=_mark_touched,
            args=(field_key,),
        )
    elif field_type == 'slider':
        if not isinstance(value, (int, float)):
            value = field.get('default', field.get('min', 0))
            st.session_state[field_key] = value
        st.slider(
            field['label'],
            min_value=field.get('min', 0),
            max_value=field.get('max', 10),
            key=field_key,
            on_change=_mark_touched,
            args=(field_key,),
        )
    elif field_type == 'select':
        options = field.get('options', [])
        neutral_option = field.get('neutral_option', '— Select —')
        if not options or options[0] != neutral_option:
            options = [neutral_option] + options
        if value not in options:
            value = neutral_option if neutral_option in options else (options[0] if options else "")
            st.session_state[field_key] = value
        st.selectbox(
            field['label'],
            options,
            key=field_key,
            on_change=_mark_touched,
            args=(field_key,),
        )
    else:
        st.text_input(
            field['label'],
            placeholder=field.get('placeholder', f"Enter {field['label'].lower()}"),
            key=field_key,
            on_change=_mark_touched,
            args=(field_key,),
        )


def render_context_step():
    project_key = st.session_state.get("concept_project_type", "house")
    placeholder = {
        "house": "e.g. We host large family gatherings twice a year and want a big veranda...",
        "villa": "e.g. We want a guest-friendly private villa with a strong outdoor living feel and a quiet family wing...",
        "resort": "e.g. A family-run boutique resort with guests expecting privacy, a central courtyard feel, and minimal service noise...",
        "office": "e.g. This office needs privacy for leadership and openness for team collaboration...",
        "warehouse": "e.g. We need a high-clear-span storage block with good access for trucks and fast loading...",
    }.get(project_key, "Tell us about how you'll use this space")

    if "concept_lifestyle_context" not in st.session_state:
        st.session_state["concept_lifestyle_context"] = st.session_state.get("concept_lifestyle", "")

    st.text_area(
        "Lifestyle / Business Context",
        key="concept_lifestyle_context",
        placeholder=placeholder,
        on_change=_mark_touched,
        args=("concept_lifestyle_context",),
    )


def _render_generation_status_messages(status_callback=None):
    st.markdown("<div class='ba-card-title'>Generating Concept</div>", unsafe_allow_html=True)
    status_steps = [
        "Understanding your requirements",
        "Mapping zoning logic",
        "Drafting your concept",
        "Preparing the report",
    ]
    status_placeholder = st.empty()
    for idx, step in enumerate(status_steps):
        message = f"{'●' if idx == 0 else '○'} {step}"
        if status_callback is not None:
            status_callback(message)
        else:
            status_placeholder.info(message)
        st.markdown(f"<div style='padding:6px 0; color:#8fb4d9;'>{message}</div>", unsafe_allow_html=True)
        time.sleep(0.8)
    st.markdown("<div style='height:20px;' />", unsafe_allow_html=True)
    st.info("Conceptual visualization only — consult a licensed architect before construction.")


def _build_villa_amenities() -> list:
    amenities = []
    if st.session_state.get("concept_pool") == "Yes":
        amenities.append("Swimming Pool")
    if st.session_state.get("concept_home_theatre") == "Yes":
        amenities.append("Home Theatre")
    if st.session_state.get("concept_gym") == "Yes":
        amenities.append("Home Gym")
    if st.session_state.get("concept_guest_suite") == "Yes":
        amenities.append("Guest Suite")
    if st.session_state.get("concept_staff_quarters") == "Yes":
        amenities.append("Servant Room")
    if isinstance(st.session_state.get("concept_garden_extent"), (int, float)) and st.session_state.get("concept_garden_extent", 0) >= 6:
        amenities.append("Backyard Garden")
    return amenities


def render_detailed_layout_step():
    project_key = st.session_state.get("concept_project_type", "house")
    st.markdown("<div class='ba-card-title'>Detailed Layout Preview</div>", unsafe_allow_html=True)

    if project_key != "villa":
        st.info(
            "Detailed villa layout preview is available for the Villa project type only. "
            "Other project types will retain concept-level output without a professional layout preview."
        )
        return

    plot_width = st.session_state.get("concept_plot_width")
    plot_length = st.session_state.get("concept_plot_length")

    bedrooms = st.session_state.get("concept_bedrooms", 4)
    bathrooms = st.session_state.get("concept_bathrooms", 4)
    amenities = _build_villa_amenities()

    if not isinstance(plot_width, (int, float)) or not isinstance(plot_length, (int, float)):
        st.warning("Plot dimensions are missing. Please complete Step 2 (Plot & Site) before generating a detailed layout.")
        if st.button("Go to Plot & Site", key="go_to_plot_step"):
            st.session_state["concept_step"] = 1
            st.rerun()
        return

    st.markdown(f"<div style='margin-bottom:12px; color:#e8edf5;'>Bedrooms: {bedrooms}, Bathrooms: {bathrooms}, Plot: {plot_width} x {plot_length} ft</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='margin-bottom:8px; color:#e8edf5;'>Villa amenities included: {', '.join(amenities) if amenities else 'None selected'}</div>", unsafe_allow_html=True)

    if st.button("Generate Villa Layout Preview", key="generate_villa_layout_preview"):
        try:
            solver = LayoutSolver(plot_width, plot_length, bedrooms, bathrooms, amenities, vastu_mode="Strict")
            rooms, outdoor_amenities = solver.solve()
            svg_code = render_professional_floorplan(plot_width, plot_length, rooms, outdoor_amenities, "Strict")
            st.session_state["concept_villa_layout_svg"] = svg_code
            st.session_state["concept_villa_layout_meta"] = {
                "buildup_area": sum(r.area for r in rooms),
                "vastu_score": calculate_vastu_score("Strict", plot_width, plot_length, rooms),
                "total_cost": calculate_cost(sum(r.area for r in rooms), amenities)[0],
                "duration_days": calculate_cost(sum(r.area for r in rooms), amenities)[2],
                "outdoor_amenities": outdoor_amenities,
            }
        except Exception as exc:
            st.error(f"Unable to build the villa layout preview: {exc}")
            st.session_state.pop("concept_villa_layout_svg", None)
            st.session_state.pop("concept_villa_layout_meta", None)

    if st.session_state.get("concept_villa_layout_svg"):
        svg_code = st.session_state["concept_villa_layout_svg"]
        streamlit_html(svg_code, height=700, scrolling=True)
        meta = st.session_state.get("concept_villa_layout_meta", {})
        st.markdown(
            f"<div style='margin-top:14px; color:#e8edf5;'>"
            f"<b>Estimated Buildup Area:</b> {meta.get('buildup_area', 0):.0f} sq ft &nbsp; | &nbsp; "
            f"<b>Vastu Score:</b> {meta.get('vastu_score', 0)} / 100 &nbsp; | &nbsp; "
            f"<b>Estimated Cost:</b> ₹{meta.get('total_cost', 0):,} &nbsp; | &nbsp; "
            f"<b>Construction Duration:</b> {meta.get('duration_days', 0)} days"
            f"</div>",
            unsafe_allow_html=True,
        )
    else:
        st.info("Press the button above to generate a villa layout preview with strict Vastu placement.")


def render_output_step():
    report = st.session_state.get("concept_report")
    if not report:
        st.warning("No concept generated yet. Go back to the Lifestyle Context step and generate a concept.")
        return

    st.markdown("<div class='ba-card-title'>Concept Output</div>", unsafe_allow_html=True)
    left, right = st.columns([1, 1])
    with left:
        streamlit_html(generate_zoning_diagram_svg(report), height=get_diagram_height(report), scrolling=False)
    with right:
        def _build_section_card(header: str, body_html: str) -> str:
            return (
                f"<div style='margin-bottom:18px;'>"
                f"<div style='color:#f4a261; text-transform:uppercase; letter-spacing:1.2px; font-size:11px; font-weight:700; margin-bottom:8px;'>{html_escape.escape(header)}</div>"
                f"<div style='background:rgba(26,35,56,0.6); border:1px solid #16304a; border-radius:10px; padding:14px; box-shadow:0 0 0 1px rgba(255,255,255,0.02) inset;'>"
                f"{body_html}"
                f"</div>"
                f"</div>"
            )

        def _render_bullets(items: list) -> str:
            if not items:
                return "<div style='color:#e8edf5; font-size:15px; line-height:1.65;'>No items available.</div>"
            bullets = []
            for item in items:
                text = html_escape.escape(str(item))
                bullets.append(
                    f"<div style='display:flex; gap:8px; align-items:flex-start; margin:0 0 8px 0;'>"
                    f"<span style='color:#f4a261; font-size:16px; line-height:1.4;'>•</span>"
                    f"<span style='color:#e8edf5; font-size:15px; line-height:1.65;'>{text}</span>"
                    f"</div>"
                )
            return "".join(bullets)

        def _render_space_allocation(items: list) -> str:
            if not items:
                return "<div style='color:#e8edf5; font-size:15px; line-height:1.65;'>No allocation details available.</div>"
            bullets = []
            for item in items:
                zone_name = html_escape.escape(str(item.get('zone_name', item.get('space', 'Zone'))))
                area_sqft = item.get('area_sqft', item.get('area', 0))
                percent = item.get('percent', item.get('pct', 0))
                bullets.append(
                    f"<div style='display:flex; gap:8px; align-items:flex-start; margin:0 0 8px 0;'>"
                    f"<span style='color:#f4a261; font-size:16px; line-height:1.4;'>•</span>"
                    f"<span style='color:#e8edf5; font-size:15px; line-height:1.65;'>{zone_name}: {area_sqft} sq ft ({percent}%)</span>"
                    f"</div>"
                )
            return "".join(bullets)

        concept_summary = html_escape.escape(str(report.get('concept_summary', '')))
        st.markdown(
            _build_section_card(
                "Concept Summary",
                f"<p style='margin:0; color:#e8edf5; font-size:15px; line-height:1.65;'>{concept_summary}</p>",
            ),
            unsafe_allow_html=True,
        )

        st.markdown(
            _build_section_card(
                "Zoning Logic",
                _render_bullets(report.get('zoning_logic', [])),
            ),
            unsafe_allow_html=True,
        )

        st.markdown(
            _build_section_card(
                "Space Allocation",
                _render_space_allocation(report.get('space_allocation', [])),
            ),
            unsafe_allow_html=True,
        )

        st.markdown(
            _build_section_card(
                "Adjacency Rationale",
                _render_bullets(report.get('adjacency_rationale', [])),
            ),
            unsafe_allow_html=True,
        )

        st.markdown(
            _build_section_card(
                "Future Expansion Ideas",
                _render_bullets(report.get('future_expansion', [])),
            ),
            unsafe_allow_html=True,
        )

        disclaimer_html = (
            f"<div style='background:rgba(11,19,36,0.9); border:1px solid #00e5b0; border-radius:10px; padding:14px; color:#00e5b0; font-size:15px; line-height:1.65;'>"
            f"{html_escape.escape(str(report.get('disclaimer', '')))}"
            f"</div>"
        )
        st.markdown(
            f"<div style='margin-bottom:18px;'>"
            f"<div style='color:#f4a261; text-transform:uppercase; letter-spacing:1.2px; font-size:11px; font-weight:700; margin-bottom:8px;'>Disclaimer</div>"
            f"{disclaimer_html}"
            f"</div>",
            unsafe_allow_html=True,
        )


def render_export_step():
    st.markdown("<div class='ba-card-title'>Export</div>", unsafe_allow_html=True)
    report = st.session_state.get("concept_report")
    if not report:
        st.info("Generate a concept first to prepare export-ready information.")
        return

    report_text = report.get("concept_summary", "") or "Concept report ready."
    st.info("Your concept report is ready for export.")
    st.download_button(
        label="Download concept summary",
        data=report_text,
        file_name="concept_summary.txt",
        mime="text/plain",
        key="download_concept_summary",
    )


def validate_step(step_index: int):
    if step_index == 0:
        project_type = st.session_state.get("concept_project_type")
        if project_type in (None, ""):
            return False, "Please select a project type before continuing."
        return True, ""

    if step_index == 1:
        plot_width = st.session_state.get("concept_plot_width")
        plot_length = st.session_state.get("concept_plot_length")
        if plot_width in (None, "", 0) or plot_length in (None, "", 0):
            return False, "Please provide valid plot width and plot length before continuing."
        return True, ""

    if step_index == 2:
        project_key = st.session_state.get("concept_project_type", "house")
        schema = get_requirement_schema(project_key)
        invalid_fields = []

        def _mark_if_required(field: dict):
            if field.get("required") is not True:
                return

            key = field["key"]
            field_key = f"concept_{key}"
            stored_value = st.session_state.get(field_key)
            neutral_value = field.get("neutral_option", "— Select —")

            if stored_value is None:
                invalid_fields.append(field["label"])
                return

            if field["type"] == "select":
                if stored_value == neutral_value:
                    invalid_fields.append(field["label"])
                return

            if isinstance(stored_value, str):
                if not stored_value.strip():
                    invalid_fields.append(field["label"])
                return

            if field["type"] in {"number", "slider"}:
                try:
                    float(stored_value)
                except (TypeError, ValueError):
                    invalid_fields.append(field["label"])

        for section in schema.get("sections", []):
            for field in section.get("fields", []):
                _mark_if_required(field)

        if schema.get("advanced"):
            for field in schema["advanced"]:
                _mark_if_required(field)

        if invalid_fields:
            unique_fields = list(dict.fromkeys(invalid_fields))
            return False, "Please complete the required requirements fields before continuing: " + ", ".join(unique_fields)
        return True, ""

    if step_index == 3:
        lifestyle_context = st.session_state.get("concept_lifestyle_context", "")
        if not isinstance(lifestyle_context, str) or not lifestyle_context.strip():
            return False, "Please describe the lifestyle or business context before generating a concept."
        return True, ""

    return True, ""


def concept_layout_generator_page():
    st.markdown("<h1 class='main-header'>🧠 AI Conceptual Layout Generator</h1>", unsafe_allow_html=True)
    if "concept_report" not in st.session_state:
        st.session_state["concept_report"] = None

    steps = [
        ("Project Type", render_project_type_selector),
        ("Plot & Site", render_plot_step),
        ("Requirements", render_requirements_step),
        ("Lifestyle Context", render_context_step),
        ("Concept Output", render_output_step),
        ("Detailed Layout", render_detailed_layout_step),
        ("Export", render_export_step),
    ]

    step_index = st.session_state.get("concept_step", 0)
    current_step = steps[step_index][0]
    _render_secondary_caption(f"Step {step_index + 1} of {len(steps)} • {current_step}", margin_top="0.1rem", margin_bottom="0.75rem")

    steps[step_index][1]()

    if step_index == 3:
        col_back, col_next = st.columns([1, 1])
        with col_back:
            if st.button("← Prev", use_container_width=True):
                st.session_state["concept_step"] = max(0, step_index - 1)
                st.rerun()
        with col_next:
            if st.button("Generate Concept", use_container_width=True):
                is_valid, message = validate_step(step_index)
                if not is_valid:
                    st.session_state["concept_step_warning"] = message
                else:
                    try:
                        status_placeholder = st.empty()

                        def _update_generation_status(message: str):
                            status_placeholder.info(message)

                        _render_generation_status_messages(_update_generation_status)
                        report = run_generation(status_callback=_update_generation_status)
                        st.session_state["concept_report"] = report
                        st.session_state["concept_step"] = 4
                        st.rerun()
                    except Exception as exc:
                        st.error(f"Could not generate the concept: {exc}")
    else:
        col_back, col_next = st.columns([1, 1])
        with col_back:
            if st.button("← Prev", use_container_width=True):
                st.session_state["concept_step"] = max(0, step_index - 1)
                st.rerun()
        with col_next:
            if st.button("Next →", use_container_width=True):
                is_valid, message = validate_step(step_index)
                if not is_valid:
                    st.session_state["concept_step_warning"] = message
                else:
                    st.session_state["concept_step"] = min(len(steps) - 1, step_index + 1)
                    st.rerun()

    warning_message = st.session_state.get("concept_step_warning")
    if warning_message:
        st.warning(warning_message)
        st.session_state.pop("concept_step_warning", None)

    if step_index == 4 and st.button("Regenerate Variant", use_container_width=True):
        st.session_state["concept_report"] = run_generation(single_variant=True)
        st.rerun()


def run_generation(single_variant: bool = False, status_callback=None):
    project_key = st.session_state.get("concept_project_type", "house")
    requirements = {}
    for key, value in st.session_state.items():
        if key.startswith("concept_") and key not in {
            "concept_project_type",
            "concept_lifestyle",
            "concept_lifestyle_context",
            "concept_step",
            "concept_plot_width",
            "concept_plot_length",
            "concept_orientation",
            "concept_site_note",
        }:
            requirements[key.replace("concept_", "")] = value

    stored_plot_width = st.session_state.get("concept_plot_width")
    stored_plot_length = st.session_state.get("concept_plot_length")
    if not isinstance(stored_plot_width, (int, float)) or not isinstance(stored_plot_length, (int, float)):
        raise ValueError(
            "Plot width/length are not set. Please complete Step 2 (Plot & Site) before generating a concept."
        )

    plot_info = {
        "plot_width": stored_plot_width,
        "plot_length": stored_plot_length,
        "orientation": st.session_state.get("concept_orientation") or "Not specified",
        "site_note": st.session_state.get("concept_site_note", ""),
    }
    lifestyle_context = st.session_state.get("concept_lifestyle_context", st.session_state.get("concept_lifestyle", ""))
    client = ConceptGeneratorClient()
    payload = client.generate_concept(
        project_key,
        requirements,
        lifestyle_context,
        plot_info,
        variant_hint="Produce a distinct zoning variant." if single_variant else "",
        status_callback=status_callback,
    )
    return normalize_report(payload)