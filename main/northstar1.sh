#!/bin/bash
if [ -f "/home/orangepi/miniconda3/etc/profile.d/conda.sh" ]; then
    . "/home/orangepi/miniconda3/etc/profile.d/conda.sh"
    CONDA_CHANGEPS1=false conda activate vision
fi
cd /home/orangepi/vision/vision1/northstar
python __init__.py
