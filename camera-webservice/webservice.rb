require 'sinatra'
require 'json'
require 'aws-sdk'
require 'socket'
require 'elasticsearch'
require 'securerandom'
require 'date'

config = JSON.parse(File.read(File.dirname(__FILE__) + '/config.json'))

$endpoint = config['endpoint']
$bucket_name = config['bucket']
access_key = config['access_key']
secret_access_key = config['secret_access_key']
$camera_command = config['secret_access_key']

es_config = {host: config['elasticsearch_host']}

$es = Elasticsearch::Client.new(es_config)

cred = Aws::Credentials.new(access_key, secret_access_key)
$client = Aws::S3::Client.new(region: 'us-east-1', endpoint: $endpoint, credentials: cred, force_path_style: true, ssl_verify_peer: false)

# Return a test message for testing
get "/" do
  content_type :json
  {:message => "Webservice is running"}.to_json
end

# URL to take a photo
get "/take_photo" do
  content_type :json

  # Take photo and upload to StorageGRID  
  bucket = $bucket_name
  image_url = write_webcam_image_to_s3(bucket)

  # Log IP address of curent host into elasticsearch
  ip_address = Socket.ip_address_list[1].ip_address
  ts = DateTime.now.strftime('%Q').to_i
  $es.index index: 'raspberries', type: 'ip_info', id: ip_address, body: { timestamp: ts }

  # Return success message and URL to photo
  {:message => "Took photo with camera", :image_url => image_url}.to_json
end

def write_webcam_image_to_s3(bucket)
  # Create random name for image
  image_name = SecureRandom.hex(32) + ".jpg";
  
  # Take picture and store it as image_name
  cli_cmd = $camera_command + " " + image_name
  `#{cli_cmd}`

  # Open Image file & upload it to StorageGRID
  image_file = File.open(image_name, "r+")
  $client.put_object(bucket: bucket, key: image_name,
    metadata: { 'foo' => 'bar' },
    body: image_file.read,
    server_side_encryption: 'AES256'
  )
  image_file.close

  # Delete temporary image file from disk
  File.delete(image_file)

  # return full URL of image
  $endpoint + "/" + bucket + "/" + image_name
end
