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

        BudgetbyLlm = self.budgetInput

        
        # model = LLM_model(prompt)
        # response = model.llm_model()
        # return response
        return BudgetbyLlm

    def mainModel2(self):
        output = self.giveSpendingAnalysis()
        if output:
            return output
        else : 
            return f"could not generate the output"



