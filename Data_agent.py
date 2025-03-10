import json
import re
import ast
from model import LLM_model
import re
import pandas as pd



class analysisAgent():
    def __init__(self,input):
        self.input = input
        
    def agentBudgetingAndExpenseTracking(self, userInput):
        payload = userInput
        prompt = f"""
            You are an AI financial assistant helping a user manage their finances.
            Below are the details of their financial situation in JSON format:

            monthly income = {payload["incomeDetails"]["monthlyIncome"]}
            debt information = {payload['debtInformation']}
            financial goals = {payload['financialGoals']}
            investment preferences = {payload['investmentPreferences']}
            savings details = {payload['savingsDetails']}


            ### **Tasks**

            1️⃣ **Budget Allocation (JSON):**

            Based on the user's Information mentioned above , provide a recommended monthly budget allocation in JSON format.  Consider all the users information given above.  Ensure the total allocation does not exceed the user's monthly income.  Use the following categories:

            *   Rent/Mortgage
            *   Utilities (Electricity, Water, Gas, Internet, Phone)
            *   Groceries
            *   Transportation (Car Payment, Gas/Public Transit, Maintenance)
            *   Entertainment
            *   Savings (Emergency Fund, Goals)
            *   Debt Repayment (Loans, Credit Cards)
            *   Healthcare (Insurance, Medical Expenses)
            *   Miscellaneous (Personal Care, Clothing, etc.)

            Example JSON format:

            ```json
            {{
            "Rent/Mortgage": XXXX,
            "Utilities": XXXX,
            "Groceries": XXXX,
            "Transportation": XXXX,
            "Entertainment": XXXX,
            "Savings": XXXX,
            "Debt Repayment": XXXX,
            "Healthcare": XXXX,
            "Miscellaneous": XXXX
            }}
            ```
            **DO NOT** provide any extra explanation—only return the requested JSON .
        """
        # Call the model
        model = LLM_model(prompt)
        response = model.llm_model()
        return response

    def agentAnalyticsAndReporting(self, userInput):

        payload = userInput
        totalSalary = payload['incomeDetails']['monthlyIncome']
        recurringExpenses = payload['expenseDetails']['recurringExpenses']
        totalExpenses = sum(recurringExpenses.values())
        savings = payload['savingsDetails']['currentSavings']
        debtLoans = payload['debtInformation']['loans']
        creditCards = payload['debtInformation']['creditCards']

        # Debt Details
        totalLoanOutstanding = sum(loan['outstandingAmount'] for loan in debtLoans)
        totalCreditOutstanding = sum(card['outstandingBalance'] for card in creditCards)
        totalDebt = totalLoanOutstanding + totalCreditOutstanding

        # Key Financial Ratios
        savingsRate = round((savings / totalSalary) * 100, 2)
        debtToIncomeRatio = round((totalDebt / totalSalary) * 100, 2)
        expenseToIncomeRatio = round((totalExpenses / totalSalary) * 100, 2)

        # Constructing the prompt for analytics
        prompt = f"""
        You are an AI financial analytics assistant. Analyze the user's financial data and provide insights.
        
        ### **Financial Overview**
        - **Total Income:** ₹{totalSalary}
        - **Total Expenses:** ₹{totalExpenses}
        - **Current Savings:** ₹{savings}
        - **Total Debt (Loans + Credit Cards):** ₹{totalDebt}

        ### **Key Ratios**
        - **Savings Rate:** {savingsRate}%
        - **Debt-to-Income Ratio:** {debtToIncomeRatio}%
        - **Expense-to-Income Ratio:** {expenseToIncomeRatio}%

        ### **Tasks**
        1️⃣ **Financial Summary**  
        - Generate a clear summary of the user's financial health.  
        - Identify if the user is overspending or managing finances well.  

        2️⃣ **Insights & Trends**  
        - Detect patterns (e.g., increasing expenses, low savings, high debt).  
        - Suggest possible improvements in financial habits.  

        3️⃣ **Monthly & Yearly Report (JSON Format)**  
        - Provide a structured report of expenses, savings, and debt for the past month and year.  

        **Response Format:**  
        ```json
        {{
            "summary": "Your finances are stable, but you are spending 50% of your income on rent.",
            "recommendations": [
                "Reduce entertainment expenses by 10% to save more.",
                "Increase investments in Mutual Funds."
            ],
            "monthly_report": {{
                "income": {totalSalary},
                "expenses": {totalExpenses},
                "savings": {savings},
                "debt": {totalDebt}
            }},
            "yearly_projection": {{
                "expected_savings": {savings + (totalSalary - totalExpenses) * 12},
                "expected_debt_reduction": {totalDebt - (sum(loan['monthlyEMI'] for loan in debtLoans) * 12)}
            }}
        }}
        ```
        **Only return the structured JSON response. No additional explanation.**
        """

        # Call the model
        model = LLM_model(prompt)
        response = model.llm_model()

        return response


    def extract(self,response):
        # Extract the dictionary
        dict_pattern = r"\{[^{}]+\}"
        dict_match = re.search(dict_pattern, response)
        if dict_match:
            dict_val = eval(dict_match.group())
        else:
            dict_val = None
        return dict_val 

    def mainModel(self):
        output = self.agentBudgetingAndExpenseTracking(self.input)
        budget = self.extract(output)
        if budget:
            print(budget)
        else : 
            print("couldnt extract the budget")
        return budget 

    def mainModel2(self):
        output = self.agentAnalyticsAndReporting(self.input)
        analysis = self.extract(output)
        if analysis:
            print(analysis)

        return analysis
        


# if __name__ == '__main__':

#     agent = analysisAgent()

#     agent.testModel()
