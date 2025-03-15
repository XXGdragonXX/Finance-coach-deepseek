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
        logging.info(f"This is the budget we are getting from the llm geenrated using the intial user response {self.budgetInput})
        # savingsbyLlm = self.budgetInput['Savings']
        # totalIncome = sum(self.sum(budgetInput.values()))
        # prompt = f"""

        #     The savings determined by the model is {savingsbyLlm} . 
        #     Below the spendings done by the user has been given in dictionary format 
        #     {self.input}
        #     Do the summation of all the spendings


        # """
        
        # model = LLM_model(prompt)
        # response = model.llm_model()
        # return response
        return "I am still testing this ..."

    def mainModel2(self):
        output = self.giveSpendingAnalysis()
        if output:
            return output
        else : 
            return f"could not generate the output"



