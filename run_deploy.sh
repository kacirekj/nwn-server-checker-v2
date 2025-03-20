#!/bin/bash


echo "Load configuration"

project_name="nwn-server-checker-v2"
remote_server="app@ssh.rosti.cz"
target_folder="/srv/app"

echo "Update remote folder"
rsync -arv -v -e "ssh -p 12339" --exclude .git --exclude data --exclude web/asset ../$project_name $remote_server:$target_folder

