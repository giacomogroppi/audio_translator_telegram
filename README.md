# Audio Translator Telegram
This is a python3 script, that work with API's telegram bot, to convert image and audio into text
This is a script, written in python, that can translate audio, photo, video message, video, into text.
He also understand were, during the audio, there are moment of silent, and he substitute them with commas

## Getting Started

To execute the project all you need are:
- install the python dependencies in the folder installazione
```
sudo chmod +x ./installazione/pip.sh && ./installazione/pip.sh
```

- Create a token for your telegram bot, and you also need to discover your chat_id


### Compiling
If you want to ran the programm in a dedicated server is better if you compile it with pyinstaller.
By using this command:
```
pyinstaller ricerca.py --onefile
```
This command will create in a folder named dist an executable file

## Installazione.sh
This script allow you to compile the programm and restart the service

## Service [systemd]
In the folder installazione the script, in python, installazione_file.py, that create:
- the service with the current path of the folder [for the python compiled script]
- the service that allow you to compile the project remotely


## Authors

* **Giacomo Groppi** - (https://github.com/giacomogroppi) or (giamg01@gmail.com)
