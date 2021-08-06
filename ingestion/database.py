import urllib.parse
from pymongo import MongoClient

class Database:
    
    CLIENT = None
    DATABASE = None
    
    @staticmethod
    def get_connection_string(options):
        hostname = urllib.parse.quote_plus(options['DB_HOST'])
        username = urllib.parse.quote_plus(options['DB_USER'])
        password = urllib.parse.quote_plus(options['DB_PASS'])
        port = int(options['DB_PORT'])
        return "mongodb://%s:%s@%s:%d/?authSource=admin" % (username, password, hostname, port)
    
    @classmethod
    def initialize(cls, options):
        uri = Database.get_connection_string(options)
        cls.CLIENT = MongoClient(uri)
        if cls.CLIENT:
            print("OK")
        return cls.CLIENT
        
    @classmethod
    def use(cls, database):
        cls.DATABASE = cls.CLIENT[database]
        if cls.DATABASE:
            print("OK")
        return cls.DATABASE
        
    @classmethod
    def insert_many(cls, collection, data):
        if cls.DATABASE:
            print("Inserting data into %s collection." % (collection,))
            return cls.DATABASE[collection].insert_many(data)
        else:
            print("No database currently loaded.")
            
    @classmethod
    def insert_one(cls, collection, record):
        if cls.DATABASE:
            print("Inserting record into %s collection." % (collection,))
            return cls.DATABASE[collection].insert_one(record)
        else:
            print("No database currently loaded.")
        
    @classmethod
    def find(cls, collection, query):
        if cls.DATABASE:
            print("Querying any %s collection: '%s'" % (collection, query))
            return cls.DATABASE[collection].find(query)
        else:
            print("No database currently loaded.")
    
    @classmethod
    def find_one(cls, collection, query):
        if cls.DATABASE:
            print("Querying one from %s collection: '%s'" % (collection, query))
            return cls.DATABASE[collection].find_one(query)
        else:
            print("No database currently loaded.")