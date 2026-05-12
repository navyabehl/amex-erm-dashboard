# ============================================================
# utils/rag_engine.py
# RAG (Red / Amber / Green) Status Engine
# Escalation Report Generator
# ============================================================

import pandas as pd
from datetime import datetime


def get_rag_status(value, green_threshold, amber_threshold, higher_is_worse=True):
    """
    Returns RAG status, emoji, and colour hex for a given metric.
    higher_is_worse=True  → higher value = more risk (most metrics)
    higher_is_worse=False → lower value = more risk (e.g. NPS, brand value)
    """
    if higher_is_worse:
        if value <= green_threshold:
            return "GREEN", "🟢", "#2ecc71"
        elif value <= amber_threshold:
            return "AMBER", "🟡", "#f39c12"
        else:
            return "RED", "🔴", "#e74c3c"
    else:
        if value >= green_threshold:
            return "GREEN", "🟢", "#2ecc71"
        elif value >= amber_threshold:
            return "AMBER", "🟡", "#f39c12"
        else:
            return "RED", "🔴", "#e74c3c"


def evaluate_credit_risk(df, thresholds):
    results = []
    latest = df.iloc[-1]
    prev = df.iloc[-2]

    # Net write-off rate
    val = latest["Net_WriteOff_Rate_pct"]
    t = thresholds["net_writeoff_rate"]
    status, emoji, color = get_rag_status(val, t["green"], t["amber"])
    results.append({
        "Metric": t["label"], "Value": f"{val:.2f}%",
        "Status": status, "Emoji": emoji, "Color": color,
        "YoY Change": f"{val - prev['Net_WriteOff_Rate_pct']:+.2f}%"
    })

    # Delinquency rate
    val = latest["Delinquency_Rate_30d_pct"]
    t = thresholds["delinquency_rate"]
    status, emoji, color = get_rag_status(val, t["green"], t["amber"])
    results.append({
        "Metric": t["label"], "Value": f"{val:.2f}%",
        "Status": status, "Emoji": emoji, "Color": color,
        "YoY Change": f"{val - prev['Delinquency_Rate_30d_pct']:+.2f}%"
    })

    # Provision to revenue
    prov = latest["Credit_Loss_Provision_Mn"]
    rev = latest["Net_Revenue_Bn"] * 1000
    val = round((prov / rev) * 100, 2)
    prev_prov = prev["Credit_Loss_Provision_Mn"]
    prev_rev = prev["Net_Revenue_Bn"] * 1000
    prev_val = round((prev_prov / prev_rev) * 100, 2)
    t = thresholds["provision_to_revenue"]
    status, emoji, color = get_rag_status(val, t["green"], t["amber"])
    results.append({
        "Metric": t["label"], "Value": f"{val:.2f}%",
        "Status": status, "Emoji": emoji, "Color": color,
        "YoY Change": f"{val - prev_val:+.2f}%"
    })

    return results


def evaluate_operational_risk(df, thresholds):
    results = []
    latest = df.iloc[-1]
    prev = df.iloc[-2]

    # Legal provision YoY growth
    yoy = ((latest["Legal_Regulatory_Provisions_Mn"] - prev["Legal_Regulatory_Provisions_Mn"])
           / prev["Legal_Regulatory_Provisions_Mn"]) * 100
    t = thresholds["legal_provision_growth"]
    status, emoji, color = get_rag_status(yoy, t["green"], t["amber"])
    results.append({
        "Metric": t["label"], "Value": f"{yoy:.1f}%",
        "Status": status, "Emoji": emoji, "Color": color,
        "YoY Change": f"{yoy:+.1f}%"
    })

    # Complaints index
    val = latest["Customer_Complaints_Index"]
    t = thresholds["complaints_index"]
    status, emoji, color = get_rag_status(val, t["green"], t["amber"])
    results.append({
        "Metric": t["label"], "Value": str(int(val)),
        "Status": status, "Emoji": emoji, "Color": color,
        "YoY Change": f"{val - prev['Customer_Complaints_Index']:+.0f}"
    })

    # Op loss to revenue
    val = round((latest["Operational_Loss_Estimate_Mn"] / (latest["Other_Operating_Expenses_Bn"] * 1000)) * 100, 2)
    prev_val = round((prev["Operational_Loss_Estimate_Mn"] / (prev["Other_Operating_Expenses_Bn"] * 1000)) * 100, 2)
    t = thresholds["op_loss_to_revenue"]
    status, emoji, color = get_rag_status(val, t["green"], t["amber"])
    results.append({
        "Metric": t["label"], "Value": f"{val:.2f}%",
        "Status": status, "Emoji": emoji, "Color": color,
        "YoY Change": f"{val - prev_val:+.2f}%"
    })

    return results


def evaluate_fraud_risk(df, thresholds):
    results = []
    latest = df.iloc[-1]
    prev = df.iloc[-2]

    # Fraud loss rate
    val = latest["Fraud_Loss_Rate_bps"]
    t = thresholds["fraud_loss_rate_bps"]
    status, emoji, color = get_rag_status(val, t["green"], t["amber"])
    results.append({
        "Metric": t["label"], "Value": f"{val} bps",
        "Status": status, "Emoji": emoji, "Color": color,
        "YoY Change": f"{val - prev['Fraud_Loss_Rate_bps']:+.0f} bps"
    })

    # Fraud YoY growth
    yoy = ((latest["Fraud_Losses_Mn"] - prev["Fraud_Losses_Mn"]) / prev["Fraud_Losses_Mn"]) * 100
    t = thresholds["fraud_yoy_growth"]
    status, emoji, color = get_rag_status(yoy, t["green"], t["amber"])
    results.append({
        "Metric": t["label"], "Value": f"{yoy:.1f}%",
        "Status": status, "Emoji": emoji, "Color": color,
        "YoY Change": f"{yoy:+.1f}%"
    })

    return results


def evaluate_reputational_risk(df, thresholds):
    results = []
    latest = df.iloc[-1]
    prev = df.iloc[-2]

    # ESG risk score (lower = better, so higher_is_worse=True)
    val = latest["ESG_Risk_Score"]
    t = thresholds["esg_risk_score"]
    status, emoji, color = get_rag_status(val, t["green"], t["amber"])
    results.append({
        "Metric": t["label"], "Value": f"{val:.1f}",
        "Status": status, "Emoji": emoji, "Color": color,
        "YoY Change": f"{val - prev['ESG_Risk_Score']:+.1f}"
    })

    # CFPB actions
    val = latest["CFPB_Actions"]
    t = thresholds["cfpb_actions"]
    status, emoji, color = get_rag_status(val, t["green"], t["amber"])
    results.append({
        "Metric": t["label"], "Value": str(int(val)),
        "Status": status, "Emoji": emoji, "Color": color,
        "YoY Change": f"{val - prev['CFPB_Actions']:+.0f}"
    })

    # Regulatory fines
    val = latest["Regulatory_Fines_Mn"]
    t = thresholds["regulatory_fines"]
    status, emoji, color = get_rag_status(val, t["green"], t["amber"])
    results.append({
        "Metric": t["label"], "Value": f"${val:.0f}M",
        "Status": status, "Emoji": emoji, "Color": color,
        "YoY Change": f"${val - prev['Regulatory_Fines_Mn']:+.0f}M"
    })

    return results


def get_overall_rag(all_results):
    """Aggregate RAG: worst status across all metrics."""
    statuses = [r["Status"] for r in all_results]
    if "RED" in statuses:
        return "RED", "🔴", "#e74c3c"
    elif "AMBER" in statuses:
        return "AMBER", "🟡", "#f39c12"
    return "GREEN", "🟢", "#2ecc71"


def generate_escalation_report(year, credit, operational, fraud, reputational):
    """Generate a plain-text governance escalation report."""
    all_results = credit + operational + fraud + reputational
    overall_status, overall_emoji, _ = get_overall_rag(all_results)

    red_items = [r for r in all_results if r["Status"] == "RED"]
    amber_items = [r for r in all_results if r["Status"] == "AMBER"]

    report = f"""
================================================================================
    ENTERPRISE RISK MANAGEMENT — GOVERNANCE ESCALATION REPORT
    American Express (AXP) | Risk Reporting Period: FY {year}
    Generated: {datetime.now().strftime("%d %B %Y, %H:%M")}
    Prepared for: Chief Risk Officer (CRO) | AEBC Risk Oversight Committee
================================================================================

OVERALL RISK STATUS: {overall_emoji} {overall_status}

--------------------------------------------------------------------------------
EXECUTIVE SUMMARY
--------------------------------------------------------------------------------
This report provides an independent risk oversight summary across Credit Risk,
Operational Risk, Fraud Risk, and Reputational Risk, assessed against the
enterprise risk appetite framework. Metrics are derived from AXP's publicly
reported financial disclosures (10-K/10-Q filings).

Total Metrics Monitored : {len(all_results)}
GREEN (Within Appetite) : {sum(1 for r in all_results if r['Status'] == 'GREEN')}
AMBER (Approaching Limit): {sum(1 for r in all_results if r['Status'] == 'AMBER')}
RED   (Appetite Breached): {sum(1 for r in all_results if r['Status'] == 'RED')}

--------------------------------------------------------------------------------
ESCALATION ITEMS — IMMEDIATE ATTENTION REQUIRED
--------------------------------------------------------------------------------
"""
    if red_items:
        for item in red_items:
            report += f"  🔴 [{item['Metric']}] Current: {item['Value']} | YoY: {item['YoY Change']}\n"
            report += f"     → Risk appetite threshold breached. Recommend immediate review.\n\n"
    else:
        report += "  No RED items identified in this reporting period.\n\n"

    report += """--------------------------------------------------------------------------------
WATCH LIST — AMBER METRICS APPROACHING APPETITE LIMITS
--------------------------------------------------------------------------------
"""
    if amber_items:
        for item in amber_items:
            report += f"  🟡 [{item['Metric']}] Current: {item['Value']} | YoY: {item['YoY Change']}\n"
            report += f"     → Monitor closely. Escalate if trend continues next quarter.\n\n"
    else:
        report += "  No AMBER items identified in this reporting period.\n\n"

    report += f"""--------------------------------------------------------------------------------
RISK DOMAIN SUMMARY
--------------------------------------------------------------------------------

  CREDIT RISK
"""
    for r in credit:
        report += f"    {r['Emoji']} {r['Metric']}: {r['Value']} (YoY: {r['YoY Change']})\n"

    report += "\n  OPERATIONAL RISK\n"
    for r in operational:
        report += f"    {r['Emoji']} {r['Metric']}: {r['Value']} (YoY: {r['YoY Change']})\n"

    report += "\n  FRAUD RISK\n"
    for r in fraud:
        report += f"    {r['Emoji']} {r['Metric']}: {r['Value']} (YoY: {r['YoY Change']})\n"

    report += "\n  REPUTATIONAL RISK\n"
    for r in reputational:
        report += f"    {r['Emoji']} {r['Metric']}: {r['Value']} (YoY: {r['YoY Change']})\n"

    report += """
--------------------------------------------------------------------------------
DISCLAIMER
--------------------------------------------------------------------------------
This dashboard is an independent academic simulation built using publicly
available AXP financial disclosures. Risk appetite thresholds are illustrative
and do not represent American Express internal risk frameworks.
Data sources: AXP 10-K (2019–2023), Brand Finance, Sustainalytics, CFPB.
================================================================================
"""
    return report
