# Hack-night instructions

The hack-night is intended to be a lightly structured event designed to allow hackers to explore, innovate and learn.  The following instructions are provided as general roadmap to provide some structure.

## What's Level Hacker Are You?
Hackers are encouraged and should feel free to customize their work as they choose.

* **Novice hackers (NOOBS):**
May want to follow the activity outline more closely. They may want to pair up with another Intermediate hacker for additional support.  Novice hackers should definitely review the PREWORK.md document prior to the event to make sure they are prepared to get the most out of the event.

The instructions provided below are most likely not detailed enough for a novice hacker.  Please contact the hack-night lead for additional supporting documentation - which provids a few more step-by-step instructins.

* **Intermediate hackers:**
The instructions below are written with the Intermediate hacker in mind.  The instructions are intentionally terse with the assumption that the hacker will use resources like **Google** to provide missing information.  

The intermediate hacker should explore inside the files provided in Git to look for opportunities to customize, extend and improve the implementation.

If you are already familiar with learnings in a particular portion of the instructions, move along as quickly as you like to the next section where you can explore new ideas and technology.    

* **Advanced hackers:**
Advanced should scan the below instructions and then create there own roadmap or project.  Advanced users are also welcome to come in with their own project or an idea for advanced integration.

* **Other Hacker ideas:**
See the file named OtherHackerIdeas.md for some potentially interesting extensions to the hack-night activity.  Please feel free to share these ideas with the rest of the team - specifically with a focus on how these help NetApp SE's better understand 3rd Platform/DevOps customers and sales motion.  

## Getting help
Google and Youtube is how the modern developer learns.  If you have a question, are getting an error message, or need to learn to do something - **Try Google first**.

If you then get stuck - ask your teammates - We are **"Team NetApp"** - never fail alone!

If you are still stuck - ask a hack-night lead for help.

## Hack-night Modules
The hack-night instructions are divided into modules to help provide structure and to help the hack-night leaders assess progress.

### *=> START HERE* Get the latest Hack-night files from GitHub
You will want to get (clone) the hack-night files from https://github.com/NetAppEMEA/hackathon-vol1


### Module 0: Pre-Hack Night work
Look in a file named PREWORK.md which details suggested activities to do **BEFORE** coming to hack-night.  It is encouraged that all hackers read thru the PREWORK.md document - even if that means you are doing that during the even.  

### Module 1: Connect to RaspberryPI, Take Picture and View the image
1. SSH to remotely connect to your RaspberryPI.
2. Install the fswebcam and figure out how to take a picture.
Hint: Google "fswebcam"
Note: You may need to run the following command to load the camera driver.
*%> sudo modprobe bcm2835-v4l2*
3. Copy the image back to your PC (using SCP) and view the image.

### Module 2: Connect to S3 and Create a Bucket - Connect to ElasticSearch
* For security reasons, the instructor will provide an email which contains information on how to connect to the SGWS S3.  The same email will provide instructions for connecting to the ElasticSearch server.

1. Install a S3 browser tool like "*S3 browser*" for Windows or "*CyberDuck*" for Mac Note: CyberDuck won't allow you to set Bucket Policies.
2. Connect, create a S3 bucket, then upload/download a file or image.
3. Install an ElasticSearch Toolbox and connect to the ElasticSearch server.

### Module 3: Setup RaspberryPI Camera Webservice
* The files and instructions you need are in the *camera-webservice* directory.
* You will have the opportunity to use either the Python or the Ruby based webservice code.  

### Module 4: Get Webservice to upload S3 images
Instructions are in the *camera-webservice/README.md* file

### Module 5: Get Webservice to upload ElasticSearch data
Instructions are in the *camera-webservice/README.md* file

### Module 6: Explore and search with ElasticSearch
Using the ElasticSearch Toolbox tools explore the data updated by all the hackers.  Come up with an idea of what to search.  Update the your webservice to add additional meta data to upload.

### Module 7: Setup Docker and web app (webapp)
This module will be performed on your laptop and will not require the RaspberryPI.

* The files and instructions can be found in the *webapp* directory.  
