from moz_sql_parser import parse
import mysql.connector
import json
import time

# Globals
HOR_CONDITION = 'city'
DHOR_CONDITION = 'reserveId'

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

def EXIT():
	cursor.close()
	conn.close()
	exit(0)	
### Create connection with the local mysql server

# Run the daemon from here


def Decomposer():
	conn = mysql.connector.connect(
	user='pragun', password='letscode', host='localhost', database='Lonely')

	cursor = conn.cursor()
	print("Connection to mysql server established")
	
	print("Enter your Query:")
	### Taking Input

	input_query = input()

	### Parsing and generatign jasonizable tree

	print("Decomposing the query")

	parse_tree = parse(input_query)
	# print("Initial Parse Tree")
	# print(parse_tree)


	### Important Arrays
	attribs = []
	origSelect = []
	relations = []
	wheres = []
	wherecond = {}
	whereop = {}

	if isinstance(parse_tree['select'], list):
		for i in parse_tree['select']:
			attribs.append(i['value'])

	else:
		attribs.append(parse_tree['select']['value'])
		origSelect.append(parse_tree['select']['value'])

	if 'where' in parse_tree:
		for res in parse_tree['where']:
			if res != 'and' and res != 'or':
				attribs.append(parse_tree['where'][res][0])
				wheres.append(parse_tree['where'][res][0])
				wherecond[parse_tree['where'][res][0]] = parse_tree['where'][res][1]
				if isinstance(parse_tree['where'][res][1],dict):
					wherecond[parse_tree['where'][res][0]] = parse_tree['where'][res][1]['literal']

				whereop[parse_tree['where'][res][0]] = res
			else:
				for j in parse_tree['where'][res]:
					for key, value in j.items():
						attribs.append(value[0])
						wheres.append(value[0])
						wherecond[value[0]] = value[1]
						if isinstance(value[1], dict):
							wherecond[value[0]] = value[1]['literal']
						whereop[value[0]] = key


	if isinstance(parse_tree['from'], str):
		relations.append(parse_tree['from'])
	else :
		for rel in parse_tree['from']:
			relations.append(rel)

	# print(attribs)
	attribs = list((set(attribs)))
	relations = list((set(relations)))
	wheres = list((set(wheres)))


	### Query decomposition

	query_frags = ( "SELECT id, FragmentType, SiteId From Fragments "
		"WHERE RelationName = %s;")


	QuerySites = {} # Contains query for each sites
	Sites = {} # contains all the sites for a given type of fragment
	fragTypes = {} #contains name of the relation for the given type of fragmentation
	fragSites = {} # contains a map mappping fragId to SiteId
	for rel in relations:
		cursor.execute(query_frags, (rel, ))
		FragsRes = cursor.fetchall()
		try:
			fragTypes[FragsRes[0][1]] = rel;
			Sites[FragsRes[0][1]] = []
			for i in FragsRes:
				Sites[i[1]].append(i[2])
				fragSites[i[0]] = i[2]
		except:
			print('empty query')
			EXIT()
	fragAttrib = {}
	fragAttribName = {}
	map_attid_to_name = {}
	for att in attribs:
		ind = 0 
		for rel in relations:
			query = "SELECT id FROM Attributes WHERE AttributeName='"+str(att)+"' and RelationName ='"+str(rel)+"';"
			cursor.execute(query)
			res = cursor.fetchall()
			if len(res) != 0:
				if rel not in fragAttrib:
					fragAttrib[rel] = []
					fragAttribName[rel] = []
				fragAttrib[rel].append(res[0][0])
				fragAttribName[rel].append(att)
				map_attid_to_name[res[0][0]] = att
			ind += 1

	fragFreq = {} # for vertical
	siteLocality = [] #for horizontal 
	siteLocality2 = [] #for Dhorizontal 
	fragsFin = {}
	if 'Ver' in fragTypes:
		for att in fragAttrib[fragTypes['Ver']]:
			try:
				query = "SELECT FragmentId from VerFragment WHERE AttributeId="+str(att)+";"
				cursor.execute(query)
				res2 = cursor.fetchall()
				for sId in res2:
					if sId[0] not in fragFreq:
						fragFreq[sId[0]] = []
					fragFreq[sId[0]].append(att)
			except:
				print("Attribute doesn't exist in Ver Frag or SiteId missing\nExiting")
				EXIT()
		flag = -1
		for sid in fragFreq:
			if len(fragFreq[sid]) == len(fragAttrib[fragTypes['Ver']]):
				print("Performing Vertical frag query on a single site is sufficient")
				flag = fragSites[sid]  

		queryV = "SELECT "
		if flag == -1:
			print("need to perform vertical frag on multiple sites")

			for sid in fragFreq:
				whereFlag = False
				for attid in fragFreq[sid]:
					tp = map_attid_to_name[attid]
					if tp in wheres:
						whereFlag = True
			# for sid in fragFreq:
				queryV = "SELECT "
				for attid in fragFreq[sid]:
					queryV += (map_attid_to_name[attid] + ", ")
				queryV = queryV[:-2]
				queryV += " FROM " 
				queryV += fragTypes['Ver']+" "
				wq = ""
				for attid in fragFreq[sid]:
					tp = map_attid_to_name[attid]
					if tp in wheres:
						wq += FormWhereQueries(whereop[tp], tp, wherecond[tp])
						wq += " and "
				if whereFlag == True and wq=="":
					continue
				if wq != "":
					queryV += " WHERE " + wq[:-4] + ";"
				print("Query at site with id:", fragSites[sid] )
				print(queryV)
				if fragSites[sid] not in QuerySites:
					QuerySites[fragSites[sid]] = []
				QuerySites[fragSites[sid]].append(queryV)

		
		else:
			for att in fragAttribName[fragTypes['Ver']]:
				queryV += (att+", ")
			queryV = queryV[:-2]
			queryV += " FROM ";
			queryV += fragTypes['Ver'];
			temp = ""
			for att in fragAttribName[fragTypes['Ver']]:
				if att in wheres:
					temp += FormWhereQueries(whereop[att], att, wherecond[att])
					temp += " and "

			if temp !=  "":
				queryV += " WHERE "
				queryV += temp[:-4]
				queryV += ";"

			print("perform the query on the following site with id:", flag, sep=" ")
			print(queryV)
			if flag not in QuerySites:
				QuerySites[flag] = []
			QuerySites[flag].append(queryV)

		#Queries



	if 'Hor' in fragTypes:
		queryH = "SELECT "
		wq = ""
		for att in fragAttribName[fragTypes['Hor']]:
			queryH += (att+", ")
			if att in wheres:
				wq += FormWhereQueries(whereop[att], att, wherecond[att])
				wq += " and "

		queryH = queryH[:-2]
		queryH += " FROM ";
		queryH += fragTypes['Hor'];
		if wq != "":
			queryH += " WHERE "
			queryH += wq[:-4]
			queryH += ";"

		if len(wheres) == 0 or HOR_CONDITION not in wheres:
			print("Need to perform queries for horizontal Frag on all sites")
			for siteId in Sites['Hor']:
				if siteId not in QuerySites:
					QuerySites[siteId] = []
				QuerySites[siteId].append(queryH)
			print("Query ==> ", queryH)

		else:
			condition = wherecond[HOR_CONDITION]
			
			if not (isinstance(condition, str) or isinstance(condition, int)):
				print("The query has wrong brackets for a string\nplease rectify")
				EXIT()
			query = "select FragmentId from HorFragment where `condition` = '"+str(condition)+"';"

			cursor.execute(query)
			result = cursor.fetchall()
			try:
				fragId = result[0][0]
			except:
				print("Fragment doesn't exist \nexiting")
				EXIT()
			siteId = fragSites[fragId]
			print("Need to perform horizontal frag query on a single site with SITE ID",siteId)
			print("Query ==> ", queryH)
			if siteId not in QuerySites:
				QuerySites[siteId] = []
			QuerySites[siteId].append(queryH)
			# fragsFin['Hor'].append(siteId)

	if 'DHor' in fragTypes:
		queryDH = "SELECT "
		wq = ""
		for att in fragAttribName[fragTypes['DHor']]:
			queryDH += (att+", ")
			if att in wheres:
				wq += FormWhereQueries(whereop[att], att, wherecond[att])
				wq += " and "

		queryDH = queryDH[:-2]
		queryDH += " FROM ";
		queryDH += fragTypes['DHor'];
		if wq != "":
			queryDH += " WHERE "
			queryDH += wq[:-4]
			queryDH += ";"

		if len(wheres) == 0 or DHOR_CONDITION not in wheres:
			print("Need to perform queries for Derived horizontal Frag on all sites")
			for siteId in Sites['DHor']:
				if siteId not in QuerySites:
					QuerySites[siteId] = []
				QuerySites[siteId].append(queryDH)
			print("Query ==>",queryDH)
			
		else:
			condition = wherecond[DHOR_CONDITION]
			
			if not (isinstance(condition, str) or isinstance(condition, int)):
				print("The query has wrong brackets for a string\nplease rectify")
				EXIT()
			query = "select FragmentId from DHorFragment where `condition` = '"+str(condition)+"';"

			cursor.execute(query)
			result = cursor.fetchall()
			try:
				fragId = result[0][0]
			except:
				print("Fragment doesn't exist \nexiting")
				EXIT()
			siteId = fragSites[fragId]
			print("Need to perform Derived horizontal frag query on a single site with ID",siteId)
			print("Query ==>",queryDH)
			if siteId not in QuerySites:
				QuerySites[siteId] = []
			QuerySites[siteId].append(queryDH)

	for i in range(2): print()
	# for i in range(130):
	# 	print('#',end='',flush=True)
		# time.sleep(0.005)
	# for i in range(5): print()
	# print("Printing final Query Tree (with optimisations)")
	# print()
	# for key, value in QuerySites.items():
	# 	print("Queries to run on Site with ID",key)
	# 	print(value)

	# for i in range(2): print()
	# for i in range(130):
	# 	print('#',end='',flush=True)
	# 	# time.sleep(0.005)
	# for i in range(5): print()

	# print("Printing jasonizable Query Tree (with optimisations)")
	# print()

	# for key, value in QuerySites.items():
	# 	print("Queries for Site with ID",key)
	# 	for val in value:
	# 		print(json.dumps(parse(val)))
	# print()

	cursor.close()
	conn.close()
	return QuerySites;
## close the connections
# cursor.close()
# conn.close()

