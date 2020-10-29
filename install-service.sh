#!/bin/bash

STATUS_SERVICE=amya-logo-2.service
SPLASH_SERVICE=splashscreen.service
SPLASH_SHUTTINGDOWN_SERVICE=shuttingdown_lcd.service
SPLASH_HALTED_SERVICE=halted_lcd.service
DEST=/lib/systemd/system

sudo cp $STATUS_SERVICE $DEST
sudo cp $SPLASH_SERVICE $DEST
sudo cp $SPLASH_SHUTTINGDOWN_SERVICE $DEST
sudo cp $SPLASH_HALTED_SERVICE $DEST

sudo systemctl daemon-reload
sudo systemctl enable $STATUS_SERVICE
sudo systemctl start $STATUS_SERVICE

sudo systemctl enable $SPLASH_SERVICE
sudo systemctl start $SPLASH_SERVICE
 
sudo systemctl enable $SPLASH_SHUTTINGDOWN_SERVICE
sudo systemctl start $SPLASH_SHUTTINGDOWN_SERVICE

sudo systemctl enable $SPLASH_HALTED_SERVICE
sudo systemctl start $SPLASH_HALTED_SERVICE

sudo systemctl restart amya-logo-2.service
