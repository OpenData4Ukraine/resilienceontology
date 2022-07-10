
import json
from pydoc import describe
# from xml.etree.ElementTree import Comment

from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SOSA, SSN, TIME, VOID, XMLNS, XSD
from rdflib import Graph, URIRef, Literal, BNode, Namespace

#description解析子函数
def getDesc(desc_str):
	obj = {}
	desc = desc_str.splitlines()
	for d in desc:
		if(len(d) != 0):
			l = d.split(":", 1)
			if(len(l) > 1):
				key = l[0].strip().replace("/", "_").replace(" ", "_") # 属性名替换空格和/为_(如'VIOLENCE LEVEL' -> 'VIOLENCE_LEVEL')
				value = l[1].strip()
				if(len(value) != 0):
					obj[key] = value
	return obj

#locate file
# file = '/home/angelaluty/WebstormProjects/MasterProject/data/geojson/russian-ukraine-monitor.geojson'
file = './russian-ukraine-monitor.geojson'
#file = 'russian-ukraine-monitor.geojson'

my_graph = Graph()
my_graph.bind("dct", DCTERMS)
my_graph.bind("rdfs", RDFS) # rdfs:comment
my_graph.bind("schema", SDO) # schema:Date   schema:Country  schema:City  schema:GeoCoordinates  schema:url   schema:State (state or province of a country)

my_graph.bind("geo", URIRef("http://www.w3.org/2003/01/geo/wgs84_pos#"))  # geo:lat   geo:long
GEO = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")

my_graph.bind("km4c", URIRef("http://www.disit.org/km4city/schema#"))  # km4c:Province   km4c:Weapons_and_ammunition
KM4C = Namespace("http://www.disit.org/km4city/schema#")


# print ('title is ', DCTERMS)

with open(file) as f:
	gj = json.load(f)
	# features = gj['type'][0]
	# print ('There are ', len(gj['geojson']['features']), ' entries')
	for e in gj['geojson']['features']:
		# print('keys are: ', e.keys())
		event_id = 0
		for f in ['id', 'type', 'geometry', 'properties']:
		# for f in e.keys():
			#id转换成知识图谱的格式，URIRef转换格式
			if f == 'id':
				event_id = URIRef('https://cs.vu.nl/resilience/event/' + str(e[f]))
				print ('=========================\n')
				print ('event_id : ' , event_id)

			if f == 'geometry':
				coordinates = e[f]['coordinates']
				my_graph.add((event_id, GEO.lat, Literal(str(coordinates[0]))))
				my_graph.add((event_id, GEO.long, Literal(str(coordinates[1]))))

			if f == 'properties':
				# print ('feature = properties')
				for g in e[f].keys(): # ['title', 'description', 'group', 'media_url', 'marker-color']:
					# print ('\t sub-feature = ',g, '\t->\t', e[f][g])
					if g == 'title':
						print ((event_id, DCTERMS.title, Literal(e[f][g])))
						# <https://cs.vu.nl/resilience#/event/3330938974> dct:title "12/05/2022 Increase in size of suspected mass graves in the Vynohradna cemetery east of Mariupol" .
						#加入图谱中
						my_graph.add((event_id, DCTERMS.title, Literal(e[f][g])))

					if g == 'media_url':
						print ((event_id, SDO.discussionUrl, URIRef(e[f][g])))
						my_graph.add((event_id, SDO.discussionUrl, URIRef(e[f][g])))

					#解析description
					if g == 'description':
						item = getDesc(e[f][g]) # 解析后的description
						# print ('description = ' , item)
						for key in item.keys(): # ['ENTRY', 'VIOLENCE_LEVEL', 'LINK', 'GEOLOCATION', 'BRIEF_DESCRIPTION', 'DATE', ...]
							# TODO
							if key == 'DATE':
								print (event_id, SDO.date, Literal(item[key]))
								my_graph.add((event_id, SDO.date, Literal(item[key])))
							if key == 'LINK':
								if(("http://" in item[key]) or ("https://" in item[key])):
									print (event_id, SDO.relatedLink, URIRef(item[key].split(" ", 1)[0]))
									my_graph.add((event_id, SDO.relatedLink, URIRef(item[key].split(" ", 1)[0])))
							if key == 'GEOLOCATION':
							# 	# print (key + ':' + Literal(item[key]))
								if(("http://" in item[key]) or ("https://" in item[key])):
									my_graph.add((event_id, SDO.URL, URIRef(item[key].split(" ", 1)[0])))
							if key == 'BRIEF_DESCRIPTION':
								# print (key + ':' + Literal(item[key]))
								my_graph.add((event_id, RDFS.comment, Literal(item[key])))
							if key == 'COORDINATES':
								# print (key + ':' + Literal(item[key]))
								my_graph.add((event_id, SDO.GeoCoordinates, Literal(item[key])))
							if key == 'COUNTRY':
								# print (key + ':' + Literal(item[key]))
								my_graph.add((event_id, SDO.Country, Literal(item[key])))
							if key == 'PROVINCE':
							# 	# print (key + ':' + Literal(item[key]))
								my_graph.add((event_id, KM4C.Province, Literal(item[key]))) # km4c:Province
							if key == 'DISTRICT':
							# 	# print (key + ':' + Literal(item[key]))
								my_graph.add((event_id, KM4C.District, Literal(item[key]))) # km4c:District
							if key == 'TOWN_CITY':
								# print (key + ':' + Literal(item[key]))
								my_graph.add((event_id, SDO.City, Literal(item[key])))
							if key == 'ARMS_MUNITION':
								# print (key + ':' + Literal(item[key]))
								my_graph.add((event_id, KM4C.Weapons_and_ammunition, Literal(item[key]))) # km4c:Weapons_and_ammunition

			# else:

				# print ('feature = ',f, ' -> ', e[f])

		# print ('=========================\n\n')

my_graph.serialize("output.ttl")
