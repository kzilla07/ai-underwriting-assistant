# AI-Powered Underwriting Assistant (Prototype Logic)
# Tech stack: Streamlit + OpenAI + Pandas

import streamlit as st
import openai
import pandas as pd

# Config
st.set_page_config(page_title="AI Underwriting Assistant", layout="wide")
openai.api_key = "your-openai-api-key-here"

# Sidebar Inputs
st.sidebar.header("Deal Inputs")
purchase_price = st.sidebar.number_input("Purchase Price ($)", value=5000000)
rent_per_unit = st.sidebar.number_input("Monthly Rent/Unit ($)", value=1800)
unit_count = st.sidebar.number_input("Number of Units", value=40)
expense_ratio = st.sidebar.slider("Operating Expense Ratio (%)", min_value=30, max_value=60, value=40)
development_costs = st.sidebar.number_input("Rehab/Development Costs ($)", value=2000000)
exit_cap_rate = st.sidebar.slider("Exit Cap Rate (%)", min_value=3.5, max_value=6.0, value=5.0)
hold_period = st.sidebar.slider("Hold Period (years)", 2, 10, 5)

# Calculations
gross_income = rent_per_unit * unit_count * 12
operating_expenses = gross_income * (expense_ratio / 100)
net_operating_income = gross_income - operating_expenses

# Exit Value & Returns
exit_value = net_operating_income / (exit_cap_rate / 100)
project_cost = purchase_price + development_costs
profit = exit_value - project_cost
untrended_roc = net_operating_income / project_cost

# Display Output
st.title("AI-Enhanced Underwriting Output")
st.subheader("Financial Summary")
st.metric("NOI", f"${net_operating_income:,.0f}")
st.metric("Untrended Return on Cost", f"{untrended_roc:.2%}")
st.metric("Estimated Exit Value", f"${exit_value:,.0f}")
st.metric("Total Profit (Unlevered)", f"${profit:,.0f}")

# AI Commentary Generator
if st.button("Generate AI Commentary"):
    prompt = f"""
    This is a real estate multifamily underwriting summary:
    - Purchase Price: ${purchase_price:,}
    - Rent per Unit: ${rent_per_unit}
    - Unit Count: {unit_count}
    - NOI: ${net_operating_income:,.0f}
    - ROC: {untrended_roc:.2%}
    - Exit Cap Rate: {exit_cap_rate}%
    - Exit Value: ${exit_value:,.0f}
    - Profit: ${profit:,.0f}
    
    Write a 3-paragraph investment summary suitable for LPs.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    ai_summary = response.choices[0].message.content
    st.subheader("AI-Generated Investment Summary")
    st.write(ai_summary)

# Export
if st.button("Export Summary as PDF"):
    st.warning("PDF export functionality not implemented in this prototype.")
