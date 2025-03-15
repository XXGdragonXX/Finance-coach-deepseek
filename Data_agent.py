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

            *   Rent
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
            "Rent": XXXX,
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

    def extract(self,response):
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

