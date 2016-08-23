from .codecommon import (
    ex_query, normalize_name,
)

#### Search ####
def find_by_filemeta(meta):
    return ex_query('''
        MATCH (m :code)
        USING INDEX m:code(filename)
        WHERE
            m.schema_rev = { schema_rev } AND
            m.project = { project } AND
            m.version = { version } AND
            m.filename = { filename }
        RETURN m
        ''', **meta)


# Find uses and definitions of named entities. Scope-aware
# XXX Make a union, names or attr

q_path_scope = '''
MATCH
  (nn :code)-[:scope]->(scope),
  (scope)<-[:body *0..5]-(file :code)
USING INDEX nn:code(nname)
WHERE
    nn.nname = { nname } AND
    exists(file.filename)
WITH file, nn, scope
  MATCH (nn)<-[:defs]-(def)
  OPTIONAL MATCH
    pDef = shortestPath((def)<-[*..4]-(scope))
WITH file, nn, scope, collect(distinct [def, pDef]) AS allDef
  MATCH (nn)<-[:uses]-(use)
  OPTIONAL MATCH
    pUse = shortestPath((use)<-[*..4]-(scope))
RETURN file.filename AS filename, file.project AS project,
       nn, nn.name AS name,
       allDef, collect(distinct [use, pUse]) AS allUse
LIMIT { limit }
'''

def find_path_def_use(name, limit=4):
    norm = normalize_name(name)
    return ex_query(q_path_scope, nname=norm, limit=limit)


#### More definitions ####
q_def_by_id = '''
START s=node({ sid })
MATCH (s)-[:uses]->(name)<-[:defs]-(found),
      (name)-[:scope]->(scope)
OPTIONAL MATCH
  path = shortestPath((found)<-[*..4]-(scope))
RETURN name.name AS name, found as def, path
'''

def find_def_by_id(sid):
    return ex_query(q_def_by_id, sid=sid)

#### More products ####
q_prod_by_id = '''
START s=node({ sid })
MATCH (s)-[:defs]->(name)<-[:uses]-(found),
      (name)-[:scope]->(scope)
OPTIONAL MATCH
  path = shortestPath((found)<-[*..4]-(scope))
RETURN name.name AS name, found as prod, path
'''

def find_prod_by_id(sid, limit=4):
    return ex_query(q_prod_by_id, sid=sid)

#### More friends ####
q_friends_by_id = '''
START s=node({ sid })
MATCH (s)-[:uses]->(name)<-[:defs]-(found),
      (name)-[:scope]->(scope)
WHERE name.name <> { myname }
OPTIONAL MATCH
  path = shortestPath((found)<-[*..4]-(scope))
RETURN name.name AS name, found as friend, path
'''

def find_friends_by_id(sid, myname, depth=10):
    return ex_query(q_friends_by_id, sid=sid, myname=myname)


#### More ####
def find_use_from_def(nid, name):
    return []
