#!/bin/bash
sudo mkdir /storage/tmp
sudo TMPDIR=/storage/tmp/ pip3 install --cache-dir=/storage/tmp --build=/storage/tmp FBpyGIF
sudo TMPDIR=/storage/tmp/ pip3 install --cache-dir=/storage/tmp --build=/storage/tmp numpy
./install-service.sh
