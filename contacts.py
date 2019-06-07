#!/usr/bin/env python
'''Helper script for command line contact management.

Store contacts in plain ol' text file (e.g. ~/contacts.txt). You can store them
in any old format since we just grep for information. However I use something
like::

    Contact Name
    ============
    
    p: phone-number
    h: home phone-number
    m: mobile-number
    e: email
    www: web address
    a: multi-line address

@author: http://rufuspollock.org/
@license: MIT
'''
import sys
import os
import optparse

if __name__ == '__main__':
    usage = '''%%prog {search-string}
    
    Find contacts in ~/contacts.txt using grep by {search-string}

More Info
=========

%s
    ''' % __doc__
    parser = optparse.OptionParser(usage)
    options,args = parser.parse_args()
    fp = '~/contacts.txt'
    if len(args) == 0:
        print 'You need to supply a search string'
        sys.exit(1)
    search_for = args[0]
    cmd = 'grep --after-context 8 --ignore-case %s %s' % (search_for, fp)
    print cmd
    os.system(cmd)

