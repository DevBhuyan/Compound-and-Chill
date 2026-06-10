#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 22:47:23 2026

@author: dev
"""


def calculate(principal: float,
              annual_roi: float,
              tenure_months: float):
    """
    Generates a month-by-month loan amortization schedule.

    Parameters:
    principal (float): The initial loan amount.
    annual_roi (float): Annual interest rate in percentage (e.g., 8.5 for 8.5%).
    tenure_months (int): Total loan tenure in months.

    Returns:
    list: A list of dictionaries containing the breakdown for each month.
    """
    monthly_rate = (annual_roi / 12) / 100

    if monthly_rate == 0:
        emi = principal / tenure_months
    else:
        emi = (principal * monthly_rate * ((1 + monthly_rate) **
               tenure_months)) / (((1 + monthly_rate) ** tenure_months) - 1)

    schedule = []
    opening_balance = principal

    for month in range(1, tenure_months + 1):
        interest_paid = opening_balance * monthly_rate

        principal_paid = emi - interest_paid

        if opening_balance < principal_paid:
            principal_paid = opening_balance
            emi = principal_paid + interest_paid

        closing_balance = opening_balance - principal_paid

        schedule.append({
            "Month": month,
            "Opening Balance": round(opening_balance, 2),
            "EMI": round(emi, 2),
            "Interest Paid": round(interest_paid, 2),
            "Principal Paid": round(principal_paid, 2),
            "Closing Balance": round(max(0.0, closing_balance), 2)
        })

        opening_balance = closing_balance
        if opening_balance <= 0:
            break

    return schedule


def get_inputs():
    """
    Returns the metadata configuration for the Amortization Schedule calculate function parameters.
    This metadata defines the type, constraints, step precision, and 
    default values for building dynamic UI forms or validation layers.
    """

    return {
        "principal": {
            "label": "Loan Amount (₹)",
            "widget": "number",
            "type": float,
            "default": 5000000,
            "min": 0,
            "max": float("inf"),
            "show_slider": True,
            "slider_min": 0,
            "slider_max": 20000000,
            "step": 10000,
            "allowed_values": []
        },
        "annual_roi": {
            "label": "Interest Rate (%)",
            "widget": "number",
            "type": float,
            "default": 8.5,
            "min": 0,
            "max": 100,
            "show_slider": True,
            "slider_min": 0,
            "slider_max": 25,
            "step": 0.05,
            "allowed_values": []
        },
        "tenure_months": {
            "label": "Tenure (Months)",
            "widget": "number",
            "type": int,
            "default": 240,
            "min": 1,
            "max": 600,
            "show_slider": True,
            "slider_min": 1,
            "slider_max": 360,
            "step": 1,
            "allowed_values": []
        }
    }
