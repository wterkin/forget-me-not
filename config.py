#!/usr/bin/python
# -*- coding: utf-8 -*-

CONFIG_FILE_PATH = "~/.config/forget-me-not/" 
CONFIG_FILE_NAME = "forget-me-not.json"


class Configuration(object):
    def __init__(self):
        self.config = dict()
        if not self._check_config_folder():
            
            self._create_config_folder()
        
    def _check_config_folder():
        pass
    
    def _create_config_folder():
        pass
    
    def store_value(self, pkey, pvalue):
        pass
    
    def restore_value(self, pkey):
        pass
        
    def write_config():
        pass
    
    def read_config():
        pass
    
    
