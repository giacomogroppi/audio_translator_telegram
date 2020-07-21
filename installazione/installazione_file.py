import os 

os.system("./pip.sh")
os.system("sudo ./pip.sh")

posizione_file = os.getcwd()

posizione_file = posizione_file[:-13]

with open("bottelegram.service", 'w') as f:
    testo = '\n[Unit]\nDescription=ciao\nAfter=mysql.service\n\n[Service]\nWorkingDirectory=' + str(posizione_file) + '/\nExecStart=' + str(posizione_file) + 'dist/ricerca'
    f.write(testo)
    f.write('\n[Install]\nWantedBy=network-online.target')

with open("ricompilazionetelegram.service", 'w') as f:
    testo = '\n[Unit]\nDescription=Programma che ricompila telegram\nAfter=mysql.service\n\n[Service]\nExecStart=/bin/bash ' + str(posizione_file) + 'installazione.sh'
    f.write(testo)
    f.write('\n[Install]\nWantedBy=network-online.target')



"""
Sposta i file per i server
"""

array = [
    'cp bottelegram.service /etc/systemd/system/bottelegram.service',
    'cp ricompilazionetelegram.service /etc/systemd/system/ricompilazionetelegram.service'
]

for x in array:
    os.system(x)
