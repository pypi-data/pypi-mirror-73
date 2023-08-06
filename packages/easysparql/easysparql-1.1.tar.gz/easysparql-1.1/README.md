# easysparql
A python wrapper to easily query knowledge graphs with SPARQL


# Install

## via setuptools
```python setup.py ```

## via pip
```pip install easysparql```

# Example
```
from easysparql.easysparql import run_query, get_entities, get_classes

DBPEDIA_ENDPOINT = "https://dbpedia.org/sparql"

albert_uri = "http://dbpedia.org/resource/Albert_Einstein"
albert_name = "Albert Einstein"
scientist = "http://dbpedia.org/ontology/Scientist"

classes = get_classes(albert_uri, DBPEDIA_ENDPOINT)

entities = get_entities(albert_name, DBPEDIA_ENDPOINT, "@en")

query = "select distinct ?Concept where {[] a ?Concept} LIMIT 100"
results = run_query(query, DBPEDIA_ENDPOINT)

```
