#camera-webservice

## Summary: Python or Ruby based implementation
Two version are available, one in Ruby and one in Python; pick your poison! The webservice.py and webservice.rb programs were written for this Hack-night event.  You will not find any information specifically about the scripts, but you will find lots of information about the libraries used in the script.  

Which ever language you choose, the process to getting the webservice running is the same.  If you are really good, you can do step 1-4 in one go, but most hackers might find the incremental approach easier to follow.  

1. Get the webservices running
2. Get the webservice to snap pictures
3. Get the webservice to upload images to S3
4. Get the webservice to upload meta data to ElasticSearch.

### Key learnings
Now is a good time to make sure you understand all the dependencies and packages that are needed.  Part of the learning is to understand what *'python-pip'* is, what *'boto3'* is used for and how it, and how to install Python and Ruby packages.  Learn about *flask* and *shotgun*.  The hack-night leader might stop and ask you what they are.

This is a good time to **"Ask Google"** - *"what is boto3"* or *"how to install boto3*.  These are all open source libraries and tools.    

### Python version - based on Flask - `webservice.py` ###
* OS Package dependencies: `python-pip`
* Python module dependencies: `flask flask-restful boto3 elasticsearch`
* On Windows: the above plus python module `pillow` and [CommandCam](https://batchloaf.wordpress.com/commandcam/ "CommandCam") photo software placed in same directory as `webservice.py`

### Ruby version - based on Sinatra - `webservice.rb` ###
* Install Ruby - OS Package dependencies: `ruby ruby-dev`
* Ruby gem dependencies: `sinatra shotgun aws-sdk json elasticsearch` *Tip:  use the* `--no-document` *option to decrease time to install!!*
* Run using: `shotgun --host 0.0.0.0 --port 8080 webservice.rb`


### Common: Steps - Configure service - `config.json` ###
1. First rename the `config.json.example` to `config.json`
2. Next, update all parameters to meet your needs
**Note:** Use the same values you used previously.  
3. For the `camera_command` parameter these might be helpful:
  * Example linux USB camera: `fswebcam -r 640x480 --jpeg 85 --delay 1`
  * Example native raspberry camera module: `raspistill -o`
  * Example windows usb camera: `CommandCam.exe /quiet /filename`

### Python: Step 1 - Install required packages.  Test the webservice.
The webservice.py script has the following dependencies. Make sure these are installed.
* OS Package dependencies: `python-pip`
* Python module dependencies: `flask flask-restful boto3 elasticsearch`

* Start the webservice and check that it is running.
*Hint* Open the webservice.py file and try to understand what it is doing.

### Ruby: Step 1 - Install required packages.  Test the webservice.
The webservice.rb script has the following dependencies. Make sure these are installed.
* OS Package dependencies: `ruby ruby-dev`
* Ruby gem dependencies: `sinatra shotgun aws-sdk json elasticsearch`
*Tip:  use* `--pip--` *with the* `--no-document` *option to decrease time to install!!*

* Start the webservice and check that it is running.
*Hint* Open the webservice.rb file and try to understand what it is doing.
* Run using: `shotgun --host 0.0.0.0 --port 8080 webservice.rb`


### Common: Step 2 - Test the webcamera
* Verify that images are being taken.  
* Why aren't the images saved?

### Common: Step 3 - Test the S3 Object upload
* View the objects using the S3 Browser/CyberDuck.
* Change the bucket the images a place in.

### Common: Step 4 - Test the ElasticSearch upload
* Modify/Add ElasticSearch meta data being uploaded.
* Look at the uploaded data using the ElasticSearch Toolbox
