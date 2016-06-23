#camera-webservice

Two version are available, one in Ruby and one in Python; pick your poison!

### Ruby version - based on Sinatra - `webservice.rb` ###
* Install Ruby - OS Package dependencies: `ruby ruby-dev`
* Ruby gem dependencies: `sinatra shotgun aws-sdk json elasticsearch` *Tip:  use the* `--no-document` *option to decrease time to install!!*
* Run using: `shotgun --host 0.0.0.0 --port 8080 webservice.rb`

### Python version - based on Flask - `webservice.py` ###
* OS Package dependencies: `python-pip`
* Python module dependencies: `flask flask-restful boto3 elasticsearch`
* On Windows: the above plus python module `pillow` and [CommandCam](https://batchloaf.wordpress.com/commandcam/ "CommandCam") photo software placed in same directory as `webservice.py`

### Configure service - `config.json` ###

* First rename the `config.json.example` to `config.json`
* Next, update all parameters to meet your needs
* For the `camera_command` parameter these might be helpful:
  * Example linux USB camera: `fswebcam -r 640x480 --jpeg 85 --delay 1`
  * Example native raspberry camera module: `raspistill -o`
  * Example windows usb camera: `CommandCam.exe /quiet /filename`
