cd /home/ubuntu/bottelegram
rm -r build/ dist/ __pycache__/
pyinstaller /home/ubuntu/bottelegram/ricerca.py --onefile --spacpath /home/ubuntu/bottelegram/
sudo systemctl restart bottelegram.service
