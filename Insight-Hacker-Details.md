#Insight 2016 Hacker Night Details

Welcome to the Hacker Event.  Below are the most basic instructions to get started.  The rest is up to you to figure out.

##Remember:
	1. Google is the hackers new bookshelf.
	2. You are part of Team NetApp - don't fail alone.
	3. If you are really stuck or have an idea you would like to discuss, please feel free to engage one of the Lead Hackers.


##Teams
You will be assigned to one of five Scrum Teams.  There are enough Raspberry PI units available to allow hackers to work in pairs.  This is not a competition, but it innovation, creativity and problem solving is recognized.  If you are an absolute NOOB (little to no UNIX skills), then you should partner with a more experienced hacker, just so you don't struggle too much.

##Raspberry PI Devices
The lead hacker will have 10 Raspberry PI units to use during the lab.  If you have your own, you are welcome to use it.  The Raspberry PI units come with Rapbian pre-installed and configured with a clean but updated installation.  The RaspPI units have hard wired IP addresses connected to the hacknight wireless network.   You will connect to the RaspPI using SSH from your laptop.

If you brought your own RaspPI unit, it should have some sort of camera installed and working.  The hack even requires it.


##HackerNet
A WIFI connection has been provided so the Raspberry PI devices can connect and have a set hardwired IP address.
Raspberry PI devices provided by the lead hacker have IP addresses 10.69.69.xx where the xx matches the name of the Raspberry PI. Example raspberrypi_04 has an IP address of 10.69.69.4.

SSID: hacknight  for raspberrypi_2  to raspberrypi_17
SSID: hacknight2 for raspberrypi_18 to raspberrypi_35
Password: pihackers

##Connecting to the Raspberry PI
Connect to the Raspberry PI using SSH.  IP Addresses are written on the Raspberry PI case.
Raspberry PI Unit Name: raspberrypi_xx matches the IP address 10.69.69.xx
User: pi
Password: raspberry

Your laptop MUST be connected to the same wireless network.


##Hacker Night GitHub Repo
You can find all the hacknight files and documents on GitHub: https://github.com/NetAppEMEA/hackathon-vol1


##S3 Object Storage Servers
There are two S3 Object Storage servers you can choose from.  Or setup your own S3 Server.

###SGWS
Server: `webscaledemo.netapp.com`
Access_key: `VWULUMGSVOPHVZZM56LZ`
Secret_access_key: `qc6CQ4p4X4GVC76rgEuk6bgozP3H2D6TI3ms1RpN`


###AWS S3
Server: `s3.amazonaws.com`
Access_key: `AKIAICJFODZNY24U2DJA`
Secret_access_key: `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`


###Elasticsearch Server
Elasticsearch version: 2.3
Endpoint:  `https://search-netapp-hackernet-vjwfdxrvkvs56u6g6d56mwjhsi.us-west-2.es.amazonaws.com`
Domain ARN: `arn:aws:es:us-west-2:440113846901:domain/netapp-hackernet`
Kibana: `search-netapp-hackernet-vjwfdxrvkvs56u6g6d56mwjhsi.us-west-2.es.amazonaws.com/_plugin/kibana/`
