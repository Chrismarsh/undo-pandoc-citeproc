from __future__ import print_function
from panflute import *
from functools import partial
import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# converts the prefix or suffix to a plain string
def to_string(elem):
    prefix = []
    for s in elem:
        if hasattr(s, 'text'):
            prefix.append(s.text)

    prefix = ' '.join(prefix)
    return prefix


def isolate_citation(elem, doc):
    # Surrounds the citations with Emph section so we can more easily find it later.
    if isinstance(elem, Cite):

        for c in elem.citations:
            prefix = to_string(c.prefix)
            suffix = to_string(c.suffix)
            citeType = c.mode
            with open('citations.txt', 'a') as f:
                f.write('%s;%s;%s;%s\n' % (c.id, prefix, suffix, citeType))

        return Emph(elem)


def main(doc=None):
    with open('citations.txt', 'w') as f:
        pass
    return run_filter(isolate_citation, doc=doc)


if __name__ == "__main__":
    main()
