import json
import re
import ast
from model import LLM_model
import re
import pandas as pd



class analysisAgent():
    def __init__(self,input):
        self.input = input
        

    def testPayload(self):
        print("Giving the Test payload to the agent weeeeeee")
        return {
            "user": {
                "name": "John Doe",
                "age": 30,
                "location": "Mumbai, India"
            },
            "incomeDetails": {
                "monthlyIncome": 80000,
                "incomeSources": [
                {
                    "type": "Salary",
                    "amount": 70000
                },
                {
                    "type": "Freelancing",
                    "amount": 10000
                }
                ]
            },
            "expenseDetails": {
                "recurringExpenses": {
                "rent": 20000,
                "utilities": 5000,
                "groceries": 10000,
                "transportation": 5000,
                "entertainment": 5000,
                "other": 1000
                }
            },
            "debtInformation": {
                "loans": [
                {
                    "type": "Home Loan",
                    "outstandingAmount": 1200000,
                    "monthlyEMI": 15000
                }
                ],
                "creditCards": [
                {
                    "bank": "ABC Bank",
                    "outstandingBalance": 20000,
                    "minimumDue": 2000
                }
                ]
            },
            "financialGoals": {
                "shortTerm": [
                {
                    "goal": "Vacation",
                    "amount": 50000,
                    "timeFrame": "6 months"
                }
                ],
                "longTerm": [
                {
                    "goal": "Retirement Fund",
                    "amount": 5000000,
                    "timeFrame": "20 years"
                }
                ]
            },
            "investmentPreferences": {
                "riskTolerance": "Moderate",
                "preferredInvestmentTypes": ["Mutual Funds", "Stocks"]
            },
            "savingsDetails": {
                "currentSavings": 200000,
                "preferredSavingMethods": ["Fixed Deposit", "Recurring Deposit"]
            },
            "taxInformation": {
                "taxBracket": "20%",
                "taxSavingInvestments": ["PPF", "ELSS"]
            },
            "creditScore": 750
            }

    def agentBudgetingAndExpenseTracking(self, userInput):
        payload = userInput
        
        # Extracting relevant financial details
        totalSalary = payload['incomeDetails']['monthlyIncome']
        recurringExpenses = payload['expenseDetails']['recurringExpenses']
        location = payload['user']['location']
        loans = payload['debtInformation']['loans']
        creditCards = payload['debtInformation']['creditCards']
        
        # Constructing the refined prompt
        prompt = f"""
        You are an AI financial assistant helping a user manage their finances.
        Below are the details of their financial situation:
        
        - **Total Salary:** ₹{totalSalary}
        - **Recurring Expenses:** {recurringExpenses}
        - **Location:** {location}
        - **Loans:** {loans}
        - **Credit Cards:** {creditCards}
        - **Minimum Recommended Savings:** 20% of ₹{totalSalary} = ₹{totalSalary * 0.2}
        
        ### **Tasks**
        1️⃣ **Budget Allocation:**  
        - Suggest an **ideal budget allocation** for each category (in JSON format).  
        - Ensure that the total allocation does not exceed the user's total salary.  
        - Include categories like Rent, Utilities, Groceries, Transportation, Entertainment, Savings, Debt Repayment, and Miscellaneous.  
        
        2️⃣ **Expense Tracking Alert:**  
        - Compare actual **spent** values against budgeted amounts and flag categories where the user has exceeded the budget.  
        - Present the data in a **table format** with columns:  
            **|Category | Budget | Spent | Difference | Alert|**  
        - The **Alert** column should contain:
            - `"Within Budget"` if within limits
            - `"Exceeds Budget"` if overspending is detected

        ### **Response Format**
        **Budget Allocation (JSON Object):**
        ```json
        {{
        "Rent": XX,
        "Utilities": XX,
        "Groceries": XX,
        "Transportation": XX,
        "Entertainment": XX,
        "Savings": XX,
        "Debt Repayment": XX,
        "Miscellaneous": XX
        }}
        ```
        
        **Expense Tracking Table:**
        ```
        | Category       | Budget  | Spent  | Difference | Alert          |
        |---------------|---------|--------|-----------|---------------|
        | Rent         | XX      | XX     | ±XX       | Within Budget / Exceeds Budget |
        ```
        
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
