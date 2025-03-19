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
            elif Difference == 0:
                Status = "On Budget"
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
        return dataframe


    def mainModel2(self):
        output = self.giveSpendingAnalysis()
        if output.empty:
            return f"could not generate the output"
        else : 
            return output



