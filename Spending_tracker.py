import json
import re
import ast
from model import LLM_model
import re
import pandas as pd
from Data_agent import analysisAgent
import logging

class spendAgent():
    def __init__(self,input,budgetInput):
        self.input = input
        self.budgetInput = budgetInput

    def giveSpendingAnalysis(self):
        logging.info(f"This is the budget we are getting from the llm geenrated using the intial user response {self.budgetInput}")
        savingsbyLlm = self.budgetInput['Savings']
        totalIncome = sum(self.budgetInput.values())
        actualSaving = totalIncome - sum(self.input.values())
        # dataframe = pd.DataFrame(columns=['Expense','Budget','Spending','Difference','Status','Variance'])
        tracker_list = []
        for key in self.input.keys():
            expense = key
            Budget = self.budgetInput[key]
            Spending = self.input[key]
            Difference = Spending - Budget
            if Difference < 0:
                Status = "Underspending"
            elif Difference > 0:
                Status = "Overspending"
            variance = (Difference/Budget)*100
            trackerDict = {
                "Expense":expense,
                "Budget":Budget,
                "Spending":Spending,
                "Difference":Difference,
                "Status":Status,
                "Variance":variance
            }
            tracker_list.append(trackerDict)
        dataframe = pd.DataFrame(tracker_list)
        logging.info(dataframe.head())    
            
        prompt = f"""
                You are an expert in generating detailed financial reports. Below is the financial data provided:

                1. Savings determined by the model: {savingsbyLlm}
                2. Actual savings of the user: {actualSaving}
                3. Decided budget: {self.budgetInput} (a dictionary where keys are expense categories and values are budgeted amounts)
                4. Spending by the person: {self.input} (a dictionary where keys are expense categories and values are actual spending amounts)

                Based on the information above, create a table with the following schema:

                | Expense         | Budgeted Amount | Actual Spending | Difference | Status           | Variance (%) |
                |-----------------|-----------------|-----------------|------------|------------------|--------------|

                **Instructions:**
                1. Only provide the table and strictly adhere to the schema.
                2. For each expense category in `self.input`, compare the actual spending with the corresponding budgeted amount in `self.budgetInput`.
                3. Calculate the `Difference` as `Actual Spending - Budgeted Amount`.
                4. Determine the `Status` as follows:
                - If `Difference` is negative, label it as "Underspending".
                - If `Difference` is positive, label it as "Overspending".
                - If `Difference` is zero, label it as "On Budget".
                5. Calculate the `Variance (%)` as `(Difference / Budgeted Amount) * 100`.
                6. Ensure the table is clear, concise, and easy to read.
                7. Do not include any additional explanations or text outside the table.
        """
        return dataframe


    def mainModel2(self):
        output = self.giveSpendingAnalysis()
        if output:
            return output
        else : 
            return f"could not generate the output"



