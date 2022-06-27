# Pycache are evil, don't produce them
from multiprocessing.sharedctypes import Value
import re
import sys
from unicodedata import category
import attr

from matplotlib.pyplot import hist
sys.dont_write_bytecode = True

# universal import
from universal_imports import *

#------------------------------

import helper

#------------------------------

class account():

    #------------------------------

    def __init__(self):

        self.name = None
        self.value = None
        self.currency = None
        self.account_type = None
        self.rewards_type = None
        self.rewards = None

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

    def set_attributes(self, name, value, currency, account_type, rewards_type, rewards):

        """
        DESCRIPTION:
            Set the relevant attributes of an account to the desired value.
        """

        # the name of the account
        self.name = name

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
    # GETTING ATTRIBUTES FUNCTION GROUP

    def get_name(self):
        return self.name

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

    #------------------------------

    def export_data(self):
        """
        DESCRIPTION:
            1. A master function that calls both export_attributes and export_history in the correct order.
        """

        self.export_attributes()
        self.export_history()

    #------------------------------

    def export_attributes(self):
        """
        DESCRIPTION:
            1. Export the latest attributes of the account into a csv file with ONE line
            2. Each column header is the name of the attribute; the single entry is the value
        """

        # build the data structure for the Pandas dataframe
        data = {"Name":[self.name], "Value":[self.value], "Currency":[self.currency], "Account Type":[self.account_type],\
            "Rewards Type":[self.rewards_type], "Rewards":[self.rewards]}

        # create the Pandas dataframe
        attributes_df = pd.DataFrame(data)

        # export the Pandas dataframe as csv
        file_path = "Internal Data/" + self.name + "_attributes.csv"
        attributes_df.to_csv(file_path, index = False)

    #------------------------------

    def export_history(self):
        """
        DESCRIPTION:
            Export the account's history into a csv file for future pick-ups
        """

        # read the internal history as a Pandas dataframe
        history_df = pd.DataFrame(self.history)

        # export the dataframe as a csv
        file_path = "Internal Data/" + self.name + "_history.csv"
        history_df.to_csv(file_path, index = False)

    #------------------------------

    def load_data(self, account_name):
        """
        DESCRIPTION:
            A master function that calls load_attributes then load_history in the correct order.
            It also simplifies somewhat the function call
        """

        attributes_path = "Internal Data/" + account_name + "_attributes.csv"
        history_path = "Internal Data/" + account_name + "_history.csv"

        self.load_attributes(attributes_path)
        self.load_history(history_path)

    #------------------------------

    def load_attributes(self, file_path):
        """
        DESCRIPTION:
            Load the attributes of an account from a csv file
            ALWAYS LOAD ATTRIBUTES BEFORE LOADING HISTORY

        INPUT SIGNATURE:
            1. file_path (string): the path, including the name, of the file from the folder of this code
        """

        # read the csv file into a Pandas dataframe
        attributes_df = pd.read_csv(file_path)

        # write the attributes to the account
        self.set_attributes(attributes_df["Name"][0],\
            attributes_df["Value"][0],\
            attributes_df["Currency"][0],\
            attributes_df["Account Type"][0],\
            attributes_df["Rewards Type"][0],\
            attributes_df["Rewards"][0])

    #------------------------------

    def load_history(self, file_path):
        """
        DESCRIPTION:
            Load the history of the account from a csv file

        INPUT SIGNATURE:
            1. file_path (string): the path, including the name, of the file from the folder of this code
        """

        # read the csv file as a Pandas dataframe
        history_df = pd.read_csv(file_path)
        history_df['Date'] = pd.to_datetime(history_df['Date']) # convert to datetime for ease of use in the future

        # convert each column into a list and load into the internal data structure
        self.history["Action"] = history_df["Action"].to_list()
        self.history["Amount"] = history_df["Amount"].to_list()
        self.history["Date"] = history_df["Date"].to_list()
        self.history["Category"] = history_df["Category"].to_list()
        self.history["Rewards"] = history_df["Rewards"].to_list()