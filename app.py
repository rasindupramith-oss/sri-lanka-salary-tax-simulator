import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Sri Lanka Salary & APIT Tax Simulator",
    page_icon="💼",
    layout="wide"
)

# 2. Header & Overview
st.title("💼 Sri Lanka Salary, APIT Tax & Take-Home Pay Simulator")
st.markdown("""
*An interactive payroll and tax intelligence tool based on the official Inland Revenue Department (IRD) APIT guidelines (effective for Year of Assessment 2025/2026 onwards).*  
**Created by Rasindu Pramith** | *BSc (Hons) in Applied Statistics, University of Colombo*
""")
st.divider()

# 3. Interactive User Inputs (Sidebar)
st.sidebar.header("💵 Enter Your Salary Details")
basic_salary = st.sidebar.number_input("Monthly Basic Salary (LKR):", min_value=30000, max_value=2000000, value=200000, step=10000)
allowances = st.sidebar.number_input("Fixed / Transport / Living Allowances (LKR):", min_value=0, max_value=1000000, value=50000, step=5000)
other_deductions = st.sidebar.number_input("Other Deductions (Staff Loan, Insurance) (LKR):", min_value=0, max_value=500000, value=0, step=5000)

st.sidebar.markdown("---")
st.sidebar.info("""
**Tax Relief Note:**
Under current IRD rules, the first **Rs. 150,000 / month (Rs. 1.8M / year)** is 100% Tax-Free Personal Relief.
""")

# 4. Payroll & Tax Math Engine
gross_salary = basic_salary + allowances
employee_epf = basic_salary * 0.08
employer_epf = basic_salary * 0.12
employer_etf = basic_salary * 0.03
total_retirement = employee_epf + employer_epf + employer_etf

# APIT Tax Slabs Calculation
tax = 0.0
taxable_income = gross_salary

slab_breakdown = []

if taxable_income > 150000:
    excess = taxable_income - 150000
    slab_breakdown.append({'Slab': 'First Rs. 150,000 (Relief)', 'Taxable Amount': min(taxable_income, 150000), 'Rate': '0%', 'Tax Paid': 0.0})
    
    # Slab 1: Next 83,333.33 @ 6%
    slab1 = min(excess, 83333.33)
    tax1 = slab1 * 0.06
    tax += tax1
    slab_breakdown.append({'Slab': 'Rs. 150,000 - 233,333', 'Taxable Amount': slab1, 'Rate': '6%', 'Tax Paid': tax1})
    excess -= slab1
    
    # Slab 2: Next 41,666.67 @ 18%
    if excess > 0:
        slab2 = min(excess, 41666.67)
        tax2 = slab2 * 0.18
        tax += tax2
        slab_breakdown.append({'Slab': 'Rs. 233,333 - 275,000', 'Taxable Amount': slab2, 'Rate': '18%', 'Tax Paid': tax2})
        excess -= slab2
        
    # Slab 3: Next 41,666.67 @ 24%
    if excess > 0:
        slab3 = min(excess, 41666.67)
        tax3 = slab3 * 0.24
        tax += tax3
        slab_breakdown.append({'Slab': 'Rs. 275,000 - 316,667', 'Taxable Amount': slab3, 'Rate': '24%', 'Tax Paid': tax3})
        excess -= slab3

    # Slab 4: Next 41,666.67 @ 30%
    if excess > 0:
        slab4 = min(excess, 41666.67)
        tax4 = slab4 * 0.30
        tax += tax4
        slab_breakdown.append({'Slab': 'Rs. 316,667 - 358,333', 'Taxable Amount': slab4, 'Rate': '30%', 'Tax Paid': tax4})
        excess -= slab4

    # Slab 5: Above 358,333.33 @ 36%
    if excess > 0:
        tax5 = excess * 0.36
        tax += tax5
        slab_breakdown.append({'Slab': 'Above Rs. 358,333', 'Taxable Amount': excess, 'Rate': '36%', 'Tax Paid': tax5})
else:
    slab_breakdown.append({'Slab': 'First Rs. 150,000 (Relief)', 'Taxable Amount': taxable_income, 'Rate': '0%', 'Tax Paid': 0.0})

take_home_pay = gross_salary - employee_epf - tax - other_deductions
effective_tax_rate = (tax / gross_salary) * 100 if gross_salary > 0 else 0
cost_to_company = gross_salary + employer_epf + employer_etf

# 5. Top Metric Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Net Take-Home Pay", f"Rs. {take_home_pay:,.2f}")
col2.metric("📉 APIT Income Tax", f"Rs. {tax:,.2f}", f"Effective: {effective_tax_rate:.1f}%", delta_color="inverse")
col3.metric("🏦 Monthly Retirement (EPF+ETF)", f"Rs. {total_retirement:,.2f}")
col4.metric("🏢 Total Cost to Company (CTC)", f"Rs. {cost_to_company:,.2f}")

st.write("")

# 6. Interactive Visualizations
chart_col1, chart_col2 = st.columns([1.4, 1.0])

with chart_col1:
    st.subheader("📊 From Gross Salary to Cash in Hand")
    # Plotly Waterfall Chart
    fig_waterfall = go.Figure(go.Waterfall(
        name="Salary Flow",
        orientation="v",
        measure=["absolute", "relative", "relative", "relative", "total"],
        x=["Gross Earnings", "Employee EPF (8%)", "APIT Tax", "Other Deductions", "Net Take-Home"],
        textposition="outside",
        text=[f"Rs. {gross_salary:,.0f}", f"-Rs. {employee_epf:,.0f}", f"-Rs. {tax:,.0f}", f"-Rs. {other_deductions:,.0f}", f"Rs. {take_home_pay:,.0f}"],
        y=[gross_salary, -employee_epf, -tax, -other_deductions, 0],
        connector={"line": {"color": "#BDC3C7"}},
        decreasing={"marker": {"color": "#E74C3C"}},
        increasing={"marker": {"color": "#2ECC71"}},
        totals={"marker": {"color": "#0984E3"}}
    ))
    fig_waterfall.update_layout(template="plotly_white", height=420)
    st.plotly_chart(fig_waterfall, use_container_width=True)

with chart_col2:
    st.subheader("🥧 Where Does Your Gross Salary Go?")
    # Donut Chart Breakdown
    breakdown_data = {
        'Component': ['Take-Home Pay', 'Employee EPF (8%)', 'APIT Tax'],
        'Amount': [take_home_pay, employee_epf, tax]
    }
    if other_deductions > 0:
        breakdown_data['Component'].append('Other Deductions')
        breakdown_data['Amount'].append(other_deductions)
        
    df_donut = pd.DataFrame(breakdown_data)
    fig_donut = px.pie(
        df_donut, 
        names='Component', 
        values='Amount',
        hole=0.45,
        color='Component',
        color_discrete_map={
            'Take-Home Pay': '#2ECC71',
            'Employee EPF (8%)': '#F39C12',
            'APIT Tax': '#E74C3C',
            'Other Deductions': '#95A5A6'
        }
    )
    fig_donut.update_layout(height=420)
    st.plotly_chart(fig_donut, use_container_width=True)

# 7. Detailed Tax Slabs Audit Table
st.divider()
st.subheader("📑 Step-by-Step Tax Deduction Audit (IRD Progressive Tables)")
df_slabs = pd.DataFrame(slab_breakdown)
df_slabs['Taxable Amount'] = df_slabs['Taxable Amount'].apply(lambda x: f"Rs. {x:,.2f}")
df_slabs['Tax Paid'] = df_slabs['Tax Paid'].apply(lambda x: f"Rs. {x:,.2f}")
st.table(df_slabs)

# 8. Educational Section
st.markdown("""
### 💡 Did You Know?
* **Marginal vs. Effective Rate:** Entering the 18% or 24% tax bracket does **NOT** mean you pay 18% or 24% on your whole salary. Only the portion of your income that falls inside that specific slab is taxed at that rate.
* **Hidden Employer Contributions:** Your employer contributes an additional **12% to EPF** and **3% to ETF** on top of your gross pay. For a Rs. 200,000 basic salary, that is **Rs. 30,000 in free monthly savings** added directly to your Central Bank retirement accounts!
""")
