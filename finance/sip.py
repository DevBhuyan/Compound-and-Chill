#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 22:34:19 2026

@author: dev
"""


def calculate(initial_monthly_investment: float,
              annual_return_rate: float,
              tenure_years: float,
              step_up_percentage: float = 0.0):
    """
    Calculates the future value of a Step-Up SIP.

    Parameters:
    initial_monthly_investment (float): The starting investment amount for the first year.
    annual_return_rate (float): Expected annual return rate in percentage (e.g., 12 for 12%).
    tenure_years (int/float): The total investment period in years.
    step_up_percentage (float): The yearly increase in investment percentage (e.g., 10 for 10%).

    Returns:
    dict: A breakdown containing Total Invested, Future Value, and Estimated Returns.
    """
    monthly_rate = (annual_return_rate / 12) / 100
    total_months = int(tenure_years * 12)

    total_invested = 0
    future_value = 0
    current_monthly_investment = initial_monthly_investment

    for month in range(1, total_months + 1):
        if month > 1 and (month - 1) % 12 == 0:
            current_monthly_investment *= (1 + (step_up_percentage / 100))

        total_invested += current_monthly_investment

        # Put the money in and grow it by 1 month of interest
        future_value += current_monthly_investment
        future_value *= (1 + monthly_rate)

    estimated_returns = future_value - total_invested


    return {
        "Total Invested (₹)": round(total_invested, 2),
        "Estimated Returns (₹)": round(estimated_returns, 2),
        "Future Value (₹)": round(future_value, 2)
    }


def get_inputs():
    """
    Returns the metadata configuration for the Step-Up SIP calculate function parameters.
    This metadata defines the type, constraints, step precision, and 
    default values for building dynamic UI forms or validation layers.
    """

    return {
        "initial_monthly_investment": {
            "label": "Monthly SIP (₹)",
            "widget": "number",
            "type": float,
            "default": 10000,
            "min": 100,
            "max": float("inf"),
            "show_slider": True,
            "slider_min": 100,
            "slider_max": 100000,
            "step": 500,
            "allowed_values": []
        },
        "annual_return_rate": {
            "label": "Expected Annual Return (%)",
            "widget": "number",
            "type": float,
            "default": 12.0,
            "min": 0,
            "max": 100,
            "show_slider": True,
            "slider_min": 0,
            "slider_max": 30,
            "step": 0.1,
            "allowed_values": []
        },
        "tenure_years": {
            "label": "Investment Duration (Years)",
            "widget": "number",
            "type": float,
            "default": 20,
            "min": 0.08,
            "max": 100,
            "show_slider": True,
            "slider_min": 1,
            "slider_max": 50,
            "step": 1,
            "allowed_values": []
        },
        "step_up_percentage": {
            "label": "Annual Step-Up (%)",
            "widget": "number",
            "type": float,
            "default": 10,
            "min": 0,
            "max": 500,
            "show_slider": True,
            "slider_min": 0,
            "slider_max": 50,
            "step": 1,
            "allowed_values": []
        }
    }
