#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 22:35:24 2026

@author: dev
"""


def calculate(principal: float,
              annual_interest_rate: float,
              tenure_months: float):
    """
    Calculates the Equated Monthly Installment (EMI) for a loan.

    Parameters:
    principal (float): The total loan amount borrowed.
    annual_interest_rate (float): The annual interest rate in percentage (e.g., 7.2 for 7.2%).
    tenure_months (int/float): The loan repayment period in months.

    Returns:
    float: The monthly EMI amount rounded to two decimal places.
    """
    monthly_rate = (annual_interest_rate / 12) / 100

    

    if monthly_rate == 0:
        emi = principal / tenure_months
    else:
        numerator = principal * monthly_rate * (
            (1 + monthly_rate) ** tenure_months
        )
        denominator = ((1 + monthly_rate) ** tenure_months) - 1
        emi = numerator / denominator

    total_payment = emi * tenure_months
    total_interest = (total_payment - principal)

    return {
        "Monthly EMI (₹)": round(emi, 2),
        "Principal Amount": round(principal, 2),
        "Total Interest Paid (₹)": round(total_interest, 2),
        "Total Payment (₹)": round(total_payment, 2)
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
            "slider_max": 1000000000,
            "step": 0.01,
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
            "slider_max": 100.0,
            "step": 0.01,
            "allowed_values": []
        },
        "tenure_months": {
            "label": "Loan Tenure (Months)",
            "widget": "number",
            "type": float,
            "default": 12.0,
            "min": 1.0,
            "max": 480.0,
            "show_slider": True,
            "slider_min": 1,
            "slider_max": 480,
            "step": 0.01,
            "allowed_values": []
        }
    }
