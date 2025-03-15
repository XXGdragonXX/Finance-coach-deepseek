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
        del self.budgetInput['Savings']
        prompt = f"""
                You are an expert in generating detailed financial reports. Below is the financial data provided:

                1. Savings determined by the model: {savingsbyLlm}
                2. Actual savings of the user: {actualSaving}
                3. Decided budget: {self.budgetInput}
                4. Spending by the person: {self.input}

                Based on the information above, create a table with the following schema:

                | Expense| Budgeted Amount | Actual Spending |Difference|Status|Variance (%)|

                **Instructions:**
                1. Only provide the table and strictly adhere to the schema.
                2. For each expense category in `self.input`, calculate whether the user is underspending or overspending compared to the budget (`self.budgetInput`).
                3. Ensure the table is clear, concise, and easy to read.
                4. Do not include any additional explanations or text outside the table.
        """
        
        model = LLM_model(prompt)
        response = model.llm_model()
        return response

        # return f"""
        #         saving by llm = {savingsbyLlm}
        #         total income of the user  = {totalIncome}
        #         actualSaving = {actualSaving}
        
        # """

    def mainModel2(self):
        output = self.giveSpendingAnalysis()
        if output:
            return output
        else : 
            return f"could not generate the output"



