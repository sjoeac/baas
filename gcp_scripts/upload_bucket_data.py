import os
import shutil
import datetime
import zipfile
import subprocess
from zipfile import ZipFile

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
            shutil.rmtree(dir_dst)


print ("Syncing Bucket data to GCP Storage...")
cmd_args = ['gsutil', 'rsync', '-r', './backup/', 'gs://mydata-1']
s3_folder_data  = subprocess.call(cmd_args)

if os.path.exists(dir_dst):
    shutil.rmtree(dir_dst)
