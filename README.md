Ubuntu 22.02 from orangepi websit (gui version for easier camera calibration, use xfce, most ligtweight gui)   
(need to figure out why vnc and samba don't work, but not critical)  
Installed openssh  
Done with miniconda (from conda website), theoretically you don't need this, I used it to quickly set up and make new virtual python environments for testing purposes  
  
Python 3.9  
  
Pip dependencies:   
opencv and opencv contrib version 4.5.5.64  
numpy version 1.23.1  
wpilib python latest from docs, and make sure it is the aarch64 (or arm64) version (do not do pip install ntcore, that is a completely different library, don't ask me how I know)  
pillow latest (as of now, version 10.3.0)  


~~Also need to look into making sure that camera ids don't change if they get disconnected/reconnected, there's a post on how to do it in 6328's 2023 build thread~~

First change the cameras serial numbers to something unique with arducam's serial number changer (don't change device name, that causes some problems): [https://docs.arducam.com/UVC-Camera/Serial-Number-Tool-Guide/](url)  

Then run `sudo apt install v4l-utils ` then `v4l2-ctl --list-devices` and find the device number of the cameras  
Note: if a camera is at the index video0, the next camera will be at video2, not video1 because of drivers and stuff (idk the exact reason why but that's the way it works)
`

Place this inside a new file called 99-camera-config.rules inside the /etc/udev/rules.d directory (make sure to change serial numbers to match the result of `sudo udevadm info --name=/dev/videoX --attribute-walk` where x is camera number.

`SUBSYSTEM=="video4linux", ATTRS{idVendor}=="0c45", ATTRS{idProduct}=="6366", ATTRS{serial}=="UC621", SYMLINK+="cam0"
SUBSYSTEM=="video4linux", ATTRS{idVendor}=="0c45", ATTRS{idProduct}=="6366", ATTRS{serial}=="UC6211", SYMLINK+="cam1"`  

After this, run `sudo udevadm control --reload-rules && sudo udevadm trigger` to refresh the rules  
Then test by running `sudo v4l2-ctl -d /dev/cam0 --list-formats-ext ` where cam0 is the symlink you created  
  
Also you need to run `sudo udevadm control --reload-rules && sudo udevadm trigger` every time the cameras are disconnected/connected after boot 

Start on boot  
Make an sh file called northstarX.sh somewhere where you can easily access for each northstar instance running on that coproccessor
Put this in the sh file  
```
```  
run `chmod +x northstarX.sh`  
naigate to `/etc/systemd/system`  
create a file called northstarX.service
put this in the file:  
```
[Unit]
Description=northstarX
After=network.target

[Service]
ExecStart=/Path/To/sh/file.sh
Type=simple
Restart=always

[Install]
WantedBy=multi-user.target
```
