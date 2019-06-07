#!/usr/bin/env python
'''Convert a short movie (e.g. a screencast) to a gif
'''
import os
import shutil

def convert(infp, outfp='out.gif'):
    tmp = '/tmp/togif'
    if os.path.exists(tmp):
        print('Temp path %s already exists' % tmp)
        return
    os.makedirs(tmp)

    # outfpogv = outfp + '.ogv'
    tmpgif = os.path.join(tmp, 'tmp.gif')

    cmds = [
        # cut down to first 10s
        # 'ffmpeg -ss 00:00:00 -t 00:00:10 -i %s %s' % (infp, outfpogv),
        'vlc "%s" --video-filter=scene --vout=dummy --scene-ratio=2 --scene-path=%s vlc://quit' % (infp, tmp),
        'convert %s/*.png %s' % (tmp, tmpgif),
        # 'gifsicle -O %s -o %s' % (tmpgif, outgif),
        'convert %s -fuzz 10%% -layers Optimize %s' % (tmpgif, outfp),
        ]

    for cmd in cmds:
        os.system(cmd)

    # shutil.rmtree(tmp)
    print('Wrote gif to: %s' % outfp)

import sys
if __name__ == '__main__':
    infp = sys.argv[1]
    outfp = sys.argv[2]
    convert(infp, outfp)

