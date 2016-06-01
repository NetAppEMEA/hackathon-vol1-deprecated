# hackathon-vol1 -- NetApp's first Hackers Night!

![alt text](https://cloud.githubusercontent.com/assets/917241/15464979/702523d0-20d2-11e6-8d88-2b71e30863d5.png "Your Challenge")


Software in this repo includes two services:

* **camera-webservice**: Web service that exposes a RESTful API to use a local webcam to take a photo, upload it to an S3 target, and post metadata to ElasticSearch.  Two versions are available, one written in Ruby and another in Python.
* **webapp**: Web app that displays a list of camera-webservice instances known to ElasticSearch allowing you to take photos.  Includes a Dockerfile for containerized use.  

*Note: Config must be set prior to build/run.*

## Plan of attack:

### Step 1: Setup S3 accessible storage
Create a new tenant, new bucket, permissions to allow ‘everyone’ read access
verify success by putting data using a S3 client and getting via a web browser

*Hints*

* Get NetApp SGW system and credentials from the hackers night leaders
* Recommended S3 clients are S3 browser for Win, and CyberDuck for Mac
* Manage bucket permissions from your S3 client.  Check repo for sample  `bucket_policy.json`
* On MacOSX, can also use s3cmd: `s3cmd setpolicy bucket_policy.json s3://bucketname` (make sure to configure s3cmd before that)

### Step 2: Setup Raspberry Pi and camera web service (camera-webservice)
Perform a raspbian OS minimal installation, grow filesystem, make note of IP address and potentially move Pi somewhere in the building, install camera app and take a photo, install git and ruby, install rvm and gems, clone camera web service from github, update S3 and other details it will use, run camera web service and verify you can take a photo

*Hints*

* To grow the filesystem, check out raspi-config
* The camera app to install for a USB webcam is called fswebcam, and don’t forget if using a native Raspberry camera, you have to enable it
* Use git to clone the repo and configure the `camera-webservice`
* Configure using `config.json`; details found in README.md within the camera-webservice dir
* Once running, it exposes a URI that accepts a GET request: `/take_photo`

### Step 3: Setup Docker and web app (webapp)
Install docker machine on your laptop, test some containers (try Ubuntu and httpd), clone web app from github, build a container for your web app, start container, verify you can access and take a photo

*Hints*

* Use git to clone the repo and configure the `webapp`
* Get the IP of your docker host:
 *  `docker-machine ip`
* Show local container images:
 *  `docker images`
* Run a container:
 *  `docker run --rm -p 8081:8081 <image_id>`
* Show all running containers:
 *  `docker ps`
* Stop a running container:
 *  `docker stop <id>`
* Exec a command (like a shell) into a running container:
 *  `docker exec -it <container-name-or-id> bash`
* Build a container:
 *  `docker build -t netapp/hacker .`
* You can also run the webservice manually, but then you also need to install all the gems as did on the camera-webservice:
 * `shotgun --host 0.0.0.0 --port 8081 webapp.rb`

### Step 4: Do more!
Try the python based camera web service on your Raspberry Pi and from your laptop, check out ElasticSearch and see what’s in it, use your smart phone somehow, make a web app to show all the photos, etc!
