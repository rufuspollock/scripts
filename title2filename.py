#!/usr/bin/env python
# (c) 2006 Rufus Pollock
# Licensed under the MIT license with the added allowance that attribution
# (i.e. inclusion of this copyright license) is *not* required.

import re
import os
import sys

def standardizeName(oldName):
    """Standardize a name (remove or convert all non-standard characters)"""
    newName = oldName.strip()
    illegalCharsToDiscard = ['?', '"', '.', ':', ',', '(', ')', "'"]
    illegalCharsToConvert = ['-']
    for char in illegalCharsToDiscard:
        newName = newName.replace(char, '')
    newName = '_'.join(newName.split())
    for char in illegalCharsToConvert:
        newName = newName.replace(char, '_')
    
    # if lowercase followed by uppercase transform to lower_lower
    regEx = re.compile('([a-z])([A-Z])')
    newName = regEx.sub(r'\1_\2',newName) 
    newName = newName.lower()
    return newName

# use py.test
class TestStandardizeName:
    
    def test1(self):
        nameIn = "The Man is Here"
        nameOut = "the_man_is_here"
        # print standardizeName(nameIn)
        assert nameOut == standardizeName(nameIn)
    
    def test2(self):
        nameIn = "theManIsHERe"
        nameOut = "the_man_is_here"
        assert nameOut == standardizeName(nameIn)
    
    def test3(self):
        illegalCharsToDiscard = ['?', '"', '.', ':']
        illegalCharsToConvert = ['-']
        nameOut = 'first_second'
        for char in illegalCharsToDiscard:
            nameIn = 'First%s Second' % char
            assert nameOut == standardizeName(nameIn)
        for char in illegalCharsToConvert:
            nameIn = 'First%sSecond' % char
            assert nameOut == standardizeName(nameIn)

    def test_4(self):
        namein = '    My Name is\n\n  John   '
        exp = 'my_name_is_john'
        out = standardizeName(namein)
        assert exp == out
        
if __name__ == '__main__':
    import optparse
    usage = \
'''usage: %prog [options] <title>

Take in a title and convert it to a appropriate form to use in a filename
returning the result on stdout (on macosx will also write result direct to
clipboard on macosx using pbcopy).'''

    parser = optparse.OptionParser(usage)
    options, args = parser.parse_args()
    
    if len(args) == 0:
        parser.print_help()
        sys.exit(0)
    nameIn = args[0]
    nameOut = standardizeName(nameIn)
    # see also http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/410615
    # for alternative native python way to paste to mac osx clipboard
    # macosx 
    # cin, cout = os.popen2('pbcopy')
    cin, cout = os.popen2('xclip -i -selection clipboard')
    cin.write(nameOut)
    cin.close()
    cout.close()
    print nameOut
