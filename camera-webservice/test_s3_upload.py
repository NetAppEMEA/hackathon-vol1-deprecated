#!/usr/bin/python
################################################################################
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
################################################################################

# Python pagackage installation instructions - using 'pip' 
# pip is a package management system used to install and manage python packages
#--------------------------------------- 
# %> pip install flask flask-restful pillow boto3 json elasticsearch


# Include/import elasticsearch
from elasticsearch     import Elasticsearch

# Import native python libraries
import time, socket, uuid, os, boto3, json, sys
from boto3.s3.transfer import S3Transfer



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
	sys.stderr.write('FATAL: Cannot open or parse configuration file : ' + str(e) + '\n\n')
	exit()



try:
        s3_object   = "/home/pi/hackathon-vol1/camera-webservice/4e0b2dd2-1658-4537-91a4-3bd4176c278b.jpg"
        s3_key_name = 'nacknight/4e4b2dd2-1658-4537-91a4-3bd4176c278b.jpg'

	#--------------------------------------- 
	# Upload to S3 object store repository
	#--------------------------------------- 
        session = boto3.session.Session(
            aws_access_key_id=conf['access_key'], 
            aws_secret_access_key=conf['secret_access_key']
        )
        s3 = session.resource(service_name='s3')
        obj = s3.Object(
            conf['bucket'], 
            s3_key_name 
        )
        obj.upload_file(s3_object)
        #os.remove(filename)

        #s3 = boto3.resource('s3')

        for bucket in s3.buckets.all():
            print("INFO: Bucket \'%s\' contains the following object keys" % bucket.name)
            
            # list objects in the bucket
            for obj in bucket.objects.all():
                print("\t%s" % obj.key)

        print("\n")

        # # upload a new file
        # data = open(filename, 'rb')
        # s3.Bucket(conf['bucket']).put_object(Key=filename_str, Body=data)

        # client   = boto3.client(
        #    's3',
        #    aws_access_key_id=conf['access_key'], 
        #    aws_secret_access_key=conf['secret_access_key']
        # )
        # transfer = S3Transfer(client)
        # transfer.upload_file(
        #    filename, 
        #    conf['bucket'],
        #    filename
        # ) 

# if error occurs in 'try' block - generate an exception message
except Exception as e:
	print("FATAL: Problem uploading file to S3 Bucket.\n")
        print("       %s\n" % e)
	exit()


try: 
	#--------------------------------------- 
	# Post image to Elasticsearch for later searching
	#--------------------------------------- 
	# es = Elasticsearch([conf['elasticsearch_host']])
	# ts = int(round(time.time() * 1000))
	# res = es.index(index='raspberries', doc_type='ip_info', id=ip_address, body={ 'timestamp': ts })
	# print(res['created'])
        print("INFO: Elasticsearch commented out for now\n");

# if error occurs in 'try' block - generate an exception message
except Exception as e:
	print("FATAL: Problem writing to Elascticsearch .\n")
        print("       %s\n" % e)
	exit()

#--------------------------------------- 
# Return success
#--------------------------------------- 
print ("INFO: program done\n");



