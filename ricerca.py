try:
    import da_importare
except:
    """
    Serve per gestire l'errore di pycompile su macchine aws
    """
    pass

from pydub.silence import split_on_silence
import speech_recognition as sr
import telepot
import os
import libreria as libreria
import psutil
#from pygame import mixer
import time
import socket
import re
import random as random
from os import path
from pydub import AudioSegment
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup
from googletrans import Translator
from random import randrange
from datetime import datetime
import cv2
import pytesseract
import io
import json
import numpy as np
import requests
from ast import literal_eval
import ast



chat_id_admin1 = ''
chat_id_admin2 = ''


VERSIONE = 'stable'
VERSIONE = 'testing'

#controlla la versione e setta i nomi delle tabelle in base a cosa è direzionata la versione attuale del file
if VERSIONE == 'stable':
    tabella = 'utenti'
    tabellaaggiornamento = 'statistiche'
    TOKEN = '' #STABLE
else:
    tabella = 'utenti2'
    tabellaaggiornamento = 'statistiche2'
    TOKEN = '' #TESTING


lingue = {
    'it-IT': '/Italiano',
    'ar-IL': '/Arabic',  
    'de-DE': '/German',
    'en-GB': '/English',
    'es-ES': '/Spanish',
    'fr-FR': '/French',
    'ja-JP': '/Japanese',
    'ko-KR': '/Korean',
    'nl-NL': '/Dutch',
    'pl-PL': '/Polish',
    'pt-BR': '/Portuguese',
    'ru-RU': '/Russian',
    'th-TH': '/Thai',
    'tr-TR': '/Turkish',
    'bg-BG': '/Bulgarian',
    'ca-ES': '/Catalan',
    'cs-CZ': '/Czech', 
    'da-DK': '/Danish',
    'el-GR': '/Greek',
    'fi-FI': '/Finnish',
    'hi-IN': '/Hindi',
    'hr-HR': '/Croatian',
    'hu-HU': '/Hungarian',
    'id-ID': '/Indonesian', 
    'lt-LT': '/Lithuanian', 
    'pt-PT': '/Portuguese', 
    'ro-RO': '/Romanian',
    'sk-SK': '/Slovak', 
    'sl-SI': '/Slovenian',
    'sr-RS': '/Serbian', 
    'uk-UA': '/Ukrainian', 
    'vi-VN': '/Vietnamese'
}


# Define a function to normalize a chunk to a target amplitude.
def match_target_amplitude(aChunk, target_dBFS):
    ''' Normalize given audio chunk '''
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)


def pubblicita(chat_id, bot, msg):
    language = libreria.selectcondizionato(tabella, "chat_id", chat_id, "lingua")[0][0]
    testo = traduttore('Se vuoi aiutarci nello sviluppo e nel mantenimento di questo bot /donate anche solo un caffè è ben accetto!\n\nPer info sulle sponsorizzazioni', language) +" /sponsor"
    bot.sendMessage(chat_id, testo)
    
def pubblicitadonate(chat_id, bot, msg):
    language = libreria.selectcondizionato(tabella, "chat_id", chat_id, "lingua")[0][0]
    testo = traduttore('se vuoi aiutarci nello sviluppo e nel mantenimento di questo bot /donate anche solo un caffè è ben accetto! Usa paypal.', language) +"\n paypal.me/Ticozzi"
    bot.sendMessage(chat_id, testo)


def admin(chat_id, bot, msg):
    risultato = libreria.selectcompleta(tabella)
    with open("utenti.txt", 'w') as f:
        for x in risultato:
            f.write(str(x) + "\n")
    
    try:
        f.close()
    except:
        pass

    
    
    bot.sendDocument(chat_id, open("utenti.txt", 'rb'))
    
    os.system("rm -r utenti.txt")

def verificachat(chat_id):
    """
    false se non ci sono utenti
    true se ci sono utenti registrati
    """
    if len(libreria.selectcondizionatodato(tabella, "chat_id", chat_id)) == 0:
        #vuol dire che non ci sono utenti
        return False 
    else:
        return True


def start(chat_id, bot, msg, verifica, verificatraduzione):
    if verificatraduzione:
        if verifica:
            language = libreria.selectcondizionato(tabella, "chat_id", chat_id, "lingua")[0][0]
            bot.sendMessage(
                chat_id, 
                (traduttore(("Ben tornato, la lingua che hai impostato precedentemente è "),language) + " " + str(lingue[str(language)])[1:] + "\n "+ traduttore("Se vuoi modificarla digita",language) + " /setlanguage"))
        
        else:
            language_chat = msg['from']['language_code']
            controllo = False
            language = 'en-GB'
            for x in lingue:
                if x[:2] == language_chat:
                    language = x #se viene modificata qua vuol dire che ha riconosciuto che lingua è [nella maggior parte dei casi la prende]
                    controllo = True #se True vuol dire che ha riconosciuto la lingua
            
            if controllo:
                bot.sendMessage(chat_id, traduttore("Ho capito dai tuoi settaggi di telegram che parli ",language) + " " +str(lingue[language])[1:] + "\n\n" + traduttore("Se vuoi cambiarla digita",language) + " /setlanguage " + traduttore("per cambiare lingua",language))
            
            else:
                messaggio = 'Welcome\nChoose your language: \n'
                for x in lingue:
                    messaggio += lingue[x] + "\n"
                bot.sendMessage(chat_id, messaggio)
            libreria.insertdue(tabella, ["chat_id", "lingua","audio", "foto"], [chat_id, language, "0", "0"])
            
            
            """
            Inserimento nella tabella di aggiornamento
            """
            anno_mese_giorno = str(datetime.now())[:10]

            try:#in caso non esistesse il record prima prova a inserirlo, in caso non esiste lo inserisce lui   
                persone_registrate_oggi = libreria.selectcondizionato(tabellaaggiornamento, "giorno", str(anno_mese_giorno), "personeregistrate")[0][0]
                libreria.update(tabellaaggiornamento, "personeregistrate", str(int(persone_registrate_oggi)+1), "giorno", str(anno_mese_giorno))
            except:
                libreria.insertdue(tabellaaggiornamento, ["giorno", "audiotradotti", "personeregistrate", "fototradotte"], [str(anno_mese_giorno), "0", "1", "0"])

    else:
        #crea l'utente con la lingua inglese, e dopo gli fa scegliere se vuole cambiarla
        #language_chat = msg['from']['language_code']
        #controllo = False
        language = 'en-GB'
        #for x in lingue:
        #    if x[:2] == language_chat:
        #        language = x #se viene modificata qua vuol dire che ha riconosciuto che lingua è [nella maggior parte dei casi la prende]
        #        controllo = True #se True vuol dire che ha riconosciuto la lingua
        #    
        #bot.sendMessage(chat_id, traduttore("Ho capito dai tuoi settaggi di telegram che parli",language) + " " +str(lingue[language])[1:] + "\n\n" + traduttore("Se vuoi cambiarla digita",language) + " /setlanguage " + traduttore("per cambiare lingua",language)) 
        libreria.insertdue(tabella, ["chat_id", "lingua","audio", "foto"], [chat_id, language, 0, 0])




def traduttore (text,language):
    language = language[0:2]
    translator = Translator()
    stringa = translator.translate(text, dest=language)

    return str(stringa.text)
    

def adminstatistiche(chat_id, bot, msg, file_id, nomefiletemporaneo):
    """
    /messaggioatutti 0.50 Ciao a tutti
    """
    if file_id and nomefiletemporaneo:
        percentuale = msg['caption'][17:22]
        testo = msg['caption'][22:]
    else:    
        percentuale = msg['text'][17:21]
        testo = msg['text'][22:]

    percentuale = float(percentuale)
    

    risultato = libreria.selectcompleta(tabella)
    numeroquery = len(risultato) #risultato della query
    quanti = int(numeroquery * percentuale) 

    print(quanti)
    #non costruisce l'array grosso come quante persone devono ricevere la pubblicità, in quanto basta che vengano aggiunti elementi con chat_idarray.extend(())
    chat_idarray = []


    #costruzione dell'array randomico
    numero_randomico = []
    
    k = 0 #contatore per il ciclo dopo
    
    while True:  
        if k == quanti:
            break
            #può uscire dal ciclo perchè vuol dire che ha finito di inserire numeri all'interno dell'array
        
        temporaneo = random.randint(0,len(risultato)-1)
        controllo = True

        
        for x in numero_randomico:
            if temporaneo == x:
                controllo = False
                break
                
        if controllo:
            #deve aggiungere a numero_randomico il numero
            numero_randomico.append(temporaneo)
            k += 1
            

    #manda il messaggio a tutte le persone
    messaggi_errore = []    
    for x in numero_randomico:
        try:
            dainserire = risultato[x][0]
            chat_idarray.append(dainserire)
        except Exception as e:
            messaggi_errore.append(str(e))


    
    #manda i messaggi
    for x in risultato:
        try:    
            chat_id = int(x[0])
            if nomefiletemporaneo and file_id:
                """
                vuol dire che deve mandare solo il testo senza la foto
                e quindi non deve inviare un bel cazzo
                """
                bot.sendPhoto(chat_id, photo=open(nomefiletemporaneo + ".png", 'rb'))
            else:
                """
                Vuol dire che non ci sono file da mandare come testo o altro
                """
                pass
            
            bot.sendMessage(chat_id, testo)
        except Exception as e:
            messaggi_errore.append(str(e))


    """
    Manda i messaggi di errore
    """    
    if not messaggi_errore:
        bot.sendMessage(chat_id_admin1, "messaggio inviato correttamente, abbiamo inviato il messaggio a: " + str(quanti) + " persone")
        bot.sendMessage(chat_id_admin2, "messaggio inviato correttamente, abbiamo inviato il messaggio a: " + str(quanti) + " persone")
    else:
        #costruzione del messaggio di errore
        for x in messaggi_errore:
            testo_admin = x + "\n" #così mette a capo a ogni errore
        bot.sendMessage(int(chat_id_admin1), str(testo_admin))   
        bot.sendMessage(int(chat_id_admin2), str(testo_admin)) 

        bot.sendMessage(chat_id_admin1, "messaggio inviato a " + str(quanti - len(messaggi_errore)))
        bot.sendMessage(chat_id_admin2, "messaggio inviato a " + str(quanti - len(messaggi_errore)))


    if nomefiletemporaneo and file_id:
        #c'è da eliminare la foto
        os.system("rm -r " + str(nomefiletemporaneo) + ".png")
        
    try:
        del chat_id, testo, numero_randomico, bot, numeroquery, controllo, quanti, x, risultato, percentuale
    except Exception as e:
        print("Errore nell'eliminazione delle variabili: ", e)

    


def amministratorefoto(bot, msg, chat_id):
    if str(chat_id) == str(chat_id_admin1) or str(chat_id) == str(chat_id_admin2):
        try:
            if msg['caption'][:16] == '/messaggioatutti':
                nomefiletemporaneo = ''
                nomefiletemporaneo = str(chat_id) + str(random.randint(1,100000))
                try:
                    file_id = msg['photo']['file_id']
                except:
                    file_id = msg['photo'][0]['file_id']
                bot.download_file(file_id, nomefiletemporaneo+".png")
                
                adminstatistiche(chat_id, bot, msg, file_id, nomefiletemporaneo)

                return False #vuol dire che ha recepito il fatto che era un /messaggioatutti
            else:
                return True

        except Exception as e:
            bot.sendMessage(chat_id, str(e))
            return True
    
    else:
        return True #serve per non far fare il controllo

def riconoscimentofoto(bot, msg, chat_id):
    """
    Riconoscimento di scritte e testo all'interno dell'immagine
    """
    language = libreria.selectcondizionato(tabella, "chat_id", chat_id, "lingua")[0][0]
    
    
    messaggio = bot.sendMessage(
        chat_id,
        traduttore(
            "Sto traducendo...",
            language
        )
    )

    nomefiletemporaneo = ''
    nomefiletemporaneo = str(chat_id) + str(random.randint(1,100000))
    try:
        file_id = msg['photo']['file_id']
    except:
        file_id = msg['photo'][0]['file_id']
    bot.download_file(file_id, nomefiletemporaneo+".png")
                
    img = cv2.imread(nomefiletemporaneo + ".png")

    url_api = "https://api.ocr.space/parse/image"
    _, compressedimage = cv2.imencode(".jpg", img, [1, 90])
    file_bytes = io.BytesIO(compressedimage)

    result = requests.post(url_api,
                files = {"screenshot.jpg": file_bytes},
                data = {"apikey": "21a236bc1a88957",
                        "language": "eng"})


    result = result.content.decode()
    risultato = json.loads(result)

    verifica = True
    try: 
        parsed_results = risultato.get("ParsedResults")[0]
    except:
        verifica = False

    try:
        text_detected = parsed_results.get("ParsedText")
    except:
        verifica = False
    
    #Dopo aver controllato l'integrità della stringa 
    if verifica:
        bot.deleteMessage((chat_id,int(messaggio['message_id'])))
        bot.sendMessage(chat_id, str(text_detected))
    else:
        language = libreria.selectcondizionato(tabella, "chat_id", chat_id, "lingua")[0][0]
        bot.sendMessage(chat_id, traduttore("Scusami non sono riuscito a tradurre il testo, prova a ritagliare meglio la foto",language))
        return False

    
    os.system("rm -r " + nomefiletemporaneo + ".png")
    #bot.sendMessage(chat_id, traduttore("Scusami non sono ancora in grado di tradutte la foto che mi hai inviato", language))


    anno_mese_giorno = str(datetime.now())[:10]

    try:#in caso non esistesse il record prima prova a inserirlo, in caso non esiste lo inserisce lui   
        foto_tradotte = libreria.selectcondizionato(tabellaaggiornamento, "giorno", str(anno_mese_giorno), "fototradotte")[0][0]
        libreria.update(tabellaaggiornamento, "fototradotte", str(int(foto_tradotte)+1), "giorno", str(anno_mese_giorno))
    except:
        libreria.insertdue(tabellaaggiornamento, ["giorno", "audiotradotti", "personeregistrate", "fototradotte"], [str(anno_mese_giorno), str(0), "0", "1"])
    
    foto_tradotte = libreria.selectcondizionato(tabella, "chat_id", str(chat_id), "foto")[0][0]
    try:
        foto_tradotte = int(foto_tradotte)
    except:
        """
        Vuol dire che può considerarlo anche come se fosse una stringa 
        """
        pass

    if isinstance(foto_tradotte, str):
        foto_tradotte = 0
    else:
        """
        Vuol dire che ha riconosciuto l'account che ha, perchè è un int
        """
    
    libreria.update(tabella, "foto", str(int(foto_tradotte)+1), "chat_id", str(chat_id))


def ricompilazione(bot, msg, chat_id):
    """Non serve l'autentificazione con sudo in quanto viene eseguito come un superuser [da systemd]
    """
    bot.sendMessage(chat_id, "inizio a compilare")
    os.system("sudo systemctl restart ricompilazionetelegram.service")
    bot.sendMessage(chat_id_admin1, "ricompilo") if str(chat_id) != str(chat_id_admin1) else print("")




def salvataggio_file_py(bot, msg, chat_id, content_type):
    """Salvataggio del file in locale
    E Ricompilazione con il restart del bot da remoto
    sudo systemctl restart ricompilazionetelegram.service
    """

    try:
        file_id = msg['document']['file_id']
        

        nome_temporaneo = 'ricerca_copia.py'
        posizione = os.getcwd()[:-4]
        
        os.system("rm -r " + str(posizione) +"ricerca.py")

        bot.sendMessage(chat_id, "Ricevuto ") if str(chat_id_admin1) == str(chat_id) else print("")
        bot.download_file(file_id, str(nome_temporaneo))  

        os.system("mv ricerca.py " + posizione )

        ricompilazione(bot, msg, chat_id)

        return True, True
    except Exception as e:
        return False, e
    
def audio_translator(bot, msg, chat_id, content_type):
    language = libreria.selectcondizionato(tabella, "chat_id", chat_id, "lingua")[0][0]
    messaggio = bot.sendMessage(
        chat_id,
        traduttore(
            "Sto traducendo...",
            language
        )
    )

    nomefiletemporaneo = ''
    numero_randomico_file = str(random.randint(1,100000))
    nomefiletemporaneo = str(chat_id) + numero_randomico_file
        
    if content_type == 'voice':
        file_id = msg['voice']['file_id']
    else:
        file_id = msg['audio']['file_id']
    bot.download_file(file_id, str(nomefiletemporaneo)+".mp3")    

    """
    Parte in cui il bot con una maggia riesce a dividerlo per spazi
    """

                                                                         
    src = nomefiletemporaneo + ".mp3"
    dst = nomefiletemporaneo + ".wav"
                                                                  
    os.system("ffmpeg -i " + src + " -acodec pcm_u8 -ar 22050 " + dst)

    cwd = os.getcwd()
        
    testo_array = []

    audio_originale = AudioSegment.from_wav(str(cwd) + '/' + nomefiletemporaneo + ".wav")
        
    media_chunks_volume = audio_originale.dBFS
    if str(media_chunks_volume) != '-inf':

        # Split track where the silence is 2 seconds or more and get chunks using 
        # the imported function.
        print("media_chunks_volume: ",media_chunks_volume)
        chunks = split_on_silence (
            # Use the loaded audio.
            audio_originale, 
            # Specify that a silent chunk must be at least 2 seconds or 2000 ms long.
            min_silence_len = 400,
            # Consider a chunk silent if it's quieter than -16 dBFS.
            # (You may want to adjust this parameter.)
            silence_thresh = float(media_chunks_volume + media_chunks_volume*0.4),
            keep_silence = 200
        )

        # Ogni volta che salva un file in temporaneo poi fa un .append(nome_chuck) per poterlo poi riprendere
        nomi_file = []
        
        
        # Process each chunk with your parameters
        for i, chunk in enumerate(chunks):
            # Create a silence chunk that's 0.5 seconds (or 500 ms) long for padding.
            silence_chunk = AudioSegment.silent(duration=500)

            # Add the padding chunk to beginning and end of the entire chunk.
            audio_chunk = silence_chunk + chunk + silence_chunk

            # Normalize the entire chunk.
            normalized_chunk = match_target_amplitude(audio_chunk, -20.0)

            # Export the audio chunk with new bitrate.
            chunk_name = nomefiletemporaneo + "_" + str(i) + ".wav"
            normalized_chunk.export(
                chunk_name,
                bitrate = "192k",
                format = "wav"
            )
                
            nomi_file.append(chunk_name) 
    else:
        """
        A questo punto se il volume è troppo basso e non si riesce a capire bene la
        soglia del parlato, si può direttamente mandare tutto l'audio a google, senza
        neanche provare a tagliarlo
        """
        nomi_file = []
        nomi_file.append(dst)

        
        

    
    if testo_array is None:
        """
        Vuol dire che la funzione per tagliare i silenzi non è riuscita --> 
        Appende a nomi_file direttamente il file compresso con ffmpeg 
        """
        nomi_file.append(dst) 


    if 1:

        for x in nomi_file:
            sound = x
                
            r = sr.Recognizer()   #Speech recognition
            audio = sr.AudioFile(sound)
            with audio as source:
                audio_content = r.record(source)
                   
            testo_temporaneo = r.recognize_google(audio_content,language=language)
                
            testo_array.append(testo_temporaneo)

            os.system("rm -r " + str(sound))
                
        


        testo = ''
        for i, x in enumerate(testo_array):
            testo = testo + str(x) 
            if i < len(testo_array) - 1:
                testo = testo + ", "

        bot.deleteMessage((chat_id,int(messaggio['message_id'])))
        bot.sendMessage(chat_id, testo)

        audio = libreria.selectcondizionato(tabella, "chat_id", chat_id, "audio")[0][0]#in questo modo prende dal db il valore di quanti audio ha tradotto
        libreria.update(tabella, "audio", str(int(audio)+1), "chat_id", str(chat_id))


    try:
        print("")
    except Exception as e:
        messaggiodierrore = str("scusami abbiamo avuto questo problema, manda il messaggio a questa mail per avvisare l'amministratore del bot dell'errore, solo se persiste\n\n audiomessagetotex@gmail.com\n\n\n") + str(e)
        bot.sendMessage(chat_id, messaggiodierrore)
        print("ERRORE: ",str(e))
        pass
            
    anno_mese_giorno = str(datetime.now())[:10]

    try:#in caso non esistesse il record prima prova a inserirlo, in caso non esiste lo inserisce lui   
        audio = libreria.selectcondizionato(tabellaaggiornamento, "giorno", str(anno_mese_giorno), "audiotradotti")[0][0]
        libreria.update(tabellaaggiornamento, "audiotradotti", str(int(audio)+1), "giorno", str(anno_mese_giorno))
    except:
        libreria.insertdue(tabellaaggiornamento, ["giorno", "audiotradotti", "personeregistrate", "fototradotte"], [str(anno_mese_giorno), str(1), "0", "0"])



def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'voice' or content_type == 'audio':
        if verificachat(chat_id):#true ha l'account
            pass
        else:
            start(chat_id, bot, msg, False, True)
        audio_translator(bot, msg, chat_id, content_type)
        
    elif content_type == 'text':
        if msg['text'] == '/stato' and (int(chat_id) == int(chat_id_admin1) or int(chat_id) == int(chat_id_admin2)):
            admin(chat_id, bot, msg)
        elif msg['text'] == '/reboot' and (int(chat_id) == int(chat_id_admin1) or int(chat_id) == int(chat_id_admin2)):
            bot.sendMessage(chat_id,"Riavvio adesso")
            bot.sendMessage(chat_id_admin1,"Riavvio adesso") if str(chat_id) != str(chat_id_admin1) else print("")
            try:
                #Non serve l'autentificazione del superuser in quanto viene eseguito lato root
                os.system("sudo reboot")
            except:
                bot.sendMessage(chat_id, "Non sono riuscito a riavviare il computer")
                bot.sendMessage(chat_id_admin1,"Non sono riuscito a riavviare il computer") if str(chat_id) != str(chat_id_admin1) else print("")


    
        elif msg['text'] == '/ricompila' and (int(chat_id) == int(chat_id_admin1) or int(chat_id) == int(chat_id_admin2)):
            ricompilazione(bot, msg, chat_id)
        elif msg['text'] == '/aggiornamento' and (int(chat_id) == int(chat_id_admin1) or int(chat_id) == int(chat_id_admin2)):
            anno_mese_giorno = str(datetime.now())[:10]
            if len(libreria.selectcondizionatodato(tabellaaggiornamento, "giorno", str(anno_mese_giorno))) == 0:
                libreria.insertdue(tabellaaggiornamento, ["giorno", "audiotradotti", "personeregistrate", "fototradotte"], [str(anno_mese_giorno), str(0), str(0), str(0)])

            risultato = libreria.selectcompleta(tabellaaggiornamento)
            for x in risultato:
                if str(x[0]) == str(anno_mese_giorno):
                    """
                    a questo punto vuol dire che stiamo analizzando l'array contente il giorno corrente
                    """
                    audio_tradotti = str(x[1])
                    persone_registrate = str(x[2])
                    foto_tradotte = str(x[3])

                    risultato_utenti = libreria.selectcompleta(tabella)
                    
                    audio_tradotti_totali = 0
                    foto_tradotte_totali = 0

                    for k in risultato_utenti:
                        audio_tradotti_totali = audio_tradotti_totali + int(k[2])
                        try: 
                            foto_tradotte_totali = foto_tradotte_totali + int(k[3])
                        except:
                            pass

                    testo = 'Audio tradotti oggi: ' + audio_tradotti + "\nPersone registrate oggi: " + persone_registrate + "\nFoto tradotte oggi: " + str(foto_tradotte) +"\n\nUtenti in totale: " + str(len(risultato_utenti)) + "\nAudio totali: " + str(audio_tradotti_totali) + "\nFoto tradotte in totale: " + str(foto_tradotte_totali)
                    bot.sendMessage(chat_id, testo)
                    break


        elif msg['text'][:16] == '/messaggioatutti' and (int(chat_id) == int(chat_id_admin1) or int(chat_id) == int(chat_id_admin2)):
            adminstatistiche(chat_id, bot, msg, False, False)
            

        elif msg['text'] == '/sponsor':
            language = libreria.selectcondizionato(tabella=tabella, campo="chat_id", valore=chat_id, campo2="lingua")[0][0]
            testo = traduttore('Per tutte le info, prezzi e modalità per le sponsorizzazioni (la tua pubblicità in questo canale) scrivi all’indirizzo mail:', language) + " audiomessagetotex@gmail.com."
            bot.sendMessage(chat_id, testo)

        elif msg['text'] == '/start':
            if verificachat(chat_id):
                start(chat_id, bot, msg, True, True)#se True vuol dire che è registrato, secondo False vuol dire che non ha chiesto di cambiare la lingua
            else:
                start(chat_id, bot, msg, False, True)#se False vuol dire che non è ancora registrato, secondo False vuol dire che non ha chiesto di cambiare la lingua
            
            pubblicita(chat_id, bot, msg)
            language = libreria.selectcondizionato(tabella=tabella, campo="chat_id", valore=chat_id, campo2="lingua")[0][0]
            bot.sendMessage(chat_id, 
                traduttore("Inoltrami un messaggio vocale ''o un qualsiasi file audio'' e io lo traduttò in un messaggio di testo.\nOppure inviami una foto e ritagliala sulla parte che ti interessa convertire in testo.", language))
        
        elif msg['text'] == '/donate':
            if verificachat(chat_id):
                pass
            else:
                start(chat_id, bot, msg, False, True)#crea dicendogli che ha capito una lingua
            
            pubblicitadonate(chat_id, bot, msg)

        elif msg['text'] == '/setlanguage':
            if verificachat(chat_id):
                pass
            else:
                start(chat_id, bot, msg, False, False)#se False vuol dire che non è ancora registrato, il secondo per dirgli che deve registrarlo senza output, con la lingua inglese
            
            language = libreria.selectcondizionato(tabella, "chat_id", chat_id, "lingua")[0][0]
            messaggio = traduttore("Setta la tua lingua",language) + "\n"
            for x in lingue:
                messaggio += str(lingue[x]) + "\n"
            bot.sendMessage(chat_id, messaggio)

        elif msg['text'] == '/privacy':
            if verificachat(chat_id):
                pass
            else:
                start(chat_id, bot, msg, False, True)#se False vuol dire che non è ancora registrato, il secondo per dirgli che deve registrarlo senza output, con la lingua inglese
            
            language = libreria.selectcondizionato(tabella, "chat_id", chat_id, "lingua")[0][0]
            testo = "Il bot registra l'utente e i suoi settaggi come la lingua e il chat id in modo da non dover reimpostare ogni volta la lingua.\nI messaggi vocali inviati vengono cancellati non appena vengono tradotti in testo e quest'ultimo non può essere richiamato o ricercato in nessun modo all'interno del log.\nIn questo modo solamente voi potete conoscere il contenuto dei vostri audio e la relativa trascrizione."
            testo = traduttore(testo, language)
            bot.sendMessage(chat_id, testo)
        
        elif msg['text'][0] == '/':
            """
            Cerca di capire se il comando / è per settare una lingua
            """
            if verificachat(chat_id):
                pass
            else:
                start(chat_id, bot, msg, False, False)#lo crea zitto con lingua = en-GB
                
            controllo = False
            for y, x in lingue.items():
                if x == msg['text']:
                    language = y
                    audio = libreria.selectcondizionato(tabella=tabella, campo="chat_id", valore=chat_id, campo2="audio")[0][0]
                    foto = libreria.selectcondizionato(tabella=tabella, campo="chat_id", valore=chat_id, campo2="foto")[0][0]
                    try:
                        libreria.deletecondizionato(tabella, "chat_id", chat_id)
                    except Exception as e:
                        print(e, "probabilmente non c'era già il record con l'utente")

                    libreria.insertdue(tabella, ["chat_id","lingua","audio", "foto"], [chat_id, language, audio, foto])
                    controllo = True
            if controllo:
                bot.sendMessage(chat_id, (traduttore("Lingua impostata correttamente su",language) + " " + str(lingue[language])[1:]))
            else:
                #se non capisco che lingua mi ha chiesto di impostare, o se sta cercando un comando che non esiste 
                language = libreria.selectcondizionato(tabella=tabella, campo="chat_id", valore=chat_id, campo2="lingua")[0][0]
                bot.sendMessage(chat_id, ((traduttore("Scusami non sono ancora in grado di settare questa lingua o di fare la cosa che mi hai chiesto, se vuoi cambiare una lingua devi digitare",language) + " /setlanguage\n\n" +traduttore("Se hai dei consigli o per qualunque segnalazione scrivi a audiomessagetotex@gmail.com",language))))
            
            
        

        else:
            #in caso mi ha mandato un testo o dello scritto
            if verificachat(chat_id):
                pass #pass perchè tanto la recupero dopo la lingua [solo in caso l'account già esiste]
                # language = libreria.selectcondizionato("utenti", "chat_id", chat_id, "lingua")
            else:
                start(chat_id, bot, msg, False, True)#capisce zitto che lingua ha settato su telegram

            language = libreria.selectcondizionato(tabella=tabella, campo="chat_id", valore=chat_id, campo2="lingua")[0][0]#prende la lingua dal db in caso l'abbia cambiata

            bot.sendMessage(chat_id, traduttore("Scusami non sono ancora in grado si fare quello che mi hai chiesto", language))   
    
    elif content_type == 'photo':#in caso sia un immagine o qualcosa d'alttro
        controllo = True
        if str(chat_id) == str(chat_id_admin1) or str(chat_id) == str(chat_id_admin2):
            controllo = amministratorefoto(bot, msg, chat_id)
            
        if controllo:
            riconoscimentofoto(bot, msg, chat_id)
    else:       
        if verificachat(chat_id):
            pass
        else:
            start(chat_id, bot, msg, False, True)
            

        if str(chat_id) == str(chat_id_admin1):
            verifica, errore = salvataggio_file_py(bot, msg, chat_id, content_type)
            if verifica:
                bot.sendMessage(chat_id_admin1, "Ricompilazione avvenuta con successo tranki")
            else:
                bot.sendMessage(chat_id_admin1, str(errore) + "\n\nsorry")

        else:
            language = libreria.selectcondizionato(tabella, "chat_id", chat_id, "lingua")[0][0]
            bot.sendMessage(chat_id, traduttore("Scusami non sono ancora in grado di fare quello che mi hai chiesto", language))



language = 'en-GB'
bot = telepot.Bot(TOKEN)
bot.message_loop(on_chat_message)

while 1:
    time.sleep(10)


