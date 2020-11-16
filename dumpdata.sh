python3 manage.py dumpdata core.document core.tag > documents.json
python3 manage.py dumpdata core.topic core.keyword core.topicmodel > topics.json
python3 manage.py dumpdata core.originaltopicprobabilities > probabilities.json