# Pycache are evil, don't produce them
from multiprocessing.sharedctypes import Value
import sys
sys.dont_write_bytecode = True

# universal import
from universal_imports import *

#------------------------------

import helper

#------------------------------

class account():

    #------------------------------

    def __init__(self, value, currency, account_type, rewards_type, rewards):

        # real time value of the account
        self.value = value # start with an initial value

        # the currency of the account
        self.currency = currency # user input string

        # type of the account
        self.account_type = account_type # this value will be actively edited upon the creation of an account

        # rewards type of the account
        self.rewards_type = rewards_type # ("points", "miles", "cash")

        # total amount of rewards
        self.rewards = rewards

        #------------------------------
        # CRITICAL PART

        # a dictionary storing all transaction history of the account
        # history = {action:["Expense", "Income"], amount:["4516", "7"], date:["<datetime_object>"]}
        self.history = {"Action":[],\
            "Amount":[],\
            "Date":[],\
            "Category":[],\
            "Rewards":[]}

        # "Action" is type string
        # "Amount" is type float
        # "Date" is datetime object
        # "Category" is int (the whole program will define a few categories to follow)
        # "Rewards" is the rate of earning specific to a transaction

        # END OF CRITICAL PART
        #------------------------------

    #------------------------------
    # GETTING ATTRIBUTES FUNCTION GROUP

    def get_value(self):
        return self.value

    def get_currency(self):
        return self.currency

    def get_account_type(self):
        return self.account_type

    def get_rewards_type(self):
        return self.rewards_type

    def get_rewards(self):
        return self.rewards

    #------------------------------

    def transaction(self, action, amount, date, category, rewards):
        """
        DESCRIPTION:
            Record a transaction into the account history

        INPUT SIGNATURE:
            1. action: "string" (E, I, L, C) stand for Expense, Income, Lend, Collect
            2. amount: float
            3. date: "string" ("2022-27-06")
            4. category: int (1, 2, 3, 4, etc.)
            5. rewards: float (2, 0.02, etc.)
        """

        # convert date variable to datetime object
        date = helper.datetime_convert(date)

        self.history["Action"].append(action)
        self.history["Amount"].append(amount)
        self.history["Date"].append(date),
        self.history["Category"].append(category)
        self.history["Rewards"].append(rewards)

    #------------------------------

    