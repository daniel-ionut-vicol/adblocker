#!/bin/bash

nohup python3 -m http.server 5500 --bind 0.0.0.0 --directory /mnt/data/mlserver/adblock/pyton/flask_backend/v8 > run_fileserver.log &

