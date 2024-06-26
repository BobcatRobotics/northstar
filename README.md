# Steps to get 6328's NorthStar working (adapted to use for 177)

## Initial Installation
1. Get an OrangePi and flash Ubuntu 22.02 XFCE (from the OrangePi website, not from Ubuntu website) to a microSD card. The GUI is necessary for calibration, but if you already have the calibration file, then you could theoretically run this headless. Note: If you decide to run it headless, make sure to reflect that when installing opencv.
   
3. Install openssh to connect via SSH, not necessary if you have a monitor.
   
5. Install miniconda (from the conda website). Theoretically you don't need this, I used it to quickly set up and make new virtual python environments for testing purposes.
   
7. Use conda to create and activate a new Python 3.9 environment
   
9. Install the following python dependencies (make sure you are in the conda environment you created):
   1. ~~opencv-python==4.5.5.64~~ See below
   2. ~~opencv-contrib-python==4.5.5.64~~ See below
   3. numpy==1.23.1
   4. pillow==10.3.0
   5. wpilib python latest from docs, and make sure it is the aarch64 (or arm64)   
      version (do not do pip install ntcore, that is a completely different library,
      don't ask me how I know)
      https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-2/python-setup.html
   6. ```pip install pycairo PyGObject``` this is needed to install gi
10. Now copy the code from this repo and place it into a folder in the home directory.
   
## Create Symlink
Before we actually run NorthStar, we need to make sure that each camera has a symlink so they connect properly on boot.
   
1. First change the camera's serial numbers to something unique with arducam's serial number changer (don't change device name, that causes some problems)  [https://docs.arducam.com/UVC-Camera/Serial-Number-Tool-Guide/](url)
   
2. Then run `sudo apt install v4l-utils` then `v4l2-ctl --list-devices` and find the device number of the cameras
   Note: if a camera is at the index video0, the next camera will be at video2,         not video1 because of drivers and stuff (idk the exact reason why but that's         the way it works)

3. Place the following code inside a new file camed 99-camera-config.rules inside the /etc/udev/rules.d directory (make sure to change serial numbers to match the result of `sudo udevadm info --name=/dev/videoX --attribute-walk`, where X is camera number.
```
SUBSYSTEM=="video4linux", ATTRS{idVendor}=="0c45", ATTRS{idProduct}=="6366", ATTRS{serial}=="UC621", SYMLINK+="cam0"
SUBSYSTEM=="video4linux", ATTRS{idVendor}=="0c45", ATTRS{idProduct}=="6366", ATTRS{serial}=="UC6211", SYMLINK+="cam1"
```
4. After this, run `sudo udevadm control --reload-rules && sudo udevadm trigger` to refresh the rules.
    
5. Then test the rules by running `sudo v4l2-ctl -d /dev/cam0 --list-formats-ext` where cam0 is the symlink you created
   
6. IMPORTANT: You need to run `sudo udevadm control --reload-rules && sudo udevadm trigger` every time the cameras are disconnected/connected after boot
   

## Make Northstar start on boot
   
1. Make a .sh file called northstarX.sh somewhere where you can easily access for each northstar instance running on that coproccessor
Put this in the sh file
**(Make sure to verify the miniconda directory and northstar directories)**
```
#!/bin/bash
if [ -f "/home/orangepi/miniconda3/etc/profile.d/conda.sh" ]; then
    . "/home/orangepi/miniconda3/etc/profile.d/conda.sh"
    CONDA_CHANGEPS1=false conda activate vision
fi
cd /home/orangepi/vision/vision/northstar
python __init__.py
```  

2. `chmod +x northstarX.sh`
   
4. Navigate to `/etc/systemd/system`

5. Create a file called northstarX.service and put this in the file:  
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

6. After that, run `sudo systemctl daemon-reload`  
Then run `sudo systemctl enable northstarX.service`  and you should start northstar on boot. Make sure to repeat for all instances of northstar.

## Build OpenCV manually for gstreamer
```
# <navigate to where you want the opencv-python repo to be stored>
git clone --recursive https://github.com/skvark/opencv-python.git
cd opencv-python
git checkout 64 #this is the tag for opencv-python 4.5.5.64
```
IMPORTANT: after cloning the repo, make sure to change the version in pyproject.toml to ```scikit-build==0.13.0```
[https://github.com/opencv/opencv-python/issues/648](url)
```
export CMAKE_ARGS="-DWITH_GSTREAMER=ON"
export ENABLE_CONTRIB=1
pip install --upgrade pip wheel
# this is the build step - the repo estimates it can take from 5 
#   mins to > 2 hrs depending on your computer hardware
pip wheel . --verbose
pip install opencv_contrib_python*.whl
# note, wheel may be generated in dist/ directory, so may have to cd first
```
Theoretically, the build steps are not needed, and you can just install the prebuilt file in this repo (named opencv_contrib_python*.whl)

## Calibration
Use instructions in 6328 calibration-instructions.txt
Holy Cows calibration board: for a 24 inch monitor (at least mine: 12x9, PPI=264, Scale=12)

Or, take images and run the manual calibrate.py file.

## Benchmarking
FPS is measured at the beggining, and after sustained loads to simulate a real match. All cameras are focused and placed about 5 feet away from an apriltag with an exposure of 150 and a gain of 2. Everything is measured at its max resolution (1600x1200 for arducams and 1600x1304 for ThriftyCams).


##### ThriftyCams
| Time | FPS |
| ------------- | ------------- |
| Immediately after boot  | 55-60  |
| 45 seconds in  | 45-50  |
| 1:30 minutes in  | 30-40  |
| 2 minutes in  | 28-34 |
| 2:30 minutes in  | 25-32 |

##### Arducams
| Time | FPS |
| ------------- | ------------- |
| Immediately after boot  | 45-50  |
| 45 seconds in  | 35-40  |
| 1:30 minutes in  | 30-35  |
| 2 minutes in  | 25-30 |
| 2:30 minutes in  | 20-28 |

The declining performance is due to thermal throttling on the OrangePi. Better cooling systems may better articulate the differences between the cameras, but the extra 10 peak fps on the ThriftyCams seem to help, at least somewhat. Another thing to consider is that ThriftyCams are running at a higher resolution than the ArduCams. Still, they have slightly better frame rates than the ArduCams. 


### Todo
1. Need to figure out why vnc and samba don't work, but this isn't critical
2. ~~Need to look into making sure that camera ids don't change if they get disconnected/reconnected, there's a post on how to do it in 6328's 2023 build thread~~
3. ~~Gstreamer: [https://discuss.bluerobotics.com/t/opencv-python-with-gstreamer-backend/8842
](url)~~
4. Object tracking+detection: [https://github.com/google-coral/example-object-tracker/tree/master/gstreamer](url)


https://www.chiefdelphi.com/t/yolov5-8-training-and-conversion-to-rknn-notebooks/452716?u=adithya_anand
