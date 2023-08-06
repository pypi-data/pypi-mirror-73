#! /usr/bin/env python3
import os
from os.path import getsize
import sys
import fire
import pprint
import time
import sqlite3


from .tools import Tools
from .config import Config
from .progress import ProgressPercentage

        
            
class TowerCrane():
    def __init__(self):
        """
        Make an instance of our cloud, DB, and tools.
        Which we then use in our commands.
        """
        self.project_name = "beer"  # os.path.basename(os.getcwd())
        self.project_dir = "/Users/taha/T/ds/projects/beer"  #os.getcwd() 
        
        self._config  = Config()
        self.s3 = self._config.get_cloud_client()
        self.db = self._config.get_db_client()
        self.tools = Tools(cloud_client=self.s3,db=self.db)
        
                
    def config(self):
        """
        starting config prompt for setting up the towercrane DB and Cloud
        """
        self._config.config_towercrane()
        
        
    def state(self):
        """
        state of Towercrane for current directory
        """
        self.tools.state(self.project_dir)
        
        
    def scan(self):
        """
        Scan the directory 
        """
        self.tools.scan(self.project_dir)
        
    def init(self):
        """
        Project Initialization: scans the directory and adds the files
        """
        self.tools.init_project(self.project_name,self.project_dir)
        self.tools.scan(self.project_dir)
        self.tools.add(self.project_name,self.project_dir)
        

    def upload(self):   
        """
        Uploading
        """
        queue_files = self.tools.load_queue(self.project_name,state="upload")
        self.tools.upload(self.project_name,self.project_dir,queue_files)
        self.db.change_state_file(queue_files,'uploaded')
        self.db.change_state_file(queue_files,'local_and_cloud')
        #TODO  check with aws if they're uploaded completely
        

    def remove(self):
        """
        Removing
        """
        queue_files = self.tools.load_queue(self.project_name,state="local_and_cloud")
        self.db.change_state_file(queue_files,'remove')
        queue_files = self.tools.load_queue(self.project_name,state="remove")
        self.tools.remove(queue_files,self.project_name,self.project_dir)
        self.db.change_state_file(queue_files,"removed")
        self.db.change_state_file(queue_files,'cloud')
        # TODO check if they're removed completely with a os.listdir()


    def download(self):
        """
        Downloading
        """
        
        queue_files = self.tools.load_queue(self.project_name,state="cloud")
        self.db.change_state_file(queue_files,'download')
        queue_files = self.tools.load_queue(self.project_name,state="download")
        self.tools.download(self.project_name,self.project_dir,queue_files)
        self.db.change_state_file(queue_files,'local_and_cloud')


 
if __name__ == "__main__":
    fire.Fire(TowerCrane)


    
    
