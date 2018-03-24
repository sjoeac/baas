import os
import shutil
import datetime
import zipfile
import subprocess
from zipfile import ZipFile
import re
import logging
import sys
import pickle

logging.basicConfig(format='%(asctime)s %(message)s', filename="sample.log", level=logging.INFO)
 
#logging.debug("This is a debug message")
#logging.info("Informational message")
#logging.error("An error has happened!")

dir_src = "./backup/"
now  = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
dir_dst = dir_src + now

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
        with ZipFile(dir_dst + '.zip','w') as zip:
            logging.info ("Archiving " + file + " to ..." + dir_dst + '.zip')
            print ("Archiving " + file + " to ..." + dir_dst + '.zip')
            zip.write(file)
            shutil.rmtree(dir_dst)


print ("Start Syncing Bucket data to GCP Storage...")
logging.info ("Start Syncing Bucket data to GCP Storage...")
cmd_args = ['gsutil', 'rsync', '-r', './backup/', 'gs://mydata-1']
#s3_folder_data  = subprocess.call(cmd_args)
#s3_folder_data  = subprocess.check_output(cmd_args)

try:
    data = subprocess.check_output(cmd_args)
    logging.info ("Sync Completed...")
except Exception as e:
    logging.info(e)


print ("Cleaning up...")
logging.info ("Cleaning up...")
for file in os.listdir(dir_src):
    if os.path.isdir(dir_src + file):
        shutil.rmtree(dir_src + file)

logging.info ("Backup Process Ended..." + now )
