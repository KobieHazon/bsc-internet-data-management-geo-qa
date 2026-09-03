import rdflib

wiki_dom = "https://en.wikipedia.org/"

query1 = "select (COUNT(DISTINCT ?pm) as ?pm_count) where {?country <" + wiki_dom + "prime_minister> ?pm}"

query2 = "select (count(?country) as ?country_count) where { \
?country <" + wiki_dom + "capital> ?capital }"

query3 = "select (count(?country) as ?country_count) where { \
?country <" + wiki_dom + "government> ?government. \
FILTER CONTAINS(LCASE(str(?government)), \"republic\") }"

query4 = "select (count(?country) as ?country_count) where { \
?country <" + wiki_dom + "government> ?government. \
FILTER CONTAINS(LCASE(str(?government)), \"monarchy\") }"

g = rdflib.Graph()
g.parse("ontology.nt", format="nt")
print("#############################################################")
print("query1:")
print(list(g.query(query1))[0]['pm_count'])
print("query2:")
print(list(g.query(query2))[0]['country_count'])
print("query3:")
print(list(g.query(query3))[0]['country_count'])
print("query4:")
print(list(g.query(query4))[0]['country_count'])
