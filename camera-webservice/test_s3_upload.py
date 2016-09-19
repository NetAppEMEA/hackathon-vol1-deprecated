#!/usr/bin/python
##########################################################################
# Camera Web Service Program
#
# This program uses two key tools Flask and Elasticsearch
# Flask - Flask is a microframework for Python based on Werkzeug, Jinja 2 and good intentions.
#         It provides a built-iin development server and debugger.  It handles RESTful
#         request dispatching.
# Elasticsearch - is a search engine based on Lucene. It provides a distributed,
#         multitenant-capable full-text search engine with an HTTP web interface
#         and schema-free JSON documents.
#
# Run this program
#         %> python camera-webservice
#         %> ./camera-webservice
#
# Code Example References
#     flask-restul api quickstart: http://flask-restful-cn.readthedocs.io/en/0.3.4/quickstart.html
#
##########################################################################

# Python pagackage installation instructions - using 'pip'
# pip is a package management system used to install and manage python packages
#---------------------------------------
# %> pip install flask flask-restful pillow boto3 json elasticsearch


# Include/import elasticsearch
from elasticsearch import Elasticsearch

# Import native python libraries
import time
import socket
import uuid
import os
import boto3
import json
import sys
from boto3.s3.transfer import S3Transfer


#---------------------------------------
# read json formatted config file - load values for later use
#---------------------------------------
try:
    with open('config.json') as data_file:
        conf = json.load(data_file)
        conf['s3_endpoint']
        conf['s3_bucket']
        conf['s3_access_key']
        conf['s3_secret_access_key']
        conf['elasticsearch_host']
        conf['camera_command']

# if error occurs in 'try' block - generate an exception message
except Exception as e:
    sys.stderr.write(
        'FATAL: Cannot open or parse configuration file : ' + str(e) + '\n\n')
    exit()


s3_object = '/home/pi/image.jpg'
s3_key_name = 'nacknight/image.jpg'
filename = 'image.jpg'

#---------------------------------------
# Upload to S3 object store repository
#    https://<s3 bucket>.<s3 endpoint>/<s3 key_name>  - stores the picture/object
#---------------------------------------
print("--- Writing image to S3 Object storage...")

# S3 endpoint url  (s3.amazon.com)
s3_endpoint = conf['s3_endpoint']

# get the S3 bucket name from the config.json file
s3_bucket = conf['s3_bucket']

# the label or key name it will be called in S3
# NOTE: the key_name can be things like 'my_pic' or 'my_pictures/my_pic'
# the key_name will represented in S3 as <endpoint>/<key_name>
s3_key_name = 'hacknight/' + filename

# the item we are going to store in S3
s3_object = filename


try:
    # connect to S3 using boto3 API by passing access key and secret access keys.
    # the S3 endpoint is inferred from the key pair upon connection
    session = boto3.session.Session(
        aws_access_key_id=conf['s3_access_key'],
        aws_secret_access_key=conf['s3_secret_access_key']
    )

    # if end point is AWS S3
    if 'amazonaws.com' in s3_endpoint:
        print("---   AWS Upload ---")
        s3_url = 'https//:' + s3_endpoint + '/' + s3_bucket + '/' + s3_key_name

        # AWS infers the endpoint from the s3_access_key/account info
        s3 = session.resource(service_name='s3')

    # else assume NetApp StorageGrid Webscale (SGWS)
    else:
        print("---   SGWS Upload ---")
        # SGWS requires full endpoint passed to the session.resource
        s3_endpoint = "https://" + conf['s3_endpoint'] + ":443"
        s3_url = s3_endpoint + '/' + s3_bucket + '/' + s3_key_name

        s3 = session.resource(service_name='s3',
                              endpoint_url=s3_endpoint,
                              verify=False
                              )

    # report path where the picture is uploaded (path style for compatability)
    print("--- S3 upload path: " + s3_url)

    # defined a new S3 object by specifying the bucket and key_name that you
    # will store the file
    obj = s3.Object(
        s3_bucket,
        s3_key_name
    )

    # upload the actual file/object to S3
    obj.upload_file('/tmp/' + filename)

    print("---   s3_bucket:   " + s3_bucket)
    print("---   s3_key_name: " + s3_key_name)
    print("---   filename:    " + filename)

    # remove local copy of the picture we just took
    #os.remove('/tmp/' + filename)

# handle any errors which might occur
except botocore.exceptions.ClientError as e:
    print "Unexpected error during S3 upload: %s" % e


#---------------------------------------
# Return success
#---------------------------------------
print ("INFO: program done\n")
