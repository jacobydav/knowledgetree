//Programming and testing
//Navigate to the folder
cd Documents/knowledgetree
//Activate your virtual environment by running:
source .venv/bin/activate
//I am using Thonny to write the program
//Open Thonny
In the bottom right of the Thonny window, you can change the python interpreter.
Set it to the python3 that is located inside the virtual environment.
For example: /home/rpi/Documents/knowledgetree/.venv/bin/python3

Now you can run the program from within Thonny.

//To run the program from the terminal with the virtual environment activated
python k_tree.py

//Git procedure
git add .
git commit -m "Commit message goes here"
git push

//SystemD service
The file is /lib/systemd/system/knowledgetree.service
Example commands:
sudo systemctl enable knowledgetree
sudo systemctl start knowledgetree
sudo systemctl status knowledgetree
sudo systemctl stop knowledgetree
sudo systemctl disable knowledgetree
sudo systemctl daemon-reload
