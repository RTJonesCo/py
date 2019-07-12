#!/bin/bash

echo Loading Active911 Program
echo $PWD
cd /home/pi/code/active911_project
echo $PWD
python3 /home/pi/code/active911_project/run.py 2>&1 | tee /home/pi/code/active911_project/running.log
