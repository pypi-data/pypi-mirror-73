import logging
import os
import boto3
from botocore.exceptions import ClientError
from .progress import ProgressPercentage
from os.path import getsize

class S3():
    """
    Cloud Tools:
    These are the tools for working with cloud    
    """
    
    def __init__(self,region="us-east-1"):
        # self.aws_auth()
        self.region = region
        self.s3_client = boto3.client('s3', region_name=region)
        self.s3_res = boto3.resource('s3')
        # if not self.check_client(self.s3_client):
        #     print("Can not connect to AWS S3 client. Token might be expired.")
            # def aws_auth(self):
            #     os.system("cat aws.cred > ~/.aws/credentials")

    # def check_client(self,client):
    #     print(hasattr(client,'__class__'))
    #     if hasattr(client,'__class__'):
    #         return True
    #     else:
    #         return False
        

    def list_buckets(self):
        response = self.s3_client.list_buckets()
        buckets = response['Buckets']
        return buckets

    def list_objects(self, bucket_name):
        mybucket = self.s3_res.Bucket(bucket_name)
        all_objects = []
        for object_summary in mybucket.objects.all() :
            all_objects.append(object_summary.key)
        return all_objects
        
        
    def get_public_url(self,bucket_name,object_name):
        response = self.s3_client.get_bucket_location(Bucket=bucket_name)
        # bucket_location = response['LocationConstraint'] if response['LocationConstraint'] else "us-east-1"
        object_url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}" # for now i don't care about the other regions. TODO
        return object_url
        
    def create_bucket(self,bucket_name):
        try:
            if self.region is None or self.region == "us-east-1":
                self.s3_res.create_bucket(Bucket=bucket_name)
            else:
                location = {'LocationConstraint': self.region}
                self.s3_res.create_bucket(Bucket=bucket_name,
                                        CreateBucketConfiguration=location)
        except ClientError as e:
            logging.error(e)
            return False
        return True
    
    
    def upload_file(self,bucket_name,abspath,file_name,object_name):
        try:
            with open(abspath, "rb") as f:
                response = self.s3_client.upload_fileobj(f,bucket_name, object_name,
                                                         Callback=ProgressPercentage(file_name+".zip",size=float(getsize(abspath)))
                                                            )
                # self.s3_client.put_object_acl(Bucket=bucket_name,Key=object_name)
                # bucket.Acl().put(ACL='public-read')
                # obj.Acl().put(ACL='public-read')
            
                return True, response
            
        except ClientError as e:
            logging.error(e)
            return False
        
    
    
    def download_file(self,bucket_name,object_name,project_dir):
        try:
            file_size = self.s3_client.head_object(
                                            Bucket=bucket_name,
                                            Key=object_name
                                            )['ContentLength']
        
            with open(os.path.join(project_dir,object_name), 'wb') as f:
                response = self.s3_client.download_fileobj(bucket_name, object_name, f,
                                                           Callback=ProgressPercentage(object_name,float(file_size))
                                                           )
                                                          
        except ClientError as e:
            logging.error(e)
            return False
        return True
    
    

    def list_cloud_projects(self):
        buckets_names = []
        buckets = self.list_buckets()
        for bucket in buckets :
            buckets_names.append(bucket["Name"])
        return buckets_names
    
    def create_cloud_project(self,project_name):
        bucket_name = project_name
        self.create_bucket(bucket_name)


