#camera-webservice

## Summary: Python or Ruby based implementation
Two version are available, one in Ruby and one in Python; pick your poison! The webservice.py and webservice.rb programs were written for this Hack-night event.  You will not find any information specifically about the scripts, but you will find lots of information about the libraries used in the script.  

Which ever language you choose, the process to getting the webservice running is the same.  If you are really good, you can do step 1-4 in one go, but most hackers might find the incremental approach easier to follow.  

1. Install dependencies and then get the basic webservice running
2. Get the webservice to snap pictures
3. Get the webservice to upload images to S3
4. Get the webservice to upload meta data to ElasticSearch.

### Key learnings
Now is a good time to make sure you understand all the dependencies and packages that are needed.  Part of the learning is to understand what *'python-pip'* is, what *'boto3'* is used for and how it, and how to install Python and Ruby packages.  Learn about *flask* and *shotgun*.  The hack-night leader might stop and ask you what they are.

This is a good time to **"Ask Google"** - *"what is boto3"* or *"how to install boto3*.  These are all open source libraries and tools.    

### Python version - based on Flask - `webservice.py` ###
You will need to make sure Python and its dependencies are installed.  *Hint:* you will use `apt-get` and `pip`.

### Ruby version - based on Sinatra - `webservice.rb` ###
You will need to make sure Ruby and its dependencies are installed.  *Hint:* you will have to Google how to install Ruby on RaspberryPI and then you will load dependencies using `gem`.

### Common: Steps - Configure service - `config.json` ###
1. First rename the `config.json.example` to `config.json`
2. Next, update all parameters to meet your needs
**Note:** Use the same values you used previously.  
3. For the `camera_command` parameter these might be helpful:
  * Example linux USB camera: `fswebcam -r 640x480 --jpeg 85 --delay 1`
  * Example native raspberry camera module: `raspistill -o`

### Python: Step 1 - Install required packages.  Test the webservice.
The webservice.py script has the following dependencies. Make sure these are installed.
* OS Package dependencies: `python-pip`
* Python module dependencies: `flask flask-restful pillow boto3 elasticsearch picamera `
*Tip use:* `pip` *to install Python Modules*

* Start the webservice and check that it is running.
*Hint* Open the webservice.py program file and try to understand what it is doing.


### Ruby: Step 1 - Install required packages.  Test the webservice.
The webservice.rb script has the following dependencies. Make sure these are installed.
* OS Package dependencies: `ruby ruby-dev and install rvm and gems`
*    also install rubygems-update
* Ruby gem dependencies: `shotgun aws-sdk sinatra json elasticsearch`
*Tip:  use* `gem` *with the* `--no-document` *option to install the Ruby packages with no documentation - which decreases time to install!!*

    Install rvm, ruby and required gems (Ruby modules)
    %> apt-get install ruby ruby-dev
    %> gpg --keyserver hkp://keys.gnupg.net --recv-keys \
           409B6B1796C275462A1703113804BB82D39DC0E3
    %> \curl -sSL https://get.rvm.io | bash -s stable

* Start the webservice and check that it is running.
*Hint* Open the webservice.rb file and try to understand what it is doing.
* Run using: `shotgun --host 0.0.0.0 --port 8080 webservice.rb`


### Common: Step 2 - Test the webservice is running
* Load the browser to http://<ip address>:8080  
* Debug: if errors, check that the program packages are installed.

### Common: Step 3 - Test taking a simple picture
* Load the browser to http://<ip address>:8080/test
* Did you see a picture.  If the camera did not work, go back and test that fswebcam is working.

### Common: Step 4 - Test the S3 and ElasticSearch upload
* Load the browser to http://<ip address>:8080/photo
* If errors, check the S3 and ElasticSearch settings in the config.json file.


## More hacking ideas - Keep Going!
1. Add more key/value pair information to the ElasticSearch post.  If you were going to add meta data to an image, what sort of meta data might you include about the picture?
2. Upload a file to ElasticSearch - think what if I uploaded a perfstat to Elasticsearch every hour, then let Elasticsearch search and report on the information in the perfstat file.  Is this practical application.
3. Add object attributes to the S3 upload.  
4. Change the RESTful API calls.  If you don't like http://<ip_address>/test, change it to something else.  
5. If you tried the Python, try getting the Ruby version working.
