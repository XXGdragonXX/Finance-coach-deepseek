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

            {payload}

            ### **Tasks**

            1️⃣ **Budget Allocation (JSON):**

            Based on the user's monthly income of {payload["incomeDetails"]["monthlyIncome"]}, provide a recommended monthly budget allocation in JSON format.  Consider the user's recurring expenses, debt information, financial goals, and savings details.  Ensure the total allocation does not exceed the user's monthly income.  Use the following categories:

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
            "Rent/Mortgage": 1000,
            "Utilities": 200,
            "Groceries": 300,
            "Transportation": 150,
            "Entertainment": 100,
            "Savings": 500,
            "Debt Repayment": 200,
            "Healthcare": 50,
            "Miscellaneous": 50
            }}
            ```

            2️⃣ **Expense Tracking and Alerts (Table):**

            Assume the user has provided the following actual expenses for the month (these are example values; replace with actual user input if available in the payload - if not assume these):

            *   Rent/Mortgage: 1050
            *   Utilities: 250
            *   Groceries: 320
            *   Transportation: 180
            *   Entertainment: 120
            *   Savings: 450
            *   Debt Repayment: 220
            *   Healthcare: 60
            *   Miscellaneous: 70


            Create a table comparing the budgeted amounts (from the JSON above) to the actual expenses.  Include the difference and an alert indicating whether the user is within budget or exceeding the budget for each category.

            **Table Format:**

            | Category           | Budget | Spent | Difference | Alert           |
            |--------------------|--------|-------|------------|-----------------|
            | Rent/Mortgage     | 1000   | 1050  | -50        | Exceeds Budget |
            | Utilities          | 200    | 250   | -50        | Exceeds Budget |
            | Groceries          | 300    | 320   | -20        | Exceeds Budget |
            | Transportation     | 150    | 180   | -30        | Exceeds Budget |
            | Entertainment      | 100    | 120   | -20        | Exceeds Budget |
            | Savings            | 500    | 450   | 50         | Within Budget   |
            | Debt Repayment     | 200    | 220   | -20        | Exceeds Budget |
            | Healthcare         | 50     | 60    | -10        | Exceeds Budget |
            | Miscellaneous      | 50     | 70    | -20        | Exceeds Budget |

            **DO NOT** provide any extra explanation—only return the requested JSON and table.
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


    def extractTableAndDictionary(self,response):
        # Extract the dictionary
        dict_pattern = r"\{[^{}]+\}"
        dict_match = re.search(dict_pattern, response)
        if dict_match:
            budgetAllocation = eval(dict_match.group())
        else:
            budgetAllocation = None

        # Extract the table
        table_pattern = r"\|.*\|\n\|.*\|\n(\|.*\|\n)*"
        table_match = re.search(table_pattern, response)
        if table_match:
            table_text = table_match.group()
            # Convert table to DataFrame
            rows = [row.strip().split("|")[1:-1] for row in table_text.strip().split("\n")]
            headers = [header.strip() for header in rows[0]]
            data = [[item.strip() for item in row] for row in rows[2:]]
            expenseTracking = pd.DataFrame(data, columns=headers)
        else:
            expenseTracking = None

        return budgetAllocation , expenseTracking



    def mainModel(self):
        output = self.agentBudgetingAndExpenseTracking(self.input)
        budget,tracker = self.extractTableAndDictionary(output)
        if budget:
            print(budget)
        else : 
            print("couldnt extract the budget")
        if not tracker.empty:
            print(tracker.head())
        else:
            print("could not geenrate the tracker.....")
        return budget , tracker

    def mainModel2(self):
        output = self.agentAnalyticsAndReporting(self.input)
        analysis = self.extractTableAndDictionary(output)
        if analysis:
            print(analysis)

        return analysis
        


# if __name__ == '__main__':

#     agent = analysisAgent()

#     agent.testModel()
