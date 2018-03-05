import os
import shutil
import datetime
import zipfile
import subprocess
from zipfile import ZipFile

# make sure that these directories exist
dir_src = "./backup/"
now  = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
dir_dst = dir_src + now

if not os.path.exists(dir_dst):
    os.makedirs(dir_dst)

for file in os.listdir(dir_src):
    if '2018' not  in file:
        print ("Zipping ..." + file)
        src_file = os.path.join(dir_src, file)
        dst_file = os.path.join(dir_dst, file)
        shutil.move(src_file, dst_file)
        with ZipFile(dir_dst + '.zip','w') as zip:
            zip.write(file)


print ("Syncing Bucket data to AWS S3...")
cmd_args = ['aws', 's3', 'sync', './backup/','s3://mydata-1/','--storage-class','STANDARD_IA']
s3_folder_data  = subprocess.call(cmd_args)

shutil.rmtree('./backup')
if not os.path.exists(dir_src):
    os.makedirs(dir_src)
