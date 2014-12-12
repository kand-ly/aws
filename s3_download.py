#!/usr/bin/python

import sys
import getopt
import boto
from boto.s3.key import Key


class S3Connection(object):
    def __init__(self):
        self.connection = boto.connect_s3()

    def get_bucket(self, name):
        try:
            b = self.connection.get_bucket(name)
        except S3ResponseError:
            b = self.connection.create_bucket(name)
        return S3Bucket(name, b)

class S3Bucket(object):
    def __init__(self, name, bucket):
        self.name = name
        self.bucket = bucket

    def getfile(self, srcfile, dstfile):
        k = Key(self.bucket)
        k.key = srcfile
        k.get_contents_to_filename(dstfile)


def usage(progname):
    print progname + ' <bucket> <srcfile> [dstfile]'
    
        
def main(argv):
    srcfile = ""
    dstfile = ""
    bucket = ""

    try:
        opts, args = getopt.getopt(argv[1:],"h")
    except getopt.GetoptError:
        usage(argv[0])
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage(argv[0])
            sys.exit()

    if len(args) < 2:
        usage(argv[0])
        sys.exit(2)

    bucket = args[0]
    srcfile = args[1]
    if len(args) < 3:
        dstfile = srcfile
    else:
        dstfile = args[2]

    s3conn = S3Connection()
    bucket_object = s3conn.get_bucket(bucket)
    bucket_object.getfile(srcfile, dstfile)

    print 'Downloaded ' + bucket + ':' + srcfile + ' to ' + dstfile
        
if __name__ == "__main__":
    main(sys.argv)
