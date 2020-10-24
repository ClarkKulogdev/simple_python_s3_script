import boto3
import random
import awscli
import glob
import os
import pathlib
import json
from botocore.exceptions import ClientError


###Client_AWS_S3###
s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3',region_name = 'us-east-1')

#print(s3_client) #check if s3_client connected
#print(s3_resource) #check if s3_resource connected

#creating a bucket function
def create_new_bucket(buck_name):
    try:
        s3_client.create_bucket(Bucket = buck_name) #creating a new bucket by input name
        print("Bucket name \""+buck_name+"\" is created." ) #success!
        print("Returning to Option List")
        
    except Exception as Error_Creating_Bucket:
        print(Error_Creating_Bucket)
        ask_user = input("Create Name again? Y/N:")

        ### Ask again the user ####
        if ask_user.lower() == 'y':
            print("Enter Name for the new bucket:")
            new_buck_name = input()
            create_new_bucket(new_buck_name)
        elif ask_user.lower() == 'n':
            print("Returning to Option List...")
        
        else:
            print("Wrong key, returning to option list...")
            

def list_all_created_bucket():
   response= s3_client.list_buckets()
   now_listed = list(response['Buckets']) #putting the list of buckets and informations
   print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
   print("List of existing buckets:")

   for num in range(len(now_listed)):
       print(num,now_listed[num]['Name'])
    
   print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

def read_data_in_that_buc(num):
    response = s3_client.list_buckets()
    now_listed = list(response['Buckets'])

    try:

        s3_resource = boto3.resource('s3')
        selected_bucs = s3_resource.Bucket(now_listed[int(num)]['Name'])
        print("Files in \""+now_listed[int(num)]['Name']+"\" are the following:")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        for obj in selected_bucs.objects.all():
            print(obj.key)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    except:
        print("Invalid Number:")
        print("Enter number again? Press N to return option list:")
        ask_user = input()

        if ask_user.lower() == 'n':
            print("Returning to option list...")

        else:
            print("Enter Number:")
            new_num = input()
            read_data_in_that_buc(new_num)

def upload_data(num):


    response = s3_client.list_buckets()
    now_listed = list(response['Buckets'])

    try:

        s3_resource = boto3.resource('s3')
        selected_bucs = now_listed[int(num)]['Name']
        print("Selected Folder:"+selected_bucs)

        print("Enter the location of the files to be uploaded (example: ../Documents/* (if upload all files in this folder) ):")
        located_files = []
        location_of_files = []
        while location_of_files == "" or located_files == []:
            location_of_files = input()
            located_files = glob.glob(os.path.join(location_of_files))
            #print(located_files)
            if located_files == []:
                print("Location of folder/ file is not exist!")
                print("Enter the location of folder/files")
            if location_of_files == "":
                print("Enter a valid Location:")
        #print(location_of_files)
        ###verify location###
        #print(located_files)
        #print(selected_bucs)

        for file in located_files:
            #print(file)
            #print(selected_bucs)
            upload_file(file, selected_bucs)


    except Exception as error_up:
        print(error_up)
        print("Invalid Number:")
        print("Enter number again? Press N to return option list:")
        ask_user = input()

        if ask_user.lower() == 'n':
            print("Returning to option list...")

        else:
            print("Enter Number:")
            new_num = input()
            upload_data(new_num)       


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    new_name = file_name.split('/')
    
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = new_name[-1]
        print("Uploading \"" + object_name + "\" to bucket name: "+bucket)
    #"""
    try:
        response = s3_client.upload_file(file_name, bucket,object_name)
        print(object_name + " is now uploaded.")
    
    except ClientError as e:
        logging.error(e)
        return False
    return True 
    #"""

while True:
    msg=None
    #display options
    print("______________________________________________________")
    print("||[0]Create Bucket:                                 ||")
    print("||[1]List existing buckets:                         ||")
    print("||[2]Read data in a bucket (specific bucket):       ||")
    print("||[3]Write data in a bucket (specific bucket):      ||")
    print("||[4]Exit:                                          ||")
    print("||__________________________________________________||")
    #choose mode
    mode = input("Enter Mode:")

    if mode == '0': 
        buck_name = input("Enter Bucket name:")
        create_new_bucket(buck_name)

    elif mode == '1':
        list_all_created_bucket()
    elif mode == '2':
        list_all_created_bucket()
        print("Enter the Number of the bucket:")
        buc_num = input()
        read_data_in_that_buc(buc_num)
    elif mode == '3':
        list_all_created_bucket()
        print("Enter the Number of the bucket:")
        buc_num_in_upload = input()
        upload_data(buc_num_in_upload)
        pass
    elif mode == '4':
        break
    else:
        msg = ("Wrong key!")

    if msg != None:
        print(msg)



