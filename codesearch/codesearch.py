# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>
from .codecommon import (
    ex_query, test_files, normalize_name,
)


# <codecell>
# Get the relevant source code
def get_ctx(nodes, size=0):
    " Get line numbers surrounding the nodes"
    nos = set()
    for n in nodes:
        no = n['lineno']
        nend = n['lineend'] or no
        no = no or nend
        if no:
            nos.update(range(no - 1 - size, nend + size))
    return sorted(nos)


def get_snippet(lines, nos):
    ' Make a text snippet from line numbers '
    return '\n'.join(map(lines.__getitem__, nos))

def get_num_lines(lines, nos):
    ' Make [(no, line), ..] from line numbers '
    return [(no, lines[no]) for no in nos]


def load(
    source_files=test_files,
):
    file_lines = {}
    for source_file in source_files:
        with open(source_file) as fd:
            source = fd.read()

        file_lines[source_file] = source.splitlines()
    return file_lines


# Find the definition of a name in a parent scope of a node (by id)
q_node_def = '''
start use=node(%i)
match path =
    (use) <-[*..20]- (scope {scope: True}) -[rdefs *0..6]-> (def)
    where "%s" in def.defs
    // Rewrite this with shortestPath?
    and none(rdef in rdefs where exists(endNode(rdef).scope) and endNode(rdef) <> def)
return def, scope, path
'''


def find_def_by_id_old(nid, name):
    norm = normalize_name(name)
    return ex_query(q_node_def % (nid, norm))


# Find the next use of a name in a parent scope of a node (by id)
q_use_from_def = '''
start def=node(%i)
match path =
    (use) <-[*..20]- (scope {scope: True}) -[rdefs *0..6]-> (def)
    where "%s" in use.uses
    and use.lineno > def.lineno
    // Rewrite this with shortestPath?
    and none(rdef in rdefs where exists(endNode(rdef).scope) and endNode(rdef) <> def)
return use, scope, path order by use.lineno limit 1
'''


def find_use_from_def_old(nid, name):
    norm = normalize_name(name)
    return ex_query(q_use_from_def % (nid, norm))


# Find named attributes (or key in a container). Dependency: their parent or container.
q_attr = '''
match path = (use:code {attr: "%s"}) --> (def:code)
match (file)-[*]->(use) where exists(file.filename)
return file, use.attr as name, use, def, path
'''

def find_attr(attr):
    norm = attr
    # norm = normalize_name(attr)  # XXX Should normalize/index attr in the db
    return ex_query(q_attr % (norm))

# Find external names (import). Dependency: file or package where it is defined.
# TODO

# <codecell>

# Find friends (named entities in the same statement as a node). Stop at the statement level.
q_friends = '''
start center=node(%i)
match path = (center)-[rels *1..%i]-(n)
where none(r in rels where exists(startNode(r).stmt))
return n, length(path) as len
'''


def find_friends_by_id_old(nid, depth=10):
    return ex_query(q_friends % (nid, depth))


# <codecell>

# Find named products of an expression (definition of names by the
# parent statement):
# - target name
# - function that returns it or use it as default value
# - class that contains it or derives from it
# Getting parent statements that define names (direct or tuple assignement)
# XXX A bit specific with the return exception
# XXX Could be simpler based on line numbers (find the path afterwards)
# XXX sort and limit
q_products = '''
start n=node(%i)
match path =
    (n) <-[ups *0..%i]- (stmt {stmt: true}) -[downs *0..2]-> (def)
    where exists(def.defs)
    and none(r in ups where exists(endNode(r).stmt) and endNode(r).ntype <> "Return")
    and none(r in downs where exists(endNode(r).stmt))  // Maybe unnecessary
return def, stmt, path limit 1
'''


def find_products_by_id_old(nid, depth=3):
    return ex_query(q_products % (nid, depth))


# <codecell>

# Find code execution (effects of the parent statement)
# - block of code (if, for, while) executed or not because of it
# - function call using it as argument


from .codeexplore import (
    find_path_def_use,
    find_prod_by_id,
    find_friends_by_id,
)

CTX_LINES = 0

# Format the database results
def make_code(nodes):
    return get_ctx(nodes, size=CTX_LINES)


def render_node_path(name, node, path=None):
    out = {
        'id': node._id,
        'type': node['ntype'],
        'name': name,
        'lines': make_code((node, )),
    }
    if path:
        out['path'] = make_code(path.nodes[1:])
    return out


def render_all_nodes(nodes):
    return [
        render_node_path(sname, stmt, path)
        for sname, stmt, path in nodes
    ]

# Search by name, find other members of the same expression, all definitions,
# and the direct product
# XXX Should care more about external names and attributes on them


def search_deep(name):
    out = {}
    res_name = find_path_def_use(name)
    res_attr = find_attr(name)
    res_both = list(res_name) + list(res_attr)
    out['summary'] = '%s names, %s attributes' % (
        len(res_name), len(res_attr))

    out2 = []
    out['results'] = out2
    for row in res_both:
        out3 = {}
        out2.append(out3)

        out3['name'] = name = row['name']
        out3['filename'] = row['filename']
        out3['project'] = row['project']

        out3['defs'] = [
            render_node_path(name, node, path)
            for node, path in row['allDef']]

        out3['uses'] = uses = []
        for use, use_path in row['allUse']:
            friends = []
            products = []
            # Looking for friends
            friends.extend(find_friends_by_id(use._id, myname=name))
            # Looking for products
            products.extend(find_prod_by_id(use._id))

            use_data = render_node_path(name, use, use_path)
            use_data['hels'] = render_all_nodes(friends)
            use_data['pros'] = render_all_nodes(products)
            uses.append(use_data)

    return res_both, out
