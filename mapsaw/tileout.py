# Copyright (c) 2010 Nick Thompson
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php


import os, subprocess

def optipng(inf, outf):
    cmd = 'optipng'
    exitcode = subprocess.call([cmd, '-quiet', '-out', outf, inf])
    if exitcode != 0:
        raise Exception('%s command failed with exit code %d' % (cmd, exitcode))


# size is in K
def osx_ramdisk(name, size):
    # for mac osx
    mountpoint = os.path.join('/Volumes', name)
    if os.path.exists(mountpoint):
        return mountpoint

    blocksize = 512
    ramdesc = 'ram://%d' % size * (1024 / blocksize)
    p = subprocess.Popen(['hdiutil', 'attach', '-nomount', ramdesc],
                         stdout=subprocess.PIPE)
    subout,suberr = p.communicate()
    loc = subout.strip()
    print 'LOC',loc

    # format the disk using HFS
    exitcode = subprocess.call(['diskutil', 'erasevolume', 'HFS+', name, loc])
    if exitcode != 0:
        raise Exception('%s command failed with exit code %d' % ('diskutil', exitcode))

    # 1.1GB disk (2.2 is max)
    #diskutil erasevolume HFS+ "scratch" $(hdiutil attach -nomount ram://2330860)

    return mountpoint

def ramdisk():
    # should empty it?
    # should check that there's enough free space?
    if os.path.isdir('/dev/shm'):
        return '/dev/shm'

    # detect OSX?
    return osx_ramdisk('scratch', 2**20)
    
