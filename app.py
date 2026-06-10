#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 21:45:26 2026

@author: dev
"""


import streamlit as st
from calculators import CALCULATORS


# ==================================================
# Page Configuration
# ==================================================

st.set_page_config(
    page_title="Compound",
    page_icon="📈",
    layout="wide"
)


# ==================================================
# Sidebar
# ==================================================

st.sidebar.title("📈 Compound")

selected_calculator = st.sidebar.selectbox(
    "Select Calculator",
    list(CALCULATORS.keys())
)

calculator = CALCULATORS[selected_calculator]

st.title(selected_calculator)


# ==================================================
# Input Rendering
# ==================================================

inputs = {}

for input_name, config in calculator["inputs"].items():

    label = config.get(
        "label",
        input_name.replace("_", " ").title()
    )

    widget = config.get("widget", "number")

    default = config.get("default")

    # ----------------------------------------------
    # SELECT BOX
    # ----------------------------------------------

    if widget == "select":

        allowed_values = config.get("allowed_values", [])

        if not allowed_values:
            st.warning(
                f"{input_name} configured as select "
                "but no allowed_values provided."
            )
            continue

        default_index = 0

        if default in allowed_values:
            default_index = allowed_values.index(default)

        inputs[input_name] = st.selectbox(
            label,
            allowed_values,
            index=default_index
        )

    # ----------------------------------------------
    # CHECKBOX
    # ----------------------------------------------

    elif widget == "checkbox":

        inputs[input_name] = st.checkbox(
            label,
            value=bool(default)
        )

    # ----------------------------------------------
    # NUMERIC INPUTS
    # ----------------------------------------------

    else:

        min_value = config.get("min")
        max_value = config.get("max")
        step = config.get("step", 1)

        if default is None:

            if min_value not in [None, float("-inf")]:
                default = min_value
            else:
                default = 0

        show_slider = config.get("show_slider", False)

        # ------------------------------------------
        # Slider Mode
        # ------------------------------------------

        if show_slider:

            slider_min = config.get("slider_min")
            slider_max = config.get("slider_max")

            if slider_min is None or slider_max is None:

                st.warning(
                    f"{input_name} requested slider "
                    "but slider_min/slider_max missing."
                )

                inputs[input_name] = st.number_input(
                    label,
                    value=default,
                    step=step
                )

            else:

                # Ensure all slider arguments share the same type.
                # Streamlit requires min_value, max_value, value, and step to be of matching types.
                # If step is a float, cast the other numeric arguments to float.
                _min_val = slider_min
                _max_val = slider_max
                _default_val = default
                _step_val = step

                if isinstance(_step_val, float):
                    # Convert to float to match step type
                    _min_val = float(_min_val) if _min_val is not None else None
                    _max_val = float(_max_val) if _max_val is not None else None
                    _default_val = float(_default_val) if _default_val is not None else None

                # Render both a slider and a precise number input side‑by‑side.
                # Use Streamlit session_state to keep them in sync so that changing
                # either widget updates the other and the calculation.
                state_key = f"{input_name}_value"
                # Initialise the shared state if not present.
                if state_key not in st.session_state:
                    st.session_state[state_key] = _default_val

                slider_key = f"{input_name}_slider"
                number_key = f"{input_name}_number"

                col_slider, col_number = st.columns(2)

                with col_slider:
                    st.slider(
                        label,
                        min_value=_min_val,
                        max_value=_max_val,
                        value=st.session_state[state_key],
                        step=_step_val,
                        key=slider_key,
                        on_change=lambda sk=slider_key, st_key=state_key: st.session_state.update({st_key: st.session_state[sk]})
                    )

                with col_number:
                    st.number_input(
                        f"{label} (precise)",
                        min_value=_min_val,
                        max_value=_max_val,
                        value=st.session_state[state_key],
                        step=_step_val,
                        key=number_key,
                        on_change=lambda nk=number_key, st_key=state_key: st.session_state.update({st_key: st.session_state[nk]})
                    )

                # Use the synchronized value for calculations.
                inputs[input_name] = st.session_state[state_key]

        # ------------------------------------------
        # Number Input Mode
        # ------------------------------------------

        else:

            kwargs = {
                "label": label,
                "value": default,
                "step": step
            }

            if min_value not in [None, float("-inf")]:
                kwargs["min_value"] = min_value

            if max_value not in [None, float("inf")]:
                kwargs["max_value"] = max_value

            inputs[input_name] = st.number_input(**kwargs)


# ==================================================
# Calculation
# ==================================================

try:

    result = calculator["calculate"](**inputs)

    st.divider()
    st.subheader("Results")

    # ----------------------------------------------
    # Dictionary Output
    # ----------------------------------------------

    if isinstance(result, dict):

        for key, value in result.items():

            if isinstance(value, dict):

                st.markdown(f"### {key}")

                for subkey, subvalue in value.items():
                    st.write(f"**{subkey}:** {subvalue}")

            else:

                st.write(f"**{key}:** {value}")

    # ----------------------------------------------
    # List Output
    # ----------------------------------------------

    elif isinstance(result, list):

        st.dataframe(
            result,
            use_container_width=True
        )

    # ----------------------------------------------
    # Scalar Output
    # ----------------------------------------------

    else:

        st.metric(
            label="Result",
            value=result
        )

except Exception as e:

    st.error(
        f"Calculation failed:\n\n{type(e).__name__}: {e}"
    )
