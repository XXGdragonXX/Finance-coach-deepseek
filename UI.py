import streamlit as st
import json
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from streamlit_option_menu import option_menu
from Data_agent import analysisAgent

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    st.title("🏦 Personal Finance Coach")
    st.write("Welcome to your personal finance coach! Track, analyze, and optimize your financial health.")
    
    with st.form("finance_form"):
        st.header("👤 User Information")
        name = st.text_input("Name", "John Doe")
        age = st.number_input("Age", min_value=18, max_value=100, value=30)
        location = st.text_input("Location", "Mumbai, India")
        
        st.header("💰 Income Details")
        monthly_income = st.number_input("Monthly Income", min_value=0, value=80000)
        num_sources = st.number_input("Number of Income Sources", min_value=1, value=2)
        income_sources = []
        for i in range(num_sources):
            with st.expander(f"Income Source {i+1}"):
                type_ = st.text_input(f"Source Type {i+1}", "Salary" if i == 0 else "Freelancing")
                amount = st.number_input(f"Amount {i+1}", min_value=0, value=70000 if i == 0 else 10000)
                income_sources.append({"type": type_, "amount": amount})
        
        st.header("📉 Expense Details")
        recurring_expenses = {
            "rent": st.number_input("Rent", min_value=0, value=20000),
            "utilities": st.number_input("Utilities", min_value=0, value=5000),
            "groceries": st.number_input("Groceries", min_value=0, value=10000),
            "transportation": st.number_input("Transportation", min_value=0, value=5000),
            "entertainment": st.number_input("Entertainment", min_value=0, value=5000),
            "other": st.number_input("Other", min_value=0, value=1000)
        }
        
        st.header("💳 Debt Information")
        loans = []
        num_loans = st.number_input("Number of Loans", min_value=0, value=1)
        for i in range(num_loans):
            with st.expander(f"Loan {i+1}"):
                loan_type = st.text_input(f"Loan Type {i+1}", "Home Loan")
                outstanding_amount = st.number_input(f"Outstanding Amount {i+1}", min_value=0, value=1200000)
                monthly_emi = st.number_input(f"Monthly EMI {i+1}", min_value=0, value=15000)
                loans.append({"type": loan_type, "outstandingAmount": outstanding_amount, "monthlyEMI": monthly_emi})
        
        st.header("🎯 Financial Goals")
        short_term_goals = [{"goal": "Vacation", "amount": 50000, "timeFrame": "6 months"}]
        long_term_goals = [{"goal": "Retirement Fund", "amount": 5000000, "timeFrame": "20 years"}]
        
        st.header("📈 Investment Preferences")
        risk_tolerance = st.selectbox("Risk Tolerance", ["Low", "Moderate", "High"], index=1)
        investment_types = st.multiselect("Preferred Investment Types", ["Mutual Funds", "Stocks", "Bonds", "Real Estate"], ["Mutual Funds", "Stocks"])
        
        st.header("💾 Savings Details")
        current_savings = st.number_input("Current Savings", min_value=0, value=200000)
        saving_methods = st.multiselect("Preferred Saving Methods", ["Fixed Deposit", "Recurring Deposit", "Savings Account"], ["Fixed Deposit", "Recurring Deposit"])
        
        st.header("📝 Tax Information")
        tax_bracket = st.text_input("Tax Bracket", "20%")
        tax_saving_investments = st.multiselect("Tax Saving Investments", ["PPF", "ELSS", "NPS"], ["PPF", "ELSS"])
        
        st.header("📊 Credit Score")
        credit_score = st.number_input("Credit Score", min_value=300, max_value=900, value=750)
        
        submitted = st.form_submit_button("Submit & Analyze")
    
    if submitted:
        st.session_state['user_data'] = {
            "user": {"name": name, "age": age, "location": location},
            "incomeDetails": {"monthlyIncome": monthly_income, "incomeSources": income_sources},
            "expenseDetails": {"recurringExpenses": recurring_expenses},
            "debtInformation": {"loans": loans},
            "financialGoals": {"shortTerm": short_term_goals, "longTerm": long_term_goals},
            "investmentPreferences": {"riskTolerance": risk_tolerance, "preferredInvestmentTypes": investment_types},
            "savingsDetails": {"currentSavings": current_savings, "preferredSavingMethods": saving_methods},
            "taxInformation": {"taxBracket": tax_bracket, "taxSavingInvestments": tax_saving_investments},
            "creditScore": credit_score
        }
        st.session_state['page'] = "Output"
        st.experimental_rerun()
    
if "page" not in st.session_state:
    st.session_state['page'] = "Input"

if st.session_state['page'] == "Input":
    main()
elif st.session_state['page'] == "Output":
    st.header("📊 Financial Analysis")
    analyser = analysisAgent(st.session_state['user_data'])
    
    if st.button("Generate Budget Chart"): 
        budget = analyser.mainModel()
        sorted_budget = dict(sorted(budget.items(), key=lambda item: item[1], reverse=True))
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.set_theme(style="whitegrid")
        sns.barplot(x=list(sorted_budget.values()), y=list(sorted_budget.keys()), palette="coolwarm", ax=ax)
        ax.set_xlabel("Amount (INR)", fontsize=12)
        ax.set_ylabel("Category", fontsize=12)
        ax.set_title("Monthly Budget Allocation", fontsize=14, fontweight='bold')
        for i, value in enumerate(sorted_budget.values()):
            ax.text(value + 500, i, f"{value:,}", va='center', fontsize=11, color='black')
        st.pyplot(fig)
    
    if st.button("Generate Analytics"): 
        analysis = analyser.mainModel2()
        st.json(analysis)
    
    if st.button("Go Back"):
        st.session_state['page'] = "Input"
        st.experimental_rerun()