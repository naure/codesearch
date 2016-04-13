from .codecommon import (
    ex_query,
)


# <codecell>
# Search by name, then by simple proximity
q_around = '''
start center=node(%i)
match (center)-[*0..%i]-(n)
return n
'''


def get_neighbors(node, depth=1):
    return [row[0] for row in ex_query(q_around % (node._id, depth))]


q_parents_children = '''
start center=node(%i)
match (p)-[*0..%i]->(center)-[*0..%i]->(c)
return p, c
'''


def get_lineage(node, depth=1):
    " Return parents and children "
    " XXX Returns duplicates "
    lineage = []
    for row in ex_query(q_parents_children % (node._id, depth, depth)):
        if row[0]:
            lineage.append(row[0])
        if row[1]:
            lineage.append(row[1])
    return lineage


# Search for a name, its definition, its neighbors, and print results
def search(name, ctx_lines=1):
    from .utils import *

    file_lines = load()

    res = find_path_def_use(name)
    print(red('%s results for "%s"' % (len(res), name)))
    for i, row in enumerate(res):
        filename = row['file']['filename']
        lines = file_lines[filename]
        defi = row['def']
        use = row['use']
        path = row['path']
        around_def = get_neighbors(defi, depth=1) if defi else []
        around_use = get_neighbors(use, depth=2) if use else []
        path_nodes = path.nodes if path else []
        #around_path = reduce(list.__add__, map(get_neighbors, path_nodes, [1] * len(path_nodes)))

        print('\n%s) %s' % (i + 1, use))
        print(red('---- Definition context ----'))
        print(highlight(get_snippet(lines, get_ctx(
            around_def, size=ctx_lines)), name))
        print()
        print(red('---- Use context ----'))
        print(highlight(get_snippet(lines, get_ctx(
            around_use, size=ctx_lines)), name))
        print()
        print(red('---- Path context ----'))
        print(highlight(get_snippet(lines, get_ctx(
            path_nodes, size=ctx_lines)), name))
    return res
