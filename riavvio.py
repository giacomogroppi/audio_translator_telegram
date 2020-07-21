import os
import time
import sys

comando = sys.argv[1]
print(comando)

time.sleep(5)

if comando == 'riavvio':
    os.system("sudo reboot")
elif comando == 'servizio':
    os.system("sudo systemctl restart bottelegram.service")

else:
    """ it is called wrong """
    OSError("non riesco a riavviare")