#!/usr/bin/python
# pip install flask flask-restful pillow boto3 json elasticsearch

from flask import Flask, jsonify, abort, make_response, request
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
import time, socket, uuid, os, boto3, json, sys
from elasticsearch import Elasticsearch
if os.name == 'nt':
	from PIL import Image

app = Flask(__name__, static_url_path="")
api = Api(app)

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

class RootAPI(Resource):

	def get(self):
		return make_response(jsonify({'message' : "Webservice is running"}), 200)
	
class TakePhotoAPI(Resource):

	def get(self):
		return self.post()

	def post(self):
		# Maybe do something with post variables later...
		try:
			req = request.json		
		except:
			pass

		# Take photo
		filename = str(uuid.uuid4())
		if os.name == 'nt':
			os.system(conf['camera_command'] + ' ' + filename)
			im = Image.open(filename)
			im.save(filename + '.jpg', 'JPEG')
			os.remove(filename)
			filename += '.jpg'
		else:
			filename += '.jpg'
			os.system(conf['camera_command'] + ' ' + filename)

		# Upload to S3
		session = boto3.session.Session(aws_access_key_id=conf['access_key'], aws_secret_access_key=conf['secret_access_key'])
		s3 = session.resource(service_name='s3', endpoint_url=conf['endpoint'], verify=False)
		obj = s3.Object(conf['bucket'], filename)
		obj.upload_file(filename)
		os.remove(filename)
		url = conf['endpoint'] + "/" + conf['bucket'] + "/" + filename
		
		# Post to ES
		es = Elasticsearch([conf['elasticsearch_host']])
		ts = int(round(time.time() * 1000))
		res = es.index(index='raspberries', doc_type='ip_info', id=ip_address, body={ 'timestamp': ts })
		print(res['created'])

		
		# Return success
		print ('## Took photo and saved it at: ' + url)
		return make_response(jsonify({'message' : "Took photo with camera", "image_url" : url}), 200)

api.add_resource(TakePhotoAPI, '/take_photo')
api.add_resource(RootAPI, '/')

if __name__ == '__main__':

	try:
		with open('config.json') as data_file:    
			conf = json.load(data_file)
			conf['endpoint']
			conf['bucket']
			conf['access_key']
			conf['secret_access_key']
			conf['elasticsearch_host']
			conf['camera_command']
	except Exception as e:
		sys.stderr.write('FATAL: Cannot open or parse configuration file : ' + str(e) + '\n\n')
		exit()

	ip_address = get_ip_address()
	app.run(host='0.0.0.0', port=8080, debug=True )

