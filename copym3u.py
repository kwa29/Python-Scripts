#!/usr/bin/env python
# Mp3 playlist to files mover
# Copies all files in an m3u playlist to given directory
# and renames them to indicate the order in the playlist
# by kognuant 2009.06.11
# linux ( an a and a t) koant ( a d and an o and a t) com

import os
import shutil
import sys
import re
import csv

def main(argv=None):
	if argv is None:
		argv = sys.argv

	if argv is None or len(argv) <= 1:
		print "Error: no m3u playlist file provided"
		return 2
	else:
		path = argv[1]


	if argv is None or len(argv) <= 2:
		print "Error: no target directory provided"
		return 2
	else:
		dir = argv[2]

		
	if os.path.isfile(path) and os.path.isdir(dir):
	    # Parse m3u file
	    mp3Files = readm3u(path)
	    # Move files
	    copyFiles(mp3Files, dir)
	else:
		print "Error:", path, "is not a file or ", dir, " is not a directory"
		return 2

# Reads mp3 file locations from m3u
def readm3u(path):
    fileHandle = open (path, 'r')
    reader = csv.reader(open(path, "r"))
    
    # List of mp3files
    mp3Files = []
    
    for row in reader:
        if len(row)<1:
            # Skip blanks
            continue
        elif row[0].startswith("#"):
            # Ignore comments
            continue
        else:
            # store rule
            mp3Files.append(row[0])
    
    fileHandle.close()   
    
    return mp3Files


# Moves given files to target directory
def copyFiles(mp3Files,targetDir):
    
    targetDirExists=0
    # Check that target directory exists and is a directory        
    if os.path.isdir(targetDir):
        targetDirExists=1
    else:
        print "target is not a directory: ", targetDir

    idx=0

    for mp3 in mp3Files:
	print mp3
	sourceFile = mp3

	# Boolean flags
	sourceIsFile=0
	sourceirectory=0
	targetFileExists=1
	
	# Check that the source file exists and isn't a directory
	if os.path.isfile(sourceFile):
	    sourceIsFile=1
	elif os.path.isdir(sourceFile):
	    sourceIsDirectory=1
	else:
		print "source is not a file or a directory: ", sourceFile

	sourceFilename = os.path.basename(sourceFile)

	print sourceFilename

	# get the absolute path of the destination file         
	targetFile = targetDir + "%03d__%s" % (idx, sourceFilename)
	idx=idx+1

	print targetFile

	# Check that the file doesn't already exist
	if os.path.exists(targetFile):
	    print "target exists: ", targetFile
	else:
	    targetFileExists=0

	# If flags allow moving, then proceed        
	if(targetFileExists==0 and sourceIsFile==1 and targetDirExists==1):
	    shutil.copy(sourceFile,targetFile)
	else:
	    print "Can't copy..."
                        
if __name__ == "__main__":
	sys.exit(main())
