#!/usr/bin/python

import sys
import getopt
import boto
from boto.s3.connection import Location


class S3Connection(object):
    def __init__(self):
        self.connection = boto.connect_s3()

    def create_bucket(self, name, region):
        if region == "":
            self.connection.create_bucket(name)
        else:
            self.connection.create_bucket(name, None, region)


def main(argv):
    bucket = ""
    region = ""

    try:
        opts, args = getopt.getopt(argv[1:],"hr:")
    except getopt.GetoptError:
        print 'Option error'
        print argv[0] + ' -r <region> <bucket>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'Usage:'
            print argv[0] + ' -r <region> <bucket>'
            print '\n'.join(eval('Location.' + i) for i in dir(Location) if i[0].isupper())
            sys.exit()
        elif opt == '-r':
            region = str(arg)

    if len(args) < 1:
        print 'Arg error'
        print argv[0] + ' -r <region> <bucket>'
        sys.exit(2)

    bucket = args[0]

    print 'Creating bucket ' + bucket + ' in ' + (region if region != "" else 'DEFAULT')
        
    s3conn = S3Connection()
    s3conn.create_bucket(bucket, region)

if __name__ == "__main__":
    main(sys.argv)
