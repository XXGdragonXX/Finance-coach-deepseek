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
