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


Also need to look into making sure that camera ids don't change if they get disconnected/reconnected, there's a post on how to do it in 6328's 2023 build thread
