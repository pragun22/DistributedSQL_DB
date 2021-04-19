import mysql.connector
import requests
import random 
import time
from flask import Flask, jsonify, request

app = Flask(__name__)

LogFile = open("Participant.log", "a+", buffering=1)

@app.route('/')
def health():
	return jsonify({'message':"Hello World"})

@app.route('/abort')
def Abort():
	print("Global Abort recieved")
	print("Aborting from process")
	LogFile.write("Abort\n")
	return jsonify({'response':'abort-ack'})

@app.route('/prepare')
def prepare():
	print("Recieved response Prepare from the Co-ordinator")

	rand = random.random()
	if rand < 0.1:
		print("Not ready to commit, preparing abort")
		LogFile.write("Abort\n")
		return jsonify({'response' : 'Abort'})

	elif rand < 0.15:
		time.sleep(6)
		return jsonify({'response' : 'Vote-Commit'})

	else:
		print("Ready to commit")
		LogFile.write("Ready\n")
		return jsonify({'response' : 'Vote-Commit'})

@app.route('/query', methods=['POST'])
def performQuery():
	
	data = request.json
	print(data)

	try:
		conn = mysql.connector.connect(user='pragun', password='letscode', host='localhost', database='Lonely')
		cursor = conn.cursor()
		print(data['Query'])
		cursor.execute(data['Query'])
		conn.commit()
		cursor.close()
		conn.close()
	except Exception as e:
		print(e)
	
	LogFile.write("Commit\n")
	print("Txn Succesful")
	return jsonify({'response' : 'Ack'})





if __name__ == '__main__':
	app.run(debug = True, host = '0.0.0.0', port='7000')
