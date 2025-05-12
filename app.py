import streamlit as st
import openai
import pandas as pd

# Configuration
st.set_page_config(page_title="AI Underwriting Assistant", layout="wide")
openai.api_key = "your-openai-api-key-here"  # Replace with your actual key temporarily

# Sidebar Inputs
st.sidebar.header("Deal Inputs")
purchase_price = st.sidebar.number_input("Purchase Price ($)", value=5000000)
rent_per_unit = st.sidebar.number_input("Monthly Rent/Unit ($)", value=1800)
unit_count = st.sidebar.number_input("Number of Units", value=40)
expense_ratio = st.sidebar.slider("Operating Expense Ratio (%)", min_value=30, max_value=60, value=40)
development_costs = st.sidebar.number_input("Rehab/Development Costs ($)", value=2000000)
exit_cap_rate = st.sidebar.slider("Exit Cap Rate (%)", min_value=3.5, max_value=6.0, value=5.0)
hold_period = st.sidebar.slider("Hold Period (years)", 2, 10, 5)

# Entity Selection
st.sidebar.header("Select Your Role")
entity_type = st.sidebar.selectbox("Investment Entity", ["General Partner/Sponsor", "Limited Partner", "Lender"])

# Entity-specific Inputs
st.sidebar.header("Investment Inputs")

if entity_type == "General Partner/Sponsor":
    gp_equity = st.sidebar.number_input("GP Equity Contribution ($)", value=500000)
    acquisition_fee = st.sidebar.number_input("Acquisition Fee (%)", value=1.0)
    asset_mgmt_fee = st.sidebar.number_input("Asset Mgmt Fee (% of EGI)", value=1.0)
    promote_share = st.sidebar.slider("Promote Share (%)", 10, 50, 20)
elif entity_type == "Limited Partner":
    lp_equity = st.sidebar.number_input("LP Equity Contribution ($)", value=3000000)
    preferred_return = st.sidebar.slider("Preferred Return (%)", 6, 12, 8)
    equity_multiple = st.sidebar.slider("Target Equity Multiple", 1.5, 3.0, 2.0)
elif entity_type == "Lender":
    loan_amount = st.sidebar.number_input("Loan Amount ($)", value=4000000)
    interest_rate = st.sidebar.slider("Interest Rate (%)", 3.0, 9.0, 6.0)
    term = st.sidebar.slider("Loan Term (years)", 1, 10, 5)

# Basic Calculations
gross_income = rent_per_unit * unit_count * 12
operating_expenses = gross_income * (expense_ratio / 100)
net_operating_income = gross_income - operating_expenses
exit_value = net_operating_income / (exit_cap_rate / 100)
project_cost = purchase_price + development_costs
profit = exit_value - project_cost
untrended_roc = net_operating_income / project_cost

# Display
st.title("AI-Enhanced Underwriting Output")
st.subheader("Financial Summary")
st.metric("NOI", f"${net_operating_income:,.0f}")
st.metric("Untrended Return on Cost", f"{untrended_roc:.2%}")
st.metric("Estimated Exit Value", f"${exit_value:,.0f}")
st.metric("Total Profit (Unlevered)", f"${profit:,.0f}")

# Role-Specific Outputs
st.subheader("Entity-Specific Outputs")

if entity_type == "General Partner/Sponsor":
    total_fees = acquisition_fee / 100 * purchase_price + asset_mgmt_fee / 100 * gross_income * hold_period
    promote_profit = (promote_share / 100) * profit
    st.write(f"**Total Fees (Acquisition + Asset Mgmt):** ${total_fees:,.0f}")
    st.write(f"**Promote Profit:** ${promote_profit:,.0f}")
    st.write(f"**Timing of Fees:** Acquisition at close, AM Fees annually, Promote at exit")

elif entity_type == "Limited Partner":
    total_return = lp_equity * equity_multiple
    pref_earnings = lp_equity * (preferred_return / 100) * hold_period
    st.write(f"**Total Return at Exit:** ${total_return:,.0f}")
    st.write(f"**Preferred Earnings (Over Hold):** ${pref_earnings:,.0f}")
    st.write(f"**Timing:** Pref Paid Annually (if structured as coupon), Remainder at Exit")

elif entity_type == "Lender":
    annual_interest = loan_amount * (interest_rate / 100)
    total_interest = annual_interest * term
    st.write(f"**Annual Interest Income:** ${annual_interest:,.0f}")
    st.write(f"**Total Interest Over Term:** ${total_interest:,.0f}")
    st.write(f"**Timing:** Interest Paid Annually or Monthly, Principal at Maturity")

# AI Commentary Generator
if st.button("Generate AI Commentary"):
    prompt = f"""
    Real estate underwriting summary:
    - Role: {entity_type}
    - Purchase Price: ${purchase_price:,}
    - Rent per Unit: ${rent_per_unit}
    - Unit Count: {unit_count}
    - NOI: ${net_operating_income:,.0f}
    - Exit Value: ${exit_value:,.0f}
    - Profit: ${profit:,.0f}
    
    Write a 3-paragraph investment summary suitable for LPs or lenders.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    ai_summary = response.choices[0].message.content
    st.subheader("AI-Generated Investment Summary")
    st.write(ai_summary)
