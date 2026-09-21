import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Sri Lanka Smart Salary & Tax Simulator",
    page_icon="💵",
    layout="wide"
)

# 2. Custom CSS for Luxury FinTech Styling
st.markdown("""
<style>
    /* Metric Card Styling */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border: 1px solid #334155;
        padding: 18px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    div[data-testid="stMetric"]:hover {
        border-color: #38bdf8;
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
    div[data-testid="stMetric"] label {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-size: 1.6rem !important;
        font-weight: 800 !important;
    }
    /* Section Headings */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# 3. Header & Overview
st.title("💼 Sri Lanka Salary, APIT Tax & Take-Home Pay Simulator")
st.markdown("""
*An interactive personal finance intelligence tool calibrated with the official Inland Revenue Department (IRD) APIT progressive tax tables (effective for Year of Assessment 2025/2026 onwards).*  
**Engineered by Rasindu Pramith** | *BSc (Hons) in Applied Statistics, University of Colombo*
""")
st.divider()

# 4. Interactive User Inputs (Sidebar)
st.sidebar.header("💵 Enter Your Salary Details")
basic_salary = st.sidebar.number_input("Monthly Basic Salary (LKR):", min_value=30000, max_value=2500000, value=200000, step=10000)
allowances = st.sidebar.number_input("Fixed / Transport / Living Allowances (LKR):", min_value=0, max_value=1500000, value=40000, step=5000)
other_deductions = st.sidebar.number_input("Other Deductions (Staff Loan, Insurance) (LKR):", min_value=0, max_value=500000, value=20000, step=5000)

view_mode = st.sidebar.radio("View Projections As:", ["Monthly", "Annualized (12 Months)"], horizontal=True)
multiplier = 12 if view_mode == "Annualized (12 Months)" else 1

st.sidebar.markdown("---")
st.sidebar.info("""
**💡 IRD Tax Relief Rule:**
The first **Rs. 150,000 / month (Rs. 1,800,000 / year)** is 100% Tax-Free Personal Relief under modern Sri Lankan tax legislation.
""")

# 5. Core Payroll & Tax Math Engine
gross_salary = basic_salary + allowances
employee_epf = basic_salary * 0.08
employer_epf = basic_salary * 0.12
employer_etf = basic_salary * 0.03
total_retirement = employee_epf + employer_epf + employer_etf

# APIT Progressive Tax Calculation
tax = 0.0
taxable_income = gross_salary

slab_breakdown = []

if taxable_income > 150000:
    excess = taxable_income - 150000
    slab_breakdown.append({'Tax Slab': 'First Rs. 150,000 (Tax-Free Relief)', 'Taxable Base': min(taxable_income, 150000), 'Tax Rate': '0%', 'Tax Deducted': 0.0})
    
    # Slab 1: Next 83,333.33 @ 6%
    slab1 = min(excess, 83333.33)
    tax1 = slab1 * 0.06
    tax += tax1
    slab_breakdown.append({'Tax Slab': 'Rs. 150,000 – 233,333', 'Taxable Base': slab1, 'Rate': '6%', 'Tax Deducted': tax1})
    excess -= slab1
    
    # Slab 2: Next 41,666.67 @ 18%
    if excess > 0:
        slab2 = min(excess, 41666.67)
        tax2 = slab2 * 0.18
        tax += tax2
        slab_breakdown.append({'Tax Slab': 'Rs. 233,333 – 275,000', 'Taxable Base': slab2, 'Rate': '18%', 'Tax Deducted': tax2})
        excess -= slab2
        
    # Slab 3: Next 41,666.67 @ 24%
    if excess > 0:
        slab3 = min(excess, 41666.67)
        tax3 = slab3 * 0.24
        tax += tax3
        slab_breakdown.append({'Tax Slab': 'Rs. 275,000 – 316,667', 'Taxable Base': slab3, 'Rate': '24%', 'Tax Deducted': tax3})
        excess -= slab3

    # Slab 4: Next 41,666.67 @ 30%
    if excess > 0:
        slab4 = min(excess, 41666.67)
        tax4 = slab4 * 0.30
        tax += tax4
        slab_breakdown.append({'Tax Slab': 'Rs. 316,667 – 358,333', 'Taxable Base': slab4, 'Rate': '30%', 'Tax Deducted': tax4})
        excess -= slab4

    # Slab 5: Above 358,333.33 @ 36%
    if excess > 0:
        tax5 = excess * 0.36
        tax += tax5
        slab_breakdown.append({'Tax Slab': 'Above Rs. 358,333', 'Taxable Base': excess, 'Rate': '36%', 'Tax Deducted': tax5})
else:
    slab_breakdown.append({'Tax Slab': 'First Rs. 150,000 (Tax-Free Relief)', 'Taxable Base': taxable_income, 'Rate': '0%', 'Tax Deducted': 0.0})

take_home_pay = gross_salary - employee_epf - tax - other_deductions
effective_tax_rate = (tax / gross_salary) * 100 if gross_salary > 0 else 0
cost_to_company = gross_salary + employer_epf + employer_etf

# 6. Top Financial KPI Widgets
prefix = "Annual" if multiplier == 12 else "Monthly"
col1, col2, col3, col4 = st.columns(4)
col1.metric(f"💰 {prefix} Take-Home Pay", f"Rs. {take_home_pay * multiplier:,.2f}")
col2.metric(f"📉 {prefix} APIT Tax", f"Rs. {tax * multiplier:,.2f}", f"Effective: {effective_tax_rate:.1f}%", delta_color="inverse")
col3.metric(f"🏦 {prefix} Retirement (EPF+ETF)", f"Rs. {total_retirement * multiplier:,.2f}")
col4.metric(f"🏢 {prefix} Cost to Company (CTC)", f"Rs. {cost_to_company * multiplier:,.2f}")

st.write("")

# 7. Visual Analytics (Waterfall & Donut)
chart_col1, chart_col2 = st.columns([1.3, 1.0])

with chart_col1:
    st.subheader(f"📊 Cashflow Waterfall ({prefix})")
    fig_waterfall = go.Figure(go.Waterfall(
        name="Salary Flow",
        orientation="v",
        measure=["absolute", "relative", "relative", "relative", "total"],
        x=["Gross Salary", "Employee EPF (8%)", "APIT Tax", "Other Deductions", "Net Take-Home"],
        textposition="outside",
        text=[f"Rs. {gross_salary*multiplier:,.0f}", f"-Rs. {employee_epf*multiplier:,.0f}", f"-Rs. {tax*multiplier:,.0f}", f"-Rs. {other_deductions*multiplier:,.0f}", f"Rs. {take_home_pay*multiplier:,.0f}"],
        y=[gross_salary*multiplier, -employee_epf*multiplier, -tax*multiplier, -other_deductions*multiplier, 0],
        connector={"line": {"color": "#64748b", "width": 1.5}},
        decreasing={"marker": {"color": "#ef4444"}},
        increasing={"marker": {"color": "#10b981"}},
        totals={"marker": {"color": "#0ea5e9"}}
    ))
    fig_waterfall.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=420)
    st.plotly_chart(fig_waterfall, use_container_width=True)

with chart_col2:
    st.subheader(f"🥧 Salary Allocation ({prefix})")
    breakdown_data = {
        'Component': ['Take-Home Pay', 'Employee EPF (8%)', 'APIT Tax'],
        'Amount': [take_home_pay * multiplier, employee_epf * multiplier, tax * multiplier]
    }
    if other_deductions > 0:
        breakdown_data['Component'].append('Other Deductions')
        breakdown_data['Amount'].append(other_deductions * multiplier)
        
    df_donut = pd.DataFrame(breakdown_data)
    fig_donut = px.pie(
        df_donut, 
        names='Component', 
        values='Amount',
        hole=0.5,
        color='Component',
        color_discrete_map={
            'Take-Home Pay': '#10b981',
            'Employee EPF (8%)': '#f59e0b',
            'APIT Tax': '#ef4444',
            'Other Deductions': '#64748b'
        }
    )
    fig_donut.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=420)
    st.plotly_chart(fig_donut, use_container_width=True)

# 8. Progressive Audit Table
st.divider()
st.subheader("📑 Step-by-Step Tax Deduction Audit (IRD Progressive Tables)")
df_slabs = pd.DataFrame(slab_breakdown)
df_slabs['Taxable Base'] = df_slabs['Taxable Base'].apply(lambda x: f"Rs. {x*multiplier:,.2f}")
df_slabs['Tax Deducted'] = df_slabs['Tax Deducted'].apply(lambda x: f"Rs. {x*multiplier:,.2f}")
st.table(df_slabs)

# 9. Practical Financial Takeaways
st.markdown("""
### 💡 Strategic Salary Insights
1. **The Marginal Tax Myth:** Entering a higher tax bracket does **NOT** tax your whole income at that rate. Only the slice of earnings within that bracket is taxed at the higher percentage.
2. **The Wealth Engine (Employer Contribution):** Your employer pays an extra **12% to EPF** and **3% to ETF** on top of your gross pay. For a Rs. 200,000 basic salary, that is **Rs. 30,000 in free wealth built monthly** in Central Bank trust accounts!
""")
