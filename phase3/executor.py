from moz_sql_parser import parse
import mysql.connector
import numpy as np
import os
import json
import time
from decomposer import Decomposer

def EXIT():
	cursor.close()
	conn.close()
	exit(0)


HOR_CONDITION = 'city'
DHOR_CONDITION = 'reserveId'

def operation(arr, op):
	arr = np.array(arr)
	if op == 'SUM':
		return np.sum(arr)
	if op == 'MIN':
		return np.min(arr)
	if op == 'MAX':
		return np.max(arr)
	if op == 'AVG':
		return np.mean(arr)

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

if isinstance(parse_tree['from'], str):
	relations.append(parse_tree['from'])
else :
	for rel in parse_tree['from']:
		relations.append(rel)


if isinstance(parse_tree['select'], list):
		for i in parse_tree['select']:
			if isinstance(i['value'], str):
				selects.append(i['value'])
			else:
				for temp in i['value']:
					aggs[temp] = i['value'][temp]
					attribToAggs[i['value'][temp]] = temp
					# selects.append(i['value'][temp])
else:
	if isinstance(parse_tree['select']['value'], str): 
		selects.append(parse_tree['select']['value'])
	else:
		for temp in parse_tree['select']['value']:
			if temp not in aggs:
				aggs[temp] = []
			aggs[temp].append(parse_tree['select']['value'][temp])
			attribToAggs[parse_tree['select']['value'][temp]] = temp



if 'groupby' not in parse_tree and len(aggs)!=0:
	print("Error with query\nLooking for groupby but couldn't find it")
	exit(0)

if isinstance(parse_tree['groupby'], list):
	for val in parse_tree['groupby']:
		groupby.append(val['value'])
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
print('havingcond =>', havingcond)

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
print('RelationToFragmentIds  =>', RelationToFragmentIds)

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
print('AttribIdToAttrib =>',AttribIdToAttrib)

QueryForSite = {}


# need to include and & or as well
if 'Hor' in FragmentTypeToId:
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

if 'DHor' in FragmentTypeToId:

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
	queryH += gb[:-2] ;


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

if 'Ver' in FragmentTypeToId:
	siteIdToAttrib = {}

	for fragId in FragmentTypeToId['Ver']:
		for attribId in AttribIdToAttrib:
			query = "SELECT * FROM VerFragment WHERE FragmentId = " + str(fragId) + " and AttributeId = " + str(attribId)
			cursor.execute(query)
			res = cursor.fetchall()
			if len(res)!=0:
				siteId = FragmentIdToSite[fragId]
				if siteId not in siteIdtoattrib:
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
		for attId in siteIdtoattrib[flagId]:
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
		queryV += gb[:-2] ;

		if Hq != "":
			queryV += " Having " + Hq[:-4] + ";"

		print("query ===>", queryV)

		if flagId not in QueryForSite:
			QueryForSite[flagId] = []
		QueryForSite[flagId].append(queryV)