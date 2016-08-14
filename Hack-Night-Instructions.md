# Hack-night instructions

The hack-night is intended to be a lightly structured event designed to allow hackers to explore, innovate and learn.  The following instructions are provided as general roadmap to provide some structure.

## What's Level Hacker Are You?
Hackers are encouraged and should feel free to customize their work as they choose.

* Novice hackers (NOOBS)
May want to follow the activity outline more closely. They may want to pair up with another Intermediate hacker for additional support.  Novice hackers should definitely review the PREWORK.md document prior to the event to make sure they are prepared to get the most out of the event.

The instructions provided below are most likely not detailed enough for a novice hacker.  Please contact the hack-night lead for additional supporting documentation - which provids a few more step-by-step instructins.

* Intermediate hackers
The instructions below are written with the Intermediate hacker in mind.  The instructions are intentionally terse with the assumption that the hacker will use resources like **Google** to provide missing information.  

The intermediate hacker should explore inside the files provided in Git to look for opportunities to customize, extend and improve the implementation.

If you are already familiar with learnings in a particular portion of the instructions, move along as quickly as you like to the next section where you can explore new ideas and technology.    

* Advanced hackers
Advanced should scan the below instructions and then create there own roadmap or project.  Advanced users are also welcome to come in with their own project or an idea for advanced integration.

* Other Hacker ideas
See the file named OtherHackerIdeas.md for some potentially interesting extensions to the hack-night activity.  Please feel free to share these ideas with the rest of the team - specifically with a focus on how these help NetApp SE's better understand 3rd Platform/DevOps customers and sales motion.  

## Getting help
Google and Youtube is how the modern developer learns.  If you have a question, are getting an error message, or need to learn to do something - Try Google first.

If you then get stuck - ask your teammates - We are **"Team NetApp"** - never fail alone!

If you are still stuck - ask a hack-night lead for help.

## Hack-night Modules
The hack-night instructions are divided into modules to help provide structure and to help the hack-night leaders assess progress.

### Module 0: Pre-Hack Night work
Look in a file named PREWORK.md which details suggested activities to do **BEFORE** coming to hack-night.  It is encouraged that all hackers read thru the PREWORK.md document - even if that means you are doing that during the even.  

### Module 1: Connect to RaspberryPI, Take Picture and View the image
* SSH to remotely connect to your RaspberryPI.
* Install the fswebcam and figure out how to take a picture.
Hint: Google "fswebcam"
Note: You may need to run the following command to load the camera driver.
%> sudo modprobe bcm2835-v4l2
* Copy the image back to your PC (using SCP) and view the image.
