#!/bin/bash


echo "Load configuration"

project_name="nwn-server-checker-v2"
server_port="8080"
remote_server="app@ssh.rosti.cz"
ssh_public_key="~/.ssh/MyAccountSSHKeypair.pem"
target_folder="/srv/app"


echo "Update remote folder"
rsync -arv -v -e "ssh -p 12339" --exclude .git ../$project_name $remote_server:$target_folder

