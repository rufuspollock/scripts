#!/usr/bin/env python
# Convert csv files to qif format
#
# See http://en.wikipedia.org/wiki/QIF
# requires dateutil

import csv, sys

import dateutil.parser
def norm_date(datestr):
    '''Format to month/day/year'''
    date = dateutil.parser.parse(datestr)
    return '%02d/%02d/%04d' % (date.month, date.day, date.year)
#     if "-" in datestr: # assuming m/d/y
#         p = datestr.split("-")
#         return "%s/%s/%s" % (p[1], p[0], p[2])
#     elif '/' in datestr:
#         p = datestr.split('/')
#         return '%s/%s/%s' % (p[1], p[0], p[2])
#     else:
#         raise Exception('Unknown date format')

def make_mapper(mappings):
    def mymapper(row, key):
        if key in mappings:
            return row[mappings[key]]
        else:
            return ''

def convert(fileobj, mapper=None):
    '''
    D: Date
    P: Payee
    T: amount of item
    M: Memo (description of transaction)
    L: Category:subcat (or class)
    N: Number (of check)
    A: Address (not used usually)
    ^: ender of entry
    '''
    rows = csv.reader(fileobj)
    header = rows.next()
    # defaults = { 'D': 0, 'P': 1, 'T': 2, 'M': 3 }
    # if mapper = None:
    #    if 'Date' in header:
    # print header

    output = u'!Type:Bank\n'
    ## TODO: skip blank rows
    for l in rows:
        for key in [ 'D', 'P', 'T', 'M', 'L', 'N', 'A' ]:
            val = mapper(l, key)
            if val:
                if key == 'D':
                    val = norm_date(val)
                output += u'%s%s\n' % (key, val)
        output +=  u'^\n' # end transaction
    return output.encode('utf8')


from optparse import OptionParser
import sys
if __name__ == '__main__':
    parser = OptionParser('''%prog {csv-file-path}
            
If no csv file provided read from stdin.
''')
    options, args = parser.parse_args()
    if len(args) == 0:
        fileobj = sys.stdin
    elif len(args) == 1:
        fileobj = open(args[0])
    else:
        parser.print_help()
        sys.exit(1)
    print convert(fileobj)

