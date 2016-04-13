import re
from collections import defaultdict

from sklearn import hmm


RE_TOKENS = re.compile(
    r'( \w+ | [ ]{1,4} | \n | . )',
    re.MULTILINE | re.VERBOSE)

def tokenize(source):
    return RE_TOKENS.findall(source)

def count(tokens):
    counts = defaultdict(
        lambda: defaultdict(
            int))

    last_t = None
    for t in tokens:
        c = counts[last_t]
        c[t] += 1
        c[None] += 1
        last_t = t

    return counts

def token_features(obs):
    " Attributes an integer to each distinct token "
    n = 0
    d = {}
    l = []
    for tokens in obs:
        for t in tokens:
            if t not in d:
                d[t] = n
                l.append(t)
                n += 1
    return (
        lambda ints: [l[i] for i in ints],
        lambda tokens: [d[t] for t in tokens],
    )

def learn(obs, n_states=10):
    i2t, t2i = token_features(obs)
    tokens_i = list(map(t2i, obs))

    model = hmm.MultinomialHMM(n_states, n_iter=20)
    model.fit(tokens_i)

    return model, i2t, t2i

def sample(model, i2t, n):
    return ''.join(i2t(model.sample(n)[0]))
