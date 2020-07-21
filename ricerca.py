# -*- coding: utf-8 -*-
#versione 18 luglio 21:03

try:
    import da_importare
except:
    """
    Serve per gestire l'errore di pycompile su macchine aws
    """
    pass
import subprocess
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
import riconoscimento_lingua as ric_ling
from audio_ritorno import riconoscimento


VERSIONE = 'stable'
#VERSIONE = 'testing'

stringa = '/home/ubuntu/bottelegram/config.json' if VERSIONE == 'stable' else 'config.json'

with open(stringa,) as f:
    data = json.load(f)


chat_id_admin1 = data['chat_id_admin1']
chat_id_admin2 = data['chat_id_admin2']

#controlla la versione e setta i nomi delle tabelle in base a cosa è direzionata la versione attuale del file
if VERSIONE == 'stable':
    tabella = 'utenti'
    tabellaaggiornamento = 'statistiche'
    #TOKEN = '' #STABLE
    TOKEN = data['token_stable']
else:
    tabella = 'utenti2'
    tabellaaggiornamento = 'statistiche2'
    #TOKEN = '' #TESTING
    TOKEN = data['token_unstable']

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



            #libreria.insertdue(tabella, ["chat_id", "lingua","audio", "foto"], [chat_id, language, "0", "0"])


            """
            Inserimento nella tabella di aggiornamento
            """
            #anno_mese_giorno = str(datetime.now())[:10]

            #try:#in caso non esistesse il record prima prova a inserirlo, in caso non esiste lo inserisce lui
            #    persone_registrate_oggi = libreria.selectcondizionato(tabellaaggiornamento, "giorno", str(anno_mese_giorno), "personeregistrate")[0][0]
            #    libreria.update(tabellaaggiornamento, "personeregistrate", str(int(persone_registrate_oggi)+1), "giorno", str(anno_mese_giorno))
            #except:
            #    libreria.insertdue(tabellaaggiornamento, ["giorno", "audiotradotti", "personeregistrate", "fototradotte"], [str(anno_mese_giorno), "0", "1", "0"])

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
    add_db(chat_id,lingua=language)





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
            language = libreria.selectcondizionato(tabella, "chat_id", chat_id, "lingua")[0][0]
            testo_tradotto = traduttore(testo, language)
            bot.sendMessage(chat_id, testo_tradotto)
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
    """
    Controllo se la foto che è stata mandata è stata mandata era
    sia da parte dell'admin uno e due.

    Controllo successivo se è presente il /messaggioatutto [per mandare il
    messaggio a tutte le persone iscritte al bot]
    """
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
            bot.sendMessage(chat_id_admin1, str(e))
            bot.sendMessage(chat_id_admin2, str(e))
            return True

    else:
        return True #serve per non far fare il controllo

def riconoscimentofoto(bot, msg, chat_id):
    errori_traduzione = []
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
    except Exception as e:
        errori_traduzione.append(e)
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
    except Exception as e:
        errori_traduzione.append(e)
        verifica = False

    try:
        text_detected = parsed_results.get("ParsedText")
    except Exception as e:
        errori_traduzione.append(e)
        verifica = False

    bot.deleteMessage((chat_id,int(messaggio['message_id'])))
    """
    Dopo aver controllato il risultato della foto manda la traduzione
    In caso sia entrato con un errore manda il messaggio all'admin con l'errore
    e poi gli dice che ha avuto un problema
    """

    if verifica:
        bot.sendMessage(chat_id, str(text_detected))
    else:
        language = libreria.selectcondizionato(tabella, "chat_id", chat_id, "lingua")[0][0]
        bot.sendMessage(chat_id, traduttore("Scusami non sono riuscito a tradurre il testo, prova a ritagliare meglio la foto",language))


    os.system("rm -r " + nomefiletemporaneo + ".png")

    if verifica == False and verifica is not None:
        for errori_temporaneo in errori_traduzione:
            bot.sendMessage(chat_id_admin1, errori_temporaneo)


    anno_mese_giorno = str(datetime.now())[:10]

    #try:#in caso non esistesse il record prima prova a inserirlo, in caso non esiste lo inserisce lui
    #    foto_tradotte = libreria.selectcondizionato(tabellaaggiornamento, "giorno", str(anno_mese_giorno), "fototradotte")[0][0]
    #    libreria.update(tabellaaggiornamento, "fototradotte", str(int(foto_tradotte)+1), "giorno", str(anno_mese_giorno))
    #except:
    #    libreria.insertdue(tabellaaggiornamento, ["giorno", "audiotradotti", "personeregistrate", "fototradotte"], [str(anno_mese_giorno), str(0), "0", "1"])

    #foto_tradotte = libreria.selectcondizionato(tabella, "chat_id", str(chat_id), "foto")[0][0]


    #try:
    #    foto_tradotte = int(foto_tradotte)
    #except:
    #    """
    #    Vuol dire che è una stringa e nella colonna l'utente non ha mai tradotto una foto
    #    --> E quindi lo considera 0
    #    """
    #    if isinstance(foto_tradotte, str):
    #        foto_tradotte = 0

    add_db(chat_id, content_type="photo")
    #libreria.update(tabella, "foto", str(int(foto_tradotte)+1), "chat_id", str(chat_id))


def ricompilazione(bot, msg, chat_id):
    """
    Non serve l'autentificazione con sudo in quanto viene eseguito come un superuser [da systemd]

    You can not have superuser to restart the service because it will execute with systemd
    """
    bot.sendMessage(chat_id, "inizio a compilare")
    os.system("systemctl restart ricompilazionetelegram.service > log_ricompilazione.txt")

    with open("log_ricompilazione.txt") as f:
        testo_log_ricompilazione = f.readlines()

    os.system("rm -r log_ricompilazione.txt")
    bot.sendMessage(chat_id_admin1, str(testo_log_ricompilazione))





def salvataggio_file_py(bot, msg, chat_id, content_type):
    """
    Salvataggio del file in locale
    E Ricompilazione con il restart del bot da remoto
    sudo systemctl restart ricompilazionetelegram.service

    Download the file in the path folder
    ricompilation and restart of systemd service [ricompilazionetelegram.service]
    """

    try:
        file_id = msg['document']['file_id']

        nome_temporaneo = 'ricerca.py'

        os.system("rm -r /home/ubuntu/bottelegram/ricerca.py")

        bot.sendMessage(chat_id, "Ricevuto")
        bot.download_file(file_id, str(nome_temporaneo))

        os.system("mv ricerca.py /home/ubuntu/bottelegram/ricerca.py")

        ricompilazione(bot, msg, chat_id)

        return True, True
    except Exception as e:
        return False, e

def audio_translator(bot, msg, chat_id, content_type, nome):
    language = libreria.selectcondizionato(tabella, "chat_id", chat_id, "lingua")[0][0]
    messaggio = bot.sendMessage(
        chat_id,
        traduttore(
            "Sto traducendo...",
            language
        )
    )

    if not nome:
        nomefiletemporaneo = ''
        numero_randomico_file = str(random.randint(1,100000))
        nomefiletemporaneo = str(abs(chat_id)) + numero_randomico_file


        if content_type == 'voice':
            file_id = msg['voice']['file_id']
            bot.download_file(file_id, str(nomefiletemporaneo)+".mp3")
        else:
            """
            Vuol dire che è per forza un audio, e non un messaggio vocale diretto

            Non è neanche un audio che gli viene passato in quanto altrimenti entrerebbe in quello
            prima
            """

            file_id = msg['audio']['file_id']
            bot.download_file(file_id, str(nomefiletemporaneo)+".mp3")

        src = nomefiletemporaneo + ".mp3"
        dst = nomefiletemporaneo + ".wav"

    else:
        nomefiletemporaneo = nome[:-4]
        src = nome

        # In questo punto viene rimosso il .mp4 e sostituito con .wav
        dst = nome[:-4] + ".wav"



    """Qua fa la compressione del file audio e lo comprime in wav"""
    #os.system("ffmpeg -i " + src + " -acodec pcm_u8 -ab 800k -ar 44100 " + dst)

    """ Cambio bitrait mp3 """
    #os.system("ffmpeg -i " + src + " -ab 800k -ar 44100 " + src)

    """ Altra prova per la codifica in wav """
    os.system("ffmpeg -i " + src + " " + dst)
    cwd = os.getcwd()

    testo_array = []

    audio_originale = AudioSegment.from_wav(cwd + '/' + nomefiletemporaneo + ".wav")
    #audio_originale = AudioSegment.from_file(cwd + "/" + nomefiletemporaneo + ".mp3", format = 'mp3')


    try:
        media_chunks_volume = audio_originale.dBFS
    except:
        media_chunks_volume = None


    if str(media_chunks_volume) != '-inf' and media_chunks_volume is not None:
        # Split track where the silence is 2 seconds or more and get chunks using
        # the imported function.
        print("media_chunks_volume: ",media_chunks_volume)
        chunks = split_on_silence (
            # Use the loaded audio.
            audio_originale,
            # Specify that a silent chunk must be at least 2 seconds or 2000 ms long.
            min_silence_len = 250,
            # Consider a chunk silent if it's quieter than -16 dBFS.
            # (You may want to adjust this parameter.)
            silence_thresh = float(media_chunks_volume + media_chunks_volume*0.3),
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


    try:
        #inizializzazione della classe come recognizer
        r = sr.Recognizer()


        def audio_direct(bot, dst, language, chat_id, verifica = True):
            """
            Fa la traduzione diretta a google e dopo manda il testo
            """
            try:
                sound = dst
                audio = sr.AudioFile(sound)
                with audio as source:
                    audio_content = r.record(source)


                testo_tradotto_intero = r.recognize_google(
                                                        audio_content,
                                                        language=language,
                                                        show_all=True
                                                        )

                print(testo_tradotto_intero)

                if not testo_tradotto_intero:
                    """ If it is [] --> return false and '' """
                    return False, ''

                testo_tradotto_intero = testo_tradotto_intero['alternative'][0]['transcript']

                if verifica:
                    testo_invio = traduttore('Testo senza eliminazione dei silenzi', language)

                    testo_invio = testo_invio + "\n\n" + testo_tradotto_intero

                    bot.sendMessage(chat_id, testo_invio, reply_to_message_id=msg['message_id'])
                    return True, testo_invio

                else:
                    return True, testo_tradotto_intero
            
            except Exception as e:
                """ Error in e """
                return False, e





        try:
            for x in nomi_file:
                """
                Fa la traduzione in caso ci siano più di un chuck
                E appende tutto a testo_array
                """

                sound = x

                #Speech recognition
                audio = sr.AudioFile(sound)
                with audio as source:
                    audio_content = r.record(source)

                testo_temporaneo = r.recognize_google(
                                            audio_content,
                                            language=language
                                        )

                testo_array.append(testo_temporaneo)


        except:
            """
            In questo caso se ha riscontrato qualche errore nella traduzione
            lascia stare e invia solo quello completo
            """

            testo_array.clear()
            nomi_file.clear()



        testo = ''
        for i, x in enumerate(testo_array):
            testo = testo + str(x)
            if i < len(testo_array) - 1:
                testo = testo + ", "

        bot.deleteMessage((chat_id,int(messaggio['message_id'])))

        if testo_array: # If the array is not empty the testo_array return True
            """ Se la traduzione con i silenzi ha funzionato """
            """ Fa la traduzione solamente senza direttamente i silenzi """
            testo = traduttore("Testo con l'eliminazione dei silenzi", language) + "\n\n" + testo if len(nomi_file) > 1 else testo

            bot.sendMessage(
                chat_id, 
                testo, 
                reply_to_message_id=msg['message_id']
                )


        else:
            """ Se la traduzione con i silenzi ha fallito """
            testo = traduttore('Scusami non sono riuscito a eliminare i silenzi e sostituirli con le virgole', language)
            messaggio_eliminazione = bot.sendMessage(
                chat_id, 
                testo, 
                reply_to_message_id=msg['message_id']
                )

            if len(nomi_file) < 2:
                bot.deleteMessage((chat_id, messaggio_eliminazione['message_id']))
                verifica, testo_funzione = audio_direct(bot, dst, language, chat_id, False)
                if verifica:
                    bot.sendMessage(chat_id, testo_funzione, reply_to_message_id=msg['message_id'])
                
                
                else:

                    """

                    Vuol dire che non è riuscito a tradurre niente
                    --> o è vuoto
                    --> o è un errore

                    """
                    try:
                        bot.deleteMessage( (chat_id, messaggio_eliminazione['message_id']))
                    except:
                        pass


                    if isinstance(testo_funzione, str):
                        if testo_funzione == '':
                            #bot.deleteMessage((chat_id, niente['message_id']))
                            bot.sendMessage(chat_id, traduttore("Il messaggio è vuoto", language), reply_to_message_id=msg['message_id'])

                    else:    
                        bot.sendMessage(chat_id, traduttore("Scusaci non siamo riusciti a tradurre niente",language))

            
            # bot.sendMessage(chat_id, str(testo_funzione), reply_to_message_id=msg['message_id'])
            

        if len(nomi_file) > 1:
            """ manda il messaggio in caso si siano divisi anche i silenzi """
            verifica, testo = audio_direct(bot, dst, language, chat_id)


    except Exception as e:
        if "messaggio_eliminazione" in locals():
            try:
                bot.deleteMessage((chat_id, messaggio_eliminazione['message_id']))
            except:
                pass

        elif "messaggio" in locals():
            try:
                bot.deleteMessage((chat_id, messaggio_eliminazione['message_id']))
            except:
                pass

        else:
            """ It means there is no messagge send to the chat_id """
            pass
        
        
        messaggiodierrore = "Scusami abbiamo avuto questo problema, manda il messaggio a questa mail per avvisare l'amministratore del bot dell'errore, solo se persiste\n\n audiomessagetotex@gmail.com\n\n\n"
        language = libreria.selectcondizionato(tabella=tabella, campo="chat_id", valore=chat_id, campo2="lingua")[0][0]
        bot.sendMessage(chat_id, traduttore(messaggiodierrore, language) + str(e), reply_to_message_id=msg['message_id'])

    #anno_mese_giorno = str(datetime.now())[:10]

    #if content_type == 'voice' or 'audio':#in caso non esistesse il record prima prova a inserirlo, in caso non esiste lo inserisce lui
        #audio = libreria.selectcondizionato(tabellaaggiornamento, "giorno", str(anno_mese_giorno), "audiotradotti")[0][0]
        #libreria.update(tabellaaggiornamento, "audiotradotti", str(int(audio)+1), "giorno", str(anno_mese_giorno))
    #elif content_type == 'video_note':
    add_db(chat_id, content_type)

    os.system("rm -r " + str(abs(chat_id)) + "*")


def add_db(chat_id, content_type = None, lingua = None):
    utenti_valori = {
        "voice": "audio",
        "audio": "audio",
        "video_note" : "video_messaggi",
        "video" : "video",
        "photo" : "foto"
    }
    statistiche_valori = {
        "voice": "audiotradotti",
        "audio": "audiotradotti",
        "video_note" : "video_messaggi_tradotti",
        "video" : "video_tradotti",
        "photo" : "fototradotte"
    }

    """ Controllo per quanto riguarda l'esistenza del giorno corrente in 'statistiche' """
    anno_mese_giorno = str(datetime.now())[:10]
    valore = libreria.selectcondizionatodato(tabellaaggiornamento, "giorno", anno_mese_giorno)
    if not valore:
        """ Vuol dire che bisogna aggiungere il giorno perchè c'è già """
        libreria.insertdue(tabellaaggiornamento,
            ["giorno",
            "audiotradotti",
            "personeregistrate",
            "fototradotte",
            "video_messaggi_tradotti",
            "video_tradotti"],

            [anno_mese_giorno,
            "0",
            "0",
            "0",
            "0",
            "0"])


    if content_type and lingua is None:
        """ Vuol dire che la funzione è stata richiamata senza specificare la lingua """
        """ Utenti [user] """
        valore = libreria.selectcondizionato(tabella, "chat_id", chat_id, utenti_valori[content_type])[0][0]

        try:
            """
            In case the user didn't have 0 in the db
            """
            valore_utente = int(valore)
        except:
            valore_utente = 0


        libreria.update(
            tabella,
            utenti_valori[content_type],
            str(valore_utente + 1),
            "chat_id",
            chat_id
            )

        """ Statistiche [statistic] """
        valore = libreria.selectcondizionato(tabellaaggiornamento, "giorno", anno_mese_giorno, statistiche_valori[content_type])[0][0]
        try:
            valore = int(valore)
        except:
            valore = 0

        try:
            valore_utente = int(valore)
        except:
            valore_utente = 0


        libreria.update(
            tabellaaggiornamento,
            statistiche_valori[content_type],
            str(valore_utente + 1),
            "giorno",
            anno_mese_giorno
            )
    elif lingua is not None and content_type is None and not verificachat(chat_id):
        """
        insert per le persone che si iscrivono e fanno /start
        """

        libreria.insertdue(tabella,
            [
                "chat_id",
                "lingua",
                "audio",
                "foto",
                "video_messaggi",
                "video"
            ],
            [
                chat_id,
                lingua,
                "0",
                "0",
                "0",
                "0"
            ])

        valore = libreria.selectcondizionato(tabellaaggiornamento, "giorno", anno_mese_giorno, "personeregistrate")[0][0]
        libreria.update(
            tabellaaggiornamento,
            "personeregistrate",
            str(int(valore) + 1),
            "giorno",
            anno_mese_giorno
            )


    else:
        pass
    #if content_type == 'voice' or 'audio':#in caso non esistesse il record prima prova a inserirlo, in caso non esiste lo inserisce lui
        #audio = libreria.selectcondizionato(tabellaaggiornamento, "giorno", str(anno_mese_giorno), "audiotradotti")[0][0]
        #libreria.update(tabellaaggiornamento, "audiotradotti", str(int(audio)+1), "giorno", str(anno_mese_giorno))



def scissione(bot, msg, chat_id, content_type):
    """
    verifica = True or False --> if all work fine
    nome = name of the file in local
    e = False or
    """

    nome_video_temporaneo = str(abs(chat_id)) + str(random.randint(1,100000)) + '.mp4'
    file_id = msg['video']['file_id'] if content_type == 'video' else msg['video_note']['file_id']

    try:
        bot.download_file(file_id, str(nome_video_temporaneo))

        command_shell = "ffmpeg -i " + nome_video_temporaneo + " -ab 600k -ac 2 -ar 44100 -vn " + nome_video_temporaneo[:-4] + ".mp3 > " + "log_" + nome_video_temporaneo[:-4] + ".txt"

        os.system(command_shell)

        #with open("log_" + nome_video_temporaneo[:-4], "r") as f:
        #    log_scissione = f.readlines()

        """
        Funzione successiva: gestire l'errore di ffmpeg [per adesso non scrive neanche sul log
        --> lo lascia vuoto]
        """
        if True:
            os.system("rm -r " + nome_video_temporaneo)
            os.system("rm -r " + "log_" + nome_video_temporaneo[:-4] + ".txt")
            return True, nome_video_temporaneo[:-4] + '.mp3', False

        else:
            os.system("rm -r " + nome_video_temporaneo)
            os.system("rm -r " + "log_" + nome_video_temporaneo[:-4] + ".txt")
            return False, None, None

        import sys
        sys.exit("siamo qua, ho finito la scissione")
    except Exception as e:

        """
        Errore che ritorna in questa parte dell'except è se qualcosa va male lato python
        In caso di errore nel salvataggio o altre cose
        Nel log sopra viene preso il log di ffmpeg da bash
        """
        s.system("rm -r " + "log_" + nome_video_temporaneo[:-4] + ".txt")
        os.system("rm -r " + nome_video_temporaneo)

        return True, None, e
    



def on_chat_message(msg):
    
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'voice' or content_type == 'audio':
        if not verificachat(chat_id):#true ha l'account
            start(chat_id, bot, msg, False, True)

        audio_translator(bot, msg, chat_id, content_type, False)

    elif content_type == 'text':
        if msg['text'] == '/stato' and (int(chat_id) == int(chat_id_admin1) or int(chat_id) == int(chat_id_admin2)):
            admin(chat_id, bot, msg)
        elif msg['text'] == '/reboot' and (int(chat_id) == int(chat_id_admin1) or int(chat_id) == int(chat_id_admin2)):
            bot.sendMessage(chat_id,"Riavvio adesso")
            bot.sendMessage(chat_id_admin1,"Riavvio adesso") if str(chat_id) != str(chat_id_admin1) else 0
            
            subprocess.Popen(['python', 'riavvio.py', 'riavvia'])
            
            bot.sendMessage(chat_id_admin1, "avviata")


        elif msg['text'][:10] == '/ricompila' and (int(chat_id) == int(chat_id_admin1) or int(chat_id) == int(chat_id_admin2)):
            ricompilazione(bot, msg, chat_id)
        elif msg['text'][:14] == '/aggiornamento' and (int(chat_id) == int(chat_id_admin1) or int(chat_id) == int(chat_id_admin2)):
            anno_mese_giorno = str(datetime.now())[:10]
            if len(libreria.selectcondizionatodato(tabellaaggiornamento, "giorno", str(anno_mese_giorno))) == 0:
                libreria.insertdue(
                    tabellaaggiornamento,
                    ["giorno",
                    "audiotradotti",
                    "personeregistrate",
                    "fototradotte",
                    "video_messaggi_tradotti",
                    "video_tradotti"],

                    [str(anno_mese_giorno),
                    str(0),
                    str(0),
                    str(0),
                    str(0),
                    str(0)])

            risultato = libreria.selectcompleta(tabellaaggiornamento)
            for x in risultato:
                if str(x[0]) == str(anno_mese_giorno):
                    """
                    a questo punto vuol dire che stiamo analizzando l'array contente il giorno corrente
                    """
                    audio_tradotti = str(x[1])
                    persone_registrate = str(x[2])
                    foto_tradotte = str(x[3])
                    video_messaggi_tradotti = str(x[4])
                    video_tradotti = str(x[5])

                    risultato_utenti = libreria.selectcompleta(tabella)

                    audio_tradotti_totali = 0
                    foto_tradotte_totali = 0
                    video_messaggi_tradotti_totali = 0
                    video_tradotti_totali = 0

                    for k in risultato_utenti:
                        try:
                            audio_tradotti_totali = audio_tradotti_totali + int(k[2])
                        except:
                            pass
                        try:
                            foto_tradotte_totali = foto_tradotte_totali + int(k[3])
                        except:
                            pass


                        try:
                            video_messaggi_tradotti_totali = video_messaggi_tradotti_totali + int(k[4])
                        except:
                            pass

                        try:
                            video_tradotti_totali = video_tradotti_totali + int(k[5])
                        except:
                            pass
                    testo = 'Audio tradotti oggi: ' + str(audio_tradotti) + "\nPersone registrate oggi: " + str(persone_registrate) + "\nFoto tradotte oggi: " + str(foto_tradotte) +"\nVideo messaggi tradotti: " + str(video_messaggi_tradotti) +"\nVideo tradotti: " + str(video_tradotti) +"\n\nUtenti in totale: " + str(len(risultato_utenti)) + "\nAudio totali: " + str(audio_tradotti_totali) + "\nFoto tradotte in totale: " + str(foto_tradotte_totali) + "\nVideo tradotti: " + str(video_messaggi_tradotti_totali) + "\nVideo tradotti in totale: " + str(video_tradotti_totali)
                    bot.sendMessage(chat_id, testo)

        elif msg['text'][:8] == '/comandi' and str(chat_id) == str(chat_id_admin1):
            testo = """
            /messaggioatutti 1.00 ciao

            /ricompila ricompila il file che c'è già invia un file chiamato ricerca.py e lui lo ricompilerà

            /reboot riavvia la macchina

            /service riavvia il bottelegram.service
            """
            bot.sendMessage(chat_id, testo)

        elif msg['text'][:8] == '/service' and chat_id == int(chat_id_admin1):
            subprocess.Popen(['python', 'riavvio.py', 'servizio'])
            bot.sendMessage(chat_id_admin1, "Non sono riuscito a riavviare il servizio")

        elif msg['text'][:16] == '/messaggioatutti' and (int(chat_id) == int(chat_id_admin1) or int(chat_id) == int(chat_id_admin2)):
            adminstatistiche(chat_id, bot, msg, False, False)


        elif msg['text'][:8] == '/sponsor':
            language = libreria.selectcondizionato(tabella=tabella, campo="chat_id", valore=chat_id, campo2="lingua")[0][0]
            testo = traduttore('Per tutte le info, prezzi e modalità per le sponsorizzazioni (la tua pubblicità in questo canale) scrivi all’indirizzo mail:', language) + " audiomessagetotex@gmail.com."
            bot.sendMessage(chat_id, testo)

        elif msg['text'][:6] == '/start':
            if verificachat(chat_id):
                start(chat_id, bot, msg, True, True)#se True vuol dire che è registrato, secondo False vuol dire che non ha chiesto di cambiare la lingua
            else:
                start(chat_id, bot, msg, False, True)#se False vuol dire che non è ancora registrato, secondo False vuol dire che non ha chiesto di cambiare la lingua

            pubblicita(chat_id, bot, msg)
            language = libreria.selectcondizionato(tabella=tabella, campo="chat_id", valore=chat_id, campo2="lingua")[0][0]
            bot.sendMessage(chat_id,
                traduttore("Inoltrami un media (messaggio vocale, video messaggio, video, foto, o un file audio) e io lo tradurrò in testo.\n Se vuoi inviarmi una foto ritagliala sulla parte che ti interessa convertire in testo.", language))

        elif msg['text'][:7] == '/donate':
            if verificachat(chat_id):
                pass
            else:
                start(chat_id, bot, msg, False, True)#crea dicendogli che ha capito una lingua

            pubblicitadonate(chat_id, bot, msg)

        elif msg['text'][:12] == '/setlanguage':
            if verificachat(chat_id):
                pass
            else:
                start(chat_id, bot, msg, False, False)#se False vuol dire che non è ancora registrato, il secondo per dirgli che deve registrarlo senza output, con la lingua inglese

            language = libreria.selectcondizionato(tabella, "chat_id", chat_id, "lingua")[0][0]
            messaggio = traduttore("Setta la tua lingua",language) + "\n"
            for x in lingue:
                messaggio += str(lingue[x]) + "\n"
            bot.sendMessage(chat_id, messaggio)

        elif msg['text'][:8] == '/privacy':
            if not verificachat(chat_id):
                start(chat_id, bot, msg, False, True)#se False vuol dire che non è ancora registrato, il secondo per dirgli che deve registrarlo senza output, con la lingua inglese

            language = libreria.selectcondizionato(tabella, "chat_id", chat_id, "lingua")[0][0]
            testo = "Il bot registra l'utente e i suoi settaggi come la lingua e il chat id in modo da non dover reimpostare ogni volta la lingua.\nI messaggi vocali inviati vengono cancellati non appena vengono tradotti in testo e quest'ultimo non può essere richiamato o ricercato in nessun modo all'interno del log.\nIn questo modo solamente voi potete conoscere il contenuto dei vostri audio e la relativa trascrizione."
            testo = traduttore(testo, language)
            bot.sendMessage(chat_id, testo)

        elif msg['text'][:11] == '/sourcecode':
            """
            It send the link for the repo in github
            """
            language = libreria.selectcondizionato(tabella, "chat_id", chat_id, "lingua")[0][0]
            testo = traduttore("Se vuoi leggere il codice sorgente del bot clicca su", language) + " https://github.com/giacomogroppi/audio_translator_telegram"
            bot.sendMessage(chat_id, testo)

        elif msg['text'][0] == '/':
            """
            Cerca di capire se il comando / è per settare una lingua
            """
            if not verificachat(chat_id):
                start(chat_id, bot, msg, False, False)#lo crea zitto con lingua = en-GB

            controllo = False
            for y, x in lingue.items():
                if x == msg['text'][:len(x)]:
                    language = y

                    libreria.update(tabella, "lingua", language, "chat_id", chat_id)
                    controllo = True
            if controllo:
                bot.sendMessage(chat_id, (traduttore("Lingua impostata correttamente su",language) + " " + str(lingue[language])[1:].lower()))
            else:
                #se non capisco che lingua mi ha chiesto di impostare, o se sta cercando un comando che non esiste
                language = libreria.selectcondizionato(tabella=tabella, campo="chat_id", valore=chat_id, campo2="lingua")[0][0]
                bot.sendMessage(chat_id, ((traduttore("Scusami non sono ancora in grado di settare questa lingua o di fare la cosa che mi hai chiesto, se vuoi cambiare una lingua devi digitare",language) + " /setlanguage\n\n" +traduttore("Se hai dei consigli o per qualunque segnalazione scrivi a audiomessagetotex@gmail.com",language))))


        else:
            # in caso mi ha mandato un testo o dello scritto
            if not verificachat(chat_id):
                start(chat_id, bot, msg, False, True)#capisce zitto che lingua ha settato su telegram

            language = libreria.selectcondizionato(tabella=tabella, campo="chat_id", valore=chat_id, campo2="lingua")[0][0]#prende la lingua dal db in caso l'abbia cambiata
        
            if chat_type != "group":
                bot.sendMessage(chat_id, traduttore("Scusami non sono ancora in grado si fare quello che mi hai chiesto", language))

    elif content_type == 'photo' and chat_type != 'group': # in caso sia un immagine o qualcosa d'altro
        controllo = True
        if str(chat_id) == str(chat_id_admin1) or str(chat_id) == str(chat_id_admin2):
            controllo = amministratorefoto(bot, msg, chat_id)

        if controllo:
            riconoscimentofoto(bot, msg, chat_id)

    elif content_type == 'video' or content_type == 'video_note':
        if not verificachat(chat_id):
            """ It means the user is not register in the db """
            start(chat_id, bot, msg, False, False)


        verifica, nome, e = scissione(bot, msg, chat_id, content_type)
        
        if verifica:
            audio_translator(bot, msg, chat_id, content_type, nome)
        else:
            language = libreria.selectcondizionato(tabella, "chat_id", chat_id, "lingua")[0][0]
            bot.sendMessage(
                chat_id,
                traduttore("Scusa ho avuto questo problema", language) + " " + str(e))

            bot.sendMessage(chat_id_admin1, "video" + str(e)) if chat_id_admin1 != chat_id else 0
    elif content_type == 'document':
        """
        If the file the bot reciving is a py, he download it in the saim folder and compile with the systemd service
        Only if the file that the admin send is name ricerca.py it will compile it --> In any other case it will send
        a message to aller him of the name of the file [if he want to compile it]
        """

        if not verificachat(chat_id):
            """ It means the user is not register in the db """
            start(chat_id, bot, msg, False, False)


        if str(chat_id) == str(chat_id_admin1):
            if msg['document']['file_name'] == 'ricerca.py':
                verifica, errore = salvataggio_file_py(bot, msg, chat_id, content_type)
                if verifica:
                    bot.sendMessage(chat_id_admin1, "Ricompilazione avvenuta con successo tranki")
                else:
                    bot.sendMessage(chat_id_admin1, str(errore) + "\n\nsorry")
            else:
                bot.sendMessage(chat_id, "If you want to compile it you need to change the name of the file from " + str(msg['document']['file_name']) + " to ricerca.py")
        else:
            language = libreria.selectcondizionato(tabella, "chat_id", chat_id, "lingua")[0][0]
            bot.sendMessage(chat_id, traduttore("Scusami non sono ancora in grado di fare quello che mi hai chiesto", language))

    else:
        """
        In caso gli arrivi qualche cosa che non è in grado di gestire
        """
        if chat_type != 'group':
            language = libreria.selectcondizionato(tabella, "chat_id", chat_id, "lingua")[0][0]
            bot.sendMessage(chat_id, traduttore("Scusami non sono ancora in grado di fare quello che mi hai chiesto", language))


language = 'en-GB'
bot = telepot.Bot(TOKEN)
try:
    bot.sendMessage(chat_id_admin1, "online")
except:
    pass
bot.message_loop(on_chat_message)


while True:
    time.sleep(10)
