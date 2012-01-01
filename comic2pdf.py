# Converts .cbr and .cbz files to .pdf
#
# Use:  python comic2pdf.py FOLDER_CONTAINING_COMIC_FILES
# -- Only works with comicbook files that contain JPG's (for now)
# -- Has problems with files that don't export as a folder containing JPG's
#
# Requires ImageMagick and WinRar
# ImageMagick:  http://www.imagemagick.org/script/
# RARLAB:  http://www.rarlab.com/download.htm
#
# Author:  Bran Sorem
# Date:  12-26-11
# Website:  www.bransorem.com
#
# License:  You can do what you want with it (and you should) - but I'd prefer some credit
# I am not liable for any misuse or other licensing conflicts

import os, sys, zipfile, shutil, subprocess

failed = False

def handlerar(filein):
    fileout = filein[:-4] + '.rar'
    shutil.copy(filein, fileout)
    command = 'unrar e ' + '"' + fileout + '" "' + filein[:-4] + '"/'
    # get files before extraction
    old_files = os.listdir(os.getcwd())

    # use subprocess to run unrar command
    try:
        nout = open('NULL', 'w')
        retcode = subprocess.call(command, shell=True, stdout=nout, stderr=nout)
        nout.close()
        os.remove('NULL')
        if retcode < 0:
            print >>sys.stderr, "Child was terminated by signal", -retcode
    except OSError, e:
        print >>sys.stderr, "Execution failed:", e

    new_files = os.listdir(os.getcwd())
    # get difference between ls's
    newdir = [adir for adir in new_files if not adir in old_files]
    os.remove(fileout)
    print "Converting " + filein + " -> " + filein[:-4] + ".pdf"
    # should be the only one! I'm not bothering to parallelize it
    if len(newdir) == 1:
    	toPDF(filein[:-4], newdir[0])
    else:
	    print "*** Oops, couldn't create a file.  Skipped " + filein + " ***"
	    failed = True

def handlezip(filein):
    fileout = filein[:-4] + '.zip'
    shutil.copy(filein, fileout)
    zipr = zipfile.ZipFile(fileout, 'r')
    # get files before extraction
    old_files = os.listdir(os.getcwd())
    tempdir = filein[:-4] + "/"
    zipr.extractall(tempdir)
    # and files after extraction
    new_files = os.listdir(os.getcwd())
    # get difference between ls's
    newdir = [adir for adir in new_files if not adir in old_files]
    os.remove(fileout)
    print "Converting " + filein + " -> " + filein[:-4] + ".pdf"
    # should be the only one! I'm not bothering to parallelize it
    if len(newdir) == 1:
    	toPDF(filein[:-4], newdir[0])
    else:
	    print "*** Oops, couldn't create file.  Skipped " + filein + " ***"
	    failed = True
    
def toPDF(filename, newdir):
    fileout = '"' + filename + '".pdf'
    # ImageMagick call (convert all JPG's in folder to a single PDF)
    # convert "DIRECTORY"/*.jpg FILENAME.pdf
    command = 'convert "' + newdir + '"/*.jpg ' + fileout
    try:
        os.system(command)
    except:
	    print "*** Oops, couldn't create a file.  Skipped " + filein + " ***"
	    failed = True
    # remove temp directory
    shutil.rmtree(newdir)
    
def opendir(directory):
    # look at all files in directory
    for file in os.listdir(directory):
        # file extension cbr only
        if file[-4:] == '.cbz':
	        # change to zip
	        handlezip(file)
        elif file[-4:] == '.cbr':
            # change to rar
            handlerar(file)
    if failed:
		print "WARNING: some items were skipped"


os.chdir(sys.argv[1])
opendir(os.getcwd())
