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


#--------------------------------------- 
# include Python packages
# from <module/package> include <functions>
#--------------------------------------- 
# Include/import Flask and its functional libraries
from flask             import Flask, jsonify,  abort,    make_response,  request
from flask_restful     import Api,   Resource, reqparse, fields, marshal

# Include/import boto3 package for S3 object store handling
from boto3.s3.transfer import S3Transfer

# Include/import elasticsearch
from elasticsearch     import Elasticsearch

# Import native python libraries
import time, socket, uuid, os, boto3, json, sys


#--------------------------------------- 
# check if this script is running on Windows
#--------------------------------------- 
#    os.name The name of the operating system dependent module imported. 
#    The following names have currently been registered: 'posix', 'nt', 'mac', 'os2', 'ce', 'java', 'riscos'.
if os.name == 'nt':
	from PIL import Image

#--------------------------------------- 
# create instance of Flask and Flask-RESTful API
#--------------------------------------- 
# create an instance of Flask - __name__ is the name of application running - in this case 'camera-webservice'
app = Flask(__name__, static_url_path="")

# create an instance of the RESTful Api
api = Api(app)


#============================================================ 
# Sub-routines
#============================================================ 

#--------------------------------------- 
# return IP address subroutines
#--------------------------------------- 
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

#--------------------------------------- 
# RootAPI is the class which gets called when the http://<ip address>/ is called
#--------------------------------------- 
class RootAPI(Resource):

        # return a HTML message in the browser indicating the Webservice is running
	def get(self):
		return make_response(jsonify({'message' : "Webservice is running.<br>To take picture http://<ip>:8080/take_photo"}), 200)
	
#--------------------------------------- 
# TakePhotoAPI - collection of sub-routines
# to call the camera, upload to S3 and store info in elasticsearch
#--------------------------------------- 
class TakePhotoAPI(Resource):

        # what to do when a web call is made 
	def get(self):
		return self.post()

        # this proc gets called when a POST called gets made 
	def post(self):
		# Maybe do something with post variables later...
		try:
			req = request.json		
		except:
			pass

                #--------------------------------------- 
		# Take photo
                #--------------------------------------- 
                try: 
                    # create randomized filename 
                    # uuid4() generates a random UUID. The chance of a collision is really, really, 
                    #         really small. Small enough, that you shouldn't worry about it.
	            filename = str(uuid.uuid4())

                    # if Windows OS
	            if os.name == 'nt':
                        # make system call to call camera executable 
                        # in this case      conf['camera_command'] is something like 'fswebcam -r 640x480 --jpeg 85 --delay 1'
	            	os.system(conf['camera_command'] + ' ' + filename)

                        # get the file from the camera
	            	im = Image.open(filename)
                        # rename the file with the .jpg file extension
	            	im.save(filename + '.jpg', 'JPEG')

                        # remove the temp file which is missing the .jpg extension 
	            	os.remove(filename)
                        # filename now includes the .jpg extension
	            	filename += '.jpg'

                    # if not Windows OS
	            else:
                        # add .jpg file extension to the pictures filename
	            	filename += '.jpg'

                        # make system call to call camera executable 
                        # in this case      conf['camera_command'] is something like 'fswebcam -r 640x480 --jpeg 85 --delay 1'
	            	os.system(conf['camera_command'] + ' ' + filename)

		# if error occurs in 'try' block - generate an exception message
		except Exception as e:
			print('ERROR: Problem occured while snapping picture.\n')
                        print('       %s\n', e)
                        # return HTTPS status code - server error (status code 500)
		        return make_response(jsonify({'message' : "Problem occured while snapping picture.", "ERROR_MSG" : e}), 500)
			exit()

		
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
                #       the key_name will represented in S3 as <endpoint>/<key_name>
                s3_key_name = 'nacknight/' + filename

                # the item we are going to store in S3
                s3_object   = filename

                # report path where the picture is uploaded
                s3_url      = 'https://' + s3_bucket + '.' + s3_endpoint + '/' + s3_key_name
        
                # connect to S3 using boto3 API by passing access key and secret access keys.  
                # the S3 endpoint is inferred from the key pair upon connection
                session = boto3.session.Session(
                    aws_access_key_id=conf['access_key'], 
                    aws_secret_access_key=conf['secret_access_key']
                )
                s3 = session.resource(service_name='s3')
                
                # defined a new S3 object by specifying the bucket and key_name that you will store the file
                obj = s3.Object(
                    s3_bucket,
                    s3_key_name 
                )

                # upload the actual file/object to S3
                obj.upload_file(s3_object)

                # remove local copy of the picture we just took
                os.remove(filename)

                #--------------------------------------- 
		# Post image to Elasticsearch for later searching
                #--------------------------------------- 
                print("--- Post image to Elasticsearch at %s...", conf['elasticsearch_host'])
	        es = Elasticsearch([conf['elasticsearch_host']])
	        ts = int(round(time.time() * 1000))
	        res = es.index(index='raspberries', doc_type='ip_info', id=ip_address, body={ 'timestamp': ts })
	        print(res['created'])

		
                #--------------------------------------- 
		# Return success
                #--------------------------------------- 
		print ('## Photo \'%s\'taken and uploaded to S3 Object storage: %s', s3_url )

                # generate a http return code of 200
                # HTTP Status Codes
                #   1xx Informational. 
                #   2xx Success. ...
                #   3xx Redirection. ...
                #   4xx Client Error. ...
                #   5xx Server Error.
		return make_response(jsonify({'message' : "Photo taken with RaspberryPI camera and image updated to S3 Object storage:", "image_url" : s3_url}), 200)


#============================================================# 
# main program - starts here
#============================================================# 

# when a call is make to http://<ip address>:<port>/take_photo
# call the class TakePhotoAPI
api.add_resource(TakePhotoAPI, '/take_photo')

# when a call is make to http://<ip address>:<port>/
# call the class RootAPI
api.add_resource(RootAPI, '/')

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
		sys.stderr.write('FATAL: Cannot open or parse configuration file : ' + str(e) + '\n\n')
		exit()

        #--------------------------------------- 
        # get the IP address of the current machine
        #--------------------------------------- 
	ip_address = get_ip_address()

        #--------------------------------------- 
        # start the Flask web service
        #--------------------------------------- 
	app.run(host='0.0.0.0', port=8080, debug=True )


