from .cloud import S3
from .db import DB
import time
import sys
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
        
        cloudtype = input("what is your choice for cloud storage? aws or gcloud: ") or "aws"
        self.set_mother_config("cloudtype",cloudtype)
        
        
        auth_done = input("Have you authenticated your aws yourself? (y/n): ") or "n"
        if auth_done in ["n","N","no","NO"] :
            print("Here is a link to a simple guide for configuring your aws: \n\nhttps://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config")
        elif auth_done in ["y","Y","yes","YES"] :
            print(f" Checking if your {cloudtype} is Authenticated properly ...")
            # self.s3_client.list_buckets() TODO
            
        
        
    """
    Reading Config Table 
    and getting cloud and DB clients based on the configs.
    
    get_cloud_client:  returns either the s3 or gcloud
    get_db_client:     returns db client
    """
    def get_cloud_client(self):
        # first read from DB and see what cloud to use
        cloudtype = self.mother_config["cloudtype"] 
        if cloudtype == "notset" :
            sys.exit('Cloud is not configured in towercrane.\nplease use "towercrane config" first. ')
        
        elif cloudtype == "aws" :
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
        # we can run our db test here
        return self.db

    
    
    
    

        
    
 