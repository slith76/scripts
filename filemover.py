#!/usr/bin/env python
"""
" script to synchronize two directories with the following structure
"
" 	filemover.py -s <srcdir> -d <dstdir>
" 	
"	srcdir/dirA/files -> dstdir/dirA/files
"	* es exsistieren keine Files in Level 1 (srcdir)
"	* es existieren keine Verzeichnisse in Level 2 (srcdir/dirA)
"	* alle Verzeichnisse werden im Level 1 syncronisiert 
"	* dann werden alle Files aus srcdir/dir* in die dstdir-Struktur kopiert und
"		in srcdir geloescht
"
"""

import	os
#import  os.path
import 	hashlib
import 	shutil
import  logging
import 	sys
import  getopt

log_file = os.path.expanduser('~') + "/.filemover.log"
if not os.path.exists(log_file):
    datei = file(log_file, 'a')
    datei.close()

logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s %(message)s')


def sync_dirs(dir1, dir2):
    source_dirlist = os.listdir(dir1)
    #dest_dirlist = os.listdir(dir2)
    logging.info('[start] synchronize ' + dir1 + ' -> ' + dir2)

    for element in source_dirlist:
        if os.path.isdir(os.path.join(dir1, element)):
            if not os.path.isdir(os.path.join(dir2, element)):
                print element + ' nicht gefunden'
                os.makedirs(os.path.join(dir2, element))
                print os.path.join(dir2, element) + ' angelegt'


def md5Checksum(filePath):
    fh = open(filePath, 'rb')
    m = hashlib.md5()
    while True:
        data = fh.read(8192)
        if not data:
            break
        m.update(data)
    return m.hexdigest()


def main(argv):
    source_path = ''
    dest_path = ''
    try:
        opts, args = getopt.getopt(argv, "hs:d:", ["srcdir=", "dstdir="])
    except getopt.GetoptError:
        print 'filemover.py -s <srcdir> -d <dstdir>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'filemover.py -s <srcdir> -d <dstdir>'
            sys.exit()
        elif opt in ("-s", "--srcdir"):
            source_path = arg
        elif opt in ("-d", "--dstdir"):
            dest_path = arg

    if source_path == '' or dest_path == '':
        print 'filemover.py -s <srcdir> -d <dstdir>'
        sys.exit()

    sync_dirs(source_path, dest_path)
    sync_dirs(dest_path, source_path)

    source_dirlist = os.listdir(source_path)
    #dest_dirlist = os.listdir(dest_path)

    for dir in source_dirlist:
        if os.path.isdir(os.path.join(source_path, dir)):
            source_element_dirlist = os.listdir(os.path.join(source_path, dir))
            for file in source_element_dirlist:
                if os.path.isfile(os.path.join(source_path, dir, file)):
                    # nur kopieren wenn nicht schon vorhanden
                    shutil.copy(os.path.join(source_path, dir, file), os.path.join(dest_path, dir))
                    # MD5 Summe bestimmen und vergleichen
                    if md5Checksum(os.path.join(source_path, dir, file)) == md5Checksum(os.path.join(dest_path,
                                                                                                     dir, file)):
                        os.remove(os.path.join(source_path, dir, file))
                        print os.path.join(source_path, dir, file) + ' kopiert und entfernt'
                        logging.info('[file] ' + os.path.join(source_path, dir, file) + " moved")

if __name__ == "__main__":
    main(sys.argv[1:])
