# config.py
# Author: Ian Effendi
# 
# Application configuration settings and environment variables.

import os
from bunch import Bunch
from dynaconf import Dynaconf
from dotenv import dotenv_values

# Dynaconf reads from the *.toml configuration files

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    merge_enabled = True,
    settings_files=['settings.toml', '.secrets.toml'],    
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load this files in the order.

# Environment reads from the *.env files.
class Configuration:
    """Load in *.env files."""
    
    def __init__(self, envPath):
        self.envPath = envPath
        self.env = Bunch(
            **Configuration.load_env("config.env"),
            **Configuration.load_env(".secrets.env"),
            **os.environ)
        
    def load_env(self, filename):
        return dotenv_values(self.envPath + filename)