
# <codecell>

from pypy.interpreter.pyparser import pyparse
from pypy.interpreter.astcompiler import ast
from pypy.interpreter.astcompiler.astbuilder import ast_from_node
from pypy.tool.pytest.objspace import TinyObjSpace

from .codecommon import normalize_name, assert_tree
from .ogm import OG

# <codecell>
# Source code to tree (AST)
space = TinyObjSpace()
pyparser = pyparse.PythonParser(space)
compile_info = pyparse.CompileInfo("<filename>", "exec")


def source_to_tree(source):
    parsetree = pyparser.parse_source(source, compile_info)
    tree = ast_from_node(space, parsetree, compile_info)
    return tree


# <codecell>
# Find nodes that define new names
def make_def_finders():

    # Class Definition
    def ClassDef(node, links):
        yield node.name

    # Function Definition
    def FunctionDef(node, links):
        yield node.name

    # Variable name (node.id)
    def Name(node, links):
        if (
            node.ctx == ast.Store or
            node.ctx == ast.AugStore or
            node.ctx == ast.Param
        ):
            yield node.id

    return locals()  # DRY

def_finders = make_def_finders()


# Find references to names
def make_ref_finders():
    # Direct reference by variable name (node.id)
    def Name(node, links):
        if node.ctx == ast.Load or node.ctx == ast.AugLoad:
            yield node.id

    return locals()  # DRY

ref_finders = make_ref_finders()


# Find references to attributes
def make_att_finders():
    # Reference by attribute (node.attr)
    def Attribute(node, links):
        if node.ctx == ast.Load or node.ctx == ast.AugLoad:
            yield node.attr

    return locals()

att_finders = make_att_finders()


# Find constants
def constNum(node):
    yield node.n


def constStr(node):
    yield node.s


# Caracteristics of nodes
def get_type(node):
    return type(node).__name__


def is_scope(node):
    return get_type(node) in ['Module', 'ClassDef', 'FunctionDef', 'Lambda']


def is_class(node):
    return get_type(node) == 'ClassDef'


def is_stmt(node):
    # XXX too specific, and `arguments` doesn't have a lineno.
    return isinstance(node, ast.stmt) or get_type(node) == 'arguments'

# <codecell>

''' Turn the tree into a data model
'''

DATA_FIELDS = [
    'id', 'name', 'attr', 'asname', 'module', 'level', 'op', 'ops', 'ctx',
    'nl', 'n', 's', 'lineno', 'col_offset',
]
LINK_FIELDS = [
    'value', 'target', 'test', 'iter', 'slice', 'dest', 'msg',
    'func',
    'globals', 'locals',
    'key', 'value', 'elt', 'arg',
    'left', 'right', 'operand',
    'context_expr', 'optional_vars',
    'type', 'inst', 'tback',
    'lower', 'upper', 'step',
    # Duplicates:
    'body', 'name', 'args',
]
LINK_SEQ_FIELDS = [
    'values', 'names', 'bases', 'body', 'targets',
    'keys', 'values', 'elts', 'generators', 'comparators',
    'orelse', 'decorator_list',
    'handlers', 'finalbody',
    'args', 'vararg', 'keywords', 'starargs', 'kwargs', 'defaults',
    'dims', 'ifs',
]
# XXX In the top-level class Expression (instead of Module), body is a simple
# reference -_- Also exec.body, call.args, excepthandler.name. Also
# Compare.ops is a list of numbers

# Since the naming is inconsistent, guess the kind of field at runtime
ALL_FIELDS = set(DATA_FIELDS + LINK_FIELDS + LINK_SEQ_FIELDS)


def node_to_data(node):
    ''' Extract type, data, link types and links from a node
        Convert the tree into a data tree:
            node =
                __dict__: {field: data}
                __rel__: {link_type: [node, ]}
    '''
    assert isinstance(node, ast.AST), 'Not an AST node'
    ntype = get_type(node)
    tree = OG()
    tree.ntype = ntype
    data = tree.__dict__
    links = tree.__rel__

    for field in ALL_FIELDS:
        value = getattr(node, field, None)
        if value:
            if isinstance(value, ast.AST):
                links[field] = [node_to_data(value)]
            elif isinstance(value, list) and isinstance(value[0], ast.AST):
                links[field] = [node_to_data(v) for v in value]
            else:
                data[field] = value

    def_find = def_finders.get(ntype)
    if def_find:
        defs = def_find(node, links)
        if defs:
            data['defs'] = defs

    ref_find = ref_finders.get(ntype)
    if ref_find:
        uses = ref_find(node, links)
        if uses:
            data['uses'] = uses

    att_find = att_finders.get(ntype)
    if att_find:
        atts = att_find(node, links)
        if atts:
            data['atts'] = atts

    if is_scope(node):
        data['scope'] = True

    if is_stmt(node):
        data['stmt'] = True

    return tree


def flatten_data(data_tree):
    " Extract a list of data of all nodes, ignoring relationships "
    data, links = data_tree.tuple()
    yield data
    for link_type, children in links.items():
        for child in children:
            for d in flatten_data(child):
                yield d


def simplify_tree(data_tree):
    """ Extract the names refered to by nodes, and make them nodes of their
        own, with defs/uses links.
    """
    assert_tree(data_tree)

    def is_import(data):
        return data['ntype'] in ['Import', 'ImportFrom']

    def is_func(data):
        return data['ntype'] == 'FunctionDef'

    def is_return(data):
        return data['ntype'] in ['Return', 'Yield']

    class Scope(dict):
        def __init__(self, stmt, parent=None):
            self.stmt = stmt
            self.parent = parent

        def find_scope(self, name):
            return (
                self if name in self else
                None if self.parent is None else
                self.parent.find_scope(name)
            )

        def get_scope(self, name):
            " Find in which scope `name` is defined or is to be defined "
            return self.find_scope(name) or self

    Module = lambda name: OG(
        ext_name=name,
        ext_name_n=normalize_name(name),
    )

    NameNode = lambda scopeStmt, name: OG(
        name=name,
        nname=normalize_name(name),
        __rel__={'scope': [scopeStmt]})

    AttrNode = lambda attr: OG(
        attr=attr,
        nattr=normalize_name(attr),
        __rel__={'attr_of': []})  # XXX Figure out the parent object if possible

    def create_name(scope, name):
        s = scope.get_scope(name)
        namenode = s.get(name)
        if namenode is None:
            namenode = NameNode(s.stmt, name)
            s[name] = namenode
        return namenode

    modules = {}

    def create_modules(scope, data, links):
        # Transform an import statement in a list: [(Local NameNode, External Module), ..]
        if 'module' in data:  # As in "from `module` import .."
            base_mod = data['module'] + '.'
        else:
            base_mod = ''  # import `name` [as `asname`]
        for name_data in links['names']:
            base_name = name_data.name.split('.', 1)[0]
            # The module that is external to the current file
            mod_name = base_mod + base_name
            mod = modules.get(mod_name)
            if not mod:
                mod = modules[mod_name] = Module(mod_name)
            # The alias or the root module goes into the current namespace
            namenode = create_name(
                scope,
                getattr(name_data, 'asname', None) or base_name)
            namenode._relate('module', mod)
            yield namenode, mod

    def rec(tree, parent_scope, parent_func=None):
        data, links = tree.tuple()

        stree = OG()
        sdata, slinks = stree.tuple()
        for k in ['ntype', 'scope', 'lineno', 'attr']:
            v = data.get(k)
            if v:
                sdata[k] = v

        # Scope-nodes create their own scope
        scope = Scope(stree, parent_scope) if 'scope' in data else parent_scope
        assert scope is not None, "The root of the tree must be a scope"

        # Lists of NameNodes: defined, used, and attributes
        defs, uses, atts = [], [], []
        # Link names used in this statement to `names` in the parent scope
        defs.extend([
            create_name(parent_scope, name)
            for name in data.get('defs', [])])

        uses.extend(
            create_name(parent_scope, name)
            for name in data.get('uses', []))

        # Entering a function ? Its NameNode is in `defs`
        func = defs if is_func(data) else parent_func

        # Returning from a function ? Link to the function's NameNode
        if is_return(data):
            defs.extend(func)

        # Import external names ?
        if is_import(data):
            exts = []
            for namenode, mod in create_modules(parent_scope, data, links):
                defs.append(namenode)
                exts.append(mod)
        else:
            exts = None

        # Collect children statements or merged data
        children_defs = set()
        children_uses = set()
        children_atts = set()
        lineend = data.get('lineno', 0)
        for link_type, children in links.items():
            children_stmt = []
            for child in children:
                if hasattr(child, 'stmt'):
                    # Include as child statement and its simplified subtree
                    children_stmt.append(
                        rec(child, scope, func))
                else:
                    # Merge all data in an expression
                    for child_data in flatten_data(child):
                        children_defs.update(child_data.get('defs', []))
                        children_uses.update(child_data.get('uses', []))
                        children_atts.update(child_data.get('atts', []))
                        lineend = max(lineend, child_data.get('lineno', 0))
            if children_stmt:
                slinks[link_type] = children_stmt

        # Link names used in child expressions to `names` in the current scope
        defs.extend(
            create_name(scope, name)
            for name in children_defs)

        uses.extend(
            create_name(scope, name)
            for name in children_uses)

        # Link attributes used in child expressions to `attributes` in the current scope
        atts.extend(
            AttrNode(attr)
            for attr in children_atts)
        # XXX Should deduplicate names

        # Records the links if any
        if defs:
            slinks['defs'] = defs
        if uses:
            slinks['uses'] = uses
        if atts:
            slinks['atts'] = atts
        if exts:
            slinks['exts'] = exts

        sdata['lineend'] = lineend
        return stree

    # Go recursion
    return rec(data_tree, None)
