from elasticsearch import Elasticsearch

es = Elasticsearch()

with open('out.csv', 'r') as datafile:
    lines = datafile.read().split('\n')
    lines = [l for l in lines if l]
    for line in lines:
        exercise, date, weight = line.split(',')   
        print 'date: %s' % date 
        doc = {
            'date': date,
            'exercise': exercise.lower(),
            'weight': weight
        }

        res = es.index(index="lifts",doc_type="lifting_set",body=doc)
        print res['result']

es.indices.refresh(index="lifts")


