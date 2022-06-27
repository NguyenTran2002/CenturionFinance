# Pycache are evil, don't produce them
from multiprocessing.sharedctypes import Value
import sys
sys.dont_write_bytecode = True

# universal import
from universal_imports import *

#------------------------------
# TO BE IMPLEMENTED

def datetime_convert(target_string):
    """
    DESCRIPTION
        Convert a simple YYYY-MM-DD to a datetime object
    """

    return pd.to_datetime(target_string)