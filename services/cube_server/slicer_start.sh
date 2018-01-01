#!/bin/bash
# Initialize the database schema if it's not already in place
#CONNECTION_STRING=$(cat slicer.ini | ./ini_value.py -s store -k url)

python  -m scripts.setup_data
echo 'Starting slicer cube server on port 5000..'
slicer serve slicer.ini