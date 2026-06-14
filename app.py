#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 21:45:26 2026

@author: dev
"""


import streamlit as st
from streamlit import session_state as ss
from calculators import CALCULATORS
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt


if "current_cs" not in ss:
    ss.current_cs = "$"




# ---------------------------------------------------------------------
# Helper functions for dynamic result visualisation
# ---------------------------------------------------------------------


def _format_numeric_display(value, config):
    if isinstance(value, (int, float)):
        label = config.get("label", "")

        if "₹" in label or "amount" in label.lower():
            if isinstance(value, int):
                return f"{ss.current_cs}{value:,}"
            return f"{ss.current_cs}{value:,.2f}"

        if "%" in label or "rate" in label.lower() or "interest" in label.lower():
            return f"{value:.2f}%"

        if isinstance(value, int):
            return f"{value:,}"

        return f"{value:,.2f}"

    return str(value)


def _render_pie_chart(numeric_items):
    df = pd.DataFrame({
        "label": list(numeric_items.keys()),
        "value": list(numeric_items.values())
    })

    chart = alt.Chart(df).mark_arc(innerRadius=70, stroke="#f8fafc", strokeWidth=2).encode(
        theta=alt.Theta(field="value", type="quantitative"),
        color=alt.Color(
            "label:N",
            scale=alt.Scale(range=["#1d4ed8", "#059669", "#f59e0b", "#ef4444", "#7c3aed", "#0ea5e9"]),
            legend=alt.Legend(title=None, orient="right", labelFontSize=12)
        ),
        tooltip=[
            alt.Tooltip("label:N", title="Category"),
            alt.Tooltip("value:Q", title="Amount", format=",.2f")
        ]
    ).properties(width=360, height=360)

    return chart.configure_view(strokeOpacity=0).configure_title(
        fontSize=16,
        anchor="start",
        color="#0f172a"
    ).configure_legend(
        labelFontSize=12,
        titleFontSize=0
    )


def _render_plain(result):
    """Fallback plain‑text rendering (unchanged from original logic)."""
    if isinstance(result, dict):
        for key, value in result.items():
            if isinstance(value, dict):
                st.markdown(f"### {key}")
                for subkey, subvalue in value.items():
                    st.write(f"**{subkey}:** {subvalue}")
            else:
                st.write(f"**{key}:** {value}")
    elif isinstance(result, list):
        st.dataframe(result, use_container_width=True)
    else:
        st.metric(label="Result", value=result)


def render_result(result, viz_cfg=None):
    """Render ``result`` according to an optional visualisation config.

    The ``viz_cfg`` dictionary is expected to be supplied by the calculator
    definition (see the documentation in the assistant's previous message).
    If the config is missing or the data shape does not match the requested
    visualisation, the function gracefully falls back to the plain‑text
    representation.
    """
    if not viz_cfg:
        if isinstance(result, dict):
            numeric_items = {
                key: value
                for key, value in result.items()
                if isinstance(value, (int, float))
            }

            if numeric_items and len(numeric_items) > 1:
                # Try to create a meaningful pie chart: prefer Principal vs Interest (absolute amounts).
                principal_key = next((k for k in result.keys() if "principal" in k.lower()), None)
                total_payment_key = next((k for k in result.keys() if "total payment" in k.lower()), None)

                pie_items = None

                if principal_key and total_payment_key:
                    try:
                        principal_val = float(result[principal_key])
                        total_payment_val = float(result[total_payment_key])
                        interest_amount = max(0.0, total_payment_val - principal_val)
                        pie_items = {"Principal": principal_val, "Interest": interest_amount}
                    except Exception:
                        pie_items = None

                # Fallback: remove percentage and tiny/duplicated fields (like monthly EMI) from pie
                if pie_items is None:
                    pie_items = {
                        k: v for k, v in numeric_items.items()
                        if isinstance(v, (int, float)) and v > 0 and ("%" not in k) and ("emi" not in k.lower() and "monthly" not in k.lower())
                    }

                # If still empty, fall back to original numeric items
                if not pie_items:
                    pie_items = numeric_items

                left, right = st.columns([2, 1])

                with left:
                    st.markdown("### Summary")
                    for key, value in result.items():
                        if isinstance(value, (int, float)):
                            st.metric(label=key.replace('₹', ss.current_cs), value=_format_numeric_display(value, {"label": key}))
                        else:
                            st.write(f"**{key}:** {value}")

                with right:
                    if all(isinstance(v, (int, float)) and v >= 0 for v in pie_items.values()):
                        st.altair_chart(_render_pie_chart(pie_items), use_container_width=True)
                return

        _render_plain(result)
        return

    vtype = viz_cfg.get("type")

    try:
        if vtype == "metric":
            label = viz_cfg.get("label", "Result")
            st.metric(label=label, value=result)

        elif vtype == "pie" and isinstance(result, dict):
            label_key = viz_cfg.get("label_key")
            value_key = viz_cfg.get("value_key")
            if label_key and value_key:
                labels = [v.get(label_key) for v in result.values()]
                values = [v.get(value_key) for v in result.values()]
                fig, ax = plt.subplots()
                ax.pie(values, labels=labels, autopct="%1.1f%%")
                st.pyplot(fig)
            else:
                _render_plain(result)

        elif vtype in {"bar", "line"} and isinstance(result, list):
            df = pd.DataFrame(result)
            x_col = viz_cfg.get("x") or (
                df.columns[0] if not df.empty else None)
            if x_col and x_col in df.columns:
                df = df.set_index(x_col)
            if vtype == "bar":
                st.bar_chart(df)
            else:
                st.line_chart(df)

        elif vtype == "dataframe":
            if isinstance(result, (list, dict)):
                df = pd.DataFrame(result)
                st.dataframe(df, use_container_width=True)
            else:
                _render_plain(result)

        else:
            _render_plain(result)
    except Exception:
        _render_plain(result)


def _sync_slider_to_number(state_key):
    st.session_state[f"{state_key}_number"] = st.session_state[f"{state_key}_slider"]
    st.session_state[f"{state_key}_last_changed"] = "slider"


def _sync_number_to_slider(state_key):
    st.session_state[f"{state_key}_slider"] = st.session_state[f"{state_key}_number"]
    st.session_state[f"{state_key}_last_changed"] = "number"


def render_numeric_input(
    label,
    config,
    state_key
):
    expected_type = config.get("type", float)

    caster = float if expected_type is float else int

    default_value = caster(config["default"])

    slider_key = f"{state_key}_slider"
    number_key = f"{state_key}_number"
    last_key = f"{state_key}_last_changed"

    if slider_key not in st.session_state:
        st.session_state[slider_key] = default_value

    if number_key not in st.session_state:
        st.session_state[number_key] = default_value

    if last_key not in st.session_state:
        st.session_state[last_key] = "slider"

    slider_min = caster(config["slider_min"])
    slider_max = caster(config["slider_max"])
    step = caster(config["step"])

    col1, col2 = st.columns([4, 1])

    with col1:
        st.slider(
            label, 
            min_value=slider_min,
            max_value=slider_max,
            step=step,
            key=slider_key,
            on_change=_sync_slider_to_number,
            args=(state_key,)
        )

    with col2:
        st.markdown(
            f"<div style='font-size:1.1rem; font-weight:600;'>"
            f"{_format_numeric_display(st.session_state[slider_key], config)}"
            f"</div>",
            unsafe_allow_html=True
        )
        st.caption("Current")

    st.number_input(
        "Exact",
        min_value=slider_min,
        max_value=slider_max,
        step=step,
        key=number_key,
        label_visibility="collapsed",
        on_change=_sync_number_to_slider,
        args=(state_key,)
    )

    if st.session_state[last_key] == "number":
        current_value = st.session_state[number_key]
    else:
        current_value = st.session_state[slider_key]

    return caster(current_value)

# ==================================================
# Page Configuration
# ==================================================


st.set_page_config(
    page_title="Compound",
    page_icon="📈",
    layout="wide"
)

st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {display: none !important;}
    .css-1d391kg {padding-top: 0rem !important;}
    .stApp {background: #eef2ff !important;}
    .block-container {padding: 1.2rem 2rem !important; background: #eef2ff !important;}
    .block-container h1,
    .block-container h2,
    .block-container h3,
    .block-container h4,
    .block-container h5,
    .block-container h6,
    .block-container p,
    .block-container label,
    .block-container {
        color: #000000 !important;
    }
    .stMetric > div {
        border-radius: 1rem !important;
        padding: 1rem !important;
        background: #ffffff !important;
        color: #000000 !important;
        box-shadow: 0 16px 32px rgba(15, 23, 42, 0.08) !important;
    }
    .stSlider > div {
        background: #ffffff !important;
        border-radius: 1rem !important;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06) !important;
        padding: 1rem !important;
    }
    .streamlit-expanderHeader {
        background: #ffffff !important;
        border-radius: 1rem !important;
        color: #000000 !important;
    }
    .css-1o9w0hw {background: #eff6ff !important;}
    .css-1330x6k {color: #000000 !important;}
    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# Sidebar
# ==================================================

st.sidebar.title("📈 Compound")

selected_calculator = st.sidebar.selectbox(
    "Select Calculator",
    list(CALCULATORS.keys())
)

tier = CALCULATORS[selected_calculator]

st.title(selected_calculator)

# Dictionary of major world currencies formatted as "Code (Name)":"Symbol"
world_currencies = {
    "USD (US Dollar)": "$", "EUR (Euro)": "€", "GBP (British Pound)": "£",
    "JPY (Japanese Yen)": "¥", "INR (Indian Rupee)": "₹", "CNY (Chinese Yuan)": "¥",
    "CAD (Canadian Dollar)": "$", "AUD (Australian Dollar)": "$", "CHF (Swiss Franc)": "CHF",
    "BRL (Brazilian Real)": "R$", "RUB (Russian Ruble)": "₽", "MXN (Mexican Peso)": "$"
}


currency_symbol = world_currencies[st.sidebar.selectbox(
    "Select Curency",
    list(world_currencies.keys())
)]
ss.current_cs = currency_symbol


# ==================================================
# Input Rendering
# ==================================================

tabs = st.tabs(list(tier.keys()))

for idx, calculator in enumerate(tier.values()):

    with tabs[idx]:

        inputs = {}

        for input_name, config in calculator["inputs"].items():

            label = config.get(
                "label",
                input_name.replace("_", " ").title()
            )
            label = label.replace("₹", ss.current_cs)

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

                    inputs[input_name] = render_numeric_input(
                        label,
                        config,
                        f"{selected_calculator}_{idx}_{input_name}"
                    )

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

            # Use the visualisation configuration supplied by the calculator (if any).
            viz_cfg = calculator.get("visualisation")
            render_result(result, viz_cfg)

        except Exception as e:

            st.error(
                f"Calculation failed:\n\n{type(e).__name__}: {e}"
            )
