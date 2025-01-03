#!/bin/bash


echo "Load configuration"

project_name="nwn-server-checker-v2"
remote_server="app@ssh.rosti.cz"
target_folder="/srv/app"

echo "Update remote folder"
rsync -avz -e "ssh -p 12339" $remote_server:$target_folder/$project_name/data/sqlite.db data/sqlite.db

