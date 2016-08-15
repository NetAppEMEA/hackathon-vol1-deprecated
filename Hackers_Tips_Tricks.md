# Hackers Tips and Tricks


## GitHub Desktop Client
Check out this helpful desktop tool: https://desktop.github.com

## Not your Grandfathers 'vi'
  * NotePad++
  If you'll be editing files from your Windows desktop, use an editor such as NotePad++ https://notepad-plus-plus.org/
  * Atom editor
  This editor is available on Win, Mac and Linux.  http://www.atom.io 


## Tools for Remotely Access
### SSH Client  
  * If you are on a Windows laptop, you will need an ssh client, such as Putty http://www.putty.org/

  * If you are on a Mac, you can use the built-in Terminal application or iTerm (https://www.iterm2.com/) to ssh into your Pi

### VNC (tightvncserver)
Desktop emulation tools, such as VNC are also helpful for remote access to your PI.
`tightvncserver` is pre-installed on the RaspberryPI.  Google for more information.


### Using Remote Desktop Client (RDP)
If you want to use the Remote Desktop Client (RDP) to connect remotely to your RaspberryPi, you need to install the `xrdp` package.

  * Open terminal on your Pi
	* Type the following command "sudo apt-get install xrdp"
	* If prompted, enter your password (the default is "raspberry")
	* If prompted, type "Y" and press enter.
	* This is now installing xrdp onto your Pi which is the software we are going to use for the remote desktop connection.  Wait for it to complete.
	* Reboot your Pi.  

Reference:  http://www.raspberrypiblog.com/2012/10/how-to-setup-remote-desktop-from.html
