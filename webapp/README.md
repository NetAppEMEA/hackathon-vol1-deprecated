# webapp

One service is available:

* `webapp.rb`: Web app written in Ruby using Sinatra. Includes a Dockerfile for containerized use.
* Use the dockerfile to build a container and run it on your laptop/host

%> gem install shotgun haml unirest sinatra elasticsearch --no-document

### Setup Docker and web app (webapp)
Install docker machine on your laptop, test some containers (try Ubuntu and httpd), clone web app from github, build a container for your web app, start container, verify you can access and take a photo.

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


##Basic instructions webclient (docker container)
 	1. Download and install docker toolbox on your pc (or docker engine on a linux box if you have one somewhere on the NetApp network)

 	2. Open the docker quickstart terminal MINGW32

 	3. Run a simple container to verify it works (try other words instead of boo):
 	docker run docker/whalesay cowsay boo
 	docker ps –a
 	docker images

 	4. And another, this time lets run Ubuntu latest with an interactive shell:
 	$ docker run -it ubuntu:latest bash
 	root@93330ed8220c:/# cat /etc/*rel*
 	DISTRIB_ID=Ubuntu
 	DISTRIB_RELEASE=16.04
 	DISTRIB_CODENAME=xenial
 	DISTRIB_DESCRIPTION="Ubuntu 16.04 LTS"
 	root@93330ed8220c:/# ps -ef
 	UID        PID  PPID  C STIME TTY          TIME CMD
 	root         1     0  1 09:45 ?        00:00:00 bash
 	root         9     1  0 09:45 ?        00:00:00 ps –ef
 	root@93330ed8220c:/# exit

 	5. Or a webserver with Apache httpd latest:
 	$ docker run -dit -p 9000:80 httpd:latest
 	$ docker ps
 	CONTAINER ID        IMAGE                                  COMMAND                  CREATED             STATUS              PORTS                                                       NAMES
 	00612874ff26        httpd:latest                           "httpd-foreground"       3 seconds ago       Up 2 seconds        0.0.0.0:9000->80/tcp                                        hungry_williams
 	<<So this is mapping port 80 in the container to port 9000 on the docker host.  Run docker-machine ip to get your docker host IP.  Then open http://DOCKER-MACHINE-IP:9000 and see if it works>>
 	<<Now exec a command to open shell in that container>>
 	$ docker exec -i -t 006 bash
 	root@00612874ff26:/usr/local/apache2# ps -ef
 	UID        PID  PPID  C STIME TTY          TIME CMD
 	root         1     0  0 10:05 ?        00:00:00 httpd -DFOREGROUND
 	daemon       6     1  0 10:05 ?        00:00:00 httpd -DFOREGROUND
 	daemon       7     1  0 10:05 ?        00:00:00 httpd -DFOREGROUND
 	daemon       8     1  0 10:05 ?        00:00:00 httpd -DFOREGROUND
 	root        90     0  0 10:05 ?        00:00:00 bash
 	root        93    90  0 10:05 ?        00:00:00 ps –ef
 	root@00612874ff26:/usr/local/apache2# kill 1
 	<<Because you killed the process that initiated the container it now stops too!>
 	$ docker ps
 	CONTAINER ID        IMAGE                                  COMMAND                  CREATED             STATUS              PORTS                                                       NAMES
 	 
 	6. Clone the hackathon repo from git to get the webclient code and cd into it:
 	$ git clone https://github.com/NetAppEMEA/hackathon-vol1
 	$ cd hackathon-vol1/webapp

  7. Edit the webapp to set your desired camera IP
 	cd hackathon-vol1/webapp
 	nano webapp.rb

  8. Build and run container
 	$ cd hackathon-vol1/webapp
 	$ docker build -t netapp/webapp .
 	$ docker images
 	$ docker run -p 8081:8081 netapp/webapp

  9. Go to http://DOCKER-MACHINE-IP:8081 and see if it loads.  Take a picture and see if it loads.

  10. Start hacking.  Change to manage a different camera (don’t forget to stop your container or run a new one on a different port), or extend the service to allow taking photos from multiple cameras, or whatever.  Hack!

##Docker Tips and Tricks
 	• %> docker build -t my_webservice .
 	• %> docker run -name my_webservice_1 -i -t my_webservice
 	• %> docker ps
 	• %> docker ps -l
 	• %> docker kill <id>
 To detach yourself from the container, use the escape sequence CTRL+P followed by CTRL+Q.
