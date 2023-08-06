import unittest
from easysparql import easysparql

ENDPOINT = "https://dbpedia.org/sparql"
albert_uri = "http://dbpedia.org/resource/Albert_Einstein"
albert_name = "Albert Einstein"
scientist = "http://dbpedia.org/ontology/Scientist"
foaf_name = "http://xmlns.com/foaf/0.1/name"


class TestEasySPARQL(unittest.TestCase):

    def test_get_entities(self):
        entities = easysparql.get_entities(subject_name=albert_name, endpoint=ENDPOINT, language_tag="@en")
        self.assertGreater(len(entities), 0, 'No entities are returned')

    def test_get_classes(self):
        classes = easysparql.get_classes(entity_uri=albert_uri, endpoint=ENDPOINT)
        self.assertGreater(len(classes), 0, 'No classes are returned')

    def test_parents_of_class(self):
        parents = easysparql.get_parents_of_class(class_uri=scientist, endpoint=ENDPOINT)
        self.assertGreater(len(parents), 0, 'No parents are returned')

    def test_get_subjects(self):
        subjects = easysparql.get_subjects(class_uri=scientist, endpoint=ENDPOINT)
        self.assertGreater(len(subjects), 0, 'No subjects are returned')

    def test_subject_properties(self):
        properties = easysparql.get_properties_of_subject(subject_uri=albert_uri, endpoint=ENDPOINT)
        self.assertGreater(len(properties), 0, 'No properties are returned')

    def test_property_count(self):
        num = easysparql.get_property_count(subject_uri=albert_uri, property_uri=foaf_name, endpoint=ENDPOINT)
        self.assertGreater(num, 0, 'No name is found')


if __name__ == '__main__':
    unittest.main()
