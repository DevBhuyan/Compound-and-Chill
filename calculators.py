#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 23:04:34 2026

@author: dev
"""

from finance import (
    emi,
    sip,
    loan_prepayment,
    lumpsum,
    repayment_schedule
)


CALCULATORS = {
    "EMI Calculator": {
        "inputs": emi.get_inputs(),
        "calculate": emi.calculate
    },
    "SIP Calculator": {
        "inputs": sip.get_inputs(),
        "calculate": sip.calculate
    },
    "Loan Prepayment Calculator": {
        "inputs": loan_prepayment.get_inputs(),
        "calculate": loan_prepayment.calculate
    },
    "Lumpsum Investment Calculator": {
        "inputs": lumpsum.get_inputs(),
        "calculate": lumpsum.calculate
    },
    "Loan Repayment Schedule": {
        "inputs": repayment_schedule.get_inputs(),
        "calculate": repayment_schedule.calculate
    }
}
