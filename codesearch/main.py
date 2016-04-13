import yaml

from .codecommon import (
    db,
    SCHEMA_REV,
)
from .ogm import insert_tree
from .codeexplore import find_by_filemeta
from .codeanalysis import (
    source_to_tree,
    node_to_data,
    simplify_tree,
)


def dump(tree, source_file):
    with open(source_file + '.yml', 'w') as fd:
        yaml.dump(tree.__dict__, fd)


def analyse(fd, meta):
    " Parse source files and insert the trees into the db "
    source = fd.read()

    tree = source_to_tree(source)

    data_tree = node_to_data(tree)
    simple_tree = simplify_tree(data_tree)
    root = simple_tree.__dict__
    root.update(meta)
    return simple_tree


def main():
    import argparse
    import os
    import fnmatch
    import traceback
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["parse", "cleardb", "tokens"])
    parser.add_argument("files", nargs='*')
    parser.add_argument("-n", "--no-check", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    def parse(filename):
        if fnmatch.fnmatch(filename, '*.py'):
            print("Parsing %s" % filename)
            try:
                meta = {
                    'schema_rev': SCHEMA_REV,
                    'project': 'test',
                    'version': '0.1',
                    'filename': filename,
                }
                if not args.no_check and find_by_filemeta(meta):
                    raise ValueError(
                        'This file is already in the database: %s' % meta)
                with open(filename) as fd:
                    tree = analyse(fd, meta)
                insert_tree(tree, label='code')
                dump(tree, filename)
                if args.verbose:
                    print yaml.dump(tree.__dict__)
            except Exception:
                print("Error parsing %s" % filename)
                traceback.print_exc()
                print("----\n")

    if args.action == "cleardb":
        db.clear()
    elif args.action in ["parse", "tokens"]:
        fn = parse if args.action == "parse" else tokenize
        for arg_file in args.files:
            if os.path.isdir(arg_file):
                for root, dirnames, filenames in os.walk(arg_file):
                    for filename in filenames:
                        fn(os.path.join(root, filename))
            else:
                fn(arg_file)
