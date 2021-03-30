import requests
import os
from config import *

os.system("./mysql_init.sh")
print("[INFO] Cleared CryptDB Database...")
response=requests.get("http://13.233.17.3:3000//api/delete")
print("[INFO] Cleared Cloud Database...")
with open("fp.txt","r") as fp_file:
	fp_list=fp_file.read().splitlines()
	fp_list=[x.split(" ") for x in fp_list]
	print("[INFO] Enrolling {} Students...".format(len(fp_list)))
	for i in range(len(fp_list)):
		fp_list[i]=[int(x) for x in fp_list[i]]
		response = requests.post("http://localhost:5000/api/enroll",json={"id":i+1,"fp":fp_list[i]})
		if response.status_code != requests.codes.ok:
			print("[ERROR] Enrollment Failed!")
			break
	print("[INFO] Enrolled successfully!".format(len(fp_list)))

