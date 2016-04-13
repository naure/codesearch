# <codecell>
from py2neo import neo4j

# XXX put db and index creation in a function
db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

SCHEMA_REV = 1


def assert_tree(tree):
    data, links = tree.tuple()
    assert isinstance(data, dict), data
    assert isinstance(links, dict), links


def ex_query(q, **params):
    return neo4j.CypherQuery(db, q).execute(**params)


def first_to_dict(res):
    return res[0][0].get_properties()


# Label index
for prop in ['nname', 'nattr', 'ext_name_n', 'filename', ]:
    try:
        db.schema.create_index('code', prop)
    except ValueError as e:
        pass  # print str(e)

# Lucene index: idx = db.get_or_create_index(neo4j.Node, 'names')

# <codecell>
# Tokenizer
import re
RE_TOKEN_SEP = re.compile(r'[^\w-]+')
RE_TOKEN_DEL = re.compile(r'[_-]+')


def normalize_name(name):
    return RE_TOKEN_DEL.sub('', name).lower()


def tokenize(name):
    return [normalize_name(token) for token in RE_TOKEN_SEP.split(name)]


test_files = [
    'data/example.py',
    'data/example_django.py',
    'data/example_view.py',
    'data/example_mini.py',
]
