import re


def red(s):
    return "\x1b[31m%s\x1b[0m" % s
def green(s):
    return "\x1b[32m%s\x1b[0m" % s
def blue(s):
    return "\x1b[34m%s\x1b[0m" % s
def magenta(s):
    return "\x1b[35m%s\x1b[0m" % s
def cyan(s):
    return "\x1b[36m%s\x1b[0m" % s
def bold(s):
    return "\x1b[1m%s\x1b[0m" % s


def highlight(text, word, color=magenta):
    return re.sub(r'\b%s\b' % word, color(word), text)


def print_neo(lines, n):
    if isinstance(n, list):
        for e in n:
            print(blue(str(e)))
        print()
    else:
        print(blue(str(n)))

    try:
        print('| %s' % magenta(lines[n['lineno'] - 1]))
    except:
        pass


def print_neo_rel(lines, n):
    print_neo(lines, n)
    try:
        print('->', blue(' '.join([str((r.type, str(r.end_node))) for r in n.match_outgoing()])))
        print('<-', blue(' '.join([str((r.type, str(r.start_node))) for r in n.match_incoming()])))
    except:
        pass


def print_path(lines, p):
    for r in p:
        print_neo(lines, r.start_node)
        print(r.type)
    print_neo(lines, r.end_node)


def print_results(lines, res):
    print(red('  - %s results' % len(res)))
    for d in res.data:
        for i, col in enumerate(d.columns):
            n = d.values[i]
            print(green(col), '=', end=' ')
            print_neo(lines, n)
        print()
