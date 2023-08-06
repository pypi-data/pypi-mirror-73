import random
import string
import os
from os.path import getsize
import shutil
import errno
import time
import zipfile
from tabulate import tabulate

bucket_name =  "paperclip-projects"

"""
Config tools 

id_generator:  for id generation 
read_config:   reading config file
write_config:  writing config file
"""
def id_generator(length):
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def read_config(project_dir):
    PaperclipConfig = {"project_name":"",
                       "projectkey":"",
                       "publicurl":""}
    with open(os.path.join(project_dir,"paperclip"),"r") as f:
        for line in f.readlines():
            configKey = line.strip().split(":")[0]
            configValue = line.strip().split(":")[1]
            PaperclipConfig[configKey] = configValue
    return PaperclipConfig
    
def write_config(project_dir,PaperclipConfig):
    with open(os.path.join(project_dir,"paperclip"),"w") as f:
            f.write("project_name:"+PaperclipConfig["project_name"]+"\n"+
                    "projectkey:"+PaperclipConfig["projectkey"]+"\n"+
                    "publicurl:"+PaperclipConfig["publicurl"]
                    )








class Tools():
    def __init__(self,cloud_type="aws",cloud_client=None,db=None):
        self.cloud_type = cloud_type
        self.cloud_client = cloud_client
        self.db = db
        
    """
    Local Tools:
    These are the tools for project initialization, scanning files and adding them to DB.
    
    init_project:   initializing project config, and storage in the cloud.
    scan:           scanning local files               
    add:            adding files to DB with local state
    """
    def init_project(self,project_name,project_dir):
        """
        checks if it can find a paperclip file. 
        if not, creates one and creates the project too.
        """
        projectkey = id_generator(10)
        if "paperclip" not in os.listdir(project_dir):
            print(f'Initializing project:"{project_name}" with projectkey: "{projectkey}" ')
            self.PaperclipConfig = {"project_name":project_name,
                                    "projectkey":projectkey,
                                    "publicurl":""
                                    }
            write_config(project_dir,self.PaperclipConfig)
            project_insert_report = self.db.create_project(project_name,project_dir,projectkey)
            print(project_insert_report)
        
        elif "paperclip" in os.listdir(project_dir):
           self.PaperclipConfig = read_config(project_dir)
           print(f'project:"{self.PaperclipConfig["project_name"]}" with projectkey: "{self.PaperclipConfig["projectkey"]}" Already Exists')
           

        
        
    def scan(self,project_dir):
        """
        Scans the local files and looks for one of the file dtypes.
        And then adds what it finds to a dictionary.
        """
        ftypes = [".csv", ".data", ".xlsx"]
        print("Scanning directory : ",project_dir)
        print("Searching for : ",ftypes)
        self.localfiles = {}
        for dirpath, dirnames, filenames in os.walk(project_dir, topdown=True):
            for filename in filenames:
                for ftype in ftypes:
                    if ftype in filename:
                        self.localfiles[filename] = {
                            "filename": filename,
                            "filesize": getsize(os.path.join(dirpath, filename)),
                            "abspath": os.path.join(dirpath, filename),
                            "dirpath": dirpath,
                            
                        }
        print("Found These: ",[file_name for file_name in self.localfiles.keys()])    
    
    def add(self,project_name,project_dir):
        if self.localfiles:
            for k,file_meta in self.localfiles.items():
                filekey = id_generator(20)
                projectkey = self.PaperclipConfig["projectkey"]
                file_insert_report = self.db.create_file(file_meta,project_name,filekey,projectkey)
                print(file_insert_report)

    
    """
    Queue Tools:
    These are the tools for running tasks on a loaded queue.
    
    load_queue: loads a queue using a state and db tools
    upload:     loads a queue of fiels with upload state
    
    """
    def load_queue(self,project_name,state):
        files_with_state = self.db.get_files_with_state(project_name,state)
        return files_with_state


    def _zip(self,project_name,project_dir,filekey_abspaths):
        os.chdir(project_dir)
        zipObj = zipfile.ZipFile(f"{project_name}.zip","w")
        for filekey,abspath in filekey_abspaths:
            print("added to zip: ",filekey, "  ",abspath)
            zipObj.write(abspath,arcname=f"{filekey}_" +os.path.basename(abspath)+".original")
        zipObj.close()
    
    
    def upload(self,project_name,project_dir,queue_files):
        zippath = os.path.join(project_dir,project_name+".zip")
        object_name = project_name+".zip"
        # bucket_name = project_name + "-project-datasets"  # remove
        
        if project_name+".zip" in os.listdir(project_dir):
            os.remove(os.path.join(project_dir,project_name+".zip"))    
        
        filekey_abspaths = [(f[0],f[3]) for f in queue_files]
        self._zip(project_name,project_dir,filekey_abspaths)
        print("Uploading zip: ",zippath)
        self.cloud_client.upload_file(bucket_name,zippath,project_name,object_name)
        
        
        # get public url of zip file, and then read and write the public url to paperclip file
        publicurl = self.cloud_client.get_public_url(bucket_name,object_name)
        self.PaperclipConfig = read_config(project_dir)
        self.PaperclipConfig["publicurl"] = publicurl 
        write_config(project_dir,self.PaperclipConfig)
        print(self.PaperclipConfig["publicurl"])
        
        
        
        # def write_config(project_dir,PaperclipConfig):
        # with open(os.path.join(project_dir,"paperclip"),"w") as f:
        #     f.write("project_name:"+PaperclipConfig["project_name"]+"\n"+
        #             "projectkey:"+PaperclipConfig["projectkey"]+"\n"+
        #             "publicurl:"+PaperclipConfig["publicurl"]
        #             )


    
    def remove(self,queue_files,project_name,project_dir):
        filekey_abspaths = [(f[0],f[3]) for f in queue_files]
        print(filekey_abspaths)
        for filekey,abspath in filekey_abspaths:
            try:
                
                os.remove(abspath)
                os.system(f"touch {os.path.dirname(abspath)}/{filekey}_{os.path.basename(abspath)}.paperclip")
                print("removed :"+ abspath)
                time.sleep(0.5)
                
            except OSError as e: 
                if e.errno == errno.ENOENT: # errno.ENOENT = no such file or directory
                    print("no such file to remove")
                else:
                    raise 
        os.remove(os.path.join(project_dir,f"{project_name}.zip"))
    
    
    def download(self,project_name,project_dir,queue_files):
        # first download the zip
        # bucket_name = project_name + "-project-datasets"  # remove
        object_name = project_name + ".zip"
        print(f"Downloading {object_name} from Bucket \"{bucket_name}\"")
        self.cloud_client.download_file(bucket_name,object_name,project_dir)
    
        #distribute the files to their original spots
        unzip_dir = f"{project_name}_unzip"
        if unzip_dir in os.listdir(project_dir):
            shutil.rmtree(os.path.join(project_dir,unzip_dir))
            print("removed :",unzip_dir)
        
        zippath = os.path.join(project_dir,f'{project_name}.zip')
        with zipfile.ZipFile(zippath , 'r') as zipObj:
            os.chdir(project_dir)
            os.mkdir(unzip_dir)
            zipObj.extractall(unzip_dir)
    
        
        """
        It walks in the whole project directory and finds .paperfile files and replaces them with the files with same filekey 
        which were extracted from the zip file.
        """
        os.chdir(project_dir)
        os.walk(project_dir)
        for dirpath, dirnames, filenames in os.walk(project_dir, topdown=True):
            for filename in filenames:
                if ".paperclip" in filename:
                    filekey = filename.split("_")[0]
                    original_filename = "".join(filename.strip(".paperclip").split("_")[1:])
                    for zip_file in os.listdir(unzip_dir):
                        if filekey in zip_file:
                            print(f"cp {os.path.join(project_dir,unzip_dir,zip_file)}  {os.path.join(dirpath,original_filename)}")
                            os.system(f"cp {os.path.join(project_dir,unzip_dir,zip_file)}  {os.path.join(dirpath,original_filename)}")
                            os.remove(os.path.join(dirpath,filename))
        
        shutil.rmtree(os.path.join(project_dir,unzip_dir))
        os.remove(os.path.join(project_dir,object_name))
            
    
    def state(self,project_dir):
        """
        if paperclip file exists, gets the project and its files from db 
        and pretty prints them
        """
        
        if "paperclip" not in os.listdir(project_dir):
            print('(!) No project has been initialized yet.\n => you can use "paperclip init" to start a new project.\n => Or it might be because you have lost the "paperclip config file" ')
        
        elif "paperclip" in os.listdir(project_dir):
            PaperclipConfig = read_config(project_dir)
            project, files = self.db.get_project(PaperclipConfig["projectkey"])
            files_table = tabulate([[file[1],file[0],file[2],file[-1]] for file in files], headers=['File Name', 'File Key','Size','state'], tablefmt='orgtbl')
            print(f'project:"{PaperclipConfig["project_name"]}" with projectkey: "{PaperclipConfig["projectkey"]}"\nFiles added to the project: \n\n{files_table}')
            
            


 
        
        
        