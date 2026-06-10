#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 22:44:31 2026

@author: dev
"""


import math


def calculate(remaining_principal: float,
              remaining_tenure_months: int,
              annual_roi: float,
              prepayment_amount: float,
              prepayment_fee_percentage: float = 0.0,
              tax_applicable: bool = True):
    """
    Calculates savings from a loan prepayment, evaluating both Tenure and EMI reduction options.
    Factors in prepayment fees and 18% GST (India).

    Returns:
    dict: A comparative analysis of both prepayment strategies.
    """

    fee_decimal = prepayment_fee_percentage / 100
    raw_prepayment_fee = prepayment_amount * fee_decimal
    gst_on_fee = (raw_prepayment_fee * 0.18) if tax_applicable else 0.0
    total_prepayment_charges = raw_prepayment_fee + gst_on_fee
    total_cash_outflow = prepayment_amount + total_prepayment_charges

    monthly_rate = (annual_roi / 12) / 100

    if monthly_rate == 0:
        original_emi = remaining_principal / remaining_tenure_months
        original_total_payable = remaining_principal
    else:
        original_emi = (remaining_principal * monthly_rate * ((1 + monthly_rate) **
                        remaining_tenure_months)) / (((1 + monthly_rate) ** remaining_tenure_months) - 1)
        original_total_payable = original_emi * remaining_tenure_months

    original_total_interest = original_total_payable - remaining_principal

    new_principal = remaining_principal - prepayment_amount
    if new_principal <= 0:
        return {"Status": "Loan fully paid off by prepayment."}

    if monthly_rate == 0:
        new_tenure_months = math.ceil(new_principal / original_emi)
    else:
        log_numerator = original_emi
        log_denominator = original_emi - (new_principal * monthly_rate)

        if log_denominator <= 0:
            new_tenure_months = 1  # Closes immediately next month
        else:
            new_tenure_months = math.ceil(
                math.log(log_numerator / log_denominator) / math.log(1 + monthly_rate))

    strategy_a_total_payable = (
        original_emi * new_tenure_months) + total_cash_outflow
    strategy_a_interest_saved = original_total_payable - strategy_a_total_payable
    tenure_saved_months = remaining_tenure_months - new_tenure_months

    if monthly_rate == 0:
        new_emi = new_principal / remaining_tenure_months
    else:
        new_emi = (new_principal * monthly_rate * ((1 + monthly_rate) **
                   remaining_tenure_months)) / (((1 + monthly_rate) ** remaining_tenure_months) - 1)

    strategy_b_total_payable = (
        new_emi * remaining_tenure_months) + total_cash_outflow
    strategy_b_interest_saved = original_total_payable - strategy_b_total_payable
    emi_reduction = original_emi - new_emi

    return {
        "Prepayment Charges Breakdown": {
            "Prepayment Fee": round(raw_prepayment_fee, 2),
            "GST (18%)": round(gst_on_fee, 2),
            "Total Charges Paid to Bank": round(total_prepayment_charges, 2),
            "Total Outflow from Pocket": round(total_cash_outflow, 2)
        },
        "Baseline (No Prepayment)": {
            "Current EMI": round(original_emi, 2),
            "Total Interest Remaining": round(original_total_interest, 2)
        },
        "Option 1: Reduce Tenure (EMI stays same)": {
            "New Remaining Tenure": f"{new_tenure_months} months",
            "Tenure Saved": f"{tenure_saved_months} months",
            "Net Money Saved": round(strategy_a_interest_saved, 2)
        },
        "Option 2: Reduce EMI (Tenure stays same)": {
            "New Lower EMI": round(new_emi, 2),
            "EMI Reduced By": round(emi_reduction, 2),
            "Net Money Saved": round(strategy_b_interest_saved, 2)
        }
    }


def get_inputs():
    """
    Returns the metadata configuration for the calculate function parameters.
    This metadata defines the type, constraints, step precision, and 
    default values for building dynamic UI forms or validation layers.
    """

    return {
        "remaining_principal": {
            "label": "Outstanding Loan Amount (₹)",
            "widget": "number",
            "type": float,
            "default": 3000000,
            "min": 0,
            "max": float("inf"),
            "show_slider": True,
            "slider_min": 0,
            "slider_max": 10000000,
            "step": 10000,
            "allowed_values": []
        },
        "remaining_tenure_months": {
            "label": "Remaining Tenure (Months)",
            "widget": "number",
            "type": int,
            "default": 180,
            "min": 1,
            "max": 600,
            "show_slider": True,
            "slider_min": 1,
            "slider_max": 360,
            "step": 1,
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
        "prepayment_amount": {
            "label": "Prepayment Amount (₹)",
            "widget": "number",
            "type": float,
            "default": 500000,
            "min": 1,
            "max": float("inf"),
            "show_slider": True,
            "slider_min": 10000,
            "slider_max": 5000000,
            "step": 10000,
            "allowed_values": []
        },
        "prepayment_fee_percentage": {
            "label": "Prepayment Charges (%)",
            "widget": "number",
            "type": float,
            "default": 0,
            "min": 0,
            "max": 100,
            "show_slider": True,
            "slider_min": 0,
            "slider_max": 10,
            "step": 0.1,
            "allowed_values": []
        },
        "tax_applicable": {
            "label": "GST Applicable",
            "widget": "checkbox",
            "default": True,
            "allowed_values": [True, False]
        }
    }
