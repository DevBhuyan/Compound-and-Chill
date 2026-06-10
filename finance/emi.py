#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 22:35:24 2026

@author: dev
"""


def calculate(principal: float,
              annual_interest_rate: float,
              tenure_years: float):
    """
    Calculates the Equated Monthly Installment (EMI) for a loan.

    Parameters:
    principal (float): The total loan amount borrowed.
    annual_interest_rate (float): The annual interest rate in percentage (e.g., 7.2 for 7.2%).
    tenure_years (int/float): The loan repayment period in years.

    Returns:
    float: The monthly EMI amount rounded to two decimal places.
    """
    monthly_rate = (annual_interest_rate / 12) / 100

    total_months = tenure_years * 12

    if monthly_rate == 0:
        return round(principal / total_months, 2)

    numerator = principal * monthly_rate * (
        (1 + monthly_rate) ** total_months
    )
    denominator = ((1 + monthly_rate) ** total_months) - 1
    emi = numerator / denominator

    return {
        "EMI": round(emi, 2)
    }


def get_inputs():
    """
    Returns the metadata configuration for the EMI calculate function parameters.
    This metadata defines the type, constraints, step precision, and 
    default values for building dynamic UI forms or validation layers.
    """

    return {
        "principal": {
            "label": "Loan Amount (₹)",
            "widget": "number",
            "type": float,
            "default": 5000000,
            "min": 0.0,
            "max": float("inf"),
            "show_slider": True,
            "slider_min": 0,
            "slider_max": 20000000,
            "step": 10000,
            "allowed_values": []
        },
        "annual_interest_rate": {
            "label": "Annual Interest Rate (%)",
            "widget": "number",
            "type": float,
            "default": 8.5,
            "min": 0.0,
            "max": 100.0,
            "show_slider": True,
            "slider_min": 0.0,
            "slider_max": 25.0,
            "step": 0.05,
            "allowed_values": []
        },
        "tenure_years": {
            "label": "Loan Tenure (Years)",
            "widget": "number",
            "type": float,
            "default": 20.0,
            "min": 0.083,
            "max": 50.0,
            "show_slider": True,
            "slider_min": 1,
            "slider_max": 40,
            "step": 0.25,
            "allowed_values": []
        }
    }
