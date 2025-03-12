import json
import re
import ast
from model import LLM_model
import re
import pandas as pd
from Data_agent import analysisAgent

class spendAgent():
    def __init__(self,input,budgetInput):
        self.input = input
        self.budgetInput = budgetInput

    def giveSpendingAnalysis(self):

        

        prompt = f"""

            You are an expert in analysing budget and spending analysis , below in dictionary format I have given my overall spend in a month 
            {self.input}
            I want you to create a report based on the below allocated budget 
            {self.budgetInput}
            create a table in the below format keeping the below format 
            Category|Allocated (₹)|	Actual (₹)|	Surplus/Deficit (₹)|
            ** Instructions ** 
            1. Whatever money is left in income - overall spend is part of savings
            3. Keep it to point and do not give too much extra information 
        """
        
        model = LLM_model(prompt)
        response = model.llm_model()
        return response

    def mainModel2(self):
        output = self.giveSpendingAnalysis()
        if output:
            return output
        else : 
            return f"could not generate the output"



