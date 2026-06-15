#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 22:38:21 2026

@author: dev
"""


def calculate(principal: float,
              annual_return_rate: float,
              tenure_years: float,
              compounding_frequency: int = 1):
    """
    Calculates the future value of a lumpsum investment using compound interest.

    Parameters:
    principal (float): The initial one-time investment amount.
    annual_return_rate (float): Expected annual return rate in percentage (e.g., 12 for 12%).
    tenure_years (int/float): The total investment period in years.
    compounding_frequency (int): Times interest compounds per year. Default is 1 (Annual).
                                 Use 4 for Quarterly, 12 for Monthly.

    Returns:
    dict: A breakdown containing Total Invested, Future Value, and Estimated Returns.
    """
    rate_per_period = (annual_return_rate / compounding_frequency) / 100

    total_periods = tenure_years * compounding_frequency

    future_value = principal * ((1 + rate_per_period) ** total_periods)

    estimated_returns = future_value - principal

    return {
        "Total Invested": round(principal, 2),
        "Estimated Returns": round(estimated_returns, 2),
        "Future Value": round(future_value, 2)
    }


def get_inputs():
    """
    Returns the metadata configuration for the Lumpsum calculate function parameters.
    This metadata defines the type, constraints, step precision, and 
    default values for building dynamic UI forms or validation layers.
    """

    return {
        "principal": {
            "label": "Investment Amount (₹)",
            "widget": "number",
            "type": float,
            "default": 100000,
            "min": 0,
            "max": float("inf"),
            "show_slider": True,
            "slider_min": 0,
            "slider_max": 10000000,
            "step": 10000,
            "allowed_values": []
        },
        "annual_return_rate": {
            "label": "Expected Return (%)",
            "widget": "number",
            "type": float,
            "default": 12,
            "min": 0,
            "max": 100,
            "show_slider": True,
            "slider_min": 0,
            "slider_max": 30,
            "step": 0.1,
            "allowed_values": []
        },
        "tenure_years": {
            "label": "Duration (Years)",
            "widget": "number",
            "type": float,
            "default": 10,
            "min": 0.001,
            "max": 100,
            "show_slider": True,
            "slider_min": 1,
            "slider_max": 50,
            "step": 1,
            "allowed_values": []
        },
        "compounding_frequency": {
            "label": "Compounding Frequency",
            "widget": "select",
            "default": 1,
            "allowed_values": [
                1,
                2,
                4,
                12,
                365
            ]
        }
    }
