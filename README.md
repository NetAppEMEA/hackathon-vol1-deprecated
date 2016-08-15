# hackathon-vol1 -- NetApp's Hackers Night!

![alt text](https://cloud.githubusercontent.com/assets/917241/15464979/702523d0-20d2-11e6-8d88-2b71e30863d5.png "Your Challenge")

![alt text](https://cloud.githubusercontent.com/assets/8753615/17655610/1e46e3e4-6265-11e6-80b2-a80222830ede.jpg "Challenge #1")

![alt text](https://cloud.githubusercontent.com/assets/8753615/17655608/1caa42f6-6265-11e6-844a-8e624ff35ef7.jpg "Challenge #2")



Software in this repo includes two services:

* **camera-webservice**: Web service that exposes a RESTful API to use a local webcam to take a photo, upload it to an S3 target, and post metadata to ElasticSearch.  Two versions are available, one written in Ruby and another in Python. This can be deployed on a laptop or e.g., on a Raspberry Pi.
* **webapp**: Web app that displays a list of camera-webservice instances known to ElasticSearch allowing you to take photos.  Includes a Dockerfile for containerized use.

*Note: Config must be set prior to build/run.*

## Plan of attack:

### Step 0: Pre-work or Initial Getting Started
* You will access the RaspberryPI using ssh.  
** If you are on a Mac, you can simply open a Terminal window and type %> ssh pi@<rasppi IP address>
** If you are using Windows install a tool like Putty

### Step 1: Setup S3 accessible storage
* Create a new storage tenant, new bucket, permissions to allow anonymous read access to the bucket via bucket policies
* Verify success by putting data using a S3 client and downloading it via a web browser

*Hints*

* Get NetApp SGWS system and credentials from the hackers night leaders
  Alternatively you can setup an AWS S3 bucket.
* Recommended S3 clients are S3 browser for Win, and CyberDuck for Mac (CyberDuck won't allow you to set Bucket Policies)
* Manage bucket permissions from your S3 client.  Check repo for sample policy: `bucket_policy.json`
* On MacOSX, can also use s3cmd: `s3cmd setpolicy bucket_policy.json s3://bucketname` (make sure to configure s3cmd before that)

### Step 2: Setup Raspberry Pi and camera web service (camera-webservice)
Perform a NOOB/raspbian installation - you will need a mouse/keyboard/monitor for the initial setup.  
Once connected; make note of IP address and potentially move Pi somewhere in the building and Connect headless using ssh.
Install camera app and take a photo.
Install git and ruby, install rvm and gems.
Clone camera web service from github, update S3 and other details it will use, run camera web service and verify you can take a photo

*Hints*

* To grow the filesystem, check out raspi-config (this may not be needed if using the latest NOOB/raspbian distribution)
* The camera app to install for a USB webcam is called fswebcam, and don’t forget if using a native Raspberry camera, you have to enable it
     If webcam is still not working (built-in camera on RaspberryPI 3 B unit)
	pi@raspberrypi_01:~ $ fswebcam
	--- Opening /dev/video0...
	stat: No such file or directory
	pi@raspberrypi_01:~ $ vcgencmd get_camera
	supported=1 detected=1
	pi@raspberrypi_01:~ $ sudo modprobe bcm2835-v4l2
	pi@raspberrypi_01:~ $ ls /dev/video0 
* Use git to clone the repo and configure the `camera-webservice`
* Configure using `config.json`; details found in README.md within the camera-webservice dir
* Once running, it exposes a URI that accepts a GET request: `/take_photo`

### Step 3: Setup Docker and web app (webapp)
Install docker machine on your laptop, test some containers (try Ubuntu and httpd), clone web app from github, build a container for your web app, start container, verify you can access and take a photo.
Docker can now run fully packed under MacOSX (https://docs.docker.com/docker-for-mac/) and also Windows.

*Hints*

* Use git to clone the repo and configure the `webapp`
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
* Get the IP of your docker host: (might not be needed any more in the new semi-native Docker version for MacOSX/Windows)
 *  `docker-machine ip`
* You can also run the webservice manually, but then you also need to install all the gems as did on the camera-webservice:
 * `shotgun --host 0.0.0.0 --port 8081 webapp.rb`

### Step 4: Do more!
Try the python based camera web service on your Raspberry Pi and from your laptop, check out ElasticSearch and see what’s in it, use your smart phone somehow, make a web app to show all the photos, etc!
