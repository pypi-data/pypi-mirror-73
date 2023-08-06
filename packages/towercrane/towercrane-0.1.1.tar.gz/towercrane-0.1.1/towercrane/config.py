from .cloud import S3
from .db import DB
import time
bucket_name =  "towercrane-projects"


class Config():
    def __init__(self):
        self.db = DB()
        self.db.setupDB()
        self.mother_config = self.db.get_mother_config()
        self.set_mother_config = self.db.set_mother_config
        

    def config_towercrane(self):
        """
        Pormpt for setting up TowerCrane
        
        It asks for your cloud of choice
        and if you have already done the authentication.
        ... Other Questions To Be Added
        """
        
        cloudtype = input("what is your choice for cloud storage? aws or gcloud") or "aws"
        print(cloudtype)
        self.set_mother_config("cloudtype",cloudtype)
        auth_done = input("Have you authenticated your aws yourself? (y/n)") or "n"
        if not auth_done == "y":
            print("Here is a link to how you shoud do it.")
            
        
        
    """
    Reading Config Table 
    and getting cloud and DB clients based on the configs.
    
    get_cloud_client:  returns either the s3 or gcloud
    get_db_client:     returns db client
    """
    def get_cloud_client(self):
        # first read from DB and see what cloud we should be using 
        cloudtype = self.mother_config["cloudtype"] 
        if cloudtype == "aws" :
            cloud_client = S3()
            cloud_projects = cloud_client.list_cloud_projects()
            if bucket_name not in cloud_projects:
                print("There is no towercrane-projects bucket, creating one ...")
                cloud_client.create_cloud_project(bucket_name)
                print("created: ",bucket_name)           
            return cloud_client
            
        elif cloudtype == "gcloud" :
            pass
            # cloud_client = Gcloud()
            # return cloud_client
    
    
    def get_db_client(self):
        # in case you need to do any testing with tables in DB do it here.
        return self.db

    
    
    
    

        
    
 