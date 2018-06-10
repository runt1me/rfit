from elasticsearch import Elasticsearch

es = Elasticsearch()
res = es.indices.delete(index="lifts",ignore=[400,404])

print res