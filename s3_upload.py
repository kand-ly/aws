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

    def addfile(self, srcfile, dstfile):
        k = Key(self.bucket)
        k.key = dstfile
        k.set_contents_from_filename(srcfile)


def main(argv):
    srcfile = ""
    dstfile = ""
    bucket = ""

    try:
        opts, args = getopt.getopt(argv[1:],"h")
    except getopt.GetoptError:
        print 'Option error'
        print argv[0] + ' <srcfile> <bucket> [dstfile]'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'Usage:'
            print argv[0] + ' <srcfile> <bucket> [dstfile]'
            sys.exit()

    if len(args) < 2:
        print 'Arg error'
        print argv[0] + ' <srcfile> <bucket> [dstfile]'
        sys.exit(2)

    srcfile = args[0]
    bucket = args[1]
    if len(args) < 3:
        dstfile = srcfile
    else:
        dstfile = args[2]

    print 'Uploading ' + srcfile + ' to ' + bucket + ':' + dstfile
        
    s3conn = S3Connection()
    bucket_object = s3conn.get_bucket(bucket)
    bucket_object.addfile(srcfile, dstfile)

if __name__ == "__main__":
    main(sys.argv)
