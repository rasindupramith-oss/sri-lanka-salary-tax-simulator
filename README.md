# 💵 Sri Lanka Salary, APIT Tax & Take-Home Pay Simulator

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sri-lanka-salary-tax-simulator.streamlit.app/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Visualization](https://img.shields.io/badge/Visualization-Plotly-3F4F75?style=flat&logo=plotly&logoColor=white)](https://plotly.com/)
[![Affiliation](https://img.shields.io/badge/Affiliation-University%20of%20Colombo-gold?style=flat)](https://science.cmb.ac.lk/)

> **An interactive personal finance and payroll intelligence tool calibrated with the official Inland Revenue Department (IRD) Advance Personal Income Tax (APIT) progressive tables (effective Year of Assessment 2025/2026 onwards).**

🔗 **Live Interactive Application:** [sri-lanka-salary-tax-simulator.streamlit.app](https://sri-lanka-salary-tax-simulator.streamlit.app/)

---

## 📌 Problem & Motivation

In Sri Lanka, recent macroeconomic shifts and tax reforms have created widespread confusion around compensation planning and salary negotiations:
* **The "Marginal Tax Myth":** Many employees believe that crossing into a higher tax bracket reduces their net take-home pay, misunderstanding how marginal progressive taxation works.
* **Cost-to-Company (CTC) Opacity:** Candidates often negotiate based on gross salary without understanding statutory EPF (8% employee vs. 12% employer), ETF (3%), and non-taxable allowances.

This application was engineered to provide **100% transparent, audit-level clarity** for Sri Lankan professionals, job seekers, and HR leaders by translating complex IRD statutory legislation into intuitive visual cashflows.

---

## 🚀 Key Features

* **📑 Exact IRD Progressive APIT Calibration:** Models the official progressive tax slabs starting above the **Rs. 150,000 / month (Rs. 1.8M / year)** tax-free personal relief.
* **🏦 Statutory Social Security Modeling:** Calculates employee EPF (8%), employer EPF (12%), and employer ETF (3%), accurately quantifying total retirement wealth accrual.
* **📊 Dynamic Cashflow Waterfall:** A visual waterfall diagram showing how gross income step-by-step breaks down into deductions, taxes, and final net disposable income.
* **🥧 Interactive Salary Allocation Donut:** A high-level proportion breakdown between take-home pay, statutory savings, and tax liabilities.
* **🔄 Dual Projection Horizons:** Seamlessly toggle between **Monthly Cashflows** and **Annualized Projections (12 Months)**.
* **📑 Step-by-Step Progressive Tax Audit Table:** Complete mathematical transparency showing the exact taxable base, marginal rate, and tax deducted per slab.

---

## 🔬 Payroll & Tax Mathematical Framework

### 1. Gross Earnings & Statutory Retirement
* Gross Salary = Basic Salary + Allowances

Statutory contributions are strictly anchored to the **Basic Salary**:
* Employee EPF (8%) = 0.08 × Basic Salary
* Employer EPF (12%) = 0.12 × Basic Salary
* Employer ETF (3%) = 0.03 × Basic Salary
* Cost to Company (CTC) = Gross Salary + Employer EPF + Employer ETF

### 2. IRD APIT Progressive Tax Brackets (YA 2025/2026)

| Monthly Taxable Bracket | Marginal Rate | Monthly Taxable Base | Max Tax in Slab |
| :--- | :---: | :---: | :---: |
| **First Rs. 150,000** | **0%** | Rs. 150,000.00 | *Rs. 0.00 (Tax-Free)* |
| **Rs. 150,000 – 233,333** | **6%** | Rs. 83,333.33 | Rs. 5,000.00 |
| **Rs. 233,333 – 275,000** | **18%** | Rs. 41,666.67 | Rs. 7,500.00 |
| **Rs. 275,000 – 316,667** | **24%** | Rs. 41,666.67 | Rs. 10,000.00 |
| **Rs. 316,667 – 358,333** | **30%** | Rs. 41,666.67 | Rs. 12,500.00 |
| **Above Rs. 358,333** | **36%** | Excess | Balance × 36% |

### 3. Net Take-Home Reconciliation
* Net Take-Home Pay = Gross Salary - Employee EPF - APIT Tax - Other Deductions
* Effective Tax Rate (%) = (APIT Tax / Gross Salary) × 100

---

## 🛠️ Tech Stack & Architecture

* **Language:** Python 3.10+
* **Application Framework:** Streamlit
* **Data Processing:** Pandas
* **Visualizations:** Plotly Graph Objects (Waterfall chart) & Plotly Express (Donut chart)
* **Design & Styling:** Custom CSS with Modern Dark FinTech Theme

---

## 💻 Local Installation & Setup

To run this simulator on your local machine:

```bash
# 1. Clone the repository
git clone https://github.com/rasindupramith-oss/sri-lanka-salary-tax-simulator.git
cd sri-lanka-salary-tax-simulator

# 2. Create and activate a virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install required libraries
pip install -r requirements.txt

# 4. Launch the application
streamlit run app.py
```

The simulator will launch automatically at `http://localhost:8501`.

---

## 💡 Practical Takeaways for Professionals

1. **The Marginal Fallacy:** Crossing into the 18% or 24% bracket does **not** tax your entire salary at that rate. Only the portion falling within that specific slice is subject to the higher percentage.
2. **The Hidden Wealth Factor:** For a Rs. 200,000 basic salary, your employer contributes an additional **Rs. 30,000 monthly** (12% EPF + 3% ETF) directly into Central Bank-managed trust funds—representing risk-free, tax-advantaged long-term compounding.

---

## 👨‍💻 Author

**Rasindu Pramith**  
*Undergraduate, BSc (Hons) in Applied Statistics*  
*Faculty of Science, University of Colombo, Sri Lanka*  

* 🌐 **Portfolio:** [rasindupramith-oss.github.io](https://rasindupramith-oss.github.io/)
* 💼 **LinkedIn:** [linkedin.com/in/rasindu-pramith](https://www.linkedin.com/in/rasindu-pramith/)
* 💻 **GitHub:** [@rasindupramith-oss](https://github.com/rasindupramith-oss)

---

## 📄 License
This project is open-source and distributed under the [MIT License](LICENSE).
