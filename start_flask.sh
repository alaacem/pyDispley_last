#!/bin/bash

# Search for all PIDs associated with anzeige_flask.py and terminate them
/home/hiwiadmin/pyDisplay/shutdown_flask.sh


source /home/hiwiadmin/pyDisplay/myenv/bin/activate

# Now run anzeige_flask.py
echo "Running as: $(whoami)"

#export DISPLAY=:0
/home/hiwiadmin/pyDisplay/myenv/bin/python3 /home/hiwiadmin/pyDisplay/main.py&
#run keyboard

chromium-browser --kiosk --app=http://127.0.0.1:4000/ --disable-overlay-scrollbar&
sudo /home/hiwiadmin/pyDisplay/myenv/bin/python3 /home/hiwiadmin/pyDisplay/key.py&
sudo /home/hiwiadmin/pyDisplay/myenv/bin/python3 /home/hiwiadmin/pyDisplay/scrapping.py&
#start browser

#run disply spar
#sudo /home/hiwiadmin/pyDisplay/myenv/bin/python3 /home/hiwiadmin/#pyDisplay/display_spar.py &
