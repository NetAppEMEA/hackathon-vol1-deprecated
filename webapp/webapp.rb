#!/usr/bin/ruby
################################################################################
# Web Service Program
# Web app that displays a list of camera-webservice instances known to
# ElasticSearch allowing you to take photos.  Includes a Dockerfile for
# containerized use.
#
# This program uses three key tools Sinatra, Haml and Elasticsearch
# Sinatra - Sinatra is a free and open source software web application library
#         and domain-specific language written in Ruby. It is an alternative to
#         other Ruby web application frameworks such as Ruby on Rails, Merb,
#         Nitro, and Camping.
# Haml    - is a markup language predominantly used with Ruby that cleanly and
#         simply describes the HTML of any web document without the use of inline
#         code. It is a popular alternative to using Rails templating language
#         (.erb) and allows you to embed Ruby code into your markup.
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
# %> gem install shotgun haml unirest sinatra elasticsearch --no-document

#---------------------------------------
# include Ruby gem packages
# require <module/package>
#---------------------------------------
require 'sinatra'
require 'unirest'
require 'elasticsearch'
require 'date'
require 'bundler/setup'

#---------------------------------------
# configure Elasticsearch
#---------------------------------------

# Elasticsearch host address
# NOTE: use the same elasticsearch host from the camera-webservice config.json
# Example:    es_config = {host: "10.65.57.29:9200"}
#es_config = "https://search-netapp-hackernet1-ackkiroy2wwz72pevo63v7yx6u.us-west-2.es.amazonaws.com/"
# Elasticsearch host address
es_config         = { host: "https://search-netapp-hackernet-vjwfdxrvkvs56u6g6d56mwjhsi.us-west-2.es.amazonaws.com/" }


# instantiate Elasticsearch instance
es = Elasticsearch::Client.new(es_config)
Unirest.timeout(20)

#---------------------------------------
# Show welcome web page
#    http://<ip_address>/
#---------------------------------------
get "/" do

  # create ElasticSearch query
  # Get known raspberries/endpoints from Elasticsearch
  response = es.search index: 'raspberries', q: '*'
  @ips = []

  response['hits']['hits'].each do |r|
    @ips << r['_id']
  end

  haml :index
end

#---------------------------------------
# Show take photo page
#    http://<ip_address>/photo/<remote_raspi ip_address>
#---------------------------------------
get "/photo/:ip" do
  raspberry_ip = params[:ip]

  # Call webservice endopoint
  response = Unirest.get "http://#{raspberry_ip}:8080/photo"
  @image_url = response.body['image_url'].to_s

  haml :show_photo
end
