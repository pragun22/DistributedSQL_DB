from moz_sql_parser import parse
import mysql.connector
import os
import json
import csv
import time

def EXIT():
	cursor.close()
	conn.close()
	exit(0)


HOR_CONDITION = 'city'
DHOR_CONDITION = 'reserveId'
URL = {}
URL['1'] = '10.3.5.212'
URL['2'] = '10.3.5.211'
URL['3'] = '10.3.5.208'
URL['localhost'] = 'localhost'
index = {}
SelectivityFactors = [[0]*3]*3
with open('SelectivityFactors.csv', 'r') as file:
    reader = csv.reader(file)
    i = 1
    for row in reader:
        ind =0
        print(row)
        if i == 1:
        	for col in row:
        		if col == '':
        			continue
        		index[col] = ind
        		ind += 1
        else:
        	for col in row:
        		if ind !=0:
        			SelectivityFactors[i-2][ind-1] = col
        		ind += 1
        i+=1

print("index ==> ", index)
print("SelectivityFactors ==> ", SelectivityFactors)

if SelectivityFactors[0][1] > SelectivityFactors[1][0]:
	URL['localhost'] = URL['1']
else:
	URL['localhost'] = URL['2']

if SelectivityFactors[0][2] > SelectivityFactors[0][0]:
	URL['localhost'] = URL['3']

def FormWhereQueries(op, operand1, operand2):
	if op == 'eq':
		return str(operand1)+ " = '"+ str(operand2) +"'"
	if op == 'lt':
		return str(operand1)+ " < "+ str(operand2)
	if op == 'gt':
		return str(operand1)+ " > "+ str(operand2)
	if op == 'lte':
		return str(operand1)+ " <= "+ str(operand2)
	if op == 'gte':
		return str(operand1)+ " >= "+ str(operand2)	



## Connecting to Server

conn = mysql.connector.connect(
	user='pragun', password='letscode', host=URL['localhost'], database='Lonely')

cursor = conn.cursor()

print("Connection to mysql server established")

# res = Decomposer()
# print(res)
class Exiting(Exception):
    pass
EXIT = Exiting()

while True:
	print("Enter your Query:")

	input_query = input()

	### Parsing and generatign jasonizable tree

	try:

		print("Decomposing the query")

		try:
			parse_tree = parse(input_query)
		except Exception as e:
			print("Error with query")
			print(e)
			raise EXIT
		# print("Initial Parse Tree")
		print(parse_tree)

		selects = []
		aggs = {}
		attribToAggs = {}
		groupby = []
		havingcond = {}
		havingop = {}
		having = []
		wherecond = {}
		whereop = {}
		where = []
		
		relations = []

		joinFlag = False
		semiJoinCond = None 
		joinAtts = []
		if isinstance(parse_tree['from'], str):
			relations.append(parse_tree['from'])
		else :
			for rel in parse_tree['from']:
				if isinstance(rel, str):
					relations.append(rel)
				else:
					try:
						relations.append(rel['join'])
						semiJoinCond = rel['on']
						for temp in rel['on']:
							joinAtts.append(rel['on'][temp][0].split('.')[1])
							joinAtts.append(rel['on'][temp][1].split('.')[1])
						joinFlag = True
					except Exception as e:
						print("Error in join syntax")
						print(e)
						raise EXIT


		if isinstance(parse_tree['select'], list):
				for i in parse_tree['select']:
					if isinstance(i['value'], str):
						if '.' in i['value']:
							selects.append(i['value'].split('.')[1])
						else:
							selects.append(i['value'])
					else:
						for temp in i['value']:
							if '.' in i['value'][temp]:
								aggs[temp] = i['value'][temp].split('.')[1]
								attribToAggs[i['value'][temp].split('.')[1]] = temp
							else:
								aggs[temp] = i['value'][temp]
								attribToAggs[i['value'][temp]] = temp
							# selects.append(i['value'][temp])
		else:
			if isinstance(parse_tree['select']['value'], str): 
				if '.' in parse_tree['select']['value']:
					selects.append(parse_tree['select']['value'].split('.')[1])
				else:
					selects.append(parse_tree['select']['value'])
			else:
				for temp in parse_tree['select']['value']:
					if temp not in aggs:
						aggs[temp] = []

					tp = parse_tree['select']['value'][temp]
					if '.' in tp:
						tp = tp.split('.')[1]
					aggs[temp].append(tp)
					attribToAggs[tp] = temp



		if 'groupby' not in parse_tree and len(aggs)!=0:
			print("Error with query\nLooking for groupby but couldn't find it")
			# exit(0)
			raise EXIT

		try:
			if 'groupby' in parse_tree:
				if isinstance(parse_tree['groupby'], list):
					for val in parse_tree['groupby']:
						if val['value'].find('.')!=-1:
							groupby.append(val['value'].split('.')[1])
						else:
							groupby.append(val['value'])
				else:
					if '.' in parse_tree['groupby']['value']:
							groupby.append(parse_tree['groupby']['value'].split('.')[1])
					else:
						groupby.append(parse_tree['groupby']['value'])

			if 'having' in parse_tree:
				for res in parse_tree['having']:
					if res != 'and' and res != 'or':
						tp = parse_tree['having'][res][0]
						tp2 = parse_tree['having'][res][1]
						if '.' in tp:
							tp = tp.split('.')[1]
						if not isinstance(tp2, dict) and '.' in str(tp2):
							tp2 = tp2.split('.')[1]
						having.append(tp)
						havingcond[tp] = tp2
						if isinstance(tp2, dict):
							havingcond[tp] = tp2['literal']
						havingop[tp] = res
					else:
						for j in parse_tree['having'][res]:
							if 'and' not in j and 'or' not in j:
								for key, value in j.items():
									tp = value[0]
									tp2 = value[1]
									if '.' in tp:
										tp = tp.split('.')[1]
									having.append(tp)
									# print(tp2)
									if isinstance(tp2, dict):
										print(tp2)
										if '.' in tp2['literal']:
											havingcond[tp] = tp2['literal'].split('.')[1]
										else:
											havingcond[tp] = tp2['literal']
									else:
										if '.' in str(tp2):
											tp2 = tp2.split('.')[1]
										havingcond[tp] = tp2
									havingop[tp] = key
							else:
								for _,k1 in j.items():
									for k in k1:
										for key, value in k.items():
											tp = value[0]
											tp2 = value[1]
											if '.' in tp:
												tp = tp.split('.')[1]
											having.append(tp)
											# print(tp2)
											if isinstance(tp2, dict):
												if '.' in tp2['literal']:
													havingcond[tp] = tp2['literal'].split('.')[1]
												else:
													havingcond[tp] = tp2['literal']
											else:
												if '.' in str(tp2):
													tp2 = tp2.split('.')[1]
												havingcond[tp] = tp2
											havingop[tp] = key


			if 'where' in parse_tree:
				for res in parse_tree['where']:
					if res != 'and' and res != 'or':
						tp = parse_tree['where'][res][0]
						tp2 = parse_tree['where'][res][1]
						if '.' in tp:
							tp = tp.split('.')[1]
						if '.' in str(tp2):
							tp2 = tp2.split('.')[1]
						where.append(tp)
						wherecond[tp] = tp2
						if isinstance(tp2, dict):
							wherecond[tp] = tp2['literal']
						whereop[tp] = res
					else:
						for j in parse_tree['where'][res]:
							if 'and' not in j and 'or' not in j:
								for key, value in j.items():
									tp = value[0]
									tp2 = value[1]
									if '.' in tp:
										tp = tp.split('.')[1]
									where.append(tp)
									if isinstance(tp2, dict):
										wherecond[tp] = tp2['literal']
									else:
										if '.' in str(tp2):
											tp2 = tp2.split('.')[1]
										wherecond[tp] = tp2
									whereop[tp] = key

							else:
								for _,k1 in j.items():
										for k in k1:
											for key, value in k.items():
												tp = value[0]
												tp2 = value[1]
												if '.' in tp:
													tp = tp.split('.')[1]
												where.append(tp)
												if isinstance(tp2, dict):
													wherecond[tp] = tp2['literal']
												else:
													if '.' in str(tp2):
														tp2 = tp2.split('.')[1]
													wherecond[tp] = tp2
												whereop[tp] = key
		except Exception as e:
			print('error in Parsing', e)
			raise EXIT



		selects = list(set(selects))
		aggs = list(set(aggs))
		groupby = list(set(groupby))
		having = list(set(having))
		where = list(set(where))

		print('STEP 1 printing all the datastructrues after Parsing')
		print('selects =>', selects)
		print('aggs =>', aggs)
		print('attribToAggs =>', attribToAggs)
		print('relations =>', relations)
		print('groupby =>', groupby)
		print('having =>', having)
		print('where =>', where)
		print('havingop =>', havingop)
		print('havingcond =>', havingcond,end='\n\n\n')

		# for H in having:
		# 	if H not in groupby :
		# 		print("Error in query having statement\nExiting")
		# 		exit(0)
		for S in selects:
			if (S not in groupby or S in aggs ) and 'groupby' in parse_tree:
				print("Error in query\nExiting")
				# exit(0)
				raise EXIT


		FragmentIdToSite = {}
		FragmentIdToType = {}
		FragmentTypeToId = {}
		FragmentTypeToRelation = {}
		RelationToFragmentIds = {}

		for rel in relations:
			query_frags = ( "SELECT id, FragmentType, SiteId From Fragments "
				"WHERE RelationName = %s;")

			cursor.execute(query_frags, (rel, ))
			FragsRes = cursor.fetchall()

			if len(FragsRes) == 0:
				print("empty query while finding Fragments for the given relation name\nRelation name Doesn't exist\nExiting")
				# exit(0)
				raise EXIT
			
			if rel not in RelationToFragmentIds:
				RelationToFragmentIds[rel] = []
			for i in FragsRes:

				RelationToFragmentIds[rel].append(i[0])
				FragmentIdToType[i[0]] = i[1]
				if i[1] not in FragmentTypeToId:
					FragmentTypeToId[i[1]] = []
				FragmentTypeToId[i[1]].append(i[0])
				FragmentTypeToRelation[i[1]] = rel
				FragmentIdToSite[i[0]] = i[2]
			
		print("STEP 2, printfing after gathering fragment and siteInfo")
		print('FragmentIdToSite =>', FragmentIdToSite)
		print('FragmentIdToType =>', FragmentIdToType)
		print('FragmentTypeToId =>', FragmentTypeToId)
		print('FragmentTypeToRelation =>', FragmentTypeToRelation)
		print('RelationToFragmentIds  =>', RelationToFragmentIds,end='\n\n\n')

		RelationToAttribs = {}
		RelationToAttribsId = {}
		AttribsToRelation = {}
		AttribIdToAttrib = {}

		for i in groupby:
			if i not in selects:
				selects.append(i)

		temp = []
		for att in selects:
			temp.append(att)

		for att in attribToAggs:
			if att not in temp:
				temp.append(att)
		for att in having:
			if att not in temp:
				temp.append(att)

		for att in where:
			if att not in temp:
				temp.append(att)

		for att in joinAtts:
			if att not in temp:
				temp.append(att)

		for attrib in temp:
			for rel in relations:
				if rel not in RelationToAttribs:
					RelationToAttribs[rel] = []
					RelationToAttribsId[rel] = []
				
				query = "SELECT id FROM Attributes WHERE AttributeName='"+str(attrib)+"' and RelationName ='"+str(rel)+"';"
				cursor.execute(query)
				res = cursor.fetchall()
				if len(res) != 0:
					
					RelationToAttribs[rel].append(attrib)
					RelationToAttribsId[rel].append(res[0][0])
					AttribIdToAttrib[res[0][0]] = attrib
					
					if attrib not in AttribsToRelation:
						AttribsToRelation[attrib] = []
					AttribsToRelation[attrib].append(rel)

		print("STEP 3 printing about relation and attributes")
		print('RelationToAttribs =>',RelationToAttribs)
		print('RelationToAttribsId =>',RelationToAttribsId)
		print('AttribsToRelation =>',AttribsToRelation)
		print('AttribIdToAttrib =>',AttribIdToAttrib,end='\n\n\n')




		if 'Hor' in FragmentTypeToRelation:
			try:
				sitesHor=[]
				if HOR_CONDITION in having:
					condition = havingcond[HOR_CONDITION]
					query = "select FragmentId from HorFragment where `condition` = '"+str(condition)+"';"
					cursor.execute(query)
					result = cursor.fetchall()
					try:
						fragId = result[0][0]
					except:
						print("Fragment doesn't exist \nexiting")
						# EXIT()
						raise EXIT
					siteId = FragmentIdToSite[fragId]		
					sitesHor.append(siteId)
				else:
					for fragId in FragmentTypeToId['Hor']:
						sitesHor.append(FragmentIdToSite[fragId])
			except Exception as e:
				print("Error while finding sites for Horizontal Fragment")
				print(e)

			try:
				attribsHor = RelationToAttribs[FragmentTypeToRelation['Hor']]
				attribTypeHor = {}
				query = "DESCRIBE " + FragmentTypeToRelation['Hor']
				cursor.execute(query)
				res = cursor.fetchall()
				for i in res:
					attribTypeHor[i[0]] = i[1].decode('utf-8')
				dataHor = []
				for siteId in sitesHor:
					conn2 = mysql.connector.connect(user='pragun', password='letscode', host=URL[str(siteId)], database='Lonely')
					cursor2 = conn2.cursor()
					query = "SELECT " + ', '.join(attribsHor) + " FROM " + str(FragmentTypeToRelation['Hor'])  + ";"
					cursor2.execute(query)
					res = cursor2.fetchall()
					dataHor = dataHor + res
				cursor.execute("DROP TABLE IF EXISTS `TempHor`")
				query = "CREATE TABLE `TempHor`("
				for att in attribsHor:
					query+= str(att) + " "+ str(attribTypeHor[att]) + " not null, "
				query = query[:-2]
				query += ");"
				print(query)
				cursor.execute(query)
				for dat in dataHor:
					query = "INSERT INTO `TempHor` VALUES( "
					for i in dat:
						if not isinstance(i, int):
							query+="'"
						query += str(i)
						if not isinstance(i, int):
							query+="'"
						query += ", "
					query = query[:-2]
					query += ");"
					cursor.execute(query)

			except Exception as e:
				print("Error while moving data to one site for semi-join for Horizontal Fragment")
				print(e)

			input_query = input_query.replace(FragmentTypeToRelation['Hor'],'TempHor')

		if 'DHor' in FragmentTypeToRelation:
			try:
				sitesDHor=[]
				if DHOR_CONDITION in having:
					condition = havingcond[DHOR_CONDITION]
					query = "select FragmentId from DHorFragment where `condition` = '"+str(condition)+"';"
					cursor.execute(query)
					result = cursor.fetchall()
					try:
						fragId = result[0][0]
					except:
						print("Fragment doesn't exist \nexiting")
						# EXIT()
						raise EXIT
					siteId = FragmentIdToSite[fragId]		
					sitesDHor.append(siteId)
				else:
					for fragId in FragmentTypeToId['DHor']:
						sitesDHor.append(FragmentIdToSite[fragId])
			except Exception as e:
				print("Error while finding sites for Horizontal Fragment")
				print(e)

			try:
				attribsDHor = RelationToAttribs[FragmentTypeToRelation['DHor']]
				attribTypeDHor = {}
				query = "DESCRIBE " + FragmentTypeToRelation['DHor']
				cursor.execute(query)
				res = cursor.fetchall()
				for i in res:
					attribTypeDHor[i[0]] = i[1].decode('utf-8')
				dataDHor = []
				for siteId in sitesDHor:
					conn2 = mysql.connector.connect(user='pragun', password='letscode', host=URL[str(siteId)], database='Lonely')
					cursor2 = conn2.cursor()
					query = "SELECT " + ', '.join(attribsDHor) + " FROM " + str(FragmentTypeToRelation['DHor'])  + ";"
					cursor2.execute(query)
					res = cursor2.fetchall()
					dataDHor = dataDHor + res
				cursor.execute("DROP TABLE IF EXISTS `TempDHor`")
				query = "CREATE TABLE `TempDHor`("
				for att in attribsDHor:
					query+= str(att) + " "+ str(attribTypeDHor[att]) + " not null, "
				query = query[:-2]
				query += ");"
				cursor.execute(query)
				for dat in dataDHor:
					query = "INSERT INTO `TempDHor` VALUES( "
					for i in dat:
						if not isinstance(i, int):
							query+="'"
						query += str(i)
						if not isinstance(i, int):
							query+="'"
						query += ", "
					query = query[:-2]
					query += ");"
					cursor.execute(query)

			except Exception as e:
				print("Error while moving data to one site for semi-join for DHorizontal Fragment")
				print(e)


			input_query = input_query.replace(FragmentTypeToRelation['DHor'],'TempDHor')

		if 'Ver' in FragmentTypeToRelation:
			try:
				siteIdToAttribVer = {}
				sitesVer = []
				mapSiteIdToFragIdVer = {}

				for fragId in FragmentTypeToId['Ver']:
					for attribId in AttribIdToAttrib:
						query = "SELECT * FROM VerFragment WHERE FragmentId = " + str(fragId) + " and AttributeId = " + str(attribId)
						cursor.execute(query)
						res = cursor.fetchall()
						if len(res)!=0:
							siteId = FragmentIdToSite[fragId]
							mapSiteIdToFragIdVer[siteId] = fragId
							if siteId not in siteIdToAttribVer:
								siteIdToAttribVer[siteId] = []
							siteIdToAttribVer[siteId].append(attribId)

				TotalAtt = len(RelationToAttribsId[FragmentTypeToRelation['Ver']])

				for siteId in siteIdToAttribVer:
					if len(siteIdToAttribVer[siteId]) == 1 and 27 in siteIdToAttribVer[siteId]:
						continue
					sitesVer.append(siteId)
					if len(siteIdToAttribVer[siteId]) == TotalAtt:
						sitesVer = []
						sitesVer.append(siteId)
						break
				if len(sitesVer) == 0:
					sitesVer.append(1)
			except Exception as e:
				print("Error while finding sites for Vertical Fragment")

			try:
				VerMap = {}
				Veratts = []
				attribTypeVer = {}
				for siteId in sitesVer:
					conn2 = mysql.connector.connect(user='pragun', password='letscode', host=URL[str(siteId)], database='Lonely')
					cursor2 = conn2.cursor()

					query = "SELECT AttributeId from VerFragment WHERE FragmentId="+str(mapSiteIdToFragIdVer[siteId]) +" and AttributeId IN (SELECT id from Attributes WHERE AttributeName='guestId' and RelationName='" + str(FragmentTypeToRelation['Ver']) +"');"
					cursor.execute(query)
					res = cursor.fetchall()
					res = res[0][0]
					if res in siteIdToAttribVer[siteId]:
						siteIdToAttribVer[siteId].remove(res)
					siteIdToAttribVer[siteId].insert(0, res)
					query = "DESCRIBE " + FragmentTypeToRelation['Ver']
					cursor2.execute(query)
					res = cursor2.fetchall()
					for i in res:
						attribTypeVer[i[0]] = i[1].decode('utf-8')
					query = "SELECT "
					for attId in siteIdToAttribVer[siteId]:
						if attId not in AttribIdToAttrib:
							query += "guestId, "
						else:
							query += str(AttribIdToAttrib[attId]) + ", "
					query = query[:-2] 
					query += " FROM " + str(FragmentTypeToRelation['Ver']) +";"
					# print(query)
					cursor2.execute(query)
					res = cursor2.fetchall()
					for att in siteIdToAttribVer[siteId]:
						temp = None
						if att not in AttribIdToAttrib:
							Temp = "guestId"
						else:
							Temp = AttribIdToAttrib[att]
						if Temp not in Veratts:
							Veratts.append(Temp)
					for i in res:
						if i[0] not in VerMap:
							VerMap[i[0]] = []
						for j in range(1, len(i)):
							VerMap[i[0]].append(i[j])
				
				## Creating temp Ver fragment
				cursor.execute("DROP TABLE IF EXISTS `TempVer`")
				query = "CREATE TABLE `TempVer`("
				for att in Veratts:
					query +=  str(att) + " " + str(attribTypeVer[att]) +" not null, "
				query = query[:-2]
				query += ");"
				cursor.execute(query)
				for dat in VerMap:
					query = "INSERT INTO `TempVer` VALUES( "
					query += str(dat) + ", "
					for i in VerMap[dat]:	
						if not isinstance(i, int):
							query+="'"
						query += str(i)
						if not isinstance(i, int):
							query+="'"
						query+=", "
					query = query[:-2]
					query += ");"
					cursor.execute(query)

			except Exception as e:
				print("Error while moving data for semi join in Ver Fragment")
				print(e)


			input_query = input_query.replace(FragmentTypeToRelation['Ver'],'TempVer')
		
		
		cursor.execute("DROP TABLE IF EXISTS `CHECK`")
		cursor.execute("CREATE TABLE `CHECK` (id int not null)")
		cursor.execute("INSERT INTO `CHECK` VALUES(1)")

		print("\n\n\nPrinting final Result:\n")

		print(input_query)



		try:
			cursor.execute(input_query)
			res  = cursor.fetchall()
			print(res)
		except Exception as e:
			print("Error while executing the final query\n\n")
			print(e)
			print("\nExiting")
	

	except Exiting:
		continue