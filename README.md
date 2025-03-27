# AI Chatbot

## Overview
This project is an AI Chatbot that can engage in conversations with the user. The chatbot takes voice inputs, processes them using speech-to-text (STT), generates responses via the OpenAI API, and outputs the responses through text-to-speech (TTS). A graphical user interface (GUI) is also included to display the chat history and chatbot status during conversations.

## Features
### Core Features
- **Speech-to-Text (STT)**: Uses the Speech Recognition library to convert microphone inputs into text.

- **Text-to-Speech (TTS)**: Uses the eSpeak library to convert the chatbot's responses into speech.

- **Graphical User Interface (GUI)**: Provides a display built using Tkinter to allow the user to interact with the application. Also displays the chat history and chatbot status during conversations.

### Additional Features
- **Save and Load Chat**: Stores conversations between the user and chatbot to enable the user to continue a conversation at a later date. 

- **Dynamic Speaking Tones**: Adjusts the chatbot's tone based on conversation context.

- **Language Customization**: Supports six different languages (English, Spanish, French, German, Italian, and Portuguese).

- **Mini-Games**: Offers minigames including chess and tic-tac-toe for the user to play against the chatbot. Boards are displayed on the GUI.

- **AI-Generated Avatars**: Generates avatars that reflect the chatbot's mood using a machine-learning model built with PyTorch.

## Try Out the Project
*This project was initially designed to run on a Raspberry Pi, along with a monitor and microphone. However, it can also be easily run on a personal device.*

### Clone the Repository:
```
git clone https://github.com/Jiatao7/AI-Chatbot.git
cd AI-Chatbot
```

### Create Virtual Environment:
In the terminal, run:
~~~ 
pip install virtual env
virtual env venv
venv\Scripts\activate.bat
~~~

### Install Libraries:
Once the virtual environment is launched, install the required libraries by running:
~~~ 
pip install openai speechrecognition gtts playsound torch torchvision matplotlib PyAudio Pillow
~~~

### Configure API Key:
Obtain an OpenAI API key: https://openai.com/api/

Then store the key in a .env file:
~~~
API_KEY=<insert api key>
~~~

### Run the Chatbot:
Run the ```app.py``` file in the ```src``` folder.
