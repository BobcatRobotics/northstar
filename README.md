Ubuntu 22.02 from orangepi websit (gui version for easier camera calibration, use xfce, most ligtweight gui)   
(need to figure out why vnc and samba don't work, but not critical)  
Installed openssh  
Done with miniconda (from conda website), theoretically you don't need this, I used it to quickly set up and make new virtual python environments for testing purposes  
  
Python 3.9  
  
Pip dependencies:   
opencv and opencv contrib version 4.5.5.64  
numpy version 1.23.1  
wpilib python latest from docs (do not do pip install ntcore, that is a completely different library, don't ask me how I know)  
pillow latest (as of now, version 10.3.0)  


~~Also need to look into making sure that camera ids don't change if they get disconnected/reconnected, there's a post on how to do it in 6328's 2023 build thread~~

First change the cameras serial numbers to something unique with arducam's serial number changer (don't change device name, that causes some problems): [https://docs.arducam.com/UVC-Camera/Serial-Number-Tool-Guide/](url)  

Place this inside a new file called 99-camera-config.rules inside the /etc/udev/rules.d directory (make sure to change serial numbers to match the result of `sudo udevadm info --name=/dev/videoX --attribute-walk` where x is camera number, found by trial and error of ` sudo v4l2-ctl -d /dev/camX --list-formats-ext`): here X will be trial and error, and if a camera is at 0, the next camera will be at 2, not 1:  

`SUBSYSTEM=="video4linux", ATTRS{idVendor}=="0c45", ATTRS{idProduct}=="6366", ATTRS{serial}=="UC621", SYMLINK+="cam0"
SUBSYSTEM=="video4linux", ATTRS{idVendor}=="0c45", ATTRS{idProduct}=="6366", ATTRS{serial}=="UC6211", SYMLINK+="cam1"`  

After this, run `sudo udevadm control --reload-rules && sudo udevadm trigger` to refresh the rules  
Then test by running `sudo v4l2-ctl -d /dev/cam0 --list-formats-ext ` where cam0 is the symlink you created
