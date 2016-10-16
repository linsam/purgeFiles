#!/usr/bin/env python2
#
# Idea here is to override the list and delete functions from the real
# purgeFiles with simulations that work on an internal state. Then we can
# populate fake files, play with time, and execute the purgeFiles algorithm to
# experiment with different settings

import pf
import time
import datetime
import os
import sys

def main():
    # Example simulation. Each iteration, we create a new backup file named
    # after the date, apply the purgeFiles algorithm to it, and display the
    # remaining files.
    #
    # The remaining files are output to standard error, so you can view the
    # purgeFiles output only by redirecting stderr to /dev/null, or only view
    # the filelist over the iterations by redirecting stdout to /dev/null.
    if len(sys.argv) != 3:
        print "Usage: %s ITERATIONS AGESET" % sys.argv[0]
        sys.exit(1)
    iterations = int(sys.argv[1])
    ages = sys.argv[2]

    date = datetime.date.today()
    for iteration in range(iterations):
        fileList.append(File(date.isoformat()))
        date += datetime.timedelta(days=1)
        # Use a safe-sounding directory to prevent user alarm.
        # Don't force in case something goes wrong and our simulated delete
        # isn't called
        pf.purge("simulation://", "*", ages, False)
        print >>sys.stderr, fileList
        ageAll()
    if 0:
        # For fun, pretend a year goes by and no new files are created, but
        # purgeFiles gets run. (e.g. an errant system time update and cron
        # calls for a purge
        ageAll(365*24*60*60)
        pf.purge("simulation://", "*", ages, False)
        print >>sys.stderr, fileList




# Overrides implementation follows

fileList = []

class File(object):
    """A pretend file for the purpose of simulating purgeFiles"""
    def __init__(self, name="", startage=2):
        self.name = name
        self.mtime = time.time()
        if startage:
            self.age(startage)
    def age(self, seconds=60*60*24):
        """Make this file older by the given ammount of time (default 1 day)"""
        self.mtime -= seconds
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name

def ageAll(seconds=24*60*60):
    for i in fileList:
        i.age(seconds)

def deleteFile(file, force):
    """Override, simulate a deletion"""
    fname = file[2]
    for i in fileList:
        if i.name == fname:
            fileList.remove(i)
            print "Deleted: %s" % fname
            break
    else:
        raise Exception("Didn't find file %s" % fname)
pf.deleteFile = deleteFile

def getSortedDirList(directory, pattern):
    """Override, simulate finding files"""
    res = []
    for f in fileList:
        res.append((f.mtime, "", f.name))
    return sorted(res)
pf.getSortedDirList = getSortedDirList

def checkBackupArea(directory):
    """Override, simulate checking the given area.

    Only accepts "simulation://"
    """
    if directory != "simulation://":
        return False
    return True
pf.checkBackupArea = checkBackupArea

# Boilerplate
if __name__ == "__main__":
    main()
