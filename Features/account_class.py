# Pycache are evil, don't produce them
from multiprocessing.sharedctypes import Value
import re
import sys
from unicodedata import category
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
            3. date: "string" ("2022-06-27")
            4. category: int (1, 2, 3, 4, etc.)
            5. rewards: float (2, 0.02, etc.)
        """

        # convert date variable to datetime object
        date = helper.datetime_convert(date)

        # record the transaction into history
        self.history["Action"].append(action)
        self.history["Amount"].append(amount)
        self.history["Date"].append(date),
        self.history["Category"].append(category)
        self.history["Rewards"].append(rewards)

        # update real time attributes
        if (action == "E") or (action == "L"):
            self.value -= amount
            self.rewards += amount * rewards
        else:
            self.value += amount
            self.rewards -= amount * rewards

    #------------------------------

    def redeem_rewards(self, amount, rate, date):
        """
        DESCRIPTION:
            Redeem the rewards within self.rewards and transfer it into the main account

        INPUT SIGNATURE:
            1. amount (float): the amount of rewards to be redeem
            2. rate (float): amount of the currency earned from a unit of reward; this should be ONE for cash reward
                and 0.01 for 1 cent per point
            3. date (string): "2022-06-27"
        """

        # update the new amount of remaining rewards
        self.rewards -= amount
        
        # calculate the real value of the redeemed rewards
        amount_redeemed = amount * rate

        # add the redeemed rewards as a transaction
        self.transaction(action = "I",\
            amount = amount_redeemed,\
            date = date,\
            category = 0,\
            rewards = 0)