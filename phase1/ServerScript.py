import sshtunnel


import mysql.connector
with sshtunnel.SSHTunnelForwarder(
	('10.3.5.212'),
	ssh_username='user',ssh_password='iiit123',remote_bind_address=("CP4",22)
	) as tunnel:

	conn = mysql.connector.connect(
		user='pragun', password='letscode', host='127.0.0.1', port=tunnel.local_bind_port, database='Lonely')
	cursor = conn.cursor()

	insert_stmt = (
		"Select id from Fragments"
		)
	data = (1, 934567981, 'Surya Kumar', 'Wilsons Limited');
	try:
		cursor.execute(insert_stmt)
		print('hi')
		conn.commit()
	except:
		conn.rollback()

	Print("Test successful")
	conn.close()
