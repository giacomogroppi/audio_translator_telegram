import asyncio
import speech_recognition as sr
from googletrans import Translator




#if __name__ == "__main__":
#    import time
#    s = time.perf_counter()
#
#    asyncio.run(main())
#    elapsed = time.perf_counter() - s
#    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
#



async def audio_direct(dst, language):
    """
    Fa la traduzione diretta a google e dopo manda il testo
    """
    if 1:
        r = sr.Recognizer()
        sound = dst
        audio = sr.AudioFile(sound)
        with audio as source:
            audio_content = r.record(source)
                

        testo_tradotto_intero = r.recognize_google(
                                                audio_content, 
                                                language=language,
                                                show_all=True
                                                )

    return testo_tradotto_intero

    try:
        print("")
    except Exception as e:
        """ Error in e """
        pass




async def lingua_ritorno(dst, lingue=None):
    """
    Funzione da eseguire esternamente
    """
    if lingue is None:
        import sys
        sys.exit("Lingue can't be None")
    if not isinstance(lingue, list):
        import sys
        sys.exit("lingua must be a list")
    if not isinstance(dst, str):
        import sys
        sys.exit("dst must be the path of the audio")


    #testo = await asyncio.gather(
    #    audio_direct(dst, "it-IT") 
    #    )

    #nomi_funzioni = []
    #"""
    #Scrittura delle funzioni per poi poterle mandare dentro il gather
    #"""
    #for x in lingue:
    #    nomi_funzioni.append("audio_direct(dst, " + x + ")")
    
    #print(nomi_funzioni)
    
    testo = await asyncio.gather(
        *[audio_direct(dst, x) for x in lingue]
    )

    #lingua = audio_direct(dst, lingue)
    more_confident_parameter = float(0)
    for i, x in enumerate(testo): 
        try:
            if float(x['alternative'][0]['confidence']) > float(more_confident_parameter):
                print("entra") 
                more_confident_parameter = float(x['alternative'][0]['confidence'])
                lingua_affidabile = lingue[i]
        except:
            pass
        
    return lingua_affidabile


def riconoscimento__init(dst=None, lingue = None):
    if dst is None:
        import sys
        sys.exit("You have to set the path of the audio")
        

    if lingue is None or not isinstance(lingue, dict):
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

    lingue_passato = []

    for x in lingue:
        lingue_passato.append(x)
    import time
    x = time.time()
    lingua_affidabile = asyncio.run(lingua_ritorno(dst, lingue_passato))
    
    return lingua_affidabile