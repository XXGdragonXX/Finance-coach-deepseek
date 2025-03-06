import streamlit as st
import json

from Data_agent import analysisAgent

def main():
    st.title("Personal Finance Coach")
    
    # User Information
    st.header("User Information")
    name = st.text_input("Name", "John Doe")
    age = st.number_input("Age", min_value=18, max_value=100, value=30)
    location = st.text_input("Location", "Mumbai, India")
    
    # Income Details
    st.header("Income Details")
    monthly_income = st.number_input("Monthly Income", min_value=0, value=80000)
    income_sources = []
    num_sources = st.number_input("Number of Income Sources", min_value=1, value=2)
    
    for i in range(num_sources):
        with st.expander(f"Income Source {i+1}"):
            type_ = st.text_input(f"Source Type {i+1}", "Salary" if i == 0 else "Freelancing")
            amount = st.number_input(f"Amount {i+1}", min_value=0, value=70000 if i == 0 else 10000)
            income_sources.append({"type": type_, "amount": amount})
    
    # Expense Details
    st.header("Expense Details")
    recurring_expenses = {
        "rent": st.number_input("Rent", min_value=0, value=20000),
        "utilities": st.number_input("Utilities", min_value=0, value=5000),
        "groceries": st.number_input("Groceries", min_value=0, value=10000),
        "transportation": st.number_input("Transportation", min_value=0, value=5000),
        "entertainment": st.number_input("Entertainment", min_value=0, value=5000),
        "other": st.number_input("Other", min_value=0, value=1000),
    }
    
    # Debt Information
    st.header("Debt Information")
    loans = []
    num_loans = st.number_input("Number of Loans", min_value=0, value=1)
    for i in range(num_loans):
        with st.expander(f"Loan {i+1}"):
            loan_type = st.text_input(f"Loan Type {i+1}", "Home Loan")
            outstanding_amount = st.number_input(f"Outstanding Amount {i+1}", min_value=0, value=1200000)
            monthly_emi = st.number_input(f"Monthly EMI {i+1}", min_value=0, value=15000)
            loans.append({"type": loan_type, "outstandingAmount": outstanding_amount, "monthlyEMI": monthly_emi})
    
    # Credit Card Information
    credit_cards = []
    num_cards = st.number_input("Number of Credit Cards", min_value=0, value=1)
    for i in range(num_cards):
        with st.expander(f"Credit Card {i+1}"):
            bank = st.text_input(f"Bank {i+1}", "ABC Bank")
            outstanding_balance = st.number_input(f"Outstanding Balance {i+1}", min_value=0, value=20000)
            minimum_due = st.number_input(f"Minimum Due {i+1}", min_value=0, value=2000)
            credit_cards.append({"bank": bank, "outstandingBalance": outstanding_balance, "minimumDue": minimum_due})
    
    # Financial Goals
    st.header("Financial Goals")
    short_term_goals = []
    num_short_goals = st.number_input("Number of Short-Term Goals", min_value=0, value=1)
    for i in range(num_short_goals):
        with st.expander(f"Short-Term Goal {i+1}"):
            goal = st.text_input(f"Goal {i+1}", "Vacation")
            amount = st.number_input(f"Amount {i+1}", min_value=0, value=50000)
            time_frame = st.text_input(f"Time Frame {i+1}", "6 months")
            short_term_goals.append({"goal": goal, "amount": amount, "timeFrame": time_frame})
    
    # Investment Preferences
    st.header("Investment Preferences")
    risk_tolerance = st.selectbox("Risk Tolerance", ["Low", "Moderate", "High"], index=1)
    preferred_investments = st.multiselect("Preferred Investments", ["Mutual Funds", "Stocks", "Bonds", "Real Estate"], ["Mutual Funds", "Stocks"])
    
    # Savings Details
    st.header("Savings Details")
    current_savings = st.number_input("Current Savings", min_value=0, value=200000)
    preferred_saving_methods = st.multiselect("Preferred Saving Methods", ["Fixed Deposit", "Recurring Deposit", "Savings Account"], ["Fixed Deposit", "Recurring Deposit"])
    
    # Tax Information
    st.header("Tax Information")
    tax_bracket = st.selectbox("Tax Bracket", ["5%", "10%", "20%", "30%"], index=2)
    tax_saving_investments = st.multiselect("Tax Saving Investments", ["PPF", "ELSS", "NPS", "FD"], ["PPF", "ELSS"])
    
    # Credit Score
    credit_score = st.slider("Credit Score", min_value=300, max_value=900, value=750)
    
    # Submit Button
    if st.button("Submit"):
        user_data = {
            "user": {"name": name, "age": age, "location": location},
            "incomeDetails": {"monthlyIncome": monthly_income, "incomeSources": income_sources},
            "expenseDetails": {"recurringExpenses": recurring_expenses},
            "debtInformation": {"loans": loans, "creditCards": credit_cards},
            "financialGoals": {"shortTerm": short_term_goals},
            "investmentPreferences": {"riskTolerance": risk_tolerance, "preferredInvestmentTypes": preferred_investments},
            "savingsDetails": {"currentSavings": current_savings, "preferredSavingMethods": preferred_saving_methods},
            "taxInformation": {"taxBracket": tax_bracket, "taxSavingInvestments": tax_saving_investments},
            "creditScore": credit_score
        }
        analyser = analysisAgent(user_data)
        budget , tracker = analyser.mainModel()
        st.table(tracker)
        # st.json(user_data)


if __name__ == "__main__":
    main()