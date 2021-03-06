# This is a simple script that plots the in-/out-degree of entities before and
# after integration

from hdt import HDTDocument, IdentifierPosition
import networkx as nx
from collections import Counter
import matplotlib.pyplot as plt
from collections import Counter
import networkx.algorithms.distance_measures as dm
import random

owl_sameas = "http://www.w3.org/2002/07/owl#sameAs"
skos_exactMatch = "http://www.w3.org/2004/02/skos/core#exactMatch"
skos_broadMatch = "http://www.w3.org/2004/02/skos/core#broadMatch"
skos_broader = "http://www.w3.org/2004/02/skos/core#broader"
skos_narrowMatch = "http://www.w3.org/2004/02/skos/core#narrowMatch"
skos_narrower = "http://www.w3.org/2004/02/skos/core#narrower"
skos_relatedMatch = "http://www.w3.org/2004/02/skos/core#relatedMatch"
skos_closeMatch = "http://www.w3.org/2004/02/skos/core#closeMatch"
subPropertyOf = 'http://www.w3.org/2000/01/rdf-schema#subPropertyOf'
inv = 'http://www.w3.org/2002/07/owl#inverseOf'


collect_big_in = {}
collect_big_out = {}

fig, axs = plt.subplots(2)
# axs[0].set_title('in-degree')
# axs[1].set_title('out-degree')
fig.set_figwidth(6)
fig.set_figheight(10)

# files = ['fibo-skos', 'fibo-owl', 'fro', 'hfr', 'lkif', 'bro', 'figi', 'stw', 'stw-mappings', 'jel', 'fund']
files = ['saref4bldg', 'iot-lite', 'km4city-1.6.7',  'schema-org',   'PipeOntology',  'RoadOntology',  'GroundOntology',
 'Smart_City_Ontology_2.0', 'empathi', 'resilience_extended']
# files = ['fibo-vD', 'fibo-owl', 'fro', 'hfr', 'lkif', 'bro', 'figi', 'stw', 'jel', 'fund', 'stw-mapping', 'my_mapping']
kg_name = {'saref4bldg':'SAREF', 'iot-lite':'IOT Lite', 'km4city-1.6.7':'KM4City', 'schema-org':'Schema.org', 'PipeOntology':'PipeOntology', 'RoadOntology':'RoadOntology', 'GroundOntology':'GroundOntology', 'Smart_City_Ontology_2.0':'SCO2.0',
 'empathi':'Empathi', 'resilience_extended':'Extension'}
in_degree_map = {}
out_degree_map = {}

combi = set()

markers = ["." , "," , "o" , "v" , "^" , "<", ">"]
colors = ['g','b','c','m', 'y', 'k']

for file in files:
	path_to_file = file+'.hdt'
	hdt_kg = HDTDocument(path_to_file)
	triples, cardinality = hdt_kg.search_triples("", "", "")
	entities = set()
	g = nx.DiGraph()
	ct_in = Counter()
	ct_out = Counter()
	for s, p, o in triples:
		if str(s)[0] != '"' and not (str(s)[0] == '_' and str(s)[1] == ':'):
			entities.add(s)
		# else:
			# print ('Subject - not an entity but a string/number',s)

		if str(o)[0] != '"'  and not (str(o)[0] == '_' and str(o)[1] == ':'):
			entities.add(o)
		# else:
			# print ('Object - not an entity but a string/number',o)
			g.add_edge(s, o)

	print ('\n\nKG ', file, 'has ', cardinality, 'triples')
	print ('\t with ', len (entities), ' entities')
	try:
		print ('\t diameter = ', dm.diameter(g))
	except Exception as e:
		print ('\t diameter = infinite')

	for n in g.nodes():
		d = g.in_degree(n)
		ct_in[d] += 1
		if d > 1000:
			collect_big_in[n] = d
		d = g.out_degree(n)
		ct_out[d] += 1
		if d > 70:
			collect_big_out[n] = d
	print ('in: ',ct_in)
	print ('out:', ct_out)
	color = random.choice(colors)
	shape = random.choice(markers)
	while (color, shape) in combi:
		color = random.choice(colors)
		shape = random.choice(markers)
	combi.add((color,shape))
	# in
	x = ct_in.keys()
	y = ct_in.values()
	axs[0].scatter(x, y, alpha = 0.4, label=kg_name[file], marker=shape, color=color)
	print ('max in = ', max(x))
	# out
	x = ct_out.keys()
	y = ct_out.values()
	axs[1].scatter(x, y, alpha = 0.4, label=kg_name[file], marker=shape, color=color)
	print ('max out = ', max(x))



print ('\n\n----------INTEGRATED----------\n')

path_to_file = './integrated.hdt'
hdt_kg = HDTDocument(path_to_file)
triples, cardinality = hdt_kg.search_triples("", "", "")
entities = set()



g = nx.DiGraph()
ct_in = Counter()
ct_out = Counter()
for s, p, o in triples:
	if str(s)[0] != '"'  and not (str(s)[0] == '_' and str(s)[1] == ':') :
		entities.add(s)
	# else:
		# print ('Subject - not an entity but a string/number',s)

	if str(o)[0] != '"' and not (str(o)[0] == '_' and str(o)[1] == ':'):
		entities.add(o)
	# else:
		# print ('Object - not an entity but a string/number',o)
		g.add_edge(s, o)

	# if "hasImpactOn" in str(o):
	# 		print (s, p, o)

print ('\n\nKG ', file, 'has ', cardinality, 'triples')
print ('\t with ', len (entities), ' entities')
try:
	print ('\t diameter = ', dm.diameter(g))
except Exception as e:
	print ('\t diameter = infinite')

for n in g.nodes():
	d = g.in_degree(n)
	ct_in[d] += 1
	if d > 200:
		collect_big_in[n] = d
	d = g.out_degree(n)
	ct_out[d] += 1
	if d > 500:
		collect_big_out[n] = d

print ('in: ',ct_in)
print ('out:', ct_out)

# in
x = ct_in.keys()
y = ct_in.values()
axs[0].scatter(x, y, alpha = 0.5, label='integrated', color='r')
# out
x = ct_out.keys()
y = ct_out.values()
axs[1].scatter(x, y, alpha = 0.5, label='integrated' , color='r')

print ('the integrated KG has ', cardinality, 'triples')
print ('\t with ', len (entities), ' entities')


axs[0].spines['top'].set_visible(False)
axs[0].spines['right'].set_visible(False)
axs[1].spines['top'].set_visible(False)
axs[1].spines['right'].set_visible(False)
axs[0].autoscale(tight=True)
axs[0].legend()
axs[1].autoscale(tight=True)
axs[1].legend()

axs[1].set_yscale('log')
axs[1].set_xscale('log')
axs[0].set_yscale('log')
axs[0].set_xscale('log')

axs[0].set_xlabel('in-degree')
axs[0].set_ylabel('frequency')
axs[1].set_xlabel('out-degree')
axs[1].set_ylabel('frequency')

plt.savefig('degree.png', bbox_inches='tight', dpi = 300)

# plt.show()
collect_big_in = {k: v for k, v in sorted(collect_big_in.items(), key=lambda item: item[1])}
for n in collect_big_in.keys():
	print (n, ' has in-degree ', collect_big_in[n])

collect_big_out = {k: v for k, v in sorted(collect_big_out.items(), key=lambda item: item[1])}
for n in collect_big_out.keys():
	print (n, ' has out-degree ', collect_big_out[n])
	# triples, cardinality = hdt_kg.search_triples(n, "", "")
	# l = 0
	# for s,p,o in triples:
	# 	p = str(p)
	# 	if 'definition' in p or 'label' in p:
	# 		print (n, p, o)
	# 	l += 1
	# 	if l > 20:
	# 		break
