#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Clean text from a pdf document

Replace non-ascii chars with their equivalent.
'''

class Cleaner(object):
    replacements = {
        '“' : '"',
        '”' : '"',
        '–' : '-',
        '’' : "'",
        }

    def __init__(self, quote=False):
        self.quote = quote

    def run(self, text):
        out = self.clean(text)
        if self.quote:
            out = self.add_quotes(out)
        return out

    def clean(self, text):
        out = text
        for rpl,val in self.replacements.items():
            out = out.replace(rpl, val)
        return out

    def add_quotes(self, text):
        out = '\n'.join([ u'> ' + line for line in text.splitlines() ])
        return out

    def paragraph(self):
        # TODO: handle lots of blank lines
        # get median line length
        lengths = [ len(x.strip()) for x in text.splitlines() if len(x.strip()) > 0 ]
        median = lengths[len(lengths)/2]
        lines = text.splitlines()
        def para(line):
            if len(line) < median - 5:
                return line + '\n'
            else:
                return line

# only implemented for linux/gnome
def get_clipboard_contents():
    import pygtk
    pygtk.require('2.0')
    import gtk
    clipboard = gtk.clipboard_get()
    text = clipboard.wait_for_text()
    return text


import sys
import optparse
if __name__ == '__main__':
    usage = '''%prog [file-path]

    Read text and print to standard out.

    file-path: read the (plain) text in file at file-path, or, if not provided,
    read from clipboard
    '''
    parser = optparse.OptionParser(usage)
    parser.add_option('-Q', '--quote', action='store_true', default=False,
            help='Markdown quote the text')
    options, args = parser.parse_args()
    
    if args:
        infn = args[0]
        instr = file(infn).read()
    else:
        instr = get_clipboard_contents()
    cleaner = Cleaner(quote=options.quote)
    out = cleaner.run(instr)
    print out

