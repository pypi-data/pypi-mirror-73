# easysparql
A python wrapper to easily query knowledge graphs with SPARQL

[![Build Status](https://ahmad88me.semaphoreci.com/badges/easysparql.svg)](https://ahmad88me.semaphoreci.com/projects/easysparql)
[![codecov](https://codecov.io/gh/oeg-upm/easysparql/branch/master/graph/badge.svg)](https://codecov.io/gh/oeg-upm/easysparql)


# Install

## via setuptools
```python setup.py ```

## via pip
```pip install easysparql```

## Run tests
```python -m unittest discover```

# Example
```
from easysparql import easysparql

DBPEDIA_ENDPOINT = "https://dbpedia.org/sparql"

albert_uri = "http://dbpedia.org/resource/Albert_Einstein"
albert_name = "Albert Einstein"
scientist = "http://dbpedia.org/ontology/Scientist"
foaf_name = "http://xmlns.com/foaf/0.1/name"


classes = easysparql.get_classes(albert_uri, DBPEDIA_ENDPOINT)

entities = easysparql.get_entities(albert_name, DBPEDIA_ENDPOINT, "@en")

parents = easysparql.get_parents_of_class(scientist, DBPEDIA_ENDPOINT)

query = "select distinct ?Concept where {[] a ?Concept} LIMIT 100"
results = easysparql.run_query(query, DBPEDIA_ENDPOINT)

subjects = easysparql.get_subjects(class_uri=scientist, endpoint=DBPEDIA_ENDPOINT)

properties = easysparql.get_properties_of_subject(subject_uri=albert_uri, endpoint=DBPEDIA_ENDPOINT)

num = easysparql.get_property_count(subject_uri=albert_uri, property_uri=foaf_name, endpoint=DBPEDIA_ENDPOINT)

```

