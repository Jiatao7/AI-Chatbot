## Display

### Initial Setup:
Creating the virtual environment:
- Open a new cmd terminal in VS code (if not default, click dropdown arrow next to '+' on the terminal top right then choose command prompt)
- In the terminal, ```pip install virtual env```
- Create an environment: ```virtual env venv```
- Launch environment: ```venv\Scripts\activate.bat.``` You should see (venv) at the beginning of the command line if you've successfully entered the environment.

Setup/install necessary libraries:
- Once the virtual environment is launched, run:
    - ```pip install openai speechrecognition gtts playsound torch torchvision matplotlib PyAudio Pillow```
- Make sure your python interpreter is correct by doing ```CTRL + SHIFT + P```, then "Python: Select Interpreter", and choosing "Python 3.11.4" or similar

### Every time:
Launching the display is hella easy:
- Just run the ```app.py``` file in ```src```
Launching the display may be tricky:
- The program is executed from the ```app.py``` file in folder ```src```
- You may need to install a variety of modules including: torch, speech_recognition, tkinter, translate, and more.
- You will need to compile it in a virtual environment if you are not using Python 3.12
- If you are using python 3.12, it should run easily then.
- The display is made using tkinter library