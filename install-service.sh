#!/bin/bash

SERVICE=amya-logo-2.service

sudo cp $SERVICE /lib/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE
sudo systemctl start $SERVICE
