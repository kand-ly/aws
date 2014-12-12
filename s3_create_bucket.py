#!/usr/bin/python

import sys
import getopt
import boto
from boto.s3.connection import Location


class S3Connection(object):
    def __init__(self):
        self.connection = boto.connect_s3()

    def create_bucket(self, name, region):
        self.connection.create_bucket(name, None, region)


def usage(progname):
    print progname + ' -r <region> <bucket>'

    
def main(argv):
    bucket = ""
    region = Location.DEFAULT

    try:
        opts, args = getopt.getopt(argv[1:],"hr:")
    except getopt.GetoptError:
        usage(argv[0])
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            usage(argv[0])
            print '\n'.join(eval('Location.' + i) for i in dir(Location) if i[0].isupper())
            sys.exit()
        elif opt == '-r':
            region = arg

    if len(args) < 1:
        usage(argv[0])
        sys.exit(2)

    bucket = args[0]

    s3conn = S3Connection()
    s3conn.create_bucket(bucket, region)

    print 'Created bucket ' + bucket + ' in ' + (region if region != "" else 'us-east-1')
        
if __name__ == "__main__":
    main(sys.argv)
