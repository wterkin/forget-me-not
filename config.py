#!/usr/bin/python
# -*- coding: utf-8 -*-

from pathlib import Path

CONFIG_FOLDER = ".config/forget-me-not/" 
CONFIG_FILE_NAME = "forget-me-not.json"


class Configuration(object):
    def __init__(self):
        self.config = dict()
        if not self._check_config_folder():
            
            self._create_config_folder()
        
        
    def _check_config_folder(self):
        config_folder_path = Path(Path.home() / CONFIG_FOLDER)
        return config_folder_path.exists()
     
    def _create_config_folder(self):
        config_folder_path = Path(Path.home() / CONFIG_FOLDER)
        config_folder_path.mkdir()
    
    def store_value(self, pkey, pvalue):
        pass
    
    def restore_value(self, pkey):
        pass
        
    def write_config(self):
        pass
    
    def read_config(self):
        pass
    
    
