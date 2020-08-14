#!/bin/bash

STATUS_SERVICE=amya-logo-2.service
SPLASH_SERVICE=splashscreen.service
DEST=/etc/systemd/system

sudo cp $STATUS_SERVICE $DEST
sudo cp $SPLASH_SERVICE $DEST

sudo systemctl daemon-reload
sudo systemctl enable $STATUS_SERVICE
sudo systemctl start $STATUS_SERVICE
sudo systemctl enable $SPLASH_SERVICE
sudo systemctl start $SPLASH_SERVICE
