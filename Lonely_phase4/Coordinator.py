from moz_sql_parser import parse
import mysql.connector
import os
import json
import csv
import time
import threading 
import requests

LogFile = open("CoordinatorLog.log", "a+", buffering=1)
urls = ["http://10.3.5.212:7000/", "http://10.3.5.211:7000/", "http://10.3.5.208:7000/"]


def GlobAbortFun():
	print("The transaction is not possible sending global abbort to all site")
	LogFile.write("Global Abort\n")
	# LogFile.flush()

	for i in urls:
		try:
			requests.get(i + 'abort', timeout=20)
		except requests.exceptions.Timeout:
			continue
		except Exception as e:
			continue

TxnId = 0

while True:
	TxnId+=1
	print("Enter your update query")

	inp = input()

	# print("Checking health of site")
	# LogFile.write('Checking health of systems')
	# response = requests.get(urls[0])
	# print(response.json())
	LogFile.write("Commit Txn"+str(TxnId)+"\n")
	# LogFile.flush()
	print("Sending Prepare Message to each site")

	GlobAbort = False

	for i in urls:
		try : 
			LogFile.write("Prepare "+i+"\n")
			response = requests.get(i+'prepare', timeout=5)
			if response.json()['response'] == 'Abort':
				print("Recieved Abort from site", i, sep=" ")
				LogFile.write("Abort "+i+"\n")
				GlobAbort = True

		except requests.exceptions.Timeout:
			print("Timeout Occured for the prepare on url = ", i, sep=" ")
			LogFile.write("Timeout "+i+"\n")
			GlobAbort = True
			
		except Exception as e:
			print("Error with requests for site with id = ", i, sep=" ")
			LogFile.write("Error "+i+"\n")
			print(e)
			GlobAbort = True
			
	# LogFile.flush()


	if GlobAbort:
		GlobAbortFun()
		continue

	print('Sending Global Commit for transaction')
	LogFile.write("GlobalCommit\n")
	# LogFile.flush()

	query = {'Query':inp}
	for i in urls:
		try: 
			response = requests.post(i+'/query', json=query, timeout = 10)
			if response.json()['response'] == 'Abort':
				print("Recieved Abort from site", i, sep=" ")
				LogFile.write("Abort "+i+"\n")
				GlobAbort = True
		except requests.exceptions.Timeout:
			print("Timeout Occured with url ", i, sep="")
			GlobAbort = True
			break
		except Exception as e:
			print("Error while executing txn for site with id = ", i, sep=" ")
			LogFile.write("Error "+i+"\n")
			print(e)
			GlobAbort = True
			break
	# LogFile.flush()

	if GlobAbort:
		GlobAbortFun()
		continue

	print("Recieved Acknowledgment from every Site")
	LogFile.write("End Of Txn"+str(TxnId)+"\n")

	# LogFile.flush()


LogFile.close()