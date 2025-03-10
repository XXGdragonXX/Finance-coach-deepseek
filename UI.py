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

def home_page():
    st.title("🏦 Personal Finance Coach")
    st.write("Welcome to your personal finance coach! Track, analyze, and optimize your financial health.")

def user_info_page():
    st.header("👤 User Information")
    name = st.text_input("Name", "John Doe")
    age = st.number_input("Age", min_value=18, max_value=100, value=30)
    location = st.text_input("Location", "Mumbai, India")
    return {"name": name, "age": age, "location": location}

def income_page():
    st.header("💰 Income Details")
    monthly_income = st.number_input("Monthly Income", min_value=0, value=80000)
    num_sources = st.number_input("Number of Income Sources", min_value=1, value=2)
    income_sources = []
    for i in range(num_sources):
        with st.expander(f"Income Source {i+1}"):
            type_ = st.text_input(f"Source Type {i+1}", "Salary" if i == 0 else "Freelancing")
            amount = st.number_input(f"Amount {i+1}", min_value=0, value=70000 if i == 0 else 10000)
            income_sources.append({"type": type_, "amount": amount})
    return {"monthlyIncome": monthly_income, "incomeSources": income_sources}

def expenses_page():
    st.header("📉 Expense Details")
    recurring_expenses = {
        "Rent": st.number_input("Rent", min_value=0, value=20000),
        "Utilities": st.number_input("Utilities", min_value=0, value=5000),
        "Groceries": st.number_input("Groceries", min_value=0, value=10000),
        "Transportation": st.number_input("Transportation", min_value=0, value=5000),
        "Entertainment": st.number_input("Entertainment", min_value=0, value=5000),
    }
    return {"recurringExpenses": recurring_expenses}

def debt_page():
    st.header("💳 Debt Information")
    loans = []
    num_loans = st.number_input("Number of Loans", min_value=0, value=1)
    for i in range(num_loans):
        with st.expander(f"Loan {i+1}"):
            loan_type = st.text_input(f"Loan Type {i+1}", "Home Loan")
            outstanding_amount = st.number_input(f"Outstanding Amount {i+1}", min_value=0, value=1200000)
            monthly_emi = st.number_input(f"Monthly EMI {i+1}", min_value=0, value=15000)
            loans.append({"type": loan_type, "outstandingAmount": outstanding_amount, "monthlyEMI": monthly_emi})
    return {"loans": loans}

def budget_chart_page(user_data):
    st.header("📊 Budget Chart")
    analyser = analysisAgent(user_data)
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

def analytics_page(user_data):
    st.header("📈 Financial Analytics")
    analyser = analysisAgent(user_data)
    if st.button("Generate Analytics"): 
        analysis = analyser.mainModel2()
        st.json(analysis)

# Sidebar navigation
selected = option_menu(
    menu_title="Personal Finance Coach", 
    options=["Home", "User Info", "Income", "Expenses", "Debt", "Budget Chart", "Analytics"],
    icons=["house", "person", "wallet", "receipt", "credit-card", "bar-chart", "graph"],
    menu_icon="cast", 
    default_index=0,
    orientation="horizontal"
)

# Page routing
if selected == "Home":
    home_page()
elif selected == "User Info":
    user_data = user_info_page()
elif selected == "Income":
    user_data["incomeDetails"] = income_page()
elif selected == "Expenses":
    user_data["expenseDetails"] = expenses_page()
elif selected == "Debt":
    user_data["debtInformation"] = debt_page()
elif selected == "Budget Chart":
    budget_chart_page(user_data)
elif selected == "Analytics":
    analytics_page(user_data)


