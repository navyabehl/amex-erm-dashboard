# 📊 AmEx ERM Risk Appetite Dashboard

An independent Enterprise Risk Management (ERM) simulation that monitors American Express's publicly reported risk metrics against hypothetical risk appetite thresholds — replicating the kind of oversight function performed by a bank's Chief Risk Officer (CRO) organisation.

> **Built by:** Navya Behl | M.Sc. Economics, Dr. B.R. Ambedkar School of Economics University  
> **Purpose:** Academic portfolio project demonstrating ERM concepts, risk monitoring, and data automation

---

## 🎯 Project Motivation

The ERM function at any financial institution is responsible for:
- Monitoring risk exposure across Credit, Operational, Fraud, and Reputational risk domains
- Assessing whether metrics remain within the board-approved **risk appetite**
- Escalating breaches to governance forums (e.g. Risk Oversight Committee, CRO)
- Automating risk reporting dashboards to improve monitoring efficiency

This project simulates exactly that workflow using **American Express's publicly disclosed financial data** (10-K/10-Q annual and quarterly filings, 2019–2023).

---

## 🗂️ Risk Domains Covered

| Risk Domain | Key Metrics Monitored |
|---|---|
| **Credit Risk** | Net write-off rate, 30-day delinquency rate, provision-to-revenue ratio |
| **Operational Risk** | Legal/regulatory provisions, customer complaints index, operational loss ratio |
| **Fraud Risk** | Fraud loss rate (bps), fraud YoY growth, fraud losses vs. prevention investment |
| **Reputational Risk** | ESG risk score, CFPB regulatory actions, regulatory fines, brand value, NPS |

---

## 🟢🟡🔴 RAG Status Framework

Each metric is assessed against a two-tier risk appetite threshold:

```
GREEN  → Metric within risk appetite
AMBER  → Metric approaching appetite limit (early warning)
RED    → Metric has breached risk appetite → escalation required
```

The overall portfolio status reflects the **worst metric** across all domains — consistent with conservative ERM practice.

---

## 📋 Governance Escalation Report

The dashboard auto-generates a plain-text **escalation report** formatted for a CRO / Risk Oversight Committee, including:
- Overall risk status and metric summary
- RED items requiring immediate attention
- AMBER watch-list items
- Full domain-by-domain breakdown

Reports are downloadable as `.txt` files.

---

## 🛠️ Tech Stack

| Tool | Use |
|---|---|
| Python | Core analysis and data pipeline |
| Streamlit | Interactive dashboard UI |
| Plotly | Time-series charts and trend visualisations |
| Pandas | Data wrangling and metric computation |

---

## 📁 Project Structure

```
amex-erm-dashboard/
│
├── app.py                   # Main Streamlit dashboard
├── requirements.txt
│
├── data/
│   └── amex_data.py         # AXP public financial data + risk appetite thresholds
│
└── utils/
    └── rag_engine.py        # RAG evaluation engine + escalation report generator
```

---

## 🚀 How to Run

```bash
# 1. Clone the repo
git clone https://github.com/navyabehl/amex-erm-dashboard.git
cd amex-erm-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch dashboard
streamlit run app.py
```

---

## 📊 Data Sources

All data is sourced from **publicly available disclosures** — no proprietary or internal AmEx data is used:

- **American Express 10-K Annual Reports** (2019–2023) — write-off rates, delinquency, provisions, fraud losses
- **Brand Finance Global 500** — brand value estimates
- **Sustainalytics** — ESG risk scores
- **Consumer Financial Protection Bureau (CFPB)** — regulatory actions count
- **AXP Investor Day Presentations** — supplementary operational metrics

---

## ⚠️ Disclaimer

This is an **independent academic simulation**. Risk appetite thresholds are illustrative and calibrated to AXP's peer group for educational purposes — they do not represent American Express's internal risk frameworks, policies, or governance standards. This project is not affiliated with or endorsed by American Express.

---

## 📌 Key ERM Concepts Demonstrated

- **Risk Appetite Framework** — defining quantitative tolerance limits per risk domain
- **Risk Exposure Monitoring** — tracking metrics against thresholds over time
- **Governance Escalation** — automated reporting for Risk Oversight Committees
- **Multi-Risk Aggregation** — Credit, Operational, Fraud, and Reputational risk in one view
- **Dashboard Automation** — Python-based reporting replacing manual monitoring
