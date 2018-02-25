import subprocess
import sys

print ("Listing Buckets")
cmd_args = ['aws', 's3', 'ls']
s3_folder_data  = subprocess.call(cmd_args)


print ("\nListing Bucket Data")
cmd_args2 = ['aws', 's3', 'ls', 'mydata-1']
s3_folder_data2  = subprocess.call(cmd_args2)
