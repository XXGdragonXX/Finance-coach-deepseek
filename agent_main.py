import json
import re
import ast
from model import LLM_model
import re
import pandas as pd



class analysisAgent():
    def __init__(self):
        pass
        

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
                "entertainment": 3000,
                "other": 2000
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

    def agentBudgetingAndExpenseTracking(self):
        payload = self.testPayload()
        recurringExpenses = payload['expenseDetails']['recurringExpenses']
        totalSalary = payload['incomeDetails']['monthlyIncome']
        location = payload['user']['location']
        prompt = f"""
        I want to manage my finances effectively. Here are my details:
        total salary = {totalSalary}
        recurring exoenses = {recurringExpenses}
        location = {location}
        Based on this information:
        Suggest an ideal budget allocation for each expense category in dictionary format.
        Track my expenses and alert me if I exceed my budget in any category in table format.
        Do not give any extra information and strictly only provide dictionary and table "
        """

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



    def testModel(self):

        output = self.agentBudgetingAndExpenseTracking()
        budget,tracker = self.extractTableAndDictionary(output)
        if budget:
            print(budget)
        else : 
            print("couldnt extract the budget")

        if not tracker.empty:
            print(tracker.head())
        else:
            print("could not geenrate the tracker.....")
        


if __name__ == '__main__':

    agent = analysisAgent()

    agent.testModel()
