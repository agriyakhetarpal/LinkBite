#!/bin/bash
  
# turn on bash's job control
set -m
  
# start the primary process and put it in the background
uvicorn "shortener.main:app" --host "0.0.0.0" --port 8000 &
  
# start the helper process
python gradio-app.py

# the my_helper_process might need to know how to wait on the
# primary process to start before it does its work and returns
  
# bring the primary process back into the foreground
# and leave it there
fg %1