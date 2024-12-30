#!/bin/bash


echo "Load configuration"

project_name="kalorie"
server_port="4000"
remote_server="ubuntu@3.66.153.206"
ssh_public_key="~/.ssh/MyAccountSSHKeypair.pem"
target_folder="~/projekty/"


echo "Update remote folder"

rsync -arv -v -e "ssh -i $ssh_public_key" --exclude .data --exclude .git ../$project_name $remote_server:$target_folder


echo "Restart remote running application"

ssh -i $ssh_public_key $remote_server << HERE
sudo lsof -i:$server_port -t | sudo xargs kill
cd $target_folder/$project_name
pip3 install -r requirements.txt
cd server
python3 app.py
HERE


echo "Done"
