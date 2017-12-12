#!/bin/bash
# Initialize the database schema if it's not already in place
#CONNECTION_STRING=$(cat slicer.ini | ./ini_value.py -s store -k url)

python  -m scripts.setup_data