from unittest.mock import patch

import concept_generator.ui_flow as ui_flow


class DummyContainer:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class DummyStreamlit:
    def __init__(self):
        self.session_state = {}
        self.markdown_calls = []
        self.number_input_values = []
        self.number_input_index = 0

    def markdown(self, *args, **kwargs):
        self.markdown_calls.append(args[0])

    def info(self, *args, **kwargs):
        return None

    def warning(self, *args, **kwargs):
        return None

    def error(self, *args, **kwargs):
        return None

    def success(self, *args, **kwargs):
        return None

    def columns(self, *args, **kwargs):
        return [DummyContainer(), DummyContainer()]

    def number_input(self, label, **kwargs):
        if self.number_input_index < len(self.number_input_values):
            value = self.number_input_values[self.number_input_index]
            self.number_input_index += 1
        else:
            value = kwargs.get("default", kwargs.get("min_value", 0))
        self.session_state[kwargs["key"]] = value
        return value

    def selectbox(self, label, options, **kwargs):
        value = self.session_state.get(kwargs["key"], options[0])
        self.session_state[kwargs["key"]] = value
        return value

    def text_input(self, label, **kwargs):
        value = self.session_state.get(kwargs["key"], kwargs.get("value", ""))
        self.session_state[kwargs["key"]] = value
        return value

    def button(self, label, **kwargs):
        return False


def test_plot_step_persists_dimensions_into_session_state():
    fake_st = DummyStreamlit()
    fake_st.session_state["concept_project_type"] = "house"
    fake_st.number_input_values = [1000, 2000]

    with patch.object(ui_flow, "st", fake_st):
        ui_flow.render_plot_step()

    assert fake_st.session_state["concept_plot_width"] == 1000
    assert fake_st.session_state["concept_plot_length"] == 2000


def test_detailed_layout_step_uses_saved_plot_dimensions():
    fake_st = DummyStreamlit()
    fake_st.session_state["concept_project_type"] = "villa"
    fake_st.session_state["concept_plot_width"] = 1000
    fake_st.session_state["concept_plot_length"] = 2000
    fake_st.session_state["concept_bedrooms"] = 4
    fake_st.session_state["concept_bathrooms"] = 4

    with patch.object(ui_flow, "st", fake_st):
        ui_flow.render_detailed_layout_step()

    rendered = "\n".join(fake_st.markdown_calls)
    assert "Plot: 1000 x 2000 ft" in rendered
