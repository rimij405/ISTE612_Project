# Import system packages.
import sys, os
import urllib.parse
import datetime
import json

# Import data processing tools.
import pandas as pd

# Import MongoDB related packages.
from pymongo import MongoClient
from dotenv import dotenv_values

# Application related libraries.
from config import Config
from database import Database

# Load the environment variables.
Config.initialize('./../.env')

# Initialize the database and make connection.
Database.initialize(Config.ENV)
Database.use('region')
results = Database.find('zipcodes', {})

# Load the DataFrame results.
df = pd.DataFrame(list(results))

# Display the DataFrame.
print(df)