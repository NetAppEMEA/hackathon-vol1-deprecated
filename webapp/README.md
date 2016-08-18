# webapp

One service is available:

* `webapp.rb`: Web app written in Ruby using Sinatra. Includes a Dockerfile for containerized use.
* Use the dockerfile to build a container and run it on your laptop/host

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
