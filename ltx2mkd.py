#!/usr/bin/env python
'''Convert from latex to markdown.

Done:
  * emph
  * textbf
  * sections
  * itemize
  * enumerate
  * cite
  * comments

TODO:
  * footnote
'''

import re

def convert(fileobj_or_str):
    if isinstance(fileobj_or_str, basestring):
        text = fileobj_or_str
    else:
        text = fileobj_or_str.read()
    text = text.replace('``', '"')
    text = text.replace("''", '"')
    text = text.replace('`', "'")
    flags = re.UNICODE | re.MULTILINE
    regex = re.compile('\\\\emph{([^}]+)}', flags)
    text = regex.sub(r'*\1*', text)

    regex = re.compile('\\\\textbf{([^}]+)}', flags)
    text = regex.sub(r'**\1**', text)

    section = re.compile(r'\\?section{([^}]+)}', flags)
    text = section.sub(r'### \1', text)
    text = text.replace('\\subsub', '##')
    text = text.replace('\\sub', '#')

    text = text.replace('\\begin{itemize}', '')
    text = text.replace('\\end{itemize}', '')
    text = text.replace('\\begin{enumerate}', '')
    text = text.replace('\\end{enumerate}', '')
    text = text.replace('\\item', '*')

    # TODO: sort out comments
    commentre = re.compile(r'[^\\]%.*$', flags=re.MULTILINE)
    text = commentre.sub(r'', text)
    text = text.replace('\\%', '%')

    fnre = re.compile('\\\\footnote{([^}]|\n)*\s*}', flags)
    text = fnre.sub(r'', text)

    citere = re.compile('\\\cite[^}]*{([^}]+)}', flags)
    biblio = 'http://rufuspollock.org/economics/biblio/#'
    def makecite(match):
        citeid = match.group(1) 
        title = citeid.replace('_', ' ').capitalize()
        title = title.replace('ea', 'et al')
        link = biblio + citeid
        return '[%s](%s)' % (title, link)
    text = citere.sub(makecite, text)
    return text

def test_1():
    out = convert("`abc'")
    assert out == "'abc'", out

    out = convert('emph{abc}')
    assert out == 'emph{abc}', out
    out = convert('\\emph{abc}')
    assert out == '*abc*', out

    out = convert('textbf{abc}')
    assert out == 'textbf{abc}', out
    out = convert('\\textbf{abc}')
    assert out == '**abc**', out

    out = convert('\\citet*{mischel_ea_1980}')
    assert out == '[Mischel et al 1980](http://rufuspollock.org/economics/biblio/#mischel_ea_1980)', out

    # TODO: test enumerate

import optparse
import sys
if __name__ == '__main__':
    usage = '''%prog {file-path}

Convert latex file at {file-path} to markdown and print to stdout.
'''
    parser = optparse.OptionParser(usage)
    options, args = parser.parse_args()
    assert len(args) > 0, 'You need to supply a file path'
    fp = args[0]
    print convert(open(fp))

