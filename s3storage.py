doc = """A very minimal (as minimal as possible) library for reading
and deleting things from s3.  Please BE WARNED this library has no
test suite as it is tested by the s3duplicitybackup tests, and in
order for it to have tests I have to create all sorts of extra
functionality (like uploading stuff) that is not the goal of the
functionality of this library so far (it just supports the backup
system)

"""

__doc__ = doc

import os
import boto
from boto.s3.connection import S3Connection, Location, Key

## create a connection

## create a bucket in Europe
# conn.create_bucket('mybucket', location=Location.EU)

## get all buckets
# buckets = conn.get_all_buckets()
# binf = buckets[0]


def connection(keyid, secret):
    """Return an s3 connection object"""
    return S3Connection(aws_access_key_id, aws_secret_access_key)


def ls(path='', delimiter=None, bucket='somecompany', conn=None):
    """Thin wrapper over the bucket.list function"""
    conn = conn or S3Connection(aws_access_key_id, aws_secret_access_key)
    b = conn.get_bucket(bucket)
    return b.list(path.lstrip('/'), delimiter)


def path_exists(path, conn=None, exact=False):
    if exact is True:
        filterfun = lambda k: k.key == path
    else:
        filterfun = lambda k: k.key == path or k.key.startswith(path)
    paths = filter(filterfun, ls(os.path.split(path)[0], conn))
    return paths and True or False


def delete_dir(path, conn, bucket='somecompany'):
    b = conn.get_bucket(bucket)
    keys = ls(path, bucket=bucket, conn=conn)
    [b.delete_key(k) or k for k in keys]
    # check that the "directory" is actually gone
    contents = list_dir(path, conn=conn, bucket=bucket)
    if contents:
        return (False, contents)
    else:
        return (True, contents)


def list_dir(path='', bucket='somecompany', conn=None, full=False):
    """list the contents of a path, but only one level deep"""
    path = path.endswith('/') or path + '/'
    if full is True:
        return [p.name for p in ls(path, '/', bucket, conn)]
    else:
        return [p.name.partition(path)[2].rstrip('/') for p in ls(path, '/', bucket, conn)]


def mkdir(path='', bucket='somecompany', conn=None):
    """Stubbed function for compatibility.  The concept of creating a
    directory on s3 makes no sense
    """
    return True
