import streamlit as st
import json
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import plotly.express as px
from streamlit_option_menu import option_menu
from Data_agent import analysisAgent
from Spending_tracker import spendAgent

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def mainForm():
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
            "debtInformation": {"loans": loans},
            "financialGoals": {"shortTerm": short_term_goals, "LongTerm": long_term_goals},
            "investmentPreferences": {"riskTolerance": risk_tolerance, "preferredInvestmentTypes": investment_types},
            "savingsDetails": {"currentSavings": current_savings, "preferredSavingMethods": saving_methods},
            "taxInformation": {"taxBracket": tax_bracket, "taxSavingInvestments": tax_saving_investments},
            "creditScore": credit_score
        }
        st.session_state['page'] = "Output"
        st.rerun()

def expenseForm():
    st.title("Your expense analysis")
    st.write ("Here you can added your expenses and we will analyse and give you details of what you are doing wrong")
    with st.form("expense_input_form"):
        st.subheader("Monthly Expenses")
        rent = st.number_input("Rent/Mortgage", min_value=0, value=20000)
        utilities = st.number_input("Utilities", min_value=0, value=5000)
        groceries = st.number_input("Groceries", min_value=0, value=10000)
        transportation = st.number_input("Transportation", min_value=0, value=5000)
        entertainment = st.number_input("Entertainment", min_value=0, value=5000)
        debtRepayment = st.number_input("Debt Repayment", min_value=0, value=1000)
        healthcare = st.number_input("Healthcare",min_value=0, value=1000)
        miscellaneous = st.number_input("Miscellanous",min_value=0, value=1000)
        
        submitted_expenses = st.form_submit_button("Submit Expenses")
    
    if submitted_expenses:
        del st.session_state['expenses']
        st.session_state['expenses'] = {
            "Rent": rent,
            "Utilities": utilities,
            "Groceries": groceries,
            "Transportation": transportation,
            "Entertainment": entertainment,
            "DebtRepayment":debtRepayment,
            "Healthcare":healthcare,
            "Miscellaneous":miscellaneous 
        }
        st.session_state['page'] = "ExpenseAnalysis" 
        st.rerun()



    
if "page" not in st.session_state:
    st.session_state['page'] = "Input"

if st.session_state['page'] == "Input":
    mainForm()
elif st.session_state['page'] == "Output":
    st.header("📊 Financial Analysis")
    
    # Check if the budget is already computed and stored in session_state
    if 'budget' not in st.session_state:
        analyser = analysisAgent(st.session_state['user_data'])
        budget = analyser.mainModel()
        sorted_budget = dict(sorted(budget.items(), key=lambda item: item[1], reverse=True))
        st.session_state['budget'] = sorted_budget
    
    if st.button("Go Back"):
        st.session_state['page'] = "Input"
        st.rerun()
    if st.button("Analyse your spending habits"):
        st.session_state['page'] = "Expense Input"
        st.rerun()
    elif st.button("View Budget Allocation"):
        st.session_state['page'] = "ExpenseAnalysis"
        st.rerun()

elif st.session_state['page'] == "Expense Input":
    expenseForm()
    if st.button("Go Back"):
        st.session_state['page'] = "Output"
        st.rerun()

elif st.session_state['page'] == "ExpenseAnalysis":
    sorted_budget = st.session_state['budget']
    st.subheader(f" {st.session_state['user_data']['user']['name']}'s Budget Report")
    fig = px.bar(
        x=list(sorted_budget.keys()),
        y=list(sorted_budget.values()),
        labels={"x": "Category", "y": "Amount (INR)"},
        title="Monthly Budget Allocation",
        text=[f"{value:,}" for value in sorted_budget.values()],  # Add values as text on bars
        color=list(sorted_budget.values()),  # Add color gradient
        color_continuous_scale=px.colors.sequential.Viridis  # Use a color scale
    )
    
    # Update layout for better readability
    fig.update_traces(textposition='outside')  
    fig.update_layout(
        xaxis_title="Category",
        yaxis_title="Amount (INR)",
        title_font_size=20,
        title_x=0.5,  
        showlegend=False, 
        hovermode="x unified"  
    )
    
    # Display the Plotly chart
    st.plotly_chart(fig, use_container_width=True)
    
    if 'expenses' in st.session_state.keys():
        # Check if the spending analysis report is already computed and stored in session_state
        if 'spending_report' not in st.session_state:
            spendAnalyser = spendAgent(st.session_state['expenses'], st.session_state['budget'])
            report = spendAnalyser.mainModel2()
            st.session_state['spending_report'] = report
        st.write(st.session_state['spending_report'])
        
        if st.button("Go Back"):
            st.session_state['page'] = "Expense Input"
            st.rerun()
    
    if st.button("Go Back"):
        st.session_state['page'] = "Output"
        st.rerun()


