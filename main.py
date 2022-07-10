# This is a Python script for the analysis of each individual knowledge graph and
# the integrated knowledge graph.
# More specifically, we study how the triples regarding the 10 relations works
# during the integration of 11 files from 9 ontologies.
# -----
# A plot of the connected components of skos:exactMatch is exported as
# connected_components_frequency.png
from hdt import HDTDocument, IdentifierPosition
import networkx as nx
from collections import Counter
import matplotlib.pyplot as plt


owl_sameas = "http://www.w3.org/2002/07/owl#sameAs"
owl_equivalentClass = "http://www.w3.org/2002/07/owl#equivalentClass"
skos_exactMatch = "http://www.w3.org/2004/02/skos/core#exactMatch"
skos_broadMatch = "http://www.w3.org/2004/02/skos/core#broadMatch"
skos_broader = "http://www.w3.org/2004/02/skos/core#broader"
skos_narrowMatch = "http://www.w3.org/2004/02/skos/core#narrowMatch"
skos_narrower = "http://www.w3.org/2004/02/skos/core#narrower"
skos_relatedMatch = "http://www.w3.org/2004/02/skos/core#relatedMatch"
skos_closeMatch = "http://www.w3.org/2004/02/skos/core#closeMatch"
lkif_eq = 'http://www.estrellaproject.org/lkif-core/norm.owl#strictly_equivalent'
rdfs_subClassOf = "http://www.w3.org/2000/01/rdf-schema#subClassOf"
files = ['saref4bldg', 'iot-lite', 'km4city-1.6.7',  'schema-org',   'PipeOntology',  'RoadOntology',  'GroundOntology',
 'Smart_City_Ontology_2.0', 'empathi', 'resilience_extended']

# owl:equivalentClass

for file in files:
	path_to_file = file+'.hdt'
	hdt_kg = HDTDocument(path_to_file)
	triples, cardinality = hdt_kg.search_triples("", "", "")
	entities = set()
	for s, p, o in triples:
		if str(s)[0] != '"' and str(s)[0] != '_' and str(s)[1] != ':':
			entities.add(s)
		# else:
			# print ('Subject - not an entity but a string/number',s)

		if str(o)[0] != '"' and str(s)[0] != '_' and str(s)[1] != ':':
			entities.add(o)
		# else:
			# print ('Object - not an entity but a string/number',o)
	print ('\n\nKG ', file, 'has ', cardinality, 'triples')
	print ('\t with ', len (entities), ' entities')

	#owl_equivalentClass
	triples, cardinality = hdt_kg.search_triples("", owl_equivalentClass, "")
	print ('owl:equivalentClass ', cardinality)

	# owl:sameAs
	triples, cardinality = hdt_kg.search_triples("", owl_sameas, "")
	print ('owl:sameAs ', cardinality)

	# skos:exactMatch
	triples, cardinality = hdt_kg.search_triples("", skos_exactMatch, "")
	print ('skos:exactMatch ', cardinality)


	# skos:broadMatch
	triples, cardinality = hdt_kg.search_triples("", skos_broadMatch, "")
	print ('skos:broadMatch ', cardinality)

	# skos:broader
	triples, cardinality = hdt_kg.search_triples("", skos_broader, "")
	print ('skos:broader ', cardinality)

	# skos:narrowMatch
	triples, cardinality = hdt_kg.search_triples("", skos_narrowMatch, "")
	print ('skos:narrowMatch ', cardinality)

	# skos:narrower
	triples, cardinality = hdt_kg.search_triples("", skos_narrower, "")
	print ('skos:narrower ', cardinality)

	# skos:closeMatch
	triples, cardinality = hdt_kg.search_triples("", skos_closeMatch, "")
	print ('skos:closeMatch ', cardinality)

	# skos:relatedMatch
	triples, cardinality = hdt_kg.search_triples("", skos_relatedMatch, "")
	print ('skos:relatedMatch ', cardinality)

	# lkif_eq
	triples, cardinality = hdt_kg.search_triples("", lkif_eq, "")
	print ('lkif:eq ', cardinality)

	# subClassOf
	triples, cardinality = hdt_kg.search_triples("", rdfs_subClassOf, "")
	print ('rdfs:subClassOf ', cardinality)


print ('\n\n----------INTEGRATED----------\n')




path_to_file = './integrated.hdt'
hdt_kg = HDTDocument(path_to_file)
triples, cardinality = hdt_kg.search_triples("", "", "")
entities = set()
for s, p, o in triples:
	if str(s)[0] != '"' and str(s)[0] != '_' and str(s)[1] != ':':
		entities.add(s)
	# else:
		# print ('Subject - not an entity but a string/number',s)

	if str(o)[0] != '"' and str(s)[0] != '_' and str(s)[1] != ':':
		entities.add(o)
	# else:
		# print ('Object - not an entity but a string/number',o)
print ('the integrated KG has ', cardinality, 'triples')
print ('\t with ', len (entities), ' entities')
# owl:sameAs
triples, cardinality = hdt_kg.search_triples("", owl_sameas, "")
print ('owl:sameAs ', cardinality)
