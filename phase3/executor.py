from moz_sql_parser import parse
import mysql.connector
import os
import json
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
	user='pragun', password='letscode', host='localhost', database='Lonely')

cursor = conn.cursor()

print("Connection to mysql server established")

# res = Decomposer()
# print(res)


print("Enter your Query:")

input_query = input()

### Parsing and generatign jasonizable tree

print("Decomposing the query")

try:
	parse_tree = parse(input_query)
except:
	print("Error with query")
	exit(0)
# print("Initial Parse Tree")
print(parse_tree)

selects = []
aggs = {}
attribToAggs = {}
groupby = []
havingcond = {}
havingop = {}
having = []
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
			except:
				print("Error in join syntax")
				exit(0)


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
	exit(0)

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
			having.append(parse_tree['having'][res][0])
			havingcond[parse_tree['having'][res][0]] = parse_tree['having'][res][1]
			if isinstance(parse_tree['having'][res][1],dict):
				havingcond[parse_tree['having'][res][0]] = parse_tree['having'][res][1]['literal']

			havingop[parse_tree['having'][res][0]] = res
		else:
			for j in parse_tree['having'][res]:
				for key, value in j.items():
					having.append(value[0])
					havingcond[value[0]] = value[1]
					if isinstance(value[1], dict):
						havingcond[value[0]] = value[1]['literal']
					havingop[value[0]] = key



print('STEP 1 printing all the datastructrues after Parsing')
print('selects =>', selects)
print('aggs =>', aggs)
print('attribToAggs =>', attribToAggs)
print('relations =>', relations)
print('groupby =>', groupby)
print('having =>', having)
print('havingop =>', havingop)
print('havingcond =>', havingcond,end='\n\n\n')

# for H in having:
# 	if H not in groupby :
# 		print("Error in query having statement\nExiting")
# 		exit(0)
for S in selects:
	if S not in groupby or S in aggs:
		print("Error in query\nExiting")
		exit(0)


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
		exit(0)
	
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

QueryForSite = {}


# need to include and & or as well
if 'Hor' in FragmentTypeToId and 'Ver' in FragmentTypeToId:
	
	## finding sites for 'Hor'
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
				EXIT()
			siteId = FragmentIdToSite[fragId]		
			sitesHor.append(siteId)
		else:
			for fragId in FragmentTypeToId['Hor']:
				sitesHor.append(FragmentIdToSite[fragId])
		## finding sites for 'Ver'
		
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
			if len(siteIdToAttribVer[siteId]) == 1 and 'id' in siteIdToAttribVer[siteId]:
				continue
			sitesVer.append(siteId)
			if len(siteIdToAttribVer) == TotalAtt:
				sitesVer = []
				sitesVer.append(siteId)
				break
		if len(sitesVer) == 0:
			sitesVer.append(1)
	except Exception as e:
		print("Error while optimisng relations for semi join:")
		print(e)
	try:
		## Bringinn Hor to one place
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
			query+= str(att) + " "+ str(attribTypeHor[att]) + ", "
		query = query[:-2]
		query += ");"
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
			print(query)
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
			query +=  str(att) + " " + str(attribTypeVer[att]) +", "
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
		print("Error while transferring data for semi join")
		print(e)
	
	tempQ = input_query.replace(FragmentTypeToRelation['Hor'], 'TempHor')
	tempQ = tempQ.replace(FragmentTypeToRelation['Ver'], 'TempVer')
	print("Printing Q", tempQ)
	try:
		cursor.execute(tempQ)
		res = cursor.fetchall()
		for i in res:
			print(res)

		cursor.execute("DROP Table TempHor")
		cursor.execute("DROP Table TempVer")
		cursor.close()
		conn.close()
	except Exception as e:
		print("Error while executing final Query")
		print(e)

elif 'Hor' in FragmentTypeToId and 'DHor' in FragmentTypeToId:
	pass

elif 'Ver' in FragmentTypeToId and 'DHor' in FragmentTypeToId:
	pass

 
elif 'Hor' in FragmentTypeToId:
	print("For Horizontal Fragments")
	queryH = "SELECT "
	Hq = ""
	gb = " GROUP BY "
	for att in RelationToAttribs[FragmentTypeToRelation['Hor']]:
		
		if att in selects:
			queryH += (att+", ")
		elif att in attribToAggs:
			queryH += (attribToAggs[att] +"(" + att + "), ")
		if att in groupby:
			gb += (att+", ")
		if att in having:
			Hq += FormWhereQueries(havingop[att], att, havingcond[att])
			Hq += " and "

	queryH = queryH[:-2]
	queryH += " FROM " + FragmentTypeToRelation['Hor'];
	queryH += gb[:-2] ;


	if Hq != "":
		queryH += " Having "
		queryH += Hq[:-4]
		queryH += ";"

	if HOR_CONDITION in having:
		condition = havingcond[HOR_CONDITION]
		query = "select FragmentId from HorFragment where `condition` = '"+str(condition)+"';"
		cursor.execute(query)
		result = cursor.fetchall()
		try:
			fragId = result[0][0]
		except:
			print("Fragment doesn't exist \nexiting")
			EXIT()
		siteId = FragmentIdToSite[fragId]		
		print("Only need to perform Horizontal Fragment query on site with ID ", siteId)
		QueryForSite[siteId].append(queryH)

	else:
		print("Need to perform queries on all the Sites")

		for fragId in FragmentTypeToId['Hor']:
			siteId = FragmentIdToSite[fragId]
			if siteId not in QueryForSite:
				QueryForSite[siteId] = []
			QueryForSite[siteId].append(queryH)

	print(queryH)

elif 'DHor' in FragmentTypeToId:

	print("For Derived Horizontal Fragments")
	queryH = "SELECT "
	Hq = ""
	gb = " GROUP BY "
	for att in RelationToAttribs[FragmentTypeToRelation['DHor']]:
		
		if att in selects:
			queryH += (att+", ")
		elif att in attribToAggs:
			queryH += (attribToAggs[att] +"(" + att + "), ")
		if att in groupby:
			gb += (att+", ")
		if att in having:
			Hq += FormWhereQueries(havingop[att], att, havingcond[att])
			Hq += " and "

	queryH = queryH[:-2]
	queryH += " FROM " + FragmentTypeToRelation['DHor'];
	queryH += gb[:-2]


	if Hq != "":
		queryH += " Having "
		queryH += Hq[:-4]
		queryH += ";"

	print(queryH)
	if DHOR_CONDITION in having:
		condition = havingcond[DHOR_CONDITION]
		query = "select FragmentId from DHorFragment where `condition` = '"+str(condition)+"';"
		cursor.execute(query)
		result = cursor.fetchall()
		try:
			fragId = result[0][0]
		except:
			print("Fragment doesn't exist \nexiting")
			EXIT()
		siteId = FragmentIdToSite[fragId]		
		print("Only need to perform Derived Horizontal Fragment query on site with ID ", siteId)
		QueryForSite[siteId].append(queryH)
	else:
		print("Need to perform queries on all the Sites")

		for fragId in FragmentTypeToId['DHor']:
			siteId = FragmentIdToSite[fragId]
			if siteId not in QueryForSite:
				QueryForSite[siteId] = []
			QueryForSite[siteId].append(queryH)


# create siteIdtoattrib
# check if a single site suffices or need to take from multiple sites

elif 'Ver' in FragmentTypeToId:
	siteIdToAttrib = {}

	for fragId in FragmentTypeToId['Ver']:
		for attribId in AttribIdToAttrib:
			query = "SELECT * FROM VerFragment WHERE FragmentId = " + str(fragId) + " and AttributeId = " + str(attribId)
			cursor.execute(query)
			res = cursor.fetchall()
			if len(res)!=0:
				siteId = FragmentIdToSite[fragId]
				if siteId not in siteIdToAttrib:
					siteIdToAttrib[siteId] = []
				siteIdToAttrib[siteId].append(attribId)

	TotalAtt = len(RelationToAttribsId[FragmentTypeToRelation['Ver']])

	flagId = -1

	for siteId in siteIdToAttrib:
		if len(siteIdToAttrib) == TotalAtt:
			flagId = siteId
			break
	if flagId == -1:
		print("need to perform query on all sites")
		query = "SELECT id from Attributes WHERE RelationName="+str(FragmentTypeToRelation['Ver'])+" AttributeName='id'"
		cursor.execute(query)
		masterId = cursor.fetchall()[0][0]
		masterAtt = AttribIdToAttrib[masterId] 
		for siteId in siteIdToAttrib:
			print('FOR SITE with ID', siteId)
			if masterAtt not in siteIdToAttrib[siteId]:
				siteIdToAttrib[siteId].append(masterAtt)
			queryV = "SELECT "
			Hq = ""
			
			for attId in siteIdtoattrib[flagId]:
				att = AttribIdToAttrib[attId]
				
				queryV += (att+", ")
				if att in having:
					Hq += FormWhereQueries(havingop[att], att, havingcond[att])
					Hq += " and "

			queryV = queryV[:-2]
			queryV += " FROM " + FragmentTypeToRelation['Ver'];
			if Hq != "":
				queryV += " Having " + Hq[:-4] + ";"


			print("query ===>", queryV)
		



	else:
		print("Perform query on a single site with id ", flagId)
		queryV = "SELECT "
		Hq = ""
		gb = " GROUP BY "
		for attId in siteIdToAttrib[flagId]:
			att = AttribIdToAttrib[attId]
			if att in selects:
				queryV += (att+", ")
			elif att in attribToAggs:
				queryV += (attribToAggs[att] +"(" + att + "), ")
			if att in groupby:
				gb += (att+", ")
			if att in having:
				Hq += FormWhereQueries(havingop[att], att, havingcond[att])
				Hq += " and "
		queryV = queryV[:-2]

		queryV += " FROM " + FragmentTypeToRelation['Ver'];
		queryV += gb[:-2]

		if Hq != "":
			queryV += " Having " + Hq[:-4] + ";"

		print("query ===>", queryV)

		if flagId not in QueryForSite:
			QueryForSite[flagId] = []
		QueryForSite[flagId].append(queryV)

