#!/usr/bin/python
##########################################################################
# Camera Web Service Program
#
# This program uses three key tools Flask, boto3 and Elasticsearch
# Flask - Flask is a microframework for Python based on Werkzeug, Jinja 2 and good intentions.
#         It provides a built-iin development server and debugger.  It handles RESTful
#         request dispatching.
# boto3 - is the Amazon Web Services (AWS) Software Development Kit (SDK) for
#         Python, which allows Python developers to write software that makes
#         use of services like Amazon S3 and Amazon EC2.
# Elasticsearch - is a search engine based on Lucene. It provides a distributed,
#         multitenant-capable full-text search engine with an HTTP web interface
#         and schema-free JSON documents.
#
# Run this program
#         %> python webservice.py
#         %> ./webservice.py
#
# Code Example References
#     flask-restul api quickstart: http://flask-restful-cn.readthedocs.io/en/0.3.4/quickstart.html
#
##########################################################################

# Python pagackage installation instructions - using 'pip'
# pip is a package management system used to install and manage python packages
#---------------------------------------
# %> pip install flask flask-restful pillow boto3 elasticsearch picamera


#---------------------------------------
# include Python packages
# from <module/package> include <functions>
#---------------------------------------
# Include/import Flask and its functional libraries
from flask import Flask, jsonify,  abort,    make_response,  request, send_file
from flask_restful import Api,   Resource, reqparse, fields, marshal

# Include/import PiCamera - this is a RaspberryPI Camera library
from picamera import PiCamera

# Include/import boto3 package for S3 object store handling
from boto3.s3.transfer import S3Transfer

# Include/import elasticsearch
from elasticsearch import Elasticsearch

# Import native python libraries
import time
import datetime
import socket
import uuid
import os
import boto3
import json
import sys
import fcntl
import struct


#---------------------------------------
# create instance of Flask and Flask-RESTful API
#---------------------------------------
# create an instance of Flask - __name__ is the name of application
# running - in this case 'camera-webservice'
app = Flask(__name__, static_url_path="")

# create an instance of the RESTful Api
api = Api(app)


#============================================================
# Sub-routines
#============================================================

#---------------------------------------
# return IP address of wlan0
#---------------------------------------
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

#---------------------------------------
# sub-routine to take photo
#---------------------------------------


def takePhoto():
    print("--- Taking Photo...")
    # current time
    now = datetime.datetime.now()

    # create randomized filename
    filename = now.strftime("%Y%m%d-%H%M%S") + '.jpg'

    # open the camera connection
    camera = PiCamera()

    # adjust resolution for efficiency
    camera.resolution = (640, 480)

    # rotate if needed
    #camera.rotation = 180

    # add the current time as text to the image
    camera.annotate_text = now.strftime("%Y-%m-%d %I:%M:%S%p")

    # capture the image
    camera.capture('/tmp/' + filename)

    # close the camera connection
    camera.close()

    print("--- Photo named: " + filename)

    return filename

#---------------------------------------
# RESTful call when http://<ip address>/ is called
#---------------------------------------


@app.route("/")
def index():
    # return a HTML message in the browser indicating the Webservice is running
    my_message2 = "TEST camera only: http://%s:8080/test" % ip_address
    my_message3 = "To take take picture, upload to S3 and Elasticsearch: http://%s:8080/photo" % ip_address
    my_message4 = "To list photos: http://%s:8080/list" % ip_address

    return make_response(
        jsonify(
            {
                'message1': "Webservice is running.",
                'message2': my_message2,
                'message3': my_message3,
                'message4': my_message4,
                'success': True
            }
        ), 200)

#---------------------------------------
# RESTful call when http://<ip address>/test is called
#   this call takes a picture and displays it on the screen
#---------------------------------------


@app.route("/test")
def testCamera():
    return send_file('/tmp/' + takePhoto(), mimetype='image/jpeg')

#---------------------------------------
# RESTful call when http://<ip address>/list is called
#   this call returns a list of images stored in S3
#---------------------------------------


@app.route("/list")
def listPhotos():
    # connect to s3
    session = boto3.session.Session(
        aws_access_key_id=conf['access_key'],
        aws_secret_access_key=conf['secret_access_key']
    )

    client = session.client('s3')

    # return a json list of all objects in the location
    return make_response(
        jsonify(
            client.list_objects(
                Bucket=conf['bucket'],
                Prefix='hacknight/',
                Delimiter='/'
            )
        ), 200
    )

#---------------------------------------
# photo - collection of sub-routines
# to call the camera, upload to S3 and store info in elasticsearch
#---------------------------------------


@app.route("/photo")
def photo():
    #---------------------------------------
    # Take photo
    #---------------------------------------
    filename = takePhoto()
    send_file('/tmp/' + filename, mimetype='image/jpeg')

    #---------------------------------------
    # Upload to S3 object store repository
    #    https://<s3 bucket>.<s3 endpoint>/<s3 key_name>  - stores the picture/object
    #---------------------------------------
    print("--- Writing image to S3 Object storage...")

    # S3 endpoint url  (s3.amazon.com)
    s3_endpoint = conf['endpoint']

    # get the S3 bucket name from the config.json file
    s3_bucket = conf['bucket']

    # the label or key name it will be called in S3
    # NOTE: the key_name can be things like 'my_pic' or 'my_pictures/my_pic'
    # the key_name will represented in S3 as <endpoint>/<key_name>
    s3_key_name = 'hacknight/' + filename

    # the item we are going to store in S3
    s3_object = filename

    # report path where the picture is uploaded
    s3_url = 'https://' + s3_bucket + '.' + s3_endpoint + '/' + s3_key_name
    print("--- S3 upload path: " + s3_url)

    try:
        # connect to S3 using boto3 API by passing access key and secret access keys.
        # the S3 endpoint is inferred from the key pair upon connection
        session = boto3.session.Session(
            aws_access_key_id=conf['access_key'],
            aws_secret_access_key=conf['secret_access_key']
        )
        s3 = session.resource(service_name='s3')

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
        os.remove('/tmp/' + filename)

    # handle any errors which might occur
    except botocore.exceptions.ClientError as e:
        print "Unexpected error during S3 upload: %s" % e

    #---------------------------------------
    # Post image to Elasticsearch for later searching
    #---------------------------------------
    try:
        print("--- Post image to Elasticsearch at: " + conf['elasticsearch_host'])
        es = Elasticsearch(
                            [conf['elasticsearch_host']],
                            port=443,
                            use_ssl=True,
                            )
        ts = int(round(time.time() * 1000))
        # data to post
        res = es.index(index='raspberries',
                       doc_type='ip_info',
                       id=ip_address,
                       body={
                           'hostname':  hostname,
                           'timestamp': ts,
                           'date':      datetime.datetime.now()
                       }
                       )
        print("--- Post complete: ")
        print(" response: '%s'" % (res))
        print(res['created'])

    # if error/exception occurs
    except elasticsearch.ElasticsearchException as es1:
        print "Unexpected error during Elasticsearch upload %s" % es1

    #---------------------------------------
    # Return success
    #---------------------------------------
    print (
        '--- Photo \'{0}\' taken and uploaded to S3 Object storage'.format(s3_key_name))
    # print ('## Photo \'%s\'taken and uploaded to S3 Object storage: %s',
    # s3_url )

    # generate a http return code of 200
    # HTTP Status Codes
    #   1xx Informational.
    #   2xx Success. ...
    #   3xx Redirection. ...
    #   4xx Client Error. ...
    #   5xx Server Error.
    return make_response(
        jsonify(
            {
                'message': 'Photo \'{0}\' taken and uploaded to S3 Object storage and metadata posted Elasticsearch.'.format(s3_key_name),
                's3_url' : s3_url,
                'elasticsearch_host' : conf['elasticsearch_host'],
                'image_key': s3_key_name,
            }
        ), 200
    )


#============================================================#
# main program - starts here
#============================================================#

if __name__ == '__main__':

    #---------------------------------------
    # read json formatted config file - load values for later use
    #---------------------------------------
    try:
        with open('config.json') as data_file:
            conf = json.load(data_file)
            conf['endpoint']
            conf['bucket']
            conf['access_key']
            conf['secret_access_key']
            conf['elasticsearch_host']
            conf['camera_command']

    # if error occurs in 'try' block - generate an exception message
    except Exception as e:
        sys.stderr.write(
            'FATAL: Cannot open or parse configuration file : ' + str(e) + '\n\n')
        exit()

    #---------------------------------------
    # get info about the current machine (wireless IP address)
    #---------------------------------------
    hostname = socket.gethostname()
    ip_address = get_ip_address('wlan0')

    #---------------------------------------
    # start the Flask web service
    #---------------------------------------
    app.run(host=ip_address, port=8080, debug=True)
