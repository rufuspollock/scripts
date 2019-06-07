#!/usr/bin/env python
# Convert a whole directory tree of flac files to oggs 
# This script is Public Domain: copy, redistribute, reuse freely and without
# restriction
import os
import shutil
import commands

# set src and dest path in __main__ below

def run_cmd(cmd):
    status, output = commands.getstatusoutput(cmd)
    if status:
        print 'Had error running [%s]: %s' % (cmd, output)

def convert_to_ogg_crude(srcPath, destPath, clean=True):
    if clean:
        shutil.rmtree(destPath)
    if not os.path.exists(destPath):
        os.makedirs(destPath)
    os.chdir(srcPath)
    cmds = [
        "find . -type d -exec mkdir %s/'{}' \\;" % destPath,
        "find . -name '*.flac' -exec oggenc --quiet --quality 4 '{}' \\;",
        "find . -name '*.ogg' -exec mv '{}' %s/'{}' \\;" % destPath,
        ]
    for cmd in cmds:
        run_cmd(cmd)

def get_offset(root, path):
    tlen = len(os.path.normpath(root))
    out = os.path.normpath(path)[tlen:]
    if out.startswith('/'): return out[1:]
    else: return out

def get_dest_path(src_base_path, dest_base_path, file_path):
    offset = get_offset(src_base_path, file_path)
    dest = os.path.join(dest_base_path, offset)
    dest = dest[:-5] + '.ogg'
    return dest

def convert_to_ogg(src_base_path, dest_base_path):
    """Convert all flac files in src_base_path to ogg files under dest_base_path
    NB: do not seem to have to create dest directories as oggenc does it.
    """
    oggcmd = 'oggenc --quiet --quality 4 --output "%s" "%s"'
    for root, dirs, files in os.walk(src_base_path):
        for file in files:
            fbase, fext = os.path.splitext(file)
            if fext == '.flac':
                tpath = os.path.join(root, file)
                print('Considering %s' % tpath)
                dest = get_dest_path(src_base_path, dest_base_path, tpath)
                if not os.path.exists(dest):
                    print('  Processing to %s' % dest) 
                    tcmd = oggcmd % (dest, tpath)
                    status, output = commands.getstatusoutput(tcmd)
                    if status:
                        print('Error: %s' % output)
                else:
                    print('  Skipping')

import unittest
class TestConvertOggToFlac(unittest.TestCase):
    src = '/var/share/music'
    dest = '/var/share/ogg'
    
    def test_get_dest_path(self):
        offset = 'blah/jones.flac'
        inpath = os.path.join(self.src, offset)
        out = get_dest_path(self.src, self.dest, inpath)
        exp = os.path.join(self.dest, offset[:-5] + '.ogg')
        self.assertEqual(out, exp)

if __name__ == '__main__':
    # base directory for flac files
    src_base = '/var/share/music'
    # destination directory for ogg files
    dest_base = '/var/lib/ogg'
    convert_to_ogg(src_base, dest_base)
    # unittest.main()
