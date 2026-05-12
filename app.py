# ============================================================
# app.py — AmEx ERM Risk Appetite Dashboard
# Streamlit Application
# ============================================================


import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from amex_data import (
    get_credit_risk_data, get_operational_risk_data,
    get_fraud_risk_data, get_reputational_risk_data,
    get_risk_appetite_thresholds
)
from rag_engine import (
    evaluate_credit_risk, evaluate_operational_risk,
    evaluate_fraud_risk, evaluate_reputational_risk,
    get_overall_rag, generate_escalation_report
)

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="AmEx ERM Risk Appetite Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .stMetric { border-radius: 8px; padding: 12px; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
    .rag-card {
        border-radius: 10px; padding: 14px 18px; margin: 6px 0;
        display: flex; justify-content: space-between; align-items: center;
        font-size: 0.92rem; box-shadow: 0 1px 4px rgba(0,0,0,0.07);
    }
    .rag-green  { background: #eafaf1; border-left: 5px solid #2ecc71; }
    .rag-amber  { background: #fef9e7; border-left: 5px solid #f39c12; }
    .rag-red    { background: #fdedec; border-left: 5px solid #e74c3c; }
    .section-header { font-size: 1.05rem; font-weight: 700; color: #2c3e50; margin: 16px 0 8px 0; }
    .overall-banner {
        border-radius: 12px; padding: 18px 24px; text-align: center;
        font-size: 1.3rem; font-weight: 700; margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .disclaimer {
        font-size: 0.75rem; color: #888; margin-top: 30px;
        border-top: 1px solid #ddd; padding-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ── Load data ────────────────────────────────────────────────
credit_df    = get_credit_risk_data()
ops_df       = get_operational_risk_data()
fraud_df     = get_fraud_risk_data()
rep_df       = get_reputational_risk_data()
thresholds   = get_risk_appetite_thresholds()

YEARS = credit_df["Year"].tolist()

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.image("amex_logo.png", width=120)
    st.markdown("## ERM Dashboard")
    st.markdown("**Enterprise Risk Management**  \nRisk Appetite Monitoring")
    st.divider()

    selected_year = st.selectbox("📅 Reporting Period", YEARS[1:], index=len(YEARS)-2)
    st.divider()

    st.markdown("**Risk Appetite Thresholds**")
    st.markdown("""
    | Status | Meaning |
    |--------|---------|
    | 🟢 GREEN | Within appetite |
    | 🟡 AMBER | Approaching limit |
    | 🔴 RED   | Appetite breached |
    """)
    st.divider()
    st.markdown("**Data Sources**")
    st.caption("AXP 10-K/10-Q (2019–2023)  \nBrand Finance · Sustainalytics  \nCFPB Public Disclosures")
    st.divider()
    st.caption("Academic simulation. Thresholds are illustrative.")

# ── Filter data to selected year ─────────────────────────────
yr_idx = YEARS.index(selected_year)

def filter_to_year(df, year_idx):
    return df.iloc[:year_idx + 1].reset_index(drop=True)

c_df = filter_to_year(credit_df, yr_idx)
o_df = filter_to_year(ops_df, yr_idx)
f_df = filter_to_year(fraud_df, yr_idx)
r_df = filter_to_year(rep_df, yr_idx)

# ── Evaluate RAG ─────────────────────────────────────────────
if yr_idx == 0:
    st.warning("Select 2020 or later to enable YoY comparison.")
    st.stop()

credit_results = evaluate_credit_risk(c_df, thresholds["credit"])
ops_results    = evaluate_operational_risk(o_df, thresholds["operational"])
fraud_results  = evaluate_fraud_risk(f_df, thresholds["fraud"])
rep_results    = evaluate_reputational_risk(r_df, thresholds["reputational"])
all_results    = credit_results + ops_results + fraud_results + rep_results

overall_status, overall_emoji, overall_color = get_overall_rag(all_results)

# ── Header ───────────────────────────────────────────────────
st.markdown(f"## 📊 AmEx Enterprise Risk Appetite Dashboard — FY {selected_year}")
st.markdown("*Independent risk oversight simulation using American Express public financial disclosures*")

# ── Overall banner ───────────────────────────────────────────
banner_bg = {"GREEN": "#eafaf1", "AMBER": "#fef9e7", "RED": "#fdedec"}[overall_status]
banner_border = {"GREEN": "#2ecc71", "AMBER": "#f39c12", "RED": "#e74c3c"}[overall_status]
st.markdown(f"""
<div class="overall-banner" style="background:{banner_bg}; border: 2px solid {banner_border};">
    {overall_emoji} Overall Risk Status: <span style="color:{banner_border}">{overall_status}</span>
    &nbsp;|&nbsp; {sum(1 for r in all_results if r['Status']=='GREEN')} GREEN &nbsp;
    {sum(1 for r in all_results if r['Status']=='AMBER')} AMBER &nbsp;
    {sum(1 for r in all_results if r['Status']=='RED')} RED
    &nbsp;|&nbsp; {len(all_results)} Metrics Monitored
</div>
""", unsafe_allow_html=True)

# ── KPI summary row ──────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
latest_c = c_df.iloc[-1]
latest_f = f_df.iloc[-1]
latest_o = o_df.iloc[-1]
latest_r = r_df.iloc[-1]

col1.metric("Net Write-Off Rate", f"{latest_c['Net_WriteOff_Rate_pct']:.2f}%",
            f"{latest_c['Net_WriteOff_Rate_pct'] - c_df.iloc[-2]['Net_WriteOff_Rate_pct']:+.2f}%")
col2.metric("Fraud Loss Rate", f"{latest_f['Fraud_Loss_Rate_bps']} bps",
            f"{latest_f['Fraud_Loss_Rate_bps'] - f_df.iloc[-2]['Fraud_Loss_Rate_bps']:+.0f} bps")
col3.metric("Complaints Index", f"{int(latest_o['Customer_Complaints_Index'])}",
            f"{latest_o['Customer_Complaints_Index'] - o_df.iloc[-2]['Customer_Complaints_Index']:+.0f}")
col4.metric("ESG Risk Score", f"{latest_r['ESG_Risk_Score']:.1f}",
            f"{latest_r['ESG_Risk_Score'] - r_df.iloc[-2]['ESG_Risk_Score']:+.1f}")

st.divider()

# ── Main tabs ────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔴 Credit Risk", "⚙️ Operational Risk",
    "🕵️ Fraud Risk", "🌐 Reputational Risk", "📋 Escalation Report"
])

def render_rag_cards(results):
    for r in results:
        css = {"GREEN": "rag-green", "AMBER": "rag-amber", "RED": "rag-red"}[r["Status"]]
        st.markdown(f"""
        <div class="rag-card {css}">
            <span><strong>{r['Emoji']} {r['Metric']}</strong></span>
            <span>{r['Value']}</span>
            <span style="color:#666">YoY: {r['YoY Change']}</span>
            <span><strong>{r['Status']}</strong></span>
        </div>""", unsafe_allow_html=True)

# ── Tab 1: Credit Risk ───────────────────────────────────────
with tab1:
    col_l, col_r = st.columns([1, 1.6])
    with col_l:
        st.markdown('<div class="section-header">Credit Risk Indicators</div>', unsafe_allow_html=True)
        render_rag_cards(credit_results)

    with col_r:
        fig = make_subplots(rows=2, cols=1, subplot_titles=(
            "Net Write-Off Rate (%)", "Credit Loss Provision (USD Mn)"))
        years = c_df["Year"].tolist()

        fig.add_trace(go.Scatter(x=years, y=c_df["Net_WriteOff_Rate_pct"],
            mode="lines+markers", name="Write-Off Rate",
            line=dict(color="#3498db", width=2.5)), row=1, col=1)
        fig.add_hline(y=thresholds["credit"]["net_writeoff_rate"]["green"],
            line_dash="dot", line_color="#2ecc71", annotation_text="Green", row=1, col=1)
        fig.add_hline(y=thresholds["credit"]["net_writeoff_rate"]["amber"],
            line_dash="dot", line_color="#f39c12", annotation_text="Amber", row=1, col=1)

        colors = ["#2ecc71" if v > 0 else "#e74c3c" for v in c_df["Credit_Loss_Provision_Mn"]]
        fig.add_trace(go.Bar(x=years, y=c_df["Credit_Loss_Provision_Mn"],
            name="Provision", marker_color=colors), row=2, col=1)

        fig.update_layout(height=380, showlegend=False,
            margin=dict(t=40, b=20), plot_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

    # Delinquency trend
    st.markdown('<div class="section-header">Delinquency Rate Trend</div>', unsafe_allow_html=True)
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=years, y=c_df["Delinquency_Rate_30d_pct"],
        mode="lines+markers+text", text=[f"{v}%" for v in c_df["Delinquency_Rate_30d_pct"]],
        textposition="top center", line=dict(color="#9b59b6", width=2.5), fill="tozeroy",
        fillcolor="rgba(155,89,182,0.1)"))
    fig2.add_hline(y=1.2, line_dash="dot", line_color="#2ecc71", annotation_text="Green Threshold")
    fig2.add_hline(y=1.6, line_dash="dot", line_color="#f39c12", annotation_text="Amber Threshold")
    fig2.update_layout(height=220, margin=dict(t=20, b=20), plot_bgcolor="white",
        yaxis_title="30-Day Delinquency Rate (%)")
    st.plotly_chart(fig2, use_container_width=True)

# ── Tab 2: Operational Risk ──────────────────────────────────
with tab2:
    col_l, col_r = st.columns([1, 1.6])
    with col_l:
        st.markdown('<div class="section-header">Operational Risk Indicators</div>', unsafe_allow_html=True)
        render_rag_cards(ops_results)

    with col_r:
        years = o_df["Year"].tolist()
        fig = make_subplots(rows=2, cols=1, subplot_titles=(
            "Legal & Regulatory Provisions (USD Mn)", "Customer Complaints Index"))

        fig.add_trace(go.Bar(x=years, y=o_df["Legal_Regulatory_Provisions_Mn"],
            marker_color="#e67e22", name="Legal Provisions"), row=1, col=1)
        fig.add_trace(go.Scatter(x=years, y=o_df["Customer_Complaints_Index"],
            mode="lines+markers", line=dict(color="#c0392b", width=2.5),
            name="Complaints Index"), row=2, col=1)
        fig.add_hline(y=thresholds["operational"]["complaints_index"]["green"],
            line_dash="dot", line_color="#2ecc71", annotation_text="Green", row=2, col=1)
        fig.add_hline(y=thresholds["operational"]["complaints_index"]["amber"],
            line_dash="dot", line_color="#f39c12", annotation_text="Amber", row=2, col=1)

        fig.update_layout(height=380, showlegend=False,
            margin=dict(t=40, b=20), plot_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

# ── Tab 3: Fraud Risk ────────────────────────────────────────
with tab3:
    col_l, col_r = st.columns([1, 1.6])
    with col_l:
        st.markdown('<div class="section-header">Fraud Risk Indicators</div>', unsafe_allow_html=True)
        render_rag_cards(fraud_results)

    with col_r:
        years = f_df["Year"].tolist()
        fig = make_subplots(rows=2, cols=1, subplot_titles=(
            "Fraud Losses vs Prevention Investment (USD Mn)",
            "Fraud Loss Rate (Basis Points)"))

        fig.add_trace(go.Bar(x=years, y=f_df["Fraud_Losses_Mn"],
            name="Fraud Losses", marker_color="#e74c3c"), row=1, col=1)
        fig.add_trace(go.Bar(x=years, y=f_df["Fraud_Prevention_Investment_Mn"],
            name="Prevention Investment", marker_color="#2ecc71"), row=1, col=1)

        fig.add_trace(go.Scatter(x=years, y=f_df["Fraud_Loss_Rate_bps"],
            mode="lines+markers", line=dict(color="#e74c3c", width=2.5),
            name="Fraud Rate (bps)"), row=2, col=1)
        fig.add_hline(y=thresholds["fraud"]["fraud_loss_rate_bps"]["green"],
            line_dash="dot", line_color="#2ecc71", annotation_text="Green", row=2, col=1)
        fig.add_hline(y=thresholds["fraud"]["fraud_loss_rate_bps"]["amber"],
            line_dash="dot", line_color="#f39c12", annotation_text="Amber", row=2, col=1)

        fig.update_layout(height=380, barmode="group", showlegend=True,
            legend=dict(orientation="h", y=1.05),
            margin=dict(t=40, b=20), plot_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

# ── Tab 4: Reputational Risk ─────────────────────────────────
with tab4:
    col_l, col_r = st.columns([1, 1.6])
    with col_l:
        st.markdown('<div class="section-header">Reputational Risk Indicators</div>', unsafe_allow_html=True)
        render_rag_cards(rep_results)

    with col_r:
        years = r_df["Year"].tolist()
        fig = make_subplots(rows=2, cols=2, subplot_titles=(
            "Brand Value (USD Bn)", "Net Promoter Score",
            "ESG Risk Score", "Regulatory Fines (USD Mn)"))

        fig.add_trace(go.Scatter(x=years, y=r_df["Brand_Value_Bn"],
            mode="lines+markers", fill="tozeroy",
            fillcolor="rgba(52,152,219,0.15)",
            line=dict(color="#3498db", width=2)), row=1, col=1)
        fig.add_trace(go.Bar(x=years, y=r_df["Net_Promoter_Score"],
            marker_color="#2ecc71"), row=1, col=2)
        fig.add_trace(go.Scatter(x=years, y=r_df["ESG_Risk_Score"],
            mode="lines+markers", line=dict(color="#f39c12", width=2)), row=2, col=1)
        fig.add_trace(go.Bar(x=years, y=r_df["Regulatory_Fines_Mn"],
            marker_color="#e74c3c"), row=2, col=2)
        fig.add_hline(y=150, line_dash="dot", line_color="#f39c12",
            annotation_text="Amber", row=2, col=2)

        fig.update_layout(height=400, showlegend=False,
            margin=dict(t=40, b=20), plot_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

# ── Tab 5: Escalation Report ─────────────────────────────────
with tab5:
    st.markdown('<div class="section-header">📋 Governance Escalation Report</div>', unsafe_allow_html=True)
    st.markdown(f"*Auto-generated for FY {selected_year} — ready for CRO / Risk Oversight Committee*")

    report_text = generate_escalation_report(
        selected_year, credit_results, ops_results, fraud_results, rep_results)

    st.download_button(
        label="⬇️ Download Report (.txt)",
        data=report_text,
        file_name=f"AmEx_ERM_Escalation_Report_{selected_year}.txt",
        mime="text/plain"
    )

    st.code(report_text, language=None)

# ── Disclaimer ───────────────────────────────────────────────
st.markdown("""
<div class="disclaimer">
⚠️ <strong>Disclaimer:</strong> This is an independent academic simulation using publicly available
American Express financial disclosures (10-K/10-Q filings, Brand Finance, Sustainalytics, CFPB).
Risk appetite thresholds are illustrative and do not represent AXP's internal risk frameworks.
Built by Navya Behl for educational and portfolio purposes.
</div>
""", unsafe_allow_html=True)
