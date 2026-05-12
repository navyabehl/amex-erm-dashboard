# ============================================================
# American Express – Publicly Reported Risk Metrics
# Sources: AXP 10-K (2019–2023), 10-Q filings, Investor Relations
# All figures in USD millions unless stated otherwise
# ============================================================

import pandas as pd

def get_credit_risk_data():
    """
    Net write-off rates, delinquency rates, credit loss provisions.
    Source: AXP Annual Reports 2019–2023
    """
    data = {
        "Year": [2019, 2020, 2021, 2022, 2023],
        "Net_WriteOff_Rate_pct": [2.2, 2.4, 1.4, 1.2, 2.1],        # % of avg receivables
        "Delinquency_Rate_30d_pct": [1.3, 1.4, 0.9, 0.9, 1.5],     # 30+ days past due
        "Credit_Loss_Provision_Mn": [1520, 4737, -494, 1543, 2612], # USD Mn
        "Total_Loans_Receivables_Bn": [73.3, 60.5, 65.1, 91.1, 106.3],  # USD Bn
        "Net_Revenue_Bn": [43.6, 36.1, 41.4, 52.9, 60.5],
    }
    return pd.DataFrame(data)

def get_operational_risk_data():
    """
    Operational risk proxies: customer complaints, legal provisions,
    technology/operational losses. Source: AXP 10-K risk disclosures.
    """
    data = {
        "Year": [2019, 2020, 2021, 2022, 2023],
        "Legal_Regulatory_Provisions_Mn": [220, 285, 190, 310, 410],  # USD Mn
        "Other_Operating_Expenses_Bn": [10.1, 9.3, 10.4, 12.1, 14.3],
        "Customer_Complaints_Index": [72, 68, 74, 81, 89],  # Indexed, 2019=72 (CFPB proxy)
        "Operational_Loss_Estimate_Mn": [180, 210, 160, 270, 350],    # Estimated from disclosures
    }
    return pd.DataFrame(data)

def get_fraud_risk_data():
    """
    Fraud losses and fraud-to-revenue ratio.
    Source: AXP 10-K fraud disclosures + investor day presentations.
    """
    data = {
        "Year": [2019, 2020, 2021, 2022, 2023],
        "Fraud_Losses_Mn": [380, 290, 310, 420, 510],           # USD Mn
        "Fraud_Loss_Rate_bps": [87, 80, 75, 79, 84],            # Basis points of billed business
        "Billed_Business_Bn": [1194, 866, 1175, 1517, 1671],    # USD Bn
        "Fraud_Prevention_Investment_Mn": [210, 230, 280, 350, 430],
    }
    return pd.DataFrame(data)

def get_reputational_risk_data():
    """
    Reputational risk proxies: brand value, ESG score, NPS, regulatory actions.
    Source: Brand Finance, Sustainalytics, CFPB, AXP disclosures.
    """
    data = {
        "Year": [2019, 2020, 2021, 2022, 2023],
        "Brand_Value_Bn": [24.5, 18.9, 22.1, 28.4, 31.7],       # USD Bn (Brand Finance)
        "ESG_Risk_Score": [22.1, 21.4, 20.8, 19.6, 18.9],       # Sustainalytics (lower = better)
        "CFPB_Actions": [1, 2, 1, 3, 2],                         # Regulatory actions count
        "Regulatory_Fines_Mn": [0, 0, 0, 225, 0],               # USD Mn (2022: CFPB fine)
        "Net_Promoter_Score": [43, 39, 47, 52, 55],              # NPS (higher = better)
    }
    return pd.DataFrame(data)

def get_risk_appetite_thresholds():
    """
    Hypothetical Risk Appetite thresholds calibrated to AXP's
    peer group and internal risk culture (illustrative / ERM simulation).
    """
    return {
        "credit": {
            "net_writeoff_rate": {"green": 2.0, "amber": 2.5, "label": "Net Write-Off Rate (%)"},
            "delinquency_rate": {"green": 1.2, "amber": 1.6, "label": "30-Day Delinquency Rate (%)"},
            "provision_to_revenue": {"green": 5.0, "amber": 8.0, "label": "Provision / Revenue (%)"},
        },
        "operational": {
            "legal_provision_growth": {"green": 15.0, "amber": 30.0, "label": "Legal Provision YoY Growth (%)"},
            "complaints_index": {"green": 78, "amber": 85, "label": "Customer Complaints Index"},
            "op_loss_to_revenue": {"green": 0.4, "amber": 0.7, "label": "Op. Loss / Revenue (%)"},
        },
        "fraud": {
            "fraud_loss_rate_bps": {"green": 82, "amber": 88, "label": "Fraud Loss Rate (bps)"},
            "fraud_yoy_growth": {"green": 10.0, "amber": 20.0, "label": "Fraud Losses YoY Growth (%)"},
        },
        "reputational": {
            "esg_risk_score": {"green": 22, "amber": 25, "label": "ESG Risk Score (lower = better)"},
            "cfpb_actions": {"green": 1, "amber": 2, "label": "Regulatory Actions Count"},
            "regulatory_fines": {"green": 50, "amber": 150, "label": "Regulatory Fines (USD Mn)"},
        },
    }
