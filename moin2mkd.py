#!/usr/bin/env python
import re

def convert(fileobj_or_str):
    if isinstance(fileobj_or_str, basestring):
        text = fileobj_or_str
    else:
        text = fileobj_or_str.read()
    flags = re.UNICODE | re.MULTILINE
    regex = re.compile("'''''(.+)''''", flags)
    text = regex.sub(r'***\1***', text)

    regex = re.compile("'''(.*)'''", flags)
    text = regex.sub(r'**\1**', text)

    regex = re.compile("''(.+)''", flags)
    text = regex.sub(r'*\1*', text)

    # headings
    for x in reversed(range(1,6)):
        moin_head = '=' * x
        section = re.compile('%s\s*(.+)\s*%s' % (moin_head, moin_head), flags)
        text = section.sub('%s \\1' % ('#' * x), text)
    
    # links
    regex = re.compile(r'\[\[([^|]+)\|([^]]+)\]\]', flags)
    text = regex.sub(r'[\2](\1)', text)
    # for html
    # text = regex.sub(r'<a href="\1">\2</a>', text)

    return text

def test_1():
    out = convert("''abc''")
    assert out == '*abc*', out

    out = convert("'''abc'''")
    assert out == '**abc**', out
    
    in_ = '''
= H1 =

== H2 ==

=== H3 ===

==== H4 ====

===== H5 =====

 * [[http://rufuspollock.org/|website]] [[http://rufuspollock.org/|again]]
    '''
    expout = '''
# H1

## H2

### H3

#### H4

##### H5

 * [website](http://rufuspollock.org/) [again](http://rufuspollock.org/)
    '''
    out = convert(in_)
    # assert out == expout, out
    print out
    for line1,line2 in zip(expout.split(), out.split()):
        assert line1 == line2, line2

import optparse
import sys
if __name__ == '__main__':
    usage = '''%prog {file-path}

Convert moin file at {file-path} to markdown and print to stdout.
'''
    parser = optparse.OptionParser(usage)
    options, args = parser.parse_args()
    assert len(args) > 0, 'You need to supply a file path'
    fp = args[0]
    print convert(open(fp))

