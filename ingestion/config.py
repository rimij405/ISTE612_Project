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

class Config:
    
    ENV = None
    ENV_PATH = None        
        
    @classmethod
    def load_env(cls, filename):
        return dotenv_values(cls.ENV_PATH + filename)
    
    @classmethod
    def initialize(cls, envPath):
        cls.ENV_PATH = envPath
        cls.ENV = {
            **Config.load_env(".config"),
            **Config.load_env(".secrets"),
            **os.environ
        }
        cls.set('LOOKUP_SHEETS', cls.get('LOOKUP_SHEETS').split(','))
        
    @classmethod
    def get(cls, setting):
        return cls.ENV[setting]
    
    @classmethod
    def set(cls, setting, value):
        cls.ENV[setting] = value
