//Initial setup begin
//Install some opencv dependencies
sudo apt install build-essential cmake git libgtk-3-dev libavcodec-dev libavformat-dev libswscale-dev


//Install the python virtual environment
sudo apt install python3-venv
//Create the virtual environment by navigating to the python project folder and running:
python3 -m venv .venv

//To install OpenCV in the virtual environment:
//Activate your virtual environment by running:
source .venv/bin/activate

//The prompt will change. You will see (.venv) at the beginning of the prompt in the terminal.
//Now Install opencv while the virtual environment is active
pip install opencv-python
//Initial setup end

//Programming and testing
//Activate your virtual environment by running:
source .venv/bin/activate
//I am using Thonny to write the program
//Open Thonny
In the bottom right of the Thonny window, you can change the python interpreter.
Set it to the python3 that is located inside the virtual environment.
For example: /home/rpi/Documents/K_Tree/.venv/bin/python3

Now you can run the program from within Thonny.

//To run the program from the terminal with the virtual environment activated
python k_tree.py