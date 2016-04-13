from py2neo import neo4j, node, rel

from .codecommon import db


class OG(object):
    " A generic class to hold properties "
    def __init__(self, __rel__=None, **kwargs):
        self.__dict__ = kwargs
        self.__rel__ = __rel__ or {}

    def tuple(self):
        return self.__dict__, self.__rel__

    def _relate(self, rel_type, obj):
        if rel_type not in self.__rel__:
            self.__rel__[rel_type] = set()
        self.__rel__[rel_type].add(obj)


def datatree_to_node_rel(data_tree):
    ''' Returns a list of nodes data and a list of relationships:
        [node data, ], [(parent id, rel type, child id), ]
        Ids are indexes in the nodes list. 'rel type' is a string.
    '''
    nodes = []
    nodes_id = {}
    rels = []

    def filter_data(data):
        return {k: v for k, v in data.iteritems() if k[0] != '_'}

    def new_node(data):
        nid = nodes_id.get(id(data))
        if nid is not None:
            return nid, False  # Has already been processed
        if hasattr(data, '__node__'):
            nid = data.__node__  # Has a node in the db
        else:
            nodes.append(filter_data(data))  # Will create in new node
            nid = len(nodes) - 1  # id within the batch request
        nodes_id[id(data)] = nid
        return nid, True  # Created

    def new_rel(this_id, link_type, child_id):
        rels.append((this_id, link_type, child_id))
        return len(rels) - 1

    def walk(tree):
        data, links = tree.tuple()
        this_id, new = new_node(data)

        if new:
            for link_type, children in links.items():
                for child in children:
                    child_id = walk(child)
                    new_rel(this_id, link_type, child_id)

        return this_id
    walk(data_tree)
    return nodes, rels


def insert_tree(tree, label=None):
    nodes, rels = datatree_to_node_rel(tree)
    ret = db.create(*(
        list(map(node, nodes))
        +
        list(map(rel, rels))
    ))
    # Label the nodes
    if label:
        batch = neo4j.WriteBatch(db)
        for n in ret:
            if isinstance(n, neo4j.Node):
                batch.add_labels(n, label)
        batch.submit()
    return ret
