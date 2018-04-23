import os
import shutil
import datetime
import subprocess
from zipfile import ZipFile
import re
import logging
import sys
import requests


#Logging parameters
logging.basicConfig(format='%(asctime)s %(message)s', filename="backup.log", level=logging.INFO)

#Email paramaters
sender_email = '@gmail.com'
sender_name = 'Stephen'
subject = 'Bucket Testing'
content = 'email content here...'
 
#logging.debug("This is a debug message")
#logging.info("Informational message")
#logging.error("An error has happened!")
url = "https://api.sendgrid.com/v3/mail/send"

dir_src = "./backup/"
now  = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
dir_dst = dir_src + now

#cloud_provider = 'AWS'
#cmd_args = ['aws', 's3', 'sync', './backup/','s3://mydata-1/','--storage-class','STANDARD_IA']

cloud_provider = 'GCP'
cmd_args = ['gsutil', 'rsync', '-r', './backup/', 'gs://mydata-1']

logging.info ("-------------------------------------------------")
logging.info ("Backup Process Started..." + now )

if not os.path.exists(dir_dst):
    logging.info ("Creating Directory..." + dir_dst)
    print ("Creating Directory..." + dir_dst)
    os.makedirs(dir_dst)


for file in os.listdir(dir_src):
    if not re.match("^\d{4}_", file):
        print ("Processing..." + file)
        src_file = os.path.join(dir_src, file)
        dst_file = os.path.join(dir_dst, file)
        shutil.move(src_file, dst_file)
        logging.info ("Moved " + file + " to ..." + dir_dst)
        print ("Moved " + file + " to ..." + dir_dst)


print ("Start Syncing Bucket data to " + cloud_provider + " Storage...")
logging.info ("Start Syncing Bucket data to " + cloud_provider + " Storage...")

try:
    data = subprocess.check_output(cmd_args)
    logging.info ("Sync Completed...")
    print ("Sync Completed...")
    content = "Sync Completed..."
except Exception as e:
    logging.info(e)
    print (e)
    content = e


"""
# Block for Directory cleanup
print ("Cleaning up...")
logging.info ("Cleaning up...")
for file in os.listdir(dir_src):
    if os.path.isdir(dir_src + file):
        shutil.rmtree(dir_src + file)

shutil.rmtree(dir_dst)
"""

payload = '{"personalizations":[{"to":[{"email":"' + sender_email + '","name":"'+ sender_name +'"}],"subject":"' + subject + '"}],"from":{"email":"' + sender_email + '","name":"' + sender_name + '"},"reply_to":{"email":"' + sender_email + '","name":"' + sender_name + '"},"subject":"' + subject + '","content":[{"type":"text/html","value":"' + content + '"}]}'


headers = {
    'authorization': "Bearer SG.",
    'content-type': "application/json"
    }

response = requests.request("POST", url, data=payload, headers=headers)
#print(response.text)
#print (response.status_code)

if response.status_code == 202:
    logging.info ("Emailed Sent Status Sucessful..." + now )
else:
    logging.info ("Emailed Sent Status Failure..." + now )


logging.info ("Backup Process Ended..." + now )
print  ("Backup Process Ended..." + now )
