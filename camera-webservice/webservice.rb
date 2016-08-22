#!/usr/bin/ruby
################################################################################
# Camera Web Service Program
#
# This program uses two key tools Sinatra and Elasticsearch
# Sinatra - Sinatra is a free and open source software web application library
#         and domain-specific language written in Ruby. It is an alternative to
#         other Ruby web application frameworks such as Ruby on Rails, Merb,
#         Nitro, and Camping.
# Elasticsearch - is a search engine based on Lucene. It provides a distributed,
#         multitenant-capable full-text search engine with an HTTP web interface
#         and schema-free JSON documents.
#
# Run this program
#         %> shotgun --host 0.0.0.0 --port 8080 webservice.rb
#
#
################################################################################

# Ruby pagackage installation instructions - using 'gem'
# gem is a package management system used to install and manage ruby packages
#---------------------------------------
#  Install rvm, ruby and required gems (Ruby modules)
#  %> apt-get install ruby ruby-dev
#  %> gpg --keyserver hkp://keys.gnupg.net --recv-keys \
#         409B6B1796C275462A1703113804BB82D39DC0E3
#  %> \curl -sSL https://get.rvm.io | bash -s stable
#  <<logout and login again>>
#  %> gem install rubygems-update
#  %> gem install shotgun aws-sdk sinatra json elasticsearch --no-document

#---------------------------------------
# include Ruby gem packages
# require <module/package>
#---------------------------------------
require 'sinatra'
require 'json'
require 'aws-sdk'
require 'socket'
require 'elasticsearch'
require 'securerandom'
require 'date'

#---------------------------------------
# parse config.json file and extract key/value pairs
#---------------------------------------
config = JSON.parse(File.read(File.dirname(__FILE__) + '/config.json'))

# S3 values
$region           = config['region']
$endpoint         = config['endpoint']
$http_endpoint    = 'https://' + $endpoint
$bucket_name      = config['bucket']
access_key        = config['access_key']
secret_access_key = config['secret_access_key']

# camera command
$camera_command   = config['camera_command']

# Elasticsearch host address
es_config         = { host: config['elasticsearch_host'] }

#---------------------------------------
# initialize ElasticSearch instance
#---------------------------------------
$es = Elasticsearch::Client.new(es_config)

#---------------------------------------
# Return a test message for testing
#---------------------------------------
get '/' do
    content_type :json
    { message: 'Webservice is running' }.to_json
end

#---------------------------------------
# URL to take a photo
#---------------------------------------
get '/take_photo' do
    content_type :json

    #---------------------------------------
    # Take photo
    #---------------------------------------
    # get date/time to use in filename
    now = Time.now.strftime("%Y%m%d-%H%M%S")

    # Create random name for image
    image_filename = now + '.jpg'
    puts "image_filename: " + image_filename

    temp_image_filename = '/tmp/' + image_filename

    puts 'INFO: Smile the camera is taking a picture.'
    puts '      $cli_cmd'
    # Take picture and store it as image_name
    cli_cmd = $camera_command + ' ' + temp_image_filename
    `#{cli_cmd}`

    #---------------------------------------
    # Upload to S3 object store repository
    #    https://<s3 bucket>.<s3 endpoint>/<s3 key_name>  - stores the picture/object
    #---------------------------------------
    # # Take photo and upload to StorageGRID
    # print out config info for debug
    puts 'INFO: config.json values'
    puts '      S3 endpoint:      '   + $endpoint
    puts '      S3 endpoint (http): ' + $http_endpoint

    # initialize S3 connection instance
    s3 = Aws::S3::Client.new(region: $region,
                             endpoint: $http_endpoint,
                             access_key_id: access_key,
                             secret_access_key: secret_access_key,
                             force_path_style: true,
                             ssl_verify_peer: false)

    # return full URL of image
    image_url = $http_endpoint + '/' + $bucket_name + '/' + image_filename

    # Open Image file & upload it to StorageGRID
    File.open(temp_image_filename, 'rb') do |image_file|
        s3.put_object(bucket: $bucket_name,
                      key:  'hacknight/' + image_filename,
                      body: image_file)
    end
    #image_file.close

    # Delete temporary image file from disk
    File.delete(temp_image_filename)

    #---------------------------------------
    # Post image to Elasticsearch for later searching
    #---------------------------------------
    # # Log IP address of curent host into elasticsearch
    ip_address = Socket.ip_address_list[1].ip_address

    # $es.index index: 'raspberries', type: 'ip_info', id: ip_address, body: { timestamp: now }

    # # Return success message and URL to photo
    {:message => "Took photo with camera", :image_url => image_url}.to_json

    { message: 'Took photo with camera',
      image_name: image_filename,
      image_saved_at: temp_image_filename,
      cli_cmd: cli_cmd,
      image_url: image_url }.to_json
end
